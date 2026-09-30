// ---- 9.16.0: the taxonomy (a tree with its leaves) and the ontology in three more forms: relation graph, class diagram, entity-relationship diagram ----
// Taxonomy: the chapter at the root, classes nested by "is a kind of", worked examples and matching book concepts as leaves.
let ONTO=null;
async function ontoLoad(){if(ONTO)return ONTO;await ensureGraph();
 const nodesQ=PFX+'SELECT ?s ?label ?kind WHERE { GRAPH ?g { { ?s a owl:Class . BIND("class" AS ?kind) } UNION { ?s a owl:NamedIndividual . BIND("individual" AS ?kind) } OPTIONAL { ?s rdfs:label ?label } } FILTER(CONTAINS(STR(?g),":chapter:")) }';
 const bookQ=PFX+'SELECT ?s ?label WHERE { GRAPH ?g { ?s skos:definition ?d ; rdfs:label ?label } FILTER(CONTAINS(STR(?g),":book:")) }';
 const edgesQ=PFX+'SELECT ?a ?p ?b WHERE { GRAPH ?g { ?a ?p ?b . FILTER(isIRI(?b) && ?p != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> || ?p = <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>) } FILTER(CONTAINS(STR(?g),":chapter:")) }';
 const N=new Map();(await sparql(nodesQ)).forEach(r=>{if(!N.has(r.s))N.set(r.s,{id:r.s,label:r.label||r.s.split(/[#/]/).pop(),kind:r.kind})});
 const book=await sparql(bookQ);const E=[];
 (await sparql(edgesQ)).forEach(r=>{if(N.has(r.a)&&N.has(r.b)&&r.a!==r.b)E.push({a:r.a,b:r.b,p:r.p.split(/[#/]/).pop()})});
 const lab=[...N.values()].filter(n=>n.kind==='class').map(n=>[n.label.toLowerCase(),n.id]);
 book.forEach(r=>{const l=r.label.toLowerCase();const hit=lab.find(([cl])=>cl.length>3&&(l===cl||l.includes(cl)||cl.includes(l)));if(hit){N.set(r.s,{id:r.s,label:r.label,kind:'book'});E.push({a:r.s,b:hit[1],p:'same concept (label match)'})}});
 ONTO={nodes:[...N.values()],edges:E,seed:1};return ONTO}
async function drawOnto(){const st=document.getElementById('ostat');if(ONTO){renderOnto();return}st.textContent='reading the knowledge graph...';await ontoLoad();renderOnto()}
function ontoBuild(){if(ONTO.par)return;const par=new Map(),nodes=new Map(ONTO.nodes.map(n=>[n.id,n]));
 const up=(a,b)=>{for(let x=b,i=0;x&&i<50;x=par.get(x),i++)if(x===a)return true;return false};
 const put=(a,b,any)=>{if(a===b||par.has(a)||!nodes.has(a)||!nodes.has(b)||(!any&&nodes.get(b).kind!=='class')||up(a,b))return;par.set(a,b)};
 ONTO.edges.filter(e=>e.p==='subClassOf').forEach(e=>put(e.a,e.b));
 ONTO.edges.filter(e=>e.p==='type').forEach(e=>put(e.a,e.b));
 ONTO.edges.filter(e=>e.p.indexOf('same concept')===0).forEach(e=>put(e.a,e.b));
 const other=ONTO.edges.filter(e=>e.p!=='subClassOf'&&e.p!=='type'&&e.p!=='disjointWith'&&e.p.indexOf('same concept')!==0&&nodes.get(e.a).kind==='individual'&&nodes.get(e.b).kind==='individual');
 for(let pass=0;pass<4;pass++)other.forEach(e=>put(e.b,e.a,true));
 ONTO.par=par}
const ONTO_PH={subClassOf:['is a kind of','has kinds'],type:['is an example of','has examples'],disjointWith:['cannot also be','cannot also be'],'same concept (label match)':['is the same concept as (matched by name)','is the same concept as (matched by name)']};
function ontoPhrase(p,fwd){const q=ONTO_PH[p];return q?q[fwd?0:1]:p.replace(/([a-z])([A-Z])/g,'$1 $2').toLowerCase()+(fwd?'':' (from)')}
function renderOnto(){const el=document.getElementById('taxo');if(!ONTO||!el)return;ontoBuild();
 const on={};document.querySelectorAll('[data-okind]').forEach(c=>on[c.dataset.okind]=c.checked);const byOid=new Map(ONTO.nodes.map(n=>[n.id,n]));
 const show=n=>on[n.kind];const vpar=id=>{let x=ONTO.par.get(id),i=0;while(x&&!show(byOid.get(x))&&i++<50)x=ONTO.par.get(x);return x||null};
 const rank={class:0,individual:1,book:2};const root={id:null,label:D.title,children:[]};const T=new Map();
 ONTO.nodes.filter(show).forEach(n=>T.set(n.id,{id:n.id,label:n.label,kind:n.kind,children:[]}));
 T.forEach(t=>{const p=vpar(t.id);(p&&T.get(p)?T.get(p):root).children.push(t)});
 const sortK=n=>{n.children.sort((a,b)=>(rank[a.kind]-rank[b.kind])||a.label.localeCompare(b.label));n.children.forEach(sortK)};sortK(root);
 const COLW=210,BW=180,LH=15,GAP=10;let y=10,maxd=0;const list=[];
 (function lay(n,d){n.lines=wrapText(n.label,d===0?26:22);n.h=n.lines.length*LH+12;n.d=d;maxd=Math.max(maxd,d);if(!n.children.length){n.y=y;y+=n.h+GAP}else{n.children.forEach(c=>lay(c,d+1));const a=n.children[0],b=n.children[n.children.length-1];n.y=(a.y+a.h/2+b.y+b.h/2)/2-n.h/2}list.push(n)})(root,0);
 const W=(maxd+1)*COLW+30,H=y+10;let s='<svg viewBox="0 0 '+W+' '+H+'" role="group" aria-label="Chapter taxonomy as a tree">';
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
 document.getElementById('taxoinfo').innerHTML='<b>'+esc(n.label)+'</b> <span class="note">('+KL[n.kind]+')</span>'+(path.length?'<p class="note">Under: '+path.map(p=>esc(p.label)).join(' › ')+'</p>':'')
  +(page?'<p class="row"><button class="btn g" data-go="'+page.id+'">Go to its section</button><button class="btn g" data-detail="'+page.id+'">Open its card</button></p>':'')+(nb?'<div class="kv">Connections</div><ul>'+nb+'</ul>':'<p class="note">No other connections.</p>')}
document.addEventListener('keydown',e=>{const g=e.target.closest&&e.target.closest('g.on[data-oid]');if(g&&(e.key==='Enter'||e.key===' ')){e.preventDefault();if(ONTO)ontoInfo(g.dataset.oid)}});

// ---- what each example is written with and what it does: read by Python's own parser from the example snippets ----
const OG_CON={index:'indexing  x[i]',slice:'slicing  x[a:b]',call:'function call  f(x)',method:'method call  x.m()',assign:'assignment  x = …',unpack:'unpacking  a, *b = …',itemassign:'item or slice assignment  x[i] = …',augassign:'augmented assignment  x += …',delete:'del statement',loop:'for or while loop',comp:'list comprehension',compare:'comparison or membership',boolop:'and / or',binop:'operator + or *',funcdef:'function definition',literal:'list or tuple written out',kwarg:'keyword argument'};
const OG_BEH={inplace:'changes the list itself',new:'builds a new value',copy:'copies a list',share:'shares one list under two names',repeat:'repeats over items',test:'asks a yes-or-no question',search:'searches for an item',shortcut:'stops early when the answer is known',measure:'measures its length',order:'puts items in order',random:'chooses at random',bind:'gives a name to a value',define:'defines a function'};
const OG_PY=String.raw`
import ast, json
S = json.loads(__SNIPS__)
MUT = {'append','insert','remove','pop','sort','reverse','extend','clear','shuffle'}
def parse(src):
    s = src.strip()
    for c in (s, s + ' pass', s + '\n    pass'):
        try: return ast.parse(c), c
        except SyntaxError: continue
    return None, s
out = {}
for cid, src in S.items():
    tree, code = parse(src)
    if tree is None: continue
    con, beh = {}, {}
    def seg(n):
        try: return (ast.get_source_segment(code, n) or type(n).__name__)[:70]
        except Exception: return type(n).__name__
    def C(k, n): con.setdefault(k, seg(n))
    def B(k, n): beh.setdefault(k, seg(n))
    for n in ast.walk(tree):
        if isinstance(n, ast.Subscript):
            if isinstance(n.ctx, ast.Store): C('itemassign', n); B('inplace', n)
            elif isinstance(n.ctx, ast.Del): C('delete', n); B('inplace', n)
            elif isinstance(n.slice, ast.Slice): C('slice', n); B('new', n)
            else: C('index', n)
        elif isinstance(n, ast.Call):
            for k in n.keywords: C('kwarg', n)
            f = n.func
            if isinstance(f, ast.Attribute):
                C('method', n); a = f.attr
                if a in MUT: B('inplace', n)
                if a in ('sort', 'reverse'): B('order', n)
                if a == 'index': B('search', n)
                if a in ('copy', 'deepcopy'): B('copy', n)
                if isinstance(f.value, ast.Name) and f.value.id == 'random': B('random', n)
            elif isinstance(f, ast.Name):
                C('call', n)
                if f.id == 'len': B('measure', n)
                if f.id == 'sorted': B('order', n); B('new', n)
                if f.id in ('list', 'tuple'): B('new', n)
        elif isinstance(n, ast.Assign):
            C('assign', n)
            if any(isinstance(t, (ast.Tuple, ast.List)) for t in n.targets): C('unpack', n)
            if any(isinstance(t, ast.Name) for t in n.targets): B('bind', n)
            if isinstance(n.value, ast.Name) and all(isinstance(t, ast.Name) for t in n.targets): B('share', n)
        elif isinstance(n, ast.AugAssign): C('augassign', n); B('bind', n)
        elif isinstance(n, ast.Delete): C('delete', n)
        elif isinstance(n, (ast.For, ast.While)): C('loop', n); B('repeat', n)
        elif isinstance(n, (ast.ListComp, ast.GeneratorExp)): C('comp', n); B('repeat', n); B('new', n)
        elif isinstance(n, ast.Compare):
            C('compare', n); B('test', n)
            if any(isinstance(o, (ast.In, ast.NotIn)) for o in n.ops): B('search', n)
        elif isinstance(n, ast.BoolOp): C('boolop', n); B('test', n); B('shortcut', n)
        elif isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Mult)): C('binop', n); B('new', n)
        elif isinstance(n, ast.FunctionDef): C('funcdef', n); B('define', n)
        elif isinstance(n, (ast.List, ast.Tuple)) and isinstance(n.ctx, ast.Load): C('literal', n)
        elif isinstance(n, ast.Starred): C('unpack', n)
    out[cid] = {'con': con, 'beh': beh}
print(json.dumps(out))
`;
let OFACTS=null;
async function ogFacts(){if(OFACTS)return OFACTS;const sn={};D.nodes.forEach(n=>{if(n.level===3&&n.example)sn[n.id]=n.example});
 try{OFACTS=await pyJSON(OG_PY.replace('__SNIPS__',JSON.stringify(JSON.stringify(sn))))}catch(e){OFACTS={}}return OFACTS}
// the rows of the concept column: subjects, topics and concepts in reading order
function ogRows(){const rows=[];const walk=(n,d)=>{rows.push({n,d});kids(n.id).forEach(k=>walk(k,d+1))};D.nodes.filter(n=>n.level===1).forEach(t=>walk(t,0));return rows}
function ogEdges(rows,F,layers){const E=[];
 rows.forEach(r=>{const f=F[r.n.id];if(!f)return;Object.keys(f.con||{}).forEach(k=>E.push({layer:'syntax',c:r.n.id,t:k,ev:f.con[k]}));Object.keys(f.beh||{}).forEach(k=>E.push({layer:'behaviour',c:r.n.id,t:k,ev:f.beh[k]}))});return E}
async function drawOgraph(){const el=document.getElementById('onto'),st=document.getElementById('gstat');if(el.querySelector('svg')){return}
 st.textContent='reading the knowledge graph and the examples...';let O=null;try{O=await ontoLoad()}catch(e){}const F=await ogFacts();ogRender(O,F)}
function ogRender(O,F){const el=document.getElementById('onto'),st=document.getElementById('gstat');
 const on={};document.querySelectorAll('[data-glayer]').forEach(c=>on[c.dataset.glayer]=c.checked);
 const rows=ogRows(),E=ogEdges(rows,F||{}),ry=new Map();const RH=28,Y0=44;rows.forEach((r,i)=>{r.y=Y0+i*RH;ry.set(r.n.id,r.y+RH/2)});
 const H=Y0+rows.length*RH+30,XC=300,CW=300,XL=20,XR=760,BW=200;
 const place=(kind,keys)=>{const items=keys.map(k=>{const ys=E.filter(e=>e.layer===kind&&e.t===k).map(e=>ry.get(e.c));return {k,cnt:ys.length,y:ys.reduce((a,b)=>a+b,0)/Math.max(1,ys.length)}}).filter(x=>x.cnt).sort((a,b)=>a.y-b.y);let last=-1e9;items.forEach(it=>{it.y=Math.max(it.y,last+34);last=it.y});const over=last-(H-40);if(over>0)items.forEach(it=>it.y-=over);return items};
 const con=on.syntax?place('syntax',Object.keys(OG_CON)):[],beh=on.behaviour?place('behaviour',Object.keys(OG_BEH)):[];
 const cy=new Map(con.map(i=>[i.k,i.y])),by=new Map(beh.map(i=>[i.k,i.y]));
 let s='<svg viewBox="0 0 980 '+H+'" role="group" aria-label="Ontology graph: meaning, syntax and behaviour">';
 s+='<text class="colh" x="'+(XL+BW/2)+'" y="24" text-anchor="middle">'+(on.syntax?'SYNTAX: how it is written':'')+'</text><text class="colh" x="'+(XC+CW/2)+'" y="24" text-anchor="middle">'+(on.meaning?'MEANING: what it is':'CONCEPTS')+'</text><text class="colh" x="'+(XR+BW/2)+'" y="24" text-anchor="middle">'+(on.behaviour?'BEHAVIOUR: what it does':'')+'</text>';
 // the edges first, so the boxes sit on top
 if(on.meaning){rows.forEach(r=>{const p=r.n.parent&&rows.find(q=>q.n.id===r.n.parent);if(!p)return;const x0=XC+p.d*16+6,y0=p.y+RH/2+8,x1=XC+r.d*16-2,y1=r.y+RH/2;s+='<path class="ge me" data-a="'+esc(r.n.id)+'" data-b="'+esc(p.n.id)+'" d="M'+x0+' '+y0+' V'+y1+' H'+x1+'" fill="none"><title>'+esc(r.n.label+' is a kind of '+p.n.label)+'</title></path>'})}
 E.forEach(e=>{if(!on[e.layer])return;const y1=ry.get(e.c);if(e.layer==='syntax'){const y2=cy.get(e.t);if(y2==null)return;const xr=XC+(rows.find(q=>q.n.id===e.c).d)*16,x1=XC-2,x2=XL+BW;s+='<path class="ge sy" data-a="'+esc(e.c)+'" data-b="syn:'+e.t+'" d="M'+x1+' '+y1+' C'+(x1-70)+' '+y1+' '+(x2+70)+' '+y2+' '+x2+' '+y2+'" fill="none"><title>'+esc(xlab(e.c)+' is written with '+OG_CON[e.t]+' — found in: '+e.ev)+'</title></path>'}
  else{const y2=by.get(e.t);if(y2==null)return;const x1=XC+CW+2,x2=XR;s+='<path class="ge be" data-a="'+esc(e.c)+'" data-b="beh:'+e.t+'" d="M'+x1+' '+y1+' C'+(x1+80)+' '+y1+' '+(x2-80)+' '+y2+' '+x2+' '+y2+'" fill="none"><title>'+esc(xlab(e.c)+' '+OG_BEH[e.t]+' — found in: '+e.ev)+'</title></path>'}});
 // the concept column
 rows.forEach(r=>{const x=XC+r.d*16,w=CW-r.d*16,lv=r.n.level;s+='<g class="og-c lv'+lv+'" data-gid="'+esc(r.n.id)+'" data-c="'+esc(r.n.id)+'" tabindex="0" role="button" aria-label="'+esc(r.n.label)+'"><rect x="'+x+'" y="'+(r.y+2)+'" width="'+w+'" height="'+(RH-4)+'" rx="6"/><text x="'+(x+8)+'" y="'+(r.y+RH/2+4)+'">'+esc(r.n.label.length>36?r.n.label.slice(0,35)+'…':r.n.label)+'</text><title>'+esc(r.n.label)+'</title></g>'});
 con.forEach(i=>{s+='<g class="og-k sy" data-gid="syn:'+i.k+'" tabindex="0" role="button" aria-label="'+esc(OG_CON[i.k])+'"><rect x="'+XL+'" y="'+(i.y-13)+'" width="'+BW+'" height="26" rx="13"/><text x="'+(XL+BW/2)+'" y="'+(i.y+4)+'" text-anchor="middle">'+esc(OG_CON[i.k].split('  ')[0])+'</text><title>'+esc(OG_CON[i.k])+'</title></g>'});
 beh.forEach(i=>{s+='<g class="og-k be" data-gid="beh:'+i.k+'" tabindex="0" role="button" aria-label="'+esc(OG_BEH[i.k])+'"><rect x="'+XR+'" y="'+(i.y-13)+'" width="'+BW+'" height="26" rx="13"/><text x="'+(XR+BW/2)+'" y="'+(i.y+4)+'" text-anchor="middle">'+esc(OG_BEH[i.k])+'</text><title>'+esc(OG_BEH[i.k])+'</title></g>'});
 el.innerHTML='<div class="diagram">'+s+'</svg></div>';
 {const sv=el.querySelector('svg'),vw=980,vh=Math.min(H,Math.max(420,(el.clientHeight||560)*980/Math.max(640,el.clientWidth||760)));sv.dataset.vbkeep='0 0 '+vw+' '+vh}
 zoomable(el.querySelector('.diagram'));
 const nS=E.filter(e=>e.layer==='syntax').length,nB=E.filter(e=>e.layer==='behaviour').length,nM=rows.filter(r=>r.n.parent).length+(O?O.edges.filter(e=>e.p==='disjointWith').length+O.edges.filter(e=>e.p.indexOf('same concept')===0).length:0);
 st.textContent=rows.length+' concepts · '+nM+' meaning links · '+nS+' syntax links · '+nB+' behaviour links';el.__E=E;el.__O=O;setTimeout(fitViews,30)}
function ogSelect(gid){const el=document.getElementById('onto');if(!el.__E)return;const E=el.__E,O=el.__O;const svg=el.querySelector('svg');
 svg.querySelectorAll('.sel,.dim').forEach(x=>x.classList.remove('sel','dim'));
 const rel=new Set([gid]);const hit=e=>e.getAttribute('data-a')===gid||e.getAttribute('data-b')===gid;
 svg.querySelectorAll('path.ge').forEach(p=>{if(hit(p)){p.classList.add('sel');rel.add(p.getAttribute('data-a'));rel.add(p.getAttribute('data-b'))}});
 // a concept's neighbours in the tree: its kinds too
 svg.querySelectorAll('path.me').forEach(p=>{if(rel.has(p.getAttribute('data-a'))&&rel.has(p.getAttribute('data-b')))p.classList.add('sel')});
 svg.classList.add('has-sel');svg.querySelectorAll('g[data-gid]').forEach(g=>{if(rel.has(g.dataset.gid)){g.classList.add('sel')}else g.classList.add('dim')});svg.querySelectorAll('path.ge:not(.sel)').forEach(p=>p.classList.add('dim'));
 const info=document.getElementById('ontoinfo');let h='';
 if(gid.indexOf('syn:')===0||gid.indexOf('beh:')===0){const isS=gid[0]==='s',k=gid.slice(4),list=E.filter(e=>e.layer===(isS?'syntax':'behaviour')&&e.t===k);
  h='<b>'+esc(isS?OG_CON[k]:OG_BEH[k])+'</b> <span class="note">('+(isS?'syntax':'behaviour')+')</span><p class="note">'+(isS?'Found in the syntax tree of the example of':'What the example of')+' '+list.length+' concept'+(list.length>1?'s':'')+(isS?'.':' does, by the rule on the left.')+'</p><ul>'+list.map(e=>'<li><button class="jump" data-gid="'+esc(e.c)+'">'+esc(xlab(e.c))+'</button> <code>'+esc(e.ev)+'</code></li>').join('')+'</ul>'}
 else{const n=byId[gid];const par=n.parent?byId[n.parent]:null,ch=kids(gid),sy=E.filter(e=>e.layer==='syntax'&&e.c===gid),be=E.filter(e=>e.layer==='behaviour'&&e.c===gid);
  const cls=n.class_iri&&O?O.edges.filter(e=>e.a===n.class_iri||e.b===n.class_iri):[];
  const dj=cls.filter(e=>e.p==='disjointWith').map(e=>{const o=O.nodes.find(x=>x.id===(e.a===n.class_iri?e.b:e.a)),pg=o&&D.nodes.find(x=>x.class_iri===o.id);return pg?'<button class="jump" data-gid="'+esc(pg.id)+'">'+esc(pg.label)+'</button>':(o?esc(o.label):'')}).filter(Boolean);
  const bk=cls.filter(e=>e.p.indexOf('same concept')===0).map(e=>{const o=O.nodes.find(x=>x.id===e.a);return o?esc(o.label):''}).filter(Boolean);
  h='<b>'+esc(n.label)+'</b> <span class="note">('+['','subject','topic','concept'][n.level]+')</span><p class="row"><button class="btn g" data-detail="'+esc(gid)+'">Open its card</button><button class="btn g" data-go="'+esc(gid)+'">Go to its section</button></p>'
   +'<div class="kv">Meaning</div><ul>'+(par?'<li>is a kind of <button class="jump" data-gid="'+esc(par.id)+'">'+esc(par.label)+'</button></li>':'')+(ch.length?'<li>has kinds: '+ch.slice(0,8).map(k=>'<button class="jump" data-gid="'+esc(k.id)+'">'+esc(k.label)+'</button>').join(' ')+(ch.length>8?' and '+(ch.length-8)+' more':'')+'</li>':'')+(dj.length?'<li>cannot also be: '+dj.slice(0,6).join(' ')+'</li>':'')+(bk.length?'<li>is the same concept as, in the book: '+bk.join(', ')+'</li>':'')+'</ul>'
   +(sy.length?'<div class="kv">Syntax (how its example is written)</div><ul>'+sy.map(e=>'<li><button class="jump" data-gid="syn:'+e.t+'">'+esc(OG_CON[e.t].split('  ')[0])+'</button> <code>'+esc(e.ev)+'</code></li>').join('')+'</ul>':'')
   +(be.length?'<div class="kv">Behaviour (what its example does)</div><ul>'+be.map(e=>'<li><button class="jump" data-gid="beh:'+e.t+'">'+esc(OG_BEH[e.t])+'</button> <code>'+esc(e.ev)+'</code></li>').join('')+'</ul>':'<p class="note">This is a group of concepts; look at its kinds for syntax and behaviour.</p>')}
 info.innerHTML=h}
document.addEventListener('click',e=>{const g=e.target.closest&&e.target.closest('#onto [data-gid], #ontoinfo [data-gid]');if(!g)return;if(g.closest('#onto')&&g.dataset.c){e.stopImmediatePropagation()}ogSelect(g.dataset.gid)},true);
document.addEventListener('keydown',e=>{const g=e.target.closest&&e.target.closest('#onto g[data-gid]');if(g&&(e.key==='Enter'||e.key===' ')){e.preventDefault();ogSelect(g.dataset.gid)}});
document.addEventListener('change',async e=>{if(e.target.matches&&e.target.matches('[data-glayer]')&&OFACTS){ogRender(ONTO,OFACTS)}});

// ---- the class diagram: each concept as a class with what it is written with and what it does ----
function ocDesc(id){const F=OFACTS||{},all=[id].concat(qUnder(id));const con=new Set(),beh=new Set();all.forEach(c=>{const f=F[c];if(f){Object.keys(f.con||{}).forEach(k=>con.add(k));Object.keys(f.beh||{}).forEach(k=>beh.add(k))}});return {con:[...con],beh:[...beh]}}
async function drawOclass(){const el=document.getElementById('oclass'),sel=document.getElementById('ocsub');if(!el)return;el.innerHTML='<p class="note">reading the examples...</p>';await ogFacts();
 const top=byId[sel.value]||D.nodes.find(n=>n.level===1);const short=k=>OG_CON[k].split('  ')[0];
 const BW=210,COLW=270,LH=14,GAP=14;let y=10,maxd=0;const list=[];
 const mk=(n,d)=>{const f=ocDesc(n.id),own=(OFACTS[n.id]!==undefined);const attrs=f.con.slice(0,5).map(short).concat(f.con.length>5?['… +'+(f.con.length-5)]:[]),ops=f.beh.slice(0,5).map(k=>OG_BEH[k]).concat(f.beh.length>5?['… +'+(f.beh.length-5)]:[]);
  return {n,d,head:wrapText(n.label,26),st:['','subject','topic','concept'][n.level],attrs,ops,children:kids(n.id).map(k=>mk(k,d+1))}};
 const root=mk(top,0);
 (function lay(t){t.h=20+t.head.length*LH+6+(t.attrs.length+1)*LH+4+(t.ops.length+1)*LH+6;maxd=Math.max(maxd,t.d);if(!t.children.length){t.y=y;y+=t.h+GAP}else{t.children.forEach(lay);const a=t.children[0],b=t.children[t.children.length-1];t.y=(a.y+a.h/2+b.y+b.h/2)/2-t.h/2}list.push(t)})(root);
 const W=(maxd+1)*COLW+30,H=y+10;let s='<svg viewBox="0 0 '+W+' '+H+'" role="group" aria-label="Class diagram of '+esc(top.label)+'"><defs><marker id="oc-tri" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" orient="auto"><path d="M1 1 L11 6 L1 11 Z" fill="var(--bg)" stroke="var(--ink)" stroke-width="1.3"/></marker></defs>';
 list.forEach(t=>t.children.forEach(c=>{const x1=c.d*COLW+10,y1=c.y+20,x2=t.d*COLW+10+BW,y2=t.y+t.h/2,mx=x2+(x1-x2)/2;s+='<path class="oc-e" fill="none" marker-end="url(#oc-tri)" d="M'+x1+' '+y1+' H'+mx+' V'+y2+' H'+(x2+1)+'"><title>'+esc(c.n.label+' is a kind of '+t.n.label)+'</title></path>'}));
 list.forEach(t=>{const x=t.d*COLW+10;let yy=t.y;s+='<g class="oc-b lv'+t.n.level+'" data-c="'+esc(t.n.id)+'" tabindex="0" role="button" aria-label="'+esc(t.n.label)+'"><rect x="'+x+'" y="'+t.y+'" width="'+BW+'" height="'+t.h+'" rx="4"/>'
  +'<text class="oc-st" x="'+(x+BW/2)+'" y="'+(yy+13)+'" text-anchor="middle">«'+t.st+'»</text>';yy+=20;
  s+='<text class="oc-h" x="'+(x+BW/2)+'" y="'+(yy+LH-2)+'" text-anchor="middle">'+t.head.map((l,i)=>'<tspan x="'+(x+BW/2)+'" dy="'+(i?LH:0)+'">'+esc(l)+'</tspan>').join('')+'</text>';yy+=t.head.length*LH+6;
  s+='<line x1="'+x+'" x2="'+(x+BW)+'" y1="'+yy+'" y2="'+yy+'"/><text class="oc-k" x="'+(x+6)+'" y="'+(yy+LH-2)+'">written with</text>'+t.attrs.map((a,i)=>'<text x="'+(x+12)+'" y="'+(yy+LH*(i+2)-2)+'">'+esc(a)+'</text>').join('');yy+=(t.attrs.length+1)*LH+4;
  s+='<line x1="'+x+'" x2="'+(x+BW)+'" y1="'+yy+'" y2="'+yy+'"/><text class="oc-k" x="'+(x+6)+'" y="'+(yy+LH-2)+'">does</text>'+t.ops.map((a,i)=>'<text x="'+(x+12)+'" y="'+(yy+LH*(i+2)-2)+'">'+esc(a)+'</text>').join('')+'<title>'+esc(t.n.label)+'</title></g>'});
 el.innerHTML='<div class="diagram">'+s+'</svg></div>';
 {const sv=el.querySelector('svg'),vw=Math.min(W,Math.max(700,el.clientWidth||760)),vh=Math.min(H,Math.max(420,el.clientHeight||560));sv.dataset.vbkeep='0 0 '+vw+' '+vh}
 zoomable(el.querySelector('.diagram'));document.getElementById('ocstat').textContent=list.length+' classes under '+top.label;setTimeout(fitViews,30)}
document.addEventListener('change',e=>{if(e.target.id==='ocsub')drawOclass()});

// ---- the entity-relationship diagram: the schema behind the ontology, with the live counts ----
const OE_ENT={
 subject:{x:30,y:40,label:'Subject',attrs:['label','definition','section'],n:()=>D.nodes.filter(n=>n.level===1).length,sample:()=>D.nodes.filter(n=>n.level===1).map(n=>n.label)},
 topic:{x:330,y:40,label:'Topic',attrs:['label','definition','section','belongs to a subject'],n:()=>D.nodes.filter(n=>n.level===2).length,sample:()=>D.nodes.filter(n=>n.level===2).map(n=>n.label)},
 concept:{x:630,y:40,label:'Concept',attrs:['label','definition','example (code)','belongs to a topic','ontology class'],n:()=>D.nodes.filter(n=>n.level===3).length,sample:()=>D.nodes.filter(n=>n.level===3).map(n=>n.label)},
 example:{x:630,y:300,label:'Example',attrs:['code','result','syntax tree','shown for a concept'],n:()=>D.nodes.filter(n=>n.io).length,sample:()=>D.nodes.filter(n=>n.io).map(n=>n.example||n.io.code)},
 syntax:{x:330,y:300,label:'Syntax construct',attrs:['name','pattern'],n:()=>{const F=OFACTS||{},s=new Set();Object.values(F).forEach(f=>Object.keys(f.con||{}).forEach(k=>s.add(k)));return s.size},sample:()=>Object.values(OG_CON)},
 behaviour:{x:930,y:40,label:'Behaviour',attrs:['name','rule found in the syntax tree'],n:()=>{const F=OFACTS||{},s=new Set();Object.values(F).forEach(f=>Object.keys(f.beh||{}).forEach(k=>s.add(k)));return s.size},sample:()=>Object.values(OG_BEH)},
 book:{x:930,y:300,label:'Book concept',attrs:['label','definition in the book'],n:()=>ONTO?ONTO.nodes.filter(n=>n.kind==='book').length:0,sample:()=>ONTO?ONTO.nodes.filter(n=>n.kind==='book').map(n=>n.label):[]}};
const OE_REL=[['subject','topic','one','many','contains'],['topic','concept','one','many','contains'],['concept','example','one','zeromany','is shown by'],['example','syntax','many','many','is written with'],['concept','behaviour','many','many','does'],['concept','book','zeroone','zeroone','is the same as']];
function oeGlyph(x,y,dx,dy,kind){const nx=-dy,ny=dx,f=(a,b)=>[x+dx*a+nx*b,y+dy*a+ny*b];let s='';const L=(p,q)=>'<line x1="'+p[0]+'" y1="'+p[1]+'" x2="'+q[0]+'" y2="'+q[1]+'"/>';
 if(kind==='one'){s+=L(f(10,-7),f(10,7))+L(f(15,-7),f(15,7))}
 if(kind==='many'||kind==='zeromany'){s+=L(f(14,0),f(0,-8))+L(f(14,0),f(0,8))+L(f(14,0),f(0,0));if(kind==='zeromany'){const c=f(21,0);s+='<circle cx="'+c[0]+'" cy="'+c[1]+'" r="4" fill="var(--bg)"/>'}}
 if(kind==='zeroone'){s+=L(f(10,-7),f(10,7));const c=f(18,0);s+='<circle cx="'+c[0]+'" cy="'+c[1]+'" r="4" fill="var(--bg)"/>'}return s}
async function drawOerd(){const el=document.getElementById('oerd');if(!el)return;await ogFacts();try{await ontoLoad()}catch(e){}
 const BW=210,LH=16;const H=520,W=1180;const box=k=>{const e=OE_ENT[k];return {x:e.x,y:e.y,w:BW,h:30+e.attrs.length*LH+10}};
 let s='<svg viewBox="0 0 '+W+' '+H+'" role="group" aria-label="Entity-relationship diagram of the ontology">';
 OE_REL.forEach(([a,b,ca,cb,verb])=>{const A=box(a),B=box(b);const ax=A.x+A.w/2,ay=A.y+A.h/2,bx=B.x+B.w/2,by=B.y+B.h/2;let p1,p2,d1,d2;
  if(Math.abs(ax-bx)>Math.abs(ay-by)){const right=bx>ax;p1=[right?A.x+A.w:A.x,ay];p2=[right?B.x:B.x+B.w,by];d1=[right?1:-1,0];d2=[right?-1:1,0]}else{const down=by>ay;p1=[ax,down?A.y+A.h:A.y];p2=[bx,down?B.y:B.y+B.h];d1=[0,down?1:-1];d2=[0,down?-1:1]}
  s+='<g class="oe-r"><line x1="'+p1[0]+'" y1="'+p1[1]+'" x2="'+p2[0]+'" y2="'+p2[1]+'"/>'+oeGlyph(p1[0],p1[1],d1[0],d1[1],ca)+oeGlyph(p2[0],p2[1],d2[0],d2[1],cb)+'</g>';
  const mx=(p1[0]+p2[0])/2,my=(p1[1]+p2[1])/2;s+='<rect class="oe-v" x="'+(mx-verb.length*3.4-6)+'" y="'+(my-10)+'" width="'+(verb.length*6.8+12)+'" height="20" rx="10"/><text class="oe-vt" x="'+mx+'" y="'+(my+4)+'" text-anchor="middle">'+esc(verb)+'</text>'});
 Object.keys(OE_ENT).forEach(k=>{const e=OE_ENT[k],b=box(k);s+='<g class="oe-e" data-ent="'+k+'" tabindex="0" role="button" aria-label="'+esc(e.label)+', '+e.n()+' in this chapter"><rect x="'+b.x+'" y="'+b.y+'" width="'+b.w+'" height="'+b.h+'" rx="6"/><rect class="oe-hd" x="'+b.x+'" y="'+b.y+'" width="'+b.w+'" height="26" rx="6"/><text class="oe-t" x="'+(b.x+b.w/2)+'" y="'+(b.y+18)+'" text-anchor="middle">'+esc(e.label)+' ('+e.n()+')</text>'+e.attrs.map((a,i)=>'<text x="'+(b.x+10)+'" y="'+(b.y+26+LH*(i+1))+'">'+(i===0?'◆ ':'· ')+esc(a)+'</text>').join('')+'</g>'});
 s+='<g class="oe-key" transform="translate(30,470)"><text x="0" y="0">Key: | one · crow’s foot many · ○ optional. Each line reads from either end, for example one subject contains many topics; one concept is shown by zero or more examples.</text></g></svg>';
 el.innerHTML='<div class="diagram">'+s+'</div>';zoomable(el.querySelector('.diagram'));setTimeout(fitViews,30)}
function oeInfo(k){const e=OE_ENT[k];const sm=e.sample();document.getElementById('oerdinfo').innerHTML='<b>'+esc(e.label)+'</b> <span class="note">('+e.n()+' in this chapter)</span><div class="kv">Attributes</div><ul>'+e.attrs.map(a=>'<li>'+esc(a)+'</li>').join('')+'</ul><div class="kv">Relationships</div><ul>'+OE_REL.filter(r=>r[0]===k||r[1]===k).map(r=>'<li>'+esc(OE_ENT[r[0]].label)+' <i>'+esc(r[4])+'</i> '+esc(OE_ENT[r[1]].label)+'</li>').join('')+'</ul><div class="kv">Some of them</div><ul>'+sm.slice(0,10).map(x=>'<li>'+esc(String(x).slice(0,80))+'</li>').join('')+(sm.length>10?'<li class="note">and '+(sm.length-10)+' more</li>':'')+'</ul>'}
document.addEventListener('click',e=>{const g=e.target.closest&&e.target.closest('#oerd [data-ent]');if(g)oeInfo(g.dataset.ent)});
document.addEventListener('keydown',e=>{const g=e.target.closest&&e.target.closest('#oerd [data-ent]');if(g&&(e.key==='Enter'||e.key===' ')){e.preventDefault();oeInfo(g.dataset.ent)}});
