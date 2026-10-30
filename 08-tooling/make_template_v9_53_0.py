#!/usr/bin/env python3
"""Makes course_page_template_v9_53_0.html from course_page_template_v9_52_4.html (which stays). Task TK_U8_Page_Build (urgent, Owner's instruction of 2026-10-30).
Changes: (1) EVERY diagram (each svg figure the page draws, in every tab and in the detail card) gets a full-screen option and a user-resizable panel, next to the zoom that
exists; the controls sit in a toolbar above the figure and a resize strip below it, never over the figure; (2) the Playground sample 'Sort with a key' no longer uses lambda
(key=len). Refuses to overwrite. Usage: make_template_v9_53_0.py"""
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); src = os.path.join(H, "course_page_template_v9_52_4.html"); dst = os.path.join(H, "course_page_template_v9_53_0.html")
if os.path.exists(dst): sys.exit("refusing to overwrite " + dst)
t = open(src, encoding="utf-8").read()
def rep(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:70]); t = t.replace(old, new)
rep("<!-- course_page_template version 9.52.4 (SEN0414):",
    "<!-- course_page_template version 9.53.0 (SEN0414): over 9.52.4 - every diagram the page draws (each svg figure, in every tab and in the detail card) has a full-screen button (the Fullscreen API, with a fixed overlay where the API is missing or refuses; the Esc key and a visible button leave it) and a resizable panel (a handle under the figure: drag with mouse or finger, or the arrow keys; the figure refits to the panel); the controls sit in a toolbar above the figure and a strip below it, never over the figure; the zoom stays; the Playground sample 'Sort with a key' uses key=len, not a lambda. Version 9.52.4 follows. course_page_template version 9.52.4 (SEN0414):")
