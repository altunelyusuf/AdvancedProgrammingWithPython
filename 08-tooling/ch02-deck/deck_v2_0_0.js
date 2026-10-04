// SEN0414 chapter 2 lecture deck, version 2.0.0.
//
// 2.0.0 replaces the 16-slide deck v1.0.x, which was written before the chapter corpus existed and covered about a
// dozen of the chapter's ideas. This version is built from sen0414_ch02_corpus_v1_0_0.py: it walks the corpus taxonomy
// in the taxonomy's own order - seven branches, thirteen groups, fifty-three leaf concepts - gives every concept its
// own slide, and shows the concept's worked example with the output that executing it produced. Because the structure
// and almost all of the text are new, this is a MAJOR bump.
//
// Nothing on a slide is typed from memory. Shell results and program transcripts come from examples_out_v1_1_0.json,
// written by running examples_v1_1_0.py under the course interpreter; the source list comes from
// sources_out_v1_0_0.json, read out of the chapter's RDODI research record; the questions come from the chapter's own
// question bank; the prose is compressed, for speaking, from the corpus paragraphs, and every claim the corpus takes
// from the textbook or the documentation keeps the corpus's own author-year citation.
//
// Usage: node deck_v2_0_0.js <out.pptx>
const VERSION = "2.0.0";
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const EX = JSON.parse(fs.readFileSync(__dirname + '/examples_out_v1_1_0.json'));
const SRC = JSON.parse(fs.readFileSync(__dirname + '/sources_out_v1_0_0.json'));
const OBJ = JSON.parse(fs.readFileSync(__dirname + '/../ch02-page/objectives_v1_0_1.json'));
const BANK = JSON.parse(fs.readFileSync(__dirname + '/../ch02-page/question_bank_v1_1_0.json'));
const CH = require(__dirname + '/deck_content_v1_0_0.js');
const PG = EX._programs, py = EX._python;

const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9';
pres.author = 'Yusuf Altunel'; pres.title = 'SEN0414 Chapter 2 - Flow Control';
pres.subject = 'Lecture deck built from the chapter 2 corpus and its executed examples';
const K = require(__dirname + '/deck_kit_v1_0_0.js')(pres);
const { C, H, B, M, HT, TOP, FLOOR, LX, LW, RX, RW, FW, DEFS, CODES } = K;
const note = (s, t) => s.addNotes(t);
const rows = key => EX[key].map(([c, r]) => [c, r]);
// the directory the build happened to run in is removed from a file name inside an error report; nothing else is
const errLine = l => l.replace(/File "[^"]*[\\/]/, 'File "');
let built = 0;

