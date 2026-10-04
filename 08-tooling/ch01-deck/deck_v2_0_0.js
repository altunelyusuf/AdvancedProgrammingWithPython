// SEN0414 chapter 1 lecture deck, version 2.0.0.
//
// 2.0.0 replaces the 19-slide deck v1.0.x, which was written before the chapter corpus existed and covered fourteen
// of the chapter's ideas. This version is built from sen0414_ch01_corpus_v1_2_0.py: it walks the corpus taxonomy in
// the taxonomy's own order - five branches, sixteen groups, thirty leaf concepts - gives every concept its own slide,
// and shows the concept's worked example with the output that executing it produced. Because the deck's structure and
// almost all of its text are new, this is a MAJOR bump.
//
// Nothing on a slide is typed from memory. Code results come from examples_out_v1_1_0.json, written by running
// examples_v1_1_0.py under the course interpreter; the source list comes from sources_out_v1_0_0.json, read out of the
// chapter's RDODI research record; the prose is compressed, for speaking, from the corpus paragraphs; claims the
// corpus quotes from the textbook or the documentation carry the corpus's own author-year citation.
//
// Usage: node deck_v2_0_0.js <out.pptx>
const VERSION = "2.0.0";
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const EX = JSON.parse(fs.readFileSync(__dirname + '/examples_out_v1_1_0.json'));
const SRC = JSON.parse(fs.readFileSync(__dirname + '/sources_out_v1_0_0.json'));
const OBJ = JSON.parse(fs.readFileSync(__dirname + '/../ch01-page/objectives_v1_1_1.json'));
const PG = EX._programs, py = EX._python;

const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9';
pres.author = 'Yusuf Altunel'; pres.title = 'SEN0414 Chapter 1 - Python Basics';
pres.subject = 'Lecture deck built from the chapter 1 corpus and its executed examples';

// ---------- house style: the colours, faces and the ">>>" title motif of deck v1.0.1 ----------
const C = { navy:'1E2A3A', blue:'306998', yellow:'FFD43B', ink:'1F2933', mute:'5B6B7B', card:'F1F4F8',
            code:'17202B', codeTxt:'E6EDF3', green:'7EE787', red:'FF7B72', white:'FFFFFF', line:'D0D7DE', deep:'0F1823' };
const H = 'Cambria', B = 'Calibri', M = 'Courier New';
const W = 10, HT = 5.625;                       // the page, in inches
const PT = 72, LH = 1.22;                       // points per inch; line height as a multiple of the font size
const CW = { [M]:0.605, [B]:0.50, [H]:0.52 };   // average character width as a fraction of the font size,
                                                // each a little wider than layout_check_v1_0_0.py assumes, so that
                                                // this file always reserves at least as much room as the check demands
const TOP = 1.26, FLOOR = 5.10;                 // the band a content slide may use, in inches

function wrapLines(text, wIn, fs, face) {       // how many rendered lines this text takes in a box this wide
  const cpl = Math.max(1, Math.floor(wIn * PT / (CW[face] * fs)));
  let lines = 0;
  String(text).split('\n').forEach(l => { lines += Math.max(1, Math.ceil(l.length / cpl)); });
  return lines;
}
function estH(text, wIn, fs, face) { return wrapLines(text, wIn, fs, face) * fs * LH / PT; }
// the largest size from sizes at which this text still fits a box of this width and height
function fitFs(text, wIn, hIn, sizes, face) {
  for (const fs of sizes) if (estH(text, wIn, fs, face) <= hIn) return fs;
  return sizes[sizes.length - 1];
}
function chip(s, x, y, w, h, fsz) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill:{color:C.yellow}, line:{color:C.yellow}, rectRadius:0.08 });
  s.addText('>>>', { x, y, w, h, fontFace:M, fontSize:fsz, bold:true, color:C.navy, align:'center', valign:'middle', margin:0, isTextBox:true });
}
function light() { const s = pres.addSlide(); s.background = { color:C.white }; return s; }
function dark()  { const s = pres.addSlide(); s.background = { color:C.navy };  return s; }
function title(s, t, sub) {
  chip(s, 0.42, 0.34, 0.60, 0.42, 14);
  s.addText(t, { x:1.15, y:0.24, w:8.4, h:0.60, fontFace:H, fontSize: t.length > 46 ? 24 : 28, bold:true, color:C.navy, margin:0, valign:'middle', isTextBox:true });
  if (sub) s.addText(sub, { x:1.15, y:0.82, w:8.4, h:0.34, fontFace:B, fontSize:13, italic:true, color:C.mute, margin:0, valign:'middle', isTextBox:true });
}
function rule(s, y) { s.addShape(pres.shapes.RECTANGLE, { x:0.42, y, w:9.16, h:0.015, fill:{color:C.line}, line:{color:C.line} }); }
function note(s, t) { s.addNotes(t); }

// a soft card with a heading and a paragraph; its height is computed from the text, so nothing overflows
function card(s, x, y, w, head, body, accent, opts={}) {
  const fs = opts.fs || 13, hf = opts.hf || 15;
  const inner = w - 0.40;
  const h = opts.h || (0.18 + (head ? hf * LH / PT + 0.10 : 0) + estH(body, inner, fs, B) + 0.20);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill:{color:opts.fill || C.card}, line:{color:opts.fill || C.card}, rectRadius:0.10 });
  let ty = y + 0.14;
  if (head) { s.addText(head, { x:x+0.20, y:ty, w:inner, h:hf*LH/PT, fontFace:H, fontSize:hf, bold:true, color:accent || C.blue, margin:0, valign:'middle', isTextBox:true }); ty += hf*LH/PT + 0.08; }
  s.addText(body, { x:x+0.20, y:ty, w:inner, h:h - (ty - y) - 0.14, fontFace:B, fontSize:fs, color:opts.color || C.ink, margin:0, valign:'top', isTextBox:true });
  return h;
}
// the height card() will use for this text, computed before the card is drawn
function cardH(body, w, fs, head, hf) { return 0.18 + (head ? (hf || 15) * LH / PT + 0.10 : 0) + estH(body, w - 0.40, fs, B) + 0.20; }
// a dark card of shell lines. rows are [source, result] or [source, null] for a statement that shows nothing.
// The type size is chosen so that the longest line fits the card's width, so a long result can never run off the card.
function codeCard(s, rows, x, y, w, opts={}) {
  if (rows[rows.length-1][1] === null) throw new Error('a code card must end with a line that shows a value');
  const lines = []; rows.forEach(([c, r]) => { lines.push('>>> ' + c); if (r !== null) lines.push(r); });
  const inner = w - 0.44;
  const longest = Math.max(...lines.map(l => l.length));
  const fs = Math.min(opts.max || 15, Math.max(opts.min || 8, Math.floor(inner * PT / (CW[M] * longest))));
  // a line longer than the smallest type still fits wraps, so the height is counted from the wrapped lines
  const h = opts.h || (0.22 + lines.reduce((n, l) => n + wrapLines(l, inner, fs, M), 0) * fs * LH / PT);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill:{color:C.code}, line:{color:C.code}, rectRadius:0.10 });
  const runs = [];
  rows.forEach(([c, r], i) => {
    const last = i === rows.length - 1;
    runs.push({ text:'>>> ', options:{ color:C.yellow, bold:true } });
    runs.push({ text:c, options:{ color:C.codeTxt, breakLine: r !== null || !last } });
    if (r !== null) runs.push({ text:r, options:{ color: /^[A-Za-z]*Error:/.test(r) ? C.red : C.green, breakLine: !last } });
  });
  s.addText(runs, { x:x+0.22, y:y+0.11, w:inner, h:h-0.22, fontFace:M, fontSize:fs, valign:'top', margin:0, isTextBox:true });
  s.addText('run under Python ' + py, { x, y:y+h+0.02, w, h:0.22, fontFace:B, fontSize:9, italic:true, color:C.mute, align:'right', margin:0, isTextBox:true });
  return h + 0.26;
}
// a dark card of lines that are NOT shell input: a program, a terminal command, a transcript. Never prefixed with the
// shell prompt, so the deck check leaves it alone; whole programs are checked by program_check instead.
function plainCode(s, lines, x, y, w, opts={}) {
  const inner = w - 0.44;
  const longest = Math.max(...lines.map(l => (l[0] || '').length));
  let fs = Math.min(opts.max || 13, Math.max(opts.min || 7, Math.floor(inner * PT / (CW[M] * Math.max(longest, 1)))));
  if (opts.maxH) while (fs > 6 && 0.22 + lines.reduce((n, l) => n + wrapLines(l[0] || ' ', inner, fs, M), 0) * fs * LH / PT > opts.maxH) fs -= 0.5;
  const h = opts.h || (0.22 + lines.reduce((n, l) => n + wrapLines(l[0] || ' ', inner, fs, M), 0) * fs * LH / PT);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill:{color:opts.fill || C.code}, line:{color:opts.fill || C.code}, rectRadius:0.10 });
  s.addText(lines.map(([t, col], i) => ({ text:t || ' ', options:{ color: col || C.codeTxt, breakLine: i < lines.length-1 } })),
            { x:x+0.22, y:y+0.11, w:inner, h:h-0.22, fontFace:M, fontSize:fs, valign:'top', margin:0, isTextBox:true });
  return h;
}
function caption(s, t, x, y, w) { s.addText(t, { x, y, w, h:0.22, fontFace:B, fontSize:9, italic:true, color:C.mute, align:'right', margin:0, isTextBox:true }); }
// a small taxonomy picture: a root box with its children under it, joined by elbow connectors
function tree(s, x, y, w, root, kids, opts={}) {
  const rw = Math.min(3.0, w), rx = x + (w - rw) / 2, rh = 0.42;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:rx, y, w:rw, h:rh, fill:{color:C.navy}, line:{color:C.navy}, rectRadius:0.08 });
  s.addText(root, { x:rx, y, w:rw, h:rh, fontFace:H, fontSize:13, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true });
  const n = kids.length, gap = 0.12, kw = (w - gap * (n - 1)) / n, ky = y + rh + 0.34;
  const kh = opts.kh || 0.90;
  s.addShape(pres.shapes.RECTANGLE, { x:rx + rw/2 - 0.008, y:y + rh, w:0.016, h:0.17, fill:{color:C.blue}, line:{color:C.blue} });
  s.addShape(pres.shapes.RECTANGLE, { x:x + kw/2, y:y + rh + 0.16, w:w - kw, h:0.016, fill:{color:C.blue}, line:{color:C.blue} });
  kids.forEach(([lab, sub], i) => {
    const kx = x + i * (kw + gap);
    s.addShape(pres.shapes.RECTANGLE, { x:kx + kw/2 - 0.008, y:y + rh + 0.16, w:0.016, h:0.18, fill:{color:C.blue}, line:{color:C.blue} });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:kx, y:ky, w:kw, h:kh, fill:{color:C.card}, line:{color:C.blue}, rectRadius:0.06 });
    s.addText(lab, { x:kx+0.08, y:ky+0.07, w:kw-0.16, h:0.34, fontFace:H, fontSize:11.5, bold:true, color:C.blue, align:'center', valign:'middle', margin:0, isTextBox:true });
    if (sub) s.addText(sub, { x:kx+0.08, y:ky+0.40, w:kw-0.16, h:kh-0.46, fontFace:B, fontSize:9.5, color:C.ink, align:'center', valign:'top', margin:0, isTextBox:true });
  });
  return rh + 0.34 + kh;
}
function tableBox(s, head, rows, x, y, w, colW, opts={}) {
  const fs = opts.fs || 12;
  const t = [head.map(h2 => ({ text:h2, options:{ bold:true, color:C.white, fill:{color:C.blue} } }))];
  rows.forEach(r => t.push(r.map((cell, i) => (typeof cell === 'object') ? cell : { text:cell, options:(opts.mono||[]).includes(i) ? { fontFace:M } : {} })));
  s.addTable(t, { x, y, w, colW, fontFace:B, fontSize:fs, color:C.ink, border:{ type:'solid', pt:0.5, color:C.line }, rowH:opts.rowH || 0.30, valign:'middle' });
  return (rows.length + 1) * (opts.rowH || 0.30);
}

