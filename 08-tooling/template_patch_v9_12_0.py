"""Makes course_page_template_v9_12_0.html from v9_11_0. Usage: template_patch_v9_12_0.py <in.html> <out.html>
9.12.0 (the owner's review of 2026-09-30): (1) every reference in an agent's answer is a control: the inline [n] and the source chips open that passage in the detail card
(kind, file, full text, the concepts it mentions as links, a search for it), and the chip in the answer is marked; the book, course and research sources, which have no
section of their own, are no longer dead text. (2) A page-wide search: a Search button in the title bar, the / key or Ctrl+K; it finds concepts by name, definition and code
at once, and on request the book, course and research passages; each result goes to its section or opens the passage. (3) The small local model's reply is checked against
the passages it was given: sentences whose words are not found in them are removed, and when nothing is left the sources' own sentences are shown, so 'at the top of this page
you would find a section' cannot be invented. (4) A 'how do I write / construct / what is the syntax' question also shows the concept's worked example."""
import sys
s = open(sys.argv[1], encoding="utf-8").read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:90])
    s = s.replace(old, new)

rep("<!-- course_page_template version 9.11.0:", "<!-- course_page_template version 9.12.0: clickable references and source chips in agent answers, a page-wide search (button, / and Ctrl+K), a check that the local model's reply is supported by its passages. Earlier: --><!-- course_page_template version 9.11.0:")

CSS = """/* 9.12.0: clickable references, page search */
button.rn,button.src{font:inherit;border:0;background:none;cursor:pointer;color:var(--blue);text-decoration:underline;padding:0 .1rem;min-width:24px;min-height:24px}
button.rn{font-size:.78rem;vertical-align:super;line-height:1}
button.src{font-size:.78rem;text-align:left;border-radius:6px;padding:.1rem .4rem;background:var(--card);text-decoration:none;color:var(--ink);border:1px solid var(--line)}
button.src:hover,button.rn:hover{background:var(--yellow);color:#1F2933}
button.src.flash{outline:3px solid var(--blue);background:var(--yellow);color:#1F2933}
#srchBtn{margin-left:auto;background:var(--yellow);color:#1F2933;border:0;font-weight:700}
#srch{position:fixed;inset:0;background:rgba(15,21,28,.55);z-index:60;display:flex;align-items:flex-start;justify-content:center;padding:6vh 1rem 1rem}
#srch[hidden]{display:none}
#srch .box{background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:14px;width:min(46rem,100%);max-height:86vh;display:flex;flex-direction:column;box-shadow:0 12px 40px rgba(0,0,0,.35)}
#srch .bar{display:flex;gap:.5rem;padding:.7rem;border-bottom:1px solid var(--line)}
#srch input{flex:1;font-size:1.05rem;padding:.5rem .7rem;border-radius:8px;border:1px solid var(--line);background:var(--panel);color:var(--ink)}
#srch .res{overflow:auto;padding:.4rem .7rem .8rem}
#srch .hit{display:block;width:100%;text-align:left;border:0;background:none;color:var(--ink);padding:.45rem .5rem;border-radius:8px;cursor:pointer;font:inherit}
#srch .hit:hover,#srch .hit:focus{background:var(--card);outline:2px solid var(--blue)}
#srch .hit b{color:var(--blue)}#srch .hit small{display:block;color:var(--mute)}#srch mark{background:var(--yellow);color:#1F2933;border-radius:3px}
#srch .grp{font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:var(--mute);margin:.6rem .3rem .2rem}
#srch .foot{padding:.5rem .8rem;border-top:1px solid var(--line);font-size:.85rem;color:var(--mute)}
.srcview .full{white-space:pre-wrap;background:var(--card);border-radius:8px;padding:.6rem .8rem;margin:.4rem 0}
"""
rep("</style>", CSS + "</style>")

rep('<div class="fsctl" role="group" aria-label="Text size">', '<button class="btn g" id="srchBtn" aria-label="Search this page" title="Search this page (press / or Ctrl+K)" aria-haspopup="dialog">🔍 Search</button><div class="fsctl" role="group" aria-label="Text size">')
rep('<div id="ctx" role="menu" hidden></div>', '<div id="srch" aria-label="Search this page" hidden><div class="box"><div class="bar"><input id="srchq" type="search" placeholder="Search concepts, definitions and code..." aria-label="Search this page" autocomplete="off"><button class="btn g" id="srchX" aria-label="Close search">✕</button></div><div class="res" id="srchres" aria-live="polite"></div><div class="foot">Enter opens the first result · ↑ ↓ move · Esc closes</div></div></div><div id="ctx" role="menu" hidden></div>')

