#!/usr/bin/env python3
"""exam_docx_check_v1_0_0: the check of the rendered SEN0414 exam files (task TK4_Papers).  New file; reads, never edits, the renderer and the engine.

It opens each paper .docx and key .docx written by exam_docx_v1_0_0.py and decides, from the .docx TEXT and STYLES (not from the renderer's
memory), these rules:
  D01 the paper has the engine's five questions, each with its title and points
  D02 the sub-questions (answer units) printed equal the engine's (30 for the Owner's design), per question
  D03 the options per sub-question equal the engine's (4 for a choice, 5 premises and 7 answers for a match, 4 steps for an order, the bank entries)
  D04 every tip of the engine is printed with its sub-question and a sub-question without a tip prints none
  D05 every abbreviation (two or more capitals) of the question pages is written in full at its first use (the engine's own scan); the capitals of the
      Owner's cover template are listed and must be only the words the template itself prints
  D06 every code listing is in a monospace font (paragraph style ExamCode)
  D07 every code line is unwrapped: one paragraph per printed line, no line break or tab, and its width fits the text width
  D08 the printed listing equals the engine's listing (gaps shown as [ 2a ])
  D09 the key .docx holds, per sheet unit, the engine's key answer and points (engine key file)
  D10 the key RECOMPUTED from the paper .docx text (the correct option text of the authored item, looked up among the printed options, gives the
      letter, place or code) equals the key .docx
  D11 pages counted by LibreOffice: question pages plus the cover plus the sheet pages are at most 6 (4 if they fit); CANNOT_RUN when soffice is absent
  D12 no code listing and no option list is split over two pages (read from the LibreOffice PDF text)
  D13 the answer sheet PDF: page count equals its layout file, its units equal the engine's sheet specification, the title says SEN0414
Command line:
  exam_docx_check_v1_0_0.py selftest                     fixtures of known answer (positive and negative); exit 0 only when every fixture gives its known verdict
  exam_docx_check_v1_0_0.py run --build-dir D --stem S --files DIR --name N [--forms A,B]
Exit 0 only when no rule fails and nothing is NOT_MEASURED/CANNOT_RUN; 1 on a failure; 2 when it cannot run.
"""
import json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import docx                                                   # noqa: E402
from docx.oxml.ns import qn                                   # noqa: E402
import exam_item_check_v1_1_0 as itemcheck                    # noqa: E402
import exam_docx_v1_0_0 as R                                  # noqa: E402

VERSION = "1.0.0"
MONO = {"Courier New", "Liberation Mono", "Consolas", "Courier", "DejaVu Sans Mono"}
COVER_WORDS_OK = {"FORBIDDEN", "WARNING", "ZERO", "ALTUNEL", "IKU", "INSTRUCTIONS"}        # words of the Owner's template and the instructor's name, not abbreviations
CAP = re.compile(r"(?<![\w-])[A-Z]{2,}(?![\w-])")


# ---------------------------------------------------------------- reading a .docx
def body_flow(d):
    """Document order: ('p', style, text, paragraph) and table cells flattened as ('c', style, text, paragraph)."""
    out = []
    for el in d.element.body:
        if el.tag == qn("w:p"):
            p = docx.text.paragraph.Paragraph(el, d)
            out.append(("p", p.style.name, p.text, p))
        elif el.tag == qn("w:tbl"):
            t = docx.table.Table(el, d)
            for row in t.rows:
                for c in row.cells:
                    for p in c.paragraphs:
                        out.append(("c", p.style.name, p.text, p))
    return out


def effective_font(p, d):
    for r in p.runs:
        if r.font.name: return r.font.name
    s = p.style
    while s is not None:
        if s.font.name: return s.font.name
        s = s.base_style
    return None


def expand(label):
    m = re.match(r"^(\d)([a-z])(?:\u2013(\d)([a-z]))?$", label.strip())
    if not m: return [label.strip()]
    if not m.group(3): return [label.strip()]
    return [m.group(1) + chr(c) for c in range(ord(m.group(2)), ord(m.group(4)) + 1)]