// ============================================================================================================
// THE CHAPTER, IN THE TAXONOMY'S OWN ORDER (sen0414_ch01_corpus_v1_2_0.py)
// Every leaf gives: t = its label, sub = the one line under the title, def = what it is, in words compressed for
// speaking from the corpus paragraphs, ex = the key of its executed session or a program, watch = the corpus's own
// "watch out", note = what to say while the slide is up.
// ============================================================================================================
const CH = [
{ id:'Value', label:'Values', roman:'I',
  blurb:'Everything a program handles is a value, and the kind of a value decides what can be done with it. The branch takes the two numeric kinds first, then text, and then the two ideas that explain them both: the data type and the expression.',
  note:'Open the branch by saying that nothing in Python happens except to values. Students arrive believing that a number and a number in quotation marks are the same thing; the whole branch exists to take that belief apart. Promise them that by the end of it they will be able to look at any line and say what kind of value it produces, which is the single most useful habit in the chapter.',
  groups:[
  { label:'Numeric values', sub:'Integers and floating-point numbers, and why the difference is not cosmetic',
    body:'Numeric values are the numbers a program calculates with, and chapter 1 meets two kinds of them. An integer is a whole number and is stored exactly, however large it grows. A floating-point number has a fractional part and is stored in binary with a fixed precision, so it can only approximate many decimal fractions (Python Software Foundation, 2026). When the two kinds meet in one expression the integer is converted to floating point, which is why 4 * 3.75 - 1 evaluates to 14.0, and division with the / operator always returns a float, so 6 / 3 is 2.0 and not 2.',
    ex:'intmix', exW:3.5,
    note:'Spend a moment on the two results on the right, because they are the cheapest way to show that the difference between the two numeric kinds is a fact about storage and not about how the number is written. Ask the class what 6 / 3 should give before you reveal it; most will say 2, and the surprise makes the rule memorable. Say plainly that the rule is not a defect: a division operator that sometimes returned an integer and sometimes a float would be far harder to reason about.',
    leaves:[
    { t:'Integer', sub:'A whole number, stored exactly, with no upper limit',
      def:'An integer is a whole number without a fractional part, such as 42, 0 or -7, and in Python it belongs to the type int - the same name the int function uses when it converts a value (Python Software Foundation, 2026). Integers count things: the items of a list, the passes of a loop, the characters that len reports. Python integers have unlimited precision, so a calculation never silently overflows the way a fixed-size integer does in many other languages; 2 ** 100 is computed exactly, to all thirty-one of its digits.',
      ex:'integer',
      watch:'An integer typed at the keyboard arrives as text. The call int(\'42\') gives the integer 42, but the string \'42\' itself cannot take part in arithmetic until it has been converted.',
      note:'Point at the thirty-one digit result and say that it is exact, not rounded and not an approximation: this is the headline property of Python integers and it is why Python is used for cryptography and for identifiers that must never wrap. Students who have met C or Java should be told explicitly that there is no 32-bit or 64-bit limit here. The mistake to warn against is the third line of the card: int(\'42\') is a conversion, and until it has happened the digits are text.' },
    { t:'Floating-point number', sub:'A number with a fractional part, stored in binary',
      def:'A floating-point number, or float, is a number with a fractional part, such as 3.14 or -0.5, and it belongs to the type float (Python Software Foundation, 2026). Floats appear whenever a literal contains a decimal point, whenever the / operator is used, whenever the float function converts a value, and whenever an integer and a float are mixed. Because they are stored in binary with a fixed precision, some decimal fractions have no exact representation, which is why the sum of 0.1 and 0.2 carries a tiny error and why round is needed to display it (Python Software Foundation, 2026).',
      ex:'float',
      watch:'Comparing two calculated floats for exact equality is risky for the same reason: 0.1 + 0.2 == 0.3 evaluates to False. Round for display, and compare with a tolerance when precision matters.',
      note:'This is the slide students remember for years, so do not rush it. Run the first line live if you can. Emphasise that Python is not being careless: it is showing the nearest value a binary float can hold, exactly. Connect it forward to money, where the right answer is to work in whole units or in a decimal type, and backwards to the closing section of the book chapter on how computers store data in binary. The error to expect in their code is an equality test on a calculated float that never becomes true.' }]},
  { label:'Text values', sub:'Strings, and the operators that work on them',
    body:'Text values are sequences of characters that a program reads, stores and prints, and chapter 1 treats text as a value like any other, governed by the same expression rules as numbers (Sweigart, 2025). In Python text is represented by the string type, written between quotation marks. The same operators that act on numbers act on strings with another meaning: + joins two strings and * repeats one, and the function len measures the result. Because strings carry everything a person types or reads, a program that cannot handle them cannot talk to its user.',
    ex:'string', exW:4.0,
    note:'Use the third line of the card as the hook for the whole group: the string \'7\' and the integer 7 look alike and behave differently, and Python refuses to guess which was meant. Say that this refusal is a design decision, not a limitation, and that the chapters on files and on the web will make students grateful for it. Ask what len(\'Hello, world!\') counts; someone will forget the comma, the space or the exclamation mark.',
    leaves:[
    { t:'String', sub:'A sequence of characters between quotation marks',
      def:'A string is a sequence of characters written between quotation marks, such as \'Alice\' or \'Hello, world!\'; Python names the type str, and either single or double quotation marks may enclose the text (Python Software Foundation, 2026). Strings are written as literals, returned by the input function, produced by the str function and built by formatted string literals, and they are what print finally shows. Strings are immutable, so an operation never alters a string in place: it builds a new one.',
      ex:'repl',
      watch:'A string that looks like a number is still text, and Python does not convert between the two silently (Sweigart, 2025). The count in a replication must be a whole number, so \'Alice\' * 2.5 is refused.',
      note:'Work down the card line by line and ask what each one will give before you show it. The fourth line is the teaching point: the error message names both types, which is how Python tells you what it would have needed. Mention immutability now even though nothing in this chapter depends on it, because the chapter on lists will contrast the two and students who heard the word early take the contrast more easily.' }]},
  { label:'The value model', sub:'The two ideas that explain every value: the data type and the expression',
    body:'The value model is the pair of ideas on which the rest of the chapter rests. Every value has a data type, and an expression is a piece of code that evaluates to a value. The two depend on each other, because the type of an expression\'s result is decided by the types of the values it combines. Without the idea of a type, Python\'s error messages are hard to read, since many of them report that a type did not fit an operation; without the idea of an expression, the shell, the function call and the formatted string look like three unrelated features instead of three places where the same rule applies.',
    ex:'expr', exW:3.4,
    note:'Tell the class that the two slides that follow are the pivot of the chapter: everything before them is examples, everything after them is consequences. The test you want students to be able to run in their heads is: what is the type of what this produces. Offer them the practical version of the same test in the shell, where the type function answers it out loud.',
    leaves:[
    { t:'Data type', sub:'The kind of a value, which decides what can be done with it',
      def:'A data type is the kind of a value, and it decides both what the value can do and what can be done with it; every Python object has one, and the type function reports it (Python Software Foundation, 2026). A value receives its type when it is created: the literal 42 makes an int and 3.14 makes a float. Python checks types when an operation runs rather than before the program starts, so a wrong combination is reported only when its line is reached, and the message names both types involved.',
      ex:'datatype',
      watch:'A variable has no type of its own; the value it refers to has one. Assigning a string to a name that held a number is allowed and simply changes what the name refers to.',
      note:'Show that the three answers are not words but classes: type(7) reports the class itself. Then make the connection students need: every TypeError they will ever see is this slide, reported at the moment of the operation. Mention the timing explicitly - the check happens when the line runs, which is why a mistake inside a branch that is never taken stays invisible until the data changes.' },
    { t:'Expression', sub:'A piece of code that evaluates to a value',
      def:'An expression is a piece of code that Python can evaluate to a value, built from literals, names, operators and function calls; 2 + 3 * 6 is an expression whose value is 20 (Python Software Foundation, 2026). Almost everything a program computes is an expression, and larger expressions are made by putting smaller ones inside them. Python evaluates the smallest parts first and replaces each with its value until one value remains: in 3 * (2 + 4) the parentheses give 6 and the multiplication then gives 18.',
      ex:'expr',
      watch:'An expression is not a statement. An assignment such as spam = 42 stores a value but is not itself an expression, so it produces nothing to print (Python Software Foundation, 2026).',
      note:'Reading an expression correctly means finding the order in which its parts are evaluated, so trace 3 * (2 + 4) aloud, replacing each part with its value as you go; that visible reduction is the skill the precedence slide will then formalise. Close with the expression-versus-statement distinction, because it is the reason the shell shows a value for one line and nothing at all for the next, which confuses nearly every beginner at least once.' }]}]},

{ id:'Operation', label:'Operations', roman:'II',
  blurb:'An operation combines values into a new value, and in Python most operations are written with an operator between their operands. The branch covers arithmetic on numbers, joining and repeating text, and the assignment that gives a value a name.',
  note:'Introduce the branch by saying that operations are what make a program do work: without them, values could only be stored and shown. The rules are fixed by the language, which means two readers who follow them reach the same answer whatever they expected (Python Software Foundation, 2026) - that is the promise this branch has to make good on, and precedence is where it is tested.',
  groups:[
  { label:'Arithmetic operations', sub:'Seven operators, and the order in which they apply',
    body:'Arithmetic operations calculate with numbers, and the chapter introduces seven operators for them: +, -, *, /, //, % and ** (Sweigart, 2025). Between them they cover addition, subtraction, multiplication, true division, whole-number division, the remainder and exponentiation, which is enough for most everyday calculation. Each takes two numbers and returns a number, and the result is a float whenever either operand is a float or the operator is /. When several appear in one expression they are applied in a documented order, which the next slides set out.',
    table:{ head:['Operator','Operation','Example','Evaluates to'], keys:[['**','exponent','2 ** 8'],['%','modulus, the remainder','23 % 7'],['//','integer (floor) division','23 // 7'],['/','true division','23 / 7'],['*','multiplication','3 * 5'],['-','subtraction','5 - 2']], from:'ops' },
    note:'Read the table from the top down and say that it is in precedence order, highest first, which is also the order the next slide draws as a ladder. Every value in the last column was produced by evaluating the expression beside it, so if a student doubts one, run it. The two rows worth pausing on are // and %, because they are the two most students have never met, and the row for / because its answer is a float.',
    leaves:[
    { t:'Operator', sub:'A symbol that performs an operation on its operands',
      def:'An operator is a symbol that tells Python to perform an operation on the values around it, which are called its operands: in 7 % 3 the symbol % is the operator and 7 and 3 are its operands (Python Software Foundation, 2026). Operators let a calculation be written in the notation of mathematics, so that a line such as price * count reads almost like the formula it implements. Most operators in this chapter are binary, taking one operand on each side, and the same symbol can mean different things for different types: 2 + 3 adds, while \'a\' + \'b\' joins.',
      ex:'operator',
      watch:'Treat / and // as different operators, not as two spellings of one: 7 / 2 gives 3.5 while 7 // 2 gives 3.',
      note:'The point to land is that the operands decide what the operator does, which is why the same plus sign adds numbers and joins text. That idea returns in every later chapter, and it is also the reason an error message has to name the types rather than just the operator. Finish with the last two lines of the card: students read / and // as the same thing far longer than you would expect.' },
    { t:'Operator precedence', sub:'Which operator is applied first when several appear',
      def:'Operator precedence is the rule that decides which operator is applied first when an expression contains several of them, and it is fixed by the language: ** binds first, then *, /, // and %, then + and - (Python Software Foundation, 2026). Precedence is what makes an expression mean exactly one thing; without it, 2 + 3 * 6 could be read as 30 or as 20 and two programmers could disagree about what a line computes. Parentheses override the order, and operators of equal precedence are applied from left to right.',
      ex:'prec', ladder:true,
      watch:'The power operator binds more tightly than a minus sign on its left, so -3 ** 2 evaluates to -9 while (-3) ** 2 evaluates to 9 (Python Software Foundation, 2026).',
      note:'Work the ladder from the top: parentheses first, then the exponent, then the multiplying group, then the adding group. Then show the card: the third and fourth lines are the pair that catches almost everyone, so ask for a prediction before revealing -9. The last line, 8 / 2 * 3, settles the left-to-right rule for equal precedence and also quietly shows that true division has made the result a float.' },
    { t:'Integer division and the remainder', sub:'Splitting one division into a quotient and a remainder',
      def:'Integer division splits a division into a whole-number quotient and a remainder. Floor division, written //, gives the quotient rounded down, and the modulus operator, written %, gives what is left over (Sweigart, 2025). Many problems ask exactly those two questions - how many whole groups fit, and what remains - when items are packed into boxes, seconds are converted to minutes or a total is split into equal parts. For 23 and 7 the quotient is 3 and the remainder is 2, because 3 times 7 plus 2 is 23.',
      ex:'intdiv', threeway:true,
      watch:'Floor division rounds down, not towards zero, so -7 // 2 evaluates to -4 because -3.5 rounded downward is -4 (Python Software Foundation, 2026).',
      note:'Use the three cards to show that one division answers three different questions, then write the check on the board: seven times three plus two is twenty-three. The negative case on the card is the one to dwell on, because every student expects -3; say the word downward rather than smaller and it usually lands. This pair of operators returns in the chapter on loops, where it is the usual way to ask whether a number is even.' }]},
  { label:'Text operations', sub:'The same two operator symbols, with a different meaning',
    body:'Text operations build new strings from existing ones, and two operators do it in this chapter: + joins strings, which the book calls string concatenation, and * repeats one, which it calls string replication (Sweigart, 2025). Joining and repeating are enough to assemble a sentence out of pieces or to draw a line of dashes under a title, and they make visible the general rule that one operator symbol can mean different things for different types. Both operations return a new string and leave the originals unchanged; + needs two strings, and * needs a string and a whole number.',
    ex:'concat', exW:4.4,
    note:'Say that this group is the first place where the type of the operands visibly changes what an operator does, and that the error on the third line of the card is the proof. Set up the next two slides by asking the class which they would rather write for a long message: a chain of plus signs, or something else. The answer they do not yet have is the f-string, at the end of the deck.',
    leaves:[
    { t:'Concatenation', sub:'Joining two strings with the + operator',
      def:'String concatenation joins two strings into one with the + operator, so that \'Alice\' + \'Bob\' gives \'AliceBob\' (Sweigart, 2025). Programs assemble messages out of pieces constantly - a greeting, a name, some punctuation - and concatenation is the plainest way to do it. Python builds a new string holding the characters of the left operand followed by those of the right one, and it adds nothing of its own: no space appears unless a space is part of one of the strings, which is why \'Hello\' + \'world\' gives \'Helloworld\'.',
      ex:'concat',
      watch:'Both operands must be strings. The expression \'Alice\' + 42 raises a TypeError, because Python does not convert types silently; convert the number with str, or use an f-string (Sweigart, 2025).',
      note:'The missing space in the second line is worth a few seconds, because students blame Python for it and the habit of checking their own spaces is cheap to build now. The error on the third line is the one they will meet most often this term: read the message out loud and show that it names both types, so the message itself tells you which conversion is missing. Give them both repairs, str(42) and the f-string, and say that the second is what the rest of the course will use.' },
    { t:'Replication', sub:'Repeating a string with the * operator',
      def:'String replication repeats a string a whole number of times with the * operator, so that \'Alice\' * 3 gives \'AliceAliceAlice\' (Sweigart, 2025). It builds repeated patterns without typing them out: a row of dashes under a title, a padding of spaces, a separator in printed output. The operands are a string and an integer, in either order, and the integer says how many copies to make. A count of zero or less produces the empty string, because a count below zero is treated as zero (Python Software Foundation, 2026).',
      ex:'repl',
      watch:'The count must be a whole number. The expression \'Alice\' * 2.5 raises a TypeError, and multiplying one string by another is not allowed either.',
      note:'The third line is the quiet one: a count of zero gives the empty string rather than an error, which matters because a width computed by a program can easily turn out to be zero. The last line gives you the chance to ask what half a copy of a word would even mean, which is exactly why Python refuses. If the room is quick, mention that the same two operators behave the same way on lists in a later chapter.' }]},
  { label:'Binding operations', sub:'Giving a value a name so that later lines can use it',
    body:'A binding operation gives a value a name, so that later lines can refer to it, and in Python the main one is the assignment statement (Sweigart, 2025). Without names, every value would have to be recomputed or retyped each time it was needed; binding lets a program keep a result, reuse it and describe it in words. The language reference puts the idea briefly: names refer to objects, and names are introduced by name binding operations (Python Software Foundation, 2026). The chapter\'s section on storing values in variables introduces it with the equals sign.',
    ex:'var', exW:3.4,
    note:'Read the card as a story in time: the name is created, used, re-bound, used again, and then a name that was never created is asked for and Python refuses. The last line is deliberate - it shows that names are case-sensitive and that an unknown name is an error rather than an empty value, which is different from several languages students may have met.',
    leaves:[
    { t:'Variable', sub:'A name that refers to a value',
      def:'A variable is a name that refers to a value stored in the computer\'s memory: after spam = 42 the name spam refers to the integer 42 and can be used wherever that value is needed (Sweigart, 2025). Variables let a program remember results, reuse them in later expressions and describe them with meaningful words, so that tax_rate is easier to read than a bare 0.125. Assigning the same name again makes it refer to a new value, and a name that was never assigned cannot be read: doing so raises a NameError.',
      ex:'var',
      watch:'Names are case-sensitive, cannot contain spaces and cannot begin with a digit. PEP 8 asks for lower-case words joined by underscores, as in my_age (Van Rossum et al., 2001).',
      note:'Make the naming rule a habit from the first week rather than a correction in the fourth: lower case, underscores, and a name that says what the value is. The last line of the card shows that Spam and spam are two different names, which is the most common cause of a NameError in beginners\' code after a plain typing mistake. Say that the error names the exact word Python could not find, so the message points straight at the fix.' },
    { t:'Assignment', sub:'Storing the value of an expression under a name',
      def:'An assignment statement stores a value in a variable with the equals sign: in spam = 42 the name on the left is bound to the value of the expression on the right (Sweigart, 2025). It is how a program keeps a result so that later expressions can use it, and it is the most common statement in the chapter\'s programs. Python evaluates the right-hand side first and only then binds the name, which is what makes spam = spam + 1 work: the old value is read, one is added, and the result is stored under the same name.',
      ex:'assign',
      watch:'The equals sign is not mathematical equality. It means store, not compare, and the assignment itself produces no value to print.',
      note:'Say the evaluation order out loud - right first, then the name - because that single sentence explains the line students find strangest, spam = spam + 1. If anyone objects that it is false as an equation, agree: it is not an equation. Chapter 2 introduces the comparison operator that does ask whether two values are equal, so promise it now rather than leaving the ambiguity open.' }]}]},

{ id:'BuiltInFunction', label:'Built-in functions', roman:'III',
  blurb:'A built-in function is one Python provides ready to use, with nothing to import. The chapter\'s first program uses six of them - print, input, len, str, int and float - and the branch takes them in four groups: calling, input and output, conversion, and measurement.',
  note:'Say that built-in functions are a program\'s first abilities: to show something, to ask for something, to measure something and to change a value from one type to another. Every one of them is used by calling it, and the call is an expression, so its result can be stored, printed or put inside a larger expression. That single sentence is what makes the whole branch hang together.',
  groups:[
  { label:'Calling a function', sub:'Asking Python to run a function now, with given values',
    body:'Calling a function means asking Python to run it now, with given values. The call is written as the function\'s name followed by parentheses, and the values inside the parentheses are its arguments (Python Software Foundation, 2026). Calling is how a program reuses work that has already been written, whether Python wrote it or the student did, instead of repeating the steps each time. Because a call is an expression, it has a value and can appear anywhere a value can: on the right of an assignment, inside another call, or inside the braces of a formatted string.',
    ex:'call', exW:4.4,
    note:'The last line of the card is there to show that a function is itself a value: writing the name without parentheses does not call it, it merely names it. That is the cause of a silent bug students meet when they write print without the parentheses and nothing appears. Make the distinction once here and point back to it whenever it recurs.',
    leaves:[
    { t:'Function call', sub:'Running a function and using the value it returns',
      def:'A function call runs a function with the values given inside parentheses, called its arguments, and the call evaluates to the function\'s return value: in round(3.14159, 2) the name round is the function, 3.14159 and 2 are the arguments, and the value is 3.14 (Python Software Foundation, 2026). Python evaluates the arguments first and then runs the function with them. A function returns a value to the place where it was called, and if its code ends without returning anything the value is None - which is why print is used for what it does and not for what it gives back.',
      ex:'call',
      watch:'The parentheses are required. Writing print without them does not call the function, it only names it, and a program that does this displays nothing.',
      note:'Name the parts out loud on the first line - function, arguments, return value - because students who can read a call can read most lines of a beginner\'s program. The second line is a free reminder that round and int do different things to 4.7. Mention that print returns None, which the corpus records as an executed check, so a line such as spam = print(\'hi\') leaves None in spam rather than the text.' }]},
  { label:'Input and output', sub:'The two directions of every conversation with a user',
    body:'Input and output functions connect a program to its user: print sends text out, and input reads text in (Sweigart, 2025). A program that can neither show a result nor ask a question cannot be used by anyone, so these two are the first functions any program needs. Both work with text. The print function turns its arguments into strings and writes them, and input returns whatever the user typed as a string, which means that a number read from the keyboard has to be converted before it can take part in arithmetic.',
    program:'print_v1_0_0.py',
    note:'Run the program and read the four lines of output against the four lines of source. The second line is the one that teaches: sep and end are ordinary keyword arguments with defaults, so the space between the arguments and the newline at the end are choices and not laws. The empty third line proves what end normally does. Keep this slide in reserve when students later ask why their output is on one line or on too many.',
    leaves:[
    { t:'print', sub:'Writing values to the screen as text',
      def:'The print function writes its arguments to the screen as text: the call print(\'Hello, world!\') displays Hello, world! and then moves to a new line (Python Software Foundation, 2026). Output is how a program reports what it has done; without it a program run from a file would compute in silence. All the arguments are converted to strings as str would convert them and written one after another, separated by a space and followed by a newline, because the keyword arguments sep and end default to a space and a newline (Python Software Foundation, 2026).',
      program:'print_v1_0_0.py',
      watch:'In the interactive shell a bare expression is displayed automatically, but in a saved program only print produces output: an expression on a line of its own is evaluated and its value is thrown away.',
      note:'The gap between the shell and a saved file is a real source of confusion in the first weeks: a student tries a line in the shell, sees a value, copies the line into a file and sees nothing. Say explicitly that the shell is printing on their behalf and that a file will not. Then show the second line of the program again and tell them that sep and end are how they control spacing without building the string themselves.' },
    { t:'input', sub:'Reading a line from the keyboard, always as text',
      def:'The input function waits for the user to type a line and returns it; if it is given a prompt, it writes that text first, without a trailing newline (Python Software Foundation, 2026). Input is what lets one program serve many people: the same code can greet any name or calculate with any age the user supplies. It reads a line from the keyboard, strips the trailing newline and returns the rest as a string, so that whatever the user types - even 20 - arrives as text.',
      program:'firstprogram_v1_1_0.py',
      watch:'Because the result is always a string, adding 1 to it fails, and int(input()) is the usual way to read a whole number. Typing something that is not a whole number then raises a ValueError.',
      note:'Point at the transcript and say that the 20 beside the prompt is text at the moment it arrives, and that only the int call on the next line of the source turns it into a number. Then ask what happens if the user types twenty instead; the answer is the ValueError in the watch-out line, and this is the first time the class meets a program that can be broken by its own user. Chapter 2 and the chapter on debugging both return to it.' }]},
  { label:'Conversion functions', sub:'Moving a value from one type to another',
    body:'Conversion functions change a value from one data type to another, and the chapter uses three of them: str, int and float (Python Software Foundation, 2026). Values arrive and leave as text, yet arithmetic needs numbers and messages need strings, so conversion is the bridge between the two. Each function takes a value and returns a new one of its own type, leaving the original untouched: int(\'42\') returns the integer 42, float(\'3.5\') returns the float 3.5, and str(29) returns the string \'29\'.',
    ex:'conv', exW:4.6,
    note:'Say that this group is the practical answer to every TypeError in the chapter. Walk down the card and stop at int(4.7): converting a float with int discards the fraction, which is not the same as rounding, and round is the function that rounds. The last line is the error students will hit the first time they let a user type a price, and the message is specific enough to point at the cause.',
    leaves:[
    { t:'Type conversion', sub:'str, int and float, and what each one refuses',
      def:'Type conversion produces a value of another type from an existing one: int(\'42\') gives the integer 42, float(\'3.5\') gives the float 3.5 and str(29) gives the string \'29\' (Python Software Foundation, 2026). Without conversion, text from the keyboard could not be used in arithmetic and numbers could not be joined into a message. A conversion function reads the value it is given and builds a new one; it never changes the original. The int function refuses text that is not a whole number, so int(\'4.2\') raises a ValueError, whereas int(4.7) is 4, because converting a float discards its fraction.',
      ex:'conv',
      watch:'Converting the float 4.7 with int does not round it: round(4.7) is 5 while int(4.7) is 4. Use the function that matches the intention.',
      note:'Draw the difference between int(\'4.2\') and int(4.7) on the board as two different questions: the first asks Python to read text that is not a whole number, and it refuses; the second asks it to drop a fraction it already has, and it obliges. Students who confuse the two write a conversion where they meant a rounding and lose money or marks by one unit. Finish by saying that the ValueError message quotes the offending text back, which is the fastest clue they will get.' }]},
  { label:'Measurement functions', sub:'Asking a value about itself without changing it',
    body:'A measurement function reports a property of a value without altering it, and the first one the chapter uses is len (Sweigart, 2025). Knowing the size of a value is the starting point of many decisions: whether a password is long enough, whether a name fits a label, whether a collection has anything in it at all. The function takes one argument and returns a whole number, the number of items in it; for a string the items are its characters. The same function is used on lists, dictionaries and other collections in later chapters, which is why it is worth meeting properly now.',
    ex:'length', exW:4.6,
    note:'Ask for a prediction on len(\'a b\') before you show it; the space is an item like any other and students routinely forget it. The last line is the useful failure: len has nothing to count in a number, so it refuses, and the standard repair is to turn the number into text first. That repair, len(str(n)), is a small but genuinely useful idiom for counting digits.',
    leaves:[
    { t:'len', sub:'Counting the items in a value',
      def:'The len function returns the number of items in an object; for a string this is the number of characters, so len(\'hello\') is 5 (Python Software Foundation, 2026). Counting characters answers practical questions - whether a name is empty, whether a text is too long for a field - and the result is an ordinary integer, so it can be used in arithmetic or joined into a message after conversion with str. The function counts every character, including spaces and punctuation, which is why len(\'a b\') is 3.',
      ex:'length',
      watch:'The function counts the characters of a string, not the digits of a number: len(12345) raises a TypeError, while len(str(12345)) is 5.',
      note:'Say that len is the first function students meet that asks a value about itself rather than changing it, and that this read-only quality is why it is safe to use anywhere. Then use the last two lines to make a general point about Python\'s error messages: object of type \'int\' has no len() tells you both the type and the missing ability, which is enough to find the repair without searching.' }]}]},

{ id:'ExecutionEnvironment', label:'The execution environment', roman:'IV',
  blurb:'Where code runs matters as much as what it says. This branch is the part of the chapter that the textbook does not have: the shell students type into, the interpreter and its CPython implementation, the builds that decide how threads can run, and the release and proposal system that governs how Python changes.',
  note:'Introduce this branch honestly: it is not in the third edition. It is here because the Python students run in 2026 is newer than the one the book describes, and because an advanced course has to be able to say what the interpreter is before it can talk about threads, packaging or performance. Tell them that everything on these slides was read in the current documentation and that the chapter research record names every page.',
  groups:[
  { label:'The interactive environment', sub:'Type an expression, see its value at once',
    body:'An interactive environment lets a learner type Python and see the result immediately, and the chapter starts there, with expressions entered into the interactive shell and evaluated as soon as they are entered (Sweigart, 2025). Immediate feedback shortens the cycle of trying an idea and finding out whether it works, which is why interpreted languages typically have a shorter development and debugging cycle than compiled ones (Python Software Foundation, 2026). The environment reads a line, evaluates it, prints the result and waits for the next: a read-eval-print loop, or REPL.',
    ex:'shell', exW:3.4,
    note:'This is where the course actually begins for a student sitting at a machine. Encourage them to keep a shell open beside every lecture and to test the claim on the slide rather than believe it. Name the acronym REPL once and explain each letter, because it appears in tool documentation constantly and nobody explains it there.',
    leaves:[
    { t:'The interactive shell', sub:'The read-eval-print loop, replaced in Python 3.13',
      def:'The interactive shell is the program in which statements and expressions are typed at a prompt and their results appear at once; it is also called the interactive interpreter or the REPL, an acronym for read-eval-print loop (Python Software Foundation, 2026). It is the quickest place to test an idea or explore a module, and it removes the need to save and run a file for a one-line experiment. In interactive mode the interpreter prompts with three greater-than signs for a new command and with three dots for a continuation line, and it keeps the value of the last expression in the variable named with a single underscore.',
      ex:'shell',
      changed:'Python 3.13 replaced the shell with a new interactive interpreter: multi-line editing with history, colour in prompts and tracebacks by default, and the commands help, exit and quit usable without parentheses (Python Software Foundation, 2026).',
      watch:'A learner who cannot leave the shell can type quit(); the end-of-file key, Control-D on Unix or Control-Z on Windows, also works at the primary prompt (Python Software Foundation, 2026).',
      note:'Demonstrate this one live rather than describing it, and point out the colour in the prompt and in a traceback, because that colour is itself evidence that they are not running the interpreter the book was written against. The underscore variable is a genuinely useful trick for a lecture: compute something, then continue from it without retyping. End with the escape route, since being trapped in a shell is a real first-week problem.' }]},
  { label:'The Python implementation', sub:'The language, the program that runs it, and the bytecode in between',
    body:'Python is a language, and a Python implementation is a program that reads code written in that language and carries it out: the language defines what a program means, the implementation decides how the computer does it. Separating the two explains why the same code can run on more than one program, and why features such as the global interpreter lock or the interactive shell belong to an implementation rather than to the language itself. The implementation students use is CPython, which compiles source to bytecode and then executes that bytecode on a virtual machine.',
    ex:'cpython', exW:4.8,
    note:'Make the distinction concrete with the two lines on the card: the running program reports its own name. Say that from here on, when the course says Python without qualification it means CPython, and that this is also the convention the documentation uses. The payoff comes two slides later, when the global interpreter lock turns out to be a property of this implementation and not of the language.',
    leaves:[
    { t:'The Python interpreter', sub:'The program that reads your code and runs it',
      def:'The Python interpreter is the program that reads Python code and runs it. Python is an interpreted rather than a compiled language, which means source files can be run directly without explicitly creating an executable first (Python Software Foundation, 2026). Running source directly gives a shorter development and debugging cycle than a compiled language, although the programs generally run more slowly. Started with no arguments the interpreter opens the interactive shell; given a file name it runs that script; given -c it runs the statements on the command line.',
      term:['$ python3.14', '$ python3.14 script.py', '$ python3.14 -c "print(2 + 2)"', '$ python3.14 --version'],
      watch:'A computer can hold several interpreters. The commands python, python3 and versioned names such as python3.14 may point to different versions, so check which one is running before blaming the code.',
      note:'Show the three ways of starting it and say which one they will use for homework. Then tell them the truth the glossary itself admits: interpreted is a simplification, because the source is compiled to bytecode first, and the distinction can be blurry for that reason. The practical warning is the last one - on a shared or old machine, python and python3 are routinely different versions, and the first thing to do when an example misbehaves is to ask the interpreter its version.' },
    { t:'CPython', sub:'The implementation the course means when it says Python',
      def:'CPython is the canonical implementation of the Python programming language, as distributed on python.org, and the name is used when it is necessary to distinguish this implementation from others such as Jython or IronPython (Python Software Foundation, 2026). Unless it says otherwise, this course means CPython when it says Python: CPython is the reference interpreter for which the core developers write the language\'s design documents (Warsaw et al., 2000). It compiles source code to bytecode and executes that bytecode on a virtual machine, and it can be built in more than one way.',
      ex:'cpython',
      watch:'Bytecode is specific to CPython and to its version: bytecodes are not expected to work between different Python virtual machines, nor to be stable between releases (Python Software Foundation, 2026).',
      note:'The name matters because it is the handle for everything that follows: the global interpreter lock, the bytecode and the free-threaded build are all described in the documentation as properties of CPython, never of Python. Say that out loud, because students who miss it come away believing that Python the language cannot use more than one core, which is not what the sources say.' },
    { t:'Bytecode', sub:'The internal form your source is compiled into',
      def:'Bytecode is the internal representation of a Python program inside the CPython interpreter: source code is compiled into bytecode, which runs on a virtual machine that executes the machine code corresponding to each instruction (Python Software Foundation, 2026). Compiling once into a compact internal form lets CPython run the same program repeatedly without reading the source text again, and the bytecode is cached in .pyc files, so running the same file is faster the second time. The dis module can display it, which is the quickest way to see what the compiler really made of a line.',
      program:'bytecode_v1_0_0.py',
      watch:'Bytecode is an implementation detail. The instruction names change between Python releases, so a program should never depend on them (Python Software Foundation, 2026).',
      note:'This is a short detour, but it pays for itself: the listing shows the two names being loaded, the multiplication carried out and only then the addition, which is precedence made visible as instructions rather than asserted as a rule. Tell the class that they will never need to read bytecode in this course, and that seeing it once removes the mystery from the word compiled when it is applied to Python.' }]},
  { label:'The interpreter build', sub:'Threads, the global interpreter lock, and the build without it',
    body:'An interpreter build is one particular way of compiling CPython from its source. The default build and the free-threaded build behave alike for most programs but differ in how threads can use the processor (Python Software Foundation, 2026). The build decides how a program can use the machine, which is why a course on advanced Python has to explain threads and the global interpreter lock before it can teach multithreading. A build is chosen when CPython is compiled, and a running program can be asked which one it is.',
    ex:'gil', exW:5.6,
    note:'Say why this group is in a chapter 1 lecture at all: course outcome LO-4 is about designing concurrent programs with threads, and that outcome cannot be reached without the vocabulary on these three slides. The two lines on the card are the honest answer for the machine in front of them: this interpreter still has the lock. Promise the full treatment later in the term and keep it.',
    leaves:[
    { t:'Thread', sub:'A separate flow of execution inside one program',
      def:'A thread is a separate flow of execution inside one program, so that several activities can be in progress at once; in the threading module the Thread class represents an activity run in a separate thread of control (Python Software Foundation, 2026). Threads let a program keep working while one activity waits - for a file, for an answer over a network - and on a machine with several cores they can in principle run at the same moment. All the threads of a program share the same memory, because the threading module operates within a single process. A thread is started with its start method, and another thread waits for it with join.',
      program:'thread_v1_0_0.py',
      watch:'Because threads share memory, two threads that change the same value can disturb each other. Built-in types in the free-threaded build use internal locks, yet the documentation still recommends threading.Lock or another synchronisation primitive (Python Software Foundation, 2026).',
      note:'Read the program as three moves: create the thread with the work it is to do, start it, and wait for it. The output proves that the main thread really did wait, which is what join means. Say that sharing memory is both why threads are cheap and why they are dangerous, and that the danger - two threads changing one value - is the subject of the later multithreading lecture, not of this one.' },
    { t:'The global interpreter lock', sub:'Why one thread at a time runs Python bytecode',
      def:'The global interpreter lock, or GIL, is the mechanism the CPython interpreter uses to ensure that only one thread executes Python bytecode at a time (Python Software Foundation, 2026). The lock simplifies the implementation by making the object model, including critical built-in types such as dict, implicitly safe against concurrent access; the price is that much of the parallelism offered by multi-processor machines is lost. A thread must hold the lock to run bytecode and the others wait their turn, although the lock is always released during input and output, and some extension modules release it during heavy work.',
      ex:'gil',
      watch:'The lock is a mechanism of the CPython interpreter, not a rule of the language, and the default build of CPython still has it. PEP 703 calls it an obstacle to using multi-core CPUs from Python efficiently (Gross, 2023).',
      note:'Give both halves of the trade, because students who hear only the second half conclude that threads are useless in Python. The lock buys safety and simplicity; it costs parallel computation. Then give the practical rule: for work that waits - files, networks - the lock is released and threads help; for work that computes, they do not, in the default build. The card shows that the build in front of them is the default one.' },
    { t:'The free-threaded build', sub:'CPython compiled without the lock, supported since 3.14',
      def:'A free-threaded build is a build of CPython that supports free threading, a model in which several threads can run Python bytecode simultaneously within the same interpreter; it is configured with the --disable-gil option before compilation (Python Software Foundation, 2026). Free-threaded execution allows full use of the available processing power by running threads in parallel on the available cores, although not all software benefits automatically. PEP 703 proposed making the lock optional and PEP 779 set the criteria for supported status: phase I made the build available but experimental, phase II makes it officially supported but still optional, and phase III would make it the default (Wouters et al., 2025).',
      phases:true,
      watch:'Some third-party packages with an extension module may not be ready for a free-threaded build, and importing such a module can switch the lock back on with a warning (Python Software Foundation, 2026).',
      note:'This is the newest thing in the deck, so date it precisely: the build became available in 3.13 and officially supported in 3.14, which is the release the course uses. Walk the three phases and say which one we are in. Be careful not to oversell it - the watch-out line is real, and a student who installs the free-threaded build and then cannot install a package they need will not thank you.' }]},
  { label:'Python releases', sub:'Versions, the schedule they follow, and the proposals behind them',
    body:'A Python release is a published version of the language and its interpreter, identified by a version number, together with the proposals and the schedule that led up to it. Features, error messages and even the interactive shell change between releases, so a learner needs to know which release is in use and which releases are still supported. Each release follows a documented schedule: a first release date, a period of bug fixes, a period of security fixes only, and an end-of-life date (Python Software Foundation, 2026). Changes to the language are proposed in Python Enhancement Proposals.',
    ex:'version', exW:5.2,
    note:'Ask the room which Python they have installed; the answers will differ, and that is the point of the group. Show the two lines on the card as the way to find out from inside a program. Then say that the course pins its examples to one interpreter and records which one, so that a result on a slide can be reproduced rather than trusted.',
    leaves:[
    { t:'Python version', sub:'The number that identifies a release',
      def:'A Python version is the number that identifies a release, such as 3.14.4; Python reports it with the --version option, and a program can read it from sys.version_info, whose fields include major, minor and micro. The version decides which features a program can use: Python 3.13 introduced the new interactive interpreter and Python 3.14 made free-threaded Python officially supported, so a program written for a newer version may fail on an older one (Python Software Foundation, 2026). A new version is released each October, bug fixes follow, and security fixes continue until the end of life, five years after the first release.',
      ex:'version',
      watch:'The course uses 3.14, but the chapter\'s examples were run under both Python 3.12.3 and Python 3.14.4 and printed identical output, so an older installed version does not change the results shown here.',
      note:'The watch-out line is the one that matters to students with an older machine, so read it out: nothing in this chapter depends on the newest release. Then point at the version the card reports, which is the interpreter that produced every result in this deck, and explain why a teaching deck should say so: a result nobody can reproduce is a claim, not a demonstration.' },
    { t:'Python Enhancement Proposal', sub:'How Python changes, and where to read why',
      def:'A Python Enhancement Proposal, or PEP, is a design document that provides information to the Python community or describes a new feature for Python or its processes or environment (Warsaw et al., 2000). PEPs are the primary mechanism for proposing major new features, for collecting community input on an issue and for documenting the design decisions that have gone into Python, so they explain not only what Python does but why. The author of a PEP is responsible for building consensus and for documenting dissenting opinions, and the proposals are kept as text files in a versioned repository, so their revision history is the historical record.',
      peps:true,
      watch:'A PEP records a proposal and its status, not a promise. When the reference implementation is complete and merged, the status becomes Final, and the Steering Council has the final authority over approval (Warsaw et al., 2000).',
      note:'Tell students that a PEP is the best written explanation they will find of almost any Python design decision, and that reading one is a reasonable thing to do rather than an expert activity. The four on the slide are the ones this chapter has already leaned on. If anyone asks why a feature they liked in another language is missing, the honest answer is usually that there is a PEP explaining the decision.' }]}]},

{ id:'ModernPractice', label:'Modern practice', roman:'V',
  blurb:'Modern practice is the way Python programmers work today: the idioms experienced developers prefer, and the tools they use to install, run and organise code. Pairing each basic with its current counterpart avoids unlearning later.',
  note:'Explain the reason for this branch in one sentence: a student who learns only the basics writes code that works but looks dated, and a student who has never installed a package cannot use the libraries that make Python useful - which is course outcome LO-1. The branch has two halves, one about how a string is built and one about how a project is set up.',
  groups:[
  { label:'String formatting', sub:'Building a string out of text and values in one step',
    body:'String formatting builds a string out of text and values in one step. Building strings by concatenation works, but a formatted string literal lets a program write an expression between braces inside the string, and the tutorial notes that the older str.format method requires more manual effort (Python Software Foundation, 2026). Concatenation requires converting every number with str and keeping track of spaces, which is easy to get wrong; a format places each value where it belongs in the sentence and does the conversion itself. Python 3.12 gave f-strings a formal grammar (Galindo Salgado et al., 2022).',
    program:'concat_vs_fstring_v1_0_0.py',
    note:'Show the two lines of the program side by side and point out that they print exactly the same text. Then count what the first line costs: two plus signs, an explicit str call and two spaces that have to be remembered. Ask which of the two the class would rather read in six months. That is the whole argument, and it does not need to be longer.',
    leaves:[
    { t:'f-string', sub:'An expression inside the string, evaluated as the string is built',
      def:'An f-string, short for formatted string literal, is a string literal prefixed with f or F whose braces hold expressions; Python evaluates each expression and inserts its value into the text, so f\'{2 ** 8}\' gives \'256\' (Python Software Foundation, 2026). It states in one place both the sentence the user will read and the values that fill it: shorter than concatenation, needing no str calls, and keeping spaces and punctuation visible. Any expression is allowed inside the braces, and after a colon a format specification can be given, so that f\'{1 / 3:.2f}\' gives \'0.33\' (Galindo Salgado et al., 2022).',
      ex:'fstr',
      watch:'The prefix f is required. Without it the braces are ordinary characters, as the last line of the card shows, and the program prints the braces instead of the value.',
      note:'The last line of the card is the error they will make: the same string without the prefix prints its own braces, and because it is not an error Python says nothing. Tell them to read any string with braces and check for the f. The format specification after the colon is worth a sentence, because fixing a price or a percentage to two decimal places is something they will want in the first project.' }]},
  { label:'Tooling', sub:'Packages, environments, and the manager that handles both',
    body:'Tooling is the set of programs a Python developer uses around the language itself: to install interpreters and packages, to keep projects apart and to run code. Working with these tools is part of programming as much as writing code is, and much of Python\'s usefulness comes from packages written by others, so a learner who cannot install and isolate them is limited to the standard library. The three slides that follow explain what a package is, how a virtual environment keeps projects separate, and how a package manager automates both.',
    ex:'package', exW:4.4,
    note:'Connect this group to course outcome LO-1, which is about selecting and applying libraries: nothing in that outcome is reachable without the three ideas here. The card shows what an import actually produces - a module object, bound to a name - which is the smallest honest answer to the question of what importing does. The chapter on loops will go much further.',
    leaves:[
    { t:'Package', sub:'A module that can contain other modules',
      def:'A package is a Python module that can contain submodules or, recursively, subpackages; a module is an object that serves as an organisational unit of Python code and is loaded into a program by importing it (Python Software Foundation, 2026). Packages are how code is shared: the standard library is the collection of packages and modules distributed with the interpreter, and third-party packages add everything else a project may need. Applications often use packages outside the standard library, and they sometimes need a specific version of a library, for example because a particular bug has been fixed in it.',
      ex:'package',
      watch:'One Python installation cannot satisfy every application. If one program needs version 1.0 of a library and another needs version 2.0, installing either leaves the other unable to run - the problem a virtual environment solves (Python Software Foundation, 2026).',
      note:'Keep this short and factual, because the next two slides are the ones that solve the problem. The watch-out line is the entire motivation for virtual environments, so state it as a scenario rather than a rule: two of their own projects, one library, two incompatible versions. Everyone has met the equivalent outside programming and the analogy lands quickly.' },
    { t:'Virtual environment', sub:'A self-contained Python and set of packages, per project',
      def:'A virtual environment is a self-contained directory tree containing a Python installation for a particular version of Python plus a number of additional packages (Python Software Foundation, 2026). Different applications can use different environments, so conflicting requirements stop mattering: one project keeps version 1.0 of a library while another uses version 2.0, and upgrading one does not affect the other. The venv module creates and manages them, and a common place for one is a directory named .venv inside the project folder.',
      term:['$ python3.14 -m venv .venv', '$ source .venv/bin/activate', '$ python -m pip install <package>', '$ deactivate'],
      watch:'A virtual environment belongs to one project. The packages installed into it are not visible to other environments, and deleting its directory removes them.',
      note:'Run these four commands in front of the class if the room allows it, because the idea is obvious once seen and abstract until then. Point out that the environment is just a directory: nothing is registered anywhere, and deleting the folder undoes everything, which makes experimenting safe. Then say that the next slide replaces all four commands with a tool that does them for you.' },
    { t:'Package manager', sub:'uv: one tool for interpreters, environments and dependencies',
      def:'A package manager installs, upgrades and removes packages and keeps track of the versions a project needs. The tool uv is a package and project manager for Python written in Rust, whose documentation promises a single tool to replace pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv and more (Astral, 2026). It installs and manages Python versions, creates virtual environments, runs scripts and records a project\'s dependencies in a lockfile, and it works on macOS, Linux and Windows. It was the most admired technology in the 2025 Stack Overflow Developer Survey, at 74 per cent (Stack Overflow, 2025).',
      term:['$ uv init my-project', '$ uv add requests', '$ uv run main.py', '$ uv python install 3.14'],
      watch:'The tool presents itself as a replacement for pip and virtualenv, so a learner will meet those names in older documentation and should know that they do the same jobs separately.',
      note:'Say that uv installed the Python 3.14.4 that produced every result in this deck, which is the most honest endorsement available. Each command creates the environment it needs, so the four lines on the slide are the whole workflow for a small project. Be fair to the older tools: pip and virtualenv are not wrong, they are several tools where this is one, and students will see both in the wild.' }]}]}
];

