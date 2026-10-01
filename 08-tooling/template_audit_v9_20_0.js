
// ---- audit log (zipped), clear option, code patterns in the Playground list ----
const AUD_KEY='course-page-audit:'+D.title;let AUD=[];try{AUD=JSON.parse(localStorage.getItem(AUD_KEY)||'[]')||[]}catch(e){AUD=[]}
function audSave(){AUD=AUD.slice(-500);try{localStorage.setItem(AUD_KEY,JSON.stringify(AUD))}catch(e){}}
function audit(ev,detail){const s=xidLoad();AUD.push({at:new Date().toISOString(),event:ev,student_number:s.number||'',detail:detail||{}});audSave()}
audit('page_opened',{page:'chapter '+XEX_CH,page_version:D._version||''});
// zip writer (stored, no compression): enough for a few small text files
const ZCRC=(()=>{const t=new Uint32Array(256);for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=c&1?0xEDB88320^(c>>>1):c>>>1;t[n]=c>>>0}return t})();
function zCrc(b){let c=0xFFFFFFFF;for(let i=0;i<b.length;i++)c=ZCRC[(c^b[i])&255]^(c>>>8);return (c^0xFFFFFFFF)>>>0}
function zipStore(files){const enc=new TextEncoder(),parts=[],cen=[];let off=0;const d=new Date(),dt=((d.getFullYear()-1980)<<9)|((d.getMonth()+1)<<5)|d.getDate(),tm=(d.getHours()<<11)|(d.getMinutes()<<5)|(d.getSeconds()>>1);
 const u16=(v,a)=>{a.push(v&255,(v>>8)&255)},u32=(v,a)=>{a.push(v&255,(v>>8)&255,(v>>16)&255,(v>>>24)&255)};
 files.forEach(f=>{const name=enc.encode(f.name),data=typeof f.data==='string'?enc.encode(f.data):f.data,crc=zCrc(data),h=[];
  u32(0x04034b50,h);u16(20,h);u16(0x0800,h);u16(0,h);u16(tm,h);u16(dt,h);u32(crc,h);u32(data.length,h);u32(data.length,h);u16(name.length,h);u16(0,h);
  parts.push(new Uint8Array(h),name,data);const c=[];u32(0x02014b50,c);u16(20,c);u16(20,c);u16(0x0800,c);u16(0,c);u16(tm,c);u16(dt,c);u32(crc,c);u32(data.length,c);u32(data.length,c);u16(name.length,c);u16(0,c);u16(0,c);u16(0,c);u16(0,c);u32(0,c);u32(off,c);
  cen.push(new Uint8Array(c),name);off+=h.length+name.length+data.length});
 let cl=0;cen.forEach(x=>cl+=x.length);const e=[];u32(0x06054b50,e);u16(0,e);u16(0,e);u16(files.length,e);u16(files.length,e);u32(cl,e);u32(off,e);u16(0,e);
 const all=parts.concat(cen,[new Uint8Array(e)]);let n=0;all.forEach(x=>n+=x.length);const out=new Uint8Array(n);let p=0;all.forEach(x=>{out.set(x,p);p+=x.length});return out}