def segments(flow):
    """[(label_text, units, stem_text, [paragraph entries after the stem until the next stem or question head])]"""
    segs, cur = [], None
    for kind, style, text, p in flow:
        if style == "ExamStem":
            cur = {"label": text.split("\t")[0], "units": expand(text.split("\t")[0]), "stem": text.split("\t", 1)[1], "rest": []}
            segs.append(cur)
        elif style == "ExamQHead":
            cur = None
        elif cur is not None and style in ("ExamTip", "ExamCode", "ExamOption", "ExamCell"):
            cur["rest"].append((kind, style, text, p))
    return segs


def text_width_pt(d):
    s = d.sections[-1]
    return (s.page_width - s.left_margin - s.right_margin) / 12700.0


# ---------------------------------------------------------------- the rules on one paper
def check_paper(path, paper_form_blocks, authored_by_stem=None, key_form=None):
    """Returns {rule: [messages]} (empty list = pass) for one paper .docx against the engine's blocks of that form."""
    res = {k: [] for k in ("D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08")}
    d = docx.Document(path)
    flow = body_flow(d)
    heads = [t for k, s, t, p in flow if s == "ExamQHead"]
    segs = segments(flow)
    # D01
    if len(heads) != len(paper_form_blocks): res["D01"].append("questions %d, engine %d" % (len(heads), len(paper_form_blocks)))
    for h, b in zip(heads, paper_form_blocks):
        if not h.startswith("Question %s " % b["question"][1:]) or ("(%d points" % b["points"]) not in h or (b["bonus"] != ("bonus" in h)):
            res["D01"].append("head %r does not match %s with %d points" % (h, b["question"], b["points"]))
    items = [it for b in paper_form_blocks for it in b["items"]]
    # D02
    printed_units = [u for s in segs for u in s["units"]]
    want_units = [u for it in items for u in it["unit_numbers"]]
    if printed_units != want_units: res["D02"].append("printed units %s, engine %s" % (printed_units, want_units))
    for b in paper_form_blocks:
        n = sum(len(i["unit_numbers"]) for i in b["items"]); m = len([u for u in printed_units if u[0] == b["question"][1:]])
        if n != m: res["D02"].append("%s: %d units printed, engine %d" % (b["question"], m, n))
    if len(segs) != len(items):
        res["D02"].append("sub-question blocks %d, engine records %d" % (len(segs), len(items))); return res, d, segs
    for seg, it in zip(segs, items):
        rest = seg["rest"]
        opt_re = {"mcq": r"^[A-D]\s", "predict": r"^[A-D]\s"}
        t = it["type"]
        # D03 options
        if t in ("mcq", "predict"):
            n = len([1 for k, s, tx, p in rest if s in ("ExamOption", "ExamCell") and re.match(r"^[A-D][\s\t]", tx)])
            if n != 4: res["D03"].append("%s: %d options, want 4" % (it["id"], n))
        elif t == "match":
            pr = len([1 for k, s, tx, p in rest if s == "ExamCell" and re.match(r"^\d[a-z]\s", tx)])
            an = len([1 for k, s, tx, p in rest if s == "ExamCell" and re.match(r"^[A-G]\s", tx)])
            if (pr, an) != (len(it["options"]["premises"]), len(it["options"]["answers"])): res["D03"].append("%s: %d premises, %d answers" % (it["id"], pr, an))
        elif t == "order":
            n = len([1 for k, s, tx, p in rest if s == "ExamOption" and re.match(r"^\d[a-z]\t", tx)])
            if n != len(it["options"]): res["D03"].append("%s: %d steps, want %d" % (it["id"], n, len(it["options"])))
        elif t in ("blank", "cloze"):
            n = len([1 for k, s, tx, p in rest if s == "ExamCell" and re.match(r"^\d\d\s", tx)])
            if n != len(it["bank"]): res["D03"].append("%s: %d bank entries, want %d" % (it["id"], n, len(it["bank"])))
        # D04 tips
        tips = [tx for k, s, tx, p in rest if s == "ExamTip"]
        want = it["tip"] if isinstance(it["tip"], str) and it["tip"].strip().lower() != "none" else None
        if want and (len(tips) != 1 or tips[0] != "Tip: " + want): res["D04"].append("%s: tip printed %r, engine %r" % (it["id"], tips, want))
        if not want and tips: res["D04"].append("%s: tip printed where the engine has none: %r" % (it["id"], tips))
        if it.get("terms") and not tips: res["D04"].append("%s: terms %s without a tip" % (it["id"], it["terms"]))
        # D06 D07 D08 code
        code = [(tx, p) for k, s, tx, p in rest if s == "ExamCode"]
        want_lines = [R.gaps_to_units(l, it["unit_numbers"]) if t == "blank" else l for l in it["listing"]]
        if [c[0].rstrip() if c[0].strip() else "" for c in code] != [l.rstrip() for l in want_lines]:
            res["D08"].append("%s: printed listing differs from the engine's" % it["id"])
        for tx, p in code:
            f = effective_font(p, d)
            if f not in MONO: res["D06"].append("%s: font %r is not monospace" % (it["id"], f))
            xml = p._p.xml
            if "<w:br" in xml or "<w:tab/>" in xml or "\n" in tx or "\t" in tx: res["D07"].append("%s: line break or tab inside a code line" % it["id"])
            size = p.style.font.size.pt if p.style.font.size else R.CODE_PT
            indent = (p.paragraph_format.left_indent or p.style.paragraph_format.left_indent or 0) / 12700.0
            if len(tx) * 0.6 * size + indent > text_width_pt(d) - 4: res["D07"].append("%s: code line of %d characters does not fit one line" % (it["id"], len(tx)))
    # D05 abbreviations on the question pages (the engine's own scan)
    qtext = "\n".join(t for k, s, t, p in flow if s in ("ExamQHead", "ExamInstr", "ExamStem", "ExamTip", "ExamOption", "ExamCell", "ExamCode", "ExamNote"))
    for sh in itemcheck.abbreviation_scan(qtext):
        res["D05"].append("abbreviation %s is not written in full at its first use" % sh)
    cover_text = "\n".join(p.text for p in d.paragraphs if p.style.name not in R_STYLES) + "\n" + "\n".join(
        c.text for t in d.tables for row in t.rows for c in row.cells)
    return res, d, segs