const QUESTIONS = [
 ['What is the value of 2 + 3 * 6, and which rule decides it?', 'Operator precedence'],
 ['Why does 0.1 + 0.2 not print 0.3?', 'Floating-point numbers'],
 ['What type of value does input() return when the user types 42?', 'Input and conversion'],
 ['What happens when Python evaluates \'Alice\' + 42, and what are the two repairs?', 'Concatenation'],
 ['What is the difference between int(4.7) and round(4.7)?', 'Type conversion'],
 ['23 // 7 is 3 and 23 % 7 is 2. What single sentence about 23 and 7 do the two together state?', 'Integer division'],
 ['Why is -3 ** 2 equal to -9 rather than 9?', 'Operator precedence'],
 ['What does len(12345) do, and what is the usual repair?', 'Measurement'],
 ['Which implementation of Python does this course mean when it says Python, and how can a running program say so itself?', 'CPython'],
 ['What does the global interpreter lock prevent, and is it a property of the language or of the implementation?', 'The interpreter build'],
 ['Rewrite \'Hello, \' + name + \'! You are \' + str(age) + \'.\' as a formatted string literal.', 'f-strings'],
 ['Two of your projects need different versions of the same library. What solves this, and why?', 'Virtual environments']
];

// ============================================================================================================
// building the deck
// ============================================================================================================
let built = 0;
function rows(key) { return EX[key].map(([c, r]) => [c, r]); }

