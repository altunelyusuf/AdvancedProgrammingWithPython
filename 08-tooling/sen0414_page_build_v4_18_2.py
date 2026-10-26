#!/usr/bin/env python3
"""Builds a SEN0414 chapter page from the course-neutral template (version 4 onward: agents on RDODI's default toolkit). The page embeds the corpus
its agents search, as Turtle: the book's chapter ontology at the exact commit the course's textbook part pins, the
course ontology (profile, outcomes, textbook), and the chapter's RDODI ontology, document and research record.
Each block names its file and hash. Usage: sen0414_page_build_v4_18_2.py <NN>"""
__version__ = "4.18.2"
# 4.18.2 (over 4.18.1; a NEW file): the default template is course_page_template_v9_52_3.html (the Python worker restores sys.path, the added non-library modules, the working folder and os.environ after every run); nothing else changed.
# 4.18.1 (over 4.18.0; repair): the default template is course_page_template_v9_52_2.html (its description comment no longer closes early); the build REFUSES
#   (e) a template whose comment openers and closers differ in number, or in which a closing sequence lies inside a comment (comments must alternate open/close), and
#   (f) a template or a built page that has any text between <body> and the first <header> (comments and white space excepted). The charset guard is kept. Nothing else changed.
# 4.18.0 (over 4.17.0; the owner's page standard of 2026-10-22/23, ported from the sibling's builder 4.15.0): (a) the default template is
#   course_page_template_v9_52_1.html (the character-set declaration first in head, the panel level, one tab row, the chapter-code tab, the Playground by name; the
#   page declares <meta name="page-standard" content="9.52">); (b) the page data may carry "chaptercode" (the deck's chapter-code manifest, read by the
#   page-data builder 2.25.0) - the build stops when the template it was given cannot show it, so a manifest is never dropped silently; (c) environment
#   PAGE_SCRATCH names a folder that receives the page and its corpus manifest instead of 03-materials/chNN/page and 08-tooling/chNN-page, and PAGE_DATA_DIR
#   names the folder the page data is read from (default 08-tooling/chNN-page), so a scratch page can be built outside the repository; (d) REPAIR: the build
#   refuses a page whose first byte sequence in head is not <meta charset="utf-8"> below byte 512 (the HTML encoding prescan reads only 1,024 bytes), and
#   reads the template and writes the page as UTF-8. Page version 9.90.0 and later = template 9.52.1 + data 2.25.0 + builder 4.18.0.
# 4.17.0 (over 4.16.0): the default template is course_page_template_v9_49_0.html (a recorded picture under a concept paragraph); nothing else changed.
# 4.16.0 (over 4.15.0): the default template is course_page_template_v9_48_0.html (no number varied in an example with a while loop); nothing else changed.
# 4.15.0 (over 4.14.0): the default template is course_page_template_v9_47_0.html (breadcrumb pills on one row); nothing else changed.
# 4.14.0 (over 4.13.0): the default template is course_page_template_v9_46_0.html (blank and vary skip helper code); nothing else changed.
# 4.13.0 (over 4.12.0): the default template is course_page_template_v9_45_0.html (a note on a chapter example whose result in the browser differs from the recorded one); nothing else changed.
# 4.12.0 (over 4.11.0): the default template is course_page_template_v9_45_0.html (Pyodide packages named by the chapter, a note on stand-in examples); nothing else changed.
# 4.11.0 (over 4.10.0): the default template is course_page_template_v9_43_0.html (a chapter's embedded pure-Python wheels, data.py_wheels); nothing else changes.
# 4.10.0 (over 4.9.0): the default template is course_page_template_v9_42_0.html, which adds the Lab tab's Chapter
#   examples pane (data["examples"], from the page-data builder 2.7.0); nothing else changes here, since the new
#   pane needs no new corpus block or placeholder - it reads data.examples straight off D like every other pane.
# 4.9.0 (over 4.8.0): (a) the default template is course_page_template_v9_37_0.html - the two-fold look-and-feel series
#   9.26.0-9.37.0 ported from the sibling course's proven 9.33.0-9.44.0 (stories, Learn sections, concept map, ontology
#   layers, chapter ERD, fit, no machinery chips, ERD connections, reading area, relocate on every diagram, narrative
#   diagrams); (b) two more kinds of corpus block - the chapter's diagrams ABox (data["ndiag_abox"], kind "chapter",
#   composed by the data builder 2.6.0 and embedded here, never a file of the package) and the CME narrative-to-diagram
#   mapping (kind "standard", read from the CME checkout named by CME_REPO at the digests the configuration recorded;
#   a changed file stops the build). Page 9.27.0 = template 9.39.0 (9.37.0 plus the exam identity from the configuration, 9.38.0, and the standard kept out of the agents' search, 9.39.0, and a chosen entity's labels placed further out, 9.40.0, and code-named instances named by their class, 9.41.0) + configuration 1.4.0.
# 4.8.0 (over 4.7.0): the default template is course_page_template_v9_24_0.html - the same repairs SEN0401's template
#   9.28.0 carries (an agent retrieves only from its own slice and hands over outside it; the guide ranks only owners;
#   the taxonomy opens as classes only, placed on the root, with worked examples named by what they show; outcomes
#   sort by number and an unapproved set says so; an empty layer and an absent chapter index are not shown; the page
#   explains its own vocabulary). The page data also gains "index_page": the chapter index that really sits beside the
#   page, or "" when there is none, which is what the template now needs before it will show the "All chapters" link.
#   The corpus embedding is left exactly as it was: see the note in sen0401_page_build_v4_4_0.py - a <script>
#   element's content is raw text, a browser does not resolve character references in it (verified in Chromium), and
#   escaping `&` here would corrupt a block rather than repair one.
# 4.7.0: a chapter's newest question_bank_v*.json (if it has one) fills __BANK__ in the template; a chapter without one gets an empty bank.
# 4.6.0: the quiz is the chapter's newest quiz_v*.json (4.5.2 named quiz_v1_0_1.json, which only chapters 1 and 2 have).
import glob, hashlib, json, os, re, subprocess, sys
import glob as _glob
latest_input = lambda d, stem: sorted(_glob.glob(os.path.join(d, stem + '_v*.json')), key=lambda x: [int(v) for v in x.rsplit('_v', 1)[1][:-5].split('_')])[-1]  # page inputs are versioned; the newest one is current
PV = os.environ.get("PAGE_VER", "9_4_2")  # generated files carry the page version they were produced for
N = sys.argv[1]; REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); ONT = "/home/claude/Ontologies"
T = open(os.path.join(REPO, "08-tooling", os.environ.get("PAGE_TEMPLATE", "course_page_template_v9_52_3.html")), encoding="utf-8").read()
def _guard(txt, what):
    import re as _re
    o, c = txt.count("<!--"), txt.count("-->")
    if o != c:
        raise SystemExit("%s refused: %d comment openers against %d closers (an early closing comment shows its text above the header)" % (what, o, c))
    i = 0
    while True:
        a = txt.find("<!--", i)
        if a < 0:
            break
        b = txt.find("-->", a + 4)
        if b < 0 or "<!--" in txt[a + 4:b]:
            raise SystemExit("%s refused: comments do not alternate open/close at byte %d" % (what, a))
        i = b + 3
    bd = txt.find("<body"); hd = txt.find("<header", bd)
    if bd < 0 or hd < 0:
        raise SystemExit("%s refused: no <body> or no <header>" % what)
    between = _re.sub(r"<!--.*?-->", "", txt[txt.find(">", bd) + 1:hd], flags=_re.S).strip()
    if between:
        raise SystemExit("%s refused: text between <body> and the header: %r" % (what, between[:80]))

