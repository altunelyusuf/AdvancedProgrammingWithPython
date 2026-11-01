# SEN0414 printed exams: design of the five-question paper (version 1.2.0)

Task TK4_Design2. Machine-readable twin: `04-assessment/exams/exam_design_v1_2_0.json` (38 decisions, each with a reason). New files; `04-assessment/exams/exam_design_v1_1_0.md` and `04-assessment/exams/exam_design_v1_1_0.json` stay as committed and controlled. Brief: `08-tooling/briefs/exam/r10/BRIEF_TK4_Design2.md`. Nothing under 03-materials is changed.

Scope (the Owner's words of 2026-11-01 13:04 Istanbul, as relayed, and the decisions of 2026-10-30 that still hold): a cover page, then five questions, Q1 to Q4 of 25 points and Q5 of 10 points as a bonus; chapters 1 to 8 (chapter 5 in); a physical printed paper of one 60-minute sitting; code on paper is read-and-choose plus fill-the-blank; page-interactive questions are seeds and never copied; two forms A and B; the answer sheet is the SEN0401 sheet. The new item rules N1 to N5 of the brief apply.

## 0. Result in six lines

- 30 sub-questions: Q1 6, Q2 7, Q3 7, Q4 6, Q5 4; points per question 25, 25, 25, 25, 10 (bonus); base total 100, highest mark 110.
- Chapters 1 to 8 get 4, 4, 4, 4, 3, 4, 4, 3 sub-questions (the lineage defaults add to 33; chapters 2, 3 and 4 each give up one).
- Time: 2630 s planned = 73.1 per cent of the 60 minutes (limit 90 per cent = 3240 s).
- Bloom: Remember 0; Apply and above 27 of 30 (91 of 100 points); Analyze and above 11 of 30 (32 of 100 points).
- Pages: 6 (cover, four question pages, one answer-sheet page). Four in total is not possible at a readable size (section 6).
- Answer sheet: 31 units (30 sub-questions and the form mark F), measured 1 sheet page with the SEN0401 module.

## 1. The cover page

Page 1 is the İstanbul Kültür University (İKÜ) exam cover page, filled from the template the Owner supplied. The template is another course's document and is not stored in the repository. Filled: department; course code and name; exam kind; student name line; student identity number (ID) line; academic year; term; date and time; duration 60 minutes; instructor; grade table: Q1 /25, Q2 /25, Q3 /25, Q4 /25, Q5 bonus /10, Total /100; instructions rewritten for the answer-sheet paper; learning outcomes per question; program outcomes row (dash); cheating warning. Inputs the Papers task must supply and this design does not guess: academic year, term, date, time. The instructions are rewritten because nothing is written on the paper: Write your name and identity number (ID) on the cover; answer on the answer sheet only, nothing is marked on the paper; fill the bubbles completely; copy the two-digit form mark into box F; devices are not allowed; the five questions and the bonus are explained in one line each.

## 2. The five questions

| Question | Title | Points | Sub-questions | Types | Format |
|---|---|---|---|---|---|
| Q1 | Read the program and predict | 25 | 6 | predict, mcq | Each sub-question shows a short program (at most 12 lines). The student reads it and chooses what it prints or does (predict), or chooses the effect of a run (mcq with a listing). |
| Q2 | Complete the program | 25 | 7 | blank, cloze | One program with numbered gaps (blank) and one explanation with numbered gaps (cloze); the gaps are filled from a printed option bank, each entry printed with a two-digit code that the student writes into the sheet. |
| Q3 | Choose the right tool and say why it fits | 25 | 7 | match, mcq | Five situations are matched to seven lettered tools or reasons (A to G); two further sub-questions choose the reason why a tool fits. |
| Q4 | Find the effect of a change, or put the steps in order | 25 | 6 | order, mcq | Four printed steps of a task are put in order (the place 1 to 4 of each step); two mcq ask what changes when a line or a setting is changed. |
| Q5 (bonus) | Bonus: across chapters | 10 | 4 | mcq | Four mcq that need two or more chapters together or ask for a consequence, an exception or a reason. |

One sub-question is one mark on the answer sheet (assumption A1): a choice row, a gap, a match premise or an order step.

### 2.1 The sub-questions

| Id | Type | Unit | Points | Bloom | Asks | First chapter | Seconds | Cross-chapter | Indirect |
|---|---|---|---|---|---|---|---|---|---|
| Q1a | predict | choice | 4 | 3 | effect | 1 | 120 |  |  |
| Q1b | predict | choice | 4 | 3 | effect | 2 | 120 |  |  |
| Q1c | predict | choice | 4 | 3 | effect | 3 | 120 |  |  |
| Q1d | mcq | choice | 4 | 4 | effect | 4 | 100 |  |  |
| Q1e | mcq | choice | 4 | 4 | effect | 6 | 100 |  |  |
| Q1f | mcq | choice | 5 | 4 | effect | 7 | 100 | yes |  |
| Q2a | blank | bank | 4 | 3 | use | 1 | 30 |  |  |
| Q2b | blank | bank | 4 | 3 | use | 2 | 30 |  |  |
| Q2c | blank | bank | 4 | 3 | use | 3 | 30 |  |  |
| Q2d | blank | bank | 4 | 3 | use | 4 | 30 |  |  |
| Q2e | cloze | bank | 3 | 2 | reason | 5 | 24 |  |  |
| Q2f | cloze | bank | 3 | 2 | reason | 6 | 24 |  |  |
| Q2g | cloze | bank | 3 | 2 | reason | 8 | 24 |  |  |
| Q3a | match | match | 3 | 3 | use | 1 | 48 |  |  |
| Q3b | match | match | 3 | 3 | use | 2 | 48 |  |  |
| Q3c | match | match | 3 | 3 | use | 3 | 48 |  |  |
| Q3d | match | match | 3 | 3 | use | 4 | 48 |  |  |
| Q3e | match | match | 3 | 3 | use | 5 | 48 |  |  |
| Q3f | mcq | choice | 5 | 4 | reason | 7 | 60 | yes |  |
| Q3g | mcq | choice | 5 | 4 | reason | 8 | 60 | yes |  |
| Q4a | order | order | 4 | 3 | use | 3 | 30 |  |  |
| Q4b | order | order | 4 | 3 | use | 5 | 30 |  |  |
| Q4c | order | order | 4 | 3 | use | 6 | 30 |  |  |
| Q4d | order | order | 4 | 3 | use | 7 | 30 |  |  |
| Q4e | mcq | choice | 4 | 4 | effect | 8 | 100 | yes | yes |
| Q4f | mcq | choice | 5 | 5 | effect | 4 | 60 | yes | yes |
| Q5a | mcq | choice | 3 | 4 | effect | 1 | 60 | yes | yes |
| Q5b | mcq | choice | 3 | 4 | reason | 2 | 60 | yes | yes |
| Q5c | mcq | choice | 2 | 5 | effect | 6 | 100 | yes | yes |
| Q5d | mcq | choice | 2 | 4 | reason | 7 | 100 | yes | yes |

Points per question: Q1 25, Q2 25, Q3 25, Q4 25, Q5 10. Whole numbers throughout.

### 2.2 Chapters (sub-questions per chapter, by the first chapter an item needs)

| Question | Ch 1 | Ch 2 | Ch 3 | Ch 4 | Ch 5 | Ch 6 | Ch 7 | Ch 8 | Sum |
|---|---|---|---|---|---|---|---|---|---|
| Q1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 6 |
| Q2 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 7 |
| Q3 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 7 |
| Q4 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 6 |
| Q5 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 4 |
| Weight | 4 | 4 | 4 | 4 | 3 | 4 | 4 | 3 | 30 |

Chosen weights 4, 4, 4, 4, 3, 4, 4, 3. The lineage agent's defaults 4, 5, 5, 5, 3, 4, 4, 3 add to 33 and the paper has 30, so chapters 2, 3 and 4 each give up one; the others stay as the defaults had them (assumption A2). Chapter 5 is asked in Q2, Q3 and Q4 only (A3). Cross-chapter sub-questions: 9 (all of Q5, Q3f, Q3g, Q4e, Q4f, Q1f); indirect sub-questions: 6 (Q4e, Q4f and all of Q5), each with an indirect_form. A gap is recorded: no critical-points file exists for chapter 5 (section 10).

## 3. New item rules and fields

- N1 no memorisation: nothing asks for a name, keyword, definition, function signature or syntax detail from memory; Bloom level 1 is not allowed (0 of 30 here).
- N2 no required recall of terms: a term used gets a TIP (at most 20 words) printed with the stem or in a margin line; the answer never depends on the term's name; the tip never repeats an option.
- N3 abbreviations in full at first use, for example 'integrated development environment (IDE)': a registry of short forms and a scan of the assembled paper in print order (the scan is a function of the design check, with fixtures of known answer).
- N4 each sub-question asks about use (13), reason (7) or effect (10), recorded in the field asks.
- N5 the stem keeps the Owner's 10-to-30-word rule; the tip is a separate printed part.

| New field | Values | Rule |
|---|---|---|
| question | Q1, Q2, Q3, Q4, Q5 | the question the sub-question belongs to; its type must be allowed in that question's format |
| sub | a, b, c, ... in order | unique within the question, letters without gaps; the sheet unit number is the question digit and the letter (1a ... 5d) |
| tip | text of at most 20 words, or none | required when terms is not empty (N2); never equal to an option; not counted in the 10-to-30 words of the stem (N5) |
| terms | list of the specific terms the sub-question uses; may be empty | at most two per sub-question; each has a tip (N2); no term is the answer |
| asks | use, reason or effect | exactly one of the three (N4) |

The 17 fields of `04-assessment/exams/exam_design_v1_1_0.md` section 2 stay. The validator `04-assessment/exams/exam_item_check_v1_0_0.py` checks exactly those 17 and stays; extending it is the task TK4_ItemRules2. Seeds and the near-copy rule are unchanged (`04-assessment/exams/exam_nocopy_v1_0_0.py`).

## 4. Time

Rates reused from section 5 of v1_1_0 (derived by division where an item had several parts): mcq_plain 60 s, mcq_code 100 s, predict 120 s, match_premise 48 s, order_step 30 s, blank_gap 30 s, cloze_gap 24 s.

| Part | Seconds |
|---|---|
| 30 sub-questions at their rates | 1812 |
| 10 s to read a tip, 30 sub-questions | 300 |
| 30 s per question for its shared text, 5 questions | 150 |
| cover and instructions | 120 |
| filling the sheet, 8 s per unit, 31 units | 248 |
| Total | 2630 = 73.1 per cent of 3600 s |

The limit is 90 per cent of 3600 s = 3240 s; 610 s are spare. The four allowances are this design's own (assumption A5) and the 8 s per unit is NOT_MEASURED with students.

## 5. Bloom rule on sub-questions and on points

| Level | Sub-questions |
|---|---|
| 1 | 0 |
| 2 | 3 |
| 3 | 16 |
| 4 | 9 |
| 5 | 2 |
| 6 | 0 |

Remember (1) is not allowed and has 0. Apply and above (levels 3 to 6): 27 of 30 (rule: more than half). Analyze and above (levels 4 to 6): 11 of 30 (rule: at least 8). By points, of the 100 base points: 91 at Apply and above (rule: at least 50) and 32 at Analyze and above. Create is not reached because nothing is written; Evaluate is asked as a judgement between two designs or two programs (Q4f, Q5c). Reading of the levels is assumption A4.

## 6. Page budget

6 pages: the cover (page 1), four pages of questions (pages 2 to 5) and the answer sheet (page 6, one page, measured).

| Part | Lines |
|---|---|
| Q1 three predict (19 lines) and three mcq with a listing (17 lines) | 108 |
| Q2 one program with four gaps, one text with three gaps, two option banks, seven tips | 54 |
| Q3 one match block (14 lines) and two plain mcq (7 lines each), three tips | 31 |
| Q4 one order block (10), one mcq with a listing (17), one plain mcq (7), tips | 36 |
| Q5 two plain mcq (7) and two mcq with a listing (17), four tips | 52 |
| Q1 tips | 6 |
| headings of Q1 to Q5 (title, points, one instruction line) | 15 |
| Total | 302 |

At 96 lines per page (relaxed layout; the dense layout of v1_1_0 had 112) that is 4 question pages. Four pages in total leave two pages of questions: 2 x 112 = 224 lines at the densest layout of v1_1_0 against about 302 lines needed, so the type would shrink to about 74 per cent of 10 point, i.e. under 7.5 point. The Owner's rule is 'fit with 6 pages but better formatting and readability' when 4 do not fit.

Levers, in this order:

1. option layout: Four options of at most 30 characters each print two per line (A and B, then C and D); longer options print one per line. (saves up to 2 lines per mcq)
2. code width: A listing is declared 45 characters (one column) or 90 (both columns, a full-width box); lines are shortened, never wrapped. (a 45-wide listing sits beside its options)
3. spacing and margins: A blank line before each sub-question; margins 12 mm, not below 10 mm; keep-together on each sub-question and its tip. (readability; 96 lines per page instead of 112)

Never used as levers: Body text below 10 point, code below 9 point, shading, a sub-question split over two pages, the sheet squeezed. These are not used to win a page.

How the engine measures: The engine builds the paper as .docx, converts it with LibreOffice (soffice --headless --convert-to pdf) in a scratch folder and reads the page count with pdfinfo; the fill of the last question page is read from the lowest text line of that page (pdftotext -bbox). Pass: Cover + question pages = 5 and the last question page at most 92 per cent full (spare of one block for the difference between LibreOffice and Word); the sheet is 1 page by the module's own layout. Then the total is 6. Fail: More than 4 question pages is a FAIL of the layout: levers are applied in their order; if still over, the engine stops and reports, it never shrinks the type. How Word lays the same .docx out is NOT_MEASURED (LibreOffice is the measure); the printed result must be looked at once by a person.

The figure above is an estimate; the first build must report the measured page count.

## 7. The answer sheet

Reused, never edited: `/home/claude/sen0401/08-tooling/exam/sen0401_exam_answersheet_v1_0_0.py` (sheet) and `/home/claude/sen0401/08-tooling/exam/sen0401_exam_answersheet_v1_1_0.py` (reader), with the SHA-256 values recorded in the json (`answer_sheet.reuse`). The vendoring rule, geometry (A4, 15 mm margin, 150 dpi), mark style, form-mark unit F and reading rules of section 7 of v1_1_0 stay. What changes is the unit list: one unit per sub-question.

| Unit kind | Units | Which |
|---|---|---|
| choice | 14 | Q1a to Q1f, Q3f, Q3g, Q4e, Q4f, Q5a to Q5d |
| match | 5 | Q3a to Q3e (A to G) |
| order | 4 | Q4a to Q4d (cells 1 to 4) |
| bank | 8 | Q2a to Q2g (two-digit codes) and the form mark F |

31 units in all; the design check builds this list in the module's own layout and reads the page count (1). Units run in paper order after F; the module closes each block of at most 5 (choice, match, order) or 3 (bank) with its left-blank row. The title the module prints, SEN0401 answer sheet, is overprinted on the rendered PDF (assumption A9). Output: one position-exact PDF with its layout file, the same for both forms.

## 8. Key and outputs

- Key per paper and form: a .docx (answer, points, reason, tip and chapter of every sub-question, in print order, editable) and a machine key (JSON with, for every sheet unit, the answer and the points, a SHA-256 over its content, kind, form and version). Points: the sub-question table; Q5 is reported on its own line; no negative marking. Refusal: refused when kind, form and version differ from the form mark read in unit F.
- Outputs: paper A and B as editable .docx; key A and B as .docx and machine .json; the answer sheet as one position-exact PDF with its layout file. No QTI, no interactive HTML.
- Two forms: same structure; the type, points, Bloom level and sheet unit of every position are equal; B reorders sub-questions only among positions of the same type, points and Bloom level and reorders options, so one sheet layout serves both. Keys of the 14 choice sub-questions: A 4, B 4, C 3, D 3; no letter three times in a row.
- Bonus: Q5 is reported on its own line; the highest mark is 110 (A8, open question Q1).

## 9. Reading, grading

Unchanged from section 9 of v1_1_0: the module's reader reads every unit; held rows, held sheets and doubted X marks go to a person; the second check compares `read_sheet` and `read_naive`; no negative marking. Points per unit are those of the sub-question table.

## 10. Assumptions, open questions and gaps

| No | Assumption | If the other answer holds |
|---|---|---|
| A1 | A match premise and an order step are each one sub-question (so Q3 has 5 + 2 and Q4 has 4 + 2). | If a whole match block or order block were one sub-question, Q3 would have 3 and Q4 3 sub-questions and the total 30 could not be reached with the brief's 7 and 6; Q3 and Q4 would need seven and six separate blocks and the paper would grow by about 40 lines. |
| A2 | Chapter weights 4, 4, 4, 4, 3, 4, 4, 3 (the lineage defaults reduced by one in chapters 2, 3 and 4). | Any other weights summing to 30 change only the chapter matrix and the choice of seeds; time, points and the sheet do not change. |
| A3 | Chapter 5 is asked only in Q2, Q3 and Q4. | Putting it in Q1 needs a listing about debugging with a traceback; the page estimate rises by about 10 lines. |
| A4 | Bloom reading 'Apply and above' = levels 3 to 6 for the majority rule, and 'Analyze and above' = levels 4 to 6 for the 8-of-30 rule, both also by points. | If the majority rule meant Analyze and above, 11 of 30 (37 per cent) would fail it; at least 16 sub-questions at levels 4 to 6 would be needed, i.e. most of Q2 and Q3 would have to become why-questions. |
| A5 | The allowances: 10 s per tip, 30 s per shared text, 120 s cover, 8 s per sheet unit. | They add 818 s in all; the sub-questions alone take 1812 s, so 1428 s of the 3240 s are free for allowances: they could be 1.7 times as large before the 90 per cent rule fails. |
| A6 | Term, date and time are inputs to the Papers task and are not decided here. | If the engine had to default them, a wrong date would be printed on every paper. |
| A7 | Program outcomes are left as a dash because the repository has none; learning outcomes per question come from 01-outcomes/sen0414_outcomes_v1_0_0.ttl, which says it is a draft that fills an empty catalogue page. | If the department supplies program outcomes, the cover's row is filled by a one-line input; nothing else changes. |
| A8 | The bonus adds to the total (up to 110). | If the total is capped at 100, the mark of a student with a perfect Q1 to Q4 gains nothing from Q5; the cover's total row changes to 'at most 100'. |
| A9 | The sheet title is overprinted to read SEN0414. | If accepted as it is, the sheet says SEN0401; if overprinted, one more engine step and one look by a person. |
| A10 | Q5 uses mcq only. | A match or order bonus would add sheet units of another kind and about 10 lines. |

Open questions for the Owner (each has a default; the design uses it):

| No | Question | Default | If the answer changes |
|---|---|---|---|
| Q1 | Does the bonus raise the total above 100 or is the total capped at 100? | adds, reported on its own line | Only the cover's total row and the key's total rule. |
| Q2 | Which term, date and time are printed on the cover? | supplied by the Owner when the papers are built | Only the cover's three fields. |
| Q3 | Are there program outcomes of the department to print on the cover? | a dash | One row of the cover. |
| Q4 | Overprint the sheet title to SEN0414, or accept SEN0401? | overprint without editing the module | One engine step and one look by a person. |

Gap found: No critical-points file for chapter 5 exists (only chapters 1 to 4 and 6 to 8). Chapter 5 sub-questions cannot yet be linked to a critical point as the item rules R06 and R07 require; 3 sub-questions have chapter 5 as first chapter. Needed: A new file critical_points_ch05_v1_0_0.json made from the chapter 5 deck by the task that writes the items; not made here.

## 11. Sources cited

`08-tooling/briefs/exam/r10/BRIEF_TK4_Design2.md`; `08-tooling/briefs/exam/r10/INDEX.md`; `04-assessment/exams/exam_design_v1_1_0.md`; `04-assessment/exams/exam_item_check_v1_0_0.py`; `04-assessment/exams/exam_nocopy_v1_0_0.py`; `01-outcomes/sen0414_outcomes_v1_0_0.ttl`; `04-assessment/exams/critical_points_ch01_04_v1_0_0.json`; `04-assessment/exams/critical_points_ch06_08_v1_0_0.json`; the two module files named in section 7.

## 12. Decisions with reasons

1. **Scope of the pair.** Midterm and make-up, both over chapters 1 to 8 (chapter 5, Debugging, now in); one 60-minute sitting; physical printed paper; one printed key per paper and form; this design is version 1.2.0 and replaces the single 30-item list of v1_1_0 by five questions. *Reason:* The Owner's instruction of 2026-11-01 13:04 (Istanbul) and the chapter list of the brief; v1_1_0 stays as committed and controlled.
2. **Cover page.** Page 1 is the İstanbul Kültür University (İKÜ) exam cover page, filled from the supplied template: department, course, exam kind, student name and identity number (ID) lines, academic year, term, date and time, duration, instructor, the grade table with rows Q1 to Q4, the bonus row Q5 and Total, the instructions, a row of learning outcomes per question, and the cheating warning. The generic parts are filled for SEN0414; the instructions are rewritten for an answer-sheet paper (nothing is written on the paper). The template itself is never stored in the repository. *Reason:* The Owner asked that the generic parts of the attached page be filled appropriately for each exam; the template is another course's document and must not be committed.
3. **Cover page: fields filled by the engine.** Course line from the course profile; instructor from the course outline (Yusuf Altunel); duration 60 minutes; academic year, term, date and time supplied by the Papers task as inputs (not guessed); learning outcomes per question from the outcomes file by the chapters of the question's sub-questions; program outcomes left empty with a printed dash because the repository has none (they are the department's, not the course's). *Reason:* No term, date or program-outcome fact is available in the repository; inventing them would break the rule against inventing facts. Marked A6 and A7.
4. **Five questions.** Q1 to Q4 are 25 points, Q5 is a 10-point bonus: base total 100, bonus up to 10. 30 sub-questions: Q1 6, Q2 7, Q3 7, Q4 6, Q5 4. Each question has one format. *Reason:* The Owner's wish (4 questions of 25, a fifth of 10, bonus) and the sub-question numbers of the brief.
5. **Format of Q1.** Read the program and predict: three predict (choose the printed output) and three mcq with a listing (choose the effect of a run). Points 4, 4, 4, 4, 4, 5. *Reason:* Predict and mcq with a listing are the code-reading types kept in v1_1_0; the last is worth 5 because it combines two chapters.
6. **Format of Q2.** Complete the program: four blank gaps in one program and three cloze gaps in one explanation, each from its own option bank of at most 10 entries printed with two-digit codes. Points 4, 4, 4, 4, 3, 3, 3. *Reason:* Blank and cloze are the fill-in types kept; bank units hold at most 3 per block in the SEN0401 sheet, so 7 gaps give 3 blocks; the cloze asks WHY a construct exists, so it carries the reason questions.
7. **Format of Q3.** Choose the tool and say why it fits: a match block of five situations to seven lettered answers (3 points per premise) and two mcq on reasons (5 each). *Reason:* Match and mcq on reasons are the types the brief names; one premise is one sheet unit, so partial credit comes by premise.
8. **Format of Q4.** Order and effect: four printed steps are put in order (4 points per step) and two mcq on consequences (4 and 5). *Reason:* Order and mcq on consequences are the types the brief names; one step is one sheet unit (cells 1 to 4).
9. **Format of Q5.** Bonus across chapters: four mcq, two with a listing, that need two or more chapters or ask for a consequence, exception or reason. Points 3, 3, 2, 2. *Reason:* The brief names cross-chapter and indirect items; mcq is the only type that reads cleanly as an extra on the paper.
10. **One sub-question, one sheet unit.** A sub-question is the unit that is marked on the answer sheet: one choice row, one bank unit (a gap), one match premise or one order step. A match block of five premises is five sub-questions (3a to 3e); an order block of four steps is four sub-questions (4a to 4d). The form mark F is the 31st unit and is not a sub-question. *Reason:* The brief fixes 30 sub-questions with whole-number points and an answer sheet unit per sub-question; this is the only reading that gives 7 for Q3 (5 + 2) and 6 for Q4 (4 + 2). Marked A1.
11. **Points per sub-question.** Whole numbers: Q1 4,4,4,4,4,5; Q2 4,4,4,4,3,3,3; Q3 3,3,3,3,3,5,5; Q4 4,4,4,4,4,5; Q5 3,3,2,2; these add to 25, 25, 25, 25 and 10. *Reason:* The brief asks for whole numbers adding to the question total; heavier points go to the sub-questions that sit higher in Bloom's levels or combine chapters.
12. **Chapter weights.** Chapters 1 to 8 get 4, 4, 4, 4, 3, 4, 4, 3 sub-questions (= 30). The lineage agent's defaults 4, 5, 5, 5, 3, 4, 4, 3 add to 33, three too many; chapters 2, 3 and 4 each give up one. *Reason:* The defaults add to 33 and the paper has 30 sub-questions, so three must go; chapters 2, 3 and 4 had the largest defaults (5 each), and taking one from each makes chapters 1 to 4 equal at 4 and keeps the defaults of chapters 5, 6, 7 and 8. Marked A2.
13. **Chapters spread over questions.** Every question touches several chapters (matrix in blueprint.chapter_matrix); chapter 5 is asked in Q2, Q3 and Q4 (debugging steps, tools, order of steps), never in Q1 or Q5. *Reason:* A spread stops one question becoming one chapter's test, and the debugging chapter fits the tool and order formats best. Marked A3.
14. **Time per sub-question.** The 60 minutes must be enough: the rates of v1_1_0 section 5 are reused (derived per premise, step and gap by division), plus four allowances of this design: 10 s to read a tip, 30 s per question for its shared text, 120 s for the cover, 8 s per sheet unit. Total 2630 s = 73.1 per cent of 3600 s, within the 90 per cent rule (3240 s). *Reason:* The measure is reused as the brief demands; the allowances cover what the new paper adds (tips, cover, a sheet filled from a separate paper). The 8 s per unit is a guess that is NOT_MEASURED with students. Marked A5.
15. **Why the paper is shorter in time than v1_1_0.** 73 per cent of the sitting is planned (v1_1_0 planned 82 per cent) although the number of sub-questions is the same. *Reason:* Match premises, order steps and gaps are quick and are now counted as sub-questions; the spare time is kept as a reserve for reading the tips and for slower readers.
16. **Bloom rule on sub-questions.** No sub-question at Remember (level 1): 0 of 30. Levels: Understand 3, Apply 16, Analyze 9, Evaluate 2, Create 0. Apply and above 27 of 30 (the rule: majority); Analyze and above 11 of 30 (the rule: at least 8). *Reason:* The brief's rule, with Remember no longer allowed (N1). Create cannot be asked on a paper where nothing is written. Marked A4.
17. **Bloom rule on points.** Of the 100 base points, 91 are at Apply and above (the rule: at least 50) and 32 at Analyze and above; counted again in the check from the sub-question table. *Reason:* The Owner's emphasis on use and reason is also a weighting wish; a rule by item count alone could be met with cheap sub-questions, so the points are tested too.
18. **What a sub-question asks.** Every sub-question has a field asks: use (how a construct is used), reason (why it exists) or effect (what changes). Counts: use 13, reason 7, effect 10. *Reason:* N4 of the brief: no sub-question asks for a name, keyword, definition, signature or syntax detail; the Owner's last sentence is read as: not syntax trivia, why a construct exists and how it is used matter more than its name.
19. **No memorisation (N1).** Bloom level 1 is not allowed; an item that can be answered by recalling a name, keyword, definition, function signature or syntax detail fails the item check; the answer must follow from reading the code or the situation. *Reason:* N1 of the brief.
20. **Terms and tips (N2).** Each sub-question has terms (the specific terms it uses, possibly none) and tip (a short phrase of at most 20 words printed with the stem, or a margin line, that says what the term means). If terms is not empty the tip is not empty; the correct answer never depends on knowing the term's name; the tip never repeats an option text. *Reason:* N2 of the brief: students are not forced to remember terminology, and are helped when a term is used.
21. **Abbreviations in full at first use (N3).** The engine keeps a registry of short forms (short, full form) for the whole paper including the cover; in print order, the first occurrence of each short form must be the full form followed by the short form in brackets, e.g. 'integrated development environment (IDE)'. A scan of the assembled text fails the paper if any all-capital token of two or more letters, outside the registry's exceptions (option letters, form mark), appears before its expansion. *Reason:* N3 of the brief; the scan is a function of the design check with fixtures of known answer.
22. **Stem length (N5).** The stem keeps the Owner's 10-to-30-word rule; the tip is not counted in the 30 words. *Reason:* N5 of the brief; a tip is a separate printed part, so a stem plus tip can run longer without breaking the rule on the stem.
23. **New item fields.** The item model of v1_1_0 (17 fields) gets five new fields: question (Q1 to Q5), sub (a, b, c, ...), tip, terms, asks. The item validator is extended by the next task (TK4_ItemRules2); this design only fixes the fields. *Reason:* The brief names these five fields; the validator v1_0_0 stays as committed and checks exactly 17 fields.
24. **Item types.** The six kept types stay (mcq, predict, match, order, blank, cloze); the eleven dropped types stay dropped. Per question: Q1 predict and mcq; Q2 blank and cloze; Q3 match and mcq; Q4 order and mcq; Q5 mcq. *Reason:* The brief builds the formats from the six kept types.
25. **Seeds and near-copy rule.** Page-interactive questions remain seeds only; every item passes the near-copy measure of v1_1_0 section 2.1 (04-assessment/exams/exam_nocopy_v1_0_0.py). *Reason:* The Owner's earlier decision that still holds.
26. **Page budget: 6 pages.** Six pages: cover, four pages of questions, one page of answer sheet. Four in total is not possible at a readable size. *Reason:* Estimated 302 lines against 224 available in two pages; see page_budget.why_not_four. The estimate is checked by the engine's measurement.
27. **Page budget: levers.** Option layout first, code width second, spacing and margins third; the type size is never a lever. *Reason:* The Owner asked for better formatting and readability on 6 pages; the engine measures, and no text is squeezed below readable size.
28. **How the engine measures pages.** Paper as .docx converted by LibreOffice to PDF; pages read with pdfinfo; fill of the last question page read from the lowest text line; the sheet pages come from the module's layout. Word's own layout is NOT_MEASURED. *Reason:* The measure must be a tool run, not an estimate; the environment has soffice and pdfinfo. Word may differ, so a spare of 8 per cent is kept.
29. **Answer sheet.** The SEN0401 answer sheet module (sen0401_exam_answersheet_v1_0_0.py) and reader (v1_1_0) are reused unedited. Units: one per sub-question and the form mark F: 14 choice, 5 match, 4 order, 8 bank (7 gaps and F) = 31 units, measured 1 sheet page in the module's own layout. *Reason:* The brief and the coordinator's acceptance of 2026-11-01 (the reader needs exact bubble positions). Fewer units than v1_1_0 (54) because a gap, premise or step is now one sub-question, not three units per item.
30. **Sheet unit order.** Units run in paper order Q1a ... Q5d after F; consecutive units of one kind form blocks of at most 5 (choice, match, order) or 3 (bank) closed by the module's left-blank row. *Reason:* The module groups consecutive units of one kind; paper order keeps the student's transfer simple.
31. **Bonus in the total.** Q5 is reported on its own line; the paper's score is Q1 to Q4 (out of 100) plus Q5 (up to 10), so the highest mark is 110. Capping at 100 for the course grade is a separate decision of the Owner. *Reason:* The Owner wrote '100 plus up to 10 bonus'. Marked A8.
32. **Key.** One key per paper and form: an editable .docx for people (answer, points, reason, the tip and a note on the chapter for every sub-question) and a machine key (JSON with SHA-256 over its content) with answer and points of every sheet unit. The key is refused when kind, form or version differ from the form mark in unit F. *Reason:* The brief asks for the key as .docx; the machine key keeps the v1_1_0 rule of a digest-sealed key file.
33. **Outputs.** Paper A and B as .docx; key A and B as .docx; the machine keys as JSON; the answer sheet as one position-exact PDF with its layout file, built by the SEN0401 sheet module; no QTI, no interactive HTML. *Reason:* The brief.
34. **Two forms.** Forms A and B have the same structure: the type, points, Bloom level and sheet unit of every position are equal; B reorders sub-questions only within a question among positions of the same type, points and Bloom level (a position with its own points, such as Q1f, keeps its place), and reorders options; so one sheet layout serves both. *Reason:* Equal positions keep the key points and the sheet identical; reordering stops neighbours copying.
35. **Letters.** Of the 14 choice sub-questions the keys are A 4, B 4, C 3, D 3 (differ by at most one); no letter is the key of three in a row; the match answers use A to G with five different letters. *Reason:* Same intent as v1_1_0 section 5 for a smaller number.
36. **Chapter 5 critical points are missing.** The repository has critical points for chapters 1 to 4 and 6 to 8 only; chapter 5 has a question bank and a chapter-code manifest but no critical-points file. The 3 sub-questions that have chapter 5 as first chapter therefore cannot yet satisfy the item rule that links an item to a critical point. This design records the gap; it does not create the file. *Reason:* The item validator (R06, R07) needs the link; creating the critical points is another task (it needs the chapter 5 deck read), and inventing them would break the rules. See owner_decisions.open_gaps.
37. **Reuse of the sheet title.** The module prints the title SEN0401 answer sheet; the engine overprints the title line on the rendered PDF (a white box with the SEN0414 text) without editing the module, and a person looks at the result once. *Reason:* Carried from v1_1_0 question Q6 with the same default; the module cannot be edited. Marked A9.
38. **Nothing committed is edited.** All files are new versions; v1_0_0 and v1_1_0 design, check and validator files stay. *Reason:* The rule of the executors.
