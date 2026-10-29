#!/usr/bin/env python3
"""Exam briefs, version 1.1.0: runs sen0414_lineage_brief_exam_v1_0_0.py (unchanged) and appends (a) the Owner's chapter decision of 2026-10-30 to every brief and
(b) for the design task the starting points carried over from earlier printed-paper rules and what this course needs differently. Output: 08-tooling/briefs/exam/r2 (or argv[2])."""
import os, sys, subprocess
here = os.path.dirname(os.path.abspath(__file__)); tgt = sys.argv[1] if len(sys.argv) > 1 else "ALL"
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "briefs", "exam", "r2")
subprocess.run([sys.executable, os.path.join(here, "sen0414_lineage_brief_exam_v1_0_0.py"), tgt, out], check=True)
CH = ("\n## Update of 2026-10-30 (the Owner's decision, relayed)\nThe chapter list is fixed: the exams cover chapters 1 to 8 without chapter 5 (Debugging), that is chapters 1, 2, 3, 4, 6, 7 and 8. "
      "Where this brief says the list is still open, this sentence replaces it. Chapter 5 stays complete as chapter material and receives no work.\n")
DESIGN = """
## Starting points carried over from earlier printed-paper rules, and what this course needs differently
These come from a finished piece of work on a printed paper for another course. They are starting points to adopt, change or reject with a reason in your decisions list; they are not orders.
Adopt as they are:
- Item types by suitability for print. Suited: four-option single-answer choice (about 60 s), choice with a short code listing (about 100 s), matching premises to a longer list of answers (about 240 s), ordering the steps of a process (about 120 s), fill-in from a shared numbered bank (about 45 s), a single number in a box (about 120 s), trace: the printed result of a short listing (about 120 s). Allowed only when the paper names it: short written answer (marking rubric of at most 3 points), diagram labelling, writing code on paper. Not suited: every type that needs a screen (run code, drag, query a live endpoint, free chat).
- Paper conventions: black ink on white, light theme, no shading or colour; body text 10 point or larger, code 8 point or larger; no student name or number printed on the paper; a version number that is exactly the previous plus one; every item has a position, a unique item key, one type, one Bloom level (1 to 6), at least one chapter and at least one link to a course source (deck slide, speaker note, corpus passage, story).
- Time: the summed answer time of the items must stay at or under 90 per cent of the 60 minutes (the rest is reading and checking).
- Mix: more than half of the items at Apply or above (name the reading you use, Apply and up or Analyze and up); counts of the correct letters A, B, C, D differ by at most one and no letter is the key of four items in a row; a synthesis item names two or more chapters.
- Code: a listing has at most 12 lines and no line is wrapped; declare the width that prints unwrapped (about 45 characters at 9 point in two columns of A4, about 90 in one column).
- Engine rules: a quota of items per chapter that adds up to the number of items; a minimum number of synthesis items; indirect items (asking for a consequence, an exception or a reason) only if the paper enables them and each states its form; the make-up paper repeats a midterm item only if the pair allows it; item keys unique; every term used is found in the course corpus; the pair of papers is complete (midterm and make-up, each with its key).
- Answer sheet and grading: a sheet with fixed corner markers and one mark style, holding no personal data; a machine reads only what it reads with certainty; a doubtful or double mark is held and a person looks at the original sheet whose reading is final; every sheet is tied to its paper by a version mark; tested on synthetic sheets only.
Needs to be different for this course (decide and give reasons):
- The course is Python programming: many items are about code. Decide how a listing is shown on paper so no line wraps, which code types are kept (predict the printed output, find the faulty line, complete a blank in the code, order the lines), what the exact-match rule for an output answer is (quotes, spaces, line breaks, how a list or dictionary prints), and whether writing a few lines of code on paper is enabled (it is not unless you give a marking rubric and say who marks it).
- Chapters 1, 2, 3, 4, 6, 7, 8 only; the names of the course's own terms come from the course corpus of those chapters, not from any other course.
- Money, fees, supply and other arithmetic of the other course do not carry over; numeric answers here are results of expressions, counts of loop passes, lengths, indexes.
- The Bloom reading and the item counts per type are not yet fixed by the Owner: state the assumption you use in the design, mark it as an assumption, and keep it easy to change.
"""
for t in os.listdir(out):
    if not t.startswith("BRIEF_"): continue
    p = os.path.join(out, t); s = open(p, encoding="utf-8").read()
    i = s.find("\n## Order of work")
    add = CH + (DESIGN if "Design" in t else "")
    s = s[:i] + add + s[i:] if i > 0 else s + add
    open(p, "w", encoding="utf-8").write(s)
print("briefs in", out)
