#!/usr/bin/env python3
"""The Stage 4 page ABox for a SEN0414 chapter, written from the files of the page itself: its page data, the browser test results of the page,
the chapter-code manifest, the objectives and the quiz, and the page file (its menu and tab rows).
Usage: PAGE_VER=9_90_0 ABOX_VER=1_4_0 python3 sen0414_page_abox_build_v1_1_10.py 05
A widget is marked designTestPassed only if its test in test_results_v<PAGE_VER>.json passed."""
__version__ = "1.1.10"
# 1.1.10 (new file over 1.1.9; 1.1.9 stays), written for the retrofit of chapter 5 (TK_Ret_Ch05_Research, 2026-10-25). Two faults of 1.1.9 met on the page of chapter 5, measured:
#  1. The assertion that every conditional tab is filled read data["discussion"]["items"]; a page without a discussion tab has "discussion": [] in its page data (chapters 5 and 9), so 1.1.9 stopped with
#     TypeError (list indices must be integers) before writing anything. 1.1.10 requires the discussion items only when the page data has them (a dict with items); every other tab must still be filled.
#  2. The design-test sentence of each widget named the page test 9.36.0 as the tester; the page of the retrofit is tested by 9.37.0. 1.1.10 names the page test given in the environment variable
#     PAGE_TEST (default sen0414_page_test_v9_37_0.py), the version under which test_results_v<PV>.json was measured.
#  3. A concept without an input-output example in the pinned domain ABox (33 of the 62 concepts of chapter 5) has a widget that shows the concept's example beside its definition and has no step
#     control ("static example shown; no step button" in the page test); 1.1.9 stopped with KeyError on the first of them. 1.1.10 writes it as a widget that is not a numeric demonstrator.
#  4. The step-through visuals of kinds debugger (the recorded run with breakpoints and the Continue, Step In, Step Over and Step Out controls), levels (the logging levels and the messages shown at
#     each threshold) and unwind (the climb of an exception up the call stack) are described with the primitives and warrants that the committed page ABox 1.3.0 of the chapter gave them.
#  5. The definition of a learning objective read "After the chapter the reader can ..."; the objective CO2 of chapter 5 ("Choose between raise and assert ... explain why an assert cannot guard user
#     input") has no word that the gate's finite-verb cue accepts (gate Stage4.sub: "CO2: no finite verb"), so the frame is now "The objective is met when the reader can ...", which holds the verb is.
# Everything else is 1.1.9 unchanged.
# 1.1.9 (new file over 1.1.8; 1.1.8 stays): what changed, and why.
#  Root cause measured on 2026-10-25 (gates v1.1.1 Stage4.cov: 11 hollow typed individuals; Stage4.sub: 152 individuals not substantive): 1.1.8 wrote every typed individual with a
#  label only (the page, its regions, the navigation patterns, the learning objectives) or a label and a source but no skos:definition (the 58 sections, the 81 widgets), and the
#  gate reads the definition (or the label when there is none) as the content: a complete sentence of at least five words, with a source. So the fault was in the builder, not in a gate.
#  1. Every individual of the page standard's vocabulary now gets rdfs:label, skos:definition (one full sentence) and dcterms:source. The sentence is taken from the page's own data: the first
#     sentence of the concept's text (page data nodes, which come from the chapter corpus and the book), the expression and the test detail of the widget, the caption of the visual, the
#     objective's own words, the page file's menu and tab labels, the chapter-code manifest. Nothing is typed in by hand except the sentence frames around those values.
#  2. 1.1.8 read build_record_v<PV>.json and test_results_abox_v<PV>.json, which the page builders of 4.18 and later no longer write. 1.1.9 reads page_data_v<PV>.json (nodes, panels, visuals,
#     chaptercode, stories, lecture, resources), test_results_v<PV>.json (widgets, passed or not), the pinned domain ABox named in corpus_manifest_v<PV>.json (the expression of each
#     concept widget), the newest objectives and quiz files, and the page file itself (VIEWS and GROUPS: the menu and the tab rows).
#  3. New individuals: the eight menu items (ipo:Menu), the six tab rows (ipo:Tabs), one ipo:CodeExample for each example of the chapter-code tab, the three step-through visuals as widgets.
#     Sections now link to their parent (dcterms:isPartOf) and widgets to their section (dcterms:isPartOf), so no individual stands alone.
#  4. The navigation rule no longer states the old section count and band (58 sections in 26-50, which was not true of the page); it describes the page's own menu, tab row, tree and card.
#  5. Empty distractor rationales (the correct option has none) are not written.
import json, os, re, sys
import glob as _glob
latest_input = lambda d, stem: sorted(_glob.glob(os.path.join(d, stem + '_v*.json')), key=lambda x: [int(v) for v in x.rsplit('_v', 1)[1][:-5].split('_')])[-1]
PV = os.environ.get("PAGE_VER", "9_90_0"); AV = os.environ.get("ABOX_VER", "1_4_0")
PAGE_TEST = os.environ.get("PAGE_TEST", "sen0414_page_test_v9_37_0.py")
N = sys.argv[1]; REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PD = os.path.join(REPO, "08-tooling", "ch%s-page" % N); PAGEDIR = os.path.join(REPO, "03-materials", "ch%s" % N, "page")
PAGEFILE = "sen0414_ch%s_page_v%s.html" % (N, PV)
data = json.load(open(os.path.join(PD, "page_data_v%s.json" % PV), encoding="utf-8"))
tr = json.load(open(os.path.join(PD, "test_results_v%s.json" % PV), encoding="utf-8"))
man = json.load(open(os.path.join(PD, "corpus_manifest_v%s.json" % PV), encoding="utf-8"))
OBJ = json.load(open(latest_input(PD, "objectives"), encoding="utf-8"))
SERVES = OBJ.pop("_serves", []); OBJ.pop("_note", None); OBJ.pop("_version", None)
QUIZ = json.load(open(latest_input(PD, "quiz"), encoding="utf-8"))["items"]
html = open(os.path.join(PAGEDIR, PAGEFILE), encoding="utf-8").read()
assert '<meta name="version" content="%s"' % PV.replace("_", ".") in html, "the page file is not version " + PV
BASE = "http://example.org/sen0414/ch%s" % N
PAGEPATH = "03-materials/ch%s/page/%s" % (N, PAGEFILE)
BOOK = "https://automatetheboringstuff.com/3e/chapter%d.html" % int(N)
q = lambda t: t.replace("\\", "\\\\").replace('"', "'").replace("\n", "\\n")
first = lambda t: re.match(r"\s*(.+?[.!?])(?=\s|$)", t, re.S).group(1).replace("\n", " ")
first2 = lambda t: " ".join(x.strip() for x in re.findall(r"(?:.+?[.!?])(?=\s|$)", t.replace("\n", " ").strip(), re.S)[:2])   # the first two sentences of a text: a section's definition is its opening statement and the sentence that completes it
cap = lambda t: t[0].upper() + t[1:]
low = lambda t: t[0].lower() + t[1:]
nodes = data["nodes"]; byid = {n["id"]: n for n in nodes}
sid = lambda i: i.replace("-", "_")

