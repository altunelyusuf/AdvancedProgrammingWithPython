#!/usr/bin/env python3
"""Browser test of the 9.22.0 interaction changes on a chapter page: no code-pattern list in any editor, every Code Lab example runs, the live-model bar is at the top of the Agents view,
multiple choice ends with "None of the above" (and is marked right either way), ordering lines by dragging, by holding the arrows and by keyboard, the hand-in zip button at the top of the Exam view.
usage: sen0414_interaction_test_v1_0_0.py NN  (PAGE_VER in the environment)"""
import os, sys, json
from playwright.sync_api import sync_playwright
NN = sys.argv[1]; PV = os.environ.get("PAGE_VER", "9_22_0")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page = os.path.join(REPO, "03-materials", "ch" + NN, "page", "sen0414_ch%s_page_v%s.html" % (NN, PV))
res = {}; F = lambda k, ok, d="": (res.__setitem__(k, bool(ok)), print("[%s] %s %s" % ("PASS" if ok else "FAIL", k, d)))
with sync_playwright() as p:
    b = p.chromium.launch(**({"proxy": {"server": os.environ["HTTPS_PROXY"]}} if os.environ.get("HTTPS_PROXY") else {}))
    pg = b.new_context(viewport={"width": 1100, "height": 900}).new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + page); pg.wait_for_timeout(2500)
    pg.click("#groups >> text=Lab"); pg.click('.viewsub [data-tab="codelab"]')
    F("no 'Code patterns' list in any editor (the Playground keeps its single list)", pg.locator("[data-edtpl]").count() == 0 and pg.locator("#pex optgroup").count() == 2)
    n = pg.locator("#clsnip option").count(); outs = []
    for i in range(n):
        pg.select_option("#clsnip", str(i)); pg.click("#clrun"); pg.wait_for_function("()=>{const t=document.getElementById('clout').textContent.trim();return t.length>0&&!/running/.test(t)}", timeout=90000); outs.append(pg.text_content("#clout").strip())
    F("every Code Lab example runs without an error", n >= 5 and not any("Error" in o[:40] for o in outs), "%d examples" % n)
    F("the first Code Lab examples need only the chapter (no import, no def) and the others say 'Advanced'", all("import" not in pg.evaluate("CODELAB_SNIPPETS[%d][1]" % i) and "def " not in pg.evaluate("CODELAB_SNIPPETS[%d][1]" % i) for i in range(4)) and sum("Advanced" in pg.evaluate("CODELAB_SNIPPETS[%d][0]" % i) for i in range(n)) >= 3)
    pg.click("#groups >> text=Agents")
    F("Enable live LLM and the model choice are at the top of the Agents view", pg.evaluate("(()=>{const k=document.querySelector('[data-pane=agents] .kit'),a=document.querySelector('[data-pane=agents] .agentsview');return !!k&&k.getBoundingClientRect().top<a.getBoundingClientRect().top&&!!k.querySelector('#llmbtn')})()"))
    # multiple choice
    r = pg.evaluate("""async()=>{let none=0,left=0,tot=0,bad=[];for(let sd=1;sd<=60;sd++){const its=(await xExamBuild('M',sd)).filter(i=>i.type==='mcq');for(const it of its){tot++;const last=it.options[it.options.length-1];if(last==='None of the above')none++;else bad.push(it.q);if(last==='None of the above'&&it.answer===it.options.length-1)left++;
        const a=await xMark(it,it.answer),w=await xMark(it,(it.answer+1)%it.options.length);if(a.score!==1||w.score>=1)bad.push('mark:'+it.q)}}return {tot,none,left,bad:bad.slice(0,3)}}""")
    F("multiple choice ends with 'None of the above'; sometimes it is the right answer; right scores 1, wrong scores 0", r["tot"] > 100 and r["none"] == r["tot"] and 0.1 < r["left"] / r["tot"] < 0.4 and not r["bad"], str(r))
    pg.click("#groups >> text=Practice"); pg.click('.viewsub [data-tab="exam"]')
    F("the hand-in / audit zip button is at the top of the Exam view, above the student details", pg.evaluate("(()=>{const z=document.getElementById('xeauditzip'),i=document.querySelector('#xesno');return z&&z.getBoundingClientRect().top<i.getBoundingClientRect().top&&document.querySelectorAll('#xeauditzip').length===1})()"))
    pg.uncheck("#xetimeron"); pg.fill("#xesno", "20210001"); pg.fill("#xesname", "Test"); pg.fill("#xessur", "Student")
    for t in range(8):
        pg.fill("#xecode", ""); pg.click("#xestart"); pg.wait_for_selector("#xefinish", timeout=120000)
        if pg.locator("#xeout ol.exlines").count(): break
        pg.click("#xefinish"); pg.wait_for_selector("#xelock", timeout=60000)
    ol = pg.locator("#xeout ol.exlines").first; order = lambda: ol.evaluate("o=>[...o.children].map(l=>l.querySelector('code').dataset.l).join(',')")
    start = order(); ol.locator("li").first.scroll_into_view_if_needed()
    g0 = ol.locator(".exgrip").nth(0).bounding_box(); last = ol.locator("li").last.bounding_box()
    pg.mouse.move(g0["x"] + 8, g0["y"] + 8); pg.mouse.down(); pg.mouse.move(g0["x"] + 8, last["y"] + last["height"] - 2, steps=12); pg.mouse.up()
    d = order().split(","); F("a line is dragged by its handle all the way to the bottom", d[-1] == start.split(",")[0] and len(d) == len(start.split(",")), "%s -> %s" % (start, order()))
    btn = ol.locator("li").last.locator('[data-exmv="-1"]').bounding_box(); before_last = order().split(",")[-1]
    pg.mouse.move(btn["x"] + 6, btn["y"] + 6); pg.mouse.down(); pg.wait_for_timeout(1800); pg.mouse.up(); pg.wait_for_timeout(300)
    F("holding the up arrow keeps the line moving until it reaches the top", order().split(",")[0] == before_last, order())
    one = order(); b2 = ol.locator("li").nth(2).locator('[data-exmv="-1"]'); b2.click(); two = order()
    F("a single click on an arrow still moves exactly one place", sum(a != b for a, b in zip(one.split(","), two.split(","))) == 2, "%s -> %s" % (one, two))
    ol.locator(".exgrip").nth(1).focus(); k0 = order(); pg.keyboard.press("ArrowDown"); k1 = order(); pg.keyboard.press("Home"); k2 = order()
    F("on the handle, Down moves the line one place and Home sends it to the first", k0 != k1 and k2.split(",")[0] == k1.split(",")[2], "%s %s %s" % (k0, k1, k2))
    F("the page's errors are empty", not errs, str(errs[:2]))
json.dump(res, open(os.path.join(REPO, "08-tooling", "ch%s-page" % NN, "interaction_test_results_v1_0_0.json"), "w"), indent=1)
print("interaction test: %d pass, %d fail" % (sum(res.values()), len(res) - sum(res.values())))
