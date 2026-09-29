"""Makes course_page_template_v9_8_0.html from v9_7_0. Usage: template_patch_v9_8_0.py <in.html> <out.html>
9.8.0, from the owner's review of the chapter 5 page (2026-09-29): choosing an example in the Playground or the Code Lab fills the code
at once (no Load button); Step through needs no Trace button - the first Step, Back, First or Play traces the program, and a changed program
or input is traced again; the Step-through view and the Code pipeline each offer a list of examples (general programs plus the chapter's
own) and choosing one fills the code and runs it."""
import sys
s = open(sys.argv[1], encoding="utf-8").read()
def rep(old, new, count=1):
    global s
    assert s.count(old) >= 1, old[:80]
    s = s.replace(old, new, count)

# 1. no Load buttons: choosing fills
rep('<button class="btn g" id="pload">Load example</button>', '')
rep('<button class="btn g" id="clload">Load snippet</button>', '')
# 2. example lists
rep("const PSTAGES=", r"""const TRACE_EX=[['Sum with a for loop','total = 0\nfor n in range(1, 5):\n    total = total + n\nprint(total)'],['A function calling a function','def square(x):\n    return x * x\n\ndef sum_of_squares(a, b):\n    return square(a) + square(b)\n\nprint(sum_of_squares(3, 4))'],['A while loop that counts down',"n = 3\nwhile n > 0:\n    print(n)\n    n = n - 1\nprint('done')"],['A branch',"age = 15\nif age >= 18:\n    print('adult')\nelif age >= 13:\n    print('teen')\nelse:\n    print('child')"]];
Object.entries(D.visuals||{}).forEach(([k,v])=>{if(k[0]==='_'||!byId[k])return;const c=v.kind==='trace'&&v.code?(Array.isArray(v.code)?v.code.join('\n'):v.code):(v.kind==='debugger'&&v.lines?v.lines.join('\n'):null);if(c&&!TRACE_EX.some(e=>e[1]===c))TRACE_EX.push([byId[k].label+' (this chapter)',c])});
const PIPE_EX=[['Price with tax','price = 20\nprint(price + price * 0.18)'],['Arithmetic precedence','x = 2 + 3 * 6\nprint(x)'],['A function definition and call','def double(x):\n    return x * 2\nprint(double(21))'],['A comparison and a branch',"n = 7\nif n % 2 == 0:\n    print('even')\nelse:\n    print('odd')"],['A loop','for i in range(3):\n    print(i)']];
D.nodes.filter(n=>n.io).forEach(n=>{if(!PIPE_EX.some(e=>e[1]===n.io.code))PIPE_EX.push([n.label+' (this chapter)',n.io.code])});
const exOpts=l=>l.map((e,i)=>'<option value="'+i+'">'+esc(e[0])+'</option>').join('');
const PSTAGES=""")
# 3. step-through: example list, no Trace button
rep("""<textarea class="code" id="trcode" """, """<div class="row"><label class="note" for="trex">Example:</label><select id="trex" aria-label="Example program">'+exOpts(TRACE_EX)+'</select></div><textarea class="code" id="trcode" """)
rep('<button class="btn" id="trgo">Trace</button>', '')
rep("Run a program one line at a time. Python\\u2019s own line tracer", "Run a program one line at a time: press Step and Python\\u2019s own line tracer")
rep("TR.i=0;TR.src=src.split('\\n');", "TR.i=0;TR.src=src.split('\\n');TR.key=src+'\\u0001'+document.getElementById('trin').value;")
rep("function tracePlay(){", """async function traceEnsure(){const key=document.getElementById('trcode').value+'\\u0001'+document.getElementById('trin').value;if(TR&&TR.key===key)return false;await traceStart();return true}
async function traceStep(d){const fresh=await traceEnsure();if(!TR||fresh)return;TR.i=d===0?0:Math.max(0,Math.min(TR.steps.length-1,TR.i+d));traceShow()}
async function tracePlay(){if(!trTimer)await traceEnsure();tracePlay0()}
function tracePlay0(){""")
rep("if(!TR)return;document.getElementById('trplay').textContent", "if(!TR)return;if(TR.i>=TR.steps.length-1)TR.i=0;document.getElementById('trplay').textContent")
rep("if(t.id==='trnext'&&TR){TR.i=Math.min(TR.steps.length-1,TR.i+1);traceShow();return}if(t.id==='trprev'&&TR){TR.i=Math.max(0,TR.i-1);traceShow();return}if(t.id==='trfirst'&&TR){TR.i=0;traceShow();return}",
    "if(t.id==='trnext'){traceStep(1);return}if(t.id==='trprev'){traceStep(-1);return}if(t.id==='trfirst'){traceStep(0);return}")
# 4. pipeline: example list, runs on demand
rep("""<textarea class="code" id="ppcode" """, """<div class="row"><label class="note" for="ppex">Example:</label><select id="ppex" aria-label="Example code">'+exOpts(PIPE_EX)+'</select></div><textarea class="code" id="ppcode" """)
rep('<button class="btn" id="ppgo">Run the pipeline</button>', '<button class="btn" id="ppgo">Run again</button>')
rep("PIPE.stage=0;st.textContent=PIPE.error||'';pipeShow()", "PIPE.stage=0;PIPE.key=document.getElementById('ppcode').value;st.textContent=PIPE.error||'';pipeShow()")
rep("function pipeShow(){", """async function pipeEnsure(){if(PIPE&&PIPE.key===document.getElementById('ppcode').value)return false;await pipeRun();return true}
async function pipeNav(d){const fresh=await pipeEnsure();if(!PIPE||fresh)return;PIPE.stage=Math.max(0,Math.min(4,PIPE.stage+d));pipeShow()}
async function pipeStage(n){await pipeEnsure();if(!PIPE)return;PIPE.stage=n;pipeShow()}
function pipeShow(){""")
rep("if(t.id==='ppnext'&&PIPE){PIPE.stage=Math.min(4,PIPE.stage+1);pipeShow();return}if(t.id==='ppprev'&&PIPE){PIPE.stage=Math.max(0,PIPE.stage-1);pipeShow();return}", "if(t.id==='ppnext'){pipeNav(1);return}if(t.id==='ppprev'){pipeNav(-1);return}")
rep("if(stg&&PIPE){PIPE.stage=+stg.dataset.stage;pipeShow();return}", "if(stg){pipeStage(+stg.dataset.stage);return}")
# 5. choosing fills at once
rep("document.addEventListener('change',e=>{", """document.addEventListener('change',e=>{const id=e.target.id;
 if(id==='pex'){const v=e.target.value;document.getElementById('pcode').value=v==='first'?D.course.playground.code:byId[v].io.code;fitViews()}
 if(id==='clsnip'){document.getElementById('clcode').value=CODELAB_SNIPPETS[+e.target.value][1];fitViews()}
 if(id==='trex'){document.getElementById('trcode').value=TRACE_EX[+e.target.value][1];fitViews();TR=null;traceEnsure()}
 if(id==='ppex'){document.getElementById('ppcode').value=PIPE_EX[+e.target.value][1];fitViews();PIPE=null;pipeEnsure()}
 """)
open(sys.argv[2], "w", encoding="utf-8").write(s); print("written", sys.argv[2], len(s))
