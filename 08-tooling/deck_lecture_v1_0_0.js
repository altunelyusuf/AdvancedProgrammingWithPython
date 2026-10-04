// SEN0414 lecture sequence, version 1.0.0: the order and the layout of a chapter lecture, built from the chapter plan.
// The sequence is the chapter's own taxonomy: a title, what the chapter covers in the book's own sections, the
// objectives it serves, the chapter drawn as one connected tree, then every branch with a divider that draws the branch,
// a lead slide per sub-branch that tables its concepts, and a slide per concept carrying that concept's own paragraphs,
// its executed example and the chapter's warning about it; then a recap, the chapter's own questions, the sources the
// research record verified, and the week ahead.
//
// Every sentence comes from the plan or from the executed examples. The chapter's deck file passes `hooks.diagrams`,
// a map from a concept's identifier to a function that draws that concept's executed diagram over the whole content
// area instead of the default prose-and-example layout; the title, the footer and the speaker notes stay the same.
'use strict';
const VERSION = '1.0.0';
const Y_TOP = 1.32, Y_BOT = 5.02;

function buildLecture(D, plan, EX, hooks) {
  hooks = hooks || {};
  const PR = EX._programs, CE = EX._concepts || {}, LP = EX._leaf_program || {};
  const K = plan.concepts;
  const chapterWord = 'chapter ' + plan.chapter;
  const CITE = chapterWord + ' of Automate the Boring Stuff with Python, 3rd edition (Sweigart, 2025)';
  const SRC = ' Every printed result on this slide was produced by running the code under Python ' + plan.python + '.';
  const branchOf = id => { let n = id; while (K[n].parent) n = K[n].parent; return n; };
  const subOf = id => (K[id].level === 3 ? K[id].parent : id);
  const crumb = id => (K[id].level === 3 ? K[branchOf(id)].label + '  >  ' + K[K[id].parent].label : K[branchOf(id)].label);
  const para = (id, i) => K[id].paras[i] || '';
  const longProgram = p => { const L = PR[p].code.replace(/\n+$/, '').split('\n'); return L.length > 14 || L.reduce((a, l) => Math.max(a, l.length), 0) > 58; };

  // ---------------------------------------------------------------- 1. title
  let s = D.dark();
  D.lec('', '', plan.deck_title);
  D.rect(s, { x: 0.6, y: 1.1, w: 1.2, h: 0.8, fill: D.C.yellow, lineColor: D.C.yellow, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.12 });
  D.txt(s, '>>>', { x: 0.6, y: 1.1, w: 1.2, h: 0.8, fontFace: D.M, fontSize: 30, bold: true, color: D.C.navy, align: 'center' });
  D.txt(s, plan.deck_title, { x: 0.6, y: 2.05, w: 8.8, h: 0.9, fontFace: D.H, fontSize: 36, bold: true, color: D.C.white });
  D.txt(s, plan.deck_strapline, { x: 0.6, y: 2.95, w: 8.8, h: 0.6, fontSize: 17, italic: true, color: D.C.yellow, valign: 'top' });
  D.txt(s, 'SEN0414 Advanced Programming  |  Fall 2026  |  Yusuf Altunel, PhD  |  Istanbul Kultur University',
    { x: 0.6, y: 4.3, w: 8.8, h: 0.4, fontSize: 13, color: 'C9D4E0' });
  D.txt(s, plan.doc_title + '  |  ' + plan.concepts_count + ' concepts, ' + plan.leaf_count + ' of them worked through, all results re-run under Python ' + plan.python,
    { x: 0.6, y: 4.72, w: 8.8, h: 0.4, fontSize: 11, italic: true, color: '8FA3B8' });
  D.note(s, 'Welcome. This is ' + CITE + ', rebuilt for an advanced course from the chapter corpus: ' + plan.concepts_count +
    ' concepts, each explained in its own paragraphs, with every printed result on these slides produced by running the code under Python ' +
    plan.python + ' rather than copied from the book. ' + plan.doc_about +
    ' Say at the start that the interactive page for this chapter carries the same taxonomy, the same examples and a question bank, so nothing shown here is unavailable afterwards.');

  // ---------------------------------------------------------------- 2. what the chapter covers
  s = D.light();
  D.title(s, 'What this chapter covers', 'The book\'s own sections, and what this lecture adds to them');
  D.lec('', '', 'What this chapter covers');
  D.prose(s, plan.doc_about + '\n' + plan.provenance, 0.45, Y_TOP, 5.3, 2.5, 0);
  D.band(s, 0.45, 4.0, 5.3, 1.0, 'Read with it', 'The chapter page for this chapter carries the same concepts, the same executed examples and a question bank; the chapter document carries every paragraph in full.', D.C.blue, D.C.blueBg, 1);
  D.ftxt(s, 'The sections of ' + chapterWord + ', as the book sets them out', { x: 6.05, y: Y_TOP - 0.06, w: 3.5, h: 0.36 }, [11.5, 11, 10.5, 10], { bold: true, color: D.C.navy }, 'bsh');
  {
    const n = plan.book_sections.length, h = Math.min(0.36, 3.3 / n);
    plan.book_sections.forEach((t, i) => {
      const yy = Y_TOP + 0.38 + i * h;
      D.rect(s, { x: 6.05, y: yy, w: 3.5, h: h - 0.03, fill: i % 2 ? D.C.card : D.C.blueBg, lineColor: i % 2 ? D.C.card : D.C.blueBg }, 'bs');
      D.ftxt(s, (i + 1) + '.  ' + t, { x: 6.15, y: yy, w: 3.3, h: h - 0.03 }, [11, 10.5, 10, 9.5, 9, 8.5, 8], { color: D.C.ink }, 'bst');
    });
  }
  D.footer(s, 'Source: ' + plan.corpus_file + ' and the textbook ontology for the 3rd edition', CITE);
  D.note(s, 'Set the frame before any code. The left column is what the chapter is about and where its content comes from; the right column is the book\'s own table of contents for ' +
    chapterWord + ', taken from the textbook ontology, so students can line the lecture up against their reading. ' + plan.provenance +
    ' Emphasise that where this lecture goes beyond the book it says so on the slide and names the source.');

  // ---------------------------------------------------------------- 3. objectives
  s = D.light();
  D.title(s, 'What you should be able to do afterwards', plan.outcome_line);
  D.lec('', '', 'What you should be able to do afterwards');
  {
    const obs = plan.objectives, n = obs.length, h = Math.min(0.72, 3.5 / n);
    obs.forEach(([code, text, bloom], i) => {
      const yy = Y_TOP + i * (h + 0.06);
      D.rect(s, { x: 0.45, y: yy, w: 0.95, h: h, fill: D.C.blue, lineColor: D.C.blue, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.08 }, 'ob', i + 1);
      D.ftxt(s, code, { x: 0.45, y: yy, w: 0.95, h: h }, [16, 14, 12], { fontFace: D.H, bold: true, color: D.C.white, align: 'center' }, 'obc', i + 1);
      D.rect(s, { x: 1.5, y: yy, w: 6.75, h: h, fill: D.C.card, lineColor: D.C.card, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.08 }, 'obb', i + 1);
      D.ftxt(s, text, { x: 1.62, y: yy, w: 6.5, h: h }, [13.5, 13, 12.5, 12, 11.5, 11, 10.5], { color: D.C.ink }, 'obt', i + 1);
      D.rect(s, { x: 8.35, y: yy, w: 1.2, h: h, fill: D.C.amberBg, lineColor: D.C.amber, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.08 }, 'obl', i + 1);
      D.txt(s, bloom, { x: 8.35, y: yy, w: 1.2, h: h, fontSize: 11.5, bold: true, color: D.C.amber, align: 'center' }, 'oblt', i + 1);
    });
  }
  D.footer(s, 'Source: ' + plan.objectives_file + ' and 01-outcomes/sen0414_outcomes_v1_0_0.ttl', 'the level on the right is the Bloom level the objective is written at');
  D.note(s, 'Read the objectives out: they are what the week is marked against, and the exam questions for this chapter are written to them. ' +
    plan.outcome_note + ' Click them in one at a time so the room has a moment on each, and tell students the chapter page lists the same objectives beside the quiz.');

  // ---------------------------------------------------------------- 4. the chapter as one tree
  s = D.light();
  D.title(s, 'The chapter as one tree', 'Every concept this lecture teaches, in the order it teaches them; the number in each box is how many concepts it holds');
  D.lec('', '', 'The chapter as one tree');
  D.chapterTree(s, plan, 0.4, 1.45, 9.2, 3.3, 1);
  D.footer(s, 'Drawn from ' + plan.corpus_file + ', the same taxonomy the chapter page draws', CITE);
  D.note(s, 'This is the map for the next three hours, and it is the chapter\'s own taxonomy, not a summary written for the slides: the interactive page draws the same tree. ' +
    'Each column is a branch, each box under it a sub-branch, and the number is how many concepts sit inside it. ' +
    'Tell students that every box becomes a slide, that the order on this map is the order of the lecture, and that when they lose the thread they should ask which box we are in. ' +
    'Click the branches in one at a time.');

  // ---------------------------------------------------------------- the branches
  plan.tree.forEach(branch => {
    const b = K[branch.id];
    // branch divider
    s = D.dark();
    D.lec(branch.id, '', b.label);
    D.txt(s, b.label, { x: 0.6, y: 0.38, w: 8.8, h: 0.72, fontFace: D.H, fontSize: 30, bold: true, color: D.C.white });
    {
      const lead = D.splitSentences(para(branch.id, 0)).slice(0, 2).join(' ');
      D.ftxt(s, lead, { x: 0.6, y: 1.12, w: 8.8, h: 0.74 }, [16, 15, 14, 13, 12, 11.5], { italic: true, color: D.C.yellow, valign: 'top' }, 'brlead');
    }
    D.branchTree(s, plan, branch, 0.5, 2.0, 9.0, 2.9, 1);
    D.note(s, b.paras.join(' ') + ' This divider is the branch\'s own description from the chapter corpus; the boxes under it name every concept in the branch, so the room can see how far there is to go.');

    branch.subs.forEach(sub => {
      const sc = K[sub.id];
      // sub-branch lead
      s = D.light();
      D.title(s, sc.label, D.splitSentences(para(sub.id, 0))[0]);
      D.lec(sub.id, '', sc.label);
      {
        const body = sc.paras.slice(1).join('\n');
        D.prose(s, body, 0.45, Y_TOP, 4.9, Y_BOT - Y_TOP, 0, [13.5, 13, 12.5, 12, 11.5]);
      }
      D.leafTable(s, plan, sub, 5.6, 1.35, 3.95, 3.6, 1);
      D.footer(s, K[branch.id].label + '  >  ' + sc.label, CITE);
      D.note(s, sc.paras.join(' ') + ' Use this slide to say what the next few slides are for before any of them appears: the table on the right is exactly the concepts that follow, each with the example the chapter uses for it. ' +
        'Click the rows in one at a time if the room is new to the material.');

      // the concepts
      sub.leaves.forEach(leafId => {
        const c = K[leafId];
        const io = CE[leafId];
        const pname = LP[leafId];
        const hook = (hooks.diagrams || {})[leafId];
        // a concept that has both a worked program and an expression example gets two slides, so neither the
        // expression nor the program has to be left off; so does a concept whose program is too long to share one.
        const twoSlides = pname && (longProgram(pname) || !!io);
        // the talk track: why it matters, where it is met, how it works in full (the slide may show only the
        // opening sentences of that paragraph) and what students get wrong - the concept's own paragraphs
        const notes = [para(leafId, 1), para(leafId, 2), para(leafId, 3), para(leafId, 4)].filter(Boolean).join(' ');
        // the concept's own first paragraph, and as much of how-it-works as the box holds at a readable size;
        // fitText does the cutting, always at a sentence boundary, and the whole paragraph stays in the notes.
        const proseText = para(leafId, 0) + '\n' + para(leafId, 3);
        const watch = para(leafId, 4);

        // every concept gets its definition slide in its own words, whatever else it also gets: an executed
        // diagram is shown after the words, never instead of them
        {
          s = D.light();
          D.title(s, c.label, c.definition);
          D.lec(leafId, '', c.label);
          if (pname && !twoSlides) {
            D.prose(s, proseText, 0.45, Y_TOP, 4.35, 2.46, 0, [13, 12.5, 12]);
            D.band(s, 0.45, 3.90, 4.35, 1.08, 'Watch out', watch, D.C.amber, D.C.amberBg, 2);
            D.prog(s, PR, pname, 5.1, Y_TOP, 4.45, 2.26, 1, 11);
            D.trans(s, PR, pname, PR[pname].runs.map((_, i) => i), 5.1, 3.86, 4.45, 1.0, 3, 11);
          } else if (io) {
            const ch = Math.min(1.12, Math.max(0.72, 0.30 + 0.20 * (D.wrapLines('>>> ' + io[0], 2.72, 10, D.M) + D.wrapLines(io[1], 2.72, 10, D.M))));
            D.prose(s, proseText, 0.45, Y_TOP, 5.75, 2.55, 0, [13.5, 13, 12.5, 12]);
            D.band(s, 0.45, 4.02, 5.75, 0.98, 'Watch out', watch, D.C.amber, D.C.amberBg, 2);
            D.codeCard(s, [[io[0], io[1]]], 6.45, Y_TOP + 0.04, 3.1, ch, undefined, 1);
            D.card(s, 6.45, 2.76, 3.1, 2.24, 'Where you meet it', para(leafId, 2), D.C.blue, 3);
          } else {
            D.prose(s, proseText, 0.45, Y_TOP, 9.1, 2.6, 0, [14, 13.5, 13, 12.5, 12]);
            D.band(s, 0.45, 4.02, 9.1, 0.98, 'Watch out', watch, D.C.amber, D.C.amberBg, 1);
          }
          D.footer(s, crumb(leafId), 'example: ' + c.example);
          D.note(s, notes + (io || pname ? SRC : ''));
        }
        if (twoSlides) {
          s = D.light();
          D.title(s, c.label + ': the program, and what it really prints', 'The whole program, and the transcript of running it');
          D.lec(leafId, '', c.label + ': worked example');
          D.prog(s, PR, pname, 0.45, 1.35, 5.5, 3.42, 0, 12);
          D.trans(s, PR, pname, PR[pname].runs.map((_, i) => i), 6.15, 1.35, 3.4, 2.18, 1, 11);
          D.card(s, 6.15, 3.83, 3.4, 1.17, 'What to look at', para(leafId, 3), D.C.green, 2);
          D.footer(s, crumb(leafId), 'real run under Python ' + plan.python);
          D.note(s, para(leafId, 3) + ' ' + para(leafId, 4) + SRC +
            ' Walk the program line by line before clicking the transcript, and ask the room to predict the output; then click and compare.');
        }
        if (hook) {
          // the chapter's own executed diagram takes a whole slide of its own
          s = D.light();
          D.title(s, c.label + ((io || pname) ? ': drawn from a real run' : ''), c.definition);
          D.lec(leafId, leafId, c.label);
          hook(s, D, { x: 0.45, y: Y_TOP, w: 9.1, h: Y_BOT - Y_TOP }, { plan: plan, EX: EX, PR: PR, concept: c, para: i => para(leafId, i), io: io, program: pname });
          D.footer(s, crumb(leafId), 'drawn from a real run under Python ' + plan.python);
          D.note(s, notes + SRC);
        }

      });
    });
  });

  // ---------------------------------------------------------------- recap
  s = D.light();
  D.title(s, 'What you can do now', 'The chapter closed against the objectives it opened with');
  D.lec('', '', 'What you can do now');
  {
    const obs = plan.objectives, h = Math.min(0.72, 3.5 / obs.length);
    obs.forEach(([code, text], i) => {
      const yy = Y_TOP + i * (h + 0.06);
      D.rect(s, { x: 0.45, y: yy, w: 0.95, h: h, fill: D.C.green, lineColor: D.C.green, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.08 }, 'rc', i + 1);
      D.ftxt(s, code, { x: 0.45, y: yy, w: 0.95, h: h }, [16, 14, 12], { fontFace: D.H, bold: true, color: D.C.white, align: 'center' }, 'rcc', i + 1);
      D.ftxt(s, text, { x: 1.6, y: yy, w: 7.95, h: h }, [14, 13.5, 13, 12.5, 12, 11.5], { color: D.C.ink }, 'rct', i + 1);
    });
  }
  D.footer(s, 'Source: ' + plan.objectives_file, CITE);
  D.note(s, 'Close the loop: read each objective again and ask the room, for each one, which slide answered it. ' +
    plan.outcome_note + ' Anything the room cannot answer is what to send them back to the chapter page for before next week.');

  // ---------------------------------------------------------------- questions from the chapter's own bank
  {
    const per = 5;
    for (let i = 0; i < plan.questions.length; i += per) {
      const group = plan.questions.slice(i, i + per);
      s = D.light();
      D.title(s, 'Check yourself' + (plan.questions.length > per ? ' (' + (Math.floor(i / per) + 1) + ' of ' + Math.ceil(plan.questions.length / per) + ')' : ''),
        'Answer aloud first, then click for the answer; the reason for each is in the notes');
      D.lec('', '', 'Check yourself');
      group.forEach((q, j) => {
        const yy = Y_TOP + j * 0.73;
        D.rect(s, { x: 0.45, y: yy + 0.04, w: 0.44, h: 0.44, fill: D.C.yellow, lineColor: D.C.yellow, shape: D.S.OVAL }, 'qn');
        D.txt(s, String(i + j + 1), { x: 0.45, y: yy + 0.04, w: 0.44, h: 0.44, fontFace: D.H, fontSize: 14, bold: true, color: D.C.navy, align: 'center' }, 'qnt');
        D.ftxt(s, q.q, { x: 1.0, y: yy, w: 4.6, h: 0.68 }, [12.5, 12, 11.5, 11, 10.5, 10, 9.5], { color: D.C.ink }, 'qq');
        D.rect(s, { x: 5.75, y: yy + 0.02, w: 3.8, h: 0.64, fill: D.C.greenBg, lineColor: D.C.green, shape: D.S.ROUNDED_RECTANGLE, rectRadius: 0.08 }, 'qa', j + 1);
        D.ftxt(s, q.answer, { x: 5.87, y: yy + 0.02, w: 3.56, h: 0.64 }, [11.5, 11, 10.5, 10, 9.5, 9, 8.5, 8], { bold: true, color: D.C.green }, 'qat', j + 1);
      });
      D.footer(s, 'Drawn from ' + plan.question_bank_file + ', the chapter\'s own question bank', CITE);
      D.note(s, group.map((q, j) => (i + j + 1) + '. ' + q.q + ' The answer is: ' + q.answer + ' ' + q.why).join(' ') +
        ' Let the room answer before each click. The full bank of ' + plan.question_bank_size + ' questions for this chapter, with a reason for every wrong option, is on the chapter page.');
    }
  }

  // ---------------------------------------------------------------- sources
  {
    const primary = plan.sources.filter(x => x[2] === 'primary');
    const rest = plan.sources.filter(x => x[2] !== 'primary');
    const pages = [];
    for (let i = 0; i < rest.length; i += 14) pages.push(rest.slice(i, i + 14));
    pages.forEach((group, pi) => {
      s = D.light();
      D.title(s, 'Sources' + (pages.length > 1 ? ' (' + (pi + 1) + ' of ' + pages.length + ')' : ''),
        'Every source below was opened and verified for this chapter; the record is ' + plan.research_file);
      D.lec('', '', 'Sources');
      const items = (pi === 0 ? primary.concat(group) : group);
      const lineH = Math.min(0.24, 3.3 / items.length);
      items.forEach((r, j) => {
        const yy = Y_TOP + j * lineH;
        D.ftxt(s, r[0], { x: 0.45, y: yy, w: 9.1, h: lineH }, [11, 10.5, 10, 9.5, 9, 8.5, 8, 7.5], { color: r[2] === 'primary' ? D.C.navy : D.C.ink, bold: r[2] === 'primary' }, 'src');
      });
      D.txt(s, 'Slides adapt Automate the Boring Stuff with Python (CC BY-NC-SA). See NOTICE_v1_2.md. Diagrams are drawn from executed specifications.',
        { x: 0.45, y: 4.72, w: 9.1, h: 0.3, fontSize: 9.5, italic: true, color: D.C.mute }, 'lic');
      D.footer(s, 'Research record: 03-materials/ch' + plan.chapter_pad + '/rdodi/' + plan.research_file, CITE);
      D.note(s, 'The full verified list, with the time each page was read, is in 03-materials/ch' + plan.chapter_pad + '/rdodi/' + plan.research_file +
        '. The first entry is the primary source, the chapter itself; the rest are the Python documentation pages and the language proposals that this lecture cites where it goes beyond the book. ' +
        'Tell students that the chapter page\'s own resources tab links every one of them.');
    });
  }

  // ---------------------------------------------------------------- next
  s = D.dark();
  D.lec('', '', plan.next_title);
  D.txt(s, plan.next_title, { x: 0.6, y: 1.5, w: 8.8, h: 0.9, fontFace: D.H, fontSize: 30, bold: true, color: D.C.white });
  D.txt(s, plan.next_body, { x: 0.6, y: 2.5, w: 8.8, h: 1.3, fontSize: 16, color: D.C.yellow, valign: 'top' });
  D.txt(s, 'Questions?', { x: 0.6, y: 4.2, w: 8.8, h: 0.6, fontFace: D.H, fontSize: 24, italic: true, color: 'C9D4E0' });
  D.note(s, plan.next_note);
}

module.exports = { buildLecture, VERSION };