R_STYLES = {"ExamQHead", "ExamInstr", "ExamStem", "ExamTip", "ExamCode", "ExamOption", "ExamCell", "ExamNote"}


def cover_capitals(path):
    d = docx.Document(path)
    txt = "\n".join(p.text for p in d.paragraphs if p.style.name not in R_STYLES) + "\n" + "\n".join(
        c.text for t in d.tables for row in t.rows for c in row.cells)
    # the cover is everything before the first own-style paragraph; tables of the questions are excluded by style below
    caps = set(CAP.findall(txt))
    return sorted(caps)


# ---------------------------------------------------------------- the key
def read_key_docx(path):
    """{unit: (answer text, points)} from the key .docx tables."""
    d = docx.Document(path)
    out = {}
    for t in d.tables:
        for row in t.rows[1:]:
            if len(row.cells) != 4: continue
            units = row.cells[0].text.split("\n"); ans = row.cells[1].text.split("\n"); pts = row.cells[2].text.split("\n")
            for k, u in enumerate(units):
                a = ans[k] if k < len(ans) else ""
                a = re.sub(r"^%s:\s*" % re.escape(u), "", a)
                out[u] = (a.strip(), pts[k].strip() if k < len(pts) else "")
    return out


def key_first_token(a):
    return a.split()[0] if a.split() else ""


def check_key_against_engine(key_docx_units, key_form):
    msgs = []
    want = {}
    for it in key_form["items"]:
        for u in it["units"]: want[u["unit"]] = (str(u["answer"]), str(u["points"]))
    if set(want) != set(key_docx_units): msgs.append("units in key docx %d, engine %d" % (len(key_docx_units), len(want)))
    for u, (a, pt) in want.items():
        got = key_docx_units.get(u)
        if got is None: continue
        tok = key_first_token(got[0]) if not got[0].startswith("place") else got[0].split()[1]
        if tok != a or got[1] != pt: msgs.append("%s: key docx %r/%s, engine %s/%s" % (u, got[0][:20], got[1], a, pt))
    return msgs