// ---------------- the pictures this chapter needs beyond code and prose ----------------
function flowchart(s, x, y, w, cap) {                          // the shape every if statement has, drawn to fit a column
  const sc = Math.min(1, (cap - 0.30) / 2.46);
  const cx = x + w / 2, bw = Math.min(1.4, w * 0.42), bh = 0.32 * sc;
  const box = (bx, by, ww, hh, t2, fill, fc, fsz) => { s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:bx, y:by, w:ww, h:hh, fill:{color:fill}, line:{color:fill}, rectRadius:0.10 });
    s.addText(t2, { x:bx+0.04, y:by, w:ww-0.08, h:hh, fontFace:B, fontSize:fsz, bold:true, color:fc, align:'center', valign:'middle', margin:0, isTextBox:true }); };
  const seg = (x1, y1, x2, y2) => s.addShape(pres.shapes.LINE, { x:Math.min(x1,x2), y:Math.min(y1,y2), w:Math.max(0.004, Math.abs(x2-x1)), h:Math.max(0.004, Math.abs(y2-y1)), line:{ color:C.blue, width:1.5 } });
  let yy = y;
  box(cx - bw/2, yy, bw, bh, 'Start', C.navy, C.white, 10); yy += bh;
  seg(cx, yy, cx, yy + 0.18 * sc); yy += 0.18 * sc;
  const dh = 0.76 * sc, dw = Math.min(w - 0.10, 3.10);
  s.addShape(pres.shapes.DIAMOND, { x:cx - dw/2, y:yy, w:dw, h:dh, fill:{color:C.yellow}, line:{color:C.yellow} });
  s.addText('is the condition true?', { x:cx - dw/2 + 0.34, y:yy, w:dw - 0.68, h:dh, fontFace:B, fontSize:9.5, bold:true, color:C.navy, align:'center', valign:'middle', margin:0, isTextBox:true });
  const dBot = yy + dh, bx = x + 0.04, blkW = w * 0.50, blkH = 0.34 * sc, blkY = dBot + 0.20 * sc;
  box(bx, blkY, blkW, blkH, 'run the block', C.card, C.ink, 9.5);
  seg(cx - dw/2, yy + dh/2, bx + blkW/2, yy + dh/2); seg(bx + blkW/2, yy + dh/2, bx + blkW/2, blkY);
  s.addText('true', { x:bx, y:yy + dh/2 - 0.22, w:0.52, h:0.20, fontFace:B, fontSize:8.5, italic:true, color:C.mute, margin:0, isTextBox:true });
  s.addText('false', { x:cx + 0.06, y:dBot + 0.02, w:0.60, h:0.20, fontFace:B, fontSize:8.5, italic:true, color:C.mute, margin:0, isTextBox:true });
  const endY = blkY + blkH + 0.26 * sc;
  seg(cx, dBot, cx, endY); seg(bx + blkW/2, blkY + blkH, bx + blkW/2, endY); seg(bx + blkW/2, endY, cx, endY);
  box(cx - bw/2, endY, bw, bh, 'End', C.navy, C.white, 10);
  s.addText('a diamond is a decision, a rectangle a step, a rounded rectangle the start or the end (Sweigart, 2025)',
            { x, y:endY + bh + 0.04, w, h:0.46, fontFace:B, fontSize:9, italic:true, color:C.mute, margin:0, valign:'top', isTextBox:true });
  return endY + bh + 0.52 - y;
}
function clausePicture(s, y, w, cap) {                         // the header and the suite it controls
  const sc = Math.min(1, (cap - 0.28) / 1.72);
  const hh = 0.42 * sc, sh = 0.64 * sc;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:LX, y, w, h:hh, fill:{color:C.yellow}, line:{color:C.yellow}, rectRadius:0.08 });
  s.addText([{ text:'if ', options:{ bold:true, color:'8B2E00' } }, { text:"name == 'Alice'", options:{ color:C.navy } }, { text:':', options:{ bold:true, color:'8B2E00' } }],
            { x:LX + 0.20, y, w:w - 0.40, h:hh, fontFace:M, fontSize:13, valign:'middle', margin:0, isTextBox:true });
  s.addText('the header: a keyword, a condition and a colon', { x:LX + 0.20, y:y + hh + 0.02, w:w - 0.40, h:0.20, fontFace:B, fontSize:9, italic:true, color:C.mute, margin:0, isTextBox:true });
  const sy = y + hh + 0.24;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:LX + 0.40, y:sy, w:w - 0.40, h:sh, fill:{color:C.code}, line:{color:C.code}, rectRadius:0.08 });
  s.addText([{ text:"print('Hi, Alice.')", options:{ color:C.codeTxt, breakLine:true } }, { text:"print('How are you?')", options:{ color:C.codeTxt } }],
            { x:LX + 0.62, y:sy + 0.05, w:w - 0.84, h:sh - 0.10, fontFace:M, fontSize:11, valign:'top', margin:0, isTextBox:true });
  s.addText('the suite: the indented block the header controls', { x:LX + 0.40, y:sy + sh + 0.02, w:w - 0.40, h:0.20, fontFace:B, fontSize:9, italic:true, color:C.mute, margin:0, isTextBox:true });
  K.caption(s, 'the book calls the block alone the clause; the reference calls the header and the block together a clause', LX, sy + sh + 0.24, w);
  return sy + sh + 0.48 - y;
}
function truthTables(s, y, w, cap) {                           // three tables, every cell produced by running it
  const val = k => Object.fromEntries(EX[k]);
  const a = val('andop'), o = val('orop'), n = val('notop');
  const rowH = Math.max(0.24, Math.min(0.36, (cap - 0.62) / 4));
  const tw = (w - 0.50) / 3;
  [['and', [['True and True', a['True and True']], ['True and False', a['True and False']], ['False and True', a['False and True']], ['False and False', a['False and False']]]],
   ['or',  [['False or True', o['False or True']], ['False or False', o['False or False']], ['(1 == 2) or (2 == 2)', o['(1 == 2) or (2 == 2)']]]],
   ['not', [['not True', n['not True']], ['not False', n['not False']], ["not 'foo'", n["not 'foo'"]], ["not ''", n["not ''"]]]]
  ].forEach(([name, cells], i) => {
    const x = LX + i * (tw + 0.25);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w:tw, h:0.30, fill:{color:C.blue}, line:{color:C.blue}, rectRadius:0.06 });
    s.addText('the ' + name + ' operator', { x, y, w:tw, h:0.30, fontFace:H, fontSize:11, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true });
    cells.forEach(([e, v], j) => {
      const ry = y + 0.34 + j * rowH;
      s.addShape(pres.shapes.RECTANGLE, { x, y:ry, w:tw, h:rowH - 0.02, fill:{color: j % 2 ? C.white : C.card }, line:{color:C.line} });
      s.addText(e, { x:x + 0.07, y:ry, w:tw - 0.86, h:rowH - 0.02, fontFace:M, fontSize:8.5, color:C.ink, valign:'middle', margin:0, isTextBox:true });
      s.addText(v, { x:x + tw - 0.82, y:ry, w:0.75, h:rowH - 0.02, fontFace:M, fontSize:10, bold:true, color: v === 'True' ? C.ok : C.red, align:'right', valign:'middle', margin:0, isTextBox:true });
    });
  });
  K.caption(s, 'every cell was produced by evaluating the expression beside it, under Python ' + py, LX, y + 0.36 + 4 * rowH, w);
  return 0.62 + 4 * rowH;
}
function programPlan(name, budget) {
  const p = PG[name], r = p.runs[0];
  const src = p.code.replace(/\n$/, '').split('\n');
  const out = r.lines.map(ln => ln.map(x => x[0]).join(''));
  const fs = Math.min(K.fitCode(src, 5.00, CODES, budget), K.fitCode(out, 3.90, CODES, budget));
  return { name, src, out, r, fs, h: Math.max(K.codeH(src, 5.00, fs), K.codeH(out, 3.90, fs)) };
}
function programDraw(s, y, plan, errAll) {
  const r = plan.r;
  const outLines = errAll ? r.errlines.map(errLine).map(l => [l, C.red])
    : r.lines.map(ln => [ln.map(x => x[0]).join(''), ln.length > 1 ? C.yellow : C.green])
             .concat(r.errlast ? [[errLine(r.errlast), C.red]] : []);
  const fs = Math.min(plan.fs, K.fitCode(outLines.map(l => l[0]), 3.90, CODES, plan.h));
  K.plainCode(s, plan.src.map(l => [l, l.trim().startsWith('#') ? '8B949E' : C.codeTxt]), LX, y, 5.00, { fs });
  K.plainCode(s, outLines, 5.65, y, 3.90, { fs, fill:C.deep });
  const h = Math.max(K.codeH(plan.src, 5.00, fs), K.codeH(outLines.map(l => l[0]), 3.90, fs)) - 0.26;
  K.caption(s, plan.name + ', run under Python ' + py + (r.errlast ? '; its error output in red' : (r.lines.some(l => l.length > 1) ? '; typed input in yellow' : '')), LX, y + h + 0.02, FW);
  return h + 0.26;
}
// the picture that belongs on the right of a two-column leaf slide
function rightColumn(s, lf, budget) {
  const L = K.codeLines(rows(lf.ex)), fs = K.fitCode(L, RW, CODES, budget);
  return K.codeCard(s, rows(lf.ex), RX, TOP, RW, py, { fs });
}

