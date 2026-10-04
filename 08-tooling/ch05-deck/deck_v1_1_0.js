// SEN0414 chapter 5 - Debugging, deck version 1.1.0: a lecture for a three-to-four hour session, built from the
// chapter corpus rather than from a selection of it. Version 1.0.0 was already a lecture, of 37 slides, and the
// diagrams it drew from executed specifications - the recorded debugger, the logging-threshold grid, the exception
// climb, the real traceback with its carets, the level staircase and the loop trace - are kept here unchanged and
// drawn by the same code. What is new is coverage: all 82 concepts of the rewritten corpus, in the taxonomy's own
// order, each with its own paragraphs, its executed example and the chapter's own warning, and the talk track in the
// speaker notes.
// Usage: NODE_PATH=$(npm root -g) node deck_v1_1_0.js out.pptx lecture_out.json
'use strict';
const VERSION = '1.1.0';
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');
const LIB = require('../deck_lib_v1_0_0.js');
const LECT = require('../deck_lecture_v1_0_0.js');

const EX = JSON.parse(fs.readFileSync(path.join(__dirname, 'examples_out_v1_1_0.json')));
const VIS = JSON.parse(fs.readFileSync(path.join(__dirname, 'visuals_out_v1_0_0.json')));
const plan = JSON.parse(fs.readFileSync(path.join(__dirname, 'deck_plan_v1_1_0.json')));
const QB = JSON.parse(fs.readFileSync(path.join(__dirname, '../ch05-page/' + plan.question_bank_file)));

plan.python = EX._python;
plan.concepts_count = Object.keys(plan.concepts).length;
plan.leaf_count = plan.order.filter(id => plan.concepts[id].level === 3).length;
plan.question_bank_size = QB.length;
plan.deck_title = 'Chapter 5: Debugging';
plan.deck_strapline = 'Four ways to find out what a program is really doing';
plan.outcome_line = 'The five objectives this chapter is taught against, and the course outcome they serve';
plan.outcome_note = 'Say where these come from. The five chapter objectives are the chapter page\'s own, and they are what this week is marked against. Behind them stands course outcome LO-6, diagnose and harden programs with logging, tracebacks and deliberately raised exceptions, whose own record in the approved outcomes names chapter 5 of the 3rd edition as its source - so this is the one early chapter that serves an approved outcome directly rather than only preparing for one.';
plan.next_title = 'Next week: Chapter 6 - Lists';
plan.next_body = 'Before then: work through the chapter 5 interactive page - the debugger simulator, the logging table and the exception climb you saw today, all runnable, plus a question bank and a subject agent for each branch. Bring a bug of your own.';
plan.next_note = 'Chapter 6 of the 3rd edition is Lists. Ask for questions, and remind the room that the page has the same simulations they saw today and that its Lecture tab carries this talk track.';

const D = LIB.makeDeck(pptxgen, { title: 'SEN0414 Chapter 5 - Debugging', python: plan.python });
const C = D.C;
const py = plan.python;

