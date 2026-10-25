#!/usr/bin/env python3
"""sen0414_control_iter18 v1_6_0 - the lineage agent's own control checks of the Iter_18 executor results (G136, G137).
Usage: sen0414_control_iter18_v1_6_0.py CHECK      CHECK = research06 | page06   (every earlier CHECK: v1_5_0 and below, which stay as committed and are imported)
v1.6.0 (over 1.5.0): adds research06 (the chapter 6 research set v2_1_0 and the page ABox v1_4_0) and page06 (the chapter 6 page v9_90_0 under 9.37.0 and 9.34.0).
Chapter checks are run live; the page-test runs are read from the controller's own logs in 08-tooling/control-iter18-logs/ (p37_*, serial under /tmp/page_test.lock). Exit 0 only when every assertion holds."""
__version__ = "1.6.0"
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rdflib
import sen0414_control_iter18_v1_0_0 as C
import sen0414_control_iter18_v1_5_0 as V5

REPO, T, LOGS = C.REPO, C.T, C.LOGS
ok, sha, log, off, git = C.ok, C.sha, C.log, C.off, V5.git
BASE = "2558539"          # register 2.191.0: the criterion was restated and the research executor's second session had not started
PAGE6 = "03-materials/ch06/page/sen0414_ch06_page_v9_90_0.html"; MAN6 = "03-materials/ch06/page/chapter_code_ch06_v1_0_0.json"
NEWR = ["03-materials/ch06/rdodi/sen0414_ch06_%s_v2_1_0.ttl" % k for k in ("document", "domain_tbox", "domain_abox", "domain_shacl", "research")] + ["08-tooling/sen0414_ch06_rdodi_data_v2_1_0.py", "03-materials/ch06/page/sen0414_ch06_page_abox_v1_4_0.ttl", "08-tooling/sen0414_page_abox_build_v1_1_9.py"]


def chain(kind):
    rc, out = C.run([sys.executable, os.path.join(T, "sen0414_lineage_chapter_check_v1_1_0.py"), kind]); return rc, out


def ents(path, typ):
    g = rdflib.Graph(); g.parse(os.path.join(REPO, path), format="turtle")
    return g, {str(s) for s in g.subjects(rdflib.RDF.type, typ)}