// ================================ the front of the deck ================================
let s = K.dark();
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:0.6, y:1.05, w:1.2, h:0.8, fill:{color:C.yellow}, line:{color:C.yellow}, rectRadius:0.12 });
s.addText('>>>', { x:0.6, y:1.05, w:1.2, h:0.8, fontFace:M, fontSize:30, bold:true, color:C.navy, align:'center', valign:'middle', margin:0, isTextBox:true });
s.addText('Chapter 2: Flow Control', { x:0.6, y:2.05, w:8.8, h:0.80, fontFace:H, fontSize:40, bold:true, color:C.white, margin:0, isTextBox:true });
s.addText('Booleans and truthiness, comparison and Boolean operators, if / elif / else, the match statement, and the errors they raise',
          { x:0.6, y:2.90, w:8.8, h:0.70, fontFace:B, fontSize:16, italic:true, color:C.yellow, margin:0, valign:'top', isTextBox:true });
s.addText('SEN0414 Advanced Programming · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University',
          { x:0.6, y:4.35, w:8.8, h:0.34, fontFace:B, fontSize:13, color:'C9D4E0', margin:0, isTextBox:true });
s.addText('Automate the Boring Stuff with Python, 3rd edition, chapter 2 (Sweigart, 2025), renewed for an advanced course',
          { x:0.6, y:4.72, w:8.8, h:0.34, fontFace:B, fontSize:11, italic:true, color:'8FA3B8', margin:0, isTextBox:true });
