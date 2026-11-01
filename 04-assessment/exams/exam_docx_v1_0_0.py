#!/usr/bin/env python3
"""exam_docx_v1_0_0: renders one build of the SEN0414 exam engine (exam_engine_v1_1_0.py) as editable .docx files and the answer sheet PDF
(task TK4_Papers).  New file; nothing committed is edited.

For one paper (midterm or make-up) and one form (A or B) it writes
    PAPER  <stem>_form_<X>_paper.docx   cover page (exam_cover_v1_0_0.py, the Owner's template, reused unchanged) + five questions
    KEY    <stem>_form_<X>_key.docx     answer, points, reason, tip and chapters of every sub-question (for the instructor, never for students)
and once per build
    SHEET  <stem>_answersheet.pdf (+ _layout.json)  position-exact PDF made by the SEN0401 sheet module
           (/home/claude/sen0401/08-tooling/exam/sen0401_exam_answersheet_v1_0_0.py), IMPORTED and never edited.  The module prints the words
           'SEN0401' in its title; this renderer loads its own copy of the module and swaps that word for 'SEN0414' in the strings it draws
           (the module file stays byte-identical; the reader looks at bubbles and corner marks only, not at text).
An editable .docx copy of the sheet is NOT built (the reader needs exact bubble positions).

Readability rules built in: body text Arial 10 point, code Courier New 10 point in shaded paragraphs of the style ExamCode (monospace, one
printed line per paragraph, no wrapping: the line length is checked against the text width), every term that has a tip is printed with its
tip (style ExamTip), each sub-question is kept together with keep-with-next so that a listing or an option list never breaks across pages,
gaps of a program or an explanation are printed as [ 2a ] with the number of their row on the answer sheet.

Command line:
  exam_docx_v1_0_0.py render --build-dir DIR --stem NAME --out DIR [--date 'text'] [--forms A,B]
        DIR holds NAME_paper.json, NAME_key.json, NAME_sheetspec.json, NAME_build.json written by exam_engine_v1_1_0.py build.
        --date is printed on the cover as given; without it the cover keeps its marked fill-in line (the Owner has not given the date).
Exit 0 when every file was written, 2 when it cannot run.
"""
import copy, importlib.util, json, os, re, sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import docx                                                   # noqa: E402
from docx.enum.text import WD_BREAK                           # noqa: E402
from docx.enum.style import WD_STYLE_TYPE                     # noqa: E402
from docx.oxml import OxmlElement                             # noqa: E402
from docx.oxml.ns import qn                                   # noqa: E402
from docx.shared import Pt, Mm, Emu                           # noqa: E402
import exam_cover_v1_0_0 as cover_mod                         # noqa: E402

VERSION = "1.0.0"
SHEET_DIR = Path(os.environ.get("SEN0401_EXAM_DIR", "/home/claude/sen0401/08-tooling/exam"))
SHEET_FILE = "sen0401_exam_answersheet_v1_0_0.py"
BODY_FONT, CODE_FONT = "Arial", "Courier New"
BODY_PT, CODE_PT, TIP_PT, SMALL_PT = 10, 10, 9.5, 9.5
MARG_LR_MM, MARG_TB_MM = 15, 13
TEXT_WIDTH_PT = (210 - 2 * MARG_LR_MM) * 72 / 25.4
LETTERS = "ABCDEFG"
# learning outcomes that the materials file attaches to chapters (see exam_cover_v1_0_0.py); chapters without an entry add none
CHAPTER_OUTCOMES = {1: [1, 4], 5: [6], 8: [2]}


# ---------------------------------------------------------------- low-level helpers
def set_fonts(rpr_owner_style_or_run, name):
    rpr = rpr_owner_style_or_run
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts"); rpr.insert(0, rfonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(a), name)


def shade(ppr_el, fill):
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), fill)
    ppr_el.append(shd)


def box(ppr_el, sides=("top", "left", "bottom", "right"), sz=4, color="808080", space=2):
    b = OxmlElement("w:pBdr")
    for s in ("top", "left", "bottom", "right"):
        if s in sides:
            e = OxmlElement("w:" + s); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(sz)); e.set(qn("w:space"), str(space)); e.set(qn("w:color"), color)
            b.append(e)
    ppr_el.append(b)


