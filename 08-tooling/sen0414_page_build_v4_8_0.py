#!/usr/bin/env python3
"""Builds a SEN0414 chapter page from the course-neutral template (version 4 onward: agents on RDODI's default toolkit). The page embeds the corpus
its agents search, as Turtle: the book's chapter ontology at the exact commit the course's textbook part pins, the
course ontology (profile, outcomes, textbook), and the chapter's RDODI ontology, document and research record.
Each block names its file and hash. Usage: sen0414_page_build_v4_8_0.py <NN>"""
__version__ = "4.8.0"
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
T = open(os.path.join(REPO, "08-tooling", os.environ.get("PAGE_TEMPLATE", "course_page_template_v9_24_0.html"))).read()
P = os.path.join(REPO, "08-tooling", "ch%s-page" % N)
d = json.load(open(os.path.join(P, "page_data_v%s.json" % PV))); C = d["course"]["corpus"]
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
outdir = os.path.join(REPO, "03-materials", "ch%s" % N, "page")
d["index_page"] = "index.html" if os.path.exists(os.path.join(outdir, "index.html")) else ""
h = (T.replace("__TITLE__", d["title"]).replace("__PAGEVERSION__", PV.replace("_", ".")).replace("__COURSE__", d["course"]["line"]).replace("__SUB__", d["course"]["chapter_sub"].replace("{n}", str(d["chapter"])))
      .replace("__PY__", d["python"]).replace("__DATA__", safe(d)).replace("__QUIZ__", safe(QUIZ)).replace("__BANK__", safe(_bank))
      .replace("__OBJ__", safe(json.load(open(latest_input(P, "objectives"))))).replace("__CORPUS__", "\n".join(blocks)))
out = os.path.join(outdir, "sen0414_ch%s_page_v%s.html" % (N, PV))
open(out, "w").write(h); json.dump({"_version": PV.replace("_", "."), "items": log}, open(os.path.join(P, "corpus_manifest_v%s.json" % PV), "w"), indent=1)
print("written", out, len(h), "bytes; corpus:", "; ".join(log))
