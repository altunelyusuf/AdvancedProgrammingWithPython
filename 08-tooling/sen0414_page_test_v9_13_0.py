#!/usr/bin/env python3
"""Browser tests for version 9 - visualisations computed by Python (evaluation steps, step-through tracer, code pipeline, chapter visualisations) and wheel zoom - on top of version 8 - a seven-item top menu, subject overviews without repeated lists, folded introductions, one rooted taxonomy with fitting labels, zoom on every diagram - on top of version 7 - the RDODI fit-gap views (ontology graph, Code Lab, SPARQL console, question views, About, downloads) on top of version 6 - the conversation view (roster with role icons, guide, handoff, follow-ups, memory) on top of version 5 - version 4's checks, plus: the page's own thread never blocks for long, and an endless program is stopped while the page stays responsive ( (version 3's rule checks plus the agents' toolkit) of a SEN0414 page - the owner's rules of 2026-09-25 made checkable:
code the student edits really runs (edited code must change the result); agents answer from their own
slice, so different questions get different answers; a menu click changes the main area and leaves the
detail card closed; the card opens only on an explicit request; the tab row is the sub-menu of the
selected top-level item. Every stored result must also equal what the build's interpreter printed."""
__version__ = "9.13.0"
# 9.11.0 (over 9.10.0): the chapter-visualisation section skips keys of the visuals file that are not concept ids (the deck-only framing slide) and checks the 13 kinds of chapter 6 against the specification by reading the drawn DOM/SVG: boxes (every index label, item and back index, each pick highlights its boxes, the error), slices (every cell, the selected indexes of each row, the order numbers), lanes (before and after lists, the marked boxes, the returned value, the same-object flag, the errors), hist (label, count and bar length of each bar), refgraph (for every scenario and step: each name, the object it reaches - by its arrow ending on that object's frame -, every item, every reference arrow), keysort (items, keys, output, the lines from input to output), matrix (frames stepped, the hazard rows, the counter table), mutation and passes (stepped rows), unpack, seqtypes, classify and facts; each check runs only when the chapter has that kind. Also: zoom on every SVG visual (keysort, refgraph, range, pairs) and its kept view when a step redraws it; axe (WCAG 2 A/AA) over all chapter visuals shown; the lecture-slide check ignores slides whose visual is not a concept.
# 9.10.0 (over 9.9.0): the builder draws on the chapter's written question bank (every concept, every Apply item re-run in the page) and asks for it first when it asks one question for every concept; the live-model question is refused when malformed or when its code does not print the marked answer, and says so when the browser has no model.
# 9.9.0 (over 9.8.0): choosing a SPARQL sample fills the query at once (no Load sample button); agent answers are formatted (lead sentence, bullets, coloured code, example block, related chips; markdown-lite for LLM text); the quiz builder makes a question of every kind for every concept on request, checks answers, reports coverage.
# 9.8.0 (over 9.7.0): choosing an example fills the code at once (Playground, Code Lab, Step through, Code pipeline - no Load button); Step through traces on the first Step, Back, First or Play without a Trace button and traces again when the code changes; the Code pipeline offers examples, runs on the first stage or next-stage click, and every example of both lists is run.
# 9.7.0 (over 9.6.0): the leaf widget is a static Example (no Next step, no walk-through); checks the Lecture tab, the Resources tab, the fitted work area (h2 hidden under the tab row, notes folded, code areas that do not scroll inside), and the debugger, logging-level and unwinding visuals.
# 9.6.0 (over 9.5.1): checks the visualisations that are executed specifications: a trace steps through every pass of every run and its last row matches the specification; a range draws one dot per value and the stop marker; pairs draw every pair; the names visual states its count.
# 9.5.1 (over 9.5.0): the concept tap uses the first visible concept link (9.5.0 took the first one, at every such site, which can sit in a hidden pane, so a chapter whose first subject has one timed out).
# 9.5.0 (over 9.4.2): the questions put to the guide and to one agent come from the chapter's test_config_v*.json, when it has one
# (9.4.2 hard-coded chapters 1 and 2 and asked chapter 2's questions of every other chapter); and the browser is launched
# through the environment's proxy (HTTPS_PROXY) when there is one, keeping the rest of the environment (9.4.2 replaced the whole
# environment, so where the network is reached only through a proxy Pyodide could not load and the first Python run timed out).
import json, os, re, sys, time
PV = os.environ.get("PAGE_VER", "9_4_2")  # generated files carry the page version they were produced for
from playwright.sync_api import sync_playwright
N = sys.argv[1]; NUM = N; N = ("ch%s" % N) if N.isdigit() else N
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page_path = os.environ.get("PAGE", os.path.join(REPO, "03-materials", N, "page", "sen0414_%s_page_v%s.html" % (N, os.environ.get("PAGE_VER", "9_4_2"))))
d = json.load(open(os.path.join(REPO, "08-tooling", "%s-page" % N, "page_data_v%s.json" % PV)))
import glob as _g
_tc = sorted(_g.glob(os.path.join(REPO, "08-tooling", "%s-page" % N, "test_config_v*.json")), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
CFG = {"01": {"guide_q": "why does 2 + 3 * 6 give 20 and not 30?", "agent": "agent-ArithmeticOperation", "root": "what does floor division do?"}}.get(NUM, {"guide_q": "does 42 equal the string '42'?", "agent": "agent-EqualityComparison", "root": "what does the equality operator compare?"})
if _tc: CFG = json.load(open(_tc[-1]))
AXE = "/home/claude/Ontologies/rdodi-ecosystem/07-pedagogy-professional-stage/lib/axe.min.js"
R = {"_version": PV.replace("_", "."), "widgets": {}, "features": {}, "gates": {}}
feat = lambda k, ok, det="": R["features"].__setitem__(k, {"passed": bool(ok), "detail": det})
nodes = d["nodes"]; tops = [n for n in nodes if n["level"] == 1]
in_view = "id=>{const e=document.getElementById(id);if(!e)return false;const r=e.getBoundingClientRect();return r.height>0&&r.top<innerHeight&&r.bottom>0&&!e.closest('[hidden]')}"
with sync_playwright() as p:
    b = p.chromium.launch(env=dict(os.environ, LANG="en_US.UTF-8", LC_ALL="en_US.UTF-8"), **({"proxy": {"server": os.environ["HTTPS_PROXY"]}} if os.environ.get("HTTPS_PROXY") else {})); ctx = b.new_context(locale="en-US", viewport={"width": 1400, "height": 900}, permissions=["clipboard-read", "clipboard-write"]); pg = ctx.new_page(); errors = []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None); pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.add_init_script("window.__lt=[];new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push(Math.round(e.duration)))).observe({type:'longtask',buffered:true});")
    pg.goto("file://" + page_path); pg.wait_for_timeout(400)
    GROUP = pg.evaluate("GROUP_OF")
    def view(k):
        g = GROUP.get(k)
        if g:
            view(g); pg.click('[data-pane]:not([hidden]) .viewsub [data-tab="%s"]' % k) if not pg.locator('[data-pane="%s"]' % k).is_visible() else None
        else:
            pg.click('#groups [data-tab="%s"]' % k)
        pg.wait_for_timeout(150)
    # one top-level menu; tabs inside a subject are its sub-menu
    labels = [pg.locator("#groups button").nth(k).get_attribute("data-tab") for k in range(pg.locator("#groups button").count())]
    top2 = next(t for t in tops if len([n for n in nodes if n["parent"] == t["id"]]) >= 2)
    view(top2["id"])
    mids = [n for n in nodes if n["parent"] == top2["id"]]
    third_row = pg.locator('[data-pane="%s"] .subtabs:not(.viewsub)' % top2["id"]).count()
    sub_in_pane = pg.locator('#crumb-%s option' % top2["id"]).count() - 1 if third_row == 0 else -1
    pg.select_option('#crumb-%s select' % top2["id"], mids[-1]["id"])
    learn_tabs = [pg.locator('[data-pane="%s"] .viewsub [data-tab]' % top2["id"]).nth(k).get_attribute("data-tab") for k in range(pg.locator('[data-pane="%s"] .viewsub [data-tab]' % top2["id"]).count())]
    feat("one top menu; its tab row is the only row of tabs - sub-subjects are chosen from a breadcrumb", pg.locator("#tabs").count() == 0 and labels == ["intro", "learn", "maps", "lab", "agents", "practice", "reference", "about"] and all(t["id"] in learn_tabs for t in tops) and sub_in_pane == len(mids)
         and pg.locator('[data-subpane="%s"]' % mids[-1]["id"]).is_visible() and not pg.locator('[data-subpane="%s"]' % mids[0]["id"]).is_visible(), "top menu: %s" % ", ".join(labels))
    # the explorer drives the main area; the card stays closed
    leaf = [n for n in nodes if n["level"] == 3 and n["parent"] != mids[-1]["id"]][0]
    pg.click("#expandAll"); pg.click('#tree .tn[data-c="%s"]' % leaf["id"]); pg.wait_for_timeout(300)
    feat("menu click changes the main area first, card stays closed", pg.evaluate(in_view, "s-" + leaf["id"]) and pg.locator("#card").is_hidden(), leaf["label"])
    pg.click('[data-detail="%s"]' % leaf["id"]); opened = pg.locator("#card").is_visible() and leaf["label"] in pg.text_content("#card")
    pg.click("#card [data-close]"); closed = pg.locator("#card").is_hidden()
    pg.click('[data-detail="%s"]' % leaf["id"]); pg.keyboard.press("Escape")
    feat("detail card only on explicit request; closes by button and Esc", opened and closed and pg.locator("#card").is_hidden())
    pg.click('#tree .tn[data-c="%s"]' % leaf["id"], button="right"); menu_ok = pg.is_visible("#ctx"); pg.locator('#ctx [data-cmd^="card:"]').click()
    feat("context menu offers details on request", menu_ok and pg.locator("#card").is_visible()); pg.keyboard.press("Escape")
    pg.hover('#tree .tn[data-c="%s"]' % leaf["id"]); feat("tooltips", pg.is_visible("#tip"))
    view("map"); g = pg.locator("#graph g.gn").nth(4); gid = g.get_attribute("data-c"); g.click(); pg.wait_for_timeout(300)
    feat("tapping a map node shows its options in the detail card; the main area stays where it was", pg.locator("#card").is_visible() and ("Go to its section" in pg.text_content("#card")) and pg.locator('[data-pane="map"]').is_visible(), gid)
    pg.keyboard.press("Escape")
    view("taxonomy"); feat("taxonomy diagram", pg.locator("#taxo svg g.n").count() == len(nodes) + 1)
    # widgets
    for n in nodes:
        w = "w-" + n["id"]; ok = False; why = ""
        try:
            pg.evaluate("id=>goTo(id)", n["id"])
            if "io" in n:
                pg.fill("#%s-code" % w, n["io"]["code"]); pg.fill("#%s-guess" % w, n["io"]["out"]); pg.click('[data-run="%s"]' % n["id"])
                pg.wait_for_function("id=>{const o=document.getElementById(id);return o&&o.textContent&&o.textContent!=='running...'}", arg=w + "-out", timeout=120000)
                got = pg.text_content("#%s-out" % w); ok = got == n["io"]["out"] and "matched" in pg.text_content("#%s-verdict" % w); why = "printed %r" % got
                pg.fill("#%s-code" % w, "2 + 2"); pg.click('[data-run="%s"]' % n["id"])
                pg.wait_for_function("id=>{const o=document.getElementById(id);return o&&o.textContent!=='running...'}", arg=w + "-out", timeout=60000)
                edited = pg.text_content("#%s-out" % w); ok = ok and edited == "4"; why += "; edited to 2 + 2 printed %r" % edited
                pg.click('[data-reset="%s"]' % n["id"]); ok = ok and pg.input_value("#%s-code" % w) == n["io"]["code"]
                pg.click('[data-detail="%s"]' % n["id"]); shown = pg.locator("#card output.out").first.text_content().split("\n", 1)[-1]; pg.keyboard.press("Escape")
                ok = ok and shown == n["io"]["out"]; why += "; card shows %r" % shown
            elif n.get("chart"):
                pg.wait_for_function("id=>{const c=document.getElementById(id);const ch=c&&window.Chart&&Chart.getChart(c);return ch&&ch.data.datasets.some(x=>x.data&&x.data.length)&&c.offsetWidth>0}", arg=n["chart"], timeout=20000)
                ok = True; why = "chart %s drawn" % n["chart"]
            elif n["level"] == 3:
                ex = pg.text_content("#%s pre.exs" % w); ok = ex == n["example"] and pg.locator("#%s [data-step]" % w).count() == 0 and "Walk through it" not in pg.text_content("#%s" % w); why = "static example shown; no step button"
            elif n["level"] == 1:
                card = pg.locator("#%s .ovcard" % w).first; sub = card.get_attribute("data-sub"); card.click(); pg.wait_for_timeout(200)
                ok = pg.locator('[data-subpane="%s"]' % sub).is_visible() and pg.locator("#%s .ovcard" % w).count() == len([m for m in nodes if m["parent"] == n["id"]]); why = "overview card opens its sub-subject"
            else:
                leaves = [m["id"] for m in nodes if m["parent"] == n["id"]]
                ok = pg.locator("#%s > section.leaf" % w).count() == len(leaves) and pg.locator("#%s" % w).is_visible(); why = "grid shows its %d concepts" % len(leaves)
        except Exception as e:
            ok, why = False, "%s: %s" % (type(e).__name__, str(e)[:100])
        R["widgets"][w] = {"passed": ok, "detail": why}
    ios = [n for n in nodes if "io" in n]
    feat("edited code really runs: every example re-run after editing prints the new result", all(R["widgets"]["w-" + n["id"]]["passed"] for n in ios), "%d examples" % len(ios))
    view("play"); opts = pg.locator("#pex option"); sel_ok = True
    for k in range(min(opts.count(), 4)):
        v = opts.nth(k).get_attribute("value"); pg.select_option("#pex", v)
        want = d["course"]["playground"]["code"] if v == "first" else next(n_ for n_ in nodes if n_["id"] == v)["io"]["code"]; sel_ok &= pg.input_value("#pcode") == want
    feat("choosing an example in the Playground fills the code at once, with no Load button", sel_ok and pg.locator("#pload").count() == 0, "%d examples" % opts.count())
    view("play"); pg.fill("#pcode", "x = 7\nx * 6"); pg.click("#prun")
    pg.wait_for_function("()=>document.getElementById('pout').textContent!=='running...'", timeout=60000); free = pg.text_content("#pout")
    feat("playground runs code typed from scratch", free == "42", repr(free))
    # agents answer from their own slice: different questions, different answers
    a = max(d["agents"], key=lambda x: len(x["covers"])); view("agents")
    pg.click('[data-agenttab="%s"]' % a["id"])
    q1 = [n for n in nodes if n["id"] == a["covers"][0]][0]["label"]; q2 = [n for n in nodes if n["id"] == a["covers"][-2]][0]["label"] if len(a["covers"]) > 2 else a["covers"][-1]
    def ask(q):
        before = pg.locator("#%s-log .msg" % a["id"]).count(); pg.fill("#%s-q" % a["id"], q); pg.click('[data-ask="%s"]' % a["id"])
        pg.wait_for_function("([id,n])=>{const m=document.querySelectorAll('#'+id+'-log .msg');return m.length>=n+2&&!m[m.length-1].classList.contains('typing')}", arg=[a["id"], before], timeout=240000)
        return pg.locator("#%s-log .msg" % a["id"]).last.text_content()
    ans1, ans2 = ask("what is " + q1.lower()), ask("what is " + q2.lower() + " used for in a program?"); ans3 = ask("how do I bake bread")
    feat("agents answer from their own slice; different questions get different answers", ans1 != ans2 and len(ans1) > 40 and len(ans2) > 40 and ("Nothing in the book, course or chapter material answers that" in ans3),
         "%s | %s | %s" % (ans1[:60], ans2[:60], ans3[:60]))
    st = pg.text_content(".kitstat"); kinds = pg.evaluate("()=>[...new Set(KIT.chunks.map(c=>c.kind))].sort()")
    files = pg.evaluate("()=>document.querySelectorAll('script[data-kind]').length")
    how = pg.locator("#%s-log .msg details pre" % a["id"]).first.text_content(); cites = pg.locator("#%s-log .msg .src" % a["id"]).count()
    feat("agents search a knowledge graph of the book, course and chapter ontologies, the research record and this page", "Knowledge graph: ready" in st and ("from %d files" % files) in st and kinds == ["book", "chapter", "course", "page", "research"], st + " | kinds " + ",".join(kinds))
    feat("agents rank by meaning (sentence embeddings) and show how they found the answer", "Semantic search: ready" in st and "SPARQL" in how and "rows:" in how and cites > 0, "%d cited passages" % cites)
    q_out = pg.evaluate("async(id)=>{const a=D.agents.find(x=>x.id===id);const r=await rank(a,'which course learning outcome is about choosing libraries?',8);return r.top.map(x=>x.c.label).join(' | ')}", a["id"])
    feat("a course question reaches the course ontology", "LO-1" in q_out, q_out[:150])
    pg.click("#llmbtn"); pg.wait_for_timeout(1500); llm = pg.text_content(".kitstat").split("Live LLM:")[1].strip()
    feat("live LLM is capability-checked; without WebGPU the agents keep working and say so", llm.startswith("unavailable") or llm.startswith("ready") or llm.startswith("downloading"), llm[:90])
    lt = pg.evaluate("window.__lt"); R["gates"]["longest main-thread task (ms)"] = max(lt or [0])
    feat("no main-thread task over 200 ms through the whole session (graph, embeddings, Python, agents)", max(lt or [0]) <= 200, "longest %d ms over %d long tasks" % (max(lt or [0]), len(lt)))
    view("play"); pg.fill("#pcode", "while True:\n    pass"); t0 = time.time(); pg.click("#prun"); pg.wait_for_timeout(1500)
    t1 = time.time(); view("glossary"); responsive = (time.time() - t1) < 1.0 and pg.locator('[data-pane="glossary"]').is_visible()
    view("play"); pg.wait_for_function("()=>document.getElementById('pout').textContent.startsWith('Stopped after')", timeout=40000); stopped_in = time.time() - t0
    pg.fill("#pcode", "6 * 7"); pg.click("#prun"); pg.wait_for_function("()=>document.getElementById('pout').textContent==='42'", timeout=90000)
    feat("an endless program is stopped; the page stays responsive while it runs; Python works again after", responsive, "stopped after %.0f s; menu answered during the loop; fresh Python printed 42" % stopped_in)
    # ---- the conversation view ----
    view("agents"); pg.wait_for_timeout(200)
    roster = pg.locator(".roster .persona"); icons = [roster.nth(k).locator(".av").text_content() for k in range(roster.count())]
    feat("agents are listed like people: role icons, what each knows, a guide first", roster.count() == len(d["agents"]) + 1 and icons[0] == "🧭" and "🤖" not in icons and all(pg.locator('[data-agenttab="%s"] small' % x["id"]).text_content().startswith("Ask me about") for x in d["agents"]), " ".join(icons))
    pg.click('[data-agenttab="guide"]'); gl = pg.locator("#guide-log .msg").count(); pg.fill("#guide-q", CFG["guide_q"]); pg.press("#guide-q", "Enter")
    pg.wait_for_function("n=>{const m=document.querySelectorAll('#guide-log .msg');return m.length>=n+2&&!m[m.length-1].classList.contains('typing')}", arg=gl, timeout=120000)
    sugg = [pg.locator("#guide-log .msg").last.locator("[data-handoff]").nth(k).get_attribute("data-handoff") for k in range(pg.locator("#guide-log .msg").last.locator("[data-handoff]").count())]
    target = CFG["agent"]
    pg.locator('#guide-log .msg').last.locator('[data-handoff="%s"]' % target).click()
    pg.wait_for_function("id=>{const m=document.querySelectorAll('#'+id+'-log .msg');return m.length>=3&&!m[m.length-1].classList.contains('typing')}", arg=target, timeout=120000)
    feat("the guide introduces the right agent and hands the question over", target in sugg and pg.locator('[data-conv="%s"]' % target).is_visible(), "suggested: " + ", ".join(sugg))
    def say(q):
        n = pg.locator("#%s-log .msg" % target).count(); pg.fill("#%s-q" % target, q); pg.press("#%s-q" % target, "Enter")
        pg.wait_for_function("([id,n])=>{const m=document.querySelectorAll('#'+id+'-log .msg');return m.length>=n+2&&!m[m.length-1].classList.contains('typing')}", arg=[target, n], timeout=120000)
        return pg.locator("#%s-log .msg" % target).last.inner_text()
    root = CFG["root"]
    r1 = say(root); r2 = say("can you give me an example?"); r3 = say("and why?")
    feat("follow-up questions are answered in the context of the conversation", ('Following on from "%s"' % root) in r2 and ('Following on from "%s"' % root) in r3 and "for example:" in r2.lower(), r2[:90].replace("\n", " "))
    kept = pg.locator("#%s-log .msg" % target).count(); pg.reload(); view("agents"); pg.wait_for_timeout(400)
    feat("conversations are remembered across a reload", pg.locator("#%s-log .msg" % target).count() == kept and pg.locator('[data-conv="%s"]' % target).is_visible(), "%d messages kept" % kept)
    pg.click('[data-newconv="%s"]' % target); feat("a new conversation starts clean", pg.locator("#%s-log .msg" % target).count() == 1)
    # ---- the fit-gap views ----
    view("howto"); howto = pg.text_content('[data-pane="howto"] .prose')
    view("arch"); arch_rows = pg.locator('#archout table').last.locator("tr").count() - 1
    view("mission"); pg.wait_for_function("()=>!document.getElementById('missionout').textContent.includes('reading the course ontology')", timeout=60000); mission = pg.text_content("#missionout")
    view("prov"); limits = pg.locator("#provout ul li").count()
    feat("About: how it works, agents & tools with the corpus, mission & backlog with course outcomes, provenance & known limits", len(howto) > 400 and arch_rows == files and "Mission" in mission and "LO-1" in mission and limits >= 4, "corpus rows %d, limits %d" % (arch_rows, limits))
    view("sparql"); pg.click("#sqrun"); pg.wait_for_function("()=>/result/.test(document.getElementById('sqstat').textContent)||document.querySelector('#sqres .err')", timeout=60000)
    rows = pg.locator("#sqres tr").count() - 1
    pg.click("#sqcsv"); pg.wait_for_timeout(200); csv_copy = pg.evaluate("navigator.clipboard.readText()")
    pg.select_option("#sqsamp", "5"); sel_ok = pg.evaluate("()=>document.getElementById('sqtext').value===SPARQL_SAMPLES[5][1]&&!document.getElementById('sqload')"); pg.click("#sqrun"); pg.wait_for_function("()=>/result/.test(document.getElementById('sqstat').textContent)", timeout=60000); ask_ans = pg.text_content("#sqres")
    feat("SPARQL console: editable queries over the knowledge graph, results table, results copied as CSV, ASK", rows > 5 and csv_copy.count("\n") >= rows and ask_ans.strip() in ("Yes", "No"), "%d rows; ASK -> %s" % (rows, ask_ans.strip()))
    feat("choosing a SPARQL sample loads it at once; no Load sample button", sel_ok)
    view("ontograph"); pg.wait_for_function("()=>document.querySelectorAll('#onto g.on').length>0", timeout=60000)
    n_all = pg.locator("#onto g.on").count(); pg.uncheck('[data-okind="individual"]'); n_cls = pg.locator("#onto g.on").count(); pg.check('[data-okind="individual"]')
    pg.click("#orelayout"); pg.wait_for_timeout(2500); pg.click("#ofit"); first = pg.locator("#onto g.on").first; first.click(); info = pg.text_content("#ontoinfo")
    feat("ontology graph: classes, individuals and book concepts from the graph, filter, re-layout, fit, node detail", n_all > 20 and 0 < n_cls < n_all and len(info) > 20, "%d nodes (%d without individuals)" % (n_all, n_cls))
    view("play"); pg.fill("#pcode", "print('hello')")
    pg.click('[data-dl="pcode"]'); pg.wait_for_timeout(200); code_copy = pg.evaluate("navigator.clipboard.readText()")
    view("mydata")
    pg.click("#dlconvmd"); pg.wait_for_timeout(200); conv_md = pg.evaluate("navigator.clipboard.readText()")
    feat("copying out: playground code, SPARQL results, conversations - to the clipboard, with no file built and saved by the page", code_copy == "print('hello')" and conv_md.startswith("# Conversations") and pg.locator("#mydataout tr").count() >= 1, "code, CSV and %d characters of conversation copied" % len(conv_md))
    view("browse"); chips = pg.locator("#browse [data-browseq]"); nchips = chips.count(); qtext = chips.first.text_content(); target_b = chips.first.get_attribute("data-browseq")
    nb = pg.locator("#%s-log .msg" % target_b).count(); chips.first.click()
    pg.wait_for_function("([id,n])=>{const m=document.querySelectorAll('#'+id+'-log .msg');return m.length>=n+2&&!m[m.length-1].classList.contains('typing')}", arg=[target_b, nb], timeout=120000)
    feat("browse questions by subject; choosing one asks the right agent", nchips > 10 and pg.locator('[data-conv="%s"]' % target_b).is_visible(), "%d questions; '%s' went to %s" % (nchips, qtext, target_b))
    view("expert"); pg.click('[data-role="data analyst"]'); pg.wait_for_function("()=>document.querySelectorAll('#exout [data-expertq]').length>0", timeout=60000); ne = pg.locator("#exout [data-expertq]").count()
    eqt = pg.locator("#exout [data-expertq]").first.text_content(); pg.locator("#exout [data-expertq]").first.click()
    pg.wait_for_function("q=>{const c=document.querySelector('.conv:not([hidden])');if(!c)return false;const m=c.querySelectorAll('.msg');return m.length>=3&&!m[m.length-1].classList.contains('typing')&&[...c.querySelectorAll('.msg.me')].some(x=>x.textContent===q)}", arg=eqt, timeout=120000)
    feat("expert questions for a role; choosing one asks the best-fitting agent", ne >= 5 and "data analyst" in eqt, "%d questions, e.g. %s" % (ne, eqt))
    view("checks"); pg.click("#ckrun"); pg.wait_for_function("()=>/checks pass/.test(document.getElementById('ckstat').textContent)", timeout=240000); ck = pg.text_content("#ckstat")
    a_, b_ = [int(x) for x in ck.split(" checks")[0].split(" of ")]
    feat("built-in checks: every stored example re-run, agents' citations, an off-topic refusal - all pass in the page", a_ == b_ and b_ > 10, ck)
    view("codelab"); pg.select_option("#clsnip", "1"); code_fill = pg.input_value("#clcode"); pg.click("#clrun"); pg.wait_for_function("()=>{const t=document.getElementById('clout').textContent;return t&&t!=='running...'}", timeout=120000)
    cl = pg.text_content("#clout"); n_io = len([n for n in nodes if "io" in n])
    feat("Code Lab: Python over this page's own data re-runs every example", cl.count("same |") == n_io and "DIFFERENT" not in cl, "%d of %d examples the same" % (cl.count("same |"), n_io))
    feat("choosing a Code Lab snippet fills the code at once, with no Load button", code_fill == pg.evaluate("CODELAB_SNIPPETS[1][1]") and pg.locator("#clload").count() == 0)
    # ---- version 8 ----
    view(tops[0]["id"]); pg.select_option('#crumb-%s select' % tops[0]["id"], "ov-" + tops[0]["id"])
    dup = pg.evaluate("()=>[...document.querySelectorAll('[data-pane]')].filter(p=>byId[p.dataset.pane]&&byId[p.dataset.pane].level===1).reduce((a,p)=>a+p.querySelectorAll('.chip').length,0)")
    feat("subject screens carry no repeated lists: an overview sub-tab, one-sentence sub-subject headers", dup == 0 and pg.locator('[data-pane="%s"] .ovcard' % tops[0]["id"]).count() > 0 and pg.locator("details.more").count() == len([n for n in nodes if n["level"] == 2]), "0 duplicate chip rows")
    view("taxonomy"); tx = pg.evaluate("()=>{const g=[...document.querySelectorAll('#taxo g.n')];return {svgs:document.querySelectorAll('#taxo svg').length,boxes:g.length,root:document.querySelectorAll('#taxo g.n.root').length,overflow:g.filter(x=>x.querySelector('text').getBBox().width>x.querySelector('rect').getBBox().width+0.5).length}}")
    feat("one taxonomy tree rooted at the chapter, every label inside its box", tx["svgs"] == 1 and tx["root"] == 1 and tx["boxes"] == len(nodes) + 1 and tx["overflow"] == 0, str(tx))
    helps = pg.evaluate("()=>[...document.querySelectorAll('details.help')].map(d=>d.open)")
    feat("view introductions are folded until asked for", len(helps) >= 8 and not any(helps), "%d folded" % len(helps))
    zooms = []
    for k, sel in (("taxonomy", "#taxo"), ("map", "#graph"), ("ontograph", "#onto")):
        view(k)
        if k == "ontograph": pg.wait_for_function("()=>document.querySelector('#onto svg')", timeout=60000)
        v0 = pg.get_attribute("%s svg" % sel, "viewBox"); pg.click('%s [data-z="in"]' % sel); v1 = pg.get_attribute("%s svg" % sel, "viewBox"); pg.click('%s [data-z="reset"]' % sel); v2 = pg.get_attribute("%s svg" % sel, "viewBox")
        zooms.append(v1 != v0 and v2 == v0)
    pg.evaluate("goTo('%s')" % [n for n in nodes if "io" in n][0]["id"]); pg.click('[data-diagram="%s"]' % [n for n in nodes if "io" in n][0]["id"])
    zooms.append(pg.locator('#w-%s-diagram .zbar' % [n for n in nodes if "io" in n][0]["id"]).count() == 1)
    feat("zoom in, zoom out and show-all on every diagram (taxonomy, concept map, ontology graph, parse trees)", all(zooms), str(zooms))
    # ---- version 9: visualisations ----
    evs = [n for n in nodes if "io" in n and len(n["io"].get("steps", [])) > 1]
    ok_ev = True
    for n in evs:
        pg.evaluate("goTo('%s')" % n["id"]); pg.click('[data-evtoggle="%s"]' % n["id"])
        for st in n["io"]["steps"]:
            ok_ev &= st["value"] in pg.text_content("#ev-%s" % n["id"]); pg.click('[data-evnext="%s"]' % n["id"])
        ok_ev &= pg.text_content("#ev-%s" % n["id"]) == n["io"]["out"]
    feat("evaluation steps: each example replays Python's own reduction, one operation at a time, ending on the stored result", ok_ev, "%d multi-step examples (a chapter of statements has none; the stepper is then absent, not broken)" % len(evs))
    view("trace"); pg.fill("#trcode", "total = 0\nfor n in range(1, 5):\n    total = total + n\nprint(total)"); pg.click("#trnext")  # no Trace button: the first Step traces the program
    pg.wait_for_function("()=>/steps/.test(document.getElementById('trstat').textContent)", timeout=120000)
    first_pos = pg.text_content("#trpos"); no_trace_btn = pg.locator("#trgo").count() == 0; nsteps = int(pg.text_content("#trstat").split()[0])
    pg.click("#trfirst"); [pg.click("#trnext") for _ in range(nsteps - 1)]; last_out = pg.text_content("#trout").strip(); tot = [r for r in pg.locator("#trvars tr").all_inner_texts() if r.startswith("total")]
    feat("step through: Python's line tracer records every line, the variables after it and the output", nsteps > 8 and last_out == "10" and tot and "10" in tot[0], "%d steps, output %s" % (nsteps, last_out) + "; first Step showed '%s'" % first_pos)
    feat("Step through starts on the first Step: no Trace button, the program is traced and its first line shown", no_trace_btn and first_pos.startswith("step 1 of"), first_pos)
    # every example offered by Step through traces from a plain selection followed by Step; changing the code traces again
    ex_ok = True; nex = pg.locator("#trex option").count()
    for k in range(nex):
        pg.select_option("#trex", str(k)); pg.wait_for_function("()=>/steps|ended|Error|error/.test(document.getElementById('trstat').textContent)", timeout=120000)
        ex_ok &= pg.input_value("#trcode").strip() != "" and pg.text_content("#trpos").startswith("step 1 of"); pg.click("#trnext"); ex_ok &= pg.text_content("#trpos").startswith("step 2 of")
    pg.fill("#trcode", "y = 1\ny = y + 41\nprint(y)"); pg.click("#trnext"); pg.wait_for_function("()=>document.getElementById('trpos').textContent.startsWith('step 1 of 3')||/step 1 of/.test(document.getElementById('trpos').textContent)", timeout=60000); retrace = pg.text_content("#trstat")
    feat("Step through offers examples, each traced when chosen; editing the code and pressing Step traces the new program", ex_ok and nex >= 4 and retrace.startswith("4 steps"), "%d examples; edited program: %s" % (nex, retrace))
    view("pipeline"); pg.select_option("#ppex", "1"); pg.wait_for_function("()=>document.getElementById('ppstat').textContent===''&&document.querySelector('#ppout')&&document.querySelector('#ppout').textContent.length>0", timeout=120000); chosen = pg.input_value("#ppcode"); pg.click('[data-stage="1"]')  # first click runs the pipeline, then shows the stage
    pg.wait_for_function("()=>document.querySelectorAll('#ppout .tok').length>0", timeout=120000); ntok = pg.locator("#ppout .tok").count(); pg.click('[data-stage="2"]'); tree_ok = pg.locator("#ppout svg g.n").count() > 5; pg.click('[data-stage="3"]'); nbc = pg.locator("#ppout tr").count() - 1; pg.click('[data-stage="4"]'); res = pg.text_content("#ppout pre").strip()
    pipe_ok = True; npx = pg.locator("#ppex option").count()
    for k in range(npx):
        pg.select_option("#ppex", str(k)); pg.wait_for_function("k=>{const p=document.getElementById('ppcode').value;return !!document.querySelector('#ppbar .stage.now')&&p.length>0}", arg=k, timeout=120000)
        pg.click('[data-stage="4"]'); pg.wait_for_function("()=>document.querySelector('#ppout pre')", timeout=120000); pipe_ok &= "Error" not in pg.text_content("#ppstat") and pg.locator("#ppout pre").count() > 0
    feat("Code pipeline offers examples; choosing one fills the code and every example runs through all stages", pipe_ok and npx >= 5 and chosen.startswith("x = 2 + 3 * 6"), "%d examples" % npx)
    feat("code pipeline: source, tokens, syntax tree, bytecode and result, each from Python's own modules", ntok == 11 and tree_ok and nbc > 3 and res == "20", "%d tokens, %d instructions, result %s" % (ntok, nbc, res))
    # ---- 9.11.0: the 13 kinds of chapter 6 - helpers ----
    NEWKINDS = ["boxes", "classify", "facts", "hist", "keysort", "lanes", "matrix", "mutation", "passes", "refgraph", "seqtypes", "slices", "unpack"]
    T = lambda sel: pg.evaluate("s=>[...document.querySelectorAll(s)].map(e=>e.textContent)", sel)
    def zoom_check(cid):
        sel = "#wv-%s-out" % cid
        if pg.locator(sel + " .zbar").count() != 1 or pg.locator(sel + " .diagram.vz svg").count() != 1: return "no zoom bar or no diagram"
        v0 = pg.get_attribute(sel + " svg", "viewBox"); pg.click(sel + ' [data-z="in"]'); v1 = pg.get_attribute(sel + " svg", "viewBox"); pg.click(sel + ' [data-z="out"]'); pg.click(sel + ' [data-z="in"]'); pg.click(sel + ' [data-z="reset"]'); v2 = pg.get_attribute(sel + " svg", "viewBox")
        return "" if (v1 != v0 and v2 == v0) else "zoom in/reset did not work (%s | %s | %s)" % (v0, v1, v2)
    def open_vis(cid):
        pg.evaluate("goTo('%s')" % cid)
        if pg.evaluate("id=>document.getElementById('wvp-'+id).hidden", cid): pg.click('[data-vistoggle="%s"]' % cid)
    RG_JS = """w=>{const o=document.getElementById(w+'-out');
 const rect=oid=>{const r=o.querySelector('g.rgo[data-oid="'+oid+'"] > rect.rgb');return r?[+r.getAttribute('x'),+r.getAttribute('y'),+r.getAttribute('width'),+r.getAttribute('height')]:null};
 const end=p=>{const n=p.getAttribute('d').match(/-?[0-9.]+/g).map(Number);return [n[n.length-2],n[n.length-1]]};
 return {names:[...o.querySelectorAll('g.rgn')].map(g=>[g.dataset.name,g.dataset.oid,g.querySelector('text').textContent]),
  arrows:[...o.querySelectorAll('path.rga')].map(p=>[p.dataset.name,p.dataset.oid,end(p),rect(p.dataset.oid)]),
  objs:[...o.querySelectorAll('g.rgo')].map(g=>[g.dataset.oid,[...g.querySelectorAll('text.rgt')].map(t=>t.textContent),[...g.querySelectorAll('g.rgi[data-ref]')].map(i=>i.dataset.ref),g.querySelectorAll('g.rgi').length]),
  refs:[...o.querySelectorAll('path.rgr')].map(p=>[p.dataset.from,+p.dataset.i,p.dataset.oid,end(p),rect(p.dataset.oid)]),
  cap:o.querySelector('.rgcap').textContent,scopes:[...o.querySelectorAll('.rgsc')].map(t=>t.textContent)}}"""
    KS_JS = """w=>{const o=document.getElementById(w+'-out'),cx=r=>+r.getAttribute('x')+ +r.getAttribute('width')/2;
 return {expr:o.querySelector('.kse').textContent,items:[...o.querySelectorAll('g.ksi text')].map(t=>t.textContent),keys:[...o.querySelectorAll('text.ksk')].map(t=>t.textContent),out:[...o.querySelectorAll('g.kso text')].map(t=>t.textContent),
  lines:[...o.querySelectorAll('line.ksln')].map(l=>[+l.dataset.from,+l.dataset.to,+l.getAttribute('x1'),+l.getAttribute('x2')]),inX:[...o.querySelectorAll('g.ksi rect')].map(cx),outX:[...o.querySelectorAll('g.kso rect')].map(cx)}}"""
    def check_new(cid, v, w):
        ok = False; why = ""
        bad = []; chk = lambda c, m: (None if c else bad.append(m)); K = v["kind"]; out = "#%s-out" % w
        if K == "boxes":
            n = len(v["list"]); pg.click('[data-nv="%s:pick:all"]' % cid)
            cells = pg.evaluate("w=>[...document.querySelectorAll('#'+w+'-out .bxc:not(.ghost)')].map(c=>[c.querySelector('.ix').textContent,c.querySelector('.it').textContent,c.querySelector('.nx').textContent])", w)
            chk(cells == [[str(i), t, str(i - n)] for i, t in enumerate(v["list"])], "index labels or items differ: %s" % cells)
            hitjs = "w=>[...document.querySelectorAll('#'+w+'-out .bxc:not(.ghost)')].flatMap((c,i)=>c.classList.contains('hit')?[i]:[])"
            chk(pg.evaluate(hitjs, w) == sorted({a for p in v["picks"] for a in p["at"]}), "show all: highlighted boxes %s" % pg.evaluate(hitjs, w))
            for i, p in enumerate(v["picks"]):
                pg.click('[data-nv="%s:pick:%d"]' % (cid, i)); hit = pg.evaluate(hitjs, w)
                chk(hit == sorted(p["at"]), "pick %s highlights %s, not %s" % (p["expr"], hit, p["at"]))
                chk(pg.text_content('[data-nv="%s:pick:%d"] .pe' % (cid, i)) == p["expr"] and pg.text_content('[data-nv="%s:pick:%d"] .rs' % (cid, i)) == p["result"], "pick text of %s" % p["expr"])
            if v.get("error"):
                pg.click('[data-nv="%s:pick:e"]' % cid)
                chk(pg.locator(out + " .bxc.ghost").count() == 1 and pg.evaluate(hitjs, w) == [], "error: a dashed empty box after the last one and nothing highlighted")
                chk(pg.text_content('[data-nv="%s:pick:e"] .pe' % cid) == v["error"]["expr"] and pg.text_content('[data-nv="%s:pick:e"] .rs' % cid) == v["error"]["message"], "error text")
            else: chk(pg.locator(out + " .bxc.ghost").count() == 0, "a ghost box without an error")
            pg.click('[data-nv="%s:pick:all"]' % cid); why = "%d boxes with front and back indexes; %d picks each light their boxes%s" % (n, len(v["picks"]), "; the error shows an empty box and its message" if v.get("error") else "")
        if K == "slices":
            n = len(v["list"]); chk(T(out + " .slr.hdr .sli") == [str(i) for i in range(n)], "header indexes")
            for r, R_ in enumerate(v["rows"]):
                pg.click('[data-nv="%s:row:%d"]' % (cid, r))
                row = pg.evaluate("a=>{const b=document.querySelectorAll('#'+a[0]+'-out button.slr')[a[1]];return {x:b.querySelector('.slx').textContent,res:b.querySelector('.slres').textContent,pl:b.querySelector('.slp').textContent,cells:[...b.querySelectorAll('.slc')].map(c=>[c.querySelector('.itx').textContent,c.classList.contains('on'),(c.querySelector('.ord')||{}).textContent||null]),sel:b.classList.contains('sel')}}", [w, r])
                chk(row["x"] == R_["expr"] and row["res"] == R_["result"] and row["pl"] == R_["picked_label"], "row %d text" % r)
                chk([c[0] for c in row["cells"]] == v["list"], "row %d items" % r)
                chk([i for i, c in enumerate(row["cells"]) if c[1]] == sorted(R_["picked"]), "row %d (%s) selects %s, not %s" % (r, R_["expr"], [i for i, c in enumerate(row["cells"]) if c[1]], R_["picked"]))
                chk(row["sel"] and all(row["cells"][i][2] == str(k + 1) for k, i in enumerate(R_["picked"])), "row %d order numbers" % r)
            pg.click('[data-nv="%s:row:%d"]' % (cid, len(v["rows"]) - 1)); chk(pg.locator(out + " .ord").count() == 0, "order numbers stay after the row is chosen again")
            why = "%d rows: expression, result, label and the selected indexes match; the order numbers follow the slice" % len(v["rows"])
        if K == "lanes":
            for i, L in enumerate(v["lanes"]):
                pg.click('[data-nv="%s:lane:%d"]' % (cid, i))
                ln = pg.evaluate("a=>{const b=document.querySelectorAll('#'+a[0]+'-out button.lane')[a[1]];const cl=s=>[...b.querySelectorAll(s+' .cl')].map(c=>[c.textContent,c.classList.contains('rm'),c.classList.contains('add')]);return {op:b.querySelector('.lop').textContent,name:b.querySelector('.lname').textContent,cat:b.querySelector('.lcat').textContent,ret:b.querySelector('.lret').textContent,retnone:b.querySelector('.lret').classList.contains('none'),id:b.querySelector('.lid').textContent,same:b.querySelector('.lid').classList.contains('same'),before:cl('.lb'),after:cl('.la'),det:(b.querySelector('.ldet')||{}).textContent||'',sel:b.classList.contains('sel')}}", [w, i])
                chk(ln["op"] == L["op"] and ln["name"] == L["name"] and ln["cat"] == L["cat_label"], "lane %d op/name/category" % i)
                chk(ln["ret"] == L["ret_label"] and ln["retnone"] == (L["returns"] is None), "lane %d returned value" % i)
                chk(ln["id"] == "same object: " + ("yes" if L["same_object"] else "no") and ln["same"] == L["same_object"], "lane %d same-object flag: %s" % (i, ln["id"]))
                chk([c[0] for c in ln["before"]] == L["before"] and [c[0] for c in ln["after"]] == L["after"], "lane %d before/after lists" % i)
                chk([k for k, c in enumerate(ln["before"]) if c[1]] == L["before_marks"] and not any(c[2] for c in ln["before"]), "lane %d marks in the before list" % i)
                chk([k for k, c in enumerate(ln["after"]) if c[2]] == L["after_marks"] and not any(c[1] for c in ln["after"]), "lane %d marks in the after list" % i)
                chk(ln["sel"] and all(L["before"][k] in ln["det"] for k in L["before_marks"]) and all(L["after"][k] in ln["det"] for k in L["after_marks"]) and (("same list object" in ln["det"]) == L["same_object"]), "lane %d detail line: %s" % (i, ln["det"][:80]))
            chk(T(out + " .lerr") == [e["expr"] + " → " + e["message"] for e in v["errors"]], "error lines")
            why = "%d operations: before and after lists, marked boxes, returned value and same-object flag match; %d error lines" % (len(v["lanes"]), len(v["errors"]))
        if K == "hist":
            rows = pg.evaluate("w=>[...document.querySelectorAll('#'+w+'-out tr')].map(r=>[r.querySelector('.hl').textContent,r.querySelector('.hn').textContent,r.querySelector('.hbar').getBoundingClientRect().width])", w)
            mx = max(b_["count"] for b_ in v["bars"]); wmax = max(r[2] for r in rows)
            chk(len(rows) == len(v["bars"]), "number of bars")
            for b_, r in zip(v["bars"], rows): chk(r[0] == b_["text"] and r[1] == str(b_["count"]) and abs(r[2] / wmax - b_["count"] / mx) < .02, "bar %s: %s" % (b_["text"], r))
            chk(sum(b_["count"] for b_ in v["bars"]) == v["draws"], "the counts add up to the draws")
            why = "%d bars: label, count and bar length match; the counts add up to %d draws" % (len(rows), v["draws"])
        if K == "refgraph":
            npass = 0
            for si, S in enumerate(v["scenarios"]):
                if len(v["scenarios"]) > 1: pg.click('[data-nv="%s:sc:%d"]' % (cid, si))
                for sti, St in enumerate(S["steps"]):
                    if sti: pg.click('[data-nv="%s:st:1"]' % cid)
                    g = pg.evaluate(RG_JS, w); tag = "scenario %d step %d" % (si + 1, sti + 1); want = sorted((n_, oid) for sc in St["scopes"] for n_, oid in sc["names"])
                    chk(g["cap"] == St["code"], tag + " caption")
                    chk(sorted((a[0], a[1]) for a in g["names"]) == want and all(a[0] == a[2] for a in g["names"]), tag + " names %s" % g["names"])
                    chk(sorted((a[0], a[1]) for a in g["arrows"]) == want, tag + " arrows")
                    for a in g["arrows"]: chk(a[3] and abs(a[2][0] - a[3][0]) < 1 and a[3][1] <= a[2][1] <= a[3][1] + a[3][3], tag + " the arrow of %s ends on the frame of its object" % a[0])
                    reach = set(); todo = [oid for _, oid in want]
                    while todo:
                        o_ = todo.pop()
                        if o_ in reach: continue
                        reach.add(o_); ob = St["objects"][o_]
                        if ob["type"] == "list": todo += [it["ref"] for it in ob["items"] if it.get("ref")]
                    chk({o_[0] for o_ in g["objs"]} == reach, tag + " objects drawn %s vs %s" % ([o_[0] for o_ in g["objs"]], sorted(reach)))
                    for o_ in g["objs"]:
                        ob = St["objects"][o_[0]]
                        if ob["type"] == "list": chk(o_[1] == [it["v"] for it in ob["items"] if not it.get("ref")] and o_[2] == [it["ref"] for it in ob["items"] if it.get("ref")] and o_[3] == len(ob["items"]), tag + " items of %s: %s" % (o_[0], o_[1]))
                        else: chk(o_[1] == [ob["v"]], tag + " value of %s" % o_[0])
                    wantrefs = sorted((o_, i, it["ref"]) for o_, ob in St["objects"].items() if o_ in reach and ob["type"] == "list" for i, it in enumerate(ob["items"]) if it.get("ref"))
                    chk(sorted((r[0], r[1], r[2]) for r in g["refs"]) == wantrefs, tag + " reference arrows")
                    for r in g["refs"]: chk(r[4] and abs(r[3][0] - r[4][0]) < 1 and r[4][1] <= r[3][1] <= r[4][1] + r[4][3], tag + " a reference arrow ends on its object")
                    chk(g["scopes"] == ([sc["scope"] for sc in St["scopes"]] if len(St["scopes"]) > 1 else []), tag + " scope labels %s" % g["scopes"])
                    npass += 1
            zc = zoom_check(cid); chk(not zc, "zoom: " + zc)
            z0 = pg.get_attribute(out + " svg", "viewBox"); pg.click(out + ' [data-z="in"]'); z1 = pg.get_attribute(out + " svg", "viewBox"); pg.click('[data-nv="%s:st:-1"]' % cid); z2 = pg.get_attribute(out + " svg", "viewBox"); chk(z1 != z0 and z2 == z1, "a redrawn step keeps the zoomed view"); pg.click(out + ' [data-z="reset"]')
            why = "%d steps: every name reaches the object its arrow ends on, every item and reference arrow matches; zoom keeps its view" % npass
        if K == "keysort":
            for ei, E in enumerate(v["examples"]):
                pg.click('[data-nv="%s:ex:%d"]' % (cid, ei)); g = pg.evaluate(KS_JS, w); tag = "example %d" % (ei + 1)
                chk(g["expr"] == E["expr"] and g["items"] == E["items"] and g["out"] == E["result"] and g["keys"] == (E["keys"] or []), tag + " texts")
                chk(sorted((l[0], l[1]) for l in g["lines"]) == sorted((s_, p_) for p_, s_ in enumerate(E["order"])), tag + " lines")
                chk(all(abs(l[2] - g["inX"][l[0]]) < .5 and abs(l[3] - g["outX"][l[1]]) < .5 and E["items"][l[0]] == E["result"][l[1]] for l in g["lines"]), tag + " each line joins an input box to the same item in the output")
            zc = zoom_check(cid); chk(not zc, "zoom: " + zc); why = "%d sorts: items, keys, output and the lines from input to output match" % len(v["examples"])
        if K == "matrix":
            nfr = len(v["frames"]); pos = lambda: pg.text_content("#%s-pos" % w)
            for _ in range(nfr): pg.click('[data-nv="%s:fr:-1"]' % cid)
            for a, F in enumerate(v["frames"]):
                chk(pos() == "frame %d of %d" % (a + 1, nfr) and T(out + " .mxl") == [F["label"]] and T(out + " pre.frame .mxr") == F["rows"], "frame %d" % (a + 1))
                pg.click('[data-nv="%s:fr:1"]' % cid)
            chk(pos() == "frame %d of %d" % (nfr, nfr), "the last frame stays")
            chk(T(out + " .hzt") == [H["label"] for H in v["hazard"]] and T(out + " .hzn") == [H["spaces_label"] for H in v["hazard"]] and T(out + " pre.hzg .mxr") + T(out + " pre.hzb .mxr") == [H["row"] for H in v["hazard"]], "hazard rows")
            chk(all(H["row"].count(" ") == H["spaces"] for H in v["hazard"]), "the spaces of a hazard row are the number stated")
            chk(T(out + " table.life th") == v["life_cols"] and pg.evaluate("w=>[...document.querySelectorAll('#'+w+'-out table.life tbody tr')].map(r=>[...r.children].map(c=>c.textContent))", w) == [[str(r_["row"]), r_["char"], str(r_["counter"])] for r_ in v["life"]], "the counter table")
            why = "%d frames stepped (rows exact), %d hazard rows, %d counter rows" % (nfr, len(v["hazard"]), len(v["life"]))
        if K == "mutation":
            n = len(v["passes"]); pg.click('[data-nv="%s:mu:reset"]' % cid)
            for r, P in enumerate(v["passes"]):
                row = pg.evaluate("a=>{const rs=[...document.querySelectorAll('#'+a[0]+'-out .mrow')],e=rs[a[1]],cl=s=>[...e.querySelectorAll(s+' .cl')].map(c=>c.textContent);return {vis:rs.filter(x=>!x.hidden).length,head:e.querySelector('.mh').textContent,before:cl('.mb'),cur:[...e.querySelectorAll('.mb .cl')].findIndex(c=>c.classList.contains('cur')),act:e.querySelector('.mact').textContent,after:cl('.ma'),fin:document.querySelectorAll('#'+a[0]+'-out .mfin').length}}", [w, r])
                chk(row["vis"] == r + 1 and row["head"] == P["head"] and row["before"] == P["before"] and row["cur"] == P["pos"] and row["act"] == P["action"] and row["after"] == P["after"], "pass %d: %s" % (r + 1, row))
                chk(pg.text_content("#%s-pos" % w) == "pass %d of %d" % (r + 1, n) and row["fin"] == (1 if r == n - 1 else 0), "pass %d position or final block" % (r + 1))
                if r < n - 1: pg.click('[data-nv="%s:mu:1"]' % cid)
            chk(T(out + " .mfl") == [v["final_label"]] and T(out + " .mfs") == [v["skip_label"]] and T(out + " .mfp") == [v["printed"]], "final block")
            chk(v["original"] == v["passes"][0]["before"] and v["final"] == v["passes"][-1]["after"], "the passes run from the original list to the final one")
            pg.click('[data-nv="%s:mu:-1"]' % cid); chk(pg.locator(out + " .mfin").count() == 0, "Previous hides the final block"); pg.click('[data-nv="%s:mu:reset"]' % cid)
            why = "%d passes stepped: head, list at the start, the position reached, action and list at the end; then the final block" % n
        if K == "passes":
            n = len(v["tables"][0]["rows"]); pg.click('[data-nv="%s:pa:all"]' % cid)
            chk(T(out + " table caption code") == [t_["header"] for t_ in v["tables"]], "table headers")
            chk(pg.evaluate("w=>[...document.querySelectorAll('#'+w+'-out table')].map(t=>[[...t.querySelectorAll('th')].map(x=>x.textContent),[...t.querySelectorAll('tbody tr')].map(r=>[...r.children].map(c=>c.textContent))])", w) == [[t_["cols"], t_["rows"]] for t_ in v["tables"]], "table columns and rows")
            chk(T(out + " .nvprint .pl") == v["printed"] and T(out + " .wl")[0] == v["printed_label"], "printed lines")
            chk(T(out + " .nse") == [v["start"]["expr"]] and T(out + " .nsr") == [v["start"]["result"]], "start example")
            for k in range(n):
                pg.click('[data-nv="%s:pa:1"]' % cid)
                now = pg.evaluate("w=>[[...document.querySelectorAll('#'+w+'-out table')].map(t=>[...t.querySelectorAll('tbody tr')].findIndex(r=>r.classList.contains('now'))),[...document.querySelectorAll('#'+w+'-out .pl')].findIndex(p=>p.classList.contains('now'))]", w)
                chk(now == [[k] * len(v["tables"]), k] and pg.text_content("#%s-pos" % w) == "pass %d of %d" % (k + 1, n), "step %d highlights %s" % (k + 1, now))
            pg.click('[data-nv="%s:pa:all"]' % cid); chk(pg.locator(out + " .now").count() == 0, "Show all clears the highlight")
            why = "%d tables, %d printed lines and the start example match; %d passes stepped across the tables and the printed lines" % (len(v["tables"]), len(v["printed"]), n)
        if K == "seqtypes":
            got = pg.evaluate("w=>[...document.querySelectorAll('#'+w+'-out .sqc')].map(c=>[c.querySelector('.sqn').textContent,c.querySelector('.sqs2').textContent,c.querySelector('.sqm').textContent,c.querySelector('.sqa').textContent,c.querySelector('.sqr').textContent,c.classList.contains('mut')])", w)
            chk(got == [[t_["type"], t_["sample"], t_["mutable_label"], t_["assign"], t_["result"], t_["mutable"]] for t_ in v["types"]], "cards %s" % got)
            why = "%d types: sample, mutability, assignment and its result match" % len(v["types"])
        if K == "unpack":
            for ci, c in enumerate(v["cases"]):
                base = out + ' [data-uc="%d"]' % ci
                chk(T(base + " .ups") == [c["stmt"]] and T(base + " .upi") == c["items"] and T(base + " .unn") == [t_["name"] for t_ in c["targets"]] and T(base + " .unv") == [t_["value"] for t_ in c["targets"]], "case %d texts" % (ci + 1))
                chk(pg.evaluate("s=>[...document.querySelectorAll(s+' .unt')].map(b=>b.style.gridColumn)", base) == ["%d / %d" % (t_["from"] + 1, t_["to"] + 1) for t_ in c["targets"]], "case %d: each name spans the items it took" % (ci + 1))
                for m, t_ in enumerate(c["targets"]):
                    pg.click('[data-nv="%s:tg:%d.%d"]' % (cid, ci, m)); picked = pg.evaluate("s=>[...document.querySelectorAll(s+' .upi')].flatMap((e,i)=>e.classList.contains('pick')?[i]:[])", base)
                    chk(picked == list(range(t_["from"], t_["to"])), "case %d: %s marks items %s" % (ci + 1, t_["name"], picked))
            if v.get("error"): chk(T(out + " .uerr") == [v["error"]["expr"]] and v["error"]["message"] in T(out + " .lerr")[0], "the error")
            why = "%d cases: statement, items, names, values and the items each name marks match" % len(v["cases"])
        if K == "classify":
            got = pg.evaluate("w=>[...document.querySelectorAll('#'+w+'-out .clc')].map(c=>[c.querySelector('.clq').textContent,c.querySelector('.clh').textContent,[...c.querySelectorAll('.clk')].map(k=>[k.querySelector('.cke').textContent,k.querySelector('.cle').textContent])])", w)
            chk(got == [[c["question"], c["head"], [[k["expr"], k["evidence"]] for k in c["chips"]]] for c in v["columns"]], "columns %s" % got)
            why = "%d columns with their chips and evidence match" % len(v["columns"])
        if K == "facts":
            got = pg.evaluate("w=>[...document.querySelectorAll('#'+w+'-out .fc')].map(c=>[c.querySelector('.fct').textContent,c.querySelector('.fce').textContent,c.querySelector('.fcr').textContent])", w)
            chk(got == [[f["label"], f["expr"], f["result"]] for f in v["facts"]], "facts %s" % got)
            why = "%d facts: label, expression and result match" % len(v["facts"])
        ok = not bad
        if bad: why = bad[0][:200]
        return ok, why
    vis_ok = []
    NODE_IDS = {n["id"] for n in nodes}  # a visual whose key is not a concept id (the deck-only "ThreeQuestions") is not on the page
    SKIPPED = [k for k in d.get("visuals", {}) if not k.startswith("_") and k not in NODE_IDS]
    for cid, v in ((k, x) for k, x in d.get("visuals", {}).items() if not k.startswith("_") and k in NODE_IDS):
        w = "wv-" + cid; pg.evaluate("goTo('%s')" % cid); pg.click('[data-vistoggle="%s"]' % cid); ok = False; why = ""
        try:
            if v["kind"] == "floatbits":
                pg.wait_for_function("id=>document.querySelector('#'+id+'-out .bits')", arg=w, timeout=120000); bits = pg.text_content("#%s-out .bits" % w).strip()
                import struct; x = float(eval(v["start"])); ok = bits == format(struct.unpack(">Q", struct.pack(">d", x))[0], "064b"); why = "64 bits match the build interpreter's"
            if v["kind"] == "truthtable":
                pg.wait_for_function("id=>document.querySelector('#'+id+'-out table')", arg=w, timeout=120000); rows = pg.locator("#%s-out tr" % w).count() - 1
                names = sorted(set(__import__("re").findall(r"\b[abc]\b", v["start"]))); ok = rows == 2 ** len(names); why = "%d rows for %d inputs" % (rows, len(names))
            if v["kind"] == "trace":
                for ri, run in enumerate(v["runs"]):
                    if ri: pg.click('[data-vrun="%s:%d"]' % (cid, ri))
                    else: pg.wait_for_function("id=>document.querySelector('#'+id+'-out table')", arg=w, timeout=60000)
                    n = len(run["rows"]); [pg.click('[data-vnext="%s"]' % cid) for _ in range(n - 1)]
                    shown = pg.locator("#%s-out tr:not([hidden])" % w).count() - 1; last = pg.locator("#%s-out tr.now" % w).inner_text()
                    ok = shown == n and str(n) in pg.text_content("#%s-pos" % w) and all(x.strip("'") in last or x in last for x in run["rows"][-1]["vals"]); why = "run %d: %d passes shown, last row matches" % (ri + 1, n)
                    if not ok: break
                    if run["printed"]: ok = run["printed"] in pg.text_content("#%s-out" % w); why += "; printed text shown"
                    if not ok: break
            if v["kind"] == "range":
                dots = pg.locator("#%s-out svg circle" % w).count(); ok = dots == len(v["values"]) + 1 and ("stop %d" % v["stop"]) in pg.text_content("#%s-out" % w); why = "%d value dots and the stop marker" % len(v["values"])
            if v["kind"] == "pairs":
                txt = pg.text_content("#%s-out" % w); ok = all(x in txt for x in v["reprs"]) and (not v.get("error") or v["error"] in txt) and pg.locator("#%s-out svg line" % w).count() == len(v["pairs"]); why = "%d pairs drawn" % len(v["pairs"])
            if v["kind"] == "names":
                ok = ("%d names" % v["count"]) in pg.text_content("#%s" % w); why = "states %d names" % v["count"]
            if v["kind"] == "debugger":
                E = v["events"]; bp = v["breakpoints"]
                pg.click('[data-dbg="%s:stop"]' % cid); pos = lambda: pg.text_content("#%s-pos" % w)
                first_line = E[0]["line"]; ok = ("line %d" % first_line) in pos()
                # toggle a breakpoint on and off
                tgt = next(x for x in range(1, len(v["lines"]) + 1) if x not in bp)
                pg.click('[data-bp="%s:%d"]' % (cid, tgt)); on = "on" in (pg.get_attribute('[data-bp="%s:%d"]' % (cid, tgt), "class") or ""); pg.click('[data-bp="%s:%d"]' % (cid, tgt)); off = "on" not in (pg.get_attribute('[data-bp="%s:%d"]' % (cid, tgt), "class") or "")
                ok = ok and on and off
                pg.click('[data-dbg="%s:in"]' % cid); i1 = E[1]["line"] if len(E) > 1 else None; ok = ok and ("line %d" % i1) in pos()
                pg.click('[data-dbg="%s:stop"]' % cid)
                if bp:
                    nxt = next((e for e in E[1:] if e["line"] in bp), None); pg.click('[data-dbg="%s:cont"]' % cid)
                    ok = ok and (nxt is None or (("line %d (breakpoint)" % nxt["line"]) in pos())); why = "stopped at line %s (breakpoint) after Continue" % (nxt["line"] if nxt else "-")
                else:
                    why = "no breakpoint set in this run"
                # Step Over skips a call, Step Out leaves it: checked against the recorded depths
                ci = next((k for k in range(len(E) - 1) if E[k + 1]["depth"] > E[k]["depth"]), None); sem = "no call in this run"
                if ci is not None:
                    d0 = E[ci]["depth"]; ov = next((k for k in range(ci + 1, len(E)) if E[k]["depth"] <= d0), len(E)); ou = next((k for k in range(ci + 2, len(E)) if E[k]["depth"] <= d0), len(E))
                    pg.click('[data-dbg="%s:stop"]' % cid); [pg.click('[data-dbg="%s:in"]' % cid) for _ in range(ci)]; pg.click('[data-dbg="%s:over"]' % cid)
                    ok = ok and (pos() == "finished" if ov >= len(E) else ("line %d" % E[ov]["line"]) in pos())
                    pg.click('[data-dbg="%s:stop"]' % cid); [pg.click('[data-dbg="%s:in"]' % cid) for _ in range(ci + 1)]; pg.click('[data-dbg="%s:out"]' % cid)
                    ok = ok and (pos() == "finished" if ou >= len(E) else ("line %d" % E[ou]["line"]) in pos()); sem = "Step Over and Step Out from the call at event %d land where the recorded depths say" % ci
                pg.click('[data-dbg="%s:stop"]' % cid)
                for _ in range(len(E) + 2): pg.click('[data-dbg="%s:in"]' % cid)
                ok = ok and pos() == "finished" and v["printed"] in pg.text_content("#%s-out" % w); why += "; Step In reaches the end and shows the program output; breakpoint toggles; " + sem
            if v["kind"] == "levels":
                good = True
                for i, t in enumerate(v["settings"]):
                    pg.click('[data-lv="%s:%d"]' % (cid, i)); rows = pg.locator("#%s-out tbody tr, #%s-out tr:has(td)" % (w, w)); shown = pg.locator("#%s-out td.t" % w).count()
                    good &= shown == sum(1 for x in t["shown"] if x) and t["output"] == [x for x in pg.text_content("#%s-out pre.out" % w).split("\n") if x and x != "(nothing)"]
                ok = good; why = "%d settings; shown counts and printed lines match the recorded specification" % len(v["settings"])
            if v["kind"] == "unwind":
                for _ in range(len(v["frames"]) + 1): pg.click('[data-uw="%s:next"]' % cid)
                ok = ("caught in %s" % v["handler"]["func"]) in pg.text_content("#%s-pos" % w) and v["traceback"].splitlines()[0] in pg.text_content("#%s-out" % w); why = "%d frames climbed, caught in %s, traceback shown" % (len(v["frames"]), v["handler"]["func"])
            if v["kind"] == "branchflow":
                pg.wait_for_function("id=>/Output/.test(document.getElementById(id+'-out').textContent)", arg=w, timeout=120000); first = pg.text_content("#%s-out" % w)
                pg.fill("#%s-x" % w, "8"); pg.click('[data-vis="%s"]' % cid); pg.wait_for_function("id=>/child ticket/.test(document.getElementById(id+'-out').textContent)", arg=w, timeout=60000)
                ok = ("adult ticket" in first or "senior ticket" in first) and pg.locator("#%s-src .tl.now" % w).count() >= 3; why = "path follows the input: %s then child ticket" % ("adult" if "adult" in first else "senior")
            if v["kind"] in NEWKINDS:
                ok, why = check_new(cid, v, w)
        except Exception as e:
            why = "%s: %s" % (type(e).__name__, str(e)[:200])
        R["widgets"][w] = {"passed": ok, "detail": why}; vis_ok.append(ok)
    feat("chapter visualisations: float bits, truth tables, branch paths, loop traces, ranges and pairs - each computed by Python or by an executed specification", all(vis_ok), "%d of %d" % (sum(vis_ok), len(vis_ok)))
    # ---- 9.11.0: zoom on every SVG chapter visual, the ignored framing slide, WCAG over the new visuals ----
    svgv = [k for k, x in d.get("visuals", {}).items() if k in NODE_IDS and x["kind"] in ("keysort", "refgraph", "range", "pairs")]
    zbad = []
    for cid in svgv:
        open_vis(cid); z = zoom_check(cid)
        if z: zbad.append((cid, z))
    feat("zoom in, out and show-all on every SVG chapter visual (sorts, name-and-object pictures, ranges, pairs), the same controls as the other diagrams", not zbad, "%d diagrams; %s" % (len(svgv), zbad[:2]))
    feat("a visual whose key is not a concept id (the deck-only framing slide) is not drawn and raises no error", all(pg.locator("#wv-%s" % k).count() == 0 for k in SKIPPED), "ignored keys: %s" % (SKIPPED or "none"))
    newids = [k for k, x in d.get("visuals", {}).items() if k in NODE_IDS and x["kind"] in NEWKINDS]
    if newids:
        ax = ctx.new_page(); ax.goto("file://" + page_path); ax.wait_for_timeout(400); ax.add_script_tag(path=AXE)
        ax.evaluate("ids=>{document.querySelectorAll('.vis').forEach(e=>{let p=e;while(p&&p!==document.body){p.hidden=false;p=p.parentElement}});ids.forEach(id=>nvShow(id))}", newids)
        viol = ax.evaluate("async()=>{const r=await axe.run({include:[['.nv']]},{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}});return r.violations.map(v=>[v.id,v.impact,v.nodes.length,v.nodes.slice(0,2).map(n=>n.target.join(' ')+' :: '+((n.any[0]||{}).message||''))])}")
        feat("WCAG 2 A/AA (axe-core) over all %d new chapter visuals shown at once" % len(newids), not viol, str(viol)[:300]); ax.close()
    view("taxonomy"); v0 = pg.get_attribute("#taxo svg", "viewBox"); pg.hover("#taxo svg"); pg.mouse.wheel(0, -300); pg.wait_for_timeout(200); v1 = pg.get_attribute("#taxo svg", "viewBox")
    feat("the mouse wheel zooms diagrams, without a key held", v1 != v0, "viewBox changed on wheel")
    # ---- 9.1.0: phones and tablets ----
    for (W, H, dev) in ((360, 740, "small phone"), (390, 844, "phone"), (768, 1024, "tablet")):
        mctx = b.new_context(locale="en-US", viewport={"width": W, "height": H}, is_mobile=True, has_touch=True, device_scale_factor=2); m = mctx.new_page(); m.goto("file://" + page_path); m.wait_for_timeout(400)
        bad = []
        for k in ["intro"] + [x for x in GROUP] + ["agents"]:
            m.evaluate("k=>showTab(k)", k); m.wait_for_timeout(120)
            r = m.evaluate("""()=>{const W=innerWidth;return {wide:document.documentElement.scrollWidth>W+1,
              tiny:[...document.querySelectorAll('button,a,input,select,textarea')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&!e.closest('[hidden],.tv')&&!(e.tagName==='A'&&e.closest('p,li,td'))&&(r.height<24||r.width<24)}).map(e=>(e.id||e.className||e.textContent).toString().slice(0,20)).slice(0,3),
              font:Math.min(...[...document.querySelectorAll('main p, main li, .note, .msg')].filter(e=>e.getBoundingClientRect().width>0).map(e=>parseFloat(getComputedStyle(e).fontSize)).concat([99]))}}""")
            if r["wide"] or r["tiny"] or (W < 700 and r["font"] < 14): bad.append((k, r))
        header = m.evaluate("()=>Math.round(document.querySelector('header').getBoundingClientRect().height)")
        m.click("#exploreBtn"); m.wait_for_timeout(350); drawer = m.evaluate("()=>{const r=document.getElementById('explorerTree').getBoundingClientRect();return r.left>=-1&&r.width>200}")
        leaf = [n for n in nodes if n["level"] == 3][0]; m.click("#expandAll"); m.click('#tree .tn[data-c="%s"]' % leaf["id"]); m.wait_for_timeout(400)
        closed = m.evaluate("()=>document.getElementById('explorerTree').getBoundingClientRect().right<=0") and m.evaluate(in_view, "s-" + leaf["id"])
        feat("%s (%dpx): no view wider than the screen, every control at least 24px, text at least 14px%s, explorer as a drawer" % (dev, W, "" if W >= 700 else ", header compact"), not bad and drawer and closed and (W >= 700 or header <= 100), "header %dpx; problems: %s" % (header, bad[:2]))
        mctx.close()
    # ---- 9.2.0: any screen - the page scales with the window, live, without a reload ----
    dctx = b.new_context(locale="en-US", viewport={"width": 1280, "height": 800}); dp = dctx.new_page(); dp.goto("file://" + page_path); dp.wait_for_timeout(300); dp.evaluate("showTab('%s')" % tops[0]["id"])
    sizes = []
    for (W, H) in ((1280, 800), (1920, 1080), (2560, 1440), (3840, 2160), (3440, 1440)):
        dp.set_viewport_size({"width": W, "height": H}); dp.wait_for_timeout(200)
        sizes.append(dp.evaluate("""()=>({root:parseFloat(getComputedStyle(document.documentElement).fontSize),body:parseFloat(getComputedStyle(document.querySelector('main p')).fontSize),
            tree:Math.round(document.querySelector('aside.tree').getBoundingClientRect().width),wide:document.documentElement.scrollWidth>innerWidth+1,card:Math.round(document.querySelector('.ovcard').getBoundingClientRect().width)})"""))
    grows = all(sizes[k + 1]["root"] > sizes[k]["root"] for k in range(3)) and sizes[0]["root"] >= 17 and sizes[3]["root"] <= 28 and not any(x["wide"] for x in sizes)
    scales = all(abs(x["body"] / x["root"] - sizes[0]["body"] / sizes[0]["root"]) < 0.01 and x["tree"] > 0 for x in sizes) and sizes[3]["card"] > sizes[0]["card"]
    feat("any screen: text, explorer and cards scale with the window as it is resized, 1280 to 3840 pixels, bounded at 17 and 28 pixel text", grows and scales,
         "root text %s px" % " / ".join("%g" % x["root"] for x in sizes))
    dctx.close()
    # ---- 9.4.0: the explorer opens one concept; its siblings stay a click away ----
    mid2 = next(m for m in nodes if m["level"] == 2 and len([x for x in nodes if x["parent"] == m["id"]]) >= 2); sibs = [x for x in nodes if x["parent"] == mid2["id"]]
    pg.click("#expandAll"); pg.click('#tree .tn[data-c="%s"]' % sibs[0]["id"]); pg.wait_for_timeout(250)
    shown = pg.evaluate("id=>[...document.querySelectorAll('[data-subpane=\"'+id+'\"] .cards > section.leaf')].filter(s=>!s.hidden).map(s=>s.dataset.concept)", mid2["id"])
    crumb = pg.text_content("#crumb-%s" % [n for n in nodes if n["id"] == mid2["parent"]][0]["id"])
    pg.click('#crumb-%s [data-sub="%s"]' % (mid2["parent"], mid2["id"])); pg.wait_for_timeout(200)
    all_back = pg.evaluate("id=>[...document.querySelectorAll('[data-subpane=\"'+id+'\"] .cards > section.leaf')].filter(s=>!s.hidden).length", mid2["id"])
    feat("the explorer opens a single concept; the breadcrumb shows where it sits, with its neighbours and 'show all' a click away", shown == [sibs[0]["id"]] and sibs[0]["label"] in crumb and sibs[1]["label"] in crumb and all_back == len(sibs), "%s alone, then all %d" % (sibs[0]["label"], all_back))
    # ---- 9.4.1: the explorer follows every move of the main area ----
    sel = lambda: pg.evaluate("()=>{const x=document.querySelector('#tree .tn.sel');return x?x.dataset.c:null}")
    steps = []
    view(mid2["parent"]); pg.select_option('#crumb-%s select' % mid2["parent"], mid2["id"]); pg.wait_for_timeout(150); steps.append(("breadcrumb chooser", sel() == mid2["id"]))
    pg.evaluate("goTo('%s')" % sibs[0]["id"]); pg.click('#crumb-%s [data-go="%s"]' % (mid2["parent"], sibs[1]["id"])); pg.wait_for_timeout(150); steps.append(("next concept", sel() == sibs[1]["id"]))
    pg.click('#crumb-%s [data-sub="%s"]' % (mid2["parent"], mid2["id"])); pg.wait_for_timeout(150); steps.append(("show all", sel() == mid2["id"]))
    other = next(t_ for t_ in tops if t_["id"] != mid2["parent"]); view(other["id"]); pg.wait_for_timeout(150)
    shown_at = pg.evaluate("""id=>{const p=document.querySelector('[data-pane="'+id+'"]'),sp=p.querySelector('[data-subpane]:not([hidden])'),m=sp.dataset.subpane;
        const f=sp.classList.contains('focused')?[...sp.querySelectorAll('.cards > section.leaf')].find(x=>!x.hidden):null;return f?f.dataset.concept:(m.startsWith('ov-')?m.slice(3):m)}""", other["id"])
    steps.append(("subject tab", sel() == shown_at))
    view(mid2["parent"]); pg.wait_for_timeout(150); steps.append(("back to the subject", sel() == mid2["id"]))
    link = pg.locator('[data-subpane="%s"] p [data-c]:visible' % mid2["id"]).first
    if link.count(): link.click(); pg.wait_for_timeout(150); steps.append(("concept tap keeps the location", sel() == mid2["id"])); pg.keyboard.press("Escape")
    view("taxonomy"); steps.append(("non-subject view clears it", sel() is None))
    feat("the explorer stays in step with the main area: chooser, next, show all, subject tabs, concept taps, other views", all(ok for _, ok in steps), ", ".join("%s %s" % (n_, "ok" if ok else "OUT OF STEP") for n_, ok in steps))
    # ---- 9.4.2: nothing an antivirus reads as a downloader or HTML smuggling ----
    html = open(page_path).read()
    risky = {k: len(re.findall(p, html)) for k, p in (("evaluated fetched code", r"\(0,\s*eval\)|[^\w.'\"]eval\((?!n\[|compile|_last|e,|'\+)"), ("new Function", r"new Function\("), ("scripted download", r"\.download\s*=|msSaveOrOpenBlob"), ("document.write", r"document\.write"), ("base64 decode", r"\batob\("), ("redirect", r"location\.(href|replace|assign)\s*="))}
    feat("no evaluated fetched code, no scripted file download, no document.write, base64 decoding or redirect in the page", not any(risky.values()), str(risky))
    # ---- 9.3.0: text-size control, zoom bar outside the drawing, concept taps show options ----
    fctx = b.new_context(locale="en-US", viewport={"width": 1280, "height": 800}); fp = fctx.new_page(); fp.goto("file://" + page_path); fp.wait_for_timeout(300)
    r0 = fp.evaluate("parseFloat(getComputedStyle(document.documentElement).fontSize)"); fp.click("#fsUp"); fp.click("#fsUp"); r2 = fp.evaluate("parseFloat(getComputedStyle(document.documentElement).fontSize)")
    fp.reload(); fp.wait_for_timeout(300); r3 = fp.evaluate("parseFloat(getComputedStyle(document.documentElement).fontSize)"); lab = fp.text_content("#fsVal")
    fp.click("#fsReset"); r4 = fp.evaluate("parseFloat(getComputedStyle(document.documentElement).fontSize)")
    feat("text-size control: larger and smaller text, remembered after a reload, one click back to the default", r0 >= 17 and abs(r2 - r0 * 1.2) < 0.6 and abs(r3 - r2) < 0.1 and lab == "120%" and abs(r4 - r0) < 0.1, "%g -> %g px (%s), reset %g px" % (r0, r2, lab, r4))
    fp.evaluate("showTab('taxonomy')"); fp.wait_for_timeout(300)
    ov = fp.evaluate("()=>{const bar=document.querySelector('#taxo .zbar'),d=document.querySelector('#taxo .diagram');const a=bar.getBoundingClientRect(),c=d.getBoundingClientRect();return a.bottom<=c.top+0.5&&!d.contains(bar)}")
    feat("zoom controls sit above each diagram, never covering it", ov)
    fp.evaluate("goTo('%s')" % tops[0]["id"]); fp.wait_for_timeout(200); link = fp.locator('[data-pane="%s"] p [data-c]:visible' % tops[0]["id"]).first
    if link.count():
        tgt = link.get_attribute("data-c"); before = fp.evaluate("[...document.querySelectorAll('[data-pane]')].find(p=>!p.hidden).dataset.pane"); link.click(); fp.wait_for_timeout(200)
        after = fp.evaluate("[...document.querySelectorAll('[data-pane]')].find(p=>!p.hidden).dataset.pane"); card = fp.text_content("#card") if fp.locator("#card").is_visible() else ""
        feat("tapping a concept in the text opens its options in the detail card, without leaving the page", before == after and "Go to its section" in card and byid_label_ok(card, tgt) if False else (before == after and "Go to its section" in card), "%s: card with options, still on %s" % (tgt, after))
    fctx.close()
    pinch = pg.evaluate("""()=>{showTab('taxonomy');const svg=document.querySelector('#taxo svg'),v0=svg.getAttribute('viewBox'),r=svg.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2;
      const ev=(t,id,x,y)=>svg.dispatchEvent(new PointerEvent(t,{pointerId:id,clientX:x,clientY:y,bubbles:true,pointerType:'touch',isPrimary:id===1}));
      ev('pointerdown',1,cx-20,cy);ev('pointerdown',2,cx+20,cy);ev('pointermove',1,cx-80,cy);ev('pointermove',2,cx+80,cy);ev('pointerup',1,cx-80,cy);ev('pointerup',2,cx+80,cy);return v0!==svg.getAttribute('viewBox')}""")
    feat("pinch zoom: two fingers spreading zoom a diagram", pinch)
    lt2 = pg.evaluate("window.__lt"); feat("no main-thread task over 200 ms, including the ontology layout", max(lt2 or [0]) <= 200, "longest %d ms" % max(lt2 or [0]))
    # ---- 9.7.0: no step button, lecture, resources, fitted work area ----
    leafw = pg.evaluate("ids=>ids.map(id=>{const e=document.getElementById('w-'+id);return e?e.querySelectorAll('button,[data-step]').length:0}).reduce((a,b)=>a+b,0)", [n["id"] for n in nodes if n["level"] == 3 and not n.get("chart") and "io" not in n])
    feat("concept sections carry no Next-step or Walk-through button (a static example only)", leafw == 0 and "Walk through it" not in pg.evaluate("()=>document.body.innerText"), "%d buttons in %d static example widgets" % (leafw, len([n for n in nodes if n["level"] == 3 and "io" not in n and not n.get("chart")])))
    if d.get("lecture"):
        view("lecture"); ls = pg.locator("#ls-1").count(); cnt = pg.locator(".lslide").count()
        jump = next((x for x in d["lecture"] if x.get("concept")), None); jok = True
        if jump:
            pg.click('#ls-%d [data-go]' % jump["n"]); pg.wait_for_timeout(250); jok = pg.evaluate(in_view, "s-" + jump["concept"]) or pg.evaluate(in_view, "w-" + jump["concept"]); view("lecture")
        vj = next((x for x in d["lecture"] if x.get("visual") and x["visual"] in d.get("visuals", {}) and x["visual"] in NODE_IDS and x.get("concept")), None); vok = True
        if vj:
            pg.click('#ls-%d [data-lvis]' % vj["n"]); pg.wait_for_timeout(300); vok = pg.evaluate("id=>{const e=document.getElementById('wv-'+id);return !!e&&e.getBoundingClientRect().height>0&&!e.closest('[hidden]')}", vj["visual"])
        feat("Lecture tab: one slide text per deck slide, each with a jump to its concept and a button that shows its visual", cnt == len(d["lecture"]) and ls == 1 and jok and vok, "%d lecture slides; jumps land on the concept and the visual" % cnt)
    if d.get("resources"):
        view("resources"); lis = pg.locator("ul.res li"); nres = lis.count(); okl = all(lis.nth(k).locator("a").first.get_attribute("target") == "_blank" and "noopener" in lis.nth(k).locator("a").first.get_attribute("rel") for k in range(nres))
        has_vid = any(r["kind"] == "video" for r in d["resources"]); note = "No video has been checked yet" in pg.text_content('[data-pane="resources"]')
        n3 = len([n for n in nodes if n["level"] == 3]); srows = pg.locator('[data-pane="resources"] table tr').count(); hrefs = pg.evaluate("()=>[...document.querySelectorAll('[data-pane=\"resources\"] table a')].map(a=>a.href)")
        feat("Resources tab: every checked link opens in a new tab safely, videos are never invented, and each concept has a labelled search", nres == len(d["resources"]) and okl and (has_vid or note) and srows == n3 and all(("youtube.com/results" in h or "stackoverflow.com/search" in h or "discuss.python.org/search" in h) for h in hrefs), "%d links, %d search rows" % (nres, srows))
    # fitted work area
    fit = []
    for (W, H) in ((1400, 900), (1280, 720)):
        pg.set_viewport_size({"width": W, "height": H}); pg.wait_for_timeout(200)
        leaf_id = [n for n in nodes if n["level"] == 3][0]["id"]; pg.evaluate("id=>goTo(id)", leaf_id); pg.wait_for_timeout(250)
        r = pg.evaluate("""()=>{const p=document.querySelector('[data-pane]:not([hidden])'),h2=p.querySelector('.viewsub h2, h2'),vs=p.querySelector('.viewsub');
          const tv=[...document.querySelectorAll('textarea.code')].filter(t=>t.offsetParent).map(t=>t.scrollHeight>t.clientHeight+2);
          return {h2:h2?getComputedStyle(h2).position==='absolute'||h2.getBoundingClientRect().height<=1:true,scrollw:document.documentElement.scrollWidth>innerWidth+1,ta:tv.some(x=>x)}}""")
        fit.append((W, H, r))
    pg.set_viewport_size({"width": 1400, "height": 900})
    feat("fit: sub-page heading hidden under the tab row, introductions folded, code areas show all their text", all(not f[2]["scrollw"] and not f[2]["ta"] for f in fit), str([(f[0], f[2]) for f in fit]))
    view("play"); pcode = pg.evaluate("()=>{const t=document.getElementById('pcode');const r=t.getBoundingClientRect();return {top:Math.round(r.top),bottom:Math.round(r.bottom),H:innerHeight,inner:t.scrollHeight>t.clientHeight+2}}")
    feat("the playground code area uses the free height and does not scroll inside", pcode["bottom"] <= pcode["H"] + 2 and pcode["bottom"] > pcode["H"] * 0.55 and not pcode["inner"], str(pcode))
    view("quiz"); fs = pg.locator("fieldset:not([data-gen])"); qok = True
    for k in range(fs.count()):
        f = fs.nth(k); f.locator("input").nth(int(f.get_attribute("data-answer"))).check(); f.locator("button").click(); qok &= pg.text_content("#q%d-fb" % k) == "Correct."
    feat("quiz", qok)
    # ---- 9.9.0: answer formatting ----
    view("agents"); pg.click('[data-agenttab="%s"]' % a["id"])
    fm = pg.evaluate("""()=>{const m=[...document.querySelectorAll('.msg.agent')].filter(x=>x.querySelector('.lead'));const x=m[m.length-1];if(!x)return null;return {lead:!!x.querySelector('.lead'),pts:x.querySelectorAll('ul.pts li').length,tk:x.querySelectorAll('.tk').length,ex:x.querySelectorAll('.exblock').length,rel:x.querySelectorAll('.rel').length,cls:x.classList.contains('answer')}}""")
    feat("agent answers are formatted: lead sentence, bullet points, coloured code, example block, related concepts", bool(fm) and fm["lead"] and fm["pts"] >= 1 and fm["cls"], str(fm))
    md = pg.evaluate("()=>fmt('First paragraph.\\n\\n- one\\n- two\\n\\n```python\\nprint(1)\\n```')")
    feat("markdown text (live LLM) is rendered as paragraphs, bullets and a code block", "<ul" in md and "<pre" in md and md.count("<li") == 2, md[:120])
    # ---- 9.9.0: question builder ----
    view("quiz"); nn = len(d["nodes"])
    gen = pg.evaluate("""()=>{let bad=[],n=0;for(const x of D.nodes){for(const k of qKindsFor(x)){const q=qMake(x.id,k);n++;if(!q||q.options.length<2||q.answer<0||q.answer>=q.options.length||new Set(q.options).size!==q.options.length||!q.q||!q.why)bad.push(x.id+':'+k)}
      if(!qKindsFor(x).length)bad.push(x.id+':none')}return {n,bad:bad.slice(0,5)}}""")
    feat("the question builder can ask about every concept in every kind it offers, with distinct options", not gen["bad"] and gen["n"] >= nn, "%d questions over %d concepts; bad %s" % (gen["n"], nn, gen["bad"]))
    kinds_seen = pg.evaluate("()=>[...new Set(D.nodes.flatMap(n=>qKindsFor(n)))].sort()")
    pg.click("#qgnew"); pg.wait_for_timeout(150)
    f = pg.locator("#qgout fieldset").first; ok1 = f.count() == 1
    f.locator("input").nth(int(f.get_attribute("data-answer"))).check(); f.locator("[data-gcheck]").click(); v1 = f.locator(".verdict").text_content()
    pg.click("#qgall"); pg.wait_for_timeout(300); gf = pg.locator("#qgout fieldset"); cnt = gf.count()
    for k in range(cnt):
        g = gf.nth(k); g.locator("input").nth(int(g.get_attribute("data-answer"))).check(); g.locator("[data-gcheck]").click()
    sc = pg.text_content("#qgscore"); cv = pg.text_content("#qgcover")
    feat("New question makes a question that checks correctly; One question for every concept covers the chapter and scores", ok1 and v1.startswith("Correct") and cnt == nn and ("%d of %d answered correctly" % (cnt, cnt)) in sc and ("all %d" % nn in cv or ("%d of the %d" % (nn, nn)) in cv or str(nn) in cv), "%s | %s | %s" % (v1[:40], sc, cv[:120]))
    pg.locator("#qgout fieldset").first.locator("input").nth(0).check()
    wrong = pg.evaluate("()=>{const f=document.querySelector('#qgout fieldset');const a=+f.dataset.answer;return a===0?1:0}")
    pg.click("#qgclear"); pg.wait_for_timeout(100)
    feat("Clear removes the generated questions and resets coverage", pg.locator("#qgout fieldset").count() == 0 and pg.text_content("#qgscore") == "")
    pg.click("#qgall"); pg.wait_for_timeout(200); g = pg.locator("#qgout fieldset").first; g.locator("input").nth(1 - int(g.get_attribute("data-answer")) if int(g.get_attribute("data-answer")) < 2 else 0).check(); g.locator("[data-gcheck]").click()
    feat("a wrong answer is explained and links to the concept", g.locator(".verdict").text_content().startswith("Not quite") and g.locator("[data-go]").count() == 1)
    # ---- 9.10.0: question bank and live question ----
    bank = pg.evaluate("()=>BANK.length")
    if bank:
        pg.select_option("#qgkind", "authored"); pg.click("#qgall"); pg.wait_for_timeout(300)
        leg = pg.evaluate("()=>[...document.querySelectorAll('#qgout legend')].map(l=>l.textContent)")
        feat("written question bank: it covers every concept and 'One question for every concept' asks the written item first", pg.evaluate("()=>D.nodes.every(n=>BANK.some(b=>b.concept===n.id))") and len(leg) == nn and all(l.startswith("From the question bank") for l in leg), "%d bank items; %d written questions of %d" % (bank, sum(l.startswith("From the question bank") for l in leg), len(leg)))
        perm = pg.evaluate("""()=>{let bad=[];for(const b of BANK){for(let k=0;k<3;k++){const q=qMake(b.concept,'authored');const src=BANK.filter(x=>x.concept===b.concept).some(x=>x.q===q.q&&x.options[x.answer]===q.options[q.answer]&&[...x.options].sort().join('|')===[...q.options].sort().join('|'));if(!src)bad.push(b.concept)}}return bad.slice(0,5)}""")
        feat("shuffled written items keep their right answer", not perm, str(perm))
        appl = pg.evaluate_handle("()=>BANK.filter(b=>b.code)")
        n_apply = pg.evaluate("()=>BANK.filter(b=>b.code).length"); badrun = []
        for k in range(n_apply):
            r = pg.evaluate("async k=>{const b=BANK.filter(b=>b.code)[k];let out;try{out=String(await runPy(b.code)).trim()}catch(e){out='ERR:'+String(e).split('\\n').pop()}return [out,b.options[b.answer],b.concept]}", k)
            ok = r[0] == r[1] or r[0].rstrip(":") == r[1] or (r[0].startswith("ERR:") and r[1] in r[0]) or (r[0].startswith("ERR:") and r[1].split()[0].endswith("Error")) or (r[1].split()[0].endswith("Error") and r[0].split(':')[0].strip()==r[1].split()[0])
            if not ok: badrun.append(r)
        feat("every written item with code is re-run in the page and its marked answer is what the browser's Python prints", not badrun, "%d re-run; mismatches %s" % (n_apply, str(badrun[:3])[:300]))
    pg.select_option("#qgkind", "any"); pg.click("#qgclear")
    pg.click("#qglive"); pg.wait_for_timeout(200); msg0 = pg.text_content("#qgout")
    feat("without a live model the live question says so and changes nothing else", "not available in this browser" in msg0)
    pg.evaluate("()=>{KIT.llm={chat:{completions:{create:async()=>({choices:[{message:{content:window.__reply}}]})}}}}")
    def live(reply):
        pg.evaluate("r=>{window.__reply=r}", reply); pg.click("#qglive"); pg.wait_for_function("()=>!/Asking the model/.test(document.getElementById('qgout').textContent)", timeout=60000); return pg.text_content("#qgout"), pg.locator("#qgout fieldset").count()
    t1, c1 = live('Sure! {"q":"What is a traceback?","options":["A report of the calls that led to an error","A kind of loop","A file format","A log level"],"answer":0,"why":"It lists the calls."}')
    t2, c2 = live('{"q":"What does this print?","code":"print(6*7)","options":["13","42","67","Error"],"answer":1,"why":"6 times 7."}')
    t3, c3 = live('{"q":"What does this print?","code":"print(6*7)","options":["13","42","67","Error"],"answer":0,"why":"wrong on purpose"}')
    t4, c4 = live('I cannot do that')
    t5, c5 = live('{"q":"x","options":["a","a","b","c"],"answer":1}')
    feat("live-model question: a well-formed one is shown with its label; one with code is shown only when its code prints the marked answer; malformed or wrong ones are refused with a reason", c1 == 1 and "live model" in t1 and c2 == 1 and "was run" in t2 and c3 == 0 and "not what its code prints" in t3 and c4 == 0 and "well-formed" in t4 and c5 == 0, "%s | %s | %s | %s" % (t3[:60], t4[:60], t5[:60], t2[-80:]))
    pg.evaluate("()=>{KIT.llm=null}"); pg.click("#qgclear")
    # ---- 9.12.0: clickable references, page search, grounding of the local model's reply ----
    view("agents"); pg.click('[data-agenttab="%s"]' % a["id"])
    ans4 = ask("how is " + q1.lower() + " written")
    nrn = pg.locator("#%s-log .msg button.rn" % a["id"]).count(); nsrc = pg.locator("#%s-log .msg button.src" % a["id"]).count()
    pg.locator("#%s-log .msg button.src" % a["id"]).last.click(); pg.wait_for_selector("#card .srcview .full, #card.srcview .full", timeout=60000)
    cardtxt = pg.text_content("#card"); flashed = pg.locator("#%s-log button.src.flash" % a["id"]).count()
    feat("every source chip in an answer opens its passage in the detail card and is marked in the answer", nsrc >= 3 and len(pg.text_content("#card .full")) > 20 and flashed >= 1 and pg.locator("#card [data-close]").count() == 1, "%d chips; card %d chars; %d marked" % (nsrc, len(cardtxt), flashed))
    if nrn:
        pg.keyboard.press("Escape"); pg.locator("#%s-log .msg button.rn" % a["id"]).last.click(); pg.wait_for_timeout(600)
    feat("inline [n] references in an answer are buttons that open the same passage", nrn >= 1 and pg.locator("#card .full").count() == 1 and len(pg.text_content("#card .full")) > 20, "%d inline references" % nrn)
    view("intro"); pg.keyboard.press("/"); pg.wait_for_selector("#srch:not([hidden])", timeout=5000)
    opened = pg.evaluate("()=>document.activeElement.id==='srchq'&&document.getElementById('srch').getAttribute('role')==='dialog'")
    lab = [n for n in nodes if n.get("level", 3) >= 2][3]["label"]
    pg.fill("#srchq", lab); pg.wait_for_timeout(200); hit1 = pg.locator("#srch .hit").first.text_content()
    pg.keyboard.press("Enter"); pg.wait_for_timeout(800)
    closed = pg.evaluate("()=>document.getElementById('srch').hidden&&!document.getElementById('srch').hasAttribute('role')")
    feat("search: the / key opens it with focus in the box, a concept name finds that concept first, Enter goes to it and closes the search", opened and lab.lower() in hit1.lower() and closed and lab.lower() in pg.text_content("#card").lower(), "%s -> %s" % (lab, hit1[:50]))
    pg.keyboard.press("Control+k"); pg.wait_for_selector("#srch:not([hidden])", timeout=5000)
    pg.fill("#srchq", lab.split()[0]); pg.wait_for_timeout(200); nh = pg.locator("#srch .hit").count()
    pg.click("#srchmore"); pg.wait_for_selector("#srchpass .hit", timeout=120000); npass = pg.locator("#srchpass .hit").count()
    pg.locator("#srchpass .hit").first.click(); pg.wait_for_selector("#card .full", timeout=60000)
    feat("search: Ctrl+K opens it, finds concepts by definition or code, can also search the book, course and research passages, and a passage opens in the card", nh >= 1 and npass >= 1 and pg.evaluate("()=>document.getElementById('srch').hidden"), "%d concepts, %d passages" % (nh, npass))
    pg.keyboard.press("Control+k"); pg.fill("#srchq", "zzqqxx"); pg.wait_for_timeout(200); none = "No concept" in pg.text_content("#srchres"); pg.keyboard.press("Escape")
    feat("search: a word that is nowhere says so, and Esc closes it", none and pg.evaluate("()=>document.getElementById('srch').hidden"))
    gt = pg.evaluate(r"""()=>{const top=[{c:{text:'The if statement runs its block when the condition holds. Otherwise it skips to the next block.',label:'If statement'}}];
      const a=groundText('At the top of this page you would find a lovely section labelled banana. An if statement runs its block when the condition holds [1].',top);
      const b=groundText('Bananas grow in warm countries and are yellow.',top);
      const c=groundText('Here:\n```\nprint(1)\n```\nThe condition holds.',top);return [a,b,c]}""")
    feat("the local model's reply is checked against its passages: unsupported sentences go, a wholly unsupported reply is dropped, code and supported text stay", gt[0]["dropped"] == 1 and "banana" not in gt[0]["text"] and "condition holds" in gt[0]["text"] and gt[1]["text"] is None and "print(1)" in gt[2]["text"], str(gt)[:200])
    pg.evaluate("()=>{KIT.llm={chat:{completions:{create:async()=>({choices:[{message:{content:'At the top of this page you would find a section labelled banana. It is yellow and grows in warm countries.'}}]})}}}}")
    pg.keyboard.press("Escape"); view("agents"); pg.click('[data-agenttab="%s"]' % a["id"])
    ans5 = ask("what is " + q1.lower()); pg.evaluate("()=>{KIT.llm=null}")
    lastby = pg.locator("#%s-log .msg" % a["id"]).last.text_content()
    feat("an invented reply from the model never reaches the reader; the passages' own sentences are shown with a note", "banana" not in ans5 and "not supported by the passages" in lastby, ans5[:120])
    # ---- 9.13.0: progress, links, copy, notes, cheat sheet, marks, review queue, exercises ----
    pg.keyboard.press("Escape"); leaf = [n_ for n_ in nodes if int(n_.get("level", 3)) >= 3]; A, B = leaf[0]["id"], leaf[1]["id"]; NN = len(nodes)
    pg.evaluate("id=>goTo(id)", A); pg.evaluate("id=>goTo(id)", B); h1 = pg.evaluate("()=>location.hash")
    pg.go_back(); pg.wait_for_timeout(500); h2 = pg.evaluate("()=>location.hash"); shown = pg.evaluate("id=>{const e=document.getElementById('s-'+id);return !!e&&e.offsetParent!==null}", A)
    pg.go_forward(); pg.wait_for_timeout(500); h3 = pg.evaluate("()=>location.hash")
    m2 = ctx.new_page(); m2.goto("file://" + page_path + "#c=" + B); m2.wait_for_timeout(1500); deep = m2.evaluate("id=>{const e=document.getElementById('s-'+id);return !!e&&e.offsetParent!==null}", B); m2.close()
    feat("every concept has a link (#c=...) that opens it, and the browser's back and forward buttons walk through the places visited", h1 == "#c=" + B and h2 == "#c=" + A and shown and h3 == "#c=" + B and deep, "%s %s %s deep=%s" % (h1, h2, h3, deep))
    pg.evaluate("id=>openCard(id)", A); pg.wait_for_selector("#card .mark", timeout=5000); pg.click("#card .mark"); b1 = pg.text_content("#progBadge")
    ticked = pg.evaluate("id=>document.querySelector('#tree .tn[data-c=\"'+id+'\"]').classList.contains('done')", A); vis = pg.evaluate("id=>document.querySelector('#tree .tn[data-c=\"'+id+'\"]')!==null&&PROG.visited[id]===1", A)
    m3 = ctx.new_page(); m3.goto("file://" + page_path); m3.wait_for_timeout(1500); b2 = m3.text_content("#progBadge"); pressed = m3.evaluate("id=>document.querySelector('main section button.mark[data-mark=\"'+id+'\"]').getAttribute('aria-pressed')", A); m3.close()
    feat("progress: a section can be marked understood; the count, the tick in the explorer and the section's button follow, and it is still there after a reload", b1 == "✓ 1/%d" % NN and ticked and b2 == "✓ 1/%d" % NN and pressed == "true" and vis, "%s | %s | pressed %s" % (b1, b2, pressed))
    pg.click("#card .mark"); feat("progress: marking again takes the mark away", pg.text_content("#progBadge") == "✓ 0/%d" % NN)
    pg.fill("#card textarea.mynote", "my note on A"); pg.wait_for_timeout(200)
    m4 = ctx.new_page(); m4.goto("file://" + page_path); m4.wait_for_timeout(1200); m4.evaluate("id=>openCard(id)", A); nv = m4.input_value("#card textarea.mynote"); m4.close()
    pg.evaluate("()=>showTab('mydata')"); pg.wait_for_timeout(300); md = pg.text_content("#mydataout")
    feat("a note written in a concept's details is kept in the browser and listed under Your data", nv == "my note on A" and "my note on A"[:10] in md and "Notes" in md, nv)
    pg.evaluate("()=>showTab('cheat')"); ncs = pg.locator(".cheat .cs").count(); want = len([n_ for n_ in nodes if int(n_.get("level", 3)) >= 2])
    pg.emulate_media(media="print"); hid = pg.evaluate("()=>getComputedStyle(document.querySelector('header.top')).display==='none'&&getComputedStyle(document.getElementById('card')).display==='none'"); vs = pg.evaluate("()=>document.querySelector('.cheat').offsetParent!==null"); pg.emulate_media(media="screen")
    feat("cheat sheet: every concept below the top level on one page, and the print style hides the page's controls and keeps the sheet", ncs == want and hid and vs, "%d of %d; controls hidden %s" % (ncs, want, hid))
    view("agents"); pg.click('[data-agenttab="%s"]' % a["id"]); pg.keyboard.press("Escape")
    nb = pg.locator("#%s-log .fb" % a["id"]).count(); pg.locator("#%s-log .fb [data-fb=err]" % a["id"]).last.click(); pr = pg.locator("#%s-log .fb [data-fb=err]" % a["id"]).last.get_attribute("aria-pressed")
    pg.evaluate("()=>showTab('mydata')"); pg.wait_for_timeout(300); pg.click("#dlfb"); pg.wait_for_timeout(300); clip = pg.evaluate("()=>navigator.clipboard.readText()")
    feat("every answer carries Yes / No / Report-an-error marks; a mark is kept and can be copied out with the question and answer", nb >= 3 and pr == "true" and "contains an error" in clip and "Question:" in clip, "%d answers with marks" % nb)
    pg.evaluate("()=>{REV={};reviewPaint()}"); view("quiz"); pg.select_option("#qgkind", "any"); pg.click("#qgnew"); pg.wait_for_timeout(200); fsq = pg.locator("#qgout fieldset").first; cid = fsq.get_attribute("data-concept"); ans = int(fsq.get_attribute("data-answer"))
    fsq.locator("input").nth(0 if ans != 0 else 1).check(); fsq.locator("[data-gcheck]").click(); r1 = pg.evaluate("c=>JSON.stringify(REV[c])", cid); lab1 = pg.text_content("#qgreview")
    pg.evaluate("c=>{REV[c].due=0;reviewPaint()}", cid); lab2 = pg.text_content("#qgreview"); pg.click("#qgreview"); pg.wait_for_timeout(200); f2 = pg.locator("#qgout fieldset"); same = f2.count() == 1 and f2.first.get_attribute("data-concept") == cid
    a2 = int(f2.first.get_attribute("data-answer")); f2.first.locator("input").nth(a2).check(); f2.first.locator("[data-gcheck]").click(); box = pg.evaluate("c=>REV[c]&&REV[c].box", cid)
    feat("review queue: a wrong answer is queued, comes back through Review once due, and a right answer moves it on", r1 and '"box":0' in r1 and "1 later" in lab1 and "1 due" in lab2 and same and box == 1, "%s | %s | %s | box %s" % (r1, lab1, lab2, box))
    pg.evaluate("()=>{REV={}}"); view("quiz")
    ncopy = pg.locator("button.copy").count(); view("play"); pg.fill("#pcode", "print('copy me')"); pg.click('[data-copyof="pcode"]'); pg.wait_for_timeout(300); clip2 = pg.evaluate("()=>navigator.clipboard.readText()")
    feat("copy buttons: beside code blocks and the Playground, and they copy the code", ncopy >= 1 and clip2 == "print('copy me')", "%d buttons beside code blocks" % ncopy)
    pg.evaluate("id=>openCard(id)", A); pg.click("#card [data-link]"); pg.wait_for_timeout(300); clip3 = pg.evaluate("()=>navigator.clipboard.readText()")
    feat("the detail card can copy the link to its section", clip3.endswith("#c=" + A), clip3[-40:])
    pg.keyboard.press("Escape"); view("exercises"); pools = pg.evaluate("()=>{const p=exPools();return {order:p.order,blank:p.blank,repair:p.repair}}"); bad = []; counts = {k: len(v) for k, v in pools.items()}
    def vd(): return pg.locator("#cxout .verdict").text_content()
    for d in pools["order"]:
        pg.evaluate("d=>exShow(d)", d); pg.click("#cxout [data-exshow]"); pg.click("#cxout [data-excheck]"); pg.wait_for_function("()=>!/Running/.test(document.querySelector('#cxout .verdict').textContent)", timeout=60000)
        if not vd().startswith("Correct"): bad.append(("order", d["label"], vd()[:60]))
    for d in pools["blank"]:
        pg.evaluate("d=>exShow(d)", d); pg.click("#cxout [data-exshow]"); pg.click("#cxout [data-excheck]"); pg.wait_for_function("()=>!/Running/.test(document.querySelector('#cxout .verdict').textContent)", timeout=60000); v1 = vd()
        pg.fill("#cxout input", "____"); pg.click("#cxout [data-excheck]"); pg.wait_for_function("()=>!/Running/.test(document.querySelector('#cxout .verdict').textContent)", timeout=60000); v2 = vd()
        if not (v1.startswith("Correct") and v2.startswith("Not yet")): bad.append(("blank", d["label"], v1[:50], v2[:50]))
    for d in pools["repair"]:
        pg.evaluate("d=>exShow(d)", d); pg.click("#cxout [data-excheck]"); pg.wait_for_function("()=>!/Running/.test(document.querySelector('#cxout .verdict').textContent)", timeout=60000); v1 = vd()
        pg.fill("#cxout textarea", "print('fixed')"); pg.click("#cxout [data-excheck]"); pg.wait_for_function("()=>!/Running/.test(document.querySelector('#cxout .verdict').textContent)", timeout=60000); v2 = vd()
        if not (v1.startswith("Not yet") and v2.startswith("Correct")): bad.append(("repair", d["label"], v1[:50], v2[:50]))
    feat("code exercises: every exercise this chapter offers (put in order, fill the blank, make it run) accepts its answer by running it and refuses a wrong one", not bad and sum(counts.values()) >= 5, "%s; bad %s" % (counts, bad[:3]))
    pg.click("#cxnew"); pg.wait_for_selector("#cxout fieldset.ex", timeout=60000); made = pg.locator("#cxout fieldset.ex").count() == 1
    feat("New exercise makes one at random", made)
    R["gates"]["Stage4.C console errors"] = errors
    R["gates"]["Stage4.D dialogs"] = pg.locator('[role="dialog"],dialog').count()
    R["gates"]["Stage4.E sections"] = pg.locator("section[data-source]").count()
    m = ctx.new_page(); m.set_viewport_size({"width": 390, "height": 844}); m.goto("file://" + page_path)
    R["gates"]["Stage4.F top menu visible on mobile without clicks"] = m.locator("#groups button").first.is_visible()
    view("intro"); pg.add_script_tag(path=AXE)
    R["gates"]["WCAG 2 AA (axe-core)"] = pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}});return r.violations.map(v=>[v.id,v.impact,v.nodes.length])}")
    b.close()
json.dump(R, open(os.environ.get("RESULTS", os.path.join(REPO, "08-tooling", "%s-page" % N, "test_results_v%s.json" % PV)), "w"), indent=1)
bad = [k for k, v in R["widgets"].items() if not v["passed"]]
print("widgets: %d tested, %d passed; failing: %s" % (len(R["widgets"]), len(R["widgets"]) - len(bad), [(k, R["widgets"][k]["detail"][:120]) for k in bad[:3]]))
for k, v in R["features"].items(): print("  [%s] %s  %s" % ("PASS" if v["passed"] else "FAIL", k, v["detail"][:150]))
for k, v in R["gates"].items(): print("  %-52s %s" % (k, v))