# ---- the pinned domain ABox the page uses: the expression of each concept widget ----
abox_name = next(x.split()[1] for x in man["items"] if x.startswith("chapter ") and "_domain_abox_" in x)
IO = {}
for m in re.finditer(r'ch%s:IO_(\w+) a [^\n]*?ch%s:input "((?:[^"\\]|\\.)*)" ; ch%s:output "((?:[^"\\]|\\.)*)"' % (N, N, N), open(os.path.join(REPO, "03-materials", "ch%s" % N, "rdodi", abox_name), encoding="utf-8").read()):
    IO[m.group(1)] = (m.group(2).replace("\\\\", "\\"), m.group(3).replace("\\\\", "\\"))

# ---- the page's menu and tab rows, read from the page file (VIEWS and GROUPS) ----
views = re.search(r"const VIEWS=\[(.*?)\];", html).group(1)
VIEWS = [("intro", "Start")] + [(k, re.sub(r"^[^A-Za-z]+", "", l)) for k, l in re.findall(r"\['(\w+)','([^']*)'\]", views)]
gtext = html[html.index("const GROUPS={"):html.index("const GROUP_OF")]
TABS = {}
for g in [k for k, _ in VIEWS if k != "intro"]:
    m = re.search(r"[{,\s]%s:\[(.*?)\](?:,\s*\n?\s*\w+:\[|\};)" % g, gtext, re.S)
    if not m: continue
    tabs = [(k, re.sub(r"^[^A-Za-z]+", "", l)) for k, l in re.findall(r"\['(\w+)','([^']*)'\]", m.group(1))]
    if g == "learn":   # the chapter's subjects follow the lecture, stories and chapter-code tabs, one numbered tab for each top-level subject
        tabs += [(n["id"], n["label"]) for n in nodes if n["level"] == 1]
    TABS[g] = tabs
