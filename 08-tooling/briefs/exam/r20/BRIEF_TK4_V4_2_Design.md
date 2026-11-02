# Brief part 2 of 5: TK4_V4_2_Design (executor session SEN0414-EX-v4-2)
Read COMMON_v4_0_0.md first; it is part of this brief.

## Task
1. NEW files `exam_design_make_v1_5_0.py`, `exam_design_v1_5_0.json`, `exam_design_v1_5_0.md`, `exam_design_check_v1_5_0.py` (copy and change from v1_3_0; v1_3_0 and v1_4_0 stay): units are Q1 to Q4 only, no Q5, no scoring alternatives, no `wrong_cost*` fields, every closed unit has `alternatives` 5, hand-written units flagged; total 100 points; equal weight per unit as far as chapter quotas allow, with a table that states each unit's points and the rule that produced them (say honestly where equality is not reachable and why); expected blind gain per unit = points/5 for closed units, 0 for hand-written; page budget (paper + sheet at most 6, aim 4 or 5); tip rule: on the question, 12 words or fewer; no tips page; no penalty sentence.
2. NEW `exam_engine_v1_4_0.py`, `exam_engine_shapes_v1_4_0.ttl`, `exam_engine_fixtures_build_v1_4_0.py`, `exam_engine_fixtures_v1_4_0.json`, `exam_engine_check_v1_4_0.py` (copies of v1_2_1; E01 to E34 keep their rule where it still applies, those about penalty sentences or Q5 are replaced by tested equivalents that prove the sentences and Q5 are absent; none is weakened). The engine reads design v1_5_0 and validator v1_3_0.
3. Real build seed 1 from `items/items_v4_0_0.json` (use a synthetic five-alternative item set until part 1 commits; poll `git pull --rebase --autostash`) into `papers_r20/build/`. All engine rules PASS. Report: every unit, kind, points, key letters, blind expectation per unit.
Commit design and engine first, the real build when items are in.

## Done means
Design check, engine check (all suites) and all engine rules PASS on the real build; points sum to exactly 100; committed to CME.
