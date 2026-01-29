#!/usr/bin/env python3
"""
Transcript Reformatter Pipeline
Downloads audio, runs whisper transcription + speaker diarization,
then updates reference notes with formatted transcripts.

Usage:
  python tools/reformat_transcripts.py run          # Process all unformatted notes
  python tools/reformat_transcripts.py run --limit 5 # Process first 5 only (test)
  python tools/reformat_transcripts.py status        # Check progress
  python tools/reformat_transcripts.py preview <slug> # Preview a single note

Progress is saved to tools/data/reformat_progress.json so it can resume.
"""

import os
import re
import sys
import json
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# Setup
PROJECT_DIR = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_DIR / "content" / "reference-notes"
AUDIO_DIR = PROJECT_DIR / "audio"
DATA_DIR = PROJECT_DIR / "tools" / "data"
PROGRESS_FILE = DATA_DIR / "reformat_progress.json"
LOG_FILE = DATA_DIR / "reformat.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def load_progress():
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"completed": [], "failed": [], "skipped": []}


def save_progress(progress):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


def get_reference_notes():
    """Get all reference notes with their video IDs and types."""
    notes = []
    for f in sorted(CONTENT_DIR.glob("*.md")):
        if f.stem in ("index", "_index"):
            continue
        text = f.read_text(encoding="utf-8")

        video_id_match = re.search(r'videoId:\s*"(.+)"', text)
        if not video_id_match:
            continue

        video_id = video_id_match.group(1)
        type_match = re.search(r'type:\s*(\S+)', text)
        video_type = type_match.group(1) if type_match else "teaching"

        # Check if already formatted (has speaker labels)
        has_speakers = bool(re.search(r'^\*\*\w+', text, re.MULTILINE))

        notes.append({
            "slug": f.stem,
            "path": str(f),
            "video_id": video_id,
            "type": video_type,
            "already_formatted": has_speakers,
        })
    return notes


def download_audio(video_id):
    """Download audio from YouTube."""
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    output_path = AUDIO_DIR / f"{video_id}.wav"

    if output_path.exists():
        log.info(f"Audio already exists: {video_id}")
        return str(output_path)

    log.info(f"Downloading audio: {video_id}")
    result = subprocess.run(
        [
            "yt-dlp",
            "-x",
            "--audio-format", "wav",
            "--audio-quality", "0",
            "-o", str(AUDIO_DIR / f"{video_id}.%(ext)s"),
            f"https://www.youtube.com/watch?v={video_id}",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        log.error(f"Download failed for {video_id}: {result.stderr}")
        return None

    if output_path.exists():
        return str(output_path)

    # yt-dlp might output with different extension before conversion
    for ext in ["wav", "m4a", "webm", "opus"]:
        alt = AUDIO_DIR / f"{video_id}.{ext}"
        if alt.exists():
            # Convert to wav
            subprocess.run(
                ["ffmpeg", "-i", str(alt), "-ar", "16000", "-ac", "1", str(output_path), "-y"],
                capture_output=True,
            )
            if output_path.exists():
                alt.unlink()
                return str(output_path)

    log.error(f"Audio file not found after download: {video_id}")
    return None


def transcribe_and_diarize(audio_path, video_type):
    """Run faster-whisper transcription and pyannote diarization."""
    from faster_whisper import WhisperModel
    from pyannote.audio import Pipeline
    import torch

    log.info(f"Transcribing: {audio_path}")

    # Transcribe with faster-whisper
    model = WhisperModel("medium", device="cpu", compute_type="int8")
    segments_raw, info = model.transcribe(audio_path, beam_size=5, word_timestamps=True)
    segments = list(segments_raw)

    log.info(f"Transcription done. Language: {info.language}, Duration: {info.duration:.0f}s")

    # Diarize with pyannote
    log.info("Running speaker diarization...")
    hf_token = os.environ.get("HF_TOKEN", "")
    if not hf_token:
        token_file = PROJECT_DIR / ".env.hf"
        if token_file.exists():
            hf_token = token_file.read_text().strip()

    diarize_pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        token=hf_token,
    )

    if torch.backends.mps.is_available():
        diarize_pipeline.to(torch.device("mps"))

    diarization = diarize_pipeline(audio_path)

    # Build speaker timeline
    speaker_turns = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        speaker_turns.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker,
        })

    log.info(f"Diarization found {len(speaker_turns)} speaker turns")

    # Merge transcription segments with speaker info
    result = []
    for seg in segments:
        mid = (seg.start + seg.end) / 2
        speaker = "Unknown"
        for turn in speaker_turns:
            if turn["start"] <= mid <= turn["end"]:
                speaker = turn["speaker"]
                break
        result.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text.strip(),
            "speaker": speaker,
        })

    return result, speaker_turns