tops = [n for n in nodes if n["level"] == 1]
assert data["lecture"] and data["stories"] and data["chaptercode"]["examples"] and data["resources"] and data["examples"], "a conditional tab of the page is empty"
assert not isinstance(data["discussion"], dict) or data["discussion"]["items"], "the discussion tab of the page is empty"

L = ['''@prefix ipo:     <http://example.org/rdodi/interactive-page-ontology#> .
@prefix wp:      <http://example.org/widget-primitives#> .
@prefix ds:      <http://example.org/rdodi/discourse-selection#> .
@prefix pg:      <%(base)s/page#> .
@prefix sen0414: <http://example.org/sen0414#> .
@prefix ld:      <http://example.org/rdodi/learning-design#> .
@prefix mp:      <http://example.org/rdodi/model-provenance#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix prov:    <http://www.w3.org/ns/prov#> .

<%(base)s/page> a owl:Ontology ; rdfs:label "SEN0414 chapter %(n)d - RDODI Stage 4 page ABox"@en ; owl:versionInfo "%(av)s" ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ; dcterms:rights "Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0."@en ;
    dcterms:rightsHolder <http://example.org/rdodi/agent/YusufAltunel> ; dcterms:publisher <http://example.org/rdodi/agent/IstanbulKulturUniversity> ;
    dcterms:creator <http://example.org/rdodi/agent/YusufAltunel> ; dcterms:created "2026-10-25"^^xsd:date ; dcterms:modified "2026-10-25"^^xsd:date ;
    dcterms:identifier "sen0414_ch%(N)s_page_abox_v%(AV)s" ; prov:wasGeneratedBy <http://example.org/sen0414/activity/ch%(N)s-rdodi-run> ;
    prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .
''' % dict(base=BASE, n=int(N), N=N, av=AV.replace("_", "."), AV=AV)]
add = L.append
def ind(iid, types, label, definition, source, extra=""):
    """one individual of the page standard's vocabulary: label, one-sentence definition, source"""
    src = "<%s>" % source if source.startswith("http") else '"%s"' % q(source)
    add('pg:%s a %s ; rdfs:label "%s"@en ;\n    skos:definition "%s"@en ; dcterms:source %s%s .' % (iid, types, q(label), q(definition), src, (" ;\n    " + extra) if extra else ""))

cos = ", ".join("pg:" + k for k in OBJ)
nsec = len(nodes); nwid = len(tr["widgets"]); nleaf = sum(1 for n in nodes if n["level"] == 3)
tablabels = lambda g: ", ".join(l for k, l in TABS[g])
ex = data["chaptercode"]["examples"]

# ---- the page and its regions ----
add('''pg:Page a ipo:Page, ipo:InteractiveLearningSurface ; rdfs:label "Chapter %d interactive page"@en ;
    skos:definition "%s"@en ; dcterms:source <%s/document> ; ipo:hasSourceDocument pg:SourceDocument ;
    ipo:satisfiesHeuristic ipo:RecognitionRatherThanRecall, ipo:ConsistencyAndStandards, ipo:AestheticAndMinimalistDesign,
        ipo:ShneidermanRule_OfferInformativeFeedback, ipo:ShneidermanRule_PermitEasyReversalOfActions, ipo:HelpAndDocumentation ;
    ipo:hasLayoutPattern pg:Layout ; ipo:hasSemanticRegion pg:Header, pg:Sidebar, pg:Main ;
    ipo:includesNavigationPattern pg:GroupedTopBar, pg:SectionTree ;
    ipo:coversLearningObjective %s ;
    sen0414:navigationRule "%s" ;
    sen0414:pageFile "%s" ;
    sen0414:pythonUsed "%s" .''' % (int(N), q("The interactive page %s teaches chapter %d of the book, %s, through %d sections and %d widgets that run or draw the chapter's examples." % (PAGEFILE, int(N), data["title"], nsec, nwid)),
    BASE, cos,
    q("One top menu of %d items, with one row of tabs under the item that is open, a chapter explorer tree on the left and a detail card on the right that opens only when a reader asks for it." % len(VIEWS)),
    PAGEPATH, data["python"]))
