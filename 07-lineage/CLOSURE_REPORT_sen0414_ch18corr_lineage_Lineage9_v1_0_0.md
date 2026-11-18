# Closure Report — SEN0414 chapter 18 corrections lineage (`ex:Lineage9`)

**Register:** `07-lineage/sen0414_ch18corr_lineage_v1_6_0.ttl` (measured: last state of every item across all versions); the closure outcome is in `v1_7_0.ttl`.
**Mission:** chapter 18 (CSV, JSON and XML) is corrected to the six rulings of 2026-11-14, with the conversion kept reusable for earlier chapters.
**Measured 2026-11-18:** 4 of 4 stories and 8 of 8 tasks Done.
**Outcome:** `LS_Achieved`. The owner confirmed on 2026-11-18 ("Close; open chapters 16-17 next").

## 1. What was measured
- Deck 3.0.0 (53 slides, 27 code examples), built from a spec by the generic builder 2.4.0; notes 53 of 53 within 60–140 words.
- Material check 1.0.2: 8 of 8 (was 7 failing). Deck standard 1.1.0: 13 of 13 (was 2 failing).
- Page 9.99.2: page test 410 of 410 (was failing); 27 of 27 chapter examples run in the page; story layout pass; manifest self-check pass, old and new results identical for 27 of 27 examples.
- Review: three roles × four reviewed conditions recorded (`08-tooling/ch18-deck/logs_v3_0_0/REVIEW_RECORD_ch18_v1_0_0.md`), 12 verdicts.

## 2. Change management inside the lineage
- Material check 1.0.1 failed 41 monospaced result boxes as non-parsing code; replaced by 1.0.2 (a code frame is a shape named "code").
- Lambda-free A-box maker extended (lambdas with defaults, assigned lambdas); reusable for other chapters.

## 3. Not shown, said plainly
- The review was made by the building agent, not independently; the owner can overrule any verdict.
- Links were not re-opened this session; last opened 2026-11-12.
- The story paragraphs were re-cut to at most 30 words with the same facts; the owner has not read that wording.
- The baseline "412" failing page features was an estimate; 410 features ran.
- Three early stage commits had the trailers directly under the subject line (a lapse); later commits are correct.

## 4. Open work
Chapters 17 and 16 next (new narrow lineage, `ex:Lineage10`), then chapters 9–15 in pairs. Measured baselines with material check 1.0.2: chapters 1–8 show 4–5 failing conditions each, chapters 9–17 show 6–7 each. Each chapter's baseline is re-measured at its own mission stage. Chapters 21–22 only with the owner.

## 5. Closure actions
Outcome in `v1_7_0.ttl`. Archive is not run inside this step; `backlog_lineage_archive` goes in the next release.
