#!/usr/bin/env python3
"""sen0414_control_iter18 v1_5_0 - the lineage agent's own control checks of the Iter_18 executor results (G136, G137: the controller re-runs, never trusts the executor's log).
Usage: sen0414_control_iter18_v1_5_0.py CHECK      CHECK = pagetest37 | page09   (every earlier CHECK: see v1_4_0, which stays as committed and is imported)
v1.5.0 (over 1.4.0): adds pagetest37 (the page test 9.37.0 over 9.36.0) and page09 (the chapter 9 page v9_90_0 under 9.37.0 and 9.34.0).
The page-test runs (about 8 to 12 minutes each) are read from the logs the lineage agent kept in 08-tooling/control-iter18-logs/ (p37_*: run by the lineage agent's own driver, serially under /tmp/page_test.lock, with a TEST release key, outside the executors' sessions); the fixtures of the controller are its own pages, made from the committed page of chapter 6.
Exit 0 only when every assertion holds; the evidence bridge runs this file as the TestEvidence command."""
__version__ = "1.5.0"
import difflib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_control_iter18_v1_0_0 as C
import sen0414_control_iter18_v1_4_0 as V

REPO, T, LOGS = C.REPO, C.T, C.LOGS
ok, sha, log, off = C.ok, C.sha, C.log, C.off
SHA36 = "86c1c1f8ed979d90ca392a3e26439dc8f7046d37b633dcb705dfc44197f58d05"
RES = re.compile(r"^page (\d\d): exit 0, widgets \('(\d+)', '(\d+)'\), features passed (\d+), failed (\d+),", re.M)


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True, text=True, cwd=REPO).stdout


