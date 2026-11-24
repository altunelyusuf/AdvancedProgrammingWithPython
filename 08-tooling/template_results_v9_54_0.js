// ---- 9.54.0: the exam and its results are two functions; the result opens as soon as an exam is finished ----
// The Mock exam tab only starts and takes an exam. The Exam results tab lists every attempt (kept in this browser), opens any of them with
// the score, the answers and a correction under each question, and offers the result file. An exam can be taken again without limit.
function xrBusy(){return !!(XE&&XE.items&&XE.items.length&&!XE.done)}
function xrMsg(t){const m=document.getElementById('xrmsg');if(m)m.textContent=t||''}
async function xAfterFinish(rec){const out=document.getElementById('xeout');
 if(out)out.innerHTML='<div class="xrep" id="xefinished" role="status"><h3>Exam finished</h3><p>Exam <code>'+esc(rec.code)+'</code> is marked: <b>'+rec.got+' of '+rec.pts+' points, '+rec.pct+'%</b>. Your result, with your answers and a correction under each question, is open in the <b>Exam results</b> tab.</p>'+
  '<p class="xrow"><button class="btn" id="xegores">Open my result</button><button class="btn g" id="xeretake" data-code="'+esc(rec.code)+'">Take this exam again</button><button class="btn g" id="xeother">Take another exam</button></p></div>';
 await xExamReview(rec);showTab('examresults')}
// start: go to the Mock exam tab; the student's details are optional and only go into the result file
{const _start=xExamStart;
 xExamStart=async function(fromRec){showTab('exam');const ro=document.getElementById('xrout');if(ro)ro.innerHTML='';xrMsg('');const before=XS.recs.length;await _start(fromRec);const rec=XS.recs[XS.recs.length-1];
  if(rec&&XS.recs.length>before){rec.student=xidRead();rec.timer=document.getElementById('xetimeron').checked;xSave()}}}
// finish: mark, then show the result at once in the results tab
{const _fin=xExamFinish;
 xExamFinish=async function(timeUp){if(XE.done||!XE.items.length)return;await _fin(timeUp);const rec=XE.rec;if(rec&&rec.res)await xAfterFinish(rec)}}
// review: opens in the results tab; not while an exam is open on the Mock exam tab
{const _rev=xExamReview;
 xExamReview=async function(rec){xrMsg('');if(xrBusy()){xrMsg('An exam is still open on the Mock exam tab. Finish it there, then open a result.');return}
  await _rev(rec);XE.rec=rec;const sm=document.getElementById('xesum');
  if(sm)sm.insertAdjacentHTML('beforeend','<p class="xrow"><button class="btn g" id="xejson">Download result (JSON)</button><button class="btn g" id="xepdf">Download result (PDF)</button></p>');
  const fb=document.querySelector('#xrout #xefinish');if(fb)fb.remove()}}
// the list says how many attempts and how they went
{const _hp=xHistPaint;
 xHistPaint=function(){_hp();const el=document.getElementById('xerstat');if(!el)return;const d=XS.recs.filter(r=>r.status==='done');
  el.innerHTML=d.length?'<p class="note" role="status">Finished attempts: <b>'+d.length+'</b>. Best result: <b>'+Math.max(...d.map(r=>r.pct))+'%</b>. Latest result: <b>'+d[d.length-1].pct+'%</b>.</p>':''}}
document.addEventListener('click',async e=>{const t=e.target;if(!t.closest)return;
 const b=t.closest('#xejson,#xepdf');
 if(b){e.stopImmediatePropagation();const rec=XE.rec||XS.recs[XS.recs.length-1];if(!rec)return;const id=xidRead();
  if(id.number||id.name||id.surname){rec.student=id;try{localStorage.setItem(XID_KEY,JSON.stringify(id))}catch(_){}xSave()}
  if(typeof audit==='function')audit(b.id==='xejson'?'result_json_saved':'result_pdf_saved',{exam:rec.code});
  if(b.id==='xejson'){const o=await xResultObject(rec,true);xDownload(xFileBase(rec)+'.json','application/json',JSON.stringify(o,null,1));return}
  const o=await xResultObject(rec,true);xDownload(xFileBase(rec)+'.pdf','application/pdf',await xPdfBuild(xPdfPages(o,rec)));return}
 const g=t.closest('#xegores,#xeretake,#xeother');if(!g)return;e.stopImmediatePropagation();
 if(g.id==='xegores'){showTab('examresults');return}
 document.getElementById('xecode').value=g.id==='xeretake'?g.dataset.code:'';xExamStart()},true);
xidPaint();
