# Closure Report — SEN0414 chapters 19-20 lineage (`ex:Lineage8`)

**Register:** `07-lineage/sen0414_ch19ch20_lineage_v1_18_0.ttl` (measured: last state of every item across all versions); the closure outcome is in `v1_19_0.ttl`.
**Mission:** chapters 19 (Keeping Time, Scheduling Tasks and Launching Programs) and 20 (Sending Email, Texts and Push Notifications) are taught with a deck and an interactive page each, built to the owner's rulings of 2026-11-14.
**Measured 2026-11-18:** 22 of 22 backlog items Done.
**Outcome:** `LS_Achieved`. The owner chose "Replace check, then close" on 2026-11-18.

## 1. What was measured
- Ch19: deck 2.2.0 (42 slides), page 9.97.2, page test 412 of 412, material check 8 of 8, manifest self-check pass, story layout pass, deck standard 1.1.0 13 of 13, notes 60–140 words with a point-at opening and a lead-in on every code slide.
- Ch20: deck 2.0.1 (42 slides), page 9.99.1, page test 412 of 412, material check 8 of 8, manifest self-check pass, story layout pass, deck standard 1.1.0 13 of 13; code-slide notes 19 of 19 (1 of 19 before notes 2.0.1).
- Review: three roles × four reviewed conditions recorded for both chapters (`08-tooling/lineage8-closure/REVIEW_RECORD_ch19_ch20_v1_0_0.md`).

## 2. Change management inside the lineage
- Root cause of the page-test crash: the template started the Oxigraph module twice at once. Fixed in template 9.53.5 (single-flight initialisers); a page defect, not a tool defect.
- A-boxes made free of lambda and eval; the `schedule` package added to the recording environment.
- Declared deck check 1.0.0 predated the 2026-11-14 rulings and contradicted them (note cap, prompt detection, divider test). Replaced by 1.1.0 on the owner's confirmation of 2026-11-18 (L-66: change declared openly, old result kept as history: 3 of 13 per deck under 1.0.0).

## 3. Not shown, said plainly
- The review was made by the building agent, not independently; the owner can overrule any verdict.
- Links were not re-opened this session (no shell network); last opened 2026-11-12.
- 11 of 19 chapter examples run in the browser; 8 show their recorded result.
- Known deviations: 42-slide decks; the Alto picture for IMAP and the drawn AT&T picture are not photographs; some 9 pt code; Ch20 slides 17–19 have the result table close to the footer.
- Story repeats among chapters ≤18 found by the repeat check are out of scope until the correction time after the book.

## 4. Open work
Correction of earlier chapters (Ch18 first: 49 thin notes, 120 prompt markers, 112 non-parsing frames, 3 short titles, a labelled story layout, 36 missing page frames, 322 lambdas) per the rulings, by change management; chapters 21–22 only with the owner.

## 5. Closure actions
Outcome in `v1_19_0.ttl`. Archive is not run inside this step; `backlog_lineage_archive` goes in the next release.
