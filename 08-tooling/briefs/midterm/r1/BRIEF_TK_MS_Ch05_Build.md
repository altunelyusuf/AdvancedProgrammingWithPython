# Brief for the executor session SEN0414-MS-ch05

Task TK_MS_Ch05_Build (story ST_MS_Ch05), written by the lineage agent for the Owner's midterm scope. Executor session name: **SEN0414-MS-ch05**. Estimated 4.0 hours of agent work (an estimate: nobody has witnessed a start; the real start is recorded at work begun).

## The task
**Bring SEN0414 Chapter 05 (Debugging) to the Chapter 8 Friday standard: new deck, new manifest, new page, as new files.**
- Newest now: deck `03-materials/ch05/SEN0414_Ch05_Debugging_3e_v3_0_0.pptx`, page `03-materials/ch05/page/sen0414_ch05_page_v9_90_0.html`, manifest `03-materials/ch05/page/chapter_code_ch05_v1_0_0.json`.
- Build: the deck as the next version above the newest deck (`v3_1_0` in its name; the generator under `08-tooling/ch05-deck/` as new files), the manifest `chapter_code_ch05_v1_1_0.json`, then the page `03-materials/ch05/page/sen0414_ch05_page_v9_91_0.html` with its page data, corpus manifest and builder files as new files, on template v9_53_1. Order: deck and manifest first (push the manifest early), then the page built from the manifest.

## Measured gap of the newest deck (the lineage agent's runs of 2026-11-01; fix exactly these, nothing more is asked to be re-measured)
- deck check v1.1.0: D3 FAIL code slides: explanation beside the code + executed result as a visual | 12 of 21 code slides complete (57%); without explanation: [8, 10, 13, 15, 22, 23, 31, 36]; without visual result: [9, 13, 15, 22]
- deck check v1.1.0: M1 FAIL chapter-code manifest equals the deck's code boxes (text, order) | 0 of 21 deck code slides equal their manifest example in text and order; differences: ['20 manifest examples, 21 deck code slides', 'example 1 (slide 7): c
- deck check v1.1.0: SUMMARY PASS=11 FAIL=2 NOT_MEASURED=0 | failing: D3,M1
- controller C1-C8: [FAIL] C1 no prompts  slide 7: prompt line '>>> def box_print(symbol, widt'; slide 7: prompt line '>>>     if len(symbol) != 1:'; slide 7: prompt line ">>>         raise Exception('S"; slide 7: prompt line '>>>     if width <= 2:'
- controller C1-C8: [FAIL] C2 no lambda  slide 38
- controller C1-C8: [FAIL] C3 indentation  slide 7: line 1 ends with a colon and the next line is not deeper; slide 7: line 2 ends with a colon and the next line is not deeper; slide 7: line 2 ends with a colon and the next line is not deeper; slide 
- controller C1-C8: [FAIL] C4 no 5N1K labels  slide 6: label word 'WHO'; slide 6: label word 'WHAT'; slide 6: label word 'WHEN'; slide 6: label word 'WHERE'; slide 6: label word 'WHY'; slide 6: label word 'HOW'; slide 18: label word 'WHO'; slide 18: 
- controller C1-C8: [FAIL] C5 notes 40-60 words  slide 2: 32 words (needs 40-60); slide 3: 30 words (needs 40-60); slide 5: 29 words (needs 40-60); slide 6: 33 words (needs 40-60); slide 7: 29 words (needs 40-60); slide 8: 27 words (needs 40-60); sli
- controller C1-C8: [FAIL] C6 every code box compiles  slide 7: invalid syntax; slide 7: invalid syntax; slide 7: invalid syntax; slide 7: invalid syntax; slide 8: invalid syntax; slide 8: invalid syntax; slide 9: invalid syntax; slide 9: invalid syn
- controller C1-C8: [FAIL] C8 manifest equals code boxes in order  example 1 (boxprint) is not a code box of the deck after example 0; example 2 (exceptionobj) is not a code box of the deck after example 1; example 3 (unwinding) is not a code box of 
Also check by reading, not by a new tool: the page's own code (chapter-code tab, Playground starter, exercises, exam items) for `>>>` and lambda; the page does not yet have full screen or a resizable panel on every diagram (template v9_53_1 gives it) and its chapter-code tab does not equal the deck code in slide order.

## Done means (the lineage agent will run these itself on your files, once each plus the repeated page test)
- deck check v1_1_0: SUMMARY PASS=13 FAIL=0; teaching check T1 to T6 met; overlap check CLEAN; controller checks: no prompt, no lambda, indentation, no label words, notes 40 to 60 words, compile, numbered, manifest equals the deck code.
- page test 9.38.0 and 9.37.0 pass on the final page, the leak probe, Playground width probe, story-layout probe and chapter check as for Chapter 8; page code equals the manifest, name for name, in order.

## Why this work exists
The Owner (12:13 and 12:26 Istanbul, 2026-11-01, recorded as relayed): the slides and the interactive page of the midterm chapters must reach the quality of the Chapter 8 work of Friday 2026-10-30, and the slide code must match the page's Chapter Examples tab. 'Simplify the tasks of the agents to concentrate on the issues we have solved on Friday, and pass the useless effort spent to remeasure the already succeeded parts.'