_guard(T, "the template")
P = os.path.join(REPO, "08-tooling", "ch%s-page" % N)
PD = os.environ.get("PAGE_DATA_DIR") or P
d = json.load(open(os.path.join(PD, "page_data_v%s.json" % PV), encoding="utf-8")); C = d["course"]["corpus"]
if d.get("chaptercode") and 'data-pane="chaptercode"' not in T:
    raise SystemExit("the page data carries a chapter-code manifest (%d examples) but the template has no chapter-code tab (data-pane=\"chaptercode\"); use a template of 9.52.1 or later" % len(d["chaptercode"]["examples"]))
safe = lambda o: json.dumps(o).replace("</", "<\\/")
latest = lambda pat: sorted(glob.glob(pat), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-4].split("_")])[-1]
pin = re.search(r'pinnedCommit "([0-9a-f]{40})"', open(os.path.join(REPO, C["book_pin_source"])).read()).group(1)
blocks = []
def add(kind, name, text):
    h = hashlib.sha256(text.encode()).hexdigest()[:16]
    blocks.append('<script type="text/turtle" data-kind="%s" data-name="%s" data-sha256="%s">%s</script>' % (kind, name, h, text.replace("</script", "<\\/script")))
    return "%s %s %s" % (kind, name, h)
log = []
for pat in C["book"]:
    path = pat.replace("{nn}", N)
    text = subprocess.run(["git", "-C", ONT, "show", "%s:%s" % (pin, path)], capture_output=True, text=True, check=True).stdout
    log.append(add("book", os.path.basename(path) + "@" + pin[:8], text))
