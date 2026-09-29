"""Makes course_page_template_v9_7_0.html from v9_6_0. Usage: template_patch_v9_7_0.py <in.html> <out.html>
9.7.0 answers the owner's review of 2026-09-29:
 - the per-section 'Next step' button is gone: a leaf concept shows its example at once (it only revealed one hidden line);
 - the title and the folded note above every Maps/Lab/Practice/Reference view no longer take a row: the title is kept for screen
   readers, the note is a small 'About' button in the corner;
 - diagrams and code areas fill the space that is left (fitViews), code boxes grow with their text;
 - new visualisations that are executed specifications: debugger (breakpoints, continue, step in, step over, step out), logging levels,
   exception unwinding;
 - a Lecture tab under Learn (the deck's talk track, slide by slide) and a Resources tab under Reference, with searches for videos
   and discussions that are labelled as searches, not as recommendations; the concept card lists the resources of its concept."""
__version__ = "1.0.0"
import sys
s = open(sys.argv[1], encoding="utf-8").read()
def rep(old, new, count=1):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new, count)

# 1. leaf concept: no walkthrough button
rep("""if(n.level===3){return '<div class="widget" id="'+w+'"><div class="wl">Walk through it</div><ol class="steps"><li>'+esc(n.example||'')+'</li><li hidden>'+linkify(n.definition||n.body,n.id)+'</li></ol><button class="btn" data-step="'+w+'">Next step</button></div>'}""",
    """if(n.level===3){return n.example?'<div class="widget" id="'+w+'"><div class="wl">Example</div><pre class="exs">'+esc(n.example)+'</pre></div>':''}""")

# 2. folded note -> corner button; h2 kept for screen readers
rep("""if(p.dataset.pane==='agents'||byId[p.dataset.pane])return;const h=p.querySelector(':scope > h2');const n=h&&h.nextElementSibling;if(n&&n.matches('p.note')){const d=document.createElement('details');d.className='help';d.innerHTML='<summary>ⓘ About this view</summary>';n.replaceWith(d);d.appendChild(n)}});""",
    """if(p.dataset.pane==='agents'||byId[p.dataset.pane])return;const h=p.querySelector(':scope > h2');if(!h)return;const ns=[];let n=h.nextElementSibling;while(n&&n.matches('p.note,p.legend')){ns.push(n);n=n.nextElementSibling}if(ns.length){const d=document.createElement('details');d.className='help';d.innerHTML='<summary title="About this view">ⓘ About</summary>';ns[0].replaceWith(d);ns.forEach(x=>d.appendChild(x))}});""")

# 3. groups: lecture first under Learn, resources under Reference
rep("const GROUPS={learn:tops.map(t=>[t.id,ICON[1]+' '+t.label]),", "const GROUPS={learn:[...(D.lecture&&D.lecture.length?[['lecture','🎓 Lecture']]:[]),...tops.map(t=>[t.id,ICON[1]+' '+t.label])],")
rep("reference:[['glossary','📖 Glossary'],['refs','🔗 References']],", "reference:[['glossary','📖 Glossary'],['refs','🔗 References'],...(D.resources&&D.resources.length?[['resources','🧭 Resources']]:[])],")