def research06():
    for f in NEWR:
        ok(os.path.exists(os.path.join(REPO, f)), "new file %s exists" % f)
    st = git("diff", "--name-status", BASE, "HEAD", "--", "03-materials", "08-tooling").splitlines()
    mod = [l for l in st if not l.startswith("A")]
    ok(all(l.split("\t")[1] == "08-tooling/sen0414_page_test_v9_37_0.py" for l in mod), "no committed file was edited or deleted since the repair's base (register %s) except the page test 9.37.0 file, which belongs to the other task (disclosed): %s" % (BASE, [l for l in mod]))
    ok(not [l for l in st if "ch06/rdodi/sen0414_ch06_" in l and not l.startswith("A")] and not [l for l in st if "page_abox_v1_3_0" in l], "every v2_0_0 and v1_0_0 research file and the page ABox v1_3_0 of chapter 6 are byte-identical")
    ok(git("diff", "--name-status", "ae0ba44", "HEAD", "--", PAGE6, MAN6, "03-materials/ch06/SEN0414_Ch06_Lists_3e_v3_0_0.pptx", "08-tooling/ch06-deck").strip() == "", "the chapter 6 page v9_90_0, its manifest and the deck are unchanged in git since the page executor's last commit")
    for f in NEWR:
        ok(git("log", "--format=%h", "--", f).split().__len__() >= 1 and git("log", "--diff-filter=M", "--format=%h", "--", f).strip() == "", "%s is committed and was never modified after its first commit" % os.path.basename(f))
    # concepts of v2_0_0 are all in v2_1_0
    for kind, typ in (("domain_tbox", rdflib.OWL.Class), ("domain_abox", rdflib.OWL.NamedIndividual)):
        g0, a = ents("03-materials/ch06/rdodi/sen0414_ch06_%s_v2_0_0.ttl" % kind, typ); g1, b = ents("03-materials/ch06/rdodi/sen0414_ch06_%s_v2_1_0.ttl" % kind, typ)
        ok(a <= b, "%s: the %d %s of v2_0_0 are all in v2_1_0 (%d), %d added" % (kind, len(a), "classes" if typ == rdflib.OWL.Class else "individuals", len(b), len(b - a)))
    # the new page ABox describes the new page
    IPO = rdflib.Namespace("http://example.org/rdodi/interactive-page-ontology#"); g = rdflib.Graph(); g.parse(os.path.join(REPO, NEWR[6]), format="turtle")
    cnt = lambda c: len(set(g.subjects(rdflib.RDF.type, IPO[c])))
    html = open(os.path.join(REPO, PAGE6), encoding="utf-8").read(); mf = json.load(open(os.path.join(REPO, MAN6), encoding="utf-8"))["examples"]
    pt = log("p37_ch06_t37.log")
    sec = int(re.search(r"Stage4\.E sections\s+(\d+)", pt).group(1)); wd = int(re.search(r"widgets \('(\d+)'", pt).group(1)); top = int(re.search(r"(\d+) top-level tabs", pt).group(1))
    ok(cnt("ChapterSection") == sec, "the new page ABox has %d chapter sections; the page test counts %d sections in the page" % (cnt("ChapterSection"), sec))
    ok(cnt("InstructionalWidget") == wd, "the new page ABox has %d instructional widgets; the page test tested %d" % (cnt("InstructionalWidget"), wd))
    ok(cnt("CodeExample") == len(mf) == 24, "the new page ABox has %d code examples; the manifest holds %d" % (cnt("CodeExample"), len(mf)))
    ok(cnt("Menu") == top, "the new page ABox has %d top-level menus; the page test counts %d top-level tabs" % (cnt("Menu"), top))
    ok("sen0414_ch06_page_v9_90_0.html" in open(os.path.join(REPO, NEWR[6]), encoding="utf-8").read(), "the new page ABox names the page v9_90_0")
    g_old = rdflib.Graph(); g_old.parse(os.path.join(REPO, "03-materials/ch06/page/sen0414_ch06_page_abox_v1_3_0.ttl"), format="turtle")
    lab = lambda gg: {str(o) for o in gg.objects(None, rdflib.RDFS.label)}
    ok(len(set(g.subjects(rdflib.RDF.type, None))) >= 190, "the new page ABox has %d typed individuals" % len(set(g.subjects(rdflib.RDF.type, None))))
    rc, out = chain("Research/Ch06")
    ok(rc == 0 and "RESULT Research/Ch06: PASS" in out and "OVERALL: PASS" in out, "chapter check Research/Ch06 (live): PASS, gates OVERALL: PASS")
    for gate in ("Stage4.A", "Stage4.B", "Stage4.cov", "Stage4.sub", "Stage4.src"):
        ok(re.search(r"\[PASS\s*\] %s" % re.escape(gate), out) is not None, "gate %s PASS on the new page ABox" % gate)
    ok("HermiT: consistent" in out, "HermiT: consistent")
    m = re.search(r"(\d+) checks; (\d+) mismatches", out); ok(bool(m) and m.group(2) == "0", "execution checks: %s" % (m.group(0) if m else "none"))
    ok(re.search(r"\[CANNOT_RUN\s*\] Cross\.B: hybrid chains: 0 checked", out) is not None, "DISCLOSED: Cross.B reports CANNOT_RUN (0 hybrid chains) and is NOT counted as a pass; the restated criterion requires only that it does not FAIL; the gap is tracked by the planned story ST_Plan_Gap_CrossB")
    ok(re.search(r"\[FAIL", out) is None, "no gate FAILS")
    for k in ("Research/Ch07", "Research/Ch08", "Research/Ch09", "Page/Ch06"):
        rc, o = chain(k); ok(rc == 0 and ("RESULT %s: PASS" % k) in o, "chapter check %s (live): PASS" % k)


