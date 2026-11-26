# Lineage12 — chapter 13 release record and three-role review (2026-11-26)

Released versions: deck 3.1.0 (`03-materials/ch13/SEN0414_Ch13_WebScraping_3e_v3_1_0.pptx`, spec `08-tooling/ch13-deck/spec_v3_1_0`, builder 2.10.0), chapter-code manifest 1.2.0, slide-credit asset file `story_images_v3_0_0.json`, lecture export 3.1.0, domain A-box 1.0.4 (no lambda), page 9.102.0 on template 9.55.0 (page A-box `sen0414_ch13_page_abox_v9_102_0.ttl`), page test 9.42.0. Earlier versions stay in the repository: deck 2.0.0 and 3.0.0, manifests 1.0.0 and 1.1.0, A-box 1.0.3, page 9.96.0.

## What was measured (logs in `08-tooling/lineage12-opening/ch13_deck_3_1_0/` and `08-tooling/ch13-page/logs_v9_102_0/`)
| Check | Result |
|---|---|
| Deck standard 1.3.0 | 13 of 13 pass |
| Fit, layout, notes, overlap, reader notes, story prose | all pass |
| Material check (deck and page) | 8 of 8 pass: no prompt, no lambda (page: 0 occurrences, was 74), every code frame parses, every code frame is in the page |
| Page test 9.42.0 | 416 pass, 0 fail, widgets 94 of 94 |
| Page shapes (run-in-order menu) | conforms |
| Story repeat check | chapter 13 alone: clean; chapters 1 to 25: same single candidate as before (chapters 2 and 3, PEP 572), none in chapter 13; highest overlap of a chapter 13 story is 0.081 |
| Content compared with deck 2.0.0 | 51 slides = 51, 24 examples with the same names, 6 stories with the same links and pictures, 14 resource links the same; one example code changed (the lambda of the webbrowser example became a def) |
| Lambda-free A-box | 38 expressions (19 examples, label and input) rewritten; old and new results equal in all 38 |
| Version check | exit 0 |

## Faults found while doing it, and what was done
1. The register held the four chapter 13 stories but no tasks. The work was done and the tasks were written in the same register version that records it (1.11.0); this is the wrong order (work should reach the register first) and is recorded as a deviation, not as a pass.
2. Four result pictures overlapped the takeaway or the balloons (slides 18, 19, 22, 41). Their notes and sizes were changed in the visuals; fit and overlap checks then pass.
3. One code example had a function split over two code boxes, so the frame did not parse alone; regrouped. The webbrowser example held a lambda; now a plain def.
4. The builder refused a research concept without a plain-meaning row (Practice Programs); a row was added.
5. Story paragraphs of 31 to 38 words were refused by the 30-word limit; shortened without removing a fact.
6. The slide credits of four pictures (Reitz, the Tenniel picture, the Selenium and Playwright logos) were built by the chapter's old builder. The generic builder's fallback would have said "Wikimedia Commons" for pictures that do not come from there, so a new asset file records each credit as the old deck showed it.
7. Review found three statements in the notes that the sources do not support: why Requests was written (the notes said what had frustrated its author; the sources only list the words Frustration and Conception), that Playwright reacts "not to a timer" (not in the sources), and the ordinal of the first-spider story (it is the second story of the chapter). Corrected in spec 3.1.0; deck 3.0.0 was committed first and is superseded. A page 9.101.0 built on deck 3.0.0 was replaced before its test finished and was removed, because it was never committed or released.
8. The page's Lecture tab carried the old deck's "Everyday pictures" notes; a lecture export from deck 3.1.0 replaced it, and the page now contains no such text.

## Three-role review
**Academician (accuracy).** Story facts were compared with the chapter 13 draft and the old deck content (dates 30 June 1994, 1993, 13 and 14 February 2011, 2004, 30 September 2020 and 30 January 2020; counts 130, 2,738, 23,500 and 100,000; RFC 9309; versions 2.34.2, 3.14.5, 4.51.0, 1.63.0). Numbers named in the notes of the code slides were checked against the code and its real run; the only one not in them is the date 12 October 2026, which comes from the chapter research. Three notes did not agree with the sources and were corrected (fault 7). Verdict: accept.
**Faculty reviewer (the rulings).** One thing per slide: deck standard D10 passes on all 41 content slides. Notes carry the lecture and speak to the reader (63 to 95 words; reader-note check passes; no presenter directions, no think-of). No everyday analogy in deck or page (box label IN SHORT; Lecture tab regenerated). Plain code without prompts or lambda, only taught Python. Run-in-order menu item present and conforming. Content, stories and examples are unchanged except where a ruling forced a change (compare log). Verdict: accept.
**Undergraduate reader.** Read the eight In-short slides, the notes of the first code slides and the practice slide: each short wording is explained in full sentences and points to related slides. One limit: the practice questions give no answers, as before. Verdict: accept with that limit stated.

## Honest limits
The owner has not opened the page or the deck. The slides were rendered and looked at with LibreOffice, not PowerPoint. The browser examples run in Python 3.13 (Pyodide) while the recorded results are from Python 3.13.18; the book's 3.14.6 interpreter is not available in this workspace. The page test ran with a test key, not the instructor's. The chapter's third-party tools (requests, Beautiful Soup, Selenium, Playwright) are shown by standard-library stand-ins because a page cannot reach the web; no live site was fetched. The 14 resource links are those of deck 2.0.0 and were not re-opened in this session. The slide-credit data was reproduced from the old deck, not re-checked against the file pages of the pictures. The merge scripts that move register states are the lineage's own tooling, a deviation from the rule that tool gaps go to BRSF; it is to be handed over.
