#!/usr/bin/env python3
"""Quick audit of one page with the checks of sen0414_page_test_diag_v1_0_0.py (every tab visited): prints each count and exits 0 only when all diagram checks hold.
Usage: diag_audit_run_v9_92_0.py PAGE.html   (run under flock /tmp/page_test.lock). Task TK_U8_Page_Build."""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sen0414_page_test_diag_v1_0_0 as T
from playwright.sync_api import sync_playwright
page = "file://" + os.path.abspath(sys.argv[1]); bad = []
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1400, "height": 900}); pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(page); pg.wait_for_timeout(1500)
    states = T.build_states(pg); print(len(states), "states (tabs, concepts, parse-tree diagrams)")
    figs, per = T.audit_all(pg, states); print("diagrams per state:", {k[:60]: v for k, v in per.items() if v}); print("states visited:", len(per), "; distinct figures seen:", len(figs))
    ok, det = T.verdict_figures(figs); print("FIGURES", ok, det)
    for k, r in figs:
        if not (r["fs"] and r["handle"]) or r["cover"]: print("  defect:", k, r)
    if not ok: bad.append("figures")
    lam = T.lambda_audit(pg); print("LAMBDA places:", lam)
    if lam: bad.append("lambda")
    pg.evaluate("showTab('taxonomy')"); pg.wait_for_timeout(500)
    okb, detb = T.behaviour(pg, "#taxo .dpanel"); print("BEHAVIOUR", okb, detb)
    if not okb: bad.append("behaviour")
    print("page errors:", errs[:5]); b.close()
print("DIAG AUDIT", "FAILED: %s" % bad if bad else "PASS"); sys.exit(1 if bad else 0)
