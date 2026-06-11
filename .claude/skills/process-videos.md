---
name: process-videos
description: Check for new AOA YouTube videos and process any that are missing into source + teaching pages with semantic backlinks
user_invocable: true
---

# Process New Videos

Check the Art of Accomplishment YouTube channel for new videos that haven't been added to the knowledge base yet, then process them.

## Prerequisites

Before running, verify:
1. `yt-dlp --version` should return a version
2. Python dependencies installed (`pip install -r requirements.txt`)

If any prerequisite is missing, tell the user what they need to do and stop.

## Steps

### 1. Check for new videos

Run the RSS checker:

```bash
python tools/check_rss.py
```

This compares the AOA YouTube RSS feed against existing source pages in `content/sources/`. Report:
- How many videos are in the feed
- How many already have source pages
- Which specific videos are new (title + URL)

If there are no new videos, tell the user and stop.

### 2. Confirm with user

List the new videos and ask the user to confirm they want to process all of them, or let them pick specific ones.

### 3. Fetch transcripts

For each video to process, run:

```bash
python tools/process_video.py <VIDEO_URL>
```

This fetches the transcript via yt-dlp auto-captions, saves it to `transcripts/`, and outputs video metadata (title, duration, date).

### 4. Generate content

For each video, read the transcript and generate:

**Source page** (`content/sources/SLUG.md`):
- Follow the format in AGENTS.md exactly
- Include frontmatter (title, source URL, videoId, type, duration, category, topics, date)
- Include iframe embed, Summary (2-4 paragraphs), Key Concepts (wiki links to teachings), Key Quotes (4-8), full Transcript
- type values: coaching-session, short-lesson, podcast
- Do NOT add an H1 heading

**Teaching pages** (`content/teachings/SLUG.md`):
- Extract 3-8 atomic teachings from the source (fewer for very short videos)
- Each title should be a complete sentence expressing one insight
- Include frontmatter (title, source wiki link, related wiki links, tags)
- Body: 2-4 paragraphs, include a pull quote
- Sections: Related Concepts, Source
- Search existing teachings for related concepts to cross-link
- Do NOT add an H1 heading

### 5. Run semantic backlinks

After all videos are processed, regenerate embeddings and apply backlinks:

```bash
python tools/semantic_links.py embed
python tools/semantic_links.py apply --threshold 0.75 --top-n 5 --write
```

### 6. Commit and push

After all content is generated and backlinks applied, commit and push the changes:

1. Stage the new/modified files: `git add content/ transcripts/ tools/data/metadata.json`
2. Create a commit with a message like: `add: process N new videos (video-title-1, video-title-2)`
3. Push to the remote: `git push`

This ensures other contributors won't re-process the same videos.

### 7. Summary

Report what was created and that the changes have been pushed.
