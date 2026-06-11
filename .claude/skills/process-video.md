---
name: process-video
description: Process a single YouTube video URL into source + teaching pages with semantic backlinks
user_invocable: true
---

# Process a Single Video

Process one YouTube video into the knowledge base.

## Arguments

The user should provide a YouTube URL or video ID as the argument. Examples:
- `/process-video https://www.youtube.com/watch?v=VIDEO_ID`
- `/process-video VIDEO_ID`

If no URL is provided, ask the user for one.

## Prerequisites

Before running, verify:
1. `yt-dlp --version` returns a version
2. Python dependencies installed (`pip install -r requirements.txt`)

If any prerequisite is missing, tell the user what they need to do and stop.

## Steps

### 1. Check if already processed

Search `content/sources/` for the video ID:

```bash
grep -r "VIDEO_ID" content/sources/ -l
```

If found, tell the user this video has already been processed.

### 2. Fetch transcript and metadata

```bash
python tools/process_video.py <URL_OR_ID>
```

This fetches the transcript via yt-dlp, saves it, and outputs metadata (title, duration, date).

### 3. Generate source page

Read the transcript from `transcripts/VIDEO_ID_clean.txt` and create `content/sources/SLUG.md`:

- Follow the format in AGENTS.md exactly
- Include frontmatter (title, source URL, videoId, type, duration, category, topics, date)
- Include iframe embed, Summary (2-4 paragraphs), Key Concepts (wiki links to teachings), Key Quotes (4-8), full Transcript
- type: coaching-session | short-lesson | podcast
- Do NOT add an H1 heading

### 4. Generate teaching pages

Extract 3-8 atomic teachings (fewer for short videos). For each, create `content/teachings/SLUG.md`:

- Title as a complete sentence expressing one insight
- Frontmatter: title, source (wiki link), related (wiki links to existing teachings), tags
- Body: 2-4 paragraphs, include a pull quote
- Sections: Related Concepts, Source
- Search existing teachings for cross-links: `grep -r "KEYWORD" content/teachings/ -l`
- Do NOT add an H1 heading

### 5. Run semantic backlinks

```bash
python tools/semantic_links.py embed
python tools/semantic_links.py apply --threshold 0.75 --top-n 5 --write
```

### 6. Commit and push

After content is generated and backlinks applied, commit and push the changes:

1. Stage the new/modified files: `git add content/ transcripts/ tools/data/metadata.json`
2. Create a commit with a message like: `add: process "Video Title"`
3. Push to the remote: `git push`

This ensures other contributors won't re-process the same video.

### 7. Report results

List the files created and confirm the changes have been pushed.
