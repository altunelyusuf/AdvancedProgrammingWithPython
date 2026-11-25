# From a book's code to one source, one slide and one page: method guide 1.0.1 (over 1.0.0, which stays: 1.0.1 replaces a time claim that had no log and states the measured row length)

Written 2026-11-25 from the work on chapters 10 and 11 of SEN0414 (Lineage11). Every claim names the file or log that shows it (in square brackets). A claim with no file is marked "not proven".

## 1. What the method gives

One JSON file per chapter holds every code example once. From it the tools make the slide code, the page example and the page's "Slide code" tab, so the three cannot differ. [08-tooling/code_source_make_v1_2_0.py, its docstring]

## 2. The steps, in order

1. **Trace.** For each subject of the chapter, find the block of the book's own code. Write the source: book programs as they are; where the book shows a shell session, write a plain program with the result as a comment. Every example carries a `book` field that names the book block, or the reason there is none. [03-materials/ch10/source/ch10_code_source_v1_3_0.json, 03-materials/ch11/source/ch11_code_source_v1_4_0.json]
2. **Make.** `python3 08-tooling/code_source_make_v1_2_0.py SOURCE.json OUT_DIR` writes the examples list, the examples module for the deck builder and the Slide code tab. Running it twice gives identical files. [same docstring]
3. **Build the deck.** `python3 08-tooling/chapter_deck_build_v2_9_0.py SPEC_DIR`, run from the repository root. The spec folder holds the words, the notes and the output paths; the builder holds no chapter text and runs every example in slide order, so every printed result comes from a run. [08-tooling/chapter_deck_build_v2_9_0.py, docstring; 08-tooling/ch10-deck/spec_v4_5_0/spec.py]
4. **Run the deck checks.** Standard (`sen0414_deck_standard_check_v1_3_0.py NN DECK MANIFEST`), fit, layout, notes, overlap, reader notes and story prose; each writes one log. [08-tooling/ch10-deck/logs_v4_5_0/, 08-tooling/ch11-deck/logs_v4_4_0/]
5. **Run the code check.** `python3 08-tooling/code_check_v1_2_0.py SOURCE.json --manifest M --deck D --page P`. It fails when the manifest differs from the source (C1), a slide does not hold the code in exactly one box (C2), the page does not hold the code as one whole string (C3), the example does not run (C4), or the shown code does not run alone, which is what a student who copies the one box gets (C5). [08-tooling/code_check_v1_2_0.py, docstring]
6. **Export the lecture text.** `ch10-deck/lecture_export_v2_0_0.py DECK PYTHON_VERSION` writes the slide titles and notes that the page's lecture tab shows. A page built without this step shows the notes of an older deck: chapter 10's lecture tab had still described the earlier 24-slide deck until it was re-exported. [08-tooling/ch10-page/lecture_v1_0_0.json, lecture_v2_0_0.json]
7. **Build the page.** Page data, then the page, with the next page version in the environment and an underscored version (`9_25_0`): `PAGE_VER=9_25_0 python3 08-tooling/sen0414_page_data_v2_30_0.py NN /usr/bin/python3.13`, then `PAGE_VER=9_25_0 PAGE_TEMPLATE=course_page_template_v9_54_0.html python3 08-tooling/sen0414_page_build_v4_18_3.py NN`. A dotted version writes wrongly named files. [08-tooling/ch10-page/page_data_v9_25_0.json]
8. **Run the full page test.** `PAGE_TEST_FILE=sen0414_page_test_v9_41_0.py flock /tmp/page_test.lock python3 08-tooling/sen0414_page_test_run_v1_1_0.py NN 9_25_0`. It takes several minutes per chapter; run it in the background and read the last lines (`RESULT: PASS`). [08-tooling/ch10-page/logs_v9_25_0/page_test.log, 08-tooling/ch11-page/logs_v9_26_0/page_test.log]
9. **Check stories.** `python3 08-tooling/sen0414_story_repeat_check_v1_0_0.py 1 25` lists stories that overlap an earlier chapter; read each pair before release. [its output on 2026-11-25 listed two Ken Thompson pairs for chapter 10]

## 3. Rules that the work taught

- Every changed file gets its own new version; earlier versions stay. A manifest that names a deck is a changed file when the deck changes. [08-tooling/cme_version_check_v1_0_0.py exits 0; chapter_code_ch10_v1_7_0.json beside v1_6_0]
- A table row that wraps pushes the table over the slide number. Chapter 10's tables of 8 or 9 rows failed the overlap check on two slides until their longer rows were shortened; the longest row left in those tables is 89 characters. The overlap check finds it. [08-tooling/ch10-deck/logs_v4_5_0/overlap.log after the rows were shortened]
- A check that encodes a rule must change when the rule changes: the standard's D4 asked for an everyday analogy until the Owner ruled on 2026-11-24 that none belongs in the materials; check 1.3.0 accepts the plain "IN SHORT" box. [08-tooling/sen0414_deck_standard_check_v1_3_0.py]
- Windows is the default environment: a hidden set-up step lets the same code run with Windows paths. [08-tooling/sen0414_windows_setup_v1_1_0.json]
- Set examples to fixed seeds and sorted listings so the result is the same on every computer. [03-materials/ch10/source/ch10_code_source_v1_3_0.json, fields `book` of glob, fileinfo, quizquestion]
- Notes are for the reader, 60 to 140 words, with no direction to a presenter. [08-tooling/ch10-deck/spec_v4_5_0/notes_v4_4_0.py; the reader notes check logs]
- One lineage stage per commit, every check logged; work reaches the register before a file. [07-lineage/sen0414_ch1011simp_lineage_v1_46_0.ttl to v1_49_0.ttl]

## 4. What was proven, and what was not

Proven on chapters 10 and 11 (18 and 19 examples, 41 slides each):
- Code check C1 to C5: 0 findings on both chapters. [08-tooling/ch10-page/logs_v9_25_0/code_check_C1_C5.log, 08-tooling/ch11-page/logs_v9_26_0/code_check_C1_C5.log]
- Full page test: 410 and 414 features passed, 0 failed. [the two page_test.log files above]
- Three tools work on both chapters and hold no chapter text: the source step, the code check and the deck builder. [a search of the three files for "chapter 10", "chapter 11", "ch10" and "ch11" finds nothing]

Not proven:
- **Traced to the book.** 27 of the 37 examples are traced to a block of the book; the other 10 (one in chapter 10, nine in chapter 11) name a reason, usually that the book shows the subject in its text or as a task but gives no code. [the `book` fields of the two source files]
- **Independent review.** The three-role reviews were made by the agent that built the materials and are not independent. [07-lineage/sen0414_ch1011simp_lineage_v1_26_0.ttl]
- **Other chapters.** The method was not run on chapters 1 to 9 or 12 to 25 as a whole; only the exam results change reached chapters 1 to 9 and 12 to 20, and those pages have only the focused test, not the full one. [07-lineage/sen0414_ch1011simp_lineage_v1_44_0.ttl]
- **Other courses.** The page data, page build and page test tools carry the course's name and its template; another course needs its own equivalents of steps 6 to 8. [the file names, `sen0414_*`]
