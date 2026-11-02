# Brief part 5 of 5: TK4_V4_5_Measure (executor session SEN0414-EX-v4-5)
Read COMMON_v4_0_0.md first; it is part of this brief. Starts when part 4 has committed the delivery set.

## Task
NEW `exam_papers_measure_v1_3_0.py` (copy of v1_2_0; none of its checks weakened; add checks: page budget paper+sheet at most 6, no Q5, no penalty wording, tip at most 12 words and printed on the question, 5 alternatives per closed unit, sheet one page and closed units only, key grading procedure on one page, SHA256.txt matches). Run it over `papers_r20/delivery`, keep the log, report every PASS/FAIL/NOT_MEASURED verbatim (margins, fonts, overlap, text clipping, image view of each page). Word is not measured.

## Done means
Measure log committed to CME; every FAIL reported, none worked around.
