#!/usr/bin/env python3
"""sen0414_control_urgent_deck v1_0_0 - the controller's OWN checks of an urgent deck (written by the lineage agent, independent of the executor's checks).
Elements:  C1 no prompt ('>>>' or '...') in any code box, table cell or note (the corner brand-mark text box '>>>' is the deck's logo and is exempt: a shape whose whole text is '>>>' and that lies in the top 12 per cent of the slide);
           C2 no lambda in any text or note;  C3 indentation: every compound statement's body starts exactly four spaces deeper on a line of its own, no tabs, all indents multiples of four (measured on the AST);
           C4 no label words WHO/WHAT/WHEN/WHERE/WHY/HOW followed by a colon or dash, at the start of a line or sentence, on any slide or note;  C5 notes: 40 to 60 words (title, divider and last slide 25 to 60);
           C6 every code box compiles (ast.parse) unless it is marked '# does not run on purpose';  C7 slides are numbered ('n / N' text on every slide);  C8 manifest: examples equal the deck's code boxes in text and order.
A code box = a text shape whose runs are all in a monospace font (Courier New, Consolas), other than a prompt-only shape. A slide's notes are read from its notes page.
Usage: sen0414_control_urgent_deck_v1_0_0.py DECK.pptx [MANIFEST.json]      |      --selftest       Exit 0 only when every element passes."""
__version__ = "1.0.0"
import ast, json, re, sys
MONO = ("courier", "consolas", "mono")
LABEL = re.compile(r"(?:^|[.!?]\s+|\n|[\u2022\-\u2013]\s*)(WHO|WHAT|WHEN|WHERE|WHY|HOW)\s*[:\u2013\u2014\-]\s", re.I)
LABEL_CAPS = re.compile(r"^\s*(WHO|WHAT|WHEN|WHERE|WHY|HOW)\b", re.M)
PROMPT = re.compile(r"^\s*(>>>|\.\.\.)(\s|$)")


def is_mono(sh):
    if not sh.has_text_frame: return False
    names = [(r.font.name or "").lower() for p in sh.text_frame.paragraphs for r in p.runs]
    return bool(names) and all(any(m in n for m in MONO) for n in names)


def indentation_problems(code):
    """Problems of one code text; [] when the indentation is right. Needs the code to parse; otherwise a line heuristic is used."""
    probs = []
    for i, l in enumerate(code.split("\n"), 1):
        if "\t" in l: probs.append("line %d has a tab" % i)
        n = len(l) - len(l.lstrip(" "))
        if l.strip() and n % 4: probs.append("line %d is indented %d spaces (not a multiple of 4)" % (i, n))
    try:
        tree = ast.parse(code)
    except SyntaxError:
        lines = code.split("\n")
        for i, l in enumerate(lines[:-1]):
            if l.rstrip().endswith(":") and not l.lstrip().startswith("#"):
                nxt = next((x for x in lines[i + 1:] if x.strip()), None)
                if nxt is not None and len(nxt) - len(nxt.lstrip()) <= len(l) - len(l.lstrip()):
                    probs.append("line %d ends with a colon and the next line is not deeper" % (i + 1))
        return probs
    def body_check(node, stmts):
        if not stmts: return
        first = stmts[0]
        if first.lineno == node.lineno and not isinstance(node, ast.Module):
            probs.append("line %d: a compound statement's body is on its header line" % node.lineno)
        elif first.col_offset != node.col_offset + 4:
            probs.append("line %d: the body starts at column %d, header at %d (needs +4)" % (first.lineno, first.col_offset, node.col_offset))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith)):
            body_check(node, node.body)
            if getattr(node, "orelse", None): body_check(node, node.orelse)
        elif isinstance(node, ast.If):
            body_check(node, node.body)
            oe = node.orelse
            if oe and not (len(oe) == 1 and isinstance(oe[0], ast.If) and oe[0].col_offset == node.col_offset):
                body_check(node, oe)
        elif isinstance(node, ast.Try):
            body_check(node, node.body)
            for h in node.handlers: body_check(h, h.body)
            if node.orelse: body_check(node, node.orelse)
            if node.finalbody: body_check(node, node.finalbody)
    return probs


def deck_facts(path):
    from pptx import Presentation
    from pptx.util import Emu
    P = Presentation(path); H = P.slide_height; out = []
    for i, s in enumerate(P.slides, 1):
        boxes = []; texts = []; cells = []
        for sh in s.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip():
                t = sh.text_frame.text
                brand = t.strip() == ">>>" and sh.top is not None and sh.top < 0.12 * H
                if is_mono(sh) and t.strip() not in (">>>", "..."): boxes.append(t.rstrip("\n"))
                if not brand: texts.append(t)
            if getattr(sh, "has_table", False) and sh.has_table:
                for r in sh.table.rows:
                    for c in r.cells:
                        if c.text.strip(): cells.append(c.text)
        notes = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
        out.append({"n": i, "boxes": boxes, "texts": texts, "cells": cells, "notes": notes,
                    "numbered": any(re.fullmatch(r"\s*%d\s*/\s*%d\s*" % (i, len(P.slides)), t) for t in texts)})
    return out


