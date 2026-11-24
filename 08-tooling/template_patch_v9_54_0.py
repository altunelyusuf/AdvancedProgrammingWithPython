#!/usr/bin/env python3
"""Template 9.54.0 = 9.53.7 + the mock exam and its results as two functions.
1. A new tab, Exam results, holds the list of attempts, the review of any attempt (score, points by subject, the answer to every
   question and a correction under each), the result file (JSON and PDF) and the hand-in zip. The Mock exam tab only starts and takes an exam.
2. When an exam is finished it is marked and the result opens at once in the Exam results tab. The release-code lock of 9.19.0 and
   the code check are removed; nothing is withheld.
3. An exam can be taken again as often as wished (same code = same questions, or a new code).
4. Student number, name and surname are optional; they only go into the result file and the hand-in zip.
5. The result file keeps page_marks and page_total, which the instructor's result desk re-checks.
usage: template_patch_v9_54_0.py IN(9.53.7) OUT(9.54.0)"""
import sys, os
__version__ = "9.54.0"
here = os.path.dirname(os.path.abspath(__file__))
s = open(sys.argv[1], encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)
def cut(start, end, new="", keep_end=True):
    global s
    assert s.count(start) == 1 and s.count(end) == 1, (s.count(start), s.count(end), start[:60])
    i, j = s.index(start), s.index(end)
    assert i < j
    s = s[:i] + new + (s[j:] if keep_end else s[j + len(end):])
# 1 the release code and the lock are gone; the new results code takes their place
cut("// the release code: R1.", "// the result file\n")
js = open(os.path.join(here, "template_results_v9_54_0.js"), encoding="utf-8").read()
cut("// the locked view\n", "xidPaint();\n", js.rstrip("\n").rsplit("\nxidPaint();", 1)[0] + "\n", keep_end=True)
rep("{const _v=xVerifyRelease;xVerifyRelease=async function(c,rec){const r=await _v(c,rec);audit(r.ok?'release_accepted':'release_refused',{exam:rec.code,reason:r.ok?'':r.why});return r}}\n", "")
# 2 the review writes into the results tab
rep("const out=document.getElementById('xeout');clearInterval(XE.timer);XE.done=true;XE.items=JSON.parse(JSON.stringify(items));XE.kind=rec.kind;XE.seed=+rec.code.slice(2);XE.rec=null;",
    "const out=document.getElementById('xrout');clearInterval(XE.timer);XE.done=true;XE.items=JSON.parse(JSON.stringify(items));XE.kind=rec.kind;XE.seed=+rec.code.slice(2);XE.rec=null;")
rep("<div id=\"xetimer\" role=\"timer\">Review of exam <code>", "<div id=\"xrtitle\" role=\"status\">Review of exam <code>")
rep("#xetimer{position:sticky;", "#xetimer,#xrtitle{position:sticky;")
# 3 the result file always carries the page's marks; the PDF says so
rep("if(withMarks&&rec.released){o.released=true;o.release_code=rec.release;o.page_marks=", "if(withMarks&&rec.res){o.page_marks=")
rep("if(o.released)put('Score (released by the instructor): '", "if(o.page_total)put('Score (marked by this page): '")
rep("else put('The score and the correct answers are withheld until the instructor gives the release code. The instructor marks the result file.',24,false,'#B42318',14);",
    "else put('This attempt was not finished, so it has no score yet.',24,false,'#B42318',14);")
rep("const sc=o.released&&o.page_marks?", "const sc=o.page_marks?")
rep("Submit the .json file; this PDF is your copy.", "Hand in the .json file if your instructor asks for it; this PDF is your copy.")
rep("result files saved, release codes tried, data cleared). No answers and no release codes are written into the log.", "result files saved, data cleared). No answers are written into the log.")
# 4 the Mock exam tab: only taking an exam
i = s.index("function examPane(){")
j = s.index("\n", i)
line = s[i:j]
a = line.index('<div class="row xzip">')
b = line.index('<div class="row"><label class="note" for="xekind">')
line = line[:a] + line[b:]
for x, y in [("Every exam you start is kept under <b>My exams</b> in this browser, so you can come back to it later, review it with your answers and corrections, retake it, or ask for an alternative.",
               "Every exam you start is kept in this browser, so you can come back to it later, take the same exam again as often as you wish, or ask for an alternative."),
             ("Marking happens when you finish; corrections are folded under each question.",
              "Marking happens when you finish, and your result opens at once in the <b>Exam results</b> tab, with your answers and a correction under each question."),
             ('<div id="xehist"></div><div id="xeclearbox"></div></div>\'}', '</div>\'}')]:
    assert line.count(x) == 1, x[:60]
    line = line.replace(x, y)
