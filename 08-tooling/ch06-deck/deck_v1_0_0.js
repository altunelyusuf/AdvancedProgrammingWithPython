// SEN0414 chapter 6 - Lists, deck version 1.0.0: a lecture, not a listing. Every slide states its point as a sentence, draws the idea
// (lists as boxes with indexes, slices as brackets, aliasing as two names pointing at one box, sorts before and after, the matrix screensaver frames:
// all specifications executed under Python and drawn natively - the page draws the same specifications), keeps code to a few executed lines,
// and carries the talk track in its speaker notes. Click builds (objectName "...|bN") are attached by anim_inject_v1_0_0.py.
// The talk track and the page concept of every slide are also written to lecture_out_v1_0_0.json, which the chapter page shows as its Lecture tab.
// Usage: NODE_PATH=$(npm root -g) node deck_v1_0_0.js out.pptx lecture_out.json
const VERSION = "1.0.0";
const pptxgen = require('pptxgenjs'); const fs = require('fs');
const EX = JSON.parse(fs.readFileSync('examples_out_v1_0_0.json')); const py = EX._python; const PR = EX._programs;
const VIS = JSON.parse(fs.readFileSync('visuals_out_v1_0_0.json'));
const TAX = JSON.parse(fs.readFileSync('taxonomy_out_v1_0_0.json')).nodes; const N = {}; TAX.forEach(n => N[n.id] = n);
const kids = id => TAX.filter(n => n.parent === id); const tops = TAX.filter(n => n.level === 1); const leavesOf = id => TAX.filter(n => n.level === 3 && (n.parent === id || (N[n.parent] && N[n.parent].parent === id)));
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.author = 'Yusuf Altunel'; pres.title = 'SEN0414 Chapter 6 - Lists';
const C = { navy:'1E2A3A', blue:'306998', yellow:'FFD43B', ink:'1F2933', mute:'5B6B7B', card:'F1F4F8', code:'17202B', codeTxt:'E6EDF3', green:'2E9E5B', greenBg:'DDF3E6', red:'D64545', redBg:'FBE1E1', amber:'B7791F', amberBg:'FCEFD0', white:'FFFFFF', line:'9AA8B8', blueBg:'E3EEF8' };
const H='Cambria', B='Calibri', M='Courier New';
const S = pres.shapes;
// ---- naming and builds ---------------------------------------------------------------------------------------------------
const nm = (name, k) => (name || 'x') + (k ? '|b' + k : '');
const vn = (id, path) => 'v:' + id + ':' + path;
const rect = (s, o, name, k) => s.addShape(o.shape || S.RECTANGLE, Object.assign({ line:{ color:o.lineColor || o.fill || C.card, width:o.lw || 1, dashType:o.dash }, objectName: nm(name, k) }, o, { fill:{ color:o.fill || C.card } }));
const txt = (s, t, o, name, k) => s.addText(t, Object.assign({ fontFace:B, fontSize:13, color:C.ink, margin:0, isTextBox:true, valign:'middle', objectName: nm(name, k) }, o));
const arrow = (s, x1, y1, x2, y2, o, k) => { o = o || {}; const x = Math.min(x1, x2), y = Math.min(y1, y2), w = Math.abs(x2 - x1), h = Math.abs(y2 - y1);
  s.addShape(S.LINE, { x, y, w, h, flipH: x2 < x1, flipV: y2 < y1, line:{ color:o.color || C.mute, width:o.w || 2, endArrowType: o.noHead ? undefined : 'triangle', dashType:o.dash }, objectName: nm(o.name || 'arrow', k) }); };
const chip = (s, x, y) => { rect(s, { x, y, w:0.62, h:0.42, fill:C.yellow, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }); txt(s, '>>>', { x, y, w:0.62, h:0.42, fontFace:M, fontSize:15, bold:true, color:C.navy, align:'center' }); };
function title(s, t, sub) { cur.title = t; chip(s, 0.45, 0.32); txt(s, t, { x:1.2, y:0.22, w:8.35, h:0.62, fontFace:H, fontSize:22, bold:true, color:C.navy, fit:'shrink' }, 'title');
  if (sub) txt(s, sub, { x:1.2, y:0.82, w:8.35, h:0.34, fontSize:14, italic:true, color:C.mute }, 'subtitle'); }
