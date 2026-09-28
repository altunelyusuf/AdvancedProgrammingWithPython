const VERSION = "1.0.0";
const pptxgen = require('pptxgenjs'); const fs = require('fs');
const EX = JSON.parse(fs.readFileSync('examples_out_v1_0_0.json')); const py = EX._python; const PR = EX._programs;
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.author = 'Yusuf Altunel'; pres.title = 'SEN0414 Chapter 3 - Loops';
const C = { navy:'1E2A3A', blue:'306998', yellow:'FFD43B', ink:'1F2933', mute:'5B6B7B', card:'F1F4F8', code:'17202B', codeTxt:'E6EDF3', green:'7EE787', red:'FF7B72', white:'FFFFFF' };
const H='Cambria', B='Calibri', M='Courier New';
function chip(s,x,y){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w:0.62,h:0.42,fill:{color:C.yellow},line:{color:C.yellow},rectRadius:0.08}); s.addText('>>>',{x,y,w:0.62,h:0.42,fontFace:M,fontSize:14,bold:true,color:C.navy,align:'center',valign:'middle',margin:0,isTextBox:true}); }
function title(s,t,sub){ chip(s,0.5,0.38); s.addText(t,{x:1.25,y:0.28,w:8.2,h:0.62,fontFace:H,fontSize:30,bold:true,color:C.navy,margin:0,valign:'middle',isTextBox:true}); if(sub) s.addText(sub,{x:1.25,y:0.86,w:8.2,h:0.34,fontFace:B,fontSize:13,italic:true,color:C.mute,margin:0,isTextBox:true}); }
function codeCard(s,rows,x,y,w,h,fs){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,fill:{color:C.code},line:{color:C.code},rectRadius:0.1}); const runs=[];
  rows.forEach(([c,r],i)=>{ runs.push({text:'>>> ',options:{color:C.yellow,bold:true}}); runs.push({text:c,options:{color:C.codeTxt,breakLine:true}}); runs.push({text:r,options:{color:/Error/.test(r)?C.red:C.green,breakLine:i<rows.length-1}}); });
  s.addText(runs,{x:x+0.2,y:y+0.12,w:w-0.4,h:h-0.24,fontFace:M,fontSize:fs||15,valign:'top',margin:0,paraSpaceAfter:2,isTextBox:true});
  s.addText('run under Python '+py,{x,y:y+h+0.04,w,h:0.24,fontFace:B,fontSize:9,italic:true,color:C.mute,align:'right',margin:0,isTextBox:true}); }
function prog(s,p,x,y,w,h,fs){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,fill:{color:C.code},line:{color:C.code},rectRadius:0.1});
  s.addText(PR[p].code.trim().split('\n').map((l,i,a)=>({text:l,options:{color:C.codeTxt,breakLine:i<a.length-1}})),{x:x+0.2,y:y+0.12,w:w-0.4,h:h-0.24,fontFace:M,fontSize:fs||12,valign:'top',margin:0,isTextBox:true}); }
function trans(s,p,ris,x,y,w,h,fs){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,fill:{color:C.card},line:{color:C.card},rectRadius:0.1}); const t=[];
  ris.forEach((ri,k)=>{ const L=PR[p].runs[ri].lines; if(k>0) t.push({text:'— another run —',options:{color:C.mute,italic:true,breakLine:true,fontFace:B}});
    L.forEach((segs,i)=>{ segs.forEach((sg,j)=>t.push({text:sg[0],options:{color:sg[1]?C.blue:C.ink,bold:sg[1],breakLine:j===segs.length-1&&!(k===ris.length-1&&i===L.length-1)}})); }); });
  s.addText(t,{x:x+0.15,y:y+0.1,w:w-0.3,h:h-0.2,fontFace:M,fontSize:fs||12,valign:'top',margin:0,paraSpaceAfter:2,isTextBox:true});
  s.addText('real run'+(ris.length>1?'s':'')+' under Python '+py+(PR[p].runs[ris[0]].inputs.length?' — typed input in blue':''),{x,y:y+h+0.04,w,h:0.24,fontFace:B,fontSize:9,italic:true,color:C.mute,margin:0,isTextBox:true}); }
