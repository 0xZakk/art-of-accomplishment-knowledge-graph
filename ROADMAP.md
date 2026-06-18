# Zettelkasten Site — UX/Design Roadmap

## Completed
- [x] Rebrand to AOA design system (Poppins font, color palette, custom SCSS)
- [x] Default to light theme
- [x] Remove duplicate headings on index pages
- [x] Remove background highlight from internal links
- [x] Remove dates from all page templates and listings
- [x] Fix squished titles in folder listings (grid layout)
- [x] 1. Topics page — remove duplicate list (hidePageList frontmatter flag)
- [x] 2. Topic pages — rich summaries (600-1200 words) with inline literature note links
- [x] 3. Topic pages — removed explicit literature notes lists; connections through summary text
- [x] 4. Literature notes — stripped summaries from Related Concepts links (1119 files)
- [x] 5. Sidebar — removed scroll/blur on TOC and Backlinks (full natural height)
- [x] 6. Literature Notes index — removed categorized lists
- [x] 7. Tags page — styled tag headers + added intro paragraph
- [x] 8. Reference notes — categorized all 295 videos (108 podcast, 95 lesson, 87 coaching, 5 guest)
- [x] 9. Graph view — increased spacing/repulsion, hover-only labels
- [x] 10. Home page — full redesign (no sidebars, expanded intro, about sections, embedded graph, courses)

## Blocked
- **Transcript reformatting** — Pipeline built (whisper + pyannote diarization), blocked on YouTube 403s. Ready to run when yt-dlp fixes land.

## Future
- Deploy to production (Vercel/Netlify/GitHub Pages) — DONE (Netlify)
- Ongoing maintenance (process new videos as they come out)
- Re-enable OG image generation before production
- Semantic reference note linking per topic (embeddings-based, deferred)

## Graph RAG / Conversational Interface
Build a Graph RAG interface on top of the knowledge graph so users can query Joe Hudson's teachings in natural language.

**What it does:**
- User asks a question (e.g. "What does Joe say about anger and boundaries?")
- System searches the graph for relevant teachings, literature notes, and reference notes
- Returns a synthesized answer with source citations linking back to specific content

**Why it matters:**
- Mattia mentioned this as a potential lead magnet with email gate for AOA (2026-02-25 kickoff meeting)
- Came up again in the 2026-02-20 knowledge graph exploration call with an AOA community member
- The graph already has ~1,248 teachings mapped across 296 sources — the data is ready

**TODO:**
- [ ] Research Graph RAG architectures (Neo4j + vector embeddings vs. direct semantic search over existing content)
- [ ] Prototype: build a simple query interface that searches the zettelkasten content and returns sourced answers
- [ ] Design email-gated landing page for AOA to use as lead magnet
- [ ] Draft one-pager describing the graph's contents and potential uses (for Mattia/Mark to evaluate)
- [ ] Explore whether this could be a standalone product vs. embedded in the AOA site
