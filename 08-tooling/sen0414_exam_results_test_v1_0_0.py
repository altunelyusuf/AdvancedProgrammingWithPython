#!/usr/bin/env python3
"""sen0414_exam_results_test 1.0.0 - tests the mock exam and exam results behaviour of template 9.54.0 on one built chapter page.
Used for the pages retrofitted by page_retrofit_exam_v1_0_0.py (their full test versions still assert the release lock that was removed).
usage: sen0414_exam_results_test_v1_0_0.py PAGE.html   exit 0 only when every check passes"""
import sys, os, json, zipfile, tempfile
import re, hashlib as _hl, ssl as _ssl, urllib.request as _ur
from playwright.sync_api import sync_playwright
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sen0414_page_test_v9_41_0.py"), encoding="utf-8").read()
exec(_src[_src.index("def _cdn_cached"):_src.index("import glob as _g")])   # the same cached CDN route as the page test (Pyodide for the question generators)
__version__ = "1.0.0"
page_path = os.path.abspath(sys.argv[1]); AXE = "/home/claude/Ontologies/rdodi-ecosystem/07-pedagogy-professional-stage/lib/axe.min.js"
res = []
def feat(k, ok, det=""):
    res.append(bool(ok)); print("  [%s] %s  %s" % ("PASS" if ok else "FAIL", k, str(det)[:300]))
FILL = r"""()=>{document.querySelectorAll('#xeout fieldset[data-xi]').forEach((fs,i)=>{const it=XE.items[i],k=xKey(it),set=(sel,v)=>{const e=fs.querySelector(sel);e.value=v};
 if(it.type==='mcq')fs.querySelector('input[value="'+k+'"]').checked=true;
 else if(it.type==='multi')k.forEach(j=>{fs.querySelectorAll('input[type=checkbox]')[j].checked=true});
 else if(it.type==='judge'){fs.querySelector('input[value="'+k.v+'"]').checked=true;fs.querySelector('select').value=k.s}
 else if(it.type==='match')fs.querySelectorAll('select[data-row]').forEach(s=>{s.value=s.dataset.row});
 else if(it.type==='order'){const ol=fs.querySelector('ol');[...ol.children].sort((a,b)=>a.querySelector('code').dataset.l-b.querySelector('code').dataset.l).forEach(li=>ol.appendChild(li))}
 else if(it.type==='repair')set('textarea',xfix(it));
 else set('textarea,input.xin',String(k))})}"""
