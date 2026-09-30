"""Makes course_page_template_v9_14_0.html from v9_13_0. Usage: template_patch_v9_14_0.py <in.html> <out.html>
9.14.0 (the owner's request of 2026-09-30 14:21): (1) ten question types beyond multiple choice, each checked by rule and each answered with a correction -
fill in the blank in a definition (typed), true or false with the right concept to name, matching, predict the output (typed), fill in the blank in code
(checked by running it), put the lines in order, make it run, write the code (checked by running it and by the construct it must use), short answer (checked
against the key ideas of the model answer); numbers in code questions are changed on the fly and the expected result is computed by running the changed code;
(2) mock exams - a midterm-style and a final-style exam built from a code, so the same code gives the same exam; timer, marking, per-question corrections,
per-subject result, weak concepts sent to the review queue, result copied out; (3) the live model: Qwen2.5-Coder-0.5B (kept by the RDODI experiments) is the
default where the device's memory allows, with the small SmolLM2 as the choice for weaker devices."""
import sys
s = open(sys.argv[1], encoding="utf-8").read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:90])
    s = s.replace(old, new)

rep("<!-- course_page_template version 9.13.0:", "<!-- course_page_template version 9.14.0: ten question types with corrections, mock midterm and final exams from a code, live model choice. Earlier: --><!-- course_page_template version 9.13.0:")

CSS = """/* 9.14.0: question types and mock exams */
fieldset.xq{border:1px solid var(--line);border-radius:10px;margin:.7rem 0;padding:.5rem .9rem}fieldset.xq.right{border-color:var(--ok)}fieldset.xq.wrong{border-color:var(--bad)}fieldset.xq.half{border-color:var(--yellow)}
fieldset.xq legend{font-weight:700}.xtag{font-weight:400;font-size:.85em;color:var(--mute)}
input.xin,select.xin{font:inherit;border:1px solid var(--line);border-radius:6px;padding:.2rem .4rem;background:var(--panel);color:var(--ink);max-width:100%}
textarea.xin{width:100%;font:inherit;font-family:ui-monospace,monospace;min-height:3.2rem;border:1px solid var(--line);border-radius:8px;padding:.4rem;background:var(--panel);color:var(--ink)}
.xmsg{margin:.4rem 0 .1rem;font-weight:600}.xfix{margin:.1rem 0 .3rem}.xrow{display:flex;flex-wrap:wrap;gap:.4rem;align-items:center;margin:.3rem 0}
.xpart{margin:1rem 0 .2rem;border-bottom:2px solid var(--line);font-size:1.05rem}
#xetimer{position:sticky;top:0;z-index:5;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:.3rem .6rem;margin:.4rem 0;font-weight:700}
.xrep{border:2px solid var(--line);border-radius:10px;padding:.5rem .9rem;margin:.6rem 0}.xrep table{border-collapse:collapse;width:100%}.xrep td,.xrep th{border-bottom:1px solid var(--line);padding:.2rem .4rem;text-align:left}
.xmatch{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:.3rem .6rem;align-items:center;margin:.3rem 0}
"""
rep("</style>", CSS + "</style>")

# a defect found while writing 9.14.0: a Python-style escape was left in a JavaScript string and showed as text (U0001F9E9) in the heading
rep("<h3>\\U0001F9E9 Build your own questions</h3>", "<h3>🧩 Build your own questions</h3>")

# choice of the live model: the coder model kept by the RDODI experiments where its memory fits 60% of the device's reported memory (RDODI's own rule), else the small one
rep("async function enableLLM(){", "function llmModelFor(f16,pref,gb){const fits=Math.round((gb||4)*1024*0.6)>=1100,coder=pref==='coder'||(pref!=='small'&&fits);return {coder,model:coder?(f16?'Qwen2.5-Coder-0.5B-Instruct-q4f16_1-MLC':'Qwen2.5-Coder-0.5B-Instruct-q4f32_1-MLC'):(f16?WEBLLM_MODEL_F16:WEBLLM_MODEL_F32)}}\nasync function enableLLM(){")
# the tables the two new panes are built from must exist before the panes are assembled
EARLY = r"""
const XT_LABEL={mcq:'Multiple choice',cloze:'Fill in the blank (words)',judge:'True or false, with correction',match:'Matching',predict:'Predict the output',blank:'Fill in the blank (code)',order:'Put the lines in order',repair:'Make it run',write:'Write the code',short:'Short answer'};
const XT_PTS={mcq:1,cloze:1,judge:2,match:2,predict:2,blank:2,order:2,repair:3,write:3,short:3};
const XT_PART={mcq:'A',cloze:'A',judge:'A',match:'A',predict:'B',blank:'B',order:'B',repair:'C',write:'C',short:'D'};
const XT_PARTS={A:'Part A - the concepts',B:'Part B - reading code',C:'Part C - writing code',D:'Part D - explaining in words'};
const XEXAM={M:{name:'Midterm-style',minutes:40,prefer:['Remember','Understand'],mix:[['mcq',4],['cloze',2],['judge',2],['match',1],['predict',2],['blank',1],['order',1],['short',1]]},
 F:{name:'Final-style',minutes:75,prefer:['Apply','Analyze'],mix:[['mcq',4],['judge',1],['match',1],['predict',3],['blank',2],['order',1],['repair',2],['write',2],['short',3]]}};
"""
rep("function qKindsFor(n){", EARLY + "function qKindsFor(n){")

# the 9.13.0 exercise 'make it run' accepted an empty program; it now needs a program and keeps most of it
rep("else{const code=fs.querySelector('textarea').value,out=await runPy(code);if(!exIsErr(out)){ok=true;", "else{const code=fs.querySelector('textarea').value,out=await runPy(code);if(!code.trim()){msg='Not yet: the program is empty.'}else if(!exIsErr(out)&&!xKeeps(d.code,code)){msg='Not yet: it runs, but most of the program is gone. Keep the program and fix the mistake in it.'}else if(!exIsErr(out)){ok=true;")
# panes and menu
rep("['exercises','🧩 Code exercises'],", "['exercises','🧩 Code exercises'],['qtypes','✍ Question types'],['exam','📝 Mock exam'],")
rep("P+=cheatPane();P+=exercisesPane();panes.innerHTML=P;", "P+=cheatPane();P+=exercisesPane();P+=qtypesPane();P+=examPane();panes.innerHTML=P;")

