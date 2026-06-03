# Citation Formats

Paleontology Research Skills must always cite primary sources. The default citation format is
**APA 7**, but the user can override via `user.md` → `Data Preferences` →
`Citation format`.

## Supported formats

| Code | Standard | Example |
|------|----------|---------|
| `APA` | APA 7th edition | Smith, J., & Jones, A. (2023). *A new theropod from the Morrison Formation*. **Journal of Vertebrate Paleontology**, 43(2), e1234567. https://doi.org/10.1080/02724634.2023.1234567 |
| `GB/T 7714` | Chinese national standard GB/T 7714-2015 | Smith J, Jones A. A new theropod from the Morrison Formation[J]. Journal of Vertebrate Paleontology, 2023, 43(2): e1234567. DOI: 10.1080/02724634.2023.1234567 |
| `Vancouver` | ICMJE / numbered | Smith J, Jones A. A new theropod from the Morrison Formation. J Vertebr Paleontol. 2023;43(2):e1234567. |
| `MLA` | MLA 9th | Smith, John, and Anne Jones. "A new theropod from the Morrison Formation." *Journal of Vertebrate Paleontology*, vol. 43, no. 2, 2023, e1234567. |

## Required fields

Every citation must include, at minimum:

| Field | Source |
|-------|--------|
| Author(s) | CrossRef `author[].family`, `author[].given` |
| Year | CrossRef `issued.date-parts[0][0]` |
| Title | CrossRef `title[0]` |
| Container (journal/book) | CrossRef `container-title[0]` |
| DOI | CrossRef `DOI` |
| URL | CrossRef `URL` (when no DOI) |

## DOI handling

- Always render the DOI as a URL: `https://doi.org/<doi>` (HTTPS, lowercase scheme).
- Never invent a DOI — if CrossRef returns no `DOI`, render `URL` instead.
- Never strip the `10.` prefix.

## Multiple authors

| Author count | APA | GB/T 7714 |
|--------------|-----|-----------|
| 1 | `Smith, J.` | `Smith J` |
| 2 | `Smith, J., & Jones, A.` | `Smith J, Jones A` |
| 3-20 | full list, comma + `&` before last | full list, comma-separated |
| 21+ | first 19, `..., ` + last author (APA only) | `et al` after 3 in GB/T 7714 |

## No-fabrication rule

If you cannot find an authoritative citation for a claim, **say so explicitly**:

> "I could not find a peer-reviewed citation for X. The most cited related
> work is Y (DOI: ...). The user should verify before publishing."

Never invent author names, titles, journals, years, or DOIs.