note(s, 'Open the session by saying what flow control is for: a program that ran every line in order, every time, could never react to its input. This is chapter 2 of Automate the Boring Stuff with Python, 3rd edition (Sweigart, 2025), rebuilt for an advanced course, so the book\'s own material is here in full and beside it are the parts of today\'s Python the book does not reach. Every result in this deck was produced by running the code under Python ' + py + ', and every claim beyond the book comes from the chapter\'s research record, so anything on a slide can be checked rather than taken on trust.');
built++;

s = K.light(); K.title(s, 'What this session covers', 'The chapter\'s four objectives, and where they sit in the course');
Object.keys(OBJ).filter(k => !k.startsWith('_')).forEach((k, i) => {
  const y = 1.30 + i * 0.66;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:LX, y, w:0.80, h:0.54, fill:{color:C.blue}, line:{color:C.blue}, rectRadius:0.07 });
  s.addText(k.replace('CO', 'CO-'), { x:LX, y, w:0.80, h:0.54, fontFace:H, fontSize:13, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true });
  s.addText(OBJ[k][0], { x:1.38, y, w:6.9, h:0.54, fontFace:B, fontSize:12.5, color:C.ink, valign:'middle', margin:0, isTextBox:true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:8.45, y:y + 0.09, w:1.10, h:0.36, fill:{color:C.card}, line:{color:C.card}, rectRadius:0.06 });
  s.addText(OBJ[k][1], { x:8.45, y:y + 0.09, w:1.10, h:0.36, fontFace:B, fontSize:11, italic:true, color:C.mute, align:'center', valign:'middle', margin:0, isTextBox:true });
});
const loText = OBJ._note + ' The chapter is nevertheless the groundwork every later outcome stands on: the decisions taught here appear in every program of the rest of the course.';
K.card(s, LX, 4.04, FW, 'Which course outcomes this chapter serves', loText, C.blue, { fs:K.fitFs(loText, 8.70, 0.62, [12.5, 12, 11.5, 11, 10.5, 10], B), hf:14 });
note(s, 'Read the four chapter objectives and say that the session is built to reach them in that order. Then be straight about the last card: the course\'s approved learning outcomes are advanced ones, and the chapter objectives for flow control are not claimed to serve any of them - that is what the chapter\'s own objectives file records, and inventing a link would be worse than admitting there is none. Say instead what is true: nothing later in the course can be written without these decisions.');
built++;

