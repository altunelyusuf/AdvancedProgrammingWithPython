const pptxgen = require('pptxgenjs'); const fs = require('fs');
const EX = JSON.parse(fs.readFileSync('examples_out.json')); const py = EX._python; const PR = EX._programs;
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.author = 'Yusuf Altunel'; pres.title = 'SEN0414 Chapter 2 - if-else and Flow Control';
const C = { navy:'1E2A3A', blue:'306998', yellow:'FFD43B', ink:'1F2933', mute:'5B6B7B', card:'F1F4F8', code:'17202B', codeTxt:'E6EDF3', green:'7EE787', red:'FF7B72', white:'FFFFFF' };
const H='Cambria', B='Calibri', M='Courier New';
function chip(s,x,y){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w:0.62,h:0.42,fill:{color:C.yellow},line:{color:C.yellow},rectRadius:0.08}); s.addText('>>>',{x,y,w:0.62,h:0.42,fontFace:M,fontSize:14,bold:true,color:C.navy,align:'center',valign:'middle',margin:0,isTextBox:true}); }
function title(s,t,sub){ chip(s,0.5,0.38); s.addText(t,{x:1.25,y:0.28,w:8.2,h:0.62,fontFace:H,fontSize:30,bold:true,color:C.navy,margin:0,valign:'middle',isTextBox:true}); if(sub) s.addText(sub,{x:1.25,y:0.86,w:8.2,h:0.34,fontFace:B,fontSize:13,italic:true,color:C.mute,margin:0,isTextBox:true}); }
function codeCard(s,rows,x,y,w,h,fs){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,fill:{color:C.code},line:{color:C.code},rectRadius:0.1}); const runs=[];
  rows.forEach(([c,r],i)=>{ runs.push({text:'>>> ',options:{color:C.yellow,bold:true}}); runs.push({text:c,options:{color:C.codeTxt,breakLine:true}}); runs.push({text:r,options:{color:/Error/.test(r)?C.red:C.green,breakLine:i<rows.length-1}}); });
  s.addText(runs,{x:x+0.2,y:y+0.12,w:w-0.4,h:h-0.24,fontFace:M,fontSize:fs||15,valign:'top',margin:0,paraSpaceAfter:2,isTextBox:true});
  s.addText('run under Python '+py,{x,y:y+h+0.04,w,h:0.24,fontFace:B,fontSize:9,italic:true,color:C.mute,align:'right',margin:0,isTextBox:true}); }
function prog(s,p,x,y,w,h){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,fill:{color:C.code},line:{color:C.code},rectRadius:0.1});
  s.addText(PR[p].code.trim().split('\n').map((l,i,a)=>({text:l,options:{color:C.codeTxt,breakLine:i<a.length-1}})),{x:x+0.2,y:y+0.12,w:w-0.4,h:h-0.24,fontFace:M,fontSize:12,valign:'top',margin:0,isTextBox:true}); }
function runs(s,p,x,y,w,h){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,fill:{color:C.card},line:{color:C.card},rectRadius:0.1}); const t=[];
  PR[p].runs.forEach(([inp,out],i)=>{ const [prompt,res]=out.split(/: (.*)/s); t.push({text:prompt+': ',options:{color:C.ink}}); t.push({text:inp,options:{color:C.blue,bold:true,breakLine:true}}); t.push({text:res,options:{color:C.ink,breakLine:i<PR[p].runs.length-1}}); });
  s.addText(t,{x:x+0.15,y:y+0.1,w:w-0.3,h:h-0.2,fontFace:M,fontSize:12,valign:'top',margin:0,paraSpaceAfter:4,isTextBox:true});
  s.addText('three real runs under Python '+py+' \u2014 typed input in blue',{x,y:y+h+0.04,w,h:0.24,fontFace:B,fontSize:9,italic:true,color:C.mute,margin:0,isTextBox:true}); }
function card(s,x,y,w,h,head,body,accent){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,fill:{color:C.card},line:{color:C.card},rectRadius:0.1});
  s.addText(head,{x:x+0.2,y:y+0.15,w:w-0.4,h:0.4,fontFace:H,fontSize:17,bold:true,color:accent||C.blue,margin:0,isTextBox:true});
  s.addText(body,{x:x+0.2,y:y+0.58,w:w-0.4,h:h-0.7,fontFace:B,fontSize:13,color:C.ink,margin:0,valign:'top',isTextBox:true}); }
