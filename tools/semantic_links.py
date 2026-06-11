#!/usr/bin/env python3
"""
Semantic Link Generator for Joe Hudson Zettelkasten
Generates embeddings for all literature notes and finds semantically similar pairs.

Usage:
  # Generate embeddings (first run)
  python tools/semantic_links.py embed

  # Show top connections at a given threshold
  python tools/semantic_links.py report --threshold 0.75

  # Show connections for a specific note
  python tools/semantic_links.py inspect <slug>

  # Apply links to files (writes to markdown)
  python tools/semantic_links.py apply --threshold 0.75 --top-n 5
"""

import os
import re
import json
import sys
import numpy as np
from pathlib import Path

CONTENT_DIR = Path(__file__).parent.parent / "content" / "teachings"
DATA_DIR = Path(__file__).parent.parent / "tools" / "data"
EMBEDDINGS_FILE = DATA_DIR / "embeddings.npz"
METADATA_FILE = DATA_DIR / "metadata.json"


def parse_note(filepath):
    """Extract title, slug, and body content from a literature note."""
    text = filepath.read_text(encoding="utf-8")

    # Extract title from frontmatter
    title_match = re.search(r'^title:\s*"(.+)"', text, re.MULTILINE)
    title = title_match.group(1) if title_match else filepath.stem.replace("-", " ").title()

    # Strip frontmatter
    parts = text.split("---", 2)
    body = parts[2].strip() if len(parts) >= 3 else text

    # Remove markdown links syntax but keep text
    body = re.sub(r'\[\[.*?\|(.*?)\]\]', r'\1', body)
    body = re.sub(r'\[\[(.*?)\]\]', r'\1', body)

    # Remove headings markers
    body = re.sub(r'^#+\s+', '', body, flags=re.MULTILINE)

    return {
        "slug": filepath.stem,
        "title": title,
        "body": body,
        "path": str(filepath),
    }


def load_notes():
    """Load all literature notes."""
    notes = []
    for f in sorted(CONTENT_DIR.glob("*.md")):
        if f.stem in ("index", "_index"):
            continue
        note = parse_note(f)
        if note["body"]:
            notes.append(note)
    return notes


def cmd_embed():
    """Generate embeddings for all literature notes."""
    from sentence_transformers import SentenceTransformer

    print("Loading notes...")
    notes = load_notes()
    print(f"Found {len(notes)} literature notes")

    print("Loading model (BAAI/bge-base-en-v1.5)...")
    model = SentenceTransformer("BAAI/bge-base-en-v1.5")

    print("Generating embeddings...")
    texts = [n["body"] for n in notes]
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)

    # Save
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(EMBEDDINGS_FILE, embeddings=embeddings)
    metadata = [{"slug": n["slug"], "title": n["title"]} for n in notes]
    METADATA_FILE.write_text(json.dumps(metadata, indent=2))

    print(f"Saved {len(notes)} embeddings to {EMBEDDINGS_FILE}")
    print(f"Saved metadata to {METADATA_FILE}")


def load_embeddings():
    """Load pre-computed embeddings and metadata."""
    data = np.load(EMBEDDINGS_FILE)
    embeddings = data["embeddings"]
    metadata = json.loads(METADATA_FILE.read_text())
    return embeddings, metadata


def compute_similarity(embeddings):
    """Compute cosine similarity matrix. Embeddings are already normalized."""
    return embeddings @ embeddings.T


def cmd_report(threshold=0.75, top_n=5):
    """Show a report of connections at a given threshold."""
    embeddings, metadata = load_embeddings()
    sim_matrix = compute_similarity(embeddings)
    n = len(metadata)

    # Zero out self-similarity
    np.fill_diagonal(sim_matrix, 0)

    # Stats
    upper = sim_matrix[np.triu_indices(n, k=1)]
    above_threshold = np.sum(upper >= threshold)
    total_pairs = len(upper)

    print(f"=== Semantic Similarity Report ===")
    print(f"Notes: {n}")
    print(f"Threshold: {threshold}")
    print(f"Pairs above threshold: {above_threshold} / {total_pairs} ({above_threshold/total_pairs*100:.2f}%)")
    print(f"Average connections per note: {above_threshold * 2 / n:.1f}")
    print()

    # Score distribution
    print("Score distribution:")
    for t in [0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5]:
        count = np.sum(upper >= t)
        avg = count * 2 / n
        print(f"  >= {t:.2f}: {count:>6} pairs ({avg:.1f} avg per note)")
    print()

    # Sample: show 20 random connections at the threshold
    print(f"=== Sample Connections (threshold >= {threshold}) ===")
    pairs = []
    for i in range(n):
        top_indices = np.argsort(sim_matrix[i])[::-1][:top_n]
        for j in top_indices:
            if sim_matrix[i][j] >= threshold:
                pairs.append((sim_matrix[i][j], metadata[i], metadata[j]))

    # Sort by score, show top 30
    pairs.sort(key=lambda x: -x[0])
    for score, a, b in pairs[:30]:
        print(f"  {score:.3f}  {a['title'][:50]:<50}  ↔  {b['title'][:50]}")

    print()
    print(f"=== Weakest Connections at Threshold ===")
    # Show the bottom 10 near the threshold
    near_threshold = [(s, a, b) for s, a, b in pairs if s >= threshold]
    near_threshold.sort(key=lambda x: x[0])
    for score, a, b in near_threshold[:10]:
        print(f"  {score:.3f}  {a['title'][:50]:<50}  ↔  {b['title'][:50]}")


