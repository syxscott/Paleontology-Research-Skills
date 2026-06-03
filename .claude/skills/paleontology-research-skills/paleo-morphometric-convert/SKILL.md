---
name: paleo-morphometric-convert
description: 🔄 Convert geometric morphometric landmark data between TPS, NTSys, CSV, JSON, and Excel formats. Handles single-specimen and multi-specimen files, with validation of landmark counts. Use when the user has landmarks in one format and needs another (e.g. TPS for MorphoJ, CSV for R, Excel for inspection). Does NOT extract landmarks from images — for that use `paleo-morphometric`.
---

# Morphometric Data Format Conversion

Converts geometric morphometric (GM) landmark datasets between the formats commonly used by MorphoJ, NTSys-pc, R `geomorph`, and custom pipelines.

## When to Use

- "Convert this TPS file to Excel"
- "I have a CSV of landmarks — make it TPS for MorphoJ"
- "Merge these multiple TPS files into one"
- "Validate this landmark dataset"
- "Convert from NTSys to JSON"

## When NOT to Use

- Extract landmarks from a fossil **image** → use `paleo-morphometric`
- Statistical shape analysis → use R `geomorph` or MorphoJ

## Supported Formats

| Format | Extension | Notes |
|---|---|---|
| **TPS** | `.tps` | MorphoJ / `tpsdig` standard. Supports multi-specimen. |
| **NTSys** | `.nts` | NTSys-PC matrix format. |
| **CSV** | `.csv` | Long format: `specimen_id,landmark_id,x,y[,type,name]` |
| **JSON** | `.json` | PaleoClaw / GeoClaw native (single or array of payloads) |
| **Excel** | `.xlsx` | One Summary sheet with all rows (requires `openpyxl`) |

## Usage

```bash
# TPS -> CSV
python3 scripts/convert.py --input fossils.tps --to csv --out fossils.csv

# CSV -> TPS
python3 scripts/convert.py --input data.csv --to tps --out data.tps

# Excel -> JSON (single output file)
python3 scripts/convert.py --input lm.xlsx --to json --out lm.json

# Merge multiple TPS files into one
python3 scripts/convert.py --merge file1.tps file2.tps file3.tps --to tps --out merged.tps

# Validate (report landmark count consistency, missing values)
python3 scripts/convert.py --input fossils.tps --validate
```

## Output Format

```json
{
  "input_format": "tps",
  "output_format": "csv",
  "output_path": "fossils.csv",
  "specimens_count": 12,
  "landmarks_per_specimen": 64,
  "validation": {
    "all_same_count": true,
    "missing_landmarks": 0,
    "warnings": []
  }
}
```

## Notes

- **TPS multi-specimen blocks** are auto-detected (blank line + new `LM=` header).
- **NTSys** matrix is read as 2D coordinates with header `1 N P 0`.
- For **scale**: TPS preserves; CSV/JSON allow per-specimen scale; NTSys does NOT.
- If openpyxl is missing, Excel I/O degrades gracefully with a clear error message.
