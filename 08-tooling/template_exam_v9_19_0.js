
// ---- graded exams: student identity, locked result, release code, result files (JSON and PDF) ----
// The instructor's public key and the release-code format are fixed by the course configuration. The lock is a courtesy of the
// page, not security: the page runs on the student's own computer. The released code is checked with the instructor's public key.
const XEX_PUB=__EXAM_PUB__, XEX_PREFIX='__EXAM_PREFIX__', XEX_BONUS=__EXAM_BONUS__;
const XEX_CH=String(D.chapter==null?'0':D.chapter).padStart(2,'0');
const XID_KEY='course-page-student';
function xidLoad(){try{return JSON.parse(localStorage.getItem(XID_KEY)||'null')||{}}catch(e){return {}}}
function xidRead(){const g=i=>{const e=document.getElementById(i);return e?e.value.replace(/\s+/g,' ').trim():''};return {number:g('xesno'),name:g('xesname'),surname:g('xessur')}}
function xidCheck(s){const bad=[];if(!/^[A-Za-z0-9-]{3,20}$/.test(s.number))bad.push('the student number (3 to 20 letters or digits)');
 if(!/^[\p{L}][\p{L}\s'’.-]{1,59}$/u.test(s.name))bad.push('your name');if(!/^[\p{L}][\p{L}\s'’.-]{1,59}$/u.test(s.surname))bad.push('your surname');return bad}
function xidPaint(){const s=xidLoad();[['xesno','number'],['xesname','name'],['xessur','surname']].forEach(([i,k])=>{const e=document.getElementById(i);if(e&&!e.value&&s[k])e.value=s[k]})}
function xidMsg(t){const m=document.getElementById('xeidmsg');if(m)m.textContent=t||''}
// canonical JSON and SHA-256 (tamper evidence only: anyone can recompute it)
function xCanon(v){if(Array.isArray(v))return '['+v.map(xCanon).join(',')+']';if(v&&typeof v==='object')return '{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+xCanon(v[k])).join(',')+'}';return JSON.stringify(v===undefined?null:v)}
function xSha256Js(bytes){const K=[];for(let i=2,n=0;n<64;i++){let p=1;for(let j=2;j*j<=i;j++)if(i%j==0){p=0;break}if(p){K[n++]=(Math.pow(i,1/3)%1*4294967296)|0}}
 let H=[];for(let i=2,n=0;n<8;i++){let p=1;for(let j=2;j*j<=i;j++)if(i%j==0){p=0;break}if(p){H[n++]=(Math.pow(i,1/2)%1*4294967296)|0}}
 const l=bytes.length,nb=((l+9+63)>>6)<<6,b=new Uint8Array(nb);b.set(bytes);b[l]=0x80;const dv=new DataView(b.buffer);dv.setUint32(nb-4,(l*8)>>>0);dv.setUint32(nb-8,Math.floor(l*8/4294967296));
 const w=new Int32Array(64);for(let o=0;o<nb;o+=64){for(let i=0;i<16;i++)w[i]=dv.getInt32(o+i*4);for(let i=16;i<64;i++){const a=w[i-15],c=w[i-2];w[i]=(w[i-16]+(((a>>>7)|(a<<25))^((a>>>18)|(a<<14))^(a>>>3))+w[i-7]+(((c>>>17)|(c<<15))^((c>>>19)|(c<<13))^(c>>>10)))|0}
  let [a,b2,c,d,e,f,g,h]=H;for(let i=0;i<64;i++){const t1=(h+(((e>>>6)|(e<<26))^((e>>>11)|(e<<21))^((e>>>25)|(e<<7)))+((e&f)^(~e&g))+K[i]+w[i])|0,t2=((((a>>>2)|(a<<30))^((a>>>13)|(a<<19))^((a>>>22)|(a<<10)))+((a&b2)^(a&c)^(b2&c)))|0;h=g;g=f;f=e;e=(d+t1)|0;d=c;c=b2;b2=a;a=(t1+t2)|0}
  H=[(H[0]+a)|0,(H[1]+b2)|0,(H[2]+c)|0,(H[3]+d)|0,(H[4]+e)|0,(H[5]+f)|0,(H[6]+g)|0,(H[7]+h)|0]}
 return H.map(x=>(x>>>0).toString(16).padStart(8,'0')).join('')}
