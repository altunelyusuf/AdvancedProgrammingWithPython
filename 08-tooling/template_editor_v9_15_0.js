// ---------- 9.15.0: code editor, tips, agent list width, card closing, navigation trail ----------
// Placeholders filled by template_patch_v9_15_0.py: __PYDOC__ (python_docs_v1_0_0.json)
const PYDOC=__PYDOC__;
const ED_KW=new Set(Object.keys(PYDOC.keywords)),ED_BI=new Set(Object.keys(PYDOC.builtins));
const ED_CONST=new Set(['True','False','None']);
const EDK='course-page-editor',ED_FONTS={mono:'"Courier New",Courier,monospace',code:'Consolas,Menlo,"DejaVu Sans Mono",monospace',sys:'ui-monospace,SFMono-Regular,monospace'};
let EDS={fs:14,ff:'mono',ln:true};
try{Object.assign(EDS,JSON.parse(localStorage.getItem(EDK)||'{}'))}catch(e){}
EDS.fs=Math.max(11,Math.min(24,+EDS.fs||14));if(!ED_FONTS[EDS.ff])EDS.ff='mono';
function edApply(){const r=document.documentElement.style;r.setProperty('--edfs',EDS.fs);r.setProperty('--edff',ED_FONTS[EDS.ff]);try{localStorage.setItem(EDK,JSON.stringify(EDS))}catch(e){}
 document.querySelectorAll('.ed').forEach(edGutter);document.querySelectorAll('.edtools [data-edfs]').forEach(x=>x.textContent=EDS.fs)}
