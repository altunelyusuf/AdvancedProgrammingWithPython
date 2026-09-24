const pptxgen = require('pptxgenjs');
const fs = require('fs');
const EX = JSON.parse(fs.readFileSync('examples_out.json'));
const FP = JSON.parse(fs.readFileSync('first_program.json'));
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9';
pres.author = 'Yusuf Altunel'; pres.title = 'SEN0414 Chapter 1 - Python Basics';
const C = { navy:'1E2A3A', blue:'306998', yellow:'FFD43B', ink:'1F2933', mute:'5B6B7B', card:'F1F4F8', code:'17202B', codeTxt:'E6EDF3', green:'7EE787', red:'FF7B72', white:'FFFFFF' };
const H = 'Cambria', B = 'Calibri', M = 'Courier New';
const py = EX._python;

function chip(s, x, y) { // the motif: a Python-yellow ">>>" prompt chip beside every title
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w:0.62, h:0.42, fill:{color:C.yellow}, line:{color:C.yellow}, rectRadius:0.08 });
  s.addText('>>>', { x, y, w:0.62, h:0.42, fontFace:M, fontSize:14, bold:true, color:C.navy, align:'center', valign:'middle', margin:0, isTextBox:true });
}
function title(s, t, sub) {
  chip(s, 0.5, 0.38);
  s.addText(t, { x:1.25, y:0.28, w:8.2, h:0.62, fontFace:H, fontSize:30, bold:true, color:C.navy, margin:0, valign:'middle', isTextBox:true });
  if (sub) s.addText(sub, { x:1.25, y:0.86, w:8.2, h:0.34, fontFace:B, fontSize:13, italic:true, color:C.mute, margin:0, isTextBox:true });
}
function codeCard(s, rows, x, y, w, h, opts={}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill:{color:C.code}, line:{color:C.code}, rectRadius:0.1 });
  const runs = [];
  rows.forEach(([c, r], i) => {
    runs.push({ text:'>>> ', options:{ color:C.yellow, bold:true } });
    runs.push({ text:c, options:{ color:C.codeTxt, breakLine:true } });
    const err = /Error:/.test(r);
    runs.push({ text:r, options:{ color: err ? C.red : C.green, breakLine: i < rows.length-1 } });
  });
  s.addText(runs, { x:x+0.2, y:y+0.12, w:w-0.4, h:h-0.24, fontFace:M, fontSize:opts.fs||15, valign:'top', margin:0, paraSpaceAfter:2, isTextBox:true });
  s.addText('run under Python ' + py, { x, y:y+h+0.04, w, h:0.24, fontFace:B, fontSize:9, italic:true, color:C.mute, align:'right', margin:0, isTextBox:true });
}
function note(s, t) { s.addNotes(t); }
function light() { const s = pres.addSlide(); s.background = { color:C.white }; return s; }
function dark() { const s = pres.addSlide(); s.background = { color:C.navy }; return s; }
function card(s, x, y, w, h, head, body, accent) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill:{color:C.card}, line:{color:C.card}, rectRadius:0.1 });
  s.addText(head, { x:x+0.2, y:y+0.15, w:w-0.4, h:0.4, fontFace:H, fontSize:17, bold:true, color:accent||C.blue, margin:0, isTextBox:true });
  s.addText(body, { x:x+0.2, y:y+0.58, w:w-0.4, h:h-0.7, fontFace:B, fontSize:13, color:C.ink, margin:0, valign:'top', isTextBox:true });
}
const g = (k, i) => EX[k][i];