results_pane = ("\nfunction resultsPane(){return '<div role=\"tabpanel\" data-pane=\"examresults\" hidden><h2>📊 Exam results</h2>"
 "<p class=\"note\">This tab keeps the results of your mock exams. When you finish an exam on the Mock exam tab, it is marked and its result opens here at once: your points, your points by subject, your answer to every question and a correction under each one. Every attempt stays in this browser, so you can open it again later, see how your results change, and go back to the Mock exam tab to take the same exam again as often as you wish. Nothing here is sent anywhere.</p>"
 "<div id=\"xerstat\"></div><p class=\"note\" id=\"xrmsg\" role=\"status\"></p><div id=\"xehist\"></div><div id=\"xrout\" aria-live=\"polite\"></div>"
 "<details class=\"xfile\"><summary>Result file and hand-in (optional)</summary><p class=\"note\">If your instructor asks for your result as a file, add your student number, name and surname here before you download it. They go only into the files you download and stay in this browser.</p>"
 "<div class=\"row\"><label class=\"note\" for=\"xesno\">Student number</label><input class=\"xin\" id=\"xesno\" size=\"12\" autocomplete=\"off\"><label class=\"note\" for=\"xesname\">Name</label><input class=\"xin\" id=\"xesname\" size=\"14\" autocomplete=\"off\"><label class=\"note\" for=\"xessur\">Surname</label><input class=\"xin\" id=\"xessur\" size=\"14\" autocomplete=\"off\"></div>"
 "<div class=\"row xzip\"><button class=\"btn\" id=\"xeauditzip\">Download my hand-in and audit log (zip)</button><span class=\"note\">One zip with the result file of each exam you finished and a log of what was done on this page. Kept in this browser until you ask for it.</span></div></details>"
 "<div id=\"xeclearbox\"></div></div>'}")
s = s[:i] + line + results_pane + s[j:]
# 5 the tab and the pane
rep("['exam','📝 Mock exam'],", "['exam','📝 Mock exam'],['examresults','📊 Exam results'],")
rep("P+=examPane();", "P+=examPane();P+=resultsPane();")
# 6 the list of attempts
rep("'<h3>My exams</h3><p class=\"note\">Every exam you start is kept here, in this browser. Open one again, review the marked attempt with its corrections, or take the same questions once more.</p>",
    "'<h3>My attempts</h3><p class=\"note\">Every exam you start is kept here, in this browser, with its score once you finish. Open an attempt to see your answers and the corrections, or take the same questions once more. You can take an exam as often as you wish.</p>")
rep("(r.status==='done'?(r.released?r.pct+'% ('+r.got+' of '+r.pts+')':'submitted, result locked'):'not finished')", "(r.status==='done'?r.pct+'% ('+r.got+' of '+r.pts+')':'not finished')")
rep("data-xeact=\"review\" data-xeid=\"'+r.id+'\">Review</button>", "data-xeact=\"review\" data-xeid=\"'+r.id+'\">Open result</button>")
rep("No exam yet. Start one above; it will be kept here.", "No exam yet. Start one on the Mock exam tab; its result will be kept here.")
rep("const o=document.getElementById('xeout');if(o)o.innerHTML='';", "['xeout','xrout'].forEach(i=>{const o=document.getElementById(i);if(o)o.innerHTML=''});")
rep(".xlock{border-color:var(--blue)}", "details.xfile{border:1px solid var(--line);border-radius:10px;margin:.5rem 0;padding:.3rem .8rem}details.xfile summary{cursor:pointer;font-weight:600}")
rep("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">\n", "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">\n<!-- course_page_template version 9.54.0 (SEN0414): the mock exam and its results are two functions - a new Exam results tab lists every attempt and opens its score, answers and corrections; a finished exam is marked and its result opens at once; the release-code lock and the identity gate of 9.19.0 are removed; an exam can be taken again without limit; the result file keeps the page's own marks for the instructor's desk. -->\n")
rep("the twelve question types, the mock exam, questions by subject", "the twelve question types, the mock exam with its results kept in a separate tab, questions by subject")
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("wrote", sys.argv[2], len(s))
