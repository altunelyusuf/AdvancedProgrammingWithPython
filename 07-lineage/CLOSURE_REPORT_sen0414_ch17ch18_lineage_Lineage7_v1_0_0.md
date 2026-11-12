# Closure Report — SEN0414 chapters 17-18 lineage (`ex:Lineage7`)

**Register:** `07-lineage/sen0414_ch17ch18_lineage_v1_16_0.ttl` (measured, last state of every item read across all 17 files); the closure outcome is in `v1_17_0.ttl`.
**Mission:** chapters 17 (PDF and Word Documents) and 18 (CSV, JSON and XML) of the third edition are taught with a deck and an interactive page, each produced from one owner-approved chapter draft.
**Measured 2026-11-12:** 14 of 14 backlog items Done. 0 Ready, 0 InProgress, 0 Cancelled.
**Outcome:** `LS_Achieved`. The owner chose "Close as Achieved" on 2026-11-11 (before the last change was built) and, on 2026-11-12, told me to replace the repeated story and not to ask again; that was taken as the confirmation.

## 1. Fit-gap and impact analysis
**Fit.** Ch17: deck v2_1_0 (59 slides), page v9_96_1. Ch18: deck v2_0_3 (53 slides), page v9_96_2. Each built from its approved draft (ch17 v1_0_2, ch18 v1_0_1 and v1_0_2). Deck standard check v1.0.0 13 of 13, overlap clean, 20 links answer 200, manifest self-check re-runs every example, stories self-check 0 failures.
**Gap, found and closed inside the mission.** No step checked a chapter's stories against the chapters already presented. Change request (register v1_7_0 to v1_12_0) added the story-uniqueness area, goal and objective; three repeated stories were replaced (ch17 story 3; ch18 story 3; ch18 story 5, same source page as ch16's SQLite story). Re-run on 2026-11-12 over the newest stories of chapters 1-18: no repeated link involves chapters 17 or 18.
**Not clean, said plainly.**
- The page test stops at 70 features passed, 0 failed when the browser tab crashes; the accepted ch17 page v9_96_0 stops at the same place on this machine, so the remaining features are not verified here.
- Deck standard check v1.1.0 fails D3, D12 and M1 on the accepted decks too; v1.0.0 was used.
- The new ch18 story 5 picture is the module's own history header drawn as text, not a photograph (no free portrait of Fredrik Lundh was found); the preference for real pictures is not met for that story.
- The wording of draft ch18 v1_0_2 was not separately approved; the owner approved replacing the story.
- The repeat check compares links, so it is a lower bound.
**Own lapses, named.** The first ch18 build still carried the ElementTree story whose source page repeated ch16; my own check found it after the render, which cost a second build. The v1_11_0 register was committed once without a prefix and repaired in the next commit.
**Impact of closing.** None.

## 2. Disposition of open work
Repeats in already-presented chapters (JSON in ch7 and ch10, UTF-8 in ch8 and ch10, PEP 572 in ch2 and ch3, OOXML in ch14) are out of scope by `Excl7_CoveredChapterCorrections` (owner ruling 2026-11-11: no changes to presented chapters until the whole book is done). They stay recorded for the correction time reserved after the book.

## 3. Guards
`Obj7_DraftsApproved`, `Obj7_StateChecksRecorded` and `Obj7_StoriesNotRepeated` (2 to 0) met; goals `G7_StateChecked`, `G7_DraftApproved`, `G7_StoriesNotRepeated` satisfied; no scope exclusion violated (the render came after approval, `Excl7_RenderBeforeApproval`).

## 4. Closure actions
Outcome in `v1_17_0.ttl`. Archive is not run inside this step.