def make_styles(doc):
    """Own paragraph styles (names are used by the check): ExamQHead, ExamInstr, ExamStem, ExamTip, ExamCode, ExamOption, ExamCell, ExamNote."""
    st = doc.styles

    def add(name, size, bold=False, italic=False, font=BODY_FONT, before=0, after=0, left=0, first=0, keep_next=True, line=None):
        s = st.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        s.base_style = st["Normal"]
        s.font.name = font; s.font.size = Pt(size); s.font.bold = bold; s.font.italic = italic
        set_fonts(s.element.get_or_add_rPr(), font)
        pf = s.paragraph_format
        pf.space_before = Pt(before); pf.space_after = Pt(after); pf.left_indent = Mm(left); pf.first_line_indent = Mm(first)
        pf.keep_with_next = keep_next; pf.keep_together = True; pf.widow_control = True
        pf.line_spacing = line if line else 1.0
        return s
    add("ExamQHead", 11.5, bold=True, before=7, after=2)
    add("ExamInstr", SMALL_PT, italic=True, after=3)
    add("ExamStem", BODY_PT, before=5, after=1, left=14, first=-14)
    add("ExamTip", TIP_PT, italic=True, after=2, left=14)
    add("ExamCode", CODE_PT, font=CODE_FONT, left=14, line=1.0)
    add("ExamOption", BODY_PT, left=20, first=-6, after=0.5)
    add("ExamCell", BODY_PT, keep_next=True)
    add("ExamNote", SMALL_PT, after=2)
    return doc


def add_par(doc, text="", style="ExamNote", keep_next=None, runs=None, align=None):
    p = doc.add_paragraph(style=style)
    if runs is None:
        runs = [(text, {})]
    for t, f in runs:
        r = p.add_run(t)
        if f.get("b"): r.bold = True
        if f.get("i"): r.italic = True
        if f.get("mono"):
            r.font.name = CODE_FONT; set_fonts(r._r.get_or_add_rPr(), CODE_FONT)
        if f.get("size"): r.font.size = Pt(f["size"])
    if keep_next is not None:
        p.paragraph_format.keep_with_next = keep_next
    if align:
        p.alignment = align
    return p


def no_borders_table(doc, rows, cols, widths_mm):
    t = doc.add_table(rows=rows, cols=cols)
    tblPr = t._tbl.tblPr
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr()
        cs = OxmlElement("w:cantSplit"); trPr.append(cs)
        for c, w in zip(row.cells, widths_mm):
            c.width = Mm(w)
    return t


def cell_text(cell, runs, style="ExamCell", keep_next=True):
    p = cell.paragraphs[0]
    p.style = cell.part.document.styles[style] if hasattr(cell.part, "document") else p.style
    for t, f in runs:
        r = p.add_run(t)
        if f.get("b"): r.bold = True
        if f.get("mono"):
            r.font.name = CODE_FONT; set_fonts(r._r.get_or_add_rPr(), CODE_FONT)
    p.paragraph_format.keep_with_next = keep_next
    return p


def add_field(par, instr):
    r = par.add_run()
    for kind, txt in (("begin", None), (None, instr), ("end", None)):
        if kind:
            e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), kind); r._r.append(e)
        else:
            e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt; r._r.append(e)


# ---------------------------------------------------------------- content helpers
def gaps_to_units(text, unit_numbers):
    """[[n]] -> [ 2a ]: the number of the row of the answer sheet that takes this gap."""
    def sub(m):
        k = int(m.group(1)) - 1
        return "[ %s ]" % (unit_numbers[k] if k < len(unit_numbers) else "?")
    return re.sub(r"\[\[(\d+)\]\]", sub, text)


def unit_span(nums):
    return nums[0] if len(nums) == 1 else "%s–%s" % (nums[0], nums[-1])


def points_text(it, bonus):
    return "%d point%s" % (it["points"], "" if it["points"] == 1 else "s")


def question_outcomes(block):
    s = set()
    for it in block["items"]:
        for c in it["chapters"]:
            s.update(CHAPTER_OUTCOMES.get(c, []))
    return sorted(s)


