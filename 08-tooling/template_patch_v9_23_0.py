#!/usr/bin/env python3
"""Template patch 9.23.0 (over 9.22.0):
1. multiple choice no longer ends with "None of the above" (a last option of that kind is a hint in itself);
2. a new question type, "Multiple choice, several correct": five statements, the learner ticks every one that describes the concept; marking gives partial credit and takes a point off for a wrong tick;
3. the input row of the Playground and of Step through appears only when the program calls input(), with suggested values that fit the calls; otherwise a short note says no input is needed;
4. a concept's text is shown as paragraphs, each opening with what it answers (what it is, why it matters, where it is met, how it works, what to watch for), from the data's `paras`.
usage: template_patch_v9_23_0.py IN(9.22.0) OUT(9.23.0)"""
import sys, os
__version__ = "9.23.0"
here = os.path.dirname(os.path.abspath(__file__))
s = open(sys.argv[1], encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)
# 1 + 2: xMcq back to its plain form, the multi type next to it
a = s.index("const XNONE='None of the above';"); e = s.index("// choose a concept that can carry the type, going through the candidate list")
plain = """function xMcq(b,R){const idx=xsh(b.options.map((_,i)=>i),R);
 return {type:'mcq',pts:XT_PTS.mcq,concept:b.concept,level:b.level||'Understand',q:b.q,code:b.code||'',options:idx.map(i=>b.options[i]),answer:idx.indexOf(b.answer),why:b.why}}
"""
s = s[:a] + plain + open(os.path.join(here, "template_multi_v9_23_0.js"), encoding="utf-8").read() + "\n" + s[e:]
rep("const XT_LABEL={mcq:'Multiple choice',", "const XT_LABEL={mcq:'Multiple choice',multi:'Multiple choice, several correct',")
rep("const XT_PTS={mcq:1,", "const XT_PTS={mcq:1,multi:2,")
rep("const XT_PART={mcq:'A',", "const XT_PART={mcq:'A',multi:'A',")
rep("mix:[['mcq',6],['judge',2]", "mix:[['mcq',5],['multi',1],['judge',2]")
rep("mix:[['mcq',4],['judge',1]", "mix:[['mcq',3],['multi',1],['judge',1]")
rep("type==='judge'?xJudge(n,R):", "type==='judge'?xJudge(n,R):type==='multi'?xMulti(n,R):")
# drawing, reading, marking, key
rep("else if(it.type==='cloze')h='<p class=\"note\">Topic: ", "else if(it.type==='multi')h='<p>'+esc(it.q)+'</p>'+it.options.map((o,j)=>'<label style=\"display:block\"><input type=\"checkbox\" name=\"'+id+'\" value=\"'+j+'\"> '+esc(o)+'</label>').join('')+'<p class=\"note\">Tick every statement that fits. A wrong tick takes away one right one.</p>';\n  else if(it.type==='cloze')h='<p class=\"note\">Topic: ")
rep("if(it.type==='mcq'){const c=q('input:checked');return c?+c.value:null}", "if(it.type==='mcq'){const c=q('input:checked');return c?+c.value:null}  if(it.type==='multi'){return [...fs.querySelectorAll('input[type=checkbox]:checked')].map(c=>+c.value)}")
rep("async function xMark(it,a){let score=0,msg='',fix='';\n", "async function xMark(it,a){let score=0,msg='',fix='';\n if(it.type==='multi')return xMarkMulti(it,a);\n")
rep("it.type==='mcq'?it.answer:", "(it.type==='mcq'||it.type==='multi')?it.answer:")
rep("const xFp=x=>x.type+':'+(x.concept||'')+':'+(x.type==='mcq'?x.q:", "const xFp=x=>x.type+':'+(x.concept||'')+':'+(x.type==='multi'?x.options.filter((_,i)=>x.answer.includes(i)).sort().join('|'):x.type==='mcq'?x.q:")
rep("if(it.type==='mcq'){if(a!=null){const r=fs.querySelectorAll('input[type=radio]')[a];if(r)r.checked=true}}", "if(it.type==='mcq'){if(a!=null){const r=fs.querySelectorAll('input[type=radio]')[a];if(r)r.checked=true}}  else if(it.type==='multi'){(Array.isArray(a)?a:[]).forEach(j=>{const r=fs.querySelectorAll('input[type=checkbox]')[j];if(r)r.checked=true})}")
rep("const xIsAns=a=>a!=null&&a!==''&&!(a&&typeof a==='object'&&!Array.isArray(a)&&Object.values(a).every(v=>v==null||v===''));", "const xIsAns=a=>a!=null&&a!==''&&!(Array.isArray(a)&&!a.length)&&!(a&&typeof a==='object'&&!Array.isArray(a)&&Object.values(a).every(v=>v==null||v===''));")
rep("if(it.type==='mcq')return String.fromCharCode(65+a)+'. '+it.options[a];", "if(it.type==='mcq')return String.fromCharCode(65+a)+'. '+it.options[a];  if(it.type==='multi')return a.map(j=>String.fromCharCode(65+j)).join(', ')+': '+a.map(j=>it.options[j]).join(' | ');")
# 3 input rows
rep("""<div class="row"><label class="note" for="pin">Input lines for input():</label><input class="guess" id="pin" value="'+esc(D.course.playground.inputs)+'" aria-describedby="pinhelp"><span class="note" id="pinhelp">separate lines with |</span><button class="btn" id="prun">Run</button></div>""",
    """<div class="row"><span class="inbox" id="pinbox"><label class="note" for="pin">Input lines for input():</label><input class="guess" id="pin" value="'+esc(D.course.playground.inputs)+'" aria-describedby="pinhelp"><span class="note" id="pinhelp">separate lines with |</span></span><span class="note" id="pinnone" hidden>This program does not call input(), so it needs no typed input.</span><button class="btn" id="prun">Run</button></div>""")
