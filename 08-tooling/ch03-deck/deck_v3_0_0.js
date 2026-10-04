// SEN0414 chapter 3 lecture deck, version 3.0.0.
//
// 3.0.0 replaces the 30-slide deck v2.0.x, which was written before the chapter corpus existed and covered the book's
// own loop material. This version is built from sen0414_ch03_corpus_v1_0_0.py: it walks the corpus taxonomy in the
// taxonomy's own order - five branches, seventeen groups, fifty-two leaf concepts - gives every concept its own slide,
// and shows the concept's worked example with the output that executing it produced. Because the structure and almost
// all of the text are new, this is a MAJOR bump.
//
// Nothing on a slide is typed from memory. Shell results and program transcripts come from examples_out_v2_0_0.json,
// written by running examples_v2_0_0.py - whose whole programs are the chapter corpus's own - under the course
// interpreter; the source list comes from sources_out_v1_0_0.json, read out of the chapter's RDODI research record;
// the questions come from the chapter's own question bank; the prose is compressed, for speaking, from the corpus
// paragraphs, and every claim the corpus takes from the textbook or the documentation keeps its author-year citation.
//
// Usage: node deck_v3_0_0.js <out.pptx>
const VERSION = "3.0.0";
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const EX = JSON.parse(fs.readFileSync(__dirname + '/examples_out_v2_0_0.json'));
const SRC = JSON.parse(fs.readFileSync(__dirname + '/sources_out_v1_0_0.json'));
const OBJ = JSON.parse(fs.readFileSync(__dirname + '/../ch03-page/objectives_v1_0_0.json'));
const BANK = JSON.parse(fs.readFileSync(__dirname + '/../ch03-page/question_bank_v1_1_0.json'));
const CH = require(__dirname + '/deck_content_v1_0_0.js');
const PG = EX._programs, py = EX._python;

const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9';
pres.author = 'Yusuf Altunel'; pres.title = 'SEN0414 Chapter 3 - Loops and Modules';
pres.subject = 'Lecture deck built from the chapter 3 corpus and its executed examples';
const K = require(__dirname + '/../ch02-deck/deck_kit_v1_0_0.js')(pres);
const { C, H, B, M, HT, TOP, FLOOR, LX, LW, RX, RW, FW, DEFS, CODES } = K;
const note = (s, t) => s.addNotes(t);
const rows = key => EX[key].map(([c, r]) => [c, r]);
// the directory the build happened to run in is removed from a file name inside an error report; nothing else is
const errLine = l => l.replace(/File "[^"]*[\\/]/, 'File "');
const warnLine = r => (r.errlines.find(l => l.includes('SyntaxWarning')) || '').replace(/^.*?([A-Za-z]*Warning:)/, '$1');
let built = 0;

