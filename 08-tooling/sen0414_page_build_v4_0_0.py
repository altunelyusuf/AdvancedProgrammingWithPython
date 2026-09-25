#!/usr/bin/env python3
"""Version 4 of a SEN0414 chapter page: version 3 plus agents on RDODI's default toolkit. The page embeds the corpus
its agents search, as Turtle: the book's chapter ontology at the exact commit the course's textbook part pins, the
course ontology (profile, outcomes, textbook), and the chapter's RDODI ontology, document and research record.
Each block names its file and hash. Usage: sen0414_page_build_v4_0_0.py <NN>"""
import glob, hashlib, json, os, re, subprocess, sys
N = sys.argv[1]; REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); ONT = "/home/claude/Ontologies"
T = open(os.path.join(REPO, "08-tooling", os.environ.get("PAGE_TEMPLATE", "course_page_template_v4_0_0.html"))).read()
P = os.path.join(REPO, "08-tooling", "ch%s-page" % N)
d = json.load(open(os.path.join(P, "page_data_v2.json"))); C = d["course"]["corpus"]
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
h = (T.replace("__TITLE__", d["title"]).replace("__COURSE__", d["course"]["line"]).replace("__SUB__", d["course"]["chapter_sub"].replace("{n}", str(d["chapter"])))
      .replace("__PY__", d["python"]).replace("__DATA__", safe(d)).replace("__QUIZ__", safe(json.load(open(os.path.join(P, "quiz.json")))))
      .replace("__OBJ__", safe(json.load(open(os.path.join(P, "objectives.json"))))).replace("__CORPUS__", "\n".join(blocks)))
out = os.path.join(REPO, "03-materials", "ch%s" % N, "page", "sen0414_ch%s_page_v%s.html" % (N, os.environ.get("PAGE_VER", "4_0_1")))
open(out, "w").write(h); json.dump(log, open(os.path.join(P, "corpus_manifest.json"), "w"), indent=1)
print("written", out, len(h), "bytes; corpus:", "; ".join(log))
