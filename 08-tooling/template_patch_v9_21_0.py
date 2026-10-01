#!/usr/bin/env python3
"""Template patch 9.21.0 (over 9.20.0): exam questions that do not ask for memorised wording.
1. the "......" masking is gone: true/false statements and matching descriptions are whole sentences (only the concept's own name is replaced by "this idea");
2. sentences about the book's layout ("the chapter starts with ...", sections, the author) are never used as a question - a question is drawn only from a concept's own definition;
3. the midterm no longer has fill-in-the-word questions (exact wording): it has more multiple-choice questions from the question bank and prefers the Understand and Apply levels;
4. a new exam (no code typed) is chosen among up to 300 candidate exams for the fewest questions the student has already had, so the same questions do not come back at once;
   a typed code still gives exactly the same exam.
usage: template_patch_v9_21_0.py IN(9.20.0) OUT(9.21.0)"""
import sys
__version__ = "9.21.0"
s = open(sys.argv[1], encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)
# 1+2 whole sentences, only from definitions
rep("const xdef=n=>xclean(n.definition||qFirst(n));", """const xdef=n=>xclean(n.definition||qFirst(n));
// a sentence fit to be a question: from the concept's own definition (or its body when that is a plain statement), never about the book's layout
const XMETA=/\\b(chapter|section|the book|the author|this text|sweigart)\\b|\\bfirst program\\b/i;
function xFact(n){let t=xclean(n.definition||'');if(t.split(/\\s+/).length<5)t=xclean(qFirst(n));return (t.split(/\\s+/).length<5||t.split(/\\s+/).length>45||XMETA.test(t))?'':t}
function xNoLabel(t,label){const e=String(label).replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&');return t.replace(new RegExp('\\\\b'+e+'\\\\b','gi'),'this idea')}""")
rep("function xCloze(n,R){const s=xdef(n),wc", "function xCloze(n,R){const s=xFact(n),wc")
rep("function xJudge(n,R){const s=xdef(n);if(!s||s.split(' ').length<6)return null;\n const sib=D.nodes.filter(x=>x.id!==n.id&&x.level===n.level&&xdef(x)&&xdef(x)!==s&&xdef(x).split(' ').length>=6);",
    "function xJudge(n,R){const s=xFact(n);if(!s)return null;\n const sib=D.nodes.filter(x=>x.id!==n.id&&x.level===n.level&&xFact(x)&&xFact(x)!==s);")
rep("claim:n.label,text:qMask(owner),truth,owner:owner.id,options:opts.map(x=>x.id),sentence:xdef(owner)}}", "claim:n.label,text:xNoLabel(xFact(owner),owner.label),truth,owner:owner.id,options:opts.map(x=>x.id),sentence:xFact(owner)}}")
rep("function xMatch(n,R){const ok=x=>xdef(x)&&xdef(x).split(' ').length>=5;", "function xMatch(n,R){const ok=x=>!!xFact(x);")
rep("rows:xsh(items,R).map(x=>({id:x.id,def:qMask(x)}))", "rows:xsh(items,R).map(x=>({id:x.id,def:xNoLabel(xFact(x),x.label)}))")
rep("else{model=xdef(n);if(model.split(' ').length<7)return null;", "else{model=xFact(n);if(model.split(' ').length<7)return null;")
# the practice question "Which concept does this describe?" uses the same readable sentence
a = s.index("function qMask(n){"); e = s.index("\n", a)
s = s[:a] + "function qMask(n){return xNoLabel(xFact(n)||xclean(qFirst(n)),n.label)}" + s[e:]
# 3 midterm without fill-in-the-word
rep("M:{name:'Midterm-style',minutes:40,prefer:['Remember','Understand'],mix:[['mcq',4],['cloze',2],['judge',2],['match',1],['predict',2],['blank',1],['order',1],['short',1]]}",
    "M:{name:'Midterm-style',minutes:40,prefer:['Understand','Apply','Analyze'],mix:[['mcq',6],['judge',2],['match',1],['predict',2],['blank',1],['order',1],['short',1]]}")
rep("const XFALL=['mcq','cloze','judge','short'];", "const XFALL=['mcq','judge','short'];")
# multiple-choice questions that ask what the book says (chapter, section, author) are not used in an exam, and the preferred levels are kept when there are enough of them
rep("let bs=BANK.filter(b=>set.has(b.concept)&&!used.has('mcq:'+b.q));const pf=ctx.prefer||[];",
    "let bs=BANK.filter(b=>set.has(b.concept)&&!used.has('mcq:'+b.q)&&!XMETA.test(b.q));const pf=ctx.prefer||[];{const pl=bs.filter(b=>pf.includes(b.level));if(pl.length)bs=pl}")
rep("const bs=BANK.filter(b=>b.concept===n.id&&String(b.why||'').split(' ').length>=9);", "const bs=BANK.filter(b=>b.concept===n.id&&String(b.why||'').split(' ').length>=9&&!XMETA.test(b.q)&&!XMETA.test(b.options[b.answer]));")
# 4 fresh questions
rep("else{k=document.getElementById('xekind').value;seed=1+Math.floor(Math.random()*99999)}\n const code=k+'-'+seed;items=XS.items[code]?JSON.parse(JSON.stringify(XS.items[code])):null;\n if(!items){items=await xExamBuild(k,seed);",
"""else{k=document.getElementById('xekind').value;seed=0}
 if(!seed){const seen=new Set();Object.values(XS.items||{}).forEach(its=>(its||[]).forEach(x=>seen.add(xFp(x))));let best=null;
  for(let t=0;t<300;t++){const sd=1+Math.floor(Math.random()*99999),its=await xExamBuild(k,sd),dup=its.filter(x=>seen.has(xFp(x))).length;if(!best||dup<best.dup)best={sd,its,dup};if(!dup)break}
  seed=best.sd;items=best.its;XS.items[k+'-'+seed]=JSON.parse(JSON.stringify(items))}
 const code=k+'-'+seed;if(!items)items=XS.items[code]?JSON.parse(JSON.stringify(XS.items[code])):null;
 if(!items){items=await xExamBuild(k,seed);""")
rep("async function xExamStart(){", "const xFp=x=>x.type+':'+(x.concept||'')+':'+(x.type==='mcq'?x.q:x.type==='predict'||x.type==='blank'?x.code:'');\nasync function xExamStart(){")
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("wrote", sys.argv[2], len(s))
