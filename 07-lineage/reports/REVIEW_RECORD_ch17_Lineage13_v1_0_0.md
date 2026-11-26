# Lineage13 review record, chapter 17 (PDF and Word Documents) — 2026-11-26

Reviewed: deck SEN0414_Ch17_PDFAndWordDocuments_3e_v4_0_0.pptx (59 slides, 28 code slides, unchanged) and page 9.100.0 (71 code frames, 95 widgets, 416 page-test features passed, 0 failed). Reviews are made by the building agent in three roles, not by independent people. Evidence: `08-tooling/lineage13-opening/ch17/`, `08-tooling/lineage13-opening/ch17_page_9_100_0/`, `08-tooling/ch17-page/logs_v9_100_0/` and the release record `REPORT_Lineage13_ch17_release_and_review_v1_0_0.md`.

Four conditions: A content unchanged beyond a ruling; B reader-facing slides (one thing per slide, notes); C code and page (no prompt, no lambda, runs in order); D checks recorded before release.

| # | Role | Condition | Verdict | Basis |
|---|---|---|---|---|
| 1 | Academician | A | accept | two recorded paragraphs now show the real run; the pypdf value equals the wheel the page runs |
| 2 | Academician | B | accept | deck standard 1.3.0 passes 13 of 13; notes name only what code or sources support |
| 3 | Academician | C | accept | all 71 frames parse; examples run and the printed results are those on the slides |
| 4 | Academician | D | accept | every check has a log; the page test is 0 failed after the one rebuild |
| 5 | Faculty reviewer | A | accept with note | content compare log: everything equal except two recorded paragraphs (recording interpreter) |
| 6 | Faculty reviewer | B | accept | reader-notes and story-prose checks clean; phrase scan 0 hits; two or more result shapes on 28 of 28 code slides |
| 7 | Faculty reviewer | C | accept | no prompt, no lambda (0 occurrences in the page); run-in-order menu item present, page shape conforms |
| 8 | Faculty reviewer | D | accept | checks and reviews recorded before release in the release record and register |
| 9 | Undergraduate reader | A | accept | stories and examples read as before; nothing new to learn first |
| 10 | Undergraduate reader | B | accept | each short wording is explained in full sentences in the notes with links to related slides |
| 11 | Undergraduate reader | C | accept | every code frame is in the page and runs; plain code, no prompts |
| 12 | Undergraduate reader | D | accept with limits | the owner has not opened deck or page; slides were rendered with LibreOffice only; page test used a test key |

Verdicts: 12 (accept 9, accept with note or limits 3).