// ---- the highlighter ----
const ED_RE=/(#[^\n]*)|((?:[rRbBfFuU]{1,2})?(?:"""[\s\S]*?(?:"""|$)|'''[\s\S]*?(?:'''|$)|"(?:\\.|[^"\\\n])*(?:"|$)|'(?:\\.|[^'\\\n])*(?:'|$)))|(\b\d[\d_]*(?:\.\d*)?(?:[eE][+-]?\d+)?\b)|(@[A-Za-z_][\w.]*)|([A-Za-z_]\w*)|([\s\S])/g;
function pyHL(src){let out='',prev='',m;ED_RE.lastIndex=0;const E=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
 while((m=ED_RE.exec(src))){const t=m[0];
  if(m[1]){out+='<i class="hc">'+E(t)+'</i>'}
  else if(m[2]){out+='<i class="hs">'+E(t)+'</i>'}
  else if(m[3]){out+='<i class="hn">'+E(t)+'</i>'}
  else if(m[4]){out+='<i class="hd">'+E(t)+'</i>'}
  else if(m[5]){let c='';if(prev==='def'||prev==='class')c='hf';else if(ED_CONST.has(t))c='hn';else if(ED_KW.has(t))c='hk';else if(t==='self'||t==='cls')c='hv';else if(ED_BI.has(t))c='hb';
   out+=c?'<i class="'+c+'">'+t+'</i>':t;prev=t;continue}
  else out+=E(t);
  if(!/^\s+$/.test(t))prev=''}
 return out}
// ---- editors ----
const ED_HELP=[['Tab / Shift+Tab','indent / dedent (the selected lines, or the current one)'],['Enter','new line at the same indent, one deeper after a colon'],['Backspace','removes a whole indent step'],['( [ { " \'','closed for you; typing the closing one moves past it'],['Ctrl+/','comment or uncomment the lines'],['Ctrl+Space','suggestions (they also appear as you type)'],['Ctrl+Enter','run (Playground)'],['Esc then Tab','leave the box with the keyboard']];
const ED_TPL=[['For loop over numbers','for i in range($0):\n    print(i)'],['For loop over a list','for item in $0:\n    print(item)'],['While loop','while $0:\n    pass'],['If, elif, else','if $0:\n    pass\nelif False:\n    pass\nelse:\n    pass'],['Function with a docstring','def name($0):\n    """What it does."""\n    return None'],['Class with __init__','class Name:\n    def __init__(self$0):\n        pass'],['Try and except','try:\n    $0\nexcept ValueError as e:\n    print("Problem:", e)'],['Read a file line by line','with open("$0data.txt") as f:\n    for line in f:\n        print(line.rstrip())'],['List comprehension','result = [x for x in $0 if x]'],['Dictionary comprehension','result = {k: v for k, v in $0.items()}'],['Count words with a dictionary','counts = {}\nfor word in $0.split():\n    counts[word] = counts.get(word, 0) + 1\nprint(counts)'],['Ask for a number','n = int(input("$0Enter a number: "))'],['Print with an f-string','print(f"{$0}")'],['Sort with a key','result = sorted($0, key=lambda x: x)'],['Check with assert','assert $0, "message"'],['Main guard','if __name__ == "__main__":\n    main()$0']];
const EDVAL=Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value');
function edGutter(ed){const ta=ed.querySelector('textarea.edta');if(!ta)return;const on=EDS.ln&&ed.dataset.full==='1';ed.classList.toggle('noln',!on);
 const n=(EDVAL.get.call(ta).match(/\n/g)||[]).length+1;const g=ed.querySelector('.edgut');if(g){let s='';for(let i=1;i<=n;i++)s+=i+'\n';g.firstChild.textContent=s}
 ed.style.setProperty('--edgw',on?(String(n).length+1.6)+'ch':'0px')}
function edPaint(ta){const ed=ta.closest('.ed');if(!ed)return;ed.querySelector('.edhl').innerHTML=pyHL(EDVAL.get.call(ta))+'\n';edGutter(ed);edSync(ta)}
function edSync(ta){const ed=ta.closest('.ed');if(!ed)return;const h=ed.querySelector('.edhl'),g=ed.querySelector('.edgut');h.scrollTop=ta.scrollTop;h.scrollLeft=ta.scrollLeft;if(g)g.scrollTop=ta.scrollTop}
function edEnhance(ta){if(ta.classList.contains('edta')||ta.closest('.ed'))return;const full=ta.id==='pcode'||ta.id==='clcode'||ta.classList.contains('mycode');
 const ed=document.createElement('div');ed.className='ed';ed.dataset.full=full?'1':'0';
 ed.innerHTML=(full?'<div class="edtools" role="toolbar" aria-label="Editor tools"><select class="edsel" data-edtpl aria-label="Insert a code template"><option value="">Templates</option>'+ED_TPL.map((t,i)=>'<option value="'+i+'">'+esc(t[0])+'</option>').join('')+'</select>'
  +'<span class="edgrp"><button type="button" class="edb" data-edact="dedent" aria-label="Dedent the selected lines" data-tip="Dedent (Shift+Tab)">⇤</button><button type="button" class="edb" data-edact="indent" aria-label="Indent the selected lines" data-tip="Indent (Tab)">⇥</button><button type="button" class="edb" data-edact="comment" aria-label="Comment or uncomment the selected lines" data-tip="Comment (Ctrl+/)">#</button></span>'
  +'<span class="edgrp"><button type="button" class="edb" data-edact="smaller" aria-label="Smaller code text" data-tip="Smaller code text">A−</button><span class="edfs" aria-hidden="true"><span data-edfs>'+EDS.fs+'</span> px</span><button type="button" class="edb" data-edact="larger" aria-label="Larger code text" data-tip="Larger code text">A+</button></span>'
  +'<select class="edsel" data-edff aria-label="Code font"><option value="mono">Courier New</option><option value="code">Consolas / Menlo</option><option value="sys">System monospace</option></select>'
  +'<label class="edln"><input type="checkbox" data-edln> Line numbers</label><button type="button" class="edb" data-edact="help" aria-expanded="false" aria-label="Editor shortcuts" data-tip="Editor shortcuts">?</button></div>'
  +'<div class="edhelp" hidden><table>'+ED_HELP.map(r=>'<tr><th scope="row">'+esc(r[0])+'</th><td>'+esc(r[1])+'</td></tr>').join('')+'</table></div>':'')
  +'<div class="edbox"><pre class="edhl" aria-hidden="true"></pre><div class="edgut" aria-hidden="true"><div></div></div></div>';
 if(full)ed.classList.add('hastools');
 ta.parentNode.insertBefore(ed,ta);ed.querySelector('.edbox').appendChild(ta);
 ta.classList.add('edta');ta.setAttribute('wrap','off');ta.setAttribute('spellcheck','false');ta.setAttribute('autocapitalize','off');ta.setAttribute('autocomplete','off');ta.setAttribute('autocorrect','off');
 if(!ta.readOnly)ta.setAttribute('aria-autocomplete','list');
 Object.defineProperty(ta,'value',{get(){return EDVAL.get.call(ta)},set(v){EDVAL.set.call(ta,v);edPaint(ta)},configurable:true});
 if(full){const ff=ed.querySelector('[data-edff]');ff.value=EDS.ff;ed.querySelector('[data-edln]').checked=EDS.ln}
 edPaint(ta);edApply()}
function edScan(root){(root||document).querySelectorAll('textarea.code:not(#sqtext):not(.edta),textarea.mycode:not(.edta)').forEach(edEnhance)}
edScan();
new MutationObserver(m=>{if(m.some(x=>x.addedNodes.length))edScan()}).observe(document.body,{childList:true,subtree:true});
// ---- editing helpers ----
function edIns(ta,text){ta._prog=true;ta.focus();let ok=false;try{ok=document.execCommand('insertText',false,text)}catch(_){}
 if(!ok){ta.setRangeText(text,ta.selectionStart,ta.selectionEnd,'end');ta.dispatchEvent(new InputEvent('input',{bubbles:true,inputType:'insertText'}))}ta._prog=false}
function edRepl(ta,a,b,text,s0,s1){ta.setSelectionRange(a,b);edIns(ta,text);if(s0!=null)ta.setSelectionRange(s0,s1==null?s0:s1)}
function edLines(ta){const v=ta.value,s=ta.selectionStart;let e=ta.selectionEnd;if(e>s&&v[e-1]==='\n')e--;const a=v.lastIndexOf('\n',s-1)+1;let b=v.indexOf('\n',e);if(b<0)b=v.length;return {a,b,text:v.slice(a,b),s,e:ta.selectionEnd}}
function edIndent(ta,dir){const v=ta.value,L=edLines(ta),multi=L.s!==L.e;
 if(dir>0&&!multi){const col=L.s-L.a,n=4-col%4;edIns(ta,' '.repeat(n));return}
 const lines=L.text.split('\n');let d0=0,dLast=0;
 const out=lines.map((ln,i)=>{if(dir>0){const r=ln.trim()?'    '+ln:ln;if(i===0)d0=r.length-ln.length;dLast=r.length-ln.length;return r}
  const m=ln.match(/^( {1,4}|\t)/);const r=m?ln.slice(m[0].length):ln;if(i===0)d0=r.length-ln.length;dLast=r.length-ln.length;return r}).join('\n');
 const s2=Math.max(L.a,L.s+d0),e2=L.e+lines.reduce((t,ln,i)=>t+(dir>0?(ln.trim()?4:0):-(ln.match(/^( {1,4}|\t)/)||[''])[0].length),0);
 edRepl(ta,L.a,L.b,out,multi?L.a:s2,multi?L.a+out.length:s2)}
function edComment(ta){const L=edLines(ta),lines=L.text.split('\n'),non=lines.filter(x=>x.trim());const all=non.length&&non.every(x=>/^\s*#/.test(x));
 const ind=Math.min(...non.map(x=>x.match(/^ */)[0].length),1e9);
 const out=lines.map(x=>{if(!x.trim())return x;if(all)return x.replace(/^(\s*)# ?/,'$1');return x.slice(0,ind)+'# '+x.slice(ind)}).join('\n');
 const one=L.s===L.e;edRepl(ta,L.a,L.b,out,one?Math.min(L.a+out.length,L.s+(out.length-L.text.length)):L.a,one?null:L.a+out.length)}
function edTemplate(ta,i){const t=ED_TPL[i];if(!t)return;const v=ta.value,s=ta.selectionStart,a=v.lastIndexOf('\n',s-1)+1,before=v.slice(a,s),ind=(before.match(/^ */)[0]);
 let body=t[1].split('\n').map((l,k)=>k?ind+l:l).join('\n');const pos=body.indexOf('$0');body=body.replace('$0','');let pre='';if(before.trim()){pre='\n'+ind}
 edIns(ta,pre+body);if(pos>=0){const start=ta.selectionStart-body.length+pos;ta.setSelectionRange(start,start)}ta.focus()}
// ---- suggestions ----
let EDAC={ta:null,items:[],i:0,from:0};
const edac=document.createElement('div');edac.id='edac';edac.setAttribute('role','listbox');edac.setAttribute('aria-label','Suggestions');edac.hidden=true;document.body.appendChild(edac);
const edlive=document.createElement('div');edlive.id='edlive';edlive.className='edsr';edlive.setAttribute('role','status');document.body.appendChild(edlive);
function edMetrics(ta){const cs=getComputedStyle(ta),c=edMetrics.c||(edMetrics.c=document.createElement('canvas').getContext('2d'));c.font=cs.fontSize+' '+cs.fontFamily;
 return {cw:c.measureText('M').width,lh:parseFloat(cs.lineHeight)||parseFloat(cs.fontSize)*1.5,pl:parseFloat(cs.paddingLeft),pt:parseFloat(cs.paddingTop)}}
function edCands(ta,manual){const v=ta.value,p=ta.selectionStart;if(ta.selectionEnd!==p)return null;const mm=v.slice(0,p).match(/([A-Za-z_]\w*)?$/),pre=mm[1]||'',from=p-pre.length;
 const dot=v[from-1]==='.'&&!/\d$/.test(v.slice(Math.max(0,from-2),from-1));
 const lineStart=v.lastIndexOf('\n',from-1)+1;if(/^\s*#/.test(v.slice(lineStart,from)))return null;
 if(pre.length<(manual?(dot?0:1):(dot?1:2)))return null;
 const lo=pre.toLowerCase(),seen=new Set(),out=[];const add=(n,k,d)=>{if(seen.has(n)||n===pre)return;if(!n.toLowerCase().startsWith(lo))return;seen.add(n);out.push({n,k,d})};
 if(dot){for(const key of Object.keys(PYDOC.methods)){const n=key.split('.')[1];add(n,'method',key.split('.')[0]+' - '+PYDOC.methods[key])}}
 else{Object.keys(PYDOC.keywords).forEach(k=>add(k,'keyword',PYDOC.keywords[k]));Object.keys(PYDOC.builtins).forEach(k=>add(k,'built-in',PYDOC.builtins[k]));
  (v.match(/[A-Za-z_]\w{1,}/g)||[]).forEach(w=>{if(w!==pre)add(w,'in your code','')})}
 out.sort((a,b)=>(a.k==='in your code')-(b.k==='in your code')||a.n.length-b.n.length||a.n.localeCompare(b.n));
 return out.length?{items:out.slice(0,8),from}:null}
function edAcShow(ta,manual){const r=edCands(ta,manual);if(!r){edAcHide();return}
 EDAC={ta,items:r.items,i:0,from:r.from};edacDraw();const m=edMetrics(ta),bb=ta.getBoundingClientRect(),v=ta.value.slice(0,ta.selectionStart).split('\n');
 const x=bb.left+m.pl+v[v.length-1].length*m.cw-ta.scrollLeft,y=bb.top+m.pt+v.length*m.lh-ta.scrollTop;edac.hidden=false;
 const h=edac.offsetHeight;edac.style.left=Math.max(4,Math.min(x,innerWidth-edac.offsetWidth-8))+'px';edac.style.top=(y+h>innerHeight-8?Math.max(4,y-m.lh-h):y)+'px';
 ta.setAttribute('aria-controls','edac');edlive.textContent=r.items.length+' suggestions. Use the arrow keys, Enter to accept, Escape to close.'}
function edacDraw(){edac.innerHTML=EDAC.items.map((c,i)=>'<div role="option" id="edac-'+i+'" data-i="'+i+'" aria-selected="'+(i===EDAC.i)+'"><b>'+esc(c.n)+'</b><small>'+esc(c.k)+(c.d?' · '+esc(c.d.length>70?c.d.slice(0,69)+'…':c.d):'')+'</small></div>').join('');
 if(EDAC.ta)EDAC.ta.setAttribute('aria-activedescendant','edac-'+EDAC.i)}
function edAcHide(){if(edac.hidden)return;edac.hidden=true;if(EDAC.ta){EDAC.ta.removeAttribute('aria-activedescendant');EDAC.ta.removeAttribute('aria-controls')}EDAC.items=[]}
function edAcAccept(){const c=EDAC.items[EDAC.i],ta=EDAC.ta;if(!c||!ta)return;const from=EDAC.from;edAcHide();edRepl(ta,from,ta.selectionStart,c.n)}
edac.addEventListener('mousedown',e=>{const o=e.target.closest('[data-i]');if(!o)return;e.preventDefault();EDAC.i=+o.dataset.i;edAcAccept()});
// ---- keys ----
const ED_PAIR={'(':')','[':']','{':'}'},ED_CLOSE=new Set([')',']','}']);
document.addEventListener('keydown',e=>{const ta=e.target;if(!ta.classList||!ta.classList.contains('edta')||ta.readOnly||e.isComposing)return;const k=e.key,mod=e.ctrlKey||e.metaKey;
 if(!edac.hidden&&EDAC.ta===ta){if(k==='ArrowDown'||k==='ArrowUp'){e.preventDefault();EDAC.i=(EDAC.i+(k==='ArrowDown'?1:EDAC.items.length-1))%EDAC.items.length;edacDraw();return}
  if(k==='Enter'||k==='Tab'){e.preventDefault();edAcAccept();return}if(k==='Escape'){e.preventDefault();e.stopPropagation();edAcHide();return}
  if(k==='ArrowLeft'||k==='ArrowRight'||k==='Home'||k==='End'||k==='PageUp'||k==='PageDown')edAcHide()}
 if(k==='Escape'){ta._free=true;return}
 if(k==='Tab'&&ta._free&&!e.shiftKey){ta._free=false;return}ta._free=false;
 if(mod&&k===' '){e.preventDefault();edAcShow(ta,true);return}
 if(mod&&k==='Enter'&&ta.id==='pcode'){e.preventDefault();const b=document.getElementById('prun');if(b)b.click();return}
 if(mod&&k==='/'){e.preventDefault();edComment(ta);return}
 if(mod||e.altKey)return;
 const v=ta.value,s=ta.selectionStart,en=ta.selectionEnd;
 if(k==='Tab'){e.preventDefault();edIndent(ta,e.shiftKey?-1:1);return}
 if(k==='Enter'&&!e.shiftKey){e.preventDefault();const a=v.lastIndexOf('\n',s-1)+1,line=v.slice(a,s),ind=line.match(/^ */)[0],code=line.replace(/#.*$/,'').trimEnd();
  const pv=v[s-1],nx=v[s];
  if(s===en&&ED_PAIR[pv]&&ED_PAIR[pv]===nx){edIns(ta,'\n'+ind+'    \n'+ind);const p=s+1+ind.length+4;ta.setSelectionRange(p,p);return}
  edIns(ta,'\n'+ind+(code.endsWith(':')?'    ':''));return}
 if(k==='Backspace'&&s===en&&s>0){const a=v.lastIndexOf('\n',s-1)+1,line=v.slice(a,s);
  if(line.length&&/^ +$/.test(line)){e.preventDefault();const n=line.length%4||4;edRepl(ta,s-n,s,'');return}
  const pv=v[s-1],nx=v[s];if((ED_PAIR[pv]&&ED_PAIR[pv]===nx)||((pv==='"'||pv==="'")&&nx===pv)){e.preventDefault();edRepl(ta,s-1,s+1,'');return}}
 if(k.length===1){
  if(ED_CLOSE.has(k)||k==='"'||k==="'"){if(s===en&&v[s]===k){e.preventDefault();ta.setSelectionRange(s+1,s+1);return}}
  if(ED_PAIR[k]||k==='"'||k==="'"){const cl=ED_PAIR[k]||k;
   if(s!==en){e.preventDefault();const sel=v.slice(s,en);edIns(ta,k+sel+cl);ta.setSelectionRange(s+1,s+1+sel.length);return}
   const nx=v[s],pv=v[s-1]||'';const okNext=!nx||/[\s)\]}:;,.]/.test(nx);
   if(!okNext)return;if((k==='"'||k==="'")&&(pv===k||(/\w/.test(pv)&&!(/[rRbBfFuU]/.test(pv)&&!/\w/.test(v[s-2]||'')))))return;
   e.preventDefault();edIns(ta,k+cl);ta.setSelectionRange(s+1,s+1);return}}
},true);
document.addEventListener('input',e=>{const ta=e.target;if(!ta.classList||!ta.classList.contains('edta'))return;edPaint(ta);edTipHide();
 if(ta.readOnly||ta._prog)return;const t=e.inputType||'';if(t.indexOf('insert')===0&&t!=='insertFromPaste'&&t!=='insertLineBreak'&&/[\w.]$/.test(ta.value.slice(0,ta.selectionStart)))edAcShow(ta,false);else edAcHide()},true);
document.addEventListener('scroll',e=>{const ta=e.target;if(ta.classList&&ta.classList.contains('edta'))edSync(ta)},true);
document.addEventListener('focusout',e=>{if(e.target.classList&&e.target.classList.contains('edta')){edAcHide();e.target._free=false}},true);
document.addEventListener('mousedown',e=>{if(!e.target.closest('#edac'))edAcHide()},true);
// ---- toolbar ----
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-edact]');if(!b)return;const ed=b.closest('.ed'),ta=ed.querySelector('textarea.edta'),a=b.dataset.edact;
 if(a==='help'){const h=ed.querySelector('.edhelp'),on=h.hidden;h.hidden=!on;b.setAttribute('aria-expanded',on);return}
 if(a==='smaller'||a==='larger'){EDS.fs=Math.max(11,Math.min(24,EDS.fs+(a==='larger'?1:-1)));edApply();setTimeout(fitViews,30);return}
 ta.focus();if(a==='indent')edIndent(ta,1);if(a==='dedent')edIndent(ta,-1);if(a==='comment')edComment(ta)});
document.addEventListener('change',e=>{const t=e.target;if(t.matches&&t.matches('[data-edtpl]')){const ta=t.closest('.ed').querySelector('textarea.edta');const i=+t.value;t.value='';if(!isNaN(i)&&t.value!==undefined)edTemplate(ta,i)}
 if(t.matches&&t.matches('[data-edff]')){EDS.ff=t.value;edApply();setTimeout(fitViews,30)}
 if(t.matches&&t.matches('[data-edln]')){EDS.ln=t.checked;document.querySelectorAll('[data-edln]').forEach(x=>x.checked=EDS.ln);edApply()}});
// ---- hover help ----
function edWordAt(line,col){if(col<0||col>line.length)return null;const re=/[A-Za-z_]\w*/g;let m;while((m=re.exec(line))){if(col>=m.index&&col<=m.index+m[0].length)return {w:m[0],i:m.index}}return null}
function edDoc(w,line,i){const dot=line[i-1]==='.';
 if(dot){const hits=Object.keys(PYDOC.methods).filter(k=>k.split('.')[1]===w);if(!hits.length)return null;return hits.slice(0,3).map(k=>k.split('.')[0]+'.'+PYDOC.methods[k]).join('\n')}
 if(PYDOC.keywords[w])return PYDOC.keywords[w];if(PYDOC.builtins[w])return PYDOC.builtins[w];return null}
let EDTIP='';function edTipHide(){if(EDTIP){EDTIP='';tip.hidden=true}}
document.addEventListener('mousemove',e=>{const ta=e.target;if(!ta.classList||!ta.classList.contains('edta'))return;const m=edMetrics(ta),bb=ta.getBoundingClientRect();
 const x=e.clientX-bb.left-m.pl+ta.scrollLeft,y=e.clientY-bb.top-m.pt+ta.scrollTop;if(x<0||y<0){edTipHide();return}
 const row=Math.floor(y/m.lh),col=Math.floor(x/m.cw),line=ta.value.split('\n')[row];if(line==null){edTipHide();return}
 const w=edWordAt(line,col);const d=w&&edDoc(w.w,line,w.i);if(!d){edTipHide();return}
 if(EDTIP!==d){EDTIP=d;tip.textContent=d;tip.hidden=false}});
document.addEventListener('mouseleave',e=>{if(e.target.classList&&e.target.classList.contains('edta'))edTipHide()},true);
// ---- tips on the elements that carry one (mouse and keyboard) ----
document.addEventListener('focusin',e=>{const d=e.target.closest&&e.target.closest('[data-tip]');if(!d)return;const r=d.getBoundingClientRect();tip.textContent=d.dataset.tip;tip.hidden=false;tip.style.left=Math.max(4,Math.min(r.left,innerWidth-tip.offsetWidth-8))+'px';tip.style.top=(r.bottom+6)+'px'});
document.addEventListener('focusout',e=>{if(e.target.closest&&e.target.closest('[data-tip]'))tip.hidden=true});
// ---- the agent list: adjustable width ----
const RSK='course-page-roster',RS_MIN=56,RS_MAX=360,RS_DEF=192;let RSW=RS_DEF;try{RSW=+localStorage.getItem(RSK)||RS_DEF}catch(e){}
function rosterSet(px,save){RSW=Math.max(RS_MIN,Math.min(RS_MAX,Math.round(px)));const v=document.querySelector('.agentsview');if(!v)return;v.style.setProperty('--rw',RSW+'px');v.classList.toggle('icons',RSW<110);
 const s=v.querySelector('.rsplit');if(s)s.setAttribute('aria-valuenow',RSW);if(save)try{localStorage.setItem(RSK,RSW)}catch(e){}}
rosterSet(RSW);
(function(){const s=document.querySelector('.rsplit');if(!s)return;let drag=null;
 s.addEventListener('pointerdown',e=>{drag={x:e.clientX,w:RSW};s.setPointerCapture(e.pointerId);e.preventDefault()});
 s.addEventListener('pointermove',e=>{if(drag)rosterSet(drag.w+e.clientX-drag.x)});
 s.addEventListener('pointerup',()=>{if(drag){drag=null;rosterSet(RSW,true)}});s.addEventListener('pointercancel',()=>{drag=null});
 s.addEventListener('keydown',e=>{const k=e.key;let w=null;if(k==='ArrowLeft')w=RSW-16;else if(k==='ArrowRight')w=RSW+16;else if(k==='Home')w=RS_MIN;else if(k==='End')w=RS_DEF;if(w!=null){e.preventDefault();rosterSet(w,true)}});
 s.addEventListener('dblclick',()=>rosterSet(RSW<110?RS_DEF:RS_MIN,true))})();
// ---- the right-hand card closes when the main area changes context ----
(function(){const cur=()=>{const p=document.querySelector('#panes [data-pane]:not([hidden])');return p?p.dataset.pane:''};
 const st=showTab,gt=goTo;
 showTab=function(k){const before=cur();st(k);if(cur()!==before)closeCard()};
 goTo=function(id){closeCard();gt(id)}})();
// ---- the navigation trail: Back, Forward and the places visited ----
const SID=Math.random().toString(36).slice(2);let TRAIL=[{v:'',l:'Start'}],TIDX=0;
function trailLabel(v){let m;const clean=s=>String(s).replace(/^[^\p{L}\p{N}]+/u,'').trim();
 if((m=v.match(/^c=(.+)$/))){return byId[m[1]]?byId[m[1]].label:m[1]}
 if((m=v.match(/^t=(.+)$/))){const k=m[1];const gb=document.querySelector('#groups [data-tab="'+k+'"]');if(gb)return clean(gb.textContent);for(const g in GROUPS){const h=GROUPS[g].find(x=>x[0]===k);if(h)return clean(h[1])}const w=VIEWS.find(x=>x[0]===k);if(w)return clean(w[1]);const h2=document.querySelector('#panes [data-pane="'+k+'"] > h2');return h2?clean(h2.textContent):k}
 return v||'Start'}
function navPaint(){const b=document.getElementById('navBack'),f=document.getElementById('navFwd'),p=document.getElementById('navTrail');if(!b)return;
 b.disabled=TIDX<=0;f.disabled=TIDX>=TRAIL.length-1;b.dataset.tip=TIDX>0?'Back to '+TRAIL[TIDX-1].l:'Nothing to go back to';f.dataset.tip=TIDX<TRAIL.length-1?'Forward to '+TRAIL[TIDX+1].l:'Nothing to go forward to';
 b.setAttribute('aria-label',b.dataset.tip);f.setAttribute('aria-label',f.dataset.tip);
 const m=document.getElementById('navMenu');m.innerHTML=TRAIL.map((t,i)=>({t,i})).reverse().map(({t,i})=>'<button type="button" role="menuitem" data-nav="'+i+'"'+(i===TIDX?' aria-current="true"':'')+'>'+(i===TIDX?'● ':'')+esc(t.l)+'</button>').join('');p.disabled=TRAIL.length<2}
hashPush=function(v){if(NAV_SILENT||!NAV_READY||location.hash==='#'+v)return;TRAIL.length=TIDX+1;TRAIL.push({v,l:trailLabel(v)});TIDX=TRAIL.length-1;try{history.pushState({i:TIDX,sid:SID},'','#'+v)}catch(e){}navPaint()};
addEventListener('popstate',e=>{closeCard();const s=e.state;
 if(s&&s.sid===SID&&TRAIL[s.i]){TIDX=s.i}else{const v=decodeURIComponent(location.hash.replace(/^#/,''));TRAIL=[{v,l:trailLabel(v)}];TIDX=0;try{history.replaceState({i:0,sid:SID},'')}catch(_){}}navPaint()});
setTimeout(()=>{const p=document.querySelector('#panes [data-pane]:not([hidden])');let v=decodeURIComponent(location.hash.replace(/^#/,''));
 if(!v&&p){v='t='+p.dataset.pane}TRAIL=[{v,l:trailLabel(v)}];TIDX=0;try{history.replaceState({i:0,sid:SID},'','#'+v)}catch(e){}navPaint()},140);
document.addEventListener('click',e=>{const t=e.target.closest&&e.target.closest('#navBack,#navFwd,#navTrail,[data-nav]');const menu=document.getElementById('navMenu');
 if(!t){if(menu&&!menu.hidden)menu.hidden=true;return}
 if(t.id==='navBack'){history.back();return}if(t.id==='navFwd'){history.forward();return}
 if(t.id==='navTrail'){menu.hidden=!menu.hidden;t.setAttribute('aria-expanded',!menu.hidden);if(!menu.hidden){const c=menu.querySelector('[aria-current]')||menu.querySelector('button');if(c)c.focus()}return}
 if(t.dataset.nav!=null){menu.hidden=true;document.getElementById('navTrail').setAttribute('aria-expanded','false');const i=+t.dataset.nav;if(i!==TIDX)history.go(i-TIDX)}});
document.addEventListener('keydown',e=>{const menu=document.getElementById('navMenu');if(e.altKey&&!e.ctrlKey&&!e.metaKey&&(e.key==='ArrowLeft'||e.key==='ArrowRight')&&!(e.target.matches&&e.target.matches('input,textarea,select'))){e.preventDefault();(e.key==='ArrowLeft'?document.getElementById('navBack'):document.getElementById('navFwd')).click();return}
 if(menu&&!menu.hidden){if(e.key==='Escape'){menu.hidden=true;const p=document.getElementById('navTrail');p.setAttribute('aria-expanded','false');p.focus();e.stopPropagation();return}
  if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();const bs=[...menu.querySelectorAll('button')],i=bs.indexOf(document.activeElement);bs[(i+(e.key==='ArrowDown'?1:bs.length-1))%bs.length].focus()}}},true);
navPaint();
