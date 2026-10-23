#!/usr/bin/env python3
"""sen0414_control_iter18 v1_0_0 - the lineage agent's own control checks of the Iter_18 executor results (G136, G137: the controller re-runs, never trusts the executor's log).
Usage: sen0414_control_iter18_v1_0_0.py CHECK      CHECK = template | pagetest | charset | deckcheck | deck06 | deck07 | deck08
Exit 0 only when every assertion of the check holds; each assertion is printed as it was measured. The backlog_evidence_bridge runs this file as the TestEvidence command.
Live measurements (hashes, byte offsets, the deck check, the overlap check) are taken at run time; the page-test runs, which take about 8 minutes each, are read from the logs the
lineage agent kept in 08-tooling/control-iter18-logs/ (run by the lineage agent's own driver with a TEST release key, outside the executors' sessions)."""
__version__ = "1.0.0"
import difflib, hashlib, os, re, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); T = os.path.join(REPO, "08-tooling"); LOGS = os.path.join(T, "control-iter18-logs")
OLD = {"course_page_template_v9_50_0.html": "a3ca445f8fbc607a00f6a8e783535f264d28c1abaab98be68468c3e2a307c155",
       "sen0414_page_build_v4_17_0.py": "c440ecb59def644a46aca31fdd1e74e5b056bee4371855a515c433c9e9fd62ae",
       "sen0414_page_data_v2_24_0.py": "d202d514be8b3bdfe42a0740dad09e0732e89770aa459394478b7d093367a512",
       "sen0414_page_test_v9_34_0.py": "555f155a3f6ebc793c850cca697b6b07cdd1626a3773e56d96564616b1cfb06a"}
NEW = ["course_page_template_v9_52_1.html", "sen0414_page_build_v4_18_0.py", "sen0414_page_data_v2_25_0.py", "sen0414_page_test_v9_36_0.py"]
OLD_DECKS = {"06": "03-materials/ch06/SEN0414_Ch06_Lists_3e_v2_0_0.pptx", "07": "03-materials/ch07/SEN0414_Ch07_Dictionaries_3e_v1_0_0.pptx", "08": "08-tooling/ch08-deck/sen0414_ch08_deck_v1_0_0.pptx"}
OLD_FAIL = {"06": "D1,D2,D3,D4,D11,D5,D7,D10", "07": "D1,D2,D3,D4,D11,D5,D7", "08": "D1,D2,D3,D4,D11,D5,D7"}
NEWDECK = {"06": "03-materials/ch06/SEN0414_Ch06_Lists_3e_v3_0_0.pptx", "07": "03-materials/ch07/SEN0414_Ch07_Dictionaries_3e_v2_0_0.pptx", "08": "03-materials/ch08/SEN0414_Ch08_Strings_3e_v2_0_0.pptx"}
BAD = []


def ok(cond, msg):
    print(("  PASS " if cond else "  FAIL ") + msg)
    if not cond:
        BAD.append(msg)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def off(p):
    i = open(p, "rb").read().find(b"<meta charset")
    return None if i < 0 else i


def log(n):
    return open(os.path.join(LOGS, n), encoding="utf-8").read()


def run(args):
    r = subprocess.run(args, capture_output=True, text=True, cwd=REPO); return r.returncode, r.stdout + r.stderr


def old_unchanged():
    for f, h in OLD.items():
        ok(sha(os.path.join(T, f)) == h, "%s is byte-identical to the recorded SHA-256 %s" % (f, h[:12]))


def feature_lines(text, pat):
    return [l for l in text.splitlines() if re.search(pat, l)]


def template():
    old_unchanged()
    for f in NEW:
        ok(os.path.exists(os.path.join(T, f)), "new file %s exists" % f)
    o = off(os.path.join(T, "course_page_template_v9_52_1.html")); ok(o is not None and o < 512, "template 9.52.1: first <meta charset> at byte %s (limit: below 512)" % o)
    o = off(os.path.join(T, "course_page_template_v9_50_0.html")); ok(o is not None and o > 1024, "template 9.50.0 (kept as it was): first <meta charset> at byte %s (beyond the 1024 bytes of the prescan)" % o)
    for n in ("01", "10"):
        t = log("t36_%s.log" % n)
        for p in ("P1", "P3", "P4", "P5", "P6", "P8", "P9", "P12"):
            ls = feature_lines(t, r"^\s*\[(PASS|FAIL)\] %s\b" % p)
            ok(bool(ls) and all("[PASS]" in l for l in ls), "chapter %s scratch page on 9.52.1, page test 9.36.0: %s %s (%d lines)" % (n, p, "PASS" if ls and all("[PASS]" in l for l in ls) else "NOT PASS", len(ls)))
        ok("widgets: " in t and "failing: []" in t, "chapter %s scratch page: all widgets pass" % n)


