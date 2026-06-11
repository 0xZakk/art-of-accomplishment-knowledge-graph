#!/usr/bin/env python3
"""
AOA Video Transcript Fetcher

Fetches transcripts and metadata for YouTube videos via yt-dlp.
Content generation (source pages, teaching pages) is handled by Claude Code.

Usage:
    python tools/process_video.py https://www.youtube.com/watch?v=VIDEO_ID
    python tools/process_video.py VIDEO_ID
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CONTENT_DIR = REPO_ROOT / "content"
SOURCES_DIR = CONTENT_DIR / "sources"
TRANSCRIPTS_DIR = REPO_ROOT / "transcripts"


# ---------------------------------------------------------------------------
# Transcript fetching
# ---------------------------------------------------------------------------

def extract_video_id(url_or_id: str) -> str:
    """Extract YouTube video ID from URL or return as-is if already an ID."""
    patterns = [
        r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})",
        r"^([A-Za-z0-9_-]{11})$",
    ]
    for pattern in patterns:
        m = re.search(pattern, url_or_id)
        if m:
            return m.group(1)
    raise ValueError(f"Cannot extract video ID from: {url_or_id}")


def clean_vtt(vtt_text: str) -> str:
    """Strip VTT timestamps and deduplicate lines into clean transcript text."""
    lines = []
    seen = set()
    for line in vtt_text.splitlines():
        line = line.strip()
        if not line or line.startswith("WEBVTT") or "-->" in line or re.match(r"^\d+$", line):
            continue
        line = re.sub(r"<[^>]+>", "", line).strip()
        if line and line not in seen:
            seen.add(line)
            lines.append(line)
    return " ".join(lines)


def clean_txt(txt: str) -> str:
    """Clean a plain text transcript (remove extra whitespace)."""
    txt = re.sub(r"[\[\(]\d{2}:\d{2}:\d{2}[\]\)]", "", txt)
    txt = re.sub(r"\s+", " ", txt)
    return txt.strip()


def fetch_auto_captions(video_id: str) -> str | None:
    """Try to get auto-generated captions via yt-dlp. Returns clean text or None."""
    with tempfile.TemporaryDirectory() as tmpdir:
        outpath = Path(tmpdir) / video_id
        cmd = [
            "yt-dlp",
            "--write-auto-sub",
            "--skip-download",
            "--sub-lang", "en",
            "--sub-format", "vtt",
            "--no-warnings",
            "-o", str(outpath),
            f"https://www.youtube.com/watch?v={video_id}",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  yt-dlp failed: {result.stderr[:200]}", file=sys.stderr)
            return None

        vtt_files = list(Path(tmpdir).glob("*.vtt"))
        if not vtt_files:
            print("  No VTT file found after yt-dlp run.", file=sys.stderr)
            return None

        vtt_text = vtt_files[0].read_text(encoding="utf-8")
        return clean_vtt(vtt_text)


def get_transcript(video_id: str) -> str:
    """
    Get transcript for a video. Priority:
    1. Existing file in transcripts/
    2. yt-dlp auto-captions
    """
    for suffix in [".txt", ".en.vtt", "_clean.txt"]:
        candidate = TRANSCRIPTS_DIR / f"{video_id}{suffix}"
        if candidate.exists():
            text = candidate.read_text(encoding="utf-8")
            if suffix.endswith(".vtt"):
                return clean_vtt(text)
            return clean_txt(text)

    print(f"  Fetching auto-captions for {video_id}...")
    transcript = fetch_auto_captions(video_id)
    if transcript:
        TRANSCRIPTS_DIR.mkdir(exist_ok=True)
        (TRANSCRIPTS_DIR / f"{video_id}.en.vtt").write_text(transcript, encoding="utf-8")
        return transcript

    raise RuntimeError(f"Could not get transcript for {video_id}. Check yt-dlp.")


# ---------------------------------------------------------------------------
# Video metadata
# ---------------------------------------------------------------------------

def get_video_metadata(video_id: str) -> dict:
    """Fetch video title, duration, upload date via yt-dlp."""
    cmd = [
        "yt-dlp",
        "--no-warnings",
        "--skip-download",
        "--print", "%(title)s\t%(duration_string)s\t%(upload_date)s\t%(description)s",
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"title": video_id, "duration": "??:??", "date": datetime.now().strftime("%Y-%m-%d"), "description": ""}

    parts = result.stdout.strip().split("\t", 3)
    title = parts[0] if len(parts) > 0 else video_id
    duration = parts[1] if len(parts) > 1 else "??:??"
    raw_date = parts[2] if len(parts) > 2 else ""
    description = parts[3] if len(parts) > 3 else ""

    if raw_date and len(raw_date) == 8:
        date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
    else:
        date = datetime.now().strftime("%Y-%m-%d")

    return {"title": title, "duration": duration, "date": date, "description": description}


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Convert text to a filesystem-safe slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def source_slug_exists(video_id: str) -> str | None:
    """Check if a source page for this video ID already exists. Returns slug or None."""
    for f in SOURCES_DIR.glob("*.md"):
        content = f.read_text(encoding="utf-8")
        if f'videoId: "{video_id}"' in content or f"videoId: '{video_id}'" in content:
            return f.stem
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Fetch transcript and metadata for an AOA YouTube video.")
    parser.add_argument("video", help="YouTube URL or video ID")
    args = parser.parse_args()

    video_id = extract_video_id(args.video)
    print(f"Processing video: {video_id}")

    # Check if already processed
    existing = source_slug_exists(video_id)
    if existing:
        print(f"  Source page already exists: content/sources/{existing}.md")
        return

    # Get metadata
    print("  Fetching video metadata...")
    meta = get_video_metadata(video_id)
    print(f"  Title: {meta['title']}")
    print(f"  Duration: {meta['duration']}")
    print(f"  Date: {meta['date']}")

    # Get transcript
    print("  Getting transcript...")
    transcript = get_transcript(video_id)
    word_count = len(transcript.split())
    print(f"  Transcript: {word_count} words")

    # Save clean transcript
    TRANSCRIPTS_DIR.mkdir(exist_ok=True)
    clean_path = TRANSCRIPTS_DIR / f"{video_id}_clean.txt"
    clean_path.write_text(transcript, encoding="utf-8")
    print(f"  Saved: transcripts/{video_id}_clean.txt")

    # Output metadata as JSON for Claude Code to consume
    output = {
        "video_id": video_id,
        "title": meta["title"],
        "duration": meta["duration"],
        "date": meta["date"],
        "transcript_path": str(clean_path),
        "word_count": word_count,
    }
    print(f"\n--- METADATA ---")
    print(json.dumps(output, indent=2))
    print(f"--- END METADATA ---")
    print(f"\nTranscript fetched. Use Claude Code to generate source and teaching pages.")


if __name__ == "__main__":
    main()