// ---------------- pictures ----------------
function outLines(r, mode) {
  if (mode === 'fail') return r.lines.filter(l => l[0][0] !== '').map(l => [l.map(x => x[0]).join(''), C.green])
                                     .concat(r.errlines.map(l => [errLine(l), C.red]));
  if (mode === 'warn') return r.lines.map(l => [l.map(x => x[0]).join(''), C.green]).concat([[warnLine(r), C.yellow]]);
  return r.lines.map(l => [l.map(x => x[0]).join(''), l.length > 1 ? C.yellow : C.green]);
}
function programPlan(name, cap, mode) {
  const p = PG[name], r = p.runs[0];
  const src = p.code.replace(/\n$/, '').split('\n');
  const out = outLines(r, mode).map(l => l[0]);
  let fs2 = Math.min(K.fitCode(src, 5.00, CODES, cap), K.fitCode(out.length ? out : [' '], 3.90, CODES, cap));
  const hh = f => Math.max(K.codeH(src, 5.00, f), K.codeH(out.length ? out : [' '], 3.90, f));
  while (fs2 > 5 && hh(fs2) > cap) fs2 -= 0.5;      // a long program is set smaller rather than allowed off the page
  return { name, src, r, mode, fs:fs2, h: hh(fs2) };
}
function programDraw(s, y, plan) {
  const out = outLines(plan.r, plan.mode);
  K.plainCode(s, plan.src.map(l => [l, l.trim().startsWith('#') ? '8B949E' : C.codeTxt]), LX, y, 5.00, { fs:plan.fs });
  K.plainCode(s, out.length ? out : [[' ', C.green]], 5.65, y, 3.90, { fs:plan.fs, fill:C.deep });
  const tail = plan.mode === 'fail' ? '; its error output in red'
             : plan.mode === 'warn' ? '; the warning its compilation produced in yellow'
             : (plan.r.lines.some(l => l.length > 1) ? '; typed input in yellow' : '');
  K.caption(s, plan.name + ', run under Python ' + py + tail, LX, y + plan.h - 0.24, FW);
  return plan.h;
}
// the transcript of a run whose listing is shown elsewhere in the deck
function transcriptBlock(s, y, name, cap, w) {
  const r = PG[name].runs[0], out = outLines(r, null);
  let h;
  if (out.length > 8) h = cols2(s, out, y, cap - 0.26, C.deep);
  else { const fs2 = K.fitCode(out.map(l => l[0]), w, CODES, cap); h = K.plainCode(s, out, LX, y, w, { fs:fs2, fill:C.deep }); }
  K.caption(s, 'a real run of ' + name + ' under Python ' + py + '; typed input in yellow', LX, y + h + 0.02, w);
  return h + 0.26;
}
// two programs side by side, each with the output of its own run underneath
function pairPlan(names, cap) {
  const cw = 4.48;
  let fs2 = 12;
  const of2 = names.map(n => outLines(PG[n].runs[0], PG[n].mayfail ? 'fail' : null).map(l => l[0]));
  const src = names.map(n => PG[n].code.replace(/\n$/, '').split('\n'));
  for (const c of [12, 11, 10, 9, 8, 7]) {
    fs2 = c;
    const hh = Math.max(...names.map((n, i) => 0.28 + K.codeH(src[i], cw, c) - 0.26 + 0.08 + K.codeH(of2[i], cw, c) - 0.26));
    if (hh + 0.26 <= cap && src.concat(of2).every(ls => ls.every(l => l.length <= Math.floor((cw - 0.44) * 72 / (0.605 * c))))) break;
  }
  const h = Math.max(...names.map((n, i) => 0.28 + K.codeH(src[i], cw, fs2) - 0.26 + 0.08 + K.codeH(of2[i], cw, fs2) - 0.26));
  return { names, cw, fs:fs2, src, of2, h: h + 0.26 };
}
function pairDraw(s, y, plan) {
  plan.names.forEach((n, i) => {
    const x = LX + i * (plan.cw + 0.14);
    s.addText(n, { x, y, w:plan.cw, h:0.24, fontFace:B, fontSize:10, bold:true, color:C.blue, margin:0, valign:'middle', isTextBox:true });
    const h1 = K.plainCode(s, plan.src[i].map(l => [l, C.codeTxt]), x, y + 0.28, plan.cw, { fs:plan.fs });
    K.plainCode(s, outLines(PG[n].runs[0], PG[n].mayfail ? 'fail' : null), x, y + 0.36 + h1, plan.cw, { fs:plan.fs, fill:C.deep });
  });
  K.caption(s, 'both programs run under Python ' + py + '; each output is the output of the program above it', LX, y + plan.h - 0.24, FW);
  return plan.h;
}
// a block of code or output set in two columns, so that a long one still fits on one slide
function cols2(s, lines, y, cap, fill) {
  const half = Math.ceil(lines.length / 2), cw = 4.68;
  const cols = [lines.slice(0, half), lines.slice(half)];
  const txt = lines.map(l => (typeof l === 'string' ? l : l[0]) || ' ');
  let fs2 = 6;
  for (const c of [12, 11, 10, 9, 8, 7, 6]) {
    fs2 = c;
    const hh = Math.max(...cols.map(col => K.codeH(col.map(l => (typeof l === 'string' ? l : l[0]) || ' '), cw, c))) - 0.26;
    if (hh <= cap && txt.every(l => l.length <= Math.floor((cw - 0.44) * 72 / (0.605 * c)))) break;
  }
  cols.forEach((col, i) => { if (col.length) K.plainCode(s, col, LX + i * (cw + 0.14), y, cw, { fs:fs2, fill }); });
  return Math.max(...cols.map(col => col.length ? K.codeH(col.map(l => (typeof l === 'string' ? l : l[0]) || ' '), cw, fs2) - 0.26 : 0));
}
function listing(s, y, name, cap) {
  const src = PG[name].code.replace(/\n$/, '').split('\n');
  const h = cols2(s, src.map(l => [l, l.trim().startsWith('#') ? '8B949E' : C.codeTxt]), y, cap - 0.26, C.code);
  K.caption(s, 'the complete listing of ' + name + ', read the left column first', LX, y + h + 0.02, FW);
  return h + 0.26;
}
// the two-loop structure of the chapter's second game, and the three ways out of it
function structure(s, y, w, cap) {
  const h = Math.min(cap, 2.10);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:LX, y, w, h, fill:{color:C.card}, line:{color:C.blue}, rectRadius:0.10 });
  s.addText('the main game loop  ·  one game each time round', { x:LX + 0.16, y:y + 0.08, w:w - 0.32, h:0.26, fontFace:B, fontSize:11, bold:true, color:C.blue, margin:0, valign:'middle', isTextBox:true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:LX + 0.30, y:y + 0.40, w:w - 0.60, h:0.74, fill:{color:C.white}, line:{color:C.yellow}, rectRadius:0.08 });
  s.addText('the player input loop  ·  keeps asking until the move is r, p, s or q', { x:LX + 0.46, y:y + 0.44, w:w - 0.92, h:0.26, fontFace:B, fontSize:10.5, bold:true, color:'8B6B00', margin:0, valign:'middle', isTextBox:true });
  s.addText('q → sys.exit() leaves the program   ·   r, p, s → break leaves this loop   ·   anything else → ask again',
            { x:LX + 0.46, y:y + 0.72, w:w - 0.92, h:0.34, fontFace:B, fontSize:10, color:C.ink, margin:0, valign:'middle', isTextBox:true });
  s.addText('then: the computer draws a move, the chain of comparisons decides the winner, and one of the three scores is increased',
            { x:LX + 0.30, y:y + 1.22, w:w - 0.60, h:0.40, fontFace:B, fontSize:10.5, color:C.ink, margin:0, valign:'top', isTextBox:true });
  K.caption(s, 'the structure of the listing shown two slides back (Sweigart, 2025)', LX, y + h - 0.24, w);
  return h;
}
// a message the chapter corpus produced, quoted with the way it was produced
function quoteBlock(s, y, w, text, provenance) {
  const h = K.plainCode(s, [[text, C.red]], LX, y, w, { fs:12, fill:C.deep });
  s.addText(provenance, { x:LX, y:y + h + 0.04, w, h:0.46, fontFace:B, fontSize:9.5, italic:true, color:C.mute, margin:0, valign:'top', isTextBox:true });
  return h + 0.52;
}

