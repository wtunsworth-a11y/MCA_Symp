# OCR outputs — provenance

Three source PDFs in `waves_paper_sources/` were scanned or had a broken font
encoding, so their text was not machine-readable. They were OCR'd here (tesseract
5.3.4, rendered via poppler `pdftoppm`) on 2026-07-29.

| Original | Identity | Why OCR was needed | Outputs |
|---|---|---|---|
| `504.pdf` | **PNG Protected Areas Act 2024** | Scanned images, no text layer | `504_ProtectedAreasAct2024.txt` + `504_ProtectedAreasAct2024_OCR.pdf` (searchable) |
| `201_challenging.pdf` | **Anderson (2005)** — *Challenging ICAD in PNG: the Bismarck Ramu Group* | CID-encoded font — normal extraction returns garbage | `201_Anderson2005_BismarckRamu.txt` + `201_Anderson2005_BismarckRamu_OCR.pdf` (searchable) |
| `National Forest Plan.pdf` | **PNG National Forest Plan (2012)**, PNGFA | Scanned images, no text layer | `NationalForestPlan2012.txt` (text only) |

**Notes**
- The `.txt` sidecars are the working text used for grounding the Waves paper. OCR
  is ~99% clean; expect occasional header/marginalia artefacts (e.g. stray
  characters at page tops). **Verify any direct quotation against the page image
  before it goes in a deliverable** — no OCR'd text is quoted without that check.
- Searchable PDFs are re-rasterised (JPEG @200 dpi) with a hidden text layer, so
  they are larger than the originals. Provided for the two sources destined for the
  **symposium reading pack** (PA Act 2024, Anderson 2005).
- The National Forest Plan searchable PDF (~24 MB) was **not committed** — it is not
  part of the reading pack, and its text sidecar covers the drafting need. It can be
  regenerated on request.

## Added 2026-07-29 (large scans pushed via git)

| Original | Identity | Output |
|---|---|---|
| `The Motupore.pdf` | **Saulei & Ellis (eds, 1997)** — *The Motupore Conference: ICAD Practitioners' Views from the Field* (2nd ICAD Conference, Motupore Island UPNG, 1–5 Sep 1997; DEC/UNDP PNG/93/G31) | `Motupore.txt` |
| `Race for the Rainforest.pdf` | **McCallum & Sekhran (1997)** — *Race for the Rainforest* (PNG Biodiversity [Conservation & Resource Mgmt] Programme) | `RaceForTheRainforest_i.txt` |
| `Race for the Rainforest ii.pdf` | **Ellis (1999)** — *Race for the Rainforest II* | `RaceForTheRainforest_ii.txt` |

Text-only sidecars (these are large grey-lit scans, not reading-pack items). Same
quotation-verification caveat applies. Identities of the two *Race* volumes to be
confirmed against their title pages before citing.
