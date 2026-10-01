// ---- 9.23.0: multiple choice with several correct statements (select all that apply) ----
const XPRON=/^(It|Its|This|That|These|Those|They|Their|Them|He|She|Both|Such|There|Here|However|But|And|So|Because|Instead|Also|Then|Once|Each)\b/;
// whole sentences of a concept's own text that stand on their own (they name their subject and say something checkable)
function xSents(n){const raw=[n.definition||''].concat((n.paras||[]).map(p=>p.text));const out=[];
 raw.forEach(t=>String(t).split(/(?<=[.!?])\s+(?=[A-Z])/).forEach(s=>{s=xclean(s);const w=s.split(/\s+/).length;if(w>=7&&w<=40&&!XMETA.test(s)&&!XPRON.test(s)&&!/\?$/.test(s)&&!out.includes(s))out.push(s)}));return out}
function xMulti(n,R){const mine=xSents(n);if(mine.length<2)return null;
 const up=new Set();let t=n;while(t){up.add(t.id);t=t.parent?byId[t.parent]:null}
 const below=x=>{let u=x;while(u){if(u.id===n.id)return true;u=u.parent?byId[u.parent]:null}return false};
 const lw=new Set(xwords(n.label).filter(w=>w.length>3).map(xstem)),pool=D.nodes.filter(x=>x.id!==n.id&&x.level>=2&&!up.has(x.id)&&!below(x)&&x.parent!==n.parent);
 const others=[];pool.forEach(x=>xSents(x).forEach(s=>{if(!xwords(s).some(w=>lw.has(xstem(w)))&&!mine.includes(s))others.push({s,id:x.id})}));
 const nt=Math.min(mine.length,R()<.6?2:3),nf=5-nt,seen=new Set(),fa=[];
 xsh(others,R).forEach(o=>{if(fa.length<nf&&!seen.has(o.id)){seen.add(o.id);fa.push(o)}});
 if(fa.length<nf)return null;
 const tr=xsh(mine,R).slice(0,nt),items=xsh(tr.map(s=>({s,ok:1,id:n.id})).concat(fa.map(o=>({s:o.s,ok:0,id:o.id}))),R);
 return {type:'multi',concept:n.id,level:'Understand',q:'Which of these statements describe “'+n.label+'”? Select all that apply.',options:items.map(x=>x.s),answer:items.map((x,i)=>x.ok?i:-1).filter(i=>i>=0),
  why:'The statements that describe “'+n.label+'”: '+tr.join(' ')+' The others describe '+fa.map(o=>'“'+xlab(o.id)+'”').join(', ')+'.'}}
function xMarkMulti(it,a){const sel=Array.isArray(a)?a.filter(j=>j>=0&&j<it.options.length):[];if(!sel.length)return {score:0,msg:'Nothing selected.',fix:esc(it.why||'')};
 const hit=sel.filter(j=>it.answer.includes(j)).length,wr=sel.length-hit,score=Math.round(Math.max(0,(hit-wr)/it.answer.length)*100)/100;
 return {score,msg:score===1?'Correct: every right statement chosen and no wrong one.':hit+' of '+it.answer.length+' right statements chosen'+(wr?'; '+wr+' wrong choice'+(wr>1?'s':'')+' taken off.':'.'),fix:esc(it.why||'')}}
