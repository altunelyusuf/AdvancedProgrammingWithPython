#!/usr/bin/env python3
"""Checks what the exam questions look like and that new exams do not repeat at once: for a chapter page, 8 new midterm exams are started and finished one after the other
through the page's own controls. Requires: no "......" in any question, nothing about the book's layout in a statement, no fill-in-the-word question in a midterm,
and across the 8 exams fewer repeated questions than the same exams would have if the seeds had been drawn blindly. usage: sen0414_exam_questions_test_v1_0_0.py NN  (PAGE_VER in the environment)"""
import os, sys, re, json
from playwright.sync_api import sync_playwright
NN = sys.argv[1]; PV = os.environ.get("PAGE_VER", "9_21_0")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page = os.path.join(REPO, "03-materials", "ch" + NN, "page", "sen0414_ch%s_page_v%s.html" % (NN, PV))
res = {}; F = lambda k, ok, d="": (res.__setitem__(k, bool(ok)), print("[%s] %s %s" % ("PASS" if ok else "FAIL", k, d)))
with sync_playwright() as p:
    b = p.chromium.launch(**({"proxy": {"server": os.environ["HTTPS_PROXY"]}} if os.environ.get("HTTPS_PROXY") else {}))
    pg = b.new_context(viewport={"width": 1300, "height": 900}).new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + page); pg.wait_for_timeout(800)
    G = pg.evaluate("GROUP_OF").get("exam")
    if G: pg.click('#groups [data-tab="%s"]' % G)
    pg.click('[data-pane]:not([hidden]) .viewsub [data-tab="exam"]') if G else pg.click('#groups [data-tab="exam"]')
    pg.uncheck("#xetimeron"); pg.select_option("#xekind", "M")
    pg.fill("#xesno", "20210001"); pg.fill("#xesname", "Test"); pg.fill("#xessur", "Student")
    texts = []; fps = []
    for i in range(8):
        pg.fill("#xecode", ""); pg.click("#xestart"); pg.wait_for_selector("#xefinish", timeout=240000)
        texts.append(pg.inner_text("#xeout")); fps.append(pg.evaluate("XE.items.map(xFp)"))
        pg.click("#xefinish"); pg.wait_for_selector("#xelock", timeout=240000)
    alltext = "\n".join(texts)
    F("no '......' (masked words) in any question of 8 midterms", "……" not in alltext and "......" not in alltext)
    F("no statement about the book's layout (chapter / section / author / citation) in the 8 midterms", not re.search(r"\b(chapter|section|the book|the author)\b|Sweigart|\(\w+, 20\d\d\)", alltext, re.I), "")
    F("no fill-in-the-word question in a midterm", "Fill in the blank (words)" not in alltext)
    pool = pg.evaluate("D.nodes.filter(n=>xFact(n)).length")
    seen = set(); rep = 0; total = 0
    for fp in fps:
        for x in fp:
            total += 1; rep += (x in seen)
        seen.update(fp)
    # blind drawing for the same pool, for comparison: the same 8 exams, seeds chosen without looking at what was asked
    blind = pg.evaluate("""async()=>{const seen=new Set();let rep=0,total=0;for(let i=0;i<8;i++){const its=await xExamBuild('M',1+Math.floor(Math.random()*99999));its.forEach(x=>{total++;if(seen.has(xFp(x)))rep++});its.forEach(x=>seen.add(xFp(x)))}return [rep,total]}""")
    F("a new exam avoids what the student has already had: clearly fewer repeated questions than blind drawing (at most 80%)", rep <= 0.8 * blind[0], "%d of %d repeated (blind drawing: %d of %d); %d usable concepts" % (rep, total, blind[0], blind[1], pool))
    F("the page's errors are empty", not errs, str(errs[:2]))
    sample = [l for l in texts[0].split("\n") if l.strip()][:30]
    print("\n".join(sample))
json.dump(res, open(os.path.join(REPO, "08-tooling", "ch%s-page" % NN, "exam_questions_test_results_v1_0_0.json"), "w"), indent=1)
print("exam questions test: %d pass, %d fail" % (sum(res.values()), len(res) - sum(res.values())))
