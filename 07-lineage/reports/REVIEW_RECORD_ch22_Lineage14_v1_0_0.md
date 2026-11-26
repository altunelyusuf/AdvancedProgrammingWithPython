# Lineage14 review record, chapter 22 (Reading Text from Images) — 2026-11-27

Reviewed: deck SEN0414_Ch22_ReadingTextFromImages_3e_v4_0_0.pptx (38 slides, 15 code slides, 6 native charts) and page 9.109.0 (100 widgets, 416 page-test features passed, 0 failed). Reviews are made by the building agent in three roles, not by independent people. Slides 15, 24 and 34 were looked at as renders; the others were checked by the deck checks and extracted text.

Four conditions: A content, B reader-facing slides, C code and page, D checks recorded before release.

| # | Role | Condition | Verdict | Basis |
|---|---|---|---|---|
| 1 | Academician | A | accept | the 15 printed results come from real Tesseract 5.3.4 under Python 3.12.3; the limits slide measures size, tilt, noise and repairs at build time; five stories are dated with a link, each picture sourced and licensed |
| 2 | Academician | B | accept | deck standard 1.3.0 passes; notes name only what the code or sources support |
| 3 | Academician | C | accept | all code frames parse; 73 A-box inputs rewritten without lambda with all results equal; pytesseract 0.3.13 shipped as a wheel so its two concept examples run in the browser |
| 4 | Academician | D | accept | every check has a log; the first two page-test runs failed (12, then 10 features) and are explained below |
| 5 | Faculty reviewer | A | accept | comparison with the first-version deck logged (26 to 38 slides; lambda or prompt occurrences 48 to 0) |
| 6 | Faculty reviewer | B | accept | reader-notes, story-prose, fit, layout, overlap clean; no analogy, prompt or lambda; code lines do not wrap |
| 7 | Faculty reviewer | C | accept | run-in-order menu item present; page A-box conforms to the page shapes |
| 8 | Faculty reviewer | D | accept | story-repeat control clean (best overlap 0.12); checks recorded before release |
| 9 | Undergraduate reader | A | accept | each result is explained before the next idea; plain words |
| 10 | Undergraduate reader | B | accept | short wordings explained in full sentences with links to related slides |
| 11 | Undergraduate reader | C | accept with limits | 14 of 15 chapter examples show recorded results because they need Tesseract, pdftotext or NAPS2; the screen examples draw their own screen |
| 12 | Undergraduate reader | D | accept with limits | owner has not opened deck or page; LibreOffice rendering only; test key; two GitHub resource links not checkable from this session (403 from the session's own access policy); reCAPTCHA picture only 250 by 47 px; Goldberg stone picture licence is Copyrighted free use |

Verdicts: 12 (accept 10, accept with limits 2).
