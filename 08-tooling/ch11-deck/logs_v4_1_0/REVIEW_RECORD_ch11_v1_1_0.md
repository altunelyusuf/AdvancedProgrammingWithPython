# Review record, chapter 11, deck 4.1.0 and page 9.22.0 (2026-11-24)

Reviewed: deck 03-materials/ch11/SEN0414_Ch11_OrganizingFiles_3e_v4_1_0.pptx, page 03-materials/ch11/page/sen0414_ch11_page_v9_22_0.html, source 03-materials/ch11/source/ch11_code_source_v1_2_0.json, manifest chapter_code_ch11_v1_4_0.json.
**Who reviewed:** the agent that built the material, once per role. This is NOT an independent review; the owner can overrule any verdict. It reads the four conditions of the Lineage11 goal (teachability, understandability, explainability, human communication) from each of three roles.
Evidence read in this session: the code, printed result, balloon, two result balloons and note of all 19 code slides side by side; a rendered contact sheet of 19 code slides and slides 7 and 13, 20, 26, 34 at larger size; the logs of the automatic checks.

## What the review found and changed (before the verdicts)
1. The notes, result balloons and some takeaways of the 19 code slides were still written for the old several-box code (they spoke of a first, second and third box, of 300 and 500 bytes, of snap.zip). They were written again (notes 4.0.0) from what each program and its sample files really print.
2. Two codes used os without importing it, so a student who copies the one box got a NameError (unlink, archives). The imports were added to the source (1.2.0) and a new check C5 (shown code alone runs after the set-up) was made; it fails the old source on exactly these two and passes the new one.
3. Three slide titles named things the code does not show (glob and rglob, bytes per folder, all ZIP modes); they were renamed to match their code.
4. The copytree result visual said "same names in both: False" on a correct run; the visual was repaired.

## Verdicts
| Reviewed condition | Academician (true and sourced?) | Faculty reviewer (teaches to the outcomes?) | Undergraduate reader (can I follow it?) |
|---|---|---|---|
| Teachability: one code, one idea, one result per slide | Met: 19 programs, 10 traced to a block of the book, 9 with a named reason in the source; each result comes from a run | Met: five parts keep their route; 19 of 19 research concepts covered; no slide added (41) | Met: one box per slide, copyable whole; the sample files are named in the note |
| Understandability: code and wording a beginner can follow | Met: shell prompts removed, plain programs; Linux prints PosixPath where the book shows WindowsPath, and the note says so | Met: the longest code (project 5, 21 lines) is the book's own program and sits in one box at 9 pt | Partly met: slide 34 is dense at 9 pt, readable only on a large screen; no change made |
| Explainability: the note and balloons say why, not only what | Met: every note states what the program does, what it printed and one limit or risk, with numbers from the run | Met: notes 87 to 127 words (limit 60 to 140), reader-facing, no presenter direction | Met: balloon, result balloons and note agree with each other and with the printed result |
| Human communication: plain sentences, everyday links | Met: everyday-picture slides and four stories are unchanged from the approved deck | Met: 12 everyday pictures kept | Met on the 19 code slides read; the rest of the deck is unchanged from deck 3.0.0 |

## Not covered and still open
- The story facts and links were not re-opened (no network in the shell) and were not changed.
- The page's per-concept examples (inside the concept panels) still come from the old deck's transcript (examples_out_v3_0_0.json); they are not the chapter code and were not part of this change. Reported to the owner.
- The old teaching check 1.0.0 and the builder's older manifest self-check 2.1.0 were not used: the first predates the rulings of 2026-11-14 and the second runs code without its hidden set-up lines.
