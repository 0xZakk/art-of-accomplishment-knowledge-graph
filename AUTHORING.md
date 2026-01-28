# Authoring Guide

Guidelines for creating and linking content in this Zettelkasten.

## Wiki Links Must Include Folder Paths

**Important:** When linking between notes, always include the full folder path in wiki links.

❌ **Wrong:**
```markdown
- [[Purpose is lived in the present moment]]
- [[Doubt is leaving your heart]]
```

✅ **Correct:**
```markdown
- [[literature-notes/purpose-is-lived-in-the-present-moment|Purpose is lived in the present moment]]
- [[literature-notes/doubt-is-leaving-your-heart|Doubt is leaving your heart]]
```

### Format
```
[[folder/filename-slug|Display Text]]
```

- `folder/filename-slug` — path relative to `content/`, without `.md` extension
- `Display Text` — human-readable link text (after the `|`)

### Why?
Quartz resolves wiki links relative to the content root. Without the folder path, links like `[[Purpose is lived]]` will 404 because Quartz looks for `/purpose-is-lived` instead of `/literature-notes/purpose-is-lived-in-the-present-moment`.

## Folder Structure

```
content/
├── index.md                    # Homepage
├── literature-notes/           # Key concepts (atomic ideas)
│   ├── index.md
│   └── [concept-slug].md
├── reference-notes/            # Video summaries + transcripts
│   ├── index.md
│   └── [video-slug].md
└── transcripts/                # Raw transcripts (if separated)
```

## Filename Conventions

- Use lowercase
- Use hyphens for spaces: `purpose-is-lived-in-the-present-moment.md`
- Keep it concise but descriptive
- Match the slugified version of the title

## No H1 Headings in Content

**Important:** Do NOT include an H1 (`# Title`) in your markdown content. Quartz automatically renders the `title` from frontmatter as an H1. Adding another creates duplicate headings.

❌ **Wrong:**
```markdown
---
title: "My Note Title"
---

# My Note Title

Content starts here...
```

✅ **Correct:**
```markdown
---
title: "My Note Title"
---

Content starts here...
```

## Frontmatter

### Literature Notes
```yaml
---
title: "Concept Title"
source: "[[reference-notes/video-slug|Video Title]]"
related:
  - "[[literature-notes/other-concept|Other Concept]]"
tags:
  - tag1
  - tag2
---
```

**Required sections at the bottom of each literature note:**
1. `## Related Concepts` - Links to other literature notes
2. `## Source` - Link back to the reference note this concept came from

```markdown
## Related Concepts

- [[literature-notes/other-concept|Other Concept]] - Brief description

## Source

- [[reference-notes/video-slug|Video Title]]
```

### Reference Notes
```yaml
---
title: "Video Title"
source: https://youtube.com/watch?v=VIDEO_ID
videoId: "VIDEO_ID"
type: coaching-session
duration: "MM:SS"
topics:
  - topic1
  - topic2
date: YYYY-MM-DD
---
```
