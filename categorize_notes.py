#!/usr/bin/env python3
"""
Script to categorize all reference notes by adding a category field to their frontmatter.
"""

import os
import re
from pathlib import Path

# Define the categories
CATEGORIES = {
    "coaching": "Coaching Session",
    "podcast": "Podcast Episode", 
    "guest": "Guest Appearance",
    "teaching": "Short Lesson"
}

def analyze_content(filepath, title, frontmatter_content, main_content):
    """
    Analyze the content to determine the appropriate category.
    """
    title_lower = title.lower()
    content_lower = main_content.lower()
    
    # Check for coaching sessions
    if (("coaching session" in content_lower) or 
        ("joe hudson works with" in content_lower) or
        ("in this coaching" in content_lower) or
        (frontmatter_content and "type: coaching-session" in frontmatter_content)):
        return CATEGORIES["coaching"]
    
    # Check for guest appearances (Joe appearing on other podcasts)
    if (("chris williamson" in content_lower) or
        ("dr. k" in content_lower) or 
        ("dr k" in content_lower) or
        ("lex fridman" in content_lower) or
        ("joe sanok" in content_lower) or
        ("sam altman" in content_lower) or
        ("emile deweaver" in content_lower) or
        (("on " in title_lower and ("podcast" in title_lower or "show" in title_lower)) and
         "art of accomplishment" not in title_lower)):
        return CATEGORIES["guest"]
    
    # Check for Art of Accomplishment podcast episodes
    if (("art of accomplishment" in content_lower) or
        ("welcome to the art of accomplishment" in content_lower) or
        ("brett kistler" in content_lower) or
        ("with my co-host" in content_lower) or
        ("today's guest" in content_lower) or
        (frontmatter_content and "type: interview" in frontmatter_content and "duration:" in frontmatter_content)):
        return CATEGORIES["podcast"]
    
    # Default to Short Lesson (teaching videos, standalone content)
    return CATEGORIES["teaching"]

def process_file(filepath):
    """
    Process a single markdown file to add category field.
    """
    print(f"Processing: {filepath.name}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into frontmatter and main content
    if content.startswith('---\n'):
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            main_content = parts[2]
        else:
            frontmatter = ""
            main_content = content
    else:
        frontmatter = ""
        main_content = content
    
    # Check if category already exists
    if "category:" in frontmatter:
        print(f"  ✓ Already has category")
        return
    
    # Extract title
    title_match = re.search(r'title:\s*"([^"]+)"', frontmatter)
    title = title_match.group(1) if title_match else filepath.stem
    
    # Determine category
    category = analyze_content(filepath, title, frontmatter, main_content)
    print(f"  → {category}")
    
    # Add category to frontmatter
    # Find the right place to insert it (after type if it exists, otherwise after title)
    lines = frontmatter.split('\n')
    insert_index = -1
    
    for i, line in enumerate(lines):
        if line.startswith('type:'):
            insert_index = i + 1
            break
        elif line.startswith('duration:') and insert_index == -1:
            insert_index = i + 1
            break
        elif line.startswith('videoId:') and insert_index == -1:
            insert_index = i + 1
            break
    
    if insert_index == -1:
        # Find title line
        for i, line in enumerate(lines):
            if line.startswith('title:'):
                insert_index = i + 1
                break
    
    if insert_index != -1:
        lines.insert(insert_index, f'category: "{category}"')
    else:
        # Add at the end of frontmatter
        lines.append(f'category: "{category}"')
    
    # Reconstruct the file
    new_frontmatter = '\n'.join(lines)
    new_content = f"---\n{new_frontmatter}\n---\n{main_content}"
    
    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    """Main function to process all reference notes."""
    notes_dir = Path("content/reference-notes")
    
    if not notes_dir.exists():
        print(f"Directory {notes_dir} not found!")
        return
    
    # Get all markdown files
    md_files = list(notes_dir.glob("*.md"))
    
    print(f"Found {len(md_files)} files to process\n")
    
    # Process each file
    category_counts = {
        "Coaching Session": 0,
        "Podcast Episode": 0, 
        "Guest Appearance": 0,
        "Short Lesson": 0
    }
    
    for filepath in sorted(md_files):
        if filepath.name == "index.md":
            continue
            
        try:
            old_content = ""
            with open(filepath, 'r', encoding='utf-8') as f:
                old_content = f.read()
            
            process_file(filepath)
            
            # Count the category
            with open(filepath, 'r', encoding='utf-8') as f:
                new_content = f.read()
                for category in category_counts:
                    if f'category: "{category}"' in new_content:
                        category_counts[category] += 1
                        break
                        
        except Exception as e:
            print(f"  ✗ Error processing {filepath.name}: {e}")
    
    # Print summary
    print("\n" + "="*50)
    print("CATEGORIZATION SUMMARY")
    print("="*50)
    total = sum(category_counts.values())
    
    for category, count in category_counts.items():
        percentage = (count / total) * 100 if total > 0 else 0
        print(f"{category:20} {count:3d} files ({percentage:5.1f}%)")
    
    print(f"{'TOTAL':20} {total:3d} files")

if __name__ == "__main__":
    main()