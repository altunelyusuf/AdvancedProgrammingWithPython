# SEN0414 printed exams: design of the paper (version 1.1.0)

Task TK4_DesignRev. Machine-readable twin: `04-assessment/exams/exam_design_v1_1_0.json` (50 decisions, each with a reason). This version is new files; `04-assessment/exams/exam_design_v1_0_0.md` and `04-assessment/exams/exam_design_v1_0_0.json` stay as committed and controlled. Sections 7 and 9 of v1.0.0 (own sheet geometry, digit rows, thresholds) are replaced by the SEN0401 sheet's own; sections 3 and 5 are redone for the revised types; section 10 became section 10 below. Nothing under 03-materials is changed.

Scope (the Owner's statements of 2026-10-29 and 2026-10-30): two papers, midterm and make-up (only the midterm is built first); chapters 1, 2, 3, 4, 6, 7, 8 (chapter 5 out); 60 minutes each; physical printed paper; a printed key per paper; no QTI, no CATS export, no interactive HTML.

## 0. Owner's decisions and assumptions

Decided on 2026-10-30 (relayed; each with its reason in `owner_decisions.decided`): physical printed paper of one 60-minute sitting; code on paper is read-and-choose plus fill-the-blank and nothing is written freely; the interactive pages' questions are seeds and never copied; chapters 1, 2, 3, 4, 6, 7, 8; the answer sheet is a separate bubble grid that reuses the SEN0401 sheet and reader; the midterm is made first.

Assumptions still open (marked A, kept as numbers, full list with the effect of each answer in section 10):

| No | Assumption | Where it sits |
|---|---|---|
| A1 | Bloom reading "Apply and up" (levels 3 to 6) | `blueprint.share_apply_or_above` |
| A2 | 30 items per paper | `blueprint.items` |
| A3 | Items per chapter 4, 5, 5, 5, 4, 4, 3 | `blueprint.chapters` |
| A5 | No negative marking | grading key rule |
| A6 | Times per item: 60 s plain mcq, 100 s mcq with code, 120 s predict, 240 s match, 120 s order, 90 s blank item, 60 s cloze item (the blank and cloze values are this design's own: two sheet marks per gap) | section 5 |
| A8 | At least 9 cross-chapter items and 6 indirect items per paper | section 5 |
| A9 | Two forms (A, B) per paper | section 7 |

The v1.0.0 assumptions A4 (two hand-marked short items) and A7 (45 and 15 per cent fill thresholds) are gone: A4 by the Owner's decision, A7 because the sheet module has its own thresholds.

## 1. What is reused and what is new

Reused, unchanged from v1.0.0:
- the exam-kind idea and the type names of the pages' engine (`08-tooling/course_page_template_v9_52_4.html`, `08-tooling/template_exam_v9_19_0.js`);
- the newest chapter banks as seeds only (`08-tooling/ch01-page/question_bank_v1_1_1.json`, `08-tooling/ch02-page/question_bank_v1_1_1.json`, `08-tooling/ch03-page/question_bank_v1_1_1.json`, `08-tooling/ch04-page/question_bank_v1_1_1.json`, `08-tooling/ch06-page/question_bank_v2_0_0.json`, `08-tooling/ch07-page/question_bank_v1_1_0.json`, `08-tooling/ch08-page/question_bank_v1_0_0.json`): 839 items, 357 (42.5 per cent) at Apply or Analyze, none at Evaluate or Create;
- the weight of the midterm (30 per cent) from `04-assessment/sen0414_assessment_v1_0_0.ttl`;
- the chapter-code manifests (`03-materials/ch01/page/chapter_code_ch01_v1_0_0.json` and the same file for chapters 2, 3, 4, 6, 7, 8) as the list of listings the students have seen;
- the critical points: `04-assessment/exams/critical_points_ch01_04_v1_0_0.json` and `04-assessment/exams/critical_points_ch06_08_v1_0_0.json`.

Reused new in this version: the SEN0401 answer sheet and reader (section 7). Not reused: the Exam desk (`08-tooling/sen0414_exam_desk_v2_2_0.html`), the release tool (`08-tooling/sen0414_exam_release_v1_0_0.py`) and the page engine's question generation.

New: the item model with the validator, the near-copy measure, the general assembler, the printed layout, key and sheet specification, the reading and grading method.

## 2. Item model

One record per item; the validator `04-assessment/exams/exam_item_check_v1_0_0.py` checks exactly these 17 fields and no other.

| Field | Meaning | Rule (validator rule) |
|---|---|---|
| id | unique key | text, unique across both papers (R02) |
| chapters | chapters it needs | non-empty list among 1, 2, 3, 4, 6, 7, 8 (R03) |
| source | links to the course | non-empty list of `path` or `path#place`; each file exists (R04) |
| bloom | level | integer 1 to 6 (R05) |
| critical_point | the point it tests | the text of the point of a linked entry (R07) |
| course_point | links to the list | list of `<critical-points file>#<position from 0>`; each resolves (R06) |
| seed_item | the page item it grew from | `none` or `<bank path>#<position from 0>` inside that file (R08) |
| type | one kept type | mcq, predict, match, order, blank, cloze (R09) |
| stem | the question | text; gap markers `[[1]]`, `[[2]]` for blank and cloze |
| listing | code lines | list of at most 12 lines (R13), each no wider than code_width and without a line break (R14) |
| options_or_blanks | the options | mcq, predict: 4 texts; match: 5 premises and 7 answers; order: 4 steps; blank, cloze: gaps and a bank of 1 to 10 entries |
| answer | the key | mcq, predict: a letter A to D; match: 5 different letters A to G; order: the place 1 to 4 of each printed step; blank, cloze: different bank serials, one per gap (R10) |
| points | whole number | mcq 3, predict 4, match 5, order 4, blank and cloze one per gap (R15) |
| reason | why the answer is right | non-empty text (R18) |
| indirect_form | consequence, exception, reason or none | (R17) |
| code_width | declared width | 45 or 90 (R14) |
| bank_id | the shared bank | `none` for mcq, predict, match, order; a name for blank and cloze; markers, gap count and bank size agree (R16) |

Options must not overlap (R11: equal after normalising, or one inside another as a run of at least three words; predict outputs only equal after removing spaces) and must not say "all of the above" or "none of the above" (R12). Option length similarity and a single defensible answer are checked by a person.

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

### 2.2 Enhancement iteration (point c)
A seed becomes an exam item by changing at least one of: a new angle; a cross-chapter link; a reasoning step; a changed code case. The change is recorded in the item, the near-copy measure must pass, and the course_point stays.

### 2.3 The item validator
`04-assessment/exams/exam_item_check_v1_0_0.py` is a library (`check_items(list)` returns the failures) and a command line (`check ITEMS.json`, `selftest`). `04-assessment/exams/exam_item_check_fixtures_v1_0_0.json` holds 25 fixtures of known verdict: a valid item of each of the six kept types, a valid mcq with a listing, and one defective item for each of the 18 rules R01 to R18. The self-test prints expected and actual for each, checks that every kept type and every rule is covered, and exits 0 only when all are as expected. The fixture items are structural test items (their reason says FIXTURE) and are never exam items.

## 3. Types for print

| Type | Verdict | Printed form, sheet unit kind and reason |
|---|---|---|
| mcq | kept | A to D, one letter -> unit kind choice; also combination-of-statements, find-the-faulty-line (four line numbers), compare-two-designs |
| predict | kept | choose one of four printed outputs -> choice. The digit-and-sign form of v1.0.0 is dropped: the sheet has no unit for a number a person writes |
| match | kept | 5 premises to 7 answers A to G -> match, one unit per premise, 1 point each |
| order | kept | 4 printed steps; the cell 1 to 4 of the place each takes -> order, one unit per step, 1 point each |
| blank | kept | code gap, shared bank of printed two-digit codes -> bank, one unit per gap |
| cloze | kept | sentence gap, shared bank -> bank, one unit per gap |
| short | dropped | nothing is written freely (decision below) |
| multi, judge, repair, program, write, string, graph, object, ask, sparql | dropped | as in v1.0.0; program and write also by the Owner's decision of 2026-10-30 |

Short items: the recommended default is none. Nothing is written freely, so every answer is read by the machine, no marker, rubric or double entry is needed, and the sheet needs no human unit. Keeping even one would put hand marking back into a 60-minute sitting. The cost: Create (Bloom level 6) cannot be asked on a choice paper and Evaluate only by comparing two designs; section 5 says so.

## 4. Code on paper
- Listing: at most 12 lines, no wrapped line, 9 point monospace; declared width 45 characters (two columns) and 90 (one column); too long means shortened, never wrapped. Lines are numbered when a question refers to a line.
- Code tasks kept: predict the output by choosing one of four printed outputs; find the faulty line by choosing a line number; complete the gap from the numbered bank; order the lines. Nothing is written.
- Output options are written as Python prints them: text without quotes; list `[1, 2]`; dictionary `{'a': 1}`; repr of text with quotes; two lines of output as two lines in the option. No two options differ only in a space.
- A numeric result is asked as one of four printed numbers (results of expressions, counts of loop passes, lengths, indexes). No money or fee arithmetic.

## 5. Blueprint of one paper (midterm and make-up alike): the sums

| Type | Items | Seconds each | Seconds | Points each | Points | Sheet unit kind | Sheet units |
|---|---|---|---|---|---|---|---|
| mcq plain | 9 | 60 | 540 | 3 | 27 | choice | 9 |
| mcq with code | 7 | 100 | 700 | 3 | 21 | choice | 7 |
| predict | 5 | 120 | 600 | 4 | 20 | choice | 5 |
| match | 2 | 240 | 480 | 5 (1 per premise) | 10 | match | 10 |
| order | 2 | 120 | 240 | 4 (1 per step) | 8 | order | 8 |
| blank | 3 | 90 | 270 | 3 (3 gaps) | 9 | bank | 9 |
| cloze | 2 | 60 | 120 | 3 and 2 (gaps) | 5 | bank | 5 |
| form mark F | | | | | | bank | 1 |
| Total | 30 | | 2950 s = 49.2 min | | 100 | | 54 |

- Items: 9 + 7 + 5 + 2 + 2 + 3 + 2 = 30. Time: 540 + 700 + 600 + 480 + 240 + 270 + 120 = 2950 s; the limit is 90 per cent of 3600 s = 3240 s; 2950 is 81.9 per cent, 290 s to spare. Points: 27 + 21 + 20 + 10 + 8 + 9 + 5 = 100.
- Chapters (first chapter of the item): 1:4, 2:5, 3:5, 4:5, 6:4, 7:4, 8:3 = 30.
- Bloom (A1): Remember 2, Understand 7, Apply 11, Analyze 8, Evaluate 2, Create 0 = 30; levels 3 to 6 = 11 + 8 + 2 + 0 = 21 (70 per cent, above 50). With "Analyze and up" it is 8 + 2 = 10 of 30 (33 per cent) and fails. Evaluate: mcq judging two designs or programs. Create is not reached, because nothing is written.
- Letters: 21 lettered items (16 mcq and 5 predict): A 6, B 5, C 5, D 5 = 21; no letter is the key of four items in a row; holds again for each form after shuffling.
- Cross-chapter: at least 9 items name two or more chapters. Indirect items: at least 6, each with indirect_form.
- Banks: blank bank 10 entries for 9 gaps, cloze bank 7 entries for 5 gaps (at most 10, the sheet's limit). Each entry prints a two-digit code (serial 0 to 9 and its check digit). Order is a seeded permutation, the seed stored in the build record; gaps of one item have different keys; no serial is the key of three gaps in a row; the bank is never in gap order.
- Pair: the make-up repeats no item of the midterm; a critical point may recur through a different item.
- Item order: four parts by type (choice, trace, bank fill-in, match and order); positions 1 to 30 run through the paper and are the numbers on the sheet. Instructions per part are printed once.

## 6. Saving pages
Two columns of A4, margins 12 mm, body 10 point or more, code 9 point, black on white without shading; a listing printed once and shared by the items that refer to it; no answer space on the paper; no name or number printed. Estimate: about 393 lines (63 plain mcq, 119 mcq with code, 95 predict, 28 match, 20 order, 43 bank items, 25 for page 1) at about 112 lines per page = 3.5 pages, so **4 paper pages (2 sheets) and the answer sheet of 2 pages (1 sheet, measured below): 6 pages, 3 sheets per student.** The paper figure is an estimate: the first build must report the real count, and more than 4 paper pages is a failure of this design.

## 7. The answer sheet: the SEN0401 sheet and reader, reused

Modules (read-only, never edited), in `/home/claude/sen0401/08-tooling/exam/`:
- `/home/claude/sen0401/08-tooling/exam/sen0401_exam_answersheet_v1_0_0.py`: the sheet (specification, layout, renderer, Damm check digit, registration on corner marks, bubble features, naive reader). SHA-256 `929184f5ed0a52b975677eb59f511b69b3982024e8a8bd858e20278afe4dcf23`.
- `/home/claude/sen0401/08-tooling/exam/sen0401_exam_answersheet_v1_1_0.py`: the reader (`read_sheet` with optical-density flags; imports the v1_0_0 module). SHA-256 `758cd9af5d300d6c1cf0dc4046e381cb1a78034494e513c733f40e18fd034573`.

### 7.1 How the SEN0414 repository obtains them
Recommended and decided here: byte-identical vendored copies in 08-tooling (named sen0401_exam_answersheet_v1_0_0.py and sen0401_exam_answersheet_v1_1_0.py, with a vendor record holding the two SHA-256 values above), made by the engine task; this task adds files only under 04-assessment/exams. At every control the copy is compared byte for byte with the source and with the recorded digest (the design check already compares the source with the digest now). A changed source means the sheet geometry, thresholds or reader changed after this design: the check fails, the vendored copy is not replaced by itself, and a person decides whether to adopt the new version and repeat the sample reading test before any paper is printed. The modules need reportlab, numpy, scipy, OpenCV, the DejaVu fonts and pdftoppm.

### 7.2 Unit kinds defined by the module
The module's block rules name five kinds: choice, match, order, bank, human (at most 5, 5, 5, 3, 4 units per block, each block closed by a "left blank" row).

| Unit kind | Rows | What it is |
|---|---|---|
| choice | 1 | one row of labelled bubbles, the options come from the specification |
| match | 1 | the same, one unit per premise |
| order | 1 | the same, one unit per step, numbered cells |
| bank | 2 | two rows of digits 0 to 9 that make a code: serial digit and its Damm check digit |
| human | 0 | a box of digit cells written by hand; the reader only sees ink and holds the unit for a person |

### 7.3 Mapping of the kept types
mcq and predict -> choice (A to D); match -> match (5 units, A to G); order -> order (4 units, cells 1 to 4); blank and cloze -> bank (one unit per gap). Nothing maps to human, and nothing needs a unit the sheet lacks. Where v1.0.0 needed digit rows (predict by number, the check number) the item type or the tie was changed: predict is only by choice; the sheet-to-paper tie is the unit F (below).

### 7.4 What was run
The module was run in a scratch folder outside the repository (not kept), on a specification of the 54 units of the blueprint (F, 21 choice, 10 match, 8 order, 14 bank): the layout gave 2 sheet pages; marks were drawn into the rasterised sheet at random valid answers and read back by `read_sheet`: 54 of 54 correct with no flag. A row with two filled bubbles gave the flag double; a bubble crossed out with an X and no other mark gave no value and no flag. NOT_MEASURED: a printed sheet that was scanned or photographed; a sheet turned by 180 degrees; the module's thresholds on SEN0414 sheets; a scan at a resolution other than 150 dpi (the reader works in its own 150 dpi frame, so a scan must be resized first).

### 7.5 What the reader reads and what it holds for a person
By machine: every mcq and predict letter, every match premise, every order step, every bank code (blank, cloze and the form mark F) with its check digit, and the closure row of every block. Held for a person: the identification box (a rectangle filled by hand); every row flagged double, faint, incomplete, check-digit or held-block; every sheet page that cannot be registered (fewer than three corner marks found); a doubted X. A struck-through bubble reads as empty.

### 7.6 Geometry and rules (the module's own)
A4 portrait (595.28 by 841.89 pt), margin 15 mm, two columns of 245 pt, bubble radius 5.5 pt, pitch 19 pt, row 15.5 pt, four L-shaped corner marks on every page (leg 8 mm), reading at 150 dpi. Printed rules: fill the bubble completely; X through a bubble withdraws it; exactly one filled bubble per row, two count as no answer; after each block fill the bubble of every number left blank; codes are two digits; no marks outside bubbles and boxes. The engine writes a layout file and the reader reads that file.

### 7.7 Tie between sheet and paper, and two forms
The module has no version strip, parity cell or check-number rows. It prints a form code (four digits and a check digit) in the header, read by a person only. Added here with existing kinds only: unit F, one bank unit that the student fills with the printed two-digit form mark of the paper (serial 0 midterm A, 1 midterm B, 2 make-up A, 3 make-up B, plus its check digit). The grading tool compares it with the key's form and refuses a mismatch. Two forms A and B: same items in different order inside blocks of equal type, options reordered; the type of every position is equal, so one layout serves both. The paper version is exactly the previous plus one.

### 7.8 Dropped from v1.0.0
Digit rows with a sign cell, the version strip with parity, the three check-number rows, the two calibration cells, the hollow corner marker, the 5 degree tilt limit, the 200 dpi limit and the 45 and 15 per cent fill thresholds. The module has none of them; whether a tilt limit is needed is NOT_MEASURED.

## 8. Reducing mistakes in giving answers
Printed once on page 1: use the answer sheet only; fill whole circles; one mark per row; X through a bubble to withdraw; fill the blank-number bubbles at the end of each block; copy the form mark into unit F. In the items: numbering equal to the sheet; options A to D in fixed order; no "all/none of the above" (R12); no negative stem unless the word is in capitals; options of similar length and without overlap (R11); the key not systematically the longest; absolute words only when true in Python; one answer defensible. A reminder at the end of each part names its sheet rows.

## 9. Reading, assessing, grading
- Reading: the module's reader (7.5). Filled from a mean ink of 0.50 inside the ring at 150 dpi, faint from 0.12 (or optical density 0.03), struck when three of four corner patches hold ink. These replace 45 and 15 per cent.
- By hand: identification box, held rows and sheet pages, doubted X. The person's reading of the original sheet is final.
- Sheet page held: fewer than three corner marks found. Bank unit held: incomplete, double, faint or check-digit failure. Block held: closure row disagrees with blank rows, and a shifted run is held to where it lands.
- Row held (double): a person decides, an X-ed bubble counts as withdrawn; undecidable scores zero. An empty row scores zero.
- Key: one file per paper and form with a SHA-256 digest; refused when kind, form and version differ from the form mark in unit F. Points: mcq 3, predict 4, match 1 per premise, order 1 per step, blank and cloze 1 per gap; 100 in all; no negative marking (A5).
- Second check: the module's `read_sheet` and `read_naive` must agree per row or the row is held; the total is recomputed by a second routine; a person compares original and result for every held sheet and a random sample of at least 10 per cent (at least 5).
- Tests: synthetic sheets only, built with known marks, including a double mark, a faint mark, an X-ed mark, a wrong-form sheet and a skewed or low-resolution sheet; none of these has been built yet (NOT_MEASURED).

## 10. Questions still open for the Owner

Each has a recommended default; the design uses the default until he answers. Full text in `owner_decisions.open`.

| No | Question | Default (assumption) | What another answer would change |
|---|---|---|---|
| Q1 | Items per paper | 30 (A2) | time (about 32 items is the most at this mix), points rescaled to 100, sheet units (1.8 per item), chapter quota and letter counts; pages are re-measured |
| Q2 | Bloom reading | Apply and up (A1) | Analyze and up gives 10 of 30 (33 per cent) and fails; it needs at least 16 items at levels 4 to 6, which on a choice paper means mostly compare-two-designs, indirect and trace items and fewer items |
| Q3 | Chapter weights | 4, 5, 5, 5, 4, 4, 3 (A3) | only the quota table; nothing else |
| Q4 | Final chapter list | 1, 2, 3, 4, 6, 7, 8 | the quota table and the validator's chapter set; critical points of an added chapter must exist first |
| Q5 | Wrong answers cost points | no (A5) | the key rule and the total |
| Q6 | The reused sheet prints "SEN0401 answer sheet" in its title and the module cannot be edited | overprint the title line on the rendered PDF in the engine task, without editing the module | if accepted as it is, SEN0414 students get a sheet titled SEN0401; if overprinted, one more engine step and one look by a person |

## 11. Sources cited (all exist)
`08-tooling/briefs/exam/r4/BRIEF_TK4_DesignRev.md`; `04-assessment/exams/exam_design_check_v1_0_0.py`; the repository files named in sections 1 and 2; the two module files named in section 7.
