#!/usr/bin/env python3
"""sen0414_control_iter20_page v1_1_0 (over v1_0_0, which stays as committed: the new page is the newest page v9_95_0 or above, through sen0414_control_iter20_pagetests_v1_1_0) (a NEW file over sen0414_control_iter19_page_v1_5_0.py, which stays as committed; chapters 10 to 25: the new page is v9_95_0, the base is the register commit that planned Iter_20, the earlier newest page and its stored test result are found per chapter, the story-layout evidence is the log of the story-layout probe v1_0_0)
Usage: sen0414_control_iter20_page_v1_0_0.py pageNN        NN = 10..25
pageNN controls the new page v9_95_0 of chapter NN: static (charset below byte 512, comment openers equal closers, page-standard meta and template 9.52.2 header, the chapter-code tab data equals the manifest which equals the deck's code boxes, stories embedded as data URIs, no committed file modified since the base, everything committed, the first-line error scan of the manifest), dynamic (the controller's own serial runs under the lock by sen0414_control_iter20_pagetests_v1_0_0.py: 9.37.0 passes with equal widgets, P2/P11/P12 pass, no [FAIL] and no [SKIP]; 9.34.0 on the new page and on the earlier newest page, not below), and the story-layout probe on every story at 1366x768, 1400x900 and 390x844.
Exit 0 only when every assertion holds; the evidence bridge runs this file as the TestEvidence command."""
__version__ = "1.1.0"
import glob, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_control_iter18_v1_0_0 as C
import sen0414_control_iter20_deck_v1_0_0 as D
from sen0414_control_iter20_pagetests_v1_1_0 import PV, old_ver

REPO, T, ok, off = C.REPO, C.T, C.ok, C.off
LOGS = os.path.join(T, "control-iter20-logs")
RES = re.compile(r"^page (\d\d): exit 0, widgets \('(\d+)', '(\d+)'\), features passed (\d+), failed (\d+),", re.M)


def log(n):
    return open(os.path.join(LOGS, n), encoding="utf-8").read()


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True, text=True, cwd=REPO).stdout