s = K.light();
const nG = CH.reduce((n, b) => n + b.groups.length, 0), nL = CH.reduce((n, b) => n + b.groups.reduce((m, g) => m + g.leaves.length, 0), 0);
K.title(s, 'The chapter as a map', CH.length + ' branches, ' + nG + ' groups, ' + nL + ' concepts — and the order we take them in');
CH.forEach((br, i) => {
  const x = 0.42 + i * 1.325;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y:1.30, w:1.22, h:0.78, fill:{color:C.navy}, line:{color:C.navy}, rectRadius:0.08 });
  s.addText(br.roman + '.  ' + br.label, { x:x + 0.04, y:1.30, w:1.14, h:0.78, fontFace:H, fontSize:9.5, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true });
  br.groups.forEach((g, j) => {
    const gy = 2.20 + j * 0.74;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y:gy, w:1.22, h:0.64, fill:{color:C.card}, line:{color:C.line}, rectRadius:0.06 });
    s.addText(g.label, { x:x + 0.05, y:gy, w:1.12, h:0.64, fontFace:B, fontSize:8.5, color:C.ink, align:'center', valign:'middle', margin:0, isTextBox:true });
    s.addText(String(g.leaves.length), { x:x + 0.94, y:gy + 0.03, w:0.24, h:0.18, fontFace:B, fontSize:7.5, bold:true, color:C.blue, align:'center', margin:0, isTextBox:true });
  });
});
s.addText('The small number on each group is how many concepts it holds. The order on this map is the order of the session.',
          { x:0.42, y:4.90, w:9.16, h:0.30, fontFace:B, fontSize:12, italic:true, color:C.mute, margin:0, isTextBox:true });
note(s, 'Leave this map up long enough for the class to copy it: it is the structure of the session and of the interactive page they will use afterwards. Say that the first four branches are the book\'s own chapter, roughly in its order, and that the last three are what an advanced course adds - the match statement and the style guide, the two worked programs read critically, and the error reports they will spend the term reading. Promise to show the map again at each branch.');
built++;

// ================================ the branches ================================
CH.forEach(br => {
  s = K.dark();
  s.addText(br.roman, { x:0.6, y:1.05, w:1.3, h:1.0, fontFace:H, fontSize:54, bold:true, color:C.yellow, margin:0, valign:'middle', isTextBox:true });
  s.addText(br.label, { x:1.95, y:1.15, w:7.5, h:0.80, fontFace:H, fontSize: br.label.length > 24 ? 26 : 32, bold:true, color:C.white, margin:0, valign:'middle', isTextBox:true });
  s.addText(br.blurb, { x:0.6, y:2.35, w:8.8, h:K.estH(br.blurb, 8.8, 15, B) + 0.10, fontFace:B, fontSize:15, color:'C9D4E0', margin:0, valign:'top', isTextBox:true });
  s.addText(br.groups.map(g => g.label).join('   ·   '), { x:0.6, y:4.52, w:8.8, h:0.44, fontFace:B, fontSize:12.5, italic:true, color:C.yellow, margin:0, valign:'middle', isTextBox:true });
  note(s, br.note); built++;

  br.groups.forEach(g => {
    // ---- group slide ----
    s = K.light(); K.title(s, g.label, g.sub);
    if (g.program) {
      const plan = programPlan(g.program, 1.95);
      const bh = K.card(s, LX, TOP, FW, null, g.body, C.blue, { fs:K.fitFs(g.body, FW - 0.40, FLOOR - TOP - plan.h - 0.24, DEFS, B) });
      programDraw(s, TOP + bh + 0.12, plan);
    } else if (g.cmp) {
      const bh = K.card(s, LX, TOP, FW, null, g.body, C.blue, { fs:K.fitFs(g.body, FW - 0.40, 1.70, DEFS, B) });
      K.compare(s, TOP + bh + 0.14, FW, [g.cmp[0][0], g.cmp[0][1]], [g.cmp[1][0], g.cmp[1][1]], FLOOR - TOP - bh - 0.20);
    } else {
      const cw = g.exW || 4.0, fs = K.fitCode(K.codeLines(rows(g.ex)), cw, CODES, FLOOR - TOP);
      K.codeCard(s, rows(g.ex), 9.55 - cw, TOP, cw, py, { fs });
      const bw = 9.55 - cw - LX - 0.28;
      K.card(s, LX, TOP, bw, null, g.body, C.blue, { fs:K.fitFs(g.body, bw - 0.40, FLOOR - TOP - 0.38, DEFS, B) });
    }
    note(s, g.note); built++;

    // ---- one slide per leaf concept ----
    g.leaves.forEach(lf => {
      s = K.light(); K.title(s, lf.t, lf.sub);
      const progName = lf.program || lf.fail || lf.trace;
      const stacked = !!(progName || lf.clause || lf.ttable || lf.cmp);
      const defW = stacked ? FW : LW;
      const wFs = 11;
      const watchH = lf.watch ? K.estH('Watch out — ' + lf.watch, defW - 0.52, wFs, B) + 0.26 : 0;
      const gaps = 0.12 * (stacked ? 2 : 1);
      // the picture is given whatever is left once the shortest acceptable definition and the warning have their room
      const cap = FLOOR - TOP - watchH - gaps - 1.00;
      let extraH = 0, plan = null;
      if (progName) { plan = programPlan(progName, cap); extraH = plan.h; }
      else if (lf.clause) extraH = Math.min(cap, 2.00);
      else if (lf.ttable) extraH = 0.62 + 4 * Math.max(0.24, Math.min(0.36, (cap - 0.62) / 4));
      else if (lf.cmp)    extraH = cap;

      const defBudget = Math.max(0.60, FLOOR - TOP - watchH - extraH - gaps - 0.38);
      let y = TOP;
      y += K.card(s, LX, y, defW, null, lf.def, C.blue, { fs:K.fitFs(lf.def, defW - 0.40, defBudget, DEFS, B) }) + 0.12;
      if (lf.flow) flowchart(s, RX, TOP, RW, FLOOR - TOP);
      else if (!stacked) rightColumn(s, lf, FLOOR - TOP);
      if (plan)           y += programDraw(s, y, plan, !!lf.trace) + 0.12;
      else if (lf.clause) y += clausePicture(s, y, FW, extraH) + 0.12;
      else if (lf.ttable) y += truthTables(s, y, FW, cap) + 0.12;
      else if (lf.cmp)    y += K.compare(s, y, FW, lf.cmp[0], lf.cmp[1], FLOOR - y) + 0.12;
      if (lf.watch) y += K.watchStrip(s, LX, y, defW, lf.watch, wFs);
      if (y > HT - 0.10) throw new Error('the slide for ' + lf.t + ' runs ' + (y - HT + 0.10).toFixed(2) + ' in past the page');
      note(s, lf.note); built++;
    });
  });
});

