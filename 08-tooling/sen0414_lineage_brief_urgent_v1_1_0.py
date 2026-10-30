#!/usr/bin/env python3
"""sen0414_lineage_brief_urgent v1_1_0 - renders the executor brief of the urgent repair task TK_U8_Deck_Check from the newest register (a NEW file over v1_0_0, which stays as committed and rendered r1).
It reuses the renderer of v1_0_0 with this task only and adds the Owner's ruling on new check files and what exists now (the delivered deck v2.1.0). The coordinator passes the brief unedited.
Usage: sen0414_lineage_brief_urgent_v1_1_0.py [OUTDIR]      (default 08-tooling/briefs/urgent/r2)"""
__version__ = "1.1.0"
import importlib.util, os, sys
here = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("bu100", os.path.join(here, "sen0414_lineage_brief_urgent_v1_0_0.py")); M = importlib.util.module_from_spec(sp); sp.loader.exec_module(M)
M.SESS.clear(); M.SESS["TK_U8_Deck_Check"] = "SEN0414-U8-deckcheck-ch08"
M.ASSETS = """- the delivered deck: `03-materials/ch08/SEN0414_Ch08_Strings_3e_v2_1_0.pptx` (72 slides; read with python-pptx under the SYSTEM `python3`), its manifest `03-materials/ch08/page/chapter_code_ch08_v1_1_0.json` (24 examples), its generator `08-tooling/ch08-deck/` (v2_1_0 files);
- the old check you must not edit and whose docstring and code you read first: `08-tooling/sen0414_deck_standard_check_v1_0_0.py`; printed on the Chapter 8 deck v2.1.0 it gives D2 FAIL (14 boxes over 30 words, all of them monospace code boxes), M1 FAIL ('0 of 0 deck code slides') and D3, D5, D12 NOT_MEASURED, because it finds code boxes by '>>>' paragraphs and story slides by WHO/WHAT labels;
- the newest teaching check, whose style and fixtures you may copy (as a new file): `08-tooling/sen0414_deck_teaching_check_v1_0_0.py` with `08-tooling/sen0414_deck_teaching_fixtures_make_v1_0_0.py`;
- the Chapter 7 deck, newest version in `03-materials/ch07/`, to run the new check on as a second deck."""
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "08-tooling/briefs/urgent/r2"
    sys.argv = [sys.argv[0], out]
    M.main()
    R = ("\n## The Owner's ruling (relayed, 2026-10-30 about 03:40 Istanbul)\nNew check files beside the old deck standard check, which recognise code boxes by their monospace font and story slides without label words, are allowed; the old checks stay unchanged and keep printing what they print; the new checks must have fixtures of known answer.\n")
    p = os.path.join(here, "..", out)
    for f in os.listdir(p):
        if f.startswith("BRIEF_"):
            fp = os.path.join(p, f); s = open(fp, encoding="utf-8").read()
            i = s.find("\n## Order of work"); s = (s[:i] + R + s[i:]) if i > 0 else s + R
            open(fp, "w", encoding="utf-8").write(s)
