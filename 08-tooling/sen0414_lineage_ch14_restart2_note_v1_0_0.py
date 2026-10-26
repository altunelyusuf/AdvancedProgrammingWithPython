#!/usr/bin/env python3
"""sen0414_lineage_ch14_restart2_note v1_0_0 - notes the real start of the repair session of TK_Ret_Ch14_Page_Build (a T_Start is never repeated: the task is InProgress since 2026-10-26T10:15; the restart is an audit note, as in register 2.219.0 for the chapter 1, 3, 4, 11, 12 and 16 builds)."""
import hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
src = W.newest(); t = open(src, encoding="utf-8").read()
bf = "08-tooling/briefs/iter20/r5/BRIEF_TK_Ret_Ch14_Page_Build.md"; sha = hashlib.sha256(open(os.path.join(W.REPO, bf), "rb").read()).hexdigest()
txt = "Repair session started 2026-10-26T16:43 (real start given by the coordinator; session SEN0414-I20-page-ch14, restart inside the task, no new T_Start): brief %s passed unedited, SHA-256 %s, generated from register 2.278.0 after the NOT MET finding on page v9_96_0 (state leak of the page runtime: repair as template 9.52.3 and page v9_97_0)." % (bf, sha)
t += "\nex:TK_Ret_Ch14_Page_Build backlog:hasAuditNote %s .\n" % W.lit(txt)
print(os.path.basename(W.write_new(src, t, "second restart of the chapter 14 page build for the repair (template 9.52.3, page v9_97_0), 16:43, brief r5")))
