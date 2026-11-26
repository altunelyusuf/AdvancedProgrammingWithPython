# Lineage14 — chapter 21 release record and three-role review (2026-11-26)

Released versions: deck 4.0.0 (`03-materials/ch21/SEN0414_Ch21_GraphsAndImages_3e_v4_0_0.pptx`, 40 slides, 15 code slides, 5 native charts), chapter-code manifest 1.0.0 (`03-materials/ch21/page/chapter_code_ch21_v1_0_0.json`, 15 examples), story-picture record `03-materials/ch21/assets/story_images_v1_0_0.json` with six pictures, lambda-free domain A-box 1.0.3, stories file 1.0.1, stand-in 1.0.2, lecture file 4.0.0 (40 slides, 15 linked to a concept), page 9.108.0 on template 9.55.0 (page A-box `sen0414_ch21_page_abox_v9_108_0.ttl`). Page 9.107.0 stays as the version before the lecture file was made.

## What was measured (logs in `08-tooling/ch21-deck/logs_v4_0_0/` and `08-tooling/lineage14-opening/ch21_page_9_107_0/`, `ch21_page_9_108_0/`)
| Check | Result |
|---|---|
| Deck standard 1.3.0 | 13 of 13 pass |
| Fit, layout, notes, overlap, reader notes, story prose | all clean |
| Material check (deck and page 9.108.0) | pass 8 of 8: no prompt, no lambda, 42 of 42 code frames parse and are in the page |
| Page test 9.42.0 | 9.108.0: 416 pass, 0 fail, widgets 89 of 89 (first run) |
| Page shapes | conform (89 sections, 9 menu items, 6 tab rows, 15 examples); 0 lambda |
| Lambda-free A-box | 61 of 61 results equal to 1.0.2 |
| Content compared with page 9.107.0 | only the lecture differs |
| Version check | exit 0 |
| Links | 14 of 15 resource links answered 200; the book's chapter page answered 429 |

## Faults found while doing it, and what was done
1. The first page test of 9.107.0 failed 6 features: plt.show() under the Agg backend prints a warning in a browser, which the recording had hidden. The example is shown as recorded (stand-in 1.0.2).
2. The second and third runs failed on an outside rate limit (HTTP 429) of the semantic-search model download and on one load-timing bound; nothing was changed and the test was run again; it passed on the third run. All three logs are kept.
3. The page's Lecture tab still described the first-version deck. A lecture file for deck 4.0.0 was made and the page rebuilt as 9.108.0, then tested again (416, 0).
4. The lambda-free rewrite handled lambdas with parameters (not only err(lambda)); the maker was written for that case.
5. The old stories file carried a personal address in its link-check header; the new file 1.0.1 uses a generic one.

## Three-role review
**Academician.** Printed results are quoted from the runs; stories dated and sourced. Verdict: accept.
**Faculty reviewer.** One thing per slide; reader-facing notes with slide links; no analogy, prompt or lambda; run-in-order item conforming. Verdict: accept.
**Undergraduate reader.** Plain slides and notes in full sentences. Limits: the clipboard example is emulated; recorded results for examples that need the book's files; slides not read on a phone. Verdict: accept with limits.

## Honest limits
The owner has not opened deck or page. Slides rendered with LibreOffice, not PowerPoint. The examples were run under Python 3.12.3 (deck) and 3.13.18 (page data) with Pillow 13.0.0 and Matplotlib 3.11.2, not under 3.14.6 and Pillow 12.3.0 of the first version. The page test used a test key. The book's own chapter page could not be re-read (HTTP 429) and the deck's "opened on 2026-11-26" holds for the other 14 links. The page resources tab and Q and A bank are those of the first version (unchanged). The lineage's own scripts (register step, planner, page-input maker, lambda-free A-box maker, lecture export) are to be handed over to BRSF. The deck shape follows the owner's decision of 2026-11-26 (same shape as chapters 12 to 20).