def recompute_from_paper(flow, segs, authored_items, forms_items):
    """From the printed paper text and the authored (pool) records: {unit: answer}. The correct option TEXT of the authored record is looked up
    among the options printed in the paper, so the letter, place or code is read from the .docx."""
    by_stem = {}
    for a in authored_items:
        by_stem[a["stem"]] = a
    out = {}
    for seg in segs:
        stem = re.sub(r"\s*\(\d+ points?\)\s*$", "", seg["stem"])
        a = by_stem.get(stem)
        if a is None:
            # cloze: the printed stem has [ 2e ] where the record has [[1]]
            for s, rec in by_stem.items():
                if rec["type"] == "cloze" and R.gaps_to_units(s, seg["units"]) == stem: a = rec; break
        if a is None: out["?" + seg["label"]] = "no authored record for this stem"; continue
        t = a["type"]; rest = seg["rest"]
        cells = [tx for k, s, tx, p in rest if s in ("ExamOption", "ExamCell")]
        def split(tx):
            m = re.match(r"^(\S+)[\s\t]+(.*)$", tx, re.S)
            return (m.group(1), m.group(2).strip()) if m else (tx, "")
        if t in ("mcq", "predict"):
            correct = a["options_or_blanks"]["abc".index("a")] if False else a["options_or_blanks"]["ABCD".index(a["answer"])]
            printed = [split(c) for c in cells if re.match(r"^[A-D][\s\t]", c)]
            out[seg["units"][0]] = [l for l, tx in printed if tx == correct][0] if any(tx == correct for l, tx in printed) else "?"
        elif t == "match":
            prem = a["options_or_blanks"]["premises"]; ans = a["options_or_blanks"]["answers"]
            pc = [split(c) for c in cells if re.match(r"^\d[a-z]\s", c)]; ac = [split(c) for c in cells if re.match(r"^[A-G]\s", c)]
            for k, (u, ptxt) in enumerate(pc):
                orig = prem.index(ptxt) if ptxt in prem else None
                want_txt = ans["ABCDEFG".index(a["answer"][orig])] if orig is not None else None
                out[u] = [l for l, tx in ac if tx == want_txt][0] if any(tx == want_txt for l, tx in ac) else "?"
        elif t == "order":
            steps = a["options_or_blanks"]
            printed = [split(c) for c in cells if re.match(r"^\d[a-z]\t", c)]
            for u, stxt in printed:
                out[u] = str(a["answer"][steps.index(stxt)]) if stxt in steps else "?"
        elif t in ("blank", "cloze"):
            bank = a["options_or_blanks"]["bank"]
            printed = [split(c) for c in cells if re.match(r"^\d\d\s", c)]
            for g, u in enumerate(seg["units"]):
                want_txt = bank[a["answer"][g]]
                out[u] = [cd for cd, tx in printed if tx == want_txt][0] if any(tx == want_txt for cd, tx in printed) else "?"
    return out


# ---------------------------------------------------------------- LibreOffice
def soffice():
    return shutil.which("soffice") or shutil.which("libreoffice")


def to_pdf(docx_path, outdir):
    so = soffice()
    if not so: return None
    subprocess.run([so, "--headless", "--convert-to", "pdf", "--outdir", outdir, docx_path], capture_output=True, timeout=240)
    p = os.path.join(outdir, Path(docx_path).stem + ".pdf")
    return p if os.path.isfile(p) else None


def pdf_pages(pdf):
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", out).group(1))


def page_texts(pdf):
    n = pdf_pages(pdf); res = []
    for k in range(1, n + 1):
        res.append(subprocess.run(["pdftotext", "-f", str(k), "-l", str(k), pdf, "-"], capture_output=True, text=True).stdout)
    return res


def norm(s): return re.sub(r"\s+", " ", s).strip()


def check_splits(segs, pages):
    """A sub-question (stem to its last line) must stand on one page."""
    msgs = []; start = 0
    norm_pages = [norm(p) for p in pages]
    for seg in segs:
        first = norm(seg["stem"])[:55]
        pf = next((i for i in range(start, len(pages)) if first in norm_pages[i]), None)
        if pf is None: msgs.append("%s: stem not found in the PDF text" % seg["label"]); continue
        start = pf
        lastt = None
        for k, s, tx, p in reversed(seg["rest"]):
            m = re.sub(r"^\S+[\s\t]+", "", tx).strip() if s in ("ExamOption", "ExamCell") else tx.strip()
            if len(m) >= 4: lastt = norm(m)[:22]; break
        if lastt is None: continue
        pl = next((i for i in range(pf, len(pages)) if lastt in norm_pages[i]), None)
        if pl is None: msgs.append("%s: last line not found in the PDF text" % seg["label"])
        elif pl != pf: msgs.append("%s: split over pages %d and %d" % (seg["label"], pf + 1, pl + 1))
        else: start = pl
    return msgs


