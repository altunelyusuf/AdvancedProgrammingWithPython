#!/usr/bin/env python3
"""Checks used by the page test 9.38.0 (task TK_U8_Page_Build): (A) every diagram of the page has a FULL-SCREEN control and a RESIZABLE panel, no control covers the figure,
full screen toggles on and off (the button and Escape), and a resize changes the panel and the figure refits; (B) no code of the page has a lambda.
A diagram is any <svg> figure the page draws (viewBox at least 60 by 30) outside buttons, chips, summaries, labels, the header and the navigation, or any <canvas>.
The functions take a Playwright page; sen0414_page_test_diag_fixtures_v1_0_0.py runs them over fixture pages of KNOWN answer."""
__version__ = "1.0.0"
import json, re

AUDIT_JS = r"""()=>{
 const box=r=>({x:r.left,y:r.top,w:r.width,h:r.height,r:r.right,b:r.bottom});
 const hit=(a,b)=>a.width>0&&a.height>0&&b.width>0&&b.height>0&&a.left<b.right-0.5&&a.right>b.left+0.5&&a.top<b.bottom-0.5&&a.bottom>b.top+0.5;
 const out=[];
 document.querySelectorAll('svg,canvas').forEach(f=>{
  if(f.closest('button,.btn,.chip,summary,label,header.top,nav,#tip,.kit,[hidden]'))return;
  if(!f.getClientRects().length)return;
  if(f.tagName==='svg'){const vb=(f.getAttribute('viewBox')||'').split(/[\s,]+/).map(Number);if(vb.length!==4||vb[2]<60||vb[3]<30)return}
  const fr=f.getBoundingClientRect();if(fr.width<20||fr.height<20)return;
  const panel=f.closest('.dpanel');const host=panel?panel.querySelector(':scope>.diagram'):null;
  const rec={tag:f.tagName,label:(f.getAttribute('aria-label')||f.id||f.parentNode.id||'').slice(0,50),panel:!!panel,fs:false,handle:false,cover:[]};
  if(panel){rec.fs=!!panel.querySelector('[data-z="fs"]');rec.handle=!!panel.querySelector('.dprh');
   const figs=[f.getBoundingClientRect(),host?host.getBoundingClientRect():fr];
   panel.querySelectorAll(':scope>.zbar,:scope>.zbar *,:scope>.dprz,:scope>.dprz *').forEach(c=>{const cr=c.getBoundingClientRect();if(cr.width&&cr.height&&figs.some(g=>hit(cr,g)))rec.cover.push((c.className||c.tagName)+'')})}
  out.push(rec)});
 return out}"""

def audit_here(pg):
    return pg.evaluate(AUDIT_JS)

def audit_all(pg, visit_js, settle_ms=250):
    """visit_js: JS statements to show a state, one per list item; the audit runs after each. Figures are keyed by label+tag+state."""
    seen = {}; per_state = {}
    for st in visit_js:
        try:
            if st: pg.evaluate(st)
        except Exception as e:
            per_state[st] = "error: %s" % str(e)[:80]; continue
        pg.wait_for_timeout(settle_ms)
        for rec in audit_here(pg):
            key = (st, rec["tag"], rec["label"], len(seen))
            seen[key] = rec
        per_state[st] = sum(1 for k in seen if k[0] == st)
    return list(seen.items()), per_state

def verdict_figures(figs):
    """figs: list of ((state, tag, label, i), rec); returns (ok, detail)"""
    miss_fs = [k for k, r in figs if not r["fs"]]; miss_h = [k for k, r in figs if not r["handle"]]
    cover = [(k, r["cover"]) for k, r in figs if r["cover"]]
    ok = bool(figs) and not miss_fs and not miss_h and not cover
    return ok, "%d diagrams; without a full-screen control: %d %s; without a resize handle: %d %s; a control over the figure: %d %s" % (
        len(figs), len(miss_fs), [m[:3] for m in miss_fs[:2]], len(miss_h), [m[:3] for m in miss_h[:2]], len(cover), cover[:2])