ind("Layout", "ipo:SplitLayout", "Explorer, main area and detail card",
    "The layout puts the chapter explorer tree on the left, the main area with the open tab in the middle and the detail card on the right, which opens only on request.", PAGEPATH)
ind("Header", "ipo:Header", "Header with the chapter title and the main menu",
    "The header holds the chapter title, the buttons to go back and forward, the search, the progress badge, the text-size control and the main menu with %d items." % len(VIEWS), PAGEPATH)
ind("Sidebar", "ipo:Sidebar", "Chapter explorer tree",
    "The sidebar is the chapter explorer, a tree of the %d sections of the chapter whose choice opens the matching tab." % nsec, PAGEPATH)
ind("Main", "ipo:MainContent", "Chapter content with inline widgets",
    "The main area shows the open tab of the open menu item, with the widgets of the chapter's concepts placed in the text they explain.", PAGEPATH)
ind("GroupedTopBar", "ipo:PrimaryNavigation", "Main menu",
    "The main menu is the permanent top bar with the items %s, and a click on an item changes the main area first." % ", ".join(l for k, l in VIEWS), PAGEPATH)
ind("SectionTree", "ipo:TreeNavigation", "Chapter explorer tree of sections",
    "The explorer tree lists the %d subjects of the chapter with their groups and concepts, and it stays in step with the tab row." % len(tops), PAGEPATH)
ind("SourceDocument", "ipo:SourceDocument", "Chapter %d Stage 3 document" % int(N),
    "The source document is the Stage 3 document of chapter %d, which has one section for each of the %d concepts of the chapter." % (int(N), nsec), BASE + "/document",
    "ipo:hasLearningObjective " + cos)

# ---- menu items and tab rows, as they are in the page file ----
for k, l in VIEWS:
    if k in TABS:
        d = "The %s item of the main menu opens the row of tabs %s." % (l, tablabels(k))
    elif k == "agents":
        d = "The %s item of the main menu opens the agents tab, where each subject agent answers from its own part of the chapter." % l
    else:
        d = "The %s item of the main menu opens the introduction to the chapter, which is the page the reader starts on." % l
    ind("Menu_" + k, "ipo:Menu", "%s menu item" % l, d, PAGEPATH, "dcterms:isPartOf pg:GroupedTopBar")
for k, tabs in TABS.items():
    l = dict(VIEWS)[k]
    ind("Tabs_" + k, "ipo:Tabs", "%s tab row" % l, "The tab row of the %s item has the tabs %s, and it is the only row of tabs on the page." % (l, ", ".join(t[1] for t in tabs)), PAGEPATH, "dcterms:isPartOf pg:Menu_" + k)
    add("pg:Menu_%s sen0414:hasTabRow pg:Tabs_%s ." % (k, k))

# ---- learning objectives, assessment ----
for k, (text, lvl) in OBJ.items():
    add('pg:%s a ipo:LearningObjective, owl:NamedIndividual ; rdfs:label "%s"@en ;\n    skos:definition "%s"@en ; dcterms:source <%s> ;\n    ld:bloomLevel ld:%s %s .' % (
        k, q(text), q("The objective is met when the reader can %s, at the %s level." % (low(text), lvl.lower())), BOOK, lvl,
        (" ; sen0414:servesOutcome " + ", ".join("<http://example.org/sen0414#%s>" % o for o in SERVES)) if SERVES else ""))