def page(n):
    pdir = "03-materials/ch%s/page" % n
    P = os.path.join(REPO, pdir, "sen0414_ch%s_page_v%s.html" % (n, PV(n)))
    ok(os.path.exists(P), "the page v%s of chapter %s exists" % (PV(n), n))
    mfs = sorted(glob.glob(os.path.join(REPO, pdir, "chapter_code_ch%s_v*.json" % n)), key=D.vkey); MF = mfs[-1]
    html = open(P, "rb").read().decode("utf-8")
    o = off(P); ok(o is not None and o < 512, "first <meta charset> at byte %s (limit: below 512)" % o)
    ok(html.count("<!--") == html.count("-->"), "%d comment openers, %d closers" % (html.count("<!--"), html.count("-->")))
    ok('name="page-standard"' in html and "course_page_template version 9.52.2" in html, "the page declares page-standard and carries the template 9.52.2 header")
    m = re.search(r'<script type="application/json" id="data">(.*?)</script>', html, re.S); d = json.loads(m.group(1)); cc = d["chaptercode"]["examples"]; mf = json.load(open(MF, encoding="utf-8"))["examples"]
    ok(len(cc) == len(mf) > 0, "the page lists %d examples, the manifest %d" % (len(cc), len(mf)))
    ok([(e["order"], e["name"], e["code"]) for e in cc] == [(e["order"], e["name"], e["code"]) for e in mf], "M1: the chapter-code tab data equals the manifest in order, names and code")
    print("  OBSERVATION (not an assertion; chapters 6 to 9 are controlled with the same relation): the Chapter examples (Lab/Playground) pane has %d examples, the manifest %d; the pane equals the manifest's code in order: %s" % (len(d["examples"]), len(mf), [e["code"] for e in d["examples"]] == [e["code"] for e in mf]))
    deck = sorted(glob.glob(os.path.join(REPO, "03-materials/ch%s/SEN0414_Ch%s_*.pptx" % (n, n))), key=D.vkey)[-1]
    rc, out = C.run([sys.executable, os.path.join(T, "sen0414_deck_standard_check_v1_0_0.py"), n, os.path.relpath(deck, REPO)]); m1 = re.search(r"^M1 PASS .*?(\d+) of (\d+)", out, re.M)
    ok(bool(m1) and m1.group(1) == m1.group(2) == str(len(cc)), "the manifest equals the code boxes of the newest deck %s: %s" % (os.path.basename(deck), m1.group(0)[:120] if m1 else "no M1 PASS"))
    st = d.get("stories") or []; want = sum(len(s.get("imgs", [])) for s in st)
    ok(len(st) >= 3 and want >= 1 and len(re.findall(r"data:image/(?:jpeg|png|webp|svg\+xml);base64,", html)) >= want, "the page carries %d stories and embeds their %d picture(s) as data URIs" % (len(st), want))
    diff = git("diff", "--name-status", D.BASE, "HEAD", "--", "03-materials/ch%s" % n, "08-tooling/ch%s-page" % n, "08-tooling/ch%s-deck" % n).splitlines()
    ok(bool(diff) and all(l.startswith("A") for l in diff), "nochange: since the register commit %s the chapter folders have %d added files and no modified or deleted one" % (D.BASE, len(diff)))
    un = git("status", "--porcelain", "--", "03-materials/ch%s" % n, "08-tooling/ch%s-page" % n).strip()
    ok(un == "", "everything of the chapter page is committed (uncommitted: %s)" % (un.replace("\n", "; ")[:240] or "none"))
    a = log("p37_ch%s_t37.log" % n); r = RES.search(a)
    ok(bool(r) and r.group(2) == r.group(3) and r.group(5) == "0" and "test file: sen0414_page_test_v9_37_0.py" in a and "RESULT: PASS" in a and "[FAIL]" not in a, "page test 9.37.0 (runner v1_1_0, the controller's own serial run under the lock): %s" % (r.group(0)[:100] if r else "no result line"))
    ok("[PASS] P2 every chapter-code example" in a and "[PASS] P11" in a and "[PASS] P12" in a, "9.37.0 ran the P features (P2 run of every chapter-code example, P11, P12) and they pass")
    ok("[SKIP]" not in a, "no feature is skipped in the 9.37.0 run")
    b = log("p37_ch%s_t34.log" % n); c = log("p37_ch%s_t34_old.log" % n); nb, nc = RES.search(b), RES.search(c)
    ok(bool(nb) and nb.group(5) == "0" and nb.group(2) == nb.group(3) and "RESULT: PASS" in b and "[FAIL]" not in b, "page test 9.34.0 on the new page: %s" % (nb.group(0)[:100] if nb else "none"))
    ok(bool(nc) and nc.group(5) == "0", "page test 9.34.0 on the existing page v9_28_0 (the controller's own run): %s" % (nc.group(0)[:100] if nc else "none"))
    ok(bool(nb and nc) and int(nb.group(3)) >= int(nc.group(3)) and int(nb.group(4)) >= int(nc.group(4)), "widgets and features of the new page are not below the existing page's")
    ok(len(re.findall(r"\[SKIP\]", b)) <= len(re.findall(r"\[SKIP\]", c)), "skipped under 9.34.0: new page %d, existing page %d (not more)" % (len(re.findall(r"\[SKIP\]", b)), len(re.findall(r"\[SKIP\]", c))))
    sto = json.load(open(os.path.join(T, "ch%s-page/test_results_v%s.json" % (n, old_ver(n))), encoding="utf-8"))
    ok(bool(nb) and int(nb.group(3)) >= len(sto["widgets"]), "widgets of the new page are not below the stored result of the existing page (%d)" % len(sto["widgets"]))
    sf = log("p37_ch%s_storyfit.log" % n)
    ok("RESULT: PASS" in sf and "FAIL" not in sf, "story layout (the first story as the reader sees it, without scrolling) at 1366x768, 1400x900 and 390x844: %d story/viewport checks pass, the photograph lower than the viewport, the narrative paragraph beginning within the first screen of the story" % len(re.findall(r"^PASS", sf, re.M)))


def main():
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    assert re.fullmatch(r"page(1[0-9]|2[0-5])", c), __doc__
    page(c[4:])
    print("RESULT %s (%d failed assertion(s))" % ("FAIL" if C.BAD else "PASS", len(C.BAD))); sys.exit(1 if C.BAD else 0)


if __name__ == "__main__":
    main()
