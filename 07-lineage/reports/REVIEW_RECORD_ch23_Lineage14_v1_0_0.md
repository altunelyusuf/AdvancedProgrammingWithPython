# Lineage14 review record, chapter 23 (Controlling the Keyboard and Mouse) — 2026-11-27

Reviewed: deck SEN0414_Ch23_KeyboardAndMouse_3e_v4_0_0.pptx (41 slides, 15 code slides, 4 native charts) and page 9.110.0 (104 widgets, 416 page-test features passed, 0 failed). Reviews are made by the building agent in three roles, not by independent people. Slides 1, 7, 13, 16, 24, 27, 28, 32, 38, 40 and 41 were looked at as renders; the others were checked by the deck checks and extracted text.

Four conditions: A content, B reader-facing slides, C code and page, D checks recorded before release.

| # | Role | Condition | Verdict | Basis |
|---|---|---|---|---|
| 1 | Academician | A | accept | the 15 printed results come from the real PyAutoGUI 0.9.54 under Python 3.14.6 on a private virtual X display; the quiet-surprise table is measured at build time; six stories are dated with a live link and each picture is sourced and licensed |
| 2 | Academician | B | accept | deck standard 1.3.0 passes; notes name only what the code or the sources support |
| 3 | Academician | C | accept | all code frames parse; 74 A-box inputs rewritten without lambda, all results equal (one timing input needed a retry rule); the observer window of the lab helper was rewritten without lambda too |
| 4 | Academician | D | accept | every check has a log; faults found on the way are listed in the release report |
| 5 | Faculty reviewer | A | accept | comparison with the first-version deck logged (26 to 41 slides; lambda or prompt occurrences to 0); the cut, copy and paste story was replaced because chapter 8 tells it |
| 6 | Faculty reviewer | B | accept | reader-notes, story-prose, fit, layout, overlap clean; no analogy, prompt or lambda; code lines do not wrap |
| 7 | Faculty reviewer | C | accept | run-in-order menu item present; page A-box conforms to the page shapes; the page carries no lambda |
| 8 | Faculty reviewer | D | accept | story-repeat control clean (best overlap 0.066); checks recorded before release |
| 9 | Undergraduate reader | A | accept | each result is explained before the next idea; plain words |
| 10 | Undergraduate reader | B | accept | short wordings are explained in full sentences with links to related slides |
| 11 | Undergraduate reader | C | accept with limits | all 15 chapter examples show recorded results, because a browser has no screen, mouse or keyboard to control; the page code of a concept example includes the lab helper text |
| 12 | Undergraduate reader | D | accept with limits | owner has not opened deck or page; LibreOffice rendering only; test key; the examples ran on a virtual display, never on a real screen, Windows or macOS; the GitHub link of PyAutoGUI could not be opened from this session (403 from the session's own access policy); the CAPTCHA picture is only 290 by 80 px and its credit names no author; the deck has 41 slides, one more than the agreed about 34 to 40 |

Verdicts: 12 (accept 10, accept with limits 2).