function card(s,x,y,w,h,head,body,accent){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,fill:{color:C.card},line:{color:C.card},rectRadius:0.1});
  s.addText(head,{x:x+0.2,y:y+0.15,w:w-0.4,h:0.4,fontFace:H,fontSize:17,bold:true,color:accent||C.blue,margin:0,isTextBox:true});
  s.addText(body,{x:x+0.2,y:y+0.58,w:w-0.4,h:h-0.7,fontFace:B,fontSize:13,color:C.ink,margin:0,valign:'top',isTextBox:true}); }
const light=()=>{const s=pres.addSlide(); s.background={color:C.white}; return s;}, dark=()=>{const s=pres.addSlide(); s.background={color:C.navy}; return s;}, note=(s,t)=>s.addNotes(t);
const BK='Automate the Boring Stuff with Python, 3rd edition, chapter 3 (Sweigart, 2025)';

let s=dark(); s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.6,y:1.2,w:1.2,h:0.8,fill:{color:C.yellow},line:{color:C.yellow},rectRadius:0.12});
s.addText('>>>',{x:0.6,y:1.2,w:1.2,h:0.8,fontFace:M,fontSize:30,bold:true,color:C.navy,align:'center',valign:'middle',margin:0,isTextBox:true});
s.addText('Chapter 3: Loops',{x:0.6,y:2.2,w:8.8,h:0.9,fontFace:H,fontSize:38,bold:true,color:C.white,margin:0,isTextBox:true});
s.addText('Repeating work — in the book’s terms and in today’s Python',{x:0.6,y:3.05,w:8.8,h:0.5,fontFace:B,fontSize:18,italic:true,color:C.yellow,margin:0,isTextBox:true});
s.addText('SEN0414 Advanced Programming · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University',{x:0.6,y:4.6,w:8.8,h:0.4,fontFace:B,fontSize:13,color:'C9D4E0',margin:0,isTextBox:true});
note(s,BK+'. Every result on these slides was produced by running it under Python '+py+'; every claim beyond the book is in 03-materials/ch03/rdodi.');