def behaviour(pg, panel_sel):
    """full screen on/off by the button and by Escape; a resize by mouse, by touch events and by keys; returns (ok, detail)."""
    res = {}
    P = pg.locator(panel_sel).first
    if P.count() == 0: return False, "no panel %s" % panel_sel
    P.scroll_into_view_if_needed(); pg.wait_for_timeout(150)
    host = lambda: pg.evaluate("s=>{const p=document.querySelector(s);const h=p.querySelector(':scope>.diagram'),v=h.querySelector('svg,canvas');const a=h.getBoundingClientRect(),b=v.getBoundingClientRect();return {hw:a.width,hh:a.height,vw:b.width,vh:b.height,pw:p.getBoundingClientRect().width,iw:innerWidth,ih:innerHeight}}", panel_sel)
    state = lambda: pg.evaluate("s=>{const p=document.querySelector(s);return {on:p.classList.contains('dpfs')||document.fullscreenElement===p,api:document.fullscreenElement===p,pressed:p.querySelector('[data-z=\"fs\"]').getAttribute('aria-pressed')}}", panel_sel)
    cover = lambda: pg.evaluate("""s=>{const p=document.querySelector(s),h=p.querySelector(':scope>.diagram').getBoundingClientRect();const hit=(a,b)=>a.width>0&&a.height>0&&a.left<b.right-.5&&a.right>b.left+.5&&a.top<b.bottom-.5&&a.bottom>b.top+.5;return [...p.querySelectorAll(':scope>.zbar,:scope>.zbar *,:scope>.dprz,:scope>.dprz *')].filter(c=>hit(c.getBoundingClientRect(),h)).length}""", panel_sel)
    h0 = host(); s0 = state()
    pg.evaluate("s=>document.querySelector(s+' [data-z=\"fs\"]').click()", panel_sel); pg.wait_for_timeout(500)
    s1 = state(); h1 = host(); c1 = cover()
    res["fs_on"] = s1["on"] and s1["pressed"] == "true" and h1["hw"] >= 0.9 * h1["iw"] and h1["hh"] >= 0.6 * h1["ih"]
    res["fs_mode"] = "Fullscreen API" if s1["api"] else "fixed overlay"
    res["fs_cover"] = c1
    pg.evaluate("s=>document.querySelector(s+' [data-z=\"fs\"]').click()", panel_sel); pg.wait_for_timeout(500)
    s2 = state(); res["fs_off_button"] = (not s2["on"]) and s2["pressed"] == "false"
    pg.evaluate("s=>document.querySelector(s+' [data-z=\"fs\"]').click()", panel_sel); pg.wait_for_timeout(400)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    res["fs_off_escape"] = not state()["on"]
    # resize by mouse
    P.scroll_into_view_if_needed(); h0 = host()
    hb = pg.locator(panel_sel + " .dprh").first.bounding_box()
    pg.mouse.move(hb["x"] + hb["width"] / 2, hb["y"] + hb["height"] / 2); pg.mouse.down(); pg.mouse.move(hb["x"] + hb["width"] / 2 - 90, hb["y"] + hb["height"] / 2 + 70, steps=6); pg.mouse.up(); pg.wait_for_timeout(300)
    h2 = host(); res["mouse"] = abs(h2["hh"] - h0["hh"]) >= 40 and abs(h2["pw"] - h0["pw"]) >= 40
    res["refit"] = abs(h2["vh"] - h0["vh"]) > 1 or abs(h2["vw"] - h0["vw"]) > 1
    # resize by touch events
    pg.evaluate("""s=>{const h=document.querySelector(s+' .dprh'),r=h.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2;const e=(t,dx,dy)=>h.dispatchEvent(new PointerEvent(t,{pointerId:77,pointerType:'touch',isPrimary:true,bubbles:true,cancelable:true,clientX:x+dx,clientY:y+dy,button:0,buttons:1}));e('pointerdown',0,0);e('pointermove',30,50);e('pointermove',50,80);e('pointerup',50,80)}""", panel_sel); pg.wait_for_timeout(300)
    h3 = host(); res["touch"] = h3["hh"] - h2["hh"] >= 30
    # resize by keys
    pg.locator(panel_sel + " .dprh").first.focus(); pg.keyboard.press("ArrowDown"); pg.keyboard.press("ArrowDown"); pg.wait_for_timeout(200)
    h4 = host(); res["keys"] = h4["hh"] - h3["hh"] >= 30
    res["within_screen"] = h4["hh"] <= h4["ih"] and h4["pw"] <= h4["iw"] + 1
    ok = all(v for k, v in res.items() if k not in ("fs_mode",)) and res["fs_cover"] == 0
    return ok, json.dumps(res)

LAMBDA_RE = re.compile(r"\blambda\b")
def lambda_audit(pg):
    """every code surface of the page: the data (all strings), the quiz, the question bank, the Playground samples, every code box; returns list of (where, snippet)"""
    hits = pg.evaluate(r"""()=>{const out=[];const re=/\blambda\b/;const walk=(o,p,n)=>{if(typeof o==='string'){if(re.test(o))out.push([p,o.slice(Math.max(0,o.search(re)-30),o.search(re)+50)])}else if(Array.isArray(o)){o.forEach((v,i)=>walk(v,p+'['+i+']',n))}else if(o&&typeof o==='object'){for(const k in o)walk(o[k],p+'.'+k,n)}};
     for(const id of ['data','quiz','qbank','objectives']){const e=document.getElementById(id);if(e){try{walk(JSON.parse(e.textContent),id,0)}catch(x){out.push([id,'unreadable'])}}}
     if(typeof ED_TPL!=='undefined')walk(ED_TPL,'ED_TPL',0);
     document.querySelectorAll('textarea,pre.code,code,.codebox').forEach((t,i)=>{const v=(t.value!==undefined&&t.tagName==='TEXTAREA')?t.value:t.textContent;if(re.test(v))out.push(['code box '+i+' '+(t.id||''),v.slice(Math.max(0,v.search(re)-30),v.search(re)+50)])});
     return out}""")
    return hits