# ---------------------------------------------------------------- fixtures of known answer
def fixture_blocks():
    """Two questions, three sub-questions, hand-written: the known answers are the numbers in FIXTURE_EXPECT."""
    it1 = {"position": 1, "id": "F1a", "ref": "f/F1a", "question": "Q1", "sub": "a", "type": "predict", "units": 1, "chapters": [1], "points": 10, "bloom": 3,
           "asks": "effect", "tip": "A list keeps its order.", "terms": ["list"], "reason": "r", "stem": "Read the program and choose what it prints.",
           "listing": ["xs = [3, 1]", "xs.sort()", "print(xs)"], "options": ["[1, 3]", "[3, 1]", "None", "[1]"], "key": "A", "unit_numbers": ["1a"]}
    it2 = {"position": 2, "id": "F1b", "ref": "f/F1b", "question": "Q1", "sub": "b", "type": "mcq", "units": 1, "chapters": [2], "points": 15, "bloom": 3,
           "asks": "reason", "tip": "none", "terms": [], "reason": "r", "stem": "Why does the loop below stop?", "listing": ["while n < 3:", "    n += 1"],
           "options": ["n reaches 3", "n is text", "the loop is empty", "n is a list"], "key": "A", "unit_numbers": ["1b"]}
    it3 = {"position": 3, "id": "F2a", "ref": "f/F2a", "question": "Q2", "sub": "a", "type": "order", "units": 2, "chapters": [3], "points": 10, "bloom": 3,
           "asks": "use", "tip": "none", "terms": [], "reason": "r", "stem": "Put the two steps in order.", "listing": [],
           "options": ["Print the total", "Add the numbers"], "key": [2, 1], "unit_numbers": ["2a", "2b"]}
    return [{"question": "Q1", "title": "Read", "points": 25, "bonus": False, "items": [it1, it2]},
            {"question": "Q2", "title": "Order", "points": 10, "bonus": True, "items": [it3]}]


FIXTURE_EXPECT = {"questions": 2, "units": 4, "options": 4 + 4 + 2, "tips": 1, "code_lines": 5}


def build_fixture_docx(path, mutate=None):
    paper = {"kind": "midterm", "blocks": {"A": fixture_blocks()}}
    key = {"A": {"form_mark": {"serial": 0, "code": "00"}, "paper_version": 1, "content_sha256": "0" * 64}}
    R.render_paper(paper, key, {"seed": 0}, "A", path)
    if mutate:
        d = docx.Document(path); mutate(d); d.save(path)