async function xSha256(text){const bytes=new TextEncoder().encode(text);try{if(window.crypto&&crypto.subtle){const d=await crypto.subtle.digest('SHA-256',bytes);return [...new Uint8Array(d)].map(x=>x.toString(16).padStart(2,'0')).join('')}}catch(e){}return xSha256Js(bytes)}
const xb64u=s=>{s=String(s).replace(/-/g,'+').replace(/_/g,'/');const T='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/',o=[];let acc=0,bits=0;for(const ch of s){const v=T.indexOf(ch);if(v<0)continue;acc=((acc<<6)|v)&0xFFFFFF;bits+=6;if(bits>=8){bits-=8;o.push((acc>>bits)&255)}}return new Uint8Array(o)};
// the release code: R1.<scope>.<signature>; scope is "<chapter>:<exam code>", "<chapter>:*" or "*:*"
async function xVerifyRelease(code,rec){code=String(code||'').replace(/\s+/g,'');const m=code.match(/^R1\.([^.]+)\.([A-Za-z0-9_-]{86})$/);if(!m)return {ok:false,why:'That is not a release code. It starts with R1. and has two dots.'};
 const scope=m[1],ok=[XEX_CH+':'+rec.code,XEX_CH+':*','*:*'];if(!ok.includes(scope))return {ok:false,why:'This code is for another exam or chapter ('+scope+').'};
 if(!(window.crypto&&crypto.subtle))return {ok:false,why:'This browser cannot check release codes here. Open the page from the course site (https) or in a current browser.'};
 try{const key=await crypto.subtle.importKey('jwk',XEX_PUB,{name:'ECDSA',namedCurve:'P-256'},false,['verify']);
  const good=await crypto.subtle.verify({name:'ECDSA',hash:'SHA-256'},key,xb64u(m[2]),new TextEncoder().encode(XEX_PREFIX+'|'+scope));
  return good?{ok:true,scope}:{ok:false,why:'The code was not signed by the instructor.'}}catch(e){return {ok:false,why:'The code could not be checked ('+(e.message||'error')+').'}}}
// the result file
const xIsAns=a=>a!=null&&a!==''&&!(a&&typeof a==='object'&&!Array.isArray(a)&&Object.values(a).every(v=>v==null||v===''));
function xAnsText(it,a){try{if(!xIsAns(a))return '(no answer)';if(it.type==='mcq')return String.fromCharCode(65+a)+'. '+it.options[a];
 if(it.type==='judge')return (a.v==='1'?'true':a.v==='0'?'false':'(none)')+(a.s?' / '+(xlab(a.s)||a.s):'');
 if(it.type==='match')return Object.keys(a).map(k=>(xlab(k)||k)+' → '+(xlab(a[k])||a[k])).join('; ');if(it.type==='order'||Array.isArray(a))return a.join(' | ');return String(a)}catch(e){return String(a)}}
function xQText(it){return String(it.q||it.sentence||it.claim||it.prompt||it.title||it.code||it.template||'').replace(/\s+/g,' ').trim()}
async function xResultObject(rec,withMarks){const spec=XEXAM[rec.kind]||{name:'Exam',minutes:0};const items=XS.items[rec.code]||[];
 const o={format:'sen0414-exam-result',format_version:1,course:'SEN0414',chapter:D.chapter,chapter_title:D.title,page_version:(typeof PAGE_VERSION!=='undefined'?PAGE_VERSION:D._version||''),
  exam:{code:rec.code,kind:rec.kind,name:spec.name,points:rec.pts,minutes:spec.minutes,timer_used:!!rec.timer,time_up:!!rec.timeUp},
  student:rec.student||{number:'',name:'',surname:''},started:new Date(rec.at).toISOString(),finished:rec.done?new Date(rec.done).toISOString():null,
  items:items,answers:rec.ans||[],answered:(rec.ans||[]).filter(xIsAns).length};
 if(withMarks&&rec.released){o.released=true;o.release_code=rec.release;o.page_marks=(rec.res||[]).map(r=>r.score);o.page_total={got:rec.got,points:rec.pts,percent:rec.pct}}
 o.digest={alg:'SHA-256',over:'canonical JSON of this file without the digest',value:await xSha256(xCanon(o))};return o}
