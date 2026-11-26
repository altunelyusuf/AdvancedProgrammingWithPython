# Lineage13 — chapter 16 release record and three-role review (2026-11-26)

Released versions: deck 4.0.0 (`03-materials/ch16/SEN0414_Ch16_SQLiteDatabases_3e_v4_0_0.pptx`, unchanged in this lineage; spec `08-tooling/ch16-deck/spec_v4_0_0`), chapter-code manifest 1.2.0 (unchanged), lecture export 4.0.0 (new), page 9.100.0 on template 9.55.0 (page A-box `sen0414_ch16_page_abox_v9_100_0.ttl`), page test 9.42.0. Earlier versions stay in the repository until the own-versions stage removes the older page drafts.

## What was measured (logs in `08-tooling/lineage13-opening/ch16/` for the deck, `08-tooling/lineage13-opening/ch16_page_9_100_0/` and `08-tooling/ch16-page/logs_v9_100_0/` for the page)
| Check | Result |
|---|---|
| Deck standard 1.3.0 | 13 of 13 pass (opening log; the deck file is unchanged) |
| Fit, layout, notes, overlap, reader notes, story prose | all clean; notes 68 to 105 words, median 82 (54 slides) |
| Balloons | 25 of 25 code slides carry two result balloons |
| Material check (deck and new page) | 8 of 8 pass: no prompt, no lambda (0 occurrences in the page), 72 of 72 code frames parse and are in the page |
| Page test 9.42.0 | 414 pass, 0 fail, widgets 100 of 100 |
| Page shapes (run-in-order menu) | conform (9 menu items, 6 tab rows, 25 examples); the phrase of the item occurs twice in the page |
| Story repeat | chapters 16 to 20 against all others: no repeat (`MEASURE_Lineage13_story_repeat_v1_0_0.md`) |
| Content compared with page 9.99.0 | 100 concepts, 25 examples, 6 stories, 14 resource links, 21 panels equal; two recorded paragraphs and the Lecture tab differ (below) |
| Version check | exit 0 |

## Faults found while doing it, and what was done
1. The Lecture tab of page 9.99.0 described a 26-slide deck; the deck has 54 slides. A new lecture export (4.0.0) was made for the 54-slide deck; 5 code slides are linked to a page concept (the manifest names book topics and only those with the same label as a page concept could be linked).
2. The rebuild records the two examples that cannot run in a browser (SqliteCli, PythonShell) under CPython 3.13.18 instead of the failed Pyodide attempt of 9.99.0, so two paragraphs changed their wording. No ruling forces this; it is the recording interpreter of the current page-data builder. Reported to the Owner; counted as 1 change for the objective ContentChanged.
3. The first measurement of the objective stage wrote that none of the five chapters has a spec folder; specs exist. Corrected by append in register 1.4.0.

## Three-role review
**Academician (accuracy).** The deck was not changed; notes and stories were read on slides 9 and 25 against the code and the real run, and the two recorded paragraphs now state the real result of the run. Verdict: accept.
**Faculty reviewer (the rulings).** One thing per slide; notes carry the lecture and speak to the reader; no everyday analogy, prompt or lambda in deck or page; run-in-order item present and conforming; content, stories and examples unchanged except the two paragraphs named above. Verdict: accept with the one noted change.
**Undergraduate reader.** Notes explain the short wordings in full sentences with links to related slides. Limit: slides were not read on a phone. Verdict: accept with that limit.

## Honest limits
The owner has not opened the deck or the page. Slides were rendered with LibreOffice, not PowerPoint (the deck is unchanged and was not re-rendered). Recorded Python is 3.13.18 (the book's 3.14.6 is not available). The page test used a test key. Resource links were not re-opened. Story-picture credit data was not re-checked. The register step script is the lineage's own tooling, a deviation from the rule that tool gaps go to BRSF; to be handed over with the others.
