# OCR outputs — provenance

Several source PDFs in `waves_paper_sources/` were scanned or had a broken font
encoding, so their text was not machine-readable. They were OCR'd here (tesseract
5.3.4, rendered via poppler `pdftoppm`) on 2026-07-29.

Filenames were harmonised on 2026-08-09 so each `.txt` sidecar shares the base
name of its source PDF (author-year/title form). The mapping below uses the
current names.

| Source PDF | Identity | Why OCR was needed | Text sidecar |
|---|---|---|---|
| `PNG_ProtectedAreasAct2024_scan.pdf` | **PNG Protected Areas Act 2024** | Scanned images, no text layer | `PNG_ProtectedAreasAct2024.txt` (+ searchable `PNG_ProtectedAreasAct2024_OCR.pdf`) |
| `Anderson2005_BismarckRamu_ChallengingICAD.pdf` | **Anderson (2005)** — *Challenging ICAD in PNG: the Bismarck Ramu Group* | CID-encoded font — normal extraction returns garbage | `Anderson2005_BismarckRamu_ChallengingICAD.txt` (+ searchable `..._OCR.pdf`) |
| `PNG_NationalForestPlan.pdf` | **PNG National Forest Plan (2012)**, PNGFA | Scanned images, no text layer | `PNG_NationalForestPlan.txt` (text only) |

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

| Source PDF | Identity | Text sidecar |
|---|---|---|
| `SauleiEllis1997_MotuporeICADConference.pdf` | **Saulei & Ellis (eds, 1997)** — *The Motupore Conference: ICAD Practitioners' Views from the Field* (2nd ICAD Conference, Motupore Island UPNG, 1–5 Sep 1997; DEC/UNDP PNG/93/G31) | `SauleiEllis1997_MotuporeICADConference.txt` |
| `McCallumSekhran1997_RaceForTheRainforest_i_CraterMountain.pdf` | **McCallum & Sekhran (1997)** — *Race for the Rainforest* (PNG Biodiversity [Conservation & Resource Mgmt] Programme) | `McCallumSekhran1997_RaceForTheRainforest_i_CraterMountain.txt` |
| `Ellis1999_RaceForTheRainforest_ii_CraterMountain.pdf` | **Ellis (1999)** — *Race for the Rainforest II* | `Ellis1999_RaceForTheRainforest_ii_CraterMountain.txt` |

Text-only sidecars (these are large grey-lit scans, not reading-pack items). Same
quotation-verification caveat applies. Identities of the two *Race* volumes to be
confirmed against their title pages before citing.
