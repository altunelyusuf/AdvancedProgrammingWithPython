"""Makes course_page_template_v9_13_0.html from v9_12_0. Usage: template_patch_v9_13_0.py <in.html> <out.html>
9.13.0 (the owner's go-ahead of 2026-09-30 on the proposals of 9.12.0): (1) progress - a 'Mark as understood' control on every section and in the detail card, a count in the
title bar, a tick beside understood items and a dot beside visited ones in the explorer; (2) a review queue - a question answered wrongly (in the question builder or an
exercise) returns after 10 minutes, then 1, 3 and 7 days, through a Review button; (3) a link for every section and tab (#c=<concept>, #t=<tab>), the browser's back button
and forward button, and a Copy link button in the detail card; (4) copy buttons on code blocks and beside the Playground; (5) a note for every concept, kept in the
browser; (6) a print style and a Cheat sheet view of every concept; (7) Yes / No / Report-an-error marks under every answer of an agent; (8) Your data lists progress, notes,
review queue and marks, which can be copied out as Markdown or JSON (nothing leaves the browser by itself); (9) Code exercises made from the chapter's own executed examples -
put the lines in order, fill in a blank, make a program that raises an error run - each checked by running the code."""
import sys
s = open(sys.argv[1], encoding="utf-8").read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:90])
    s = s.replace(old, new)

rep("<!-- course_page_template version 9.12.0:", "<!-- course_page_template version 9.13.0: progress, review queue, section links and back button, copy buttons, notes, print style and cheat sheet, marks on answers, code exercises. Earlier: --><!-- course_page_template version 9.12.0:")

CSS = """/* 9.13.0: progress, notes, exercises, print */
#progBadge{margin-left:.6rem;color:#E6EDF3;font-size:.9rem;font-weight:700;white-space:nowrap}
.tn.done::after{content:' \\2713';color:var(--ok);font-weight:700}.tn.seen::after{content:' \\00B7';color:var(--mute);font-weight:700}
.markrow{margin:.2rem 0 .4rem}button.mark[aria-pressed=true]{background:var(--ok);color:#fff}
.cardx{margin-top:.8rem;border-top:1px solid var(--line);padding-top:.4rem}textarea.mynote{width:100%;min-height:4.5rem;font:inherit;border:1px solid var(--line);border-radius:8px;padding:.4rem;background:var(--panel);color:var(--ink)}
button.copy{display:block;margin:.1rem 0 .5rem auto;font-size:.8rem;padding:.05rem .5rem}
.fb{margin-top:.35rem;display:flex;flex-wrap:wrap;gap:.25rem;align-items:center}.fb .jump[aria-pressed=true]{background:var(--yellow);color:#1F2933}
fieldset.ex{border:1px solid var(--line);border-radius:10px;margin:.6rem 0;padding:.5rem .8rem}fieldset.ex.right{border-color:var(--ok)}fieldset.ex.wrong{border-color:var(--bad)}
ol.exlines{list-style:none;padding:0;margin:.4rem 0}ol.exlines li{display:flex;align-items:center;gap:.4rem;margin:.15rem 0}ol.exlines code{white-space:pre;background:var(--card);padding:.15rem .5rem;border-radius:6px;flex:1;overflow:auto}
input.exin{font:inherit;font-family:ui-monospace,monospace;border:1px solid var(--line);border-radius:6px;padding:.2rem .4rem;width:min(14rem,60%);background:var(--panel);color:var(--ink)}
pre.exsrc{white-space:pre-wrap}textarea.mycode{width:100%;min-height:7rem;font-family:ui-monospace,monospace;font-size:.95rem;border:1px solid var(--line);border-radius:8px;padding:.4rem;background:var(--code);color:#E6EDF3}
.cheat{column-width:22rem;column-gap:1.5rem}.cheat h3{break-after:avoid}.cs{break-inside:avoid;margin:0 0 .5rem}.cs pre{margin:.2rem 0}
@media print{header.top,aside.tree,aside.card,#ctx,#tip,#srch,#toast,.viewsub,.subtabs,nav.groups,#groups,.kit,button,.zbar,.markrow,.cardx,.fb,details.help{display:none!important}
 html,body{background:#fff!important;color:#000!important}.shell{display:block!important}main{overflow:visible!important;height:auto!important;padding:0!important;max-width:none!important}
 [role=tabpanel][hidden]{display:none!important}.cheat{column-count:2;column-width:auto;font-size:10pt}pre,code{background:#fff!important;color:#000!important;white-space:pre-wrap}pre{border:1px solid #999;padding:.2rem}
 a[href^=http]::after{content:" (" attr(href) ")";font-size:.8em}}
"""
rep("</style>", CSS + "</style>")