// ================================ front ================================
let s = K.dark();
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:0.6, y:1.05, w:1.2, h:0.8, fill:{color:C.yellow}, line:{color:C.yellow}, rectRadius:0.12 });
s.addText('>>>', { x:0.6, y:1.05, w:1.2, h:0.8, fontFace:M, fontSize:30, bold:true, color:C.navy, align:'center', valign:'middle', margin:0, isTextBox:true });
s.addText('Chapter 3: Loops and Modules', { x:0.6, y:2.05, w:8.8, h:0.80, fontFace:H, fontSize:38, bold:true, color:C.white, margin:0, isTextBox:true });
s.addText('while and for, what a loop walks through, break, continue and the loop else, and the import statement',
          { x:0.6, y:2.90, w:8.8, h:0.70, fontFace:B, fontSize:16, italic:true, color:C.yellow, margin:0, valign:'top', isTextBox:true });
s.addText('SEN0414 Advanced Programming · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University',
          { x:0.6, y:4.35, w:8.8, h:0.34, fontFace:B, fontSize:13, color:'C9D4E0', margin:0, isTextBox:true });
s.addText('Automate the Boring Stuff with Python, 3rd edition, chapter 3 (Sweigart, 2025), renewed for an advanced course',
          { x:0.6, y:4.72, w:8.8, h:0.34, fontFace:B, fontSize:11, italic:true, color:'8FA3B8', margin:0, isTextBox:true });
