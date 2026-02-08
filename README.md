# Yijing Glossary / 词汇表

A comprehensive Chinese vocabulary glossary extracted from *Yijing1+2.pdf* (pages 1009-1054), cross-referenced with Mathews' Chinese-English Dictionary and Karlgren's Grammata Serica Recensa (GSR).

## 项目简介 / Project Overview

This repository contains a structured glossary of 334 Chinese vocabulary entries from the Yijing (Book of Changes). Each entry includes:

- **拼音 (Pinyin)**: Romanized pronunciation with tone marks
- **汉字 (Hanzi)**: Chinese character
- **Mathews**: Reference number from Mathews' Chinese-English Dictionary
- **GSR**: Reference number from Karlgren's Grammata Serica Recensa
- **部首 (Radical)**: Character radical + stroke count
- **位置 (Location)**: Page/chapter location in source text
- **定义 (Definition)**: English definition from the glossary

## Data Format / 数据格式

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

## Directory Structure / 目录结构

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
│   ├── a.md                         # Entries starting with 'a'
│   ├── b.md                         # Entries starting with 'b'
│   └── ...                          # (22 letter files total)
└── data/
    └── Yijing1+2.pdf                # Source PDF (optional)
```

## Usage / 使用方法

### Viewing the Glossary

1. **Browse Online**: View the generated markdown files in the `docs/` directory
2. **Raw Data**: Access `glossary.json` for programmatic use
3. **Index**: Start at `docs/index.md` for alphabetical navigation

### Generating Documentation

To regenerate the markdown documentation from `glossary.json`:

```bash
python scripts/generate_index.py
```

This will recreate all files in `docs/`.

### Extracting from PDF

If you have the source PDF and need to re-extract the glossary:

```bash
python extract_glossary.py
```

**Requirements**: `pdfplumber` (`pip install pdfplumber`)

**Note**: The script assumes `data/Yijing1+2.pdf` exists.

## Statistics / 统计信息

| Metric | Value |
|--------|-------|
| Total Entries | 334 |
| Letter Categories | 22 |
| Largest Category | Y (42 entries) |
| Smallest Category | A, E, P (1-3 entries) |

## Data Source / 数据来源

- **Source**: *Yijing1+2.pdf*, pages 1009-1054
- **Dictionaries**:
  - Mathews' Chinese-English Dictionary
  - Karlgren's Grammata Serica Recensa (GSR)

## License

This glossary data is extracted from published academic sources. Please refer to the original works for citation and licensing information.

## Contributing

This is a standalone repository for glossary data. For issues or updates related to the extraction process, please refer to the parent project or create issues in this repository.
