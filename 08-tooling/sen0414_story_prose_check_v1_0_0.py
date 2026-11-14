#!/usr/bin/env python3
"""Story prose check v1.0.0: a story slide is told as natural prose (owner's rule: 5N1K human storytelling, never WHO / WHAT / WHEN / WHERE / WHY / HOW labels).
Fails a slide whose title starts with 'Story' when a text box starts with one of those six words as a label, or when it holds fewer than 3 prose paragraphs of 8 or more words.
Usage: python3 sen0414_story_prose_check_v1_0_0.py DECK.pptx   (exit 0 = clean)"""
import sys, re
from pptx import Presentation
LAB = re.compile(r'^\s*(WHO|WHAT|WHEN|WHERE|WHY|HOW)\b\s*[:\-]?\s', re.I)
LABUP = re.compile(r'^\s*(WHO|WHAT|WHEN|WHERE|WHY|HOW)\s{1,3}\S')  # the upper-case label style of the earlier layout
bad = []; n = 0
for i, s in enumerate(Presentation(sys.argv[1]).slides, 1):
    t = next((sh.text_frame.text for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.startswith('Story')), None)
    if t is None: continue
    n += 1; prose = 0
    for sh in s.shapes:
        if not sh.has_text_frame: continue
        x = sh.text_frame.text
        if LABUP.match(x) or re.match(r'^\s*(WHO|WHAT|WHEN|WHERE|WHY|HOW)\s*:', x, re.I): bad.append((i, 'label: ' + x[:20]))
        if sh.name == 'story' and len(x.split()) >= 8: prose += 1
    if prose < 3: bad.append((i, 'fewer than 3 prose paragraphs'))
print('story slides checked:', n)
for b in bad: print('FAIL', b)
print('RESULT', 'CLEAN' if not bad else 'FAILING (%d)' % len(bad))
sys.exit(1 if bad else 0)