note(s, 'Open with the book\'s own claim for this chapter: the two kinds of loop open up the full power of automation, because they can run lines of code millions of times per second (Sweigart, 2025). Say that chapter 2 taught a program to choose and this one teaches it to repeat, and that almost every useful program in the rest of the course is built around at least one loop. Every result in this deck was produced by running the code under Python ' + py + ', and every claim beyond the book comes from the chapter\'s research record.');
built++;

s = K.light(); K.title(s, 'What this session covers', 'The chapter\'s four objectives, and where they sit in the course');
Object.keys(OBJ).filter(k => !k.startsWith('_')).forEach((k, i) => {
  const y = 1.30 + i * 0.66;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:LX, y, w:0.80, h:0.54, fill:{color:C.blue}, line:{color:C.blue}, rectRadius:0.07 });
  s.addText(k.replace('CO', 'CO-'), { x:LX, y, w:0.80, h:0.54, fontFace:H, fontSize:13, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true });
  s.addText(OBJ[k][0], { x:1.38, y, w:6.9, h:0.54, fontFace:B, fontSize:12, color:C.ink, valign:'middle', margin:0, isTextBox:true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:8.45, y:y + 0.09, w:1.10, h:0.36, fill:{color:C.card}, line:{color:C.card}, rectRadius:0.06 });
  s.addText(OBJ[k][1], { x:8.45, y:y + 0.09, w:1.10, h:0.36, fontFace:B, fontSize:11, italic:true, color:C.mute, align:'center', valign:'middle', margin:0, isTextBox:true });
});
const loText = OBJ._note + ' The import statement taught in the fourth branch is nevertheless the door to every library the course later uses.';
K.card(s, LX, 4.04, FW, 'Which course outcomes this chapter serves', loText, C.blue, { fs:K.fitFs(loText, 8.70, 0.62, [12.5, 12, 11.5, 11, 10.5, 10], B), hf:14 });
note(s, 'Read the four chapter objectives and say the session is built to reach them in order. Then be straight about the last card: the course\'s approved outcomes are advanced, and the chapter objectives for loops are not claimed to serve one - that is what the chapter\'s own objectives file records, and inventing a link would be worse than admitting there is none. Say what is true instead: the import statement in the fourth branch is the first step of every library the course later uses.');
built++;

s = K.light();
const nG = CH.reduce((n, b) => n + b.groups.length, 0), nL = CH.reduce((n, b) => n + b.groups.reduce((m, g) => m + g.leaves.length, 0), 0);
K.title(s, 'The chapter as a map', CH.length + ' branches, ' + nG + ' groups, ' + nL + ' concepts — and the order we take them in');
CH.forEach((br, i) => {
  const x = 0.42 + i * 1.86;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y:1.26, w:1.70, h:0.62, fill:{color:C.navy}, line:{color:C.navy}, rectRadius:0.08 });
  s.addText(br.roman + '.  ' + br.label, { x:x + 0.05, y:1.26, w:1.60, h:0.62, fontFace:H, fontSize:10, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true });
  br.groups.forEach((g, j) => {
    const gy = 2.00 + j * 0.74;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y:gy, w:1.70, h:0.64, fill:{color:C.card}, line:{color:C.line}, rectRadius:0.06 });
    s.addText(g.label, { x:x + 0.06, y:gy, w:1.58, h:0.64, fontFace:B, fontSize:8.5, color:C.ink, align:'center', valign:'middle', margin:0, isTextBox:true });
    s.addText(String(g.leaves.length), { x:x + 1.42, y:gy + 0.03, w:0.24, h:0.18, fontFace:B, fontSize:7.5, bold:true, color:C.blue, align:'center', margin:0, isTextBox:true });
  });
});
s.addText('The small number on each group is how many concepts it holds. The order on this map is the order of the session.',
          { x:0.42, y:5.02, w:9.16, h:0.30, fontFace:B, fontSize:11.5, italic:true, color:C.mute, margin:0, isTextBox:true });
