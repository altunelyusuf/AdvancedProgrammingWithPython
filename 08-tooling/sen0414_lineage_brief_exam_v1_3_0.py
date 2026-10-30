#!/usr/bin/env python3
"""sen0414_lineage_brief_exam v1_3_0 - renders the executor briefs of box 2 of the exam lineage (the MIDTERM first) from the newest register. A NEW file over v1_0_0 (which stays as committed and serves box 1):
it reuses the renderer of v1_0_0 with the sessions and the 'what exists now' text of box 2. A brief names only its own session and only its own requirements. The coordinator passes a brief unedited.
Usage: sen0414_lineage_brief_exam_v1_3_0.py [TASK|ALL] [OUTDIR]      (default 08-tooling/briefs/exam/r4; INDEX.md lists the session and whether the task can start now)"""
__version__ = "1.3.0"
import importlib.util, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("b100", os.path.join(here, "sen0414_lineage_brief_exam_v1_0_0.py")); M = importlib.util.module_from_spec(sp); sp.loader.exec_module(M)
SESS = {"TK4_Distinct_Build": "SEN0414-EX-nocopy", "TK4_DesignRev": "SEN0414-EX-designrev", "TK4_Items_A": "SEN0414-EX-items-ch01-04", "TK4_Items_B": "SEN0414-EX-items-ch06-08", "TK4_Engine_Core": "SEN0414-EX-engine-core"}
M.SESS.clear(); M.SESS.update(SESS)
M.ASSETS = """- decks of the chapters: `03-materials/chNN/SEN0414_ChNN_*_3e_vX_Y_Z.pptx` (the newest version of each chapter; speaker notes are in the notes pages; read with python-pptx under the SYSTEM `python3`); corpus and stories: `08-tooling/sen0414_chNN_corpus_*.py` and `08-tooling/sen0414_chNN_stories_*.py` (newest of each); chapter-code manifests: `03-materials/chNN/page/chapter_code_chNN_v*.json` (newest);
- the controlled critical points: `04-assessment/exams/critical_points_ch01_04_v1_0_0.json` and `critical_points_ch06_08_v1_0_0.json` with their `*_not_found_v1_0_0.md` lists;
- the controlled design of the paper: `04-assessment/exams/exam_design_v1_0_0.md` and `.json` and its check `exam_design_check_v1_0_0.py` (the item model is section 2, the near-copy method section 2.1, the types section 3, the blueprint section 5); a revised design v1_1_0 exists only after the task TK4_DesignRev is Done;
- the interactive pages' question banks, SEEDS ONLY: `08-tooling/chNN-page/question_bank_v*.json` and `quiz_v1_0_0.json` (students can open these before the sitting, so no exam item is one of them or a near copy of one); the pages' exam engine is in `08-tooling/course_page_template_v9_52_4.html` and `08-tooling/template_exam_v9_19_0.js`;
- the answer sheet and its reader, to be REUSED and never edited, in the sibling repository checkout `/home/claude/sen0401/08-tooling/exam/`: `sen0401_exam_answersheet_v1_0_0.py` (the sheet: specification, layout, renderer, check digit) and `sen0401_exam_answersheet_v1_1_0.py` (the reader); read them, run them only in a scratch folder outside the repository;
- the assessment ontology `04-assessment/sen0414_assessment_v1_0_0.ttl` (weights only: midterm 30 per cent).
Nothing exists yet that builds an exam item, a paper across chapters, a printed paper, a printed key, or a tool that reads and grades a handed-in sheet for SEN0414; the tasks of box 2 build the parts named in their text."""
for name in ("RULES",):
    M.RULES = M.RULES.replace("the controller finds your commits by it)", "the controller finds your commits by it)")
if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else "ALL"
    out = sys.argv[2] if len(sys.argv) > 2 else "08-tooling/briefs/exam/r4"
    sys.argv = [sys.argv[0], tgt, out]
    M.main()
    # the Owner's decisions, appended before the order of work of every brief
    D = ("\n## The Owner's decisions of 2026-10-30 (relayed)\nPhysical printed paper; a sitting is 60 minutes; code on paper is read-and-choose plus fill-the-blank, nothing is written freely; the interactive pages' questions are visible to the students before the sitting, so they are seeds only and are never copied "
         "(the copy rule: the share of the new item's 4-word sequences found in the seed is 0.50 or more with the same answer, or 0.80 or more whatever the answer); the chapters are 1, 2, 3, 4, 6, 7, 8 (chapter 5 is out); the answer sheet is a separate bubble grid that reuses the SEN0401 sheet and reader; the midterm is made first. "
         "Not yet answered by him, so assumptions to keep easy to change: 30 items per paper, the Bloom reading Apply and up, items per chapter 4,5,5,5,4,4,3.\n")
    p = os.path.join(here, "..", out) if not os.path.isabs(out) else out
    for f in os.listdir(p):
        if f.startswith("BRIEF_"):
            fp = os.path.join(p, f); s = open(fp, encoding="utf-8").read()
            if "## The Owner's decisions of 2026-10-30" in s: continue
            i = s.find("\n## Order of work"); s = s[:i] + D + s[i:] if i > 0 else s + D
            open(fp, "w", encoding="utf-8").write(s)
