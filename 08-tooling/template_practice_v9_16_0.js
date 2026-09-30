// ---------- 9.16.0: closed corrections, the scaffolded-program question, exam history, save and open code ----------
// corrections are folded until asked for
xFeed=function(it,r){return '<p class="xmsg" role="status">'+(r.score===1?'✓ ':r.score>0?'◐ ':'✗ ')+r.msg+' <span class="note">('+(Math.round(r.score*it.pts*10)/10)+' of '+it.pts+')</span></p>'+(r.fix?'<details class="xfixd"><summary>'+(r.score===1?'Why this is right':'Show the correction')+'</summary><p class="xfix">'+r.fix+'</p></details>':'')};

// ---- complete the program: a given program with marked parts left to write, tips and notes on request ----
const XP_PASS='pass  # replace this line';
function xpBalanced(t){const o=(t.match(/[(\[{]/g)||[]).length,c=(t.match(/[)\]}]/g)||[]).length;return o===c&&!/\\\s*$/.test(t)&&!/,\s*$/.test(t)}
function xpTips(t,rest){let goal;const asg=t.match(/^([A-Za-z_][\w, *]*?)\s*=(?!=)\s*(.+)$/),aug=t.match(/^([A-Za-z_]\w*)\s*(\+=|-=|\*=|\/=)/),meth=t.match(/^([A-Za-z_]\w*)\.(\w+)\(/);
 if(asg){const names=asg[1].split(/[ ,*]+/).filter(Boolean),used=names.filter(n=>new RegExp('\\b'+n+'\\b').test(rest));goal='This line has to give a value to '+names.map(n=>'<code>'+esc(n)+'</code>').join(' and ')+(used.length?', which the lines after it use.':'.')}
 else if(aug)goal='This line has to update <code>'+esc(aug[1])+'</code> from its current value.';
 else if(meth)goal='This line has to change <code>'+esc(meth[1])+'</code> with one of its methods; the lines after it show the effect.';
 else if(/^return\b/.test(t))goal='This line has to send the function’s result back to the caller.';
 else goal='The lines after this one depend on it.';
 let shape,tok='';const call=t.match(/([A-Za-z_][\w.]*)\(/);
 if(call){const path=call[1],last=path.split('.').pop();tok=last;shape=t.replace(call[0],path.replace(/\w+$/,'____')+'(')}
 else if(asg)shape=asg[1]+' = ____';else if(/^return\b/.test(t))shape='return ____';else shape='____';
 return {goal,shape,tok}}
function xpNote(tok){if(!tok)return null;const re=new RegExp('\\b'+tok+'\\b');const n=D.nodes.find(x=>x.level===3&&x.example&&re.test(x.example))||D.nodes.find(x=>x.level===3&&re.test(x.label.toLowerCase().replace(/ /g,'_')));return n?{id:n.id,text:'“'+n.label+'”: '+xdef(n)}:null}
async function xProgramMake(ctx){const R=ctx.R,used=ctx.used||new Set(),src=[];
 if(D.course&&D.course.playground&&D.course.playground.code)src.push({label:D.course.playground.label.replace(/\s*\(uses input\)/,''),code:D.course.playground.code,inputs:String(D.course.playground.inputs||'').split('|').filter(Boolean)});
 TRACE_EX.forEach(([l,c])=>src.push({label:l,code:c,inputs:[]}));
 for(const s of xsh(src,R)){if(!s.inputs.length&&!xnoin(s.code))continue;const exp=String(await runPy(s.code,s.inputs)).trim();if(!exp||exIsErr(exp))continue;
  const L=s.code.split('\n'),cand=[];
  L.forEach((l,i)=>{const t=l.trim();if(!t||t.startsWith('#')||t.endsWith(':')||/^(print|import|from|def|class|pass|break|continue|if|elif|else|for|while|try|except|finally|with)\b/.test(t)||!xpBalanced(t))return;cand.push(i)});
  const ess=[];for(const i of xsh(cand,R)){if(ess.length>=3)break;const ind=L[i].match(/^ */)[0],alt=L.slice();alt[i]=ind+'pass';const out=String(await runPy(alt.join('\n'),s.inputs)).trim();if(out!==exp)ess.push(i)}
  if(!ess.length)continue;const k=ess.length>=3&&R()<.4?3:ess.length>=2?2:1,pick=ess.slice(0,k).sort((a,b)=>a-b),key='program:'+s.label+':'+pick.join(',');if(used.has(key))continue;
  const T=L.slice(),blanks=[];pick.forEach((i,j)=>{const t=L[i].trim(),ind=L[i].match(/^ */)[0],rest=L.slice(i+1).join('\n'),tp=xpTips(t,rest);blanks.push({n:j+1,goal:tp.goal,shape:tp.shape,note:xpNote(tp.tok),line:t});T[i]=ind+'# TODO '+(j+1)+': write the missing line'+'\n'+ind+XP_PASS});
  const fixed=L.filter((l,i)=>l.trim()&&!pick.includes(i)).map(l=>l.trim());used.add(key);
  return {type:'program',concept:(blanks.find(b=>b.note)||{note:{}}).note.id||'',level:'Apply',pts:XT_PTS.program,label:s.label,template:T.join('\n'),blanks,original:s.code,inputs:s.inputs,expected:exp,fixed}}
 return null}
function xpBody(it,id){const jump=it.concept?' <button class="jump" data-go="'+esc(it.concept)+'" aria-label="Open the concept">'+esc(xlab(it.concept))+'</button>':'';
 return '<p><b>'+esc(it.label)+'.</b> Complete the program. Under each <code># TODO</code> comment, replace the line <code>'+XP_PASS+'</code> with the missing line. Only the marked parts are yours to write; the rest is given and has to stay. Run it in your head or in the Playground: it has to print</p><pre>'+esc(it.expected)+'</pre>'
  +(it.inputs.length?'<p class="note">The program is given the input: <code>'+esc(it.inputs.join(' | '))+'</code></p>':'')
  +'<textarea class="mycode" id="'+id+'-a" spellcheck="false" rows="'+Math.min(18,it.template.split('\n').length+1)+'" aria-label="Program to complete">'+esc(it.template)+'</textarea>'
  +'<div class="xtips">'+it.blanks.map(b=>'<details><summary>Tip for TODO '+b.n+'</summary><p>'+b.goal+'</p><p>The line has this shape: <code>'+esc(b.shape)+'</code></p>'+(b.note?'<p class="note">From the chapter, '+esc(b.note.text)+'</p>':'')+'</details>').join('')+'</div>'
  +'<p class="xrow"><button class="btn g" data-xreset="1" data-template="'+esc(it.template)+'">Reset the template</button></p><span class="xj">'+jump+'</span>'}
async function xpMark(it,a){const code=String(a||''),lines=code.split('\n').map(l=>l.trim());let score=0,msg='';
 const fix='The missing '+(it.blanks.length>1?'lines were':'line was')+':<pre>'+esc(it.blanks.map(b=>b.line).join('\n'))+'</pre>The whole program:<pre>'+esc(it.original)+'</pre>';
 if(!code.trim())return {score:0,msg:'Nothing written.',fix};
 const left=lines.filter(l=>l===XP_PASS).length,gone=it.fixed.filter(l=>!lines.includes(l));
 if(left)return {score:0,msg:'A marked part is still empty: the line “'+XP_PASS+'” is still there.',fix};
 if(gone.length)return {score:0,msg:'A given line was changed or removed (“'+esc(gone[0])+'”). Only the marked parts are yours to write.',fix};
 const out=String(await runPy(code,it.inputs)).trim();
 if(exIsErr(out))msg='It raises <code>'+esc(xoneline(out))+'</code>.';else if(out===it.expected){score=1;msg='Correct: the program prints what it should.'}else msg='It prints <code>'+esc(out.slice(0,80))+'</code> instead of <code>'+esc(it.expected.slice(0,80))+'</code>.';
 return {score,msg,fix}}
{const _xBody=xBody,_xMark=xMark,_xKey=xKey,_xMake=xMake;
 xBody=function(it,id){return it.type==='program'?xpBody(it,id):_xBody(it,id)};
 xMark=async function(it,a){return it.type==='program'?await xpMark(it,a):await _xMark(it,a)};
 xKey=function(it){return it.type==='program'?it.original:_xKey(it)};
 xMake=async function(type,ctx){if(type==='program')return await xProgramMake(ctx);return await _xMake(type,ctx)}}
document.addEventListener('click',e=>{const r=e.target.closest&&e.target.closest('[data-xreset]');if(!r)return;e.stopImmediatePropagation();const ta=r.closest('fieldset').querySelector('textarea');if(ta){ta.value=r.dataset.template;ta.dispatchEvent(new Event('input',{bubbles:true}))}},true);

// ---- the exams you have made: kept, listed, and reopened later ----
const XK2='course-page-exams2:'+D.title;let XS={recs:[],items:{}};
try{XS=JSON.parse(localStorage.getItem(XK2)||'null')||XS}catch(e){}
if(!XS.recs.length&&typeof XHIST!=='undefined'&&XHIST.length)XS.recs=XHIST.map(h=>({id:h.at,code:h.code,kind:String(h.code).charAt(0),at:h.at,status:'done',pct:h.pct,got:h.got,pts:h.pts}));
function xSave(){XS.recs=XS.recs.slice(-40);const keep=new Set(XS.recs.map(r=>r.code));Object.keys(XS.items).forEach(c=>{if(!keep.has(c))delete XS.items[c]});
 const codes=Object.keys(XS.items);while(codes.length>12)delete XS.items[codes.shift()];
 for(let t=0;t<14;t++){try{localStorage.setItem(XK2,JSON.stringify(XS));return}catch(e){const c=Object.keys(XS.items)[0];if(c)delete XS.items[c];else{XS.recs=XS.recs.slice(-10)}}}}
const xRec=id=>XS.recs.find(r=>r.id===id);
xHistPaint=function(){const el=document.getElementById('xehist');if(!el)return;
 el.innerHTML=XS.recs.length?'<h3>My exams</h3><p class="note">Every exam you start is kept here, in this browser. Open one again, review the marked attempt with its corrections, or take the same questions once more.</p><div class="tscroll"><table><thead><tr><th scope="col">Exam</th><th scope="col">When</th><th scope="col">Result</th><th scope="col">Actions</th></tr></thead><tbody>'+XS.recs.slice().reverse().map(r=>{const has=!!XS.items[r.code];const nm=(XEXAM[r.kind]||{name:'Exam'}).name;
   return '<tr><td><code>'+esc(r.code)+'</code> '+esc(nm)+'</td><td>'+esc(new Date(r.at).toLocaleString())+'</td><td>'+(r.status==='done'?r.pct+'% ('+r.got+' of '+r.pts+')':'not finished')+'</td><td>'+(has?(r.status==='done'&&r.res?'<button class="btn g" data-xeact="review" data-xeid="'+r.id+'">Review</button> ':'')+'<button class="btn g" data-xeact="take" data-xeid="'+r.id+'">'+(r.status==='done'?'Retake':'Start')+'</button> ':'<span class="note">summary only </span>')+'<button class="btn g" data-xeact="del" data-xeid="'+r.id+'" aria-label="Delete this exam from my list">Delete</button></td></tr>'}).join('')+'</tbody></table></div><p><button class="btn g" id="xeclear">Clear my list</button></p>':'<p class="note">No exam yet. Start one above; it will be kept here.</p>'};
async function xExamShow(k,seed,items,rec){const out=document.getElementById('xeout'),spec=XEXAM[k],pts=items.reduce((a,x)=>a+x.pts,0),code=k+'-'+seed;
 clearInterval(XE.timer);XE.done=false;XE.kind=k;XE.seed=seed;XE.items=items;XE.rec=rec;document.getElementById('xecode').value=code;document.getElementById('xekind').value=k;
 const timerOn=document.getElementById('xetimeron').checked;XE.deadline=timerOn?Date.now()+spec.minutes*60000:0;
 out.innerHTML='<div id="xetimer" role="timer">'+esc(spec.name)+' exam <code>'+code+'</code> · '+items.length+' questions · '+pts+' points'+(timerOn?' · time left <span id="xeleft"></span>':' · no timer')+'</div><div id="xesum"></div>'+xExamHtml()+'<p class="xrow"><button class="btn" id="xefinish">Finish and mark</button></p>';
 if(timerOn){const tick=()=>{const left=Math.max(0,XE.deadline-Date.now()),el=document.getElementById('xeleft');if(el)el.textContent=Math.floor(left/60000)+':'+String(Math.floor(left/1000)%60).padStart(2,'0');if(!left&&!XE.done)xExamFinish(true)};tick();XE.timer=setInterval(tick,1000)}}
xExamStart=async function(fromRec){const out=document.getElementById('xeout');let k,seed,raw=document.getElementById('xecode').value.trim(),m,items=null;
 if(fromRec&&fromRec.code){raw=fromRec.code}
 m=raw.match(/^([MF])-(\d{1,9})$/i);
 if(m){k=m[1].toUpperCase();seed=+m[2]}else if(raw){out.innerHTML='<p class="note">An exam code looks like M-12345 (midterm) or F-12345 (final). Leave the box empty for a new exam.</p>';return}else{k=document.getElementById('xekind').value;seed=1+Math.floor(Math.random()*99999)}
 const code=k+'-'+seed;items=XS.items[code]?JSON.parse(JSON.stringify(XS.items[code])):null;
 if(!items){items=await xExamBuild(k,seed);if(!items.length){out.innerHTML='<p class="note">This chapter has too little material to build an exam.</p>';return}XS.items[code]=JSON.parse(JSON.stringify(items))}
 const rec={id:Date.now(),code,kind:k,at:Date.now(),status:'open',pts:items.reduce((a,x)=>a+x.pts,0)};XS.recs.push(rec);xSave();xHistPaint();
 await xExamShow(k,seed,items,rec)};
xExamFinish=async function(timeUp){if(XE.done||!XE.items.length)return;XE.done=true;clearInterval(XE.timer);const fin=document.getElementById('xefinish');if(fin)fin.disabled=true;const sum=document.getElementById('xesum');const res=[],ans=[];
 for(let i=0;i<XE.items.length;i++){if(sum)sum.innerHTML='<p class="note">Marking question '+(i+1)+' of '+XE.items.length+'...</p>';const it=XE.items[i],fs=document.querySelector('#xeout fieldset[data-xi="'+i+'"]');let r,a=xRead(it,fs);ans.push(a);try{r=await xMark(it,a)}catch(e){r={score:0,msg:'The check could not run ('+esc(e.message||'error')+').',fix:''}}
  res.push(r);fs.querySelector('.xfeed').innerHTML=xFeed(it,r);fs.classList.toggle('right',r.score===1);fs.classList.toggle('wrong',r.score===0);fs.classList.toggle('half',r.score>0&&r.score<1);fs.querySelectorAll('input,select,textarea,button[data-exmv],[data-xreset]').forEach(e=>{e.disabled=true});
  if(it.concept)recordReview(it.concept,r.score>=.5)}
 const rec=XE.rec;XE.result=xExamSummary(XE.kind,XE.seed,XE.items,res,timeUp===true);
 if(rec){Object.assign(rec,{status:'done',pct:XE.result.pct,got:XE.result.got,pts:XE.result.pts,ans,res:res.map(r=>({score:r.score,msg:r.msg,fix:r.fix})),by:XE.result.by,weak:XE.result.weak,timeUp:timeUp===true,done:Date.now()});xSave();xHistPaint()}
 sum.innerHTML=XE.result.html;if(sum.scrollIntoView)sum.scrollIntoView({block:'start'})};
function xExamSummary(k,seed,items,res,timeUp){const pts=items.reduce((a,x)=>a+x.pts,0),got=res.reduce((a,r,i)=>a+r.score*items[i].pts,0),pct=Math.round(100*got/pts),by={};
 items.forEach((it,i)=>{const t=xtopic(byId[it.concept]||{label:'General programs',id:''});const b=by[t.id]||(by[t.id]={label:t.label,got:0,pts:0});b.got+=res[i].score*it.pts;b.pts+=it.pts});
 const weak=[...new Set(items.filter((it,i)=>res[i].score<.5&&it.concept).map(it=>it.concept))],code=k+'-'+seed,g=Math.round(got*10)/10;
 const html='<div class="xrep" id="xereport"><h3>Result'+(timeUp?' (time was up)':'')+'</h3><p><b>'+g+' of '+pts+' points, '+pct+'%.</b> Exam <code>'+code+'</code>. Each question below shows what happened; the correction is folded under it until you open it.</p><table><tr><th>Subject</th><th>Points</th></tr>'+Object.values(by).map(b=>'<tr><td>'+esc(b.label)+'</td><td>'+(Math.round(b.got*10)/10)+' of '+b.pts+'</td></tr>').join('')+'</table>'+(weak.length?'<p>To go over again (already in your review queue): '+weak.map(c=>'<button class="jump" data-go="'+esc(c)+'">'+esc(xlab(c))+'</button>').join(' ')+'</p>':'<p>No concept fell below half marks.</p>')+'<p class="xrow"><button class="btn g" id="xecopy">Copy the result</button><button class="btn g" id="xeprint">Print</button><button class="btn g" id="xeagain">Retake this exam</button><button class="btn g" id="xenew">An alternative exam</button></p></div>';
 return {code,got:g,pts,pct,by,weak,html,md:'# '+XEXAM[k].name+' exam '+code+' - '+D.title+'\n\nScore: '+g+' of '+pts+' ('+pct+'%)\n\n'+Object.values(by).map(b=>'- '+b.label+': '+(Math.round(b.got*10)/10)+' of '+b.pts).join('\n')+(weak.length?'\n\nTo review: '+weak.map(xlab).join(', '):'')+'\n'}}
function xFill(it,fs,a){const q=s=>fs.querySelector(s);
 if(it.type==='mcq'){if(a!=null){const r=fs.querySelectorAll('input[type=radio]')[a];if(r)r.checked=true}}
 else if(it.type==='judge'){if(a&&a.v!=null){const r=fs.querySelector('input[type=radio][value="'+a.v+'"]');if(r)r.checked=true}if(a&&q('select'))q('select').value=a.s||''}
 else if(it.type==='match'){Object.keys(a||{}).forEach(k=>{const s=[...fs.querySelectorAll('select[data-row]')].find(x=>x.dataset.row===k);if(s)s.value=a[k]})}
 else if(it.type==='order'){const ol=q('ol'),lis=[...ol.querySelectorAll('li')],used=new Set();(a||[]).forEach(line=>{const li=lis.find(l=>!used.has(l)&&it.lines[+l.querySelector('code').dataset.l]===line);if(li){used.add(li);ol.appendChild(li)}})}
 else{const e=q('textarea,input.xin');if(e)e.value=a==null?'':a}}
async function xExamReview(rec){const items=XS.items[rec.code];if(!items||!rec.res)return;const out=document.getElementById('xeout');clearInterval(XE.timer);XE.done=true;XE.items=JSON.parse(JSON.stringify(items));XE.kind=rec.kind;XE.seed=+rec.code.slice(2);XE.rec=null;
 out.innerHTML='<div id="xetimer" role="timer">Review of exam <code>'+esc(rec.code)+'</code> taken '+esc(new Date(rec.at).toLocaleString())+'</div><div id="xesum"></div>'+xExamHtml();
 XE.items.forEach((it,i)=>{const fs=out.querySelector('fieldset[data-xi="'+i+'"]');xFill(it,fs,rec.ans[i]);const r=rec.res[i];fs.querySelector('.xfeed').innerHTML=xFeed(it,r);fs.classList.toggle('right',r.score===1);fs.classList.toggle('wrong',r.score===0);fs.classList.toggle('half',r.score>0&&r.score<1);fs.querySelectorAll('input,select,textarea,button[data-exmv],[data-xreset]').forEach(e=>{e.disabled=true})});
 XE.result=xExamSummary(rec.kind,XE.seed,XE.items,rec.res,!!rec.timeUp);document.getElementById('xesum').innerHTML=XE.result.html;document.getElementById('xesum').scrollIntoView({block:'start'})}
document.addEventListener('click',async e=>{const t=e.target;if(!t.closest)return;
 const a=t.closest('[data-xeact]');if(a){e.stopImmediatePropagation();const rec=xRec(+a.dataset.xeid);if(!rec)return;
  if(a.dataset.xeact==='review'){await xExamReview(rec);return}
  if(a.dataset.xeact==='take'){document.getElementById('xecode').value=rec.code;await xExamStart(rec);return}
  if(a.dataset.xeact==='del'){XS.recs=XS.recs.filter(r=>r.id!==rec.id);xSave();xHistPaint();return}}
 if(t.id==='xeclear'){e.stopImmediatePropagation();XS.recs=[];XS.items={};xSave();xHistPaint();return}
 if(t.id==='xeagain'){e.stopImmediatePropagation();document.getElementById('xecode').value=XE.kind+'-'+XE.seed;xExamStart();return}
 if(t.id==='xenew'){e.stopImmediatePropagation();document.getElementById('xecode').value='';xExamStart();return}
},true);
xHistPaint();

// ---- save the code as a file, open a file into the code ----
function edFileName(ta){return ta.dataset.fname||(ta.id==='pcode'?'playground':ta.id==='clcode'?'code-lab':ta.id.replace(/[^\w-]+/g,'')||'code')}
async function edSave(ta){const name=edFileName(ta)+'.py',txt=ta.value;
 try{if(window.showSaveFilePicker){const h=await window.showSaveFilePicker({suggestedName:name,types:[{description:'Python file',accept:{'text/x-python':['.py']}}]});const w=await h.createWritable();await w.write(txt);await w.close();toast('Saved '+h.name);return}}catch(e){if(e&&e.name==='AbortError')return}
 const url=URL.createObjectURL(new Blob([txt],{type:'text/x-python'})),a=document.createElement('a');a.href=url;a.setAttribute('download',name);a.hidden=true;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),5000);toast('Saved '+name)}