PANES = "[...document.querySelectorAll('[data-pane]')].filter(e=>!e.hidden).map(e=>e.dataset.pane)"
with sync_playwright() as p:
    b = p.chromium.launch(env=dict(os.environ, LANG="en_US.UTF-8", LC_ALL="en_US.UTF-8"), **({"proxy": {"server": os.environ["HTTPS_PROXY"]}} if os.environ.get("HTTPS_PROXY") else {})); ctx = b.new_context(locale="en-US", viewport={"width": 1280, "height": 900}, accept_downloads=True); ctx.route(re.compile(r"^https://cdn\.jsdelivr\.net/"), _cdn_cached); pg = ctx.new_page()
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + page_path); pg.wait_for_timeout(1500)
    pg.evaluate(r"""()=>{window.xfix=it=>'print = lambda *a, **k: None\ntry:\n'+it.code.split('\n').map(l=>'    '+l).join('\n')+'\nexcept Exception:\n    pass'}""")
    tabs = pg.evaluate("[...new Set([...document.querySelectorAll('[role=tab]')].map(t=>t.textContent.trim()))].filter(t=>/Mock exam|Exam results/.test(t))")
    feat("the Practice menu has two separate tabs: Mock exam and Exam results", len(tabs) == 2, tabs)
    pg.evaluate("showTab('exam')"); pg.wait_for_timeout(300)
    feat("the Mock exam tab holds no attempt list, no identity form and no release code", pg.locator('[data-pane="exam"] #xehist').count() == 0 and pg.locator('[data-pane="exam"] #xesno').count() == 0 and pg.locator("#xerel,#xelock").count() == 0)
    pg.select_option("#xekind", "F"); pg.uncheck("#xetimeron"); pg.fill("#xecode", "F-31337"); pg.click("#xestart"); pg.wait_for_selector("#xefinish", timeout=180000)
    nq = pg.locator("#xeout fieldset.xq").count(); first = pg.locator("#xeout fieldset.xq legend").first.text_content()
    feat("an exam starts from a code without a student number, name or release code", nq >= 10 and pg.input_value("#xecode") == "F-31337", "%d questions" % nq)
    pg.evaluate(FILL); pg.click("#xefinish"); pg.wait_for_selector("#xereport", timeout=240000)
    sh = pg.evaluate("()=>({panes:%s,note:!!document.querySelector('[data-pane=exam] #xefinished'),inres:!!document.querySelector('[data-pane=examresults] #xrout #xereport'),inexam:!!document.querySelector('[data-pane=exam] #xereport'),lock:document.querySelectorAll('#xelock,#xerel,#xeunlock').length,fb:document.querySelectorAll('#xrout .xfeed .xmsg').length,pct:XE.result.pct})" % PANES)
    feat("Finish marks the exam and opens the result at once in the Exam results tab, with a correction under every question and no lock", sh["panes"] == ["examresults"] and sh["note"] and sh["inres"] and not sh["inexam"] and sh["lock"] == 0 and sh["fb"] == nq and sh["pct"] >= 95 and pg.locator("#xejson").count() == 1 and pg.locator("#xepdf").count() == 1, str(sh))
    feat("the result lists points by subject", pg.locator("#xereport table tr").count() >= 2)
    feat("the attempt is listed with its score and the attempts line counts it", "F-31337" in pg.locator("#xehist").text_content() and "Finished attempts: 1" in pg.locator("#xerstat").text_content(), pg.locator("#xerstat").text_content())
    pg.click("#xeagain"); pg.wait_for_selector("#xefinish", timeout=180000)
    feat("Retake gives the same exam and goes back to the Mock exam tab", pg.locator("#xeout fieldset.xq legend").first.text_content() == first and pg.evaluate(PANES) == ["exam"])
    pg.evaluate("showTab('examresults')"); pg.locator("#xehist [data-xeact=review]").first.click(); pg.wait_for_timeout(500)
    feat("a result is not opened over an exam that is open, and the page says so", "still open" in pg.locator("#xrmsg").text_content() and pg.locator("#xrout #xereport").count() == 0)
    pg.evaluate("showTab('exam')"); pg.click("#xefinish"); pg.wait_for_selector("#xereport", timeout=240000)
    feat("an exam left unanswered scores little and is listed as a second attempt", pg.evaluate("XE.result.pct") <= 30 and pg.locator("#xehist tbody tr").count() == 2)
    pg.locator("#xehist tbody tr").nth(1).locator("[data-xeact=review]").click(); pg.wait_for_selector("#xrout #xereport", timeout=120000); pg.wait_for_timeout(400)
    rv = pg.evaluate("()=>({msgs:document.querySelectorAll('#xrout .xfeed .xmsg').length,dis:[...document.querySelectorAll('#xrout fieldset[data-xi] input,#xrout fieldset[data-xi] textarea')].filter(e=>!e.closest('.ed')).every(e=>e.disabled),ids:['xetimer','xesum','xereport'].map(i=>document.querySelectorAll('#'+i).length)})")
    feat("Open result shows the earlier attempt with answers and corrections, read-only, with no repeated page ids", rv["msgs"] == nq and rv["dis"] and all(x <= 1 for x in rv["ids"]), str(rv))
    pg.evaluate("showTab('exam')"); pg.select_option("#xekind", "M"); pg.click("#xenew"); pg.wait_for_selector("#xefinish", timeout=180000); nc = pg.input_value("#xecode")
    feat("a new exam draws another code", nc.startswith("M-"), nc)
    pg.click("#xefinish"); pg.wait_for_selector("#xereport", timeout=240000)
    rp = ctx.new_page(); rp.goto("file://" + page_path); rp.wait_for_timeout(1000); rp.evaluate("showTab('examresults')"); kept = rp.evaluate("document.querySelectorAll('#xehist tbody tr').length"); rp.close()
    feat("the attempts survive a reload", kept >= 3, kept)
    pg.evaluate("showTab('examresults')"); pg.evaluate("document.querySelector('details.xfile').open=true"); pg.fill("#xesno", "20210001"); pg.fill("#xesname", "Test"); pg.fill("#xessur", "Student")
    with pg.expect_download() as dj: pg.click("#xejson")
    jp = os.path.join(tempfile.mkdtemp(), "r.json"); dj.value.save_as(jp); ro = json.load(open(jp, encoding="utf-8"))
    feat("the result file carries the optional details, the answers, the page's own marks and a check value, with no release field", ro["student"]["number"] == "20210001" and ro.get("page_total", {}).get("points", 0) > 0 and len(ro["page_marks"]) == len(ro["items"]) and "digest" in ro and "release_code" not in ro and "released" not in ro, str(ro.get("page_total")))
    with pg.expect_download() as dp: pg.click("#xepdf")
    pdf = open(dp.value.path(), "rb").read(); feat("the PDF copy is a PDF", pdf[:5] == b"%PDF-")
    with pg.expect_download() as dz: pg.click("#xeauditzip")
    zp = os.path.join(tempfile.mkdtemp(), "a.zip"); dz.value.save_as(zp); z = zipfile.ZipFile(zp); evs = [e["event"] for e in json.loads(z.read("audit_log.json"))["events"]]; txt = z.read("audit_log.json").decode()
    feat("the hand-in zip is valid and the audit log records opened, started, finished and result saved, with no release code", z.testzip() is None and {"page_opened", "exam_started", "exam_finished", "result_json_saved"} <= set(evs) and "R1." not in txt, evs[-6:])
    pg.add_script_tag(path=AXE)
    ax = {}
    for pane in ("examresults", "exam"):
        pg.evaluate("showTab('%s')" % pane); ax[pane] = pg.evaluate("async()=>{const r=await axe.run({include:[['[data-pane=\"%s\"]']]},{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}});return r.violations.map(v=>[v.id,v.nodes.length])}" % pane)
    feat("WCAG 2 A/AA (axe-core) over the Exam results and Mock exam tabs", not ax["examresults"] and not ax["exam"], str(ax))
    pg.evaluate("showTab('examresults')"); pg.click("#xeclear"); asked = pg.locator("#xeclearyes").count() == 1 and pg.locator("#xeclearzip").count() == 1; pg.click("#xeclearyes"); pg.wait_for_timeout(300)
    feat("the clear option asks first and then empties the list and the open result", asked and pg.locator("#xehist tbody tr").count() == 0 and pg.locator("#xrout").inner_html().strip() == "")
    feat("no script errors on the page", not errs, errs[:2])
    b.close()
print("exam results test 1.0.0: %d checks, %d failed" % (len(res), res.count(False)))
sys.exit(0 if all(res) else 1)
