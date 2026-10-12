// SEN0414 chapter 13 deck renderer v1.0.0: the shared renderer ../deck_render_v1_0_0.js, unchanged, with one more item type,
// 'shapes', injected before it runs - the narrative diagrams as native PowerPoint shapes (boxes, lines, text frames) exactly as
// diagram_shapes_v1_0_0.py placed them. The shared file is read as text and compiled as the module it is; nothing in it is edited.
// Usage: node render_v1_0_0.js <deck_plan.json> <out.pptx>   (NODE_PATH must name the global node_modules, as for the shared file)
const Module = require('module'), fs = require('fs'), path = require('path');
const file = path.resolve(__dirname, '..', 'deck_render_v1_0_0.js');
let src = fs.readFileSync(file, 'utf8');
const MARK = 'const DRAW = {card:drawCard,';
if (src.indexOf(MARK) < 0) throw new Error('the shared renderer no longer has the line this wrapper extends');
const DRAWSHAPES = `
function drawShapes(s,e){ const SH={rect:pres.shapes.RECTANGLE, round:pres.shapes.ROUNDED_RECTANGLE, hex:pres.shapes.HEXAGON, oval:pres.shapes.OVAL};
  e.shapes.forEach(p=>{
    if(p.k==='box'){ const o={x:p.x,y:p.y,w:p.w,h:p.h,fill:{color:p.fill},line:{color:p.line,width:p.lw}}; if(p.shape==='round') o.rectRadius=0.08; s.addShape(SH[p.shape],o); }
    else if(p.k==='line'){ const o={x:Math.min(p.x1,p.x2),y:Math.min(p.y1,p.y2),w:Math.abs(p.x2-p.x1),h:Math.abs(p.y2-p.y1),line:{color:p.color,width:p.w}};
      if(p.arrow) o.line.endArrowType='triangle'; if(p.dash) o.line.dashType='dash';
      if(p.x2<p.x1) o.flipH=true; if(p.y2<p.y1) o.flipV=true;
      if(p.x1!==p.x2 && p.y1!==p.y2){ o.flipH=(p.x2<p.x1); o.flipV=(p.y2<p.y1); }
      s.addShape(pres.shapes.LINE,o); }
    else if(p.k==='text'){ const o={x:p.x,y:p.y,w:p.w,h:p.h,fontFace:B,fontSize:p.fs,color:p.color,bold:p.bold,italic:p.italic,align:p.align,valign:p.valign,margin:0,isTextBox:true}; if(p.fill) o.fill={color:p.fill}; s.addText(p.t,o); }
  }); }
`;
src = src.replace(MARK, DRAWSHAPES + '\nconst DRAW = {shapes:drawShapes, card:drawCard,');
const m = new Module(file, module);
m.filename = file;
m.paths = Module._nodeModulePaths(path.dirname(file));
m._compile(src, file);
