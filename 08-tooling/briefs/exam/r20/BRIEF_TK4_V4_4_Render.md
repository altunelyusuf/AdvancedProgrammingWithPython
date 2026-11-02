# Brief part 4 of 5: TK4_V4_4_Render (executor session SEN0414-EX-v4-4)
Read COMMON_v4_0_0.md first; it is part of this brief.

## Task
Prepare against a synthetic build; render the real files when part 2's build and part 3's grading procedure are committed (poll `git pull --rebase --autostash`).
1. NEW paper renderer `exam_docx_v1_4_0.py` (+ check v1_4_0) copied from the latest: no Q5, directions without penalty and Q5 sentences, legal-copy sentence kept, tip printed under the stem (12 words or fewer), 5 alternatives laid out, no tips page; paper 3 or 4 pages (cover 1, questions 2 or 3), fonts and margins as before.
2. NEW key renderer `exam_key_docx_v1_3_0.py` (+ check): key letters per unit, hand-written values, and the one-page grading procedure from part 3 as its own page.
3. NEW sheet generator `sen0414_exam_answersheet_build_v2_4_0.py` + wording file v1_2_0 + check: ONE page, closed-answer units only (choice 5 bubbles, match 5 responses per premise, order places 1 to 5, bank 5), no tips page, no penalty or Q5 sentence, default wording "Office number 10100. Do not fill it." kept.
4. Real render into `papers_r20/` and the delivery copies `papers_r20/delivery/sen0414_exam_midterm_v4_0_0_{paper.docx,paper.pdf,key.docx,key.pdf,sheet.pdf}` byte-identical to the originals, plus SHA256.txt. Total paper pages + sheet 1 at most 6 (aim 4 or 5): print the page count. View every page as an image and report what you saw. Word is not measured; say so.
Commit renderers first, the real files after.

## Done means
All checks PASS, delivery set complete with SHA256.txt matching, committed to CME.
