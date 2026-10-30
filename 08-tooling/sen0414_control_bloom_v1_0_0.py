#!/usr/bin/env python3
"""sen0414_control_bloom v1_0_0 - the Owner's Bloom rule of 2026-10-30 (about 10:30 Istanbul) checked on the revised design v1_1_0 by the controller's own count: Apply and above (Bloom 3 or higher) is the majority of the 30 items AND at least 8 of
the 30 items are at Bloom 4 or higher. Counts the levels from the design's blueprint AND from the arithmetic rows' item counts; exit 0 only when both hold and the two readings agree. Run from the repository root."""
import json, sys
d = json.load(open("04-assessment/exams/exam_design_v1_1_0.json", encoding="utf-8")); b = d["blueprint"]; lv = {int(k): v for k, v in b["bloom_levels"].items()}
n = sum(lv.values()); ap = sum(v for k, v in lv.items() if k >= 3); an = sum(v for k, v in lv.items() if k >= 4)
a = b["arithmetic"]; ok = [n == 30 == b["items"], ap * 2 > n, an >= 8, a["apply_or_above_items"] == ap, a["analyze_or_above_items"] == an]
print("items %d, Apply and above %d (%.0f%%), Analyze and above %d, rule: majority and at least 8 -> %s" % (n, ap, 100.0 * ap / n, an, "holds" if all(ok) else "FAILS"))
print("RESULT " + ("PASS" if all(ok) else "FAIL")); sys.exit(0 if all(ok) else 1)
