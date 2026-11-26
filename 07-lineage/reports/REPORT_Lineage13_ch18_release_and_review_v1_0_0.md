# Lineage13 — chapter 18 release record and three-role review (2026-11-26)

Released versions: deck 4.0.1 (`03-materials/ch18/SEN0414_Ch18_CSVJSONXML_3e_v4_0_1.pptx`, 53 slides, 27 code slides), chapter-code manifest 1.2.1 (`03-materials/ch18/page/chapter_code_ch18_v1_2_1.json`), lecture file `lecture_v4_0_1.json` (53 slides, 27 linked to a page concept), page 9.102.0 on template 9.55.0 (page A-box `sen0414_ch18_page_abox_v9_102_0.ttl`), page test 9.42.0. Deck 4.0.0, manifest 1.2.0 and page 9.101.0 were committed first and stay as earlier versions (own-version rule); the own-versions stage removes older page drafts.

## What was measured (logs in `08-tooling/ch18-deck/logs_v4_0_1/`, `08-tooling/lineage13-opening/ch18_deck_4_0_1/` and `08-tooling/lineage13-opening/ch18_page_9_102_0/`)
| Check | Result |
|---|---|
| Deck standard 1.3.0 | 13 of 13 pass (27 of 27 code slides equal the manifest; 0 of 230 code lines wrap) |
| Fit, layout, notes, overlap, reader notes, story prose | all clean (53 slides, 53 with notes for the reader) |
| Balloons | 27 of 27 code slides carry two result shapes |
| Material check (deck and new page) | pass: no prompt, no lambda (0 in the page), 72 of 72 code frames parse and are in the page |
| Page test 9.42.0 | 414 pass, 0 fail, widgets 95 of 95 |
| Page shapes | conform (95 sections, 9 menu items, 6 tab rows, 27 examples); run-in-order phrase occurs twice, 0 lambda |
| Examples old and new | 27 of 27 code and printed results identical to deck 3.0.0 |
| Phrase scan | 0 hits in slide text and notes, 0 prompts, 0 lambda |
| Links | all 42 links of chapters 18 to 20 answer 200 |
| Content compared with page 9.101.0 | equal except version, lecture and chaptercode (three corrected sentences) |
| Version check | exit 0 |

## Faults found while doing it, and what was done
1. First deck builds changed manifest 1.1.0 in place; restored from git and built as manifest 1.2.0.
2. Result visuals overlapped the result balloons on six slides; visuals compacted, title of example A4 shortened.
3. The link check showed three note sentences with a wrong description of a linked page (heise article, post by Eli Bendersky) and one slide reference; corrected as notes 4.0.1, deck 4.0.1, manifest 1.2.1, page 9.102.0.
4. Page data recorded with the chapter wheels (xmltodict 1.0.4, defusedxml 0.7.1, openpyxl 3.1.5), the versions the page runs.

## Three-role review
**Academician (accuracy).** Notes describe what the linked pages really are; examples and printed results equal the earlier deck. Verdict: accept.
**Faculty reviewer (the rulings).** One thing per slide; reader-facing notes with slide links; no analogy, prompt or lambda; two result balloons on every code slide; run-in-order item conforming. Verdict: accept.
**Undergraduate reader.** Plain concept slides and notes in full sentences. Limit: slides were not read on a phone. Verdict: accept with that limit.

## Honest limits
The owner has not opened deck or page. Slides rendered with LibreOffice, not PowerPoint. Recorded Python is 3.13.18. Page test used a test key. Links answer 200 but only the chapter 18 story links were read against their content. One story picture of chapter 18 (image_etheader) is a drawing made for the deck, with no outside source; recorded for the Owner. The lineage's own scripts (register step, page-input maker, link measure, lecture export) are to be handed over to BRSF.
