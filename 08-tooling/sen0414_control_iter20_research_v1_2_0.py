#!/usr/bin/env python3
"""sen0414_control_iter20_research v1_2_0 (over v1_1_0, which stays as committed: the page ABox may be named for v9_95_0 (the brief) or for the page version it describes; it must name the page file it describes inside, and the page file must be the newest page) (over v1_0_0, which stays as committed: the page and the page ABox are those of the NEWEST page version of the chapter, v9_95_0 or above - the chapter 11 page was repaired to v9_96_0; the chapter check run is v1_2_0, which prints the page it tested) (a NEW file; model: sen0414_control_iter19_research_v1_3_0.py, which stays as committed) - the lineage agent's own control of the research tasks of Iter_20 (criterion ex:AC2F_RetrofitResearch20), chapters 10 to 25.
Usage: sen0414_control_iter20_research_v1_0_0.py researchNN        NN = 10..25
Asserts, from the controller's own runs (log control-iter20-logs/rc20_Research_ChNN.log, written here):
 (1) the first page ABox sen0414_chNN_page_abox_v9_95_0.ttl exists, is a new file, and the page v9_95_0 it describes was not modified after it was added;
 (2) the chapter check Research/ChNN (sen0414_lineage_chapter_check_v1_1_0.py, run now) ends 'RESULT Research/ChNN: PASS': 'OVERALL: PASS', Stage4.A, B, cov, sub, src PASS on the page ABox, HermiT consistent, 0 mismatches; Cross.B is CANNOT_RUN or PASS, never FAIL, and CANNOT_RUN is not counted as a pass;
 (3) where a research file kind has a version newer than the newest committed at the Iter_20 base, the old and the new files are compared by local name (sen0414_control_iter19_compare_v1_0_0.py): no individual, class or label missing, no link missing except version metadata (versionIRI, wasRevisionOf), sources missing are printed; where none is newer the research files were not rebuilt, which is the criterion's rule when the check passed before (the pre-run log pre_Research_ChNN.log is read and must end PASS);
 (4) no committed file of the chapter is modified since the base (only additions), everything of the chapter is committed.
Exit 0 only when every assertion holds."""
__version__ = "1.2.0"
import glob, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_control_iter18_v1_0_0 as C
import sen0414_control_iter19_v1_1_0 as D

REPO, T, ok = C.REPO, C.T, C.ok
BASE = "a83369e"
LOGS = os.path.join(T, "control-iter20-logs")
PY = "/home/claude/venv314/bin/python"
KINDS = ("document", "domain_tbox", "domain_abox", "domain_shacl", "research")


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True, text=True, cwd=REPO).stdout


def line(k, s):
    m = re.search(r"^%-11s old\s+(\d+)\s+new\s+(\d+)\s+missing from new\s+(\d+)" % k, s, re.M); return tuple(int(x) for x in m.groups()) if m else None


