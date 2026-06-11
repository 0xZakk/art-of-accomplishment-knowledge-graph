#!/usr/bin/env python3
"""
AOA RSS Feed Checker

Checks the Art of Accomplishment YouTube RSS feed for new videos
and processes any that don't have a corresponding source page.

Used by the GitHub Action on the scheduled run.
"""

import os
import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SOURCES_DIR = REPO_ROOT / "content" / "sources"

CHANNEL_ID = "UCK3IN-E6f2bXdNFNOp7esOA"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

# Namespaces used in YouTube RSS
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


def get_processed_video_ids() -> set[str]:
    """Return set of video IDs that already have source pages."""
    ids = set()
    for f in SOURCES_DIR.glob("*.md"):
        text = f.read_text(encoding="utf-8")
        m = re.search(r'videoId:\s*["\']?([A-Za-z0-9_-]{11})["\']?', text)
        if m:
            ids.add(m.group(1))
    return ids


def fetch_rss() -> list[dict]:
    """Fetch and parse the AOA YouTube RSS feed. Returns list of video dicts."""
    req = urllib.request.Request(RSS_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        xml_bytes = resp.read()

    root = ET.fromstring(xml_bytes)
    videos = []

    for entry in root.findall("atom:entry", NS):
        video_id_el = entry.find("yt:videoId", NS)
        title_el = entry.find("atom:title", NS)
        published_el = entry.find("atom:published", NS)

        if video_id_el is None or title_el is None:
            continue

        videos.append({
            "id": video_id_el.text,
            "title": title_el.text,
            "published": published_el.text if published_el is not None else "",
            "url": f"https://www.youtube.com/watch?v={video_id_el.text}",
        })

    return videos


def main():
    print(f"Fetching RSS feed: {RSS_URL}")
    videos = fetch_rss()
    print(f"Found {len(videos)} videos in feed")

    processed = get_processed_video_ids()
    print(f"Already processed: {len(processed)} source pages")

    new_videos = [v for v in videos if v["id"] not in processed]
    print(f"New videos to process: {len(new_videos)}")

    if not new_videos:
        print("Nothing to do.")
        return 0

    errors = []
    for video in new_videos:
        print(f"\nProcessing: {video['title']} ({video['id']})")
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "process_video.py"), video["url"]],
            capture_output=False,
        )
        if result.returncode != 0:
            print(f"  ERROR processing {video['id']}", file=sys.stderr)
            errors.append(video["id"])

    if errors:
        print(f"\nFailed to process: {', '.join(errors)}", file=sys.stderr)
        return 1

    print(f"\nDone. Processed {len(new_videos)} new videos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
