"""Makes course_page_template_v9_9_0.html from v9_8_0. Usage: template_patch_v9_9_0.py <in.html> <out.html>
9.9.0, from the owner's review of 2026-09-29 (14:01 Istanbul): (1) choosing a SPARQL sample loads it at once, no Load button;
(2) an agent's answer is laid out for reading - a lead sentence, points as a list, code and Python's names coloured, the example
in a code block, related concepts as chips - and free text from a language model is laid out the same way (paragraphs, lists,
code fences, inline code, bold); (3) the Quiz has a question builder: it makes a new question about any concept, subject or the
whole chapter, on request, from the chapter's own data (predict an output, name a concept from its definition, place a concept
in the taxonomy, pick a kind of a concept), prefers concepts not yet asked, and can ask one question for every concept."""
import sys
s = open(sys.argv[1], encoding="utf-8").read()
def rep(old, new, count=1):
    global s
    assert s.count(old) >= 1, old[:90]
    s = s.replace(old, new, count)

# 1. SPARQL: choosing loads
rep('<button class="btn g" id="sqload">Load sample</button>', '')
rep("document.addEventListener('change',e=>{const id=e.target.id;", "document.addEventListener('change',e=>{const id=e.target.id;\n if(id==='sqsamp'){document.getElementById('sqtext').value=SPARQL_SAMPLES[+e.target.value][1];fitViews()}")

# 2. readable answers
CSS = r"""
.msg .lead{font-weight:600;margin:.1rem 0 .35rem}.msg ul.pts,.msg ul.fmt,.msg ol.fmt{margin:.2rem 0 .5rem 1.15rem;padding:0}.msg ul.pts li,.msg ul.fmt li,.msg ol.fmt li{margin:.22rem 0}.msg p.fmt{margin:.25rem 0}
.msg .rn{font-size:.72rem;color:var(--mute);vertical-align:super;margin-left:.1rem}
.tk{font-family:"Courier New",monospace;background:#EEF3F8;border:1px solid var(--line);border-radius:4px;padding:0 .22rem;color:#1B3A57;font-size:.92em}
.tk-exc{color:#B3261E;background:#FDEDEC}.tk-lit{color:#6A1B9A}.tk-str{color:#1E6B2E}.tk-lv-debug{color:#56606B}.tk-lv-info{color:#0B5CAD}.tk-lv-warning{color:#8A5A00;background:#FFF6DB}.tk-lv-error{color:#B3261E;background:#FDEDEC}.tk-lv-critical{color:#7A0C0C;background:#FBE0DE;font-weight:700}
.exblock{margin:.4rem 0;border:1px solid var(--line);border-left:4px solid var(--blue);border-radius:8px;overflow:hidden;background:var(--bg)}.exblock .wl{padding:.2rem .6rem;background:var(--card)}.exblock pre{margin:0;padding:.45rem .7rem;background:var(--code);color:#E6EDF3;font:.9rem "Courier New",monospace;white-space:pre-wrap}.exblock .exout{padding:.3rem .7rem;font-family:"Courier New",monospace}
.msg pre.fmt{margin:.4rem 0;padding:.45rem .7rem;background:var(--code);color:#E6EDF3;border-radius:8px;font:.9rem "Courier New",monospace;white-space:pre-wrap;overflow:auto}
.rel{margin:.35rem 0 .1rem;display:flex;flex-wrap:wrap;gap:.3rem;align-items:center}.rel .c{border:1px solid var(--line);border-radius:999px;padding:.05rem .6rem;background:var(--card);cursor:pointer}
.msg.agent.answer{border-left:4px solid var(--blue)}
.qgen{margin-top:1.2rem;border-top:2px solid var(--line);padding-top:.6rem}.qgen fieldset{border:0;background:var(--card);border-radius:12px;margin:.5rem 0;padding:.7rem .9rem}.qgen fieldset.right{border-left:4px solid var(--ok)}.qgen fieldset.wrong{border-left:4px solid var(--bad)}
.qgen pre{background:var(--code);color:#E6EDF3;border-radius:8px;padding:.45rem .7rem;font:.92rem "Courier New",monospace;white-space:pre-wrap}.qgen .qdef{border-left:4px solid var(--yellow);padding:.2rem .7rem;background:var(--bg);border-radius:0 8px 8px 0;margin:.3rem 0}
.qgen .cover{height:.5rem;background:var(--line);border-radius:999px;overflow:hidden;max-width:24rem}.qgen .cover i{display:block;height:100%;background:var(--ok)}
"""
rep(".quiz fieldset{", CSS + ".quiz fieldset{")

