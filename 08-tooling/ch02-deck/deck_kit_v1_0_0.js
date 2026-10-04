// The drawing kit the chapter 2 and chapter 3 lecture decks share: the house colours, faces and ">>>" title motif of
// ch01-deck/deck_v1_0_1.js, together with the measuring functions that let a slide be planned before it is drawn.
//
// Every box this kit draws has a height computed from its own text, at a type size chosen so that the text fits, and
// each average character width below is a little wider than the one ch01-deck/layout_check_v1_0_0.py assumes, so a
// slide this kit builds always reserves at least as much room as that check demands.
//
// Written out of ch01-deck/deck_v2_0_0.js rather than invented: chapter 1 proved the measuring approach, and chapters
// 2 and 3 are too long to repeat it twice more by hand.
module.exports = function kit(pres) {
  const C = { navy:'1E2A3A', blue:'306998', yellow:'FFD43B', ink:'1F2933', mute:'5B6B7B', card:'F1F4F8',
              code:'17202B', codeTxt:'E6EDF3', green:'7EE787', red:'FF7B72', white:'FFFFFF', line:'D0D7DE',
              deep:'0F1823', warmCard:'FFF1F0', warmLine:'FFD7D5', warmInk:'A4342C', ok:'1A7F37' };
  const H = 'Cambria', B = 'Calibri', M = 'Courier New';
  const PT = 72, LH = 1.22, HT = 5.625;
  const CW = { [M]:0.605, [B]:0.50, [H]:0.52 };
  const TOP = 1.26, FLOOR = 5.10;
  const LX = 0.45, LW = 5.27, RX = 5.86, RW = 3.69, FW = 9.10;
  const DEFS = [13, 12.5, 12, 11.5, 11, 10.5, 10, 9.5, 9];
  const CODES = [14, 13, 12, 11, 10, 9, 8, 7];

  function wrapLines(text, wIn, fs, face) {
    const cpl = Math.max(1, Math.floor(wIn * PT / (CW[face] * fs)));
    let n = 0; String(text).split('\n').forEach(l => { n += Math.max(1, Math.ceil(l.length / cpl)); }); return n;
  }
  const estH = (text, wIn, fs, face) => wrapLines(text, wIn, fs, face) * fs * LH / PT;
  function fitFs(text, wIn, hIn, sizes, face) {
    for (const fs of sizes) if (estH(text, wIn, fs, face) <= hIn) return fs;
    return sizes[sizes.length - 1];
  }
  const cardH = (body, w, fs, head, hf) => 0.18 + (head ? (hf || 15) * LH / PT + 0.10 : 0) + estH(body, w - 0.40, fs, B) + 0.20;

  function chip(s, x, y, w, h, fsz) {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill:{color:C.yellow}, line:{color:C.yellow}, rectRadius:0.08 });
    s.addText('>>>', { x, y, w, h, fontFace:M, fontSize:fsz, bold:true, color:C.navy, align:'center', valign:'middle', margin:0, isTextBox:true });
  }
  const light = () => { const s = pres.addSlide(); s.background = { color:C.white }; return s; };
  const dark  = () => { const s = pres.addSlide(); s.background = { color:C.navy };  return s; };
  function title(s, t, sub) {
    chip(s, 0.42, 0.34, 0.60, 0.42, 14);
    s.addText(t, { x:1.15, y:0.24, w:8.4, h:0.60, fontFace:H, fontSize: t.length > 46 ? 24 : 28, bold:true, color:C.navy, margin:0, valign:'middle', isTextBox:true });
    if (sub) s.addText(sub, { x:1.15, y:0.82, w:8.4, h:0.34, fontFace:B, fontSize:13, italic:true, color:C.mute, margin:0, valign:'middle', isTextBox:true });
  }
  const caption = (s, t, x, y, w) => s.addText(t, { x, y, w, h:0.22, fontFace:B, fontSize:9, italic:true, color:C.mute, align:'right', margin:0, isTextBox:true });

  function card(s, x, y, w, head, body, accent, opts = {}) {
    const fs = opts.fs || 13, hf = opts.hf || 15, inner = w - 0.40;
    const h = opts.h || cardH(body, w, fs, head, hf);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill:{color:opts.fill || C.card}, line:{color:opts.line || opts.fill || C.card}, rectRadius:0.10 });
    let ty = y + 0.14;
    if (head) { s.addText(head, { x:x+0.20, y:ty, w:inner, h:hf*LH/PT, fontFace:H, fontSize:hf, bold:true, color:accent || C.blue, margin:0, valign:'middle', isTextBox:true }); ty += hf*LH/PT + 0.08; }
    s.addText(body, { x:x+0.20, y:ty, w:inner, h:h - (ty - y) - 0.14, fontFace:B, fontSize:fs, color:opts.color || C.ink, margin:0, valign:'top', isTextBox:true });
    return h;
  }
  // ---- code: the shell card the deck check re-runs, and the plain card it leaves alone ----
  const codeLines = rs => { const L = []; rs.forEach(([c, r]) => { L.push('>>> ' + c); if (r !== null) L.push(r); }); return L; };
  function fitCode(lines, w, sizes, budget) {
    const inner = w - 0.44;
    for (const fs of sizes) {
      const h = 0.22 + lines.reduce((n, l) => n + wrapLines(l, inner, fs, M), 0) * fs * LH / PT;
      if (lines.every(l => l.length <= Math.floor(inner * PT / (CW[M] * fs))) && h + 0.26 <= budget) return fs;
    }
    return sizes[sizes.length - 1];
  }
  const codeH = (lines, w, fs) => 0.22 + lines.reduce((n, l) => n + wrapLines(l, w - 0.44, fs, M), 0) * fs * LH / PT + 0.26;
  function codeCard(s, rs, x, y, w, py, opts = {}) {
    if (rs[rs.length - 1][1] === null) throw new Error('a shell card must end with a line that shows a value');
    const L = codeLines(rs), inner = w - 0.44;
    const fs = opts.fs || fitCode(L, w, CODES, 99);
    const h = codeH(L, w, fs) - 0.26;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill:{color:C.code}, line:{color:C.code}, rectRadius:0.10 });
    const runs = [];
    rs.forEach(([c, r], i) => {
      const last = i === rs.length - 1;
      runs.push({ text:'>>> ', options:{ color:C.yellow, bold:true } });
      runs.push({ text:c, options:{ color:C.codeTxt, breakLine: r !== null || !last } });
      if (r !== null) runs.push({ text:r, options:{ color: /^[A-Za-z]*(Error|Exception|Interrupt|Warning):/.test(r) ? C.red : C.green, breakLine: !last } });
    });
    s.addText(runs, { x:x+0.22, y:y+0.11, w:inner, h:h-0.22, fontFace:M, fontSize:fs, valign:'top', margin:0, isTextBox:true });
    caption(s, 'run under Python ' + py, x, y + h + 0.02, w);
    return h + 0.26;
  }
  function plainCode(s, lines, x, y, w, opts = {}) {
    const inner = w - 0.44, txt = lines.map(l => (typeof l === 'string' ? l : l[0]) || ' ');
    const fs = opts.fs || fitCode(txt, w, CODES, opts.budget || 99);
    const h = 0.22 + txt.reduce((n, l) => n + wrapLines(l, inner, fs, M), 0) * fs * LH / PT;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill:{color:opts.fill || C.code}, line:{color:opts.fill || C.code}, rectRadius:0.10 });
    s.addText(lines.map((l, i) => ({ text:(typeof l === 'string' ? l : l[0]) || ' ',
              options:{ color:(typeof l === 'string' ? C.codeTxt : (l[1] || C.codeTxt)), breakLine: i < lines.length - 1 } })),
              { x:x+0.22, y:y+0.11, w:inner, h:h-0.22, fontFace:M, fontSize:fs, valign:'top', margin:0, isTextBox:true });
    return h;
  }
  function watchStrip(s, x, y, w, text, fs) {
    const h = estH('Watch out — ' + text, w - 0.52, fs, B) + 0.26;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill:{color:C.warmCard}, line:{color:C.warmLine}, rectRadius:0.08 });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w:0.07, h, fill:{color:C.red}, line:{color:C.red} });
    s.addText([{ text:'Watch out — ', options:{ bold:true, color:C.warmInk } }, { text, options:{ color:C.ink } }],
              { x:x+0.22, y:y+0.12, w:w-0.44, h:h-0.24, fontFace:B, fontSize:fs, margin:0, valign:'top', isTextBox:true });
    return h;
  }
  function tableBox(s, head, rws, x, y, w, colW, opts = {}) {
    const t = [head.map(h2 => ({ text:h2, options:{ bold:true, color:C.white, fill:{color:C.blue} } }))];
    rws.forEach(r => t.push(r.map(cell => (typeof cell === 'object') ? cell : { text:cell })));
    s.addTable(t, { x, y, w, colW, fontFace:B, fontSize:opts.fs || 12, color:C.ink, border:{ type:'solid', pt:0.5, color:C.line }, rowH:opts.rowH || 0.30, valign:'middle' });
    return (rws.length + 1) * (opts.rowH || 0.30);
  }
  // two cards side by side, for a recommended form against the form it replaces
  function compare(s, y, w, left, right, maxH) {
    const cw = (w - 0.30) / 2;
    const fs = Math.min(fitFs(left[1], cw - 0.40, maxH - 0.70, DEFS, B), fitFs(right[1], cw - 0.40, maxH - 0.70, DEFS, B));
    const h = Math.max(cardH(left[1], cw, fs, left[0], 14), cardH(right[1], cw, fs, right[0], 14));
    card(s, LX, y, cw, left[0], left[1], left[2] || C.ok, { fs, hf:14, h, fill:left[3] || C.card });
    card(s, LX + cw + 0.30, y, cw, right[0], right[1], right[2] || C.red, { fs, hf:14, h, fill:right[3] || C.warmCard, line:right[3] ? undefined : C.warmLine });
    return h;
  }
  return { C, H, B, M, PT, LH, HT, CW, TOP, FLOOR, LX, LW, RX, RW, FW, DEFS, CODES,
           wrapLines, estH, fitFs, cardH, chip, light, dark, title, caption, card,
           codeLines, fitCode, codeH, codeCard, plainCode, watchStrip, tableBox, compare };
};