note(s, 'Leave this up long enough for the class to copy it. Say that the first branch and the third are the book\'s own chapter, that the second is the supply of values a for loop needs and goes well beyond the book, that the fourth is the import statement the book introduces in passing and the course depends on, and that the fifth is what current Python adds. Promise to show the map again at each branch so nobody loses their place.');
built++;

// ================================ branches ================================
CH.forEach(br => {
  s = K.dark();
  s.addText(br.roman, { x:0.6, y:1.05, w:1.3, h:1.0, fontFace:H, fontSize:54, bold:true, color:C.yellow, margin:0, valign:'middle', isTextBox:true });
  s.addText(br.label, { x:1.95, y:1.15, w:7.5, h:0.80, fontFace:H, fontSize: br.label.length > 24 ? 26 : 32, bold:true, color:C.white, margin:0, valign:'middle', isTextBox:true });
  s.addText(br.blurb, { x:0.6, y:2.35, w:8.8, h:K.estH(br.blurb, 8.8, 15, B) + 0.10, fontFace:B, fontSize:15, color:'C9D4E0', margin:0, valign:'top', isTextBox:true });
  s.addText(br.groups.map(g => g.label).join('   ·   '), { x:0.6, y:4.46, w:8.8, h:0.56, fontFace:B, fontSize:11.5, italic:true, color:C.yellow, margin:0, valign:'top', isTextBox:true });
  note(s, br.note); built++;

  br.groups.forEach(g => {
    s = K.light(); K.title(s, g.label, g.sub);
    if (g.listing) {
      const bh = K.card(s, LX, TOP, FW, null, g.body, C.blue, { fs:K.fitFs(g.body, FW - 0.40, 1.10, DEFS, B) });
      listing(s, TOP + bh + 0.12, g.listing, FLOOR - TOP - bh - 0.12);
    } else if (g.transcript) {
      const th = Math.min(1.70, FLOOR - TOP - 1.00);
      const bh = K.card(s, LX, TOP, FW, null, g.body, C.blue, { fs:K.fitFs(g.body, FW - 0.40, FLOOR - TOP - th - 0.30, DEFS, B) });
      transcriptBlock(s, TOP + bh + 0.12, g.transcript, FLOOR - TOP - bh - 0.12, FW);
    } else if (g.pair) {
      const plan = pairPlan(g.pair, FLOOR - TOP - 1.00);
      const bh = K.card(s, LX, TOP, FW, null, g.body, C.blue, { fs:K.fitFs(g.body, FW - 0.40, FLOOR - TOP - plan.h - 0.24, DEFS, B) });
      pairDraw(s, TOP + bh + 0.12, plan);
    } else if (g.program) {
      const plan = programPlan(g.program, FLOOR - TOP - 1.00, g.fail ? 'fail' : null);
      const bh = K.card(s, LX, TOP, FW, null, g.body, C.blue, { fs:K.fitFs(g.body, FW - 0.40, FLOOR - TOP - plan.h - 0.24, DEFS, B) });
      programDraw(s, TOP + bh + 0.12, plan);
    } else {
      const cw = g.exW || 4.0, fs2 = K.fitCode(K.codeLines(rows(g.ex)), cw, CODES, FLOOR - TOP);
      K.codeCard(s, rows(g.ex), 9.55 - cw, TOP, cw, py, { fs:fs2 });
      const bw = 9.55 - cw - LX - 0.28;
      K.card(s, LX, TOP, bw, null, g.body, C.blue, { fs:K.fitFs(g.body, bw - 0.40, FLOOR - TOP - 0.38, DEFS, B) });
    }
    note(s, g.note); built++;

    g.leaves.forEach(lf => {
      s = K.light(); K.title(s, lf.t, lf.sub);
      const progName = lf.program || lf.fail || lf.warn;
      const stacked = !!(progName || lf.pair || lf.cmp || lf.quote || lf.struct || lf.transcript);
      const defW = stacked ? FW : LW;
      const wFs = 11;
      const watchH = lf.watch ? K.estH('Watch out — ' + lf.watch, defW - 0.52, wFs, B) + 0.26 : 0;
      const gaps = 0.12 * (stacked ? 2 : 1);
      const cap = FLOOR - TOP - watchH - gaps - 1.00;
      let extraH = 0, plan = null, pplan = null;
      if (progName) { plan = programPlan(progName, cap, lf.fail ? 'fail' : (lf.warn ? 'warn' : null)); extraH = plan.h; }
      else if (lf.pair) { pplan = pairPlan(lf.pair, cap); extraH = pplan.h; }
      else if (lf.cmp) extraH = cap;
      else if (lf.quote) extraH = 0.98;
      else if (lf.struct) extraH = Math.min(cap, 2.10);
      else if (lf.transcript && !lf.listing) extraH = Math.min(cap, 1.80);

      const defBudget = Math.max(0.58, FLOOR - TOP - watchH - extraH - gaps - 0.38);
      let y = TOP;
      y += K.card(s, LX, y, defW, null, lf.def, C.blue, { fs:K.fitFs(lf.def, defW - 0.40, defBudget, DEFS, B) }) + 0.12;
      if (!stacked) { const fs2 = K.fitCode(K.codeLines(rows(lf.ex)), RW, CODES, FLOOR - TOP); K.codeCard(s, rows(lf.ex), RX, TOP, RW, py, { fs:fs2 }); }
      if (plan)            y += programDraw(s, y, plan) + 0.12;
      else if (pplan)      y += pairDraw(s, y, pplan) + 0.12;
      else if (lf.cmp)     y += K.compare(s, y, FW, lf.cmp[0], lf.cmp[1], FLOOR - y) + 0.12;
      else if (lf.quote)   y += quoteBlock(s, y, FW, lf.quote[0], lf.quote[1]) + 0.12;
      else if (lf.struct)  y += structure(s, y, FW, extraH) + 0.12;
      else if (lf.transcript && !lf.listing) y += transcriptBlock(s, y, lf.transcript, extraH, FW) + 0.12;
      if (lf.watch) y += K.watchStrip(s, LX, y, defW, lf.watch, wFs);
      if (y > HT - 0.10) throw new Error('the slide for ' + lf.t + ' runs ' + (y - HT + 0.10).toFixed(2) + ' in past the page');
      note(s, lf.note); built++;
      if (lf.listing) {
        s = K.light(); K.title(s, lf.t + ': the complete listing', 'the program whose run is on the slide before this one');
        const lh = listing(s, TOP, lf.listing, lf.transcript ? 2.30 : FLOOR - TOP + 0.34);
        if (lf.transcript) transcriptBlock(s, TOP + lh + 0.12, lf.transcript, FLOOR - TOP - lh + 0.20, FW);
        note(s, 'This is the whole program, printed small on purpose: nobody reads a listing of this length from a projector, and the point of showing it is that every line the slide before discusses is here. Walk it with a pointer rather than reading it, naming the parts the class has already met - the imports, the variables set before the loop, the loop itself and the lines that decide when it ends. The same file is in the course repository, where it can be run.');
        built++;
      }
    });
  });
});