const light=()=>{const s=pres.addSlide(); s.background={color:C.white}; return s;}, dark=()=>{const s=pres.addSlide(); s.background={color:C.navy}; return s;}, note=(s,t)=>s.addNotes(t);
const BK='Automate the Boring Stuff with Python, 3rd edition, chapter 2 (Sweigart, 2025)';

let s=dark(); s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.6,y:1.2,w:1.2,h:0.8,fill:{color:C.yellow},line:{color:C.yellow},rectRadius:0.12});
s.addText('>>>',{x:0.6,y:1.2,w:1.2,h:0.8,fontFace:M,fontSize:30,bold:true,color:C.navy,align:'center',valign:'middle',margin:0,isTextBox:true});
s.addText('Chapter 2: if-else and Flow Control',{x:0.6,y:2.2,w:8.8,h:0.9,fontFace:H,fontSize:38,bold:true,color:C.white,margin:0,isTextBox:true});
s.addText('Deciding what runs \u2014 in the book\u2019s terms and in today\u2019s Python',{x:0.6,y:3.05,w:8.8,h:0.5,fontFace:B,fontSize:18,italic:true,color:C.yellow,margin:0,isTextBox:true});
s.addText('SEN0414 Advanced Programming \u00b7 Fall 2026 \u00b7 Yusuf Altunel, PhD \u00b7 \u0130stanbul K\u00fclt\u00fcr University',{x:0.6,y:4.6,w:8.8,h:0.4,fontFace:B,fontSize:13,color:'C9D4E0',margin:0,isTextBox:true});
note(s,BK+'. Every result on these slides was produced by running it under Python '+py+'; every claim beyond the book is in 03-materials/ch02/rdodi.');