# references
rep("function refs(h){return h.replace(/\\[(\\d+)\\]/g,'<span class=\"rn\">[$1]</span>')}",
"""let CUR_TOP=null;
function chunkAttr(c){return 'data-chunk="'+KIT.chunks.indexOf(c)+'" data-cl="'+esc(c.label)+'"'}
function refs(h){return h.replace(/\\[(\\d+)\\]/g,(m,n)=>{const x=CUR_TOP&&KIT.chunks&&CUR_TOP[n-1];return x&&KIT.chunks.indexOf(x.c)>=0?'<button class="rn" '+chunkAttr(x.c)+' data-n="'+n+'" title="Show source '+n+': '+esc(x.c.label)+'" aria-label="Show source '+n+': '+esc(x.c.label)+'">['+n+']</button>':'<span class="rn">'+m+'</span>'})}""")
rep("""top.slice(0,6).map((x,i)=>'<span class="src '+x.c.kind+'" title="'+esc(x.c.text)+'">['+(i+1)+'] '+KIND_LABEL[x.c.kind]+': '+esc(x.c.label)+'</span>'""",
    """top.slice(0,6).map((x,i)=>'<button class="src '+x.c.kind+'" '+chunkAttr(x.c)+' data-n="'+(i+1)+'" title="Show this passage: '+esc(x.c.text)+'">['+(i+1)+'] '+KIND_LABEL[x.c.kind]+': '+esc(x.c.label)+'</button>'""")
# answer quality and example trigger
rep("(/example|show|code|demonstrat/i.test(q)?exampleBlock(top,ag):'')", "(/example|show|code|demonstrat|construct|syntax|written|write|how (do|does|would|can|is|are)\\b/i.test(q)?exampleBlock(top,ag):'')")
rep("if(KIT.llm){text=await llmAnswer(a,q,top,hist);by='live LLM, in a background thread'}",
    "if(KIT.llm){text=await llmAnswer(a,q,top,hist);const g=groundText(text,top);if(g.text){by='live LLM, in a background thread'+(g.dropped?'; '+g.dropped+' sentence'+(g.dropped>1?'s':'')+' not supported by the passages removed':'');text=g.text}else{text=null;by='retrieval; the local model\\u2019s reply was not supported by the passages, so their own sentences are shown'}}")
rep("    html=answerHtml(cx,text,q,top,by,text?null:composedPicked(a,cx.q,top),a)+sourcesHtml(top,how)}}}", "    CUR_TOP=top;html=answerHtml(cx,text,q,top,by,text?null:composedPicked(a,cx.q,top),a)+sourcesHtml(top,how)}}}")

