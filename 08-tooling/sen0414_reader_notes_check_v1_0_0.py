#!/usr/bin/env python3
"""Reader-notes check v1.0.0 (handover practice 3: deck notes are for the reader, who gets the slides and the notes).
Fails a slide whose notes hold any of:
  directions   an instruction to a presenter or the class ("say", "tell the students", "ask the class", "click", "point to", "let's", "now we", "as you can see", "demonstrate")
  think-of     a "think of" / "imagine" / "picture" statement
  prompt       a Python prompt marker (">>>", "...", ">>")
  lambda       the word lambda or a "lambda" expression (unless the notes explain it: a slide whose title mentions lambda)
  connection   no link to another slide, chapter or related concept ("slide N", "chapter N", "see", "related", "compare", "same as", "also")
Slides with no notes are reported as missing. Usage: sen0414_reader_notes_check_v1_0_0.py DECK.pptx   (exit 0 = clean)"""
__version__ = "1.0.0"
import re, sys
from pptx import Presentation
RULES = [
    ("directions", re.compile(r"\b(say to|tell (the )?(students|class|them)|ask (the )?(students|class)|click (on|the)|point (to|at|out)|let\u2019s|let's|let us|now we|as you can see|demonstrate|walk (them|the class)|show (the )?(class|students)|presenter|you should (say|tell))\b", re.I)),
    ("think-of", re.compile(r"\b(think of|imagine|picture (a|an|the|it))\b", re.I)),
    ("prompt", re.compile(r"(>>>|\.\.\.|(?<![>\-=])>>(?!>))")),
    ("lambda", re.compile(r"\blambda\b", re.I)),
]
CONN = re.compile(r"\b(slide \d+|slides \d+|chapter \d+|chapters \d+|see |related|compare|compared|same as|also|likewise|in contrast|earlier|later|next chapter)\b", re.I)
bad = []; n = 0
for i, s in enumerate(Presentation(sys.argv[1]).slides, 1):
    n += 1
    t = s.notes_slide.notes_text_frame.text.strip() if s.has_notes_slide else ""
    if not t: bad.append((i, "missing notes")); continue
    title = next((sh.text_frame.text for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip()), "")
    for name, rx in RULES:
        if name == "lambda" and "lambda" in title.lower(): continue
        m = rx.search(t)
        if m: bad.append((i, name + ": " + m.group(0)))
    if not CONN.search(t): bad.append((i, "connection: no link to another slide, chapter or concept"))
print("slides checked:", n)
for b in bad: print("FAIL", b)
print("RESULT", "CLEAN" if not bad else "FAILING (%d)" % len(bad))
sys.exit(1 if bad else 0)