def format_transcript(segments, video_type):
    """Format segments into readable transcript with speaker labels."""
    if not segments:
        return ""

    # Figure out who is who - SPEAKER_00 is usually Joe (most speaking time)
    speaker_time = {}
    for seg in segments:
        sp = seg["speaker"]
        dur = seg["end"] - seg["start"]
        speaker_time[sp] = speaker_time.get(sp, 0) + dur

    # Sort by speaking time
    sorted_speakers = sorted(speaker_time.items(), key=lambda x: -x[1])

    # Map speaker IDs to names
    speaker_map = {}
    if video_type == "teaching":
        # Solo - just Joe
        for sp, _ in sorted_speakers:
            speaker_map[sp] = "Joe"
    elif video_type == "coaching-session":
        # Joe + caller(s)
        if sorted_speakers:
            speaker_map[sorted_speakers[0][0]] = "Joe"
        for sp, _ in sorted_speakers[1:]:
            speaker_map[sp] = "Caller"
    elif video_type == "interview":
        if sorted_speakers:
            speaker_map[sorted_speakers[0][0]] = "Joe"
        for i, (sp, _) in enumerate(sorted_speakers[1:]):
            speaker_map[sp] = f"Guest" if len(sorted_speakers) <= 3 else f"Speaker {i+2}"
    else:
        for sp, _ in sorted_speakers:
            speaker_map[sp] = sp

    speaker_map["Unknown"] = "Unknown"

    # Group consecutive segments by speaker into paragraphs
    paragraphs = []
    current_speaker = None
    current_texts = []

    for seg in segments:
        speaker = speaker_map.get(seg["speaker"], seg["speaker"])
        if speaker != current_speaker:
            if current_texts:
                paragraphs.append((current_speaker, " ".join(current_texts)))
            current_speaker = speaker
            current_texts = [seg["text"]]
        else:
            current_texts.append(seg["text"])

    if current_texts:
        paragraphs.append((current_speaker, " ".join(current_texts)))

    # Format output
    lines = []
    unique_speakers = set(speaker_map.values()) - {"Unknown"}

    if len(unique_speakers) <= 1:
        # Solo - just paragraphs, no speaker labels needed
        for speaker, text in paragraphs:
            lines.append(text)
            lines.append("")
    else:
        # Multi-speaker - add labels
        for speaker, text in paragraphs:
            lines.append(f"**{speaker}:** {text}")
            lines.append("")

    return "\n".join(lines).strip()


def update_reference_note(slug, formatted_transcript):
    """Replace the transcript section in the reference note."""
    filepath = CONTENT_DIR / f"{slug}.md"
    content = filepath.read_text(encoding="utf-8")

    # Find and replace transcript section
    transcript_pattern = r'(## Transcript\n\n)(.*?)(\n## |\Z)'
    match = re.search(transcript_pattern, content, re.DOTALL)

    if match:
        new_content = content[:match.start()] + match.group(1) + formatted_transcript + "\n" + (match.group(3) if match.group(3).startswith("\n## ") else "")
        filepath.write_text(new_content, encoding="utf-8")
        return True
    else:
        log.warning(f"No transcript section found in {slug}")
        return False


