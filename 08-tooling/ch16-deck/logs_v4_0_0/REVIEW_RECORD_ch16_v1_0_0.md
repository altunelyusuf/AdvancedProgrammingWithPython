# Review record, chapter 16, deck 4.0.0 and page 9.99.0 (2026-11-25)

Reviewed: deck 03-materials/ch16/SEN0414_Ch16_SQLiteDatabases_3e_v4_0_0.pptx (54 slides, 25 code examples), page 03-materials/ch16/page/sen0414_ch16_page_v9_99_0.html, code manifest chapter_code_ch16_v1_2_0.json.
**Who reviewed:** the agent that built the material, once per role. This is NOT an independent review; the owner can overrule any verdict. It reads the four conditions of the Lineage10 goal (teachability, understandability, explainability, human communication) from each of three roles.
Evidence read in this session: all 54 slides rendered and read as three contact sheets (text at small size only; the code lines of the longest examples, slides 28, 31, 37 and 48 with 14 lines each, were not read line by line); the logs of the deck checks (standard, fit, layout, overlap, notes, reader notes, story prose, material check, manifest self-check, analogy word search: 0 hits); the page test of 9.99.0 (414 passed, 0 failed) and the story layout probe (pass).

## What the review found
1. The deck holds no lambda and no everyday analogy word; the five lambda lines became plain def functions and all 25 examples give the same results as the earlier deck. The page data and the domain A-box 1.0.4 carry no lambda either (the first page test found 69 examples with lambda text in A-box 1.0.3; repaired and tested again).
2. Slides 28, 31, 37 and 48 carry 14-line examples at a small size; they render without overflow but are dense on a small screen.
3. Slides 25, 30 and 40 show portraits of public figures (Munroe, Gray, Codd). The ruling says photos of public figures are never downloaded or inserted. These pictures were already in the approved earlier deck and were not changed here; the owner must say whether they stay.
4. The builder still warns on 8 slides where the result picture falls a little short of its box (0.3 in or less); nothing overflows.
5. The story repeat check lists 2 older pairs to read, both outside chapter 16's own stories; the 2006 Python and SQLite story (chapter 16) and the 2014 Word name story (chapter 17) share about 0.135 overlap and were not judged.

## Verdicts
| Reviewed condition | Academician (true and sourced?) | Faculty reviewer (teaches to the outcomes?) | Undergraduate reader (can I follow it?) |
|---|---|---|---|
| Teachability: one code, one idea, one result per slide | Met: each result comes from a run; manifest equals the deck's code boxes in order | Met: five parts keep their route; 54 slides, none added | Met: one box per slide; sample data is made in the code |
| Understandability: code and wording a beginner can follow | Met: Python 3.13.18 results shown; no shell prompts; no lambda | Met, with the dense slides of finding 2 | Partly met: slides 28, 31, 37, 48 are dense on a small screen |
| Explainability: the note and balloons say why, not only what | Met: notes reader-facing, 30 to 140 words, slide links present | Met: no presenter direction, no "think of" | Met on the slides read; notes not all re-read word by word |
| Human communication: plain sentences, no everyday analogies | Met: analogy word search 0 hits | Met: plain concept rows | Met: sentences are short and plain |

## Not covered and still open
- Story facts and links were not re-opened (no network in the shell) and not changed.
- The page was not looked at in a browser window, and the Lecture tab text was only checked by the page test.
- The generic code check (C1 to C5) was not run: chapter 16 has no line-list source file.
- Whether the portraits of slides 25, 30 and 40 stay is the owner's call.
