#!/usr/bin/env python3
"""Fixture decks of known answer for sen0414_deck_standard_check_v1_1_0.py (D1 to D12 and M1). Builds, with python-pptx, small synthetic decks (synthetic text only, no student data):
a clean deck that meets every element, and for each element at least one deck built to fail it (each breaks that element and, where it cannot be helped, the stated others), plus
decks built to report NOT_MEASURED (no code box; no divider; no story slide) and decks built to pass although they look like a failure (a 66-word code box passes D2; the brand mark '>>>' is no
code box). build_all(folder) writes every deck into its own root (folder/<name>/03-materials/ch99/fixture.pptx with rdodi research and page manifest) and returns
{name: (root, deck_path, expected)}, expected = the known answer of every element. The check's --selftest prints expected and actual for each. Run alone: prints the known answers as JSON.
"""
__version__ = "1.1.0"
import json, os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

CH = "99"
ELEMENTS = ["D%d" % i for i in range(1, 13)] + ["M1"]
CONCEPTS = ["String literal", "Escape sequence", "Raw string"]
NOTE = ("Tell the class what the slide shows in two short sentences. Give one example from the code on the slide and run it. "
        "Then ask the class one question about the result and let two students answer before you go on.")
CODE_A = 'word = "hello"\nprint(word.upper())\nprint(len(word))'
CODE_B = "total = 0\nfor n in [1, 2, 3]:\n    total = total + n\nprint(total)"
CODE_66 = "\n".join(["a = b + c"] * 13 + ["pass"])  # 13 x 5 words + 1 = 66 words
CODE_WIDE = "message = 'a very long line of code that cannot fit into the narrow box of the slide at all'"
EXPL_A = "The first line stores a text, the second makes it big letters, the third counts its characters. A raw string would keep every backslash."
EXPL_B = "The loop adds each number to a running total, so the total grows by one number at every turn of the loop."
STORY = ["In September 1992, Ken Thompson and Rob Pike of Bell Labs were building a new system in a New Jersey diner.",
         "Programs needed one encoding for every language that did not break old text, so that nothing old stopped working.",
         "They sketched it on a placemat, and it works by giving each character one to four bytes."]
PNG = None


def png(folder):
    global PNG
    from PIL import Image
    p = os.path.join(folder, "pic.png")
    Image.new("RGB", (300, 300), (90, 120, 160)).save(p)
    return p


def tb(s, x, y, w, h, text, mono=False, size=14, name="box", wrap=True, link=None):
    b = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    b.name = name
    tf = b.text_frame
    tf.word_wrap = wrap
    for k, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        r = p.add_run(); r.text = line
        r.font.size = Pt(size); r.font.name = "Courier New" if mono else "Calibri"
        if link:
            r.hyperlink.address = link
    return b


def chip(s):
    tb(s, 0.4, 0.28, 0.6, 0.36, ">>>", mono=True, size=13, name="chip")


def table(s, y):
    t = s.shapes.add_table(2, 2, Inches(0.4), Inches(y), Inches(9), Inches(1.0)).table
    for r, row in enumerate([["call", "printed"], ["print(len(word))", "5"]]):
        for c, v in enumerate(row):
            t.cell(r, c).text = v


def chart(s, y):
    d = CategoryChartData(); d.categories = ["a", "b", "c"]; d.add_series("n", (1, 2, 3))
    s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.4), Inches(y), Inches(6), Inches(2.1), d)