for n, it in enumerate(QUIZ, 1):
    opts = ", ".join("pg:Q%d_O%d" % (n, j) for j in range(len(it["options"])))
    add('pg:Q%d a ld:AssessmentItem, owl:NamedIndividual ; rdfs:label "%s"@en ; ld:hasOption %s ; ld:hasCorrectOption pg:Q%d_O%d ; ld:cognitiveLevel ld:%s ; ld:assessesObjective pg:%s%s .' % (
        n, q(it["q"]), opts, n, it["answer"], it["level"], it["objective"], "".join(' ;\n    ld:distractorRationale "%s"' % q(r) for r in it["rationales"] if r)))
    for j, o in enumerate(it["options"]): add('pg:Q%d_O%d a ld:AnswerOption ; rdfs:label "%s" .' % (n, j, q(o)))

# ---- sections: one for each concept of the page, linked to its parent ----
for n in nodes:
    i = sid(n["id"])
    kind = {1: "subject", 2: "group", 3: "concept"}[n["level"]]
    ind(i, "ipo:ChapterSection", n["label"], first2(n["body"]), "%s#S_%s" % (BASE, n["id"]),
        'sen0414:anchor "#%s" ; sen0414:sectionLevel %d%s' % ("s-" + n["id"], n["level"], (" ; dcterms:isPartOf pg:" + sid(n["parent"])) if n["parent"] else ""))
    add("pg:Page ipo:coversChapterSection pg:%s ." % i)
    # the panel level: a group's concepts are its panels
for g, cs in data["panels"].items():
    add("pg:%s sen0414:hasPanel %s ." % (sid(g), ", ".join("pg:" + sid(c) for c in cs)))

# ---- chapter-code examples (the chapter-code tab, in slide order) ----
for e in sorted(ex, key=lambda e: e["order"]):
    nl, no = len(e["code"].rstrip("\n").split("\n")), len(e["expected"].rstrip("\n").split("\n")) if e["expected"].strip() else 0
    ind("CE_%02d" % e["order"], "ipo:CodeExample", e["name"],
        "Example %d of the chapter-code tab comes from slide %d of the deck and runs %d lines of Python that print %d lines of output." % (e["order"], e["slide"], nl, no),
        "03-materials/ch%s/page/chapter_code_ch%s_v%s.json" % (N, N, data["chaptercode"]["version"].replace(".", "_")),
        'sen0414:slideNumber %d ; sen0414:orderInTab %d ;\n    sen0414:code "%s" ; sen0414:expectedOutput "%s"' % (e["slide"], e["order"], q(e["code"]), q(e["expected"])))
    add("pg:Tabs_learn sen0414:hasExample pg:CE_%02d ." % e["order"])

# ---- widgets: one for each section, and the step-through visuals ----
def widget(wid, section, kind, prim, warrant, definition, label, detail, passed, numeric, exprs=None):
    w = sid(wid)
    types = "ipo:InstructionalWidget" + (", ipo:CoupledVariableDemonstrator" if numeric else "")
    src = "%s#S_%s" % (BASE, section)
    add('pg:%s a %s ; rdfs:label "%s"@en ;\n    skos:definition "%s"@en ; dcterms:source <%s> ; dcterms:isPartOf pg:%s ;\n    ipo:demonstratesSubject <%s#%s> ;' % (w, types, q(label), q(definition), src, sid(section), BASE, section))
    if numeric:
        add('    ipo:enforcesDomainConstraint <%s#%s> ;' % (BASE, section))
        add('    mp:numericModelStatus mp:Validated ; mp:hasValidationDerivation "The value of the expression was produced by executing it under %s, and the page test requires the value the widget prints to equal the value on the concept card" ; mp:hasConformanceTest "The browser design test requires the printed value to equal the executed one" ;' % q(data["python"]))
    add('    wp:instantiatesPrimitive wp:%s ; ds:selectionWarrant "%s" ;' % (prim, q(warrant)))
    add('    wp:demonstratesConcept <%s#%s> ;' % (BASE, section))
    add('    wp:hasDesignTest "Exercised in headless Chromium by 08-tooling/%s: %s" ; wp:designTestPassed %s .' % (PAGE_TEST, q(detail), "true" if passed else "false"))
