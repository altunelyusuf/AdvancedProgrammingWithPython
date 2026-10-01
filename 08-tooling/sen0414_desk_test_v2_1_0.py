#!/usr/bin/env python3
"""Browser test of the instructor's exam desk 2.0 against result files that the chapter page itself makes: files and zips dropped in (also a zip inside a zip,
a folder, an audit-log zip), every answer and the correct answer shown per question, the exam grid, the key, release codes accepted by the page, the class list,
grades and the announcement page. usage: sen0414_desk_test_v2_1_0.py NN   (PAGE_VER, DESK, KEY in the environment)"""
import os, sys, json, subprocess, tempfile, zipfile, io, base64, re
from playwright.sync_api import sync_playwright
__version__ = "2.1.0"
NN = sys.argv[1]; PV = os.environ.get("PAGE_VER", "9_20_0")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page = os.path.join(REPO, "03-materials", "ch" + NN, "page", "sen0414_ch%s_page_v%s.html" % (NN, PV))
desk = os.environ.get("DESK", os.path.join(REPO, "08-tooling", "sen0414_exam_desk_v2_1_0.html"))
KEY = os.environ.get("KEY", "/home/claude/instructor_keys/sen0414_instructor_key_v1_0_0.json")
REL = os.path.join(REPO, "08-tooling", "sen0414_exam_release_v1_0_0.py")
res = {}; F = lambda k, ok, d="": (res.__setitem__(k, bool(ok)), print("[%s] %s %s" % ("PASS" if ok else "FAIL", k, d)))
tmp = tempfile.mkdtemp()
FILL = open(os.path.join(REPO, "08-tooling", "sen0414_exam_test_v1_0_0.py"), encoding="utf-8").read().split('FILL = r"""')[1].split('"""')[0]
XFIX = r"""()=>{window.xfix=it=>'print = lambda *a, **k: None\ntry:\n'+it.code.split('\n').map(l=>'    '+l).join('\n')+'\nexcept Exception:\n    pass'}"""
with sync_playwright() as p:
    b = p.chromium.launch(**({"proxy": {"server": os.environ["HTTPS_PROXY"]}} if os.environ.get("HTTPS_PROXY") else {}))
    ctx = b.new_context(accept_downloads=True, viewport={"width": 1400, "height": 900}); pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + page); pg.wait_for_timeout(500)
    G = pg.evaluate("GROUP_OF").get("exam")
    if G: pg.click('#groups [data-tab="%s"]' % G); pg.click('[data-pane]:not([hidden]) .viewsub [data-tab="exam"]')
    else: pg.click('#groups [data-tab="exam"]')
    pg.evaluate(XFIX); pg.uncheck("#xetimeron")
    def take(sno, nm, sur, code, fill, rel=None):
        pg.fill("#xesno", sno); pg.fill("#xesname", nm); pg.fill("#xessur", sur); pg.fill("#xecode", code); pg.click("#xestart"); pg.wait_for_selector("#xefinish", timeout=180000)
        if fill == "keys": pg.evaluate(FILL)
        elif fill == "half": pg.evaluate(FILL.replace("fs.querySelectorAll('select[data-row]').forEach(s=>{s.value=s.dataset.row})", "0").replace("if(it.type==='mcq')fs.querySelector('input[value=\"'+k+'\"]').checked=true;", "if(it.type==='mcq'){const w=[...fs.querySelectorAll('input[type=radio]')].find(r=>r.value!==String(k));w.checked=true}"))
        pg.click("#xefinish"); pg.wait_for_selector("#xelock", timeout=240000)
        if rel:
            pg.fill("#xerel", rel); pg.click("#xeunlock"); pg.wait_for_selector("#xereport", timeout=60000)
        with pg.expect_download() as d: pg.click("#xejson")
        path = os.path.join(tmp, "%s_%s.json" % (sno, code)); d.value.save_as(path); return path
    ALL = subprocess.check_output(["python3", REL, KEY, "*", "*"]).decode().strip()
    a1 = take("20210001", "Ayşe", "Öztürk", "F-31337", "keys", ALL)     # all right, released (page marks inside)
    a2 = take("20210002", "Can", "Demir", "F-31337", "half", ALL)        # wrong mcq / unanswered matches, released
    a3 = take("20210003", "Zeynep", "Kaya", "F-31337", "none")           # nothing answered, locked (no page marks)
    # an audit zip from the page
    with pg.expect_download() as d: pg.click("#xeauditzip")
    azip = os.path.join(tmp, "audit.zip"); d.value.save_as(azip)
    # a zip with deflate, holding two results and a zip inside it
    inner = io.BytesIO()
    with zipfile.ZipFile(inner, "w", zipfile.ZIP_DEFLATED) as z: z.write(a3, "deep/" + os.path.basename(a3))
    bundle = os.path.join(tmp, "class_results.zip")
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(a1, "results/" + os.path.basename(a1)); z.write(a2, "results/" + os.path.basename(a2)); z.writestr("more/inner.zip", inner.getvalue()); z.writestr("__MACOSX/._x", b"x"); z.writestr("notes.txt", "hello")
    changed = json.load(open(a1, encoding="utf-8")); changed["student"]["number"] = "20219999"; chp = os.path.join(tmp, "changed.json"); json.dump(changed, open(chp, "w", encoding="utf-8"))
    roster = os.path.join(tmp, "roster.csv"); open(roster, "w", encoding="utf-8").write("Student No;Name;Surname\n20210001;Ayse;Ozturk\n20210002;Can;Demir\n20210003;Zeynep;Kaya\n20210004;Mert;Aksoy\n")
    keyj = KEY
    # ---- the desk ----
    dk = ctx.new_page(); derr = []; dk.on("pageerror", lambda e: derr.append(str(e))); dk.goto("file://" + desk); dk.wait_for_timeout(300)
    DROP = """async(files)=>{const dt=new DataTransfer();for(const f of files){const bin=Uint8Array.from(atob(f.b64),c=>c.charCodeAt(0));dt.items.add(new File([bin],f.name))}
      const ev=new DragEvent('drop',{dataTransfer:dt,bubbles:true,cancelable:true});document.querySelector('main section:last-child').dispatchEvent(ev);await new Promise(r=>setTimeout(r,200))}"""
    def drop(paths):
        dk.evaluate(DROP, [{"name": os.path.basename(x), "b64": base64.b64encode(open(x, "rb").read()).decode()} for x in paths])
    drop([bundle, azip, chp, roster, keyj])
    dk.wait_for_function("()=>document.querySelector('#markmsg').textContent.startsWith('Marked')||document.querySelectorAll('#restab tbody tr').length>=4", timeout=60000)
    dk.wait_for_function("()=>DESK.S.results.length>=4&&DESK.S.results.every(r=>r.re)", timeout=420000)
    log = dk.locator("#fltb").text_content()
    F("dropped files, a deflate zip, a zip inside a zip and an audit-log zip are all read; a file that is not an exam file is named and ignored", dk.evaluate("DESK.S.results.length") == 4 and "deep/" in log and "audit log" in log and "class list" in log and "key" in log and "notes.txt" in log and "not a type" in log, log[:0])
    F("the key dropped in is accepted", "Key loaded" in dk.locator("#keymsg").text_content())
    F("a file changed after saving is flagged, the others are 'unchanged'", dk.locator("#restab tbody .bad").count() >= 1 and "changed after saving" in dk.locator("#restab tbody").text_content() and dk.locator("#restab tbody .ok").count() == 3)
    sm = dk.locator("#cards").text_content()
    F("summary cards: students, files, exams, average, files to look at, class list", "result files" in sm and "average mark" in sm and "in the class list" in sm)
    dk.fill("#rq", "Zeynep"); F("the results list is searched by number or name", dk.locator("#restab tbody tr").count() == 1); dk.fill("#rq", "")
    # detail
    idx = dk.evaluate("DESK.S.results.findIndex(r=>r.sno==='20210002')")
    dk.click('[data-open="%d"]' % idx); dk.wait_for_selector("#dtab tbody tr", timeout=10000)
    rows = dk.locator("#dtab tbody tr"); n = rows.count(); r2 = dk.evaluate("DESK.S.results[%d]" % idx)
    mcq_row = dk.evaluate("""()=>{const r=DESK.S.results.find(r=>r.sno==='20210002');const i=r.obj.items.findIndex(it=>it.type==='mcq');const tr=document.getElementById('dq'+i);return {i,txt:tr.innerText,cls:tr.className,key:r.obj.items[i].options[r.obj.items[i].answer],given:r.obj.items[r.i===undefined?i:i]&&r.obj.items[i].options[r.obj.answers[i]]}}""")
    F("one exam in detail: every question with the student's answer, the correct answer, the points and why - and the wrong answer is marked wrong",
      n == r2["obj"]["items"].__len__() and "wrong" in mcq_row["cls"] and mcq_row["key"] in mcq_row["txt"] and (mcq_row["given"] or "") in mcq_row["txt"], "%d questions; mcq: %s" % (n, mcq_row["cls"]))
    pts = dk.evaluate("DESK.S.results[%d].re.pct" % idx); pagepct = r2["obj"]["page_total"]["percent"]
    F("the desk's mark equals the page's own mark in the released file, question by question", dk.evaluate("DESK.S.results[%d].re.per.map(p=>p.score)" % idx) == r2["obj"]["page_marks"] and pts == pagepct, "%s%% desk, %s%% page" % (pts, pagepct))
    dk.check("#dwrong"); shown = dk.locator("#dtab tbody tr:visible").count(); F("'only questions not fully right' hides the fully right ones", 0 < shown < n, "%d of %d" % (shown, n)); dk.uncheck("#dwrong")
    # analysis
    key = dk.evaluate("DESK.S.results.find(r=>r.sno==='20210001').ch+'|F-31337'"); dk.select_option("#asel", key); dk.wait_for_selector(".mx tbody tr", timeout=10000)
    F("exam analysis: a grid of all students by all questions, and per question the share who got it right and the commonest wrong answers", dk.locator(".mx tbody tr").count() == 4 and dk.locator(".mx tbody td.s.r").count() > 0 and dk.locator(".mx tbody td.s.w").count() > 0 and "Fully right" in dk.locator("#analbox").text_content())
    sa = dk.locator("#analbox .sa"); stxt = " | ".join(sa.all_inner_texts()[:200])
    F("exam analysis: every student's own answer to every question is listed (number, right/wrong mark and the answer text)", sa.count() == 4 * 20 and "20210002" in stxt and dk.locator("#analbox .sa.w").count() > 0 and dk.locator("#analbox .sa.r").count() > 0, "%d answers listed" % sa.count())
    F("the desk has a way back to the index", dk.locator("a.idxlink").get_attribute("href") == "index.html")
    dk.locator(".mx tbody td.s.w").first.click(); dk.wait_for_timeout(300); F("clicking a cell opens that student's answer to that question", dk.locator("#dtab tbody tr.sel").count() == 1)
    F("the class list shows who handed in, who did not, and who is not on the list; accents do not matter", "none" in dk.locator("#rostbox").text_content() and "not in the class list" in dk.locator("#rostbox").text_content() and "differs" not in dk.locator("#rostbox").text_content())
    F("the audit log is shown with its events", "events" in dk.locator("#audbox").text_content() and dk.locator("#audbox details").count() == 1)
    dk.click("#call"); dk.wait_for_selector("#codetb tr", timeout=10000); code = dk.evaluate("DESK.S.codes[0].value")
    pg2 = ctx.new_page(); pg2.goto("file://" + page); pg2.wait_for_timeout(400)
    F("a release code made by the desk is accepted by the exam page for its exam", pg2.evaluate("async c=>(await xVerifyRelease(c,{code:'F-31337'})).ok", code))
    dk.click("#gmake"); dk.wait_for_timeout(300); g = dk.evaluate("DESK.S.grades"); g1 = next(x for x in g if x["sno"] == "20210001")
    F("grades: each student's bonus is the average of the best chapter marks times the bonus points", g1["bonus"] == round(g1["avg"] * 10) / 100 and len(g) == 4)
    with dk.expect_download() as d: dk.click("#ghtml")
    hp = os.path.join(tmp, "ann.html"); d.value.save_as(hp); ah = open(hp, encoding="utf-8").read()
    F("the announcement page is a stand-alone HTML with student numbers and bonuses and no names unless asked", "20210001" in ah and "Ayşe" not in ah and "<table" in ah)
    dk.set_viewport_size({"width": 390, "height": 800}); dk.wait_for_timeout(200); F("no sideways scroll on a phone", dk.evaluate("document.documentElement.scrollWidth") <= 391, str(dk.evaluate("document.documentElement.scrollWidth")))
    F("the desk's own errors are empty, and so are the page's", not derr and not errs, str((derr + errs)[:2]))
    b.close()
json.dump(res, open(os.path.join(REPO, "08-tooling", "ch%s-page" % NN, "desk_test_results_v2_1_0.json"), "w"), indent=1)
print("desk test: %d pass, %d fail" % (sum(res.values()), len(res) - sum(res.values())))
