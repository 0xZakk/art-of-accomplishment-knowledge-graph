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
