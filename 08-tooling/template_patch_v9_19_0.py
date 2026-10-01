#!/usr/bin/env python3
"""Template 9.19.0 = 9.18.0 + graded exams.
1. The mock exam asks for student number, name and surname before it starts (nothing starts without them).
2. After "Finish", the page shows only that the exam was submitted. The score and the corrections stay hidden until the instructor's
   release code (an ECDSA P-256 signature, checked in the page with the instructor's public key from course_page_config_v1_3_4.json).
3. The result can be downloaded as a JSON file (identity, questions, answers, SHA-256 check value) and as a PDF copy.
4. A write-question whose own reference program contains its output is no longer made (chapter 21 had one nobody could satisfy).
The lock is a courtesy of the page, not security: the page runs on the student's computer. The instructor marks the JSON files.
usage: template_patch_v9_19_0.py IN(9.18.0) OUT(9.19.0)"""
import sys, os, json
__version__ = "9.19.0"
here = os.path.dirname(os.path.abspath(__file__))
s = open(sys.argv[1], encoding="utf-8").read()
cfg = json.load(open(os.path.join(here, "course_page_config_v1_3_4.json"), encoding="utf-8"))["exam"]
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
js = open(os.path.join(here, "template_exam_v9_19_0.js"), encoding="utf-8").read()
js = js.replace("__EXAM_PUB__", json.dumps(cfg["public_key"], separators=(",", ":"))).replace("__EXAM_PREFIX__", cfg["release_prefix"]).replace("__EXAM_BONUS__", str(cfg["bonus_points"]))
# the released view also offers the files
js = js.replace("if(rec.released){await _rev(rec);return}", "if(rec.released){await _rev(rec);XE.rec=rec;const sm=document.getElementById('xesum');if(sm)sm.insertAdjacentHTML('beforeend','<p class=\"xrow\"><button class=\"btn g\" id=\"xejson\">Download result (JSON)</button><button class=\"btn g\" id=\"xepdf\">Download result (PDF)</button></p>');return}")
marker = "// ---- save the code as a file, open a file into the code ----"
rep(marker, js + "\n" + marker)
# 1 identity row
rep('<div class="row"><label class="note" for="xekind">Exam</label>',
    '<div class="xid" role="group" aria-labelledby="xeidl"><b id="xeidl" class="xidl">Who is taking the exam</b><div class="row"><label class="note" for="xesno">Student number</label><input class="xin" id="xesno" size="12" autocomplete="off" aria-required="true"><label class="note" for="xesname">Name</label><input class="xin" id="xesname" size="14" autocomplete="off" aria-required="true"><label class="note" for="xessur">Surname</label><input class="xin" id="xessur" size="14" autocomplete="off" aria-required="true"></div><p class="note" id="xeidmsg" role="alert"></p><p class="note">These three are needed before the first question. They go into your result file and its PDF. They stay in this browser and are not sent anywhere. After you finish, your score and the correct answers stay hidden until your instructor gives you the release code; the result file is what gets marked.</p></div><div class="row"><label class="note" for="xekind">Exam</label>')
rep(".xrep{border:2px solid var(--line)", ".xid{border:1px solid var(--line);border-radius:10px;margin:.5rem 0;padding:.3rem .8rem}.xidl{display:block;padding:0 .3rem}.xlock{border-color:var(--blue)}\n.xrep{border:2px solid var(--line)")
# the history shows no result before release
rep("(r.status==='done'?r.pct+'% ('+r.got+' of '+r.pts+')':'not finished')", "(r.status==='done'?(r.released?r.pct+'% ('+r.got+' of '+r.pts+')':'submitted, result locked'):'not finished')")
# 4 write questions
rep("const v=await xVary(n.io.code,R,n.io.out);return {type:'write'", "const v=await xVary(n.io.code,R,n.io.out);if(xlax(v.out).length>=4&&xlax(v.code).includes(xlax(v.out)))return null;return {type:'write'")
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("wrote", sys.argv[2], len(s))