# 4. panes for lecture and resources
panes = r"""
function searchLinks(t){const q=encodeURIComponent('python '+t);return '<a href="https://www.youtube.com/results?search_query='+q+'" target="_blank" rel="noopener">videos</a> · <a href="https://stackoverflow.com/search?q='+encodeURIComponent('[python] '+t)+'" target="_blank" rel="noopener">Stack Overflow</a> · <a href="https://discuss.python.org/search?q='+encodeURIComponent(t)+'" target="_blank" rel="noopener">Python forum</a>'}
const RKIND={documentation:'📘 Documentation',pep:'📜 PEPs',interactive:'🧪 Interactive tools',video:'🎥 Videos',discussion:'💬 Discussions'};
function resList(list){return '<ul class="res">'+list.map(r=>'<li><a href="'+esc(r.url)+'" target="_blank" rel="noopener">'+esc(r.title)+'</a> <span class="note">'+esc(r.source)+'</span><br><span class="note">'+esc(r.why)+'</span></li>').join('')+'</ul>'}
if(D.lecture&&D.lecture.length)P+='<div role="tabpanel" data-pane="lecture" hidden>'+subbar('learn')+'<h2>🎓 The lecture</h2><div class="lecture">'+D.lecture.map(s=>'<article class="lslide" id="ls-'+s.n+'"><header><span class="lnum">'+s.n+'</span><h3>'+esc(s.title)+'</h3></header><p>'+esc(s.say)+'</p>'+(s.concept&&byId[s.concept]?'<p class="lact"><button class="jump" data-go="'+s.concept+'">On the page: '+esc(byId[s.concept].label)+'</button>'+(D.visuals&&D.visuals[s.visual]?'<button class="jump" data-lvis="'+s.visual+'">Show the visual</button>':'')+'</p>':'')+'</article>').join('')+'</div></div>';
if(D.resources&&D.resources.length){const kinds=Object.keys(RKIND).filter(k=>D.resources.some(r=>r.kind===k));P+='<div role="tabpanel" data-pane="resources" hidden>'+subbar('reference')+'<h2>🧭 Resources</h2><p class="note">Every link below was opened and its title read on '+esc(D.resources_checked||'the build date')+'. Videos and discussions are not listed as recommendations unless someone has watched or read them: the searches further down are only searches.</p>'+kinds.map(k=>'<h3>'+RKIND[k]+'</h3>'+resList(D.resources.filter(r=>r.kind===k))).join('')+(D.resources.some(r=>r.kind==='video')?'':'<p class="note">No video has been checked yet, so none is listed.</p>')+'<h3>🔎 Search for videos and discussions</h3><p class="note">These open a search on another site for each concept. They are searches, not recommendations: judge what you find.</p><table>'+D.nodes.filter(n=>n.level===3).map(n=>'<tr><th><span class="c" data-c="'+n.id+'">'+esc(n.label)+'</span></th><td>'+searchLinks(n.label)+'</td></tr>').join('')+'</table></div>'}
panes.innerHTML=P;"""
rep("\npanes.innerHTML=P;", panes)

# 5. concept card: resources of the concept and searches
rep("""+'<div class="kv">Actions</div><p><button class="jump" data-go="'+id+'">Go to its section</button>'""",
    """+((D.resources||[]).filter(x=>x.concept===id).length?'<div class="kv">Learn more</div>'+resList((D.resources||[]).filter(x=>x.concept===id)):'')+'<div class="kv">Search</div><p class="note">'+searchLinks(n.label)+' (searches, not recommendations)</p><div class="kv">Actions</div><p><button class="jump" data-go="'+id+'">Go to its section</button>'""")

# 6. code areas: ids for fitting; the trace side column
rep('<textarea class="code" id="trcode" style="min-height:8rem"', '<textarea class="code" id="trcode" data-fill="0.3" style="min-height:6rem"')
rep('<div class="trgrid"><div class="trsrc" id="trsrc"></div><div><div class="wl">Variables</div>', '<div class="trgrid"><div class="trsrc" id="trsrc" data-fill="1"></div><div class="trside" data-fill="1"><div class="wl">Variables</div>')
rep('<textarea class="code" id="pcode" style="min-height:9rem"', '<textarea class="code" id="pcode" data-fill="0.5" style="min-height:9rem"')
rep('<textarea class="code" id="ppcode" style="min-height:4rem"', '<textarea class="code" id="ppcode" data-fill="0.22" style="min-height:4rem"')

# 7. fitting
fit = r"""
function fitViews(){const H=window.innerHeight;
 document.querySelectorAll('[data-pane]:not([hidden]) .diagram:not(.small),[data-pane]:not([hidden]) #graph,[data-pane]:not([hidden]) .ontowrap,[data-pane]:not([hidden]) [data-fill]').forEach(el=>{const f=el.dataset.fill?parseFloat(el.dataset.fill):1;el.style.height='auto';const top=el.getBoundingClientRect().top;el.style.height=Math.max(el.dataset.fill?120:260,(H-top-14)*f)+'px'});
 document.querySelectorAll('textarea.code:not([data-fill])').forEach(t=>{if(!t.offsetParent||t.readOnly&&false)return;t.style.height='auto';t.style.height=Math.min(Math.max(t.scrollHeight+4,60),H*0.6)+'px'})}
window.addEventListener('resize',()=>setTimeout(fitViews,50));document.addEventListener('input',e=>{if(e.target.matches&&e.target.matches('textarea.code'))fitViews()});
"""
rep("function showTab(k){", fit + "function showTab(k){")
rep("document.getElementById('center').scrollTop=0}", "document.getElementById('center').scrollTop=0;setTimeout(fitViews,60);setTimeout(fitViews,400)}")

