# Brief for the executor session SEN0414-MS-ch04 (repair round, same task)

Task TK_MS_Ch04_Build (story ST_MS_Ch04) stays the task: it is still in progress in the register because the controller's runs found one failing gate. This brief is the repair round. Session name: **SEN0414-MS-ch04**. The coordinator passes it unedited and gives the real start instant (date -u) of the repair round; the lineage agent records it.

## Why this round exists
The controller ran page test 9.38.0 twice on your page `03-materials/ch04/page/sen0414_ch04_page_v9_92_1.html` (logs `08-tooling/control-ms-logs/pagetest_9_38_0_ch04_v9_92_1_ctl1.log` and `_ctl2.log`). Both runs printed the same result: 414 features passed, 2 failed, RESULT: FAIL. The failing check is D5 "no code of the page has a lambda (data, quiz, question bank, Playground samples, every code box)": 25 places carry the word lambda. Page test 9.37.0 passed (406/0), the deck checks passed, and the deck v3_2_0 and manifest v1_2_0 have no lambda. Everything else stays as it is.

## The task
Build the next page version above v9_92_1 (name it `sen0414_ch04_page_v9_92_2.html`, or the next free number) with NO occurrence of the word lambda anywhere in the page: page data, concept bodies, findings, notes, quiz, question bank, Playground samples, every code box.
- The occurrences sit in the research ontology files the page data builder reads (the Lambda-expression concept, its paragraphs, its example, its io record, findings, sources) and in the texts that mention it (for example `data.findings[8][1]`). Find all 25 places with the page test's own D5 listing: run `08-tooling/sen0414_page_test_v9_38_0.py` once on the new page and read the D5 line in full; do not guess.
- Chapter 6 did the same repair: see commit 0031751 (ABox 2_0_1 and document 2_0_1 without lambda, rewritten examples, page v9.91.1). Copy that method. Research files change as NEW versions beside the old ones (domain ABox next above 1_3_2, document next above 1_3_0, and the others only if they carry the word); a committed file is never edited.
- Take the Lambda-expression concept out of the page's concept set and remove every sentence and link that points to it; the connected concepts must stay connected (no orphaned class). Do not replace the word by a synonym that still teaches lambda. The deck v3_2_0 already omits it, and the page must teach what the deck teaches.
- Keep the manifest `chapter_code_ch04_v1_2_0.json` unchanged (25 examples): the page's Chapter Examples tab equals it in slide order. The page, deck and manifest must stay equal name for name.
- If removing the concept breaks a research gate (RDODI gates, SHACL, subset proof) in a way you cannot repair with new versions of the research files, STOP and report the failing gate verbatim. Do not weaken the D5 gate, a threshold or a test, and do not edit page test 9.38.0.

## Tool versions to use (same as your v9.92.1 build)
Template 9.53.1, page builder 4.18.3 (or the newest 4.18.x you used for v9.92.1), page-data builder 2.27.0 (new version file only if you must change it), page tests 9.38.0 and 9.37.0 through the runner (`08-tooling/sen0414_page_test_run_v1_1_0.py`, system python3, `PAGE_TEST_FILE=...`), the leak probe, Playground width probe, story-layout probe and diagram audit as for chapter 6/8.

## Done means (the controller re-runs all of these itself)
- The word lambda is absent from the page bytes (case-insensitive).
- Page test 9.38.0: RESULT PASS with 0 failed features, on a quiet machine; page test 9.37.0: PASS.
- Leak probe, Playground width probe, story-layout probe and diagram audit pass; the Chapter Examples tab equals the manifest.
- Report each run verbatim; a FAIL stays a FAIL; NOT_MEASURED and CANNOT_RUN are not passes. The main-thread budget check needs a quiet machine: run the page tests alone, under `flock /tmp/page_test.lock`, and say if the machine was busy.

## Rules of an executor
- You are an EXECUTOR session. You do NOT touch the register (07-lineage); the lineage agent records your start and controls your result by its own re-runs.
- First `git pull --rebase --autostash` in /home/claude/AdvancedProgrammingWithPython. Commit ONLY your own new files (chapter 4 folders and your chapter-4 tool files), never `git add -A`; message ends with the task identifier in parentheses; before each push `git pull --rebase --autostash`; on a rejected push pull --rebase and push again, never force. Commit and push each verified step at once.
- Several sessions share 2 cores and a small disk (about 960 MB free): STOP and report if free space falls under 0.8 GB; delete your own scratch folders when done. No heavy parallel runs.
- Never invent a term, fact or source. Wait inside your turn for results; never schedule a wake-up.
- Final report to the coordinator: commit SHAs, new files, the verbatim output of every gate you ran, achieved / not achieved in plain words.
