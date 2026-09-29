// SEN0414 chapter 5 - Debugging, deck version 1.0.0: a lecture, not a listing. Every slide states its point as a sentence, draws the idea
// (diagrams and visuals are specifications executed under Python and drawn natively - the page draws the same specifications),
// and carries the talk track in its speaker notes. Click builds (objectName "...|bN") are attached by anim_inject_v1_0_0.py.
// The talk track and the page concept of every slide are also written to lecture_out_v1_0_0.json, which the chapter page shows as its Lecture tab.
// Usage: NODE_PATH=$(npm root -g) node deck_v1_0_0.js out.pptx lecture_out.json
const VERSION = "1.0.0";
const pptxgen = require('pptxgenjs'); const fs = require('fs');
const EX = JSON.parse(fs.readFileSync('examples_out_v1_0_0.json')); const py = EX._python; const PR = EX._programs;
const VIS = JSON.parse(fs.readFileSync('visuals_out_v1_0_0.json'));
const PD = JSON.parse(fs.readFileSync('../ch05-page/page_data_v9_7_0.json')); const NODE = {}; PD.nodes.forEach(n => NODE[n.id] = n);
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.author = 'Yusuf Altunel'; pres.title = 'SEN0414 Chapter 5 - Debugging';
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
function title(s, t, sub) { cur.title = t; chip(s, 0.45, 0.32); txt(s, t, { x:1.2, y:0.22, w:8.35, h:0.62, fontFace:H, fontSize:22, bold:true, color:C.navy, fit:'shrink' }, 'title');
  if (sub) txt(s, sub, { x:1.2, y:0.82, w:8.35, h:0.34, fontSize:14, italic:true, color:C.mute }, 'subtitle'); }