// --- 1. title ---
let s = dark();
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:0.6, y:1.05, w:1.2, h:0.8, fill:{color:C.yellow}, line:{color:C.yellow}, rectRadius:0.12 });
s.addText('>>>', { x:0.6, y:1.05, w:1.2, h:0.8, fontFace:M, fontSize:30, bold:true, color:C.navy, align:'center', valign:'middle', margin:0, isTextBox:true });
s.addText('Chapter 1: Python Basics', { x:0.6, y:2.05, w:8.8, h:0.80, fontFace:H, fontSize:40, bold:true, color:C.white, margin:0, isTextBox:true });
s.addText('Values, operations, built-in functions, the interpreter you actually run, and the practice of 2026',
          { x:0.6, y:2.90, w:8.8, h:0.64, fontFace:B, fontSize:17, italic:true, color:C.yellow, margin:0, valign:'top', isTextBox:true });
s.addText('SEN0414 Advanced Programming · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University',
          { x:0.6, y:4.35, w:8.8, h:0.34, fontFace:B, fontSize:13, color:'C9D4E0', margin:0, isTextBox:true });
s.addText('Automate the Boring Stuff with Python, 3rd edition, chapter 1 (Sweigart, 2025), renewed for an advanced course',
          { x:0.6, y:4.72, w:8.8, h:0.34, fontFace:B, fontSize:11, italic:true, color:'8FA3B8', margin:0, isTextBox:true });
