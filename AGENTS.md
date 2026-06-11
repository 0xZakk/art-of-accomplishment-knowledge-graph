# AGENTS.md — AOA Knowledge Base

Instructions for Claude Code (or any LLM agent) working with this repository.

## What This Repo Is

A plain-markdown zettelkasten of Joe Hudson's teachings from the Art of Accomplishment YouTube channel.

- `content/sources/` — one file per video (summary, transcript, quotes, linked teachings)
- `content/teachings/` — atomic concept notes, one idea per file, cross-linked
- `content/topics/` — curated theme pages grouping related teachings
- `tools/` — Python processing pipeline
- `transcripts/` — raw transcript files

There is no build step. Pure markdown.

---

## Skills

### 1. Create a Source Page from a Transcript

**When to use:** You have a YouTube video URL and want to add it to the knowledge base.

**Steps:**

1. Fetch the transcript:
   ```bash
   python tools/process_video.py VIDEO_URL
   ```
   This uses `yt-dlp` to fetch auto-captions and saves a clean transcript to `transcripts/`.

2. Create `content/sources/SLUG.md` following this format exactly:

```yaml
---
title: "Video Title"
source: https://www.youtube.com/watch?v=VIDEO_ID
videoId: "VIDEO_ID"
type: coaching-session
duration: "MM:SS"
category: "Coaching Session"
topics:
  - emotions
  - self-awareness
date: YYYY-MM-DD
---

<iframe width="560" height="315" src="https://www.youtube.com/embed/VIDEO_ID" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Summary

[2-4 paragraph summary of the video's core content]

## Key Concepts

- [[teachings/teaching-slug|Teaching title as sentence]]
- [[teachings/another-slug|Another teaching]]

## Key Quotes

> "Direct quote from the transcript."

> "Another quote."

## Transcript

[Full cleaned transcript text]
```

**Frontmatter `type` values:**
- `coaching-session` — live coaching with a participant
- `short-lesson` — Joe speaking directly to camera
- `podcast` — podcast episode or interview

**Slug convention:** lowercase, hyphens, short but descriptive. Example: `what-blocks-your-love.md`

---

### 2. Create Teaching Pages from a Source

**When to use:** You have a source page and want to extract atomic concept notes.

**Goal:** Identify 3–8 distinct teachings from the source. Each should be:
- A standalone atomic idea expressible as a single sentence (the title)
- 2–4 paragraphs elaborating the concept in plain prose
- Cross-linked to related teachings that already exist

**Format:**

```yaml
---
title: "The key insight expressed as a complete sentence"
source: "[[sources/source-slug|Source Title]]"
related:
  - "[[teachings/related-slug|Related Teaching Title]]"
tags:
  - tag1
  - tag2
---

Body: 2-4 paragraphs. Write in third person, e.g. "Joe argues that..." or directly state the insight.
Include a pull quote if there's a strong one from the source.

> "Quote from the video."

## Related Concepts

- [[teachings/related-slug|Related Teaching Title]]
- [[teachings/another-slug|Another Teaching]]

## Source

- [[sources/source-slug|Source Title]]
```

**Finding related teachings:**
- Search existing teachings for conceptually similar ideas:
  ```bash
  grep -r "KEYWORD" content/teachings/ -l
  ```
- Run semantic search:
  ```bash
  python tools/semantic_links.py inspect SLUG
  ```

**Slug convention:** Slugify the title. "Acceptance is not love" → `acceptance-is-not-love.md`

---

### 3. Run the Semantic Backlink Pipeline

**When to use:** After adding new teachings, to find and add cross-links.

```bash
# Generate embeddings for all teachings
python tools/semantic_links.py embed

# Preview connections above threshold
python tools/semantic_links.py report --threshold 0.75

# Inspect connections for a specific teaching
python tools/semantic_links.py inspect SLUG

# Apply top-5 connections to all files
python tools/semantic_links.py apply --threshold 0.75 --top-n 5
```

Uses `sentence-transformers` with `BAAI/bge-base-en-v1.5` locally (no API key needed for embeddings).

---

### 4. Full Pipeline: Video URL → Source + Teachings + Backlinks

Use the `/process-video` or `/process-videos` Claude Code skill, which will:
1. Fetch transcript + metadata via `yt-dlp` (`python tools/process_video.py URL`)
2. Generate a source page (Claude Code writes the markdown)
3. Generate 3–8 teaching pages (Claude Code writes the markdown)
4. Run semantic similarity and add backlinks (`python tools/semantic_links.py embed && apply`)

---

### 5. Content Theme Discovery

Find patterns and themes across teachings:

```bash
# Search for teachings mentioning a concept
grep -r "CONCEPT" content/teachings/ -l | wc -l

# List all tags used
grep -h "^  - " content/teachings/*.md | sort | uniq -c | sort -rn | head -30

# Find teachings from a specific source
grep -r "sources/SOURCE_SLUG" content/teachings/ -l
```

Topics are curated manually in `content/topics/`. To add a new topic page, create `content/topics/TOPIC.md` following the format in existing topic files.

---

### 6. Generate Social Content from Teachings

**When to use:** Creating tweets, LinkedIn posts, or newsletter content from a teaching.

**Process:**
1. Read the teaching file
2. Identify the sharpest insight (usually the title + first paragraph)
3. Find the best quote from the source

**Tweet formats that work well for AOA content:**
- **Reframe:** "Most people think X. Joe Hudson argues Y." (2-3 lines)
- **Insight chain:** 4-6 bullets building to a surprising conclusion
- **Quote + context:** Strong quote, then 1-2 sentences explaining why it matters

**Voice notes:**
- Plain, direct — no corporate jargon
- Concrete examples over abstract principles
- The counterintuitive take is usually the interesting one
- Joe's framing: feelings → nervous system → patterns → freedom

---

### 7. Browse and Search the Slipbox

```bash
# Full-text search
grep -r "QUERY" content/ -l

# Search only teachings
grep -r "QUERY" content/teachings/ -l

# Search only sources
grep -r "QUERY" content/sources/ -l

# Find backlinks to a specific teaching
grep -r "teachings/SLUG" content/ -l

# Count teachings per topic tag
grep -rh "^  - " content/teachings/*.md | sort | uniq -c | sort -rn
```

---

## Conventions

### Wiki Links
Always include the folder path:
```
[[teachings/slug|Display Title]]
[[sources/slug|Display Title]]
```

Never bare links like `[[slug]]` — they won't resolve correctly.

### Titles
- Teaching titles are complete sentences expressing the insight: "Acceptance is not love"
- Source titles are video titles: "What Blocks Your Love?"

### No H1 in Content
Do not add `# Title` headings — the frontmatter `title` field is the heading.

### Tags vs Topics
- `tags` in frontmatter — granular concepts (used for search/filtering)
- `topics` in frontmatter on sources — high-level theme categories (matches `content/topics/` files)

---

## Environment

```bash
pip install -r requirements.txt
```

No API keys required:
- `tools/process_video.py` — fetches transcripts via `yt-dlp` (free auto-captions)
- `tools/semantic_links.py` — uses `sentence-transformers` locally (BAAI/bge-base-en-v1.5)
- Content generation is done by Claude Code directly
