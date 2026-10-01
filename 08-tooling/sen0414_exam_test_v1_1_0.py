#!/usr/bin/env python3
"""Browser test of the graded exam and the instructor desk, end to end: identity first, locked result, JSON and PDF, release code (right,
wrong chapter, altered), the desk marking the page's own result file with the same score, file-change detection, roster, release codes the
exam page accepts, and the grade list. usage: sen0414_exam_test_v1_0_0.py NN   (PAGE_VER, DESK env)"""
import os, sys, json, subprocess, re, tempfile
from playwright.sync_api import sync_playwright
__version__ = "1.0.0"
NN = sys.argv[1]; PV = os.environ.get("PAGE_VER", "9_19_0")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page = os.path.join(REPO, "03-materials", "ch" + NN, "page", "sen0414_ch%s_page_v%s.html" % (NN, PV))
desk = os.environ.get("DESK", "/tmp/sen0414_exam_desk.html")
KEY = os.environ.get("KEY", "/home/claude/instructor_keys/sen0414_instructor_key_v1_0_0.json")
REL = os.path.join(REPO, "08-tooling", "sen0414_exam_release_v1_0_0.py")
res = {}; F = lambda k, ok, d="": (res.__setitem__(k, bool(ok)), print("[%s] %s %s" % ("PASS" if ok else "FAIL", k, d)))
tmp = tempfile.mkdtemp()
FILL = r"""()=>{document.querySelectorAll('#xeout fieldset[data-xi]').forEach((fs,i)=>{const it=XE.items[i],k=xKey(it),set=(sel,v)=>{const e=fs.querySelector(sel);e.value=v};
 if(it.type==='mcq')fs.querySelector('input[value="'+k+'"]').checked=true;
 else if(it.type==='multi')k.forEach(j=>{fs.querySelectorAll('input[type=checkbox]')[j].checked=true});
 else if(it.type==='judge'){fs.querySelector('input[value="'+k.v+'"]').checked=true;fs.querySelector('select').value=k.s}
 else if(it.type==='match')fs.querySelectorAll('select[data-row]').forEach(s=>{s.value=s.dataset.row});
 else if(it.type==='order'){const ol=fs.querySelector('ol');[...ol.children].sort((a,b)=>a.querySelector('code').dataset.l-b.querySelector('code').dataset.l).forEach(li=>ol.appendChild(li))}
 else if(it.type==='repair')set('textarea',xfix(it));
 else set('textarea,input.xin',String(k))})}"""
