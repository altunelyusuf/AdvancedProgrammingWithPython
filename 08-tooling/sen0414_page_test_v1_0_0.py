#!/usr/bin/env python3
"""Design tests and Stage 4 browser gates for a SEN0414 chapter page, in a real headless browser.
Every widget is exercised and must show exactly what its build record says Python printed.
Writes the per-widget results that the page ABox then records - a widget is marked tested only if it passed."""
import json, os, sys
from playwright.sync_api import sync_playwright
N = sys.argv[1]; REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page_path = os.path.join(REPO, "03-materials", "ch%s" % N, "page", "sen0414_ch%s_page_v1_0_0.html" % N)
page_path = os.environ.get("PAGE", page_path)  # a fixture can be tested in place of the page
rec = json.load(open(os.path.join(REPO, "08-tooling", "ch%s-page" % N, "build_record.json")))
AXE = "/home/claude/Ontologies/rdodi-ecosystem/07-pedagogy-professional-stage/lib/axe.min.js"
res = {"widgets": {}, "gates": {}}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); errors = []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None); pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto("file://" + page_path)
    for w in rec["widgets"]:
        i = w["id"]; ok = False; why = ""
        try:
            if w["kind"] in ("predict", "toggle"):
                pg.fill("#%s-guess" % i, w["out"]); pg.click('[data-run="%s"]' % i)
                shown = pg.text_content("#%s-out" % i).strip(); verdict = pg.text_content("#%s-verdict" % i)
                ok = shown == w["out"] and "matched" in verdict; why = "shows %r" % shown
                if ok and w["kind"] == "toggle":
                    pg.click('[data-toggle="%s"]' % i); pg.click('[data-run="%s"]' % i)
                    ok = pg.text_content("#%s-out" % i).strip() == w["alt_out"]; why += "; toggled shows %r" % pg.text_content("#%s-out" % i).strip()
                if ok and "err_expr" in w:
                    pg.click('[data-err="%s"]' % i); ok = pg.is_visible("#%s-err" % i) and pg.text_content("#%s-err" % i).strip() == w["err_out"]; why += "; error shown"
            elif w["kind"] == "steps":
                pg.click('[data-step="%s"]' % i); ok = pg.locator("#%s li" % i).nth(1).is_visible(); why = "second step revealed"
            else:
                pg.locator("#%s .chip" % i).first.click(); d = pg.text_content("#%s-detail" % i)
                ok = d.strip() == w["items"][0][1].strip(); why = "detail shows the first kind's definition"
        except Exception as e:
            ok, why = False, "%s: %s" % (type(e).__name__, str(e)[:80])
        res["widgets"][i] = {"passed": ok, "detail": why}
    fs = pg.locator("#quiz fieldset")
    qok = True
    for k in range(fs.count()):
        f = fs.nth(k); ans = int(f.get_attribute("data-answer")); f.locator("input").nth(ans).check(); f.locator("button").click()
        qok &= pg.text_content("#q%d-fb" % k).strip() == "Correct."
    res["gates"]["quiz"] = qok
    res["gates"]["Stage4.C console errors"] = len(errors)
    res["gates"]["Stage4.D dialogs"] = pg.locator('[role="dialog"]').count() + pg.locator("dialog").count()
    res["gates"]["Stage4.E sections"] = pg.locator("main section[data-source]").count()
    m = b.new_page(viewport={"width": 390, "height": 844}); m.goto("file://" + page_path)
    links = m.locator("nav.groups a"); vis = [links.nth(k).is_visible() for k in range(links.count())]
    res["gates"]["Stage4.F nav visible on mobile without clicks"] = all(vis) and len(vis) > 0
    pg.add_script_tag(path=AXE)
    ax = pg.evaluate("async () => { const r = await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa']}}); return r.violations.map(v => [v.id, v.impact, v.nodes.length]); }")
    res["gates"]["WCAG 2 AA violations (axe-core)"] = ax
    b.close()
json.dump(res, open(os.environ.get("RESULTS", os.path.join(REPO, "08-tooling", "ch%s-page" % N, "test_results.json")), "w"), indent=1)
bad = [k for k, v in res["widgets"].items() if not v["passed"]]
print("widgets: %d tested, %d passed; failing: %s" % (len(res["widgets"]), len(res["widgets"]) - len(bad), bad[:5]))
for k, v in res["gates"].items(): print("  %-48s %s" % (k, v))
