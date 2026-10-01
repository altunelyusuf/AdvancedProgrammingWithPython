// ---- 9.23.0: the input row appears only when the program calls input(), with values that fit the code ----
// inpCalls finds every call of input() that is real code (not inside a string or a comment) and notes what the call
// is wrapped in (int, float), the name it is stored under, the prompt it shows and whether it sits inside a loop.
function inpCalls(code){code=String(code);const re=/'''[\s\S]*?'''|"""[\s\S]*?"""|'(?:\\.|[^'\\\n])*'|"(?:\\.|[^"\\\n])*"|#[^\n]*|(?<![\w.])input\s*\(/g,out=[];let m;
 while((m=re.exec(code))){if(!/^input/.test(m[0]))continue;
  const idx=m.index,ls=code.lastIndexOf('\n',idx)+1,pre=code.slice(ls,idx),rest=code.slice(idx+m[0].length),pm=rest.match(/^\s*f?(['"])((?:\\.|(?!\1)[^\\\n])*)\1/),
   wrap=(pre.match(/\b(int|float|eval)\s*\(\s*$/)||[])[1]||'',name=(pre.match(/([A-Za-z_]\w*)\s*(?::[^=\n]+)?=\s*(?:\w+\s*\(\s*)*$/)||[])[1]||'',ind=(code.slice(ls).match(/^[ \t]*/)||[''])[0].length;
  let loop=false;if(ind>0){const before=code.slice(0,ls).split('\n');for(let k=before.length-1;k>=0;k--){const L=before[k];if(!L.trim())continue;const li=(L.match(/^[ \t]*/)||[''])[0].length;if(li<ind){loop=/^\s*(for|while)\b/.test(L);break}}}
  out.push({prompt:pm?pm[2]:'',wrap,name,loop})}
 return out}
// a value that fits the call: a whole number where int() wraps it, a decimal where float() does, a name where the prompt asks for one
function inpGuess(c){const t=(c.name+' '+c.prompt).toLowerCase();
 if(c.wrap==='float')return /temp|celsius|fahrenheit/.test(t)?'21.5':/price|cost|amount/.test(t)?'12.5':'3.5';
 if(c.wrap==='int'||c.wrap==='eval')return /\bage\b/.test(t)?'20':/year/.test(t)?'2000':/count|times|how many|limit|size/.test(t)?'3':/guess|number|num\b|\bn\b/.test(t)?'7':'5';
 if(/name|who/.test(t))return 'Ayse';
 if(/city|town/.test(t))return 'Istanbul';
 if(/colou?r/.test(t))return 'blue';
 if(/password/.test(t))return 'swordfish';
 if(/yes|no\b|y\/n|again|continue|more/.test(t))return c.loop?'yes':'no';
 return 'hello'}
function inpDefaults(calls){const L=[];calls.forEach(c=>{const g=inpGuess(c);if(c.loop){L.push(g,g);L.push(g==='yes'?'no':g)}else L.push(g)});return L}
// keeps one input row in step with the code above it: shown (with suggested values and what they are for) or replaced by a short note
function inpSync(codeId,inId,boxId,noneId,helpId){const ta=document.getElementById(codeId),inp=document.getElementById(inId);if(!ta||!inp)return;
 const calls=inpCalls(ta.value),need=calls.length>0,box=document.getElementById(boxId),none=document.getElementById(noneId),help=document.getElementById(helpId);
 if(box)box.hidden=!need;if(none)none.hidden=need;
 const sig=need?JSON.stringify(calls):'';
 if(ta._inpSig!==sig){ta._inpSig=sig;inp.dataset.edited='0';
  if(!need)inp.value='';
  else if(!(codeId==='pcode'&&ta.value===D.course.playground.code&&D.course.playground.inputs))inp.value=inpDefaults(calls).join('|');
  else inp.value=D.course.playground.inputs}
 if(help&&need){const n=calls.length,ps=calls.map(c=>c.prompt.trim()).filter(Boolean).slice(0,3).map(p=>'“'+p+'”');
  help.textContent='This program calls input() '+(n===1?'once':n+' times')+(calls.some(c=>c.loop)?' (some inside a loop, so extra lines are supplied)':'')+(ps.length?', asking '+ps.join(', '):'')+'. One line per call, separated by |. Suggested values are filled in; change them if you like.'}
}
setInterval(()=>{try{inpSync('pcode','pin','pinbox','pinnone','pinhelp');inpSync('trcode','trin','trinbox','trinnone','trinhelp')}catch(e){}},300);
document.addEventListener('input',e=>{if(e.target&&(e.target.id==='pin'||e.target.id==='trin'))e.target.dataset.edited='1'});
