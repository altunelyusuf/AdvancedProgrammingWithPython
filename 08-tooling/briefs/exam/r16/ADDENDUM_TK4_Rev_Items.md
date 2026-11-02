# Addendum to the brief of TK4_Rev_Items (session SEN0414-EX-rev-items)

Pass this file TOGETHER WITH `08-tooling/briefs/exam/r15/BRIEF_TK4_Rev_Items.md`, unedited. Where the two differ, this addendum wins. It exists because the controller's runs of the finished validator task (commit 0da99d1) and sheet task (commit 9f74ac1) settled points the first brief left open.

## 1. The validator you must use
- Use `exam_item_check_v1_2_0.py` in `/home/claude/CME/exams/SEN0414/04-assessment/exams/` (NOT v1_1_0). It keeps R01 to R24 unchanged and adds R25 to R29 (stem 10 to 20 words and one sentence; no tip, bracket definition or answer-format line in the stem; scope against the taught vocabulary; answer_format; tip field).
- Run it with the environment variable `SEN0414_ROOT=/home/claude/AdvancedProgrammingWithPython` (that repository holds `03-materials`, `08-tooling` and the points files; the CME copy does not): `SEN0414_ROOT=/home/claude/AdvancedProgrammingWithPython python3 exam_item_check_v1_2_0.py check ITEMS.json`. Exit 0 means no failure.
- The failure list of the old midterm list is in `item_rules_v1_2_0_failures_v1_0_0.md` (same folder): read it, it names what to rewrite.

## 2. answer_format is a field of every record
- Every record carries one extra field `answer_format` (the optional 23rd field of the validator): the closed sentence of its unit kind from design v1_3_0 (`answer_format.closed_list`): choice "Choose one letter."; match "Choose one letter from the list."; order "Give the place of this step, from 1 to 4."; bank (blank and cloze gaps) "Give the code of one bank word."; by hand "Write your answer in the boxes." Rule R28 checks it. Never invent another sentence.

## 3. Tips: the binding limit is 12 words, not 25
- R20 (unchanged, not weakened) allows a tip of at most 20 words; the design's 25 is only an outer figure. A tip of 21 to 25 words still fails R20.
- The tips of all records are printed together on page 2 of the answer sheet (sheet v2.0.0 in `/home/claude/CME/exams/SEN0414/08-tooling/exam/`). The controller measured what page 2 holds: 10 tips of 25 words, 15 of 20 words, or 26 of 12 words; a fuller page is refused. With 18 records the tips must be short: write each tip in at most 12 words, or `none` where the record needs none. Before you report, prove it: build the sheet layout with your real tips (`sen0414_exam_answersheet_v2_0_0.build_layout`, from the folder above) and report that it raised no SheetOverflow.
- The tip figure is a stipulation the Owner will be asked about; implement 12 words now and report the figure and the measured capacity.

## 4. Scope (the taught vocabulary)
- Use only what the vocabulary `taught_vocab_ch1_8_v1_0_0.json` holds (built from the latest deck of each chapter 1 to 8). `capitalize` and `fromkeys` are NOT taught: records Q4b (capitalize) and Q5d (fromkeys) of the old list must be rewritten without them. Rule R27 fails any untaught code name, built-in, method or module.

## 5. What stays as in the first brief
One form (the midterm paper list), 18 records, 30 units, 100 points plus the 10-point bonus question, the chapter quotas, the scoring points/(k-1), the files `items_v3_0_0.json` as NEW files in CME, nothing in the public repository, no gate weakened, results reported as printed.
