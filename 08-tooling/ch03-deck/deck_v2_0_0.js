// SEN0414 chapter 3 - Loops, deck version 2.0.0: a lecture, not a listing. Every slide states its point as a sentence, draws the idea
// (diagrams and visuals are specifications executed under Python and drawn natively - the page draws the same specifications),
// and carries the talk track in its speaker notes. Click builds (objectName "...|bN") are attached by anim_inject_v1_0_0.py.
// Usage: NODE_PATH=$(npm root -g) node deck_v2_0_0.js out.pptx
const VERSION = "2.0.0";
const pptxgen = require('pptxgenjs'); const fs = require('fs');
const EX = JSON.parse(fs.readFileSync('examples_out_v1_1_0.json')); const py = EX._python; const PR = EX._programs;
const VIS = JSON.parse(fs.readFileSync('visuals_out_v1_0_0.json'));
const PD = JSON.parse(fs.readFileSync('../ch03-page/page_data_v9_5_0.json')); const NODE = {}; PD.nodes.forEach(n => NODE[n.id] = n);
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.author = 'Yusuf Altunel'; pres.title = 'SEN0414 Chapter 3 - Loops';
const C = { navy:'1E2A3A', blue:'306998', yellow:'FFD43B', ink:'1F2933', mute:'5B6B7B', card:'F1F4F8', code:'17202B', codeTxt:'E6EDF3', green:'2E9E5B', greenBg:'DDF3E6', red:'D64545', redBg:'FBE1E1', amber:'B7791F', amberBg:'FCEFD0', white:'FFFFFF', line:'9AA8B8', blueBg:'E3EEF8' };
const H='Cambria', B='Calibri', M='Courier New';
const S = pres.shapes;
// ---- naming and builds ---------------------------------------------------------------------------------------------------
const nm = (name, k) => (name || 'x') + (k ? '|b' + k : '');
const rect = (s, o, name, k) => s.addShape(o.shape || S.RECTANGLE, Object.assign({ line:{ color:o.lineColor || o.fill || C.card, width:o.lw || 1, dashType:o.dash }, objectName: nm(name, k) }, o, { fill:{ color:o.fill || C.card } }));
const txt = (s, t, o, name, k) => s.addText(t, Object.assign({ fontFace:B, fontSize:13, color:C.ink, margin:0, isTextBox:true, valign:'middle', objectName: nm(name, k) }, o));
const arrow = (s, x1, y1, x2, y2, o, k) => { o = o || {}; const x = Math.min(x1, x2), y = Math.min(y1, y2), w = Math.abs(x2 - x1), h = Math.abs(y2 - y1);
  s.addShape(S.LINE, { x, y, w, h, flipH: x2 < x1, flipV: y2 < y1, line:{ color:o.color || C.mute, width:o.w || 2, endArrowType: o.noHead ? undefined : 'triangle', dashType:o.dash }, objectName: nm(o.name || 'arrow', k) }); };
const chip = (s, x, y) => { rect(s, { x, y, w:0.62, h:0.42, fill:C.yellow, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }); txt(s, '>>>', { x, y, w:0.62, h:0.42, fontFace:M, fontSize:15, bold:true, color:C.navy, align:'center' }); };
function title(s, t, sub) { chip(s, 0.45, 0.32); txt(s, t, { x:1.2, y:0.22, w:8.35, h:0.62, fontFace:H, fontSize:22, bold:true, color:C.navy, fit:'shrink' }, 'title');
  if (sub) txt(s, sub, { x:1.2, y:0.82, w:8.35, h:0.34, fontSize:14, italic:true, color:C.mute }, 'subtitle'); }
const light = () => { const s = pres.addSlide(); s.background = { color:C.white }; return s; };
const dark = () => { const s = pres.addSlide(); s.background = { color:C.navy }; return s; };
const note = (s, t) => s.addNotes(t);
const BK = 'Automate the Boring Stuff with Python, 3rd edition, chapter 3 (Sweigart, 2025)';
// ---- code and transcripts (checked by deck_check and program_check) ---------------------------------------------------------
function codeCard(s, rows, x, y, w, h, fs) { rect(s, { x, y, w, h, fill:C.code, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }); const runs = [];
  rows.forEach(([c, r]) => { runs.push({ text:'>>> ', options:{ color:C.yellow, bold:true } }); runs.push({ text:c, options:{ color:C.codeTxt, breakLine:true } }); runs.push({ text:r, options:{ color:/Error/.test(r) ? '#FF7B72'.slice(1) : '7EE787', breakLine:true } }); });
  txt(s, runs, { x:x + 0.2, y:y + 0.12, w:w - 0.4, h:h - 0.24, fontFace:M, fontSize:fs || 14, valign:'top', paraSpaceAfter:2 }, 'codecard');
  txt(s, 'run under Python ' + py, { x, y:y + h + 0.03, w, h:0.22, fontSize:9, italic:true, color:C.mute, align:'right' }); }
