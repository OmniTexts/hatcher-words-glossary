#!/usr/bin/env python3
"""
Extract glossary from Yijing1+2.pdf pages 1009-1054.
Generates a JSON file with pinyin, Mathews number, hanzi, GSR, radical, location, and definition.
"""

import re
import json
import pdfplumber
from typing import List, Dict, Optional

# Import the Mathews to Hanzi mapping
from pdf_mathews_to_hanzi import PDF_MATHEWS_TO_HANZI

# Page range (0-indexed: pages 1009-1054 = 1008-1053)
PAGE_START = 1008  # PDF page 1009 (0-indexed)
PAGE_END = 1054    # PDF page 1054 (exclusive, 0-indexed)

# Output file
OUTPUT_FILE = "/Users/jack/workspace/study/iching/data/glossary/glossary.json"


def parse_glossary_line(line: str) -> Optional[Dict[str, str]]:
    """
    Parse a single line from the glossary.

    Expected format:
    an1 0026 146a 40+302.0 (to be) content(ed), at peace...
    ba1 4845 281a 12+0 19.0 (a, the) eight...
    ban4 4875 181a 24+2 none (to be) half...

    Note: The PDF format is INCONSISTENT:
    - Sometimes location is concatenated: "40+302.0" (radical=40+3, location=02.0)
    - Sometimes separated by space: "12+0 19.0" (radical=12+0, location=19.0)
    - Location may have suffix: "07.2x", or be "none", or "28.T"
    """
    line = line.strip()
    if not line:
        return None

    # Skip page headers and footers
    if re.match(r'^\d+$', line) or 'Glossary' in line or 'SHAUGHNESSY' in line:
        return None

    # First, extract the first 3 fields (pinyin, mathews, gsr) and the rest
    parts = line.split(None, 3)
    if len(parts) < 4:
        return None

    pinyin, mathews, gsr, rest = parts

    # Validate mathews is 4 digits
    if not re.match(r'^\d{4}$', mathews):
        return None

    # Validate pinyin format
    if not re.match(r'^[a-z]+\d+$', pinyin):
        return None

    # Now parse the rest which contains: radical [location] definition
    # Helper function to parse radical and location
    def parse_radical_location(s: str):
        """Parse radical and location from string s, return (radical, location, definition)"""

        # Check for 'none' first
        if ' none ' in s or s.endswith(' none'):
            parts = s.split(' none', 1)
            radical_part = parts[0]
            radical_match = re.match(r'(\d+\+\d+)', radical_part)
            if radical_match:
                radical = radical_match.group(1)
                definition = parts[1].strip() if len(parts) > 1 else ''
                return radical, 'none', definition
            return None, None, None

        # Try separated: radical space location space definition
        sep_pattern = r'^(\d+\+\d+)\s+(\d+\.\d+[a-z]?|\d+\.[A-Z]+)\s+(.+)$'
        match = re.match(sep_pattern, s)
        if match:
            return match.group(1), match.group(2), match.group(3)

        # Try concatenated: stroke count + location digits together
        # Use progressive approach: try 1-digit stroke count first, then 2-digit
        for stroke_len in range(1, 3):  # Try 1 or 2 digit stroke count
            rad_pattern = rf'^(\d+\+\d{{{stroke_len}}})'
            rad_match = re.match(rad_pattern, s)
            if rad_match:
                potential_radical = rad_match.group(1)
                remaining = s[rad_match.end():]
                # Check if remaining starts with a valid location pattern
                # Location: digits.digits[suffix] or none or digits.UPPER
                loc_patterns = [
                    r'^(\d+\.\d+[a-z]?)\s+(.+)$',     # 02.0 (to be)...
                    r'^(\d+\.[A-Z]+)\s+(.+)$',        # 28.T (a, the)...
                ]
                for loc_p in loc_patterns:
                    loc_match = re.match(loc_p, remaining)
                    if loc_match:
                        return potential_radical, loc_match.group(1), loc_match.group(2)

                # Also check if location is at end (no definition after)
                loc_end_patterns = [
                    r'^(\d+\.\d+[a-z]?)$',            # 02.0 at end
                    r'^(\d+\.[A-Z]+)$',               # 28.T at end
                ]
                for loc_p in loc_end_patterns:
                    loc_match = re.match(loc_p, remaining)
                    if loc_match:
                        return potential_radical, loc_match.group(1), ''

        # No location found, everything is definition
        rad_match = re.match(r'^(\d+\+\d+)\s+(.+)$', s)
        if rad_match:
            return rad_match.group(1), '', rad_match.group(2)

        return None, None, None

    radical, location, definition = parse_radical_location(rest)

    if radical is None or not definition:
        return None

    # Look up the hanzi from Mathews number
    mathews_key = mathews
    if mathews_key not in PDF_MATHEWS_TO_HANZI:
        print(f"Warning: No hanzi found for Mathews {mathews} ({pinyin})")
        return None

    hanzi = PDF_MATHEWS_TO_HANZI[mathews_key][0]

    return {
        "pinyin": pinyin,
        "mathews": mathews,
        "hanzi": hanzi,
        "gsr": gsr,
        "radical": radical,
        "location": location,
        "definition": definition
    }


