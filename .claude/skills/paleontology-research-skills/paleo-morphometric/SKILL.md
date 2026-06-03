---
name: paleo-morphometric
description: 📐 Extract geometric morphometric landmarks from fossil images (ammonoids, brachiopods, bivalves, gastropods, trilobites, etc.). Generates N evenly-spaced semilandmarks (default 64) by tracing the largest binary silhouette contour. Exports TPS / CSV / Excel / JSON formats compatible with MorphoJ and R geomorph. Use when the user wants to extract landmarks, prepare GM data, batch-process fossil images, or visualize landmark positions.
---

# Morphometric Landmark Extraction

Extracts geometric morphometric (GM) landmarks from fossil image silhouettes for downstream shape analysis in MorphoJ, R `geomorph`, PAST, etc.

## When to Use

- "Extract landmarks from this ammonoid image"
- "Prepare morphometric data for MorphoJ from these specimens"
- "Generate semilandmarks for shape analysis"
- "Export TPS format for geometric morphometrics"
- "Batch process the fossil images in this folder"
- "Visualize the landmarks on this fossil"

## When NOT to Use

- 3D specimens or surface scans → use 3D landmark tools (Stratovan Checkpoint, etc.)
- Unclear / low-contrast images → improve image quality first
- Statistical analysis (PCA, Procrustes) → export to MorphoJ / `geomorph`
- Already-digitized landmarks → use `paleo-morphometric-convert` instead

## Supported Fossil Types

| Group | Notes |
|---|---|
| **Ammonoids** 菊石 | Primary target; outer whorl outline |
| **Brachiopods** 腕足类 | Valve outline (ventral or dorsal) |
| **Bivalves** 双壳类 | Single-valve outline |
| **Gastropods** 腹足类 | Shell silhouette |
| **Trilobites** 三叶虫 | Cephalon or pygidium outline |
| **Any fossil** | Anything with a clear binary silhouette |

## Input Requirements

- **Format**: PNG, JPG, JPEG, TIFF, WEBP (PIL/Pillow supported)
- **Quality**: Clear, complete outline; high contrast (ideally pre-thresholded binary silhouette)
- **Resolution**: Recommended ≥ 512 × 512 px

## Dependencies

```bash
pip install Pillow            # required for image processing
pip install openpyxl          # optional, only for Excel export
```

## Usage

```bash
# Single image, export TPS + CSV + JSON
python3 scripts/extract_landmarks.py \
    --image ammonoid.png \
    --num-landmarks 64 \
    --threshold 150 \
    --out-dir results/ \
    --formats tps,csv,json

# Batch process a directory of images
python3 scripts/batch_extract.py \
    --image-dir specimens/ \
    --out-dir results/ \
    --num-landmarks 64 \
    --formats tps,csv,excel

# Visualise landmarks on an image
python3 scripts/visualize_landmarks.py \
    --image fossil.png \
    --landmarks results/fossil.json \
    --out fossil_annotated.png \
    --show-numbers

# Re-export existing landmark JSON to other formats
python3 scripts/export_landmarks.py \
    --input results/specimen.json \
    --format tps \
    --out-dir converted/
```

## Output Formats

### TPS (MorphoJ / `tpsdig` compatible)

```
LM=64
256.5  128.0
260.3  130.2
...
255.8  129.5
IMAGE=specimen.png
ID=specimen_001
SCALE=1.0000
```

### CSV (long format)

```csv
specimen_id,landmark_id,x,y,type,name
specimen_001,1,256.5,128.0,semilandmark,LM01
specimen_001,2,260.3,130.2,semilandmark,LM02
...
```

### JSON (PaleoClaw native)

```json
{
  "specimen_id": "specimen_001",
  "image_path": "/abs/path/to/specimen.png",
  "image_size": {"width": 1024, "height": 768},
  "num_landmarks": 64,
  "threshold": 150,
  "scale": 1.0,
  "landmarks": [
    {"id": 1, "x": 256.5, "y": 128.0, "type": "semilandmark", "name": "LM01"},
    ...
  ],
  "timestamp": "2026-06-03T14:30:00Z",
  "algorithm": "boundary-trace + arc-length-resample"
}
```

### Excel (openpyxl, optional)

One sheet per specimen + a summary sheet with all coordinates.

## Algorithm

1. Load image and convert to 8-bit grayscale
2. Threshold to binary mask (foreground = pixel ≤ threshold; default 150)
3. Find the largest connected foreground component (4-connected flood-fill)
4. Trace its outer boundary clockwise using Moore-neighbourhood tracing
5. Compute cumulative arc length along the boundary
6. Resample to N evenly-spaced points along the perimeter (default N=64)
7. The starting point is the topmost (then leftmost) boundary pixel — orientation is consistent across specimens of similar pose

## Scientific Integrity

⚠️ **Always**:
- Visually verify landmark positions (`visualize_landmarks.py`) before downstream analysis
- Record the threshold value used (it is stored in the JSON output)
- Note that automated landmarks are SEMILANDMARKS — for fixed homologous points, you still need manual digitisation in TPSDig

## Integration

| Pair with | Why |
|---|---|
| `paleo-pbdb` | Find described specimens of the same taxon to compare morphology |
| `paleo-taxonomy` | Verify the taxonomic identification of the specimen |
| `paleo-morphometric-convert` | Convert exported landmarks between TPS / NTSys / CSV / Excel / JSON |
| `paleo-crossref` | Find published GM studies using similar methods |

## Citation

> Based on the DeepMorph algorithm (Xiaokang Liu, China University of Geosciences, Wuhan).

If you use this skill, cite:
> PaleoClaw Contributors (2026). *paleo-morphometric*: Automated landmark extraction for fossil silhouettes. PaleoClaw Skills Toolkit.

## References

- Bookstein, F.L. (1991). *Morphometric Tools for Landmark Data*. Cambridge University Press.
- Zelditch, M.L., Swiderski, D.L., Sheets, H.D. (2012). *Geometric Morphometrics for Biologists*, 2nd ed.
- Adams, D.C. & Otárola-Castillo, E. (2013). geomorph: An R package for the collection and analysis of geometric morphometric shape data. *Methods in Ecology and Evolution*, 4(4): 393-399.