# 8. new visualisations
vis = r"""
 if(v.kind==='debugger')return '<div class="vis" id="'+w+'" data-i="0"><div class="wl">Debugger simulator: a recorded run of the program</div><p class="note">'+esc(v.caption)+' Click a line number to set or clear a breakpoint (the red dot).</p><div class="row dbgbtns" role="group" aria-label="Debugger controls">'+[['cont','Continue'],['in','Step In'],['over','Step Over'],['out','Step Out'],['stop','Stop / restart']].map(([a,l])=>'<button class="btn'+(v.focus===a?'':' g')+'" data-dbg="'+n.id+':'+a+'">'+l+'</button>').join('')+'<span class="note" id="'+w+'-pos" aria-live="polite"></span></div><div class="dbg"><div class="dbgcode" id="'+w+'-code"></div><div class="dbgside"><div class="wl">Variables</div><div id="'+w+'-vars"></div><div class="wl">Call stack</div><div id="'+w+'-stack"></div><div class="wl">Output</div><pre class="out" id="'+w+'-out"></pre></div></div></div>'
 if(v.kind==='levels')return '<div class="vis" id="'+w+'"><div class="wl">Logging levels: choose the level the program logs at</div><div class="row" role="group" aria-label="Logging level">'+v.settings.map((t,i)=>'<button class="btn g" data-lv="'+n.id+':'+i+'">'+esc(t.label)+'</button>').join('')+'</div><div id="'+w+'-out"></div></div>'
 if(v.kind==='unwind')return '<div class="vis" id="'+w+'" data-k="0"><div class="wl">An exception climbs the call stack</div><p class="note">'+esc(v.caption)+'</p><div class="row"><button class="btn g" data-uw="'+n.id+':reset">⏮</button><button class="btn" data-uw="'+n.id+':next">Climb one frame ▶</button><button class="btn g" data-uw="'+n.id+':play">▶▶ Play</button><span class="note" id="'+w+'-pos" aria-live="polite"></span></div><div id="'+w+'-out"></div></div>'
 return ''}
const STATIC_VIS=['trace','range','pairs','names','debugger','levels','unwind'];
function dbgShow(id){const v=D.visuals[id],w='wv-'+id,b=document.getElementById(w),i=+b.dataset.i,E=v.events,fin=i>=E.length,e=fin?null:E[i],bps=b._bps||(b._bps=new Set(v.breakpoints||[]));
 document.getElementById(w+'-code').innerHTML=v.lines.map((l,k)=>'<div class="tl'+(e&&e.line===k+1?' now':'')+'"><span class="bp'+(bps.has(k+1)?' on':'')+'" data-bp="'+id+':'+(k+1)+'" role="button" aria-label="Breakpoint on line '+(k+1)+'" title="Breakpoint">'+(k+1)+'</span>'+esc(l)+'</div>').join('');
 document.getElementById(w+'-vars').innerHTML=e?(e.vars.length?'<table class="tt">'+e.vars.map(([a,c])=>'<tr><td><code>'+esc(a)+'</code></td><td><code>'+esc(c)+'</code></td></tr>').join('')+'</table>':'<span class="note">none yet</span>'):'<span class="note">program finished</span>';
 document.getElementById(w+'-stack').innerHTML=e?e.stack.slice().reverse().map((f,k)=>'<div class="frm'+(k===0?' top':'')+'">'+esc(f)+'</div>').join(''):'';
 document.getElementById(w+'-out').textContent=e?e.out:v.printed;
 document.getElementById(w+'-pos').textContent=e?('stopped at line '+e.line+(bps.has(e.line)?' (breakpoint)':'')):'finished'}
function dbgMove(id,a){const v=D.visuals[id],b=document.getElementById('wv-'+id),E=v.events,bps=b._bps||(b._bps=new Set(v.breakpoints||[]));let i=+b.dataset.i;if(a==='stop'){b.dataset.i=0;dbgShow(id);return}if(i>=E.length)return;const d=E[i].depth;let j=E.length;
 if(a==='in')j=i+1;else if(a==='over'){for(let k=i+1;k<E.length;k++)if(E[k].depth<=d){j=k;break}}else if(a==='out'){for(let k=i+1;k<E.length;k++)if(E[k].depth<d){j=k;break}}else if(a==='cont'){for(let k=i+1;k<E.length;k++)if(bps.has(E[k].line)){j=k;break}}
 b.dataset.i=Math.min(j,E.length);dbgShow(id)}
function levelsShow(id,i){const v=D.visuals[id],w='wv-'+id,t=v.settings[i];document.querySelectorAll('[data-lv^="'+id+':"]').forEach(x=>x.classList.toggle('on',x.dataset.lv===id+':'+i));
 document.getElementById(w+'-out').innerHTML='<p class="note">'+esc(t.note)+'</p><table class="tt"><tr><th>Call</th><th>Level</th><th>Shown?</th></tr>'+v.messages.map((m,k)=>'<tr class="'+(t.shown[k]?'':'later')+'"><td><code>'+esc(m.call)+'</code></td><td>'+esc(m.level)+' ('+m.num+')</td><td class="'+(t.shown[k]?'t':'f')+'">'+(t.shown[k]?'shown':'hidden')+'</td></tr>').join('')+'</table><div class="wl">What the program prints</div><pre class="out">'+esc(t.output.join('\n')||'(nothing)')+'</pre>'}
function unwindShow(id,k){const v=D.visuals[id],w='wv-'+id,b=document.getElementById(w);b.dataset.k=k;const n=v.frames.length,done=k>=n;
 document.getElementById(w+'-out').innerHTML='<div class="uw">'+v.frames.map((f,j)=>'<div class="uwf'+(j<k?' gone':'')+(j===k&&!done?' cur':'')+'"><b>'+esc(f.func)+'</b> <span class="note">line '+f.line+'</span><code>'+esc(f.text)+'</code>'+(j===0?'<span class="uwraise">raise '+esc(v.exc)+'</span>':'')+'</div>').join('')+'<div class="uwf handler'+(done?' cur':'')+'"><b>'+esc(v.handler.func)+'</b> <span class="note">line '+v.handler.line+'</span><code>'+esc(v.handler.text)+'</code>'+(done?'<span class="uwcatch">caught here</span>':'')+'</div></div><div class="wl">The traceback Python would print if nobody caught it</div><pre class="out">'+esc(v.traceback)+'</pre>';
 document.getElementById(w+'-pos').textContent=done?'caught in '+v.handler.func:'unwinding: '+(k)+' of '+n+' frames left'}
"""
rep("\n return ''}\nconst STATIC_VIS=['trace','range','pairs','names'];", vis)
rep("if(STATIC_VIS.includes(D.visuals[id].kind)){if(D.visuals[id].kind==='trace')vtraceShow(id);return}",
    "if(STATIC_VIS.includes(D.visuals[id].kind)){const kk=D.visuals[id].kind;if(kk==='trace')vtraceShow(id);if(kk==='debugger')dbgShow(id);if(kk==='levels')levelsShow(id,0);if(kk==='unwind')unwindShow(id,0);return}")