function edLoadText(ta,file){if(!file)return;if(file.size>300000){toast('That file is too large for the editor (limit 300 KB).');return}
 const rd=new FileReader();rd.onload=()=>{const txt=String(rd.result||'');if(txt.indexOf('\u0000')>=0){toast('That does not look like a text file.');return}ta.value=txt.replace(/\r\n?/g,'\n');ta.dispatchEvent(new Event('input',{bubbles:true}));ta.focus();ta.setSelectionRange(0,0);toast('Opened '+file.name)};rd.onerror=()=>toast('The file could not be read.');rd.readAsText(file)}
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-edact="save"],[data-edact="open"]');if(!b)return;e.stopImmediatePropagation();const ed=b.closest('.ed'),ta=ed.querySelector('textarea.edta');
 if(b.dataset.edact==='save')edSave(ta);else{const f=ed.querySelector('input.edfile');f.value='';f.click()}},true);
document.addEventListener('change',e=>{const f=e.target;if(f.matches&&f.matches('input.edfile')){const ta=f.closest('.ed').querySelector('textarea.edta');edLoadText(ta,f.files&&f.files[0])}});
document.addEventListener('dragover',e=>{if(e.target.closest&&e.target.closest('.ed[data-full="1"] .edbox')&&e.dataTransfer&&[...e.dataTransfer.types].includes('Files'))e.preventDefault()});
document.addEventListener('drop',e=>{const b=e.target.closest&&e.target.closest('.ed[data-full="1"] .edbox');if(!b||!e.dataTransfer||!e.dataTransfer.files.length)return;e.preventDefault();edLoadText(b.querySelector('textarea.edta'),e.dataTransfer.files[0])});
