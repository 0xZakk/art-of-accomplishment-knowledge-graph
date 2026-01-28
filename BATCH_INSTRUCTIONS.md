# Batch Processing Instructions

## Pipeline for each video

### 1. Download transcript
```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download --sub-format vtt \
  -o "~/dev/joe-hudson-zettelkasten-site/transcripts/%(id)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 2. Parse the VTT transcript
Read the .en.vtt file. Strip VTT headers and timestamps to get plain text. Deduplicate repeated lines (VTT often repeats lines across cues).

### 3. Create Reference Note
Save to `~/dev/joe-hudson-zettelkasten-site/content/reference-notes/SLUG.md`

**Slug:** Lowercase, hyphenated version of the title (short, max ~6 words from title).

**Format:**
```markdown
---
title: "VIDEO TITLE"
source: https://www.youtube.com/watch?v=VIDEO_ID
videoId: "VIDEO_ID"
type: TYPE
duration: "M:SS"
topics:
  - topic1
  - topic2
date: 2026-01-27
---

<iframe width="560" height="315" src="https://www.youtube.com/embed/VIDEO_ID" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Summary

2-3 paragraph summary of the video content.

## Key Concepts

- [[literature-notes/SLUG|Concept title]]

Create ONE literature note per distinct idea, concept, tool, or teaching. The number depends entirely on the content — a 5-minute video with one core idea gets 1 note. A 30-minute coaching session might have 8. A 3-hour deep dive could have 20+. Let the content dictate the count. Don't force a minimum or cap at a maximum.

## Key Quotes

> "Notable quote from the transcript"
(3-6 quotes)

## Transcript

Full cleaned transcript text.
```

**Type values:** "teaching" for solo videos, "coaching-session" for coaching, "interview" for interviews/conversations.

### 4. Create Literature Notes
For each key concept identified, save to `~/dev/joe-hudson-zettelkasten-site/content/literature-notes/SLUG.md`

**Format:**
```markdown
---
title: "Concept as a statement"
source: "[[reference-notes/REF-SLUG|Video Title]]"
related:
  - "[[literature-notes/OTHER-SLUG|Other concept]]"
tags:
  - tag1
  - tag2
---

Explanation of the concept in 2-4 paragraphs. Include relevant quotes from the transcript.

## Related Concepts

- [[literature-notes/OTHER-SLUG|Other concept]] - Brief description

## Source

- [[reference-notes/REF-SLUG|Video Title]]
```

### 5. Cross-linking
- Related concepts should link to OTHER literature notes (including ones from previous batches)
- Check existing literature notes in content/literature-notes/ for potential connections
- Use FULL paths in wiki links: `[[literature-notes/slug|Display Text]]`

## IMPORTANT
- Do NOT include H1 headings in content (title comes from frontmatter)
- Duration format: "M:SS" (calculate from the seconds value in the video list - 3rd field)
- If transcript download fails, skip that video and note it
- Do NOT duplicate existing notes - check first
