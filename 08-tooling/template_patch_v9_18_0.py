#!/usr/bin/env python3
"""Template 9.18.0 = 9.17.0 + the fixes that building chapters 7 to 24 showed the shared template needed (reported by the chapter workers, each reproduced before fixing):
1. an agent whose name matches no keyword gets a role icon from a fixed pool, never the robot (chapters had to rename their subjects to get an icon);
2. Pyodide loads the sqlite3 package (it is not in its base runtime: 40 of 68 widgets of the SQLite chapter failed);
3. the syntax and behaviour vocabulary of the ontology graph covers dictionaries, text, files, patterns, errors, imports, classes and returns, not only lists;
4. the graph's analysis script is inserted with a replacer function, so an example containing a dollar-quote sequence no longer empties the graph;
5. a chapter without a question bank still gets multiple-choice questions, made from its concepts' own definitions (chapters 21 and 23 had no questions and the question-type step timed out).
usage: template_patch_v9_18_0.py IN(9.17.0) OUT(9.18.0)"""
import sys, os
__version__ = "9.18.0"
here = os.path.dirname(os.path.abspath(__file__))
s = open(sys.argv[1], encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
# 1 icons
rep("function agentIcon(a){for(const [re,ic] of AGENT_ICONS)if(re.test(a.name))return ic;return '🤖'}",
    "const AGENT_POOL=['📘','🔎','🧪','🧰','🧮','📐','🗺️','🔧','🧬','📎','🎯','🪄','🧲','🔭','🧯','🪜'];\nfunction agentIcon(a){for(const [re,ic] of AGENT_ICONS)if(re.test(a.name))return ic;let h=0;for(const ch of String(a.name))h=(h*31+ch.charCodeAt(0))>>>0;return AGENT_POOL[h%AGENT_POOL.length]}")
# 2 sqlite3
rep("py=await loadPyodide({indexURL:'${PYODIDE_BASE}'});", "py=await loadPyodide({indexURL:'${PYODIDE_BASE}'});try{await py.loadPackage('sqlite3')}catch(e){}")
# 3 vocabulary and 4 replacer
a = s.index("const OG_CON={"); b = s.index("let OFACTS=null;")
s = s[:a] + open(os.path.join(here, "template_graph_v9_18_0.js"), encoding="utf-8").read() + s[b:]
rep("OG_PY.replace('__SNIPS__',JSON.stringify(JSON.stringify(sn)))", "OG_PY.replace('__SNIPS__',()=>JSON.stringify(JSON.stringify(sn)))")
assert "changes the list itself" in s
s = s.replace("changes the list itself", "changes the value itself").replace("shares one list under two names", "shares one value under two names")
# 5 multiple choice without a bank
rep("if(!bs.length)return null;used.add('mcq:'+b.q)" if False else "if(!bs.length)return null;used.add('mcq:'+bs[0].q);return xMcq(bs[0],R)}",
    "if(!bs.length){const auto=xAutoMcq(cids,used,R);if(!auto)return null;return xMcq(auto,R)}used.add('mcq:'+bs[0].q);return xMcq(bs[0],R)}")
rep("function xMcq(b,R){", """function xFirstSentence(t){t=String(t||'').replace(/\\s+/g,' ').trim();const m=t.match(/^.{20,}?[.!?](\\s|$)/);const x=(m?m[0].trim():t);return x.length>170?x.slice(0,167).replace(/\\s+\\S*$/,'')+'…':x}
function xAutoMcq(cids,used,R){const pool=D.nodes.filter(n=>n.level===3&&n.definition&&xFirstSentence(n.definition).length>25);const set=new Set(cids);const cand=xsh(pool.filter(n=>set.has(n.id)&&!used.has('mcq:auto:'+n.id)),R);if(!cand.length||pool.length<4)return null;const n=cand[0];used.add('mcq:auto:'+n.id);
 const right=xFirstSentence(n.definition),others=xsh(pool.filter(x=>x.id!==n.id&&xFirstSentence(x.definition)!==right),R).slice(0,3).map(x=>xFirstSentence(x.definition));if(others.length<3)return null;
 const opts=[right].concat(others);return {concept:n.id,level:'Remember',q:'Which statement describes “'+n.label+'”?',options:opts,answer:0,why:n.definition}}
function xMcq(b,R){""")
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("wrote", sys.argv[2], len(s))