def extract_glossary(pdf_path: str) -> List[Dict[str, str]]:
    """Extract glossary entries from PDF."""
    entries = []

    print(f"Opening PDF: {pdf_path}")

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages in PDF: {total_pages}")

        # Adjust page range if needed
        if PAGE_START >= total_pages:
            print(f"Error: PAGE_START ({PAGE_START}) >= total pages ({total_pages})")
            return []

        end_page = min(PAGE_END, total_pages)
        print(f"Extracting pages {PAGE_START + 1}-{end_page} (1-indexed)")

        # Accumulate multi-line definitions
        current_entry = None
        continuation_lines = []

        for page_num in range(PAGE_START, end_page):
            page = pdf.pages[page_num]
            text = page.extract_text()

            if not text:
                continue

            # Process each line
            for line in text.split('\n'):
                line = line.strip()
                if not line:
                    continue

                # Check if this line starts a new entry (pinyin pattern at start)
                # Pinyin pattern: lowercase letters + digit at start of line
                is_new_entry = re.match(r'^[a-z]+\d+\s+\d{4}\s+', line)

                if is_new_entry:
                    # Save previous entry if exists
                    if current_entry:
                        # Add any continuation lines to the definition
                        if continuation_lines:
                            current_entry['definition'] += ' ' + ' '.join(continuation_lines)
                            continuation_lines = []
                        entries.append(current_entry)
                        print(f"Added: {current_entry['pinyin']} ({current_entry['hanzi']}) - Mathews {current_entry['mathews']}")

                    # Parse new entry
                    current_entry = parse_glossary_line(line)
                    if not current_entry:
                        # If parsing failed, this might be a continuation line
                        if current_entry is None and continuation_lines is not None:
                            continuation_lines.append(line)
                        continue
                else:
                    # Continuation line - append to current entry's definition
                    if current_entry:
                        continuation_lines.append(line)

        # Don't forget the last entry
        if current_entry:
            if continuation_lines:
                current_entry['definition'] += ' ' + ' '.join(continuation_lines)
            entries.append(current_entry)
            print(f"Added: {current_entry['pinyin']} ({current_entry['hanzi']}) - Mathews {current_entry['mathews']}")

    return entries


def main():
    pdf_path = "/Users/jack/workspace/study/iching/data/Yijing1+2.pdf"

    print("=" * 60)
    print("Extracting Yijing Glossary (pages 1009-1054)")
    print("=" * 60)

    entries = extract_glossary(pdf_path)

    print(f"\nTotal entries extracted: {len(entries)}")

    # Write to JSON file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print(f"Written to: {OUTPUT_FILE}")

    # Print sample entries
    print("\n" + "=" * 60)
    print("Sample entries:")
    print("=" * 60)
    for entry in entries[:10]:
        print(f"{entry['pinyin']:8} | {entry['mathews']:6} | {entry['hanzi']:4} | {entry['radical']:6} | {entry['location']:8} | {entry['definition'][:50]}...")

    # Verify expected count
    expected = 271
    if len(entries) == expected:
        print(f"\n✓ Entry count matches expected: {expected}")
    else:
        print(f"\n⚠ Warning: Expected {expected} entries, got {len(entries)}")


if __name__ == "__main__":
    main()