// ================================ back ================================
s = K.light(); K.title(s, 'What to take away', 'One sentence for each branch of the chapter');
[['I · Repetition', 'A while loop tests its condition at the start of every pass and stops the first time it is false; a for loop runs once for each item of an iterable and needs no counter of its own.'],
 ['II · What a loop walks through', 'A range is a lazy sequence with the start included and the end excluded; enumerate adds a count, zip pairs two sequences, and every for loop asks its iterable for an iterator.'],
 ['III · Loop control', 'break leaves the innermost loop, continue gives up one pass, return leaves the function and sys.exit the program - and only a loop that ran out runs its else clause.'],
 ['IV · Modules', 'import binds the module under its own name; the from form binds the names you list; the star form binds names you cannot see, and a file named after a module hides it.'],
 ['V · Modern practice', 'An assignment expression lets a loop read and test in one line. Do not change a collection while looping over it, and do not leave a finally block with a jump.']
].forEach(([h, t], i) => {
  const y = 1.26 + i * 0.80;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:LX, y, w:2.25, h:0.70, fill:{color:C.navy}, line:{color:C.navy}, rectRadius:0.07 });
  s.addText(h, { x:LX + 0.08, y, w:2.09, h:0.70, fontFace:H, fontSize:10.5, bold:true, color:C.white, valign:'middle', margin:0, isTextBox:true });
  s.addText(t, { x:2.82, y, w:6.73, h:0.70, fontFace:B, fontSize:11, color:C.ink, valign:'middle', margin:0, isTextBox:true });
});
note(s, 'Use this as a spoken summary rather than reading it: take each branch in turn and ask the class for the sentence before you reveal it. A branch that produces silence is the one to revisit at the start of the next session. Tell students these five sentences are the minimum they should be able to reproduce without notes, and that the interactive page for chapter 3 asks them the same things in question form.');
built++;

