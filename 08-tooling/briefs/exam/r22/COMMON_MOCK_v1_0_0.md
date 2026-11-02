# COMMON text of the SEN0414 mock exam briefs (r22), part of every brief. Supersedes briefs/exam/r21/BRIEF_TK4_Mock_Exam.md (kept as history) and its ADDENDUM_1.

## Why (Owner order 2026-11-03 01:29 Istanbul = 2026-11-02T22:29Z, relayed by the coordinator)
"Now, the most urgent task is to build those mock exam interactive HTML files. If we are late, they will be totally useless." Original ask (00:45): an HTML mock exam for the course, with the option to derive new mock exams again, and NEVER the same questions as the real exam (midterm v4.0.0 items). Time is the main constraint: finish as fast as the rules allow.

## Fixed constraints
1. Scope: chapters 1 to 4 and 6 to 8. Chapter 5 (Debugging) is excluded: no chapter-5 content and no term taught only in chapter 5 (for example raise, logging levels, assert, debugger, traceback reading). Item `chapters` and `source` fields never name chapter 5.
2. The mock has the SAME structure and rules as the real exam: four questions of 25 points, 14 records and 27 units (Q1 six records a to f; Q2 two records: a bank of 4 gaps, b cloze of 3 gaps; Q3 three records: a match of 5 premises with 5 responses, b and c choice; Q4 three records: a order of 5 steps, b and c choice), five alternatives everywhere, right = its points, wrong or blank = 0, no deduction, no bonus, a tip of 12 words or fewer printed under the stem (or none). The slot table (record id = question + sub, type, chapters wanted, Bloom, points) is exactly that of the real set and is in `slot_table_v1_0_0.md` of this folder.
3. Items are NEW. No stem, listing, option set or answer of the real exam items (items_a/b v2, v3_0_0, v4_0_0, v4_0_1, all in CME `04-assessment/exams/items/`) may be reused, even renamed. Authors may read the real items ONLY to know what to avoid; the lineage agent's gate decides. The real exam items and answers never enter any public repository or any HTML file. The exclusion index stays in private CME.
4. Every answer is recomputed by running the code of the listing (the check prints each recomputed answer next to the stored one). Code on the HTML page is a listing with its choices (no live execution is required); runnable behaviour, if shown, must really run.
5. The bank is 6 pairwise-disjoint mock blocks M1 to M6 (84 records), so six derived mocks never share an item. State this exactly in the report and on the page (after six, the page says that a further mock would repeat items and offers a repeat of an earlier mock, never a silent reuse).
6. No student personal data; everything is computed locally in the browser; nothing is sent anywhere.
7. Where files go: all in `/home/claude/CME/exams/SEN0414/04-assessment/mock/` (private CME, new folder, new files only) until the Owner decides where to publish (do not ask him).

## Rules of an executor
- EXECUTOR session; you do NOT touch the register (07-lineage). The lineage agent records your start and controls your result by its own re-runs.
- New versioned files only; no committed file is edited (items, design, engine, validators, deliveries of the real exam stay byte for byte). No gate is weakened.
- First `git pull --rebase --autostash` in /home/claude/CME. Commit only your own new files; never `git add -A`; the commit message ends with your task identifier in parentheses; push, no force. Commit EARLY and often (others wait on you).
- Shared machine, 2 cores, another course's mock runs in parallel: every command under `nice -n 10`; any browser test under `flock /tmp/page_test.lock`; no heavy parallel runs; delete your scratch; STOP and report if free disk is under 0.8 GB.
- Report every result exactly as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN; the last two are not passes). A failing result is never worked around. Never invent a term or fact. Wait inside your turn; never schedule a wake-up.
- Final report to the coordinator: commit SHAs, new files with SHA-256, the verbatim output of every check, achieved / not achieved in plain words.

## The parts (all launch at once; dependencies are polled in git)
- M0 `TK4_Mock_0_Gate` (session SEN0414-EX-mock-0): mock vocabulary, mock item validator, exclusion index and gate, block merge/assembly tool, delivery check. FIRST DELIVERABLE (within about 20 minutes): vocabulary + validator, committed, because authors need them.
- M1 `TK4_Mock_1_AuthorA` (SEN0414-EX-mock-a): slots Q1a, Q1b, Q1c, Q2a for blocks M1 to M6 (24 records).
- M2 `TK4_Mock_2_AuthorB` (SEN0414-EX-mock-b): slots Q1d, Q1e, Q1f, Q2b for M1 to M6 (24 records).
- M3 `TK4_Mock_3_AuthorC` (SEN0414-EX-mock-c): slots Q3a, Q3b, Q3c for M1 to M6 (18 records).
- M4 `TK4_Mock_4_AuthorD` (SEN0414-EX-mock-d): slots Q4a, Q4b, Q4c for M1 to M6 (18 records).
- M5 `TK4_Mock_5_Html` (SEN0414-EX-mock-h): the HTML page, its build script and its browser tests (works on a synthetic bank until the real bank is merged).
After all parts commit, the lineage agent (or M0 on the coordinator's order) merges, builds and controls.

## Data contract (all parts)
Author file: `04-assessment/mock/bank/mock_items_<M1..M6>_<author>_v1_0_0.json` = a JSON list of records in the exact record format of `04-assessment/exams/items/items_v4_0_1.json` (same fields), ids = slot ids (Q1a ... Q4c) as rule R23 requires; `bank_id` = "<M1..M6>". Merged block: `mock_block_<Mk>_v1_0_0.json` = the 14 records in order Q1a..Q4c (this passes the mock validator unchanged as a list). Page data: `mock_data_v1_0_0.json` = {"version": "1.0.0", "blocks": [{"id": "M1", "records": [14 records]}, ... 6 blocks]}.
