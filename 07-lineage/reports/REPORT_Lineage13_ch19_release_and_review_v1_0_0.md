# Lineage13 — chapter 19 release record and three-role review (2026-11-26)

Released versions: deck 4.0.0 (`03-materials/ch19/SEN0414_Ch19_TimeScheduling_3e_v4_0_0.pptx`, 42 slides, 18 code slides), chapter-code manifest 1.2.0 (`03-materials/ch19/page/chapter_code_ch19_v1_2_0.json`), story-picture record `story_images_v1_1_0.json` with the new picture `image_y2038_commons.png`, lecture file `lecture_v4_0_0.json` (42 slides, 18 linked to a page concept), page 9.99.0 on template 9.55.0 (page A-box `sen0414_ch19_page_abox_v9_99_0.ttl`), page test 9.42.0. Deck 2.2.0, manifest 1.1.0 and page 9.98.0 stay as earlier versions (own-version rule); the own-versions stage removes older page drafts.

## What was measured (logs in `08-tooling/ch19-deck/logs_v4_0_0/`, `08-tooling/lineage13-opening/ch19_spec/`, `ch19_deck_4_0_0/` and `ch19_page_9_99_0/`)
| Check | Result |
|---|---|
| Deck standard 1.3.0 | 13 of 13 pass (18 of 18 code slides equal the manifest) |
| Fit, layout, notes, overlap, reader notes, story prose | all clean (42 slides, 42 with notes for the reader) |
| Balloons | 18 of 18 code slides carry two result shapes |
| Material check (deck and new page) | pass: no prompt, no lambda (0 in the page), 51 of 51 code frames parse and are in the page |
| Page test 9.42.0 | 416 pass, 0 fail, widgets 90 of 90 |
| Page shapes | conform (90 sections, 9 menu items, 6 tab rows, 18 examples); run-in-order phrase occurs twice, 0 lambda |
| Examples old and new | 18 of 18 code and expected printed results identical to deck 2.2.0 |
| Phrase scan | 0 hits in slide text and notes, 0 prompts, 0 lambda |
| Links | all 42 links of chapters 18 to 20 answer 200; the six story links of chapter 19 are Wikipedia pages and the notes say so |
| Content compared with page 9.98.0 | equal except version, chaptercode, lecture, stories and two recorded paragraphs |
| Version check | exit 0 |

## Faults found while doing it, and what was done
1. Six result visuals (slides 7, 8, 16, 19, 26, 27) overlapped the new result balloons; made lower in visuals 4.0.0.
2. Three concept slides had titles under four words; retitled.
3. One phrase ("as if") in a story sentence was found by the word search and reworded.
4. The Year 2038 story had a drawing made by the build script. A sourced picture was found and used: one frame of the public-domain animation "Year 2038 problem" by Monaneko on Wikimedia Commons, enlarged 2.4 times (400x130 to 960x312 px). It is a diagram, not a photograph, and is credited so on the slide.
5. The page data was recorded in an environment holding the wheels the page ships (tzdata 2026.5, pyperclip 1.11.0, playsound3 3.3.2, schedule 1.2.2); two recorded paragraphs (ClipboardAndSound, ZoneInfoZones) therefore show the real run instead of a missing-module message. No ruling forces this; counted as 2 changes for the objective ContentChanged.

## Three-role review
**Academician (accuracy).** Notes quote what the run printed; examples and printed results equal deck 2.2.0; the Year 2038 picture shows exactly the values of the first example. Verdict: accept.
**Faculty reviewer (the rulings).** One thing per slide; reader-facing notes with slide links; no analogy, prompt or lambda; two result balloons on every code slide; run-in-order item conforming; picture sourced and credited. Verdict: accept with the one noted change (two recorded paragraphs).
**Undergraduate reader.** Plain concept slides and notes in full sentences. Limit: slides were not read on a phone. Verdict: accept with that limit.

## Honest limits
The owner has not opened deck or page. Slides rendered with LibreOffice, not PowerPoint (three slides were looked at as images). Recorded Python is 3.13.18. Page test used a test key. Links answer 200; the six story links were not re-read against their content. The Year 2038 picture is low resolution. The lineage's own scripts (register step, planner, page-input maker, lecture export) are to be handed over to BRSF.
