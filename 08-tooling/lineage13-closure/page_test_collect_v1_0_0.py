#!/usr/bin/env python3
"""Lineage13 measure ST13_Measure_PageTest (2026-11-26): collects, for the five pages of chapters 16 to 20, the page-test result file kept beside the page data (08-tooling/chNN-page/test_results_v*.json, the one of the released page version) and counts widgets and features that passed and the pages with no failure; also names the page-test log of the release stage where one exists. Usage: page_test_collect_v1_0_0.py"""
__version__ = "1.0.0"
import glob, json, os, re, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PAGES = {16: "9_100_0", 17: "9_100_0", 18: "9_102_0", 19: "9_99_0", 20: "9_101_0"}
print("Page-test collection, Lineage13 (2026-11-26): test file sen0414_page_test_v9_42_0.py, release step with a TEST key")
ok = 0
for n, v in PAGES.items():
    page = "03-materials/ch%d/page/sen0414_ch%d_page_v%s.html" % (n, n, v)
    res = "08-tooling/ch%d-page/test_results_v%s.json" % (n, v)
    assert os.path.exists(os.path.join(R, page)), page
    d = json.load(open(os.path.join(R, res), encoding="utf-8"))
    w, f = d["widgets"], d["features"]
    wp, fp = sum(1 for x in w.values() if x["passed"]), sum(1 for x in f.values() if x["passed"])
    g = d["gates"]
    gates_ok = g.get("Stage4.C console errors") == [] and g.get("Stage4.D dialogs") == 0 and g.get("Stage4.F top menu visible on mobile without clicks") is True
    logs = glob.glob(os.path.join(R, "08-tooling/lineage13-opening/ch%d_page_%s/page_test.log" % (n, v)))
    clean = wp == len(w) and fp == len(f) and gates_ok
    ok += clean
    print("chapter %d page %s: widgets %d of %d, features %d of %d, console errors %s, dialogs %s, mobile menu %s; %s; release-stage log: %s" % (
        n, v.replace("_", "."), wp, len(w), fp, len(f), g.get("Stage4.C console errors"), g.get("Stage4.D dialogs"), g.get("Stage4.F top menu visible on mobile without clicks"),
        "passes" if clean else "FAILS", os.path.relpath(logs[0], R) if logs else "none (result file only)"))
print("pages that pass: %d of %d" % (ok, len(PAGES)))
sys.exit(0 if ok == len(PAGES) else 1)
