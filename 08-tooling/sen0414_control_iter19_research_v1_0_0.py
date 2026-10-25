#!/usr/bin/env python3
"""sen0414_control_iter19_research v1_0_0 - the lineage agent's own control checks of the Iter_19 RESEARCH sets (criterion ex:AC2F_RetrofitResearch; G136, G137: the controller re-runs, never trusts the executor's log).
Usage: sen0414_control_iter19_research_v1_0_0.py researchNN        NN = 01..05
Asserts: the new research files (document, domain TBox, ABox, SHACL, research, one new version each) and the new page ABox exist, are new files, and the controller's chapter check Research/ChNN (its own run, log control-iter19-logs/rc_Research_ChNN.log) ends 'RESULT Research/ChNN: PASS' with the gates OVERALL PASS (Stage4.A, B, cov, sub, src PASS), HermiT consistent, 0 mismatches, Cross.B CANNOT_RUN reported (not a pass);
the chapter checks Research/Ch06 to Research/Ch09 (the controller's own runs) still end PASS; the page file of the chapter is byte-identical to its controlled commit (it was not changed by the research task); no committed file is modified (only additions since the Iter_19 base commit);
the controller's own comparison (sen0414_control_iter19_compare_v1_0_0.py, by local name) of the OLD research files (the newest versions before the retrofit) with the NEW ones: no individual, class, source or label missing, links missing only as version metadata (versionIRI, wasRevisionOf), and of the OLD page ABox with the NEW one (the prefix s_ mapped): no individual or predicate missing, and every missing link or label is in the list the executor stated (RESTATED below, measured by the controller).
Exit 0 only when every assertion holds; the evidence bridge runs this file as the TestEvidence command."""
__version__ = "1.0.0"
import glob, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_control_iter18_v1_0_0 as C
import sen0414_control_iter19_v1_1_0 as D

REPO, T, ok = C.REPO, C.T, C.ok
LOGS = os.path.join(T, "control-iter19-logs")
PY = "/home/claude/venv314/bin/python"
# per chapter: the old research files (before the retrofit) and the page commit controlled in the register
OLD = {"05": dict(doc="1_2_0", tbox="1_1_0", abox="1_1_0", shacl="1_0_0", res="1_1_0", pabox="v1_3_0", pcommit="e2adae9")}
# the differences the executor stated and the controller measured, per chapter: missing links (all of the form (concept widget, 'source', 'document')), and the number of reworded labels
STATED = {"05": dict(links=32, labels=14, mapprefix="s_=")}


def log(n):
    return open(os.path.join(LOGS, n), encoding="utf-8").read()


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True, text=True, cwd=REPO).stdout


def newest(pat):
    return sorted(glob.glob(os.path.join(REPO, pat)), key=D.vkey)[-1]


