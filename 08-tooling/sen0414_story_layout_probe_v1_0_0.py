#!/usr/bin/env python3
"""sen0414_story_layout_probe v1_0_0 - the story-layout rule of the page standard, as a tool an executor runs on its own page (the lineage agent's controller runs the same rule: sen0414_control_iter19_pagetests_v1_4_0.py).
THE ONE RULE: the photograph of a story is lower than the viewport, and the narrative paragraph (the longest <p> of the story without an image, more than 60 characters) begins within the first screen of the story (top < viewport height). The FIRST story is measured as the reader sees it when the Stories tab is opened (no scrolling); every later story is measured after scrolling its card to the top. Viewports 1366x768, 1400x900 and 390x844 (phone). Every story card of the page is measured; a page without story cards FAILS.
Usage: sen0414_story_layout_probe_v1_0_0.py PAGE.html [LOGFILE]     (run with the system python3 under `flock /tmp/page_test.lock`; exit 0 only when every story passes at every viewport; the result goes to stdout and to LOGFILE if given)"""
__version__ = "1.0.0"
import os, sys


def main():
    from playwright.sync_api import sync_playwright
    page = os.path.abspath(sys.argv[1]); out, bad = [], 0
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
                 const rects=r0?[r0]:[];return {ih:ih,imgs:imgs.length,vh:innerHeight,textTop:rects.length?Math.min(...rects.map(r=>r.top)):-1,textBottom:rects.length?rects[0].top:-1}}""", i)
                good = r["textTop"] >= 0 and r["textBottom"] <= r["vh"] and r["ih"] < r["vh"]
                bad += 0 if good else 1
                out.append("%s story %d at %dx%d: photo height %d of %d, first text %s..%s, images %d" % ("PASS" if good else "FAIL", i + 1, W, H, r["ih"], r["vh"], r["textTop"], r["textBottom"], r["imgs"]))
            if n_st == 0:
                bad += 1; out.append("FAIL no story cards found at %dx%d" % (W, H))
            c.close()
        b.close()
    res = "\n".join(out) + "\nRESULT: %s\n" % ("PASS" if not bad else "FAIL")
    if len(sys.argv) > 2:
        open(sys.argv[2], "w", encoding="utf-8").write(res)
    print(res); sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