s=light(); title(s,'The chapter at a glance','The book’s sections, and where this course takes them');
[['while loops','the loop else and the := operator'],['for loops and range()','range is lazy; enumerate and zip'],['break and continue','the while True pattern'],['Importing modules','what PEP 8 says about it'],['Ending with sys.exit()','it raises an exception'],['Two short programs','iterating safely']].forEach(([a,b],i)=>{ const col=i%2,row=Math.floor(i/2),x=0.5+col*4.6,y=1.45+row*1.15;
  s.addShape(pres.shapes.OVAL,{x,y:y+0.08,w:0.55,h:0.55,fill:{color:C.blue},line:{color:C.blue}}); s.addText(String(i+1),{x,y:y+0.08,w:0.55,h:0.55,fontFace:H,fontSize:18,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addText(a,{x:x+0.7,y,w:3.7,h:0.4,fontFace:B,fontSize:15,bold:true,color:C.ink,margin:0,isTextBox:true}); s.addText('→ '+b,{x:x+0.7,y:y+0.4,w:3.7,h:0.35,fontFace:B,fontSize:13,italic:true,color:C.blue,margin:0,isTextBox:true}); });
note(s,'Section names from '+BK+'; the second line of each item is what the course adds from the chapter 3 research record.');

s=light(); title(s,'while: repeat while a condition holds','The condition is tested again after every pass');
prog(s,'waiting_v1_0_0.py',0.5,1.45,4.4,1.9,14); trans(s,'waiting_v1_0_0.py',[0],5.2,1.45,4.3,1.9,14);
card(s,0.5,3.7,9,1.3,'Unlike if','An if block runs once or not at all. A while block sends execution back to the top, so the number of passes depends on the data — here, on when the user types yes.',C.blue);
note(s,BK+', section while Loop Statements. Program written for this course; run under Python '+py+' with the three inputs shown.');

s=light(); title(s,'break, continue and while True','Leaving a loop, and skipping a pass');
prog(s,'summing_v1_0_0.py',0.5,1.45,4.9,2.55,12); trans(s,'summing_v1_0_0.py',[0],5.7,1.45,3.8,1.95,12);
card(s,5.7,3.95,3.8,1.2,'Stuck?','A program in an endless loop is stopped with Control-C, which raises KeyboardInterrupt.',C.blue);
s.addText('break leaves the loop; continue skips to the next pass. The x was skipped, the blank ended it.',{x:0.5,y:4.2,w:4.9,h:0.6,fontFace:B,fontSize:13,color:C.ink,margin:0,isTextBox:true});
note(s,BK+'. break and continue: The Python Tutorial, 4.4 (Python Software Foundation, 2026). KeyboardInterrupt: Built-in Exceptions, raised when the user hits the interrupt key, normally Control-C or Delete.');

s=light(); title(s,'for and range()','Each call makes an arithmetic progression of integers');
codeCard(s,EX.range,0.5,1.45,5.6,2.6,15);
card(s,6.4,1.45,3.1,2.9,'The end is excluded','The stop value is never part of the sequence: range(10) makes ten values, 0 to 9. A negative step counts down.',C.blue);
note(s,BK+', section for Loops and the range() Function. Results evaluated under Python '+py+' with list() so the values can be seen.');

s=light(); title(s,'range is lazy','It is not a list');
codeCard(s,EX.lazy,0.5,1.45,4.4,1.5,17); codeCard(s,EX.same,0.5,3.35,9,0.95,15);
card(s,5.2,1.45,4.3,1.75,'On demand','A range produces its values as the loop asks for them, saving space. It is iterable, so sum() and for accept it.',C.blue);
s.addText('range(10), range(0, 10) and range(0, 10, 1) give the same values — the book’s practice question 3.',{x:0.5,y:4.75,w:9,h:0.4,fontFace:B,fontSize:12,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,'The Python Tutorial, 4.3 The range() Function (Python Software Foundation, 2026): the object behaves as if it were a list but is not; it returns the successive items when iterated. Practice question from '+BK+'.');

s=light(); title(s,'for ... else','The else runs when the loop was not broken');
prog(s,'searching_v1_0_0.py',0.5,1.45,4.4,2.35,14); trans(s,'searching_v1_0_0.py',[0,1],5.2,1.45,4.3,2.35,14);
card(s,0.5,4.05,9,1.05,'Searching','A break says “found it”; the else says “searched everything and did not”. It is skipped after a break, a return or an exception.',C.blue);
note(s,'else Clauses on Loops, The Python Tutorial 4.5 and The Python Language Reference, 8.2 and 8.3 (Python Software Foundation, 2026). The program is this course’s own.');

s=light(); title(s,'The loop variable','It outlives the loop — or was never made');
prog(s,'loopvar_v1_0_0.py',0.5,1.45,4.4,1.9,14); trans(s,'loopvar_v1_0_0.py',[0],5.2,1.45,4.3,1.9,14);
card(s,0.5,3.7,9,1.3,'Two facts from the reference','Names in a for statement’s target list are not deleted when the loop ends. After a loop over an empty sequence they were never assigned. Assigning to the variable inside the block does not change the loop.',C.blue);
note(s,'The for statement, The Python Language Reference 8.3 (Python Software Foundation, 2026). Executed under Python '+py+'; the third fact is also executed in 08-tooling/sen0414_rdodi_checks_v1_0_0.py.');

s=light(); title(s,'enumerate and zip','Instead of index arithmetic');
codeCard(s,EX.enum,0.5,1.45,4.9,1.9,14); codeCard(s,EX.zip,5.6,1.45,3.9,3.0,12);
card(s,0.5,3.75,4.9,1.3,'Position and item','enumerate gives both, so range(len(a)) is rarely needed.',C.blue);
note(s,'enumerate and zip, Built-in Functions; Looping Techniques, The Python Tutorial 5.6 (Python Software Foundation, 2026). zip(strict=True) since Python 3.10 (Bucher, 2020): ValueError when the iterables differ in length. Results evaluated under Python '+py+'.');

s=light(); title(s,'Importing modules','Three forms, and what PEP 8 says');
card(s,0.5,1.45,2.9,2.4,'import random','Names stay under the module’s name: random.randint(1, 10). The clear form.',C.blue);
card(s,3.55,1.45,2.9,2.4,'import random, sys, os','Several at once. The book uses it; PEP 8 says imports should usually be on separate lines.',C.blue);
card(s,6.6,1.45,2.9,2.4,'from random import *','No prefix — and no way to tell where a name came from. The book and PEP 8 both advise against it.',C.blue);
s.addText('Prefer import random: every name shows where it came from.',{x:0.5,y:4.1,w:9,h:0.5,fontFace:B,fontSize:16,bold:true,color:C.blue,margin:0,isTextBox:true});
note(s,BK+', section Importing Modules. PEP 8 (Van Rossum et al., 2001): imports should usually be on separate lines; wildcard imports should be avoided.');

s=light(); title(s,'Ending a program: sys.exit()','It raises SystemExit');
prog(s,'quitting_v1_0_0.py',0.5,1.45,4.4,2.1,14); trans(s,'quitting_v1_0_0.py',[0],5.2,1.45,4.3,2.1,14);
card(s,0.5,3.9,9,1.2,'An exception, not a hard stop','sys.exit() raises SystemExit, so finally clauses still run, and an outer handler can intercept it. It exits the process only from the main thread.',C.blue);
note(s,BK+', section Ending a Program Early with sys.exit(). sys.exit, The Python Standard Library (Python Software Foundation, 2026).');

s=light(); title(s,'A short program: guess the number','Counted attempts, early exit, and the loop else');
prog(s,'guessing_v1_0_0.py',0.5,1.35,4.7,3.4,11); trans(s,'guessing_v1_0_0.py',[0,1],5.4,1.35,4.1,3.4,11);
s.addText('The seed makes the secret repeatable for the slide; a real game would not seed it.',{x:0.5,y:4.85,w:9,h:0.3,fontFace:B,fontSize:11,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,BK+', section A Short Program: Guess the Number. This program is the course’s own version: for attempt in range(1, 4), an early break, and the loop else instead of a flag. random.randint(a, b) returns N with a <= N <= b.');

s=light(); title(s,'Assignment expressions in loops','Read and test in one line — Python 3.8');
prog(s,'chunks_v1_0_0.py',0.5,1.45,4.4,1.6,14); trans(s,'chunks_v1_0_0.py',[0],5.2,1.45,4.3,1.6,14);
card(s,0.5,3.35,9,1.6,'The while True: pattern, shortened','The chapter’s loops read a value, test it, and break. := names the value inside the condition. PEP 572’s own example is while chunk := file.read(8192): — a loop that cannot be trivially rewritten with the two-argument iter().',C.blue);
note(s,'PEP 572, Assignment Expressions (Angelico et al., 2018), Python 3.8. The program reads an in-memory string three characters at a time.');

s=light(); title(s,'Two hazards','Changing what you iterate over, and leaving finally');
prog(s,'copying_v1_0_0.py',0.5,1.45,4.6,2.0,12); trans(s,'copying_v1_0_0.py',[0],5.4,1.45,4.1,1.0,13);
card(s,0.5,3.75,4.45,1.35,'Modifying while iterating','Tricky to get right: loop over a copy, as .copy().items() does, or build a new collection.',C.blue);
card(s,5.05,3.75,4.45,1.35,'New in 3.14','A return, break or continue that leaves a finally block now draws a SyntaxWarning (PEP 765).',C.blue);
note(s,'The for statement, The Python Tutorial 4.2 (Python Software Foundation, 2026). PEP 765 (Katriel and Coghlan, 2024), Python 3.14; What’s New In Python 3.14. The warning was reproduced under Python '+py+': ‘break’ in a ‘finally’ block.');

s=light(); title(s,'Check yourself','Predict first, then run it');
['What keys stop a program stuck in an infinite loop?','What is the difference between break and continue?','How do range(10), range(0, 10) and range(0, 10, 1) differ?','When does the else clause of a loop run?','What does zip(a, b, strict=True) do that zip(a, b) does not?'].forEach((q,i)=>{ const y=1.4+i*0.66;
  s.addShape(pres.shapes.OVAL,{x:0.5,y:y+0.04,w:0.46,h:0.46,fill:{color:C.yellow},line:{color:C.yellow}}); s.addText(String(i+1),{x:0.5,y:y+0.04,w:0.46,h:0.46,fontFace:H,fontSize:15,bold:true,color:C.navy,align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addText(q,{x:1.15,y,w:8.3,h:0.54,fontFace:B,fontSize:15,color:C.ink,valign:'middle',margin:0,isTextBox:true}); });
note(s,'Answers: Control-C (KeyboardInterrupt); break leaves the loop, continue goes to the next pass; they do not differ; when the loop finishes without a break; it raises ValueError when the iterables differ in length. Questions 1-3 follow the book’s practice questions.');

s=light(); title(s,'Sources','Every claim beyond the book is recorded in the chapter’s research record');
const src=['Sweigart, A. (2025). Automate the Boring Stuff with Python, 3rd ed., ch. 3. No Starch Press. automatetheboringstuff.com/3e','Python Software Foundation (2026). Python 3.14 documentation: Tutorial 4 and 5; Language Reference 8; Built-in Functions; sys; Built-in Exceptions; What’s New in 3.14','Angelico, C., Peters, T., van Rossum, G. (2018). PEP 572 – Assignment Expressions. peps.python.org','Bucher, B. (2020). PEP 618 – Add Optional Length-Checking To zip. peps.python.org','Katriel, I., Coghlan, A. (2024). PEP 765 – Disallow return/break/continue that exit a finally block','van Rossum, G., Warsaw, B., Coghlan, A. (2001). PEP 8 – Style Guide for Python Code'];
s.addText(src.map((t,i)=>({text:t,options:{bullet:true,breakLine:i<src.length-1}})),{x:0.5,y:1.4,w:9,h:3.4,fontFace:B,fontSize:12,color:C.ink,paraSpaceAfter:6,margin:0,valign:'top',isTextBox:true});
s.addText('Slides adapt Automate the Boring Stuff with Python (CC BY-NC-SA). See NOTICE_v1_2.md.',{x:0.5,y:4.95,w:9,h:0.3,fontFace:B,fontSize:10,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,'Full verified source list in 03-materials/ch03/rdodi/sen0414_ch03_research_v1_0_0.ttl.');

s=dark(); s.addText('Next week: Chapter 4 — Functions',{x:0.6,y:1.6,w:8.8,h:0.9,fontFace:H,fontSize:30,bold:true,color:C.white,margin:0,isTextBox:true});
s.addText('Before then: work through the chapter 3 interactive page and try its subject agents.',{x:0.6,y:2.6,w:8.8,h:0.8,fontFace:B,fontSize:17,color:C.yellow,margin:0,isTextBox:true});
s.addText('Questions?',{x:0.6,y:4.2,w:8.8,h:0.6,fontFace:H,fontSize:24,italic:true,color:'C9D4E0',margin:0,isTextBox:true});
note(s,'Chapter 4 of the 3rd edition is Functions.');
pres.writeFile({fileName:process.argv[2]}).then(f=>console.log('written',f));