note(s, 'Welcome the class and set the frame for the session. This is chapter 1 of Automate the Boring Stuff with Python, 3rd edition (Sweigart, 2025), rebuilt for an advanced course: the book\'s own material is here in full, and beside it are the parts of today\'s Python that the book does not reach. Say at the start that every result shown in this deck was produced by running the code under Python ' + py + ', installed with uv, and that every claim beyond the book comes from the chapter\'s research record, so anything on a slide can be checked rather than taken on trust.');
built++;

// --- 2. what the chapter covers, and which outcomes it serves ---
s = light(); title(s, 'What this session covers', 'The chapter\'s four objectives, and the course outcomes they serve');
const objKeys = Object.keys(OBJ).filter(k => !k.startsWith('_'));
objKeys.forEach((k, i) => {
  const y = 1.32 + i * 0.66;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:0.45, y, w:0.80, h:0.52, fill:{color:C.blue}, line:{color:C.blue}, rectRadius:0.07 });
  s.addText(k.replace('CO', 'CO-'), { x:0.45, y, w:0.80, h:0.52, fontFace:H, fontSize:13, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true });
  s.addText(OBJ[k][0], { x:1.38, y, w:6.9, h:0.52, fontFace:B, fontSize:13.5, color:C.ink, valign:'middle', margin:0, isTextBox:true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:8.45, y:y+0.08, w:1.10, h:0.36, fill:{color:C.card}, line:{color:C.card}, rectRadius:0.06 });
  s.addText(OBJ[k][1], { x:8.45, y:y+0.08, w:1.10, h:0.36, fontFace:B, fontSize:11, italic:true, color:C.mute, align:'center', valign:'middle', margin:0, isTextBox:true });
});
const loText = 'Chapter 1 serves ' + OBJ._serves.map(x => x.replace('LO', 'LO-')).join(' and ') +
  '. LO-1, on selecting and applying libraries, is begun by the tooling slides at the end of this session; LO-4, on designing concurrent programs with threads, is prepared by the slides on threads, the interpreter lock and the free-threaded build.';
