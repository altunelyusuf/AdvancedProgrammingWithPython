#!/usr/bin/env python3
"""Generic code check, version 1.1.0 (Lineage11, story ST11_Check; new file over 1.0.0, which stays as committed. 1.1.0 finds a code box by the builder's own name for a code frame, "code", as the deck standard check does, instead of by the font: the result drawings use the same font and 1.0.0 counted them as code boxes).

Fails when, for any example of a chapter source file:
  C1  the manifest code differs from the source code (or the examples are not the same, in the same order);
  C2  the deck slide of the example does not hold the code in exactly ONE code box, or the box text differs from the source code;
  C3  the page data does not hold the example code as exactly one whole string equal to the source code;
  C4  the example (hidden setup lines, then the code) does not run to the end.
It holds no chapter text. Every finding names the example and the condition.

Usage:  python3 code_check_v1_1_0.py SOURCE.json --manifest M.json   (M is the examples list or the chapter-code manifest with its examples key) [--deck D.pptx] [--page P.html] [--mono "Courier New"] [--skip-run]
Exit 0 when nothing fails, 2 otherwise. Writes nothing.
"""
__version__ = "1.1.0"
import argparse
import json
import os
import subprocess
import sys
import tempfile


def norm(lines):
    return [l.rstrip() for l in lines]


def c1(src, man):
    out = []
    if [e["id"] for e in src["examples"]] != [m["id"] for m in man]:
        out.append(("-", "C1", "manifest examples or their order differ from the source"))
        return out
    for e, m in zip(src["examples"], man):
        if norm(e["code"]) != norm(m["code"].split("\n")):
            out.append((e["id"], "C1", "manifest code differs from source code"))
    return out


def c2(src, deck, mono):
    from pptx import Presentation
    out = []
    prs = Presentation(deck)
    slides = list(prs.slides)
    for e in src["examples"]:
        n = e["slide"]
        if n < 1 or n > len(slides):
            out.append((e["id"], "C2", "slide %s does not exist" % n))
            continue
        boxes = []
        for sh in slides[n - 1].shapes:
            if not sh.has_text_frame:
                continue
            if sh.name == mono and sh.text_frame.text.strip():
                boxes.append(sh)
        if len(boxes) != 1:
            out.append((e["id"], "C2", "slide %s has %d code boxes, one is required" % (n, len(boxes))))
            continue
        got = norm(boxes[0].text_frame.text.split("\n"))
        if got != norm(e["code"]):
            out.append((e["id"], "C2", "slide %s code differs from the source code" % n))
    return out


def c3(src, page):
    html = open(page, encoding="utf-8").read()
    out = []
    for e in src["examples"]:
        code = "\n".join(e["code"])
        if json.dumps(code, ensure_ascii=False) not in html and json.dumps(code) not in html:
            out.append((e["id"], "C3", "page does not hold the example code as the source has it"))
    return out


def c4(src, timeout=60):
    out = []
    for e in src["examples"]:
        prog = "\n".join(list(e.get("setup", [])) + e["code"]) + "\n"
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "ex.py")
            open(p, "w", encoding="utf-8").write(prog)
            try:
                r = subprocess.run([sys.executable, "-I", p], cwd=d, capture_output=True, text=True, timeout=timeout)
            except subprocess.TimeoutExpired:
                out.append((e["id"], "C4", "did not finish in %d s" % timeout))
                continue
            if r.returncode:
                out.append((e["id"], "C4", "failed: " + (r.stderr.strip().splitlines() or ["?"])[-1]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--deck")
    ap.add_argument("--page")
    ap.add_argument("--mono", default="code", help="the shape name of a code frame")
    ap.add_argument("--skip-run", action="store_true")
    a = ap.parse_args()
    src = json.load(open(a.source, encoding="utf-8"))
    man = json.load(open(a.manifest, encoding="utf-8"))
    if isinstance(man, dict):
        man = man["examples"]
    f = c1(src, man)
    if a.deck:
        f += c2(src, a.deck, a.mono)
    if a.page:
        f += c3(src, a.page)
    if not a.skip_run:
        f += c4(src)
    n = len(src["examples"])
    for ex, c, m in f:
        print("FAIL %s %s: %s" % (c, ex, m))
    conds = ["C1"] + (["C2"] if a.deck else []) + (["C3"] if a.page else []) + ([] if a.skip_run else ["C4"])
    print("code_check %s: %d examples, conditions %s, %d finding(s)" % (__version__, n, "+".join(conds), len(f)))
    sys.exit(2 if f else 0)


if __name__ == "__main__":
    main()