for path in C["course"]:
    log.append(add("course", os.path.basename(path), open(os.path.join(REPO, path)).read()))
RD = os.path.join(REPO, "03-materials", "ch%s" % N, "rdodi")
for part, kind in (("domain_tbox", "chapter"), ("domain_abox", "chapter"), ("document", "chapter"), ("research", "research")):
    f = latest(os.path.join(RD, "sen0414_ch%s_%s_v*.ttl" % (N, part)))
    log.append(add(kind, os.path.basename(f), open(f).read()))
# 4.9.0: the chapter's diagrams ABox block and the CME standard that types it
if d.get("ndiag_abox"): _nab = d.pop("ndiag_abox"); log.append(add("chapter", _nab["name"], _nab["text"]))
CME_REPO = os.environ.get("CME_REPO", "/home/claude/cme"); std_note = []
for st in C.get("standards", []):
    fp = os.path.join(CME_REPO, st["folder"], st["path"]); b = open(fp, "rb").read()
    if hashlib.sha256(b).hexdigest() != st["sha256"]:
        raise SystemExit("the CME standard %s does not match the digest recorded in the configuration (%s)" % (st["path"], st["sha256"][:12]))
    log.append(add("standard", os.path.basename(st["path"]), b.decode())); std_note.append("%s@%s sha256 %s" % (os.path.basename(st["path"]), C.get("standards_package_version", "?"), st["sha256"][:16]))
# The course lineage's own mission, goals and objectives, read from the published register (About > Mission & backlog)
import rdflib
LG = rdflib.Graph(); LG.parse(latest(os.path.join(REPO, "07-lineage", "*.ttl")), format="turtle")
BK = rdflib.Namespace("http://example.org/backlog#")
mis = next(LG.subjects(rdflib.RDF.type, BK.Mission), None)
d["mission"] = {"statement": str(LG.value(mis, BK.hasMissionStatement) or ""), "outcome": str(LG.value(mis, BK.hasMissionOutcome) or ""),
                "goals": sorted(str(LG.value(g, rdflib.RDFS.label)) for g in LG.subjects(rdflib.RDF.type, BK.Goal)),
                "objectives": sorted(str(LG.value(o, rdflib.RDFS.label)) for o in LG.subjects(rdflib.RDF.type, BK.Objective))}
_bk = _glob.glob(os.path.join(P, "question_bank_v*.json")); _bank = json.load(open(latest_input(P, "question_bank"))) if _bk else []
_q = json.load(open(latest_input(P, "quiz"))); QUIZ = _q["items"] if isinstance(_q, dict) else _q  # versioned inputs wrap lists as {"_version", "items"}
outdir = os.environ.get("PAGE_SCRATCH") or os.path.join(REPO, "03-materials", "ch%s" % N, "page"); os.makedirs(outdir, exist_ok=True)
d["index_page"] = "index.html" if os.path.exists(os.path.join(outdir, "index.html")) else ""
h = (T.replace("__TITLE__", d["title"]).replace("__PAGEVERSION__", PV.replace("_", ".")).replace("__COURSE__", d["course"]["line"]).replace("__SUB__", d["course"]["chapter_sub"].replace("{n}", str(d["chapter"])))
      .replace("__PY__", d["python"]).replace("__DATA__", safe(d)).replace("__QUIZ__", safe(QUIZ)).replace("__BANK__", safe(_bank))
      .replace("__OBJ__", safe(json.load(open(latest_input(P, "objectives"))))).replace("__CORPUS__", "\n".join(blocks)))
out = os.path.join(outdir, "sen0414_ch%s_page_v%s.html" % (N, PV))
_guard(h, "the built page")
_hd = h.find("<head>"); _cs = '<meta charset="utf-8">'
if _hd < 0 or not h[_hd + 6:].startswith(_cs) or _hd + 6 + len(_cs) > 512:
    raise SystemExit('the page does not open its head with <meta charset="utf-8"> below byte 512; the template is wrong')
open(out, "w", encoding="utf-8").write(h); json.dump({"_version": PV.replace("_", "."), "items": log}, open(os.path.join(os.environ.get("PAGE_SCRATCH") or P, "corpus_manifest_v%s.json" % PV), "w"), indent=1)
print("written", out, len(h), "bytes; corpus:", "; ".join(log))
print("  chapter code:", ("%d examples from %s" % (len(d["chaptercode"]["examples"]), d["chaptercode"]["file"])) if d.get("chaptercode") else "no manifest, no chapter-code tab")
print("  guard: comments balanced, no text before the header")
print("  charset: first child of head at byte", _hd + 6)