// 1 title
let s = dark();
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:0.6, y:1.2, w:1.2, h:0.8, fill:{color:C.yellow}, line:{color:C.yellow}, rectRadius:0.12 });
s.addText('>>>', { x:0.6, y:1.2, w:1.2, h:0.8, fontFace:M, fontSize:30, bold:true, color:C.navy, align:'center', valign:'middle', margin:0, isTextBox:true });
s.addText('Chapter 1: Python Basics', { x:0.6, y:2.2, w:8.8, h:0.9, fontFace:H, fontSize:42, bold:true, color:C.white, margin:0, isTextBox:true });
s.addText('From the book\u2019s first steps to the Python you will actually run', { x:0.6, y:3.05, w:8.8, h:0.5, fontFace:B, fontSize:18, italic:true, color:C.yellow, margin:0, isTextBox:true });
s.addText('SEN0414 Advanced Programming \u00b7 Fall 2026 \u00b7 Yusuf Altunel, PhD \u00b7 \u0130stanbul K\u00fclt\u00fcr University', { x:0.6, y:4.6, w:8.8, h:0.4, fontFace:B, fontSize:13, color:'C9D4E0', margin:0, isTextBox:true });
note(s, 'Chapter 1 of Automate the Boring Stuff with Python, 3rd edition (Sweigart, 2025), renewed for an advanced course. Every code result in this deck was produced by running it under Python ' + py + ', installed with uv; every claim beyond the book comes from the chapter 1 RDODI research record in 03-materials/ch01/rdodi.');

// 2 why Python now - stat callouts
s = light(); title(s, 'Why Python, and why now', 'The language students run in 2026 is newer than the one most tutorials show');
[['3.14','current Python release','devguide.python.org/versions'],['1 Oct','Python 3.15 first release, 2026','devguide.python.org/versions'],['74%','admire uv, a Rust-built Python package manager','2025 Stack Overflow survey']].forEach(([n,l,src],i)=>{
  const x = 0.5 + i*3.05;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y:1.55, w:2.8, h:2.7, fill:{color:C.card}, line:{color:C.card}, rectRadius:0.12 });
  s.addText(n, { x, y:1.75, w:2.8, h:1.1, fontFace:H, fontSize:54, bold:true, color:C.blue, align:'center', margin:0, isTextBox:true });
  s.addText(l, { x:x+0.2, y:2.9, w:2.4, h:0.8, fontFace:B, fontSize:15, color:C.ink, align:'center', margin:0, isTextBox:true });
  s.addText(src, { x:x+0.2, y:3.75, w:2.4, h:0.35, fontFace:B, fontSize:10, italic:true, color:C.mute, align:'center', margin:0, isTextBox:true });
});
s.addText('An advanced course uses Python for its libraries and reach \u2014 so we start from the interpreter and tools students will really use.', { x:0.5, y:4.5, w:9, h:0.6, fontFace:B, fontSize:14, color:C.ink, margin:0, isTextBox:true });
note(s, 'Python 3.14 is the current bugfix release, first released 2025-10-07; 3.15 is scheduled for 2026-10-01 (Python Software Foundation, Status of Python versions). uv, a Python package manager built in Rust, was the most admired technology tag in the 2025 Stack Overflow Developer Survey at 74 per cent.');

// 3 roadmap
s = light(); title(s, 'The chapter at a glance', 'The book\u2019s sections, and where this course takes them further');
const road = [['Expressions in the interactive shell','the 3.13+ interpreter'],['Integer, float and string data types','precision and binary limits'],['String concatenation and replication','f-strings as the modern idiom'],['Storing values in variables','PEP 8 naming'],['Your first program, dissected','print, input, len, str, int, float'],['How computers store data','why 0.1 + 0.2 surprises']];
road.forEach(([a,b],i)=>{ const col=i%2, row=Math.floor(i/2); const x=0.5+col*4.6, y=1.45+row*1.15;
  s.addShape(pres.shapes.OVAL, { x, y:y+0.08, w:0.55, h:0.55, fill:{color:C.blue}, line:{color:C.blue} });
  s.addText(String(i+1), { x, y:y+0.08, w:0.55, h:0.55, fontFace:H, fontSize:18, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true });
  s.addText(a, { x:x+0.7, y, w:3.7, h:0.4, fontFace:B, fontSize:15, bold:true, color:C.ink, margin:0, isTextBox:true });
  s.addText('\u2192 ' + b, { x:x+0.7, y:y+0.4, w:3.7, h:0.35, fontFace:B, fontSize:13, italic:true, color:C.blue, margin:0, isTextBox:true }); });
note(s, 'Section names follow the 3rd edition\u2019s chapter 1 (Sweigart, 2025). The second line of each item is what this course adds, from the RDODI research record.');