card(s, 0.45, 4.08, 9.10, 'Course outcomes this chapter serves', loText, C.blue, { fs:fitFs(loText, 8.70, 0.58, [12.5, 12, 11.5, 11, 10.5, 10], B) });
note(s, 'Read the four objectives aloud and tell the class that the session is built to reach them in order: precedence first, then the numeric types, then conversion and its errors, and formatted strings at the end. Name the two course outcomes explicitly, because students are entitled to know why a basics chapter appears in an advanced course. The honest answer is on the slide: the tooling at the end is the first step of the libraries outcome, and the interpreter slides are the vocabulary the multithreading outcome will need later in the term.');
built++;

// --- 3. the chapter as a taxonomy ---
const nG = CH.reduce((n, b) => n + b.groups.length, 0), nL = CH.reduce((n, b) => n + b.groups.reduce((m, g) => m + g.leaves.length, 0), 0);
s = light(); title(s, 'The chapter as a map', CH.length + ' branches, ' + nG + ' groups, ' + nL + ' concepts \u2014 and the order we take them in');
CH.forEach((br, i) => {
  const x = 0.42 + i * 1.86;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y:1.30, w:1.70, h:0.62, fill:{color:C.navy}, line:{color:C.navy}, rectRadius:0.08 });
  s.addText(br.roman + '.  ' + br.label, { x:x+0.06, y:1.30, w:1.58, h:0.62, fontFace:H, fontSize:12, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true });
  br.groups.forEach((g, j) => {
    const gy = 2.06 + j * 0.60;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y:gy, w:1.70, h:0.50, fill:{color:C.card}, line:{color:C.line}, rectRadius:0.06 });
    s.addText(g.label, { x:x+0.06, y:gy, w:1.58, h:0.50, fontFace:B, fontSize:10, color:C.ink, align:'center', valign:'middle', margin:0, isTextBox:true });
    s.addText(String(g.leaves.length), { x:x+1.40, y:gy+0.03, w:0.26, h:0.20, fontFace:B, fontSize:8, bold:true, color:C.blue, align:'center', margin:0, isTextBox:true });
  });
});
s.addText('The small number on each group is how many concepts it holds. The order on this map is the order of the session.',
          { x:0.42, y:4.92, w:9.16, h:0.30, fontFace:B, fontSize:12, italic:true, color:C.mute, margin:0, isTextBox:true });
