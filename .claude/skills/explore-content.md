---
name: explore-content
description: Search, browse, and repurpose content from the AOA knowledge base — find teachings, discover themes, generate social content
user_invocable: true
---

# Explore Content

Help the user search, browse, and repurpose content from the knowledge base.

## What you can do

Ask the user what they're looking for. Common use cases:

### Search for teachings on a topic

Search across teachings and sources:

```bash
grep -r "QUERY" content/teachings/ -l
grep -r "QUERY" content/sources/ -l
```

Read the matching files and summarize the key insights found.

### Find related concepts

If embeddings exist (`tools/data/embeddings.npz`), use semantic search:

```bash
python tools/semantic_links.py inspect <teaching-slug>
```

This shows the most semantically similar teachings to a given one.

### Browse by topic

The curated topic pages in `content/topics/` group teachings by theme:
- anger, emotions, fear, leadership, presence, purpose-and-meaning, relationships, self-awareness, shame

Read the relevant topic page to give the user an overview.

### Find backlinks

To see everything that links to a specific teaching:

```bash
grep -r "teachings/SLUG" content/ -l
```

### Discover themes and patterns

```bash
# Count teachings per tag
grep -rh "^  - " content/teachings/*.md | sort | uniq -c | sort -rn | head -30

# Find teachings from a specific source
grep -r "sources/SOURCE_SLUG" content/teachings/ -l
```

### Repurpose content for social media

When the user wants to create social content from teachings:

1. Read the teaching file
2. Identify the sharpest insight (usually the title + first paragraph)
3. Find the best quote from the linked source

**Formats that work well for AOA content:**
- **Reframe:** "Most people think X. Joe Hudson argues Y." (2-3 lines)
- **Insight chain:** 4-6 bullets building to a surprising conclusion
- **Quote + context:** Strong quote, then 1-2 sentences explaining why it matters

**Voice guidelines:**
- Plain, direct — no corporate jargon
- Concrete examples over abstract principles
- The counterintuitive take is usually the interesting one
- Joe's framing: feelings → nervous system → patterns → freedom