JS = r"""
// ---------- 9.12.0: grounding check, source viewer, page search ----------
function groundText(text,top){const known=new Set();top.forEach(x=>toks(x.c.text+' '+x.c.label).forEach(w=>known.add(w)));let dropped=0;
 const parts=String(text||'').split(/(```[\s\S]*?```)/);
 const out=parts.map(p=>{if(/^```/.test(p))return p;
  return p.split('\n').map(line=>{const bullet=(line.match(/^\s*(?:[-*\u2022]|\d+[.)])\s+/)||[''])[0];const body=line.slice(bullet.length);
   const sents=body.split(/(?<=[.!?])\s+/).filter(x=>x.trim());
   const keep=sents.filter(sn=>{const T=toks(sn.replace(/\[\d+\]/g,''));if(T.length<3)return true;const hit=T.filter(w=>known.has(w)).length;if(hit/T.length>=0.6)return true;dropped++;return false});
   return keep.length?bullet+keep.join(' '):''}).join('\n')}).join('');
 const t=out.replace(/\n{3,}/g,'\n\n').trim();return {text:t.replace(/\[\d+\]|\s|[.,;:!?-]/g,'').length>=20?t:null,dropped}}
async function openSource(i,cl,from){const ch=await ensureChunks();let c=ch[i];if(!c||(cl&&c.label!==cl))c=ch.find(x=>x.label===cl)||c;if(!c)return;
 const card=document.getElementById('card'),T=c.text,men=D.nodes.filter(n=>n.label.length>3&&T.toLowerCase().includes(n.label.toLowerCase())&&n.id!==c.concept).slice(0,8);
 card.hidden=false;card.classList.add('open');card.classList.add('srcview');
 card.innerHTML='<button class="close" data-close title="Close details (Esc)" aria-label="Close details">✕</button><h3>📄 '+esc(c.label)+'</h3><p class="note">'+KIND_LABEL[c.kind]+(c.src&&c.src!=='this page'?' · '+esc(c.src):' · this page')+'</p><div class="full">'+esc(T)+'</div>'
  +(c.concept&&byId[c.concept]?'<p><button class="btn" data-go="'+c.concept+'">Go to the section: '+esc(byId[c.concept].label)+'</button></p>':'')
  +(men.length?'<div class="kv">Concepts it mentions</div><p>'+men.map(n=>'<button class="jump" data-go="'+n.id+'">'+esc(n.label)+'</button>').join('')+'</p>':'')
  +'<p><button class="btn g" data-search="'+esc(c.label.replace(/\s*\([^)]*\)\s*$/,''))+'">Search the page for this</button></p>';
 document.querySelectorAll('button.src.flash').forEach(b=>b.classList.remove('flash'));
 if(from){const log=from.closest('.log,.conv,[id$="-log"]')||document;log.querySelectorAll('button.src[data-cl]').forEach(b=>{if(b.dataset.cl===c.label)b.classList.add('flash')})}}
let SIDX=null,SRCH_LAST=null;
function sIndex(){if(SIDX)return SIDX;SIDX=D.nodes.map(n=>{const path=[];let p=n.parent;while(p&&byId[p]){path.unshift(byId[p].label);p=byId[p].parent}
  const def=(n.definition||n.body||'');const code=n.io?n.io.code+' '+n.io.out:'';return {n,path,label:n.label.toLowerCase(),lt:toks(n.label),dt:toks(def+' '+(n.example||'')),ct:code.toLowerCase(),def,code}});return SIDX}
function sSnippet(txt,qw){const l=txt.toLowerCase();let at=-1;for(const w of qw){const k=l.indexOf(w);if(k>=0){at=k;break}}if(at<0)return esc(txt.slice(0,140));const a=Math.max(0,at-50),z=Math.min(txt.length,a+170);let sn=esc(txt.slice(a,z));qw.forEach(w=>{sn=sn.replace(new RegExp('('+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig'),'<mark>$1</mark>')});return (a>0?'\u2026':'')+sn+(z<txt.length?'\u2026':'')}
function searchConcepts(q){const raw=q.toLowerCase().trim();if(!raw)return [];const qt=toks(q),qw=raw.split(/\s+/).filter(w=>w.length>1);
 return sIndex().map(e=>{let sc=0;if(e.label===raw)sc+=20;else if(e.label.includes(raw))sc+=10;qt.forEach(t=>{if(e.lt.includes(t))sc+=4;if(e.dt.includes(t))sc+=1;});if(e.ct&&qw.some(w=>e.ct.includes(w)))sc+=2;
  if(qt.length&&qt.every(t=>e.lt.includes(t)||e.dt.includes(t)))sc+=3;return {e,sc}}).filter(x=>x.sc>0).sort((a,b)=>b.sc-a.sc).slice(0,12).map(x=>Object.assign(x,{qw}))}
function hitHtml(x){const e=x.e;return '<button class="hit" data-hit="'+e.n.id+'"><b>'+ICON[e.n.level]+' '+esc(e.n.label)+'</b>'+(e.path.length?' <span class="note">in '+esc(e.path.join(' \u203A '))+'</span>':'')+'<small>'+sSnippet(e.def||e.code,x.qw)+'</small></button>'}
async function runSearch(){const q=document.getElementById('srchq').value,out=document.getElementById('srchres');SRCH_LAST=q;
 if(!q.trim()){out.innerHTML='<p class="note">Type a word from a concept, a definition or a piece of code. Try "loop", "return" or "elif".</p>';return}
 const hits=searchConcepts(q);out.innerHTML=(hits.length?'<div class="grp">Concepts on this page</div>'+hits.map(hitHtml).join(''):'<p class="note">No concept on this page matches "'+esc(q)+'".</p>')+'<div class="grp">Book, course and research</div><button class="btn g" id="srchmore">Also search the book, course and research passages</button>'}
async function searchPassages(){const q=SRCH_LAST||'',out=document.getElementById('srchres'),btn=document.getElementById('srchmore');if(btn)btn.textContent='Searching...';
 const {top}=await rank({covers:[]},q,8);const qw=q.toLowerCase().split(/\s+/).filter(w=>w.length>1);const qt=toks(q);
 const rows=top.filter(x=>qt.length===0||toks(x.c.text+' '+x.c.label).some(w=>qt.includes(w))).slice(0,8);
 const html=rows.length?rows.map(x=>'<button class="hit" data-chunk="'+KIT.chunks.indexOf(x.c)+'" data-cl="'+esc(x.c.label)+'"><b>\uD83D\uDCC4 '+esc(x.c.label)+'</b> <span class="note">'+KIND_LABEL[x.c.kind]+'</span><small>'+sSnippet(x.c.text,qw)+'</small></button>').join(''):'<p class="note">No passage matches.</p>';
 const m=document.getElementById('srchmore');if(m)m.outerHTML='<div id="srchpass">'+html+'</div>'}
function openSearch(q){const d=document.getElementById('srch');SRCH_FROM=document.activeElement;d.setAttribute('role','dialog');d.setAttribute('aria-modal','true');d.hidden=false;const i=document.getElementById('srchq');if(typeof q==='string')i.value=q;runSearch();i.focus();i.select()}
let SRCH_FROM=null;
function closeSearch(){const d=document.getElementById('srch');if(d.hidden)return;d.hidden=true;d.removeAttribute('role');d.removeAttribute('aria-modal');try{SRCH_FROM&&SRCH_FROM.focus&&SRCH_FROM.focus()}catch(e){}}
document.getElementById('srchq').addEventListener('input',runSearch);
document.getElementById('srch').addEventListener('keydown',e=>{const hits=[...document.querySelectorAll('#srch .hit')];
 if(e.key==='Escape'){e.stopPropagation();closeSearch();return}
 if(e.key==='Enter'&&e.target.id==='srchq'&&hits[0]){e.preventDefault();hits[0].click();return}
 if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();const i=hits.indexOf(document.activeElement);const j=e.key==='ArrowDown'?Math.min(hits.length-1,i+1):i-1;if(j<0)document.getElementById('srchq').focus();else hits[j]&&hits[j].focus()}});
document.addEventListener('keydown',e=>{const el=e.target,typing=el&&(el.matches('input,textarea,select')||el.isContentEditable);
 if((e.key==='/'&&!typing&&!e.ctrlKey&&!e.metaKey)||((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k')){e.preventDefault();openSearch()}},true);
document.addEventListener('click',e=>{const t=e.target;
 if(t.id==='srchBtn'||t.closest('#srchBtn')){openSearch();return}
 if(t.id==='srchX'){closeSearch();return}
 if(t.id==='srch'){closeSearch();return}
 if(t.id==='srchmore'){searchPassages();return}
 const h=t.closest('[data-hit]');if(h){const id=h.dataset.hit;closeSearch();goTo(id);openCard(id);return}
 const ck=t.closest('[data-chunk]');if(ck){e.stopImmediatePropagation();const inSearch=!!ck.closest('#srch');if(inSearch)closeSearch();openSource(+ck.dataset.chunk,ck.dataset.cl,inSearch?null:ck);return}
 const sq=t.closest('[data-search]');if(sq){openSearch(sq.dataset.search)}},true);
"""
rep("// ---------- one delegated handler for clicks, context menus and tooltips ----------", JS + "// ---------- one delegated handler for clicks, context menus and tooltips ----------")

# the worked example is found also for a passage that names a concept in its label ("If statement (concept section)")
rep("const cand=top.map(x=>x.c.concept&&byId[x.c.concept]||D.nodes.find(n=>n.io&&x.c.text.includes(n.io.code)))", "const nm=x=>{const l=String(x.c.label).replace(/\\s*\\([^)]*\\)\\s*$/,'').toLowerCase();return D.nodes.find(n=>n.label.toLowerCase()===l)};const cand=top.map(x=>x.c.concept&&byId[x.c.concept]||nm(x)||D.nodes.find(n=>n.io&&x.c.text.includes(n.io.code)))")

# a concept with no executed example but a written one (the first line of an if statement) shows that as its form
rep("if(n&&n.io)return '<div class=\"exblock\">", "if(n&&!n.io&&n.example&&!cand.some(m=>m&&m.io)&&/^[a-z_]+.*[:)]\\s*$/i.test(n.example))return '<div class=\"exblock\"><div class=\"wl\">Its form: '+esc(n.label)+'</div><pre>'+esc(n.example)+'</pre></div>';if(n&&n.io)return '<div class=\"exblock\">")
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("ok", len(s))