JS_FMT = r"""
// ---- readable answers (9.9.0) ----
const HL_RE=/(\b[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+(?:\(\))?|\b[A-Za-z_]\w*\(\)|'[^'\n]{1,40}'|"[^"\n]{1,40}"|\b[A-Z][A-Za-z]*(?:Error|Exception)\b|\b(?:DEBUG|INFO|WARNING|ERROR|CRITICAL)\b|\b(?:True|False|None)\b)/g;
const HL_SKIP=/^(e\.g|i\.e|etc|vs|U\.S|a\.k\.a)\.?$/i;
function hl(t){return String(t).split(HL_RE).map((p,i)=>{if(i%2===0)return esc(p);if(HL_SKIP.test(p))return esc(p);
 let c='tk';if(/(Error|Exception)$/.test(p)&&/^[A-Z]/.test(p))c+=' tk-exc';else if(/^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$/.test(p))c+=' tk-lv-'+p.toLowerCase();else if(/^(True|False|None)$/.test(p))c+=' tk-lit';else if(/^['"]/.test(p))c+=' tk-str';
 return '<code class="'+c+'">'+esc(p)+'</code>'}).join('')}
function refs(h){return h.replace(/\[(\d+)\]/g,'<span class="rn">[$1]</span>')}
// a language model's free text: paragraphs, lists, code fences, `inline code` and **bold**
function fmt(t){const lines=String(t).replace(/\r/g,'').split('\n');let out='',list=null,para=[],fence=null,code=[];
 const inline=x=>esc(x).replace(/`([^`]+)`/g,'<code class="tk">$1</code>').replace(/\*\*([^*]+)\*\*/g,'<b>$1</b>');
 const flushP=()=>{if(para.length){out+='<p class="fmt">'+refs(inline(para.join(' ')))+'</p>';para=[]}},flushL=()=>{if(list){out+='</'+list+'>';list=null}};
 for(const ln of lines){
  if(fence!==null){if(/^```/.test(ln)){out+='<pre class="fmt">'+esc(code.join('\n'))+'</pre>';fence=null;code=[]}else code.push(ln);continue}
  if(/^```/.test(ln)){flushP();flushL();fence=ln.slice(3).trim();continue}
  const b=ln.match(/^\s*(?:[-*\u2022])\s+(.*)$/),n=ln.match(/^\s*\d+[.)]\s+(.*)$/);
  if(b||n){flushP();const tag=b?'ul':'ol';if(list!==tag){flushL();out+='<'+tag+' class="fmt">';list=tag}out+='<li>'+refs(inline((b||n)[1]))+'</li>';continue}
  if(!ln.trim()){flushP();flushL();continue}
  flushL();para.push(ln.trim())}
 if(fence!==null)out+='<pre class="fmt">'+esc(code.join('\n'))+'</pre>';flushP();flushL();return out}
function exampleBlock(top){for(const x of top){const n=x.c.concept&&byId[x.c.concept]||D.nodes.find(n=>n.io&&x.c.text.includes(n.io.code));if(n&&n.io)return '<div class="exblock"><div class="wl">For example: '+esc(n.label)+'</div><pre>'+esc(n.io.code)+'</pre><div class="exout">\u2192 '+hl(n.io.out)+'</div></div>'}return ''}
function relatedChips(top){const seen=new Set(),ids=[];top.forEach(x=>{const c=x.c.concept;if(c&&byId[c]&&!seen.has(c)){seen.add(c);ids.push(c)}});
 return ids.length?'<div class="rel"><span class="note">Related:</span> '+ids.slice(0,5).map(c=>'<span class="c" data-c="'+c+'" role="button" tabindex="0">'+esc(byId[c].label)+'</span>').join('')+'</div>':''}
function answerHtml(cx,text,q,top,by,picked){
 let body;
 if(text)body=fmt(text);
 else{const P=picked||[];body=P.length?'<p class="lead">'+refs(hl(P[0].t+' ['+(P[0].i+1)+']'))+'</p>'+(P.length>1?'<ul class="pts">'+P.slice(1).map(p=>'<li>'+refs(hl(p.t+' ['+(p.i+1)+']'))+'</li>').join('')+'</ul>':''):''}
 return (cx.follow?'<span class="note">Following on from "'+esc(cx.follow)+'".</span> ':'')+body+(/example|show|code|demonstrat/i.test(q)?exampleBlock(top):'')+relatedChips(top)+' <span class="note">('+by+')</span>'}
"""
rep("function composedAnswer(a,q,top){", JS_FMT + "function composedAnswer(a,q,top){return composedPicked(a,q,top).map(p=>esc(p.t)+' ['+(p.i+1)+']').join(' ')}\nfunction composedPicked(a,q,top){")
rep(" return picked.map(p=>esc(p.t)+' ['+(p.i+1)+']').join(' ')}", " return picked}")
rep("""html=(cx.follow?'<span class="note">Following on from "'+esc(cx.follow)+'".</span> ':'')+(text?esc(text):composedAnswer(a,cx.q,top)+(/example|show|code|demonstrat/i.test(q)?exampleFor(top):''))+' <span class="note">('+by+')</span>'+sourcesHtml(top,how)}}}""",
    """html=answerHtml(cx,text,q,top,by,text?null:composedPicked(a,cx.q,top))+sourcesHtml(top,how)}}}""")