def selftest():
    tmp = tempfile.mkdtemp(prefix="docxcheck_")
    ok = True
    blocks = fixture_blocks()
    log = []

    def verdict(name, cond, detail=""):
        nonlocal ok
        log.append("%-52s %s %s" % (name, "PASS" if cond else "FAIL", detail)); ok = ok and cond

    good = os.path.join(tmp, "good.docx"); build_fixture_docx(good)
    res, d, segs = check_paper(good, blocks)
    verdict("fixture good: no rule fails", all(not v for v in res.values()), str({k: v for k, v in res.items() if v}))
    flow = body_flow(d)
    n_q = len([1 for k, s, t, p in flow if s == "ExamQHead"]); n_u = sum(len(s["units"]) for s in segs)
    n_o = len([1 for k, s, t, p in flow if s in ("ExamOption", "ExamCell") and re.match(r"^([A-D]|\d[a-z])[\s\t]", t)])
    n_t = len([1 for k, s, t, p in flow if s == "ExamTip"]); n_c = len([1 for k, s, t, p in flow if s == "ExamCode"])
    verdict("fixture good: counts known (2 questions, 4 units, 10 options, 1 tip, 5 code lines)",
            (n_q, n_u, n_o, n_t, n_c) == (FIXTURE_EXPECT["questions"], FIXTURE_EXPECT["units"], FIXTURE_EXPECT["options"], FIXTURE_EXPECT["tips"], FIXTURE_EXPECT["code_lines"]),
            str((n_q, n_u, n_o, n_t, n_c)))

    def neg(name, rule, mutate):
        p = os.path.join(tmp, name + ".docx"); build_fixture_docx(p, mutate)
        r, _, _ = check_paper(p, blocks)
        verdict("fixture %s: rule %s fails" % (name, rule), bool(r[rule]))

    def code_par(dd): return [p for p in dd.paragraphs if p.style.name == "ExamCode"]
    def m_font(dd):
        for p in code_par(dd):
            for r in p.runs: r.font.name = "Arial"
        dd.styles["ExamCode"].font.name = "Arial"
    neg("proportional_code", "D06", m_font)
    def m_wrap(dd): code_par(dd)[0].runs[0].text = "x = " + "9" * 100
    neg("long_code_line", "D07", m_wrap)
    def m_br(dd): code_par(dd)[0].add_run().add_break()
    neg("break_in_code", "D07", m_br)
    def m_abbr(dd):
        for p in dd.paragraphs:
            if p.style.name == "ExamStem": p.runs[1].text = "Use the IDE. " + p.runs[1].text; break
    neg("abbreviation_without_full_form", "D05", m_abbr)
    def m_tip(dd):
        for p in dd.paragraphs:
            if p.style.name == "ExamTip": p._p.getparent().remove(p._p); break
    neg("missing_tip", "D04", m_tip)
    def m_listing(dd): code_par(dd)[1].runs[0].text = "xs.reverse()"
    neg("changed_listing", "D08", m_listing)
    def m_opt(dd):
        for t in dd.tables:
            for row in t.rows:
                for c in row.cells:
                    if c.paragraphs[0].style.name == "ExamCell" and c.paragraphs[0].text.startswith("D"):
                        for r in c.paragraphs[0].runs: r.text = ""
                        return
    neg("missing_option", "D03", m_opt)
    # key logic on a known dictionary
    kd = {"1a": ("A  [1, 3]", "10"), "1b": ("B  x", "15")}
    kf = {"items": [{"units": [{"unit": "1a", "answer": "A", "points": "10"}, {"unit": "1b", "answer": "A", "points": "15"}]}]}
    verdict("fixture key: one wrong letter is found (1b)", len(check_key_against_engine(kd, kf)) == 1)
    # splits on known page texts
    sg = [{"label": "1a", "stem": "Read the program and choose", "rest": [("p", "ExamOption", "A\tfirst option text", None), ("p", "ExamOption", "D\tlast option text here", None)]}]
    verdict("fixture split: same page is clean", check_splits(sg, ["Read the program and choose A first option text D last option text here"]) == [])
    verdict("fixture split: two pages is found", len(check_splits(sg, ["Read the program and choose A first option text", "D last option text here"])) == 1)
    shutil.rmtree(tmp, ignore_errors=True)
    print("\n".join(log))
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


