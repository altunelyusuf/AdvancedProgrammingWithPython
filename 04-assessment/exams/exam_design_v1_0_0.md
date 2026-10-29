# SEN0414 printed exams: design of the paper (version 1.0.0)

Task TK4_Design. Machine-readable twin: `04-assessment/exams/exam_design_v1_0_0.json` (47 decisions, each with a reason). The engine and the grading tool are built from these two files. Nothing under 03-materials is changed.

Scope (the Owner's statements of 2026-10-29 and 2026-10-30): two papers, midterm and make-up; chapters 1, 2, 3, 4, 6, 7, 8 (chapter 5 out); 60 minutes each; physical printed paper; a printed answer key per paper; no QTI, no CATS export, no interactive HTML.

## 0. Assumptions (marked A, each easy to change)

| No | Assumption | Where it sits |
|---|---|---|
| A1 | Bloom reading is "Apply and up" (levels 3 to 6). With "Analyze and up" the plan gives 11 of 30 (37 per cent) and fails | `blueprint.share_apply_or_above` |
| A2 | 30 items per paper | `blueprint.items` |
| A3 | Items per chapter 4, 5, 5, 5, 4, 4, 3 (proportional to bank sizes 109, 131, 143, 142, 123, 122, 69, largest remainder) | `blueprint.chapters` |
| A4 | Two short items per paper, hand-marked, rubric of at most 3 points | `blueprint.types.short` |
| A5 | No negative marking | grading key rule |
| A6 | Times per item: 60 s plain mcq, 100 s mcq with code, 240 s match, 120 s order, 60 s code blank, 45 s sentence cloze, 120 s predict, 240 s short (the short and code-blank values are this design's own) | section 4 |
| A7 | Fill thresholds 45 per cent (filled) and 15 per cent (empty) of the read area | section 9 |
| A8 | At least 9 cross-chapter items and 6 indirect items per paper | section 5 |
| A9 | Two forms (A, B) per paper | section 7 |

## 1. What is reused and what is new

Reused:
- the exam-kind idea and the 17 type names of the pages' engine (`08-tooling/course_page_template_v9_52_4.html`, `XEXAM`: kind, minutes, preferred levels, mix of types; `08-tooling/template_exam_v9_19_0.js`);
- the newest chapter banks as seeds only (`08-tooling/ch01-page/question_bank_v1_1_1.json`, `ch02-page/question_bank_v1_1_1.json`, `ch03-page/question_bank_v1_1_1.json`, `ch04-page/question_bank_v1_1_1.json`, `ch06-page/question_bank_v2_0_0.json`, `ch07-page/question_bank_v1_1_0.json`, `ch08-page/question_bank_v1_0_0.json`): 839 items, 357 (42.5 per cent) at Apply or Analyze, none at Evaluate or Create. Seeds, never exam items (Owner's ruling of 2026-10-30);
- the weight of the midterm (30 per cent) from `04-assessment/sen0414_assessment_v1_0_0.ttl`;
- the chapter-code manifests (`03-materials/chNN/page/chapter_code_chNN_v1_0_0.json`) as the list of listings the students have seen.

Not reused: the Exam desk (`08-tooling/sen0414_exam_desk_v2_2_0.html`), the release tool (`08-tooling/sen0414_exam_release_v1_0_0.py`) and the page engine's question generation (typed answers, timer, locked result, release code: all screen flow).

New: the item model with seed link; the near-copy measure; the general assembler across chapters; the printed layout, key and answer sheet; the reading and grading method.

## 2. Item model

One record per item. All fields are checkable by a tool.

| Field | Meaning | Rule |
|---|---|---|
| id | unique key of the item | unique across both papers |
| chapters | list of chapters it needs | at least one of 1, 2, 3, 4, 6, 7, 8; synthesis items list two or more |
| source | links to the course | at least one of deck slide, speaker note, corpus passage, story; each must exist |
| bloom | level 1 to 6 | integer |
| critical_point | the point it tests | text of the entry named in course_point |
| course_point | link to the critical-points list | `<file>#<position from 0>`, at least one. The files are made by TK4_Points_A and TK4_Points_B; their names were not known when this was written |
| seed_item | the page item it grew from | `<bank path>#<position from 0>` or `none` |
| type | one kept type | mcq, match, order, blank, cloze, predict, short |
| stem | the question | listing at most 12 lines, no wrapped line |
| options_or_blanks | options A to D, or numbered bank and gaps | no overlap, similar length, no "all/none of the above" |
| answer | the key | letter, digits, bank numbers, order, or rubric |
| points | number | per section 9 |
| reason | one sentence why the answer is right | printed in the key |
| indirect_form | consequence, exception, reason or none | required when the item is indirect |
| code_width | declared width in characters | 45 (two columns) or 90 (one column) |
| bank_id | the shared bank a blank or cloze draws from | |

### 2.1 Near-copy measure (the Owner's ruling, point b)
- Text of an item = stem, code and options joined. Words = lower-case runs of letters, digits and underscore.
- C(new, seed) = share of the new item's 4-word sequences that also occur in the seed.
- Near copy when C is at least 0.50 and the correct answers are equal as normalised text, or when C is at least 0.80 whatever the answer. Checked against every seed in the seven banks, every listing in the seven chapter-code manifests (a listing identical after whitespace is a copy unless a changed case alters its output), and between the two papers.
- Why this measure. Measured on the 839 items (351,541 pairs): the 99.9th percentile of C between different items is 0.273 (one direction) and the largest is 0.733 (two stems that share a code template, different answers). Over both directions only one pair reaches 0.50 with the same answer text and none reaches 0.80. A stem-only measure was rejected: many stems are the same short template ("what does this program print?").
- Fixture with known answers, computed with the method (seed: "Which statement about values in Python is correct?" with its four options, key A):

| Variant | C | Same answer text | Verdict |
|---|---|---|---|
| identical | 1.000 | yes | near copy |
| one word of the stem changed ("true" for "correct") | 0.942 | yes | near copy |
| stem rewritten, options kept | 0.871 | yes | near copy |
| stem rewritten, two options swapped, key moved | 0.786 | yes | near copy |
| new angle: a claim about `x = 3 * 'ab'`, four new options | 0.000 | no | not a copy |

The tool built later must print these five values. A SHACL rule and its fixture are built from this table later.

### 2.2 Enhancement iteration (point c)
A seed becomes an exam item by changing at least one of: a new angle (same critical point from the other side, e.g. the consequence for the definition); a cross-chapter link (a second chapter's idea is needed); a reasoning step (two steps or a reason, not recall); a changed code case (a different listing whose output differs). The change is recorded in the item, the near-copy measure must pass, and the course_point stays.

## 3. Types for print (the 17 types)

| Type | Verdict | Printed form and reason |
|---|---|---|
| mcq | kept | A to D, one letter; also combination-of-statements, find-the-faulty-line (line numbers), compare-two-designs |
| match | kept | 5 premises to 8 answers A to H; 1 point per premise |
| order | kept | 4 steps or code lines; row per position; 1 point per position |
| blank | kept | code gap, shared numbered bank; bank number marked |
| cloze | kept | sentence gap, shared numbered bank |
| predict | kept | choose one of 4 printed outputs, or a number of up to two digits with sign |
| short | kept | back of the answer sheet, hand-marked, rubric at most 3 points, at most 2 per paper |
| multi | dropped | penalty scheme; idea moves into mcq combinations |
| judge | dropped | 50 per cent guess; idea moves into "which statement is true" |
| repair | dropped | needs a screen to edit and run; moves into mcq about a numbered listing |
| program, write | dropped | code on paper is not enabled: no rubric, no named marker (if enabled later: the paper names it, a rubric of at most 3 points, the instructor marks) |
| string, graph, object, ask, sparql | dropped | need a screen, typed text or a live endpoint |

## 4. Code on paper
- Listing: at most 12 lines, no wrapped line, 9 point monospace; declared width 45 characters (two columns) and 90 (one column); too long means shortened, never wrapped. Lines are numbered when a question refers to a line.
- Code tasks kept: predict the output, find the faulty line, complete a gap from the bank, order the lines.
- Output options are written as Python prints them: text without quotes; list `[1, 2]`; dictionary `{'a': 1}`; repr of text with quotes; two lines of output as two lines in the option. No two options differ only in a space.
- Exact match applies only to the optional hand case (not enabled by default): whole line, quotes, comma-space and line breaks significant, trailing space not.
- Numeric answers: results of expressions, counts of loop passes, lengths, indexes (the sign cell covers negative indexes). No money or fee arithmetic.

## 5. Blueprint of one paper (midterm and make-up alike)

| Type | Items | Seconds each | Seconds | Points each | Points | Reading |
|---|---|---|---|---|---|---|
| mcq plain | 8 | 60 | 480 | 3 | 24 | letter |
| mcq with code | 6 | 100 | 600 | 3 | 18 | letter |
| match | 2 | 240 | 480 | 5 | 10 | 5 rows A to H |
| order | 2 | 120 | 240 | 4 | 8 | 4 rows A to D |
| blank | 3 | 60 | 180 | 3 | 9 | 3 gaps each |
| cloze | 2 | 45 | 90 | 3 and 2 | 5 | 3 and 2 gaps |
| predict | 5 | 120 | 600 | 4 | 20 | 3 by letter, 2 by digits |
| short | 2 | 240 | 480 | 3 | 6 | by hand |
| Total | 30 | | 3150 s = 52.5 min (87.5 per cent of 60; limit 90 per cent = 3240 s) | | 100 | |

- Chapters (first chapter of the item): 1:4, 2:5, 3:5, 4:5, 6:4, 7:4, 8:3 = 30.
- Bloom (A1): Remember 2, Understand 7, Apply 10, Analyze 7, Evaluate 3, Create 1 = 30; levels 3 to 6 = 21 (70 per cent). Evaluate: mcq judging two designs or programs, and one short item. Create: one short item.
- Letters: 17 lettered items (14 mcq and 3 predict) A 5, B 4, C 4, D 4; no letter is the key of four items in a row; holds again for each form after shuffling.
- Cross-chapter: at least 9 items name two or more chapters; synthesis items are among them. Indirect items (consequence, exception, reason): at least 6, each with indirect_form.
- Banks: one shared bank per part (blank: 11 entries for 9 gaps; cloze: 7 entries for 5 gaps, at most 12). Order is a seeded permutation, the seed stored in the build record; gaps of one item have different keys; no bank number is the key of three gaps in a row; the bank is never in gap order.
- Pair: the make-up repeats no item of the midterm (no equal id, no pair at the near-copy level); a critical point may recur through a different item.
- Item order: five parts by type (choice, trace, bank fill-in, match and order, short); positions 1 to 30 run through the paper and are the numbers on the sheet. Instructions per part are printed once.

## 6. Saving pages
Two columns of A4, margins 12 mm, body 10 point or more, code 9 point, black on white without shading; a listing printed once and shared by the items that refer to it; no answer space on the paper (answers go to the sheet); no name or number printed. Estimate: about 370 lines (56 plain mcq, 102 mcq with code, 28 match, 20 order, 43 bank items, 75 predict, 20 short, 25 for page 1) at about 112 lines per page = 3.3 pages, so **4 paper pages (2 sheets, both sides) and 1 answer sheet (both sides): 6 pages, 3 sheets per student.** An estimate: the first build must report the real count, and more than 4 paper pages is a failure of this design.

## 7. Answer sheet and geometry
- A4 portrait, both sides; the back is ruled for the two short answers. Two forms A and B per paper: same items in different order inside blocks of equal type, options reordered; the type of every position is equal across forms, so one layout serves both.
- Corner markers (mm, page 210 by 297): solid 8 by 8 squares centred at (14, 14), (196, 14), (14, 283); a hollow square (8 outside, 3 hole) at (196, 283), which tells an upright sheet from a turned one. Four markers allow a projective correction of a photograph.
- Cells: bubble 4.5 mm, pitch 7.0 across and 6.5 down, read area the inner 3.0 mm. Scan or photo: 300 dpi target, 200 dpi least (at 200 dpi the read area is about 24 pixels across).
- Header (20 to 55 mm): version strip of 12 cells, three digit rows for the paper check number, two calibration cells (one empty, one filled, pre-printed), the student-ID line of 80 mm.
- Fields from 56 to 275 mm in two columns; cells start at x 32 mm (left) and x 120 mm (right); item number at the left of each row. Rows: 17 choice (A to D), 6 digit rows (0 to 9: tens, ones, sign), 10 match (A to H), 8 order (A to D), 9 blank and 5 cloze (bank numbers 1 to 12) = 55 rows in 33 rows per column with headings.
- The engine writes a layout file giving each position's cells in mm; the reader reads that file and does not guess.
- Version mark: strip cells 1 kind (0 midterm, 1 make-up), 2 form (0 A, 1 B), 3 to 8 paper version in binary, 9 even parity over 1 to 8, 10 to 12 empty. The same is printed in words in each page footer of the paper. The check number on page 1 of the paper (three digits derived from kind, form and version) is filled by the student into the digit rows, so a sheet is tied to its paper. A paper's version is exactly the previous plus one.
- Student-ID line: handwritten, read by a person only; no personal data printed or stored; all test sheets synthetic and so marked.

## 8. Reducing mistakes in giving answers
Printed once on page 1: use the answer sheet only; fill the whole circle; one mark per row; cross out to withdraw; empty row means no answer. In the items: numbering equal to the sheet; options A to D in fixed order; no "all of the above" or "none of the above"; no negative stem unless the word is in capitals; options of similar length and without overlap, the key not systematically the longest; absolute words (always, never) only when true in Python; one answer defensible. A reminder at the end of each part names its sheet rows. One mark style only.

## 9. Reading, assessing, grading
- By machine: version strip, check number, calibration cells, every choice, digit, match, order and bank row. Filled at 45 per cent or more of the read area darker than the calibration, empty at 15 per cent or less, doubtful between (A7, to be fitted on synthetic sheets).
- By hand: student-ID line, the short answers, every held row and sheet, every crossed-out mark. The person's reading of the original sheet is final.
- Whole sheet held: marker missing, below 200 dpi, parity failure, check number different from the strip, tilt above 5 degrees after correction.
- Row held: doubtful cell, row not found, two or more filled cells. A person decides, a crossed-out mark counts as withdrawn; undecidable scores zero. An empty row scores zero and is not held.
- Key: one file per paper and form, with a SHA-256 digest; refused when kind, form and version differ from the strip. Points 100 in all: mcq 3, predict 4, match 1 per premise, order 1 per position, blank and cloze 1 per gap, short up to 3 by hand. No negative marking (A5).
- Second check: two independent readings per row (threshold; darkest cell with margin) must agree; the total is recomputed by a second routine; a person compares original and result for every held sheet and a random sample of at least 10 per cent (at least 5); short marks are entered twice.
- Tests: synthetic sheets only, built with known marks, including a rotated sheet, a low-resolution sheet, a double mark, a faint mark, a crossed-out mark and a wrong-form sheet.

## 10. What the Owner must supply
1. Bloom reading: Apply and up, or Analyze and up (A1). Decides whether the plan passes.
2. Short items: 0, 1 or 2, and who marks them (A4).
3. Whether code-writing on paper is enabled (then a rubric and a marker are named).
4. Whether wrong answers cost points (A5).
5. Length of the student number, if it is to be read by machine.
6. The final items per chapter after the lectures (A3).

Not found: the critical points of the instructor are collected by TK4_Points_A and TK4_Points_B; their file names were unknown when this design was written, so `course_point` is a link form, not yet a link.

## 11. Sources cited (all exist in the repository)
`08-tooling/briefs/exam/r3/BRIEF_TK4_Design.md`; `08-tooling/course_page_template_v9_52_4.html`; `08-tooling/template_exam_v9_19_0.js`; `08-tooling/sen0414_exam_desk_v2_2_0.html`; `08-tooling/sen0414_exam_release_v1_0_0.py`; `08-tooling/ch01-page/question_bank_v1_1_1.json`; `08-tooling/ch02-page/question_bank_v1_1_1.json`; `08-tooling/ch03-page/question_bank_v1_1_1.json`; `08-tooling/ch04-page/question_bank_v1_1_1.json`; `08-tooling/ch06-page/question_bank_v2_0_0.json`; `08-tooling/ch07-page/question_bank_v1_1_0.json`; `08-tooling/ch08-page/question_bank_v1_0_0.json`; `04-assessment/sen0414_assessment_v1_0_0.ttl`; `03-materials/ch01/page/chapter_code_ch01_v1_0_0.json` (and the same file for chapters 2, 3, 4, 6, 7, 8).