def research(n):
    R = "03-materials/ch%s/rdodi/sen0414_ch%s_" % (n, n)
    pvs = [tuple(int(x) for x in re.search(r"_page_v(\d+)_(\d+)_(\d+)\.html$", f).groups()) for f in glob.glob(os.path.join(REPO, "03-materials/ch%s/page/sen0414_ch%s_page_v*.html" % (n, n)))]
    pv = "%d_%d_%d" % max(v for v in pvs if v >= (9, 95, 0))
    cand = [x for x in ("03-materials/ch%s/page/sen0414_ch%s_page_abox_v%s.ttl" % (n, n, v) for v in (pv, "9_95_0")) if os.path.exists(os.path.join(REPO, x))]
    pa = cand[0] if cand else "03-materials/ch%s/page/sen0414_ch%s_page_abox_v%s.ttl" % (n, n, pv)
    pg_named = os.path.exists(os.path.join(REPO, pa)) and ("sen0414_ch%s_page_v%s.html" % (n, pv)) in open(os.path.join(REPO, pa), encoding="utf-8").read()
    ok(pg_named, "the page ABox %s names the page file it describes, sen0414_ch%s_page_v%s.html (the newest page)" % (os.path.basename(pa), n, pv))
    pg = "03-materials/ch%s/page/sen0414_ch%s_page_v%s.html" % (n, n, pv)
    ok(os.path.exists(os.path.join(REPO, pa)) and git("ls-tree", BASE, "--", pa).strip() == "", "the first page ABox %s (named for the page version it describes, %s) exists and is a new file (not in the base commit)" % (os.path.basename(pa), pv))
    ok(git("log", "--diff-filter=M", "--format=%h", "--", pg).strip() == "" and os.path.exists(os.path.join(REPO, pg)), "the page v%s was not modified after it was added by the page task" % pv + "")
    log = os.path.join(LOGS, "rc20_Research_Ch%s.log" % n)
    r = subprocess.run(["python3", os.path.join(T, "sen0414_lineage_chapter_check_v1_2_0.py"), "Research/Ch%s" % n], capture_output=True, text=True, cwd=REPO); t = r.stdout + r.stderr
    open(log, "w", encoding="utf-8").write(t)
    ok(r.returncode == 0 and "RESULT Research/Ch%s: PASS" % n in t and "OVERALL: PASS" in t and "HermiT: consistent" in t and re.search(r"\b0 mismatches", t) is not None, "chapter check Research/Ch%s (the controller's own run, exit %d): %s" % (n, r.returncode, re.findall(r"^(RESULT[^\n]*)", t, re.M)))
    ok(all("[PASS" in l for l in t.splitlines() if re.match(r"\[\w+\s*\] Stage4\.(cov|sub|src|B|A)", l)) and all(("Stage4." + k) in t for k in ("A", "B", "cov", "sub", "src")), "Stage4 A, B, cov, sub, src all present and PASS on the new page ABox")
    cb = re.search(r"Cross\.B[^\n]*", t)
    ok(bool(cb) and "FAIL" not in cb.group(0), "Cross.B does not FAIL (%s); CANNOT_RUN is reported openly and NOT counted as a pass" % (cb.group(0)[:120] if cb else "absent"))
    rebuilt = []
    for fn in KINDS:
        fs = sorted(glob.glob(os.path.join(REPO, R + fn + "_v*.ttl")), key=D.vkey)
        old = [f for f in fs if git("ls-tree", BASE, "--", os.path.relpath(f, REPO)).strip()]
        if fs and old and fs[-1] != old[-1]:
            rebuilt.append((fn, os.path.relpath(old[-1], REPO), os.path.relpath(fs[-1], REPO)))
    if rebuilt:
        cmp_ = os.path.join(T, "sen0414_control_iter19_compare_v1_0_0.py")
        olds = ",".join(x[1] for x in rebuilt); news = ",".join(x[2] for x in rebuilt)
        rc, out = C.run([PY, cmp_, n, olds, news])
        miss = re.findall(r"MISSING links: \((.*)\)", out)
        ok(all(line(k, out) and line(k, out)[2] == 0 for k in ("individuals", "classes", "labels")), "rebuilt research files %s, old against new (by local name): individuals %s, classes %s, labels %s (old, new, missing)" % ([x[0] for x in rebuilt], line("individuals", out), line("classes", out), line("labels", out)))
        ok(all(re.search(r"'(versionIRI|wasRevisionOf)'", m) for m in miss), "rebuilt research files: the %d links missing are version metadata only" % len(miss))
        print("INFO sources missing (judged by the controller):", re.findall(r"MISSING sources: (.*)", out))
    else:
        pre = open(os.path.join(LOGS, "pre_Research_Ch%s.log" % n), encoding="utf-8").read()
        ok("RESULT Research/Ch%s: PASS" % n in pre, "the research files were not rebuilt, and the check passed before the retrofit (pre-run log): nothing was changed for its own sake")
    d = git("diff", "--name-status", BASE, "HEAD", "--", "03-materials/ch%s" % n, "08-tooling/ch%s-page" % n, "08-tooling/ch%s-deck" % n).splitlines()
    ok(bool(d) and all(l.startswith("A") for l in d), "nochange: since %s the chapter folders have %d added files and no modified or deleted one" % (BASE, len(d)))
    un = git("status", "--porcelain", "--", "03-materials/ch%s" % n).strip(); ok(un == "", "everything of the chapter is committed (uncommitted: %s)" % (un.replace("\n", "; ")[:200] or "none"))


def main():
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    assert re.fullmatch(r"research(1\d|2[0-5])", c), __doc__
    research(c[8:])
    print("RESULT %s (%d failed assertion(s))" % ("FAIL" if C.BAD else "PASS", len(C.BAD))); sys.exit(1 if C.BAD else 0)


if __name__ == "__main__":
    main()