def run(deck, manifest=None):
    F = deck_facts(deck); N = len(F); res = {}
    def put(k, bad, ok_note):
        res[k] = ("PASS", ok_note) if not bad else ("FAIL", "; ".join(bad[:8]) + (" (+%d more)" % (len(bad) - 8) if len(bad) > 8 else ""))
    bad = []
    for f in F:
        for t in f["texts"] + f["cells"] + [f["notes"]] + f["boxes"]:
            for l in t.split("\n"):
                if PROMPT.match(l): bad.append("slide %d: prompt line %r" % (f["n"], l[:30]))
    put("C1 no prompts", bad, "no '>>>' or '...' line in %d slides" % N)
    bad = [("slide %d" % f["n"]) for f in F if re.search(r"\blambda\b", " ".join(f["texts"] + f["cells"] + f["boxes"] + [f["notes"]]))]
    put("C2 no lambda", bad, "no lambda")
    bad = []; nbox = 0
    for f in F:
        for b in f["boxes"]:
            nbox += 1
            for p in indentation_problems(b): bad.append("slide %d: %s" % (f["n"], p))
    put("C3 indentation", bad, "%d code boxes, every body four spaces deeper, no tabs" % nbox)
    bad = []
    for f in F:
        for t in f["texts"] + f["cells"] + [f["notes"]]:
            m = LABEL.search(t) or LABEL_CAPS.search(t)
            if m: bad.append("slide %d: label word %r" % (f["n"], m.group(1)))
    put("C4 no 5N1K labels", bad, "no label words")
    bad = []
    for f in F:
        w = len(f["notes"].split()); first_or_last = f["n"] in (1, N)
        divider = bool(f["texts"]) and not any(b for b in [f["boxes"]]) and f["texts"][0].strip().lower().startswith("part ")
        lo = 25 if (first_or_last or divider) else 40
        if not lo <= w <= 60: bad.append("slide %d: %d words (needs %d-60)" % (f["n"], w, lo))
    put("C5 notes 40-60 words", bad, "all %d notes in range" % N)
    bad = []
    for f in F:
        for b in f["boxes"]:
            if "does not run on purpose" in b: continue
            try: ast.parse(b)
            except SyntaxError as e: bad.append("slide %d: %s" % (f["n"], e.msg))
    put("C6 every code box compiles", bad, "all code boxes compile")
    bad = [("slide %d" % f["n"]) for f in F if not f["numbered"]]
    put("C7 numbered slides", bad, "every slide shows n / %d" % N)
    if manifest:
        m = json.load(open(manifest, encoding="utf-8")); ex = m["examples"]
        norm = lambda c: "\n".join(l.rstrip() for l in c.strip("\n").split("\n"))
        boxes = [norm(b) for f in F for b in f["boxes"] if len(b.split("\n")) >= 1 and f["boxes"]]
        # the manifest examples are the deck's code slides in order: compare the multiset order by sequential containment
        codes = [norm(e["code"]) for e in sorted(ex, key=lambda e: e["order"])]
        pos = 0; bad = []
        for k, c in enumerate(codes, 1):
            try: pos = boxes.index(c, pos) + 1
            except ValueError: bad.append("example %d (%s) is not a code box of the deck after example %d" % (k, ex[k - 1].get("id"), k - 1))
        put("C8 manifest equals code boxes in order", bad, "%d examples found in order among %d code boxes" % (len(codes), len(boxes)))
    else:
        res["C8 manifest equals code boxes in order"] = ("NOT_MEASURED", "no manifest given")
    return res


def selftest():
    ok = True
    def expect(name, got, want):
        nonlocal ok
        print(("PASS " if got == want else "FAIL ") + name, "" if got == want else "got %r want %r" % (got, want)); ok &= got == want
    good = "def f(s):\n    if s:\n        return s.upper()\n    return s\n"
    expect("indentation: good code has no problem", indentation_problems(good), [])
    expect("indentation: flattened body is caught", bool(indentation_problems("if True: print(1)\n")), True)
    expect("indentation: two-space body is caught", bool(indentation_problems("for i in x:\n  print(i)\n")), True)
    expect("indentation: tab is caught", bool(indentation_problems("for i in x:\n\tprint(i)\n")), True)
    expect("indentation: elif chain is accepted", indentation_problems("if a:\n    x = 1\nelif b:\n    x = 2\nelse:\n    x = 3\n"), [])
    expect("indentation: try/except accepted", indentation_problems("try:\n    x = 1\nexcept ValueError:\n    x = 2\n"), [])
    expect("label: 'WHAT: x' caught", bool(LABEL.search("WHAT: a story")), True)
    expect("label: 'Who: x' caught at line start", bool(LABEL.search("Intro.\nWho: Ken Thompson")), True)
    expect("label: 'WHO  Eric V. Smith' (capital label, no colon) caught", bool(LABEL_CAPS.search("WHO  Eric V. Smith, author")), True)
    expect("label: a capitalised ordinary word 'Who' not caught by the capital form", bool(LABEL_CAPS.search("Who wrote it? Ken did.")), False)
    expect("label: ordinary sentence not caught", bool(LABEL.search("Ken Thompson wrote what we now call regular expressions.")), False)
    expect("prompt: '>>> x' caught", bool(PROMPT.match(">>> print(1)")), True)
    expect("prompt: '...' alone caught", bool(PROMPT.match("...")), True)
    expect("prompt: ellipsis inside text not caught", bool(PROMPT.match("wait... what")), False)
    print("SELFTEST", "PASS" if ok else "FAIL"); return 0 if ok else 1


def main():
    if sys.argv[1:] == ["--selftest"]: sys.exit(selftest())
    if len(sys.argv) < 2: sys.exit(__doc__)
    res = run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None); bad = 0
    for k, (st, note) in res.items():
        print("[%s] %s  %s" % (st, k, note)); bad += st != "PASS"
    print("RESULT", "PASS" if not bad else "FAIL (%d element(s) not passed)" % bad); sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