// ================================ the back of the deck ================================
s = K.light(); K.title(s, 'What to take away', 'One sentence for each branch of the chapter');
[['I · Values', 'A Boolean has exactly two members, and every other value can be asked whether it counts as true: None, zero and the empty collections are false, everything else is true.'],
 ['II · Comparisons', 'The equality operators compare values of any type; the identity operators ask whether two names mean one object, and that question is reserved for None.'],
 ['III · Boolean operations', 'not binds first, then and, then or. Evaluation stops as soon as the answer is known, and with values that are not Booleans the result is one of the operands.'],
 ['IV · Flow control', 'A condition, a colon and an indented block: that shape is the whole of if, elif and else, and the first true condition in a chain is the only one that runs.'],
 ['V · Modern practice', 'A match statement compares one value against patterns, which an elif chain can only do by repeating the value; PEP 8 asks for the plain test over a comparison with True.'],
 ['VI · Worked programs', 'A chain with no else clause may run nothing at all, and a variable assigned only inside its branches then does not exist when a later line asks for it.'],
 ['VII · Error reports', 'Read the last line first: it names the kind of error, which is more reliable than its wording, and the lines above it say where the program was.']
].forEach(([h, t], i) => {
  const y = 1.24 + i * 0.57;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:LX, y, w:2.05, h:0.50, fill:{color:C.navy}, line:{color:C.navy}, rectRadius:0.07 });
  s.addText(h, { x:LX + 0.07, y, w:1.91, h:0.50, fontFace:H, fontSize:10.5, bold:true, color:C.white, valign:'middle', margin:0, isTextBox:true });
  s.addText(t, { x:2.62, y, w:6.93, h:0.50, fontFace:B, fontSize:10.5, color:C.ink, valign:'middle', margin:0, isTextBox:true });
});
note(s, 'Use this slide as a spoken summary rather than reading it out: take each branch in turn and ask the class for the sentence before you reveal it. A branch that produces silence is the branch to revisit at the start of the next session. Tell students that these seven sentences are the minimum they should be able to reproduce without notes, and that the interactive page for chapter 2 asks them the same things in question form.');
built++;