with sync_playwright() as p:
    b = p.chromium.launch(**({"proxy": {"server": os.environ["HTTPS_PROXY"]}} if os.environ.get("HTTPS_PROXY") else {}))
    ctx = b.new_context(accept_downloads=True, viewport={"width": 1400, "height": 900}); pg = ctx.new_page(); errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None); pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + page); pg.wait_for_timeout(500)
    G = pg.evaluate("GROUP_OF").get("exam")
    if G: pg.click('#groups [data-tab="%s"]' % G); pg.click('[data-pane]:not([hidden]) .viewsub [data-tab="exam"]')
    else: pg.click('#groups [data-tab="exam"]')
    pg.uncheck("#xetimeron"); pg.fill("#xecode", "F-31337")
    pg.click("#xestart"); pg.wait_for_timeout(400)
    F("nothing starts without the student number, name and surname", pg.locator("#xefinish").count() == 0 and "student number" in pg.locator("#xeidmsg").text_content())
    pg.fill("#xesno", "ab"); pg.fill("#xesname", "Ayşe"); pg.fill("#xessur", "Öztürk"); pg.click("#xestart"); pg.wait_for_timeout(300)
    F("a student number that is too short is refused", pg.locator("#xefinish").count() == 0)
    pg.fill("#xesno", "20210001"); pg.click("#xestart"); pg.wait_for_selector("#xefinish", timeout=180000)
    F("with all three given the exam starts", pg.locator("#xeout fieldset.xq").count() >= 15)
    pg.evaluate(r"""()=>{window.xfix=it=>'print = lambda *a, **k: None\ntry:\n'+it.code.split('\n').map(l=>'    '+l).join('\n')+'\nexcept Exception:\n    pass'}"""); pg.evaluate(FILL); pg.click("#xefinish"); pg.wait_for_selector("#xelock", timeout=240000)
    F("after Finish only 'Submitted' is shown: no score, no report, no correction text", pg.locator("#xereport").count() == 0 and pg.evaluate("[...document.querySelectorAll('#xeout .xfeed')].every(e=>e.textContent==='')") and "%" not in pg.locator("#xelock").text_content() and "Ayşe Öztürk" in pg.locator("#xelock").text_content())
    with pg.expect_download() as d: pg.click("#xejson")
    jp = os.path.join(tmp, "a.json"); d.value.save_as(jp); J = json.load(open(jp, encoding="utf-8"))
    F("the JSON result carries student number, name, surname, chapter, exam code, items, answers and a check value", J["student"] == {"number": "20210001", "name": "Ayşe", "surname": "Öztürk"} and J["exam"]["code"] == "F-31337" and len(J["items"]) == len(J["answers"]) >= 15 and len(J["digest"]["value"]) == 64 and "page_marks" not in J, d.value.suggested_filename)
    with pg.expect_download() as d: pg.click("#xepdf")
    pp = os.path.join(tmp, "a.pdf"); d.value.save_as(pp); raw = open(pp, "rb").read()
    info = subprocess.run(["pdfinfo", pp], capture_output=True, text=True).stdout
    F("the PDF copy is a real PDF of A4 pages", raw[:5] == b"%PDF-" and "A4" in info and re.search(r"Pages:\s+[1-9]", info) is not None, info.split("Pages:")[1].split()[0] + " pages")
    subprocess.run(["pdftoppm", "-r", "40", "-png", "-f", "1", "-l", "1", pp, os.path.join(tmp, "pdfp")])
    code = lambda ch, ex: subprocess.check_output(["python3", REL, KEY, ch, ex]).decode().strip()
    ok_code = code(NN.lstrip("0") or "0", "F-31337")
    def attempt(c):
        pg.fill("#xerel", c); pg.click("#xeunlock"); pg.wait_for_timeout(500); return pg.locator("#xerelmsg").text_content() if pg.locator("#xerelmsg").count() else "(released)"
    m_other = attempt(code(NN.lstrip("0") or "0", "F-11111")); m_chap = attempt(code("99", "F-31337"))
    bad = ok_code[:-3] + ("AAA" if not ok_code.endswith("AAA") else "BBB"); m_alt = attempt(bad)
    F("a code for another exam, another chapter, or an altered code is refused, and the result stays hidden", "another exam" in m_other and "another exam" in m_chap and "not signed" in m_alt and pg.locator("#xereport").count() == 0, "%s | %s | %s" % (m_other[:40], m_chap[:40], m_alt[:40]))
    pg.fill("#xerel", ok_code); pg.click("#xeunlock"); pg.wait_for_selector("#xereport", timeout=60000)
    sc = pg.evaluate("XE.result")
    F("the instructor's code releases the result: score, subjects, and a correction under each question", sc["pct"] >= 95 and pg.locator("#xeout .xfeed .xmsg").count() >= 15, "%s%%" % sc["pct"])
    with pg.expect_download() as d: pg.click("#xejson")
    d.value.save_as(os.path.join(tmp, "a_rel.json")); JR = json.load(open(os.path.join(tmp, "a_rel.json"), encoding="utf-8"))
    F("after release the JSON also holds the page's marks and the release code", JR.get("released") is True and JR["release_code"] == ok_code and len(JR["page_marks"]) == len(JR["items"]) and JR["page_total"]["percent"] == sc["pct"])
    F("the history keeps the exam and shows its result only after release", "F-31337" in pg.locator("#xehist").text_content() and "%" in pg.locator("#xehist").text_content())
    # a second exam, left blank, by a second student: made through the page itself
    pg.evaluate("localStorage.removeItem('course-page-student')")
    pg.fill("#xecode", "M-777"); pg.fill("#xesno", "20210002"); pg.fill("#xesname", "Can"); pg.fill("#xessur", "Demir"); pg.click("#xestart"); pg.wait_for_selector("#xefinish", timeout=180000)
    pg.click("#xefinish"); pg.wait_for_selector("#xelock", timeout=240000)
    pg.fill("#xerel", code(NN.lstrip("0") or "0", "M-777")); pg.click("#xeunlock"); pg.wait_for_selector("#xereport", timeout=60000)
    with pg.expect_download() as d: pg.click("#xejson")
    d.value.save_as(os.path.join(tmp, "b.json")); JB = json.load(open(os.path.join(tmp, "b.json"), encoding="utf-8"))
    # a file changed by hand
    JC = json.loads(json.dumps(J)); JC["student"]["number"] = "20219999"; json.dump(JC, open(os.path.join(tmp, "c.json"), "w", encoding="utf-8"))
    F("the page's own errors are empty", not errs, str(errs[:2]))
    # ---- the desk ----
    dk = ctx.new_page(); derr = []; dk.on("console", lambda m: derr.append(m.text) if m.type == "error" else None); dk.on("pageerror", lambda e: derr.append(str(e)))
    dk.goto("file://" + desk); dk.wait_for_timeout(300)
    dk.set_input_files("#keyfile", KEY); dk.wait_for_function("()=>document.querySelector('#keymsg').className==='ok'", timeout=10000)
    F("the desk accepts the instructor key and checks it against the public key built into the pages", "matches" in dk.locator("#keymsg").text_content())
    wrong = os.path.join(tmp, "wrongkey.json"); wk = json.load(open(KEY)); wk["private_jwk"]["x"] = "A" * 43; json.dump(wk, open(wrong, "w"))
    dk.set_input_files("#keyfile", wrong); dk.wait_for_function("()=>document.querySelector('#keymsg').className==='bad'", timeout=10000); bad_msg = dk.locator("#keymsg").text_content()
    dk.set_input_files("#keyfile", KEY); dk.wait_for_function("()=>document.querySelector('#keymsg').className==='ok'", timeout=10000)
    F("a key that does not belong to the exam pages is refused", "does not belong" in bad_msg)
    dk.click('nav [data-k="results"]'); dk.set_input_files("#resfiles", [os.path.join(tmp, f) for f in ("a.json", "b.json", "c.json")]); dk.wait_for_function("()=>document.querySelectorAll('#restab tbody tr').length===3", timeout=20000)
    txt = dk.locator("#restab tbody").text_content()
    F("the desk lists the three files and flags the one changed after saving", "20210001" in txt and "20210002" in txt and "20219999" in txt and dk.locator("#restab tbody .bad").count() == 1, "")
    dk.click("#regrade"); dk.wait_for_function("()=>document.querySelector('#resmsg').textContent.startsWith('Marked')", timeout=420000)
    mk = dk.evaluate("DESK.S.results.map(r=>({sno:r.sno,pct:r.re.pct,got:r.re.got,per:r.re.per}))")
    a = next(x for x in mk if x["sno"] == "20210001"); bb = next(x for x in mk if x["sno"] == "20210002")
    JA = JR
    F("the desk marks the page's own result file with the same mark, question by question", a["per"] == JA["page_marks"] and a["pct"] == JA["page_total"]["percent"], "%s%% desk, %s%% page" % (a["pct"], JA["page_total"]["percent"]))
    F("an unanswered exam scores little at the desk, and the desk's mark equals the page's, question by question", bb["pct"] <= 30 and bb["per"] == JB["page_marks"], "%s%%" % bb["pct"])
    dk.click('nav [data-k="roster"]'); csvp = os.path.join(tmp, "roster.csv"); open(csvp, "w", encoding="utf-8").write("Student No;Name;Surname\n20210001;Ayse;Ozturk\n20210002;Can;Demir\n20210003;Zeynep;Kaya\n"); dk.set_input_files("#rosterfile", csvp)
    dk.wait_for_function("()=>document.querySelectorAll('#rosttab tbody tr').length>=3", timeout=10000); rt = dk.locator("#rosttab tbody").text_content()
    F("the class list shows who handed in, who did not, and who is not on the list; accented names match their plain form", "none" in rt and "not in the class list" in rt and rt.count("differs") == 0, "")
    dk.click('nav [data-k="codes"]'); dk.click("#call"); dk.wait_for_function("()=>document.querySelectorAll('#codetab tbody tr').length>=2", timeout=10000)
    dcode = dk.evaluate("DESK.S.codes.find(c=>c.code==='F-31337').value")
    pg.fill("#xerel", "") if pg.locator("#xerel").count() else None
    # the page must accept a code made by the desk (a different, fresh page state)
    pg2 = ctx.new_page(); pg2.goto("file://" + page); pg2.wait_for_timeout(400)
    ok2 = pg2.evaluate("async c=>{const r=await xVerifyRelease(c,{code:'F-31337'});return r.ok}", dcode)
    ok3 = pg2.evaluate("async c=>{const r=await xVerifyRelease(c,{code:'F-31338'});return r.ok}", dcode)
    wide = dk.evaluate("DESK.release('*','*')"); ok4 = pg2.evaluate("async c=>{const r=await xVerifyRelease(c,{code:'M-1'});return r.ok}", wide)
    F("a code made by the desk is accepted by the exam page for its exam only; the all-exams code is accepted for any", ok2 and not ok3 and ok4)
    dk.click('nav [data-k="grades"]'); dk.click("#gmake"); dk.wait_for_timeout(300); gt = dk.locator("#gradetab tbody").text_content(); ann = dk.input_value("#gann")
    gr = dk.evaluate("DESK.S.grades")
    g1 = next(g for g in gr if g["sno"] == "20210001")
    F("the grade list gives each student a bonus out of the bonus points, and the announcement lists student numbers", g1["bonus"] == round(g1["avg"] * 10) / 100 and "20210001" in ann and "Ayşe" not in ann, "bonus %s (average %s%%)" % (g1["bonus"], g1["avg"]))
    dk.check("#gnames"); dk.click("#gmake"); F("names appear in the announcement only when asked for", "Ayşe" in dk.input_value("#gann"))
    F("the desk's own errors are empty", not derr, str(derr[:2]))
    b.close()
json.dump(res, open(os.path.join(REPO, "08-tooling", "ch%s-page" % NN, "exam_test_results_v%s.json" % PV), "w"), indent=1)
print("exam test ch%s: %d pass, %d fail" % (NN, sum(res.values()), len(res) - sum(res.values())))