// ---- the executed visuals of deck version 1.0.0, kept and drawn by the same code -------------------------------
const stackTxt = e => e.stack.join(' \u203a ');
const varsTxt = e => e.vars.map(([a, b]) => a + ' = ' + b).join('; ') || 'none yet';
const outTxt = e => e.out || '(nothing printed yet)';
const lineTxt = (V, e) => 'stopped at line ' + e.line + (V.breakpoints.includes(e.line) ? ' (breakpoint)' : '');
// the same moves the page's debugger makes: In = the next stop; Over = the next stop at the same depth or shallower;
// Out = the next stop shallower; Continue = the next breakpoint
function dbgTarget(V, i, a) {
  const E = V.events, d = E[i].depth; let j = E.length;
  if (a === 'in') j = i + 1;
  else if (a === 'over') { for (let k = i + 1; k < E.length; k++) if (E[k].depth <= d) { j = k; break; } }
  else if (a === 'out') { for (let k = i + 1; k < E.length; k++) if (E[k].depth < d) { j = k; break; } }
  else if (a === 'cont') { for (let k = i + 1; k < E.length; k++) if (V.breakpoints.includes(E[k].line)) { j = k; break; } }
  return j;
}
function debugPanel(s, id, ev, x, y, w, fs, k, label) {
  const V = VIS[id], E = V.events[ev], n = V.lines.length, lh = fs * 0.0205 + 0.012, codeH = n * lh + 0.16;
  const nx = 'v:' + id + ':e' + ev + ':';
  if (label) D.ftxt(s, label, { x, y: y - 0.3, w, h: 0.28 }, [12, 11, 10, 9.5], { bold: true, color: C.navy }, 'dbglabel', k);
  D.rect(s, { x, y, w, h: codeH, fill: C.code, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.08 }, 'dbgbox', k);
  D.rect(s, { x: x + 0.06, y: y + 0.08 + (E.line - 1) * lh, w: w - 0.12, h: lh, fill: '3B5B87', lineColor: '3B5B87' }, nx + 'hl:box', k);
  V.breakpoints.forEach(b => D.rect(s, { x: x + 0.1, y: y + 0.08 + (b - 1) * lh + lh * 0.18, w: lh * 0.64, h: lh * 0.64, fill: C.red, lineColor: C.red, shape: D.S.OVAL }, nx + 'bp' + b + ':dot', k));
  D.txt(s, V.lines.map((l, i) => ({ text: String(i + 1), options: { color: '8FA3B8', breakLine: i < n - 1 } })),
    { x: x + 0.3, y: y + 0.08, w: 0.3, h: n * lh, fontFace: D.M, fontSize: fs, valign: 'top', align: 'right', lineSpacing: lh * 72 }, 'dbgnums', k);
  D.txt(s, V.lines.map((l, i) => ({ text: l, options: { color: C.codeTxt, breakLine: i < n - 1 } })),
    { x: x + 0.68, y: y + 0.08, w: w - 0.8, h: n * lh, fontFace: D.M, fontSize: fs, valign: 'top', lineSpacing: lh * 72 }, 'dbgcode', k);
  const rows = [['line', lineTxt(V, E), C.navy], ['vars', varsTxt(E), C.ink], ['stack', stackTxt(E), C.ink], ['out', outTxt(E), C.ink]];
  let yy = y + codeH + 0.06;
  const tag = { line: '', vars: 'Variables  ', stack: 'Call stack  ', out: 'Printed  ' };
  rows.forEach(([f, t, col]) => {
    D.rect(s, { x, y: yy, w, h: 0.25, fill: f === 'line' ? C.amberBg : C.card, lineColor: f === 'line' ? C.amber : C.card, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.05 }, 'dbgrow', k);
    if (tag[f]) D.txt(s, tag[f], { x: x + 0.08, y: yy, w: 0.86, h: 0.25, fontSize: 9, bold: true, color: C.mute }, 'dbgtag', k);
    D.ftxt(s, t, { x: x + (tag[f] ? 0.98 : 0.08), y: yy, w: w - (tag[f] ? 1.06 : 0.16), h: 0.25 }, [9.5, 9, 8.5, 8, 7.5, 7], { fontFace: D.M, bold: f === 'line', color: col }, nx + f, k);
    yy += 0.27;
  });
  return yy;
}
function unwindDraw(s, id, x, y, w, k0) {
  const V = VIS[id], F = V.frames, bh = 0.46, gap = 0.20, nx = 'v:' + id + ':';
  const all = F.map((f, i) => ({ head: f.func, line: f.line, text: f.text, name: nx + 'f' + i }))
    .concat([{ head: V.handler.func, line: V.handler.line, text: V.handler.text, name: nx + 'handler' }]);
  all.forEach((f, i) => {
    const yy = y + i * (bh + gap), last = i === all.length - 1;
    const col = i === 0 ? [C.redBg, C.red] : last ? [C.greenBg, C.green] : [C.card, C.line];
    D.rect(s, { x, y: yy, w, h: bh, fill: col[0], lineColor: col[1], lw: 2, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.08 }, 'uwbox', 0);
    D.ftxt(s, f.head + '  \u00b7  line ' + f.line + '  \u00b7  ' + f.text, { x: x + 0.12, y: yy, w: w - 0.24, h: bh }, [11, 10.5, 10, 9.5, 9, 8.5],
      { fontFace: D.M, bold: i === 0 || last, color: i === 0 ? C.red : last ? C.green : C.ink }, f.name, 0);
    if (i < all.length - 1) {
      const kk = k0 + 1 + i;
      D.arrow(s, x + w / 2, yy + bh, x + w / 2, yy + bh + gap, { color: last ? C.green : C.red, w: 2.5 }, kk);
      D.ftxt(s, i < all.length - 2 ? 'no handler here \u2014 leave the function' : 'a matching except clause: caught',
        { x: x + w / 2 + 0.12, y: yy + bh, w: w / 2 - 0.12, h: gap }, [10, 9.5, 9, 8.5, 8], { italic: true, color: i < all.length - 2 ? C.red : C.green }, 'uwlab', kk);
    }
  });
  D.txt(s, 'raise ' + V.exc, { x: x + w - 1.9, y: y - 0.32, w: 1.9, h: 0.28, fontFace: D.M, fontSize: 11, bold: true, color: C.red, align: 'right' }, nx + 'exc', k0);
}
function levelsGrid(s, id, x, y, w, k0) {
  const V = VIS[id], n = V.settings.length, lw = 2.4, cw = (w - lw) / n, rh = 0.46, nx = 'v:' + id + ':';
  V.messages.forEach((m, r) => D.ftxt(s, m.call, { x: x + 0.05, y: y + 0.44 + r * rh, w: lw - 0.1, h: rh - 0.05 }, [9, 8.5, 8, 7.5], { fontFace: D.M, color: C.navy, bold: true }, nx + 'm' + r, 0));
  V.settings.forEach((t, c) => {
    const cx = x + lw + c * cw, kk = k0 ? k0 + c : 0;
    D.rect(s, { x: cx, y, w: cw - 0.04, h: 0.4, fill: C.navy, lineColor: C.navy }, 'lvhead', kk);
    D.ftxt(s, t.label.replace(/^(level=|no )/, '$1\n').replace(/^disable/, 'disable\n'), { x: cx + 0.02, y, w: cw - 0.08, h: 0.4 }, [8.5, 8, 7.5, 7], { fontFace: D.M, bold: true, color: C.white, align: 'center' }, nx + 'h' + c, kk);
    V.messages.forEach((m, r) => {
      const on = t.shown[r];
      D.rect(s, { x: cx, y: y + 0.44 + r * rh, w: cw - 0.04, h: rh - 0.05, fill: on ? C.greenBg : C.card, lineColor: on ? C.green : C.card }, 'lvcellbox', kk);
      D.ftxt(s, on ? 'shown' : 'hidden', { x: cx, y: y + 0.44 + r * rh, w: cw - 0.04, h: rh - 0.05 }, [11, 10, 9.5, 9], { bold: on, color: on ? C.green : C.mute, align: 'center' }, nx + 'c' + c + 'r' + r, kk);
    });
  });
}
function tbCard(s, name, text, x, y, w, h, k) {
  D.rect(s, { x, y, w, h, fill: C.code, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.1 }, 'tbbox', k);
  const L = text.split('\n');
  D.txt(s, L.map((l, i) => ({ text: l, options: { color: i === L.length - 1 ? C.errTxt : /^\s+[~^]+\s*$/.test(l) ? C.yellow : /^\s*File /.test(l) ? '8FB8E8' : i === 0 ? '8FA3B8' : C.codeTxt, breakLine: i < L.length - 1 } })),
    { x: x + 0.17, y: y + 0.1, w: w - 0.34, h: h - 0.2, fontFace: D.M, fontSize: D.codeSize(L, w - 0.34, h - 0.2, 11, 5.5), valign: 'top', paraSpaceAfter: 0 }, name, k);
  D.txt(s, 'the text a real interpreter wrote to standard error, under Python ' + py, { x, y: y + h + 0.02, w, h: 0.2, fontSize: 8.5, italic: true, color: C.mute, align: 'right' }, 'tbcap', k);
}
function traceTable(s, id, run, x, y, w, rowH, k0) {
  const V = VIS[id], R = V.runs[run];
  const cols = [['n', 'Pass', 0.6]].concat(V.watch.map((v, i) => ['v' + i, v, 1.1]));
  if (R.rows.some(r => r.cond !== null)) cols.push(['cond', 'Test', 0.9]);
  cols.push(['ev', 'What happens', 0]); cols.push(['out', 'Printed', 0]);
  const fixed = cols.reduce((a, c) => a + c[2], 0), flex = cols.filter(c => c[2] === 0).length;
  cols.forEach(c => { if (c[2] === 0) c[2] = (w - fixed) / flex; });
  const cx = []; let acc = x; cols.forEach(c => { cx.push(acc); acc += c[2]; });
  cols.forEach((c, j) => {
    D.rect(s, { x: cx[j], y, w: c[2] - 0.04, h: 0.32, fill: C.navy, lineColor: C.navy }, 'tth');
    D.ftxt(s, c[1], { x: cx[j] + 0.06, y, w: c[2] - 0.16, h: 0.32 }, [11, 10, 9.5, 9], { bold: true, color: C.white, fontFace: c[0].startsWith('v') ? D.M : D.B }, 'ttht');
  });
  R.rows.forEach((r, i) => {
    const yy = y + 0.36 + i * rowH;
    const cells = { n: String(r.n), cond: r.cond === null ? '' : (r.cond ? 'True' : 'False'), ev: r.events.join('; ') || 'reached the bottom', out: r.out };
    r.vals.forEach((v, j) => cells['v' + j] = v);
    cols.forEach((c, j) => {
      const isEv = c[0] === 'ev';
      const col = isEv && r.events.length ? [C.greenBg, C.green] : [C.card, C.ink];
      D.rect(s, { x: cx[j], y: yy, w: c[2] - 0.04, h: rowH - 0.05, fill: col[0], lineColor: col[0] }, 'ttb', k0 ? k0 + i : 0);
      D.ftxt(s, cells[c[0]] || '', { x: cx[j] + 0.06, y: yy, w: c[2] - 0.16, h: rowH - 0.05 }, [11, 10.5, 10, 9.5, 9, 8.5],
        { color: col[1], bold: isEv, fontFace: (c[0].startsWith('v') || c[0] === 'out') ? D.M : D.B }, 'v:' + id + ':' + run + ':' + i + ':' + c[0], k0 ? k0 + i : 0);
    });
  });
}
function staircase(s, x, y, w, k0) {
  const L = [...EX.levels[0][1].matchAll(/\('(\w+)', (\d+)\)/g)].map(m => [m[1], +m[2]]);
  const gap = 0.12, bw = (w - gap * 4) / 5, base = y + 2.3;
  const cols = [C.blueBg, C.blueBg, C.amberBg, C.redBg, C.redBg], lines = [C.blue, C.blue, C.amber, C.red, C.red];
  L.forEach(([nme, num], i) => {
    const h = 0.7 + i * 0.36, xx = x + i * (bw + gap);
    D.rect(s, { x: xx, y: base - h, w: bw, h, fill: cols[i], lineColor: lines[i], lw: 2, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.08 }, 'stair', 0);
    D.txt(s, [{ text: nme, options: { fontFace: D.M, bold: true, fontSize: 13, color: lines[i], breakLine: true } },
      { text: String(num), options: { fontSize: 18, bold: true, color: C.navy, breakLine: true } },
      { text: 'logging.' + nme.toLowerCase() + '()', options: { fontFace: D.M, fontSize: 9, color: C.mute } }],
      { x: xx, y: base - h, w: bw, h, align: 'center' }, 'stairt', 0);
  });
  [0, 1].forEach(i => {
    const h = 0.7 + i * 0.36, xx = x + i * (bw + gap);
    D.rect(s, { x: xx, y: base - h, w: bw, h, fill: 'DDE3EA', lineColor: 'DDE3EA', shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.08, transparency: 12 }, 'hide', k0);
    D.txt(s, 'hidden at this threshold', { x: xx, y: base + 0.04, w: bw, h: 0.26, fontSize: 9, bold: true, color: C.mute, align: 'center' }, 'hidet', k0);
  });
  const ty = base - (0.7 + 2 * 0.36) - 0.06;
  D.arrow(s, x - 0.05, ty, x + w + 0.05, ty, { color: C.red, w: 2.5, dash: 'dash', noHead: true }, k0);
}