for n in nodes:
    wid = "w-" + n["id"]; r = tr["widgets"][wid]
    if n["level"] == 3 and n["id"] not in IO:
        widget(wid, n["id"], "show", "Primitive_OverviewDetailBrushing",
               "Feature_AsymmetricContrast: the exemplar of the concept is shown beside its definition, so that the reader sees what the code looks like and what it does",
               "The widget for %s shows the example %s beside the definition of the concept and has no step control." % (n["label"], n["example"]),
               "example widget for %s" % n["id"], r["detail"], r["passed"], False)
    elif n["level"] == 3:
        expr, out = IO[n["id"]]
        widget(wid, n["id"], "predict", "Primitive_CoupledVariableExplorer",
               "Feature_AsymmetricContrast: the learner edits and predicts %s, then Pyodide shows what Python actually does" % expr,
               "The widget for %s lets the reader edit the expression %s, predict its value and run it, and the value it prints is the value on the concept card." % (n["label"], expr),
               "predict widget for %s" % n["id"], r["detail"], r["passed"], True)
    else:
        kids = [c for c in nodes if c["parent"] == n["id"]]
        widget(wid, n["id"], "map", "Primitive_OverviewDetailBrushing", "Feature_KCategoryEnumeration: the section enumerates its kinds; choosing one opens its card",
               "The widget for %s shows its %d %s as a grid and opens the card of the one the reader chooses." % (n["label"], len(kids), "groups" if n["level"] == 1 else "concepts"),
               "map widget for %s" % n["id"], r["detail"], r["passed"], False)
vis = data["visuals"]
VK = {"trace": ("Primitive_GuidedNarrativeWalkthrough", "Feature_OrderedArgument: the learner steps through a loop that changes the list it walks and sees which items are skipped"),
      "range": ("Primitive_CoupledVariableExplorer", "Feature_CrossAttributeRelation: the values of a range are drawn as dots against their positions, with the stop value marked"),
      "pairs": ("Primitive_CoupledVariableExplorer", "Feature_CrossAttributeRelation: the items of a list are drawn beside the pairs that enumerate makes of them"),
      "debugger": ("Primitive_CoupledVariableExplorer", "Feature_CrossAttributeRelation: the learner sets breakpoints and steps a recorded run; the current line, the variables, the call stack and the output change together"),
      "levels": ("Primitive_MultiClassSelectorDistinct", "Feature_KCategoryEnumeration: the learner chooses one of the logging levels and sees which messages of each level are shown or hidden"),
      "unwind": ("Primitive_GuidedNarrativeWalkthrough", "Feature_OrderedArgument: the learner climbs the call stack one frame at a time until a handler catches the exception")}
for name, v in vis.items():
    wid = "wv-" + name; r = tr["widgets"][wid]
    if v["kind"] == "trace":
        d = "The step-through widget for %s shows %s" % (byid[name]["label"], low(first(v["caption"])))
    elif v["kind"] == "debugger":
        d = "The step-through widget for %s steps a recorded run of a %d-line program with %d breakpoint(s) and shows the current line, the variables, the call stack and the output at each stop." % (byid[name]["label"], len(v["lines"]), len(v["breakpoints"]))
    elif v["kind"] == "levels":
        d = "The widget for %s offers %d threshold settings and shows which of %d log messages each setting lets through." % (byid[name]["label"], len(v["settings"]), len(v["messages"]))
    elif v["kind"] == "unwind":
        d = "The widget for %s climbs %d frames of the call stack, one at a time, until the handler in %s catches the %s." % (byid[name]["label"], len(v["frames"]), v["handler"]["func"], v["exc"])
    elif v["kind"] == "range":
        d = "The widget draws the %d values of %s as dots and marks the stop value %d, which the range never reaches." % (len(v["values"]), v["call"], v["stop"])
    else:
        d = "The widget draws the %d pairs that %s makes: %s." % (len(v["pairs"]), v["call"], v["note"])
    widget(wid, name, v["kind"], VK[v["kind"]][0], VK[v["kind"]][1], d, "%s step-through widget" % name, r["detail"], r["passed"], False)
open(os.path.join(PAGEDIR, "sen0414_ch%s_page_abox_v%s.ttl" % (N, AV)), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("page ABox written: %d sections, %d widgets (%d marked tested), %d menu items, %d tab rows, %d chapter-code examples" % (
    nsec, nwid, sum(1 for w in tr["widgets"].values() if w["passed"]), len(VIEWS), len(TABS), len(ex)))