CSS = """
/* 9.53.0: full screen and a resizable panel for every diagram; the toolbar is above the figure, the resize strip below it */
.dpanel{display:block;position:relative;margin:.1rem 0 .3rem;max-width:100%}.dpanel>.zbar{margin-bottom:.25rem}.dpanel>.diagram{width:100%}
.dprz{display:flex;justify-content:flex-end;align-items:center;gap:.4rem;min-height:1.5rem;margin-top:.2rem}.dprz .note{font-size:.75rem;color:var(--muted,inherit)}
.dprh{cursor:nwse-resize;touch-action:none;font:inherit;line-height:1;padding:.15rem .5rem;min-width:2.4rem;min-height:1.5rem;border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--ink)}.dprh:focus-visible,.zbar [data-z="fs"]:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
@media (pointer:coarse){.dprh{min-width:44px;min-height:40px}}
.dpanel.dpfs{position:fixed;inset:0;z-index:10000;margin:0;max-width:none;width:auto!important;height:auto!important;display:flex;flex-direction:column;padding:.5rem .6rem;box-sizing:border-box;background:var(--bg);overflow:auto}
.dpanel.dpfs>.diagram{flex:1 1 auto;height:auto!important;min-height:0;width:100%!important;max-width:none!important;aspect-ratio:auto!important;max-height:none!important}.dpanel.dpfs>.dprz{display:none}
html.dpfs-lock,html.dpfs-lock body{overflow:hidden}
@media print{.dprz{display:none!important}}
"""
rep("</style></head><body>", CSS + "</style></head><body>")
JS = r"""
// ---------- 9.53.0: full screen and a resizable panel for every diagram ----------
// dpAttach wraps the zoom bar, the figure and a resize strip in one panel (.dpanel) and adds the full-screen button to the bar. dpSweep gives every other svg figure
// (anything drawn that the zoom code never saw) a figure box first, so that the same controls reach it.
function dpPanel(host){return host.parentNode&&host.parentNode.classList&&host.parentNode.classList.contains('dpanel')?host.parentNode:null}
function dpAttach(host){if(!host||!host.parentNode)return;let w=dpPanel(host);
 if(!w){const bar=host.previousElementSibling&&host.previousElementSibling.classList.contains('zbar')?host.previousElementSibling:null;w=document.createElement('div');w.className='dpanel';host.parentNode.insertBefore(w,bar||host);if(bar)w.appendChild(bar);w.appendChild(host);
  const rz=document.createElement('div');rz.className='dprz';rz.innerHTML='<span class="note">drag the handle, or use the arrow keys, to resize</span><button type="button" class="dprh" aria-label="Resize this diagram panel: drag, or use the arrow keys; Home restores the size" title="Resize: drag, or arrow keys (Home restores)">⇲</button>';w.appendChild(rz);dpResizer(w,host,rz.querySelector('.dprh'))}
 const bar=w.querySelector(':scope>.zbar');if(bar&&!bar.querySelector('[data-z="fs"]')){const b=document.createElement('button');b.type='button';b.className='btn g';b.dataset.z='fs';b.setAttribute('aria-pressed','false');b.title='Show this diagram on the whole screen';b.setAttribute('aria-label','Full screen');b.textContent='⛶ Full screen';bar.appendChild(b)}}
function dpSize(w,host,wd,ht){const par=w.parentNode,maxW=Math.max(160,(par?par.clientWidth:innerWidth)),maxH=Math.max(160,Math.floor(innerHeight*.92));
 const nw=Math.min(maxW,Math.max(160,Math.round(wd))),nh=Math.min(maxH,Math.max(120,Math.round(ht)));w.style.width=nw+'px';host.style.maxWidth='none';host.style.aspectRatio='auto';host.style.height=nh+'px';host.style.minHeight='0';host.dataset.usz='1';return [nw,nh]}
function dpResizer(w,host,h){let st=null;
 h.addEventListener('pointerdown',e=>{if(e.button)return;e.preventDefault();const r=host.getBoundingClientRect();st={x:e.clientX,y:e.clientY,w:w.getBoundingClientRect().width,h:r.height,id:e.pointerId};try{h.setPointerCapture(e.pointerId)}catch(x){}});
 h.addEventListener('pointermove',e=>{if(!st||e.pointerId!==st.id)return;dpSize(w,host,st.w+e.clientX-st.x,st.h+e.clientY-st.y)});
 const up=e=>{if(st&&e.pointerId===st.id){st=null;try{h.releasePointerCapture(e.pointerId)}catch(x){}window.dispatchEvent(new Event('dpresized'))}};h.addEventListener('pointerup',up);h.addEventListener('pointercancel',up);
 h.addEventListener('keydown',e=>{const k=e.key,s=(e.shiftKey?96:24);if(k==='Home'){e.preventDefault();w.style.width='';['maxWidth','aspectRatio','height','minHeight'].forEach(p=>host.style[p]='');delete host.dataset.usz;if(typeof fitViews==='function')fitViews();return}
  const dx=k==='ArrowRight'?s:k==='ArrowLeft'?-s:0,dy=k==='ArrowDown'?s:k==='ArrowUp'?-s:0;if(!dx&&!dy)return;e.preventDefault();const r=host.getBoundingClientRect();dpSize(w,host,w.getBoundingClientRect().width+dx,r.height+dy)})}
function dpFs(w,on){const b=w.querySelector('[data-z="fs"]');w.classList.toggle('dpfs',on);document.documentElement.classList.toggle('dpfs-lock',!!document.querySelector('.dpanel.dpfs'));
 if(b){b.setAttribute('aria-pressed',on?'true':'false');b.textContent=on?'✕ Exit full screen':'⛶ Full screen';b.title=on?'Leave full screen (Esc also leaves)':'Show this diagram on the whole screen'}}
function dpToggle(w){if(w.classList.contains('dpfs')){dpFs(w,false);if(document.fullscreenElement===w){try{document.exitFullscreen()}catch(x){}}return}
 document.querySelectorAll('.dpanel.dpfs').forEach(o=>dpFs(o,false));dpFs(w,true);
 try{if(w.requestFullscreen){const p=w.requestFullscreen();if(p&&p.catch)p.catch(()=>{})}}catch(x){}}
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-z="fs"]');if(!b)return;const w=b.closest('.dpanel');if(w){e.preventDefault();dpToggle(w)}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){const o=document.querySelector('.dpanel.dpfs');if(o){dpFs(o,false);if(document.fullscreenElement===o){try{document.exitFullscreen()}catch(x){}}}}});
document.addEventListener('fullscreenchange',()=>{if(!document.fullscreenElement)document.querySelectorAll('.dpanel.dpfs').forEach(o=>dpFs(o,false))});
function dpSweep(){document.querySelectorAll('svg').forEach(svg=>{if(svg.dataset.dp)return;
  if(svg.closest('button,.btn,.chip,summary,label,header.top,nav,.kit,.tip,#tip,.zoomhost,.dpanel')){if(svg.closest('.zoomhost,.dpanel'))svg.dataset.dp='1';else if(!svg.closest('header.top,nav'))svg.dataset.dp='1';return}
  const vb=(svg.getAttribute('viewBox')||'').split(/[\s,]+/).map(Number);if(vb.length!==4||vb[2]<60||vb[3]<30){svg.dataset.dp='1';return}
  svg.dataset.dp='1';const p=svg.parentNode;let host;
  if(p&&p.classList&&p.classList.contains('diagram')&&!p.classList.contains('zoomhost'))host=p;
  else{host=document.createElement('div');host.className='diagram small vz';host.style.aspectRatio=vb[2]+'/'+vb[3];host.style.maxHeight='80vh';p.insertBefore(host,svg);host.appendChild(svg)}
  if(!svg.getAttribute('data-vb0'))svg.setAttribute('data-vb0',svg.getAttribute('viewBox'));zoomable(host)})}
let dpTimer=0;new MutationObserver(()=>{clearTimeout(dpTimer);dpTimer=setTimeout(dpSweep,80)}).observe(document.body,{childList:true,subtree:true});setTimeout(dpSweep,300);
"""
rep("// ---------- relocate: any diagram whose nodes carry an identifier", JS + "// ---------- relocate: any diagram whose nodes carry an identifier")
rep("host.classList.add('zoomhost');relocatable(host)}", "host.classList.add('zoomhost');relocatable(host);dpAttach(host)}")
rep("[data-pane]:not([hidden]) .diagram:not(.small),[data-pane]:not([hidden]) #graph", "[data-pane]:not([hidden]) .diagram:not(.small):not([data-usz]),[data-pane]:not([hidden]) #graph")
rep('key=lambda x: len(x))', 'key=len)')
open(dst, "w", encoding="utf-8").write(t); print("wrote", dst)
