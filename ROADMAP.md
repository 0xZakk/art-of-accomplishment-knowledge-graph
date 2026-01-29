# Zettelkasten Site — UX/Design Roadmap

## ✅ Completed
- [x] Rebrand to AOA design system (Poppins font, color palette, custom SCSS)
- [x] Default to light theme
- [x] Remove duplicate headings on index pages
- [x] Remove background highlight from internal links
- [x] Remove dates from all page templates and listings
- [x] Fix squished titles in folder listings (grid layout)

## 🔲 Remaining

### 1. Topics page — remove duplicate list
The folder content template auto-generates a list that duplicates the hand-written topic list in the body content. Investigate why both appear and keep only the body content list with descriptions.

### 2. Topic pages — rich summaries (600-1200 words)
For each topic page, read its related literature notes and generate a comprehensive summary of Joe Hudson's ideas, concepts, experiments, and teachings. Summaries should be 600-1200 words (depending on volume of lit notes) and inline-link to the relevant literature notes throughout the text.

### 3. Topic pages — semantic reference note linking
Use embeddings (same approach as the lit note cross-linking) to find reference notes above a similarity threshold for each topic. Add a "Related Videos" section with those links. Remove the explicit literature notes list/heading — literature notes are now connected through the summary text in item #2.

### 4. Literature notes — strip summaries from Related Concepts
Remove short descriptions after links in the Related Concepts section. For example, change:
- `Searching for purpose avoids it - The search itself is the avoidance mechanism`
to just:
- `Searching for purpose avoids it`

### 5. Sidebar — remove scroll/blur on TOC and Backlinks
Make the right sidebar sections (Table of Contents, Backlinks) take up their full natural height. No max-height, no overflow scroll, no fade/blur effect.

### 6. Literature Notes index — remove categorized lists
Strip the categorized headings (Purpose & Meaning, Presence & Authenticity, Emotions, etc.) and their bullet lists from the literature-notes/index.md. Keep just the intro paragraph and let the auto-generated folder listing (with tags) serve as the full index.

### 7. Tags page — style improvements
- Make tag headers (#abandonment, #abundance, etc.) more visually distinct — larger, bolder, with a separator or background treatment
- Add an intro paragraph explaining what tags are and how to navigate them

### 8. Reference notes — categorize all videos
Go through all reference notes and assign each to one of four categories via frontmatter or folder structure:
- Coaching Sessions
- Podcast Episodes
- Guest Appearances
- Short Lessons

### 9. Graph view — improve readability
- Increase node spacing / repulsion force so nodes aren't crammed together
- Show note titles only on hover, not by default
- Make the graph navigable at the scale of 1500+ notes

### 10. Home page — full redesign
- Remove both sidebars (full-width layout for home page only)
- Write a longer introduction (~1000-1500 words) with links to appropriate sections
- Expand "About This Project" section to explain:
  - What a Zettelkasten is
  - Who built this and why
- Expand "About Joe Hudson" section with:
  - Link to Art of Accomplishment website
  - List of links to his courses and workshops
- Embed the knowledge graph in the page body (not sidebar)

---

## 🚫 Blocked
- **Transcript reformatting** — Pipeline built (whisper + pyannote diarization), blocked on YouTube 403s. Ready to run when yt-dlp fixes land.

## 📦 Future
- Deploy to production (Vercel/Netlify/GitHub Pages)
- Ongoing maintenance (process new videos as they come out)
- Re-enable OG image generation before deploy