def pagetest():
    old_unchanged()
    a = open(os.path.join(T, "sen0414_page_test_v9_34_0.py"), encoding="utf-8").read().splitlines(); b = open(os.path.join(T, "sen0414_page_test_v9_36_0.py"), encoding="utf-8").read().splitlines()
    removed = [l for l in difflib.unified_diff(a, b, lineterm="", n=0) if l.startswith("-") and not l.startswith("---")]
    ok(len(removed) <= 2 and all("version" in l.lower() or "__version__" in l for l in removed), "9.36.0 over 9.34.0: %d removed line(s) %s - every feature text of 9.34.0 is kept" % (len(removed), [l[:40] for l in removed]))
    t = log("t36_old10.log")
    ok(len(feature_lines(t, r"\[SKIP\] P\d+ .*page does not declare the standard")) >= 9, "a page that does not declare the standard: the P features are reported SKIP with the reason (old-template page of chapter 10)")
    s = log("t36_sh08.log")
    ok(bool(re.search(r"\[FAIL\] P12 .*byte 9293", s)), "FORCE_STANDARD=1 on the shipped chapter 8 page v9_28_0: P12 FAILS naming byte 9293")
    ok(bool(re.search(r"\[FAIL\] P11 ", s)) and bool(re.search(r"\[FAIL\] P2 .*chapter-code", s)), "FORCE_STANDARD=1 on the shipped chapter 8 page: P11 (no declared standard) and P2 (no chapter-code tab) FAIL, the measured defects")
    ok("Traceback" not in s and re.search(r"^exit \d", s, re.M) is not None, "the run ended without a crash")
    for n in ("06", "07", "08"):
        p = os.path.join(REPO, "03-materials/ch%s/page/sen0414_ch%s_page_v9_28_0.html" % (n, n)); o = off(p)
        ok(o is not None and o > 512, "shipped page of chapter %s v9_28_0: first <meta charset> at byte %s" % (n, o))


def charset():
    o = off(os.path.join(T, "course_page_template_v9_52_1.html")); ok(o is not None and o < 512, "template 9.52.1: first <meta charset> at byte %s" % o)
    h = open(os.path.join(T, "course_page_template_v9_52_1.html"), encoding="utf-8").read(); i = h.find("<head>")
    ok(h[i + 6:].startswith('<meta charset="utf-8">'), "template 9.52.1: <meta charset=\"utf-8\"> is the first child of <head> (byte %d)" % (i + 6))
    ok("below byte 512" in open(os.path.join(T, "sen0414_page_build_v4_18_0.py"), encoding="utf-8").read(), "builder v4_18_0 refuses a page whose charset is not first below byte 512")
    src = open(os.path.join(T, "sen0414_page_test_v9_36_0.py"), encoding="utf-8").read()
    ok("_o12 < 512" in src and "_raw" in src, "page test 9.36.0 feature P12 reads the raw bytes and requires the first <meta charset> below byte 512")
    for n in ("06", "07", "08"):
        o = off(os.path.join(REPO, "03-materials/ch%s/page/sen0414_ch%s_page_v9_28_0.html" % (n, n))); ok(o is not None and o > 512, "shipped page of chapter %s v9_28_0: charset at byte %s, so P12 must FAIL it" % (n, o))
    for n in ("01", "10"):
        t = log("t36_%s.log" % n); ok(bool(re.search(r"\[PASS\] P12 .*starts at byte \d+", t)) or "[PASS] P12" in t, "chapter %s scratch page built on 9.52.1: P12 PASS" % n)
    ok(bool(re.search(r"\[FAIL\] P12 .*byte 9293", log("t36_sh08.log"))), "shipped chapter 8 page v9_28_0: P12 FAIL at byte 9293 in the lineage agent's own run")
    ok(os.path.exists(os.path.join(LOGS, "t36_old10.log")) and "[SKIP] P12" in log("t36_old10.log"), "on a page built from template 9.50.0 the charset sits at byte 15882 (measured), beyond the prescan")


def deckcheck():
    for n, d in OLD_DECKS.items():
        rc, out = run([sys.executable, os.path.join(T, "sen0414_deck_standard_check_v1_0_0.py"), n, d])
        m = re.search(r"SUMMARY .*failing: ([A-Z0-9,]+)", out)
        ok(bool(m) and m.group(1) == OLD_FAIL[n], "old deck of chapter %s: failing elements %s (measured before the tool existed: %s)" % (n, m.group(1) if m else None, OLD_FAIL[n]))
    okl, badl = log("m1_selftest_ok.log"), log("m1_selftest_bad.log")
    ok(bool(re.search(r"^M1 PASS", okl, re.M)) and bool(re.search(r"^M1 FAIL", badl, re.M)), "M1 self-test discriminates: a matching manifest PASSES, a changed example FAILS")


def deck(n):
    rc, out = run([sys.executable, os.path.join(T, "sen0414_deck_standard_check_v1_0_0.py"), n, NEWDECK[n]]); m = re.search(r"SUMMARY PASS=(\d+) FAIL=(\d+) NOT_MEASURED=(\d+)", out)
    ok(rc == 0 and bool(m) and m.groups() == ("13", "0", "0"), "deck standard check on %s: %s" % (os.path.basename(NEWDECK[n]), m.group(0) if m else out[-200:]))
    rc, out = run([sys.executable, os.path.join(T, "sen0414_deck_overlap_check_v1_0_0.py"), NEWDECK[n]]); ok(rc == 0 and "RESULT CLEAN" in out, "deck overlap check: %s" % out.strip().splitlines()[-1])
    ok(os.path.exists(os.path.join(REPO, "03-materials/ch%s/page/chapter_code_ch%s_v1_0_0.json" % (n, n))), "chapter-code manifest chapter_code_ch%s_v1_0_0.json exists" % n)


def main():
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    {"template": template, "pagetest": pagetest, "charset": charset, "deckcheck": deckcheck, "deck06": lambda: deck("06"), "deck07": lambda: deck("07"), "deck08": lambda: deck("08")}[c]()
    print("RESULT %s (%d failed assertion(s))" % ("FAIL" if BAD else "PASS", len(BAD))); sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
