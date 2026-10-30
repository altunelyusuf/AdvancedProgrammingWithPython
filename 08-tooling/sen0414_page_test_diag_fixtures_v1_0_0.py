#!/usr/bin/env python3
"""Fixtures of known answer for the checks of sen0414_page_test_diag_v1_0_0.py (task TK_U8_Page_Build). Pages in ch08-page/fixtures_9_38_0/:
diag_good.html has two diagrams with a full-screen control and a resizable panel (must PASS every check); diag_nofs.html has a diagram with zoom only (must FAIL: no full
screen, no handle); diag_cover.html has the controls but its toolbar lies over the figure (must FAIL: a control covers the figure); lambda_bad.html has a lambda in an
example (must be FOUND); lambda_good.html has none (must find nothing). Exit 0 only when every known answer is met. Run under flock /tmp/page_test.lock."""
import os, sys, json
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import sen0414_page_test_diag_v1_0_0 as DG
from playwright.sync_api import sync_playwright
FX = os.path.join(H, "ch08-page", "fixtures_9_38_0"); bad = []
def check(name, got, want):
    ok = got == want; print("  [%s] %s: got %s, known answer %s" % ("PASS" if ok else "FAIL", name, got, want), flush=True)
    if not ok: bad.append(name)
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1000, "height": 700}); pg = ctx.new_page()
    def load(f): pg.goto("file://" + os.path.join(FX, f)); pg.wait_for_timeout(200)
    load("diag_good.html"); figs, _ = DG.audit_all(pg, [""]); ok, det = DG.verdict_figures(figs); check("good page: every diagram has full screen and a handle, none covered", ok, True); print("    " + det)
    okb, detb = DG.behaviour(pg, "#p1"); check("good page: full screen on/off, resize by mouse, touch and keys", okb, True); print("    " + detb)
    load("diag_nofs.html"); figs, _ = DG.audit_all(pg, [""]); ok, det = DG.verdict_figures(figs); check("page without the feature fails the figure check", ok, False); print("    " + det)
    load("diag_cover.html"); figs, _ = DG.audit_all(pg, [""]); ok, det = DG.verdict_figures(figs); check("page whose toolbar covers the figure fails the figure check", ok, False); print("    " + det)
    load("lambda_bad.html"); check("lambda in an example is found", len(DG.lambda_audit(pg)) > 0, True)
    load("lambda_good.html"); check("no lambda is found where there is none (key=str.lower is fine)", len(DG.lambda_audit(pg)), 0)
    b.close()
print("FIXTURES", "FAILED: %s" % bad if bad else "ALL KNOWN ANSWERS MET"); sys.exit(1 if bad else 0)
