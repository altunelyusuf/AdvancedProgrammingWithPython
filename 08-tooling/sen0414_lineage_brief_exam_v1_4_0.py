#!/usr/bin/env python3
"""sen0414_lineage_brief_exam v1_4_0 - renders the executor briefs of box 2 of the exam lineage from the newest register, a NEW file over v1_3_0 (which stays as committed): the Owner's decisions block now states what he has answered
(30 items per paper; the Bloom reading of about 10:30 Istanbul on 2026-10-30) and what is still the lineage agent's default (the items per chapter 4,5,5,5,4,4,3); the item-pool briefs state the Bloom rule with their own share.
Usage: sen0414_lineage_brief_exam_v1_4_0.py [TASK|ALL] [OUTDIR]      (default 08-tooling/briefs/exam/r6)"""
__version__ = "1.4.0"
import importlib.util, os, sys
here = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("b130", os.path.join(here, "sen0414_lineage_brief_exam_v1_3_0.py")); B3 = importlib.util.module_from_spec(sp); sp.loader.exec_module(B3)
M = B3.M
D = ("\n## The Owner's decisions of 2026-10-30 (relayed)\nPhysical printed paper; a sitting is 60 minutes; code on paper is read-and-choose plus fill-the-blank, nothing is written freely; the interactive pages' questions are visible to the students before the sitting, so they are seeds only and are never copied "
     "(the copy rule: the share of the new item's 4-word sequences found in the seed is 0.50 or more with the same answer, or 0.80 or more whatever the answer); the chapters are 1, 2, 3, 4, 6, 7, 8 (chapter 5 is out); the answer sheet is a separate bubble grid that reuses the SEN0401 sheet and reader; the midterm is made first. "
     "Answered by him: 30 items per paper. Answered by him about 10:30 Istanbul, in his words: 'B and C, but at least 8 work-out-why' per 30-item paper (B = use it, for example 'what does this 4-line code print'; C = work out why, for example 'this code crashes on the second loop, why'; recall, for example 'what does len() return', is the level below). "
     "The rule, counted on the whole paper: Apply and above (use it, work out why) is the majority of the 30 items, AND at least 8 of the 30 items are at Analyze or above (Bloom level 4 or higher). The revised design v1_1_0 has 21 of 30 at Apply and above and 10 of 30 at Analyze or above. "
     "Not yet answered by him, so an assumption to keep easy to change: items per chapter 4,5,5,5,4,4,3 for chapters 1,2,3,4,6,7,8.\n")
BLOOM = {"TK4_Items_A": ("\n## The Bloom rule for your pool (the Owner's word, counted on the whole paper)\nThe paper takes 4, 5, 5 and 5 items from chapters 1 to 4, which is 19 of its 30 items, so your share of the 8 required work-out-why items (Bloom 4 or higher) is at least 6 (the rounded-up proportion 8 times 19 over 30). "
                         "Your pool of 30 items therefore holds at least 12 items at Bloom 4 or higher (40 per cent), so that the engine can pick the 6 and still meet the chapter quotas, the type mix and the letter spread. A Bloom 4 item asks the student to work out why: why a program crashes or prints what it prints, which change fixes it, what a line causes later; it is not a recall question made longer. The majority rule (Bloom 3 or higher, at least 60 per cent of your pool) stays. The report lists, per item, its Bloom level and the reason for the level.\n"),
         "TK4_Items_B": ("\n## The Bloom rule for your pool (the Owner's word, counted on the whole paper)\nThe paper takes 4, 4 and 3 items from chapters 6, 7 and 8, which is 11 of its 30 items, so your share of the 8 required work-out-why items (Bloom 4 or higher) is at least 3 (the rounded-up proportion 8 times 11 over 30). "
                         "Your pool therefore holds at least 40 per cent of its items at Bloom 4 or higher, and at least 3 of them are in each of two different chapters, so that the engine can pick the 3 and still meet the chapter quotas, the type mix and the letter spread. A Bloom 4 item asks the student to work out why: why a program crashes or prints what it prints, which change fixes it, what a line causes later; it is not a recall question made longer. The majority rule (Bloom 3 or higher, at least 60 per cent of your pool) stays. The report lists, per item, its Bloom level and the reason for the level.\n"),
         "TK4_Engine_Core": ("\n## The Bloom rule for the engine (the Owner's word)\nA paper is refused unless Bloom 3 or higher is the majority of its 30 items AND at least 8 of its 30 items are at Bloom 4 or higher, counted on the whole paper; the blueprint check reports both counts. (Your brief at the start of your session may name only the majority; this rule is the Owner's of about 10:30 Istanbul and is part of your task.)\n")}
if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else "ALL"; out = sys.argv[2] if len(sys.argv) > 2 else "08-tooling/briefs/exam/r6"
    sys.argv = [sys.argv[0], tgt, out]; M.main()
    p = os.path.join(here, "..", out) if not os.path.isabs(out) else out
    for f in os.listdir(p):
        if not f.startswith("BRIEF_"): continue
        k = f[len("BRIEF_"):-3]; fp = os.path.join(p, f); s = open(fp, encoding="utf-8").read()
        if "## The Owner's decisions of 2026-10-30" in s: continue
        i = s.find("\n## Order of work"); add = D + BLOOM.get(k, "")
        s = s[:i] + add + s[i:] if i > 0 else s + add
        open(fp, "w", encoding="utf-8").write(s)
