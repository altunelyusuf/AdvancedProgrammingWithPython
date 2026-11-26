# Lineage12 — chapter 15 release record and three-role review (2026-11-26)

Released versions: deck 3.1.0 (`03-materials/ch15/SEN0414_Ch15_GoogleSheets_3e_v3_1_0.pptx`, spec `08-tooling/ch15-deck/spec_v3_1_0`, builder 2.10.0), chapter-code manifest 1.2.0, lecture export 3.1.0, domain A-box 1.0.5 (no lambda), pywheels 9.105.0 (boot code without lambda), page 9.106.0 on template 9.55.0 (page A-box `sen0414_ch15_page_abox_v9_106_0.ttl`), page test 9.42.0. Earlier versions stay in the repository: deck 3.0.0 (committed, superseded), manifests 1.0.0 and 1.1.0, A-box 1.0.4. Page 9.105.0 was built on deck 3.0.0, tested (PASS) and never committed except its logs (`logs_v9_105_0`); it was superseded before the page stage was committed.

## What was measured (logs in `08-tooling/lineage12-opening/ch15_deck_3_1_0/` and `08-tooling/ch15-page/logs_v9_106_0/`)
| Check | Result |
|---|---|
| Deck standard 1.3.0 | 13 of 13 pass |
| Fit, layout, notes, overlap, reader notes, story prose | all exit 0 |
| Material check (deck and page) | 8 of 8 pass: no prompt, no lambda (page: 0 occurrences), 57 of 57 code frames parse and are in the page |
| Page test 9.42.0 | 416 pass, 0 fail, widgets 95 of 95 |
| Page shapes (run-in-order menu) | conforms (9 menu items, 6 tab rows, 25 examples) |
| Story repeat check | chapter 15 alone: clean; chapters 1 to 25: the same single candidate as before (chapters 2 and 3, PEP 572), none in chapter 15 |
| Content compared with deck 2.0.0 | 53 slides = 53, 25 examples with the same names and code lines, 5 stories with the same links and pictures, 14 resource links the same, 66 analogy rows became plain-meaning rows |
| Lambda-free A-box | 12 literals rewritten; old and new results equal in all 12 |
| Version check | exit 0 |

## Faults found while doing it, and what was done
1. Deck standard D7 (one note under 60 words) and reader notes (slides 51 and 53 without a link to another slide) failed at first; notes extended.
2. Visual notes and charts overlapped result balloons on slides 10, 18, 26, 33, 34, 35, 40, 43 and 45; layouts compacted, no fact removed.
3. The register audit note said 62 rows where the log says 66; corrected before commit.
4. The A-box maker first did nothing under `--write` (an evaluated old expression changed `sys.argv`); fixed by capturing the arguments first. Page boot code held two lambdas inside an escaped string; replaced by two named functions, and the 9.105.0 test was stopped and the page rebuilt.
5. Review found five statements in the notes that the code or sources do not support (http.client and shlex "used by the projects"; "far more rows" in the real sheet; "the sheet offers no lock"; a bean_count claim that it ends the audit; the apiv3 request claim) and a wrong count (two bean totals wrong; only one). Corrected in spec 3.1.0; deck 3.0.0 and page 9.105.0 are superseded.
6. The generic builder knows no stand-in for Google, so a patch script adds the stand-in facts to the manifest; to be handed to BRSF with the other lineage tooling.
7. The lecture export had to be re-made for the 53-slide deck.

## Three-role review
**Academician (accuracy).** Notes were compared with the code and its recorded run; five unsupported statements were corrected (fault 5). Google was never reached: every example runs the real ezsheets library against the stand-in, and the slides say so. Verdict: accept.
**Faculty reviewer (the rulings).** One thing per slide; notes carry the lecture and speak to the reader; no everyday analogy, no prompt, no lambda in deck or page; run-in-order menu item present and conforming; content, stories and examples unchanged except where a ruling forced it. Slides 10 and 40 were rendered and looked at: text fits, charts and balloons do not overlap. Verdict: accept.
**Undergraduate reader.** Short wordings are explained in the notes with links to related slides. Limit: practice questions give no answers, as before. Verdict: accept with that limit.

## Honest limits
The owner has not opened the deck or the page. Slides were rendered with LibreOffice (three slides looked at), not PowerPoint. Recorded Python is 3.13.18 (the book's 3.14.6 is not available); the A-box old/new comparison also ran under 3.13. The page test used a test key. Resource links were not re-opened. Story-picture credit data was not re-checked. The merge and grooming scripts that move register states are the lineage's own tooling, a deviation from the rule that tool gaps go to BRSF; to be handed over. The page has nine menu items because of the run-in-order item; the owner may want eight.
