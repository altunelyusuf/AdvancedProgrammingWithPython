// SEN0414 lecture-deck library, version 1.0.0. One renderer for every chapter: the house style of the chapter 3, 5 and 6
// decks (colours, fonts, the >>> title motif, the code card, the program-and-transcript pair, the card, the page chip)
// together with the generic lecture the course now builds from a chapter plan — a title, what the chapter covers, the
// outcomes it serves, the taxonomy as one connected tree, then the chapter's concepts in the taxonomy's own order with a
// section divider per branch, a lead slide per sub-branch and a slide per concept, and at the end a recap, questions
// from the chapter's own question bank, the sources and the week ahead.
//
// Nothing in this file is chapter text. Every sentence a slide shows comes from the plan (which reads the chapter corpus,
// its question bank, its objectives and its research record) or from the executed examples; the chapter's own deck file
// supplies only its executed diagrams. Click builds (objectName "...|bN") are attached afterwards by anim_inject.
'use strict';
const VERSION = '1.0.0';

const C = { navy: '1E2A3A', blue: '306998', yellow: 'FFD43B', ink: '1F2933', mute: '5B6B7B', card: 'F1F4F8',
  code: '17202B', codeTxt: 'E6EDF3', green: '2E9E5B', greenBg: 'DDF3E6', red: 'D64545', redBg: 'FBE1E1',
  amber: 'B7791F', amberBg: 'FCEFD0', white: 'FFFFFF', line: '9AA8B8', blueBg: 'E3EEF8', ruleTxt: '7EE787', errTxt: 'FF7B72' };
const H = 'Cambria', B = 'Calibri', M = 'Courier New';
const EM = { Calibri: 0.50, Cambria: 0.52, 'Courier New': 0.60 };