## The Friday fixes, and only these (copy how Chapter 8 did each; do not invent a new method)
1. No `>>>` and no `...` prompt in any slide code box, note or page code the student copies. (The small brand-mark text box `>>>` in the corner of content slides stays exactly as it is.) Show a script; show its output separately as the result visual. Every result shown comes from really running the code.
2. No lambda anywhere (slides, notes, manifest, page chapter-code tab, Playground starter, exercises, exam items, answers) unless the chapter teaches lambda (it does not unless its research says so; if you find it does, STOP and tell the coordinator). Use a def function or a method reference.
3. Python indented per the standard: four spaces per level, a body line deeper than its header, no tabs, no one-line compound statements, no wrapped lines (widen the box). Every box compiles (`ast.parse`); a deliberate-error box says so on the slide and in the manifest.
4. The slides teach alone: for every concept, short full sentences (no text box over 30 words), an everyday analogy, a drawn diagram or native chart, the code, and its executed result as a visual. The page already explains well with visualisations: bring that teaching into the deck.
5. 5N1K as storytelling: who, what, when, where, why and how as connected natural sentences with real names, dates and places, a real free-licence picture (provenance in the assets file) and a live link. No label words (WHO, WHAT, ...) at line starts, no `WHAT:` forms, no heading that spells out the six questions.
6. Speaker notes 40 to 60 words on every slide (title and divider slides 25 to 60): what to tell, one example, one question for the class.
7. Slide code = one page tab: the new manifest `chapter_code_chNN_<new>.json` lists the deck's code boxes by NAME in slide order; the page's Chapter Examples tab equals it in text and order. PUSH THE MANIFEST FIRST (within about 45 minutes of your start); after that its examples change only by a new manifest version you announce.
8. Page on template `08-tooling/course_page_template_v9_53_1.html` (the Chapter 8 template: full screen and a user-resizable panel for EVERY diagram, controls never covering a figure, zoom and text-size kept) with a Lecture tab matching the deck (as the Chapter 8 page v9_92_1 has), clean layout, usable on phones.

## How to work (reuse, do not rebuild)
- Chapter 8 is your model: deck `03-materials/ch08/SEN0414_Ch08_Strings_3e_v2_1_0.pptx` and its generator `08-tooling/ch08-deck/` (v2_1_0 files), manifest `03-materials/ch08/page/chapter_code_ch08_v1_1_0.json`, page `03-materials/ch08/page/sen0414_ch08_page_v9_92_1.html` with its data `08-tooling/ch08-page/` (page_data_v9_92_1.json, corpus_manifest_v9_92_1.json, playground_width_check_v9_92_0.py, diag_audit_run_v9_92_0.py, fixtures_9_38_0) and the page builders it used (read the git log `git log --oneline | grep -i "chapter 8"` and the commits of tasks TK_U8_Deck_Build and TK_U8_Page_Build to see exactly what was changed).
- Existing tools, all unchanged and reused: deck check `08-tooling/sen0414_deck_standard_check_v1_1_0.py`, teaching check `08-tooling/sen0414_deck_teaching_check_v1_0_0.py`, overlap check `08-tooling/sen0414_deck_overlap_check_v1_0_0.py`, page tests `08-tooling/sen0414_page_test_v9_37_0.py` and `v9_38_0.py` (under `flock /tmp/page_test.lock`), leak probe v1_3_0, story-layout probe, chapter check `08-tooling/sen0414_lineage_chapter_check_v1_2_0.py`. New files for this chapter (generator, data, manifest, page) are NEW versions; no committed file is edited. Gates are never weakened; NOT_MEASURED and CANNOT_RUN are not passes.
- Do NOT re-measure what already passes and do not write new checks. Fix the failing items below; then run the existing gates ONCE on your final files and report the output exactly as printed (a FAIL stays a FAIL; if the page test fails, fix the cause and run again, reporting every run).
- Content that already passes (research, stories, pictures, analogies, diagrams, quiz, resources) is kept and adapted, not re-created.

## Rules of an executor
- You are an EXECUTOR session. Do the one task below. You do NOT touch the register (07-lineage); the lineage agent records your start and controls your result by its own re-runs.
- First `git pull --rebase --autostash` in /home/claude/AdvancedProgrammingWithPython. You commit ONLY your own new files (your chapter's folders and your own new tool files named with your chapter), never `git add -A`; message ends with the task identifier in parentheses; before each push `git pull --rebase --autostash`, and on a rejected push pull --rebase and push again (never force). Commit and push each verified step at once: the repository is the only record if the container restarts.
- Several executors run at the same time on 2 shared cores and a small disk (about 1.1 GB free): no heavy parallel runs; page tests only under `flock /tmp/page_test.lock`; delete your own scratch and temporary folders as soon as you no longer need them; STOP and report if free space falls under 0.8 GB.
- Wait inside your turn for results; never schedule a wake-up. Never invent a term, fact or source. No personal data of students.
- STOP and report, without working around it, if: the task needs a committed file edited; a gate fails and you cannot fix it within your task; anything here contradicts what you find.
- Final report to the coordinator: commit SHAs, new files, the verbatim output of every gate you ran, achieved / not achieved in plain words.