def group_instruction(block):
    """Student-facing instruction per kind of answer, with the sub-questions it covers (built from the items, so it follows any pool)."""
    groups = {}
    for it in block["items"]:
        cls = {"mcq": "choice", "predict": "choice", "blank": "bank", "cloze": "bank", "match": "match", "order": "order"}[it["type"]]
        groups.setdefault(cls, []).extend(it["unit_numbers"])
    text = {
        "choice": "choose one option (A to D) and fill its bubble in the row with the same number on the answer sheet.",
        "bank": "choose the entry of the bank that fits each gap and fill the two-digit code printed before it on the answer sheet (one bubble in the upper row, one in the lower row).",
        "match": "fill the letter of the answer that fits each situation, in the row of that situation. Not every answer is used.",
        "order": "fill the place (1 to 4) at which each step runs, in the row of that step.",
    }
    out = []
    for cls, nums in groups.items():
        out.append("%s: %s" % (unit_span(nums) if len(groups) > 1 or len(nums) > 1 else nums[0], text[cls]))
    return "  ".join(("Sub-questions " + o) if len(groups) > 1 else ("Sub-questions " + o) for o in out)


# ---------------------------------------------------------------- the paper
def render_item(doc, it):
    nums = it["unit_numbers"]
    t = it["type"]
    stem = gaps_to_units(it["stem"], nums) if t == "cloze" else it["stem"]
    # stem paragraph: label, text, points
    p = doc.add_paragraph(style="ExamStem")
    r = p.add_run(unit_span(nums) + "\t"); r.bold = True
    p.add_run(stem + " ")
    r = p.add_run("(%s)" % points_text(it, False)); r.bold = True
    # a tab stop at the hanging indent
    tabs = OxmlElement("w:tabs"); tb = OxmlElement("w:tab"); tb.set(qn("w:val"), "left"); tb.set(qn("w:pos"), str(int(Mm(14).emu / 635))); tabs.append(tb)
    p._p.get_or_add_pPr().append(tabs)
    tip = it.get("tip")
    if isinstance(tip, str) and tip.strip() and tip.strip().lower() != "none":
        add_par(doc, "", style="ExamTip", runs=[("Tip: ", {"b": True, "i": True}), (tip, {"i": True})])
    if it["listing"]:
        lines = [gaps_to_units(l, nums) if t == "blank" else l for l in it["listing"]]
        for k, line in enumerate(lines):
            cp = doc.add_paragraph(style="ExamCode")
            cp.add_run(line if line else " ")
            ppr = cp._p.get_or_add_pPr()
            box(ppr, sides=("left", "right") + (("top",) if k == 0 else ()) + (("bottom",) if k == len(lines) - 1 else ()), color="999999")
            shade(ppr, "F2F2F2")
            cp.paragraph_format.keep_with_next = True
            if k == len(lines) - 1: cp.paragraph_format.space_after = Pt(3)
        # a thin spacer keeps the box from touching the options
    if t in ("mcq", "predict"):
        opts = it["options"]
        short = max(len(o) for o in opts) <= 24
        if short:
            tbl = no_borders_table(doc, 2, 2, [45, 45])
            tbl.alignment = 0
            for k, o in enumerate(opts):
                c = tbl.rows[k // 2].cells[k % 2]
                cp = cell_text(c, [(LETTERS[k] + "  ", {"b": True}), (o, {"mono": t == "predict"})], style="ExamCell",
                               keep_next=(k // 2 == 0) or True)
                cp.paragraph_format.left_indent = Mm(14)
            # the last row must not keep with the following sub-question
            for c in tbl.rows[1].cells:
                c.paragraphs[0].paragraph_format.keep_with_next = False
        else:
            for k, o in enumerate(opts):
                cp = add_par(doc, "", style="ExamOption", runs=[(LETTERS[k] + "\t", {"b": True}), (o, {})], keep_next=(k < len(opts) - 1))
                tabs = OxmlElement("w:tabs"); tb = OxmlElement("w:tab"); tb.set(qn("w:val"), "left"); tb.set(qn("w:pos"), str(int(Mm(20).emu / 635))); tabs.append(tb)
                cp._p.get_or_add_pPr().append(tabs)
    elif t in ("blank", "cloze"):
        bank, codes = it["bank"], it["bank_codes"]
        ncol = 4
        nrow = (len(bank) + ncol - 1) // ncol
        w = (TEXT_WIDTH_PT * 25.4 / 72 - 8) / ncol
        tbl = no_borders_table(doc, nrow, ncol, [w] * ncol)
        for k, (code, entry) in enumerate(zip(codes, bank)):
            c = tbl.rows[k // ncol].cells[k % ncol]
            cp = cell_text(c, [(code + "  ", {"b": True}), (entry, {"mono": t == "blank"})], keep_next=(k // ncol < nrow - 1))
            cp.paragraph_format.left_indent = Mm(8)
        for k in range(len(bank), nrow * ncol):
            tbl.rows[k // ncol].cells[k % ncol].paragraphs[0].paragraph_format.keep_with_next = (k // ncol < nrow - 1)
    elif t == "match":
        prem, ans = it["options"]["premises"], it["options"]["answers"]
        n = max(len(prem), len(ans))
        tbl = no_borders_table(doc, n, 2, [92, 88])
        for k in range(n):
            if k < len(prem):
                cp = cell_text(tbl.rows[k].cells[0], [(nums[k] + "  ", {"b": True}), (prem[k], {})], keep_next=(k < n - 1))
                cp.paragraph_format.left_indent = Mm(14); cp.paragraph_format.first_line_indent = Mm(-9)
            if k < len(ans):
                cp = cell_text(tbl.rows[k].cells[1], [(LETTERS[k] + "  ", {"b": True}), (ans[k], {})], keep_next=(k < n - 1))
                cp.paragraph_format.left_indent = Mm(8); cp.paragraph_format.first_line_indent = Mm(-6)
    elif t == "order":
        steps = it["options"]
        for k, s in enumerate(steps):
            cp = add_par(doc, "", style="ExamOption", runs=[(nums[k] + "\t", {"b": True}), (s, {})], keep_next=(k < len(steps) - 1))
            tabs = OxmlElement("w:tabs"); tb = OxmlElement("w:tab"); tb.set(qn("w:val"), "left"); tb.set(qn("w:pos"), str(int(Mm(20).emu / 635))); tabs.append(tb)
            cp._p.get_or_add_pPr().append(tabs)
    else:
        raise ValueError("unknown item type %r" % t)
    # the last paragraph of the sub-question may be followed by a page break
    last = doc.paragraphs[-1] if doc.element.body[-2].tag == qn("w:p") else None
    if last is not None:
        last.paragraph_format.keep_with_next = False


def new_body_section(doc):
    """The cover is its own section (cover(own_section=True)); this sets the page of the questions: A4, own margins, footer with the page number."""
    sec = doc.sections[-1]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(MARG_LR_MM)
    sec.top_margin = sec.bottom_margin = Mm(MARG_TB_MM)
    sec.header_distance = Mm(6); sec.footer_distance = Mm(6)
    return sec


def footer_text(sec, text):
    sec.footer.is_linked_to_previous = False
    p = sec.footer.paragraphs[0]
    for r in list(p.runs): r._r.getparent().remove(r._r)
    r = p.add_run(text + " – page "); r.font.size = Pt(8.5); r.font.name = BODY_FONT
    add_field(p, "PAGE")
    for r in p.runs: r.font.size = Pt(8.5)
    p.alignment = 1


def render_paper(paper, key, build, form, out_path, date_text=None):
    kind = paper["kind"]
    d = cover_mod.new_document()
    questions = [(b["question"][1:], b["points"], b["bonus"]) for b in paper["blocks"][form]]
    outs = [question_outcomes(b) for b in paper["blocks"][form]]
    titles = {"midterm": "Midterm Exam", "makeup": "Make-up Exam"}
    cover_mod.cover(d, "SEN0414", "Advanced Programming", "%s - Form %s" % (titles[kind], form), "Fall", "2026-2027", date_text, "60 Minutes",
                    "Dr. Yusuf ALTUNEL", questions, outs, instructions=cover_mod.instructions_sen0414(), outcomes_ttl=cover_mod.OUTCOMES_TTL,
                    own_section=True)
    make_styles(d)
    sec = new_body_section(d)
    fm = key[form]["form_mark"]
    label = "SEN0414 %s – Form %s" % (titles[kind], form)
    footer_text(sec, label)
    p = add_par(d, "", style="ExamNote", runs=[
        ("%s, Form %s. " % (titles[kind], form), {"b": True}),
        ("On the answer sheet, in the row F, fill the code ", {}), (fm["code"], {"b": True}),
        (" (this is the mark of Form %s). Question 5 is a bonus." % form, {})], keep_next=False)
    p.paragraph_format.space_after = Pt(0)
    for b in paper["blocks"][form]:
        hp = d.add_paragraph(style="ExamQHead")
        ppr = hp._p.get_or_add_pPr(); box(ppr, sides=("top", "bottom"), sz=6, color="404040", space=1); shade(ppr, "E4E4E4")
        hp.add_run("Question %s – %s" % (b["question"][1:], b["title"]))
        hp.add_run("   (%d points%s)" % (b["points"], ", bonus" if b["bonus"] else ""))
        add_par(d, group_instruction(b), style="ExamInstr", keep_next=True)
        for it in b["items"]:
            render_item(d, it)
    # the body ends with a plain closing paragraph so that no empty page follows
    add_par(d, "End of the questions.", style="ExamNote", keep_next=False)
    d.core_properties.title = "SEN0414 %s Form %s paper" % (titles[kind], form)
    d.core_properties.author = ""
    d.save(out_path)
    return out_path


# ---------------------------------------------------------------- the key
def answer_text(it_paper, unit_idx, unit, kind):
    """Human text of one answer: letter and the option text, code and the bank entry, place and the step."""
    a = unit["answer"]
    t = it_paper["type"]
    if t in ("mcq", "predict"):
        return "%s  %s" % (a, it_paper["options"][LETTERS.index(a)])
    if t == "match":
        return "%s  %s" % (a, it_paper["options"]["answers"][LETTERS.index(a)])
    if t in ("blank", "cloze"):
        return "%s  %s" % (a, it_paper["bank"][it_paper["bank_codes"].index(a)])
    if t == "order":
        return "place %s  –  %s" % (a, it_paper["options"][unit_idx])
    return a


def render_key(paper, key, build, form, out_path):
    kind = paper["kind"]
    titles = {"midterm": "Midterm Exam", "makeup": "Make-up Exam"}
    d = cover_mod.new_document()
    make_styles(d)
    sec = d.sections[-1]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(12); sec.top_margin = sec.bottom_margin = Mm(12)
    footer_text(sec, "SEN0414 %s – Form %s – KEY (instructor only)" % (titles[kind], form))
    add_par(d, "", style="ExamQHead", runs=[("SEN0414 Advanced Programming – %s – Form %s – KEY" % (titles[kind], form), {})], keep_next=True)
    fm = key[form]["form_mark"]
    add_par(d, "For the instructor only. Engine build seed %s, paper version %s. Mark on the answer sheet in row F: %s. Key checked against the engine key data "
               "(content hash %s)." % (build["seed"], key[form]["paper_version"], fm["code"], key[form]["content_sha256"][:16]), style="ExamNote", keep_next=False)
    by_id = {}
    for b in paper["blocks"][form]:
        for it in b["items"]:
            by_id[it["id"]] = it
    for b in paper["blocks"][form]:
        add_par(d, "", style="ExamQHead", runs=[("Question %s – %s (%d points%s)" % (b["question"][1:], b["title"], b["points"], ", bonus" if b["bonus"] else ""), {})], keep_next=True)
        kitems = [k for k in key[form]["items"] if k["question"] == b["question"]]
        kitems.sort(key=lambda k: k["position"])
        tbl = d.add_table(rows=1 + len(kitems), cols=4)
        tbl.style = d.styles["Table Grid"] if "Table Grid" in [s.name for s in d.styles] else tbl.style
        tblPr = tbl._tbl.tblPr
        lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
        widths = [17, 55, 15, 99]
        for col, w in zip(tbl.columns, widths): col.width = Mm(w)
        hdr = ["Unit", "Answer", "Points", "Reason, tip and chapters"]
        for c, w, h in zip(tbl.rows[0].cells, widths, hdr):
            c.width = Mm(w); cell_text(c, [(h, {"b": True})], style="ExamNote", keep_next=True)
        for row, k in zip(tbl.rows[1:], kitems):
            it = by_id[k["id"]]
            trPr = row._tr.get_or_add_trPr(); trPr.append(OxmlElement("w:cantSplit"))
            for c, w in zip(row.cells, widths): c.width = Mm(w)
            c0, c1, c2, c3 = row.cells
            cell_text(c0, [("\n".join(u["unit"] for u in k["units"]), {"b": True})], style="ExamNote", keep_next=False)
            cp = c1.paragraphs[0]; cp.style = d.styles["ExamNote"]
            for i, u in enumerate(k["units"]):
                r = cp.add_run(("%s: " % u["unit"]) if len(k["units"]) > 1 else ""); r.bold = True
                cp.add_run(answer_text(it, i, u, k["type"]) + ("\n" if i < len(k["units"]) - 1 else ""))
            cp.paragraph_format.keep_with_next = False
            cell_text(c2, [("\n".join(str(u["points"]) for u in k["units"]), {})], style="ExamNote", keep_next=False)
            tipt = k["tip"] if isinstance(k["tip"], str) and k["tip"].strip().lower() != "none" else "no tip"
            cell_text(c3, [(k["reason"], {}), (("  Tip: " + tipt + ("" if tipt.endswith((".", "?", "!")) else ".")), {"i": True}), ("  Chapters %s; Bloom level %d." % (", ".join(map(str, k["chapters"])), k["bloom"]), {})],
                      style="ExamNote", keep_next=False)
    add_par(d, "Totals: base %s points, bonus %s points." % (key[form]["base_points"], key[form]["bonus_points"]), style="ExamNote", keep_next=False)
    d.core_properties.title = "SEN0414 %s Form %s key" % (titles[kind], form)
    d.core_properties.author = ""
    d.save(out_path)
    return out_path


# ---------------------------------------------------------------- the answer sheet (module reused unedited)
def load_sheet_module():
    p = SHEET_DIR / SHEET_FILE
    if not p.is_file():
        raise RuntimeError("sheet module not found: %s" % p)
    spec = importlib.util.spec_from_file_location("sen0401_sheet_reused", str(p))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def render_sheet(sheetspec, out_dir, stem):
    mod = load_sheet_module()
    from reportlab.pdfgen import canvas as rl_canvas
    import types

    class C(rl_canvas.Canvas):                                # only the course code in the module's own title strings is swapped
        def drawString(self, x, y, text, *a, **k): return super().drawString(x, y, text.replace("SEN0401", "SEN0414"), *a, **k)
        def setTitle(self, t): return super().setTitle(t.replace("SEN0401", "SEN0414"))
    mod.canvas = types.SimpleNamespace(Canvas=C)
    layout = mod.build_layout(sheetspec)
    pdf = os.path.join(out_dir, stem + "_answersheet.pdf"); js = os.path.join(out_dir, stem + "_answersheet_layout.json")
    mod.render(layout, pdf)
    with open(js, "w") as f:
        json.dump(layout, f, indent=1)
    return pdf, js, layout["pages"]


def main(argv):
    args = list(argv[1:])
    if not args or args[0] != "render":
        print(__doc__); return 2
    args.pop(0); opt = {}
    while args:
        a = args.pop(0)
        if a.startswith("--"): opt[a[2:]] = args.pop(0)
    try:
        bd, stem, out = Path(opt["build-dir"]), opt["stem"], opt["out"]
        paper = json.load(open(bd / (stem + "_paper.json"))); key = json.load(open(bd / (stem + "_key.json")))
        build = json.load(open(bd / (stem + "_build.json"))); spec = json.load(open(bd / (stem + "_sheetspec.json")))
    except (KeyError, OSError) as e:
        print("CANNOT_RUN: %r" % (e,)); return 2
    os.makedirs(out, exist_ok=True)
    kind_stem = opt.get("name", stem)
    for f in opt.get("forms", "A,B").split(","):
        print("wrote", render_paper(paper, key, build, f, os.path.join(out, "%s_form_%s_paper.docx" % (kind_stem, f)), opt.get("date")))
        print("wrote", render_key(paper, key, build, f, os.path.join(out, "%s_form_%s_key.docx" % (kind_stem, f))))
    pdf, js, pages = render_sheet(spec, out, kind_stem)
    print("wrote", pdf, "(%d page%s)" % (pages, "" if pages == 1 else "s")); print("wrote", js)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
