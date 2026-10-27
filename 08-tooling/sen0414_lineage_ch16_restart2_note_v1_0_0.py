#!/usr/bin/env python3
"""sen0414_lineage_ch16_restart2_note v1_0_0 - notes the real start of the repair session of TK_Ret_Ch16_Page_Build (a T_Start is never repeated: the task is InProgress since the 2026-10-27T20:50:12 start; the restart is an audit note, as in register 2.219.0 for the chapter 1, 3, 4, 11, 12 and 16 builds)."""
import hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
src = W.newest(); t = open(src, encoding="utf-8").read()
bf = "08-tooling/briefs/iter20/r16/BRIEF_TK_Ret_Ch16_Page_Build.md"; sha = hashlib.sha256(open(os.path.join(W.REPO, bf), "rb").read()).hexdigest()
txt = "Second repair session started 2026-10-27T22:32:10 (real start given by the coordinator; session SEN0414-I20-page-ch16, restart inside the task, no new T_Start): brief %s passed unedited, SHA-256 %s, generated from register 2.305.0 after the NOT MET finding on page v9_96_0 (page test 9.37.0 fails P1 and P9 at 1366 px: Playground starter lines up to 180 characters; second repair as page v9_97_0 with a new starter file of lines at most 100, leak probe on the exact built file first, then a browser width check of the Playground)." % (bf, sha)
t += "\nex:TK_Ret_Ch16_Page_Build backlog:hasAuditNote %s .\n" % W.lit(txt)
print(os.path.basename(W.write_new(src, t, "restart of the chapter 16 page build for the second repair (page v9_97_0), 22:32, brief r16")))
