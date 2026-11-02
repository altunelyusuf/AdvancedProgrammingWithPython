# ADDENDUM 1 to the SEN0414 v4.0.0 briefs (r20), written after the control of part 1 (items v4_0_0, CME 3fbd49c)

Reason: in items_v4_0_0.json the order unit Q4a is worth 16 points over 5 places = 3.2 per place, which cannot be graded by hand. All other per-gap, per-premise and per-place points are whole (Q2a 4, Q2b 3, Q3a 3 each).

1. Items: a NEW file `items/items_v4_0_1.json` (v4_0_0 stays as committed) changes only Q4a to 15 points (3 per place) and Q4b to 5 points; Q4 stays 25, total 100. Brief BRIEF_TK4_V4_1b_Items_Points.md.
2. Part 2 (design, engine, build): build from items_v4_0_1.json; the design states the points per scoring unit: one per gap, premise or place, and one per choice or number item (whole numbers only).
3. Part 3 (score): the real-build blind figures use the same unit table as part 2; each bank gap is a free choice among the 5 entries (right with chance 1/5), said in the figures.
4. Part 4 (render): when the tip of an item is 'none', print no tip line at all.
Accepted by the control: Q3a cut to 5 responses (v3_0_0 already had 7 for 5 premises); banks of 5 entries.
