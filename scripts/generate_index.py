#!/usr/bin/env python3
"""
Generate markdown documentation from glossary.json.
Creates index.md and individual letter files (a.md through z.md).
"""

import json
from collections import defaultdict
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
GLOSSARY_FILE = ROOT_DIR / "glossary.json"
DOCS_DIR = ROOT_DIR / "docs"


def load_glossary():
    """Load glossary entries from JSON file."""
    with open(GLOSSARY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def group_by_letter(entries):
    """Group entries by the first letter of pinyin."""
    grouped = defaultdict(list)
    for entry in entries:
        # Get first letter of pinyin
        first_letter = entry['pinyin'][0].lower()
        grouped[first_letter].append(entry)
    return grouped


def generate_letter_file(letter, entries):
    """Generate markdown file for a single letter."""
    lines = [
        f"# {letter.upper()}\n",
        "| 拼音 | 汉字 | Mathews | GSR | 部首 | 位置 | 定义 |",
        "|------|------|---------|-----|------|------|------|"
    ]

    for entry in entries:
        pinyin = entry['pinyin']
        hanzi = entry['hanzi']
        mathews = entry['mathews']
        gsr = entry['gsr']
        radical = entry['radical']
        location = entry['location'] if entry['location'] else ''
        # Truncate long definitions for table
        definition = entry['definition'][:80] + '...' if len(entry['definition']) > 80 else entry['definition']
        # Escape pipe characters in definition
        definition = definition.replace('|', '\\|')

        lines.append(f"| {pinyin} | {hanzi} | {mathews} | {gsr} | {radical} | {location} | {definition} |")

    return '\n'.join(lines)


def generate_index(grouped):
    """Generate index.md with links to all letter files."""
    lines = [
        "# Yijing Glossary / 词汇表索引\n",
        "This glossary contains Chinese vocabulary extracted from *Yijing1+2.pdf* (pages 1009-1054).",
        "Each entry includes pinyin, hanzi (Chinese character), Mathews dictionary number,",
        "GSR (Karlgren's Grammata Serica Recensa), radical, location, and definition.\n",
        "---",
        "\n## Statistics / 统计信息\n",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total Entries | {sum(len(v) for v in grouped.values())} |",
        f"| Letter Categories | {len(grouped)} |",
    ]

    # Find min/max categories
    counts = {letter: len(entries) for letter, entries in grouped.items()}
    max_letter = max(counts, key=counts.get)
    min_letters = [k for k, v in counts.items() if v == min(counts.values())]

    lines.append(f"| Largest Category | {max_letter.upper()} ({counts[max_letter]} entries) |")
    lines.append(f"| Smallest Category | {', '.join(l.upper() for l in min_letters)} ({counts[min_letters[0]]} entries) |")

    lines.append("\n---\n## Alphabetical Index / 字母索引\n")

    # Create links for each letter
    for letter in sorted(grouped.keys()):
        count = len(grouped[letter])
        lines.append(f"- [{letter.upper()}]({letter}.md) - {count} entries")

    return '\n'.join(lines)


def main():
    """Main generation function."""
    print("Loading glossary...")
    entries = load_glossary()
    print(f"Loaded {len(entries)} entries")

    print("Grouping by letter...")
    grouped = group_by_letter(entries)

    # Ensure docs directory exists
    DOCS_DIR.mkdir(exist_ok=True)

    # Generate individual letter files
    print("Generating letter files...")
    for letter in sorted(grouped.keys()):
        entries = grouped[letter]
        content = generate_letter_file(letter, entries)
        output_file = DOCS_DIR / f"{letter}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  {letter}.md - {len(entries)} entries")

    # Generate index
    print("Generating index.md...")
    index_content = generate_index(grouped)
    index_file = DOCS_DIR / "index.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)

    print(f"\nComplete! Generated {len(grouped)} letter files + index.md in {DOCS_DIR}")


if __name__ == "__main__":
    main()