const LEC = []; let cur = null;   // the lecture record of the slide being built: number, title, talk track, page concept, visual
const newSlide = bg => { const s = pres.addSlide(); s.background = { color:bg }; cur = { n:LEC.length + 1, title:'', say:'', concept:'', covers:[], visual:'', visuals:[] }; LEC.push(cur); return s; };
const light = () => newSlide(C.white);
const dark = () => newSlide(C.navy);
const note = (s, t) => { cur.say = t; s.addNotes(t); };
// lec(page concept, primary visual, title, other leaves the slide teaches, all visuals it draws)
const lec = (concept, visual, title, covers, visuals) => { if (title) cur.title = title; cur.concept = concept || ''; cur.visual = visual || ''; cur.covers = covers || []; cur.visuals = visuals || (visual ? [visual] : []); };
// ---- code and transcripts (checked by deck_check and program_check) ---------------------------------------------------------
// a session: '>>> ' lines and their results; a statement has no result line; every session ends with an expression
function codeCard(s, key, x, y, w, h, fs, k, dk) { const rows = EX[key]; rect(s, { x, y, w, h, fill:C.code, lineColor:dk ? '3B5B87' : C.code, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'codecardbox', k); const runs = [];
  rows.forEach(([c, r]) => { runs.push({ text:'>>> ', options:{ color:C.yellow, bold:true } }); runs.push({ text:c, options:{ color:C.codeTxt, breakLine:true } });
    if (r !== null) runs.push({ text:r, options:{ color:/^[A-Za-z]*Error:/.test(r) ? 'FF7B72' : '7EE787', breakLine:true } }); });
  runs[runs.length - 1].options.breakLine = false;
  txt(s, runs, { x:x + 0.18, y:y + 0.08, w:w - 0.36, h:h - 0.16, fontFace:M, fontSize:fs || 12, valign:'top', paraSpaceAfter:1 }, 'codecard', k); }
function prog(s, p, x, y, w, h, fs, k) { rect(s, { x, y, w, h, fill:C.code, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'progbox', k);
  txt(s, PR[p].code.trim().split('\n').map((l, i, a) => ({ text:l, options:{ color:C.codeTxt, breakLine:i < a.length - 1 } })), { x:x + 0.15, y:y + 0.08, w:w - 0.3, h:h - 0.16, fontFace:M, fontSize:fs || 12, valign:'top', paraSpaceAfter:1 }, 'prog', k); }
function trans(s, p, ris, x, y, w, h, fs, k) { rect(s, { x, y, w, h, fill:C.card, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'transbox', k); const t = [];
  ris.forEach((ri, kk) => { const L = PR[p].runs[ri].lines; if (kk > 0) t.push({ text:'— another run —', options:{ color:C.mute, italic:true, breakLine:true, fontFace:B } });
    L.forEach((segs0, i) => { const segs = []; segs0.forEach(sg => { const prev = segs[segs.length - 1]; if (sg[1] && prev && !/\s$/.test(prev[0])) segs[segs.length - 1] = [prev[0] + sg[0], true]; else segs.push(sg); });   // a prompt that ends without a space is drawn with the typed text as one run, so the transcript reads as printed
      segs.forEach((sg, j) => t.push({ text:sg[0], options:{ color:sg[1] ? C.blue : C.ink, bold:sg[1], breakLine:j === segs.length - 1 && !(kk === ris.length - 1 && i === L.length - 1) } })); }); });
  txt(s, t, { x:x + 0.12, y:y + 0.06, w:w - 0.24, h:h - 0.12, fontFace:M, fontSize:fs || 12, valign:'top', paraSpaceAfter:1 }, 'trans', k);
  txt(s, 'real run' + (ris.length > 1 ? 's' : '') + ' under Python ' + py + (PR[p].runs[ris[0]].inputs.length ? ' — typed input in blue' : ''), { x, y:y + h + 0.02, w, h:0.2, fontSize:9, italic:true, color:C.mute, align:'right' }, 'transcap', k); }
function card(s, x, y, w, h, head, body, accent, k, fs) { rect(s, { x, y, w, h, fill:C.card, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'card', k);
  txt(s, head, { x:x + 0.18, y:y + 0.08, w:w - 0.36, h:0.34, fontFace:H, fontSize:15, bold:true, color:accent || C.blue }, 'cardhead', k);
  txt(s, body, { x:x + 0.18, y:y + 0.44, w:w - 0.36, h:h - 0.52, fontSize:fs || 13, valign:'top' }, 'cardbody', k); }
function say(s, t, x, y, w, h, o, k) { txt(s, t, Object.assign({ x, y, w, h, fontSize:15, color:C.ink, valign:'top' }, o || {}), 'say', k); }
const pg = (s, where, links) => { links = (links || []).slice(); while (links.length && (where.length + links.reduce((a, l) => a + l[0].length + 6, 0)) > 112) links.pop(); rect(s, { x:0.4, y:5.13, w:1.05, h:0.3, fill:C.yellow, lineColor:C.yellow, shape:S.ROUNDED_RECTANGLE, rectRadius:0.06 }, 'pgchip'); txt(s, 'On the page', { x:0.4, y:5.13, w:1.05, h:0.3, fontSize:10, bold:true, color:C.navy, align:'center' }, 'pgchipt');
  const runs = [{ text:where + (links && links.length ? '   ·   ' : ''), options:{ color:C.mute } }]; (links || []).forEach(([l, u], i) => { runs.push({ text:l, options:{ color:C.blue, underline:{ style:'sng' }, hyperlink:{ url:u, tooltip:u } } }); if (i < links.length - 1) runs.push({ text:'   ·   ', options:{ color:C.mute } }); });
  txt(s, runs, { x:1.55, y:5.1, w:8.05, h:0.36, fontSize:10 }, 'pgtext'); };
// the page section of a leaf, in the words of the taxonomy: Learn > top > leaf
const sec = (top, ...ids) => 'Learn ▸ ' + N[top].label + ' ▸ ' + ids.map(i => N[i].label).join(', ');
const DOC = 'https://docs.python.org/3/';
const RL = { book:['Book chapter 6', 'https://automatetheboringstuff.com/3e/chapter6.html'], intro:['Tutorial: lists and slices', DOC + 'tutorial/introduction.html'], ds:['Tutorial: data structures', DOC + 'tutorial/datastructures.html'],
  types:['Built-in types: sequences', DOC + 'library/stdtypes.html'], model:['Data model', DOC + 'reference/datamodel.html'], simple:['Reference: assignment and del', DOC + 'reference/simple_stmts.html'],
  compound:['Reference: the for statement', DOC + 'reference/compound_stmts.html'], expr:['Reference: Boolean operations', DOC + 'reference/expressions.html'], copy:['copy module', DOC + 'library/copy.html'],
  random:['random module', DOC + 'library/random.html'], funcs:['Built-in functions', DOC + 'library/functions.html'], faq:['Programming FAQ', DOC + 'faq/programming.html'], sorting:['Sorting HOWTO', DOC + 'howto/sorting.html'],
  p202:['PEP 202', 'https://peps.python.org/pep-0202/'], p448:['PEP 448', 'https://peps.python.org/pep-0448/'], p3132:['PEP 3132', 'https://peps.python.org/pep-3132/'] };
// ---- visuals drawn from the executed specifications --------------------------------------------------------------------------
const ITEM = { fill:C.blueBg, lineColor:C.blue };
const fitFs = (t, wIn, fs, min) => Math.max(min || 6.5, Math.min(fs, (wIn * 72 - 5) / (0.6 * String(t).length)));   // a monospace text in a box wIn wide: the size at which it does not wrap
function cellRow(s, id, path, items, x, y, bw, bh, fs, fillOf, k, gap) { gap = gap === undefined ? 0.05 : gap;
  items.forEach((t, i) => { const f = fillOf ? fillOf(i) : ITEM; const xx = x + i * (bw + gap);
    rect(s, { x:xx, y, w:bw, h:bh, fill:f.fill, lineColor:f.lineColor, lw:f.lw || 1.25, shape:S.ROUNDED_RECTANGLE, rectRadius:0.05 }, vn(id, path + i + ':box'), k);
    txt(s, t, { x:xx + 0.02, y, w:bw - 0.04, h:bh, fontFace:M, fontSize:fitFs(t, bw - 0.04, fs), bold:true, color:f.color || C.navy, align:'center', fit:'shrink' }, vn(id, path + i), k); });
  return x + items.length * (bw + gap) - gap; }
// a list as boxes with indexes counted from the front (above) and from the back (below); picks hang below the boxes, an error beyond the end
function boxesDraw(s, id, x, y, w, k0, bw) { const V = VIS[id], n = V.list.length; bw = bw || Math.min(1.4, w * 0.6 / n); const gap = 0.08, by = y + 0.28, bh = 0.55;
  V.list.forEach((t, i) => { const xx = x + i * (bw + gap); const hit = V.picks.some(p => p.at.includes(i));
    txt(s, String(i), { x:xx, y, w:bw, h:0.26, fontFace:M, fontSize:12, color:C.mute, align:'center' }, vn(id, 'ix' + i));
    rect(s, { x:xx, y:by, w:bw, h:bh, fill:hit ? C.yellow : C.blueBg, lineColor:hit ? C.amber : C.blue, lw:1.75, shape:S.ROUNDED_RECTANGLE, rectRadius:0.06 }, vn(id, 'i' + i + ':box'));
    txt(s, t, { x:xx + 0.03, y:by, w:bw - 0.06, h:bh, fontFace:M, fontSize:fitFs(t, bw - 0.06, 13), bold:true, color:C.navy, align:'center', fit:'shrink' }, vn(id, 'i' + i));
    txt(s, String(i - n), { x:xx, y:by + bh + 0.02, w:bw, h:0.26, fontFace:M, fontSize:12, color:C.blue, align:'center' }, vn(id, 'nx' + i)); });
  const order = V.picks.map((p, i) => i).sort((a, b) => V.picks[b].at[0] - V.picks[a].at[0]);
  order.forEach((pi, lvl) => { const p = V.picks[pi], cx = x + p.at[0] * (bw + gap) + bw / 2, ly = by + bh + 0.36 + lvl * 0.3;
    arrow(s, cx, by + bh + 0.3, cx, ly + 0.14, { color:C.amber, w:1.75, noHead:true }, k0 ? k0 + lvl : 0);
    txt(s, p.expr + '  →  ' + p.result, { x:cx + 0.06, y:ly, w:Math.min(3.9, x + w - cx - 0.06), h:0.28, fontFace:M, fontSize:12, bold:true, color:C.amber }, vn(id, 'p' + pi), k0 ? k0 + lvl : 0); });
  if (V.error) { const ex = x + n * (bw + gap); const ew = x + w - ex;
    rect(s, { x:ex, y:by, w:0.5, h:bh, fill:C.white, lineColor:C.red, lw:1.5, dash:'dash', shape:S.ROUNDED_RECTANGLE, rectRadius:0.06 }, 'ghost:box', k0 ? k0 + 3 : 0);
    rect(s, { x:ex + 0.65, y:by - 0.1, w:ew - 0.65, h:bh + 0.2, fill:C.redBg, lineColor:C.red, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, vn(id, 'errbox:box'), k0 ? k0 + 3 : 0);
    txt(s, V.error.expr + '  →  ' + V.error.message, { x:ex + 0.73, y:by - 0.1, w:ew - 0.81, h:bh + 0.2, fontFace:M, fontSize:10, bold:true, color:C.red }, vn(id, 'err'), k0 ? k0 + 3 : 0); }
  return by + bh + 0.36 + V.picks.length * 0.3; }
// slices: each row is the same strip of boxes; the selected boxes are filled and bracketed
function slicesDraw(s, id, x, y, w, k0) { const V = VIS[id], n = V.list.length, cw = 0.98, ex = 1.55, sx = x + ex; const gap = 0.05;
  V.list.forEach((t, i) => txt(s, String(i), { x:sx + i * (cw + gap), y, w:cw, h:0.24, fontFace:M, fontSize:11, color:C.mute, align:'center' }, vn(id, 'hx' + i)));
  V.rows.forEach((r, ri) => { const yy = y + 0.3 + ri * 0.5; const kk = k0 ? k0 + ri : 0;
    txt(s, r.expr, { x, y:yy, w:ex - 0.05, h:0.32, fontFace:M, fontSize:13, bold:true, color:C.navy }, vn(id, 'e' + ri + 'x'), kk);
    V.list.forEach((t, i) => { const on = r.picked.includes(i); const xx = sx + i * (cw + gap);
      rect(s, { x:xx, y:yy, w:cw, h:0.32, fill:on ? C.blue : C.card, lineColor:on ? C.blue : C.line, shape:S.ROUNDED_RECTANGLE, rectRadius:0.05 }, vn(id, 'e' + ri + 'c' + i + ':box'), kk);
      txt(s, t, { x:xx + 0.02, y:yy, w:cw - 0.04, h:0.32, fontFace:M, fontSize:fitFs(t, cw - 0.04, 10.5), bold:on, color:on ? C.white : C.mute, align:'center', fit:'shrink' }, vn(id, 'e' + ri + 'c' + i), kk); });
    if (r.picked.length) { const step1 = r.picked.every((p, j) => j === 0 || p === r.picked[j - 1] + 1); const lo = Math.min(...r.picked), hi = Math.max(...r.picked);
      if (step1) arrow(s, sx + lo * (cw + gap), yy + 0.36, sx + hi * (cw + gap) + cw, yy + 0.36, { color:C.green, w:2.5, noHead:true }, kk);
      else r.picked.forEach(p => arrow(s, sx + p * (cw + gap) + 0.15, yy + 0.36, sx + p * (cw + gap) + cw - 0.15, yy + 0.36, { color:C.green, w:2.5, noHead:true }, kk)); }
    const rx = sx + n * (cw + gap) + 0.12;
    txt(s, r.result, { x:rx, y:yy - 0.03, w:x + w - rx, h:0.26, fontFace:M, fontSize:12, bold:true, color:C.green }, vn(id, 'e' + ri + 'r'), kk);
    txt(s, r.picked_label, { x:rx, y:yy + 0.22, w:x + w - rx, h:0.2, fontSize:10, italic:true, color:C.mute }, vn(id, 'e' + ri + 'p'), kk); });
  return y + 0.3 + V.rows.length * 0.5; }
// lanes: one operation each - the list before, an arrow, the list after; red boxes leave or are replaced, green boxes are new
function lanesDraw(s, id, x, y, w, laneH, k0, fs) { const V = VIS[id]; fs = fs || 10;
  V.lanes.forEach((L, r) => { const yy = y + r * laneH, kk = k0 ? k0 + r : 0; const inplace = L.category === 'in place'; const col = inplace ? C.green : C.blue;
    rect(s, { x, y:yy, w, h:laneH - 0.06, fill:C.white, lineColor:C.line, lw:0.75, shape:S.ROUNDED_RECTANGLE, rectRadius:0.06 }, 'lanebox', kk);
    txt(s, L.op, { x:x + 0.1, y:yy + 0.02, w:3.4, h:0.32, fontFace:M, fontSize:12.5, bold:true, color:C.navy }, vn(id, 'l' + r + 'op'), kk);
    txt(s, L.cat_label, { x:x + 3.55, y:yy + 0.02, w:3.35, h:0.32, fontSize:10.5, bold:true, color:col }, vn(id, 'l' + r + 'cat'), kk);
    rect(s, { x:x + w - 2.15, y:yy + 0.05, w:2.05, h:0.27, fill:L.returns === null ? C.card : C.amberBg, lineColor:L.returns === null ? C.line : C.amber, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, vn(id, 'l' + r + 'retbox:box'), kk);
    txt(s, L.ret_label, { x:x + w - 2.15, y:yy + 0.05, w:2.05, h:0.27, fontSize:10.5, bold:true, color:L.returns === null ? C.mute : C.amber, align:'center' }, vn(id, 'l' + r + 'ret'), kk);
    const bwid = (n, avail) => Math.min(0.85, (avail - 0.05 * (n - 1)) / n), by = yy + 0.37, bh = laneH - 0.37 - 0.12;
    const bw1 = bwid(L.before.length, 3.85), bw2 = bwid(L.after.length, 4.45);
    cellRow(s, id, 'l' + r + 'b', L.before, x + 0.1, by, bw1, bh, fs, i => L.before_marks.includes(i) ? { fill:C.redBg, lineColor:C.red, color:C.red } : ITEM, kk);
    arrow(s, x + 4.05, by + bh / 2, x + 4.5, by + bh / 2, { color:col, w:2.5 }, kk);
    cellRow(s, id, 'l' + r + 'a', L.after, x + 4.62, by, bw2, bh, fs, i => L.after_marks.includes(i) ? { fill:C.greenBg, lineColor:C.green, color:C.green } : ITEM, kk); });
  let yy = y + V.lanes.length * laneH;
  V.errors.forEach((e, i) => { rect(s, { x, y:yy, w, h:0.3, fill:C.redBg, lineColor:C.red, shape:S.ROUNDED_RECTANGLE, rectRadius:0.06 }, vn(id, 'e' + i + 'box:box'), k0 ? k0 + V.lanes.length : 0);
    txt(s, e.expr + '   →   ' + e.message, { x:x + 0.1, y:yy, w:w - 0.2, h:0.3, fontFace:M, fontSize:10.5, bold:true, color:C.red, fit:'shrink' }, vn(id, 'e' + i), k0 ? k0 + V.lanes.length : 0); yy += 0.34; });
  return yy; }
// reference graph: name tags on the left point at boxes; a box holds values, or a dot that points at another box
function graphPanel(s, id, sc, st, x, y, w, h, k, o) { o = o || {}; const St = VIS[id].scenarios[sc].steps[st]; const p = 'g' + sc + '.' + st + '.'; const cw = o.cw || 0.5, ch = 0.34, nameW = o.nameW || 1.25; const cwOf = it => it.ref ? cw : Math.max(cw, 0.1 + 0.075 * it.v.length); const fsg = o.fs || 10.5;
  txt(s, St.code, { x, y, w, h:0.26, fontFace: o.capMono === false ? B : M, fontSize:o.capFs || 11.5, bold:true, italic:o.capMono === false, color:C.navy }, vn(id, p + 'c'), k);
  const multi = St.scopes.length > 1; const scCol = ['306998', 'B7791F', '2E9E5B'];
  if (multi) St.scopes.forEach((scp, i) => txt(s, scp.scope, { x:x + i * 1.3, y:y + 0.27, w:1.25, h:0.2, fontSize:9.5, italic:true, bold:true, color:scCol[i] }, vn(id, p + 'sc' + i), k));
  const named = []; St.scopes.forEach((scp, si) => scp.names.forEach(([n, oid]) => named.push({ n, oid, si })));
  const rowsOids = []; named.forEach(a => { if (!rowsOids.includes(a.oid)) rowsOids.push(a.oid); });
  const innerOids = []; const collect = oid => { const ob = St.objects[oid]; if (ob.type === 'list') ob.items.forEach(it => { if (it.ref && !innerOids.includes(it.ref) && !rowsOids.includes(it.ref)) { innerOids.push(it.ref); collect(it.ref); } }); }; rowsOids.forEach(collect);
  const top0 = y + (multi ? 0.52 : 0.34); const pos = {};
  let yy = top0; rowsOids.forEach(oid => { const nn = named.filter(a => a.oid === oid).length; const rh = Math.max(ch + 0.12, nn * 0.3 + 0.06); pos[oid] = { x:x + nameW + 0.25, y:yy + (rh - ch) / 2, rh }; yy += rh + (o.rowGap || 0.1); });
  const hasInner = innerOids.length > 0; const innerX = x + w - (o.innerW || 1.9); const ipitch = o.ipitch || (ch + 0.14);
  innerOids.forEach((oid, i) => { pos[oid] = { x:innerX, y:top0 + i * ipitch, rh:ch }; });
  const objW = oid => { const ob = St.objects[oid]; return ob.type === 'list' ? (ob.items.length ? ob.items.reduce((a, it) => a + cwOf(it) + 0.04, 0) : cw) : Math.max(0.5, Math.min(1.1, 0.16 + ob.v.length * 0.11)); };
  Object.keys(pos).forEach(oid => { const ob = St.objects[oid], q = pos[oid], isInner = innerOids.includes(oid);
    if (ob.type === 'list') { if (!ob.items.length) rect(s, { x:q.x, y:q.y, w:cw, h:ch, fill:C.card, lineColor:C.blue, lw:1.5, dash:'dash', shape:S.ROUNDED_RECTANGLE, rectRadius:0.04 }, vn(id, p + oid + 'empty:box'), k);
      let cx = q.x; ob.items.forEach((it, i) => { const cwi = cwOf(it); const refc = !!it.ref;
        rect(s, { x:cx, y:q.y, w:cwi, h:ch, fill:refc ? C.white : (isInner ? C.card : C.blueBg), lineColor:C.blue, lw:1.5, shape:S.ROUNDED_RECTANGLE, rectRadius:0.04 }, vn(id, p + oid + 'i' + i + ':box'), k);
        if (!refc) txt(s, it.v, { x:cx + 0.01, y:q.y, w:cwi - 0.02, h:ch, fontFace:M, fontSize:fitFs(it.v, cwi - 0.02, fsg), bold:true, color:C.navy, align:'center', fit:'shrink' }, vn(id, p + oid + 'i' + i), k);
        else { rect(s, { x:cx + cwi / 2 - 0.05, y:q.y + ch / 2 - 0.05, w:0.1, h:0.1, fill:C.blue, lineColor:C.blue, shape:S.OVAL }, 'dot', k); }
        cx += cwi + 0.04; }); }
    else { rect(s, { x:q.x, y:q.y, w:objW(oid), h:ch, fill:C.blueBg, lineColor:C.blue, lw:1.5, shape:S.ROUNDED_RECTANGLE, rectRadius:0.04 }, vn(id, p + oid + 'v:box'), k);
      txt(s, ob.v, { x:q.x + 0.01, y:q.y, w:objW(oid) - 0.02, h:ch, fontFace:M, fontSize:fitFs(ob.v, objW(oid) - 0.02, fsg), bold:true, color:C.navy, align:'center', fit:'shrink' }, vn(id, p + oid + 'v'), k); } });
  Object.keys(pos).forEach(oid => { const ob = St.objects[oid], q = pos[oid]; if (ob.type !== 'list') return; let cxa = q.x; ob.items.forEach((it, i) => { const cwi = cwOf(it); const x0 = cxa; cxa += cwi + 0.04; if (!it.ref) return; const t = pos[it.ref];
      arrow(s, x0 + cwi / 2, q.y + ch / 2, t.x, t.y + ch / 2, { color:C.blue, w:1.5, name:'refarrow' }, k); }); });
  rowsOids.forEach(oid => { const grp = named.filter(a => a.oid === oid), q = pos[oid]; const gh = grp.length * 0.3; const gy = q.y + ch / 2 - gh / 2;
    grp.forEach((a, j) => { const ny = gy + j * 0.3; const col = scCol[a.si];
      rect(s, { x:x, y:ny + 0.02, w:nameW, h:0.26, fill:C.white, lineColor:col, lw:1.5, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, vn(id, p + 'n.' + a.n + ':box'), k);
      txt(s, a.n, { x:x, y:ny + 0.02, w:nameW, h:0.26, fontFace:M, fontSize:fitFs(a.n, nameW - 0.04, o.nfs || 10.5), bold:true, color:col, align:'center', fit:'shrink' }, vn(id, p + 'n.' + a.n), k);
      arrow(s, x + nameW, ny + 0.15, q.x, q.y + ch / 2, { color:col, w:2, name:'namearrow' }, k); }); });
  return yy; }
// a sort: the input row with its keys, lines to the output row
function keysortDraw(s, id, x, y, k0) { const V = VIS[id];
  V.examples.forEach((E, e) => { const yy = y + e * 1.17, kk = k0 ? k0 + e : 0; const n = E.items.length; const bw = Math.min(1.15, 6.2 / n), gap = 0.1, bx = x + 2.75;
    txt(s, E.title, { x, y:yy, w:2.6, h:0.26, fontFace:H, fontSize:13, bold:true, color:C.blue }, vn(id, 'x' + e + 't'), kk);
    txt(s, E.expr, { x, y:yy + 0.28, w:2.6, h:0.72, fontFace:M, fontSize:9, color:C.mute, valign:'top' }, vn(id, 'x' + e + 'expr'), kk);
    E.items.forEach((t, i) => { const xx = bx + i * (bw + gap);
      rect(s, { x:xx, y:yy, w:bw, h:0.5, fill:C.blueBg, lineColor:C.blue, lw:1.5, shape:S.ROUNDED_RECTANGLE, rectRadius:0.05 }, vn(id, 'x' + e + 'in' + i + ':box'), kk);
      txt(s, t, { x:xx + 0.02, y:yy + 0.02, w:bw - 0.04, h:E.keys ? 0.26 : 0.46, fontFace:M, fontSize:fitFs(t, bw - 0.04, 10.5), bold:true, color:C.navy, align:'center', fit:'shrink' }, vn(id, 'x' + e + 'in' + i), kk);
      if (E.keys) txt(s, E.keys[i], { x:xx + 0.02, y:yy + 0.28, w:bw - 0.04, h:0.2, fontFace:M, fontSize:9, italic:true, color:C.amber, align:'center', fit:'shrink' }, vn(id, 'x' + e + 'key' + i), kk); });
    E.order.forEach((src, pos) => { arrow(s, bx + src * (bw + gap) + bw / 2, yy + 0.5, bx + pos * (bw + gap) + bw / 2, yy + 0.8, { color:C.line, w:1.5, name:'sortline' }, kk); });
    E.result.forEach((t, i) => { const xx = bx + i * (bw + gap);
      rect(s, { x:xx, y:yy + 0.8, w:bw, h:0.3, fill:C.greenBg, lineColor:C.green, lw:1.5, shape:S.ROUNDED_RECTANGLE, rectRadius:0.05 }, vn(id, 'x' + e + 'out' + i + ':box'), kk);
      txt(s, t, { x:xx + 0.02, y:yy + 0.8, w:bw - 0.04, h:0.3, fontFace:M, fontSize:fitFs(t, bw - 0.04, 10.5), bold:true, color:C.green, align:'center', fit:'shrink' }, vn(id, 'x' + e + 'out' + i), kk); }); });
  return y + V.examples.length * 1.17; }
function factsDraw(s, id, x, y, w, h, cols, k0, o) { o = o || {}; const V = VIS[id], n = V.facts.length, rows = Math.ceil(n / cols), gw = o.gap || 0.12, cw = (w - gw * (cols - 1)) / cols, ch = (h - gw * (rows - 1)) / rows;
  V.facts.forEach((f, i) => { const xx = x + (i % cols) * (cw + gw), yy = y + Math.floor(i / cols) * (ch + gw), kk = k0 ? k0 + i : 0; const err = /Error:/.test(f.result);
    rect(s, { x:xx, y:yy, w:cw, h:ch, fill:C.card, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, vn(id, 'f' + i + 'box:box'), kk);
    if (o.style === 'rows') {
      txt(s, f.label, { x:xx + 0.12, y:yy + 0.02, w:cw - 0.24, h:0.19, fontSize:o.lfs || 10.5, bold:true, color:C.blue, fit:'shrink' }, vn(id, 'f' + i + 't'), kk);
      txt(s, f.expr, { x:xx + 0.12, y:yy + 0.21, w:cw - 0.24, h:0.19, fontFace:M, fontSize:fitFs(f.expr, cw - 0.24, o.efs || 10), color:C.mute, fit:'shrink' }, vn(id, 'f' + i + 'e'), kk);
      txt(s, f.result, { x:xx + 0.12, y:yy + 0.4, w:cw - 0.24, h:0.22, fontFace:M, fontSize:fitFs(f.result, cw - 0.24, o.rfs || 12), bold:true, color:err ? C.red : C.green, fit:'shrink' }, vn(id, 'f' + i + 'r'), kk);
    } else {
      txt(s, f.label, { x:xx + 0.12, y:yy + 0.05, w:cw - 0.24, h:0.4, fontSize:o.lfs || 11, bold:true, color:C.blue, valign:'top' }, vn(id, 'f' + i + 't'), kk);
      txt(s, f.expr, { x:xx + 0.12, y:yy + 0.46, w:cw - 0.24, h:ch - 0.46 - 0.38, fontFace:M, fontSize:o.efs || 10.5, color:C.mute, valign:'top', fit:'shrink' }, vn(id, 'f' + i + 'e'), kk);
      txt(s, f.result, { x:xx + 0.12, y:yy + ch - 0.4, w:cw - 0.24, h:0.34, fontFace:M, fontSize:fitFs(f.result, cw - 0.24, o.rfs || 14), bold:true, color:err ? C.red : C.green, fit:'shrink' }, vn(id, 'f' + i + 'r'), kk); } });
  return y + h; }
// mutation while iterating: one row for each pass of the loop, the list as it was when the pass began and the position the loop had reached
function mutationDraw(s, id, x, y, w, k0) { const V = VIS[id]; const bw = 0.5, rowH = 0.6;
  V.passes.forEach((P, r) => { const yy = y + r * rowH, kk = k0 ? k0 + r : 0;
    rect(s, { x, y:yy, w, h:rowH - 0.08, fill:C.card, shape:S.ROUNDED_RECTANGLE, rectRadius:0.06 }, 'mutrow', kk);
    txt(s, P.head, { x:x + 0.1, y:yy, w:1.75, h:rowH - 0.08, fontFace:M, fontSize:10, bold:true, color:C.navy }, vn(id, 'p' + r + 'h'), kk);
    cellRow(s, id, 'p' + r + 'b', P.before, x + 1.95, yy + 0.1, bw, rowH - 0.28, 12, i => i === P.pos ? { fill:C.yellow, lineColor:C.amber, color:C.navy, lw:2 } : ITEM, kk);
    txt(s, P.action, { x:x + 1.95 + 4 * (bw + 0.05) + 0.1, y:yy, w:w - (1.95 + 4 * (bw + 0.05) + 0.2), h:rowH - 0.08, fontSize:12, bold:true, color:/removes/.test(P.action) ? C.red : C.green }, vn(id, 'p' + r + 'a'), kk); });
  const fy = y + V.passes.length * rowH, kf = k0 ? k0 + V.passes.length : 0;
  rect(s, { x, y:fy, w, h:0.4, fill:C.redBg, lineColor:C.red, shape:S.ROUNDED_RECTANGLE, rectRadius:0.06 }, vn(id, 'finbox:box'), kf);
  txt(s, V.final_label, { x:x + 0.1, y:fy, w:2.6, h:0.4, fontFace:M, fontSize:11, bold:true, color:C.red }, vn(id, 'fin'), kf);
  txt(s, V.skip_label, { x:x + 2.9, y:fy, w:w - 3.0, h:0.4, fontSize:12.5, bold:true, color:C.red }, vn(id, 'skip'), kf);
  return fy + 0.4; }
// unpacking: the statement, the items, and under them the names with the items each one took
function unpackDraw(s, id, x, y, k0) { const V = VIS[id]; const W = 3.9;
  V.cases.forEach((c, ci) => { const yy = y + ci * 1.13, kk = k0 ? k0 + ci : 0, n = c.items.length, bw = (W - 0.06 * (n - 1)) / n;
    txt(s, c.stmt, { x, y:yy, w:W + 0.6, h:0.26, fontFace:M, fontSize:12, bold:true, color:C.navy }, vn(id, 'u' + ci + 'stmt'), kk);
    cellRow(s, id, 'u' + ci + 'i', c.items, x, yy + 0.29, bw, 0.3, 11, null, kk, 0.06);
    c.targets.forEach((t, m) => { const a = x + t.from * (bw + 0.06), wd = (t.to - t.from) * (bw + 0.06) - 0.06; const star = t.name[0] === '*';
      arrow(s, a, yy + 0.66, a + wd, yy + 0.66, { color:star ? C.amber : C.green, w:3, noHead:true }, kk);
      txt(s, t.name, { x:a, y:yy + 0.68, w:wd, h:0.22, fontFace:M, fontSize:11, bold:true, color:star ? C.amber : C.green, align:'center', fit:'shrink' }, vn(id, 'u' + ci + 'n' + m), kk);
      txt(s, t.value, { x:a, y:yy + 0.89, w:wd, h:0.2, fontFace:M, fontSize:9.5, color:C.mute, align:'center', fit:'shrink' }, vn(id, 'u' + ci + 'v' + m), kk); }); });
  return y + V.cases.length * 1.13; }
function seqtypesDraw(s, id, x, y, w, h, k0) { const V = VIS[id], n = V.types.length, gw = 0.12, cw = (w - gw * (n - 1)) / n;
  V.types.forEach((T, i) => { const xx = x + i * (cw + gw), kk = k0 ? k0 + i : 0, col = T.mutable ? C.green : C.red;
    rect(s, { x:xx, y, w:cw, h, fill:C.card, lineColor:col, lw:2, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, vn(id, 's' + i + 'box:box'), kk);
    txt(s, T.type, { x:xx + 0.12, y:y + 0.06, w:cw - 0.24, h:0.34, fontFace:M, fontSize:17, bold:true, color:col }, vn(id, 's' + i + 'name'), kk);
    txt(s, T.sample, { x:xx + 0.12, y:y + 0.42, w:cw - 0.24, h:0.26, fontFace:M, fontSize:fitFs(T.sample, cw - 0.24, 10.5), color:C.ink, fit:'shrink' }, vn(id, 's' + i + 'sample'), kk);
    rect(s, { x:xx + 0.12, y:y + 0.74, w:1.05, h:0.26, fill:T.mutable ? C.greenBg : C.redBg, lineColor:col, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, vn(id, 's' + i + 'chip:box'), kk);
    txt(s, T.mutable_label, { x:xx + 0.12, y:y + 0.74, w:1.05, h:0.26, fontSize:11, bold:true, color:col, align:'center' }, vn(id, 's' + i + 'mut'), kk);
    txt(s, T.assign, { x:xx + 0.12, y:y + 1.06, w:cw - 0.24, h:0.24, fontFace:M, fontSize:10.5, bold:true, color:C.navy }, vn(id, 's' + i + 'assign'), kk);
    txt(s, T.result, { x:xx + 0.12, y:y + 1.3, w:cw - 0.24, h:h - 1.36, fontFace:M, fontSize:9.5, color:T.mutable ? C.green : C.red, valign:'top' }, vn(id, 's' + i + 'result'), kk); });
  return y + h; }
function passesDraw(s, id, x, y, w, k0) { const V = VIS[id], gw = 0.15, tw = 2.9; const cws = [0.85, 2.05];
  V.tables.forEach((T, j) => { const xx = x + j * (tw + gw), kk = k0 ? k0 + j : 0;
    txt(s, T.header, { x:xx, y, w:tw, h:0.3, fontFace:M, fontSize:fitFs(T.header, tw, 11), bold:true, color:C.navy }, vn(id, 't' + j + 'head'), kk);
    let cx = xx; T.cols.forEach((c, ci) => { rect(s, { x:cx, y:y + 0.36, w:cws[ci] - 0.04, h:0.3, fill:C.navy, lineColor:C.navy }, vn(id, 't' + j + 'h' + ci + ':box'), kk);
      txt(s, c, { x:cx + 0.05, y:y + 0.36, w:cws[ci] - 0.14, h:0.3, fontFace:M, fontSize:10.5, bold:true, color:C.white, fit:'shrink' }, vn(id, 't' + j + 'h' + ci), kk); cx += cws[ci]; });
    T.rows.forEach((r, ri) => { let cx2 = xx; r.forEach((cell, ci) => { rect(s, { x:cx2, y:y + 0.7 + ri * 0.36, w:cws[ci] - 0.04, h:0.32, fill:C.card, lineColor:C.card }, vn(id, 't' + j + 'r' + ri + 'c' + ci + ':box'), kk);
        txt(s, cell, { x:cx2 + 0.05, y:y + 0.7 + ri * 0.36, w:cws[ci] - 0.14, h:0.32, fontFace:M, fontSize:fitFs(cell, cws[ci] - 0.14, 11), color:C.ink }, vn(id, 't' + j + 'r' + ri + 'c' + ci), kk); cx2 += cws[ci]; }); }); });
  const px = x + 2 * (tw + gw) + 0.1, pw = x + w - px, kp = k0 ? k0 + 2 : 0;
  txt(s, V.printed_label, { x:px, y, w:pw, h:0.3, fontSize:12, bold:true, color:C.navy }, vn(id, 'plabel'), kp);
  rect(s, { x:px, y:y + 0.36, w:pw, h:4 * 0.36 + 0.02, fill:C.code, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, vn(id, 'pbox:box'), kp);
  V.printed.forEach((l, i) => txt(s, l, { x:px + 0.12, y:y + 0.4 + i * 0.36, w:pw - 0.2, h:0.32, fontFace:M, fontSize:fitFs(l, pw - 0.2, 11), color:C.codeTxt }, vn(id, 'p' + i), kp));
  const st = V.start, sy = y + 0.7 + V.tables[0].rows.length * 0.36 + 0.14, ks = k0 ? k0 + 3 : 0;
  rect(s, { x, y:sy, w, h:0.4, fill:C.amberBg, lineColor:C.amber, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, vn(id, 'startbox:box'), ks);
  txt(s, st.expr, { x:x + 0.12, y:sy, w:5.2, h:0.4, fontFace:M, fontSize:11.5, bold:true, color:C.navy }, vn(id, 'startexpr'), ks);
  txt(s, st.result, { x:x + 5.4, y:sy, w:w - 5.5, h:0.4, fontFace:M, fontSize:12, bold:true, color:C.amber }, vn(id, 'startres'), ks);
  return sy + 0.4; }
function histDraw(s, id, x, y, w, rowH, k0) { const V = VIS[id], mx = Math.max(...V.bars.map(b => b.count)), lw = 2.35, bwMax = w - lw - 0.6;
  V.bars.forEach((b, i) => { const yy = y + i * rowH;
    txt(s, b.text, { x, y:yy, w:lw - 0.08, h:rowH - 0.03, fontSize:10, color:C.ink, align:'right', fit:'shrink' }, vn(id, 'h' + i + 'l'), k0);
    rect(s, { x:x + lw, y:yy + 0.02, w:bwMax * b.count / mx, h:rowH - 0.07, fill:C.blue, lineColor:C.blue }, vn(id, 'h' + i + 'bar:box'), k0);
    txt(s, String(b.count), { x:x + lw + bwMax * b.count / mx + 0.05, y:yy, w:0.5, h:rowH - 0.03, fontFace:M, fontSize:10, bold:true, color:C.blue }, vn(id, 'h' + i + 'n'), k0); });
  return y + V.bars.length * rowH; }
// matrix screensaver: rows printed by the chapter's program, one column's counter, and the misplaced decrement
function matrixDraw(s, id, x, y, k0) { const V = VIS[id]; const rh = 0.152; const FW = 5.7; let yy = y;
  V.frames.forEach((F, a) => { const kk = k0 ? k0 + a : 0;
    txt(s, F.label, { x, y:yy, w:FW, h:0.22, fontSize:11, bold:true, color:C.navy }, vn(id, 'f' + a + 'label'), kk);
    rect(s, { x, y:yy + 0.24, w:FW, h:F.rows.length * rh + 0.12, fill:C.code, shape:S.ROUNDED_RECTANGLE, rectRadius:0.06 }, vn(id, 'f' + a + 'box:box'), kk);
    F.rows.forEach((r, i) => txt(s, r, { x:x + 0.12, y:yy + 0.3 + i * rh, w:FW - 0.2, h:rh, fontFace:M, fontSize:9, color:'7EE787', margin:0 }, vn(id, 'f' + a + 'r' + i), kk));
    yy += 0.24 + F.rows.length * rh + 0.2; });
  V.hazard.forEach((Hz, a) => { const kk = k0 ? k0 + 3 : 0; const good = a === 0;
    txt(s, Hz.label, { x, y:yy, w:4.2, h:0.22, fontSize:10.5, bold:true, color:good ? C.green : C.red }, vn(id, 'hz' + a + 'label'), kk);
    txt(s, Hz.spaces_label, { x:x + 4.2, y:yy, w:FW - 4.2, h:0.22, fontSize:10.5, bold:true, color:good ? C.green : C.red, align:'right' }, vn(id, 'hz' + a + 'n'), kk);
    rect(s, { x, y:yy + 0.23, w:FW, h:rh + 0.1, fill:C.code, lineColor:good ? C.green : C.red, lw:1.5, shape:S.ROUNDED_RECTANGLE, rectRadius:0.05 }, vn(id, 'hz' + a + 'box:box'), kk);
    txt(s, Hz.row, { x:x + 0.12, y:yy + 0.28, w:FW - 0.2, h:rh, fontFace:M, fontSize:9, color:good ? '7EE787' : 'FF7B72', margin:0 }, vn(id, 'hz' + a), kk); yy += 0.23 + rh + 0.2; });
  return yy; }
function lifeTable(s, id, x, y, w, k0) { const V = VIS[id]; const cws = [0.75, 0.95, w - 1.7]; const kk = k0;
  txt(s, 'One column, pass by pass (column ' + V.column + ')', { x, y, w, h:0.24, fontSize:11, bold:true, color:C.navy }, 'lifetitle', kk);
  let cx = x; V.life_cols.forEach((c, ci) => { rect(s, { x:cx, y:y + 0.28, w:cws[ci] - 0.04, h:0.42, fill:C.navy, lineColor:C.navy }, vn(id, 'life.h' + ci + ':box'), kk);
    txt(s, c, { x:cx + 0.04, y:y + 0.28, w:cws[ci] - 0.12, h:0.42, fontSize:10, bold:true, color:C.white, fit:'shrink' }, vn(id, 'life.h' + ci), kk); cx += cws[ci]; });
  V.life.forEach((r, ri) => { let cx2 = x; const on = r.char !== 'space'; [String(r.row), r.char, String(r.counter)].forEach((cell, ci) => {
      rect(s, { x:cx2, y:y + 0.74 + ri * 0.31, w:cws[ci] - 0.04, h:0.28, fill:on ? C.greenBg : C.card, lineColor:on ? C.green : C.card }, vn(id, 'life.r' + ri + 'c' + ci + ':box'), kk);
      txt(s, cell, { x:cx2 + 0.04, y:y + 0.74 + ri * 0.31, w:cws[ci] - 0.12, h:0.28, fontFace:M, fontSize:11, bold:on, color:on ? C.green : C.mute }, vn(id, 'life.r' + ri + 'c' + ci), kk); cx2 += cws[ci]; }); });
  return y + 0.74 + V.life.length * 0.31; }
function classifyDraw(s, id, x, y, w, k0) { const V = VIS[id], gw = 0.15, cw = (w - gw * 2) / 3; const cols = [C.green, C.blue, C.amber], bgs = [C.greenBg, C.blueBg, C.amberBg];
  V.columns.forEach((c, i) => { const xx = x + i * (cw + gw), kk = k0 ? k0 + i : 0;
    rect(s, { x:xx, y, w:cw, h:3.55, fill:C.card, lineColor:cols[i], lw:2, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, vn(id, 'c' + i + 'box:box'), kk);
    txt(s, c.question, { x:xx + 0.15, y:y + 0.08, w:cw - 0.3, h:0.3, fontSize:12.5, italic:true, color:C.mute }, vn(id, 'c' + i + 'q'), kk);
    txt(s, c.head, { x:xx + 0.15, y:y + 0.4, w:cw - 0.3, h:0.4, fontFace:H, fontSize:17, bold:true, color:cols[i] }, vn(id, 'c' + i + 'h'), kk);
    c.chips.forEach((ch, j) => { const yy = y + 0.9 + j * 0.65;
      rect(s, { x:xx + 0.12, y:yy, w:cw - 0.24, h:0.58, fill:bgs[i], lineColor:cols[i], shape:S.ROUNDED_RECTANGLE, rectRadius:0.06 }, vn(id, 'c' + i + 'k' + j + 'box:box'), kk);
      txt(s, ch.expr, { x:xx + 0.2, y:yy + 0.02, w:cw - 0.4, h:0.3, fontFace:M, fontSize:12.5, bold:true, color:C.navy }, vn(id, 'c' + i + 'k' + j), kk);
      txt(s, ch.evidence, { x:xx + 0.2, y:yy + 0.31, w:cw - 0.4, h:0.24, fontSize:10, italic:true, color:C.ink, fit:'shrink' }, vn(id, 'c' + i + 'k' + j + 'ev'), kk); }); });
  return y + 3.55; }
// section divider: the top subject, its middle groups and the leaves the section teaches, drawn from the taxonomy
function divider(top, idx) { const s = dark(); const T = N[top]; lec(top, '', T.label);
  txt(s, String(idx + 1), { x:0.6, y:0.55, w:1.0, h:1.1, fontFace:H, fontSize:66, bold:true, color:C.yellow });
  txt(s, 'of ' + tops.length, { x:1.5, y:1.1, w:1.2, h:0.5, fontSize:16, italic:true, color:'C9D4E0' });
  txt(s, T.label, { x:0.6, y:1.6, w:8.8, h:0.8, fontFace:H, fontSize:36, bold:true, color:C.white });
  txt(s, T.body.replace(/ \(Sweigart, 2025\)\.$/, '.'), { x:0.6, y:2.35, w:8.8, h:0.55, fontSize:15, italic:true, color:C.yellow, valign:'top' });
  const mids = kids(top), gw = 0.2, cw = (8.8 - gw * (mids.length - 1)) / mids.length;
  mids.forEach((m, i) => { const xx = 0.6 + i * (cw + gw), lv = kids(m.id);
    txt(s, m.label, { x:xx, y:3.05, w:cw, h:0.3, fontFace:H, fontSize:15, bold:true, color:'C9D4E0' }, 'divmid', i + 1);
    lv.forEach((l, j) => { rect(s, { x:xx, y:3.4 + j * 0.31, w:cw, h:0.27, fill:'2C3E54', lineColor:'3B5B87', shape:S.ROUNDED_RECTANGLE, rectRadius:0.06 }, 'divleafbox', i + 1);
      txt(s, l.label, { x:xx + 0.1, y:3.4 + j * 0.31, w:cw - 0.2, h:0.27, fontSize:12, color:C.white }, 'divleaf', i + 1); }); });
  tops.forEach((t, i) => { const bw = 8.8 / tops.length; rect(s, { x:0.6 + i * bw, y:5.0, w:bw - 0.08, h:0.07, fill:i === idx ? C.yellow : '4A5D75', lineColor:i === idx ? C.yellow : '4A5D75' }); });
  return s; }
// =====================================================================================================================
const NOTE_SRC = ' Run under Python ' + py + '.';
const nLeaves = TAX.filter(n => n.level === 3).length;
// 1 Title
let s = dark(); lec('', '', 'Chapter 6: Lists'); rect(s, { x:0.6, y:1.0, w:1.2, h:0.8, fill:C.yellow, lineColor:C.yellow, shape:S.ROUNDED_RECTANGLE, rectRadius:0.12 });
txt(s, '>>>', { x:0.6, y:1.0, w:1.2, h:0.8, fontFace:M, fontSize:30, bold:true, color:C.navy, align:'center' });
txt(s, 'Chapter 6: Lists', { x:0.6, y:2.0, w:8.8, h:0.9, fontFace:H, fontSize:38, bold:true, color:C.white });
txt(s, 'Changed in place, made new, or only shared: three questions for every operation', { x:0.6, y:2.85, w:8.8, h:0.9, fontSize:18, italic:true, color:C.yellow, valign:'top' });
txt(s, 'SEN0414 Advanced Programming · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University', { x:0.6, y:4.45, w:8.8, h:0.35, fontSize:13, color:'C9D4E0' });
txt(s, 'Adapted from Automate the Boring Stuff with Python, 3rd edition, chapter 6 (Sweigart, 2025). Every result was produced under Python ' + py + '.', { x:0.6, y:4.85, w:8.8, h:0.3, fontSize:10.5, italic:true, color:'9FB0C4' });
note(s, 'Welcome. Chapter 6 of the book (Sweigart, 2025) is about lists, and this lecture reads it the way an advanced course should: for every operation on a list, ask whether it changes the list in place, returns a new list, or only shares the list. Every result on these slides was produced by running it under Python ' + py + ', and the diagrams are drawn from recorded runs. The chapter page has the same diagrams, and its Lecture tab carries this talk track.');

// 2 Hook
s = dark(); lec('', '', 'One list, two names, one change');
txt(s, 'One list. Two names. One change.', { x:0.7, y:0.55, w:8.6, h:0.9, fontFace:H, fontSize:34, bold:true, color:C.white });
codeCard(s, 'hook', 0.7, 1.65, 5.3, 1.6, 14, 1, true);
txt(s, 'Nothing crashed. No message. Yet the list you called spam is not the list you wrote.', { x:0.7, y:3.45, w:8.6, h:0.7, fontSize:19, italic:true, color:C.yellow, valign:'top' }, 'say', 2);
txt(s, 'Which operations change a list, which make a new one, and which only share it?', { x:0.7, y:4.2, w:8.6, h:0.8, fontFace:H, fontSize:23, bold:true, color:C.white, valign:'top' }, 'say', 3);
note(s, 'Begin with a surprise the chapter itself prints. A list is made and given a second name; the second name is used to change one item; and the original name shows the change, because both names reach one list (Sweigart, 2025). Click for the surprise, and once more for the question that organises this lecture: which operations change a list, which return a new list, and which only share it. Ask the room to predict, before each section, which of the three an operation will turn out to be.' + NOTE_SRC);

// 3 Objectives
s = light(); title(s, 'What you will be able to do with a list', tops.length + ' subjects and ' + nLeaves + ' topics: the chapter as the course’s ontology draws it'); lec('', '', 'What you will be able to do with a list');
const objs = ['Read and write a list with indexes, negative indexes and slices', 'Add, replace and remove items, and say what each call returns', 'Combine, search and order lists, and tell sort() from sorted()',
  'Loop over a list and unpack it, without changing it in the middle of the loop', 'Say what assignment, a function call, a copy and * share, and what they copy', 'Read the Magic 8 Ball and the Matrix screensaver programs'];
tops.forEach((t, i) => { const yy = 1.4 + i * 0.61;
  rect(s, { x:0.5, y:yy, w:2.85, h:0.5, fill:C.blue, lineColor:C.blue, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'objchip', i + 1);
  txt(s, t.label, { x:0.5, y:yy, w:2.85, h:0.5, fontFace:H, fontSize:15, bold:true, color:C.white, align:'center' }, 'objchipt', i + 1);
  txt(s, objs[i], { x:3.55, y:yy, w:6.1, h:0.5, fontSize:14.5 }, 'objtxt', i + 1); });
pg(s, 'Learn ▸ the six subjects of the chapter', [RL.book]);
note(s, 'Six subjects, one row each, and each row is what you should be able to do at the end. They are the six top-level subjects of the chapter’s ontology, which holds ' + nLeaves + ' topics in all: the list type and its positions; changing lists; the operations that join, search and order them; loops and unpacking; sequences and references; and the random functions with the two short programs. Click through the rows. The last row is the reward: the Magic 8 Ball and the Matrix screensaver, both of which use only what the first five rows teach.');

// 4 Three questions
s = light(); title(s, 'Three questions to ask of every list operation', 'The chapter’s operations, sorted by what a real run showed they do'); lec('', 'ThreeQuestions', 'Three questions to ask of every list operation', [], ['ThreeQuestions']);
classifyDraw(s, 'ThreeQuestions', 0.4, 1.35, 9.2, 1);
pg(s, 'Learn ▸ the spine of the whole chapter', [RL.model, RL.types]);
note(s, 'This is the organising idea, and it comes from a design rule of the documentation: a method that mutates a mutable object returns None (Python Software Foundation, 2026). So append, sort and shuffle change the list itself and give back None. Sorted, a slice, the plus operator and a comprehension leave the original alone and give back a new list. Assignment, passing an argument and the star operator do not copy anything: they only share. Each chip was run on a real list, and the small line under it is what the run showed. Click one column at a time. Every later slide asks which column an operation belongs to.' + NOTE_SRC);

// 5 Divider 1
s = divider('ListBasics', 0);
note(s, 'Section one. The list type and where its items sit: the list, its length, indexing and slicing (Sweigart, 2025).');

// 6 Boxes and indexes
s = light(); title(s, 'A list is a row of boxes, each with two numbers', 'Counted from the front (0, 1, 2 ...) and from the back (-1, -2 ...)'); lec('ListType', 'Indexing', 'A list is a row of boxes, each with two numbers', ['ListLength', 'Indexing'], ['Indexing']);
boxesDraw(s, 'Indexing', 0.5, 1.28, 9.0, 1);
codeCard(s, 'boxes', 0.5, 3.5, 9.0, 1.52, 10.5, 5);
pg(s, sec('ListBasics', 'ListType', 'ListLength', 'Indexing'), [RL.book, RL.intro]);
note(s, 'A list is an ordered sequence of values between square brackets; its items may have different types and may even be lists themselves (Sweigart, 2025). Each box has two indexes: counted from 0 at the front, and from -1 at the back, so the third item from the end is index -3. Click through the three lookups: the front, the back, and a negative index. The dashed box beyond the last item is the position that does not exist, and asking for it raises IndexError, exactly the message in the red chip. len returns the number of items. The last line of the session reaches into a list of lists, and the answer is 50.' + NOTE_SRC);

// 7 Slices
s = light(); title(s, 'A slice is a bracket over some of the boxes', 'Every slice is a new list; the original keeps all its items'); lec('Slicing', 'Slicing', 'A slice is a bracket over some of the boxes', [], ['Slicing']);
slicesDraw(s, 'Slicing', 0.4, 1.3, 9.2, 1);
say(s, VIS.Slicing.caption, 0.4, 4.68, 9.2, 0.35, { fontSize:12.5 });
pg(s, sec('ListBasics', 'Slicing'), [RL.book, RL.intro]);
note(s, 'A slice such as one to three is a new list of the items from the start index up to but not including the end index (Sweigart, 2025). Each row is the same four boxes; the filled boxes are the items the slice selects, the bracket under them shows the run, and the small line names the indexes it picked. Click row by row. Leaving out an end means the front or the back. An end past the last item is clipped rather than raising an error, which the fourth row shows. A step of two takes every second item, and a step of minus one walks the list backwards, so that row is a reversed copy (Python Software Foundation, 2026).' + NOTE_SRC);

// 8 Divider 2
s = divider('ChangingLists', 1);
note(s, 'Section two. Unlike a string or a tuple, a list can be changed in the same object, by adding, replacing and removing items (Sweigart, 2025).');

// 9 Adding and replacing
s = light(); title(s, 'Putting items in: the list itself changes', 'append and insert return None; assignment is a statement and has no value'); lec('AppendMethod', 'AddingAndReplacing', 'Putting items in: the list itself changes', ['InsertMethod', 'ItemAssignment', 'SliceAssignment'], ['AddingAndReplacing']);
lanesDraw(s, 'AddingAndReplacing', 0.4, 1.28, 9.2, 0.74, 1);
codeCard(s, 'added', 0.4, 4.25, 4.8, 0.84, 9.5, 5);
say(s, 'Assigning the result of append to spam leaves spam holding None: the list is lost.', 5.4, 4.32, 4.2, 0.7, { fontSize:12.5, bold:true, color:C.red }, 5);
pg(s, sec('ChangingLists', 'AppendMethod', 'InsertMethod', 'ItemAssignment', 'SliceAssignment'), [RL.book, RL.ds, RL.simple]);
note(s, 'Four ways to put something into a list, and all four change the list itself. Append adds one item at the end. Insert puts a value before the item at the given index and moves the later items along. Assigning to an index replaces that item, and assigning a list to a slice replaces a run of items and may change the length of the list (Sweigart, 2025; Python Software Foundation, 2026). Each lane is one real run: the list before, the list after, and what the call returned. Green boxes are new, red boxes were replaced. Click lane by lane. Notice the amber chips: append and insert return None, which is why writing spam equals spam dot append loses the list.' + NOTE_SRC);
const scTitle = (s, id, sc, x, y, w, k, col) => txt(s, VIS[id].scenarios[sc].title, { x, y, w, h:0.26, fontSize:12, bold:true, color:col || C.blue, fit:'shrink' }, vn(id, 'sc' + sc + 't'), k);
// 10 Removing
s = light(); title(s, 'Taking items out: remove, pop and del', 'remove and pop are methods; del is a statement'); lec('RemoveMethod', 'Removing', 'Taking items out: remove, pop and del', ['PopMethod', 'DelStatement'], ['Removing']);
lanesDraw(s, 'Removing', 0.4, 1.3, 9.2, 0.8, 1);
say(s, 'pop is the one that hands the removed item back; remove looks for a value, del and pop take an index.', 0.4, 4.5, 9.2, 0.5, { fontSize:13.5, bold:true, color:C.navy }, 4);
pg(s, sec('ChangingLists', 'RemoveMethod', 'PopMethod', 'DelStatement'), [RL.book, RL.ds, RL.simple]);
note(s, 'Three ways to take items out, and again the list itself changes. Remove deletes only the first item equal to the value, so from a list with three cats only one cat leaves, and it raises ValueError when there is no such item. Pop removes the item at an index, by default the last one, and is the only one of the three that returns it: here it returns 7. Del is a statement, so it has no value; the items after the one it removes move up by one index (Sweigart, 2025; Python Software Foundation, 2026). The red boxes are the items that leave. The two red bars at the bottom are the real messages of the two errors. Click lane by lane.' + NOTE_SRC);

// 11 Divider 3
s = divider('ListOperations', 2);
note(s, 'Section three. Joining, searching and ordering lists: the operations the chapter builds on the list type (Sweigart, 2025). Ordering has four topics, because sorting is where in-place and new-list operations sit side by side.');

// 12 Combining
s = light(); title(s, '+ and * make new lists; += changes the one you have', 'Concatenation and replication leave their operands alone'); lec('ConcatenationReplication', 'Combining', '+ and * make new lists; += changes the one you have', ['AugmentedAssignment'], ['Combining', 'AugmentedAssignment']);
lanesDraw(s, 'Combining', 0.4, 1.28, 9.2, 0.82, 1);
VIS.AugmentedAssignment.scenarios[0].steps.forEach((st, i) => graphPanel(s, 'AugmentedAssignment', 0, i, 0.4 + i * 2.32, 3.05, 2.22, 1.9, 3 + i, { nameW:0.6, cw:0.4, innerW:0.1, capFs:12 }));
pg(s, sec('ListOperations', 'ConcatenationReplication', 'AugmentedAssignment'), [RL.book, RL.simple, RL.faq]);
note(s, 'The plus operator joins two lists into a new list, and the star operator with an integer repeats a list into a new list; neither changes its operands (Sweigart, 2025). The two lanes on top are real runs and both are in the new-list column. The four small pictures below are the trap with the augmented operator. After b equals a, both names reach one list. The augmented assignment a plus-equals a list extends that same list in place, so b shows the change too. But a equals a plus another list builds a new list and only rebinds a: b is left behind, still holding the shorter list (Python Software Foundation, 2026). The reference calls the augmented form similar to, not the same as, the longhand. Click through the four steps.' + NOTE_SRC);

// 13 Searching
s = light(); title(s, 'Finding a value: in tells whether, index tells where', 'and a length test keeps an empty list from raising IndexError'); lec('IndexMethod', 'IndexMethod', 'Finding a value: in tells whether, index tells where', ['MembershipOperators', 'ShortCircuitGuard'], ['IndexMethod', 'MembershipOperators']);
boxesDraw(s, 'IndexMethod', 0.5, 1.28, 9.0, 1);
factsDraw(s, 'MembershipOperators', 0.4, 3.45, 9.2, 1.5, 4, 4);
pg(s, sec('ListOperations', 'MembershipOperators', 'IndexMethod', 'ShortCircuitGuard'), [RL.book, RL.expr, RL.ds]);
note(s, 'The in operator answers yes or no, and the index method answers with a position. Index returns the position of the first item equal to the value, so the first Pooka is at 1; an optional start argument finds the later one at 3; and a missing value raises ValueError, whose message reads list.index(x): x not in list under Python ' + py + ', where the chapter prints the value in the message (Sweigart, 2025). The four cards: on a string, in tests for a substring; on a list, only for a whole item, so gg is in the string eggs but not in the list holding eggs. The last two cards are short-circuiting. And and or stop as soon as the left operand decides the result and return that operand, not a Boolean, so a test that the list is not empty guards an index that would raise IndexError when the list is empty (Python Software Foundation, 2026).' + NOTE_SRC);

// 14 Ordering
s = light(); title(s, 'sort() and reverse() change the list; sorted() does not', 'Only sorted() leaves the original alone and returns the result'); lec('SortMethod', 'Ordering', 'sort() and reverse() change the list; sorted() does not', ['ReverseMethod', 'SortedFunction'], ['Ordering']);
lanesDraw(s, 'Ordering', 0.4, 1.28, 9.2, 0.8, 1);
pg(s, sec('ListOperations', 'SortMethod', 'ReverseMethod', 'SortedFunction'), [RL.book, RL.sorting, RL.funcs]);
note(s, 'This is the pair that the whole chapter’s advice about None is about. Sort orders the list in place and returns None, so writing spam equals spam dot sort leaves spam holding None. Reverse also works in place and returns None. Sorted returns a new sorted list from any iterable and leaves the original unchanged, which the third lane shows: three, one, two is still three, one, two in the before row (Sweigart, 2025; Python Software Foundation, 2026). The fourth lane is the chapter’s reminder that strings sort with uppercase letters before lowercase ones, and the red bar is the TypeError raised when a list mixes numbers and strings, because sort compares with the less-than operator only. Click lane by lane.' + NOTE_SRC);

// 15 Key and reverse
s = light(); title(s, 'A key decides the order, and ties keep their places', 'The key function is called once for each item; the sort is stable'); lec('SortKeyAndReverse', 'SortKeyAndReverse', 'A key decides the order, and ties keep their places', [], ['SortKeyAndReverse']);
keysortDraw(s, 'SortKeyAndReverse', 0.4, 1.3, 1);
pg(s, sec('ListOperations', 'SortKeyAndReverse'), [RL.book, RL.sorting]);
note(s, 'Key and reverse are keyword-only arguments of sort and sorted. In the first picture the key is str.lower; the amber line under each input box is the key the function really returned, and the output row is the result. The lower-case a and the upper-case A have the same key, so they keep the order they had: that is what stability means, and both sort and sorted are stable (Python Software Foundation, 2026). The second picture is the chapter’s reverse equals True: it sorts as if each comparison were reversed. The third picture sorts pairs by their first item only; the two blue pairs and the two red pairs keep their original order among themselves. Click example by example.' + NOTE_SRC);

// 16 Divider 4
s = divider('LoopsAndUnpacking', 3);
note(s, 'Section four. A for loop and a multiple assignment are the two ways the chapter takes a list apart, and this section adds the comprehension and the trap of changing a list while it is walked (Sweigart, 2025).');

// 17 Looping
s = light(); title(s, 'range(len()) and enumerate() visit the same items', 'Two loops, the same four passes, the same four lines'); lec('RangeLenLoop', 'Looping', 'range(len()) and enumerate() visit the same items', ['EnumerateLoop'], ['Looping']);
passesDraw(s, 'Looping', 0.4, 1.3, 9.2, 1);
say(s, VIS.Looping.caption + ' Assigning to i inside the body does not change which index comes next.', 0.4, 4.15, 9.2, 0.75, { fontSize:14 });
pg(s, sec('LoopsAndUnpacking', 'RangeLenLoop', 'EnumerateLoop'), [RL.book, RL.compound, RL.funcs]);
note(s, 'Both loops were run over the chapter’s list of four supplies and every pass was recorded. The first uses range of len to produce each index, and then indexes the list; the second lets enumerate hand over the index and the item together, so the loop needs neither len nor range (Sweigart, 2025). The printed column is identical in both tables. Enumerate takes a start argument: counting from 1 gives the pair 1 and pens first, which is the amber bar. Assigning to i inside the loop does not change which index comes next, because the range supplies the next value regardless (Python Software Foundation, 2026).' + NOTE_SRC);

// 18 Mutation while iterating
s = light(); title(s, 'Pitfall: removing while looping skips items', 'A list iterator counts positions, not values'); lec('MutationWhileIterating', 'MutationWhileIterating', 'Pitfall: removing while looping skips items', [], ['MutationWhileIterating']);
txt(s, 'Before: remove while walking', { x:0.4, y:1.25, w:3.6, h:0.26, fontSize:12, bold:true, color:C.red }, 'l1');
prog(s, 'mutation_bug_v1_0_0.py', 0.4, 1.52, 3.85, 1.22, 11); trans(s, 'mutation_bug_v1_0_0.py', [0], 0.4, 2.78, 3.85, 0.36, 12, 0);
txt(s, 'After: build a new list', { x:0.4, y:3.45, w:3.85, h:0.26, fontSize:12, bold:true, color:C.green }, 'l2', 6);
prog(s, 'mutation_fixed_v1_0_0.py', 0.4, 3.72, 3.85, 0.75, 10.5, 6); trans(s, 'mutation_fixed_v1_0_0.py', [0], 0.4, 4.5, 3.85, 0.36, 12, 6);
mutationDraw(s, 'MutationWhileIterating', 4.45, 1.3, 5.15, 1);
say(s, VIS.MutationWhileIterating.caption, 4.45, 3.95, 5.15, 0.95, { fontSize:13 }, 5);
pg(s, sec('LoopsAndUnpacking', 'MutationWhileIterating'), [RL.compound, RL.faq]);
note(s, 'A trap the chapter does not present, and the commonest bug with lists. The program removes every item below 3 while a for loop walks the list, and it prints [2, 3, 4]: the 2 was never removed. The three rows are the passes of a line trace of that very program. In pass one the loop is at position 0, sees 1 and removes it, so 2 moves into position 0. The iterator counts positions, so pass two is at position 1, which now holds 3; the 2 is never visited (Python Software Foundation, 2026). Build a new list instead, or loop over a copy: the fixed program prints [3, 4]. Click pass by pass.' + NOTE_SRC);

// 19 Unpacking and comprehension
s = light(); title(s, 'Take a list apart with names; build one with a rule', 'Multiple assignment, one starred name, and the list comprehension'); lec('MultipleAssignment', 'Unpacking', 'Take a list apart with names; build one with a rule', ['StarredUnpacking', 'ListComprehension'], ['Unpacking', 'ListComprehension']);
unpackDraw(s, 'Unpacking', 0.4, 1.3, 1);
factsDraw(s, 'ListComprehension', 5.2, 1.3, 4.4, 2.5, 1, 4, { style:'rows', gap:0.08 });
rect(s, { x:5.2, y:3.98, w:4.4, h:0.95, fill:C.redBg, lineColor:C.red, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, vn('Unpacking', 'errbox:box'), 7);
txt(s, VIS.Unpacking.error.expr + '  →  ' + VIS.Unpacking.error.message, { x:5.32, y:3.98, w:4.16, h:0.95, fontFace:M, fontSize:10, bold:true, color:C.red, valign:'middle' }, vn('Unpacking', 'err'), 7);
pg(s, sec('LoopsAndUnpacking', 'MultipleAssignment', 'StarredUnpacking', 'ListComprehension'), [RL.book, RL.p3132, RL.p448, RL.p202]);
note(s, 'Assigning a list to several names is the chapter’s multiple assignment, technically tuple unpacking: the names take the items left to right, and one name too many raises ValueError, which the red box shows with its real message (Sweigart, 2025). Current Python adds one starred name that takes whatever is left over, so the number of names no longer has to match the number of items: first and the rest, or head, the middle and last (Brandl, 2007). A star inside a list display splices a list into a new list (Landau, 2013). On the right, the list comprehension builds a new list from a rule without an append loop; it appeared in Python 2.0 (Warsaw, 2000), and its loop variable does not stay behind afterwards (Python Software Foundation, 2026).' + NOTE_SRC);

// 20 Divider 5
s = divider('SequencesAndReferences', 4);
note(s, 'Section five. Lists, strings and tuples share the sequence operations, and what a variable holds decides what copying a list means (Sweigart, 2025). This is the section that pays off the hook.');

// 21 Mutable vs immutable
s = light(); title(s, 'Lists change in place; strings and tuples do not', 'Among list, str, tuple and range only the list is a mutable sequence'); lec('MutableVersusImmutable', 'MutableVersusImmutable', 'Lists change in place; strings and tuples do not', ['TupleType'], ['MutableVersusImmutable', 'TupleType']);
seqtypesDraw(s, 'MutableVersusImmutable', 0.4, 1.3, 9.2, 2.0, 1);
factsDraw(s, 'TupleType', 0.4, 3.5, 9.2, 1.45, 3, 5);
pg(s, sec('SequencesAndReferences', 'MutableVersusImmutable', 'TupleType'), [RL.book, RL.types, RL.model]);
note(s, 'The chapter names lists, strings, range objects and tuples as sequence types and separates the mutable from the immutable ones (Sweigart, 2025). Each card ran one item assignment on a real value: it worked on the list, and raised TypeError on the string, the tuple and the range. So a changed string is not changed at all: it is rebuilt from slices of the old one, which the first bottom card shows. A tuple is written with commas, usually in parentheses; a one-item tuple needs its trailing comma, and without it you have just a string in parentheses (Python Software Foundation, 2026).' + NOTE_SRC);

// 22 Aliasing
s = light(); title(s, 'Assignment copies nothing: two names, one box', 'A number is replaced; a list is shared'); lec('ReferencesAndAliasing', 'ReferencesAndAliasing', 'Assignment copies nothing: two names, one box', [], ['ReferencesAndAliasing']);
scTitle(s, 'ReferencesAndAliasing', 0, 0.4, 1.25, 9.2, 0, C.red);
VIS.ReferencesAndAliasing.scenarios[0].steps.forEach((st, i) => graphPanel(s, 'ReferencesAndAliasing', 0, i, 0.4 + i * 3.1, 1.55, 3.0, 1.4, 1 + i, { nameW:0.85, cw:0.42, innerW:0.1, capFs:12 }));
scTitle(s, 'ReferencesAndAliasing', 1, 0.4, 3.15, 9.2, 0, C.blue);
VIS.ReferencesAndAliasing.scenarios[1].steps.forEach((st, i) => graphPanel(s, 'ReferencesAndAliasing', 1, i, 0.4 + i * 3.1, 3.45, 3.0, 1.5, 4 + i, { nameW:0.85, cw:0.42, innerW:0.1, capFs:12 }));
pg(s, sec('SequencesAndReferences', 'ReferencesAndAliasing'), [RL.book, RL.model, RL.faq]);
note(s, 'This is the answer to the hook. A variable holds a reference to a value; assigning one variable to another copies the reference, not the value (Sweigart, 2025). In the top row, the second statement gives the list a second name. The third changes an item through eggs, and because both names reach one list, spam shows the change too: both name tags point at the same box. In the bottom row, the same three statements on a number end differently, because giving spam a new value only rebinds the name spam; the number 42 that eggs holds is left alone (Python Software Foundation, 2026). Click statement by statement.' + NOTE_SRC);

// 23 Arguments
s = light(); title(s, 'A function gets the list itself, not a copy', 'A method call changes the caller’s list; an assignment only rebinds the parameter'); lec('ListArguments', 'ListArguments', 'A function gets the list itself, not a copy', [], ['ListArguments']);
prog(s, 'passing_v1_0_0.py', 0.4, 1.3, 3.05, 2.5, 8.5); trans(s, 'passing_v1_0_0.py', [0], 0.4, 3.88, 3.05, 0.55, 11, 0);
scTitle(s, 'ListArguments', 0, 3.6, 1.28, 2.9, 0, C.green); scTitle(s, 'ListArguments', 1, 6.6, 1.28, 2.9, 0, C.red);
[0, 1].forEach(sc => VIS.ListArguments.scenarios[sc].steps.forEach((st, i) => graphPanel(s, 'ListArguments', sc, i, 3.6 + sc * 3.0, 1.62 + i * 1.65, 2.9, 1.55, 1 + sc * 2 + i, { nameW:0.95, cw:0.28, innerW:0.1, capMono:false, capFs:10.5, nfs:9.5, fs:9.5 })));
pg(s, sec('SequencesAndReferences', 'ListArguments'), [RL.book, RL.faq, RL.model]);
note(s, 'The chapter’s program passes a list to a function (Sweigart, 2025). The function receives a reference to the list it is called with, so a method that changes the list inside the function changes the caller’s list: the left pair of pictures, where the parameter and spam are two names for one box, and back in the caller the box holds Hello. The right pair is the other function, which assigns a new list to the parameter: that only rebinds the local name. Inside the function the parameter now points at a new box, and back in the caller spam still holds the original three items. Arguments are passed by assignment, so there is no call by reference (Python Software Foundation, 2026). The pictures are frames of a line trace of the program on the left. Click frame by frame.' + NOTE_SRC);

// 24 Copies
s = light(); title(s, 'A shallow copy shares the inner lists', 'copy.deepcopy copies them too, and shares nothing'); lec('ShallowCopy', 'Copying', 'A shallow copy shares the inner lists', ['DeepCopy'], ['Copying']);
scTitle(s, 'Copying', 1, 0.4, 1.25, 5.6, 0, C.blue); graphPanel(s, 'Copying', 1, 3, 0.4, 1.52, 5.6, 2.3, 1, { nameW:1.0, cw:0.42, innerW:2.1, capFs:11 });
scTitle(s, 'Copying', 0, 6.3, 1.25, 3.3, 0, C.green); graphPanel(s, 'Copying', 0, 2, 6.3, 1.55, 3.3, 1.5, 3, { nameW:1.0, cw:0.42, innerW:0.1, capFs:11 });
codeCard(s, 'copied', 0.4, 3.86, 9.2, 1.22, 9.5, 4);
pg(s, sec('SequencesAndReferences', 'ShallowCopy', 'DeepCopy'), [RL.book, RL.copy, RL.faq]);
note(s, 'Copy dot copy makes a new list that holds references to the same items (Sweigart, 2025). For a flat list that is enough: on the right, changing an item of the copy leaves the original alone. For a nested list it is not: on the left, nested and shallow are two different outer lists, but the arrows from both go to the same two inner lists, so appending to an inner list of nested shows in shallow as well. Deep copy copies the inner lists as well, recursively, so nothing is shared with the original; the two lines in the session confirm it with the identity operator. The slice, the copy method and list() also make shallow copies (Python Software Foundation, 2026). Click through.' + NOTE_SRC);

// 25 [[]] * n
s = light(); title(s, 'Pitfall: [[]] * 3 is one list three times', 'Replication repeats references, not the inner lists'); lec('ReplicationAliasing', 'ReplicationAliasing', 'Pitfall: [[]] * 3 is one list three times', [], ['ReplicationAliasing']);
[0, 1].forEach(sc => { scTitle(s, 'ReplicationAliasing', sc, 0.4 + sc * 4.7, 1.25, 4.4, 0, sc === 0 ? C.red : C.green); graphPanel(s, 'ReplicationAliasing', sc, 1, 0.4 + sc * 4.7, 1.52, 4.5, 1.7, 1 + sc, { nameW:0.8, cw:0.5, innerW:1.2, capFs:11 }); });
codeCard(s, 'replicated', 0.4, 3.3, 9.2, 1.72, 11, 3);
pg(s, sec('SequencesAndReferences', 'ReplicationAliasing'), [RL.faq, RL.book]);
note(s, 'A trap the chapter does not present. Replicating a list repeats references to the same items, so a list of one empty list, times three, holds one inner list three times: the three arrows on the left end at a single box, and appending to the first item shows in all three. The comprehension on the right runs its expression once for each pass and so makes three separate lists (Python Software Foundation, 2026). The session underneath is the same two experiments as real code: the first ends in three threes, the second in one three and two empty lists. Use the star operator for immutable items such as numbers; use a comprehension for lists of lists.' + NOTE_SRC);

// 26 Divider 6
s = divider('RandomAndPrograms', 5);
note(s, 'Section six. The random functions, the two short programs and the practice work show lists in use (Sweigart, 2025). Nothing new is taught here; it is the payoff for the first five sections.');

// 27 Magic 8 ball
s = light(); title(s, 'Magic 8 Ball: a list of answers and a random index', 'Program 1 of the chapter, with a fixed seed so every run prints the same answer'); lec('MagicEightBall', 'MagicEightBall', 'Magic 8 Ball: a list of answers and a random index', ['RandomChoice', 'RandomShuffle'], ['MagicEightBall', 'RandomShuffle']);
prog(s, 'eightball_v1_0_0.py', 0.4, 1.3, 4.55, 2.5, 9); trans(s, 'eightball_v1_0_0.py', [0], 0.4, 3.9, 4.55, 0.72, 11, 1);
txt(s, VIS.MagicEightBall.draws + ' draws of randint(0, len(messages) - 1), seed ' + VIS.MagicEightBall.seed, { x:5.1, y:1.26, w:4.5, h:0.22, fontSize:10.5, bold:true, color:C.navy }, 'histtitle', 2);
histDraw(s, 'MagicEightBall', 5.1, 1.5, 4.5, 0.15, 2);
factsDraw(s, 'RandomShuffle', 5.1, 2.98, 4.5, 2.04, 1, 3, { style:'rows', gap:0.07, lfs:10, efs:9.5, rfs:11 });
pg(s, sec('RandomAndPrograms', 'MagicEightBall', 'RandomChoice', 'RandomShuffle'), [RL.book, RL.random]);
note(s, 'The first short program of the chapter keeps nine answers in a list and prints one, chosen by a random index (Sweigart, 2025). The index runs from 0 to len minus 1, which is 8, because randint includes both ends, so every answer can appear: the bars on the right are the counts of two thousand seeded draws, and every index from 0 to 8 was drawn. The one line added to the chapter’s program is the seed, so that this deck prints the same answer each time. Below the bars, the three random functions that take a list: choice returns one item and leaves the list alone; shuffle reorders the list itself and returns None; sample with k equal to the length returns a shuffled new list (Python Software Foundation, 2026). Ask the room to type a question of their own.' + NOTE_SRC);

// 28 Matrix
s = light(); title(s, 'The Matrix screensaver: one counter per column', 'Program 2 of the chapter: a list of 70 counters, printed row by row'); lec('MatrixScreensaver', 'MatrixScreensaver', 'The Matrix screensaver: one counter per column', [], ['MatrixScreensaver']);
matrixDraw(s, 'MatrixScreensaver', 0.4, 1.28, 1);
lifeTable(s, 'MatrixScreensaver', 6.4, 1.3, 3.2, 2);
txt(s, 'The counters start as a list of zeros', { x:6.4, y:4.1, w:3.2, h:0.24, fontSize:11, bold:true, color:C.navy }, 'zerolabel', 3);
codeCard(s, 'zero', 6.4, 4.38, 3.2, 0.62, 12, 3);
pg(s, sec('RandomAndPrograms', 'MatrixScreensaver'), [RL.book, RL.random]);
note(s, 'The second short program keeps one counter per column in a list of 70 zeros (Sweigart, 2025). For each column on each row: a small chance restarts a stream by setting the counter to a random number from 4 to 14; a counter above zero prints a random 0 or 1 and counts down; a counter at zero prints a space. The two green panels are rows printed by a real run of the chapter’s program with time.sleep replaced, so it finishes at once: at the start a few streams begin, and at the end many streams run at once. The table follows one column, number ' + VIS.MatrixScreensaver.column + ', through one whole stream: a space, four digits while the counter falls from 3 to 0, then a space again. Now the hazard at the bottom: the streams end only because the decrement sits in the branch for a counter above zero. If it is applied to every column, a counter at zero runs negative and the column prints digits forever; the last row of that variant has no spaces at all. Both variants were executed for this study.' + NOTE_SRC);

// 29 Summary
s = light(); title(s, 'What you can do now', 'The chapter on one page: read, change, combine, loop, trace, run'); lec('', '', 'What you can do now');
const can = [['Read', 'a list by index, negative index and slice: every slice is a new list'], ['Change', 'a list in place, and know that append, sort and shuffle return None'], ['Combine', 'with + and *, search with in and index, order with sort and sorted'],
  ['Loop', 'with range(len()) or enumerate(), and never remove from what you walk'], ['Trace', 'assignment, arguments, copies and [[]] * n as names reaching boxes'], ['Run', 'the Magic 8 Ball and the Matrix screensaver, and say why they work']];
can.forEach(([a, b], i) => { const yy = 1.3 + i * 0.6; rect(s, { x:0.5, y:yy, w:1.5, h:0.5, fill:C.blue, lineColor:C.blue, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'canchip', i + 1); txt(s, a, { x:0.5, y:yy, w:1.5, h:0.5, fontFace:H, fontSize:18, bold:true, color:C.white, align:'center' }, 'canchipt', i + 1); txt(s, b, { x:2.2, y:yy, w:7.3, h:0.5, fontSize:15 }, 'cantxt', i + 1); });
note(s, 'Close the loop on the hook: two names, one list, one change. The chapter on one page is six verbs that match the six sections. Read a list by index and slice. Change it in place, remembering what each call returns. Combine, search and order it. Loop over it without changing what you walk. Trace what assignment, a function call, a copy and star share. And run the two programs. The three questions are the summary: did the list change, did I get a new one, or do two names reach one list. Those verbs are the chapter’s learning objectives on the interactive page.');

// 30 Practice
s = light(); title(s, 'Practice: predict, then read the answer', 'Answer aloud first; each answer is a real run'); lec('PracticePrograms', 'PracticePrograms', 'Practice: predict, then read the answer', [], ['PracticePrograms']);
const qs = [['practice1', 'After spam.sort(), what did sort() give back, and what does spam hold?', 0.72], ['practice2', 'After b = a and a += [2], what does b hold?', 0.72], ['practice3', 'How many different lists does [[]] * 3 hold?', 0.9], ['practice4', 'Which items are left after removing every item below 3 while looping?', 0.9]];
qs.forEach(([key, q, hh], i) => { const cx = 0.4 + (i % 2) * 4.7, cy = i < 2 ? 1.26 : 2.56;
  txt(s, String(i + 1), { x:cx, y:cy, w:0.35, h:0.42, fontFace:H, fontSize:18, bold:true, color:C.blue }); txt(s, q, { x:cx + 0.35, y:cy, w:4.1, h:0.42, fontSize:12.5 }); codeCard(s, key, cx, cy + 0.46, 4.5, hh, 10, i + 1); });
factsDraw(s, 'PracticePrograms', 0.4, 4.0, 9.2, 1.02, 3, 5, { lfs:10, efs:9, rfs:12, gap:0.1 });
pg(s, sec('RandomAndPrograms', 'PracticePrograms'), [RL.book]);
note(s, 'Answer aloud first, then read the answer. Question one revisits sort: it returns None and the list is sorted. Question two is the augmented assignment: b shows the change, because plus-equals extends the shared list. Question three counts distinct lists in a list of one empty list times three: one. Question four is the loop that skips. The bottom row is the chapter’s own practice: 17 practice questions and 2 practice programs (Sweigart, 2025). The cards show the answer to question 3 of the chapter, the comma code program, whose function joins a list into a comma-separated string with and before the last item, and the exact chance that 100 coin flips hold a streak of six, about 0.807, which the chapter’s 10,000-experiment count approximates. The solution and the exact probability were written for this study. Sources: the book chapter, the Python 3.14 documentation (tutorial, built-in types, data model, simple statements, copy, random, the Sorting HOWTO and the Programming FAQ), and PEP 202, PEP 448 and PEP 3132. The full source list is in the chapter’s research record, 03-materials/ch06/rdodi/sen0414_ch06_research_v1_0_0.ttl.' + NOTE_SRC);
pres.writeFile({ fileName: process.argv[2] }).then(f => { fs.writeFileSync(process.argv[3], JSON.stringify({ version: VERSION, python: py, slides: LEC.map(l => ({ n: l.n, title: l.title, say: l.say, concept: l.concept, covers: l.covers, visual: l.visual, visuals: l.visuals })) }, null, 1)); console.log('written', f, LEC.length, 'slides'); });