const LEC = []; let cur = null;   // the lecture record of the slide being built: number, title, talk track, page concept, visual
const newSlide = bg => { const s = pres.addSlide(); s.background = { color:bg }; cur = { n:LEC.length + 1, title:'', say:'', concept:'', visual:'' }; LEC.push(cur); return s; };
const light = () => newSlide(C.white);
const dark = () => newSlide(C.navy);
const note = (s, t) => { cur.say = t; s.addNotes(t); };
const lec = (concept, visual, title) => { if (title) cur.title = title; cur.concept = concept || ''; cur.visual = visual || ''; };
const BK = 'Automate the Boring Stuff with Python, 3rd edition, chapter 5 (Sweigart, 2025)';
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
function chapterMap(s, x, y, w, h, kBase) { const tops = PD.nodes.filter(n => n.level === 1); const cw = (w - 0.15 * (tops.length - 1)) / tops.length;
  tops.forEach((t, i) => { const xx = x + i * (cw + 0.15); const kk = kBase ? kBase + i : 0; rect(s, { x:xx, y, w:cw, h:0.62, fill:C.blue, lineColor:C.blue, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, 'map1', kk);
    txt(s, t.label, { x:xx, y, w:cw, h:0.62, fontFace:H, fontSize:14, bold:true, color:C.white, align:'center' }, 'map1t', kk);
    PD.nodes.filter(n => n.parent === t.id).forEach((m, j) => { const yy = y + 0.78 + j * 0.62; arrow(s, xx + cw / 2, y + 0.62, xx + cw / 2, yy, { color:C.line, w:1, noHead:true }, kk);
      rect(s, { x:xx + 0.05, y:yy, w:cw - 0.1, h:0.5, fill:C.blueBg, lineColor:C.blue, shape:S.ROUNDED_RECTANGLE, rectRadius:0.06 }, 'map2', kk);
      txt(s, m.label, { x:xx + 0.08, y:yy, w:cw - 0.16, h:0.5, fontSize:11.5, color:C.navy, align:'center', bold:true }, 'map2t', kk);
      PD.nodes.filter(n => n.parent === m.id).forEach((l, q) => { /* leaves listed in the notes, not drawn */ }); }); }); }
// ---- chapter 5 visuals, drawn from the executed specifications ---------------------------------------------------------
const pg = (s, where, links) => { rect(s, { x:0.4, y:5.13, w:1.05, h:0.3, fill:C.yellow, lineColor:C.yellow, shape:S.ROUNDED_RECTANGLE, rectRadius:0.06 }, 'pgchip'); txt(s, 'On the page', { x:0.4, y:5.13, w:1.05, h:0.3, fontSize:10, bold:true, color:C.navy, align:'center' }, 'pgchipt');
  const runs = [{ text:where + (links && links.length ? '   ·   ' : ''), options:{ color:C.mute } }]; (links || []).forEach(([l, u], i) => { runs.push({ text:l, options:{ color:C.blue, underline:{ style:'sng' }, hyperlink:{ url:u, tooltip:u } } }); if (i < links.length - 1) runs.push({ text:'   ·   ', options:{ color:C.mute } }); });
  txt(s, runs, { x:1.55, y:5.1, w:8.05, h:0.36, fontSize:10 }, 'pgtext'); };
const DOC = 'https://docs.python.org/3/';
const RL = { errors:['Tutorial: errors and exceptions', DOC + 'tutorial/errors.html'], stmts:['Reference: raise and assert', DOC + 'reference/simple_stmts.html'], tb:['traceback module', DOC + 'library/traceback.html'],
  howto:['Logging HOWTO', DOC + 'howto/logging.html'], logging:['logging module', DOC + 'library/logging.html'], pdb:['pdb module', DOC + 'library/pdb.html'], cmd:['Command line: -O, PYTHONBREAKPOINT', DOC + 'using/cmdline.html'],
  p553:['PEP 553', 'https://peps.python.org/pep-0553/'], p657:['PEP 657', 'https://peps.python.org/pep-0657/'], p678:['PEP 678', 'https://peps.python.org/pep-0678/'], p768:['PEP 768', 'https://peps.python.org/pep-0768/'],
  tutor:['Python Tutor: step through code online', 'https://pythontutor.com/'] };
const stackTxt = e => e.stack.join(' › ');
const varsTxt = e => e.vars.map(([a, b]) => a + ' = ' + b).join('; ') || 'none yet';
const outTxt = e => e.out || '(nothing printed yet)';
const lineTxt = (V, e) => 'stopped at line ' + e.line + (V.breakpoints.includes(e.line) ? ' (breakpoint)' : '');
// the same moves the page's debugger makes: In = the next stop; Over = the next stop at the same depth or shallower; Out = the next stop shallower; Continue = the next breakpoint
function dbgTarget(V, i, a) { const E = V.events, d = E[i].depth; let j = E.length;
  if (a === 'in') j = i + 1; else if (a === 'over') { for (let k = i + 1; k < E.length; k++) if (E[k].depth <= d) { j = k; break; } } else if (a === 'out') { for (let k = i + 1; k < E.length; k++) if (E[k].depth < d) { j = k; break; } } else if (a === 'cont') { for (let k = i + 1; k < E.length; k++) if (V.breakpoints.includes(E[k].line)) { j = k; break; } }
  return j; }
function debugPanel(s, id, ev, x, y, w, fs, k, label) { const V = VIS[id], E = V.events[ev], n = V.lines.length, lh = fs * 0.0205 + 0.012, codeH = n * lh + 0.16; const nx = 'v:' + id + ':e' + ev + ':';
  if (label) txt(s, label, { x, y:y - 0.3, w, h:0.28, fontSize:12, bold:true, color:C.navy }, 'dbglabel', k);
  rect(s, { x, y, w, h:codeH, fill:C.code, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, 'dbgbox', k);
  rect(s, { x:x + 0.06, y:y + 0.08 + (E.line - 1) * lh, w:w - 0.12, h:lh, fill:'3B5B87', lineColor:'3B5B87' }, nx + 'hl:box', k);
  V.breakpoints.forEach(b => rect(s, { x:x + 0.1, y:y + 0.08 + (b - 1) * lh + lh * 0.18, w:lh * 0.64, h:lh * 0.64, fill:C.red, lineColor:C.red, shape:S.OVAL }, nx + 'bp' + b + ':dot', k));
  txt(s, V.lines.map((l, i) => ({ text:String(i + 1), options:{ color:'8FA3B8', breakLine:i < n - 1 } })), { x:x + 0.3, y:y + 0.08, w:0.3, h:n * lh, fontFace:M, fontSize:fs, valign:'top', align:'right', lineSpacing:lh * 72 }, 'dbgnums', k);
  txt(s, V.lines.map((l, i) => ({ text:l, options:{ color:C.codeTxt, breakLine:i < n - 1 } })), { x:x + 0.68, y:y + 0.08, w:w - 0.8, h:n * lh, fontFace:M, fontSize:fs, valign:'top', lineSpacing:lh * 72 }, 'dbgcode', k);
  const rows = [['line', lineTxt(V, E), C.navy], ['vars', varsTxt(E), C.ink], ['stack', stackTxt(E), C.ink], ['out', outTxt(E), C.ink]]; let yy = y + codeH + 0.06;
  const tag = { line:'', vars:'Variables  ', stack:'Call stack  ', out:'Printed  ' };
  rows.forEach(([f, t, col]) => { rect(s, { x, y:yy, w, h:0.25, fill:f === 'line' ? C.amberBg : C.card, lineColor:f === 'line' ? C.amber : C.card, shape:S.ROUNDED_RECTANGLE, rectRadius:0.05 }, 'dbgrow', k);
    if (tag[f]) txt(s, tag[f], { x:x + 0.08, y:yy, w:0.95, h:0.25, fontSize:9, bold:true, color:C.mute }, 'dbgtag', k);
    txt(s, t, { x:x + (tag[f] ? 0.98 : 0.08), y:yy, w:w - (tag[f] ? 1.06 : 0.16), h:0.25, fontFace:M, fontSize:9.5, bold:f === 'line', color:col, fit:'shrink' }, nx + f, k); yy += 0.27; });
  return yy; }
function unwindDraw(s, id, x, y, w, k0) { const V = VIS[id]; const F = V.frames, n = F.length; const bh = 0.6, gap = 0.32; const nx = 'v:' + id + ':';
  const all = F.map((f, i) => ({ head:f.func, line:f.line, text:f.text, name:nx + 'f' + i })).concat([{ head:V.handler.func, line:V.handler.line, text:V.handler.text, name:nx + 'handler' }]);
  all.forEach((f, i) => { const yy = y + i * (bh + gap), last = i === all.length - 1; const col = i === 0 ? [C.redBg, C.red] : last ? [C.greenBg, C.green] : [C.card, C.line];
    rect(s, { x, y:yy, w, h:bh, fill:col[0], lineColor:col[1], lw:2, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, 'uwbox', 0);
    txt(s, f.head + '  ·  line ' + f.line + '  ·  ' + f.text, { x:x + 0.12, y:yy, w:w - 0.24, h:bh, fontFace:M, fontSize:11, bold:i === 0 || last, color:i === 0 ? C.red : last ? C.green : C.ink, fit:'shrink' }, f.name, 0);
    if (i < all.length - 1) { const kk = k0 + 1 + i; arrow(s, x + w / 2, yy + bh, x + w / 2, yy + bh + gap, { color:last ? C.green : C.red, w:2.5 }, kk);
      txt(s, i < all.length - 2 ? 'no handler here — leave the function' : 'a matching except clause: caught', { x:x + w / 2 + 0.12, y:yy + bh, w:w / 2 - 0.12, h:gap, fontSize:10, italic:true, color:i < all.length - 2 ? C.red : C.green }, 'uwlab', kk); } });
  txt(s, 'raise ' + V.exc, { x:x + w - 1.9, y:y - 0.34, w:1.9, h:0.3, fontFace:M, fontSize:12, bold:true, color:C.red, align:'right' }, nx + 'exc', k0);
  return y + all.length * (bh + gap); }
function levelsGrid(s, id, x, y, w, k0) { const V = VIS[id], n = V.settings.length, lw = 2.55, cw = (w - lw) / n, rh = 0.5, nx = 'v:' + id + ':';
  V.messages.forEach((m, r) => txt(s, m.call, { x:x + 0.05, y:y + 0.44 + r * rh, w:lw - 0.1, h:rh - 0.05, fontFace:M, fontSize:9, color:C.navy, bold:true, fit:'shrink' }, nx + 'm' + r, 0));
  V.settings.forEach((t, c) => { const cx = x + lw + c * cw, kk = k0 ? k0 + c : 0; rect(s, { x:cx, y, w:cw - 0.04, h:0.4, fill:C.navy, lineColor:C.navy }, 'lvhead', kk);
    txt(s, t.label.replace(/^(level=|no )/, '$1\n').replace(/^disable/, 'disable\n'), { x:cx + 0.02, y, w:cw - 0.08, h:0.4, fontFace:M, fontSize:8.5, bold:true, color:C.white, align:'center', fit:'shrink' }, nx + 'h' + c, kk);
    V.messages.forEach((m, r) => { const on = t.shown[r]; rect(s, { x:cx, y:y + 0.44 + r * rh, w:cw - 0.04, h:rh - 0.05, fill:on ? C.greenBg : C.card, lineColor:on ? C.green : C.card }, 'lvcellbox', kk);
      txt(s, on ? 'shown' : 'hidden', { x:cx, y:y + 0.44 + r * rh, w:cw - 0.04, h:rh - 0.05, fontSize:11, bold:on, color:on ? C.green : C.mute, align:'center' }, nx + 'c' + c + 'r' + r, kk); }); });
  return y + 0.44 + V.messages.length * rh; }
function tbCard(s, name, text, x, y, w, h, fs, k) { rect(s, { x, y, w, h, fill:C.code, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'tbbox', k); const L = text.split('\n');
  txt(s, L.map((l, i) => ({ text:l, options:{ color:i === L.length - 1 ? 'FF7B72' : /^\s+[~^]+\s*$/.test(l) ? C.yellow : /^\s*File /.test(l) ? '8FB8E8' : i === 0 ? '8FA3B8' : C.codeTxt, breakLine:i < L.length - 1 } })), { x:x + 0.18, y:y + 0.1, w:w - 0.36, h:h - 0.2, fontFace:M, fontSize:fs, valign:'top', paraSpaceAfter:1 }, name, k);
  txt(s, 'the text a real interpreter wrote to standard error, under Python ' + py, { x, y:y + h + 0.03, w, h:0.22, fontSize:9, italic:true, color:C.mute, align:'right' }); }
function staircase(s, x, y, w, k0) { const L = [...EX.levels[0][1].matchAll(/\('(\w+)', (\d+)\)/g)].map(m => [m[1], +m[2]]); const gap = 0.12, bw = (w - gap * 4) / 5, base = y + 2.3; const cols = [C.blueBg, C.blueBg, C.amberBg, C.redBg, C.redBg], lines = [C.blue, C.blue, C.amber, C.red, C.red];
  L.forEach(([nme, num], i) => { const h = 0.7 + i * 0.36, xx = x + i * (bw + gap); rect(s, { x:xx, y:base - h, w:bw, h, fill:cols[i], lineColor:lines[i], lw:2, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, 'stair', 0);
    txt(s, [{ text:nme, options:{ fontFace:M, bold:true, fontSize:14, color:lines[i], breakLine:true } }, { text:String(num), options:{ fontSize:20, bold:true, color:C.navy, breakLine:true } }, { text:'logging.' + nme.toLowerCase() + '()', options:{ fontFace:M, fontSize:9.5, color:C.mute } }], { x:xx, y:base - h, w:bw, h, align:'center' }, 'stairt', 0); });
  [0, 1].forEach(i => { const h = 0.7 + i * 0.36, xx = x + i * (bw + gap); rect(s, { x:xx, y:base - h, w:bw, h, fill:'DDE3EA', lineColor:'DDE3EA', shape:S.ROUNDED_RECTANGLE, rectRadius:0.08, transparency:12 }, 'hide', k0); txt(s, 'hidden', { x:xx, y:base - h, w:bw, h:0.3, fontSize:11, bold:true, color:C.mute, align:'center' }, 'hidet', k0); });
  const ty = base - (0.7 + 2 * 0.36) - 0.06; arrow(s, x - 0.05, ty, x + w + 0.05, ty, { color:C.red, w:2.5, dash:'dash', noHead:true }, k0);
  txt(s, 'level=logging.WARNING: a message at or above the line is shown', { x:x + 0.1, y:ty - 0.38, w:w - 0.2, h:0.3, fontSize:12, bold:true, color:C.red }, 'thr', k0); }
// =====================================================================================================================
const NOTE_SRC = ' Program written for this course; run under Python ' + py + '.';
// 1 Title
let s = dark(); lec('', '', 'Chapter 5: Debugging'); rect(s, { x:0.6, y:1.2, w:1.2, h:0.8, fill:C.yellow, lineColor:C.yellow, shape:S.ROUNDED_RECTANGLE, rectRadius:0.12 });
txt(s, '>>>', { x:0.6, y:1.2, w:1.2, h:0.8, fontFace:M, fontSize:30, bold:true, color:C.navy, align:'center' });
txt(s, 'Chapter 5: Debugging', { x:0.6, y:2.2, w:8.8, h:0.9, fontFace:H, fontSize:38, bold:true, color:C.white });
txt(s, 'Four ways to find out what a program is really doing', { x:0.6, y:3.05, w:8.8, h:0.5, fontSize:18, italic:true, color:C.yellow });
txt(s, 'SEN0414 Advanced Programming · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University', { x:0.6, y:4.6, w:8.8, h:0.4, fontSize:13, color:'C9D4E0' });
note(s, 'Welcome. Chapter 5 of the book (Sweigart, 2025) is about bugs: how a program tells you it has met one, how you make it tell you sooner, and how you stop it in the middle and look. Every result on these slides was produced by running it under Python ' + py + ', and the debugger, the logging table and the exception climb you will see were recorded from real runs. The chapter page has the same diagrams, and its Lecture tab carries this talk track.');

// 2 Hook
s = dark(); lec('', '', 'The program runs, the answer is wrong');
txt(s, 'The program runs. It prints an answer. The answer is wrong — and Python says nothing.', { x:0.7, y:0.9, w:8.6, h:1.7, fontFace:H, fontSize:30, bold:true, color:C.white, valign:'top' });
txt(s, 'No traceback. No red text. Just a number that should not be that number.', { x:0.7, y:2.9, w:8.6, h:0.8, fontSize:18, italic:true, color:C.yellow, valign:'top' }, 'say', 1);
txt(s, 'Where do you even start?', { x:0.7, y:4.1, w:8.6, h:0.7, fontFace:H, fontSize:28, bold:true, color:C.white }, 'say', 2);
note(s, 'Begin with the feeling everyone has had: the program does not crash, it just gives the wrong answer. Two of this chapter’s own programs do exactly that, a factorial that returns 0 and an adding program that prints 5342 when it should print 50. Click once for the missing error message, once for the question. Ask the room how they would look for the mistake before the slides give the standard answers.' );

// 3 Map
s = light(); title(s, 'Four instruments, and what surrounds them', 'The chapter as the course’s own ontology draws it'); lec('', '', 'Four instruments, and what surrounds them');
chapterMap(s, 0.4, 1.45, 9.2, 3.2, 0);
txt(s, 'Signal an error, check a belief, keep a record, or stop and look — and the modern additions that make each one better.', { x:0.5, y:4.65, w:9, h:0.5, fontSize:14, color:C.ink, valign:'top' });
note(s, 'This is the map of the chapter, drawn from the chapter’s ontology; it is the same tree the interactive page uses. Error signalling covers raising exceptions and reading the traceback. Assertion covers assert and, importantly, when it is switched off. Logging covers setting it up, the levels and good practice. Debugger covers the controls and the standard library’s own debugger. Modern practice holds the three bugs the chapter’s programs contain. By the end you should be able to say which instrument a given problem calls for.');

// 4 Four instruments
s = light(); title(s, 'Each instrument answers a different question', 'Choose by the question, not by habit'); lec('', '', 'Each instrument answers a different question');
const inst = [['raise', 'Can the caller fix this?', 'Tell the caller', 'raise Exception(...)', C.blue], ['assert', 'Must this be true if my code is right?', 'Stop the program', 'assert x > 0', C.red], ['log', 'What did the program do?', 'Leave a record', 'logging.debug(...)', C.green], ['step', 'What is the state at this line?', 'Pause and look', 'breakpoint()', C.amber]];
inst.forEach(([a, q, d, code, col], i) => { const xx = 0.4 + i * 2.35; rect(s, { x:xx, y:1.45, w:2.2, h:3.3, fill:C.card, lineColor:col, lw:2, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'inst', i + 1);
  txt(s, a, { x:xx + 0.15, y:1.55, w:1.9, h:0.55, fontFace:M, fontSize:24, bold:true, color:col }, 'instn', i + 1);
  txt(s, q, { x:xx + 0.15, y:2.2, w:1.9, h:1.0, fontSize:14, italic:true, color:C.ink, valign:'top' }, 'instq', i + 1);
  txt(s, d, { x:xx + 0.15, y:3.3, w:1.9, h:0.4, fontFace:H, fontSize:16, bold:true, color:C.navy }, 'instd', i + 1);
  txt(s, code, { x:xx + 0.15, y:3.8, w:1.9, h:0.4, fontFace:M, fontSize:11, color:C.mute }, 'instc', i + 1); });
pg(s, 'Learn ▸ Debugging: the four subjects', []);
note(s, 'One click per instrument. Raise is for an error somebody else can handle: a caller passed a width of 1 to a function that draws boxes. Assert is for a belief of the programmer: if this list is sorted, the first item is not larger than the last, and if that is false the code is wrong and must stop. Logging is for a record: what did the program do, in what order, with which values. The debugger is for a question about state: what are the variables at exactly this line. The rest of the lecture takes them in that order and ends with three real bugs and the instrument that finds each.');

// 5 Raise
s = light(); title(s, 'Raise an exception when a call cannot be served', 'The chapter’s box_print(): three checks, three messages'); lec('RaiseStatement', '', 'Raise an exception when a call cannot be served');
prog(s, 'boxprint_v1_0_0.py', 0.4, 1.3, 5.9, 3.6, 9); trans(s, 'boxprint_v1_0_0.py', [0], 6.5, 1.3, 3.1, 2.0, 10, 1);
say(s, 'raise stops the function and hands an exception to the nearest matching except. The except clause names it (as err) and str(err) is the message written for raise.', 6.5, 3.5, 3.1, 1.5, { fontSize:12.5 }, 2);
pg(s, 'Learn ▸ Error signalling ▸ Raise statement', [RL.stmts, RL.errors]);
note(s, 'The function is the book’s box_print (Sweigart, 2025), with the calls that trigger each message. It checks its own arguments and raises an Exception with a message when one is wrong: a symbol that is not one character, a width or a height that is not greater than 2. The loop at the bottom calls it with a good box, a width of 1 and a two-character symbol. Click once for the real output: the good box prints, then two lines that begin An exception happened. The except clause caught each exception, called it err and printed str(err), which is exactly the text given to raise. Click again for the sentence to remember. Ask: why is raising better here than printing an error message inside the function? The caller can decide what to do.' + NOTE_SRC);

// 6 Unwinding
s = light(); title(s, 'An exception climbs the stack until something handles it', 'Real frames from a real run: read_age fails, its callers do not catch it'); lec('ExceptionUnwinding', 'ExceptionUnwinding', 'An exception climbs the stack until something handles it');
unwindDraw(s, 'ExceptionUnwinding', 0.4, 1.7, 5.0, 1);
prog(s, 'unwinding_v1_0_0.py', 5.6, 1.35, 4.0, 2.6, 10); trans(s, 'unwinding_v1_0_0.py', [0], 5.6, 4.15, 4.0, 0.55, 10.5, 5);
pg(s, 'Learn ▸ Error signalling ▸ Exception unwinding (drag the climb one frame at a time)', [RL.tb, RL.errors]);
note(s, 'The record on the left is the frames of a real traceback, taken from a run of the program on the right under Python ' + py + '. int(text) inside read_age cannot read the letters abc, so it raises ValueError. Nothing in read_age handles it, so the function is left; the same in load, and the same in process. Click through: each click is one more frame the exception leaves. Only the try around the call at the bottom has an except clause that matches, so it is caught there and execution continues with the print. The transcript is the proof: caught, then the message. This is why the chapter says a function should raise and let the caller who knows what to do handle it.');

// 7 Traceback reading
s = light(); title(s, 'Read a traceback from the bottom up', 'The same climb, as Python prints it when nobody catches the error'); lec('TracebackReading', 'ExceptionUnwinding', 'Read a traceback from the bottom up');
tbCard(s, 'v:ExceptionUnwinding:tb', VIS.ExceptionUnwinding.traceback, 0.4, 1.35, 5.9, 3.3, 10.5, 0);
const tbn = [['1', 'The last line', 'names the exception class and its message'], ['2', 'Outermost first', 'the frame that raised is the one just above the last line'], ['3', 'Four parts a frame', 'file, line, function, and the source line itself']];
tbn.forEach(([n, a, b], i) => { const yy = 1.35 + i * 1.12; card(s, 6.5, yy, 3.1, 1.02, n + '  ' + a, b, [C.red, C.blue, C.blue][i], i + 1); });
pg(s, 'Learn ▸ Error signalling ▸ Traceback reading', [RL.tb, RL.errors]);
note(s, 'The traceback is the same climb as the previous slide, printed by the interpreter when no handler exists. Teach students to read it from the bottom: the last line says what went wrong, in words. The lines above go backwards through the calls that led there, so the frame just above the last line is where the exception was raised. Each frame has its file, its line number, its function and the source line itself. The text on the slide was written by a real interpreter to standard error when the program ran, so it is exact, including the carets that appear under the failing expression from Python 3.11.' + NOTE_SRC);

// 8 Carets and notes
s = light(); title(s, 'Since Python 3.11: carets in tracebacks, notes on exceptions', 'The book’s tracebacks predate both'); lec('FineGrainedLocations', '', 'Since Python 3.11: carets in tracebacks, notes on exceptions');
txt(s, 'Which subscript failed?', { x:0.4, y:1.22, w:5.2, h:0.28, fontSize:13, bold:true, color:C.navy }, 'h1');
tbCard(s, 'v:FineGrainedLocations:text', VIS.FineGrainedLocations.text, 0.4, 1.55, 5.2, 1.4, 10.5, 0);
say(s, 'The tildes and carets mark the failing part of the line: the third subscript, on a value that is None (PEP 657).', 0.4, 3.35, 5.2, 0.9, { fontSize:13 }, 1);
txt(s, 'Say where in the work it happened', { x:5.8, y:1.22, w:3.8, h:0.28, fontSize:13, bold:true, color:C.navy }, 'h2');
prog(s, 'notes_v1_0_0.py', 5.8, 1.55, 3.8, 1.85, 10.5); trans(s, 'notes_v1_0_0.py', [0], 5.8, 3.55, 3.8, 0.55, 11, 2);
say(s, 'add_note attaches text to the exception; it is kept in __notes__ and printed after the traceback (PEP 678).', 5.8, 4.4, 3.8, 0.6, { fontSize:12 }, 2);
pg(s, 'Learn ▸ Error signalling ▸ Fine-grained locations, Exception notes', [RL.p657, RL.p678]);
note(s, 'Two additions since the book’s tracebacks. First, from Python 3.11 the traceback underlines the part of the line that failed. In print(data[‘a’][‘b’][‘c’]) the value at ‘b’ is None, so the third subscript fails, and the carets sit under it; before 3.11 you had to work that out yourself (Galindo Salgado et al., 2021). Second, an exception can carry notes: the program catches a ValueError, adds a note saying which field was being read, and re-raises; the note is kept in __notes__ and printed under the traceback if nobody handles it (Hatfield-Dodds, 2021). Neither is in the book; both are worth a sentence.' + NOTE_SRC);

// 9 Assert predict
s = light(); title(s, 'Predict first: does the program say the list is sorted?', 'The list has just been reversed'); lec('AssertStatement', '', 'Predict first: does the program say the list is sorted?');
prog(s, 'assertdemo_v1_0_0.py', 0.4, 1.4, 5.2, 2.1, 12); trans(s, 'assertdemo_v1_0_0.py', [0], 5.8, 1.4, 3.8, 0.75, 14, 2);
say(s, 'Before you click: what happens on the assert line, and what is printed? Write it down.', 0.4, 3.75, 5.2, 0.9, { fontSize:16, bold:true, color:C.navy });
rect(s, { x:5.8, y:2.6, w:3.8, h:1.55, fill:C.greenBg, lineColor:C.green, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'ans', 1);
txt(s, 'The list is reversed, so the first item, 73, is larger than the last, 26. The condition is false: AssertionError, and the message is empty.', { x:5.95, y:2.6, w:3.5, h:1.55, fontSize:13, bold:true, color:C.green }, 'anst', 1);
pg(s, 'Learn ▸ Assertion ▸ Assert statement', [RL.stmts]);
note(s, 'Prediction first again. The list starts unsorted, is reversed instead of sorted, and the assert says the first item must not be larger than the last. Give them thirty seconds. Click once for the answer, once for the real run. Notice that an assert with no message raises AssertionError with an empty string as its message; the printed line shows repr(str(e)), which is two quotation marks with nothing between them. The try and except is here only so the slide can print what happened; the chapter’s advice is that in a real program you do not catch an AssertionError, you fix the code.' + NOTE_SRC);

// 10 Assert vs raise
s = light(); title(s, 'User errors are handled; programmer errors are asserted', 'Assertions are for programmer errors, not user errors — the chapter’s rule'); lec('AssertVersusRaise', '', 'User errors are handled; programmer errors are asserted');
card(s, 0.4, 1.45, 4.5, 2.6, 'A user error → raise or if', 'The file is not there. The person typed abc for their age. The network is down.\n\nThe program can ask again, use a default, or tell the person. Something outside the code is wrong.', C.blue, 1);
card(s, 5.1, 1.45, 4.5, 2.6, 'A programmer error → assert', 'The list must be sorted here. The total must not be negative. This branch must be unreachable.\n\nIf the check fails the code is wrong. Stop, do not carry on, and fix it.', C.red, 2);
rect(s, { x:0.4, y:4.25, w:9.2, h:0.65, fill:C.amberBg, lineColor:C.amber, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'rule', 3); txt(s, 'Do not catch AssertionError to keep going: an assertion that fails is a bug report, not a condition to recover from.', { x:0.6, y:4.25, w:8.8, h:0.65, fontSize:14, bold:true, color:C.amber }, 'rulet', 3);
pg(s, 'Learn ▸ Assertion ▸ Assert versus raise', [RL.stmts]);
note(s, 'The distinction the chapter draws is the one to leave with. If the cause is outside your code, a missing file, bad input, a dropped connection, the program can do something sensible, so use exceptions and handle them. If the cause is a mistake in your code, there is nothing sensible to do except stop and fix it, and an assertion states the belief that turned out false. The reference defines the assert statement as equivalent to raising AssertionError only when a debug flag is set (Python Software Foundation, 2026), which is the subject of slide 12. Click through the two cards and then the rule.');

// 11 Assert message
s = light(); title(s, 'An assertion can say why it failed', 'The message is evaluated only when the condition is false'); lec('AssertMessage', '', 'An assertion can say why it failed');
prog(s, 'assertmsg_v1_0_0.py', 0.4, 1.4, 5.2, 1.6, 13); trans(s, 'assertmsg_v1_0_0.py', [0], 5.8, 1.4, 3.8, 0.7, 14, 1);
codeCard(s, [[EX.assertion[0][0], EX.assertion[0][1]]], 0.4, 3.3, 5.2, 0.9, 12);
say(s, 'AssertionError is a subclass of Exception. Everything after the comma becomes its message, so put the values there.', 5.8, 2.5, 3.8, 1.5, { fontSize:14 }, 2);
pg(s, 'Learn ▸ Assertion ▸ Assert message, Assertion failure', [RL.stmts, RL.errors]);
note(s, 'A bare assert tells you a check failed; adding a message tells you what the values were. The message is an expression after a comma and is evaluated only if the condition is false, so it costs nothing on the passing path. The line in the code card confirms that AssertionError is an ordinary exception class, a subclass of Exception, which is why an except Exception clause would catch it, and why the previous slide told you not to.' + NOTE_SRC);

// 12 Optimised
s = light(); title(s, 'Hazard: python -O removes every assert', 'Never use one to check what the program must always check'); lec('OptimisedMode', '', 'Hazard: python -O removes every assert');
prog(s, 'optimised_v1_0_0.py', 0.4, 1.4, 5.5, 1.85, 11.5); trans(s, 'optimised_v1_0_0.py', [0], 6.1, 1.4, 3.5, 0.85, 13, 1);
codeCard(s, [[EX.assertion[1][0], EX.assertion[1][1]]], 6.1, 2.6, 3.5, 0.8, 13);
rect(s, { x:0.4, y:3.65, w:9.2, h:1.2, fill:C.redBg, lineColor:C.red, lw:2, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'haz', 2);
txt(s, [{ text:'Hazard  ', options:{ bold:true, color:C.red, fontFace:H, fontSize:16 } }, { text:'Code compiled with optimisation contains no assert statements: the second run reached the print. Do not put user input, file contents or permissions behind an assert; use if and raise, which always run.', options:{ color:C.ink, fontSize:14 } }], { x:0.6, y:3.65, w:8.8, h:1.2 }, 'hazt', 2);
pg(s, 'Learn ▸ Assertion ▸ Optimised mode', [RL.cmd, RL.stmts]);
note(s, 'Not in the book, and a genuine trap. The reference says the assert statement is equivalent to if __debug__: if not expression: raise AssertionError, and that no code is generated for it when optimisation is requested, as with the -O option (Python Software Foundation, 2026). The program shows both: compiled normally the assert raises and prints the message; compiled with optimize=1 the same source runs straight through to the print. The code card shows __debug__ is True in a normal run. So an assert is a development aid; anything the program depends on for correctness under all conditions must not be one.' + NOTE_SRC);

// 13 Logging hook
s = dark(); lec('Logging', '', 'What if print calls could be switched off with one line?');
txt(s, 'You add print calls to see what is happening. Then you have to find them all again and delete them.', { x:0.7, y:0.9, w:8.6, h:1.9, fontFace:H, fontSize:28, bold:true, color:C.white, valign:'top' });
txt(s, 'What if the messages could stay in the program, and one line decided which ones show?', { x:0.7, y:3.1, w:8.6, h:1.0, fontSize:20, italic:true, color:C.yellow, valign:'top' }, 'say', 1);
note(s, 'Everyone starts with print statements. They work, and they leave a mess: you must remember to remove them, and you cannot keep some and hide others. Logging solves exactly that problem. Click for the question and let the room suggest what it would need: a way to label how important a message is, and a single switch for the threshold.');
// 14 Setup
s = light(); title(s, 'basicConfig chooses the threshold, the format and the place', 'One call at the top of the program'); lec('BasicConfig', '', 'basicConfig chooses the threshold, the format and the place');
prog(s, 'levelsdemo_v1_0_0.py', 0.4, 1.3, 9.2, 1.65, 10.5);
txt(s, "format='%(asctime)s - %(levelname)s - %(message)s'  is the chapter’s; here the time is left out so every run prints the same text", { x:0.4, y:3.1, w:5.6, h:0.5, fontSize:11, italic:true, color:C.mute, valign:'top' }, 'fmtnote');
[['%(levelname)s', 'how important', C.amber, C.amberBg], ['-', 'a separator you choose', C.mute, C.card], ['%(message)s', 'what happened', C.green, C.greenBg]].forEach(([a, b, col, bg], i) => { const xx = 0.4 + i * 1.9; rect(s, { x:xx, y:3.7, w:1.8, h:1.15, fill:bg, lineColor:col, lw:2, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, 'fmt', i + 1);
  txt(s, [{ text:a, options:{ fontFace:M, bold:true, fontSize:11.5, color:col, breakLine:true } }, { text:b, options:{ fontSize:12, color:C.ink } }], { x:xx + 0.05, y:3.7, w:1.7, h:1.15, align:'center' }, 'fmtt', i + 1); });
trans(s, 'levelsdemo_v1_0_0.py', [0], 6.2, 3.1, 3.4, 1.4, 11, 4);
pg(s, 'Learn ▸ Logging ▸ Basic config, Log format', [RL.howto, RL.logging]);
note(s, 'The setup call from the book (Sweigart, 2025), with one change: the book’s format also prints the time, which is useful in real programs and makes a slide unrepeatable, so this deck leaves it out. Three parts: the level says which messages to show, the format says what each line looks like, and the destination is the screen unless you give a file name. Click the three parts of the format string one by one, then the real output of the program above: five calls, four lines, because the threshold was INFO. Say now that the missing line is the debug call, and that the next slides explain why.' + NOTE_SRC);

// 15 Levels staircase
s = light(); title(s, 'Five levels, each with a number', 'A message is shown when its level is at least the threshold'); lec('LoggingLevels', '', 'Five levels, each with a number');
staircase(s, 0.6, 1.4, 8.8, 1);
codeCard(s, [[EX.levels[0][0], EX.levels[0][1]]], 0.5, 3.95, 9, 0.9, 12);
pg(s, 'Learn ▸ Logging ▸ Logging levels, Level threshold', [RL.howto, RL.logging]);
note(s, 'The chapter’s five levels, lowest to highest importance: DEBUG for the detail you want while developing, INFO for confirmation that things work, WARNING for something unexpected, ERROR for a failure, CRITICAL for one that may stop the program. The numbers in the code card were produced by asking the logging module for them; they are 10, 20, 30, 40 and 50 (Python Software Foundation, 2026). One click: set the threshold to WARNING and the two lowest steps disappear. The threshold is a number, so the rule is simply: shown when the message’s number is at least the threshold’s.' + NOTE_SRC);

// 16 Matrix
s = light(); title(s, 'Choose a threshold, see what is shown', 'Each column is a real run of the same five calls'); lec('LevelThreshold', 'LevelThreshold', 'Choose a threshold, see what is shown');
levelsGrid(s, 'LevelThreshold', 0.4, 1.35, 9.2, 1);
say(s, 'Raising the threshold hides the lower levels without deleting a single call. The first column is what happens with no setup at all; the last shows logging.disable(CRITICAL).', 0.4, 4.4, 9.2, 0.65, { fontSize:13 });
pg(s, 'Learn ▸ Logging ▸ Level threshold (choose the level yourself)', [RL.howto]);
note(s, 'This grid is a simulation you can also run yourself on the page. Every cell is what a real subprocess printed: for each setting the same five logging calls were run under Python ' + py + ' and the output lines were read back. Click column by column. Column one has no basicConfig at all and shows a surprise, taken up next. Columns two to six are the five thresholds; watch the shown cells shrink as the threshold rises. The last column is the disable function, which silences everything at or below the level it is given.');

// 17 Default trap
s = light(); title(s, 'Why does logging.debug print nothing?', 'Without any setup the threshold is WARNING'); lec('DefaultLevel', 'LevelThreshold', 'Why does logging.debug print nothing?');
codeCard(s, [[EX.levels[1][0], EX.levels[1][1]]], 0.4, 1.3, 9.2, 0.85, 12);
say(s, 'The root logger starts at WARNING, which is 30. Calls below it are dropped; the rest go to standard error, not the screen output of print.', 0.4, 2.55, 4.6, 1.5, { fontSize:14 });
txt(s, 'What a program with no basicConfig writes to standard error', { x:5.2, y:2.4, w:4.4, h:0.28, fontSize:12, bold:true, color:C.navy }, 'errcap');
rect(s, { x:5.2, y:2.72, w:4.4, h:1.0, fill:C.code, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'errbox', 1);
txt(s, VIS.LevelThreshold.settings[0].output.map((l, i, a) => ({ text:l, options:{ color:'FF7B72', breakLine:i < a.length - 1 } })), { x:5.35, y:2.78, w:4.1, h:0.9, fontFace:M, fontSize:11, valign:'top' }, 'v:LevelThreshold:o0', 1);
txt(s, 'debug and info: dropped', { x:5.2, y:3.8, w:4.4, h:0.35, fontSize:14, bold:true, color:C.mute }, 'drop', 2);
rect(s, { x:0.4, y:4.3, w:9.2, h:0.65, fill:C.amberBg, lineColor:C.amber, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'tip', 2); txt(s, 'The chapter’s call logging.basicConfig(level=logging.DEBUG, …) is what lowers the threshold so the debug lines appear.', { x:0.6, y:4.3, w:8.8, h:0.65, fontSize:13, bold:true, color:C.amber }, 'tipt', 2);
pg(s, 'Learn ▸ Logging ▸ Default level', [RL.howto, RL.logging]);
note(s, 'The commonest surprise for a beginner: they add logging.debug calls and see nothing. The reason is that a program with no configuration has the root logger at WARNING, which the code card reads back as 30. The box on the right is the exact standard error of a run with no setup: only the warning, error and critical lines appear, and with the logger’s name, root, in front (Python Software Foundation, 2026). Debug and info are dropped. Second click: the fix is the chapter’s own basicConfig call.' + NOTE_SRC);

// 18 Force
s = light(); title(s, 'Hazard: a second basicConfig call is ignored', 'The first call wins unless you pass force=True'); lec('ForceReconfigure', '', 'Hazard: a second basicConfig call is ignored');
prog(s, 'force_v1_0_0.py', 0.4, 1.3, 9.2, 2.0, 9.5); trans(s, 'force_v1_0_0.py', [0], 0.4, 3.55, 4.4, 0.8, 12, 1);
rect(s, { x:5.0, y:3.55, w:4.6, h:1.3, fill:C.redBg, lineColor:C.red, lw:2, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'haz', 2);
txt(s, 'basicConfig does nothing if the root logger already has handlers. Your DEBUG call vanished because an earlier call had set INFO. force=True replaces the old setup.', { x:5.15, y:3.55, w:4.3, h:1.3, fontSize:13, color:C.ink }, 'hazt', 2);
pg(s, 'Learn ▸ Logging ▸ Force reconfigure', [RL.logging]);
note(s, 'Not in the book and a frequent puzzle in notebooks and tests, where something else has already configured logging. The program calls basicConfig with INFO, then again with DEBUG; the debug call after the second setup prints nothing, because the second call was ignored. The third call passes force=True, and now the debug message appears. The logging documentation says basicConfig does nothing if the root logger already has handlers configured unless force is given (Python Software Foundation, 2026).' + NOTE_SRC);

// 19 File
s = light(); title(s, 'Log to a file instead of the screen', 'Pass a file name to basicConfig'); lec('LogToFile', '', 'Log to a file instead of the screen');
prog(s, 'filelog_v1_0_0.py', 0.4, 1.3, 9.2, 1.9, 10.5); trans(s, 'filelog_v1_0_0.py', [0], 0.4, 3.45, 4.4, 0.8, 12, 1);
say(s, 'The file keeps the record after the program ends. The last line of the program reads it back so the deck can show what was written.', 5.0, 3.45, 4.6, 1.4, { fontSize:13 }, 2);
pg(s, 'Learn ▸ Logging ▸ Log to file', [RL.howto]);
note(s, 'The chapter writes to myProgramLog.txt; this program does the same in a temporary folder so it can be re-run anywhere, then reads the file back and prints it. Two messages were logged and both appear, because the threshold was DEBUG. Nothing was printed to the screen by the logging calls themselves: the record lives in the file (Sweigart, 2025).' + NOTE_SRC);

// 20 Disable
s = light(); title(s, 'Switch every message off with one line', 'logging.disable silences a level and everything below it'); lec('DisablingLogging', '', 'Switch every message off with one line');
prog(s, 'disable_v1_0_0.py', 0.4, 1.3, 9.2, 1.95, 10); trans(s, 'disable_v1_0_0.py', [0], 0.4, 3.5, 4.4, 0.8, 12, 1);
say(s, 'disable(CRITICAL) silences all five levels. disable(NOTSET) turns them back on. The calls stay in the program; nothing has to be deleted.', 5.0, 3.5, 4.6, 1.3, { fontSize:13 }, 2);
pg(s, 'Learn ▸ Logging ▸ Disabling logging', [RL.logging]);
note(s, 'This is the answer to the hook. Print calls have to be found and deleted; log calls are silenced by one line. In the real run, the critical message before the disable call appears, the two calls after it print nothing, and after logging.disable(logging.NOTSET) errors show again (Sweigart, 2025; Python Software Foundation, 2026). It is the same idea as the last column of the grid.' + NOTE_SRC);

// 21 Lazy
s = light(); title(s, 'Give the arguments to the call, not to an f-string', 'The message is formatted only if it will be shown'); lec('LazyFormatting', '', 'Give the arguments to the call, not to an f-string');
prog(s, 'lazy_v1_0_0.py', 0.4, 1.3, 5.0, 3.0, 10.5); trans(s, 'lazy_v1_0_0.py', [0], 5.6, 1.3, 4.0, 0.75, 13, 1);
card(s, 5.6, 2.45, 1.95, 1.95, 'Arguments', "log.debug('value is %s', obj)\n\nformatted only when emitted: zero conversions here", C.green, 2);
card(s, 7.65, 2.45, 1.95, 1.95, 'f-string', "log.debug(f'value is {obj}')\n\nbuilt before the call, even when debug is hidden", C.red, 3);
pg(s, 'Learn ▸ Logging ▸ Lazy formatting', [RL.howto]);
note(s, 'A practical point the book does not make. The level here is INFO, so the debug calls are not emitted. In the first call the object is passed as an argument and the logging module only converts it to text if the message will be shown, so its __str__ ran zero times. In the second the f-string builds the text before the call, so the conversion ran once even though nothing was logged. For a cheap value it does not matter; for an expensive one it does, and the logging HOWTO’s own example makes that point (Python Software Foundation, 2026).' + NOTE_SRC);

// 22 Logging vs print
s = light(); title(s, 'Log messages are for the programmer; print is for the user', 'Practice question 8 asks why logging beats print'); lec('LoggingVersusPrint', '', 'Log messages are for the programmer; print is for the user');
card(s, 0.4, 1.45, 4.5, 2.7, 'logging', "Stays in the program.\nOne setting silences it.\nCarries a level, and can carry a time.\n\nlogging.debug('i is %s', i)", C.green, 1);
card(s, 5.1, 1.45, 4.5, 2.7, 'print()', "What the person running the program should see:\nFile not found.\nInvalid input, please enter a number.\n\nprint('File not found')", C.blue, 2);
say(s, 'Rule of thumb: if you would delete it before giving the program to someone, it is a log message.', 0.4, 4.35, 9.2, 0.55, { fontSize:15, bold:true, color:C.navy }, 3);
pg(s, 'Learn ▸ Logging ▸ Logging versus print', [RL.howto]);
note(s, 'The chapter’s practice question 8 asks why logging is better than print for the same message, and its answer is about audience: log messages are for the programmer; messages the user should see, such as file not found or invalid input, use print (Sweigart, 2025). The three lines on the left are the practical consequences you have just seen: the calls stay, one setting switches them off, and each carries a level.');
// 23 Predict factorial
s = light(); title(s, 'Predict first: what does factorial(3) return?', 'The loop is range(n + 1)'); lec('OffByOneRange', 'OffByOneRange', 'Predict first: what does factorial(3) return?');
prog(s, 'factorial_bug_v1_0_0.py', 0.4, 1.3, 9.2, 2.3, 10);
say(s, 'Before you click: what is total after the first pass, and what does the call print? 3! is 6.', 0.4, 3.75, 4.4, 1.1, { fontSize:15, bold:true, color:C.navy });
trans(s, 'factorial_bug_v1_0_0.py', [0], 5.0, 3.7, 4.6, 1.2, 9.5, 1);
pg(s, 'Learn ▸ Modern practice ▸ Off-by-one range', [RL.howto]);
note(s, 'The chapter’s factorial with its logging calls, for n of 3 so the table stays short (Sweigart, 2025). Ask what they expect; most say 6. Click for the real run: the log shows i is 0, total is 0 on the first pass and total is still 0 on every pass after it, and the call returns 0. The debug lines are what make the bug visible without a debugger: you can see the first pass multiply by zero. Do not explain yet; the next slide traces it.' + NOTE_SRC);

// 24 Trace
s = light(); title(s, 'Trace it: the first pass multiplies by zero', 'One row per pass — recorded from a real run'); lec('OffByOneRange', 'OffByOneRange', 'Trace it: the first pass multiplies by zero');
traceTable(s, 'OffByOneRange', 0, 0.4, 1.35, 9.2, 0.62, 1, 11);
say(s, VIS.OffByOneRange.caption + ' range(n + 1) starts at 0, so 0 is the first value of i.', 0.4, 4.35, 9.2, 0.7, { fontSize:13 });
pg(s, 'Learn ▸ Modern practice ▸ Off-by-one range (step through it)', []);
note(s, 'A trace table is how you reason about a loop without running it. Click row by row. Pass one: i is 0, so total times 0 is 0. From then on total stays 0, whatever i is, because anything times zero is zero. The last row also shows the debug line that closes the function and the value that print shows. This trace was recorded by a line tracer on the program on the previous slide under Python ' + py + '; the page draws the same specification as a stepper.');

// 25 Fix
s = light(); title(s, 'The fix is one line — and the log proves it', 'range(1, n + 1) starts at 1 and includes n'); lec('OffByOneRange', '', 'The fix is one line, and the log proves it');
prog(s, 'factorial_fixed_v1_0_0.py', 0.4, 1.3, 9.2, 2.3, 10); trans(s, 'factorial_fixed_v1_0_0.py', [0], 0.4, 3.7, 4.6, 1.2, 9.5, 1);
rect(s, { x:5.2, y:3.7, w:4.4, h:1.2, fill:C.greenBg, lineColor:C.green, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'fix', 2); txt(s, 'total is 1, 2, 6 on the three passes, and the call returns 6. Keep the log calls: they cost nothing at level WARNING.', { x:5.35, y:3.7, w:4.1, h:1.2, fontSize:13, bold:true, color:C.green }, 'fixt', 2);
pg(s, 'Learn ▸ Modern practice ▸ Off-by-one range', []);
note(s, 'Same program with range(1, n + 1). The log now shows i is 1 and total is 1, then 2, then 6, and the call prints 6. Notice how the logging calls stayed in place while the fix went in; when the program is finished you raise the threshold or call disable and they fall silent, rather than deleting them (Sweigart, 2025).' + NOTE_SRC);

// 26 Debugger hook
s = dark(); lec('Debugger', '', 'What if you could freeze the program on one line and look around?');
txt(s, 'What if you could freeze the program on one line and look at every variable?', { x:0.7, y:0.9, w:8.6, h:1.9, fontFace:H, fontSize:30, bold:true, color:C.white, valign:'top' });
txt(s, 'Then move forward one line at a time and watch the values change.', { x:0.7, y:3.1, w:8.6, h:1.0, fontSize:20, italic:true, color:C.yellow, valign:'top' }, 'say', 1);
note(s, 'Logging tells you what happened. Sometimes you need to ask what the state is right now, at one line, and then step forward and see. That is what a debugger is. The book’s chapter uses the debugger in the Mu editor (Sweigart, 2025); the controls have the same names in most editors, and the standard library has one of its own, which is the last part of this chapter.');

// 27 Controls
s = light(); title(s, 'Five controls, and a breakpoint to start from', 'The chapter’s debugger: Continue, Step In, Step Over, Step Out, Stop'); lec('Breakpoint', 'Breakpoint', 'Five controls, and a breakpoint to start from');
const ctl = [['Continue', 'run until the next breakpoint, or the end', 'pdb: continue', C.green], ['Step In', 'run one line; if it is a call, go inside', 'pdb: step', C.blue], ['Step Over', 'run one line; a call runs without stopping inside', 'pdb: next', C.blue], ['Step Out', 'run to the end of this function and stop back in the caller', 'pdb: return', C.blue], ['Stop', 'end the program now', 'pdb: quit', C.red]];
ctl.forEach(([a, b, c, col], i) => { const xx = 0.4 + i * 1.86; rect(s, { x:xx, y:1.4, w:1.76, h:2.4, fill:C.card, lineColor:col, lw:2, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'ctl', i + 1);
  txt(s, a, { x:xx + 0.1, y:1.48, w:1.56, h:0.45, fontFace:H, fontSize:16, bold:true, color:col }, 'ctln', i + 1);
  txt(s, b, { x:xx + 0.1, y:2.0, w:1.56, h:1.2, fontSize:12.5, valign:'top' }, 'ctlt', i + 1);
  txt(s, c, { x:xx + 0.1, y:3.35, w:1.56, h:0.35, fontFace:M, fontSize:10.5, color:C.mute }, 'ctlp', i + 1); });
rect(s, { x:0.4, y:3.95, w:9.2, h:0.6, fill:C.redBg, lineColor:C.red, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'bp', 6); txt(s, [{ text:'●  ', options:{ color:C.red, bold:true, fontSize:18 } }, { text:'A breakpoint marks a line where the debugger pauses. In the Mu editor you click a line number to set it, and click it again to remove it.', options:{ color:C.ink, fontSize:13 } }], { x:0.6, y:3.95, w:8.8, h:0.6 }, 'bpt', 6);
txt(s, 'The small program the next slides step through prints:', { x:3.2, y:4.68, w:4.1, h:0.35, fontSize:12, italic:true, color:C.mute, align:'right' }, 'dbgprog');
trans(s, 'debugdemo_v1_0_0.py', [0], 7.4, 4.65, 2.2, 0.38, 12);
pg(s, 'Learn ▸ Debugger ▸ Controls', [RL.pdb]);
note(s, 'The five controls of the chapter’s debugger, one click each. Continue runs until it reaches a breakpoint or the end. Step In executes the next line and, if the line calls a function, goes inside it. Step Over executes the next line, running any function it calls at full speed without stopping inside. Step Out runs the rest of the current function and stops when it returns (Sweigart, 2025). Stop ends the program. Under each is the command of the standard library’s debugger, pdb, that does the same job: continue, step, next and return; the page’s simulator has all five buttons. Last click: the breakpoint, the line at which you ask the debugger to pause.');

// 28 Breakpoint and Continue
s = light(); title(s, 'Continue runs to the next breakpoint', 'A recorded run of a small program: the debugger stops before each line runs'); lec('ContinueControl', 'Breakpoint', 'Continue runs to the next breakpoint');
{ const V = VIS.Breakpoint; const a = 0, b = dbgTarget(V, 0, 'cont');
  debugPanel(s, 'Breakpoint', a, 0.4, 1.65, 4.1, 9.5, 0, 'Start: stopped on the first line'); debugPanel(s, 'Breakpoint', b, 5.5, 1.65, 4.1, 9.5, 1, 'After Continue: the breakpoint at line ' + V.events[b].line);
  arrow(s, 4.55, 2.5, 5.45, 2.5, { color:C.green, w:3 }, 1); txt(s, 'Continue', { x:4.5, y:2.1, w:1.0, h:0.3, fontSize:11, bold:true, color:C.green, align:'center' }, 'cont', 1); }
pg(s, 'Learn ▸ Debugger ▸ Breakpoint, Continue (set your own breakpoints)', [RL.tutor]);
note(s, 'Both panels are frames from one recorded run of this program under Python ' + py + ': a line event stream, with the variables and the call stack at each stop. On the left the debugger has stopped before line 1, nothing has run and no variables exist. There is a breakpoint, the red dot, on line 7. Click: Continue runs the program until it reaches that line and stops there, with x already 5 because line 6 has run. This is the same simulator you get on the page, where you can set your own breakpoints by clicking a line number. If students want to see any of their own code stepped through, Python Tutor does that online.');

// 29 Step In vs Step Over
s = light(); title(s, 'Step In goes inside a call; Step Over runs it whole', 'Both start at the same line: the call to add'); lec('StepIn', 'StepIn', 'Step In goes inside a call; Step Over runs it whole');
{ const V = VIS.StepIn; const i0 = V.events.findIndex(e => e.line === 6), i1 = dbgTarget(V, i0, 'in'), i2 = dbgTarget(V, i0, 'over');
  debugPanel(s, 'StepIn', i0, 0.3, 1.65, 3.0, 9, 0, 'Stopped at line ' + V.events[i0].line); debugPanel(s, 'StepIn', i1, 3.45, 1.65, 3.0, 9, 1, 'Step In → line ' + V.events[i1].line + ', inside add'); debugPanel(s, 'StepIn', i2, 6.6, 1.65, 3.0, 9, 2, 'Step Over → line ' + V.events[i2].line + ', after add'); }
pg(s, 'Learn ▸ Debugger ▸ Step in, Step over', [RL.pdb]);
note(s, 'Three frames from the recorded run. On the left the debugger is stopped at line 6, which calls add. Click once: Step In moves into add, so the call stack now has a third frame, and a and b are its variables. Click again: Step Over, from the same starting line, runs the whole call to add at full speed and stops on the next line of main, with x already 5 and the call stack unchanged. Use Step In when you suspect the function you are calling; Step Over when you trust it and want to move on (Sweigart, 2025).');

// 30 Step Out
s = light(); title(s, 'Step Out finishes this function and stops in its caller', 'You stepped in and want to get back'); lec('StepOut', 'StepOut', 'Step Out finishes this function and stops in its caller');
{ const V = VIS.StepOut; const i0 = V.events.findIndex(e => e.line === 2), i1 = dbgTarget(V, i0, 'out');
  debugPanel(s, 'StepOut', i0, 0.4, 1.65, 4.1, 9.5, 0, 'Stopped inside add, at line ' + V.events[i0].line); debugPanel(s, 'StepOut', i1, 5.5, 1.65, 4.1, 9.5, 1, 'Step Out → line ' + V.events[i1].line + ', back in main');
  arrow(s, 4.55, 2.5, 5.45, 2.5, { color:C.blue, w:3 }, 1); txt(s, 'Step Out', { x:4.5, y:2.1, w:1.0, h:0.3, fontSize:11, bold:true, color:C.blue, align:'center' }, 'out', 1); }
pg(s, 'Learn ▸ Debugger ▸ Step out', [RL.pdb]);
note(s, 'The third stepping control. The debugger is stopped at line 2, inside add, with a and b set and three frames on the call stack. Step Out runs the rest of add and stops as soon as it returns, here at line 7 of main, with the call stack back to two frames (Sweigart, 2025). It is the way back after a Step In that turned out to be uninteresting.');

// 31 pdb and breakpoint
s = light(); title(s, 'Any Python has a debugger: breakpoint() and pdb', 'The same five controls, in the standard library'); lec('BreakpointFunction', '', 'Any Python has a debugger: breakpoint() and pdb');
codeCard(s, EX.hook.map(r => [r[0], r[1]]), 0.4, 1.3, 9.2, 2.1, 10.5);
card(s, 0.4, 3.75, 2.95, 1.25, 'breakpoint()', 'Pauses in pdb at that line (PEP 553). PYTHONBREAKPOINT=0 makes it do nothing.', C.blue, 1);
card(s, 3.525, 3.75, 2.95, 1.25, 'pdb commands', 'step, next, return, continue, break match the controls; where lists the call stack.', C.green, 2);
card(s, 6.65, 3.75, 2.95, 1.25, 'New in 3.14', 'python -m pdb -p PID attaches to a running process (PEP 768).', C.amber, 3);
pg(s, 'Learn ▸ Debugger ▸ Breakpoint function, pdb commands, Remote attach', [RL.p553, RL.p768, RL.pdb]);
note(s, 'Not in the book, which uses an editor’s debugger, but this is the tool every Python installation has. Since Python 3.7 a call to breakpoint() pauses the program in the debugger at that line; it calls sys.breakpointhook, and setting the environment variable PYTHONBREAKPOINT to 0 makes the call do nothing, so you can leave one in and switch it off (Warsaw, 2017; Python Software Foundation, 2026). The third line of the code card shows the pdb commands that match the chapter’s controls, checked against the debugger class itself, and the last confirms the quit command that matches Stop. New in Python 3.14: the debugger can attach to a process that is already running, by its process identifier, using sys.remote_exec (Galindo Salgado, Wozniski and Stojanovic, 2024); the second line confirms that this build has it.' + NOTE_SRC);

// 32 Adding bug
s = light(); title(s, 'Worked case: the sum that prints 5342', 'The debugger shows quotation marks around the values'); lec('StringConcatenation', '', 'Worked case: the sum that prints 5342');
txt(s, 'Before', { x:0.4, y:1.2, w:4.5, h:0.3, fontSize:14, bold:true, color:C.red }, 'l1'); prog(s, 'adding_bug_v1_0_0.py', 0.4, 1.5, 4.5, 1.7, 10); trans(s, 'adding_bug_v1_0_0.py', [0], 0.4, 3.35, 4.5, 1.4, 10);
txt(s, 'After', { x:5.1, y:1.2, w:4.5, h:0.3, fontSize:14, bold:true, color:C.green }, 'l2', 1); prog(s, 'adding_fixed_v1_0_0.py', 5.1, 1.5, 4.5, 1.7, 10, 1); trans(s, 'adding_fixed_v1_0_0.py', [0], 5.1, 3.35, 4.5, 1.4, 10, 1);
pg(s, 'Learn ▸ Modern practice ▸ String concatenation', [RL.errors]);
note(s, 'The book’s buggy adding program: input() returns strings, so adding first, second and third joins the text and prints The sum is 5342 (Sweigart, 2025). In the debugger’s variable pane the values would show with quotation marks, which is the clue that they are strings and not numbers. Click for the fix, int(input()) on each line, and the real run: the sum is 50. Both transcripts are real runs of these programs with the inputs 5, 3 and 42.' + NOTE_SRC);

// 33 Coin toss
s = light(); title(s, 'Worked case: a guess that can never be right', 'toss is an int; guess is a str'); lec('TypeMismatchComparison', '', 'Worked case: a guess that can never be right');
prog(s, 'cointoss_bug_v1_0_0.py', 0.4, 1.35, 5.6, 2.4, 11); trans(s, 'cointoss_bug_v1_0_0.py', [0, 1], 6.2, 1.35, 3.4, 2.1, 10.5, 1);
rect(s, { x:0.4, y:3.95, w:9.2, h:0.9, fill:C.amberBg, lineColor:C.amber, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }, 'ct', 2);
txt(s, 'A number never equals a string, so toss == guess is false for every guess, heads or tails: the last line prints the types, int str. This is one of the bugs in the chapter’s Buggy Coin Toss Game.', { x:0.6, y:3.95, w:8.8, h:0.9, fontSize:13, bold:true, color:C.amber }, 'ctt', 2);
pg(s, 'Learn ▸ Modern practice ▸ Type mismatch comparison', []);
note(s, 'The practice program in the chapter, cut down to the comparison that is wrong. random.randint(0, 1) gives an integer, the guess from input() is a string, and toss == guess compares the two, so it is always false. The seed is fixed, so the toss is heads in both runs: the run that guessed heads should have won, and it says Nope. The last line prints the two types. The other bugs in the practice program are for the students to find with the instruments of this chapter (Sweigart, 2025).' + NOTE_SRC);

// 34 Recap
s = light(); title(s, 'What you can do now', 'The chapter on one page — choose, read, log, step'); lec('', '', 'What you can do now');
const can = [['Choose', 'the instrument by the question: raise, assert, log or step'], ['Read', 'a traceback from the bottom up, with its carets and notes'], ['Log', 'with a level, one setup call, lazy arguments and one line to silence it'], ['Step', 'with breakpoints and the five controls, or with breakpoint() and pdb']];
can.forEach(([a, b], i) => { const yy = 1.45 + i * 0.9; rect(s, { x:0.5, y:yy, w:1.5, h:0.7, fill:C.blue, lineColor:C.blue, shape:S.ROUNDED_RECTANGLE, rectRadius:0.1 }); txt(s, a, { x:0.5, y:yy, w:1.5, h:0.7, fontFace:H, fontSize:18, bold:true, color:C.white, align:'center' }); txt(s, b, { x:2.2, y:yy, w:7.3, h:0.7, fontSize:16 }); });
note(s, 'Close the loop on the hook: the program runs and prints a wrong answer. Start by asking what you believe, and assert it. Add logging where you cannot tell what happened. Reach for the debugger when the state at one line is the question. Read every traceback from the bottom. Those four verbs are the chapter’s learning objectives on the interactive page.');

// 35 Check yourself
s = light(); title(s, 'Check yourself: answer aloud, then click', 'Retrieval beats re-reading'); lec('', '', 'Check yourself');
const qa = [['When do you raise, and when do you assert?', 'Raise for errors a caller can handle; assert for what must be true if the code is right.'], ['Why can an assert never guard user input?', 'python -O removes assert statements.'], ['Why does logging.debug print nothing by default?', 'The default level is WARNING, which is 30.'], ['Which control goes inside a called function?', 'Step In; Step Over runs the call, Step Out leaves the function.'], ['What does the range(n + 1) factorial return?', '0: the first pass multiplies by 0.']];
qa.forEach(([q, a], i) => { const yy = 1.35 + i * 0.75; rect(s, { x:0.5, y:yy + 0.04, w:0.46, h:0.46, fill:C.yellow, lineColor:C.yellow, shape:S.OVAL }); txt(s, String(i + 1), { x:0.5, y:yy + 0.04, w:0.46, h:0.46, fontFace:H, fontSize:15, bold:true, color:C.navy, align:'center' });
  txt(s, q, { x:1.1, y:yy, w:4.6, h:0.54, fontSize:14 }); rect(s, { x:5.8, y:yy + 0.02, w:3.8, h:0.5, fill:C.greenBg, lineColor:C.green, shape:S.ROUNDED_RECTANGLE, rectRadius:0.08 }, 'a', i + 1); txt(s, a, { x:5.9, y:yy + 0.02, w:3.6, h:0.5, fontSize:11, bold:true, color:C.green, fit:'shrink' }, 'at', i + 1); });
note(s, 'Answer aloud first, then click. Questions 1 to 3 revisit the assertion and logging material; question 4 the debugger controls from the book’s practice questions; question 5 the bug that ran through the chapter. The interactive page has a quiz with a reason for each wrong answer, so send them there before next week.');

// 36 Sources
s = light(); title(s, 'Sources', 'Every claim beyond the book is recorded in the chapter’s research record'); lec('', '', 'Sources');
const src = ['Sweigart, A. (2025). Automate the Boring Stuff with Python, 3rd ed., ch. 5. No Starch Press. automatetheboringstuff.com/3e', 'Python Software Foundation (2026). Python 3.14 documentation: Language Reference, simple statements; Built-in Exceptions; Tutorial, errors and exceptions; Logging HOWTO; logging; pdb; sys; traceback; command line and environment; What’s New in 3.14', 'Warsaw, B. (2017). PEP 553 – Built-in breakpoint()', 'Galindo Salgado, P. et al. (2021). PEP 657 – Include Fine Grained Error Locations in Tracebacks', 'Hatfield-Dodds, Z. (2021). PEP 678 – Enriching Exceptions with Notes', 'Galindo Salgado, P., Wozniski, M. and Stojanovic, I. (2024). PEP 768 – Safe external debugger interface for CPython'];
txt(s, src.map((t, i) => ({ text:t, options:{ bullet:true, breakLine:i < src.length - 1 } })), { x:0.5, y:1.4, w:9, h:3.4, fontSize:12, valign:'top', paraSpaceAfter:6 });
txt(s, 'Slides adapt Automate the Boring Stuff with Python (CC BY-NC-SA). See NOTICE_v1_2.md. Diagrams are drawn from executed specifications.', { x:0.5, y:4.95, w:9, h:0.3, fontSize:10, italic:true, color:C.mute });
note(s, 'Full verified source list in 03-materials/ch05/rdodi/sen0414_ch05_research_v1_0_0.ttl. Visual specifications: 08-tooling/ch05-deck/visuals_make_v1_0_0.py, output visuals_out_v1_0_0.json. The chapter page’s Resources tab lists the links that were opened and checked.');

// 37 Next
s = dark(); lec('', '', 'Next week: Chapter 6, Lists');
txt(s, 'Next week: Chapter 6 — Lists', { x:0.6, y:1.6, w:8.8, h:0.9, fontFace:H, fontSize:30, bold:true, color:C.white });
txt(s, 'Before then: work through the chapter 5 interactive page — the debugger simulator, the logging table and the exception climb, plus a quiz and subject agents.', { x:0.6, y:2.6, w:8.8, h:1.1, fontSize:17, color:C.yellow, valign:'top' });
txt(s, 'Questions?', { x:0.6, y:4.2, w:8.8, h:0.6, fontFace:H, fontSize:24, italic:true, color:'C9D4E0' });
note(s, 'Chapter 6 of the 3rd edition is Lists. Ask for questions, and remind them the page has the same simulations they saw today, and its Lecture tab has this talk track.');
pres.writeFile({ fileName: process.argv[2] }).then(f => { fs.writeFileSync(process.argv[3], JSON.stringify({ version: VERSION, python: py, slides: LEC.map(l => ({ n: l.n, title: l.title, say: l.say, concept: l.concept, visual: l.visual })) }, null, 1)); console.log('written', f, LEC.length, 'slides'); });