rep('aria-haspopup="dialog">🔍 Search</button>', 'aria-haspopup="dialog">🔍 Search</button><span id="progBadge" role="status" aria-label="Sections marked as understood">✓ 0/0</span>')
# review after a wrong answer
rep("if(ok)QG.right[cid]=(QG.right[cid]||0)+1;qgSave()}", "if(ok)QG.right[cid]=(QG.right[cid]||0)+1;qgSave();recordReview(cid,ok)}")
rep('<button class="btn g" id="qglive">Ask the live model</button>', '<button class="btn g" id="qgreview">Review</button><button class="btn g" id="qglive">Ask the live model</button>')
# navigation groups
rep("practice:[['quiz','✔ Quiz'],", "practice:[['quiz','✔ Quiz'],['exercises','🧩 Code exercises'],")
rep("reference:[['glossary','📖 Glossary'],", "reference:[['glossary','📖 Glossary'],['cheat','🖨 Cheat sheet'],")
rep("panes.innerHTML=P;", "P+=cheatPane();P+=exercisesPane();panes.innerHTML=P;")
rep("holder.innerHTML=html;CONV[aid].push", "if(/class=\"(lead|fmt|pts)\"/.test(html))html+=fbHtml();holder.innerHTML=html;CONV[aid].push")

JS = r"""
// ---------- 9.13.0: progress, review, links, copy, notes, cheat sheet, marks, exercises ----------
function lsGet(k,d){try{return Object.assign(d,JSON.parse(localStorage.getItem(k)||'{}'))}catch(e){return d}}
function lsSet(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
const PKEY='course-page-progress:'+D.title,NKEY='course-page-notes:'+D.title,RVKEY='course-page-review:'+D.title,FBKEY='course-page-feedback:'+D.title;
let PROG=lsGet(PKEY,{visited:{},done:{}}),NOTES=lsGet(NKEY,{}),REV=lsGet(RVKEY,{}),FBK=[];try{FBK=JSON.parse(localStorage.getItem(FBKEY)||'[]')}catch(e){}
const REV_INT=[600000,86400000,259200000,604800000];
function recordReview(cid,ok){if(!cid||!byId[cid])return;const it=REV[cid],now=Date.now();if(!ok)REV[cid]={box:0,due:now+REV_INT[0]};else if(it){it.box++;if(it.box>=REV_INT.length)delete REV[cid];else it.due=now+REV_INT[it.box]}lsSet(RVKEY,REV);reviewPaint()}
function reviewDue(){const now=Date.now();return Object.keys(REV).filter(k=>byId[k]&&REV[k].due<=now).sort((a,b)=>REV[a].due-REV[b].due)}
function reviewPaint(){const b=document.getElementById('qgreview');if(b){const n=reviewDue().length,w=Object.keys(REV).length;b.textContent='Review ('+n+' due'+(w>n?', '+(w-n)+' later':'')+')'}}
function progPaint(){const N=D.nodes.length,d=D.nodes.filter(x=>PROG.done[x.id]).length,v=D.nodes.filter(x=>PROG.visited[x.id]).length,b=document.getElementById('progBadge');if(b){b.textContent='✓ '+d+'/'+N;b.title=d+' of '+N+' sections marked as understood; '+v+' visited'}
 document.querySelectorAll('.tn[data-c]').forEach(t=>{const id=t.dataset.c;t.classList.toggle('done',!!PROG.done[id]);t.classList.toggle('seen',!PROG.done[id]&&!!PROG.visited[id])});
 document.querySelectorAll('button.mark').forEach(b=>{const on=!!PROG.done[b.dataset.mark];b.setAttribute('aria-pressed',on?'true':'false');b.textContent=on?'✓ Understood':'☐ Mark as understood'})}
function progVisit(id){if(id&&byId[id]&&!PROG.visited[id]){PROG.visited[id]=1;lsSet(PKEY,PROG);progPaint()}}
function progToggle(id){if(PROG.done[id])delete PROG.done[id];else{PROG.done[id]=1;PROG.visited[id]=1}lsSet(PKEY,PROG);progPaint()}
document.querySelectorAll('main section[data-source]').forEach(sec=>{const h=sec.querySelector('h2,h3,h4'),id=sec.dataset.concept;if(h&&id&&byId[id])h.insertAdjacentHTML('afterend','<div class="markrow"><button class="btn g mark" data-mark="'+id+'" aria-pressed="false">☐ Mark as understood</button></div>')});
// links and the back button
let NAV_SILENT=false,NAV_READY=false;
function hashPush(v){if(NAV_SILENT||!NAV_READY||location.hash==='#'+v)return;try{history.pushState(null,'','#'+v)}catch(e){}}
const _goTo=goTo,_showTab=showTab,_openCard=openCard;
goTo=function(id){NAV_SILENT=true;try{_goTo(id)}finally{NAV_SILENT=false}progVisit(id);hashPush('c='+id)};
showTab=function(k){_showTab(k);hashPush('t='+k)};
openCard=function(id){_openCard(id);progVisit(id);cardExtras(id)};
function applyHash(){const h=decodeURIComponent(location.hash.replace(/^#/,''));if(!h)return;NAV_SILENT=true;try{let m;if((m=h.match(/^c=(.+)$/))){if(byId[m[1]]){_goTo(m[1]);progVisit(m[1])}}else if((m=h.match(/^t=(.+)$/))){if(document.querySelector('[data-pane="'+m[1]+'"]')||GROUPS[m[1]])_showTab(m[1])}}finally{NAV_SILENT=false}}
addEventListener('popstate',applyHash);
setTimeout(()=>{applyHash();NAV_READY=true;progPaint();reviewPaint()},80);
function cardExtras(id){const c=document.getElementById('card');c.classList.remove('srcview');if(!byId[id])return;
 c.insertAdjacentHTML('beforeend','<div class="cardx"><div class="kv">My note</div><textarea class="mynote" data-note="'+id+'" rows="3" aria-label="My note on '+esc(byId[id].label)+'" placeholder="A note for yourself. It stays in this browser.">'+esc(NOTES[id]||'')+'</textarea><p class="row"><button class="btn g mark" data-mark="'+id+'" aria-pressed="false"></button><button class="btn g" data-link="'+id+'">Copy link to this section</button></p></div>');progPaint()}
document.addEventListener('input',e=>{const t=e.target;if(t.matches&&t.matches('textarea.mynote')){if(t.value.trim())NOTES[t.dataset.note]=t.value;else delete NOTES[t.dataset.note];lsSet(NKEY,NOTES)}});
// copy buttons
function addCopy(root){root.querySelectorAll('pre:not([data-cp])').forEach(p=>{p.dataset.cp='1';if(p.closest('#srch,.cheat,.widget,.vis')||p.textContent.trim().length<8)return;p.insertAdjacentHTML('afterend','<button class="btn g copy" data-copypre="1" aria-label="Copy this code">Copy</button>')})}
new MutationObserver(ms=>ms.forEach(m=>m.addedNodes.forEach(n=>{if(n.nodeType===1){if(n.matches('pre:not([data-cp])')){n.parentNode&&addCopy(n.parentNode)}else addCopy(n)}}))).observe(document.body,{childList:true,subtree:true});
addCopy(document);
{const pr=document.getElementById('prun');if(pr)pr.insertAdjacentHTML('afterend','<button class="btn g" data-copyof="pcode">Copy code</button>')}
// cheat sheet
function cheatPane(){return '<div role="tabpanel" data-pane="cheat" hidden><h2>🖨 Cheat sheet</h2><p class="note">Every concept of this chapter on one printable page: its definition and, where it has one, an example that was run. Choose Print, then Save as PDF to keep it.</p><div class="row"><button class="btn" id="cheatprint">Print or save as PDF</button></div><div class="cheat">'+D.nodes.filter(n=>n.level===1).map(t=>'<h3>'+esc(t.label)+'</h3>'+D.nodes.filter(n=>n.level>=2&&topOf(n.id)===t.id).map(n=>'<div class="cs"><b>'+esc(n.label)+'</b> '+esc(n.definition||n.body||'')+(n.io?'<pre data-cp="1">'+esc(n.io.code)+'\n# → '+esc(n.io.out)+'</pre>':(n.example?' <code>'+esc(n.example)+'</code>':''))+'</div>').join('')).join('')+'</div></div>'}
// marks on answers
function fbHtml(){return '<div class="fb" role="group" aria-label="Was this answer helpful?"><span class="note">Was this helpful?</span> <button class="jump" data-fb="up" aria-pressed="false">👍 Yes</button><button class="jump" data-fb="down" aria-pressed="false">👎 No</button><button class="jump" data-fb="err" aria-pressed="false">⚑ Report an error</button></div>'}
function fbRecord(btn){const msg=btn.closest('.msg'),prev=msg.previousElementSibling,q=prev&&prev.classList.contains('me')?prev.textContent:'',aid=(msg.parentElement.id||'').replace(/-log$/,''),ag=D.agents.find(a=>a.id===aid),v=btn.dataset.fb;
 const c=msg.cloneNode(true);c.querySelectorAll('.fb,.srcs,details,button').forEach(x=>x.remove());const a=c.textContent.trim().slice(0,600);
 FBK=FBK.filter(x=>!(x.q===q&&x.agent===(ag?ag.name:'Guide')));FBK.push({at:new Date().toISOString(),agent:ag?ag.name:'Guide',q,a,v});try{localStorage.setItem(FBKEY,JSON.stringify(FBK))}catch(e){}
 btn.parentElement.querySelectorAll('[data-fb]').forEach(b=>b.setAttribute('aria-pressed',b===btn?'true':'false'));toast('Saved in this browser. Copy your marks from Your data to send them to your instructor.')}
const FB_WORD={up:'helpful',down:'not helpful',err:'contains an error'};
function fbMarkdown(){return '# Marks on answers - '+D.title+'\n\n'+(FBK.length?FBK.map(x=>'- **'+x.agent+'** - '+FB_WORD[x.v]+' ('+x.at.slice(0,16).replace('T',' ')+' UTC)\n  - Question: '+x.q+'\n  - Answer: '+x.a.replace(/\n/g,' ')).join('\n'):'No marks.')+'\n'}
function notesMarkdown(){const ids=Object.keys(NOTES).filter(k=>byId[k]);return '# My notes - '+D.title+'\n\n'+(ids.length?ids.map(k=>'## '+byId[k].label+'\n\n'+NOTES[k]).join('\n\n'):'No notes.')+'\n'}
const _dmd=drawMyData;drawMyData=function(){_dmd();const el=document.getElementById('mydataout'),N=D.nodes.length,d=D.nodes.filter(x=>PROG.done[x.id]).length,v=D.nodes.filter(x=>PROG.visited[x.id]).length,ni=Object.keys(NOTES).filter(k=>byId[k]),rv=Object.keys(REV).filter(k=>byId[k]);
 el.insertAdjacentHTML('beforeend','<h3>Progress</h3><p>'+d+' of '+N+' sections marked as understood; '+v+' visited.</p><div class="cover" role="img" aria-label="'+d+' of '+N+' understood"><i style="width:'+Math.round(100*d/N)+'%"></i></div>'
  +'<h3>Notes</h3>'+(ni.length?'<ul>'+ni.map(k=>'<li><button class="jump" data-go="'+k+'">'+esc(byId[k].label)+'</button> '+esc(NOTES[k].slice(0,80))+'</li>').join('')+'</ul>':'<p class="note">No notes yet. Open a concept and write one in its details.</p>')
  +'<h3>Review queue</h3><p>'+(rv.length?rv.length+' concept'+(rv.length>1?'s':'')+' to review: '+rv.map(k=>esc(byId[k].label)).join(', ')+'.':'Nothing waiting. A question answered wrongly comes back after 10 minutes, then 1, 3 and 7 days.')+'</p>'
  +'<h3>Marks on answers</h3><p>'+FBK.length+' mark'+(FBK.length===1?'':'s')+' saved.</p><div class="row"><button class="btn g" id="dlnotes">⧉ Copy notes (Markdown)</button><button class="btn g" id="dlfb">⧉ Copy marks (Markdown)</button><button class="btn g" id="dlfbjs">⧉ Copy marks (JSON)</button><button class="btn g" id="clrprog">Reset progress, notes, review and marks</button></div>')};
// code exercises
const EX_KW=new Set(['range','len','int','str','float','not','and','or','in','is','elif','else','if','for','while','break','continue','return','True','False','None','print','sum','min','max','abs','round','sorted','def','import','from','as','pass','list','enumerate','zip']);
const exIsErr=t=>/Traceback|^\s*[A-Za-z_.]*(Error|Exception)\b[:\s(]|^[A-Za-z_.]*(Error|Exception)$/m.test(String(t));
function blankTokens(code){const re=/'[^'\n]*'|"[^"\n]*"|\d+(?:\.\d+)?|[A-Za-z_]\w*/g,T=[];let m;while((m=re.exec(code))){const t=m[0];if(/^[A-Za-z_]/.test(t)&&!EX_KW.has(t))continue;const ls=code.lastIndexOf('\n',m.index)+1;if(code.slice(ls,m.index).includes('#'))continue;T.push({t,at:m.index})}return T}
function exPools(){const P={order:[],blank:[],repair:[]},seen=new Set(),ok=c=>!/\binput\s*\(/.test(c);
 D.nodes.forEach(n=>{if(n.io&&n.io.code&&ok(n.io.code)&&exIsErr(n.io.out))P.repair.push({kind:'repair',concept:n.id,label:n.label,code:n.io.code,err:n.io.out});else if(n.io&&n.io.code&&ok(n.io.code)){const L=n.io.code.split('\n').filter(l=>l.trim());if(L.length>=3&&L.length<=9)P.order.push({kind:'order',concept:n.id,label:n.label,code:n.io.code,out:n.io.out});if(blankTokens(n.io.code).length)P.blank.push({kind:'blank',concept:n.id,label:n.label,code:n.io.code,out:n.io.out})}
  if(n.error&&n.error.code&&ok(n.error.code))P.repair.push({kind:'repair',concept:n.id,label:n.label,code:n.error.code,err:n.error.out})});
 BANK.forEach(b=>{if(b.code&&ok(b.code)&&byId[b.concept]&&/^[A-Za-z]*Error$/.test(String(b.options[b.answer]).trim())&&!P.repair.some(r=>r.code===b.code))P.repair.push({kind:'repair',concept:b.concept,label:byId[b.concept].label,code:b.code,err:b.options[b.answer]})});
 TRACE_EX.forEach(([l,c])=>{const L=c.split('\n').filter(x=>x.trim());if(L.length>=3&&L.length<=9&&ok(c)&&!seen.has(c)){seen.add(c);P.order.push({kind:'order',concept:'',label:l,code:c,out:null})}});return P}
function exercisesPane(){return '<div role="tabpanel" data-pane="exercises" hidden><h2>🧩 Code exercises</h2><p class="note">Exercises made from this chapter’s own examples, each checked by running your code: put the lines of a program in order, fill in the missing piece, or change a program so that it stops raising an error. A concept you get wrong goes to the review queue.</p><div class="row"><label class="note" for="cxkind">Kind</label><select id="cxkind" aria-label="Kind of exercise"><option value="any">any</option><option value="order">Put the lines in order</option><option value="blank">Fill in the blank</option><option value="repair">Make it run</option></select><button class="btn" id="cxnew">New exercise</button></div><div id="cxout" aria-live="polite"></div><p class="verdict" id="cxscore"></p></div>'}
let exN=0;const EXS={n:0,ok:0};
async function exPickToken(d){const T=qShuf(blankTokens(d.code));for(const k of T.slice(0,6)){const out=await runPy(d.code.slice(0,k.at)+'____'+d.code.slice(k.at+k.t.length));if(exIsErr(out))return k}return T[0]}
async function exShow(d){const id='ex'+(++exN),o=document.getElementById('cxout'),lab=d.concept?' <button class="jump" data-go="'+d.concept+'">'+esc(d.label)+'</button>':' <span class="note">'+esc(d.label)+'</span>';let h;
 if(d.kind==='order'){const L=d.code.split('\n').filter(l=>l.trim());let ix=L.map((_,i)=>i);for(let t=0;t<20&&ix.every((v,i)=>v===i);t++)ix=qShuf(ix);
  h='<fieldset class="ex" data-ex="order" data-id="'+id+'"><legend>Put the lines in order'+lab+'</legend><p class="note">Move a line with ▲ and ▼ until the program reads correctly. The spaces at the start of a line belong to it.</p><ol class="exlines" data-lines="'+esc(JSON.stringify(L))+'">'+ix.map(i=>'<li><button class="btn g" data-exmv="-1" aria-label="Move up">▲</button><button class="btn g" data-exmv="1" aria-label="Move down">▼</button><code data-l="'+i+'">'+esc(L[i])+'</code></li>').join('')+'</ol>'}
 else if(d.kind==='blank'){const k=await exPickToken(d);const shown=d.code.slice(0,k.at)+'____'+d.code.slice(k.at+k.t.length);
  h='<fieldset class="ex" data-ex="blank" data-id="'+id+'" data-at="'+k.at+'" data-tok="'+esc(k.t)+'"><legend>Fill in the blank'+lab+'</legend><p class="note">Replace <code>____</code> so that the program gives the result shown. Write it as Python would: text needs its quotes.</p><pre class="exsrc" data-cp="1">'+esc(shown)+'</pre><p>Expected result: <code>'+esc(d.out)+'</code></p><label class="note" for="'+id+'-in">Your answer</label> <input class="exin" id="'+id+'-in" autocomplete="off" spellcheck="false">'}
 else{h='<fieldset class="ex" data-ex="repair" data-id="'+id+'"><legend>Make it run'+lab+'</legend><p class="note">This program stops with an error. Change it so that it runs without one.</p><p>Python says: <code>'+esc(String(d.err).split('\n').slice(-1)[0])+'</code></p><textarea class="mycode" id="'+id+'-code" spellcheck="false" aria-label="Program to repair">'+esc(d.code)+'</textarea>'}
 h+='<p><button class="btn" data-excheck="1">Check</button> '+(d.kind==='repair'?'<button class="btn g" data-exhint="1">Hint</button>':'<button class="btn g" data-exshow="1">Show the answer</button>')+' <span class="verdict" aria-live="polite"></span></p></fieldset>';
 o.innerHTML=h;o.firstElementChild.exd=d;return o.firstElementChild}
async function exNew(){const P=exPools(),sel=document.getElementById('cxkind').value,kinds=(sel==='any'?['order','blank','repair']:[sel]).filter(k=>P[k].length);if(!kinds.length){document.getElementById('cxout').innerHTML='<p class="note">This chapter has no exercise of that kind.</p>';return null}
 const k=kinds[Math.floor(Math.random()*kinds.length)],pool=P[k];return await exShow(pool[Math.floor(Math.random()*pool.length)])}
async function exCheck(fs){const d=fs.exd,v=fs.querySelector('.verdict');let ok=false,msg='';v.textContent='Running...';
 try{if(d.kind==='order'){const L=JSON.parse(fs.querySelector('ol').dataset.lines),cur=[...fs.querySelectorAll('ol code')].map(c=>L[+c.dataset.l]),same=cur.map((x,i)=>x===L[i]).filter(Boolean).length;
   if(cur.join('\n')===L.join('\n')){ok=true;msg='Correct. '+(d.out!=null?'It prints '+d.out+'.':'')}
   else{const a=await runPy(cur.join('\n')),b=await runPy(L.join('\n'));if(!exIsErr(a)&&a===b){ok=true;msg='Accepted: a different order that gives the same result ('+a+').'}else msg='Not yet: '+same+' of '+L.length+' lines are where they belong.'}}
  else if(d.kind==='blank'){const t=fs.querySelector('input').value.trim(),at=+fs.dataset.at,tok=fs.dataset.tok;if(!t){msg='Not yet: write something in the blank first.'}else{const code=d.code.slice(0,at)+t+d.code.slice(at+tok.length),out=await runPy(code);if(!exIsErr(out)&&String(out).trim()===String(d.out).trim()){ok=true;msg='Correct. The program prints '+out+'.'}else msg='Not yet: with that, the program '+(exIsErr(out)?'raises an error ('+String(out).split('\n').slice(-1)[0].slice(0,80)+')':'prints '+String(out).slice(0,80)+' instead of '+d.out)+'.'}}
  else{const code=fs.querySelector('textarea').value,out=await runPy(code);if(!exIsErr(out)){ok=true;msg='Correct. It runs'+(String(out).trim()?' and prints '+String(out).trim().slice(0,80):'')+'.'}else msg='Not yet: it still raises '+String(out).split('\n').slice(-1)[0].slice(0,100)}}
 catch(e){msg='The check could not run ('+esc(e.message||'error')+').'}
 if(!fs.dataset.done){fs.dataset.done='1';EXS.n++;if(ok)EXS.ok++;if(d.concept)recordReview(d.concept,ok);document.getElementById('cxscore').textContent=EXS.ok+' of '+EXS.n+' exercises solved'}
 fs.classList.toggle('right',ok);fs.classList.toggle('wrong',!ok);v.textContent=msg;return ok}
document.addEventListener('click',async e=>{const t=e.target;if(!t.closest)return;
 const mv=t.closest('[data-exmv]');if(mv){e.stopImmediatePropagation();const li=mv.closest('li'),dir=+mv.dataset.exmv;if(dir<0&&li.previousElementSibling)li.parentNode.insertBefore(li,li.previousElementSibling);else if(dir>0&&li.nextElementSibling)li.parentNode.insertBefore(li.nextElementSibling,li);mv.focus();return}
 const ch=t.closest('[data-excheck]');if(ch){e.stopImmediatePropagation();exCheck(ch.closest('fieldset'));return}
 const sh=t.closest('[data-exshow]');if(sh){e.stopImmediatePropagation();const fs=sh.closest('fieldset'),d=fs.exd;if(d.kind==='order'){const ol=fs.querySelector('ol'),L=JSON.parse(ol.dataset.lines),items=[...ol.children];items.sort((a,b)=>+a.querySelector('code').dataset.l-+b.querySelector('code').dataset.l).forEach(li=>ol.appendChild(li))}else{fs.querySelector('input').value=fs.dataset.tok}return}
 const hi=t.closest('[data-exhint]');if(hi){e.stopImmediatePropagation();const fs=hi.closest('fieldset'),n=byId[fs.exd.concept];fs.querySelector('.verdict').textContent='Hint: '+(n?(n.definition||n.body):'read the error message: it names the kind of mistake and the line.');return}
 if(t.id==='cxnew'){e.stopImmediatePropagation();exNew();return}
 if(t.id==='qgreview'){e.stopImmediatePropagation();const ids=reviewDue(),o=document.getElementById('qgout');if(!ids.length){o.innerHTML='<p class="note">Nothing is due for review. A question you answer wrongly comes back after 10 minutes, then after 1, 3 and 7 days; answering it rightly moves it on.</p>';document.getElementById('qgscore').textContent='';return}
  const qs=ids.slice(0,10).map(id=>{for(const k of qShuf(qKindsFor(byId[id])).sort((a,b)=>(b==='authored')-(a==='authored'))){const q=qMake(id,k);if(q)return q}return null}).filter(Boolean);o.innerHTML=qs.map(qRender).join('');document.getElementById('qgscore').textContent='0 of '+qs.length+' answered correctly';qCover();return}
 const mk=t.closest('[data-mark]');if(mk){e.stopImmediatePropagation();progToggle(mk.dataset.mark);return}
 const lk=t.closest('[data-link]');if(lk){e.stopImmediatePropagation();copyOut('Link',location.href.split('#')[0]+'#c='+lk.dataset.link);return}
 const cp=t.closest('[data-copypre]');if(cp){e.stopImmediatePropagation();const p=cp.previousElementSibling;copyOut('Code',p?p.textContent:'');return}
 const co=t.closest('[data-copyof]');if(co){e.stopImmediatePropagation();const x=document.getElementById(co.dataset.copyof);copyOut('Code',x?x.value:'');return}
 const fb=t.closest('[data-fb]');if(fb){e.stopImmediatePropagation();fbRecord(fb);return}
 if(t.id==='cheatprint'){e.stopImmediatePropagation();window.print();return}
 if(t.id==='dlnotes'){e.stopImmediatePropagation();copyOut('Notes',notesMarkdown());return}
 if(t.id==='dlfb'){e.stopImmediatePropagation();copyOut('Marks',fbMarkdown());return}
 if(t.id==='dlfbjs'){e.stopImmediatePropagation();copyOut('Marks',JSON.stringify(FBK,null,1));return}
 if(t.id==='clrprog'){e.stopImmediatePropagation();if(t.dataset.sure!=='1'){t.dataset.sure='1';t.textContent='Click again to reset everything';return}PROG={visited:{},done:{}};NOTES={};REV={};FBK=[];[PKEY,NKEY,RVKEY,FBKEY].forEach(k=>{try{localStorage.removeItem(k)}catch(e){}});progPaint();reviewPaint();drawMyData();return}},true);
"""
rep("// ---------- one delegated handler for clicks, context menus and tooltips ----------", JS + "// ---------- one delegated handler for clicks, context menus and tooltips ----------")
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("ok", len(s))
