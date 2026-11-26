# Lineage14 — chapter 22 release record and three-role review (2026-11-27)

Released: deck 4.0.0 (`03-materials/ch22/SEN0414_Ch22_ReadingTextFromImages_3e_v4_0_0.pptx`, 38 slides, 15 code slides, 6 native charts), chapter-code manifest 2.1.0, page 9.109.0, page A-box 9.109.0, lecture file 4.0.0, pytesseract wheel record 9.109.0. Chapters 21 to 25 reading: "21–25" means the five incoming chapters; the early chapters follow after this lineage.

## What was measured (logs in `08-tooling/ch22-deck/logs_v4_0_0/` and `08-tooling/lineage14-opening/ch22_page_9_109_0/`)
| Check | Result |
|---|---|
| Deck checks (standard, fit, layout, notes, overlap, reader notes, story prose) | all zero |
| Material check (deck and page) | clean |
| Page test 9.42.0 on 9.109.0 | 416 pass, 0 fail, widgets 100 of 100 (third run) |
| Page shapes | conform |
| Lambda-free A-box | 73 of 73 equal |
| Story-repeat control | clean |
| Links | 5 of 5 story links and 13 of 15 resource links answered 200 (two 429 answers passed after waiting); 2 GitHub links not checkable here |
| Version check | exit 0 |

## Faults found, and what was done
1. Page test run 1: 12 features failed. Root cause: two concept examples import pytesseract, which a browser does not have. A pure-Python wheel (Apache-2.0, SHA-256 recorded) is now embedded; Pillow and packaging come from Pyodide.
2. Run 2: 10 features failed. Root cause: the build-time recording of the same two examples ran under an interpreter without pytesseract. The package was installed in the recording environment (disclosed environment change) and the page data rebuilt.
3. Run 3 passed: 416, 0.

## Honest limits
Owner has not opened deck or page. LibreOffice rendering only. Examples ran under Python 3.12.3 with Tesseract 5.3.4; the page data under 3.13.18. The page runs 1 of 15 chapter examples and shows the others as recorded. Story facts rest on earlier sourcing and the live link check, not on pages read this session. The Goldberg stone licence is Copyrighted free use; the reCAPTCHA picture is 250 by 47 px; no portrait of Luis von Ahn was obtained. Build environments gained rdflib, pyshacl, requests and pytesseract.