# 9. handlers
h = """ if(t.dataset.dbg){const [id,a]=t.dataset.dbg.split(':');dbgMove(id,a);return}
 if(t.dataset.bp){const [id,l]=t.dataset.bp.split(':'),b=document.getElementById('wv-'+id),bp=b._bps||(b._bps=new Set(D.visuals[id].breakpoints||[]));bp.has(+l)?bp.delete(+l):bp.add(+l);dbgShow(id);return}
 if(t.dataset.lv){const [id,i]=t.dataset.lv.split(':');levelsShow(id,+i);return}
 if(t.dataset.uw){const [id,a]=t.dataset.uw.split(':'),b=document.getElementById('wv-'+id),n=D.visuals[id].frames.length;if(a==='reset')unwindShow(id,0);else if(a==='next')unwindShow(id,Math.min(n,+b.dataset.k+1));else{unwindShow(id,0);let k=0;const hh=setInterval(()=>{k++;unwindShow(id,k);if(k>=n)clearInterval(hh)},900)}return}
 if(t.dataset.lvis){goTo(D.visuals[t.dataset.lvis]&&t.dataset.lvis);const tg=document.querySelector('[data-vistoggle="'+t.dataset.lvis+'"]');const p=document.getElementById('wvp-'+t.dataset.lvis);if(tg&&p&&p.hidden)tg.click();return}
"""
rep(" if(t.dataset.vistoggle){", h + " if(t.dataset.vistoggle){")
# vistoggle also refits
rep("d.hidden=!d.hidden;if(!d.hidden){const v=D.visuals[t.dataset.vistoggle];", "d.hidden=!d.hidden;if(!d.hidden){setTimeout(fitViews,60);const v=D.visuals[t.dataset.vistoggle];")