rep("""<div class="row"><label class="note" for="trin">Input lines:</label><input class="guess" id="trin" value="" placeholder="separate lines with |"><span class="note" id="trstat" aria-live="polite"></span></div>""",
    """<div class="row"><span class="inbox" id="trinbox" hidden><label class="note" for="trin">Input lines:</label><input class="guess" id="trin" value="" placeholder="separate lines with |" aria-describedby="trinhelp"><span class="note" id="trinhelp"></span></span><span class="note" id="trinnone">No input needed: this program does not call input().</span><span class="note" id="trstat" aria-live="polite"></span></div>""")
rep("o.textContent=await runPy(document.getElementById('pcode').value,document.getElementById('pin').value.split('|'))", "inpSync('pcode','pin','pinbox','pinnone','pinhelp');o.textContent=await runPy(document.getElementById('pcode').value,document.getElementById('pin').value.split('|'))")
rep("const src=document.getElementById('trcode').value,inp=document.getElementById('trin').value.split('|').join('\\n');", "inpSync('trcode','trin','trinbox','trinnone','trinhelp');const src=document.getElementById('trcode').value,inp=document.getElementById('trin').value.split('|').join('\\n');")
rep("async function traceEnsure(){const key=", "async function traceEnsure(){inpSync('trcode','trin','trinbox','trinnone','trinhelp');const key=")
rep("</style>", ".inbox{display:contents}.bp{margin:.5rem 0;line-height:1.55}.bp .facet{color:var(--blue,#1a56a0)}</style>")
js = open(os.path.join(here, "template_inputs_v9_23_0.js"), encoding="utf-8").read()
marker = "// ---- save the code as a file, open a file into the code ----"
rep(marker, js + "\n" + marker)
# 4 paragraphs
rep("function sec(n,tag){", "function bodyHtml(n){const ps=n.paras&&n.paras.length?n.paras:[{facet:'',text:n.body}];return ps.map(p=>'<p class=\"bp\">'+(p.facet?'<b class=\"facet\">'+esc(p.facet)+'.</b> ':'')+linkify(p.text,n.id)+'</p>').join('')}\nfunction sec(n,tag){")
rep("</'+tag+'><p>'+linkify(n.body,n.id)+'</p>'+chartBox(n)", "</'+tag+'>'+bodyHtml(n)+chartBox(n)")
rep("<summary>'+linkify(firstSentence(m.body),m.id)+'</summary><p>'+linkify(m.body,m.id)+'</p></details>", "<summary>'+linkify(firstSentence(m.body),m.id)+'</summary>'+bodyHtml(m)+'</details>")
rep("body:sec.querySelector('p').textContent", "body:(sec.querySelectorAll('p.bp').length?[...sec.querySelectorAll('p.bp')].map(p=>p.textContent).join(' '):sec.querySelector('p').textContent)")
rep("c.label+': '+c.body).slice(0,700)", "c.label+': '+c.body).slice(0,1400)")
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("wrote", sys.argv[2], len(s))
