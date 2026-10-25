#!/usr/bin/env python3
"""sen0414_control_iter19_pagetests v1_2_0 (over v1_1_0, which stays as committed: the story-layout probe measures the FIRST story as the reader sees it when the Stories tab is opened, without scrolling the card to the top - the form of v1_1_0 passed the chapter 2 page v9_90_0 whose story text begins below the fold at 1366x768 - and the log is p37_chNN_storyfit2.log; viewports 1366x768, 1400x900 and 390x844) (over v1_0_0, which stays as committed: the page version per chapter) - the lineage agent's own page runs for the Iter_19 page controls (G136, G137: the controller re-runs, never trusts the executor's log).
Usage: sen0414_control_iter19_pagetests_v1_2_0.py NN [storyfit | TAGS]     TAGS = t37,t34,t34_old (a comma list: run only those)
Runs, SERIALLY and each under flock /tmp/page_test.lock, for chapter NN: the page test 9.37.0 and 9.34.0 on the new page (v9_90_0) and 9.34.0 on the existing page (v9_28_0), through the runner v1_1_0 with a TEST key;
the logs go to 08-tooling/control-iter19-logs/p37_chNN_t37.log, p37_chNN_t34.log, p37_chNN_t34_old.log. With 'storyfit' it runs only the story-layout probe:
for every story of the Stories tab, at 1400x900 and at 390x844, the photograph is at most 55 percent of the viewport height and the story's narrative paragraph (the longest paragraph) starts so that its first two lines (top plus 40 px) lie inside the viewport for the first story, and its first line (top plus 20 px) for the later stories, whose card is scrolled to the top once the story card is at the top
(written to p37_chNN_storyfit.log; exit 0 only when every story passes)."""
__version__ = "1.2.0"
import os, subprocess, sys
T = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(T); LOGS = os.path.join(T, "control-iter19-logs")
RUN = os.path.join(T, "sen0414_page_test_run_v1_1_0.py")
PV = lambda n: "9_90_0" if n == "05" else "9_91_0"      # the page version the controller measures: chapters 1, 3 and 4 were rebuilt on the manifest 1.1.0 (ex:CR2_ErrFirst)


def runs(n, only=None):
    os.makedirs(LOGS, exist_ok=True)
    for tag, test, ver in (("t37", "sen0414_page_test_v9_37_0.py", PV(n)), ("t34", "sen0414_page_test_v9_34_0.py", PV(n)), ("t34_old", "sen0414_page_test_v9_34_0.py", "9_28_0")):
        if only and tag not in only: continue
        lf = os.path.join(LOGS, "p37_ch%s_%s.log" % (n, tag))
        with open(lf, "w", encoding="utf-8") as f:
            r = subprocess.run(["flock", "/tmp/page_test.lock", "python3", RUN, n, ver], env=dict(os.environ, PAGE_TEST_FILE=test), stdout=f, stderr=subprocess.STDOUT, cwd=REPO)
        print(tag, "exit", r.returncode, flush=True)


def storyfit(n):
    from playwright.sync_api import sync_playwright
    import glob, re
    page = sorted(glob.glob(os.path.join(REPO, "03-materials/ch%s/page/sen0414_ch%s_page_v%s.html" % (n, n, PV(n)))))[-1]
    out, bad = [], 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for W, H in ((1366, 768), (1400, 900), (390, 844)):
            c = b.new_context(viewport={"width": W, "height": H}, is_mobile=W < 500, has_touch=W < 500); pg = c.new_page(); pg.goto("file://" + page); pg.wait_for_timeout(600)
            pg.evaluate("showTab('learn')"); pg.wait_for_timeout(200)
            pg.evaluate("showTab('stories')"); pg.wait_for_timeout(500); pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(200)
            n_st = pg.locator('[data-pane="stories"] .story').count()
            for i in range(n_st):
                r = pg.evaluate("""i=>{const s=document.querySelectorAll('[data-pane=stories] .story')[i];if(i>0){s.scrollIntoView({block:'start'});window.scrollBy(0,-4);}
                 const imgs=[...s.querySelectorAll('img')].filter(x=>x.getBoundingClientRect().height>0);const ih=imgs.length?Math.max(...imgs.map(x=>x.getBoundingClientRect().height)):0;
                 const ps=[...s.querySelectorAll('p')].filter(e=>!e.querySelector('img')&&e.textContent.trim().length>60);ps.sort((x,y)=>y.textContent.length-x.textContent.length);const r0=ps.length?ps[0].getBoundingClientRect():null;
                 const rects=r0?[r0]:[];return {ih:ih,imgs:imgs.length,vh:innerHeight,textTop:rects.length?Math.min(...rects.map(r=>r.top)):-1,textBottom:rects.length?rects[0].top+(i==0?40:20):-1}}""", i)
                good = r["textTop"] >= 0 and r["textBottom"] <= r["vh"] and r["ih"] <= 0.55 * r["vh"]
                bad += 0 if good else 1
                out.append("%s story %d at %dx%d: photo height %d of %d, first text %s..%s, images %d" % ("PASS" if good else "FAIL", i + 1, W, H, r["ih"], r["vh"], r["textTop"], r["textBottom"], r["imgs"]))
            if n_st == 0:
                bad += 1; out.append("FAIL no story cards found at %dx%d" % (W, H))
            c.close()
        b.close()
    open(os.path.join(LOGS, "p37_ch%s_storyfit2.log" % n), "w", encoding="utf-8").write("\n".join(out) + "\nRESULT: %s\n" % ("PASS" if not bad else "FAIL"))
    print("\n".join(out)); print("RESULT:", "PASS" if not bad else "FAIL"); sys.exit(1 if bad else 0)


if __name__ == "__main__":
    n = sys.argv[1]
    storyfit(n) if len(sys.argv) > 2 and sys.argv[2] == "storyfit" else runs(n, sys.argv[2].split(",") if len(sys.argv) > 2 else None)