# 10. css
css = """
[data-pane]{position:relative}
.viewsub + h2{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.viewsub:has(+ h2 + details.help),.viewsub:has(+ h2 + p){margin-right:5.6rem}
[data-pane] > details.help{position:absolute;top:.15rem;right:.2rem;z-index:8;margin:0}
details.help > summary{border:1px solid var(--line);border-radius:999px;padding:.2rem .7rem;background:var(--card);list-style:none;white-space:nowrap}
details.help[open] > p{position:absolute;right:0;top:2.1rem;width:min(30rem,88vw);background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.6rem .8rem;box-shadow:0 8px 24px #0002;margin:0}
pre.exs{margin:.2rem 0;padding:.5rem .7rem;background:var(--code);color:#E6EDF3;border-radius:8px;white-space:pre-wrap;font:.933rem "Courier New",monospace}
.trside{overflow:auto}.trsrc{overflow:auto}
.dbg{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,2fr);gap:.6rem}@media (max-width:900px){.dbg{grid-template-columns:1fr}}
.dbgcode{background:var(--code);color:#E6EDF3;border-radius:8px;padding:.4rem 0;font:.9rem "Courier New",monospace;overflow:auto}
.dbgcode .tl{white-space:pre;padding:0 .6rem}.dbgcode .bp{display:inline-block;width:2.4rem;color:#8B949E;cursor:pointer;text-align:right;padding-right:.5rem;margin-right:.3rem;border-radius:4px}.dbgcode .bp.on{background:#E5484D;color:#fff}
.frm{padding:.15rem .5rem;border:1px solid var(--line);border-radius:6px;margin:.15rem 0;background:var(--card)}.frm.top{border-color:var(--blue);font-weight:700}
.uw{display:flex;flex-direction:column;gap:.35rem;max-width:34rem}.uwf{border:1px solid var(--line);border-radius:8px;padding:.35rem .6rem;background:var(--card);position:relative}.uwf code{display:block;margin-top:.15rem}.uwf.gone{opacity:.35;text-decoration:line-through}.uwf.cur{outline:2px solid var(--blue)}
.uwraise{position:absolute;right:.5rem;top:.3rem;color:var(--bad);font-weight:700;font-size:.85rem}.uwcatch{position:absolute;right:.5rem;top:.3rem;color:var(--ok);font-weight:700;font-size:.85rem}.uwf.handler{border-style:dashed}
.lecture{display:grid;gap:.6rem;grid-template-columns:repeat(auto-fill,minmax(min(26rem,100%),1fr))}.lslide{border:1px solid var(--line);border-radius:12px;padding:.6rem .9rem;background:var(--card)}.lslide header{display:flex;gap:.6rem;align-items:center}.lslide h3{margin:0;font-size:1.05rem}.lnum{background:var(--navy);color:#fff;border-radius:999px;min-width:1.8rem;height:1.8rem;display:inline-flex;align-items:center;justify-content:center;font-weight:700}.lact .jump{margin-right:.3rem}
ul.res{padding-left:1.1rem}ul.res li{margin:.3rem 0}
"""
rep("const AGENT_ICONS=[", "const AGENT_ICONS=[[/worked/i,'\U0001F52C'],[/controls/i,'\U0001F3AE'],[/debugger/i,'\U0001F41E'],[/levels/i,'\U0001F39A\uFE0F'],[/logging practice/i,'\U0001F6E0\uFE0F'],[/setup/i,'\U0001FAB5'],[/logging/i,'\U0001FAB5'],[/traceback/i,'\U0001F9FE'],[/assert/i,'\u2705'],[/rais/i,'\U0001F6A8'],")
rep(".flowwrap{display:grid", css + ".flowwrap{display:grid")
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("written", sys.argv[2], len(s))