// 4 interactive shell
s = light(); title(s, 'The interactive shell', 'Type an expression, get its value immediately');
codeCard(s, EX.shell, 0.5, 1.45, 4.3, 2.3, {fs:17});
card(s, 5.2, 1.45, 4.3, 2.6, 'New in Python 3.13', 'Python 3.13 replaced the interactive interpreter with a better one and improved its error messages \u2014 what you see from your very first expression is newer than the book\u2019s screenshots.', C.blue);
s.addText('An expression reduces to a single value. The shell evaluates it and prints the result.', { x:0.5, y:4.25, w:9, h:0.5, fontFace:B, fontSize:14, color:C.ink, margin:0, isTextBox:true });
note(s, 'What\u2019s New In Python 3.13 lists \u201cA better interactive interpreter\u201d and \u201cImproved error messages\u201d among its major changes (Python Software Foundation). Demonstrate live in the 3.14 shell.');

// 5 operators
s = light(); title(s, 'Operators', 'Seven arithmetic operators, from highest to lowest precedence');
const opRows = [['**','exponent','2 ** 8'],['%','modulus / remainder','23 % 7'],['//','integer (floor) division','23 // 7'],['/','division','23 / 7'],['*','multiplication','3 * 5'],['-','subtraction','5 - 2']];
const res = Object.fromEntries(EX.ops);
const tbl = [[{text:'Operator',options:{bold:true,color:C.white,fill:{color:C.blue}}},{text:'Operation',options:{bold:true,color:C.white,fill:{color:C.blue}}},{text:'Example',options:{bold:true,color:C.white,fill:{color:C.blue}}},{text:'Evaluates to',options:{bold:true,color:C.white,fill:{color:C.blue}}}]];
opRows.forEach(([o,n,e])=>tbl.push([{text:o,options:{fontFace:M,bold:true}},n,{text:e,options:{fontFace:M}},{text:res[e],options:{fontFace:M,color:'1A7F37'}}]));
tbl.push([{text:'+',options:{fontFace:M,bold:true}},'addition',{text:'2 + 2',options:{fontFace:M}},{text:Object.fromEntries(EX.shell)['2 + 2'],options:{fontFace:M,color:'1A7F37'}}]);
s.addTable(tbl, { x:0.5, y:1.4, w:9, colW:[1.2,3.0,2.4,2.4], fontFace:B, fontSize:14, color:C.ink, border:{type:'solid',pt:0.5,color:'D0D7DE'}, rowH:0.4 });
note(s, 'Operator table follows the 3rd edition\u2019s chapter 1 (Sweigart, 2025); every result was evaluated under Python ' + py + '.');

// 6 precedence
s = light(); title(s, 'Operator precedence decides the answer', 'Same numbers, different order, different result');
codeCard(s, [g('shell',1), g('shell',2)], 0.5, 1.45, 4.3, 1.7, {fs:18});
const ladder = ['( )  parentheses first','**  exponent','*  /  //  %','+  -'];
ladder.forEach((t,i)=>{ s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:5.2+i*0.25, y:1.45+i*0.72, w:4.3-i*0.25, h:0.58, fill:{color: i===0?C.yellow:C.card}, line:{color:i===0?C.yellow:C.card}, rectRadius:0.08 });
  s.addText(t, { x:5.4+i*0.25, y:1.45+i*0.72, w:4.0-i*0.25, h:0.58, fontFace:M, fontSize:14, bold:true, color:C.navy, valign:'middle', margin:0, isTextBox:true }); });
s.addText('Highest at the top. Equal precedence evaluates left to right.', { x:0.5, y:4.5, w:9, h:0.4, fontFace:B, fontSize:13, italic:true, color:C.mute, margin:0, isTextBox:true });
note(s, 'The Python Language Reference, section 6, tabulates precedence from most to least binding (Python Software Foundation). The book introduces the same order in chapter 1.');

