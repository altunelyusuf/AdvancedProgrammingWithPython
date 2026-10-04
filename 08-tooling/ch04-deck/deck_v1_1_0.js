// SEN0414 chapter 4 - Functions, deck version 1.1.0: a lecture for a three-to-four hour session, built from the
// chapter corpus rather than from a summary of it. Version 1.0.0 covered the chapter in 26 slides written by hand;
// this version covers all 76 concepts of the rewritten corpus, in the taxonomy's own order, with each concept's own
// paragraphs on the slide, its executed example beside them, the chapter's own warning about it underneath, and the
// talk track in the speaker notes. Five diagrams - the call stack, the exception ancestry, the four scope rules, the
// parameter kinds and name resolution - are drawn from specifications this chapter's visuals_make executed.
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
const QB = JSON.parse(fs.readFileSync(path.join(__dirname, '../ch04-page/' + plan.question_bank_file)));

plan.python = EX._python;
plan.concepts_count = Object.keys(plan.concepts).length;
plan.leaf_count = plan.order.filter(id => plan.concepts[id].level === 3).length;
plan.question_bank_size = QB.length;
plan.deck_title = 'Chapter 4: Functions';
plan.deck_strapline = 'Defining, calling, returning - and what decides which variable a name means';
// The approved course outcomes are advanced ones; the chapter page's objectives file records, and this slide repeats,
// that none of them is specific to functions, so the chapter is taught against its own five objectives.
plan.outcome_line = 'The five objectives this chapter is taught and assessed against';
plan.outcome_note = 'Be straight with the room about where these come from: the course has eight approved learning outcomes, and the chapter page\'s objectives record states that none of them is specific to functions, because chapter 4 is the language groundwork the later, library-centred outcomes are built on. These five chapter objectives are what this week is marked against, and the work they prepare is every outcome that asks students to build something.';
plan.next_title = 'Next week: Chapter 5 - Debugging';
plan.next_body = 'Before then: work through the chapter 4 interactive page - the same taxonomy you saw today, with the examples runnable, a question bank and a subject agent for each branch. Bring one function of your own that misbehaves.';
plan.next_note = 'Chapter 5 of the 3rd edition is Debugging, and it is the natural sequel: this week built functions, next week finds out what they are really doing. Ask for questions, and point students at the chapter page, whose Lecture tab carries this talk track.';

const D = LIB.makeDeck(pptxgen, { title: 'SEN0414 Chapter 4 - Functions', python: plan.python });
const C = D.C;

