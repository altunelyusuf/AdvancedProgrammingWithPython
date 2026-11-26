# Lineage12 — chapter 14 release record and three-role review (2026-11-26)

Released versions: deck 3.1.0 (`03-materials/ch14/SEN0414_Ch14_ExcelSpreadsheets_3e_v3_1_0.pptx`, spec `08-tooling/ch14-deck/spec_v3_1_0`, builder 2.10.0), chapter-code manifest 1.2.0, lecture export 3.1.0, domain A-box 1.0.4 (no lambda), page 9.104.0 on template 9.55.0 (page A-box `sen0414_ch14_page_abox_v9_104_0.ttl`), page test 9.42.0. Earlier versions stay in the repository: deck 2.0.0 and 3.0.0, manifests 1.0.0 and 1.1.0, A-box 1.0.3, pages 9.98.0 and 9.103.0 (9.103.0 was built on deck 3.0.0, tested and committed, then superseded).

## What was measured (logs in `08-tooling/lineage12-opening/ch14_deck_3_1_0/` and `08-tooling/ch14-page/logs_v9_104_0/`)
| Check | Result |
|---|---|
| Deck standard 1.3.0 | 13 of 13 pass (notes 60 to 115 words) |
| Fit, layout, notes, overlap, reader notes, story prose | all pass |
| Material check (deck and page) | 8 of 8 pass: no prompt, no lambda (page: 0 occurrences, was 191), every code frame parses, every code frame is in the page |
| Page test 9.42.0 | 416 pass, 0 fail, widgets 93 of 93 |
| Page shapes (run-in-order menu) | conforms |
| Story repeat check | chapter 14 alone: clean (highest overlap of a chapter 14 story 0.059); chapters 1 to 25: same single candidate as before (chapters 2 and 3, PEP 572), none in chapter 14 |
| Content compared with deck 2.0.0 | 51 slides = 51, 24 examples with the same names and the same code lines, 6 stories with the same links and pictures, 14 resource links the same; 48 everyday-picture rows became 48 plain-meaning rows |
| Lambda-free A-box | 7 expressions (14 literals, label and input) rewritten; old and new results equal in all 14 |
| Version check | exit 0 |

## Faults found while doing it, and what was done
1. The tasks reached the register BEFORE the work this time (register 1.12.0), and each stage moved its states in its own version (1.13.0, 1.14.0, 1.15.0, 1.16.0). The register was not corrected after the fact.
2. The builder refused a text box of 31 words, and two story paragraphs and two result pictures were too long or too tall; shortened or resized without removing a fact.
3. Three loops were split over two code boxes, so a box did not parse alone; each loop is now in one box (the code lines are unchanged).
4. The first deck checks failed deck standard D10 (three titles of fewer than four words), fit (two visual notes overlapped a balloon) and reader notes (four notes without a link to another slide, one phrase that points at an object); corrected, and all checks pass.
5. The page's Lecture tab was stale: it described an older deck of 26 slides. A lecture export for the 51-slide deck replaced it (46 slides linked to a concept).
6. The picture of the gene-name story is Figure 1 of the paper. The old deck cropped panel b; the generic builder has no crop, so the whole figure is shown, smaller and harder to read. Its credit text already described the whole figure.
7. Review found six statements in the notes that the code or the sources do not support: that read-only reading avoids creating cells; "three more parts" in the chart zip; that a file format keeps the bugs of its program in general; that volunteers "still" maintain openpyxl and that 3.1.5 is the newest release without a date (the PyPI page was opened on 2026-11-26 and agrees: 3.1.5, 28 June 2024; 1.1.0, 11 August 2010); that one Font object is shared on slides 37 and 38 (the code builds a new Font for each cell). Corrected in spec 3.1.0; deck 3.0.0 and page 9.103.0 were committed first and are superseded.

## Three-role review
**Academician (accuracy).** Story facts were compared with the chapter 14 draft and the old deck content (dates spring 1978, 8 October 1978, 1979, 2 May 1985, 30 September 1985, 19 November 1987, December 2005, December 2006, early 2008, 11 August 2010, 28 June 2024, 15 April 2013, 23 August 2016; counts 35,175, 18, 3,597, 987, 704, 19.6 percent; five countries; 2.2 against -0.1). Numbers named in the notes of the code slides were checked against the code and its real run; those not in them (114 MB and 11 MB, 72,865 rows, 629 of 23,757, 12 October 2026) come from the chapter research. Six notes did not agree with the code or the sources and were corrected (fault 7). Verdict: accept.
**Faculty reviewer (the rulings).** One thing per slide: deck standard D10 passes on all 42 content slides. Notes carry the lecture and speak to the reader (reader-note check passes; no presenter directions, no think-of). No everyday analogy in deck or page (box label IN SHORT; Lecture tab regenerated; the page holds no "Everyday pictures" text). Plain code without prompts or lambda, only taught Python. Run-in-order menu item present and conforming. Content, stories and examples are unchanged except where a ruling forced a change (compare log). Verdict: accept.
**Undergraduate reader.** Read the eight In-short slides, the notes of the first code slides and the practice slide: each short wording is explained in full sentences and points to related slides. Limits: the practice questions give no answers, as before; the gene-name picture is small (fault 6). Verdict: accept with those limits stated.

## Honest limits
The owner has not opened the page or the deck. The slides were rendered and looked at with LibreOffice (two slides), not PowerPoint. The browser examples run in Python 3.13 (Pyodide) while the recorded results are from Python 3.13.18; the book's 3.14.6 interpreter is not available in this workspace. The page test ran with a test key, not the instructor's. The 14 resource links are those of deck 2.0.0 and were not re-opened in this session (only the PyPI page was). The slide-credit data is that of `story_images_v2_0_0.json`, not re-checked against the file pages of the pictures. The merge scripts that move register states are the lineage's own tooling, a deviation from the rule that tool gaps go to BRSF; it is to be handed over.

## Correction appended after release
The release commit ead38e3 was pushed without the register: a command slip removed register 1.15.0 before 1.16.0 was written. Commit 8dd4594 restores it as 1.16.0 (the register comment says so). The repository held no live register for the time between the two commits.