// 7 division
s = light(); title(s, 'Dividing: three answers to one question', '23 divided by 7');
[['/', g('ops',1)[1], 'true division, always a float'],['//', g('ops',2)[1], 'floor division, the whole part'],['%', g('ops',3)[1], 'modulus, the remainder']].forEach(([o,v,l],i)=>{ const x=0.5+i*3.05;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y:1.5, w:2.8, h:2.8, fill:{color:C.card}, line:{color:C.card}, rectRadius:0.12 });
  s.addText('23 ' + o + ' 7', { x, y:1.65, w:2.8, h:0.5, fontFace:M, fontSize:20, bold:true, color:C.blue, align:'center', margin:0, isTextBox:true });
  s.addText(v, { x:x+0.1, y:2.25, w:2.6, h:1.0, fontFace:M, fontSize: v.length>6?17:44, bold:true, color:C.navy, align:'center', valign:'middle', margin:0, isTextBox:true });
  s.addText(l, { x:x+0.2, y:3.4, w:2.4, h:0.7, fontFace:B, fontSize:13, color:C.ink, align:'center', margin:0, isTextBox:true }); });
s.addText('Check: 7 \u00d7 3 + 2 = 23', { x:0.5, y:4.5, w:9, h:0.4, fontFace:B, fontSize:14, italic:true, color:C.mute, margin:0, isTextBox:true });
note(s, 'All three results evaluated under Python ' + py + '. // and % together split a division into quotient and remainder (Sweigart, 2025).');

// 8 data types
s = light(); title(s, 'Three data types', 'Every value has a type, and the type decides what you can do with it');
card(s, 0.5, 1.45, 2.85, 2.9, 'int', 'Whole numbers\n-2, 0, 30\nExact, with unlimited precision', C.blue);
card(s, 3.575, 1.45, 2.85, 2.9, 'float', 'Numbers with a fractional part\n-1.25, 0.5, 3.14\nStored in binary, so some decimals are approximate', C.blue);
card(s, 6.65, 1.45, 2.85, 2.9, 'str', 'Text between quotes\n\'Hello\', \'42\'\nA number in quotes is text, not a number', C.blue);
note(s, 'The Integer, Floating-Point, and String Data Types (Sweigart, 2025). Precision and representation from the Built-in Types page of the Python documentation.');

// 9 big integers
s = light(); title(s, 'Integers never overflow', 'Python integers have unlimited precision');
codeCard(s, EX.big, 0.5, 1.5, 9, 1.3, {fs:18});
card(s, 0.5, 3.2, 9, 1.35, 'Why it matters', 'Many languages cap integers at a fixed size and silently wrap around. Python computes 2 ** 100 exactly \u2014 useful for cryptography, identifiers and exact arithmetic.', C.blue);
note(s, '\u201cIntegers have unlimited precision.\u201d \u2014 Python documentation, Built-in Types, Numeric Types. Result evaluated under Python ' + py + '.');

// 10 floats
s = light(); title(s, 'Floats live in binary', 'Why 0.1 + 0.2 is not exactly 0.3');
codeCard(s, EX.float, 0.5, 1.45, 4.5, 1.7, {fs:17});
card(s, 5.3, 1.45, 4.2, 2.9, 'How computers store data', 'A float is stored in binary with fixed precision. 0.1 has no exact binary form, so the sum carries a tiny error. Round for display; never compare floats with == when money or precision matters.', C.blue);
note(s, 'Floating-Point Arithmetic: Issues and Limitations, The Python Tutorial, section 15 (Python Software Foundation). This links to the chapter\u2019s closing section, How Computers Store Data with Binary Numbers (Sweigart, 2025).');

// 11 strings
s = light(); title(s, 'Concatenation and replication', 'The same operators mean something different on strings');
codeCard(s, EX.str, 0.5, 1.45, 5.6, 2.35, {fs:15});
card(s, 6.4, 1.45, 3.1, 2.9, 'The error is a feature', 'Python will not guess whether you meant text or a number. Convert first: \'Alice\' + str(42).', C.red);
note(s, 'String Concatenation and Replication (Sweigart, 2025). The TypeError message is exactly what Python ' + py + ' prints.');

// 12 variables
s = light(); title(s, 'Variables and naming', 'A variable is a name bound to a value');
codeCard(s, EX.var.map(([c,r])=>[c.split('; ').join('\n>>> '), r]), 0.5, 1.45, 4.3, 2.3, {fs:15});
card(s, 5.2, 1.45, 4.3, 2.9, 'PEP 8 naming', 'lower_case_with_underscores for variables and functions\nMeaningful names: user_age, not ua\nNames are case-sensitive: spam and Spam differ', C.blue);
note(s, 'Storing Values in Variables (Sweigart, 2025). Naming convention from PEP 8, Style Guide for Python Code (van Rossum, Warsaw and Coghlan, 2001).');