// ---- the chapter's own executed diagrams -----------------------------------------------------------------------
// the call stack: one column per recorded moment of a real run, the frames stacked as they really were
function callStack(s, D, a, ctx) {
  const V = VIS.CallStackOrder, steps = V.steps, n = steps.length;
  D.prose(s, ctx.para(0), a.x, a.y, 9.1, 0.60, 0, [12.5, 12, 11.5]);
  const hy = 2.00, bh = 0.36, base = 4.00, cw = (a.w - 0.12 * (n - 1)) / n;
  steps.forEach((st, i) => {
    const xx = a.x + i * (cw + 0.12), k = i + 1, lab = (st.event === 'call' ? 'call ' : 'return from ') + st.func;
    D.rect(s, { x: xx, y: hy, w: cw, h: 0.30, fill: st.event === 'call' ? C.greenBg : C.redBg, lineColor: st.event === 'call' ? C.green : C.red, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.05 }, 'csh', k);
    D.ftxt(s, lab, { x: xx + 0.03, y: hy, w: cw - 0.06, h: 0.30 }, [10, 9.5, 9, 8.5, 8, 7.5], { bold: true, color: st.event === 'call' ? C.green : C.red, align: 'center' }, 'csht', k);
    st.stack.forEach((fn, j) => {
      const yy = base - (j + 1) * (bh + 0.04);
      D.rect(s, { x: xx, y: yy, w: cw, h: bh, fill: j === st.stack.length - 1 ? C.blue : C.blueBg, lineColor: C.blue, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.05 }, 'csf', k);
      D.ftxt(s, fn, { x: xx + 0.03, y: yy, w: cw - 0.06, h: bh }, [10, 9.5, 9, 8.5, 8, 7.5], { fontFace: D.M, bold: j === st.stack.length - 1, color: j === st.stack.length - 1 ? C.white : C.navy, align: 'center' }, 'csft', k);
    });
    D.ftxt(s, st.out || '(nothing yet)', { x: xx, y: base + 0.06, w: cw, h: 0.56 }, [8, 7.5, 7, 6.5, 6], { fontFace: D.M, color: C.mute, align: 'center', valign: 'top' }, 'cso', k);
  });
  D.band(s, a.x, 4.66, a.w, 0.36, 'Read it as', V.caption + ' The grey text under each column is what the program had printed by that moment.', C.blue, C.blueBg, n + 1);
}
// the exception ancestry: every class the chapter raises, with the chain the interpreter itself reports
function hierarchy(s, D, a, ctx) {
  const V = VIS.ExceptionHierarchy, rows = V.rows;
  D.prose(s, ctx.para(0), a.x, a.y, 9.1, 0.60, 0, [12.5, 12, 11.5]);
  const y0 = 2.00, rh = 0.33;
  rows.forEach((r, i) => {
    const yy = y0 + i * rh, k = i + 2;
    r.chain.forEach((cls, j) => {
      const xx = a.x + j * 2.18, last = j === r.chain.length - 1;
      D.rect(s, { x: xx, y: yy, w: 2.08, h: rh - 0.05, fill: j === 0 ? (r.under_exception ? C.blueBg : C.redBg) : C.card, lineColor: j === 0 ? (r.under_exception ? C.blue : C.red) : C.line, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.05 }, 'ehb', k);
      D.ftxt(s, cls, { x: xx + 0.04, y: yy, w: 2.0, h: rh - 0.05 }, [10, 9.5, 9, 8.5, 8, 7.5], { fontFace: D.M, bold: j === 0, color: j === 0 ? (r.under_exception ? C.navy : C.red) : C.ink, align: 'center' }, 'eht', k);
      if (!last) D.arrow(s, xx + 2.08, yy + (rh - 0.05) / 2, xx + 2.18, yy + (rh - 0.05) / 2, { color: C.line, w: 1 }, k);
    });
  });
  D.ftxt(s, V.caption, { x: a.x, y: 4.68, w: a.w, h: 0.34 }, [11.5, 11, 10.5, 10, 9.5], { color: C.amber, bold: true }, 'ehcap', rows.length + 2);
}
// the four scope rules, each decided by the compiler's own symbol table for a real function
function scopeRules(s, D, a, ctx) {
  const V = VIS.ScopeIdentification;
  D.prose(s, ctx.para(0), a.x, a.y, 4.35, 1.78, 0, [12.5, 12, 11.5]);
  D.rect(s, { x: a.x, y: 3.18, w: 4.35, h: 1.60, fill: C.code, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.1 }, 'scb');
  D.txt(s, V.code.map((l, i, arr) => ({ text: l, options: { color: C.codeTxt, breakLine: i < arr.length - 1 } })),
    { x: a.x + 0.15, y: 3.26, w: 4.05, h: 1.44, fontFace: D.M, fontSize: D.codeSize(V.code, 4.05, 1.44, 10, 6), valign: 'top' }, 'scode');
  D.txt(s, 'the program the symbol table was read from', { x: a.x, y: 4.80, w: 4.35, h: 0.2, fontSize: 8.5, italic: true, color: C.mute, align: 'right' }, 'sccap');
  const x0 = 5.05, w = 4.5, rh = 0.62;
  V.rows.forEach((r, i) => {
    const yy = a.y + i * (rh + 0.08), k = i + 1, isGlobal = r.verdict === 'global';
    D.rect(s, { x: x0, y: yy, w: w - 1.05, h: rh, fill: C.card, lineColor: C.line, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.06 }, 'srb', k);
    D.ftxt(s, r.function + ' - ' + r.condition, { x: x0 + 0.1, y: yy, w: w - 1.25, h: rh }, [10.5, 10, 9.5, 9, 8.5], { color: C.ink }, 'srt', k);
    D.rect(s, { x: x0 + w - 0.98, y: yy, w: 0.98, h: rh, fill: isGlobal ? C.blueBg : C.greenBg, lineColor: isGlobal ? C.blue : C.green, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.06 }, 'srv', k);
    D.ftxt(s, r.verdict, { x: x0 + w - 0.98, y: yy, w: 0.98, h: rh }, [12, 11, 10], { bold: true, color: isGlobal ? C.blue : C.green, align: 'center' }, 'srvt', k);
  });
  D.band(s, x0, 4.20, w, 0.78, 'How it was decided', V.caption, C.amber, C.amberBg, V.rows.length + 1);
}
// the parameter kinds: real calls, and the real text of the TypeError the illegal ones raise
function paramKinds(s, D, a, ctx) {
  const V = VIS.PositionalOnlyParameter;
  D.prose(s, ctx.para(0), a.x, a.y, 4.2, 1.86, 0, [12.5, 12, 11.5]);
  D.rect(s, { x: a.x, y: 3.28, w: 4.2, h: 1.1, fill: C.code, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.1 }, 'pkb');
  D.txt(s, V.code.map((l, i, arr) => ({ text: l, options: { color: C.codeTxt, breakLine: i < arr.length - 1 } })),
    { x: a.x + 0.15, y: 3.36, w: 3.9, h: 0.95, fontFace: D.M, fontSize: D.codeSize(V.code, 3.9, 0.95, 10, 6), valign: 'top' }, 'pkcode');
  const x0 = 4.95, w = 4.6, rh = 0.58;
  V.rows.forEach((r, i) => {
    const yy = a.y + i * (rh + 0.04), k = i + 2;
    D.rect(s, { x: x0, y: yy, w: 1.75, h: rh, fill: C.code, lineColor: C.code, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.05 }, 'pkc', k);
    D.ftxt(s, r.call, { x: x0 + 0.06, y: yy, w: 1.63, h: rh }, [11, 10, 9.5, 9, 8.5, 8], { fontFace: D.M, color: C.yellow }, 'pkct', k);
    D.rect(s, { x: x0 + 1.82, y: yy, w: w - 1.82, h: rh, fill: r.ok ? C.greenBg : C.redBg, lineColor: r.ok ? C.green : C.red, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.05 }, 'pkr', k);
    D.ftxt(s, r.result, { x: x0 + 1.9, y: yy, w: w - 2.0, h: rh }, [10.5, 10, 9.5, 9, 8.5, 8, 7.5, 7], { fontFace: D.M, bold: r.ok, color: r.ok ? C.green : C.red }, 'pkrt', k);
  });
  D.band(s, x0, 4.52, w, 0.48, 'The rule', V.caption, C.blue, C.blueBg, V.rows.length + 2);
}
// name resolution: the same lookup run four times, each time with the name one scope further out
function resolution(s, D, a, ctx) {
  const V = VIS.NameResolution, n = V.rows.length, cw = (a.w - 0.15 * (n - 1)) / n;
  D.prose(s, ctx.para(0), a.x, a.y, 9.1, 0.54, 0, [12.5, 12, 11.5]);
  V.rows.forEach((r, i) => {
    const xx = a.x + i * (cw + 0.15), k = i + 1;
    D.rect(s, { x: xx, y: 1.94, w: cw, h: 0.42, fill: C.blue, lineColor: C.blue, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.06 }, 'nrh', k);
    D.ftxt(s, (i + 1) + '. ' + r.place, { x: xx + 0.05, y: 1.94, w: cw - 0.1, h: 0.42 }, [11, 10.5, 10, 9.5, 9, 8.5, 8, 7.5], { bold: true, color: C.white, align: 'center' }, 'nrht', k);
    D.rect(s, { x: xx, y: 2.40, w: cw, h: 1.55, fill: C.code, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.06 }, 'nrc', k);
    D.txt(s, r.code.map((l, j, arr) => ({ text: l, options: { color: C.codeTxt, breakLine: j < arr.length - 1 } })),
      { x: xx + 0.1, y: 2.46, w: cw - 0.2, h: 1.43, fontFace: D.M, fontSize: D.codeSize(r.code, cw - 0.2, 1.43, 9.5, 6), valign: 'top' }, 'nrct', k);
    D.rect(s, { x: xx, y: 4.00, w: cw, h: 0.38, fill: C.greenBg, lineColor: C.green, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.06 }, 'nrf', k);
    D.ftxt(s, 'found: ' + r.found, { x: xx + 0.05, y: 4.00, w: cw - 0.1, h: 0.38 }, [10, 9.5, 9, 8.5], { fontFace: D.M, bold: true, color: C.green, align: 'center' }, 'nrft', k);
  });
  D.band(s, a.x, 4.48, a.w, 0.52, 'The order', V.caption, C.amber, C.amberBg, n + 1);
}

LECT.buildLecture(D, plan, EX, {
  diagrams: {
    CallStackOrder: callStack,
    ExceptionHierarchy: hierarchy,
    ScopeIdentification: scopeRules,
    PositionalOnlyParameter: paramKinds,
    NameResolution: resolution,
  },
});

D.pres.writeFile({ fileName: process.argv[2] }).then(f => {
  fs.writeFileSync(process.argv[3], JSON.stringify({ version: VERSION, python: plan.python,
    slides: D.LEC.map(l => ({ n: l.n, title: l.title, say: l.say, concept: l.concept, visual: l.visual })) }, null, 1));
  console.log('written', f, D.LEC.length, 'slides');
});