function xDownload(name,type,data){const url=URL.createObjectURL(new Blob([data],{type})),a=document.createElement('a');a.href=url;a.setAttribute('download',name);a.hidden=true;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),5000);toast('Saved '+name)}
const xFileBase=rec=>'sen0414-ch'+XEX_CH+'-'+rec.code+'-'+String((rec.student&&rec.student.number)||'student').replace(/[^A-Za-z0-9-]/g,'')+'-result';
// PDF: pages drawn on a canvas, stored as JPEG images inside a hand-written PDF
function xPdfPages(o,rec){const W=1240,H=1754,M=90,pages=[];let c,g,y;
 const fresh=()=>{c=document.createElement('canvas');c.width=W;c.height=H;g=c.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,W,H);g.fillStyle='#1F2933';y=M;pages.push(c)};
 const wrap=(t,font,maxw)=>{g.font=font;const out=[];String(t).split('\n').forEach(par=>{let line='';par.split(/(\s+)/).forEach(tok=>{const tr=line+tok;if(g.measureText(tr).width>maxw&&line){out.push(line.trimEnd());line=tok.trimStart()}else line=tr});out.push(line.trimEnd())});return out};
 const put=(t,size,bold,color,gap)=>{const f=(bold?'bold ':'')+size+'px "DejaVu Sans",Arial,sans-serif';wrap(t,f,W-2*M).forEach(l=>{if(y>H-M-size){fresh()}g.font=f;g.fillStyle=color||'#1F2933';g.fillText(l,M,y+size);y+=Math.round(size*1.4)});y+=gap==null?6:gap};
 fresh();put('SEN0414 Advanced Programming with Python',22,false,'#5B6B7B',2);put('Exam result',44,true,'#1E2A3A',8);
 put('Student number: '+o.student.number,30,true);put('Name: '+o.student.name+'   Surname: '+o.student.surname,30,true,null,14);
 put('Chapter '+o.chapter+': '+o.chapter_title,26,false,null,4);put('Exam '+o.exam.code+' ('+o.exam.name+'), '+o.exam.points+' points'+(o.exam.time_up?', time was up':''),26,false,null,4);
 put('Started: '+o.started+'   Finished: '+(o.finished||'not finished'),22,false,'#5B6B7B',4);put('Questions answered: '+o.answered+' of '+o.items.length,26,true,null,14);
 if(o.released)put('Score (released by the instructor): '+o.page_total.got+' of '+o.page_total.points+' points, '+o.page_total.percent+'%',30,true,'#1A7F37',14);
 else put('The score and the correct answers are withheld until the instructor gives the release code. The instructor marks the result file.',24,false,'#B42318',14);
 put('Your answers',28,true,'#1E2A3A',6);
 o.items.forEach((it,i)=>{const sc=o.released&&o.page_marks?' ['+(Math.round(o.page_marks[i]*it.pts*10)/10)+' of '+it.pts+']':'';
  put((i+1)+'. ('+it.type+', '+it.pts+' pt) '+xQText(it).slice(0,260)+sc,22,true,null,2);put('Answer: '+xAnsText(it,o.answers[i]).slice(0,600),21,false,'#306998',10)});
 put('Check value (SHA-256 of the result file): '+o.digest.value,17,false,'#5B6B7B',2);put('This value only shows whether the file was changed afterwards. Submit the .json file; this PDF is your copy.',17,false,'#5B6B7B',0);
 return pages}
async function xPdfBuild(pages){const enc=new TextEncoder(),parts=[],offs=[];let len=0;const push=b=>{if(typeof b==='string')b=enc.encode(b);parts.push(b);len+=b.length};
 const n=pages.length,imgs=await Promise.all(pages.map(c=>new Promise((res,rej)=>c.toBlob(bl=>bl?bl.arrayBuffer().then(ab=>res(new Uint8Array(ab))):rej(new Error('image')),'image/jpeg',.82))));
 const obj=(i,body)=>{offs[i]=len;push(i+' 0 obj\n');push(body);push('\nendobj\n')};
 push('%PDF-1.4\n%\xE2\xE3\xCF\xD3\n');const kids=pages.map((_,i)=>(3+i*3)+' 0 R').join(' ');
 obj(1,'<< /Type /Catalog /Pages 2 0 R >>');obj(2,'<< /Type /Pages /Kids ['+kids+'] /Count '+n+' >>');
 pages.forEach((c,i)=>{const p=3+i*3,im=p+1,ct=p+2,cs='q 595.28 0 0 841.89 0 0 cm /Im0 Do Q';
  obj(p,'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595.28 841.89] /Resources << /XObject << /Im0 '+im+' 0 R >> >> /Contents '+ct+' 0 R >>');
  offs[im]=len;push(im+' 0 obj\n<< /Type /XObject /Subtype /Image /Width '+c.width+' /Height '+c.height+' /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length '+imgs[i].length+' >>\nstream\n');push(imgs[i]);push('\nendstream\nendobj\n');
  obj(ct,'<< /Length '+cs.length+' >>\nstream\n'+cs+'\nendstream')});
 const total=3+n*3,xr=len;push('xref\n0 '+total+'\n0000000000 65535 f \n');for(let i=1;i<total;i++)push(String(offs[i]).padStart(10,'0')+' 00000 n \n');
 push('trailer\n<< /Size '+total+' /Root 1 0 R >>\nstartxref\n'+xr+'\n%%EOF\n');const out=new Uint8Array(len);let o=0;parts.forEach(b=>{out.set(b,o);o+=b.length});return out}
