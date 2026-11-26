# Lineage12 — chapter 12 release record and three-role review (2026-11-26)

Released versions: deck 3.2.0 (`03-materials/ch12/SEN0414_Ch12_CommandLinePrograms_3e_v3_2_0.pptx`, spec `08-tooling/ch12-deck/spec_v3_2_0`, builder 2.10.0), chapter-code manifest 1.3.0, lecture export 3.0.0, domain A-box 1.0.3 (no lambda), page 9.100.0 on template 9.55.0 (page A-box `sen0414_ch12_page_abox_v9_100_0.ttl`), page test 9.42.0. Earlier versions stay in the repository: deck 2.0.0, 3.0.0 and 3.1.0, manifests 1.0.0 to 1.2.0, pages up to 9.99.0.

## What was measured (logs in `08-tooling/lineage12-opening/ch12_deck_3_2_0/` and `08-tooling/ch12-page/logs_v9_100_0/`)
| Check | Result |
|---|---|
| Deck standard 1.3.0 | 13 of 13 pass |
| Fit, layout, notes, overlap, reader notes, story prose | all pass |
| Material check (deck and page) | 8 of 8 pass: no prompt, no lambda, every code frame parses, every code frame is in the page |
| Page test 9.42.0 | 414 pass, 0 fail, widgets 78 of 78 |
| Page shapes (run-in-order menu) | conforms |
| Story repeat check, chapters 1 to 25 | see `story_repeat_1_25.log`; the chapter 12 Ken Thompson name is read below |
| Content compared with deck 2.0.0 | 48 slides = 48, 23 examples with the same names, 4 stories with the same links and pictures, 14 resource links the same (`content_compare.log`) |
| Version check | exit 0 |

## Faults found while doing it, and what was done
1. First page build used a virtual-environment Python, so one example (Venv detection) recorded True. Rebuilt with the system Python; failed runs kept (`page_test_9_37_0.log`).
2. Page test 9.37.0 was the wrong base (stale: its exam step fails on every chapter, shown on chapter 17 as a control). New file 9.42.0 is made over 9.41.0.
3. Run-in-order makes nine top menu items; the standard allowed eight. 9.42.0 allows nine and says why. This is a rule conflict resolved in favour of the owner's explicit ruling; the width at 390 px passed the page test's adaptive check.
4. Seven example code groups were split inside `with`/`try`/`for` blocks, so frames did not parse alone. Regrouped (spec 3.1.0).
5. Reader-note errors found in review and corrected (spec 3.2.0): the snowstorm note described two rows combined into one block, which the code does not do; a pathlib claim about chapter 11 that was not checked.
6. The page's Lecture tab still carried the old deck's "Everyday pictures" notes. A lecture export from deck 3.2.0 (lecture_export 3.0.0) replaced it; the page now contains no such text.

## Ken Thompson overlap (chapter 12 against chapters 8, 9, 10)
Chapter 12 tells the 1973 pipe (McIlroy's 1964 memo, Version 3 Unix, the 1978 maxims; link Pipeline (Unix)). Chapter 8 tells the 1992 diner placemat, chapter 9 the 1968 regular-expression paper, chapter 10 the 1979 dbm and again the 1992 placemat. Different events, dates and links; only the person is shared. Recorded as a different story. Nothing is sent to the owner as a repeat candidate for chapter 12.

The run over chapters 1 to 25 also lists, outside this lineage's chapters and not acted on: one shared link, chapter 3 `WalrusPep572` and chapter 2 `WalrusLeads` (https://peps.python.org/pep-0572/, names Chris Angelico and Tim Peters), a repeat candidate that needs the owner's reading; and shared names only (Kernighan, Bell Labs, Sun Microsystems) in chapters 1, 5, 8, 18, 19. They go to the owner's attention in the lineage status report, not into chapters 12 to 15.

## Three-role review
**Academician (accuracy).** Story facts were compared with the chapter 12 story companion; dates, names and links agree. Two notes did not agree with the code or could not be checked and were corrected (faults 5). The example outputs quoted in notes were read against the real runs. Verdict: accept.
**Faculty reviewer (the rulings).** One thing per slide: deck standard D10 passes on all 38 content slides. Notes carry the lecture and speak to the reader (60 to 140 words; reader-note check passes; no presenter directions, no think-of). No everyday analogy anywhere in deck or page (box label IN SHORT; Lecture tab regenerated). Plain code without prompts or lambda, only taught Python. Run-in-order menu item present. The page tab that holds the slide code keeps its standard name Chapter code. Verdict: accept.
**Undergraduate reader.** Read the five In-short boxes, the notes of the first code slides and the practice slide: each short wording is explained in full sentences and points to related slides. One limit: the practice questions give no answers, as before. Verdict: accept with that limit stated.

## Honest limits
The owner has not opened the page or the deck. The browser examples run in Python 3.13 (Pyodide) while the recorded results are from Python 3.13.18; the book's 3.14.6 interpreter is not available in this workspace. The page test ran with a test key, not the instructor's.
