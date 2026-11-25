# Closure Report — SEN0414 chapters 11, 17 and 16 corrections (`ex:Lineage10`)

**Status:** DRAFT for the Owner's confirmation. Not yet closed in the register.
**Register:** `07-lineage/sen0414_ch1617corr_lineage_v1_49_0.ttl` (last state of every item across all versions).
**Mission:** the chapter 17 and chapter 16 decks and pages are corrected to the six rulings of 2026-11-14, with approved content unchanged; amended on 2026-11-19 (chapter 10 and the balloon, reader-note and own-version practices for chapters 10 and 11, as an urgency) and by the ruling of 2026-11-24 (no everyday analogies).
**Measured 2026-11-26:** 19 of 19 stories and 39 of 39 tasks Done.

## 1. What was measured (observations of 2026-11-26, register 1.49.0)
| Objective | Baseline | Result | Target |
|---|---|---|---|
| Specs run by the generic builder | 0 | 4 (chapters 11, 10, 17, 16) | 3 |
| Failing conditions of the material check on the decks | 20 | 0 | 0 |
| Failing conditions of the deck standard | 6 | 0 | 0 |
| Pages shown to pass the full page test | 0 | 4 (11: 414, 10: 410, 17: 416, 16: 414; 0 failed) | 3 |
| Recorded review verdicts of three roles | 0 | 48 (four records of 12) | 36 |
| Notes with presenter directions or think-of (chapters 10, 11) | 43 | 0 | 0 |
| Code slides with a story balloon and two result balloons | 0 | 37 (recounted from the decks) | 37 |
| Unreleased page drafts above the released page (chapters 10, 11) | 6 | 0 | 0 |
| Failing conditions of the chapter 10 deck and page | 9 | 0 | 0 |

Final materials: chapter 17 deck 4.0.0 (59 slides) and page 9.23.0; chapter 16 deck 4.0.0 (54 slides, 25 examples) and page 9.99.0; chapters 10 and 11 as left by the lineage (decks 4.5.0 and 4.4.0, pages 9.25.0 and 9.26.0). No slide was added to any deck. The page template is 9.54.1 for chapters 17 and 16.

## 2. Change management inside the lineage
- Mission amendment of 2026-11-19 (chapter 10, balloons, reader notes, own versions), run as an urgency and closed as Lineage11 on 2026-11-25; Lineage10 then resumed.
- CR10_NoAnalogies (Owner ruling 2026-11-24): accepted; chapters 17 and 16 carry plain concept rows instead of analogy slides.
- Repairs found by checks and fixed in the lineage: page budget (the page-fit routine ran once per inserted line; template 9.54.1), lambda text in the chapter 16 page data (A-box 1.0.4 and a runner that accepts `sys.exit(0)`).
- 1.47.0: Owner ruling that portraits of public figures stay. The earlier open item about them was the agent's own limit, wrongly recorded as an Owner rule, and is void.

## 3. Not shown, said plainly
- Every three-role review was made by the building agent, not independently; those of chapters 10 and 11 were given before their later changes.
- The story links of all four chapters were not opened (no network in the shell).
- No page was looked at in a browser window; the page tests and the story layout probe read them.
- The generic code check (C1 to C5) was not run on chapters 17 and 16: there is no line-list source file for them.
- The deck builder still warns on 8 slides of chapter 16 where a result picture falls up to 0.3 in short of its box; nothing overflows.
- Slides 28, 31, 37 and 48 of chapter 16 carry 14-line examples that are dense on a small screen.
- The chapter 16 and chapter 17 stories on Python-and-SQLite (2006) and the 2014 Word name story overlap by about 0.135 in the repeat check; not judged.
- The deck standard check in the repository is 1.3.0, the objective names 1.1.0.

## 4. Open work (outside this lineage)
- Other chapters (1 to 9, 12 to 15, 18 to 20, 21 to 25) were not checked for analogies and not rebuilt on template 9.54.1.
- Reports owed: vocabulary finding (no partial outcome value), the G237 / DoD10 repair report, the BRSF tool gaps handover, the lab-materials package queued after this lineage.

## 5. Closure actions
Proposed outcome: full achievement (`LS_Achieved`, `Out_Achieved`), because all nine objectives meet their targets as measured. The limits above are carried in the report. The archive (`backlog_lineage_archive`) is not run inside this step; it goes in the next release. No guard was promised in this register that needs reading again.