const WANT = ['Loop', 'Iteration', 'WhileStatement', 'InfiniteLoop', 'ForStatement', 'Accumulator', 'NestedLoop',
              'RangeStop', 'RangeStep', 'RangeDescending', 'LazyRange', 'HalfOpenRange', 'EnumerateFunction',
              'ZipStrict', 'IterableObject', 'IteratorObject', 'BreakStatement', 'ContinueStatement', 'ExitFunction',
              'LoopElseClause', 'LoopVariableScope', 'ImportStatement', 'StarImport', 'ModuleNameClash',
              'RandomModule', 'MutationWhileIterating'];
const QS = WANT.map(c => { const q = BANK.find(x => x.concept === c && !/this program/i.test(x.q)); return q ? [q.q, c] : null; }).filter(Boolean);
for (let k = 0; k < QS.length; k += 6) {
  s = K.light(); K.title(s, 'Questions', 'Predict the answer first, then settle it in the shell  ·  ' + (k / 6 + 1) + ' of ' + Math.ceil(QS.length / 6));
  QS.slice(k, k + 6).forEach(([q, tag], i) => {
    const y = 1.30 + i * 0.63;
    s.addShape(pres.shapes.OVAL, { x:LX, y:y + 0.05, w:0.44, h:0.44, fill:{color:C.yellow}, line:{color:C.yellow} });
    s.addText(String(k + i + 1), { x:LX, y:y + 0.05, w:0.44, h:0.44, fontFace:H, fontSize:14, bold:true, color:C.navy, align:'center', valign:'middle', margin:0, isTextBox:true });
    s.addText(q, { x:1.05, y, w:6.55, h:0.54, fontFace:B, fontSize:12, color:C.ink, valign:'middle', margin:0, isTextBox:true });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:7.75, y:y + 0.08, w:1.80, h:0.38, fill:{color:C.card}, line:{color:C.card}, rectRadius:0.06 });
    s.addText(tag, { x:7.78, y:y + 0.08, w:1.74, h:0.38, fontFace:B, fontSize:9, italic:true, color:C.mute, align:'center', valign:'middle', margin:0, isTextBox:true });
  });
  note(s, 'Every question on this slide is taken, word for word, from the chapter\'s own question bank in 08-tooling/ch03-page/question_bank_v1_1_0.json, which is also what the interactive page asks. Give the class a minute on each, take an answer from the room before you give one, and keep a shell open so that an answer can be settled by running it rather than by authority. The label on the right names the concept the question belongs to, so an unsure room tells you which slide to go back to.');
  built++;
}

