"""Makes course_page_template_v9_10_0.html from v9_9_0. Usage: template_patch_v9_10_0.py <in.html> <out.html>
9.10.0, from the owner's approval of 2026-09-29 (14:27 Istanbul) of two proposals: (1) an authored question bank - the question builder
draws on the chapter's own written items (kind 'From the question bank', one or more for every concept, __BANK__ filled by the build from
question_bank_v*.json when the chapter has one) and prefers them when it asks one question for every concept; (2) a live-model question:
the builder asks the page's language model (or the host's sample service) for one four-option question about a concept from the chapter's
own text, refuses one that is malformed, and, when the question carries code, runs the code on the page and refuses it unless the marked
answer is what the code prints. Without a model the button says so and nothing else changes."""
import sys
s = open(sys.argv[1], encoding="utf-8").read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:90])
    s = s.replace(old, new)
rep('<script type="application/json" id="quiz">__QUIZ__</script>', '<script type="application/json" id="quiz">__QUIZ__</script>\n<script type="application/json" id="qbank">__BANK__</script>')
rep("const QG_KINDS={predict:'Predict the output',", "const BANK=(()=>{try{return JSON.parse(document.getElementById('qbank').textContent)||[]}catch(e){return[]}})(),BSEEN=new Set();\nconst QG_KINDS={authored:'From the question bank',predict:'Predict the output',")
rep("function qKindsFor(n){const k=['name'];", "function qKindsFor(n){const k=['name'];if(BANK.some(b=>b.concept===n.id))k.push('authored');")
rep("let q={kind,concept:cid};", """let q={kind,concept:cid};
 if(kind==='authored'){const items=BANK.filter(b=>b.concept===cid);if(!items.length)return null;const fresh=items.filter(b=>!BSEEN.has(b));const b=qShuf(fresh.length?fresh:items)[0];BSEEN.add(b);const idx=qShuf(b.options.map((_,i)=>i));return {kind,concept:cid,q:b.q,code:b.code||'',options:idx.map(i=>b.options[i]),answer:idx.indexOf(b.answer),why:b.why,level:b.level}}""")
rep("<legend>'+esc(QG_KINDS[q.kind])+': '+esc(q.q)+'</legend>", "<legend>'+esc(QG_KINDS[q.kind]||'Written by the live model')+(q.level?' ('+esc(q.level)+')':'')+': '+esc(q.q)+'</legend>")
rep("+'<button class=\"btn\" data-gcheck=\"1\">Check</button>", "+(q.note?'<p class=\"note\">'+esc(q.note)+'</p>':'')+'<button class=\"btn\" data-gcheck=\"1\">Check</button>")
rep("""<button class="btn g" id="qgall">One question for every concept</button>""", """<button class="btn g" id="qgall">One question for every concept</button><button class="btn g" id="qglive">Ask the live model</button>""")
rep("Questions are made on request from this chapter\\u2019s own concepts, definitions, examples and taxonomy. A concept you have not been asked about yet comes first.", "Questions are made on request. Written items come from the chapter\\u2019s question bank; others are filled in from its concepts, definitions, examples and taxonomy; the live model, when this browser has one, writes a new one from the chapter text. A concept you have not been asked about yet comes first.")
# one for every concept: written item first
rep("for(const k of qShuf(qKindsFor(byId[id]))){const q=qMake(id,k)", "for(const k of qShuf(qKindsFor(byId[id])).sort((a,b)=>(b==='authored')-(a==='authored'))){const q=qMake(id,k)")
# live question
rep("let qgN=0;", r"""let qgN=0;
async function qLiveAsk(prompt){if(sampleNS){const r=await sampleNS(prompt,{cache:false});return r.text}
 const r=await KIT.llm.chat.completions.create({messages:[{role:'user',content:prompt}],...WEBLLM_GEN_CONFIG});return r.choices[0].message.content}
function qLiveParse(text){const m=String(text).match(/\{[\s\S]*\}/);if(!m)return null;let j;try{j=JSON.parse(m[0])}catch(e){return null}
 if(!j||typeof j.q!=='string'||!Array.isArray(j.options)||j.options.length!==4||!Number.isInteger(j.answer)||j.answer<0||j.answer>3)return null;
 const o=j.options.map(x=>String(x).trim());if(new Set(o).size!==4||o.some(x=>!x))return null;return {q:j.q.trim(),options:o,answer:j.answer,why:String(j.why||'').trim(),code:typeof j.code==='string'?j.code:''}}
async function qLive(scope){const ids=qScopeIds(scope),least=Math.min(...ids.map(i=>QG.asked[i]||0)),pick=qShuf(ids.filter(i=>(QG.asked[i]||0)===least))[0],n=byId[pick];
 const ctx=[n].concat(qKids(pick).slice(0,3)).map(x=>x.label+': '+(x.definition||x.body||'')+(x.io?' Example: '+x.io.code+' prints '+x.io.out:'')).join('\n');
 const prompt='Write ONE multiple-choice question for a second-year engineering student, using ONLY this CONTEXT from the chapter "'+D.title+'".\n\nCONTEXT:\n'+ctx+'\n\nReply with JSON only, no other text: {"q":"one line","code":"optional Python that prints one line","options":["a","b","c","d"],"answer":0,"why":"one sentence"}. Exactly four distinct options; "answer" is the index (0 to 3) of the right one; if you give code, the right option is exactly what the code prints.';
 let why='the model did not return a usable question';
 for(let k=0;k<2;k++){let t;try{t=await qLiveAsk(prompt)}catch(e){return {error:'The live model failed: '+e.message}}
  const j=qLiveParse(t);if(!j){why='the reply was not a well-formed question';continue}
  if(j.code){let out;try{out=await runPy(j.code)}catch(e){why='its code did not run';continue}if(String(out).trim()!==j.options[j.answer]){why='the marked answer was not what its code prints';continue}}
  return {kind:'live',concept:pick,q:j.q,code:j.code,options:j.options,answer:j.answer,why:j.why||'Written by the model from the chapter text.',note:'Written by the live model from the chapter text'+(j.code?'; its code was run and the marked answer is what it printed':'; not checked by running anything, so check it against the chapter')+'.'}}
 return {error:'No question this time: '+why+'.'}}""")