# live model: the kept RDODI engine where memory allows
rep("const model=adapter.features&&adapter.features.has('shader-f16')?WEBLLM_MODEL_F16:WEBLLM_MODEL_F32;",
    "let pref=null;try{pref=localStorage.getItem('course-page-llm')}catch(e){}const ch=llmModelFor(!!(adapter.features&&adapter.features.has('shader-f16')),pref,navigator.deviceMemory),model=ch.model;if(ch.coder)delete WEBLLM_GEN_CONFIG.repetition_penalty;")
rep('<button class="btn g" id="llmbtn" title="Downloads a small language model once and runs it in a background thread with WebGPU">Enable live LLM</button>',
    '<label class="note" for="llmpick">Model</label> <select id="llmpick" aria-label="Live model" title="Chosen before the live model is enabled"><option value="auto">Automatic</option><option value="coder">Qwen2.5 Coder 0.5B (better with code, about 1 GB)</option><option value="small">SmolLM2 360M (smaller, faster)</option></select> <button class="btn g" id="llmbtn" title="Downloads a small language model once and runs it in a background thread with WebGPU">Enable live LLM</button>')
rep("'WebLLM 0.2.85 with SmolLM2-360M (16- or 32-bit by GPU), in its own thread'", "'WebLLM 0.2.85 with Qwen2.5-Coder-0.5B, or SmolLM2-360M on weaker devices (16- or 32-bit by GPU), in its own thread'")