s = K.light(); K.title(s, 'Sources', 'Every claim beyond the book comes from the chapter\'s research record');
const prim = SRC.sources.filter(r => r.role === 'primary'), sec = SRC.sources.filter(r => r.role !== 'primary');
K.card(s, LX, TOP, FW, 'Primary source', prim.map(r => r.label + ' — ' + r.url).join('\n'), C.blue, { fs:11.5, hf:14 });
const secLines = sec.map(r => '· ' + r.label.replace(/ \(Python 3\.\d+\.\d+ documentation[^)]*\)/, '').replace(/ \(Python documentation\)/, ''));
const half = Math.ceil(secLines.length / 2);
const srcFs = Math.min(K.fitFs(secLines.slice(0, half).join('\n'), 4.55, 2.38, [9.5, 9, 8.5, 8, 7.5, 7], B),
                       K.fitFs(secLines.slice(half).join('\n'), 4.45, 2.38, [9.5, 9, 8.5, 8, 7.5, 7], B));
s.addText(secLines.slice(0, half).join('\n'), { x:LX, y:2.26, w:4.55, h:2.40, fontFace:B, fontSize:srcFs, color:C.ink, margin:0, valign:'top', isTextBox:true });
s.addText(secLines.slice(half).join('\n'), { x:5.10, y:2.26, w:4.45, h:2.40, fontFace:B, fontSize:srcFs, color:C.ink, margin:0, valign:'top', isTextBox:true });
s.addText(sec.length + ' secondary sources, all recorded as verified in ' + SRC._research + '. The chapter\'s own author-year citations are ' + SRC.citations.join(', ') + '. Slides adapt Automate the Boring Stuff with Python (CC BY-NC-SA); see NOTICE_v1_2.md.',
          { x:LX, y:4.70, w:FW, h:0.68, fontFace:B, fontSize:9.5, italic:true, color:C.mute, margin:0, valign:'top', isTextBox:true });
note(s, 'Do not read this slide out. Say only that the chapter has one primary source, the book, and ' + sec.length + ' secondary sources, every one of which was fetched and recorded as verified in the chapter\'s research record before anything on these slides was written. Tell students where the record lives, because the point of showing it is that they can check a claim themselves, and invite them to do exactly that when something on a slide surprises them.');
built++;

s = K.dark();
s.addText('Next: Chapter 4 — Functions', { x:0.6, y:1.35, w:8.8, h:0.80, fontFace:H, fontSize:30, bold:true, color:C.white, margin:0, valign:'middle', isTextBox:true });
s.addText('Writing your own functions: parameters and arguments, return values, scope, and the exception handling this chapter only touched.',
          { x:0.6, y:2.25, w:8.8, h:0.70, fontFace:B, fontSize:16, color:C.yellow, margin:0, valign:'top', isTextBox:true });
s.addText('Before then: work through the interactive page for chapter 3, write the guessing game from memory, and find one loop in your own code that changes what it is looping over.',
          { x:0.6, y:3.25, w:8.8, h:0.80, fontFace:B, fontSize:14, color:'C9D4E0', margin:0, valign:'top', isTextBox:true });
s.addText('Questions?', { x:0.6, y:4.45, w:8.8, h:0.50, fontFace:H, fontSize:24, italic:true, color:'8FA3B8', margin:0, valign:'middle', isTextBox:true });
note(s, 'Close by naming the homework precisely: the interactive page for chapter 3, the guessing game written from memory, which is the smallest complete program that uses everything in the first branch, and one loop in their own code that changes the collection it is walking through. That last one is worth asking for, because the hazard the session ended on is the kind students only believe once they have found it in something they wrote themselves.');
built++;

pres.writeFile({ fileName: process.argv[2] }).then(f => console.log('written', f, '-', built, 'slides, deck version', VERSION));