note(s, 'Leave this map up for a minute and let the class copy it, because it is the structure of the whole session and of the interactive page they will use afterwards. Say that the first three branches are the book\'s own chapter 1, more or less in its order, and that the last two are what an advanced course adds: where the code runs, and how people actually work today. Promise that you will show this map again at each branch so nobody loses their place.');
built++;

// --- the branches ---
const LX = 0.45, LW = 5.27, RX = 5.86, RW = 3.69, FW = 9.10;   // the two columns, and the full width
const DEFS = [13, 12.5, 12, 11.5, 11, 10.5, 10, 9.5, 9];        // the sizes a prose card may shrink through
const CODES = [14, 13, 12, 11, 10, 9, 8];                       // and the sizes a code card may shrink through

// ---- measuring a code card before it is drawn, so that a slide can be planned rather than hoped for ----
function codeLines(rs) { const L = []; rs.forEach(([c, r]) => { L.push('>>> ' + c); if (r !== null) L.push(r); }); return L; }
function plainLines(ls) { return ls.map(l => (typeof l === 'string' ? l : l[0]) || ' '); }
function fitCode(lines, w, sizes, budget) {     // the largest size at which these lines fit the width and the height
  const inner = w - 0.44;
  for (const fs of sizes) {
    const h = 0.22 + lines.reduce((n, l) => n + wrapLines(l, inner, fs, M), 0) * fs * LH / PT;
    if (lines.every(l => l.length <= Math.floor(inner * PT / (CW[M] * fs))) && h + 0.26 <= budget) return fs;
  }
  return sizes[sizes.length - 1];
}
function codeH(lines, w, fs) {
  const inner = w - 0.44;
  return 0.22 + lines.reduce((n, l) => n + wrapLines(l, inner, fs, M), 0) * fs * LH / PT + 0.26;   // including its caption
}
// a compact "watch out" strip: the label is on the same line as the sentence, which saves a slide a third of an inch
function watchStrip(s, x, y, w, text, fs) {
  const h = estH('Watch out — ' + text, w - 0.52, fs, B) + 0.26;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill:{color:'FFF1F0'}, line:{color:'FFD7D5'}, rectRadius:0.08 });
  s.addShape(pres.shapes.RECTANGLE, { x, y, w:0.07, h, fill:{color:C.red}, line:{color:C.red} });
  s.addText([{ text:'Watch out — ', options:{ bold:true, color:'A4342C' } }, { text, options:{ color:C.ink } }],
            { x:x + 0.22, y:y + 0.12, w:w - 0.44, h:h - 0.24, fontFace:B, fontSize:fs, margin:0, valign:'top', isTextBox:true });
  return h;
}
// the precedence ladder
function ladder(s, x, y, w) {
  ['( )   parentheses first', '**   exponent', '*   /   //   %', '+   -'].forEach((t, i) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:x + i * 0.18, y:y + i * 0.38, w:w - i * 0.18, h:0.32, fill:{color: i === 0 ? C.yellow : C.card}, line:{color: i === 0 ? C.yellow : C.line}, rectRadius:0.06 });
    s.addText(t, { x:x + 0.12 + i * 0.18, y:y + i * 0.38, w:w - 0.24 - i * 0.18, h:0.32, fontFace:M, fontSize:11, bold:true, color:C.navy, valign:'middle', margin:0, isTextBox:true });
  });
  caption(s, 'highest at the top; equal precedence runs left to right', x, y + 1.48, w);
  return 1.74;
}
// the three answers to 23 divided by 7
function threeway(s, y) {
  const r2 = Object.fromEntries(EX.intdiv);
  [['23 / 7', r2['23 / 7'], 'true division: always a float'], ['23 // 7', r2['23 // 7'], 'floor division: the whole part'], ['23 % 7', r2['23 % 7'], 'modulus: the remainder']]
    .forEach(([e, v, l], i) => {
      const x = LX + i * 3.08;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w:2.90, h:1.14, fill:{color:C.card}, line:{color:C.card}, rectRadius:0.10 });
      s.addText(e, { x, y:y + 0.06, w:2.90, h:0.30, fontFace:M, fontSize:15, bold:true, color:C.blue, align:'center', margin:0, isTextBox:true });
      s.addText(v, { x:x + 0.08, y:y + 0.37, w:2.74, h:0.42, fontFace:M, fontSize: v.length > 8 ? 12 : 22, bold:true, color:C.navy, align:'center', valign:'middle', margin:0, isTextBox:true });
      s.addText(l, { x:x + 0.10, y:y + 0.79, w:2.70, h:0.28, fontFace:B, fontSize:10.5, color:C.ink, align:'center', margin:0, isTextBox:true });
    });
  caption(s, '3 × 7 + 2 = 23 — the quotient and the remainder together say everything about this division', LX, y + 1.16, FW);
  return 1.42;
}
// a program beside the transcript of a real run of it
function programPlan(name, budget) {
  const p = PG[name], r = p.runs[0];
  const src = p.code.replace(/\n$/, '').split('\n');
  const out = r.lines.map(ln => ln.map(x => x[0]).join(''));
  const fs = Math.min(fitCode(src, 5.00, CODES, budget), fitCode(out, 3.90, CODES, budget));
  return { src, out, r, fs, h: Math.max(codeH(src, 5.00, fs), codeH(out, 3.90, fs)) };
}
function programDraw(s, name, y, plan) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:LX, y, w:5.00, h:plan.h - 0.26, fill:{color:C.code}, line:{color:C.code}, rectRadius:0.10 });
  s.addText(plan.src.map((l, i) => ({ text:l || ' ', options:{ color: l.trim().startsWith('#') ? '8B949E' : C.codeTxt, breakLine: i < plan.src.length - 1 } })),
            { x:LX + 0.22, y:y + 0.11, w:4.56, h:plan.h - 0.48, fontFace:M, fontSize:plan.fs, valign:'top', margin:0, isTextBox:true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:5.65, y, w:3.90, h:plan.h - 0.26, fill:{color:C.deep}, line:{color:C.deep}, rectRadius:0.10 });
  s.addText(plan.r.lines.map((ln, i) => ({ text:ln.map(x => x[0]).join('') || ' ', options:{ color: ln.length > 1 ? C.yellow : C.green, breakLine: i < plan.r.lines.length - 1 } })),
            { x:5.87, y:y + 0.11, w:3.46, h:plan.h - 0.48, fontFace:M, fontSize:plan.fs, valign:'top', margin:0, isTextBox:true });
  caption(s, name + ', run under Python ' + py + (plan.r.lines.some(l => l.length > 1) ? '; typed input in yellow' : ''), LX, y + plan.h - 0.24, FW);
  return plan.h;
}
// the picture, table or code that belongs on the right of a two-column leaf slide
function rightColumn(s, lf, x, y, w, budget) {
  if (lf.ex) { const L = codeLines(rows(lf.ex)); const fs = fitCode(L, w, CODES, budget); codeCard(s, rows(lf.ex), x, y, w, { fs }); return codeH(L, w, fs); }
  if (lf.term) { const fs = fitCode(lf.term, w, CODES, budget);
                 const h = plainCode(s, lf.term.map(l => [l, C.green]), x, y, w, { fs, fill:C.deep });
                 caption(s, 'commands typed in a terminal, not in the shell', x, y + h + 0.02, w); return h + 0.26; }
  if (lf.peps)   return tableBox(s, ['PEP', 'What it settled'],
                   [['8', 'the style guide for Python code'], ['20', 'the Zen of Python'], ['701', 'a formal grammar for f-strings'],
                    ['703', 'making the interpreter lock optional'], ['779', 'criteria for supporting free threading']],
                   x, y, w, [0.72, w - 0.72], { fs:11, rowH:0.32 }) + 0.06;
  if (lf.phases) {
    ['Phase I · available, but experimental (3.13)', 'Phase II · officially supported, still optional (3.14)', 'Phase III · would make it the default'].forEach((t, i) => {
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y:y + i * 0.62, w, h:0.52, fill:{color: i === 1 ? C.yellow : C.card}, line:{color: i === 1 ? C.yellow : C.line}, rectRadius:0.07 });
      s.addText(t, { x:x + 0.10, y:y + i * 0.62, w:w - 0.20, h:0.52, fontFace:B, fontSize:11, bold:i === 1, color:C.navy, valign:'middle', margin:0, isTextBox:true });
    });
    caption(s, 'the three phases PEP 779 defines (Wouters et al., 2025)', x, y + 1.88, w);
    return 2.14;
  }
  return 0;
}