// 13 first program
s = light(); title(s, 'Your first program', 'Saved in a file, run top to bottom');
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:0.5, y:1.4, w:5.3, h:3.3, fill:{color:C.code}, line:{color:C.code}, rectRadius:0.1 });
s.addText(FP.code.split('\n').filter(l=>l).map((l,i,a)=>({text:l, options:{color: l.startsWith('#') ? '8B949E' : C.codeTxt, breakLine: i<a.length-1}})), { x:0.7, y:1.5, w:4.95, h:3.1, fontFace:M, fontSize:11, valign:'top', margin:0, isTextBox:true });
const tr = []; FP.stdout.forEach(l=>{ if (l.startsWith('What is your age? ')) { tr.push(['What is your age? ', FP.inputs[1]]); tr.push([l.replace('What is your age? ',''), null]); } else { tr.push([l,null]); if (l==='What is your name?') tr.push([null, FP.inputs[0]]); } });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:6.0, y:1.4, w:3.5, h:3.3, fill:{color:C.card}, line:{color:C.card}, rectRadius:0.1 });
s.addText(tr.map(([o,i],k)=>[ ...(o?[{text:o,options:{color:C.ink}}]:[]), ...(i?[{text:i,options:{color:C.blue,bold:true}}]:[]) ].map((r,j,arr)=> (j===arr.length-1 && k<tr.length-1) ? {text:r.text, options:{...r.options, breakLine:true}} : r)).flat(), { x:6.15, y:1.5, w:3.2, h:3.1, fontFace:M, fontSize:11, valign:'top', margin:0, isTextBox:true });
s.addText('Output from a real run under Python ' + py + ' \u2014 typed input in blue', { x:6.0, y:4.75, w:3.5, h:0.3, fontFace:B, fontSize:9, italic:true, color:C.mute, margin:0, isTextBox:true });
note(s, 'Your First Program and Dissecting the Program (Sweigart, 2025), written here with f-strings. The transcript on the right is the program\u2019s actual output when run with the inputs shown.');

// 14 built-ins
s = light(); title(s, 'Six built-in functions', 'Always available, no import needed');
codeCard(s, EX.conv, 0.5, 1.4, 5.2, 3.2, {fs:13});
card(s, 6.0, 1.45, 3.5, 3.0, 'input() returns text', 'Whatever the user types arrives as a string. Convert it with int() or float() before doing arithmetic \u2014 and expect a ValueError when the text is not a number.', C.blue);
note(s, 'print, input, len, str, int and float are all documented on the Built-in Functions page (Python Software Foundation). Input as text is the chapter\u2019s own point (Sweigart, 2025).');

// 15 f-strings
s = light(); title(s, 'Modern idiom: f-strings', 'Build strings with values inside, instead of adding them together');
codeCard(s, EX.fstr.map(([c,r])=>[c.replace('; ','\n>>> '), r]), 0.5, 1.45, 9, 1.35, {fs:15});
card(s, 0.5, 3.15, 4.35, 1.45, 'Concatenation', "'Hello, ' + name + '!'  \u2014 works, but every value must already be a string", C.mute);
card(s, 5.15, 3.15, 4.35, 1.45, 'f-string', "f'Hello, {name}!'  \u2014 any expression inside braces, formatted for you", C.blue);
note(s, 'PEP 701, Syntactic formalization of f-strings (Galindo Salgado, Taskaya, Nikolaou and G\u00f3mez Mac\u00edas, 2022), Python 3.12.');

// 16 looking ahead
s = light(); title(s, 'Where this course goes next', 'Two things from Python 3.13+ we will return to');
card(s, 0.5, 1.45, 4.35, 2.95, 'Free-threaded Python', 'Python 3.13 introduced an experimental free-threaded build of CPython, able to run threads truly in parallel \u2014 a preview of our multithreading outcome (LO-4).', C.blue);
card(s, 5.15, 1.45, 4.35, 2.95, 'uv and the ecosystem', 'uv installs packages and even Python itself \u2014 it installed the Python used to check this deck. Choosing and using libraries is our first outcome (LO-1).', C.blue);
note(s, 'What\u2019s New In Python 3.13 lists free-threaded CPython and an experimental JIT compiler (Python Software Foundation). uv: 2025 Stack Overflow Developer Survey. LO-1 and LO-4 are SEN0414\u2019s approved learning outcomes.');