const audCsv=()=>'time,event,student_number,detail\n'+AUD.map(a=>[a.at,a.event,a.student_number,JSON.stringify(a.detail)].map(v=>'"'+String(v).replace(/"/g,'""')+'"').join(',')).join('\n')+'\n';
async function audZip(){const s=xidLoad(),files=[],log=JSON.stringify({format:'sen0414-audit-log',format_version:1,course:'SEN0414',chapter:D.chapter,chapter_title:D.title,student:{number:s.number||'',name:s.name||'',surname:s.surname||''},exported:new Date().toISOString(),events:AUD},null,1);
 files.push({name:'audit_log.json',data:log},{name:'audit_log.csv',data:'﻿'+audCsv()});
 for(const r of XS.recs){if(r.status!=='done')continue;try{const o=await xResultObject(r,true);files.push({name:'results/'+xFileBase(r)+'.json',data:JSON.stringify(o,null,1)})}catch(e){}}
 const sha=await xSha256(log);files.unshift({name:'README.txt',data:'SEN0414 chapter '+D.chapter+' - audit log of this browser\nExported: '+new Date().toISOString()+'\n\naudit_log.json / audit_log.csv: what was done on this page (page opened, exams started and finished, result files saved, release codes tried, data cleared). No answers and no release codes are written into the log.\nresults/: the result file of each finished exam, exactly as it was saved for the instructor.\nSHA-256 of audit_log.json: '+sha+'\nThe log shows what this browser recorded; it is evidence for an audit, not proof against someone who edits files.\n'});
 audit('audit_log_downloaded',{files:files.length+1});return zipStore(files)}
const audName=()=>{const s=xidLoad(),d=new Date(),p=n=>String(n).padStart(2,'0');return 'sen0414-ch'+XEX_CH+'-audit-'+String(s.number||'student').replace(/[^A-Za-z0-9-]/g,'')+'-'+d.getFullYear()+p(d.getMonth()+1)+p(d.getDate())+'-'+p(d.getHours())+p(d.getMinutes())+'.zip'};
// hooks: what is logged
{const _s=xExamStart;xExamStart=async function(fr){const n=XS.recs.length;await _s(fr);if(XS.recs.length>n){const r=XS.recs[XS.recs.length-1];audit('exam_started',{exam:r.code,kind:r.kind,points:r.pts,timer:!!r.timer})}}}
{const _f=xExamFinish;xExamFinish=async function(t){const was=XE.done;await _f(t);if(!was&&XE.done&&XE.rec){const r=XE.rec;audit('exam_finished',{exam:r.code,time_up:t===true,answered:(r.ans||[]).filter(xIsAns).length,of:(r.ans||[]).length})}}}
{const _v=xVerifyRelease;xVerifyRelease=async function(c,rec){const r=await _v(c,rec);audit(r.ok?'release_accepted':'release_refused',{exam:rec.code,reason:r.ok?'':r.why});return r}}
document.addEventListener('click',e=>{const b=e.target&&e.target.closest&&e.target.closest('#xejson,#xepdf');if(b){const r=XE.rec||XS.recs[XS.recs.length-1];if(r)audit(b.id==='xejson'?'result_json_saved':'result_pdf_saved',{exam:r.code})}},true);
// the clear option, asked first, with the audit log offered before anything is removed
function xClearAsk(){const box=document.getElementById('xeclearbox');if(!box)return;const n=XS.recs.length;
 box.innerHTML='<div class="xrep" role="alertdialog" aria-label="Clear my exam data"><h3>Clear my exam data?</h3><p>This removes <b>'+n+' exam'+(n===1?'':'s')+'</b> with their answers, and your saved student number, name and surname, from this browser. It cannot be undone. The audit log stays (and records that you cleared), unless you tick the box. Save a copy first if you still need it.</p><p class="xrow"><button class="btn g" id="xeclearzip">Download audit log (zip) first</button><label class="note"><input type="checkbox" id="xeclearaud"> also clear the audit log</label></p><p class="xrow"><button class="btn" id="xeclearyes">Yes, clear</button><button class="btn g" id="xeclearno">Keep my data</button></p></div>';
 box.scrollIntoView({block:'nearest'});const y=document.getElementById('xeclearno');if(y)y.focus()}
document.addEventListener('click',async e=>{const t=e.target;if(!t.closest)return;const b=t.closest('#xeauditzip,#xeclearzip,#xeclearyes,#xeclearno');if(!b)return;e.stopImmediatePropagation();
 if(b.id==='xeauditzip'||b.id==='xeclearzip'){xDownload(audName(),'application/zip',await audZip());return}
 if(b.id==='xeclearno'){document.getElementById('xeclearbox').innerHTML='';return}
 if(b.id==='xeclearyes'){const n=XS.recs.length,both=document.getElementById('xeclearaud').checked;audit('data_cleared',{exams:n,audit_cleared:both});
  clearInterval(XE.timer);XS.recs=[];XS.items={};xSave();xHistPaint();XE.items=[];XE.rec=null;XE.done=false;try{localStorage.removeItem(XID_KEY)}catch(_){}
  ['xesno','xesname','xessur','xecode'].forEach(i=>{const f=document.getElementById(i);if(f)f.value=''});const o=document.getElementById('xeout');if(o)o.innerHTML='';
  if(both){AUD=[];audSave()}document.getElementById('xeclearbox').innerHTML='<p class="note" role="status">Cleared: '+n+' exam'+(n===1?'':'s')+' and your details'+(both?', and the audit log':'')+'.</p>'}},true);
// the Playground has one list: this chapter's examples and the code patterns, all of which run
(function(){const s=document.getElementById('pex');if(!s)return;const ex=[...s.querySelectorAll('option')].slice(1);
 s.innerHTML='<option value="first">'+esc(D.course.playground.label)+'</option><optgroup label="Examples from this chapter">'+ex.map(o=>o.outerHTML).join('')+'</optgroup><optgroup label="Code patterns (each one runs as it is)">'+ED_TPL.map((t,i)=>'<option value="tpl:'+i+'">'+esc(t[0])+'</option>').join('')+'</optgroup>'})();

// concept names used by a result's questions, so the instructor's desk can show them without this page
function xLabels(items,ans){const ids=new Set();items.forEach((it,i)=>{if(it.concept)ids.add(it.concept);if(it.owner)ids.add(it.owner);(it.rows||[]).forEach(r=>ids.add(r.id));const a=ans[i];if(a&&typeof a==='object'&&!Array.isArray(a)){if(a.s)ids.add(a.s);Object.keys(a).forEach(k=>{ids.add(k);if(typeof a[k]==='string')ids.add(a[k])})}});const o={};ids.forEach(id=>{if(byId[id])o[id]=byId[id].label});return o}