rep(" if(t.id==='qgclear'){", """ if(t.id==='qglive'){const o=document.getElementById('qgout');if(!sampleNS&&!KIT.llm){o.innerHTML='<p class="note">The live model is not available in this browser (it needs WebGPU; switch it on under Agents). The written and generated questions work without it.</p>';return}
  o.innerHTML='<p class="note">Asking the model\\u2026</p>';qLive(document.getElementById('qgscope').value).then(q=>{o.innerHTML=q.error?'<p class="note">'+esc(q.error)+'</p>':qRender(q);document.getElementById('qgscore').textContent='';qCover()});return}
 if(t.id==='qgclear'){""")
# a reloaded conversation lays its answers out as the live ones (the 'answer' class was only added when an answer was first made)
rep("turns.forEach(t=>bubble(log,t.role==='user'?'me':'agent',t.html))})}", "turns.forEach(t=>bubble(log,t.role==='user'?'me':'agent',t.html));log.querySelectorAll('.msg.agent').forEach(m=>{if(m.querySelector('.lead,.fmt,.pts'))m.classList.add('answer')})})}")
# a program that reads the keyboard cannot be stepped through here (nobody types), so a chapter's own input() program is not offered in Step through
rep("if(c&&!TRACE_EX.some(e=>e[1]===c))", "if(c&&!/\\binput\\s*\\(/.test(c)&&!TRACE_EX.some(e=>e[1]===c))")
# stderr joins stdout in the page's Python (logging's default handler and warnings write there), as in a terminal
B = chr(92) * 2 + "n"   # the two characters backslash-backslash-n as they stand in the page's source
rep("old = sys.stdout; sys.stdout = _o" + B + "    try:", "old = sys.stdout; olde = sys.stderr; sys.stdout = _o; sys.stderr = _o" + B + "    try:")
rep("finally:" + B + "        sys.stdout = old" + B + "    return", "finally:" + B + "        sys.stdout = old; sys.stderr = olde" + B + "    return")
# every run starts with a clean logging set-up, as a new process would (Pyodide's root logger may already hold a handler, which makes basicConfig do nothing)
rep("def _run(src, inp):" + B + "    _o = io.StringIO();", "def _run(src, inp):" + B + "    import logging; [logging.root.removeHandler(_h) for _h in logging.root.handlers[:]]; logging.root.setLevel(logging.WARNING); logging.disable(logging.NOTSET)" + B + "    _o = io.StringIO();")
N = chr(10)
rep("_old = sys.stdout; sys.stdout = _o" + N + "try:", "_old = sys.stdout; _olde = sys.stderr; sys.stdout = _o; sys.stderr = _o" + N + "try:")
rep("finally:" + N + "    sys.stdout = _old" + N + "window._pyout", "finally:" + N + "    sys.stdout = _old; sys.stderr = _olde" + N + "window._pyout")
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("written", sys.argv[2], len(s))