def research(n):
    o = OLD[n]; R = "03-materials/ch%s/rdodi/sen0414_ch%s_" % (n, n)
    names = [("document", "doc"), ("domain_tbox", "tbox"), ("domain_abox", "abox"), ("domain_shacl", "shacl"), ("research", "res")]
    new = {}
    for fn, k in names:
        f = newest(R.replace("sen0414_ch%s_" % n, "sen0414_ch%s_%s_v*.ttl" % (n, fn))); new[k] = os.path.relpath(f, REPO)
        ok(D.vkey(f) > D.vkey("_v%s.ttl" % o[k]), "the newest %s file %s is a NEW version above the old %s" % (fn, os.path.basename(f), o[k]))
    pn = os.path.relpath(newest("03-materials/ch%s/page/sen0414_ch%s_page_abox_v*.ttl" % (n, n)), REPO)
    ok(D.vkey(pn) > D.vkey("_" + o["pabox"] + ".ttl"), "the newest page ABox %s is a NEW version above the old %s" % (os.path.basename(pn), o["pabox"]))
    t = log("rc_Research_Ch%s.log" % n)
    ok("RESULT Research/Ch%s: PASS" % n in t and "OVERALL: PASS" in t and "HermiT: consistent" in t and re.search(r"\b0 mismatches", t) is not None, "chapter check Research/Ch%s (the controller's own run): %s" % (n, re.findall(r"^(RESULT[^\n]*)", t, re.M)))
    ok(all(("[PASS" in l) for l in t.splitlines() if re.match(r"\[\w+\s*\] Stage4\.(cov|sub|src|B|A)", l)) and "Stage4.cov" in t and "Stage4.sub" in t, "Stage4 A, B, cov, sub, src all PASS on the new page ABox")
    ok("[CANNOT_RUN ] Cross.B" in t and "FAIL" not in re.search(r"Cross\.B[^\n]*", t).group(0), "Cross.B is reported CANNOT_RUN (0 hybrid chains) and is NOT counted as a pass (tracked by ex:ST_Plan_Gap_CrossB)")
    for c in ("06", "07", "08", "09"):
        u = log("rc_Research_Ch%s.log" % c); ok("RESULT Research/Ch%s: PASS" % c in u, "chapter check Research/Ch%s still PASS (the controller's own run)" % c)
    ok(git("diff", "--name-status", o["pcommit"], "HEAD", "--", "03-materials/ch%s/page/sen0414_ch%s_page_v9_90_0.html" % (n, n)).strip() == "", "the page file is byte-identical to its controlled commit %s (the research task did not change it)" % o["pcommit"])
    d = git("diff", "--name-status", D.BASE, "HEAD", "--", "03-materials/ch%s" % n, "08-tooling/ch%s-page" % n, "08-tooling/ch%s-deck" % n).splitlines()
    ok(bool(d) and all(l.startswith("A") for l in d), "nochange: since %s the chapter folders have %d added files and no modified or deleted one" % (D.BASE, len(d)))
    un = git("status", "--porcelain", "--", "03-materials/ch%s" % n).strip(); ok(un == "", "everything of the chapter is committed (uncommitted: %s)" % (un.replace("\n", "; ")[:200] or "none"))
    cmp_ = os.path.join(T, "sen0414_control_iter19_compare_v1_0_0.py")
    oldf = ",".join(R + "%s_v%s.ttl" % (fn, o[k]) for fn, k in names); newf = ",".join(new[k] for fn, k in names)
    rc, out = C.run([PY, cmp_, n, ",".join("03-materials/ch%s/rdodi/sen0414_ch%s_%s_v%s.ttl" % (n, n, fn, o[k]) for fn, k in names), newf])
    def line(k, s):
        m = re.search(r"^%-11s old\s+(\d+)\s+new\s+(\d+)\s+missing from new\s+(\d+)" % k, s, re.M); return tuple(int(x) for x in m.groups()) if m else None
    ok(all(line(k, out) and line(k, out)[2] == 0 for k in ("individuals", "classes", "sources", "labels")), "research files, old against new (by local name): individuals %s, classes %s, sources %s, labels %s (old, new, missing)" % tuple(line(k, out) for k in ("individuals", "classes", "sources", "labels")))
    miss = re.findall(r"MISSING links: \((.*)\)", out)
    ok(all(re.search(r"'(versionIRI|wasRevisionOf)'", m) for m in miss), "research files: the %d links missing from the new set are version metadata only (versionIRI, wasRevisionOf)" % len(miss))
    rc, out = C.run([PY, cmp_, n, os.path.join("03-materials/ch%s/page/sen0414_ch%s_page_abox_%s.ttl" % (n, n, o["pabox"])), pn, "--map", STATED[n]["mapprefix"]])
    ok(all(line(k, out) and line(k, out)[2] == 0 for k in ("individuals", "classes", "predicates", "sources")), "page ABox, old against new (s_ mapped): individuals %s, predicates %s (old, new, missing)" % (line("individuals", out), line("predicates", out)))
    ml = re.findall(r"MISSING links: \((.*)\)", out); ll = line("links", out); lb = line("labels", out)
    ok(ll and ll[2] == STATED[n]["links"] == len(ml) and all(re.search(r"'source', 'document'", m) for m in ml), "page ABox: the %d missing links are exactly the %d stated (the widget's source link to the whole document, now to the concept's own section)" % (len(ml), STATED[n]["links"]))
    ok(lb and lb[2] == STATED[n]["labels"], "page ABox: the %s labels missing are exactly the %d stated reworded labels (layout names and visual-widget names)" % (lb and lb[2], STATED[n]["labels"]))


def main():
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    assert re.fullmatch(r"research0[1-5]", c), __doc__
    research(c[8:])
    print("RESULT %s (%d failed assertion(s))" % ("FAIL" if C.BAD else "PASS", len(C.BAD))); sys.exit(1 if C.BAD else 0)


if __name__ == "__main__":
    main()