def process_one(note, dry_run=False):
    """Process a single reference note."""
    slug = note["slug"]
    video_id = note["video_id"]
    video_type = note["type"]

    log.info(f"Processing: {slug} (type={video_type}, id={video_id})")

    # Download audio
    audio_path = download_audio(video_id)
    if not audio_path:
        return "failed", "download_failed"

    # Transcribe + diarize
    try:
        segments, speaker_turns = transcribe_and_diarize(audio_path, video_type)
    except Exception as e:
        log.error(f"Transcription failed for {slug}: {e}")
        return "failed", str(e)

    # Format
    formatted = format_transcript(segments, video_type)

    if dry_run:
        print(f"\n{'='*60}")
        print(f"PREVIEW: {slug}")
        print(f"{'='*60}")
        print(formatted[:2000])
        print("...")
        return "preview", None

    # Update file
    if update_reference_note(slug, formatted):
        log.info(f"Updated: {slug}")
        return "completed", None
    else:
        return "failed", "no_transcript_section"


def cmd_run(limit=None):
    """Run the full pipeline."""
    progress = load_progress()
    notes = get_reference_notes()

    # Filter to unformatted, not yet processed
    done_set = set(progress["completed"] + progress["failed"] + progress["skipped"])
    to_process = [n for n in notes if not n["already_formatted"] and n["slug"] not in done_set]

    if limit:
        to_process = to_process[:limit]

    log.info(f"Total notes: {len(notes)}")
    log.info(f"Already formatted: {sum(1 for n in notes if n['already_formatted'])}")
    log.info(f"Already processed: {len(done_set)}")
    log.info(f"To process: {len(to_process)}")

    for i, note in enumerate(to_process, 1):
        log.info(f"[{i}/{len(to_process)}] {note['slug']}")
        try:
            status, error = process_one(note)
            if status == "completed":
                progress["completed"].append(note["slug"])
            elif status == "failed":
                progress["failed"].append(note["slug"])
                log.error(f"Failed: {note['slug']} - {error}")
        except Exception as e:
            progress["failed"].append(note["slug"])
            log.error(f"Exception processing {note['slug']}: {e}")

        save_progress(progress)

        # Clean up audio to save disk space
        audio_file = AUDIO_DIR / f"{note['video_id']}.wav"
        if audio_file.exists():
            audio_file.unlink()

    log.info(f"Done! Completed: {len(progress['completed'])}, Failed: {len(progress['failed'])}")


def cmd_status():
    """Show progress."""
    progress = load_progress()
    notes = get_reference_notes()
    formatted = sum(1 for n in notes if n["already_formatted"])

    print(f"Total reference notes: {len(notes)}")
    print(f"Already formatted (pre-existing): {formatted}")
    print(f"Completed by pipeline: {len(progress['completed'])}")
    print(f"Failed: {len(progress['failed'])}")
    print(f"Remaining: {len(notes) - formatted - len(progress['completed']) - len(progress['failed'])}")

    if progress["failed"]:
        print(f"\nFailed notes:")
        for s in progress["failed"]:
            print(f"  - {s}")


def cmd_preview(slug):
    """Preview a single note."""
    notes = get_reference_notes()
    note = next((n for n in notes if n["slug"] == slug), None)
    if not note:
        print(f"Note not found: {slug}")
        return
    process_one(note, dry_run=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "run":
        limit = None
        for i, arg in enumerate(sys.argv):
            if arg == "--limit" and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
        cmd_run(limit=limit)
    elif cmd == "status":
        cmd_status()
    elif cmd == "preview":
        if len(sys.argv) < 3:
            print("Usage: reformat_transcripts.py preview <slug>")
            sys.exit(1)
        cmd_preview(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
