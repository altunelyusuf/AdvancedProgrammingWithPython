#!/usr/bin/env python3
"""sen0414_lineage_brief_exam v1_5_0 - a NEW file over v1_4_0 (which stays as committed): adds the session of the repair task TK4_Engine_Bloom (SEN0414-EX-engine-bloom) and uses the same decisions block.
Usage: sen0414_lineage_brief_exam_v1_5_0.py [TASK|ALL] [OUTDIR]      (default 08-tooling/briefs/exam/r7)"""
__version__ = "1.5.0"
import importlib.util, os, sys
here = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("b140", os.path.join(here, "sen0414_lineage_brief_exam_v1_4_0.py")); B4 = importlib.util.module_from_spec(sp); sp.loader.exec_module(B4)
M = B4.M; M.SESS["TK4_Engine_Bloom"] = "SEN0414-EX-engine-bloom"
B4.BLOOM["TK4_Engine_Bloom"] = ""
if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else "ALL"; out = sys.argv[2] if len(sys.argv) > 2 else "08-tooling/briefs/exam/r7"
    sys.argv = [sys.argv[0], tgt, out]; M.main()
    p = os.path.join(here, "..", out) if not os.path.isabs(out) else out
    for f in os.listdir(p):
        if not f.startswith("BRIEF_"): continue
        fp = os.path.join(p, f); s = open(fp, encoding="utf-8").read()
        if "## The Owner's decisions of 2026-10-30" in s: continue
        i = s.find("\n## Order of work"); add = B4.D + B4.BLOOM.get(f[len("BRIEF_"):-3], "")
        open(fp, "w", encoding="utf-8").write(s[:i] + add + s[i:] if i > 0 else s + add)