JS = r"""
// ---------- 9.14.0: question types with corrections, and mock exams ----------
const XQ_STOP=new Set('the a an and or of to in on is are was were be been it its this that these those for with as by at from into than then so not no can will may which what when where how why does do did has have had if you your one two each any all also only such more most other use used using they them their there here about over under after before'.split(' '));
const xnorm=s=>String(s).toLowerCase().replace(/[^a-z0-9_ ]+/g,' ').replace(/\s+/g,' ').trim();
const xstem=w=>{w=String(w).toLowerCase();return w.length>4?w.replace(/(ing|ed|es|s|ly|al)$/,''):w};
const xwords=s=>xnorm(s).split(' ').filter(Boolean);
function xdist(a,b){const m=a.length,n=b.length,d=[];for(let i=0;i<=m;i++){d[i]=[i];}for(let j=1;j<=n;j++)d[0][j]=j;for(let i=1;i<=m;i++)for(let j=1;j<=n;j++)d[i][j]=Math.min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+(a[i-1]===b[j-1]?0:1));return d[m][n]}
function xrng(seed){let a=seed>>>0;return()=>{a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296}}
const xsh=(a,R)=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(R()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
const xpick=(a,R)=>a[Math.floor(R()*a.length)];
const xclean=t=>String(t||'').replace(/\s*\([^()]*\d{4}[a-z]?[^()]*\)/g,'').replace(/\s+/g,' ').trim();
const xdef=n=>xclean(n.definition||qFirst(n));
const xlab=id=>byId[id]?byId[id].label:'';
const ERR_HELP={SyntaxError:'Python could not read a line: look for a missing colon, bracket or quote.',IndentationError:'The spaces at the start of a line do not fit the block they belong to.',NameError:'A name is used that does not exist yet: check the spelling and the order of the lines.',TypeError:'An operation got a value of the wrong kind, for example text where a number is needed.',ValueError:'The value has the right kind but a wrong content, for example int() of text that is not a number.',IndexError:'The position is past the end of the sequence; positions start at 0.',KeyError:'The key is not in the dictionary.',ZeroDivisionError:'Something was divided by zero.',AttributeError:'That kind of value has no such method or attribute.',FileNotFoundError:'The file does not exist at that path.'};
let XIDF=null;function xidf(){if(XIDF)return XIDF;const df={},N=D.nodes.length;D.nodes.forEach(n=>{new Set(xwords((n.label||'')+' '+(n.definition||'')+' '+(n.body||'')).map(xstem)).forEach(w=>{df[w]=(df[w]||0)+1})});XIDF=w=>Math.log((N+1)/((df[w]||0)+1));return XIDF}
const xnoin=c=>!/\binput\s*\(/.test(c);
const xoneline=(t,k)=>String(t).split('\n').slice(-1)[0].slice(0,k||100);
const xtopic=n=>{let t=n;while(t&&t.parent&&byId[t.parent])t=byId[t.parent];return t||n};

// change up to two whole numbers in a program, and run the changed program to get its result
async function xVary(code,R,orig){const lits=[...code.matchAll(/(?<![\w.'"])\d+(?![\w.'"])/g)].filter(m=>{const ls=code.lastIndexOf('\n',m.index)+1,pre=code.slice(ls,m.index);return !pre.includes('#')&&(pre.match(/'/g)||[]).length%2===0&&(pre.match(/"/g)||[]).length%2===0&&+m[0]<=50});
 if(lits.length)for(let a=0;a<3;a++){const chosen=xsh(lits,R).slice(0,Math.min(2,lits.length)).sort((p,q)=>q.index-p.index);let c=code;chosen.forEach(m=>{const v=+m[0],d=xpick(v===0?[1,2,3]:[-2,-1,1,2,3],R);c=c.slice(0,m.index)+String(Math.max(0,v+d))+c.slice(m.index+m[0].length)});
  if(c===code)continue;let out;try{out=await runPy(c)}catch(e){continue}out=String(out).trim();if(!exIsErr(out)&&out&&out!=='(no output)'&&out.length<=80&&out.split('\n').length<=4&&out!==String(orig).trim())return {code:c,out,varied:true}}
 return {code,out:String(orig).trim(),varied:false}}

// ---- makers: each takes a concept and returns a question, or null when the concept cannot carry that type ----
function xCloze(n,R){const s=xdef(n),wc=s.split(/\s+/).length;if(!s||wc<7||wc>45)return null;
 const lw=new Set(xwords(n.label).filter(w=>w.length>=4).map(xstem)),toks=[...s.matchAll(/[A-Za-z][A-Za-z_]{3,}/g)].map(m=>m[0]).filter(w=>!XQ_STOP.has(w.toLowerCase()));
 let cand=toks.filter(w=>lw.has(xstem(w)));
 if(!cand.length){const all=new Set();D.nodes.forEach(x=>xwords(x.label).forEach(w=>all.add(xstem(w))));cand=toks.filter(w=>w.length>=5&&all.has(xstem(w)))}
 if(!cand.length){const idf=xidf();cand=toks.filter(w=>w.length>=6).sort((a,b)=>idf(xstem(b))-idf(xstem(a))).slice(0,3)}
 if(!cand.length)return null;const w=xpick(cand,R),re=new RegExp('\\b'+w+'\\b','gi');
 return {type:'cloze',concept:n.id,level:'Remember',text:s.replace(re,'………'),answer:w,sentence:s,topic:xlab(n.parent)||D.title}}
function xJudge(n,R){const s=xdef(n);if(!s||s.split(' ').length<6)return null;
 const sib=D.nodes.filter(x=>x.id!==n.id&&x.level===n.level&&xdef(x)&&xdef(x)!==s&&xdef(x).split(' ').length>=6);if(sib.length<3)return null;
 const truth=R()<.5,near=sib.filter(x=>x.parent===n.parent),owner=truth?n:xpick(near.length?near:sib,R),others=xsh(sib.filter(x=>x.id!==owner.id&&x.id!==n.id),R).slice(0,truth?3:2);
 const opts=xsh(truth?[n].concat(others):[owner,n].concat(others),R);
 return {type:'judge',concept:n.id,level:'Understand',claim:n.label,text:qMask(owner),truth,owner:owner.id,options:opts.map(x=>x.id),sentence:xdef(owner)}}
function xMatch(n,R){const ok=x=>xdef(x)&&xdef(x).split(' ').length>=5;let g=D.nodes.filter(x=>x.id!==n.id&&x.parent===n.parent&&x.level===n.level&&ok(x));if(g.length<3)g=D.nodes.filter(x=>x.id!==n.id&&x.level===n.level&&ok(x));if(g.length<3||!ok(n))return null;
 const items=[n].concat(xsh(g,R).slice(0,3));return {type:'match',concept:n.id,level:'Understand',rows:xsh(items,R).map(x=>({id:x.id,def:qMask(x)})),labels:xsh(items.map(x=>x.id),R)}}
async function xPredict(n,R){if(!n.io||!n.io.code||!xnoin(n.io.code)||exIsErr(n.io.out)||String(n.io.out).length>80)return null;const v=await xVary(n.io.code,R,n.io.out);
 return {type:'predict',concept:n.id,level:'Apply',code:v.code,expected:v.out,orig:String(n.io.out).trim(),varied:v.varied}}
async function xBlank(n,R){if(!n.io||!n.io.code||!xnoin(n.io.code)||exIsErr(n.io.out)||!blankTokens(n.io.code).length)return null;const v=await xVary(n.io.code,R,n.io.out),k=await exPickToken({code:v.code});if(!k)return null;
 return {type:'blank',concept:n.id,level:'Apply',code:v.code,expected:v.out,at:k.at,tok:k.t,shown:v.code.slice(0,k.at)+'____'+v.code.slice(k.at+k.t.length),varied:v.varied}}
function xOrder(n,R){if(!n.io||!n.io.code||!xnoin(n.io.code)||exIsErr(n.io.out))return null;const L=n.io.code.split('\n').filter(l=>l.trim());if(L.length<3||L.length>9)return null;let ix=L.map((_,i)=>i);for(let t=0;t<20&&ix.every((v,i)=>v===i);t++)ix=xsh(ix,R);
 return {type:'order',concept:n.id,level:'Apply',lines:L,shuffled:ix,expected:n.io.out}}
function xRepair(n,R){const c=[];if(n.io&&n.io.code&&xnoin(n.io.code)&&exIsErr(n.io.out))c.push({code:n.io.code,err:n.io.out});if(n.error&&n.error.code&&xnoin(n.error.code))c.push({code:n.error.code,err:n.error.out});
 BANK.forEach(b=>{if(b.concept===n.id&&b.code&&xnoin(b.code)&&/^[A-Za-z]*Error$/.test(String(b.options[b.answer]).trim()))c.push({code:b.code,err:b.options[b.answer]})});
 if(!c.length)return null;const p=xpick(c,R);return {type:'repair',concept:n.id,level:'Analyze',code:p.code,err:p.err}}
const XCORE=/\b(for|while|def|if|elif|else|return|range|len|sum|min|max|sorted|abs|round|int|str|float|list|dict|set|tuple|enumerate|zip|lambda|try|except|class|with|append|join|split|upper|lower|replace|strip|format|import)\b/g;
async function xWrite(n,R){if(!n.io||!n.io.code||!xnoin(n.io.code)||exIsErr(n.io.out))return null;const found=[...new Set(n.io.code.match(XCORE)||[])];if(!found.length)return null;
 const txt=(n.label+' '+(n.definition||'')+' '+(n.body||'')).toLowerCase(),core=found.filter(w=>new RegExp('\\b'+w+'\\b').test(txt)).slice(0,2);if(!core.length)core.push(found[0]);
 const v=await xVary(n.io.code,R,n.io.out);return {type:'write',concept:n.id,level:'Apply',expected:v.out,core,reference:v.code,varied:v.varied}}
function xShort(n,R,mode){let prompt,model,why;
 if(mode==='explain'){const bs=BANK.filter(b=>b.concept===n.id&&String(b.why||'').split(' ').length>=9);if(!bs.length)return null;const b=xpick(bs,R);prompt='Explain in your own words why “'+b.options[b.answer]+'” is the answer to this question: '+b.q;model=xclean(b.why);why=b}
 else{model=xdef(n);if(model.split(' ').length<7)return null;prompt='In your own words, what is “'+n.label+'”? Answer in one or two sentences.'}
 const idf=xidf(),lw=new Set(xwords(n.label).map(xstem)),seen=new Set(),keys=[];
 xwords(model).filter(w=>w.length>=4&&!XQ_STOP.has(w)).forEach(w=>{const st=xstem(w);if(!seen.has(st)&&!(mode!=='explain'&&lw.has(st))){seen.add(st);keys.push({w,st,x:idf(st)})}});
 keys.sort((a,b)=>b.x-a.x);const top=keys.slice(0,5);if(top.length<3)return null;
 return {type:'short',concept:n.id,level:mode==='explain'&&why&&why.level?why.level:'Understand',prompt,code:why&&why.code?why.code:'',model,keys:top}}
function xMcq(b,R){const idx=xsh(b.options.map((_,i)=>i),R);return {type:'mcq',pts:XT_PTS.mcq,concept:b.concept,level:b.level||'Understand',q:b.q,code:b.code||'',options:idx.map(i=>b.options[i]),answer:idx.indexOf(b.answer),why:b.why}}

// choose a concept that can carry the type, going through the candidate list
async function xMake(type,ctx){const R=ctx.R,used=ctx.used||new Set(),cids=ctx.cids;
 if(type==='mcq'){const set=new Set(cids);let bs=BANK.filter(b=>set.has(b.concept)&&!used.has('mcq:'+b.q));const pf=ctx.prefer||[];bs=xsh(bs,R).sort((a,b)=>(pf.includes(b.level)?1:0)-(pf.includes(a.level)?1:0));if(!bs.length)return null;used.add('mcq:'+bs[0].q);return xMcq(bs[0],R)}
 for(const cid of cids){const n=byId[cid];if(!n||used.has(type+':'+cid))continue;let it=null;
  try{it=type==='cloze'?xCloze(n,R):type==='judge'?xJudge(n,R):type==='match'?xMatch(n,R):type==='predict'?await xPredict(n,R):type==='blank'?await xBlank(n,R):type==='order'?xOrder(n,R):type==='repair'?xRepair(n,R):type==='write'?await xWrite(n,R):type==='short'?(xShort(n,R,R()<.5?'explain':'define')||xShort(n,R,'define')):null}catch(e){it=null}
  if(it){used.add(type+':'+cid);it.pts=XT_PTS[type];return it}}
 if(type==='order'){const pool=TRACE_EX.filter(([l,c])=>{const L=c.split('\n').filter(x=>x.trim());return L.length>=3&&L.length<=9&&xnoin(c)&&!used.has('order:t:'+l)});
  if(pool.length){const [l,c]=xpick(pool,R),out=String(await runPy(c)).trim();if(!exIsErr(out)){used.add('order:t:'+l);const L=c.split('\n').filter(x=>x.trim());let ix=L.map((_,i)=>i);for(let t=0;t<20&&ix.every((v,i)=>v===i);t++)ix=xsh(ix,R);return {type:'order',concept:'',level:'Apply',lines:L,shuffled:ix,expected:out,pts:XT_PTS.order,label:l}}}}
 return null}

// ---- drawing a question ----
function xIn(id,label,rows){return rows?'<textarea class="xin" id="'+id+'" rows="'+rows+'" aria-label="'+esc(label)+'" spellcheck="false"></textarea>':'<input class="xin" id="'+id+'" aria-label="'+esc(label)+'" autocomplete="off" spellcheck="false">'}
function xBody(it,id){let h='';const jump=it.concept?' <button class="jump" data-go="'+esc(it.concept)+'" aria-label="Open the concept">'+esc(xlab(it.concept))+'</button>':'';
 if(it.type==='mcq')h='<p>'+esc(it.q)+'</p>'+(it.code?'<pre>'+esc(it.code)+'</pre>':'')+it.options.map((o,j)=>'<label style="display:block"><input type="radio" name="'+id+'" value="'+j+'"> '+esc(o)+'</label>').join('');
 else if(it.type==='cloze')h='<p class="note">Topic: '+esc(it.topic)+'. Write the missing word.</p><p>'+esc(it.text)+'</p>'+xIn(id+'-a','Missing word');
 else if(it.type==='judge')h='<p>Is this statement correct?</p><p class="qdef"><b>'+esc(it.claim)+'</b>: '+esc(it.text)+'</p><label style="display:block"><input type="radio" name="'+id+'" value="1"> True</label><label style="display:block"><input type="radio" name="'+id+'" value="0"> False</label><p class="note">If it is false, which concept does the description really belong to?</p><select class="xin" id="'+id+'-s" aria-label="The concept the description belongs to"><option value="">(choose if you said false)</option>'+it.options.map(o=>'<option value="'+esc(o)+'">'+esc(xlab(o))+'</option>').join('')+'</select>';
 else if(it.type==='match')h='<p class="note">Match each description with the concept it describes.</p>'+it.rows.map((r,i)=>'<div class="xmatch"><span>'+esc(r.def)+'</span><select class="xin" data-row="'+esc(r.id)+'" aria-label="Concept for description '+(i+1)+'"><option value="">(choose)</option>'+it.labels.map(l=>'<option value="'+esc(l)+'">'+esc(xlab(l))+'</option>').join('')+'</select></div>').join('');
 else if(it.type==='predict')h='<p>What does this print or give? Write it exactly as Python shows it.</p><pre>'+esc(it.code)+'</pre>'+xIn(id+'-a','Output of the program',Math.min(4,it.expected.split('\n').length+1));
 else if(it.type==='blank')h='<p>Replace <code>____</code> so that the program gives <code>'+esc(it.expected)+'</code>. Write it as Python would: text needs its quotes.</p><pre>'+esc(it.shown)+'</pre>'+xIn(id+'-a','The missing piece');
 else if(it.type==='order')h='<p class="note">Move a line with the arrows until the program reads correctly. The spaces at the start of a line belong to it.</p><ol class="exlines">'+it.shuffled.map(i=>'<li><button class="btn g" data-exmv="-1" aria-label="Move up">▲</button><button class="btn g" data-exmv="1" aria-label="Move down">▼</button><code data-l="'+i+'">'+esc(it.lines[i])+'</code></li>').join('')+'</ol>';
 else if(it.type==='repair')h='<p>This program stops with an error. Change it so that it runs without one.</p><p>Python says: <code>'+esc(xoneline(it.err))+'</code></p><textarea class="mycode" id="'+id+'-a" spellcheck="false" aria-label="Program to repair">'+esc(it.code)+'</textarea>';
 else if(it.type==='write')h='<p>Write Python that gives exactly <code>'+esc(it.expected)+'</code>. The program has to use <b>'+it.core.map(esc).join('</b> and <b>')+'</b>, and it must work the answer out rather than write it down.</p><textarea class="mycode" id="'+id+'-a" spellcheck="false" aria-label="Your program" placeholder="Your program"></textarea>';
 else if(it.type==='short')h='<p>'+esc(it.prompt)+'</p>'+(it.code?'<pre>'+esc(it.code)+'</pre>':'')+xIn(id+'-a','Your answer',4);
 return h+(it.type==='mcq'?'':'')+'<span class="xj">'+jump+'</span>'}
function xTag(it){return XT_LABEL[it.type]+' · '+it.pts+' point'+(it.pts>1?'s':'')+(it.level?' · '+it.level:'')}

// ---- reading and marking an answer ----
function xRead(it,fs){const q=s=>fs.querySelector(s);
 if(it.type==='mcq'){const c=q('input:checked');return c?+c.value:null}
 if(it.type==='judge'){const c=q('input:checked');return {v:c?c.value:null,s:q('select').value}}
 if(it.type==='match'){const o={};fs.querySelectorAll('select[data-row]').forEach(s=>{o[s.dataset.row]=s.value});return o}
 if(it.type==='order')return [...fs.querySelectorAll('ol code')].map(c=>it.lines[+c.dataset.l]);
 const e=q('textarea,input.xin');return e?e.value:''}
const xcode=t=>String(t).split('\n').filter(l=>l.trim()&&!l.trim().startsWith('#')).length,xKeeps=(orig,a)=>xcode(a)>=Math.floor(0.7*xcode(orig));
const xnl=t=>String(t).replace(/\r/g,'').split('\n').map(l=>l.replace(/\s+$/,'')).join('\n').trim();
const xlax=t=>String(t).replace(/['"\s]/g,'').toLowerCase();
const xdefline=id=>byId[id]?'“'+esc(byId[id].label)+'”: '+esc(xdef(byId[id])):'';
async function xMark(it,a){let score=0,msg='',fix='';
 if(it.type==='mcq'){if(a==null)return {score:0,msg:'No answer chosen.',fix:'The answer is: '+esc(it.options[it.answer])+'. '+esc(it.why||'')};
  if(a===it.answer){score=1;msg='Correct.';fix=esc(it.why||'')}else{msg='Not this one.';const other=D.nodes.find(x=>xnorm(x.label)===xnorm(it.options[a]));fix='The answer is: '+esc(it.options[it.answer])+'. '+esc(it.why||'')+(other?' What you chose, '+xdefline(other.id)+'.':'')}}
 else if(it.type==='cloze'){const t=xnorm(a),w=xnorm(it.answer);
  if(!t){msg='Nothing written.'}else if(t===w||xstem(t)===xstem(w)){score=1;msg='Correct.'}
  else{const lim=w.length>=8?2:w.length>=5?1:0;if(lim&&xdist(t,w)<=lim){score=.5;msg='Close: check the spelling.'}else{const o=D.nodes.find(x=>x.id!==it.concept&&xwords(x.label).map(xstem).includes(xstem(t)));msg='Not this word.'+(o?' “'+esc(a.trim())+'” is a term of this chapter, but it belongs to '+xdefline(o.id)+'.':'')}}
  fix='The missing word is “'+esc(it.answer)+'”: '+esc(it.sentence)}
 else if(it.type==='judge'){if(a.v==null){msg='No answer chosen.'}else if(it.truth){if(a.v==='1'){score=1;msg='Correct: the statement is true.'}else msg='The statement is true.'}
  else{if(a.v==='0'){score=.5;msg='Correct that it is false.';if(a.s===it.owner){score=1;msg+=' And you named the right concept.'}else msg+=' The concept it describes is another one.'}else msg='The statement is false.'}
  fix=it.truth?'This description does belong to “'+esc(it.claim)+'”.':'The description belongs to '+xdefline(it.owner)+'. It does not describe “'+esc(it.claim)+'”.'}
 else if(it.type==='match'){let k=0;const bad=[];it.rows.forEach(r=>{if(a[r.id]===r.id)k++;else bad.push(r)});score=k/it.rows.length;msg=k+' of '+it.rows.length+' matched correctly.';fix=bad.length?bad.map(r=>esc(r.def)+' → <b>'+esc(xlab(r.id))+'</b>').join('<br>'):'All four are right.'}
 else if(it.type==='predict'){const t=xnl(a);
  if(!t){msg='Nothing written.'}else if(t===xnl(it.expected)){score=1;msg='Correct.'}else if(xlax(t)===xlax(it.expected)){score=.5;msg='Nearly: the value is right, but not in the exact form Python shows (quotes, spaces or capitals).'}
  else if(it.varied&&t===xnl(it.orig)){msg='That is what the chapter’s own example prints. Here the numbers were changed, so the result changes too.'}else msg='Not this result.';
  fix='It gives <code>'+esc(it.expected)+'</code>. Python worked this out by running exactly this program.'}
 else if(it.type==='blank'){const t=String(a).trim();if(!t){msg='Nothing written.'}else{const out=String(await runPy(it.code.slice(0,it.at)+t+it.code.slice(it.at+it.tok.length))).trim();
   if(!exIsErr(out)&&out===it.expected){score=1;msg='Correct: the program prints '+esc(out)+'.'}else msg='Not yet: with that, the program '+(exIsErr(out)?'raises an error ('+esc(xoneline(out,80))+')':'prints '+esc(out.slice(0,80))+' instead of '+esc(it.expected))+'.'}
  fix='The missing piece is <code>'+esc(it.tok)+'</code>.'}
 else if(it.type==='order'){const same=a.map((x,i)=>x===it.lines[i]).filter(Boolean).length;
  if(a.join('\n')===it.lines.join('\n')){score=1;msg='Correct.'}else{const o1=String(await runPy(a.join('\n'))).trim(),o2=String(await runPy(it.lines.join('\n'))).trim();if(!exIsErr(o1)&&o1===o2){score=1;msg='Accepted: a different order that gives the same result.'}else{score=same/it.lines.length;msg=same+' of '+it.lines.length+' lines are where they belong.'}}
  fix='The order is:<pre>'+esc(it.lines.join('\n'))+'</pre>It prints <code>'+esc(it.expected)+'</code>.'}
 else if(it.type==='repair'){const out=String(await runPy(a)).trim();if(!String(a).trim()){msg='Nothing written.'}else if(!exIsErr(out)&&!xKeeps(it.code,a)){msg='It runs, but most of the program is gone. Keep the program and fix the mistake in it.'}else if(!exIsErr(out)){score=1;msg='Correct: it runs'+(out&&out!=='(no output)'?' and prints '+esc(out.slice(0,80)):'')+'.'}else if(String(a).trim())msg=(a.trim()===it.code.trim()?'Nothing was changed. ':'')+'It still raises <code>'+esc(xoneline(out))+'</code>.';
  const kind=(String(it.err).match(/[A-Za-z]*Error/)||[''])[0];fix=(ERR_HELP[kind]?esc(ERR_HELP[kind])+' ':'')+'Read the last line of the message: it names the kind of mistake, and the line above it points to where.'}
 else if(it.type==='write'){const out=String(await runPy(a)).trim();const lit=xlax(it.expected).length>=4&&xlax(a).includes(xlax(it.expected));
  const has=it.core.filter(w=>new RegExp('\\b'+w+'\\b').test(a)),miss=it.core.filter(w=>!has.includes(w));
  if(!String(a).trim()){msg='Nothing written.'}else if(exIsErr(out)){msg='It raises <code>'+esc(xoneline(out))+'</code>.'}else if(out!==it.expected){msg='It gives <code>'+esc(out.slice(0,80))+'</code>, not <code>'+esc(it.expected)+'</code>.'}
  else if(lit){msg='The result is right, but your code contains the answer itself. Work it out with the required construct.'}else if(miss.length){score=.5;msg='The result is right, but the program does not use '+miss.map(esc).join(' and ')+'.'}else{score=1;msg='Correct: it gives '+esc(out)+' and uses '+it.core.map(esc).join(' and ')+'.'}
  fix='One way to write it:<pre>'+esc(it.reference)+'</pre>'}
 else if(it.type==='short'){const ws=xwords(a);
  if(ws.length<5){msg='Too short to mark: write a full sentence.'}else{const st=new Set(ws.map(xstem)),hit=it.keys.filter(k=>st.has(k.st)),cov=hit.length/it.keys.length;score=cov>=.6?1:cov>=.34?.5:0;
   msg=(score===1?'Covers the key ideas.':score?'Covers part of it.':'Misses the key ideas.')+' Key ideas found: '+(hit.length?hit.map(k=>'✓ '+esc(k.w)).join(', '):'none')+(hit.length<it.keys.length?'; missing: '+it.keys.filter(k=>!hit.includes(k)).map(k=>'✗ '+esc(k.w)).join(', '):'')+'.'}
  fix='Model answer: '+esc(it.model)+' <span class="note">This is a match against the key words of the model answer, not a judgement of your reasoning: compare your answer with it.</span>'}
 return {score,msg,fix}}
function xKey(it){return it.type==='order'?it.lines:it.type==='mcq'?it.answer:it.type==='match'?Object.fromEntries(it.rows.map(x=>[x.id,x.id])):it.type==='judge'?{v:it.truth?'1':'0',s:it.owner}:it.type==='cloze'?it.answer:it.type==='predict'?it.expected:it.type==='blank'?it.tok:it.type==='write'?it.reference:it.type==='short'?it.model:''}
function xFeed(it,r){return '<p class="xmsg" role="status">'+(r.score===1?'✓ ':r.score>0?'◐ ':'✗ ')+r.msg+' <span class="note">('+(Math.round(r.score*it.pts*10)/10)+' of '+it.pts+')</span></p>'+(r.fix?'<p class="xfix"><b>'+(r.score===1?'Why':'Correction')+'.</b> '+r.fix+'</p>':'')}

// ---- one question at a time, marked at once ----
const XD={n:0,pts:0,got:0};let xN=0;
function qtypesPane(){const tops=D.nodes.filter(n=>n.level===1);return '<div role="tabpanel" data-pane="qtypes" hidden><h2>✍ Question types</h2><p class="note">One question at a time, in the form you choose, marked at once with a correction. Code questions change the numbers of the chapter’s own examples and are marked by running your code, so the same question rarely comes twice. A concept you get wrong goes to the review queue.</p><div class="row"><label class="note" for="xdtype">Type</label><select id="xdtype" aria-label="Type of question"><option value="any">any</option>'+Object.keys(XT_LABEL).map(k=>'<option value="'+k+'">'+esc(XT_LABEL[k])+'</option>').join('')+'</select><label class="note" for="xdscope">About</label><select id="xdscope" aria-label="Subject of the question"><option value="all">the whole chapter</option>'+tops.map(t=>'<option value="'+esc(t.id)+'">'+esc(t.label)+'</option>').join('')+'</select><button class="btn" id="xdnew">New question</button></div><div id="xdout" aria-live="polite"></div><p class="verdict" id="xdscore"></p></div>'}
function xCandidates(scope,R){const ids=scope&&scope!=='all'?[scope].concat(qUnder(scope)):D.nodes.map(n=>n.id);return xsh(ids,R)}
async function xDrill(){const R=xrng((Math.random()*4294967295)>>>0),sel=document.getElementById('xdtype').value,scope=document.getElementById('xdscope').value,o=document.getElementById('xdout');
 const types=sel==='any'?xsh(Object.keys(XT_LABEL),R):[sel];o.innerHTML='<p class="note">Making a question...</p>';let it=null;
 for(const t of types){it=await xMake(t,{R,cids:xCandidates(scope,R),used:new Set()});if(it)break}
 if(!it){o.innerHTML='<p class="note">This chapter has no question of that type'+(scope!=='all'?' in that subject':'')+'. Try another type or the whole chapter.</p>';return null}
 const id='xd'+(++xN);o.innerHTML='<fieldset class="xq" data-xid="'+id+'"><legend>'+esc(XT_LABEL[it.type])+' <span class="xtag">'+esc(xTag(it))+'</span></legend>'+xBody(it,id)+'<p class="xrow"><button class="btn" data-xcheck="1">Check</button><button class="btn g" data-xshow="1">Show the answer</button>'+(it.type==='short'?'<button class="btn g" data-xlive="1">Comment by the live model</button>':'')+'</p><div class="xfeed" aria-live="polite"></div></fieldset>';
 const fs=o.firstElementChild;fs.xit=it;return fs}
async function xDrillCheck(fs){const it=fs.xit,r=await xMark(it,xRead(it,fs));fs.querySelector('.xfeed').innerHTML=xFeed(it,r);fs.classList.toggle('right',r.score===1);fs.classList.toggle('wrong',r.score===0);fs.classList.toggle('half',r.score>0&&r.score<1);
 if(!fs.dataset.done){fs.dataset.done='1';XD.n++;XD.pts+=it.pts;XD.got+=r.score*it.pts;if(it.concept){QG.asked[it.concept]=(QG.asked[it.concept]||0)+1;if(r.score>=.5)QG.right[it.concept]=(QG.right[it.concept]||0)+1;qgSave();recordReview(it.concept,r.score>=.5)}
  document.getElementById('xdscore').textContent=XD.n+' question'+(XD.n>1?'s':'')+' answered, '+(Math.round(XD.got*10)/10)+' of '+XD.pts+' points'}
 return r}
async function xLiveComment(fs){const it=fs.xit,a=xRead(it,fs),o=fs.querySelector('.xfeed');if(!(KIT.llm||sampleNS)){o.innerHTML+='<p class="note">The live model is not enabled. Enable it in the Agents view (a browser with WebGPU is needed).</p>';return}
 o.insertAdjacentHTML('beforeend','<p class="note xlv">Asking the live model...</p>');
 try{const t=await qLiveAsk('You are marking a student answer for the course page "'+D.title+'". Use ONLY the MODEL ANSWER. In at most 45 words say what the student got right and what is missing or wrong. Do not add facts.\n\nQUESTION: '+it.prompt+'\nMODEL ANSWER: '+it.model+'\nSTUDENT ANSWER: '+a);
  o.querySelector('.xlv').outerHTML='<p class="xfix"><b>Comment by the live model</b> (it can be wrong; the key-idea check above is the rule): '+esc(String(t).trim().slice(0,500))+'</p>'}catch(e){const x=o.querySelector('.xlv');if(x)x.textContent='The live model failed: '+(e.message||'error')}}

// ---- mock exams ----
const XFALL=['mcq','cloze','judge','short'];
const XH_KEY='course-page-exams:'+D.title;let XHIST=[];try{XHIST=JSON.parse(localStorage.getItem(XH_KEY)||'[]')}catch(e){}
const XE={items:[],kind:'M',seed:0,deadline:0,timer:null,done:false};
function examPane(){return '<div role="tabpanel" data-pane="exam" hidden><h2>📝 Mock exam</h2><p class="note">A practice exam on this chapter, built on request from its own concepts, question bank and executed examples. Its code names the exam: the same code gives the same exam again. The point values and times are this page’s defaults for practice, not the official exam rules. Marking happens when you finish; the answers and corrections come after that.</p><div class="row"><label class="note" for="xekind">Exam</label><select id="xekind" aria-label="Kind of exam"><option value="M">Midterm-style: '+XEXAM.M.mix.reduce((a,x)=>a+x[1],0)+' questions, '+XEXAM.M.minutes+' minutes</option><option value="F">Final-style: '+XEXAM.F.mix.reduce((a,x)=>a+x[1],0)+' questions, '+XEXAM.F.minutes+' minutes</option></select><label class="note" for="xecode">Exam code</label><input class="xin" id="xecode" aria-label="Exam code (leave empty for a new exam)" placeholder="new exam" size="10" autocomplete="off"><label class="note"><input type="checkbox" id="xetimeron" checked> Timer</label><button class="btn" id="xestart">Start exam</button></div><div id="xeout" aria-live="polite"></div><div id="xehist"></div></div>'}
function xHistPaint(){const el=document.getElementById('xehist');if(!el)return;el.innerHTML=XHIST.length?'<h3>Your earlier attempts</h3><table><tr><th>Exam code</th><th>Result</th><th>When</th></tr>'+XHIST.slice(-8).reverse().map(h=>'<tr><td><code>'+esc(h.code)+'</code></td><td>'+h.pct+'% ('+h.got+' of '+h.pts+')</td><td>'+esc(new Date(h.at).toLocaleString())+'</td></tr>').join('')+'</table>':''}
async function xExamBuild(kind,seed){const spec=XEXAM[kind],R=xrng(seed*7919+(kind==='F'?17:3)),tops=D.nodes.filter(n=>n.level===1),topOrder=xsh(tops.length?tops:D.nodes,R),used=new Set(),items=[],plan=[];
 spec.mix.forEach(([t,c])=>{for(let i=0;i<c;i++)plan.push(t)});const out=document.getElementById('xeout');
 for(let i=0;i<plan.length;i++){out.innerHTML='<p class="note">Building question '+(i+1)+' of '+plan.length+'...</p>';let it=null;
  for(const t of [plan[i]].concat(XFALL)){for(let a=0;a<topOrder.length&&!it;a++){const top=topOrder[(i+a)%topOrder.length];it=await xMake(t,{R,cids:xsh([top.id].concat(qUnder(top.id)),R),used,prefer:spec.prefer})}if(it)break}
  if(it)items.push(it)}
 items.sort((a,b)=>XT_PART[a.type].localeCompare(XT_PART[b.type]));return items}
function xExamHtml(){let h='',part='';XE.items.forEach((it,i)=>{const p=XT_PART[it.type];if(p!==part){part=p;h+='<h3 class="xpart">'+esc(XT_PARTS[p])+'</h3>'}
  h+='<fieldset class="xq" data-xi="'+i+'"><legend>'+(i+1)+'. '+esc(XT_LABEL[it.type])+' <span class="xtag">'+it.pts+' point'+(it.pts>1?'s':'')+'</span></legend>'+xBody(it,'xe'+i)+'<div class="xfeed" aria-live="polite"></div></fieldset>'});return h}
async function xExamStart(){const kind=document.getElementById('xekind').value,raw=document.getElementById('xecode').value.trim(),m=raw.match(/^([MF])-(\d{1,9})$/i),out=document.getElementById('xeout');
 let k=kind,seed;if(m){k=m[1].toUpperCase();seed=+m[2];document.getElementById('xekind').value=k}else if(raw){out.innerHTML='<p class="note">An exam code looks like M-12345 (midterm) or F-12345 (final). Leave the box empty for a new exam.</p>';return}else seed=1+Math.floor(Math.random()*99999);
 clearInterval(XE.timer);XE.done=false;XE.kind=k;XE.seed=seed;XE.items=await xExamBuild(k,seed);
 if(!XE.items.length){out.innerHTML='<p class="note">This chapter has too little material to build an exam.</p>';return}
 const spec=XEXAM[k],pts=XE.items.reduce((a,x)=>a+x.pts,0),code=k+'-'+seed;document.getElementById('xecode').value=code;
 const timerOn=document.getElementById('xetimeron').checked;XE.deadline=timerOn?Date.now()+spec.minutes*60000:0;
 out.innerHTML='<div id="xetimer" role="timer">'+esc(spec.name)+' exam <code>'+code+'</code> · '+XE.items.length+' questions · '+pts+' points'+(timerOn?' · time left <span id="xeleft"></span>':' · no timer')+'</div><div id="xesum"></div>'+xExamHtml()+'<p class="xrow"><button class="btn" id="xefinish">Finish and mark</button></p>';
 if(timerOn){const tick=()=>{const left=Math.max(0,XE.deadline-Date.now()),el=document.getElementById('xeleft');if(el)el.textContent=Math.floor(left/60000)+':'+String(Math.floor(left/1000)%60).padStart(2,'0');if(!left&&!XE.done)xExamFinish(true)};tick();XE.timer=setInterval(tick,1000)}}
async function xExamFinish(timeUp){if(XE.done||!XE.items.length)return;XE.done=true;clearInterval(XE.timer);const fin=document.getElementById('xefinish');if(fin)fin.disabled=true;const sum=document.getElementById('xesum');const res=[];
 for(let i=0;i<XE.items.length;i++){if(sum)sum.innerHTML='<p class="note">Marking question '+(i+1)+' of '+XE.items.length+'...</p>';const it=XE.items[i],fs=document.querySelector('#xeout fieldset[data-xi="'+i+'"]');let r;try{r=await xMark(it,xRead(it,fs))}catch(e){r={score:0,msg:'The check could not run ('+esc(e.message||'error')+').',fix:''}}
  res.push(r);fs.querySelector('.xfeed').innerHTML=xFeed(it,r);fs.classList.toggle('right',r.score===1);fs.classList.toggle('wrong',r.score===0);fs.classList.toggle('half',r.score>0&&r.score<1);fs.querySelectorAll('input,select,textarea,button[data-exmv]').forEach(e=>{e.disabled=true});
  if(it.concept)recordReview(it.concept,r.score>=.5)}
 const pts=XE.items.reduce((a,x)=>a+x.pts,0),got=res.reduce((a,r,i)=>a+r.score*XE.items[i].pts,0),pct=Math.round(100*got/pts),by={};
 XE.items.forEach((it,i)=>{const t=xtopic(byId[it.concept]||{label:'General programs',id:''});const b=by[t.id]||(by[t.id]={label:t.label,got:0,pts:0});b.got+=res[i].score*it.pts;b.pts+=it.pts});
 const weak=[...new Set(XE.items.filter((it,i)=>res[i].score<.5&&it.concept).map(it=>it.concept))],code=XE.kind+'-'+XE.seed;
 XE.result={code,got:Math.round(got*10)/10,pts,pct,by,weak,md:'# '+XEXAM[XE.kind].name+' exam '+code+' - '+D.title+'\n\nScore: '+(Math.round(got*10)/10)+' of '+pts+' ('+pct+'%)\n\n'+Object.values(by).map(b=>'- '+b.label+': '+(Math.round(b.got*10)/10)+' of '+b.pts).join('\n')+(weak.length?'\n\nTo review: '+weak.map(xlab).join(', '):'')+'\n'};
 XHIST.push({code,pct,got:XE.result.got,pts,at:Date.now()});XHIST=XHIST.slice(-30);try{localStorage.setItem(XH_KEY,JSON.stringify(XHIST))}catch(e){}
 sum.innerHTML='<div class="xrep" id="xereport"><h3>Result'+(timeUp===true?' (time was up)':'')+'</h3><p><b>'+XE.result.got+' of '+pts+' points, '+pct+'%.</b> Exam <code>'+code+'</code>. Each question below shows what was right and the correction.</p><table><tr><th>Subject</th><th>Points</th></tr>'+Object.values(by).map(b=>'<tr><td>'+esc(b.label)+'</td><td>'+(Math.round(b.got*10)/10)+' of '+b.pts+'</td></tr>').join('')+'</table>'+(weak.length?'<p>To go over again (already in your review queue): '+weak.map(c=>'<button class="jump" data-go="'+esc(c)+'">'+esc(xlab(c))+'</button>').join(' ')+'</p>':'<p>No concept fell below half marks.</p>')+'<p class="xrow"><button class="btn g" id="xecopy">Copy the result</button><button class="btn g" id="xeprint">Print</button><button class="btn g" id="xeagain">Retake this exam</button><button class="btn g" id="xenew">A new exam</button></p></div>';
 xHistPaint();if(sum.scrollIntoView)sum.scrollIntoView({block:'start'})}
xHistPaint();
document.addEventListener('click',async e=>{const t=e.target;if(!t.closest)return;
 const c=t.closest('[data-xcheck]');if(c){e.stopImmediatePropagation();await xDrillCheck(c.closest('fieldset'));return}
 const sh=t.closest('[data-xshow]');if(sh){e.stopImmediatePropagation();const fs=sh.closest('fieldset'),it=fs.xit,r=await xMark(it,xKey(it));
  fs.querySelector('.xfeed').innerHTML='<p class="xfix"><b>Answer.</b> '+r.fix+'</p>';return}
 const lv=t.closest('[data-xlive]');if(lv){e.stopImmediatePropagation();xLiveComment(lv.closest('fieldset'));return}
 if(t.id==='xdnew'){e.stopImmediatePropagation();xDrill();return}
 if(t.id==='xestart'||t.id==='xenew'){e.stopImmediatePropagation();if(t.id==='xenew')document.getElementById('xecode').value='';xExamStart();return}
 if(t.id==='xeagain'){e.stopImmediatePropagation();xExamStart();return}
 if(t.id==='xefinish'){e.stopImmediatePropagation();xExamFinish(false);return}
 if(t.id==='xecopy'){e.stopImmediatePropagation();try{await navigator.clipboard.writeText(XE.result.md);t.textContent='Copied'}catch(x){t.textContent='Copy failed'}return}
 if(t.id==='xeprint'){e.stopImmediatePropagation();window.print();return}
},true);
document.addEventListener('change',e=>{if(e.target&&e.target.id==='llmpick'){try{localStorage.setItem('course-page-llm',e.target.value)}catch(x){}}});
try{const p=localStorage.getItem('course-page-llm'),el=document.getElementById('llmpick');if(el&&p)el.value=p}catch(e){}
"""
rep("// ---------- one delegated handler for clicks, context menus and tooltips ----------", JS + "// ---------- one delegated handler for clicks, context menus and tooltips ----------")
open(sys.argv[2], "w", encoding="utf-8").write(s)