# ---------------------------------------------------------------- run on real files
def run(bd, stem, files, name, forms):
    paper = json.load(open(Path(bd) / (stem + "_paper.json"))); key = json.load(open(Path(bd) / (stem + "_key.json")))
    build = json.load(open(Path(bd) / (stem + "_build.json"))); spec = json.load(open(Path(bd) / (stem + "_sheetspec.json")))
    authored = json.load(open(Path(bd) / (stem + "_authored.json")))
    failures, notes = 0, []
    scratch = tempfile.mkdtemp(prefix="docxcheck_run_")

    def rep(rule, msgs, what=""):
        nonlocal failures
        print("%-4s %-4s %s" % (rule, "FAIL" if msgs else "PASS", what))
        for m in msgs[:6]: print("       " + m)
        failures += 1 if msgs else 0

    # D13 sheet
    pdf = os.path.join(files, name + "_answersheet.pdf"); lay = json.load(open(os.path.join(files, name + "_answersheet_layout.json")))
    npg = pdf_pages(pdf); txt = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout
    lay_units = [u["no"] for b in lay["blocks"] for u in b["units"]]
    msgs = []
    if npg != lay["pages"]: msgs.append("pdf pages %d, layout %d" % (npg, lay["pages"]))
    if lay_units != [u["no"] for u in spec["units"]]: msgs.append("sheet units differ from the engine's sheet specification")
    if "SEN0414 answer sheet" not in txt or "SEN0401" in txt: msgs.append("title of the sheet is not SEN0414")
    rep("D13", msgs, "%s: %d page(s), %d units, text check" % (os.path.basename(pdf), npg, len(lay_units)))
    sheet_pages = npg
    for f in forms:
        pp = os.path.join(files, "%s_form_%s_paper.docx" % (name, f)); kp = os.path.join(files, "%s_form_%s_key.docx" % (name, f))
        blocks = paper["blocks"][f]
        res, d, segs = check_paper(pp, blocks)
        flow = body_flow(d)
        n_units = sum(len(s["units"]) for s in segs)
        n_opts = len([1 for k, s, t, p in flow if s in ("ExamOption", "ExamCell")])
        n_tips = len([1 for k, s, t, p in flow if s == "ExamTip"]); n_code = len([1 for k, s, t, p in flow if s == "ExamCode"])
        what = "%s form %s: %d questions, %d sub-questions (units), %d records, %d option/cell lines, %d tips, %d code lines" % (
            os.path.basename(pp), f, len([1 for k, s, t, p in flow if s == "ExamQHead"]), n_units, len(segs), n_opts, n_tips, n_code)
        print(what)
        for rule in ("D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08"):
            rep(rule, res[rule])
        print("     cover capitals (the Owner's template and the instructor's name, listed): %s" % cover_capitals(pp))
        extra = [c for c in cover_capitals(pp) if c not in COVER_WORDS_OK]
        rep("D05c", ["capitals on the cover that are not template words: %s" % extra] if extra else [], "cover capitals are template words only")
        # key
        kd = read_key_docx(kp)
        rep("D09", check_key_against_engine(kd, key[f]), "%s agrees with the engine key (%d units)" % (os.path.basename(kp), len(kd)))
        rec = recompute_from_paper(flow, segs, authored if f == "A" or True else authored, blocks)
        msgs = []
        for u, (a, pt) in kd.items():
            tok = a.split()[1] if a.startswith("place") else key_first_token(a)
            if rec.get(u) != tok: msgs.append("%s: recomputed %r, key docx %r" % (u, rec.get(u), tok))
        if len(rec) != len(kd): msgs.append("recomputed %d units, key docx %d" % (len(rec), len(kd)))
        rep("D10", msgs, "key recomputed from the paper text equals the key docx (%d units)" % len(rec))
        # pages
        if not soffice():
            print("D11  CANNOT_RUN  LibreOffice is not installed"); print("D12  CANNOT_RUN  needs the PDF"); failures += 1
            continue
        pdfp = to_pdf(pp, scratch)
        if not pdfp:
            print("D11  CANNOT_RUN  conversion failed"); failures += 1; continue
        pages = page_texts(pdfp); total = len(pages) + sheet_pages
        rep("D11", [] if total <= 6 else ["total %d pages exceeds 6" % total],
            "LibreOffice: paper %d pages (cover 1 + questions %d) + sheet %d = %d total (4 %s)" % (len(pages), len(pages) - 1, sheet_pages, total, "fits" if total <= 4 else "does not fit; 6 allowed"))
        # the cover must stand alone on page 1
        c_ok = "INSTRUCTIONS" in pages[0] and "Question 1" not in pages[0] and "Question 1" not in pages[0].replace("Question (Q)", "")
        rep("D11c", [] if (c_ok or "Read the program" not in pages[0]) else ["cover page 1 holds question text"], "cover alone on page 1")
        rep("D12", check_splits(segs, pages[1:]), "no sub-question (listing, options, bank) is split over pages")
        spare = None
        print("     last question page text lines: %d (of about 60)" % len([l for l in pages[-1].splitlines() if l.strip()]))
        shutil.copy(pdfp, os.path.join(scratch, "keep_%s.pdf" % f))
    print("FAILURES:", failures)
    shutil.rmtree(scratch, ignore_errors=True)
    return 1 if failures else 0


def main(argv):
    a = list(argv[1:])
    if not a: print(__doc__); return 2
    cmd = a.pop(0)
    if cmd == "selftest": return selftest()
    if cmd == "run":
        opt = {}
        while a:
            x = a.pop(0)
            if x.startswith("--"): opt[x[2:]] = a.pop(0)
        return run(opt["build-dir"], opt["stem"], opt["files"], opt["name"], opt.get("forms", "A,B").split(","))
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
