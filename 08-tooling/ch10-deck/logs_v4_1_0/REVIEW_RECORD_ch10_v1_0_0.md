# Review record, chapter 10, deck 4.1.0 and page 9.21.0 (2026-11-24)

Reviewed: deck 03-materials/ch10/SEN0414_Ch10_ReadingWritingFiles_3e_v4_1_0.pptx, page 03-materials/ch10/page/sen0414_ch10_page_v9_21_0.html, source 03-materials/ch10/source/ch10_code_source_v1_1_0.json, manifest chapter_code_ch10_v1_3_0.json.
**Who reviewed:** the agent that built the material, once per role. This is NOT an independent review; the owner can overrule any verdict. It reads the four conditions of the Lineage11 goal (teachability, understandability, explainability, human communication) from each of three roles.
Evidence read in this session: the code, printed result, balloon, result balloons and note of all 18 code slides; a rendered contact sheet of the 18 code slides and slides 6, 13, 20, 28, 34, 37 at larger size; the logs of the automatic checks; a separate browser run of all 18 examples on the page.

## What the review found and changed (before the verdicts)
1. The first page test run failed: the shelve example raised ModuleNotFoundError in the browser (it has no dbm module). The source (1.1.0) now carries a hidden stand-in for dbm that is used only when dbm is missing; the shown code is unchanged and still runs alone on Python.
2. The Mad Libs result on the page differed from the slide because the program ended with a value that the page prints. The program now saves the story first and prints it last (source 1.1.0), so slide, page and a plain run agree.
3. The chapter 10 notes and the practice-slide answers still pointed to code that is no longer on the slides (the two bytes of the accent, a TypeError, mode x, a shelf trap); they were rewritten (notes 4.0.0).
4. Slide 6 had only chips as its result; it now has a table of the three ways to write a path. Four notes (slides 24, 30, 34, 36) lacked a link to another slide and were given one.

## Verdicts
| Reviewed condition | Academician (true and sourced?) | Faculty reviewer (teaches to the outcomes?) | Undergraduate reader (can I follow it?) |
|---|---|---|---|
| Teachability: one code, one idea, one result per slide | Met: 18 programs, 15 traced to a block of the book, 3 (modes, encoding, json) with a named reason in the source; each result comes from a run | Met: five parts keep their route; 49 of 49 research concepts covered; no slide added (41) | Met: one box per slide, copyable whole; the sample files are named in the note |
| Understandability: code and wording a beginner can follow | Met: plain programs without the interpreter; Linux prints PosixPath where the book shows WindowsPath | Partly met: the longest code (slide 37, 21 lines) is the book's own program but is dense | Partly met: slides 34 and 37 are dense at small type, readable only on a large screen; no change made |
| Explainability: the note and balloons say why, not only what | Met: notes state what the program does and what it printed, with numbers from the run | Met: notes 80 to 138 words (limit 60 to 140), reader-facing, no presenter direction | Met: balloon, result balloons and note agree with the printed result |
| Human communication: plain sentences, everyday links | Met: everyday-picture slides and four stories unchanged from the approved deck | Met: 49 of 49 concepts have an analogy | Met on the 18 code slides read; the rest of the deck is unchanged from deck 3.0.0 |

## Not covered and still open
- The story facts and links were not re-opened (no network in the shell) and were not changed. The stories of the UTF-8 and JSON slides still repeat stories told in chapters 8 and 7; this awaits the owner's decision (Lineage10).
- The page's per-concept examples (inside the concept panels) still come from the old deck's transcript; they are not the chapter code. Reported to the owner.
- The shelve example on the page uses a stand-in for dbm; on a real Python it uses the real module. The stand-in saves the shelf as one file instead of the operating system's database files.
- The old teaching check 1.0.0 and the builder's older manifest self-check 2.1.0 were not used (they predate the rulings of 2026-11-14 and run code without its hidden set-up).
