# Lineage13 — chapter 20 release record and three-role review (2026-11-26)

Released versions: deck 4.0.1 (`03-materials/ch20/SEN0414_Ch20_EmailTextsPushNotifications_3e_v4_0_1.pptx`, 42 slides, 19 code slides), chapter-code manifest 1.2.1 (`03-materials/ch20/page/chapter_code_ch20_v1_2_1.json`) and the page manifest 1.2.2 derived from it (1.2.1 plus the "recorded" markers that 1.0.2 carried on 8 examples and the note on the control example), story-picture record `story_images_v1_1_0.json` with the new picture `image_att_commons.jpg`, lecture file `lecture_v4_0_1.json` (42 slides, 21 linked to a page concept), page 9.101.0 on template 9.55.0 (page A-box `sen0414_ch20_page_abox_v9_101_0.ttl`), page test 9.42.0. Deck 4.0.0, deck 2.0.1, manifests 1.2.0 and 1.0.2 and page 9.100.0 stay as earlier versions (own-version rule); the own-versions stage removes older page drafts.

## What was measured (logs in `08-tooling/ch20-deck/logs_v4_0_0/`, `logs_v4_0_1/`, `08-tooling/lineage13-opening/ch20_spec/`, `ch20_deck_4_0_0/`, `ch20_deck_4_0_1/` and `ch20_page_9_101_0/`)
| Check | Result |
|---|---|
| Deck standard 1.3.0 | 13 of 13 pass on deck 4.0.1 (19 of 19 code slides equal the manifest) |
| Fit, layout, notes, overlap, reader notes, story prose | all clean (42 slides, 42 with notes for the reader) |
| Balloons | 19 of 19 code slides carry two result shapes |
| Material check (deck and new page) | pass 8 of 8: no prompt, no lambda (0 in the page), 58 of 58 code frames parse and are in the page |
| Page test 9.42.0 | 416 pass, 0 fail, widgets 91 of 91 |
| Page shapes | conform (91 sections, 9 menu items, 6 tab rows, 19 examples); run-in-order phrase occurs twice, 0 lambda |
| Examples old and new | 19 of 19 code and expected printed results identical to deck 2.0.1 (manifest 1.0.2), to manifest 1.2.0 and to manifest 1.2.1 |
| Phrase scan | 0 hits in slide text and notes, 0 prompts, 0 lambda |
| Links | all 42 links of chapters 18 to 20 answered 200 when checked; the story links of chapter 20 are Wikipedia pages, the RFC Editor page of RFC 821 and AT&T's support page |
| Content compared with page 9.100.0 | equal except version, chaptercode, lecture and stories; no concept node differs |
| Version check | exit 0 |

## Faults found while doing it, and what was done
1. Four result visuals (slides 18, 19, 26, 37) were too tall for the result balloons; made lower in visuals 4.0.0 (the segments visual now has a three-row table and a smaller chart).
2. The summary slide held a text of 31 words (limit 30); shortened. The title of the concept slide of part 5 had three words; lengthened.
3. The concept tables of parts 1 and 5 left the slide with 10 and 9 rows; the plain explanations were shortened to one line each.
4. The AT&T story had a drawing made by the build script. A sourced picture was found and used: the photograph "An AT&T wireless retail store in Asheville, North Carolina 01" by Harrison Keely, CC BY 4.0, Wikimedia Commons, taken 6 May 2025. It shows a shop front, not the service, and the note says so. Because deck 4.0.0 was already committed, the change is deck 4.0.1 and manifest 1.2.1.
5. The first page build recorded google-api-python-client 2.202.0 in one recorded paragraph, while the chapter research names 2.201.0. The recording environment was pinned to 2.201.0 and the page was rebuilt and re-tested; the final content compare shows no differing concept node.

## Three-role review
**Academician (accuracy).** Notes quote what the run printed; the 19 examples and printed results equal deck 2.0.1; the photograph is sourced with its licence and date. Verdict: accept.
**Faculty reviewer (the rulings).** One thing per slide; reader-facing notes with slide links; no analogy, prompt or lambda; two result balloons on every code slide; run-in-order item conforming; the story picture is real and credited. Verdict: accept.
**Undergraduate reader.** Plain concept slides and notes in full sentences. Limit: slides were not read on a phone. Verdict: accept with that limit.

## Honest limits
The owner has not opened deck or page. Slides rendered with LibreOffice, not PowerPoint (one slide was looked at as an image). Recorded Python is 3.13.18. Page test used a test key. The story links were not re-read against their content. Eight examples that need ezgmail or a local mail server show recorded results on the page, as in earlier page versions. The AT&T photograph is the 1280 by 960 px rendering that Commons serves and shows a shop front. The lineage's own scripts (register step, planner, page-input maker, lecture export) are to be handed over to BRSF.