// ---- measurement: how many lines a string takes in a box, so no slide is built that cannot hold its own text --------
function wrapLines(text, wIn, size, face) {
  const cw = (EM[face] || 0.5) * size / 72;                 // inches per character, averaged over English prose
  const perLine = Math.max(1, Math.floor(wIn / cw));
  let lines = 0;
  for (const para of String(text).split('\n')) {
    const words = para.split(/\s+/).filter(Boolean);
    if (!words.length) { lines += 1; continue; }
    let cur = 0, n = 1;
    for (const w of words) {
      const add = cur ? w.length + 1 : w.length;
      if (cur + add > perLine && cur > 0) { n += 1; cur = w.length; } else { cur += add; }
    }
    lines += n;
  }
  return lines;
}
// the height a block of text takes in a text box of this width, measured exactly as deck_fit_check_v1_0_0.py measures
// the finished file: paragraph by paragraph, wrapped at the box width less the same inset, at 1.21 line heights, plus
// the space after every paragraph but the last.
function textH(text, wIn, size, face, spaceAfterPt) {
  const paras = String(text).split('\n');
  let total = 0;
  for (const p of paras) total += wrapLines(p, Math.max(0.2, wIn - 0.04), size, face) * size * 1.21 / 72;
  return total + (paras.length - 1) * ((spaceAfterPt || 0) / 72 + 0.02);
}
function fits(text, wIn, hIn, size, face, spaceAfterPt) { return textH(text, wIn, size, face, spaceAfterPt) <= hIn - 0.02; }
function pickSize(text, wIn, hIn, sizes, face, spaceAfterPt) {
  for (const s of sizes) if (fits(text, wIn, hIn, s, face, spaceAfterPt)) return s;
  return sizes[sizes.length - 1];
}
function splitSentences(t) { return String(t).split(/(?<=[.!?]) +(?=[A-Z(])/).map(s => s.trim()).filter(Boolean); }
// the leading whole sentences of a paragraph that fit; never a part of a sentence unless even one will not fit
function trimToFit(text, wIn, hIn, size, face) {
  const ss = splitSentences(text); let out = '';
  for (const s of ss) { const next = out ? out + ' ' + s : s; if (out && !fits(next, wIn, hIn, size, face, 0)) break; out = next; }
  if (out && fits(out, wIn, hIn, size, face, 0)) return out;
  const words = (ss[0] || String(text)).split(/\s+/); let acc = '';
  for (const w of words) { const next = acc ? acc + ' ' + w : w; if (acc && !fits(next + ' ...', wIn, hIn, size, face, 0)) break; acc = next; }
  return acc ? acc + ' ...' : '';
}
// the largest listed size at which the whole text fits, with the text itself; when nothing fits, the text is cut back
// to whole sentences at the smallest listed size, so no box is ever built that its own text overflows.
function fitText(text, wIn, hIn, sizes, face, spaceAfterPt) {
  for (const s of sizes) if (fits(text, wIn, hIn, s, face, spaceAfterPt)) return { text: String(text), size: s, full: true };
  const s = sizes[sizes.length - 1];
  const paras = String(text).split('\n');
  for (let keep = paras.length - 1; keep >= 1; keep--) {
    const t = paras.slice(0, keep).join('\n');
    if (fits(t, wIn, hIn, s, face, spaceAfterPt)) {
      const room = hIn - textH(t, wIn, s, face, spaceAfterPt) - (spaceAfterPt || 0) / 72 - 0.04;
      const extra = room > 0.3 ? trimToFit(paras[keep], wIn, room, s, face) : '';
      return { text: extra ? t + '\n' + extra : t, size: s, full: false };
    }
  }
  return { text: trimToFit(text, wIn, hIn, s, face), size: s, full: false };
}
// code: the largest size at which the longest line fits the text box's width and every line fits its height
function codeSize(lines, wIn, hIn, max, min) {
  const longest = lines.reduce((a, l) => Math.max(a, l.length), 1);
  const byW = (wIn - 0.04) * 72 / (longest * EM[M]);
  const byH = (hIn - 0.02 * Math.max(0, lines.length - 1) - 0.02) * 72 / (lines.length * 1.21);
  return Math.max(min || 6, Math.min(max || 12, Math.floor(Math.min(byW, byH) * 2) / 2));
}

function makeDeck(pptxgen, opts) {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_16x9';
  pres.author = 'Yusuf Altunel';
  pres.title = opts.title;
  const S = pres.shapes;
  const LEC = [];
  let cur = null;
  const nm = (name, k) => (name || 'x') + (k ? '|b' + k : '');
  const rect = (s, o, name, k) => s.addShape(o.shape || S.RECTANGLE, Object.assign(
    { line: { color: o.lineColor || o.fill || C.card, width: o.lw || 1, dashType: o.dash }, objectName: nm(name, k) }, o, { fill: { color: o.fill || C.card } }));
  const txt = (s, t, o, name, k) => s.addText(t, Object.assign(
    { fontFace: B, fontSize: 13, color: C.ink, margin: 0, isTextBox: true, valign: 'middle', objectName: nm(name, k) }, o));
  const arrow = (s, x1, y1, x2, y2, o, k) => {
    o = o || {};
    const x = Math.min(x1, x2), y = Math.min(y1, y2), w = Math.abs(x2 - x1), h = Math.abs(y2 - y1);
    s.addShape(S.LINE, { x, y, w, h, flipH: x2 < x1, flipV: y2 < y1,
      line: { color: o.color || C.mute, width: o.w || 2, endArrowType: o.noHead ? undefined : 'triangle', dashType: o.dash }, objectName: nm(o.name || 'arrow', k) });
  };
  const newSlide = bg => { const s = pres.addSlide(); s.background = { color: bg }; cur = { n: LEC.length + 1, title: '', say: '', concept: '', visual: '' }; LEC.push(cur); return s; };
  const light = () => newSlide(C.white);
  const dark = () => newSlide(C.navy);
  const note = (s, t) => { cur.say = t; s.addNotes(t); };
  const lec = (concept, visual, title) => { if (title) cur.title = title; cur.concept = concept || ''; cur.visual = visual || ''; };
  const chip = (s, x, y) => {
    rect(s, { x, y, w: 0.62, h: 0.42, fill: C.yellow, shape: S.ROUNDED_RECTANGLE, rectRadius: 0.08 });
    txt(s, '>>>', { x, y, w: 0.62, h: 0.42, fontFace: M, fontSize: 15, bold: true, color: C.navy, align: 'center' });
  };
  // every text box below is sized with fitText, which both chooses the size and, when even the smallest listed size
  // will not hold the text, cuts it back to whole sentences - so the renderer cannot build a box that overflows.
  function ftxt(s, text, box, sizes, o, name, k) {
    const f = fitText(text, box.w, box.h, sizes, (o && o.fontFace) || B, (o && o.paraSpaceAfter) || 0);
    const parts = f.text.split('\n');
    txt(s, parts.map((p, i) => ({ text: p, options: { breakLine: i < parts.length - 1 } })),
      Object.assign({ x: box.x, y: box.y, w: box.w, h: box.h, fontSize: f.size }, o || {}), name, k);
    return f;
  }
  function title(s, t, sub) {
    cur.title = t; chip(s, 0.45, 0.32);
    ftxt(s, t, { x: 1.2, y: 0.22, w: 8.4, h: 0.6 }, [22, 20, 18, 16, 15, 14], { fontFace: H, bold: true, color: C.navy }, 'title');
    if (sub) ftxt(s, sub, { x: 1.2, y: 0.8, w: 8.4, h: 0.46 }, [14, 13, 12, 11, 10.5], { italic: true, color: C.mute, valign: 'top' }, 'subtitle');
  }
  const footer = (s, left, right) => {
    ftxt(s, left, { x: 0.45, y: 5.13, w: 5.6, h: 0.3 }, [9.5, 9, 8.5, 8], { color: C.mute }, 'crumb');
    if (right) ftxt(s, right, { x: 6.1, y: 5.13, w: 3.45, h: 0.3 }, [9.5, 9, 8.5, 8], { color: C.mute, align: 'right' }, 'cite');
  };
  // ---- the house's own content shapes --------------------------------------------------------------------------
  function codeCard(s, rows, x, y, w, h, fs, k) {
    rect(s, { x, y, w, h, fill: C.code, shape: S.ROUNDED_RECTANGLE, rectRadius: 0.1 }, 'codebox', k);
    const runs = [];
    rows.forEach(([c, r]) => {
      runs.push({ text: '>>> ', options: { color: C.yellow, bold: true } });
      runs.push({ text: c, options: { color: C.codeTxt, breakLine: true } });
      runs.push({ text: r, options: { color: /Error/.test(r) ? C.errTxt : C.ruleTxt, breakLine: true } });
    });
    const lines = rows.reduce((a, [c, r]) => a.concat(['>>> ' + c, r]), []);
    const tw = w - 0.34, th = h - 0.2;
    txt(s, runs, { x: x + 0.17, y: y + 0.1, w: tw, h: th, fontFace: M, fontSize: fs || codeSize(lines, tw, th, 13, 6), valign: 'top', paraSpaceAfter: 0 }, 'codecard', k);
    txt(s, 'run under Python ' + opts.python, { x, y: y + h + 0.02, w, h: 0.2, fontSize: 8.5, italic: true, color: C.mute, align: 'right' }, 'codecap', k);
  }
  function prog(s, PR, p, x, y, w, h, k, maxfs) {
    rect(s, { x, y, w, h, fill: C.code, shape: S.ROUNDED_RECTANGLE, rectRadius: 0.1 }, 'progbox', k);
    const lines = PR[p].code.replace(/\n+$/, '').split('\n');
    const tw = w - 0.34, th = h - 0.18;
    const fs = codeSize(lines, tw, th, maxfs || 11, 5.5);
    txt(s, lines.map((l, i, a) => ({ text: l, options: { color: C.codeTxt, breakLine: i < a.length - 1 } })),
      { x: x + 0.17, y: y + 0.09, w: tw, h: th, fontFace: M, fontSize: fs, valign: 'top', paraSpaceAfter: 0 }, 'prog', k);
    txt(s, p, { x, y: y + h + 0.02, w, h: 0.2, fontSize: 8.5, italic: true, color: C.mute, align: 'right' }, 'progcap', k);
    return fs;
  }
  function trans(s, PR, p, ris, x, y, w, h, k, maxfs) {
    rect(s, { x, y, w, h, fill: C.card, shape: S.ROUNDED_RECTANGLE, rectRadius: 0.1 }, 'transbox', k);
    const t = []; const flat = [];
    ris.forEach((ri, kk) => {
      const L = PR[p].runs[ri].lines;
      if (kk > 0) { t.push({ text: '- another run -', options: { color: C.mute, italic: true, breakLine: true, fontFace: B } }); flat.push('- another run -'); }
      L.forEach((segs, i) => {
        flat.push(segs.map(sg => sg[0]).join(''));
        segs.forEach((sg, j) => t.push({ text: sg[0], options: { color: sg[1] ? C.blue : C.ink, bold: sg[1], breakLine: j === segs.length - 1 && !(kk === ris.length - 1 && i === L.length - 1) } }));
      });
    });
    const tw = w - 0.28, th = h - 0.14;
    txt(s, t, { x: x + 0.14, y: y + 0.07, w: tw, h: th, fontFace: M, fontSize: codeSize(flat, tw, th, maxfs || 11, 5.5), valign: 'top', paraSpaceAfter: 0 }, 'trans', k);
    txt(s, 'real run' + (ris.length > 1 ? 's' : '') + ' under Python ' + opts.python + (PR[p].runs[ris[0]].inputs.length ? ' - typed input in blue' : ''),
      { x, y: y + h + 0.02, w, h: 0.2, fontSize: 8.5, italic: true, color: C.mute, align: 'right' }, 'transcap', k);
  }
  function card(s, x, y, w, h, head, body, accent, k) {
    rect(s, { x, y, w, h, fill: C.card, shape: S.ROUNDED_RECTANGLE, rectRadius: 0.1 }, 'card', k);
    ftxt(s, head, { x: x + 0.16, y: y + 0.08, w: w - 0.32, h: 0.32 }, [15, 14, 13, 12, 11, 10], { fontFace: H, bold: true, color: accent || C.blue }, 'cardhead', k);
    ftxt(s, body, { x: x + 0.16, y: y + 0.44, w: w - 0.32, h: h - 0.52 }, [13, 12.5, 12, 11.5, 11, 10.5, 10], { color: C.ink, valign: 'top' }, 'cardbody', k);
  }
  // a full-width band: the head is set in the same size as the body, so the band's height is the body's height
  function band(s, x, y, w, h, head, body, col, bg, k) {
    rect(s, { x, y, w, h, fill: bg, lineColor: col, lw: 2, shape: S.ROUNDED_RECTANGLE, rectRadius: 0.1 }, 'band', k);
    const bw = w - 0.36, bh = h - 0.12;
    // the head run is set in Cambria, and deck_fit_check measures a whole paragraph at the first named face it
    // finds in it, so the band is measured in Cambria too - the wider of the two, which is the safe way round.
    const f = fitText(head + '  ' + body, bw, bh, [13.5, 13, 12.5, 12, 11.5, 11, 10.5], H, 0);
    const shown = f.text.slice(head.length + 2);
    txt(s, [{ text: head + '  ', options: { bold: true, color: col, fontFace: H, fontSize: f.size } }, { text: shown, options: { color: C.ink, fontSize: f.size } }],
      { x: x + 0.18, y: y + 0.06, w: bw, h: bh, valign: 'top' }, 'bandt', k);
  }
  function prose(s, text, x, y, w, h, k, sizes) {
    const f = ftxt(s, text, { x, y, w, h }, sizes || [14, 13.5, 13, 12.5, 12, 11.5], { color: C.ink, valign: 'top', paraSpaceAfter: 7 }, 'prose', k);
    return f.size;
  }
  // ---- diagrams built from the taxonomy ------------------------------------------------------------------------
  // the whole chapter as one connected tree: a branch column per top concept, its sub-branches under it, joined by lines
  function chapterTree(s, plan, x, y, w, h, kBase) {
    const tops = plan.tree, n = tops.length, gap = 0.12;
    const cw = (w - gap * (n - 1)) / n;
    tops.forEach((t, i) => {
      const xx = x + i * (cw + gap), kk = kBase ? kBase + i : 0;
      rect(s, { x: xx, y, w: cw, h: 0.56, fill: C.blue, lineColor: C.blue, shape: S.ROUNDED_RECTANGLE, rectRadius: 0.08 }, 'tree1', kk);
      ftxt(s, plan.concepts[t.id].label, { x: xx + 0.04, y, w: cw - 0.08, h: 0.56 }, [13, 12, 11, 10, 9, 8.5], { fontFace: H, bold: true, color: C.white, align: 'center' }, 'tree1t', kk);
      const subs = t.subs, sh = Math.min(0.52, (h - 0.8) / Math.max(1, subs.length) - 0.1);
      subs.forEach((sb, j) => {
        const yy = y + 0.72 + j * (sh + 0.12);
        arrow(s, xx + cw / 2, j === 0 ? y + 0.56 : yy - 0.12, xx + cw / 2, yy, { color: C.line, w: 1, noHead: true }, kk);
        rect(s, { x: xx + 0.03, y: yy, w: cw - 0.06, h: sh, fill: C.blueBg, lineColor: C.blue, shape: S.ROUNDED_RECTANGLE, rectRadius: 0.06 }, 'tree2', kk);
        const lab = plan.concepts[sb.id].label + '  (' + sb.leaves.length + ')';
        ftxt(s, lab, { x: xx + 0.06, y: yy, w: cw - 0.12, h: sh }, [11, 10.5, 10, 9.5, 9, 8.5, 8], { color: C.navy, align: 'center', bold: true }, 'tree2t', kk);
      });
    });
  }
  // one branch: its sub-branches as boxes, each listing the concepts it holds
  function branchTree(s, plan, branch, x, y, w, h, kBase) {
    const subs = branch.subs, n = subs.length, gap = 0.14;
    const cw = (w - gap * (n - 1)) / n;
    subs.forEach((sb, i) => {
      const xx = x + i * (cw + gap), kk = kBase ? kBase + i : 0;
      rect(s, { x: xx, y, w: cw, h: 0.5, fill: C.yellow, lineColor: C.yellow, shape: S.ROUNDED_RECTANGLE, rectRadius: 0.08 }, 'br1', kk);
      ftxt(s, plan.concepts[sb.id].label, { x: xx + 0.04, y, w: cw - 0.08, h: 0.5 }, [14, 13, 12, 11, 10, 9], { fontFace: H, bold: true, color: C.navy, align: 'center' }, 'br1t', kk);
      const list = sb.leaves.map(l => plan.concepts[l].label).join('\n');
      rect(s, { x: xx, y: y + 0.58, w: cw, h: h - 0.58, fill: '27374B', lineColor: '3B5B87', shape: S.ROUNDED_RECTANGLE, rectRadius: 0.08 }, 'br2', kk);
      ftxt(s, list, { x: xx + 0.1, y: y + 0.66, w: cw - 0.2, h: h - 0.74 }, [12, 11, 10.5, 10, 9.5, 9, 8.5, 8, 7.5], { color: 'DCE6F2', valign: 'top' }, 'br2t', kk);
    });
  }
  // one sub-branch: a table of the concepts in it, each with the example the corpus gives it
  function leafTable(s, plan, sub, x, y, w, h, kBase) {
    const rows = sub.leaves.map(l => [plan.concepts[l].label, plan.concepts[l].example]);
    const hh = 0.34;
    const rh = Math.min(0.5, (h - hh - 0.06) / rows.length);
    const c1 = Math.min(3.1, w * 0.38);
    rect(s, { x, y, w: c1 - 0.04, h: hh, fill: C.navy, lineColor: C.navy }, 'lt');
    ftxt(s, 'Concept', { x: x + 0.07, y, w: c1 - 0.18, h: hh }, [11, 10, 9], { bold: true, color: C.white }, 'lth1');
    rect(s, { x: x + c1, y, w: w - c1, h: hh, fill: C.navy, lineColor: C.navy }, 'lt');
    ftxt(s, 'The example the chapter uses for it', { x: x + c1 + 0.07, y, w: w - c1 - 0.18, h: hh }, [11, 10, 9, 8.5], { bold: true, color: C.white }, 'lth2');
    rows.forEach(([a, b], i) => {
      const yy = y + hh + 0.04 + i * rh, kk = kBase ? kBase + i : 0;
      rect(s, { x, y: yy, w: c1 - 0.04, h: rh - 0.04, fill: C.blueBg, lineColor: C.blueBg }, 'ltb', kk);
      ftxt(s, a, { x: x + 0.07, y: yy, w: c1 - 0.18, h: rh - 0.04 }, [12, 11, 10.5, 10, 9.5, 9, 8.5], { bold: true, color: C.navy }, 'lta', kk);
      rect(s, { x: x + c1, y: yy, w: w - c1, h: rh - 0.04, fill: C.card, lineColor: C.card }, 'ltb', kk);
      ftxt(s, b, { x: x + c1 + 0.07, y: yy, w: w - c1 - 0.18, h: rh - 0.04 }, [11, 10.5, 10, 9.5, 9, 8.5, 8, 7.5], { fontFace: M, color: C.ink }, 'ltb2', kk);
    });
  }
  return { pres, S, C, H, B, M, LEC, light, dark, note, lec, title, footer, chip, rect, txt, ftxt, arrow,
    codeCard, prog, trans, card, band, prose, chapterTree, branchTree, leafTable,
    pickSize, codeSize, trimToFit, fitText, splitSentences, wrapLines, textH,
    cur: () => cur, VERSION };
}

module.exports = { makeDeck, C, H, B, M, VERSION, pickSize, codeSize, fitText, wrapLines, textH, splitSentences };
