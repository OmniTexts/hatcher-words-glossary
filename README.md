# Yijing Glossary

A comprehensive Chinese vocabulary glossary extracted from *Yijing1+2.pdf* (pages 1009-1054). See [the glossary introduction on page 1008](data/Yijing1+2.pdf#page=1008) for details about the source material and methodology.

**[Browse the Glossary Index](docs/index.md)**

---

## Project Overview

This repository contains a structured glossary of 334 Chinese vocabulary entries from the Yijing (Book of Changes). Each entry includes:

- **Pinyin**: Romanized pronunciation with tone marks
- **Hanzi**: Chinese character
- **Mathews**: Reference number from Mathews' Chinese-English Dictionary
- **GSR**: Reference number from Karlgren's Grammata Serica Recensa
- **Radical**: Character radical + stroke count
- **Location**: Page/chapter location in source text
- **Definition**: English definition from the glossary

## Quick Start

View the glossary: [docs/index.md](docs/index.md)

Or explore by letter:
- [A](docs/a.md) | [B](docs/b.md) | [C](docs/c.md) | [D](docs/d.md) | [E](docs/e.md)
- [F](docs/f.md) | [G](docs/g.md) | [H](docs/h.md) | [J](docs/j.md) | [K](docs/k.md)
- [L](docs/l.md) | [M](docs/m.md) | [N](docs/n.md) | [P](docs/p.md) | [Q](docs/q.md)
- [R](docs/r.md) | [S](docs/s.md) | [T](docs/t.md) | [W](docs/w.md) | [X](docs/x.md)
- [Y](docs/y.md) | [Z](docs/z.md)

## Data Format

Each entry in `glossary.json` follows this structure:

```json
{
  "pinyin": "an1",
  "mathews": "0026",
  "hanzi": "安",
  "gsr": "146a",
  "radical": "40+3",
  "location": "02.0",
  "definition": "(to be) content(ed), at peace, at rest..."
}
```

## Directory Structure

```
yijing-glossary/
├── README.md                        # This file
├── glossary.json                    # Complete glossary data (334 entries)
├── pdf_mathews_to_hanzi.py          # Mathews number → Hanzi mapping (7769 entries)
├── extract_glossary.py              # PDF extraction script
├── scripts/
│   └── generate_index.py            # Generate markdown documentation
├── docs/
│   ├── index.md                     # Main index page
│   ├── a.md - z.md                  # Entries grouped by first letter
└── data/
    └── Yijing1+2.pdf                # Source PDF (optional)
```

## Usage

### Generating Documentation

To regenerate the markdown documentation from `glossary.json`:

```bash
python scripts/generate_index.py
```

### Extracting from PDF

If you have the source PDF and need to re-extract the glossary:

```bash
python extract_glossary.py
```

**Requirements**: `pip install pdfplumber`

## Statistics

| Metric | Value |
|--------|-------|
| Total Entries | 334 |
| Letter Categories | 22 |
| Largest Category | Y (42 entries) |
| Smallest Category | A, E, P (1-3 entries) |

## Data Source

- **Source**: *Yijing1+2.pdf*, pages 1009-1054
- **Introduction**: See page 1008 for glossary methodology
- **Dictionaries**:
  - Mathews' Chinese-English Dictionary
  - Karlgren's Grammata Serica Recensa (GSR)

## Related Resources

This glossary is part of a broader effort to digitize and structure the Yijing tradition. For comprehensive resources including:

- Yijing Divination Methods: Guides on yarrow stalk and coin divination
- Welham Translation: An alternative translation of the Yijing text
- Bradford Hatcher's Structured Edition: The first structured presentation of Hatcher's 1,100-page Yijing translation

Visit [castiching.com](https://castiching.com) and explore the [Bradford Hatcher collection](https://castiching.com/bradford-hatcher).

## License

This glossary data is extracted from published academic sources. Please refer to the original works for citation and licensing information.
