#!/usr/bin/env python3
"""sen0414_lineage_ch17_restart_note v1_0_0 - notes the real start of the repair session of TK_Ret_Ch17_Page_Build (a T_Start is never repeated: the task is InProgress since the 2026-10-28T02:42:56 start; the restart is an audit note, as in register 2.219.0 for the chapter 1, 3, 4, 11, 12 and 16 builds)."""
import hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
src = W.newest(); t = open(src, encoding="utf-8").read()
bf = "08-tooling/briefs/iter20/r18/BRIEF_TK_Ret_Ch17_Page_Build.md"; sha = hashlib.sha256(open(os.path.join(W.REPO, bf), "rb").read()).hexdigest()
txt = "Repair session started 2026-10-28T06:12:30 (real start given by the coordinator; session SEN0414-I20-page-ch17, restart inside the task, no new T_Start): brief %s passed unedited, SHA-256 %s, generated from register 2.309.0 after the NOT MET finding on page v9_95_0 (page test 9.37.0 fails P2 intermittently: sys.modules[PIL] left None by a blanked variant of ImagesNeedPillow; repair as page v9_96_0 with pywheels_v9_96_0.json, snapshot of PIL, lxml and cryptography, a None guard, and the leak probes v1_2_0 and v1_3_0 on the exact built file first)." % (bf, sha)
t += "\nex:TK_Ret_Ch17_Page_Build backlog:hasAuditNote %s .\n" % W.lit(txt)
print(os.path.basename(W.write_new(src, t, "restart of the chapter 17 page build for the repair (page v9_96_0), 06:12, brief r18")))