// 17 self test
s = light(); title(s, 'Check yourself', 'Predict first, then run it in the shell');
const qs = ['What does 2 + 3 * 6 evaluate to, and why?','Why does 0.1 + 0.2 not print 0.3?','What is the type of the value input() returns?','Why does \'Alice\' + 42 raise an error, and how do you fix it?','Rewrite \'Hi \' + name + \'!\' as an f-string.'];
qs.forEach((q,i)=>{ const y = 1.4 + i*0.66;
  s.addShape(pres.shapes.OVAL, { x:0.5, y:y+0.04, w:0.46, h:0.46, fill:{color:C.yellow}, line:{color:C.yellow} });
  s.addText(String(i+1), { x:0.5, y:y+0.04, w:0.46, h:0.46, fontFace:H, fontSize:15, bold:true, color:C.navy, align:'center', valign:'middle', margin:0, isTextBox:true });
  s.addText(q, { x:1.15, y, w:8.3, h:0.54, fontFace:B, fontSize:15, color:C.ink, valign:'middle', margin:0, isTextBox:true }); });
note(s, 'Answers: 20 (multiplication before addition); floats are binary approximations; always a string; str and int do not combine silently, use str(42) or an f-string; f\u2019Hi {name}!\u2019. The book\u2019s own practice questions are at the end of chapter 1 (Sweigart, 2025).');

// 18 sources
s = light(); title(s, 'Sources', 'Every claim beyond the book is recorded in the chapter\u2019s research record');
const srcs = ['Sweigart, A. (2025). Automate the Boring Stuff with Python, 3rd ed., ch. 1. No Starch Press. automatetheboringstuff.com/3e','Python Software Foundation (2026). Python 3.14 documentation: Tutorial, Language Reference, Built-in Types, Built-in Functions, What\u2019s New 3.13/3.14. docs.python.org','Python Software Foundation (2026). Status of Python versions. devguide.python.org/versions','van Rossum, G., Warsaw, B., Coghlan, A. (2001). PEP 8 \u2013 Style Guide for Python Code. peps.python.org','Galindo Salgado, P. et al. (2022). PEP 701 \u2013 Syntactic formalization of f-strings. peps.python.org','Stack Overflow (2025). 2025 Developer Survey. survey.stackoverflow.co/2025'];
s.addText(srcs.map((t,i)=>({text:t, options:{bullet:true, breakLine:i<srcs.length-1}})), { x:0.5, y:1.4, w:9, h:3.4, fontFace:B, fontSize:12, color:C.ink, paraSpaceAfter:6, margin:0, valign:'top', isTextBox:true });
s.addText('Slides adapt Automate the Boring Stuff with Python (CC BY-NC-SA). See NOTICE.md.', { x:0.5, y:4.95, w:9, h:0.3, fontFace:B, fontSize:10, italic:true, color:C.mute, margin:0, isTextBox:true });
note(s, 'Full verified source list, fourteen entries, in 03-materials/ch01/rdodi/sen0414_ch01_research_v1_0_0.ttl.');

// 19 closing
s = dark();
s.addText('Next week: Chapter 2 \u2014 if-else and flow control', { x:0.6, y:1.6, w:8.8, h:0.9, fontFace:H, fontSize:28, bold:true, color:C.white, margin:0, isTextBox:true });
s.addText('Before then: install Python 3.14 (or run it with uv), and work through the interactive page for chapter 1.', { x:0.6, y:2.7, w:8.8, h:0.8, fontFace:B, fontSize:17, color:C.yellow, margin:0, isTextBox:true });
s.addText('Questions?', { x:0.6, y:4.2, w:8.8, h:0.6, fontFace:H, fontSize:24, italic:true, color:'C9D4E0', margin:0, isTextBox:true });
note(s, 'Chapter 2 of the 3rd edition is if-else and flow control; its renewed deck is the next item in this iteration.');

pres.writeFile({ fileName: process.argv[2] }).then(f => console.log('written', f));