def build(path, folder, o):
    """o = options dict, see the fixture list below."""
    prs = Presentation(); prs.slide_width, prs.slide_height = Inches(10), Inches(5.625)
    lay = prs.slide_layouts[6]
    pic = png(folder)
    slides = []  # (builder, note_words, kind)

    def title_slide(s):
        chip(s); tb(s, 0.6, 1.7, 8.8, 0.9, "Fixture title", size=32, name="title")

    def divider(s):
        tb(s, 0.5, 0.2, 9, 0.7, "Part 1: Literals", name="title"); tb(s, 0.5, 0.92, 9, 0.34, "How to write text in code", name="subtitle")
        tb(s, 0.5, 1.5, 2.2, 0.5, "String literal", name="pill"); tb(s, 2.85, 1.5, 3.3, 0.6, "Text written between quotes in the code.", name="meaning")
        if not o.get("div_nopic"):
            s.shapes.add_picture(pic, Inches(6.5), Inches(1.4), Inches(2), Inches(2)); tb(s, 6.5, 3.45, 2, 0.3, "Sample picture", size=10, name="credit")

    def code_a(s):
        chip(s); tb(s, 1.15, 0.18, 8.4, 0.55, "Strings in code", name="title")
        ca = o.get("code_a", CODE_A)
        tb(s, 0.4, 1.0, 5.0, 1.6, ca, mono=True, size=o.get("code_a_size", 14), name="code", wrap=not o.get("code_a_nowrap"))
        if o.get("mixed"):
            b = tb(s, 0.4, 2.65, 5.0, 0.3, "x " * 20, mono=True, name="mixed"); r = b.text_frame.paragraphs[0].add_run(); r.text = "y " * 20; r.font.name = "Calibri"
        if not o.get("no_expl"):
            tb(s, 5.6, 1.0, 4.0, 1.2, o.get("expl_a", EXPL_A), name="explanation")
        if not o.get("no_visual"):
            table(s, 3.0)
        if o.get("text66"):
            tb(s, 0.4, 4.3, 9, 0.8, " ".join(["word"] * 66), name="wordy")
        if o.get("chartpic"):
            p = s.shapes.add_picture(pic, Inches(6), Inches(3.9), Inches(1), Inches(1)); p.name = "chart picture"

    def code_b(s):
        chip(s); tb(s, 1.15, 0.18, 8.4, 0.55, "A loop adds numbers", name="title")
        tb(s, 0.4, 1.0, 5.0, 1.4, o.get("code_b", CODE_B), mono=True, size=14, name="code")
        tb(s, 0.4, 2.45, 9, 0.5, EXPL_B, name="explanation")
        chart(s, 3.1)

    def analogies(s):
        chip(s); tb(s, 1.15, 0.18, 8.4, 0.55, "Everyday pictures", name="title")
        names = o.get("analogy_concepts", CONCEPTS)
        tb(s, 0.5, 1.0, 9, 0.8, "ANALOGY  A " + names[0].lower() + " is like a sign over a shop door.", name="analogy")
        for k, c in enumerate(names[1:]):
            tb(s, 0.5, 1.9 + k * 0.7, 9, 0.6, "ANALOGY  A " + c.lower() + " is like a stage direction in a play.", name="analogy")
        if o.get("text66_here"):
            pass
        if o.get("text66_prose"):
            tb(s, 0.5, 3.6, 9, 1.2, " ".join(["word"] * 66), name="wordy")

    def story(s):
        chip(s); tb(s, 1.15, 0.18, 8.4, 0.55, "Story: nine people agree on one table" if not o.get("nostory") else "A plain slide about strings", name="title")
        if not o.get("story_nopic") and not o.get("nostory"):
            s.shapes.add_picture(pic, Inches(0.4), Inches(1.1), Inches(3), Inches(3)); tb(s, 0.4, 4.2, 3, 0.5, "Sample picture. Synthetic.", size=10, name="credit")
        txt = list(STORY)
        if o.get("story_nowhen"):
            txt[0] = txt[0].replace("In September 1992,", "In a certain September,")
        if o.get("nostory"):
            txt = ["A string is a sequence of characters and the quotes only mark its border in the code."] * 3
        for k, t in enumerate(txt):
            tb(s, 3.6, 1.0 + k * 1.0, 6.0, 0.9, t, name="story")
        if not o.get("story_nolink") and not o.get("nostory"):
            tb(s, 3.6, 4.2, 6.0, 0.4, "Read the source page", name="link", link="https://example.org/source")

    def resources(s):
        chip(s); tb(s, 1.15, 0.18, 8.4, 0.55, "Resources: where to go from here", name="title")
        for k in range(o.get("n_links", 5)):
            tb(s, 0.5, 1.0 + k * 0.6, 8, 0.4, "Resource number %d for further reading" % (k + 1), name="resource", link="https://example.org/r%d" % k)

    plan = [("t", title_slide)]
    if not o.get("no_divider"):
        plan.append(("d", divider))
    if not o.get("no_code"):
        plan.append(("c", code_a))
    plan.append(("a", analogies))
    if not o.get("no_code"):
        plan.append(("c", code_b))
    plan.append(("s", story)); plan.append(("r", resources))
    n = len(plan)
    for k, (kind, fn) in enumerate(plan, 1):
        s = prs.slides.add_slide(lay)
        fn(s)
        if not (o.get("unnumbered") == k):
            tb(s, 8.6, 5.2, 1.0, 0.32, "%d / %d" % (k, n), size=11, name="slide number")
        s.notes_slide.notes_text_frame.text = (" ".join(["note"] * 70) if (o.get("longnote") and kind == "a") else NOTE)
        if o.get("dark") and kind == "a":
            s.background.fill.solid(); s.background.fill.fore_color.rgb = RGBColor(0x10, 0x10, 0x20)
        else:
            s.background.fill.solid(); s.background.fill.fore_color.rgb = RGBColor(0xF8, 0xF8, 0xF4)
    prs.save(path)
    return n