rep("holder.className='msg agent';holder.innerHTML=html;CONV[aid].push", "holder.className='msg agent'+(/class=\"(lead|fmt|pts)\"/.test(html)?' answer':'');holder.innerHTML=html;CONV[aid].push")

# 3. question builder
rep("<h2>\u2714 Quiz</h2>'+Q.map(", "<h2>\u2714 Quiz</h2><p class=\"note\">The chapter quiz below covers the chapter objectives. Under it, the question builder makes a new question about any concept on request, so every concept of the chapter can be asked.</p>'+Q.map(")
rep("""<p class="verdict" id="q'+k+'-fb"></p></fieldset>'}).join('')+'</div>';""", """<p class="verdict" id="q'+k+'-fb"></p></fieldset>'}).join('')+qgenHtml()+'</div>';""")
QG = r"""
// ---- question builder (9.9.0): new questions from the chapter's own data, on request ----
const QG={asked:{},right:{}};try{const o=JSON.parse(localStorage.getItem('qgen:'+D.title)||'{}');Object.assign(QG.asked,o.asked||{});Object.assign(QG.right,o.right||{})}catch(e){}
const qgSave=()=>{try{localStorage.setItem('qgen:'+D.title,JSON.stringify({asked:QG.asked,right:QG.right}))}catch(e){}};
const qShuf=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
const qKids=id=>D.nodes.filter(n=>n.parent===id),qUnder=id=>{const r=[];const w=i=>qKids(i).forEach(k=>{r.push(k.id);w(k.id)});w(id);return r};
function qFirst(n){return (n.definition||n.body||'').split(/(?<=[.!?])\s+(?=[A-Z])/)[0]}
function qMask(n){let t=qFirst(n);String(n.label).split(/[\s\-\/]+/).filter(w=>w.length>=4).forEach(w=>{const st=w.slice(0,Math.max(4,w.length-2));t=t.replace(new RegExp('\\b'+st.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\w*','gi'),'\u2026\u2026')});return t}
const QG_KINDS={predict:'Predict the output',name:'Name the concept',place:'Place it in the taxonomy',kind:'Pick a kind of'};
function qKindsFor(n){const k=['name'];if(n.io)k.push('predict');if(n.parent)k.push('place');if(qKids(n.id).length)k.push('kind');return k}
function qMake(cid,kind){const n=byId[cid];if(!n||!qKindsFor(n).includes(kind))return null;const others=D.nodes.filter(x=>x.id!==cid);let q={kind,concept:cid};
 const four=(right,wrong)=>{const w=[...new Set(wrong.filter(x=>x!==right))].slice(0,3);const o=qShuf([right].concat(w));q.options=o;q.answer=o.indexOf(right)};
 if(kind==='predict'){const outs=[...new Set(D.nodes.filter(x=>x.io&&x.id!==cid).map(x=>String(x.io.out)))].filter(x=>x!==String(n.io.out));const pad=['None','True','False','Error','0','[]','1'].filter(x=>x!==String(n.io.out)&&!outs.includes(x));
  four(String(n.io.out),qShuf(outs).concat(pad));q.q='What does this give when it runs?';q.code=n.io.code;q.why='Python gave '+n.io.out+' when this page was built, and the page re-runs it in your browser.'}
 else if(kind==='name'){const same=others.filter(x=>x.level===n.level&&x.parent===n.parent),lvl=others.filter(x=>x.level===n.level&&x.parent!==n.parent);four(n.label,qShuf(same).concat(qShuf(lvl)).map(x=>x.label));q.q='Which concept does this describe?';q.def=qMask(n);q.why=(qFirst(n)||n.label)}
 else if(kind==='place'){const p=byId[n.parent],sib=D.nodes.filter(x=>x.level===p.level&&x.id!==p.id);four(p.label,qShuf(sib).map(x=>x.label));q.q='Where does \u201c'+n.label+'\u201d sit in the chapter\u2019s taxonomy? It is a kind of\u2026';q.why=n.label+' is a kind of '+p.label+' in the chapter\u2019s taxonomy.'}
 else if(kind==='kind'){const kids=qKids(cid),under=new Set(qUnder(cid).concat([cid])),right=qShuf(kids)[0],wrong=qShuf(D.nodes.filter(x=>!under.has(x.id)&&x.level>=right.level));four(right.label,wrong.map(x=>x.label));q.q='Which of these is a kind of \u201c'+n.label+'\u201d?';q.why=n.label+' has these kinds: '+kids.map(k=>k.label).join(', ')+'.'}
 return q.options&&q.options.length>=3?q:null}
function qScopeIds(scope){if(!scope||scope==='all')return D.nodes.map(n=>n.id);return [scope].concat(qUnder(scope))}
function qNext(scope,kind){const ids=qScopeIds(scope).filter(id=>!kind||kind==='any'||qKindsFor(byId[id]).includes(kind));if(!ids.length)return null;const least=Math.min(...ids.map(i=>QG.asked[i]||0));const pick=qShuf(ids.filter(i=>(QG.asked[i]||0)===least))[0];const ks=kind&&kind!=='any'?[kind]:qShuf(qKindsFor(byId[pick]));for(const k of ks){const q=qMake(pick,k);if(q)return q}return null}
let qgN=0;
function qRender(q){const id='g'+(++qgN);return '<fieldset data-gen="1" data-answer="'+q.answer+'" data-concept="'+q.concept+'" data-why="'+esc(q.why)+'"><legend>'+esc(QG_KINDS[q.kind])+': '+esc(q.q)+'</legend>'+(q.code?'<pre>'+esc(q.code)+'</pre>':'')+(q.def?'<div class="qdef">'+esc(q.def)+'</div>':'')+q.options.map((o,j)=>'<label style="display:block"><input type="radio" name="'+id+'" value="'+j+'"> '+(q.kind==='predict'?'<code class="tk">'+esc(o)+'</code>':esc(o))+'</label>').join('')+'<button class="btn" data-gcheck="1">Check</button> <span class="verdict" aria-live="polite"></span></fieldset>'}
function qCover(){const all=D.nodes.length,a=D.nodes.filter(n=>QG.asked[n.id]).length,r=D.nodes.filter(n=>QG.right[n.id]).length;const el=document.getElementById('qgcover');if(el)el.innerHTML='Every one of the '+all+' concepts can be asked about. You have been asked about <b>'+a+'</b> and answered <b>'+r+'</b> correctly. <div class="cover" role="img" aria-label="'+r+' of '+all+' concepts answered correctly"><i style="width:'+Math.round(100*r/all)+'%"></i></div>'}
function qgenHtml(){const tops=D.nodes.filter(n=>n.level===1),mids=D.nodes.filter(n=>n.level===2);
 return '<section class="qgen" id="qgen"><h3>\U0001F9E9 Build your own questions</h3><p class="note">Questions are made on request from this chapter\u2019s own concepts, definitions, examples and taxonomy. A concept you have not been asked about yet comes first.</p><div class="row"><label class="note" for="qgscope">About</label><select id="qgscope" aria-label="Scope of the question"><option value="all">the whole chapter</option>'+tops.map(t=>'<optgroup label="'+esc(t.label)+'"><option value="'+t.id+'">'+esc(t.label)+' (all)</option>'+mids.filter(m=>m.parent===t.id).map(m=>'<option value="'+m.id+'">'+esc(m.label)+'</option>').join('')+'</optgroup>').join('')+'</select><label class="note" for="qgkind">Kind</label><select id="qgkind" aria-label="Kind of question"><option value="any">any</option>'+Object.entries(QG_KINDS).map(([k,l])=>'<option value="'+k+'">'+esc(l)+'</option>').join('')+'</select><button class="btn" id="qgnew">New question</button><button class="btn g" id="qgall">One question for every concept</button><button class="btn g" id="qgclear">Clear</button></div><p class="note" id="qgcover"></p><div id="qgout" aria-live="polite"></div><p class="verdict" id="qgscore"></p></section>'}
"""
rep("const PSTAGES=", QG + "const PSTAGES=")
rep("if(t.dataset.check){", r"""if(t.id==='qgnew'){const q=qNext(document.getElementById('qgscope').value,document.getElementById('qgkind').value),o=document.getElementById('qgout');o.innerHTML=q?qRender(q):'<p class="note">No question of that kind for that part of the chapter.</p>';document.getElementById('qgscore').textContent='';qCover();return}
 if(t.id==='qgall'){const sc=document.getElementById('qgscope').value,ids=qScopeIds(sc),qs=ids.map(id=>{for(const k of qShuf(qKindsFor(byId[id]))){const q=qMake(id,k);if(q)return q}return null}).filter(Boolean);document.getElementById('qgout').innerHTML=qs.map(qRender).join('');document.getElementById('qgscore').textContent='0 of '+qs.length+' answered correctly';qCover();return}
 if(t.id==='qgclear'){QG.asked={};QG.right={};qgSave();document.getElementById('qgout').innerHTML='';document.getElementById('qgscore').textContent='';qCover();return}
 if(t.dataset.gcheck){const fs=t.closest('fieldset'),c=fs.querySelector('input:checked'),fb=fs.querySelector('.verdict');if(!c){fb.textContent='Choose an answer first.';return}const ok=c.value===fs.dataset.answer,cid=fs.dataset.concept;if(!fs.dataset.done){fs.dataset.done='1';QG.asked[cid]=(QG.asked[cid]||0)+1;if(ok)QG.right[cid]=(QG.right[cid]||0)+1;qgSave()}
  fs.classList.toggle('right',ok);fs.classList.toggle('wrong',!ok);fb.innerHTML=(ok?'Correct. ':'Not quite. ')+esc(fs.dataset.why)+' <button class="jump" data-go="'+cid+'">Go to the concept</button>';
  const all=document.querySelectorAll('#qgout fieldset'),right=document.querySelectorAll('#qgout fieldset.right').length,done=document.querySelectorAll('#qgout fieldset[data-done]').length;if(all.length>1)document.getElementById('qgscore').textContent=right+' of '+all.length+' answered correctly ('+done+' checked)';qCover();return}
 if(t.dataset.check){""")
open(sys.argv[2], "w", encoding="utf-8").write(s); print("written", sys.argv[2], len(s))
