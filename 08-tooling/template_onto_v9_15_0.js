function ontoBuild(){if(ONTO.par)return;const par=new Map(),nodes=new Map(ONTO.nodes.map(n=>[n.id,n]));
 const up=(a,b)=>{for(let x=b,i=0;x&&i<50;x=par.get(x),i++)if(x===a)return true;return false};
 const put=(a,b,any)=>{if(a===b||par.has(a)||!nodes.has(a)||!nodes.has(b)||(!any&&nodes.get(b).kind!=='class')||up(a,b))return;par.set(a,b)};
 ONTO.edges.filter(e=>e.p==='subClassOf').forEach(e=>put(e.a,e.b));
 ONTO.edges.filter(e=>e.p==='type').forEach(e=>put(e.a,e.b));
 ONTO.edges.filter(e=>e.p.indexOf('same concept')===0).forEach(e=>put(e.a,e.b));
 const other=ONTO.edges.filter(e=>e.p!=='subClassOf'&&e.p!=='type'&&e.p!=='disjointWith'&&e.p.indexOf('same concept')!==0&&nodes.get(e.a).kind==='individual'&&nodes.get(e.b).kind==='individual');
 for(let pass=0;pass<4;pass++)other.forEach(e=>put(e.b,e.a,true));
 ONTO.par=par}
const ONTO_PH={subClassOf:['is a kind of','has kinds'],type:['is an example of','has examples'],'same concept (label match)':['is the same concept as (matched by name)','is the same concept as (matched by name)']};
function ontoPhrase(p,fwd){const q=ONTO_PH[p];return q?q[fwd?0:1]:p.replace(/([a-z])([A-Z])/g,'$1 $2').toLowerCase()+(fwd?'':' (from)')}
function renderOnto(){const el=document.getElementById('onto');if(!ONTO)return;ontoBuild();
 const on={};document.querySelectorAll('[data-okind]').forEach(c=>on[c.dataset.okind]=c.checked);const byOid=new Map(ONTO.nodes.map(n=>[n.id,n]));
 const show=n=>on[n.kind];const vpar=id=>{let x=ONTO.par.get(id),i=0;while(x&&!show(byOid.get(x))&&i++<50)x=ONTO.par.get(x);return x||null};
 const rank={class:0,individual:1,book:2};const root={id:null,label:D.title,children:[]};const T=new Map();
 ONTO.nodes.filter(show).forEach(n=>T.set(n.id,{id:n.id,label:n.label,kind:n.kind,children:[]}));
 T.forEach(t=>{const p=vpar(t.id);(p&&T.get(p)?T.get(p):root).children.push(t)});
 const sortK=n=>{n.children.sort((a,b)=>(rank[a.kind]-rank[b.kind])||a.label.localeCompare(b.label));n.children.forEach(sortK)};sortK(root);
 const COLW=210,BW=180,LH=15,GAP=10;let y=10,maxd=0;const list=[];
 (function lay(n,d){n.lines=wrapText(n.label,d===0?26:22);n.h=n.lines.length*LH+12;n.d=d;maxd=Math.max(maxd,d);if(!n.children.length){n.y=y;y+=n.h+GAP}else{n.children.forEach(c=>lay(c,d+1));const a=n.children[0],b=n.children[n.children.length-1];n.y=(a.y+a.h/2+b.y+b.h/2)/2-n.h/2}list.push(n)})(root,0);
 const W=(maxd+1)*COLW+30,H=y+10;let s='<svg viewBox="0 0 '+W+' '+H+'" role="group" aria-label="Ontology graph as a tree">';
 list.forEach(n=>n.children.forEach(c=>{const x1=n.d*COLW+10+BW,y1=n.y+n.h/2,x2=c.d*COLW+10,y2=c.y+c.h/2,mx=(x1+x2)/2;s+='<path class="e" fill="none" d="M'+x1+' '+y1+' C'+mx+' '+y1+' '+mx+' '+y2+' '+x2+' '+y2+'"'+(c.kind==='book'?' stroke-dasharray="5 4"':'')+'/>'}));
 list.forEach(n=>{const x=n.d*COLW+10;const tx='<text x="'+(x+BW/2)+'" y="'+(n.y+LH+2)+'" text-anchor="middle">'+n.lines.map((l,i)=>'<tspan x="'+(x+BW/2)+'" dy="'+(i?LH:0)+'">'+esc(l)+'</tspan>').join('')+'</text>';
  if(n.id===null)s+='<g class="n root"><rect x="'+x+'" y="'+n.y+'" width="'+BW+'" height="'+n.h+'" rx="7"/>'+tx+'<title>'+esc(n.label)+'</title></g>';
  else s+='<g class="on k-'+n.kind+'" data-oid="'+esc(n.id)+'" tabindex="0" role="button" aria-label="'+esc(n.label+' ('+({class:'class',individual:'individual',book:'book concept'})[n.kind]+')')+'"><rect x="'+x+'" y="'+n.y+'" width="'+BW+'" height="'+n.h+'" rx="7"/>'+tx+'<title>'+esc(n.label+' ('+n.kind+')')+'</title></g>'});
 el.innerHTML='<div class="diagram">'+s+'</svg></div>';
 {const sv=el.querySelector('svg'),vw=Math.min(W,Math.max(640,el.clientWidth||760)),vh=Math.min(H,Math.max(420,(el.clientHeight||560))),cy=root.y+root.h/2;sv.dataset.vbkeep='0 '+Math.max(0,Math.min(H-vh,cy-vh/2))+' '+vw+' '+vh}
 zoomable(el.querySelector('.diagram'));
 const cnt=k=>ONTO.nodes.filter(n=>n.kind===k).length;document.getElementById('ostat').textContent=cnt('class')+' classes · '+cnt('individual')+' individuals · '+cnt('book')+' book concepts · '+ONTO.edges.length+' links';setTimeout(fitViews,30)}
function ontoInfo(id){const n=ONTO.nodes.find(x=>x.id===id);if(!n)return;ontoBuild();const path=[];for(let x=ONTO.par.get(id),i=0;x&&i<20;x=ONTO.par.get(x),i++)path.unshift(ONTO.nodes.find(z=>z.id===x));
 const nb=ONTO.edges.filter(e=>e.a===id||e.b===id).map(e=>{const fwd=e.a===id,o=ONTO.nodes.find(x=>x.id===(fwd?e.b:e.a));return o?'<li>'+esc(ontoPhrase(e.p,fwd))+' — <button class="jump" data-oid="'+esc(o.id)+'">'+esc(o.label)+'</button></li>':''}).join('');
 const page=D.nodes.find(x=>x.class_iri===id),KL={class:'class',individual:'individual',book:'concept from the book'};
 document.getElementById('ontoinfo').innerHTML='<b>'+esc(n.label)+'</b> <span class="note">('+KL[n.kind]+')</span>'+(path.length?'<p class="note">Under: '+path.map(p=>esc(p.label)).join(' › ')+'</p>':'')+'<p class="note"><code>'+esc(id)+'</code></p>'
  +(page?'<p class="row"><button class="btn g" data-go="'+page.id+'">Go to its section</button><button class="btn g" data-detail="'+page.id+'">Open its card</button></p>':'')+(nb?'<div class="kv">Connections</div><ul>'+nb+'</ul>':'<p class="note">No other connections.</p>')}
document.addEventListener('keydown',e=>{const g=e.target.closest&&e.target.closest('g.on[data-oid]');if(g&&(e.key==='Enter'||e.key===' ')){e.preventDefault();if(ONTO)ontoInfo(g.dataset.oid)}});