// the locked view
function xLockHtml(rec,note){const s=rec.student||{};const answered=(rec.ans||[]).filter(xIsAns).length;
 return '<div class="xrep xlock" id="xelock"><h3>Submitted</h3><p><b>'+esc(s.name||'')+' '+esc(s.surname||'')+'</b>, student number <b>'+esc(s.number||'')+'</b>. Exam <code>'+esc(rec.code)+'</code>: '+answered+' of '+(XS.items[rec.code]||[]).length+' questions answered.</p>'+
 '<p>Your score and the correct answers stay hidden until the instructor gives the release code for this exam. Download your result file now and hand it in as the instructor asks: the <b>.json</b> file is the one that is marked; the <b>.pdf</b> is your copy.</p>'+
 '<p class="xrow"><button class="btn" id="xejson">Download result (JSON)</button><button class="btn g" id="xepdf">Download result (PDF)</button></p>'+
 '<div class="row"><label class="note" for="xerel">Release code</label><input class="xin" id="xerel" size="40" autocomplete="off" placeholder="R1.…" aria-label="Release code from the instructor"><button class="btn g" id="xeunlock">Show my result</button></div><p class="note" id="xerelmsg" role="status">'+esc(note||'')+'</p></div>'}
function xLockPaint(rec){const sum=document.getElementById('xesum');if(sum)sum.innerHTML=xLockHtml(rec);document.querySelectorAll('#xeout .xfeed').forEach(e=>{e.innerHTML=''});document.querySelectorAll('#xeout fieldset').forEach(f=>f.classList.remove('right','wrong','half'));
 const fin=document.getElementById('xefinish');if(fin)fin.disabled=true}
// wrap: start (identity first)
{const _start=xExamStart;
 xExamStart=async function(fromRec){const id=xidRead(),bad=xidCheck(id);
  if(bad.length){xidMsg('Before the exam starts, please enter '+bad.join(', ')+'.');const f=document.getElementById(!/^[A-Za-z0-9-]{3,20}$/.test(id.number)?'xesno':'xesname');if(f)f.focus();return}
  xidMsg('');try{localStorage.setItem(XID_KEY,JSON.stringify(id))}catch(e){}
  const before=XS.recs.length;await _start(fromRec);const rec=XS.recs[XS.recs.length-1];if(rec&&XS.recs.length>before){rec.student=id;rec.timer=document.getElementById('xetimeron').checked;xSave()}}}
// wrap: finish (then lock)
{const _fin=xExamFinish;
 xExamFinish=async function(timeUp){if(XE.done||!XE.items.length)return;await _fin(timeUp);const rec=XE.rec;if(rec&&!rec.released)xLockPaint(rec)}}
// wrap: review (locked until released)
{const _rev=xExamReview;
 xExamReview=async function(rec){if(rec.released){await _rev(rec);return}
  const items=XS.items[rec.code];if(!items||!rec.res)return;const out=document.getElementById('xeout');clearInterval(XE.timer);XE.done=true;XE.items=JSON.parse(JSON.stringify(items));XE.kind=rec.kind;XE.seed=+rec.code.slice(2);XE.rec=rec;
  out.innerHTML='<div id="xetimer" role="timer">Exam <code>'+esc(rec.code)+'</code> taken '+esc(new Date(rec.at).toLocaleString())+' (result locked)</div><div id="xesum"></div>'+xExamHtml();
  XE.items.forEach((it,i)=>{const fs=out.querySelector('fieldset[data-xi="'+i+'"]');xFill(it,fs,rec.ans[i]);fs.querySelectorAll('input,select,textarea,button[data-exmv],[data-xreset]').forEach(e=>{e.disabled=true})});
  const fin=document.getElementById('xefinish');if(fin)fin.disabled=true;xLockPaint(rec);document.getElementById('xesum').scrollIntoView({block:'start'})}}
document.addEventListener('click',async e=>{const t=e.target;if(!t.closest)return;const b=t.closest('#xejson,#xepdf,#xeunlock');if(!b)return;e.stopImmediatePropagation();const rec=XE.rec||XS.recs[XS.recs.length-1];if(!rec)return;
 if(b.id==='xejson'){const o=await xResultObject(rec,true);xDownload(xFileBase(rec)+'.json','application/json',JSON.stringify(o,null,1));return}
 if(b.id==='xepdf'){const o=await xResultObject(rec,true);xDownload(xFileBase(rec)+'.pdf','application/pdf',await xPdfBuild(xPdfPages(o,rec)));return}
 if(b.id==='xeunlock'){const msg=document.getElementById('xerelmsg'),v=await xVerifyRelease(document.getElementById('xerel').value,rec);
  if(!v.ok){msg.textContent=v.why;return}rec.released=true;rec.release=document.getElementById('xerel').value.replace(/\s+/g,'');xSave();xHistPaint();XE.rec=null;await xExamReview(rec);toast('Result released')}},true);
document.addEventListener('click',e=>{if(e.target&&e.target.id==='xestart')xidPaint()},true);
xidPaint();
