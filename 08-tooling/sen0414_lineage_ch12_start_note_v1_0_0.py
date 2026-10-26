#!/usr/bin/env python3
"""sen0414_lineage_ch12_start_note v1_0_0 - audit note on TK_Ret_Ch12_Research: the coordinator states that the harness measured the executor at 80 s of work in total, so a commit in the same minute as the start 13:07 is real; the controller's remark in 2.274.0 that the start was 'probably the time of the message' is withdrawn."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now()[:19]
txt = ("CORRECTION of a remark, made on %s UTC: the controller's label of register 2.274.0 doubts the start instant 2026-10-26T13:07 of this task because the executor's commit d67987e is dated 13:07:34 UTC. The coordinator states that it read the clock just before each launch and that the harness measured this executor at 80 seconds of work in total, so the commit in the same minute is real. The doubt is withdrawn for this task; the start instant stays 13:07, and the register keeps the 2.266.0 correction of the chapter 11 research (its first two instants were the coordinator's slips of the clock, not a late reading)." % now)
t += "\nex:TK_Ret_Ch12_Research backlog:hasAuditNote %s .\n" % W.lit(txt)
print(os.path.basename(W.write_new(src, t, "withdrawal of the doubt on the start instant of the chapter 12 research (80 s of measured work)")))
