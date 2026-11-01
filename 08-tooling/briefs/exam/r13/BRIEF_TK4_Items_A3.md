# Brief for the executor session SEN0414-EX-items-a3

Task TK4_Items_A3 (written by the lineage agent for the exam change of 2026-11-01). Estimated 2.0 hours of agent work (an estimate, G120).

**Item set A, version 2.1.0: the records of set A rewritten so that set A plus set B build a paper in the engine**

Depends on: none (TK4_Items_A2 and TK4_Items_B2 are written; TK4_Items_B2 stays open until the merged lists build)

## Why this task exists and what is settled (controller's ruling, r13)
Set A (items_a_v2_0_0) and set B (items_b_v2_0_0) are each valid and add up to 30 units with the right points, but the engine v1_1_0 refuses both merged lists on E03 (units per chapter against the quota 4, 4, 4, 4, 3, 4, 4, 3: the paper has chapter 3 ten times, chapters 1, 2 and 8 once) and on E09 (cross-chapter minimum 9: the paper has 8, the make-up 6). The cause is that set A was written without the design's plan for each unit. Nothing is wrong with the engine. THE RULING:
1. The design v1_2_0 gives every unit (gap, premise, step, choice) its own chapter, points, Bloom level and asks (the table below). A record follows it unit by unit.
2. For a match, order, blank or cloze record the list `chapters` holds EXACTLY one chapter per unit, in the order of the units (no shorter list: the engine would cycle it). A bank of four gaps from chapters 1, 2, 3, 4 is one program or text in which each gap needs the idea of its own chapter; a match of five premises takes one premise from each of chapters 1 to 5; an order of four steps takes chapters 3, 5, 6, 7.
3. For a one-unit choice record the first entry of `chapters` is the chapter the engine counts for it; further entries make it cross-chapter. The nine cross-chapter units of the design are Q1f, Q3f, Q3g, Q4e, Q4f, Q5a, Q5b, Q5c and Q5d; the four of set B (Q3c, Q4c, Q5c, Q5d: chapters 8, 4, 6, 7 first) stand for Q3g, Q4f, Q5c and Q5d, so SET A MUST BRING FIVE: one for each of Q1f (chapter 7 first), Q3b (7 first, standing for Q3f), Q4b (8 first, standing for Q4e), Q5a (1 first) and Q5b (2 first), each with at least one further chapter. Indirect (consequence or exception) forms only on the choice records the design marks.
4. Set A keeps its record letters: Q1a to Q1f (six choices: three predict, three mcq), Q2a (blank, four gaps, chapters 1 2 3 4), Q2b (cloze, three gaps, chapters 5 6 8), Q3a (match, chapters 1 2 3 4 5), Q3b (mcq), Q4a (order, chapters 3 5 6 7), Q4b (mcq), Q5a, Q5b (mcq). The records of set B are not changed.
5. Write the new files `items_a_v2_1_0.json` (paper list), `items_a_v2_1_0_makeup.json` (make-up list), a provisional side file, a builder and a check. The old files stay. The make-up list shares no item with the paper list (near-copy rule, both directions) and none with set B. Reuse good wording of v2_0_0 where it already fits the plan; rewrite where it does not.
6. THE CHECK must show, for each list merged with the committed set B (by id): the validator `exam_item_check_v1_1_0.py` 0 failures; units 6/7/7/6/4 and points 25/25/25/25/10; the units per chapter equal to the quota; the cross-chapter count equal to 9 and the indirect count equal to 6; Apply and above 27 of 30 or more and Analyze and above at least 8 of 30; AND `exam_engine_v1_1_0.py build` of the merged pool exits 0 with every rule E01 to E28 passing (use the design `exam_design_v1_2_0.json`, any seed; for the make-up pass `--kind makeup --midterm BUILD.json` of the paper's build record). Report the verbatim output. If the engine still refuses, say which rule and why; do NOT edit the engine, the design, the validator or set B.

## The design's plan, unit by unit (from exam_design_v1_2_0.json)
- Q1a: predict, chapter 1, 4 points, Bloom 3, asks effect
- Q1b: predict, chapter 2, 4 points, Bloom 3, asks effect
- Q1c: predict, chapter 3, 4 points, Bloom 3, asks effect
- Q1d: mcq, chapter 4, 4 points, Bloom 4, asks effect
- Q1e: mcq, chapter 6, 4 points, Bloom 4, asks effect
- Q1f: mcq, chapter 7 (cross-chapter: the record lists two or more chapters, this one first), 5 points, Bloom 4, asks effect
- Q2a: blank, chapter 1, 4 points, Bloom 3, asks use
- Q2b: blank, chapter 2, 4 points, Bloom 3, asks use
- Q2c: blank, chapter 3, 4 points, Bloom 3, asks use
- Q2d: blank, chapter 4, 4 points, Bloom 3, asks use
- Q2e: cloze, chapter 5, 3 points, Bloom 2, asks reason
- Q2f: cloze, chapter 6, 3 points, Bloom 2, asks reason
- Q2g: cloze, chapter 8, 3 points, Bloom 2, asks reason
- Q3a: match, chapter 1, 3 points, Bloom 3, asks use
- Q3b: match, chapter 2, 3 points, Bloom 3, asks use
- Q3c: match, chapter 3, 3 points, Bloom 3, asks use
- Q3d: match, chapter 4, 3 points, Bloom 3, asks use
- Q3e: match, chapter 5, 3 points, Bloom 3, asks use
- Q3f: mcq, chapter 7 (cross-chapter: the record lists two or more chapters, this one first), 5 points, Bloom 4, asks reason
- Q3g: mcq, chapter 8 (cross-chapter: the record lists two or more chapters, this one first), 5 points, Bloom 4, asks reason
- Q4a: order, chapter 3, 4 points, Bloom 3, asks use
- Q4b: order, chapter 5, 4 points, Bloom 3, asks use
- Q4c: order, chapter 6, 4 points, Bloom 3, asks use
- Q4d: order, chapter 7, 4 points, Bloom 3, asks use
- Q4e: mcq, chapter 8 (cross-chapter: the record lists two or more chapters, this one first), 4 points, Bloom 4, asks effect (indirect)
- Q4f: mcq, chapter 4 (cross-chapter: the record lists two or more chapters, this one first), 5 points, Bloom 5, asks effect (indirect)
- Q5a: mcq, chapter 1 (cross-chapter: the record lists two or more chapters, this one first), 3 points, Bloom 4, asks effect (indirect)
- Q5b: mcq, chapter 2 (cross-chapter: the record lists two or more chapters, this one first), 3 points, Bloom 4, asks reason (indirect)
- Q5c: mcq, chapter 6 (cross-chapter: the record lists two or more chapters, this one first), 2 points, Bloom 5, asks effect (indirect)
- Q5d: mcq, chapter 7 (cross-chapter: the record lists two or more chapters, this one first), 2 points, Bloom 4, asks reason (indirect)

## Settled earlier (r12)
1. UNITS AND RECORDS. The design's 30 sub-questions are UNITS: one gap of a blank or cloze bank, one premise of a match, one step of an order, one choice (mcq or predict). An item RECORD is the printed item: one bank, one match set (5 premises, 7 answers), one order set (4 steps), or one choice. Its `points` are the sum of the points of its units; its `id` is question plus the record letter (not the design's unit letter). The units per question must add to the design counts: Q1 6, Q2 7, Q3 7, Q4 6, Q5 4, and the points per question to 25, 25, 25, 25 and 10. Set A holds, per list, Q1 6 units, Q2 7 (a bank of 4 gaps and a cloze of 3), Q3 6 (a match of 5 and one choice), Q4 5 (an order of 4 and one choice), Q5 2 of 4: so 1 unit of Q3 (one choice, 5 points), 1 unit of Q4 (one choice, 5 points) and 2 units of Q5 (2 points each, 4 in all) are still to write. The design JSON and its check do not change: they plan the units; the engine counts units from the records (`gaps`, number of `premises`, number of `steps`, 1) and compares them with the design.
2. LISTS. One list holds one record per id (R02) and ids follow question plus sub (R23); neither rule changes. A form therefore reads its own list: the engine takes one list per form (the paper list, the make-up list), each complete and valid on its own; it may take several files and refuses a list with a repeated id. Set A has `items_a_v2_0_0.json` (paper) and `items_a_v2_0_0_makeup.json` (make-up).
3. SET A (v2_0_0) was controlled (14 records per list, validator 0 failures on the controller's own call, Apply and above 13 of 14, Analyze and above 7 of 14, chapters 1 to 8, no identical stems). Its answer keys of blank and cloze are 0-based positions in the bank; match answers are letters; order answers give the place of each printed step. Choice letters are uneven (A 3, B 5, C 8, D 4); the engine permutes options per form. The near-copy tool reads only the old fields, so the check runs it on a built view; `seed_item` is `none` everywhere because set A was not copied from a page item.
4. ABBREVIATIONS to confirm with the Owner in one line each: JSON = JavaScript Object Notation, IDE = integrated development environment (and the earlier 24 of the registry).


## Why this work exists (the Owner's words of 2026-11-01 13:04 Istanbul, recorded as relayed)
'Use the attached page and fill the generic parts appropriately for each of the exams. Categorize the exam into 5 question format with possible number of sub-questions. If possible 4 questions 25 points and 5th Question is 10 points and bonus. If you can fit overall exam in 4 pages it is fine, otherwise, fit with 6 pages but better formatting and readibility. The abbreviations should be used in full form in their first usage. Never ask memorizing questions and don't force the students to remember a specific terminology. You should support the students with provide tips to remember, if you use a specific term in the exam.' (The attached page is `/home/claude/exam_cover_template/IKU_exam_cover_page_template_source.docx`.) For SEN0414 read his last sentence of that message as: not syntax trivia; why a construct exists and how it is used matters more than its name.
Earlier decisions that still hold: physical printed paper, 60-minute sitting; code on paper is read-and-choose plus fill-the-blank, nothing written freely; page-interactive questions are seeds and are never copied (near-copy rule `04-assessment/exams/exam_nocopy_v1_0_0.py`); chapters 1, 2, 3, 4, 5, 6, 7, 8 (chapter 5 assumed in); Bloom: majority at Apply and above and at least 8 of 30 at Analyze and above; paper and key also as editable .docx, the answer sheet as a position-exact PDF built by the SEN0401 sheet module (the reader needs exact bubble positions; the coordinator accepted this on 2026-11-01, as the SEN0401 owner chose); two forms A and B; the SEN0401 answer sheet module is reused (`/home/claude/sen0401/08-tooling/exam/sen0401_exam_answersheet_v1_0_0.py`).

## The new structure and the new item rules (design v1_2_0 fixes the numbers; until it exists use these)
- Page 1 is the cover page filled from the template. Then FIVE questions: Q1 to Q4 are 25 points each, Q5 is 10 points and is a bonus (total 100 plus up to 10 bonus). Each question has one format and several sub-questions; 30 sub-questions in all (Q1 6, Q2 7, Q3 7, Q4 6, Q5 4) with whole-number points that add to the question total. Formats, built from the six kept item types: Q1 read the program and predict (predict, mcq with listing); Q2 complete the program (blank, cloze with an option bank); Q3 choose the right tool and say why it fits (match, mcq on reasons); Q4 find the effect of a change or put the steps in order (order, mcq on consequences); Q5 bonus, across chapters (cross-chapter and indirect items).
- Page budget: 4 pages in total (cover included, answer sheet included) if it fits; otherwise 6 pages with clearer layout. The engine measures it; no text is squeezed below readable size.
- NEW ITEM RULES: (N1) no memorisation item: nothing asks for a name, keyword, definition, function signature or syntax detail from memory; Bloom level 1 is not allowed; (N2) no required recall of terms: if a term is used, a TIP is printed with it (a short phrase in the stem or in a margin line that reminds what the term means), and the answer never depends on knowing the term's name; (N3) every abbreviation is spelled out in full at its first use in the paper (for example 'integrated development environment (IDE)'); (N4) every sub-question asks about USE, REASON or EFFECT (what happens, why this construct exists, what changes if...), recorded in a field `asks` with one of use, reason, effect; (N5) the 10-to-30-word rule of the Owner on the stem stays.

## Rules of an executor
- You are an EXECUTOR session. Do the one task below; you do NOT touch the register (07-lineage). The lineage agent records your start and controls your result on its own re-runs.
- New versions only: a committed file is never edited; new checks are new files with fixtures of known answer. Never weaken a gate; a FAIL stays a FAIL; NOT_MEASURED and CANNOT_RUN are not passes.
- First `git pull --rebase --autostash`. Commit ONLY your own new files (never `git add -A`); the message ends with the task identifier in parentheses; pull --rebase before each push, retry if rejected, never force. Commit and push each verified step at once.
- Shared machine (2 cores, about 1 GB free disk, other sessions running): no heavy parallel runs; delete your scratch at once; stop and report below 0.8 GB free. Wait inside your turn; never schedule a wake-up. Never invent a term, fact or source. No personal data of students.
- STOP and report, without working around it, if the task needs a committed file edited, a gate fails and you cannot fix it within your task, or this brief contradicts what you find.
- Final report: commit SHAs, new files, the verbatim output of every check, achieved / not achieved in plain words.