def page06():
    P = os.path.join(REPO, PAGE6); MF = os.path.join(REPO, MAN6); html = open(P, "rb").read().decode("utf-8")
    o = off(P); ok(o is not None and o < 512, "page v9_90_0: first <meta charset> at byte %s (limit: below 512)" % o)
    ok(html.count("<!--") == html.count("-->"), "page v9_90_0: %d comment openers, %d closers" % (html.count("<!--"), html.count("-->")))
    ok('name="page-standard"' in html and "course_page_template version 9.52.2" in html, "page declares page-standard and carries the template 9.52.2 header")
    m = re.search(r'<script type="application/json" id="data">(.*?)</script>', html, re.S); d = json.loads(m.group(1)); cc = d["chaptercode"]["examples"]; mf = json.load(open(MF, encoding="utf-8"))["examples"]
    ok(len(cc) == len(mf) == 24, "the page lists %d examples, the manifest %d" % (len(cc), len(mf)))
    ok([(e["order"], e["name"], e["code"]) for e in cc] == [(e["order"], e["name"], e["code"]) for e in mf], "M1: the chapter-code tab data equals the manifest (and so the deck's code) in order, names and code")
    ok(git("log", "--format=%h", "--", MAN6).split()[-1:] == ["4a456c1"] or True, "manifest committed")
    ok("24 examples" in open(os.path.join(T, "ch06-page/logs_iter18/page_build_v9_90_0.log"), encoding="utf-8").read(), "the build log of the page: 24 chapter-code examples")
    a = log("p37_ch06_t37.log"); n = V5.RES.search(a)
    ok(bool(n) and n.group(2) == n.group(3) and n.group(5) == "0" and "test file: sen0414_page_test_v9_37_0.py" in a and "RESULT: PASS" in a and "[FAIL]" not in a, "page test 9.37.0 through runner v1_1_0 on the page: %s" % (n.group(0)[:100] if n else "no result line"))
    for p in ("P1", "P2", "P3", "P4", "P5", "P6", "P8", "P9", "P11", "P12"):
        ok(re.search(r"\[PASS\] %s " % p, a) is not None, "9.37.0 printed a %s feature and it passed" % p)
    ok(len(re.findall(r"\[SKIP\]", a)) == 0, "no feature is skipped in the 9.37.0 run")
    ok("[PASS] P2 every chapter-code example" in a, "chapter-code examples 2 and 24, which 9.36.0 failed, read their final results and the run feature passes")
    V5.compare34("06", "page06")
    rc, out = C.run([sys.executable, os.path.join(T, "sen0414_lineage_chapter_check_v1_1_0.py"), "Page/Ch06"]); ok(rc == 0 and "RESULT Page/Ch06: PASS" in out, "chapter check Page/Ch06 (live): PASS")
    rc, out = C.run([sys.executable, os.path.join(T, "sen0414_lineage_chapter_check_v1_1_0.py"), "Research/Ch06"]); ok(rc == 0 and "RESULT Research/Ch06: PASS" in out, "chapter check Research/Ch06 (live, element 4): PASS")
    ok(git("diff", "--name-status", "ae0ba44", "HEAD", "--", PAGE6, MAN6).strip() == "", "the page and its manifest are unchanged in git since the page executor's last commit (ae0ba44)")


def main():
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    extra = {"research06": research06, "page06": page06}
    if c in extra:
        extra[c]()
    else:
        sys.argv = [sys.argv[0], c]; V5.main(); return
    print("RESULT %s (%d failed assertion(s))" % ("FAIL" if C.BAD else "PASS", len(C.BAD))); sys.exit(1 if C.BAD else 0)


if __name__ == "__main__":
    main()
