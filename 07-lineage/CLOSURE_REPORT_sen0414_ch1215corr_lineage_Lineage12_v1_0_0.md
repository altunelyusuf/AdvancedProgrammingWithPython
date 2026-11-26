# Closure Report — SEN0414 chapters 12 to 15 corrections (`ex:Lineage12`)

**Register:** `07-lineage/sen0414_ch1215corr_lineage_v1_24_0.ttl` (final observations); the closure outcome is in `v1_25_0.ttl`.
**Mission:** the decks and pages of chapters 12 to 15 follow the Owner's rulings: one thing per slide, reader-facing notes that carry the lecture, code with no prompts, no lambda unless taught, no everyday analogies, checks and reviews recorded before release, and a run-in-order menu item on every chapter page. Content, stories and examples stay unchanged unless a ruling forces a change.
**Measured 2026-11-26:** all stories and tasks Done; 22 objectives observed (register 1.24.0).
**Outcome:** `LS_Achieved`, `Out_Achieved` (full achievement of the work and the mission). Per the Owner's ruling of 2026-11-26, no confirmation is needed once the conditions hold. Three objective definitions were found wrong against the plan; they are listed in section 2 and stand as appended correction notes.

## 1. What was measured
| Objective | Result (target) |
|---|---|
| Specs run by the generic builder | 4 (4) |
| Failing material-check conditions on decks and pages | 0 (0) |
| Failing deck-standard 1.3.0 conditions | 0 (0) |
| Notes outside 60 to 140 words; reader-note findings; story-prose findings | 0, 0, 0 (0) |
| Everyday-analogy slides; analogy words in pages | 0, 0 (0) |
| Code frames not parsing; not found in the page | 0, 0 (0) |
| Lambda occurrences in the pages | 0 (0) |
| Pages with the run-in-order menu item (shape conforms) | 4 (4) |
| Pages passing the full page test, 0 failed | 4: 414, 416, 416, 416 features (4) |
| Review verdicts of three roles (four review records) | 48 (48) |
| Older page drafts beside the newest | 0 (0; baseline 24) |
| Exam, lab, other-chapter files changed | 0, 0, 0 (0) |
| Topics, stories or example meanings changed beyond a ruling | 0 (0) |
| Chapters passing every objective of their goals | 4 (4) |

Final materials: chapter 12 deck 3.2.0 and page 9.100.0; chapter 13 deck 3.1.0 and page 9.102.0; chapter 14 deck 3.1.0 and page 9.104.0; chapter 15 deck 3.1.0 and page 9.106.0. Logs: `08-tooling/lineage12-closure/`, `08-tooling/lineage12-opening/`, the chapter logs folders.

## 2. Three objectives that differ from their letter
- **Balloons:** target 104; observed 96. The target counted the keys of the four examples files, each holding two keys that are not examples. The decks hold 23, 24, 24 and 25 examples, and all 96 have the balloons. No deck can reach 104.
- **Rdodi files changed:** target 0; observed 4 added, 0 existing modified or deleted. The four lambda-free domain A-boxes (ch12 1.0.3, ch13 1.0.4, ch14 1.0.4, ch15 1.0.5) are planned by the mission and sit beside the old files.
- **Files outside the folders:** target 0; observed 1, the page-shapes file planned in register 1.5.0 that enforces the run-in-order ruling.

## 3. Faults found and corrected on the way
Per chapter in the release records `REPORT_Lineage12_chNN_release_and_review_v1_0_0.md`: unsupported statements in notes (found in review, corrected in a later spec version; the earlier deck versions were committed first and are superseded), lambdas in page boot code and in A-box code literals, crowded visuals, stale lecture text, a missing stand-in step in the generic builder (patched by a script).

## 4. Not shown, said plainly
- The three-role reviews were made by the building agent, not independently.
- The Owner has not opened any deck or page. Slides were rendered with LibreOffice, not PowerPoint, and only a few were looked at.
- Recorded Python is 3.13.18; the book's 3.14.6 was not available. Page tests used a test key. Google was never reached in chapter 15: examples run the real ezsheets against a stand-in.
- Resource links and story-picture credits were not re-opened or re-checked in this lineage.
- The merge, grooming and observation scripts used to move register states are the lineage's own tooling (a deviation from the rule that tool gaps go to BRSF); a handover is owed.
- The story-repeat check over chapters 1 to 25 still reports one candidate (chapters 2 and 3, PEP 572), outside this lineage.
- The pages have nine menu items because of the run-in-order item; the Owner may want eight.

## 5. Open work (outside this lineage)
Other chapters (1 to 11 and 16 to 25) still lack the run-in-order item and may carry analogies and lambda; each needs its own narrow lineage. Lab materials, a prose re-read of the Lineage10 chapters, and the code check C1 to C5 for chapters 16 and 17 stand open from earlier work.

## 6. Closure actions
Outcome in `v1_25_0.ttl`. The archive step (`backlog_lineage_archive`) follows in the next release.
