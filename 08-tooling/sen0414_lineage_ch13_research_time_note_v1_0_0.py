#!/usr/bin/env python3
"""sen0414_lineage_ch13_research_time_note v1_0_0 - audit note on TK_Ret_Ch13_Research: the harness-measured work time of the executor, given by the coordinator. A NEW file."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now()[:19]
txt = ("EVIDENCE for the start instant, added %s UTC on the controller's question in register 2.283.0: the coordinator states the harness measured the work of the executor session SEN0414-I20-research-ch13 at 87.7 seconds (87743 ms), started 16:43 UTC. The executor's commit 40996f0 is dated 16:43:20 UTC, which is not plausible from the harness figure alone; the coordinator suggests the clock of the executor's commit and the clock of the harness may differ by about a minute. The measured 87.7 s is the evidence recorded; the controller's judgement is left open, not confirmed and not withdrawn. The result of the control does not depend on it (the controller's own run began 16:58 UTC, after the commit)." % now)
t += "\nex:TK_Ret_Ch13_Research backlog:hasAuditNote %s .\n" % W.lit(txt)
print(os.path.basename(W.write_new(src, t, "harness-measured work time of the chapter 13 research executor (87.7 s) recorded; judgement on the start instant left open")))