s=light(); title(s,'The chapter at a glance','The book\u2019s sections, and where this course takes them');
[['Boolean values','any value can be tested for truth'],['Comparison operators','chained comparisons'],['Boolean operators','short-circuit returns an operand'],['Components of flow control','blocks are indentation'],['Flow control statements','the conditional expression'],['Two short programs','match as the modern alternative']].forEach(([a,b],i)=>{ const col=i%2,row=Math.floor(i/2),x=0.5+col*4.6,y=1.45+row*1.15;
  s.addShape(pres.shapes.OVAL,{x,y:y+0.08,w:0.55,h:0.55,fill:{color:C.blue},line:{color:C.blue}}); s.addText(String(i+1),{x,y:y+0.08,w:0.55,h:0.55,fontFace:H,fontSize:18,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addText(a,{x:x+0.7,y,w:3.7,h:0.4,fontFace:B,fontSize:15,bold:true,color:C.ink,margin:0,isTextBox:true}); s.addText('\u2192 '+b,{x:x+0.7,y:y+0.4,w:3.7,h:0.35,fontFace:B,fontSize:13,italic:true,color:C.blue,margin:0,isTextBox:true}); });
note(s,'Section names from '+BK+'; the second line of each item is what the course adds from the chapter 2 research record.');

s=light(); title(s,'Comparison operators','Each asks a question and answers True or False');
const cmpOps=['==','!=','<','>','<=','>='], cmpNames=['equal to','not equal to','less than','greater than','less than or equal to','greater than or equal to'];
const tb=[[{text:'Operator',options:{bold:true,color:C.white,fill:{color:C.blue}}},{text:'Meaning',options:{bold:true,color:C.white,fill:{color:C.blue}}},{text:'Example',options:{bold:true,color:C.white,fill:{color:C.blue}}},{text:'Evaluates to',options:{bold:true,color:C.white,fill:{color:C.blue}}}]];
EX.cmp.forEach(([c,r],i)=>tb.push([{text:cmpOps[i],options:{fontFace:M,bold:true}},cmpNames[i],{text:c,options:{fontFace:M}},{text:r,options:{fontFace:M,color:'1A7F37'}}]));
s.addTable(tb,{x:0.5,y:1.4,w:9,colW:[1.2,3.4,2.2,2.2],fontFace:B,fontSize:14,color:C.ink,border:{type:'solid',pt:0.5,color:'D0D7DE'},rowH:0.42});
note(s,'Operators from '+BK+', section Comparison Operators; every result evaluated under Python '+py+'.');

s=light(); title(s,'== is not =','Comparison asks; assignment stores');
codeCard(s,EX.eq,0.5,1.45,4.4,1.6,16);
card(s,5.2,1.45,4.3,2.9,'Two different questions','== compares two values and answers True or False. = stores a value in a variable. An integer never equals a string, even one with the same digits.',C.blue);
note(s,BK+'. Results evaluated under Python '+py+'.');

s=light(); title(s,'Boolean operators','and, or and not combine truth values');
codeCard(s,EX.logic,0.5,1.45,4.2,2.1,16); codeCard(s,EX.mix,5.0,1.45,4.5,1.6,14);
s.addText('Comparisons evaluate first, then not, then and, then or.',{x:5.0,y:3.45,w:4.5,h:0.9,fontFace:B,fontSize:14,color:C.ink,margin:0,isTextBox:true});
note(s,BK+', sections Boolean Operators and Mixing Boolean and Comparison Operators.');

s=light(); title(s,'Truthiness','Any value can be tested for truth, not only True and False');
codeCard(s,EX.truth,0.5,1.45,4.4,2.5,16);
card(s,5.2,1.45,4.3,2.9,'False values','None, False, zero of any numeric type, and empty sequences are false. Everything else is true \u2014 so the string \'0\' is true.',C.blue);
note(s,'Truth Value Testing, Python documentation (Python Software Foundation, 2026). Results evaluated under Python '+py+'.');

s=light(); title(s,'Short-circuit evaluation','and and or return one of their operands, not a Boolean');
codeCard(s,EX.short,0.5,1.45,4.6,2.1,16);
card(s,5.4,1.45,4.1,2.9,'A fallback idiom','x or default gives x when x is true, and default otherwise. The second operand is evaluated only when it is needed.',C.blue);
note(s,'The Python Language Reference, Boolean operations (Python Software Foundation, 2026): x or y evaluates x; if x is true its value is returned, otherwise y is evaluated and returned.');

s=light(); title(s,'Chained comparisons','x < y <= z means x < y and y <= z');
codeCard(s,EX.chain,0.5,1.45,4.4,1.6,17);
card(s,5.2,1.45,4.3,2.6,'Read it like mathematics','Each middle value is evaluated once and compared on both sides. 3 > 2 > 5 is False because 2 > 5 is false.',C.blue);
note(s,'Comparisons, The Python Language Reference (Python Software Foundation, 2026).');

s=light(); title(s,'Blocks and indentation','Components of flow control: a condition and a block');
card(s,0.5,1.45,4.35,2.9,'Condition','An expression evaluated for its truth value, deciding which block runs next.',C.blue);
card(s,5.15,1.45,4.35,2.9,'Block','Lines at the same indentation. Python uses indentation, not braces, so indentation is part of what the program means.',C.blue);
note(s,BK+', section Components of Flow Control.');

s=light(); title(s,'if, elif, else','At most one branch of the chain runs');
prog(s,'branching.py',0.5,1.45,4.6,2.4); runs(s,'branching.py',5.4,1.45,4.1,2.4);
note(s,BK+', section Flow Control Statements. The program and its three runs were executed under Python '+py+' with the inputs shown.');

s=light(); title(s,'Choosing a value in one line','The conditional expression x if C else y');
codeCard(s,EX.cond,0.5,1.45,9,1.1,17);
card(s,0.5,2.95,9,1.5,'When to use it','When a decision chooses a value rather than runs a block. For anything longer, a full if statement stays clearer.',C.blue);
note(s,'Conditional expressions, The Python Language Reference (Python Software Foundation, 2026).');

s=light(); title(s,'The match statement','Python 3.10\u2019s alternative to long elif chains');
prog(s,'matching.py',0.5,1.45,4.9,2.6); runs(s,'matching.py',5.7,1.45,3.8,2.6);
note(s,'PEP 634, Structural Pattern Matching (Bucher and van Rossum, 2020), Python 3.10. Unlike a C or Java switch, match compares a value\u2019s shape: the case [\'go\', direction] captures the second word. Executed under Python '+py+'.');

s=light(); title(s,'Style and current Python','Write conditions others can read');
card(s,0.5,1.45,4.35,2.9,'PEP 8','Test a Boolean directly: write if greeting: rather than if greeting == True:.',C.blue);
card(s,5.15,1.45,4.35,2.9,'New in 3.14','PEP 765 disallows return, break and continue that exit a finally block \u2014 one more way the language keeps control flow predictable.',C.blue);
note(s,'PEP 8 (van Rossum, Warsaw and Coghlan, 2001); PEP 765 (Katriel and Coghlan, 2024), Python 3.14.');

s=light(); title(s,'Check yourself','Predict first, then run it');
['What does 42 == \'42\' evaluate to?','What does bool(\'0\') evaluate to, and why?','What does \'\' or \'default\' return?','How many branches of an if-elif-else chain can run?','When is match clearer than an elif chain?'].forEach((q,i)=>{ const y=1.4+i*0.66;
  s.addShape(pres.shapes.OVAL,{x:0.5,y:y+0.04,w:0.46,h:0.46,fill:{color:C.yellow},line:{color:C.yellow}}); s.addText(String(i+1),{x:0.5,y:y+0.04,w:0.46,h:0.46,fontFace:H,fontSize:15,bold:true,color:C.navy,align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addText(q,{x:1.15,y,w:8.3,h:0.54,fontFace:B,fontSize:15,color:C.ink,valign:'middle',margin:0,isTextBox:true}); });
note(s,'Answers: False; True, since only the empty string is false; \'default\'; at most one; when one value is compared against many shapes or values.');

s=light(); title(s,'Sources','Every claim beyond the book is recorded in the chapter\u2019s research record');
const src=['Sweigart, A. (2025). Automate the Boring Stuff with Python, 3rd ed., ch. 2. No Starch Press. automatetheboringstuff.com/3e','Python Software Foundation (2026). Python 3.14 documentation: Control flow tutorial; Language Reference, Expressions; Built-in Types, Truth Value Testing','Bucher, B., van Rossum, G. (2020). PEP 634 \u2013 Structural Pattern Matching: Specification. peps.python.org','Katriel, I., Coghlan, A. (2024). PEP 765 \u2013 Disallow return/break/continue that exit a finally block','van Rossum, G., Warsaw, B., Coghlan, A. (2001). PEP 8 \u2013 Style Guide for Python Code'];
s.addText(src.map((t,i)=>({text:t,options:{bullet:true,breakLine:i<src.length-1}})),{x:0.5,y:1.4,w:9,h:3.4,fontFace:B,fontSize:12,color:C.ink,paraSpaceAfter:6,margin:0,valign:'top',isTextBox:true});
s.addText('Slides adapt Automate the Boring Stuff with Python (CC BY-NC-SA). See NOTICE.md.',{x:0.5,y:4.95,w:9,h:0.3,fontFace:B,fontSize:10,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,'Full verified source list in 03-materials/ch02/rdodi/sen0414_ch02_research_v1_0_0.ttl.');

s=dark(); s.addText('Next week: Chapter 3 \u2014 Loops',{x:0.6,y:1.6,w:8.8,h:0.9,fontFace:H,fontSize:30,bold:true,color:C.white,margin:0,isTextBox:true});
s.addText('Before then: work through the chapter 2 interactive page and try its subject agents.',{x:0.6,y:2.6,w:8.8,h:0.8,fontFace:B,fontSize:17,color:C.yellow,margin:0,isTextBox:true});
s.addText('Questions?',{x:0.6,y:4.2,w:8.8,h:0.6,fontFace:H,fontSize:24,italic:true,color:'C9D4E0',margin:0,isTextBox:true});
note(s,'Chapter 3 of the 3rd edition is Loops.');
pres.writeFile({fileName:process.argv[2]}).then(f=>console.log('written',f));
