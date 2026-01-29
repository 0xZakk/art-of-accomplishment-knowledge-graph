# Joe Hudson Zettelkasten

[![Quartz](https://img.shields.io/badge/Built%20with-Quartz%20v4-blue)](https://quartz.jzhao.xyz/)
[![Content](https://img.shields.io/badge/Notes-1,545+-green)](#content-overview)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE.txt)

A comprehensive, interconnected knowledge base of **Joe Hudson's** teachings from the [Art of Accomplishment](https://www.youtube.com/@ArtofAccomplishment) YouTube channel — built as a Zettelkasten-style digital garden.

## Overview

This project transforms Joe Hudson's entire YouTube catalog into a searchable, browsable knowledge graph. Each video becomes a **reference note** with full transcript, while key concepts are extracted into atomic **literature notes** that cross-link throughout the knowledge base.

**Why this exists:**
- Joe Hudson's teachings span hundreds of videos covering self-development, emotional processing, relationships, leadership, and more
- Finding specific concepts or tracing ideas across videos was difficult
- A Zettelkasten structure enables serendipitous discovery and deep exploration of interconnected ideas

## Features

- **298 Videos Processed** — Every video from the Art of Accomplishment channel
- **300 Reference Notes** — Each with embedded video, summary, key concepts, and full transcript
- **1,245 Literature Notes** — Atomic concept notes with cross-references
- **10 Topic Categories** — Curated entry points into major themes
- **Full-Text Search** — Find any concept across the entire knowledge base
- **Knowledge Graph** — Visual exploration of how ideas connect
- **YouTube Integration** — Direct links and embedded players for source material

## Project Structure

```
joe-hudson-zettelkasten-site/
├── content/
│   ├── index.md                 # Homepage
│   ├── reference-notes/         # 300 video reference notes
│   ├── literature-notes/        # 1,245 concept notes
│   └── topics/                  # 10 curated topic pages
├── transcripts/                 # Source transcript files
├── quartz/                      # Quartz framework
├── quartz.config.ts             # Site configuration
└── quartz.layout.ts             # Layout configuration
```

### Content Types

| Type | Count | Description |
|------|-------|-------------|
| **Reference Notes** | 300 | Source-linked video notes with transcripts |
| **Literature Notes** | 1,245 | Atomic concept notes with cross-links |
| **Topics** | 10 | Curated entry points by theme |

### Topics Covered

- Purpose & Meaning
- Presence & Authenticity  
- Emotions & Emotional Processing
- Self-Awareness & Self-Discovery
- Relationships & Connection
- Shame & Self-Criticism
- Anger & Boundaries
- Fear & Anxiety
- Leadership & Business

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) v20+
- npm or yarn

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/joe-hudson-zettelkasten-site.git
cd joe-hudson-zettelkasten-site

# Install dependencies
npm install
```

### Development

```bash
# Start local development server
npx quartz build --serve

# Build for production
npx quartz build
```

The site will be available at `http://localhost:8080`.

### Deployment

This site can be deployed to any static hosting service:

```bash
# Build the site
npx quartz build

# Output is in the `public/` directory
```

See the [Quartz hosting documentation](https://quartz.jzhao.xyz/hosting) for platform-specific guides (GitHub Pages, Vercel, Netlify, etc.).

## Configuration

Key configuration files:

- **`quartz.config.ts`** — Site title, base URL, plugins, and features
- **`quartz.layout.ts`** — Page layout and component arrangement

## How It Works

### Reference Notes
Each reference note corresponds to a single YouTube video and contains:
- Embedded YouTube player
- Video metadata (duration, date, topics)
- AI-generated summary
- Links to extracted concept notes
- Key quotes
- Full transcript

### Literature Notes
Literature notes are atomic concept notes following Zettelkasten principles:
- One idea per note
- Heavily cross-linked to related concepts
- Back-linked to source reference notes
- Written in accessible language

### Knowledge Graph
Quartz automatically generates an interactive knowledge graph showing how notes connect, enabling visual exploration of Joe Hudson's interconnected teachings.

## Contributing

Contributions are welcome! Here are some ways to help:

1. **Report Issues** — Found a broken link or error? Open an issue
2. **Improve Notes** — Submit PRs to clarify or expand literature notes
3. **Add Cross-Links** — Help connect related concepts
4. **Fix Transcripts** — Correct transcription errors

Please read [AUTHORING.md](AUTHORING.md) for content guidelines.

## License

This project is licensed under the MIT License — see [LICENSE.txt](LICENSE.txt) for details.

**Note:** The content of Joe Hudson's teachings remains his intellectual property. This project is a fan-made educational resource for navigating and studying his publicly available YouTube content.

## Acknowledgments

- **[Joe Hudson](https://artofaccomplishment.com/)** — For sharing his profound teachings freely on YouTube
- **[Art of Accomplishment](https://www.youtube.com/@ArtofAccomplishment)** — Source of all video content
- **[Quartz](https://quartz.jzhao.xyz/)** — The excellent static site generator powering this digital garden
- **[Zettelkasten Method](https://zettelkasten.de/)** — The note-taking philosophy behind the structure

---

<p align="center">
  <em>Made for the Art of Accomplishment community</em>
</p>
