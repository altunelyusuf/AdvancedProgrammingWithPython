#!/usr/bin/env python3
"""Browser test of the 9.22.0 and 9.23.0 interaction changes on a chapter page: no code-pattern list in any editor, every Code Lab example runs, the live-model bar is at the top of the Agents view,
multiple choice without "None of the above" and the multiple-answer type (select all that apply, partial credit); the input row (shown only when the code calls input(), with values that fit); concept text as paragraphs, ordering lines by dragging, by holding the arrows and by keyboard, the hand-in zip button at the top of the Exam view.
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
    pg.click("#groups >> text=Lab"); pg.click('.viewsub [data-tab="codelab"] >> visible=true')
    F("no 'Code patterns' list in any editor (the Playground keeps its single list)", pg.locator("[data-edtpl]").count() == 0 and pg.locator("#pex optgroup").count() == 2)
    n = pg.locator("#clsnip option").count(); outs = []
    for i in range(n):
        pg.select_option("#clsnip", str(i)); pg.click("#clrun"); pg.wait_for_function("()=>{const t=document.getElementById('clout').textContent.trim();return t.length>0&&!/running/.test(t)}", timeout=90000); outs.append(pg.text_content("#clout").strip())
    F("every Code Lab example runs without an error", n >= 5 and not any("Error" in o[:40] for o in outs), "%d examples" % n)
    F("the first Code Lab examples need only the chapter (no import, no def) and the others say 'Advanced'", all("import" not in pg.evaluate("CODELAB_SNIPPETS[%d][1]" % i) and "def " not in pg.evaluate("CODELAB_SNIPPETS[%d][1]" % i) for i in range(4)) and sum("Advanced" in pg.evaluate("CODELAB_SNIPPETS[%d][0]" % i) for i in range(n)) >= 3)
    pg.click("#groups >> text=Agents")
    F("Enable live LLM and the model choice are at the top of the Agents view", pg.evaluate("(()=>{const k=document.querySelector('[data-pane=agents] .kit'),a=document.querySelector('[data-pane=agents] .agentsview');return !!k&&k.getBoundingClientRect().top<a.getBoundingClientRect().top&&!!k.querySelector('#llmbtn')})()"))
    # multiple choice: no 'None/All of the above'; the multiple-answer type
    r = pg.evaluate("""async()=>{let bad=[],tot=0,gen=0;for(let sd=1;sd<=60;sd++){const its=(await xExamBuild('M',sd)).filter(i=>i.type==='mcq');for(const it of its){tot++;if(it.options.some(o=>/^(none|all) of the above/i.test(o)))gen++;
        const a=await xMark(it,it.answer),w=await xMark(it,(it.answer+1)%it.options.length);if(a.score!==1||w.score>=1)bad.push('mark:'+it.q)}}return {tot,gen,bad:bad.slice(0,3)}}""")
    F("multiple choice has no 'None of the above' or 'All of the above' option; right scores 1, wrong scores 0", r["tot"] > 100 and r["gen"] == 0 and not r["bad"], str(r))
    r = pg.evaluate("""async()=>{let m=0,f=0,sizes=new Set(),ks=new Set(),bad=[],seen=new Set(),rep=0;for(let sd=1;sd<=40;sd++){for(const k of ['M','F']){const its=await xExamBuild(k,sd);const mu=its.filter(i=>i.type==='multi');if(k==='M')m+=mu.length;else f+=mu.length;
        for(const it of mu){sizes.add(it.options.length);ks.add(it.answer.length);const key=xFp(it);if(seen.has(key))rep++;seen.add(key);
          if(it.options.some(o=>/^(none|all) of the above/i.test(o)))bad.push('none/all');
          const full=await xMark(it,it.answer.slice()),one=it.answer.length>1?await xMark(it,it.answer.slice(1)):{score:0.5},wrongTick=await xMark(it,it.answer.concat([[...it.options.keys()].find(j=>!it.answer.includes(j))])),none=await xMark(it,[]),all=await xMark(it,[...it.options.keys()]);
          if(full.score!==1)bad.push('full');if(!(one.score>0&&one.score<1))bad.push('partial '+one.score);if(!(wrongTick.score<1))bad.push('tick');if(none.score!==0)bad.push('none');if(all.score>=1)bad.push('all')}}}
        return {m,f,sizes:[...sizes],ks:[...ks],bad:bad.slice(0,5),rep}}""")
    F("each Midterm-style and Final-style exam carries multiple-answer questions: five statements, two or three right; full marks only for exactly the right set, partial credit, a wrong tick costs, none scores 0", r["m"] >= 40 and r["f"] >= 40 and r["sizes"] == [5] and set(r["ks"]) <= {2, 3} and not r["bad"], str(r))
    # one multiple-answer question in the practice builder: tick, check, show the answer
    pg.click("#groups >> text=Practice"); pg.click('.viewsub [data-tab="qtypes"] >> visible=true'); pg.select_option("#xdtype", "multi"); pg.click("#xdnew"); pg.wait_for_selector("#xdout input[type=checkbox]", timeout=60000)
    nb = pg.locator("#xdout input[type=checkbox]").count(); ans = pg.evaluate("document.querySelector('#xdout fieldset').xit.answer")
    for j in ans: pg.locator("#xdout input[type=checkbox]").nth(j).check()
    pg.click("#xdout [data-xcheck]"); pg.wait_for_selector("#xdout .xmsg", timeout=20000)
    F("a multiple-answer question is ticked and checked in the practice builder (checkboxes, full marks for the right set)", nb == 5 and "Correct" in pg.text_content("#xdout .xmsg") and "(2 of 2)" in pg.text_content("#xdout .xmsg"), pg.text_content("#xdout .xmsg")[:120])
    pg.click("#xdout [data-xshow]"); F("Show the answer names the statements that fit", "describe" in pg.text_content("#xdout .xfeed"), pg.text_content("#xdout .xfeed")[:100])
    # input row
    pg.click("#groups >> text=Lab"); pg.click('.viewsub [data-tab="play"] >> visible=true'); pg.wait_for_timeout(700)
    vis = lambda sel: pg.evaluate("s=>{const e=document.querySelector(s);return !!e&&!e.hidden&&(getComputedStyle(e).display==='contents'||e.getClientRects().length>0)}", sel)
    F("Playground: the course's own program calls input(), so its input row is shown with its two lines", vis("#pinbox") and not vis("#pinnone") and pg.input_value("#pin") == "Ayse|20", pg.input_value("#pin"))
    def setcode(cid, code):
        pg.evaluate("([i,c])=>{const t=document.getElementById(i);t.value=c;t.dispatchEvent(new Event('input',{bubbles:true}))}", [cid, code]); pg.wait_for_timeout(700)
    setcode("pcode", "print(2 + 3)")
    F("Playground: a program without input() hides the input row and says that no input is needed", not vis("#pinbox") and vis("#pinnone") and "does not call input()" in pg.text_content("#pinnone") and pg.input_value("#pin") == "", pg.text_content("#pinnone"))
    cases = [("n = int(input('How many? '))\nprint(n * 2)", "3"), ("name = input('Name: ')\nprint('Hi', name)", "Ayse"), ("t = float(input('Temperature? '))\nprint(t)", "21.5"),
             ("for i in range(2):\n    x = input()\n    print(x)", "hello|hello|hello"), ("age = int(input('Your age? '))\nprint(age + 1)", "20"), ("# input() is only mentioned here\nprint('input(x)')", None)]
    ok = True; det = []
    for code, want in cases:
        code = code.replace("\\n", "\n"); setcode("pcode", code); got = pg.input_value("#pin") if vis("#pinbox") else None; det.append((want, got)); ok = ok and got == want
    F("Playground: suggested input values fit the calls (a whole number where int() wraps input, a decimal for float(), a name for a name, more lines inside a loop; mentions in a comment or a string are not calls)", ok, str(det))
    setcode("pcode", "name = input('Name: ')\nprint('Hi', name)".replace("\\n", "\n")); pg.fill("#pin", "Zeynep"); pg.wait_for_timeout(800)
    F("Playground: a value the learner typed is kept while the code stays the same", pg.input_value("#pin") == "Zeynep")
    pg.click("#prun"); pg.wait_for_function("()=>{const t=document.getElementById('pout').textContent.trim();return t.length>0&&!/running/.test(t)}", timeout=90000)
    F("Playground: the program runs with the suggested/typed input", "Hi Zeynep" in pg.text_content("#pout"), pg.text_content("#pout"))
    setcode("pcode", "age = int(input('Your age? '))\nprint(age + 1)".replace("\\n", "\n")); pg.click("#prun"); pg.wait_for_function("()=>{const t=document.getElementById('pout').textContent.trim();return t.length>0&&!/running/.test(t)}", timeout=90000)
    F("Playground: a program that needs a number runs with the suggested number", pg.text_content("#pout").strip().endswith("21"), pg.text_content("#pout"))
    pg.click("#groups >> text=Lab"); pg.click('.viewsub [data-tab="trace"] >> visible=true'); pg.wait_for_timeout(700)
    F("Step through: the sum program needs no input, so no input row is shown, only a note", not vis("#trinbox") and vis("#trinnone"))
    setcode("trcode", "name = input('Name: ')\nprint(name)".replace("\\n", "\n"))
    F("Step through: a program that calls input() shows the row with a suggested name", vis("#trinbox") and not vis("#trinnone") and pg.input_value("#trin") == "Ayse", pg.input_value("#trin"))
    pg.click("#trnext"); pg.wait_for_function("()=>/steps/.test(document.getElementById('trstat').textContent)", timeout=60000)
    F("Step through: the trace runs with the suggested input and ends without an error", "Error" not in pg.text_content("#trstat"), pg.text_content("#trstat"))
    # paragraphs
    pg.evaluate("showTab('Value')") if False else None
    r = pg.evaluate("""()=>{const n=D.nodes.find(x=>x.id==='CPython');const leaves=D.nodes.filter(x=>x.level===3);return {np:n.paras.length,facets:n.paras.map(p=>p.facet),minLeaf:Math.min(...leaves.map(x=>x.paras.length)),all:D.nodes.every(x=>x.paras&&x.paras.length>=3),html:bodyHtml(n),count:D.nodes.length}}""")
    F("every concept is written as at least three full paragraphs; none opens with a printed question label; CPython's paragraphs cover what, why, where and how", r["all"] and r["minLeaf"] >= 4 and all(f == "" for f in r["facets"]) and r["html"].count('<p class="bp">') == r["np"] and r["html"].count('class="facet"') == 0 and "What it is:" not in r["html"], str({k: r[k] for k in ("np", "facets", "minLeaf", "count")}))
    txt = pg.evaluate("document.body.innerText")
    F("the page explains CPython: the term is a concept of its own and its definition is on the page", "canonical implementation of the Python programming language" in pg.evaluate("D.nodes.find(x=>x.id==='CPython').paras[0].text"))
    pg.click("#groups >> text=Practice"); pg.click('.viewsub [data-tab="exam"] >> visible=true')
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
