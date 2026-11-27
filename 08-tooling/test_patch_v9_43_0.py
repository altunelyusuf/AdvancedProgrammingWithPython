#!/usr/bin/env python3
"""Page test 9.43.0 = 9.42.0 (textually unchanged except the lines named here) + the owner's rulings of 2026-11-27, which 9.42.0 predates:
(a) exam and quiz questions test course content, never book metadata: the concept-coverage checks count the nodes that are NOT metadata nodes (the metadata set of the
    meta clean: practice scaffolding, edition changes, errata; template 9.56.0 leaves them out of every pool), so a page that obeys the ruling no longer fails 'one question for every concept';
(b) a finished mock exam and its review show the corrections open under each question; the practice drill keeps them folded until opened (feature 'corrections are folded under the mark until opened' unchanged).
usage: test_patch_v9_43_0.py IN(9.42.0) OUT(9.43.0)"""
import sys
s = open(sys.argv[1], encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100]); s = s.replace(a, b)
rep('__version__ = "9.39.0"', '__version__ = "9.43.0"')
META = "{'PracticeWork','PracticeQuestions','PracticePrograms','PracticeProgram','PracticeProgramsAndAnswers','BookAndPractice','WorkingVocabulary','EditionChange','SecondEditionContent','BookCorrections','Questions'}"
rep('view("quiz"); nn = len(d["nodes"])', 'META_IDS = %s\n    _mid = {n["id"] for n in d["nodes"] if n["id"] in META_IDS or (n.get("label") in ("Programs", "Questions") and n.get("parent") in META_IDS)}\n    view("quiz"); nn = len([n for n in d["nodes"] if n["id"] not in _mid])' % META)
rep('pg.evaluate("()=>D.nodes.every(n=>BANK.some(b=>b.concept===n.id))")', 'pg.evaluate("()=>D.nodes.filter(n=>!(typeof XMETANODES!==\'undefined\'&&XMETANODES.has(n.id))).every(n=>BANK.some(b=>b.concept===n.id))")')
# (b) after the first finished exam of the history step
a = '''    finish_show(); pg.wait_for_timeout(300)
    hist = pg.evaluate('''
rep(a, '''    finish_show(); pg.wait_for_timeout(300)
    _fx = pg.evaluate("()=>[...document.querySelectorAll('fieldset[data-xi] details.xfixd')].map(d=>d.open)")
    feat("a finished mock exam shows its corrections open under each question (the drill keeps them folded)", len(_fx) == 0 or all(_fx), "%d corrections, %d open" % (len(_fx), sum(_fx)))
    hist = pg.evaluate(''')
open(sys.argv[2], "w", encoding="utf-8").write(s); print("wrote", sys.argv[2], len(s))
