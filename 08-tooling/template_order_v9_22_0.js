
// ---- ordering lines: drag a line, or hold ▲ / ▼ to keep moving it ----
(function(){
 const lines=li=>[...li.parentNode.children];
 const mid=el=>{const r=el.getBoundingClientRect();return r.top+r.height/2};
 const locked=li=>{const b=li.querySelector('button[data-exmv]');return !b||b.disabled};
 function stepLi(li,dir){const p=li.parentNode;if(dir<0&&li.previousElementSibling){p.insertBefore(li,li.previousElementSibling);return true}if(dir>0&&li.nextElementSibling){p.insertBefore(li.nextElementSibling,li);return true}return false}
 function followY(li,y){let moved=false;
  for(;;){const pv=li.previousElementSibling;if(pv&&y<mid(pv)){li.parentNode.insertBefore(li,pv);moved=true}else break}
  for(;;){const nx=li.nextElementSibling;if(nx&&y>mid(nx)){li.parentNode.insertBefore(nx,li);moved=true}else break}
  return moved}
 // drag by the handle: the line follows the pointer; near the top or bottom of the window the page scrolls on its own
 document.addEventListener('pointerdown',e=>{const g=e.target.closest&&e.target.closest('.exgrip');if(!g)return;const li=g.closest('li');if(!li||locked(li))return;e.preventDefault();
  let y=e.clientY,run=true;li.classList.add('dragging');try{g.setPointerCapture(e.pointerId)}catch(_){}
  const mv=ev=>{y=ev.clientY},end=()=>{run=false;li.classList.remove('dragging');g.removeEventListener('pointermove',mv);g.removeEventListener('pointerup',end);g.removeEventListener('pointercancel',end);g.removeEventListener('lostpointercapture',end)};
  g.addEventListener('pointermove',mv);g.addEventListener('pointerup',end);g.addEventListener('pointercancel',end);g.addEventListener('lostpointercapture',end);
  const tick=()=>{if(!run)return;const h=window.innerHeight;if(y<70)window.scrollBy(0,-Math.ceil((70-y)/5));else if(y>h-70)window.scrollBy(0,Math.ceil((y-(h-70))/5));followY(li,y);requestAnimationFrame(tick)};requestAnimationFrame(tick)});
 // hold ▲ / ▼: after a short pause the line keeps moving until the button is let go (or the end is reached); the line is kept in view
 let held=null,suppress=0;
 document.addEventListener('pointerdown',e=>{const b=e.target.closest&&e.target.closest('[data-exmv]');if(!b||b.disabled)return;const li=b.closest('li'),dir=+b.dataset.exmv;let timer=null,rep=null;
  const stop=()=>{clearTimeout(timer);clearInterval(rep);document.removeEventListener('pointerup',stop,true);document.removeEventListener('pointercancel',stop,true)};
  timer=setTimeout(()=>{rep=setInterval(()=>{if(!stepLi(li,dir)){clearInterval(rep);return}suppress=Date.now();li.scrollIntoView({block:'nearest'})},110)},380);
  document.addEventListener('pointerup',stop,true);document.addEventListener('pointercancel',stop,true)},true);
 // the click that ends a hold must not move the line one more step
 document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-exmv]');if(b&&suppress&&Date.now()-suppress<400){e.stopImmediatePropagation();e.preventDefault();suppress=0}},true);
 // keyboard: on the handle, Up / Down move the line, Home / End send it to the first / last place
 document.addEventListener('keydown',e=>{const g=e.target.closest&&e.target.closest('.exgrip');if(!g)return;const li=g.closest('li');if(!li||locked(li))return;let d=0;
  if(e.key==='ArrowUp')d=-1;else if(e.key==='ArrowDown')d=1;else if(e.key==='Home'||e.key==='End'){e.preventDefault();const p=li.parentNode;if(e.key==='Home')p.insertBefore(li,p.firstElementChild);else p.appendChild(li);g.focus();li.scrollIntoView({block:'nearest'});return}else return;
  e.preventDefault();stepLi(li,d);g.focus();li.scrollIntoView({block:'nearest'})});
})();
