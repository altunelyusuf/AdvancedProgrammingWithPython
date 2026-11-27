# Lineage14 — chapter 23 release record and three-role review (2026-11-27)

Released: deck 4.0.0 (`03-materials/ch23/SEN0414_Ch23_KeyboardAndMouse_3e_v4_0_0.pptx`, 41 slides, 15 code slides, 4 native charts), chapter-code manifest 1.1.0, page 9.110.0, page A-box 9.110.0, domain A-box 1.0.3, lecture file 4.0.0, stories 2.0.0, builder 2.11.0. Reading of "21–25": the five incoming chapters; the early chapters follow after this lineage.

## What was measured (logs in `08-tooling/lineage14-opening/ch23_deck_4_0_0/` and `ch23_page_9_110_0/`)
| Check | Result |
|---|---|
| Deck checks (standard, fit, layout, notes, overlap, reader notes, story prose) | all zero |
| Material check (deck and page) | clean, no lambda on the page |
| Page test 9.42.0 on 9.110.0 | 416 pass, 0 fail, widgets 104 of 104 (first run on the final page) |
| Page shapes | conform |
| Lambda-free A-box | 74 of 74 equal |
| Story-repeat control | clean |
| Links | 13 of 14 answered 200; github.com/asweigart/pyautogui answered 403 from the session's access policy and could not be checked |
| Version check | exit 0 |

## Faults found, and what was done
1. Concept tables of three parts were longer than the slide (22, 17 and 21 rows). Each now runs over two slides and the builder has a new version (2.11.0) with a wider first column; the deck grew from 38 to 41 slides.
2. The cut, copy and paste story is also told in chapter 8. It was replaced by the Control-Alt-Delete story with a public-domain keyboard picture; the story-repeat control is clean.
3. The page carried 756 lambdas, all from the observer window of the lab helper (a Python program kept in a string). The A-box maker now rewrites them as defs; the 74 results stayed equal.
4. One A-box input measures a 1.5 s timeout and differed once under load; the maker now repeats both runs up to twice (no retry was needed in the final run).
5. The first A-box run compared both versions in one process and hung; each input now runs in its own process with a five-minute limit.

## Honest limits
Owner has not opened deck or page. LibreOffice rendering only. The examples ran on a private virtual display, never on a real screen, Windows or macOS. The page runs none of the 15 chapter examples and shows all as recorded. Story facts rest on the earlier sourcing, the Wikipedia page of Control-Alt-Delete read this session, and the live link check. The CAPTCHA story (the word, 2003) stands beside chapter 22's reCAPTCHA story (2009); the control found no overlap. The CAPTCHA picture is 290 by 80 px and its credit names no author. The deck has 41 slides against the agreed about 34 to 40. The page text of the lab helper differs from the lab file by the six lambdas. Build environments gained rdflib (via uv) in the chapter 23 interpreter.
