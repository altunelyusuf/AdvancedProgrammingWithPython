# Addendum to the brief of TK4_Rev_Score (session SEN0414-EX-rev-score)

Pass this file TOGETHER WITH `08-tooling/briefs/exam/r15/BRIEF_TK4_Rev_Score.md`, unedited. Where the two differ, this addendum wins. Launch only on the lineage agent's "go".

- **Root.** Tools that read decks, points files or item sets need `SEN0414_ROOT=/home/claude/AdvancedProgrammingWithPython` (that repository holds `03-materials`, `08-tooling` and the points files; the CME copy does not). The item validator is `exam_item_check_v1_2_0.py` in `/home/claude/CME/exams/SEN0414/04-assessment/exams/`.
- **Scoring rule.** The scoring is the design v1_3_0 rule: a wrong answer costs points/(k-1), a blank costs 0, the exact blind gain per unit is 0; k comes from the item sets (alternatives, bank entries, right-hand entries, order steps). The controller recounted k for all 30 units; your tool recomputes it from the item sets and must agree with the design's scoring table.
- **Open Owner points (implement the design's default, report the figure and its measured alternatives):** the paper floor (design alternative A4: the paper total never below 0), and the penalty on the bonus question Q5 (applied in the design; say clearly in the report what changes if it is not).
- **Where files go.** All new files in `/home/claude/CME/exams/SEN0414/`; nothing in the public repository.
