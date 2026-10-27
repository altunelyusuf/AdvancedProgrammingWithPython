#!/usr/bin/env python3
"""sen0414_lineage_ch16_restart_note v1_0_0 - notes the real start of the repair session of TK_Ret_Ch16_Page_Build (a T_Start is never repeated: the task is InProgress since the 2026-10-27T20:50:12 start; the restart is an audit note, as in register 2.219.0 for the chapter 1, 3, 4, 11, 12 and 16 builds)."""
import hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
src = W.newest(); t = open(src, encoding="utf-8").read()
bf = "08-tooling/briefs/iter20/r15/BRIEF_TK_Ret_Ch16_Page_Build.md"; sha = hashlib.sha256(open(os.path.join(W.REPO, bf), "rb").read()).hexdigest()
txt = "Repair session started 2026-10-27T21:18:22 (real start given by the coordinator; session SEN0414-I20-page-ch16, restart inside the task, no new T_Start): brief %s passed unedited, SHA-256 %s, generated from register 2.303.0 after the NOT MET finding on page v9_95_0 (leak probe fails on all five seeds with wrong real runs: sqlite3 connections left alive in reference cycles; repair as page v9_96_0, garbage collection hook in the boot program, leak probe on the exact built file first)." % (bf, sha)
t += "\nex:TK_Ret_Ch16_Page_Build backlog:hasAuditNote %s .\n" % W.lit(txt)
print(os.path.basename(W.write_new(src, t, "restart of the chapter 16 page build for the repair (page v9_96_0), 21:18, brief r15")))
