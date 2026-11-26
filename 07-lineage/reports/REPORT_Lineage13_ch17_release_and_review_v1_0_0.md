# Lineage13 — chapter 17 release record and three-role review (2026-11-26)

Released versions: deck 4.0.0 (`03-materials/ch17/SEN0414_Ch17_PDFAndWordDocuments_3e_v4_0_0.pptx`, unchanged in this lineage), chapter-code manifest 1.2.0 (unchanged), lecture file `lecture_v2_0_0.json` (59 slides, equals the deck; no new export), page 9.100.0 on template 9.55.0 (page A-box `sen0414_ch17_page_abox_v9_100_0.ttl`), page test 9.42.0. Earlier versions stay in the repository until the own-versions stage removes the older page drafts.

## What was measured (logs in `08-tooling/lineage13-opening/ch17/` for the deck, `08-tooling/lineage13-opening/ch17_page_9_100_0/` and `08-tooling/ch17-page/logs_v9_100_0/` for the page)
| Check | Result |
|---|---|
| Deck standard 1.3.0 | 13 of 13 pass (28 of 28 code slides equal the manifest; 0 of 311 code lines wrap) |
| Fit, layout, notes, overlap, reader notes, story prose | all clean; notes 66 to 114 words, median 83 (59 slides) |
| Balloons | 28 of 28 code slides carry two or more result shapes |
| Material check (deck and new page) | 8 of 8 pass: no prompt, no lambda (0 occurrences in the page), 71 of 71 code frames parse and are in the page |
| Page test 9.42.0 | 416 pass, 0 fail, widgets 95 of 95 |
| Page shapes (run-in-order menu) | conform (9 menu items, 6 tab rows, 28 examples); the phrase of the item occurs twice in the page |
| Story repeat | chapters 16 to 20 against all others: no repeat (`MEASURE_Lineage13_story_repeat_v1_0_0.md`) |
| Phrase scan | 0 hits in slide text and notes, 0 prompts, 0 lambda |
| Content compared with page 9.23.0 | all parts equal except two recorded paragraphs (below) |
| Version check | exit 0 |

## Faults found while doing it, and what was done
1. The first page build recorded the pypdf version of the local interpreter (6.17.0) while the page runs the wheel 6.20.1; the page test failed 8 features, all from that one value (the PackageNameTrap example). Cause: the page-data builder records with the interpreter it is given. Rebuilt with pypdf 6.20.1; the test then passed (416, 0 failed). The recorded value now equals the one of 9.23.0.
2. The rebuild records the two examples PdfminerAlternative and OptionalDependencyAes under CPython 3.13.18 instead of the Pyodide 3.13.2 wording of 9.23.0, so two paragraphs changed. No ruling forces this. Reported to the Owner; counted as 2 changes for the objective ContentChanged.

## Three-role review
**Academician (accuracy).** The deck was not changed; the two recorded paragraphs now state the real run, and the pypdf value is the version the page really runs. Verdict: accept.
**Faculty reviewer (the rulings).** One thing per slide; notes carry the lecture and speak to the reader; no everyday analogy, prompt or lambda in deck or page; run-in-order item present and conforming; content, stories and examples unchanged except the two paragraphs named above. Verdict: accept with the one noted change.
**Undergraduate reader.** Notes explain the short wordings in full sentences with links to related slides. Limit: slides were not read on a phone. Verdict: accept with that limit.

## Honest limits
The owner has not opened the deck or the page. Slides were rendered with LibreOffice, not PowerPoint (the deck is unchanged and was not re-rendered). Recorded Python is 3.13.18 (the book's 3.14.6 is not available). The page test used a test key. Resource links were not re-opened. Story-picture credit data was not re-checked. The register step script and the page-input script are the lineage's own tooling, a deviation from the rule that tool gaps go to BRSF; to be handed over with the others.
