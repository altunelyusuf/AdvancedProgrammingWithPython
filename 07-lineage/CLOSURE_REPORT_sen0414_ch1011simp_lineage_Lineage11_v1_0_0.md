# Closure Report — SEN0414 chapters 10 and 11 urgent lineage (`ex:Lineage11`)

**Register:** `07-lineage/sen0414_ch1011simp_lineage_v1_52_0.ttl` (measured: last state of every item across all versions); the closure outcome is in `v1_53_0.ttl`.
**Mission:** chapters 10 and 11 teach the book's own code, in one piece, copyable, identical on the slide and the page, run on the page.
**Measured 2026-11-25:** 19 of 19 stories and 39 of 39 tasks Done.
**Outcome:** `LS_Achieved`, as **partial achievement** (one objective target missed, see section 1). The Owner confirmed on 2026-11-25 11:41 Istanbul ("Yes, close the urgency").

## 1. What was measured (register 1.51.0, observations of 2026-11-25)
| Objective | Result |
|---|---|
| Examples traced to a block of the book's code | **27 of 37; target 37 not reached** (chapter 10: 17 of 18, chapter 11: 10 of 19; the other 10 name why the book has no code block) |
| Slide codes that differ from the page | 0 (target 0) |
| Code slides split over more than one box | 0 (target 0) |
| Examples that run on the page with the shown result | 37 of 37 |
| Review verdicts of three roles | 24 of 24 |
| Reusable tools shown on both chapters | 3 of 3 |

Final materials: chapter 10 deck 4.5.0 and page 9.25.0, chapter 11 deck 4.4.0 and page 9.26.0 (41 slides each); code check 1.2.0 C1 to C5: 0 findings on 18 and 19 examples; full page tests 410 and 414 features passed, 0 failed.

## 2. Change management inside the lineage
Requests of the Owner served the mission and went through change requests: Windows as the default environment and no repeated stories (1.33 to 1.36); mock exam results kept apart from the exam, retakes without limit, for chapters 10 and 11 (1.37 to 1.40) and for the other 18 pages of chapters 1 to 9 and 12 to 20 (1.41 to 1.44); plain explanations instead of everyday analogies in chapters 10 and 11 (1.45 to 1.48). The method guide 1.0.1 (`08-tooling/METHOD_GUIDE_book_code_one_source_v1_0_1.md`) was written last (1.49 to 1.51).

## 3. Not shown, said plainly
- The three-role review was made by the building agent, not independently, and was given on deck 4.1.0 and pages 9.21.0 and 9.22.0, before the later changes.
- The 18 retrofitted pages (exam results change) have the focused 18-check test, not the full page test.
- Chapter 10's earlier traced count was 25 and today's is 27; the cause of the difference was not traced.
- Stage 1.38 and 1.39 were committed together, and build files for 1.34 existed before its grooming; both are noted in the register.
- The urgency tool of BRSF could not see the Done state of the urgent item because the registers keep each state change as a further statement; it was run on a copy with the latest states.
- The code example name "Where you stand" (chapter 10) is a figure of speech for the working directory; it was left because the name must match across source, manifest, deck and page.
- Documentation lines of code check 1.2.0 and builder 2.9.0 still say 1.1.0 and 2.8.0 in their first docstring line.

## 4. Open work (outside this lineage)
- The 10 examples with a named reason stay unless the Owner wants code written without a book block.
- Other chapters still carry everyday analogies and, for chapters 21 to 25, the exam results change; both need their own change requests or lineage.
- The instructor desk still issues release codes that the exam results change made unnecessary; results are per browser; a student keeps at most 40 attempts.
- A photograph of Ken Thompson sits on the chapter 10 dbm slide and was flagged.
- Lineage10 (chapters 16 and 17 corrections) resumed on 2026-11-25 (its register 1.28.0).

## 5. Closure actions
Outcome in `v1_53_0.ttl`. The archive is not run inside this step; `backlog_lineage_archive` goes in the next release.
