# Handover: the owner's rulings on decks and pages, and what the check finds on this course today (v1.1.0, 2026-11-14)

**To:** the next session of this course. **Kind:** rulings to apply, with a measured baseline. Nothing in this repository's chapters was changed; one tool was added to `08-tooling`. This version replaces v1.0.0: it asks for corrections of chapters already released as done.

## What the owner said (2026-11-14, 11:54)
The newly built slides keep the old habits. Slides are not meaningful or informative. Code is not always in the HTML file. The HTML keeps lambda-based code that complicates it for no reason. Presenter notes are insufficient. `>>` stays in code snippets. He asked for rulings.

## The six rulings, in plain words
1. **Every slide teaches one thing.** The title says what the slide teaches (at least 4 words, not a bare topic). The slide shows one thing to look at: a picture, a native chart, a diagram, a table, or code with its result. A student who has only the slide and its notes can say its point in one sentence, and the point ties to a learning outcome of the chapter.
2. **Presenter notes carry the lecture.** 60 to 140 words per content slide (at least 30 on title, part and resources slides), in full sentences; no label prefixes; a code slide's notes say what to point at and what the result shows; the notes lead into the next slide. Short sentences stay; thin notes go. This replaces the earlier "notes are cues".
3. **Slide code lives in one page tab.** Every code example on a slide appears unchanged and in slide order in one dedicated tab named **Slide code**, and the tab runs it. The Code Lab stays separate. This settles the open decision about which tab carries the slides' code.
4. **Code is plain code.** No `>>>`, `...` or `>>` before any line, in a deck or a page. No decorative prompt chip on slides. The printed result is shown beside the code, never inside it.
5. **Only taught Python.** An example uses only what this chapter or an earlier one teaches. `lambda` is not used unless the chapter teaches it; write a named function for a key or callback.
6. **Checks before release.** A deck or page is released only when every automatic condition passes on it and every reviewed condition (the three reviewer roles: academician, faculty reviewer, undergraduate reader) has a recorded verdict. Chapters in progress come first; earlier chapters are corrected after the current work is finished, as the owner ordered on 2026-11-08.

## What the check finds today

Tool: `08-tooling/cme_material_check_v1_0_0.py DECK.pptx PAGE.html` (reads only; it tests 8 automatic conditions; two named conditions, the feature register and the page running the Slide code tab, are not built yet and are not read as passes).

| chapter | slides | code frames | title 4+ words | something to look at | notes 60-140 words | no prompt markers | parses as shown | no lambda | code found in page |
|---|---|---|---|---|---|---|---|---|---|
| chapter 18 | 53 | 128 | 3/41 fail | 1/41 fail | 49/53 fail | 120/175 fail | 112/128 fail | 0/128 fail; page 322 | 36/128 fail |
| chapter 19 | 42 | 57 | 3/31 fail | 1/31 fail | 35/42 fail | 89/94 fail | 57/57 fail | 0/57 fail | no page yet |
Reading the numbers: "failed a of b" counts slides, code frames or checks. A pass on "code in page" means each frame's first line was found anywhere in the page; the one-tab rule is not yet tested.

## What is asked: corrections now
The owner's complaint is about the chapters just built, so they are corrected first, before any other chapter. In scope: SEN0414 chapter 19 (deck released as done, page still to build) and chapter 18, and chapter 20 as it is built.

1. Chapter 19 deck: rewrite the notes of 35 slides, remove the prompt markers from 89 of 94 checks (the decorative `>>>` chip and the markers in code frames), make the 57 frames parse as shown, and lengthen the 3 short titles. Build its page with the **Slide code** tab from the start.
2. Chapter 18 deck and page: the same, for 49 notes, 120 of 175 prompt checks, 112 of 128 frames that do not parse as shown, 3 short titles; 36 of its 128 slide code frames are not found in the page; remove `lambda` from the page code unless taught (322 occurrences).
3. Chapter 20 and later: built under the rulings from the first draft, so the same corrections are not needed again.

After the correction: run `08-tooling/cme_material_check_v1_0_0.py DECK.pptx PAGE.html` on each deck and page and expect every automatic check to pass; record the three roles' verdicts (academician, faculty reviewer, undergraduate reader) on the reviewed conditions (teach-back, notes for code slides, links between slides, the result beside the code). Version each corrected file by the own-version rule (the size of the change sets the step; the build inputs are not counted). Earlier chapters are corrected only after this work is finished, as the owner ordered on 2026-11-08. Report back simply: which chapters now pass and which do not.