def pagetest37():
    f36, f37 = os.path.join(T, "sen0414_page_test_v9_36_0.py"), os.path.join(T, "sen0414_page_test_v9_37_0.py")
    ok(sha(f36) == SHA36, "9.36.0 is byte-identical to the recorded SHA-256 %s" % SHA36[:12])
    ok(sha(os.path.join(T, "sen0414_page_test_v9_34_0.py")) == C.OLD["sen0414_page_test_v9_34_0.py"], "9.34.0 is byte-identical to the recorded SHA-256")
    for f in ("sen0414_page_test_v9_36_0.py", "sen0414_page_test_v9_34_0.py", "sen0414_page_test_run_v1_1_0.py"):
        ok(git("log", "--format=%h", "--", "08-tooling/" + f).split().__len__() == 1, "%s has one commit in git (never edited after it was committed)" % f)
    a = open(f36, encoding="utf-8").read().splitlines(); b = open(f37, encoding="utf-8").read().splitlines()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False); removed, added, spans = [], [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            removed += a[i1:i2]; added += b[j1:j2]; spans.append((i1 + 1, i2))
    ok(len(removed) == 4, "the diff against 9.36.0 removes exactly 4 lines (the version line, the MAN line, the wait, the error check): %d" % len(removed))
    ok(any("__version__" in l for l in removed) and any(l.strip() == "MAN = None" for l in removed) and any("wait_for_function" in l and "data-cc-result" in l for l in removed) and any("Traceback|NameError|Error:" in l for l in removed), "the four removed lines are those")
    ok(all(1 <= s <= 8 or 1470 <= s <= 1490 or 1590 <= s <= 1610 for s, e in spans), "every change lies in the header or in the P2 chapter-code step (lines %s)" % spans)
    ok(any('__version__ = "9.37.0"' in l for l in added) and any("ex:CR2_Retest37" in l for l in added), "(a) the version line is 9.37.0 and a comment names the change request")
    ok(any(r"Running(\\.\\.\\.|\\u2026)" in l and "wait_for_function" in l and "timeout=90000" in l for l in added), "(b) the wait ends when the placeholder 'Running...' (three dots or the ellipsis) is gone, same 90 s bound")
    ok(any("EXPECTED" in l and "expected" in l for l in added) and any("_tok not in _exp" in l for l in added), "(c) an error name is flagged only when it is not part of the example's recorded expected result")
    ok(len(added) == 8, "the diff adds exactly 8 lines (the version line, the comment, MAN with EXPECTED, the EXPECTED map, the wait, the 3 lines of the error check): %d" % len(added))
    d = git("diff", "76c2156", "e0af2eb", "--", "08-tooling/sen0414_page_test_v9_37_0.py")
    ch = [l for l in d.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    ok(len(ch) == 2 and r"\w*" in ch[0] and "[A-Za-z_]*" in ch[1], "DISCLOSED: the executor edited its OWN new file once more after its first commit (e0af2eb over 76c2156): one line, the error-name token regex \\w* became [A-Za-z_]*; 9.36.0 untouched")
    for ch_, v_ in (("06", None), ("07", None), ("08", None)):
        t = log("p37_ch%s_t37.log" % ch_); m = RES.search(t)
        ok(bool(m) and m.group(2) == m.group(3) and m.group(5) == "0" and "test file: sen0414_page_test_v9_37_0.py" in t and "RESULT: PASS" in t and "[FAIL]" not in t, "9.37.0 on the page of chapter %s v9_90_0 (runner v1_1_0): %s" % (ch_, m.group(0)[:100] if m else "no result line"))
    for ch_, old in (("07", "c7_t36_new.log"), ("08", "c8_t36_new.log")):
        n37 = RES.search(log("p37_ch%s_t37.log" % ch_)); n36 = RES.search(log(old))
        ok(bool(n37 and n36) and n37.group(2) == n36.group(2) and n37.group(4) == n36.group(4), "chapter %s: 9.37.0 has the same widgets (%s) and features (%s) as the 9.36.0 run (%s, %s)" % (ch_, n37.group(2), n37.group(4), n36.group(2), n36.group(4)))
    t = log("p37_ch06_t37.log")
    ok("[PASS] P2 every chapter-code example" in t and "[FAIL]" not in t, "chapter 6 page: the P2 run feature, which 9.36.0 failed on examples 2 and 24, passes under 9.37.0")
    for name, want in (("c1_text_only", "FAIL"), ("c2_crash", "FAIL"), ("c3_slow", "PASS"), ("c4_expected_error", "PASS")):
        t = log("p37_%s.log" % name); fl = [l for l in t.splitlines() if "[FAIL]" in l]
        if want == "FAIL":
            ok(any("P2 every chapter-code example" in l for l in fl) and re.search(r"^RESULT: FAIL", t, re.M) is not None, "fixture %s fails the P2 run feature (%d [FAIL] lines)" % (name, len(fl)))
        else:
            ok(not fl and re.search(r"^RESULT: PASS", t, re.M) is not None and "page 06: exit 0" in t, "fixture %s passes (no [FAIL])" % name)
    ok(all("test file: sen0414_page_test_v9_37_0.py" in log("p37_%s.log" % n) for n in ("c1_text_only", "c2_crash", "c3_slow", "c4_expected_error")), "the four fixtures ran under 9.37.0")
    for f in ("c1_text_only", "c2_crash", "c3_slow", "c4_expected_error"):
        ok("page file substituted" in log("p37_%s.log" % f), "fixture %s is a page outside the repository (a key-substituted scratch copy)" % f)


def compare34(ch, tag):
    """element (2) of a page criterion: the page test 9.34.0 reports no failure on the new page, widgets and features not below the existing page's run, skipped not more (both runs are the controller's own, serial under the lock)"""
    b = log("p37_ch%s_t34.log" % ch); c = log("p37_ch%s_t34_old.log" % ch); nb = RES.search(b); nc = RES.search(c)
    ok(bool(nb) and nb.group(5) == "0" and nb.group(2) == nb.group(3) and "RESULT: PASS" in b and "test file: sen0414_page_test_v9_34_0.py" in b and "[FAIL]" not in b, "page test 9.34.0 on the new page of chapter %s: %s" % (ch, nb.group(0)[:100] if nb else "none"))
    ok(bool(nc) and nc.group(5) == "0", "page test 9.34.0 on the existing page v9_28_0 of chapter %s (the controller's own run): %s" % (ch, nc.group(0)[:100] if nc else "none"))
    ok(bool(nb and nc) and int(nb.group(3)) >= int(nc.group(3)) and int(nb.group(4)) >= int(nc.group(4)), "widgets and features of the new page (%s, %s) are not below the existing page's (%s, %s)" % (nb.group(3), nb.group(4), nc.group(3), nc.group(4)))
    sk = lambda t: len(re.findall(r"\[SKIP\]", t))
    ok(sk(b) <= sk(c), "skipped: new page %d, existing page %d (not more)" % (sk(b), sk(c)))
    st = json.load(open(os.path.join(T, "ch%s-page/test_results_v9_28_0.json" % ch), encoding="utf-8"))
    ok(int(nb.group(3)) >= len(st["widgets"]), "widgets of the new page (%s) are not below the stored result of the existing page (%d)" % (nb.group(3), len(st["widgets"])))


MAN9 = "03-materials/ch09/page/chapter_code_ch09_v1_0_0.json"; P9 = "03-materials/ch09/page/sen0414_ch09_page_v9_90_0.html"; PAGE9_COMMIT = "fcf1173"


def page09():
    P = os.path.join(REPO, P9); MF = os.path.join(REPO, MAN9); html = open(P, "rb").read().decode("utf-8")
    ok(git("log", "--format=%h", "--", MAN9).split()[-1:] == ["7ada4a9"], "the chapter-code manifest is the one committed with the controlled deck (commit 7ada4a9) and is unchanged since")
    o = off(P); ok(o is not None and o < 512, "page v9_90_0: first <meta charset> at byte %s (limit: below 512)" % o)
    ok(html.count("<!--") == html.count("-->"), "page v9_90_0: %d comment openers, %d closers" % (html.count("<!--"), html.count("-->")))
    ok('name="page-standard"' in html and "course_page_template version 9.52.2" in html, "page declares page-standard and carries the template 9.52.2 header")
    m = re.search(r'<script type="application/json" id="data">(.*?)</script>', html, re.S); d = json.loads(m.group(1)); cc = d["chaptercode"]["examples"]; mf = json.load(open(MF, encoding="utf-8"))["examples"]
    ok(len(cc) == len(mf) == 25, "the page lists %d examples, the manifest %d" % (len(cc), len(mf)))
    ok([(e["order"], e["name"], e["code"]) for e in cc] == [(e["order"], e["name"], e["code"]) for e in mf], "M1: the chapter-code tab data equals the manifest (and so the deck's code) in order, names and code")
    ok(len(re.findall(r'data:image/(?:jpeg|png);base64,', html)) >= 4, "the page embeds the four story pictures as data URIs")
    mod = git("diff-tree", "--no-commit-id", "--name-status", "-r", PAGE9_COMMIT).splitlines()
    ok(bool(mod) and all(l.startswith("A") for l in mod), "nochange: commit %s adds %d files and modifies none" % (PAGE9_COMMIT, len(mod)))
    ok(git("diff", "--name-status", PAGE9_COMMIT, "HEAD", "--", P9, "08-tooling/ch09-page/stories_img_v2_0_0.json", "08-tooling/ch09-page/page_data_v9_90_0.json").strip() == "", "the page, its page data and the story-picture map are unchanged in git since the commit")
    ok(git("diff", "--name-status", "fcaefd1", "HEAD", "--", "08-tooling/ch09-page/stories_img_v1_0_0.json").strip() == "", "the story-picture map v1_0_0 is unchanged (the new map is a new file)")
    sj = json.load(open(os.path.join(T, "ch09-page/stories_img_v2_0_0.json"), encoding="utf-8")); fs = [x["file"] for k, v in sj.items() if not k.startswith("_") for x in v]
    ok(len(fs) == 4 and all(os.path.exists(os.path.join(REPO, "03-materials/ch09/assets", f)) for f in fs), "the map names 4 picture files and each exists in 03-materials/ch09/assets")
    prov = open(os.path.join(REPO, "03-materials/ch09/assets/ASSETS_PROVENANCE_v1_0_0.md"), encoding="utf-8").read(); ok(all(f in prov for f in fs), "every picture has a provenance line with its licence")
    a = log("p37_ch09_t37.log"); n = RES.search(a)
    ok(bool(n) and n.group(2) == n.group(3) == "63" and n.group(5) == "0" and "test file: sen0414_page_test_v9_37_0.py" in a and "RESULT: PASS" in a and "[FAIL]" not in a, "page test 9.37.0 through runner v1_1_0 on the page: %s" % (n.group(0)[:100] if n else "no result line"))
    compare34("09", "page09")
    ok(int(n.group(4)) >= 400 and "[PASS] P2 every chapter-code example" in a and "[PASS] P11 the page declares the standard" in a and "[PASS] P12" in a, "9.37.0 ran the P features (P2 run, P11, P12) and passed %s features" % n.group(4))
    ok(len(re.findall(r"\[SKIP\]", a)) == 0, "no feature is skipped in the 9.37.0 run")
    rc, out = C.run([sys.executable, os.path.join(T, "sen0414_lineage_chapter_check_v1_1_0.py"), "Research/Ch09"]); ok(rc == 0 and "RESULT Research/Ch09: PASS" in out, "chapter check Research/Ch09 (live): PASS")
    ok("[SKIP]" not in a, "no skip")


def main():
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    extra = {"pagetest37": pagetest37, "page09": page09}
    if c in extra:
        extra[c]()
    else:
        sys.argv = [sys.argv[0], c]; V.main(); return
    print("RESULT %s (%d failed assertion(s))" % ("FAIL" if C.BAD else "PASS", len(C.BAD))); sys.exit(1 if C.BAD else 0)


if __name__ == "__main__":
    main()