CH.forEach(br => {
  // ---- branch divider ----
  s = dark();
  s.addText(br.roman, { x:0.6, y:1.05, w:1.3, h:1.0, fontFace:H, fontSize:54, bold:true, color:C.yellow, margin:0, valign:'middle', isTextBox:true });
  s.addText(br.label, { x:1.95, y:1.15, w:7.5, h:0.80, fontFace:H, fontSize:34, bold:true, color:C.white, margin:0, valign:'middle', isTextBox:true });
  s.addText(br.blurb, { x:0.6, y:2.35, w:8.8, h:estH(br.blurb, 8.8, 15, B) + 0.10, fontFace:B, fontSize:15, color:'C9D4E0', margin:0, valign:'top', isTextBox:true });
  s.addText(br.groups.map(g => g.label).join('   ·   '), { x:0.6, y:4.52, w:8.8, h:0.44, fontFace:B, fontSize:12.5, italic:true, color:C.yellow, margin:0, valign:'middle', isTextBox:true });
  note(s, br.note);
  built++;

  br.groups.forEach(g => {
    // ---- group slide: what the group is, and the picture that makes it concrete ----
    s = light(); title(s, g.label, g.sub);
    if (g.table) {
      const rowH = 0.33, tH = (g.table.keys.length + 1) * rowH;
      const bh = card(s, LX, TOP, FW, null, g.body, C.blue, { fs:fitFs(g.body, FW - 0.40, FLOOR - TOP - tH - 0.52, DEFS, B) });
      const res = Object.fromEntries(EX[g.table.from]);
      tableBox(s, g.table.head, g.table.keys.map(([o, n2, e]) => [{ text:o, options:{ fontFace:M, bold:true } }, n2, { text:e, options:{ fontFace:M } },
               { text:res[e], options:{ fontFace:M, color:'1A7F37', bold:true } }]), LX, TOP + bh + 0.10, FW, [1.25, 3.25, 2.20, 2.40], { fs:12.5, rowH });
      caption(s, 'every value in the last column was produced by evaluating the expression beside it, under Python ' + py, LX, TOP + bh + 0.12 + tH, FW);
    } else if (g.program) {
      const plan = programPlan(g.program, 1.90);
      const bh = card(s, LX, TOP, FW, null, g.body, C.blue, { fs:fitFs(g.body, FW - 0.40, FLOOR - TOP - plan.h - 0.24, DEFS, B) });
      programDraw(s, g.program, TOP + bh + 0.12, plan);
    } else {
      const L = codeLines(rows(g.ex)), cw = g.exW || 4.0;
      const fs = fitCode(L, cw, CODES, FLOOR - TOP);
      codeCard(s, rows(g.ex), 9.55 - cw, TOP, cw, { fs });
      const bw = 9.55 - cw - LX - 0.28;
      card(s, LX, TOP, bw, null, g.body, C.blue, { fs:fitFs(g.body, bw - 0.40, FLOOR - TOP - 0.38, DEFS, B) });
    }
    note(s, g.note);
    built++;

    // ---- one slide per leaf concept ----
    g.leaves.forEach(lf => {
      s = light(); title(s, lf.t, lf.sub);
      const stacked = !!(lf.ladder || lf.threeway || lf.program);
      const twoCol = !stacked && !!(lf.ex || lf.term || lf.peps || lf.phases);
      const defW = twoCol ? LW : FW;
      const wFs = 11;
      const watchH = lf.watch ? estH('Watch out — ' + lf.watch, defW - 0.52, wFs, B) + 0.26 : 0;
      const chgH = (lf.changed && !twoCol) ? cardH(lf.changed, defW, 11.5, 'New since the book', 14) : 0;
      let extraH = 0, plan = null, ladderCode = null;

      if (lf.ladder) {                                        // the ladder and the shell card share one row
        const L = codeLines(rows(lf.ex)), fs = fitCode(L, 4.55, CODES, 1.74);
        ladderCode = { L, fs }; extraH = Math.max(1.74, codeH(L, 4.55, fs));
      } else if (lf.threeway) extraH = 1.42;
      else if (lf.program) { plan = programPlan(lf.program, FLOOR - TOP - watchH - 1.00); extraH = plan.h; }

      const gaps = 0.12 * (1 + (watchH > 0) + (chgH > 0) + (extraH > 0));
      const defBudget = Math.max(0.70, FLOOR - TOP - watchH - chgH - extraH - gaps - 0.38);
      let y = TOP;
      y += card(s, LX, y, defW, null, lf.def, C.blue, { fs:fitFs(lf.def, defW - 0.40, defBudget, DEFS, B) }) + 0.12;
      if (twoCol) {
        const rh = rightColumn(s, lf, RX, TOP, RW, FLOOR - TOP - (lf.changed ? 1.30 : 0));
        // what changed since the book sits under the picture, on the right, where there is room for it
        if (lf.changed) card(s, RX, TOP + rh + 0.12, RW, 'New since the book', lf.changed, C.blue,
                             { fs:fitFs(lf.changed, RW - 0.40, FLOOR - TOP - rh - 0.74, [11.5, 11, 10.5, 10, 9.5, 9], B), hf:14 });
      } else if (lf.changed) y += card(s, LX, y, defW, 'New since the book', lf.changed, C.blue, { fs:11.5, hf:14 }) + 0.12;
      if (ladderCode) { ladder(s, LX, y, 4.45); codeCard(s, rows(lf.ex), 5.00, y, 4.55, { fs:ladderCode.fs }); y += extraH + 0.12; }
      if (lf.threeway) y += threeway(s, y) + 0.12;
      if (plan)        y += programDraw(s, lf.program, y, plan) + 0.12;
      if (lf.watch)    y += watchStrip(s, LX, y, defW, lf.watch, wFs);

      if (y > HT - 0.10) throw new Error('the slide for ' + lf.t + ' runs ' + (y - HT + 0.10).toFixed(2) + ' in past the page');
      note(s, lf.note);
      built++;
    });
  });
});

// --- recap ---
s = light(); title(s, 'What to take away', 'One sentence for each branch of the chapter');
[['I · Values', 'Every value has a type, and the type decides what can be done with it. Integers are exact and unbounded; floats are binary approximations; a number in quotation marks is text.'],
 ['II · Operations', 'Operators are applied in a fixed order, so an expression means exactly one thing; the same symbol does different work on numbers and on strings, and an assignment stores rather than compares.'],
 ['III · Built-in functions', 'A call is an expression: it runs a function and has a value. print writes text out, input reads text in, str, int and float convert between types, and len measures.'],
 ['IV · The execution environment', 'The course runs CPython ' + py + '. Source is compiled to bytecode; the default build holds a global interpreter lock; the free-threaded build has been officially supported since 3.14.'],
 ['V · Modern practice', 'Build strings with f-strings rather than with plus signs, and give every project its own environment, created and filled by a package manager such as uv.']
].forEach(([h, t], i) => {
  const y = 1.26 + i * 0.80;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:0.45, y, w:2.05, h:0.70, fill:{color:C.navy}, line:{color:C.navy}, rectRadius:0.07 });
  s.addText(h, { x:0.52, y, w:1.91, h:0.70, fontFace:H, fontSize:11.5, bold:true, color:C.white, valign:'middle', margin:0, isTextBox:true });
  s.addText(t, { x:2.62, y, w:6.93, h:0.70, fontFace:B, fontSize:11.5, color:C.ink, valign:'middle', margin:0, isTextBox:true });
});
note(s, 'Use this slide as a spoken summary rather than reading it: take each branch in turn and ask the class for the sentence before you show it. If a branch produces silence, that is the branch to revisit at the start of the next session. Tell students that the five sentences are the minimum they should be able to reproduce without notes, and that the interactive page for chapter 1 will ask them the same things in question form.');
built++;

// --- questions ---
for (let k = 0; k < QUESTIONS.length; k += 6) {
  s = light(); title(s, 'Questions', 'Predict the answer first, then check it in the shell  ·  ' + (k / 6 + 1) + ' of ' + Math.ceil(QUESTIONS.length / 6));
  QUESTIONS.slice(k, k + 6).forEach(([q, tag], i) => {
    const y = 1.30 + i * 0.63;
    s.addShape(pres.shapes.OVAL, { x:0.45, y:y+0.05, w:0.44, h:0.44, fill:{color:C.yellow}, line:{color:C.yellow} });
    s.addText(String(k + i + 1), { x:0.45, y:y+0.05, w:0.44, h:0.44, fontFace:H, fontSize:14, bold:true, color:C.navy, align:'center', valign:'middle', margin:0, isTextBox:true });
    s.addText(q, { x:1.05, y, w:6.55, h:0.54, fontFace:B, fontSize:12.5, color:C.ink, valign:'middle', margin:0, isTextBox:true });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:7.75, y:y+0.08, w:1.80, h:0.38, fill:{color:C.card}, line:{color:C.card}, rectRadius:0.06 });
    s.addText(tag, { x:7.78, y:y+0.08, w:1.74, h:0.38, fontFace:B, fontSize:9.5, italic:true, color:C.mute, align:'center', valign:'middle', margin:0, isTextBox:true });
  });
  note(s, 'These questions come from the chapter\'s own question bank (08-tooling/ch01-page/question_bank_v1_1_0.json), reworded as open questions so that they can be asked aloud. Give the class a minute on each, take an answer from the room before you give one, and have a shell open so that every answer can be settled by running it rather than by authority. The tag on the right names the concept the question belongs to, so an unsure room tells you which slide to go back to.');
  built++;
}

// --- sources ---
s = light(); title(s, 'Sources', 'Every claim beyond the book comes from the chapter\'s research record');
const prim = SRC.sources.filter(r => r.role === 'primary'), sec = SRC.sources.filter(r => r.role !== 'primary');
card(s, 0.45, 1.28, 9.10, 'Primary source', prim.map(r => r.label + ' — ' + r.url).join('\n'), C.blue, { fs:11.5 });
const secLines = sec.map(r => '· ' + r.label.replace(/ \(Python 3\.14\.\d documentation[^)]*\)/, '').replace(/ \(Python documentation\)/, ''));
s.addText(secLines.slice(0, 12).join('\n'), { x:0.45, y:2.30, w:4.55, h:2.35, fontFace:B, fontSize:9.5, color:C.ink, margin:0, valign:'top', isTextBox:true });
s.addText(secLines.slice(12).join('\n'), { x:5.10, y:2.30, w:4.45, h:2.35, fontFace:B, fontSize:9.5, color:C.ink, margin:0, valign:'top', isTextBox:true });
s.addText(sec.length + ' secondary sources, all recorded as verified in ' + SRC._research + '. Slides adapt Automate the Boring Stuff with Python (CC BY-NC-SA); see NOTICE_v1_2.md.',
          { x:0.45, y:4.74, w:9.10, h:0.44, fontFace:B, fontSize:10, italic:true, color:C.mute, margin:0, isTextBox:true });
note(s, 'Do not read this slide out. Say only that the chapter has one primary source, the book, and ' + sec.length + ' secondary sources, every one of which was fetched and recorded as verified in the chapter\'s research record before anything on these slides was written. Tell students where the record lives, because the point of showing it is that they can check a claim themselves, and invite them to do exactly that when something on a slide surprises them.');
built++;

// --- closing ---
s = dark();
s.addText('Next: Chapter 2 — Flow control', { x:0.6, y:1.35, w:8.8, h:0.80, fontFace:H, fontSize:30, bold:true, color:C.white, margin:0, valign:'middle', isTextBox:true });
s.addText('Booleans and truthiness, comparison and Boolean operators, if / elif / else, the match statement, and the errors each of them raises.',
          { x:0.6, y:2.25, w:8.8, h:0.70, fontFace:B, fontSize:16, color:C.yellow, margin:0, valign:'top', isTextBox:true });
s.addText('Before then: install Python 3.14 or run it with uv, work through the interactive page for chapter 1, and bring one question you could not answer from the shell.',
          { x:0.6, y:3.25, w:8.8, h:0.70, fontFace:B, fontSize:14, color:'C9D4E0', margin:0, valign:'top', isTextBox:true });
s.addText('Questions?', { x:0.6, y:4.35, w:8.8, h:0.56, fontFace:H, fontSize:24, italic:true, color:'8FA3B8', margin:0, valign:'middle', isTextBox:true });
note(s, 'Close by naming the homework precisely rather than generally: install the interpreter or get uv to run it, and work through the chapter 1 interactive page, which asks the same questions this deck ended on. Ask each student to bring one question they could not settle in the shell; those questions are the best opening for the next session, and they also tell you which part of today did not land.');
built++;

pres.writeFile({ fileName: process.argv[2] }).then(f => console.log('written', f, '-', built, 'slides, deck version', VERSION));
