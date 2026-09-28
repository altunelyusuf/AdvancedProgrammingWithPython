const VERSION = "1.0.0";
const pptxgen = require('pptxgenjs'); const fs = require('fs');
const EX = JSON.parse(fs.readFileSync('examples_out_v1_0_0.json')); const py = EX._python; const PR = EX._programs;
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.author = 'Yusuf Altunel'; pres.title = 'SEN0414 Chapter 4 - Functions';
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
const BK='Automate the Boring Stuff with Python, 3rd edition, chapter 4 (Sweigart, 2025)';


let s=dark(); s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.6,y:1.2,w:1.2,h:0.8,fill:{color:C.yellow},line:{color:C.yellow},rectRadius:0.12});
s.addText('>>>',{x:0.6,y:1.2,w:1.2,h:0.8,fontFace:M,fontSize:30,bold:true,color:C.navy,align:'center',valign:'middle',margin:0,isTextBox:true});
s.addText('Chapter 4: Functions',{x:0.6,y:2.2,w:8.8,h:0.9,fontFace:H,fontSize:38,bold:true,color:C.white,margin:0,isTextBox:true});
s.addText('Names, scopes and the call stack — in the book’s terms and in today’s Python',{x:0.6,y:3.05,w:8.8,h:0.5,fontFace:B,fontSize:18,italic:true,color:C.yellow,margin:0,isTextBox:true});
s.addText('SEN0414 Advanced Programming · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University',{x:0.6,y:4.6,w:8.8,h:0.4,fontFace:B,fontSize:13,color:'C9D4E0',margin:0,isTextBox:true});
note(s,BK+'. Every result on these slides was produced by running it under Python '+py+'; every claim beyond the book is in 03-materials/ch04/rdodi.');

