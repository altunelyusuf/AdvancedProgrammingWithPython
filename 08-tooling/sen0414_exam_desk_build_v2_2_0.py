#!/usr/bin/env python3
"""Build the instructor's exam desk (one standalone HTML page) from the exam template, so that it marks with the SAME code as the exam page.
The marking functions are cut out of the template by name (nothing is retyped); a name that is not found stops the build.
2.2.0: also cuts xMarkMulti (the multiple-answer type of page 9.23.0).
usage: sen0414_exam_desk_build_v2_2_0.py TEMPLATE OUT.html"""
import sys, os, json, re
__version__ = "2.2.0"
here = os.path.dirname(os.path.abspath(__file__))
tpl = open(sys.argv[1], encoding="utf-8").read(); L = tpl.split("\n")
cfg = json.load(open(os.path.join(here, "course_page_config_v1_3_4.json"), encoding="utf-8"))["exam"]
def grab(pat):
    """the declaration whose first line matches pat, with its continuation lines (those that start with a space)"""
    idx = [i for i, l in enumerate(L) if re.match(pat, l)]
    assert len(idx) == 1, (pat, len(idx))
    i = idx[0]; j = i + 1
    while j < len(L) and L[j][:1] == " ": j += 1
    return "\n".join(L[i:j])
parts = []
for pat in [r"const exIsErr=", r"const xnorm=", r"const xstem=", r"const xwords=", r"function xdist\(", r"const xoneline=", r"const xcode=", r"const xnl=", r"const xlax=",
            r"const XP_PASS=", r"async function xMark\(", r"function xMarkMulti\(", r"async function xpMark\(", r"function blobWorker\(", r"function callWorker\(",
            r"function xCanon\(", r"function xSha256Js\(", r"async function xSha256\(", r"function xKey\(", r"const xIsAns=", r"function xAnsText\(", r"function xQText\("]:
    parts.append(grab(pat))
# the Python worker source is a template literal whose lines start at column 0
a = tpl.index("const PY_TIMEOUT_MS="); b = tpl.index("let pyWorker=null,pyVersion=null;")
parts.append(tpl[a:b])
stubs = """// stand-ins for what the marking code mentions only to word its feedback (the score never depends on them)
var LAB={};const D={nodes:[]},byId={},ERR_HELP={},xlab=id=>LAB[id]||id,xdef=()=>'',xdefline=()=>'',esc0=s=>String(s);
let pyWorker=null,pyVersion=null;
function newPyWorker(){pyWorker=blobWorker(PY_WORKER_SRC);pyWorker.addEventListener('message',e=>{if(e.data&&e.data.id==='boot')pyVersion=e.data.version})}
async function runPy(code,inputs){if(!pyWorker)newPyWorker();const w=pyWorker;let timer;
 const stop=new Promise(res=>{timer=setTimeout(()=>{w.terminate();if(pyWorker===w)pyWorker=null;res({out:'Stopped after '+PY_TIMEOUT_MS/1000+' s: the program was still running (an endless loop?).'})},PY_TIMEOUT_MS+(pyVersion?0:90000))});
 try{const r=await Promise.race([callWorker(w,{code:String(code),inputs:(inputs||[]).join('\\n')}),stop]);return r.out}finally{clearTimeout(timer)}}
"""
code = stubs + "\n".join(parts)
code = code.replace("esc(", "escM(")  # the marking feedback only needs a plain escape
code = "const escM=s=>String(s);\n" + code
h = open(os.path.join(here, "exam_desk_v2_2_0.tpl.html"), encoding="utf-8").read()
h = h.replace("/*__MARKING__*/", code).replace("__BONUS__", str(cfg["bonus_points"])).replace("__PUB__", json.dumps(cfg["public_key"], separators=(",", ":"))).replace("__PREFIX__", cfg["release_prefix"])
open(sys.argv[2], "w", encoding="utf-8").write(h)
print("wrote", sys.argv[2], len(h), "bytes;", len(parts), "pieces cut from", os.path.basename(sys.argv[1]))
