#!/usr/bin/env python3
"""sen0414_lineage_ch15_restart2_note v1_0_0 - notes the real start of the repair session of TK_Ret_Ch15_Page_Build (a T_Start is never repeated: the task is InProgress since the 2026-10-27T15:13 start; the restart is an audit note, as in register 2.219.0 for the chapter 1, 3, 4, 11, 12 and 16 builds)."""
import hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
src = W.newest(); t = open(src, encoding="utf-8").read()
bf = "08-tooling/briefs/iter20/r12/BRIEF_TK_Ret_Ch15_Page_Build.md"; sha = hashlib.sha256(open(os.path.join(W.REPO, bf), "rb").read()).hexdigest()
txt = "Second repair session started 2026-10-27T16:36:51 (real start given by the coordinator; session SEN0414-I20-page-ch15, restart inside the task, no new T_Start): brief %s passed unedited, SHA-256 %s, generated from register 2.297.0 after the NOT MET finding on page v9_96_0 (leak probe fails on all five seeds: py_boot runs before the worker defines _restore, so the boot wrapped nothing; second repair as page v9_96_1, pywheels_v9_95_2, lazy wrap from _before_run, leak probe on the exact built file first)." % (bf, sha)
t += "\nex:TK_Ret_Ch15_Page_Build backlog:hasAuditNote %s .\n" % W.lit(txt)
print(os.path.basename(W.write_new(src, t, "restart of the chapter 15 page build for the second repair (page v9_96_1), 16:36, brief r12")))
