# Chapter 7 deck review, version 1.0.0

Deck: `sen0414_ch07_deck_v1_0_0.pptx` (copy: `03-materials/ch07/SEN0414_Ch07_Dictionaries_3e_v1_0_0.pptx`), 26 slides, built by
`build_v1_0_0.sh python3.14 <out.pptx>` with the shared renderer `08-tooling/deck_render_v1_0_0.js`. Every console result,
program transcript, chart value and table cell is produced by `examples_run_v1_0_0.py` under Python 3.14.6 and re-produced
by the checks from the finished file.

## 1. The academician's notes

* The chapter's own claim that a dictionary has no first item is the one sentence the course corrects; slides 4, 5, 6 and 7
  carry the correction (insertion order since 3.7, equality that ignores order, the ruling of 15 December 2017, the 3.14
  wording of the unhashable error). Nothing else in the chapter was contradicted by the current language.
* The structure follows the corpus branches: type and keys (3-9), loops, counting and grouping (10-14), structuring data
  (15-19), copying and notation (20-22), practice and summary (23-26). The summary answers the five competency questions of
  the corpus, one line each.
* The chessboard is treated as a modelling lesson (what are the keys, what is absent) and not as a printing exercise; the
  board table on slide 17 is computed from the dictionary, which is the point the chapter makes about separating data from display.
* Two choices to be aware of. The birthday program is set on the slide with the same statements as the book's but with the
  dictionary on two lines and the comments set close, so that code and transcript can stand side by side at a readable
  size; it is recorded as such. The inventory practice program is shown, the validator is left to the course page's practice section,
  because 23 lines at 119 columns cannot be shown unwrapped with its output at a readable size.
* Licence: the book's own figure 7-2 is used with the credit "Sweigart (2025), Figure 7-2". The website states CC BY-NC-SA,
  the brief said CC BY-SA (see `03-materials/ch07/assets/ASSETS_PROVENANCE_v1_0_0.md`); the use is non-commercial teaching.

## 2. Expert checklist, with measured results

| check | result |
|---|---|
| slides | 26 (title, route, questions, 21 teaching slides, summary, resources, closing as a content slide) |
| agenda ranges exact and contiguous | 3-9, 10-14, 15-19, 20-22, 23-25 (asserted by the build; the closing slide is 26) |
| takeaway strip on every slide but the title | 25 of 25, each one full sentence of at most 24 words (asserted) |
| `deck_check_v1_0_0.py` | 49 console rows re-run, 1 chart and 1 table re-computed, 0 mismatches |
| `program_check_v1_0_0.py` | 9 program panels: slice verbatim, re-run equal, transcript on the slide, 0 mismatches |
| stale fixtures | 4 of 4 refused (console result, chart value, table cell by deck_check; program transcript by program_check) |
| `structure_check` | 0 paragraphs in an order PowerPoint would repair (453 misplaced elements removed by ooxml_fix) |
| `deck_layout_check` | clean: 0 overflowing frames, 0 shapes outside the slide, 0 slides without notes |
| `deck_fit_check` | 306 text frames measured, 0 overflowing, 0 overlapping |
| `deck_notes_check` | PASS, 26 of 26 slides with reader's prose (2,669 words of notes; 38 to 168 per slide) |
| code | no wrapped code; monospaced sizes 7.0 to 11 pt; every console carries "run under Python 3.14.6" or its program label does |
| charts | 1 native bar chart with data labels, taken from `Counter(message).most_common(8)` |
| stories | 4 true stories with fact rows (who, where, when, live link) and credited photographs: Van Rossum (CC BY-SA 4.0), Orwell (public domain), Staunton chess set (CC0), Crockford (CC0) |
| resources | 11 live links on slide 25, all in the chapter's `resources_v1_1_0.json`, opened on 2026-10-08 |
| analogies | phone book, coat-check ticket, shop window, tally marks, pigeonholes, seating chart, alias / shortcuts / photocopy |
| theme | one warm-ivory theme, no dark and light switching |

## 3. The undergraduate read-through

* Every slide can be read without its notes: the subtitle says what the slide shows, labels name each program and what a
  console demonstrates, and the takeaway strip says what to remember.
* Hardest slides for a first-year reader: slide 7 (hashing; the three boxes carry the rule and the console shows it) and slide 20
  (copying; the program prints 99, 99, 5 and True False, and the three boxes under it translate each into an everyday picture).
* The smallest text is the code on slides 14, 19 and 23 (7.0 to 7.6 pt), set by the long comment lines of the corpus programs;
  on a projector read those from the notes' wording and the page's Code Lab, which shows the same programs at full size.
* Slide 21 packs three ideas (JSON, TypedDict, match); it is the one slide a teacher might split in a longer session.