function prog(s, p, x, y, w, h, fs, k) { rect(s, { x, y, w, h, fill:C.code, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'progbox', k);
  txt(s, PR[p].code.trim().split('\n').map((l, i, a) => ({ text:l, options:{ color:C.codeTxt, breakLine:i < a.length - 1 } })), { x:x + 0.2, y:y + 0.1, w:w - 0.4, h:h - 0.2, fontFace:M, fontSize:fs || 12, valign:'top', paraSpaceAfter:1 }, 'prog', k); }
function trans(s, p, ris, x, y, w, h, fs, k) { rect(s, { x, y, w, h, fill:C.card, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'transbox', k); const t = [];
  ris.forEach((ri, kk) => { const L = PR[p].runs[ri].lines; if (kk > 0) t.push({ text:'— another run —', options:{ color:C.mute, italic:true, breakLine:true, fontFace:B } });
    L.forEach((segs, i) => { segs.forEach((sg, j) => t.push({ text:sg[0], options:{ color:sg[1] ? C.blue : C.ink, bold:sg[1], breakLine:j === segs.length - 1 && !(kk === ris.length - 1 && i === L.length - 1) } })); }); });
  txt(s, t, { x:x + 0.15, y:y + 0.08, w:w - 0.3, h:h - 0.16, fontFace:M, fontSize:fs || 12, valign:'top', paraSpaceAfter:1 }, 'trans', k);
  txt(s, 'real run' + (ris.length > 1 ? 's' : '') + ' under Python ' + py + (PR[p].runs[ris[0]].inputs.length ? ' — typed input in blue' : ''), { x, y:y + h + 0.03, w, h:0.22, fontSize:9, italic:true, color:C.mute, align:'right' }, 'transcap', k); }
function card(s, x, y, w, h, head, body, accent, k) { rect(s, { x, y, w, h, fill:C.card, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'card', k);
  txt(s, head, { x:x + 0.18, y:y + 0.1, w:w - 0.36, h:0.34, fontFace:H, fontSize:15, bold:true, color:accent || C.blue }, 'cardhead', k);
  txt(s, body, { x:x + 0.18, y:y + 0.46, w:w - 0.36, h:h - 0.55, fontSize:13, valign:'top' }, 'cardbody', k); }
function say(s, t, x, y, w, h, o, k) { txt(s, t, Object.assign({ x, y, w, h, fontSize:15, color:C.ink, valign:'top' }, o || {}), 'say', k); }
// ---- visuals drawn from the executed specifications --------------------------------------------------------------------------
function numberLine(s, id, x, y, w, k0) { const V = VIS[id]; const lo = Math.min(V.lo, V.start, V.stop) - 0.7, hi = Math.max(V.hi, V.start, V.stop) + 0.7; const X = v => x + (v - lo) / (hi - lo) * w;
  arrow(s, x, y + 0.55, x + w, y + 0.55, { color:C.line, w:2, noHead:true }); const ticks = []; for (let v = Math.ceil(lo); v <= Math.floor(hi); v++) ticks.push(v);
  ticks.forEach(v => { txt(s, String(v), { x:X(v) - 0.25, y:y + 0.72, w:0.5, h:0.25, fontSize:11, color:C.mute, align:'center' }, 'tick' + v); arrow(s, X(v), y + 0.5, X(v), y + 0.6, { color:C.line, w:1, noHead:true }); });
  V.values.forEach((v, i) => { rect(s, { x:X(v) - 0.17, y:y + 0.38, w:0.34, h:0.34, fill:C.blue, lineColor:C.blue, shape:S.OVAL }, 'v:' + id + ':dot' + i, k0 ? k0 + i : 0);
    txt(s, String(v), { x:X(v) - 0.17, y:y + 0.38, w:0.34, h:0.34, fontSize:11, bold:true, color:C.white, align:'center' }, 'v:' + id + ':val' + i, k0 ? k0 + i : 0); });
  const stopK = k0 ? k0 + V.values.length : 0; rect(s, { x:X(V.stop) - 0.17, y:y + 0.38, w:0.34, h:0.34, fill:C.white, lineColor:C.red, lw:2, dash:'dash', shape:S.OVAL }, 'v:' + id + ':stopdot', stopK);
  txt(s, 'stop ' + V.stop + ' — never included', { x:X(V.stop) - 1.0, y:y - 0.02, w:2.0, h:0.28, fontSize:11, bold:true, color:C.red, align:'center' }, 'v:' + id + ':stop', stopK);
  txt(s, V.call + ' → ' + V.values.length + ' value' + (V.values.length === 1 ? '' : 's'), { x, y:y + 1.0, w, h:0.3, fontFace:M, fontSize:14, bold:true, color:C.navy, align:'center' }, 'v:' + id + ':call', 0); }
function pairsLanes(s, id, x, y, w, k0) { const V = VIS[id]; const top = V.swap ? V.right : V.left, bot = V.swap ? V.left : V.right; const n = Math.max(top.length, bot.length, V.pairs.length + 0); const cw = Math.min(1.0, (w - 0.4) / Math.max(n, 3)); const gap = cw * 0.35;
  const X = i => x + i * (cw + gap); const cell = (t, xx, yy, bad, name, kk) => { rect(s, { x:xx, y:yy, w:cw, h:0.5, fill:bad ? C.redBg : C.blueBg, lineColor:bad ? C.red : C.blue, lw:bad ? 2 : 1, dash:bad ? 'dash' : undefined, shape:S.ROUNDED_RECTANGLE, rectRadius:0.06 }, name + ':box', kk);
    txt(s, String(t), { x:xx, y:yy, w:cw, h:0.5, fontFace:M, fontSize:14, bold:true, color:bad ? C.red : C.navy, align:'center' }, name, kk); };
  top.forEach((t, i) => { const bad = i >= V.pairs.length && !V.swap ? true : (i >= V.pairs.length); cell(t, X(i), y, bad && V.pairs.length < top.length, 'v:' + id + ':top' + i, k0 ? k0 + i : 0); });
  bot.forEach((t, i) => { const bad = i >= V.pairs.length && bot.length > V.pairs.length; cell(t, X(i), y + 1.15, bad, 'v:' + id + ':bot' + i, k0 ? k0 + i : 0); });
  V.pairs.forEach((p, i) => { arrow(s, X(i) + cw / 2, y + 0.5, X(i) + cw / 2, y + 1.15, { color:C.green, w:2, noHead:true }, k0 ? k0 + i : 0);
    txt(s, V.reprs[i], { x:X(i) - 0.15, y:y + 0.66, w:cw + 0.3, h:0.28, fontFace:M, fontSize:11, bold:true, color:C.green, align:'center', fill:{ color:C.white } }, 'v:' + id + ':pair' + i, k0 ? k0 + i : 0); });
  if (V.error) txt(s, V.error, { x, y:y + 1.8, w, h:0.4, fontFace:M, fontSize:11.5, bold:true, color:C.red, align:'center' }, 'v:' + id + ':error', k0 ? k0 + n : 0);
  txt(s, V.call, { x, y:y + 2.25, w, h:0.3, fontFace:M, fontSize:13, bold:true, color:C.navy, align:'center' }, 'v:' + id + ':call'); }
const EVC = e => /break|else ran/.test(e) ? [C.redBg, C.red] : /continue/.test(e) ? [C.amberBg, C.amber] : /added|got it|found|body ran/.test(e) ? [C.greenBg, C.green] : [C.card, C.mute];
function traceTable(s, id, run, x, y, w, rowH, k0, fs) { const V = VIS[id], R = V.runs[run]; const cols = [['n', 'Pass', 0.6]].concat(V.watch.map((v, i) => ['v' + i, v, 1.1])); if (R.rows.some(r => r.cond !== null)) cols.push(['cond', 'Test', 0.9]);
  cols.push(['ev', 'What happens', 0]); cols.push(['out', 'Printed', 0]); const fixed = cols.reduce((a, c) => a + c[2], 0); const flex = cols.filter(c => c[2] === 0).length; cols.forEach(c => { if (c[2] === 0) c[2] = (w - fixed) / flex; });
  const cx = []; let acc = x; cols.forEach(c => { cx.push(acc); acc += c[2]; });
  cols.forEach((c, j) => { rect(s, { x:cx[j], y, w:c[2] - 0.04, h:0.34, fill:C.navy, lineColor:C.navy }); txt(s, c[1], { x:cx[j] + 0.06, y, w:c[2] - 0.16, h:0.34, fontSize:12, bold:true, color:C.white, fontFace:c[0].startsWith('v') ? M : B }); });
  R.rows.forEach((r, i) => { const yy = y + 0.38 + i * rowH; const cells = { n:String(r.n), cond:r.cond === null ? '' : (r.cond ? 'True' : 'False'), ev:r.events.join('; ') || (r.cond === false ? 'test false: loop ends' : ''), out:r.out };
    r.vals.forEach((v, j) => cells['v' + j] = v);
    cols.forEach((c, j) => { const isEv = c[0] === 'ev', bad = c[0] === 'cond' && r.cond === false; const col = isEv && r.events.length ? EVC(r.events[0]) : bad ? [C.redBg, C.red] : c[0] === 'cond' && r.cond ? [C.greenBg, C.green] : [C.card, C.ink];
      rect(s, { x:cx[j], y:yy, w:c[2] - 0.04, h:rowH - 0.05, fill:col[0], lineColor:col[0] }, 'cellbox', k0 ? k0 + i : 0);
      txt(s, cells[c[0]] || '', { x:cx[j] + 0.06, y:yy, w:c[2] - 0.16, h:rowH - 0.05, fontSize:fs || 11, color:col[1], bold:isEv || c[0] === 'cond', fontFace:(c[0].startsWith('v') || c[0] === 'out') ? M : B }, 'v:' + id + ':' + run + ':' + i + ':' + c[0], k0 ? k0 + i : 0); }); }); }
function passStrip(s, id, run, x, y, w, k0, label) { const V = VIS[id], R = V.runs[run]; const n = R.rows.length; const gap = 0.12; const bw = (w - gap * (n - 1)) / n; const bh = 1.35;
  if (label) txt(s, label, { x, y:y - 0.3, w, h:0.28, fontSize:12, bold:true, color:C.navy, fontFace:M }, 'stripcap');
  R.rows.forEach((r, i) => { const xx = x + i * (bw + gap); const ev = r.events.length ? r.events[r.events.length - 1] : ''; const col = ev ? EVC(ev) : [C.card, C.mute]; const last = i === n - 1; const kk = k0 ? k0 + i : 0;
    rect(s, { x:xx, y, w:bw, h:bh, fill:C.card, lineColor:last && /break|else/.test(ev) ? C.red : C.line, lw:last && /break|else/.test(ev) ? 2.5 : 1, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, 'passbox', kk);
    txt(s, 'pass ' + r.n, { x:xx + 0.08, y:y + 0.04, w:bw - 0.16, h:0.26, fontSize:11, bold:true, color:C.blue }, 'v:' + id + ':' + run + ':' + i + ':n', kk);
    R.rows[i].vals.forEach((v, j) => txt(s, V.watch[j] + ' = ' + v, { x:xx + 0.08, y:y + 0.3 + j * 0.24, w:bw - 0.16, h:0.24, fontFace:M, fontSize:10.5, color:C.ink }, 'v:' + id + ':' + run + ':' + i + ':v' + j, kk));
    const ey = y + 0.3 + V.watch.length * 0.24 + 0.05; rect(s, { x:xx + 0.06, y:ey, w:bw - 0.12, h:bh - (ey - y) - 0.06, fill:col[0], lineColor:col[0], shape:S.ROUNDED_RECTANGLE, rectRadius:0.05 }, 'evbox', kk);
    txt(s, r.events.join('; ') || 'reached the bottom', { x:xx + 0.1, y:ey, w:bw - 0.2, h:bh - (ey - y) - 0.06, fontSize:10.5, bold:true, color:col[1] }, 'v:' + id + ':' + run + ':' + i + ':ev', kk);
    if (i < n - 1) arrow(s, xx + bw, y + bh / 2, xx + bw + gap, y + bh / 2, { color:C.line, w:1.5 }, kk); }); }
function chapterMap(s, x, y, w, h, kBase) { const tops = PD.nodes.filter(n => n.level === 1); const cw = (w - 0.15 * (tops.length - 1)) / tops.length;
  tops.forEach((t, i) => { const xx = x + i * (cw + 0.15); const kk = kBase ? kBase + i : 0; rect(s, { x:xx, y, w:cw, h:0.62, fill:C.blue, lineColor:C.blue, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, 'map1', kk);
    txt(s, t.label, { x:xx, y, w:cw, h:0.62, fontFace:H, fontSize:14, bold:true, color:C.white, align:'center' }, 'map1t', kk);
    PD.nodes.filter(n => n.parent === t.id).forEach((m, j) => { const yy = y + 0.78 + j * 0.62; arrow(s, xx + cw / 2, y + 0.62, xx + cw / 2, yy, { color:C.line, w:1, noHead:true }, kk);
      rect(s, { x:xx + 0.05, y:yy, w:cw - 0.1, h:0.5, fill:C.blueBg, lineColor:C.blue, shape:S.ROUNDED_RECTANGLE, rectRadius:0.06 }, 'map2', kk);
      txt(s, m.label, { x:xx + 0.08, y:yy, w:cw - 0.16, h:0.5, fontSize:11.5, color:C.navy, align:'center', bold:true }, 'map2t', kk);
      PD.nodes.filter(n => n.parent === m.id).forEach((l, q) => { /* leaves listed in the notes, not drawn */ }); }); }); }

// =====================================================================================================================
// 1 Title
let s = dark(); rect(s, { x:0.6, y:1.2, w:1.2, h:0.8, fill:C.yellow, lineColor:C.yellow, shape:S.ROUNDED_RECTANGLE, rectRadius:0.12 });
txt(s, '>>>', { x:0.6, y:1.2, w:1.2, h:0.8, fontFace:M, fontSize:30, bold:true, color:C.navy, align:'center' });
txt(s, 'Chapter 3: Loops', { x:0.6, y:2.2, w:8.8, h:0.9, fontFace:H, fontSize:38, bold:true, color:C.white });
txt(s, 'How a program does the same work again — until a condition says stop', { x:0.6, y:3.05, w:8.8, h:0.5, fontSize:18, italic:true, color:C.yellow });
txt(s, 'SEN0414 Advanced Programming · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University', { x:0.6, y:4.6, w:8.8, h:0.4, fontSize:13, color:'C9D4E0' });
note(s, 'Welcome. Today is about repetition, the idea that makes programs worth writing: a computer does the same thing again without getting bored. We follow the book’s chapter 3 (Sweigart, 2025), and where the language has moved on we say so. Every result on these slides was produced by running it under Python ' + py + ', and the traces you will see were recorded by a real run, pass by pass. Same material as the chapter 3 interactive page; the diagrams on the slides are the diagrams on the page.');

// 2 Hook
s = dark(); txt(s, 'How does a program ask again — and again — until it gets an answer it can use?', { x:0.7, y:1.0, w:8.6, h:1.6, fontFace:H, fontSize:32, bold:true, color:C.white, valign:'top' });
txt(s, 'Think of a login that says “wrong password, try again”, or a form that will not submit until the field is filled in.', { x:0.7, y:3.0, w:8.6, h:0.9, fontSize:18, italic:true, color:C.yellow, valign:'top' }, 'say', 1);
txt(s, 'That “again” is a loop.', { x:0.7, y:4.3, w:8.6, h:0.6, fontFace:H, fontSize:26, bold:true, color:C.white }, 'say', 2);
note(s, 'Start with something everyone has met. You type a password wrong; the page says try again; you do. Nobody wrote the login page a thousand times, they wrote it once and told the computer to come back. Click once for the everyday examples and once for the punchline: that “again” is what today’s chapter names. Ask the room for one more example before moving on (a game that restarts, a download that retries).');

// 3 Map
s = light(); title(s, 'Two families of loops, and what surrounds them', 'The five parts of the chapter, as the course’s own ontology draws them');
chapterMap(s, 0.5, 1.45, 9, 3.0, 0);
txt(s, 'Repetition comes as a condition loop or a counted loop; everything else supports it — the sequences to iterate over, the ways out, the modules, and current practice.', { x:0.5, y:4.6, w:9, h:0.7, fontSize:14, color:C.ink, valign:'top' });
note(s, 'This is the map of the chapter, drawn from the chapter’s ontology, the same tree the interactive page uses. Repetition splits into condition loops (while) and counted loops (for). Sequence covers range and the two helpers enumerate and zip. Loop control is break, continue, the loop else and sys.exit. Module is how you reach the library, and modern practice pairs the book’s loops with what current Python offers and with two hazards the documentation names. Tell the class: by the end they should be able to choose the right loop for a job, and to predict what it will do.');

// 4 while - flow
s = light(); title(s, 'A while loop asks its question again after every pass', 'The condition is tested at the top each time round');
const fx = 0.7, fy = 1.5;
rect(s, { x:fx, y:fy, w:1.9, h:0.55, fill:C.card, lineColor:C.line, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'flow0', 1); txt(s, 'code before the loop', { x:fx, y:fy, w:1.9, h:0.55, fontSize:12, align:'center' }, 'flow0t', 1);
arrow(s, fx + 0.95, fy + 0.55, fx + 0.95, fy + 1.05, {}, 1);
rect(s, { x:fx - 0.05, y:fy + 1.05, w:2.0, h:1.05, fill:C.amberBg, lineColor:C.amber, lw:2, shape:S.DIAMOND }, 'flowd', 1); txt(s, 'condition\ntrue?', { x:fx - 0.05, y:fy + 1.05, w:2.0, h:1.05, fontSize:13, bold:true, color:C.amber, align:'center' }, 'flowdt', 1);
arrow(s, fx + 1.95, fy + 1.575, fx + 3.05, fy + 1.575, { color:C.green }, 2); txt(s, 'yes', { x:fx + 2.1, y:fy + 1.25, w:0.7, h:0.28, fontSize:12, bold:true, color:C.green, align:'center' }, 'yes', 2);
rect(s, { x:fx + 3.05, y:fy + 1.3, w:2.1, h:0.55, fill:C.greenBg, lineColor:C.green, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'flowb', 2); txt(s, 'run the block', { x:fx + 3.05, y:fy + 1.3, w:2.1, h:0.55, fontSize:13, bold:true, color:C.green, align:'center' }, 'flowbt', 2);
arrow(s, fx + 4.1, fy + 1.3, fx + 4.1, fy + 0.6, { color:C.green, noHead:true }, 3); arrow(s, fx + 4.1, fy + 0.6, fx + 0.95, fy + 0.6, { color:C.green, noHead:true }, 3); arrow(s, fx + 0.95, fy + 0.6, fx + 0.95, fy + 1.05, { color:C.green }, 3); txt(s, 'jump back to the test', { x:fx + 1.6, y:fy + 0.28, w:2.4, h:0.28, fontSize:12, italic:true, color:C.green, align:'center' }, 'back', 3);
arrow(s, fx + 0.95, fy + 2.1, fx + 0.95, fy + 2.75, { color:C.red }, 4); txt(s, 'no', { x:fx + 1.05, y:fy + 2.2, w:0.6, h:0.28, fontSize:12, bold:true, color:C.red }, 'no', 4);
rect(s, { x:fx, y:fy + 2.75, w:1.9, h:0.55, fill:C.redBg, lineColor:C.red, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'flowe', 4); txt(s, 'code after the loop', { x:fx, y:fy + 2.75, w:1.9, h:0.55, fontSize:12, bold:true, color:C.red, align:'center' }, 'flowet', 4);
card(s, 6.4, 1.5, 3.1, 1.75, 'Unlike if', 'An if block runs once or not at all. A while block sends execution back to the top, so how many times it runs depends on the data, not on a count.', C.blue);
say(s, '“A while statement repeats its block as long as its condition is true, and tests the condition again after every pass.”', 6.4, 3.45, 3.1, 1.3, { italic:true, fontSize:12, color:C.mute });
note(s, 'Build the picture in four clicks. One: the code before the loop, then the diamond: the test. Two: if the test is true the block runs. Three: and here is the difference from if: execution jumps back to the test. Four: only when the test is false do we leave, to the code after the loop. The point to land: the number of passes is not written in the code, it is decided by the data. The reference says it in one line (Python Software Foundation, 2026). Ask: what would happen if the block never changed anything the test looks at? (that sets up the infinite loop two slides on).');

// 5 predict
s = light(); title(s, 'Predict first: how many times does the block run?', 'The user types no, then maybe, then yes');
prog(s, 'waiting_v1_0_0.py', 0.5, 1.45, 4.4, 1.75, 15); trans(s, 'waiting_v1_0_0.py', [0], 5.2, 1.45, 4.3, 1.75, 14, 2);
say(s, 'Before you click: how many times does input() run, and what is answer when the loop ends? Write it down.', 0.5, 3.55, 9, 0.7, { fontSize:16, bold:true, color:C.navy });
rect(s, { x:0.5, y:4.3, w:9, h:0.85, fill:C.greenBg, lineColor:C.green, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'ans', 1);
txt(s, 'Three times. answer is ‘yes’, and the test is what stopped the loop — the body never ran a fourth time.', { x:0.7, y:4.3, w:8.6, h:0.85, fontSize:15, bold:true, color:C.green }, 'anst', 1);
note(s, 'Prediction before explanation is one of the most reliable teaching moves there is: a student who has committed to an answer pays attention to whether it was right. Give them thirty seconds; take two or three answers. First click reveals the answer; second click reveals the real run beside the code. The trick is that the test happens before each pass, so with the third input the body runs and only afterwards does the test see ‘yes’. Program written for this course; run under Python ' + py + ' with the inputs shown.');

// 6 trace while
s = light(); title(s, 'Trace it: the test is evaluated before every pass', 'One row per test of the condition — recorded from a real run');
traceTable(s, 'WhileStatement', 0, 0.5, 1.4, 9, 0.5, 1, 12);
say(s, VIS.WhileStatement.caption + ' The last row is the one that ends the loop: the test is false, so the block is skipped and the next statement runs.', 0.5, 4.2, 9, 0.9, { fontSize:14 });
note(s, 'Trace tables are how you debug in your head, and how professionals reason about loops. Click through the rows: answer starts empty, so the test is true; each pass reads a new answer. Row four is the point: answer is ‘yes’, the test is false, the block does not run, and ‘Starting’ is printed. This trace was recorded by a line tracer running the program on the slide under Python ' + py + ' (08-tooling/ch03-deck/visuals_make_v1_0_0.py); the same specification is drawn in the interactive page.');

// 7 infinite / while True
s = light(); title(s, 'An endless loop is a bug — unless you built the exit', 'while True: is deliberate; every way out has a name');
rect(s, { x:3.7, y:2.3, w:2.6, h:0.9, fill:C.navy, lineColor:C.navy, shape:S.ROUNDED_RECTANGLE, rectRadius:0.12 }); txt(s, 'while True:', { x:3.7, y:2.3, w:2.6, h:0.9, fontFace:M, fontSize:20, bold:true, color:C.yellow, align:'center' });
const exits = [['break', 'leave this loop', 0.5, 1.4], ['return', 'leave the function', 0.5, 3.4], ['sys.exit()', 'end the program', 7.0, 1.4], ['an exception', 'unwind to a handler', 7.0, 3.4]];
exits.forEach(([a, b, xx, yy], i) => { rect(s, { x:xx, y:yy, w:2.5, h:0.85, fill:C.redBg, lineColor:C.red, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'exit', i + 1); txt(s, [{ text:a, options:{ fontFace:M, bold:true, fontSize:16, color:C.red, breakLine:true } }, { text:b, options:{ fontSize:12, color:C.ink } }], { x:xx + 0.1, y:yy, w:2.3, h:0.85, align:'center' }, 'exitt', i + 1);
  arrow(s, xx < 5 ? xx + 2.5 : xx, yy + 0.42, xx < 5 ? 3.7 : 6.3, yy < 2 ? 2.55 : 2.95, { color:C.red }, i + 1); });
txt(s, 'Stuck in one you did not mean? Control-C raises KeyboardInterrupt.', { x:0.5, y:4.75, w:9, h:0.4, fontSize:14, italic:true, color:C.mute, align:'center' });
note(s, 'If the condition never becomes false the program keeps going forever, a common programming bug (Sweigart, 2025). But while True: written on purpose is a standard pattern: you put the exit inside the loop where the decision is made. There are four ways out, one per click: break leaves this loop, return leaves the whole function, sys.exit() ends the program, and an exception unwinds until something handles it (Python Software Foundation, 2026). If you are stuck in one you did not mean, Control-C. Warn them: they will write an accidental infinite loop this semester, and that is normal.');

// 8 Which loop
s = light(); title(s, 'Choosing a loop: do you know what to loop over?', 'A counted loop knows its length before it starts; a condition loop does not');
rect(s, { x:2.9, y:1.4, w:4.2, h:0.75, fill:C.navy, lineColor:C.navy, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }); txt(s, 'Do you have the sequence — or the count — up front?', { x:3.0, y:1.4, w:4.0, h:0.75, fontSize:14, bold:true, color:C.white, align:'center' });
arrow(s, 3.6, 2.15, 2.2, 2.75, { color:C.green }, 1); arrow(s, 6.4, 2.15, 7.8, 2.75, { color:C.amber }, 2);
txt(s, 'yes', { x:2.1, y:2.3, w:0.6, h:0.3, fontSize:13, bold:true, color:C.green }, 'yes', 1); txt(s, 'no — the data decides', { x:7.0, y:2.3, w:2.4, h:0.3, fontSize:13, bold:true, color:C.amber }, 'no', 2);
rect(s, { x:0.5, y:2.75, w:3.8, h:1.6, fill:C.greenBg, lineColor:C.green, lw:2, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'for', 1);
txt(s, [{ text:'for', options:{ fontFace:M, bold:true, fontSize:22, color:C.green, breakLine:true } }, { text:'a counted loop: one pass per item', options:{ fontSize:13, color:C.ink, breakLine:true } }, { text:'for i in range(5):', options:{ fontFace:M, fontSize:13, color:C.navy } }], { x:0.6, y:2.8, w:3.6, h:1.5, align:'center' }, 'fort', 1);
rect(s, { x:5.7, y:2.75, w:3.8, h:1.6, fill:C.amberBg, lineColor:C.amber, lw:2, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'while', 2);
txt(s, [{ text:'while', options:{ fontFace:M, bold:true, fontSize:22, color:C.amber, breakLine:true } }, { text:'a condition loop: repeat while a test holds', options:{ fontSize:13, color:C.ink, breakLine:true } }, { text:'while answer != ‘yes’:', options:{ fontFace:M, fontSize:13, color:C.navy } }], { x:5.8, y:2.8, w:3.6, h:1.5, align:'center' }, 'whilet', 2);
txt(s, 'Need the position as well as the item? enumerate. Two sequences side by side? zip.', { x:0.5, y:4.6, w:9, h:0.5, fontSize:14, italic:true, color:C.mute, align:'center' }, 'more', 3);
note(s, 'This is the decision students actually face at the keyboard, so give it a slide of its own. If you can say in advance what you are looping over, or how many times, use for: the loop’s length is known before it starts. If it depends on something that changes while the program runs, such as an answer typed in, use while. The two families are drawn from the chapter’s ontology: a counted loop “runs its block once for each item of a sequence”, a condition loop “repeats as long as an expression is true” (Sweigart, 2025). Third click: the two helpers that replace most index arithmetic.');

// 9 for anatomy
s = light(); title(s, 'A for loop hands out one item per pass', 'Three things happen, in this order');
const steps = [['1', 'Evaluate the iterable — once', 'for i in range(5)  →  the sequence is worked out a single time'], ['2', 'Make an iterator from it', 'the iterator remembers where it is'], ['3', 'Assign the next item, run the block, repeat', 'until the iterator has nothing left']];
steps.forEach(([n, a, b], i) => { const yy = 1.5 + i * 1.05; rect(s, { x:0.5, y:yy, w:0.7, h:0.7, fill:C.blue, lineColor:C.blue, shape:S.OVAL }, 'stepn', i + 1); txt(s, n, { x:0.5, y:yy, w:0.7, h:0.7, fontFace:H, fontSize:22, bold:true, color:C.white, align:'center' }, 'stepnt', i + 1);
  txt(s, [{ text:a, options:{ bold:true, fontSize:17, color:C.navy, breakLine:true } }, { text:b, options:{ fontSize:13, color:C.mute, italic:true } }], { x:1.45, y:yy - 0.05, w:5.0, h:0.8 }, 'stept', i + 1); });
prog(s, 'forsum_v1_0_0.py', 6.6, 1.5, 2.9, 1.5, 14); trans(s, 'forsum_v1_0_0.py', [0], 6.6, 3.25, 2.9, 0.7, 14);
say(s, 'Assigning to i inside the block does not change the loop: the next pass takes the next item regardless.', 6.6, 4.25, 2.9, 0.9, { fontSize:12, italic:true, color:C.mute });
note(s, 'Many students think a for loop counts. It does not: it hands out items. The reference says: a for statement evaluates its iterable once, makes an iterator from it, assigns each item to the target in turn and runs the block (Python Software Foundation, 2026). One click per step. The little program on the right adds 1, 2 and 3 and prints 6; the next slide traces it. And a fact worth a demonstration: assigning to the loop variable inside the block does not change the loop.');

// 10 for trace
s = light(); title(s, 'Trace it: each pass assigns the target a fresh item', 'n takes 1, 2, 3; total grows to 6');
traceTable(s, 'ForStatement', 0, 0.5, 1.4, 9, 0.6, 1, 13);
say(s, VIS.ForStatement.caption + ' The loop ended because range(1, 4) had nothing left — no test was ever written.', 0.5, 3.9, 9, 0.9, { fontSize:14 });
note(s, 'Compare this trace with the while trace two slides back. There the condition decided; here the iterator decides. Values are shown as the block starts on each pass: n has just been assigned, total is what it was before the pass adds n. The last value, total = 6, is what the program prints. Recorded by the same line tracer under Python ' + py + '.');

// 11 range 1 arg
s = light(); title(s, 'range(5) makes five values — and never reaches 5', 'The end is never part of the sequence');
numberLine(s, 'RangeStop', 0.8, 1.6, 8.4, 1);
say(s, 'One argument: start at 0, stop before the argument. Count the dots: five values, because the counting starts at 0.', 0.5, 3.4, 9, 0.7, { fontSize:16 });
card(s, 0.5, 4.1, 9, 1.05, 'The mistake to avoid', 'Expecting range(5) to include 5. It never does — the hollow marker is where the sequence stops, not a value in it.', C.red, 7);
note(s, 'Draw the number line and click through the dots: 0, 1, 2, 3, 4. The hollow red circle at 5 is where it stops, and it never joins the sequence (Sweigart, 2025). This is the single most common range mistake, so give it its own card. The dots and values are not typed: they are what list(range(5)) returned under Python ' + py + '.');

// 12 range variants
s = light(); title(s, 'Two and three arguments move the start and the step', 'start, stop, step — and a negative step counts down');
['RangeStartStop', 'RangeStep', 'RangeDescending'].forEach((id, i) => numberLine(s, id, 0.8, 1.3 + i * 1.3, 8.4, 0));
note(s, 'Three number lines, all from real calls. With two arguments the first is where you start: range(12, 16) gives 12 to 15. A third argument is the step: range(0, 10, 2) gives the even numbers below 10. A negative step counts down, and the stop is still excluded: range(5, -1, -1) gives 5 down to 0, which is why you write -1 as the stop to include 0. Also point out that range(10), range(0, 10) and range(0, 10, 1) give the same values, which is one of the book’s practice questions.');

// 13 lazy
s = light(); title(s, 'A range is a recipe, not a list', 'It produces each value when the loop asks for it');
codeCard(s, EX.lazy, 0.5, 1.45, 4.4, 1.5, 17); codeCard(s, EX.same, 0.5, 3.4, 9, 0.95, 15);
rect(s, { x:5.2, y:1.45, w:4.3, h:1.5, fill:C.card, lineColor:C.card, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 });
txt(s, [{ text:'A list is the dishes on the table.', options:{ bold:true, color:C.navy, breakLine:true, fontSize:15 } }, { text:'A range is the recipe: it cooks each dish only when asked, so it takes almost no room.', options:{ fontSize:14, color:C.ink } }], { x:5.4, y:1.5, w:3.9, h:1.4, valign:'top' }, 'analogy');
say(s, 'Printing a range shows range(0, 10), not the numbers. It is still iterable, so sum() and for accept it.', 0.5, 4.75, 9, 0.5, { fontSize:13, italic:true, color:C.mute });
note(s, 'The reference says a range behaves like a list in many ways but is not one: it returns the successive items as you iterate, which saves space (Python Software Foundation, 2026). Analogy for the room: a list is all the dishes already on the table, a range is the recipe that makes each dish when someone asks. Show the first card: printing range(10) does not show ten numbers. Show the second card: a range of a million costs almost nothing until you use it, yet sum(range(4)) works because it is iterable. The last line is the book’s practice question 3.');

// 14 enumerate
s = light(); title(s, 'enumerate hands you the position with the item', 'Instead of range(len(a)) and an index');
pairsLanes(s, 'EnumerateFunction', 0.8, 1.45, 5.4, 1);
codeCard(s, EX.enum, 6.4, 1.45, 3.1, 2.0, 11);
card(s, 0.5, 4.25, 9, 0.95, 'Why it matters', 'The tutorial prefers enumerate to combining range and len when both the position and the item are needed — one call, no index arithmetic, no off-by-one.', C.blue, 5);
note(s, 'Here the top lane is the running count, the bottom lane is the items, and each green link is one pair enumerate hands to the loop. The tutorial prefers it to combining range and len (Python Software Foundation, 2026). Ask the class to say what the code would look like without it, and note how many places an off-by-one could hide. The pairs shown are what list(enumerate([‘tic’, ‘tac’, ‘toe’])) returned under Python ' + py + '.');

// 15 zip
s = light(); title(s, 'zip pairs items up — and stops at the shortest', 'The leftover item disappears without a word');
pairsLanes(s, 'ZipStrict', 0.8, 1.45, 5.4, 1);
codeCard(s, EX.zip.slice(0, 2), 6.4, 1.45, 3.1, 1.6, 11);
card(s, 0.5, 4.25, 9, 0.95, 'Silent truncation', 'The c has no partner and is dropped with no warning. That is exactly the bug strict=True exists to catch — next slide.', C.amber, 4);
note(s, 'Two lanes, two sequences: ‘abc’ and [1, 2]. zip pairs them up as far as it can and stops at the shortest: the c has no partner and is quietly dropped (Bucher, 2020). Silent behaviour like this is where data bugs live: two lists that should have been the same length and were not. Set up the question for the next slide: how would you make Python tell you?');

// 16 strict
s = light(); title(s, 'strict=True turns a silent mistake into an error', 'Since Python 3.10 — loud is better than wrong');
pairsLanes(s, 'ZipStrictError', 0.8, 1.35, 5.4, 1);
codeCard(s, [EX.zip[2]], 6.4, 1.45, 3.1, 1.3, 11);
card(s, 0.5, 4.25, 9, 0.95, 'When to use it', 'Whenever the two sequences are supposed to be the same length. The error appears where the data went wrong, not three functions later.', C.green, 5);
note(s, 'Same inputs, one keyword. With strict=True, zip raises ValueError when the lengths differ (Bucher, 2020), since Python 3.10. The message on the slide is what Python ' + py + ' printed. Discussion prompt: when would you rather have the silent version? (Almost never: only when truncation is the intended behaviour, and then say so in a comment.)');

// 17 break/continue strip
s = light(); title(s, 'break leaves the loop; continue skips one pass', 'The same run, pass by pass: 5, x, 7, then a blank line');
passStrip(s, 'BreakStatement', 0, 0.5, 1.6, 9, 1);
prog(s, 'summing_v1_0_0.py', 0.5, 3.15, 4.75, 2.05, 10); trans(s, 'summing_v1_0_0.py', [0], 5.4, 3.15, 4.1, 1.0, 10.5, 5);
say(s, 'x fails isdigit(), so continue skips the adding. The blank entry reaches break: the loop ends, and the total is 12.', 5.4, 4.55, 4.1, 0.65, { fontSize:12, color:C.ink }, 5);
note(s, 'Click through the four passes. Pass one adds 5. Pass two: ‘x’ is not a digit, so continue skips the rest of the block and goes back for the next entry. Pass three adds 7. Pass four: the blank entry hits break and the loop ends with total 12. Everything on the strip was recorded by tracing the program shown (swordfish.py in the book uses continue the same way). break ends the innermost enclosing loop at once; continue skips the rest of the block (Sweigart, 2025; Python Software Foundation, 2026).');

// 18 for else
s = light(); title(s, 'The loop else runs only when no pass reached break', 'Two runs of one search: found, and not found');
prog(s, 'searching_v1_0_0.py', 0.5, 1.4, 3.9, 2.15, 12); trans(s, 'searching_v1_0_0.py', [0, 1], 0.5, 3.8, 3.9, 1.35, 11);
passStrip(s, 'LoopElseClause', 0, 4.65, 1.75, 4.85 * 2 / 3, 1, 'find ‘dog’');
passStrip(s, 'LoopElseClause', 1, 4.65, 3.5, 4.85, 3, 'find ‘fish’');
say(s, 'Read the else as “searched everything, found nothing”. A break skips it.', 4.65, 4.95, 4.85, 0.45, { fontSize:12, italic:true, color:C.mute }, 4);
note(s, 'The else on a loop is one of Python’s best-kept secrets and one of its worst-named features: read it as “no break”. Top strip: the search finds dog on pass two, break fires, and the else is skipped. Bottom strip: fish is never found, no pass reaches break, the loop finishes, and the else runs. It is the tidy replacement for a found flag (Python Software Foundation, 2026). Note it is skipped by a break, a return or a raised exception.');

// 19 loop variable
s = light(); title(s, 'The loop variable outlives the loop', 'After for i in range(3), i is still there — and holds 2');
traceTable(s, 'LoopVariableScope', 0, 0.5, 1.4, 5.2, 0.5, 1, 13);
prog(s, 'loopvar_v1_0_0.py', 6.0, 1.4, 3.5, 1.75, 12.5); trans(s, 'loopvar_v1_0_0.py', [0], 6.0, 3.4, 3.5, 0.85, 14);
card(s, 0.5, 4.1, 5.2, 1.1, 'Two facts from the reference', 'The name is not deleted when the loop ends; after a loop over an empty sequence it was never assigned.', C.blue, 4);
note(s, 'The trace shows i taking 0, 1, 2. The program’s last line prints 2: names in a for statement’s target list are not deleted when the loop ends (Python Software Foundation, 2026). The flip side, which the reference also states, is that after a loop over an empty sequence the name was never assigned at all. Useful and dangerous in equal measure: it is why code that uses the loop variable after the loop can work on the test data and break on empty input.');

// 20 sys.exit
s = light(); title(s, 'sys.exit() ends a program by raising an exception', 'So it can be intercepted — and finally clauses still run');
prog(s, 'quitting_v1_0_0.py', 0.5, 1.45, 4.4, 2.1, 14); trans(s, 'quitting_v1_0_0.py', [0], 5.2, 1.45, 4.3, 2.1, 14);
card(s, 0.5, 3.95, 9, 1.2, 'An exception, not a hard stop', 'sys.exit() raises SystemExit. It ends the program only when nothing intercepts it, and only from the main thread. An argument of None or 0 means success; a string is printed to standard error.', C.blue, 1);
note(s, 'Type exit and the loop is left, and the program ends. But the mechanism is an exception, SystemExit, which is why finally clauses still run and why an outer handler can intercept it (Python Software Foundation, 2026). Tell them: this is also why sys.exit() inside a thread does not stop the program.');

// 21 worked example
s = light(); title(s, 'Putting it together: guess the number in three attempts', 'A counted loop, an early exit, and a loop else');
prog(s, 'guessing_v1_0_0.py', 0.5, 1.35, 4.7, 3.4, 11); trans(s, 'guessing_v1_0_0.py', [0, 1], 5.4, 1.35, 4.1, 3.4, 11);
say(s, 'The seed makes the secret repeatable for the slide; a real game would not seed it.', 0.5, 4.85, 9, 0.3, { fontSize:11, italic:true, color:C.mute });
note(s, 'Give them a minute to read the program before anything else, and ask: which lines are the counted loop, which is the early exit, which is the else? The loop is counted, for attempt in range(1, 4), so at most three tries. The if chain gives hints, break leaves on success, and the else clause handles the case where all three attempts fail, replacing the found flag from the book. Two real runs are on the right: a win on the third attempt, and three misses. The seed makes the secret repeatable for the slide; a real game would not seed it. Next slide: what each pass did.');

s = light(); title(s, 'Trace both runs: the last pass decides how the loop ends', 'A win on attempt 3, then three misses that reach the else');
traceTable(s, 'GuessLoop', 0, 0.5, 1.4, 9, 0.5, 1, 11);
txt(s, 'Second run — every guess too low:', { x:0.5, y:3.5, w:9, h:0.3, fontSize:12, bold:true, color:C.navy });
passStrip(s, 'GuessLoop', 1, 0.5, 3.9, 9, 0, null);
note(s, 'A worked example that uses everything so far. The loop is counted, for attempt in range(1, 4), so at most three tries. The if chain gives hints, break leaves on success, and the else clause handles the case where all three attempts fail, replacing the found flag from the book. Top: the run where the third guess is right, break fires. Bottom: the run where all three fail and the else ran (the else’s message is on the last pass). The seed makes the secret repeatable for the slide; a real game would not seed it.');

// 22 modules hook
s = dark(); txt(s, 'Where do random.randint() and sys.exit() come from?', { x:0.7, y:1.3, w:8.6, h:1.3, fontFace:H, fontSize:32, bold:true, color:C.white, valign:'top' });
txt(s, 'From modules — and there is more than one way to reach into them. Some are better than others.', { x:0.7, y:3.2, w:8.6, h:1.0, fontSize:20, italic:true, color:C.yellow, valign:'top' }, 'say', 1);
note(s, 'A program reaches the standard library’s functions by importing the module that holds them (Sweigart, 2025). We have been writing import random and import sys without discussing what they do. Three forms, one style guide. Ask: which do you think is best?');

// 23 imports
s = light(); title(s, 'Import the module: every name shows where it came from', 'Three forms — and what PEP 8 says about each');
const imps = [['import random', 'random.randint(1, 10)', 'Names stay under the module’s name.', 'the clear form', C.green, C.greenBg], ['import random, sys, os', 'one line, three modules', 'Legal, and the book uses it.', 'PEP 8: usually separate lines', C.amber, C.amberBg], ['from random import *', VIS.StarImport.count + ' names, no prefix', 'Every public name arrives with nothing to say where it came from.', 'book and PEP 8: avoid', C.red, C.redBg]];
imps.forEach(([a, b, c, d, col, bg], i) => { const xx = 0.5 + i * 3.05; rect(s, { x:xx, y:1.5, w:2.9, h:2.1, fill:bg, lineColor:col, lw:2, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'imp', i + 1);
  txt(s, [{ text:a, options:{ fontFace:M, bold:true, fontSize:14, color:col, breakLine:true } }, { text:b, options:{ fontFace:M, fontSize:12, color:C.navy, breakLine:true } }, { text:' ', options:{ fontSize:6, breakLine:true } }, { text:c, options:{ fontSize:13, color:C.ink, breakLine:true } }, { text:' ', options:{ fontSize:6, breakLine:true } }, { text:d, options:{ fontSize:13, bold:true, color:col } }], { x:xx + 0.15, y:1.55, w:2.6, h:2.0, valign:'top' }, i === 2 ? 'v:StarImport:count' : 'impt', i + 1); });
txt(s, 'random.__all__ holds ' + VIS.StarImport.count + ' names under Python ' + py + '; a star import would drop all of them into your program.', { x:0.5, y:3.85, w:9, h:0.6, fontSize:14, italic:true, color:C.mute, align:'center' }, 'v:StarImport:note', 4);
note(s, 'A traffic light for import styles. Green: import random keeps every name under its module, so random.randint tells the reader where it came from. Amber: importing several modules on one line is legal and the book does it, but PEP 8 says imports should usually be on separate lines (Van Rossum et al., 2001). Red: from random import * removes the prefix; the book itself concludes that the full name makes for more readable code (Sweigart, 2025), and PEP 8 says wildcard imports should be avoided because they make it unclear which names are present. The count on the card is len(random.__all__) under Python ' + py + '. Third click: how many names that is.');

// 24 walrus
s = light(); title(s, 'An assignment expression reads and tests in one line', 'Same behaviour, four lines shorter — Python 3.8');
txt(s, 'Before', { x:0.5, y:1.3, w:4.4, h:0.3, fontSize:14, bold:true, color:C.mute }); prog(s, 'chunks_old_v1_0_0.py', 0.5, 1.65, 4.4, 2.0, 12); trans(s, 'chunks_old_v1_0_0.py', [0], 0.5, 3.9, 4.4, 1.05, 12);
txt(s, 'After — with :=', { x:5.1, y:1.3, w:4.4, h:0.3, fontSize:14, bold:true, color:C.blue }); prog(s, 'chunks_v1_0_0.py', 5.1, 1.65, 4.4, 1.2, 13, 1); trans(s, 'chunks_v1_0_0.py', [0], 5.1, 3.9, 4.4, 1.05, 12, 1);
say(s, ':= names the value inside the condition. PEP 572’s own example: while chunk := file.read(8192).', 5.1, 3.0, 4.4, 0.8, { fontSize:12, italic:true, color:C.mute }, 1);
note(s, 'Both programs print the same three lines; check the transcripts underneath. The left one is the while True: pattern from earlier: read, test, break. The right one uses an assignment expression, added in Python 3.8 (Angelico et al., 2018): := names the value inside the condition, so the loop reads and tests in one line. PEP 572 uses while chunk := file.read(8192) as its own example of a loop that cannot be trivially rewritten with the two-argument iter(). A style you will see in modern code; you are not required to like it.');

// 25 hazards
s = light(); title(s, 'Two hazards: editing what you iterate, and leaving finally', 'Both named by the reference documentation');
prog(s, 'copying_v1_0_0.py', 0.5, 1.45, 4.6, 2.0, 12); trans(s, 'copying_v1_0_0.py', [0], 5.4, 1.45, 4.1, 1.0, 13);
card(s, 0.5, 3.75, 4.45, 1.4, 'Modifying while iterating', 'Tricky to get right. Loop over a copy — .copy().items() — or build a new collection.', C.red, 1);
card(s, 5.05, 3.75, 4.45, 1.4, 'New in Python 3.14', 'A return, break or continue that leaves a finally block now draws a SyntaxWarning (PEP 765).', C.amber, 2);
note(s, 'Two hazards, one click each. First: deleting from a dictionary while looping over it is tricky to get right, so the tutorial’s remedy is to loop over a copy, exactly what users.copy().items() does in the program on the slide, or to build a new collection (Python Software Foundation, 2026). Second: since Python 3.14, a return, break or continue that leaves a finally block draws a SyntaxWarning, per PEP 765 (Katriel and Coghlan, 2024). Reproduced under Python ' + py + '.');

// 26 recap map
s = light(); title(s, 'What you can do now', 'The chapter on one page — pick the loop, trace it, exit it, import into it');
const can = [['Choose', 'for when you know the sequence, while when the data decides'], ['Predict', 'the values range() makes, and why a range is not a list'], ['Trace', 'a loop pass by pass, including break, continue and the loop else'], ['Import', 'by module name, the way PEP 8 recommends']];
can.forEach(([a, b], i) => { const yy = 1.45 + i * 0.9; rect(s, { x:0.5, y:yy, w:1.5, h:0.7, fill:C.blue, lineColor:C.blue, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }); txt(s, a, { x:0.5, y:yy, w:1.5, h:0.7, fontFace:H, fontSize:18, bold:true, color:C.white, align:'center' }); txt(s, b, { x:2.2, y:yy, w:7.3, h:0.7, fontSize:16 }); });
note(s, 'Close the loop on the hook: how does a program ask again until it gets an answer? A while loop with a test, or a for loop over the attempts, with break when the answer is good. Four verbs to leave with: choose, predict, trace, import. Those match the chapter’s learning objectives on the interactive page.');

// 27 check yourself
s = light(); title(s, 'Check yourself: answer aloud, then click', 'Retrieval beats re-reading');
const qa = [['What stops a program stuck in an infinite loop?', 'Control-C — it raises KeyboardInterrupt.'], ['break versus continue?', 'break leaves the loop; continue skips to the next pass.'], ['range(10), range(0, 10), range(0, 10, 1)?', 'The same values.'], ['When does a loop’s else run?', 'When the loop finishes without a break.'], ['What does zip(a, b, strict=True) add?', 'A ValueError when the lengths differ.']];
qa.forEach(([q, a], i) => { const yy = 1.35 + i * 0.75; rect(s, { x:0.5, y:yy + 0.04, w:0.46, h:0.46, fill:C.yellow, lineColor:C.yellow, shape:S.OVAL }); txt(s, String(i + 1), { x:0.5, y:yy + 0.04, w:0.46, h:0.46, fontFace:H, fontSize:15, bold:true, color:C.navy, align:'center' });
  txt(s, q, { x:1.1, y:yy, w:4.6, h:0.54, fontSize:14 }); rect(s, { x:5.8, y:yy + 0.02, w:3.7, h:0.5, fill:C.greenBg, lineColor:C.green, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, 'a', i + 1); txt(s, a, { x:5.9, y:yy + 0.02, w:3.5, h:0.5, fontSize:12, bold:true, color:C.green }, 'at', i + 1); });
note(s, 'Answer aloud first, then click. Questions 1 to 3 follow the book’s practice questions; the rest test what we added. The interactive page has a quiz with a rationale for each wrong answer, so send them there before next week.');

// 28 sources
s = light(); title(s, 'Sources', 'Every claim beyond the book is recorded in the chapter’s research record');
const src = ['Sweigart, A. (2025). Automate the Boring Stuff with Python, 3rd ed., ch. 3. No Starch Press. automatetheboringstuff.com/3e', 'Python Software Foundation (2026). Python 3.14 documentation: Tutorial 4 and 5; Language Reference 8; Built-in Functions; sys; Built-in Exceptions; What’s New in 3.14', 'Angelico, C., Peters, T. and van Rossum, G. (2018). PEP 572 – Assignment Expressions', 'Van Rossum, G., Warsaw, B. and Coghlan, N. (2001). PEP 8 – Style Guide for Python Code', 'Katriel, I. and Coghlan, N. (2024). PEP 765 – Disallow return/break/continue that exit a finally block', 'Bucher, C. (2020). PEP 618 – Add Optional Length-Checking To zip'];
txt(s, src.map((t, i) => ({ text:t, options:{ bullet:true, breakLine:i < src.length - 1 } })), { x:0.5, y:1.4, w:9, h:3.4, fontSize:12, valign:'top', paraSpaceAfter:6 });
txt(s, 'Slides adapt Automate the Boring Stuff with Python (CC BY-NC-SA). See NOTICE_v1_2.md. Diagrams are drawn from executed specifications.', { x:0.5, y:4.95, w:9, h:0.3, fontSize:10, italic:true, color:C.mute });
note(s, 'Full verified source list in 03-materials/ch03/rdodi/sen0414_ch03_research_v1_0_0.ttl. Visual specifications: 08-tooling/ch03-deck/visuals_make_v1_0_0.py, output visuals_out_v1_0_0.json.');

// 29 next
s = dark(); txt(s, 'Next week: Chapter 4 — Functions', { x:0.6, y:1.6, w:8.8, h:0.9, fontFace:H, fontSize:30, bold:true, color:C.white });
txt(s, 'Before then: work through the chapter 3 interactive page — the same diagrams, plus a quiz and subject agents.', { x:0.6, y:2.6, w:8.8, h:0.9, fontSize:17, color:C.yellow, valign:'top' });
txt(s, 'Questions?', { x:0.6, y:4.2, w:8.8, h:0.6, fontFace:H, fontSize:24, italic:true, color:'C9D4E0' });
note(s, 'Chapter 4 of the 3rd edition is Functions. Ask for questions, and remind them the page has the same traces they saw today.');
pres.writeFile({ fileName: process.argv[2] }).then(f => console.log('written', f));