def cmd_inspect(slug):
    """Show connections for a specific note."""
    embeddings, metadata = load_embeddings()
    sim_matrix = compute_similarity(embeddings)

    # Find the note
    idx = None
    for i, m in enumerate(metadata):
        if m["slug"] == slug:
            idx = i
            break

    if idx is None:
        print(f"Note not found: {slug}")
        print("Available slugs (first 20):", [m["slug"] for m in metadata[:20]])
        return

    print(f"=== Connections for: {metadata[idx]['title']} ===")
    print(f"Slug: {slug}")
    print()

    scores = sim_matrix[idx].copy()
    scores[idx] = 0  # exclude self
    ranked = np.argsort(scores)[::-1]

    for rank, j in enumerate(ranked[:20], 1):
        score = scores[j]
        print(f"  {rank:>2}. {score:.3f}  {metadata[j]['title']}")


def cmd_apply(threshold=0.75, top_n=5, dry_run=True):
    """Apply semantic links to literature note files."""
    embeddings, metadata = load_embeddings()
    sim_matrix = compute_similarity(embeddings)
    np.fill_diagonal(sim_matrix, 0)
    n = len(metadata)

    slug_to_idx = {m["slug"]: i for i, m in enumerate(metadata)}
    changes = 0

    for i in range(n):
        slug = metadata[i]["slug"]
        filepath = CONTENT_DIR / f"{slug}.md"
        if not filepath.exists():
            continue

        # Find top matches above threshold
        scores = sim_matrix[i].copy()
        ranked = np.argsort(scores)[::-1]
        matches = []
        for j in ranked[:top_n]:
            if scores[j] >= threshold:
                matches.append(metadata[j])

        if not matches:
            continue

        content = filepath.read_text(encoding="utf-8")

        # Check which links already exist
        new_matches = []
        for m in matches:
            link_pattern = f"teachings/{m['slug']}"
            if link_pattern not in content:
                new_matches.append(m)

        if not new_matches:
            continue

        changes += 1
        if dry_run:
            print(f"\n{metadata[i]['title']}:")
            for m in new_matches:
                score = sim_matrix[i][slug_to_idx[m["slug"]]]
                print(f"  + [{score:.3f}] {m['title']}")
        else:
            # Build new links
            new_links = []
            for m in new_matches:
                new_links.append(f"- [[teachings/{m['slug']}|{m['title']}]]")

            # Find Related Concepts section and append, or create it
            if "## Related Concepts" in content:
                insertion = content.index("## Related Concepts")
                # Find the end of the section (next ## or ## Source)
                next_section = re.search(r'\n## ', content[insertion + 20:])
                if next_section:
                    insert_at = insertion + 20 + next_section.start()
                else:
                    insert_at = len(content)
                new_content = content[:insert_at].rstrip() + "\n" + "\n".join(new_links) + "\n" + content[insert_at:]
            elif "## Source" in content:
                insert_at = content.index("## Source")
                new_content = content[:insert_at] + "## Related Concepts\n\n" + "\n".join(new_links) + "\n\n" + content[insert_at:]
            else:
                new_content = content.rstrip() + "\n\n## Related Concepts\n\n" + "\n".join(new_links) + "\n"

            filepath.write_text(new_content, encoding="utf-8")

    action = "Would update" if dry_run else "Updated"
    print(f"\n{action} {changes} notes")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "embed":
        cmd_embed()
    elif cmd == "report":
        threshold = 0.75
        for i, arg in enumerate(sys.argv):
            if arg == "--threshold" and i + 1 < len(sys.argv):
                threshold = float(sys.argv[i + 1])
        cmd_report(threshold=threshold)
    elif cmd == "inspect":
        if len(sys.argv) < 3:
            print("Usage: semantic_links.py inspect <slug>")
            sys.exit(1)
        cmd_inspect(sys.argv[2])
    elif cmd == "apply":
        threshold = 0.75
        top_n = 5
        dry_run = True
        for i, arg in enumerate(sys.argv):
            if arg == "--threshold" and i + 1 < len(sys.argv):
                threshold = float(sys.argv[i + 1])
            if arg == "--top-n" and i + 1 < len(sys.argv):
                top_n = int(sys.argv[i + 1])
            if arg == "--write":
                dry_run = False
        cmd_apply(threshold=threshold, top_n=top_n, dry_run=dry_run)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