// ---- the concepts whose slide is one of those executed diagrams -------------------------------------------------
const diagrams = {
  InstrumentChoice(s, D, a, ctx) {
    D.prose(s, ctx.para(0), a.x, a.y, 9.1, 0.62, 0, [12.5, 12, 11.5]);
    const inst = [['raise', 'Can the caller fix this?', 'Tell the caller', 'raise Exception(...)', C.blue],
      ['assert', 'Must this be true if my code is right?', 'Stop the program', 'assert x > 0', C.red],
      ['log', 'What did the program do?', 'Leave a record', 'logging.debug(...)', C.green],
      ['step', 'What is the state at this line?', 'Pause and look', 'breakpoint()', C.amber]];
    inst.forEach(([n, q, d, code, col], i) => {
      const xx = a.x + i * 2.32, k = i + 1;
      D.rect(s, { x: xx, y: 2.06, w: 2.18, h: 2.94, fill: C.card, lineColor: col, lw: 2, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.1 }, 'inst', k);
      D.ftxt(s, n, { x: xx + 0.14, y: 2.14, w: 1.9, h: 0.5 }, [22, 20, 18], { fontFace: D.M, bold: true, color: col }, 'instn', k);
      D.ftxt(s, q, { x: xx + 0.14, y: 2.70, w: 1.9, h: 1.1 }, [14, 13, 12, 11.5], { italic: true, color: C.ink, valign: 'top' }, 'instq', k);
      D.ftxt(s, d, { x: xx + 0.14, y: 3.86, w: 1.9, h: 0.46 }, [16, 15, 14, 13], { fontFace: D.H, bold: true, color: C.navy }, 'instd', k);
      D.ftxt(s, code, { x: xx + 0.14, y: 4.40, w: 1.9, h: 0.46 }, [11, 10.5, 10, 9.5], { fontFace: D.M, color: C.mute }, 'instc', k);
    });
  },
  ExceptionUnwinding(s, D, a, ctx) {
    unwindDraw(s, 'ExceptionUnwinding', 2.0, 1.70, 6.0, 1);
    D.band(s, a.x, 4.42, a.w, 0.58, 'The climb', VIS.ExceptionUnwinding.caption, C.amber, C.amberBg, 5);
  },
  TracebackReading(s, D, a, ctx) {
    tbCard(s, 'v:ExceptionUnwinding:tb', VIS.ExceptionUnwinding.traceback, a.x, 1.34, 5.9, 3.3, 0);
    const tbn = [['1', 'The last line', 'names the exception class and its message'],
      ['2', 'Outermost first', 'the frame that raised is the one just above the last line'],
      ['3', 'Four parts a frame', 'file, line, function, and the source line itself']];
    tbn.forEach(([n, h, b], i) => D.card(s, 6.5, 1.34 + i * 1.14, 3.05, 1.04, n + '  ' + h, b, [C.red, C.blue, C.blue][i], i + 1));
    D.band(s, a.x, 4.76, a.w, 0.26, 'Read it', 'from the bottom up', C.amber, C.amberBg, 4);
  },
  FineGrainedLocations(s, D, a, ctx) {
    D.prose(s, ctx.para(0), a.x, a.y, 4.3, 1.5, 0, [12.5, 12, 11.5]);
    tbCard(s, 'v:FineGrainedLocations:text', VIS.FineGrainedLocations.text, a.x, 2.96, 4.3, 1.6, 1);
    D.rect(s, { x: 5.05, y: a.y, w: 4.5, h: 1.2, fill: C.code, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.1 }, 'fgc');
    const src = VIS.FineGrainedLocations.code.replace(/\n+$/, '').split('\n');
    D.txt(s, src.map((l, i, arr) => ({ text: l, options: { color: C.codeTxt, breakLine: i < arr.length - 1 } })),
      { x: 5.2, y: a.y + 0.08, w: 4.2, h: 1.04, fontFace: D.M, fontSize: D.codeSize(src, 4.2, 1.04, 11, 6), valign: 'top' }, 'fgct');
    D.card(s, 5.05, 2.68, 4.5, 2.32, 'What the carets mark', ctx.para(3), C.blue, 2);
  },
  LoggingLevels(s, D, a, ctx) {
    D.ftxt(s, 'level=logging.WARNING: a message is shown when its own number is at least the threshold\'s, so the two steps below the dashed line disappear',
      { x: a.x, y: 1.32, w: a.w, h: 0.32 }, [12, 11.5, 11, 10.5], { bold: true, color: C.red }, 'thr', 1);
    staircase(s, 0.6, 1.70, 8.8, 1);
    D.band(s, a.x, 4.34, a.w, 0.66, 'The rule', ctx.para(3), C.blue, C.blueBg, 2);
  },
  LevelThreshold(s, D, a, ctx) {
    levelsGrid(s, 'LevelThreshold', a.x, 1.36, 9.1, 1);
    D.band(s, a.x, 4.30, a.w, 0.70, 'Read the grid', 'Every cell is what a real run of the same five calls printed at that setting. The first column has no basicConfig at all; the last is logging.disable(CRITICAL).', C.blue, C.blueBg, 9);
  },
  OffByOneRange(s, D, a, ctx) {
    traceTable(s, 'OffByOneRange', 0, a.x, 1.34, 9.1, 0.56, 1);
    D.band(s, a.x, 4.36, a.w, 0.64, 'What the trace shows', VIS.OffByOneRange.caption, C.amber, C.amberBg, 8);
  },
  Breakpoint(s, D, a, ctx) {
    const V = VIS.Breakpoint, b = dbgTarget(V, 0, 'cont');
    debugPanel(s, 'Breakpoint', 0, a.x, 1.66, 4.1, 9.5, 0, 'Start: stopped on the first line');
    debugPanel(s, 'Breakpoint', b, 5.45, 1.66, 4.1, 9.5, 1, 'After Continue: the breakpoint at line ' + V.events[b].line);
    D.arrow(s, 4.6, 2.5, 5.4, 2.5, { color: C.green, w: 3 }, 1);
  },
  ContinueControl(s, D, a, ctx) {
    const V = VIS.ContinueControl, i0 = 0, i1 = dbgTarget(V, i0, 'cont'), i2 = dbgTarget(V, i1, 'cont');
    debugPanel(s, 'ContinueControl', i0, a.x, 1.66, 2.9, 9, 0, 'Start');
    debugPanel(s, 'ContinueControl', i1, 3.55, 1.66, 2.9, 9, 1, 'Continue \u2192 line ' + V.events[i1].line);
    debugPanel(s, 'ContinueControl', i2, 6.65, 1.66, 2.9, 9, 2, 'Continue again \u2192 line ' + V.events[i2].line);
  },
  StepIn(s, D, a, ctx) {
    const V = VIS.StepIn, i0 = V.events.findIndex(e => e.line === 6), i1 = dbgTarget(V, i0, 'in'), i2 = dbgTarget(V, i0, 'over');
    debugPanel(s, 'StepIn', i0, a.x, 1.66, 2.9, 9, 0, 'Stopped at line ' + V.events[i0].line);
    debugPanel(s, 'StepIn', i1, 3.55, 1.66, 2.9, 9, 1, 'Step In \u2192 line ' + V.events[i1].line + ', inside add');
    debugPanel(s, 'StepIn', i2, 6.65, 1.66, 2.9, 9, 2, 'Step Over \u2192 line ' + V.events[i2].line + ', after add');
  },
  StepOver(s, D, a, ctx) {
    const V = VIS.StepOver, i0 = V.events.findIndex(e => e.line === 6), i1 = dbgTarget(V, i0, 'over');
    debugPanel(s, 'StepOver', i0, a.x, 1.66, 4.1, 9.5, 0, 'Stopped at line ' + V.events[i0].line + ', which calls add');
    debugPanel(s, 'StepOver', i1, 5.45, 1.66, 4.1, 9.5, 1, 'Step Over \u2192 line ' + V.events[i1].line + ', the call ran whole');
    D.arrow(s, 4.6, 2.5, 5.4, 2.5, { color: C.blue, w: 3 }, 1);
  },
  StepOut(s, D, a, ctx) {
    const V = VIS.StepOut, i0 = V.events.findIndex(e => e.line === 2), i1 = dbgTarget(V, i0, 'out');
    debugPanel(s, 'StepOut', i0, a.x, 1.66, 4.1, 9.5, 0, 'Stopped inside add, at line ' + V.events[i0].line);
    debugPanel(s, 'StepOut', i1, 5.45, 1.66, 4.1, 9.5, 1, 'Step Out \u2192 line ' + V.events[i1].line + ', back in main');
    D.arrow(s, 4.6, 2.5, 5.4, 2.5, { color: C.blue, w: 3 }, 1);
  },
};
function PRG() { return EX._programs; }

LECT.buildLecture(D, plan, EX, { diagrams: diagrams });

D.pres.writeFile({ fileName: process.argv[2] }).then(f => {
  fs.writeFileSync(process.argv[3], JSON.stringify({ version: VERSION, python: plan.python,
    slides: D.LEC.map(l => ({ n: l.n, title: l.title, say: l.say, concept: l.concept, visual: l.visual })) }, null, 1));
  console.log('written', f, D.LEC.length, 'slides');
});