def build_all(folder):
    out = {}
    base = {}
    exp_pass = {e: "PASS" for e in ELEMENTS}
    # name: (options, manifest options, concepts in the research file, expected overrides)
    F = {
        "clean": ({}, {}, CONCEPTS, {}),
        "d1_one_slide_unnumbered": ({"unnumbered": 4}, {}, CONCEPTS, {"D1": "FAIL"}),
        "d2_text_box_66_words": ({"text66_prose": True}, {}, CONCEPTS, {"D2": "FAIL"}),
        "d2_code_box_66_words_passes": ({"code_a": CODE_66, "code_a_size": 9}, {"code_a": CODE_66}, CONCEPTS, {}),
        "d2_mixed_font_box_is_prose": ({"mixed": True}, {}, CONCEPTS, {"D2": "FAIL"}),
        "d3_no_visual_result": ({"no_visual": True}, {}, CONCEPTS, {"D3": "FAIL"}),
        "d3_no_explanation": ({"no_expl": True}, {}, CONCEPTS, {"D3": "FAIL"}),
        "d4_concept_without_analogy": ({"analogy_concepts": CONCEPTS[:2]}, {}, CONCEPTS, {"D4": "FAIL"}),
        "d11_concept_not_shown": ({}, {}, CONCEPTS + ["Zebra crossing"], {"D4": "FAIL", "D11": "FAIL"}),
        "d5_story_without_picture": ({"story_nopic": True}, {}, CONCEPTS, {"D5": "FAIL"}),
        "d5_story_without_link": ({"story_nolink": True}, {}, CONCEPTS, {"D5": "FAIL"}),
        "d5_story_without_when": ({"story_nowhen": True}, {}, CONCEPTS, {"D5": "FAIL"}),
        "d5_no_story_slide": ({"nostory": True}, {}, CONCEPTS, {"D5": "NOT_MEASURED"}),
        "d6_chart_as_picture": ({"chartpic": True}, {}, CONCEPTS, {"D6": "FAIL"}),
        "d7_note_over_60_words": ({"longnote": True}, {}, CONCEPTS, {"D7": "FAIL"}),
        "d8_two_links_only": ({"n_links": 2}, {}, CONCEPTS, {"D8": "FAIL"}),
        "d9_one_dark_slide": ({"dark": True}, {}, CONCEPTS, {"D9": "FAIL"}),
        "d10_divider_without_picture": ({"div_nopic": True}, {}, CONCEPTS, {"D10": "FAIL"}),
        "d10_no_divider": ({"no_divider": True}, {}, CONCEPTS, {"D10": "NOT_MEASURED"}),
        "d12_wrapped_code_line": ({"code_a": CODE_WIDE}, {"code_a": CODE_WIDE}, CONCEPTS, {"D12": "FAIL"}),
        "m1_swapped_pair": ({}, {"swap": True}, CONCEPTS, {"M1": "FAIL"}),
        "m1_one_character_differs": ({}, {"code_b": CODE_B.replace("total + n", "total - n")}, CONCEPTS, {"M1": "FAIL"}),
        "no_code_box_empty_manifest": ({"no_code": True}, {"empty": True}, CONCEPTS, {"D3": "NOT_MEASURED", "D12": "NOT_MEASURED", "M1": "NOT_MEASURED"}),
        "no_code_box_manifest_lists_two": ({"no_code": True}, {}, CONCEPTS, {"D3": "NOT_MEASURED", "D12": "NOT_MEASURED", "M1": "FAIL"}),
    }
    for name, (o, mo, concepts, over) in F.items():
        root = os.path.join(folder, name)
        d = os.path.join(root, "03-materials", "ch" + CH)
        for sub in ("rdodi", "page"):
            os.makedirs(os.path.join(d, sub), exist_ok=True)
        deck = os.path.join(d, "fixture.pptx")
        build(deck, folder, o)
        with open(os.path.join(d, "rdodi", "sen0414_ch%s_research_v1_0_0.ttl" % CH), "w", encoding="utf-8") as f:
            for k, c in enumerate(concepts):
                f.write('sen0414:c%d a sen0414:PrimarySourceConcept ; rdfs:label "%s" .\n' % (k, c))
        ca, cb = mo.get("code_a", o.get("code_a", CODE_A)), mo.get("code_b", CODE_B)
        ex = [] if mo.get("empty") else [{"slide": 3, "code": ca}, {"slide": 5, "code": cb}]
        if o.get("no_divider"):
            ex = [{"slide": 2, "code": ca}, {"slide": 4, "code": cb}]
        if mo.get("swap"):
            ex[0]["code"], ex[1]["code"] = ex[1]["code"], ex[0]["code"]
        json.dump({"deck": "03-materials/ch%s/fixture.pptx" % CH, "examples": ex}, open(os.path.join(d, "page", "chapter_code_ch%s_v1_0_0.json" % CH), "w"))
        out[name] = (root, deck, dict(exp_pass, **over))
    return out


if __name__ == "__main__":
    import tempfile
    t = tempfile.mkdtemp(prefix="fx110_")
    r = build_all(t)
    print(json.dumps({k: {e: v for e, v in x[2].items() if v != "PASS"} for k, x in r.items()}, indent=1))
    import shutil; shutil.rmtree(t, ignore_errors=True)