s=light(); title(s,'The chapter at a glance','The book’s sections, and where this course takes them');
[['Creating functions','def, calls, and not repeating code'],['Arguments and parameters','positional-only and keyword-only'],['Return values and None','defaults evaluated once'],['The call stack','frames, and the recursion limit'],['Local and global scopes','decided by scanning the body'],['Exception handling','and what 3.14 changed']].forEach(([a,b],i)=>{ const x=0.5+(i%2)*4.6, y=1.45+Math.floor(i/2)*1.15;
  s.addShape(pres.shapes.OVAL,{x,y:y+0.08,w:0.55,h:0.55,fill:{color:C.blue},line:{color:C.blue}}); s.addText(String(i+1),{x,y:y+0.08,w:0.55,h:0.55,fontFace:H,fontSize:18,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addText(a,{x:x+0.7,y,w:3.7,h:0.4,fontFace:B,fontSize:15,bold:true,color:C.ink,margin:0,isTextBox:true}); s.addText('→ '+b,{x:x+0.7,y:y+0.4,w:3.7,h:0.35,fontFace:B,fontSize:13,italic:true,color:C.blue,margin:0,isTextBox:true}); });
note(s,'Section names from '+BK+'; the second line of each item is what the course adds from the chapter 4 research record.');

s=light(); title(s,'def and calls','The body runs when the function is called');
prog(s,'hello_v1_0_0.py',0.5,1.45,4.4,2.1,14); trans(s,'hello_v1_0_0.py',[0],5.2,1.45,4.3,2.1,14);
card(s,0.5,3.9,9,1.2,'Define once, call often','A def statement creates the function; nothing in its body runs until a call. Each call jumps into the body and returns to the line after it.',C.blue);
note(s,BK+', section Creating Functions. The program is this course’s own, shortened from the book’s helloFunc.py; run under Python '+py+'.');

s=light(); title(s,'Why not paste the code?','The book’s own pasted listing drifted');
prog(s,'pasted_v1_0_0.py',0.5,1.45,5.6,2.3,11); trans(s,'pasted_v1_0_0.py',[0],6.3,1.45,3.2,1.1,12);
card(s,0.5,3.95,9,1.2,'Found by running both listings','The last pasted line in the book is print(\' Good evening!\') — with a leading space — so its output differs from the function version. That is the hazard the passage warns about.',C.blue);
note(s,BK+', section Creating Functions: the pasted listing ends print(\' Good evening!\'). Both of the book’s listings were run under Python '+py+' (08-tooling/sen0414_ch04_rdodi_data_v1_0_0.py, behaviours); their outputs differ in exactly that line. The program on the slide compares the two outputs as lists.');

s=light(); title(s,'Arguments and parameters','Values in, forgotten on return');
prog(s,'params_v1_0_0.py',0.5,1.45,4.6,2.4,13); trans(s,'params_v1_0_0.py',[0],5.4,1.45,4.1,1.6,12);
card(s,0.5,4.1,9,1.05,'Define, call, pass','An argument is the value passed; a parameter is the variable that receives it. The parameter does not exist once the call returns.',C.blue);
note(s,BK+', section Arguments and Parameters. The book prints NameError: name \'name\' is not defined for this mistake, as Python '+py+' does.');

s=light(); title(s,'Named parameters','Identified by name, not by position');
prog(s,'named_v1_0_0.py',0.5,1.45,4.6,1.5,14); trans(s,'named_v1_0_0.py',[0],5.4,1.45,4.1,1.5,14);
card(s,0.5,3.3,9,1.6,'print() has four','sep, end, file and flush can only be given by name. end=\'\' suppresses the newline; sep=\',\' changes the separator between values.',C.blue);
note(s,BK+', section Named Parameters. print, Built-in Functions (Python Software Foundation, 2026): sep, end, file and flush, if present, must be given as keyword arguments.');

s=light(); title(s,'Positional-only and keyword-only','What the chapter leaves for later');
prog(s,'kinds_v1_0_0.py',0.5,1.35,5.2,2.8,11); trans(s,'kinds_v1_0_0.py',[0],5.9,1.35,3.6,2.3,10.5);
card(s,0.5,4.35,9,0.85,'Slash and star','Before / : position only. After * : name only. A wrong call raises a TypeError that says which.',C.blue);
note(s,'PEP 570 (Hastings et al., 2018), Python 3.8, and PEP 3102 (Talin, 2006), Python 3.0. The program is this course’s own; run under Python '+py+'.');

s=light(); title(s,'Return values and None','A call is an expression');
prog(s,'returns_v1_0_0.py',0.5,1.45,4.6,2.3,13); trans(s,'returns_v1_0_0.py',[0],5.4,1.45,4.1,1.5,13);
codeCard(s,EX.types,0.5,4.0,4.6,1.1,13);
card(s,5.4,3.15,4.1,1.95,'Implicit None','A function with no return, or a bare return, gives back None, the only value of NoneType. Compare with is: PEP 8.',C.blue);
note(s,BK+', sections Return Values and return Statements and The None Value. return, The Python Language Reference 7.7: if an expression list is present it is evaluated, else None is substituted. PEP 8 (Van Rossum et al., 2001) on comparisons to None.');

s=light(); title(s,'Default values are evaluated once','A shared list is a classic trap');
prog(s,'defaults_v1_0_0.py',0.5,1.35,4.6,3.1,11); trans(s,'defaults_v1_0_0.py',[0],5.4,1.35,4.1,1.6,13);
card(s,5.4,3.25,4.1,1.55,'The remedy','Default to None and make the list inside the function, as collect_safely does.',C.blue);
note(s,'The Python Tutorial, 4.9.1 Default Argument Values (Python Software Foundation, 2026): the default is evaluated only once, which matters for a mutable object. The chapter defers its optional named parameters until lists and dictionaries have been met.');

s=light(); title(s,'The call stack','Where does execution go back to?');
prog(s,'stack_v1_0_0.py',0.5,1.35,5.0,3.0,11); trans(s,'stack_v1_0_0.py',[0],5.7,1.35,3.8,2.2,11);
card(s,0.5,4.45,9,0.75,'Frames','Each call adds a frame; a return removes the top one. The traceback module lists them.',C.blue);
note(s,BK+', section The Call Stack: frame objects are added to and removed from the top of the stack; the top frame is the function currently executing. The program is this course’s own; traceback.extract_stack lists the frames under Python '+py+'.');

s=light(); title(s,'The stack has a limit','RecursionError, not a crash');
prog(s,'recursion_v1_0_0.py',0.5,1.45,4.6,2.0,13); trans(s,'recursion_v1_0_0.py',[0],5.4,1.45,4.1,1.0,13);
codeCard(s,EX.limits,0.5,3.75,9,1.3,14);
note(s,'sys.getrecursionlimit and RecursionError (Python Software Foundation, 2026): the limit keeps infinite recursion from overflowing the C stack; RecursionError derives from RuntimeError. Executed under Python '+py+'.');

s=light(); title(s,'Local and global scopes','Same name, different variables');
prog(s,'scopes_v1_0_0.py',0.5,1.35,4.6,3.2,12); trans(s,'scopes_v1_0_0.py',[0],5.4,1.35,4.1,1.7,13);
card(s,5.4,3.4,4.1,1.6,'Three variables','One global name and two local ones, each in its own call. The book’s advice: give them unique names.',C.blue);
note(s,BK+', section Local and Global Scopes and Scope Rules; the book’s localGlobalSameName.py prints the same pattern. The program is this course’s own.');

s=light(); title(s,'The global statement','Assigning to the global, on purpose');
prog(s,'globalstmt_v1_0_0.py',0.5,1.45,4.6,2.7,13); trans(s,'globalstmt_v1_0_0.py',[0],5.4,1.45,4.1,1.2,13);
card(s,5.4,2.95,4.1,1.7,'Without it','An assignment inside a function makes a local variable: shadow() left the global alone.',C.blue);
note(s,BK+', section The global Statement. The program is this course’s own; run under Python '+py+'.');

s=light(); title(s,'Which scope? The compiler decides','Four rules, one fact');
prog(s,'symtable_v1_0_0.py',0.5,1.35,5.4,2.7,11); trans(s,'symtable_v1_0_0.py',[0],6.1,1.35,3.4,1.1,13);
card(s,0.5,4.3,9,0.85,'The fact','Local names are found by scanning the whole body for assignments. So an assignment anywhere makes a name local everywhere in that function.',C.blue);
note(s,BK+', section Scope Identification. The Python Language Reference 4.2.2 Resolution of names: the local variables of a code block can be determined by scanning the entire text of the block for name binding operations. The symtable module reports the result for the book’s spam, bacon and ham (a, b and c here).');

s=light(); title(s,'UnboundLocalError, in 3.14','The class is the book’s; the message is not');
prog(s,'unbound_v1_0_0.py',0.5,1.45,4.6,2.4,13); trans(s,'unbound_v1_0_0.py',[0],5.4,1.45,4.1,1.6,12);
card(s,0.5,4.1,9,1.05,'Book, then now','The book prints “local variable ‘eggs’ referenced before assignment”. Python 3.14.4 and the Programming FAQ say “cannot access local variable … where it is not associated with a value”.',C.blue);
note(s,BK+', section Scope Identification. Programming FAQ, Why am I getting an UnboundLocalError (Python Software Foundation, 2026). The class is a subclass of NameError. Executed under Python '+py+'.');

s=light(); title(s,'Between local and global: nonlocal','An inner function rebinding the outer one’s variable');
prog(s,'nonlocal_v1_0_0.py',0.5,1.45,4.6,2.6,13); trans(s,'nonlocal_v1_0_0.py',[0],5.4,1.45,4.1,0.9,14);
card(s,5.4,2.75,4.1,1.9,'Not in the chapter','Without the nonlocal line the += would make total a local of add(), and raise UnboundLocalError.',C.blue);
note(s,'The nonlocal statement, The Python Language Reference 7.13; PEP 3104 (Yee, 2006), Python 3.0. The program is this course’s own.');

s=light(); title(s,'try and except: handled inside','The function catches its own error');
prog(s,'inside_v1_0_0.py',0.5,1.45,4.6,2.6,12); trans(s,'inside_v1_0_0.py',[0],5.4,1.45,4.1,1.6,13);
card(s,0.5,4.3,9,0.85,'Where it lands','The call that failed returns None, so print shows None, and the program goes on to divide(1).',C.blue);
note(s,BK+', section Exception Handling: zeroDivide.py with the try inside spam(); the book prints 21.0, 3.5, Error: Invalid argument., None, 42.0. The Python Tutorial 8.3 (Python Software Foundation, 2026): if an exception occurs in the try clause the rest of it is skipped and a matching except clause runs. The program is this course’s own.');

s=light(); title(s,'try and except: handled outside','The error unwinds through the call');
prog(s,'outside_v1_0_0.py',0.5,1.45,4.6,2.6,12); trans(s,'outside_v1_0_0.py',[0],5.4,1.45,4.1,1.3,13);
card(s,0.5,4.3,9,0.85,'No way back','Once execution jumps to the except clause it does not return to the try clause, so divide(1) is never called.',C.blue);
note(s,BK+', section Exception Handling: the calls inside a try block, whose spam(1) is never executed. The program is this course’s own.');

s=light(); title(s,'New in 3.14: except without brackets','Several types, no as clause');
prog(s,'except758_v1_0_0.py',0.5,1.45,4.6,1.7,13); trans(s,'except758_v1_0_0.py',[0],5.4,1.45,4.1,0.9,13);
card(s,0.5,3.4,9,1.6,'PEP 758','except ValueError, TypeError: is now allowed when there is no as clause. With as, the types must still be in brackets. Python 3.13 and earlier reject the bracket-free form.',C.blue);
note(s,'PEP 758 (Galindo Salgado and Cannon, 2024), Python 3.14; What’s New In Python 3.14. Executed under Python '+py+': the form with as is a SyntaxError, multiple exception types must be parenthesized when using as.');

s=light(); title(s,'New in 3.14: annotations are deferred','A function can name what does not exist yet');
prog(s,'annotations_v1_0_0.py',0.5,1.35,5.0,2.9,11); trans(s,'annotations_v1_0_0.py',[0],5.7,1.35,3.8,1.6,11);
card(s,0.5,4.4,9,0.8,'PEP 649','Annotations are evaluated only on request; reading them raises NameError until the names exist.',C.blue);
note(s,'PEP 649 and PEP 749 (Hastings, 2021), Python 3.14; What’s New In Python 3.14 and the annotationlib module. Executed under Python '+py+'.');

s=light(); title(s,'Practice: the Collatz sequence','The book’s first practice program, run');
prog(s,'collatz_v1_0_0.py',0.5,1.35,5.0,3.3,11); trans(s,'collatz_v1_0_0.py',[0],5.7,1.35,3.8,1.2,12);
s.addText('A function that prints and returns — the book’s spec — driven by a loop until the value is 1.',{x:5.7,y:2.9,w:3.8,h:1.0,fontFace:B,fontSize:13,color:C.ink,margin:0,isTextBox:true});
note(s,BK+', Practice Programs, The Collatz Sequence: for 3 the book’s output is 3 10 5 16 8 4 2 1. This is the course’s own solution, run under Python '+py+'.');

s=light(); title(s,'Practice: input validation','try and except around int()');
prog(s,'validated_v1_0_0.py',0.5,1.35,5.0,3.6,11); trans(s,'validated_v1_0_0.py',[0],5.7,1.35,3.8,1.9,11);
s.addText('int(\'puppy\') raises ValueError; the except clause asks again.',{x:5.7,y:3.6,w:3.8,h:0.8,fontFace:B,fontSize:13,color:C.ink,margin:0,isTextBox:true});
note(s,BK+', Practice Programs, Input Validation. The course’s own solution, with the two inputs shown, run under Python '+py+'.');

s=light(); title(s,'Functions as black boxes','Inputs in, a value out');
card(s,0.5,1.45,2.9,2.6,'Inputs','The parameters — and nothing else — decide what a function does with the outside world.',C.blue);
card(s,3.55,1.45,2.9,2.6,'Output','The return value is how a result leaves; a print is a side effect, and its return value is None.',C.blue);
card(s,6.6,1.45,2.9,2.6,'Local state','Its variables live in its own scope, so its code cannot change other functions’ variables.',C.blue);
s.addText('Scopes narrow the code that could be causing a bug.',{x:0.5,y:4.3,w:9,h:0.5,fontFace:B,fontSize:16,bold:true,color:C.blue,margin:0,isTextBox:true});
note(s,BK+', section Functions as “Black Boxes” and Summary.');

s=light(); title(s,'Check yourself','Predict first, then run it');
['When does the code in a function run: at def, or at the call?','What is the difference between an argument and a parameter?','What does a function with no return statement give back?','Which variable does print(x) use if the function also assigns x later?','Where does execution go when the error is raised inside a function called in a try block?'].forEach((q,i)=>{ const y=1.4+i*0.66;
  s.addShape(pres.shapes.OVAL,{x:0.5,y:y+0.04,w:0.46,h:0.46,fill:{color:C.yellow},line:{color:C.yellow}}); s.addText(String(i+1),{x:0.5,y:y+0.04,w:0.46,h:0.46,fontFace:H,fontSize:15,bold:true,color:C.navy,align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addText(q,{x:1.15,y,w:8.3,h:0.54,fontFace:B,fontSize:15,color:C.ink,valign:'middle',margin:0,isTextBox:true}); });
note(s,'Answers: at the call; the argument is the value passed, the parameter the variable that receives it; None; the local one, so UnboundLocalError; to the matching except clause, and it does not return into the try clause. Questions 2, 6 and 13 follow the book’s practice questions.');

s=light(); title(s,'Sources','Every claim beyond the book is recorded in the chapter’s research record');
const src=['Sweigart, A. (2025). Automate the Boring Stuff with Python, 3rd ed., ch. 4. No Starch Press. automatetheboringstuff.com/3e','Python Software Foundation (2026). Python 3.14 documentation: Tutorial 4 and 8; Language Reference 4 and 7; Programming FAQ; Built-in Functions and Exceptions; sys; What’s New in 3.14','Hastings, L. (2021). PEP 649, Deferred Evaluation Of Annotations. peps.python.org/pep-0649','Galindo Salgado, P., Cannon, B. (2024). PEP 758, except without parentheses. peps.python.org/pep-0758','Hastings, L. et al. (2018). PEP 570; Talin (2006). PEP 3102; Yee, K.-P. (2006). PEP 3104','Van Rossum, G. et al. (2001). PEP 8, Style Guide for Python Code. peps.python.org/pep-0008'];
s.addText(src.map((t,i)=>({text:t,options:{bullet:true,breakLine:i<src.length-1}})),{x:0.5,y:1.4,w:9,h:3.4,fontFace:B,fontSize:12,color:C.ink,paraSpaceAfter:6,margin:0,valign:'top',isTextBox:true});
s.addText('Slides adapt Automate the Boring Stuff with Python (CC BY-NC-SA). See NOTICE_v1_2.md.',{x:0.5,y:4.95,w:9,h:0.3,fontFace:B,fontSize:10,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,'Full verified source list in 03-materials/ch04/rdodi/sen0414_ch04_research_v1_0_0.ttl.');

s=dark(); s.addText('Next week: Chapter 5 — Debugging',{x:0.6,y:1.6,w:8.8,h:0.9,fontFace:H,fontSize:30,bold:true,color:C.white,margin:0,isTextBox:true});
s.addText('Before then: work through the chapter 4 interactive page and try its subject agents.',{x:0.6,y:2.6,w:8.8,h:0.8,fontFace:B,fontSize:17,color:C.yellow,margin:0,isTextBox:true});
s.addText('Questions?',{x:0.6,y:4.2,w:8.8,h:0.6,fontFace:H,fontSize:24,italic:true,color:'C9D4E0',margin:0,isTextBox:true});
note(s,'Chapter 5 of the 3rd edition is Debugging.');
pres.writeFile({fileName:process.argv[2]}).then(f=>console.log('written',f));