// questions, drawn from the chapter's own question bank
const WANT = ['BooleanValue', 'Truthiness', 'NoneValue', 'Equality', 'EqualsVersusAssign', 'IdentityComparison',
              'Ordering', 'StringOrdering', 'AndOperator', 'OrOperator', 'ShortCircuit', 'OperandResult',
              'BooleanPrecedence', 'Indentation', 'IfStatement', 'ElifClause', 'BranchChain', 'ConditionalExpression',
              'MatchStatement', 'CasePattern', 'WildcardPattern', 'SingletonComparison', 'UnassignedName', 'TypeErrorKind'];
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
  note(s, 'Every question on this slide is taken, word for word, from the chapter\'s own question bank in 08-tooling/ch02-page/question_bank_v1_1_0.json, which is also what the interactive page asks. Give the class a minute on each, take an answer from the room before you give one, and keep a shell open so that an answer can be settled by running it rather than by authority. The label on the right names the concept the question belongs to, so an unsure room tells you which slide to go back to.');
  built++;
}

s = K.light(); K.title(s, 'Sources', 'Every claim beyond the book comes from the chapter\'s research record');
const prim = SRC.sources.filter(r => r.role === 'primary'), sec = SRC.sources.filter(r => r.role !== 'primary');
K.card(s, LX, TOP, FW, 'Primary source', prim.map(r => r.label + ' — ' + r.url).join('\n'), C.blue, { fs:11.5, hf:14 });
const secLines = sec.map(r => '· ' + r.label.replace(/ \(Python 3\.\d+\.\d+ documentation[^)]*\)/, '').replace(/ \(Python documentation\)/, ''));
const half = Math.ceil(secLines.length / 2);
s.addText(secLines.slice(0, half).join('\n'), { x:LX, y:2.26, w:4.55, h:2.40, fontFace:B, fontSize:9.5, color:C.ink, margin:0, valign:'top', isTextBox:true });
s.addText(secLines.slice(half).join('\n'), { x:5.10, y:2.26, w:4.45, h:2.40, fontFace:B, fontSize:9.5, color:C.ink, margin:0, valign:'top', isTextBox:true });
s.addText(sec.length + ' secondary sources, all recorded as verified in ' + SRC._research + '. The chapter\'s own author-year citations are ' + SRC.citations.join(', ') + '. Slides adapt Automate the Boring Stuff with Python (CC BY-NC-SA); see NOTICE_v1_2.md.',
          { x:LX, y:4.70, w:FW, h:0.68, fontFace:B, fontSize:9.5, italic:true, color:C.mute, margin:0, valign:'top', isTextBox:true });
note(s, 'Do not read this slide out. Say only that the chapter has one primary source, the book, and ' + sec.length + ' secondary sources, every one of which was fetched and recorded as verified in the chapter\'s research record before anything on these slides was written. Tell students where the record lives, because the point of showing it is that they can check a claim themselves, and invite them to do exactly that when something on a slide surprises them.');
built++;

s = K.dark();
s.addText('Next: Chapter 3 — Loops and modules', { x:0.6, y:1.35, w:8.8, h:0.80, fontFace:H, fontSize:30, bold:true, color:C.white, margin:0, valign:'middle', isTextBox:true });
s.addText('while and for, range, break and continue, the loop else clause, and the import statement that brings in the standard library.',
          { x:0.6, y:2.25, w:8.8, h:0.70, fontFace:B, fontSize:16, color:C.yellow, margin:0, valign:'top', isTextBox:true });
s.addText('Before then: work through the interactive page for chapter 2, write the three truth tables from memory, and bring one error report you could not read.',
          { x:0.6, y:3.25, w:8.8, h:0.70, fontFace:B, fontSize:14, color:'C9D4E0', margin:0, valign:'top', isTextBox:true });
s.addText('Questions?', { x:0.6, y:4.35, w:8.8, h:0.56, fontFace:H, fontSize:24, italic:true, color:'8FA3B8', margin:0, valign:'middle', isTextBox:true });
note(s, 'Close by naming the homework precisely: the interactive page for chapter 2, the three truth tables written from memory, which is the book\'s own practice question, and one error report they could not read. That last one is the most useful thing they can bring, because an error report nobody could read is the best possible opening for the chapter on loops, where the error messages get longer.');
built++;

pres.writeFile({ fileName: process.argv[2] }).then(f => console.log('written', f, '-', built, 'slides, deck version', VERSION));
