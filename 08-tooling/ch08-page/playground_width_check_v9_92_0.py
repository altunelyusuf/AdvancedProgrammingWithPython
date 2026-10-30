#!/usr/bin/env python3
"""Version 9.92.0 for chapter 8 (a NEW file over playground_width_check_v9_91_0.py; nothing changed in what it measures; task TK_U8_Page_Build). Earlier header: Version 9.96.0 for chapter 17 (a NEW file, copied from ch16-page/playground_width_check_v9_97_1.py, whose first line reads: version 9.97.1 over 9.97.0, whose 390 px run listed buttons and highlighted spans that sit inside a scrolling container - the sub-tab bar and the editor - which the reader never sees outside the screen): an element counts as wider than the screen only when no ancestor that clips or scrolls horizontally (overflow-x other than visible) ends inside the screen. The page scroll, the editor, the overlay and the text-size control are measured as before. Browser width check of the Playground of a built chapter page (a step of the executor; no gate or test is edited). Opens the Playground tab at 1366x768, 1400x900 and 390x844 and measures
the page (scrollWidth against clientWidth), every element's right edge against the viewport, the editor (textarea) and its highlighted overlay, and that the text-size control is on screen.
Exit 0 only when no element is wider than the screen, the page does not scroll sideways, and the control is on screen. Usage: playground_width_check_v9_92_0.py PAGE.html LOGFILE (run under flock /tmp/page_test.lock)"""
import os, sys
from playwright.sync_api import sync_playwright
page = os.path.abspath(sys.argv[1]); out = []; bad = 0
JS = """()=>{const iw=document.documentElement.clientWidth;const de=document.documentElement,b=document.body;
 const pane=document.querySelector('[data-pane="play"]');
 const q=(s)=>[...document.querySelectorAll(s)].filter(e=>e.getBoundingClientRect().width>0);
 const clipped=(e)=>{for(let a=e.parentElement;a&&a!==document.body;a=a.parentElement){const o=getComputedStyle(a).overflowX;if(o!=='visible'&&a.getBoundingClientRect().right<=iw+1)return true}return false};const wide=[...pane.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>iw+1||r.width>iw+1)&&getComputedStyle(e).position!=='fixed'&&!clipped(e)}).map(e=>({t:e.tagName+(e.id?'#'+e.id:'')+(e.className&&typeof e.className==='string'?'.'+e.className.split(' ')[0]:''),w:Math.round(e.getBoundingClientRect().width),r:Math.round(e.getBoundingClientRect().right)})).slice(0,6);
 const ta=document.getElementById('pcode');const tr=ta?ta.getBoundingClientRect():null;
 const ov=q('[data-pane="play"] pre, [data-pane="play"] .hl, [data-pane="play"] [class*=overlay], [data-pane="play"] [class*=highlight]').map(e=>({c:e.className,w:Math.round(e.getBoundingClientRect().width),sw:e.scrollWidth,r:Math.round(e.getBoundingClientRect().right)}));
 const f=document.querySelector('.fsctl');const fr=f?f.getBoundingClientRect():null;
 const lines=(ta?ta.value:'').split('\\n');
 return {iw:iw,docScroll:de.scrollWidth,bodyScroll:b.scrollWidth,wide:wide,textarea:tr?{w:Math.round(tr.width),r:Math.round(tr.right),sw:ta.scrollWidth,cw:ta.clientWidth}:null,overlays:ov,
  fsctl:fr?{l:Math.round(fr.left),r:Math.round(fr.right),onscreen:fr.right<=iw+1&&fr.left>=0}:null,longestLine:Math.max(...lines.map(l=>l.length)),paneW:Math.round(pane.getBoundingClientRect().width)}}"""
with sync_playwright() as p:
    br = p.chromium.launch()
    for W, H in ((1366, 768), (1400, 900), (390, 844)):
        c = br.new_context(viewport={"width": W, "height": H}, is_mobile=W < 500, has_touch=W < 500); pg = c.new_page(); pg.goto("file://" + page); pg.wait_for_timeout(800)
        pg.evaluate("showTab('play')"); pg.wait_for_timeout(1200)
        r = pg.evaluate(JS)
        ok = r["docScroll"] <= r["iw"] + 1 and not r["wide"] and r["fsctl"] and r["fsctl"]["onscreen"] and (not r["textarea"] or r["textarea"]["r"] <= r["iw"] + 1) and all(o["r"] <= r["iw"] + 1 for o in r["overlays"])
        bad += 0 if ok else 1
        out.append("%s at %dx%d: %s" % ("PASS" if ok else "FAIL", W, H, r))
        c.close()
    br.close()
res = "\n".join(out) + "\nRESULT: %s\n" % ("PASS" if not bad else "FAIL")
open(sys.argv[2], "w", encoding="utf-8").write(res); print(res); sys.exit(1 if bad else 0)
