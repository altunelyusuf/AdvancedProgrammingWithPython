#!/usr/bin/env python3
"""sen0414_lineage_ch11_restart_note v1_0_0 - notes the real start of the repair session of TK_Ret_Ch11_Page_Build (a T_Start is never repeated: the task is InProgress since 2026-10-25T12:52; the restart is an audit note, as in register 2.219.0 for the chapter 1, 3 and 4 page builds)."""
import hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
src = W.newest(); t = open(src, encoding="utf-8").read()
bf = "08-tooling/briefs/iter20/r3/BRIEF_TK_Ret_Ch11_Page_Build.md"; sha = hashlib.sha256(open(os.path.join(W.REPO, bf), "rb").read()).hexdigest()
txt = "Repair session started 2026-10-25T14:24 (real start given by the coordinator; session SEN0414-I20-page-ch11, restart inside the task, no new T_Start): brief %s passed unedited, SHA-256 %s, generated from register 2.250.0 after the NOT MET finding on page v9_95_0." % (bf, sha)
t += "\nex:TK_Ret_Ch11_Page_Build backlog:hasAuditNote %s .\n" % W.lit(txt)
print(os.path.basename(W.write_new(src, t, "restart of the chapter 11 page build for the repair (page v9_96_0), 14:24, brief r3")))
