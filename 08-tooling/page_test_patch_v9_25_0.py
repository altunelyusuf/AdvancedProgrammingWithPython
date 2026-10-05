#!/usr/bin/env python3
"""Builds sen0414_page_test_v9_25_0.py from sen0414_page_test_v9_24_0.py - the page test brought in line with
template 9.25.0, and four new assertions so the defects the adversarial audit of the sibling course's chapter 1 page
found cannot come back to this one unnoticed.

The chain's rule applies to the test as much as to the template: nothing is edited in place, so the change is this
script plus its output, and v9_24_0 stays on disk as the record of what was asserted before.

WHAT IS CORRECTED, BECAUSE A REPAIR MADE THE OLD ASSERTION WRONG

 1. "a course question reaches the course ontology" asked a SUBJECT AGENT to reach LO-1 and required it to succeed.
    Repair 1 of template 9.24.0 (the audit's F-B1) restricts an agent to the passages its own `covers` set reaches,
    and a course learning outcome is a passage of the course ontology belonging to no concept of this chapter, so it
    is in no agent's slice - by design, because handing an agent a passage it does not own is the defect that was
    repaired. The old assertion therefore demanded the leak back. It is replaced by the three things that must really
    hold: a subject agent does NOT return the outcome (the slice holds), the page-wide passage search DOES (the
    material is reachable), and the guide puts it in front of the student instead of saying it is not here (template
    9.25.0's repair 4). The last of the three is the "a student must be able to reach a course learning outcome by
    some route" assertion, asserted against the route the student actually has.
 2. "ontology graph is a rooted tree like the taxonomy ..." counted individuals in the taxonomy while the Worked
    examples layer was off. Repair 6 of template 9.24.0 (the audit's F-B3) makes the view open with the Classes layer
    alone, because all three layers at once draw several hundred boxes and none stays readable; the 9.24.0 test
    corrected the taxonomy check for that and left this one, which then measured 0 individuals against a requirement
    of more than 20. The layer is now turned on before the counts are taken, which is what the check was always
    about - that individuals and book concepts hang under their class - and off again afterwards, so the
    layer-removal count below it still falls.
 3. "a link 'All chapters' leads back to the index" required the link unconditionally. Repair 8 of template 9.24.0
    (the audit's F-B5) shows it only when a chapter index really sits beside the page, which nothing in this
    repository provides, because a link to a file that does not exist is a dead link to a student. The assertion is
    now the conditional one: the link is present, points at the index the page data names, and is visible exactly
    when there is an index, and is absent otherwise.

WHAT IS ADDED, SO THESE DEFECTS CANNOT RETURN

 4. NO VISIBLE SPARQL SAMPLE NAME CARRIES A PLACEHOLDER, and the sample that asks whether the chapter defines a class
    names a class this chapter really defines. The audit's F-B6 was a sample whose option text still read
    'Does the chapter define a class labelled "{FIRST_LEAF}"?' while the query behind it was substituted correctly.
    That exact defect does not exist in this template (it has no placeholder to substitute), but the assertion is
    cheap and is the guard the audit asked for; the second half of it catches the fault this template did have,
    where the name was fixed to a class only chapter 1 defines.
 5. TWO AGENTS WHOSE SUBJECTS DO NOT OVERLAP DO NOT GIVE THE SAME ANSWER TO THE SAME QUESTION, and the one that does
    not own the subject says so and offers to hand the question on. This is the audit's own form of F-B1 - it put one
    question to two agents with disjoint `covers` and got the same six sources back. The check already in the test
    varies the question and holds the agent fixed, which a page retrieving from the whole corpus would also pass, so
    it could not have caught that defect.
 6. A STUDENT CAN REACH A COURSE LEARNING OUTCOME BY SOME ROUTE - see 1; the guide half is the route.
 7. THE VOCABULARY TAB EXISTS AND EXPLAINS EACH TERM. Against the audit's F-D5 and the owner's rule that every term
    and tool the page uses must itself be explained: About > Words we use must carry a heading for each of ontology,
    knowledge graph, triple, taxonomy, SPARQL, agent, semantic search, Pyodide, class diagram and
    entity-relationship diagram, and each heading must be followed by a real explanation - more than 200 characters
    and more than one sentence - not a single line. A second assertion requires the explanations to be written in
    this course's own terms, with no example borrowed from the sibling Blockchain course, which is the defect
    template 9.25.0's repair 5 fixed.

usage: page_test_patch_v9_25_0.py [IN.py OUT.py]"""
__version__ = "9.25.0"
import os, sys

here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 2 else os.path.join(here, "sen0414_page_test_v9_24_0.py")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "sen0414_page_test_v9_25_0.py")
h = open(src, encoding="utf-8").read()
APPLIED = []


def rep(a, b, n=1, tag=""):
    global h
    assert h.count(a) == n, ("anchor not found %dx: %r (found %d)" % (n, a[:90], h.count(a)))
    h = h.replace(a, b)
    APPLIED.append(tag or a[:40])


# ---- version markers -------------------------------------------------------------------------------------------------
rep('__version__ = "9.24.0"\n'
    '# 9.24.0 (over 9.23.0):',
    '__version__ = "9.25.0"\n'
    '# 9.25.0 (over 9.24.0): brought in line with template 9.25.0 and the audit\'s own form of its findings - a course'
    ' learning outcome is reached by the page-wide passage search and by the guide, not by a subject agent whose slice'
    ' does not contain it; the taxonomy\'s individuals are counted with their layer turned on; the "All chapters" link'
    ' is required exactly when a chapter index sits beside the page. New: no visible SPARQL sample name carries a'
    ' placeholder and the ASK sample names a class this chapter really defines; two agents with disjoint slices do not'
    ' answer the same question alike and the one that does not own it hands it over; the vocabulary tab explains every'
    ' term it must, in full sentences, with no example from the sibling course.\n'
    '# 9.24.0 (over 9.23.0):',
    tag="version header")

# ---- 5  two agents with disjoint slices answer the same question differently -----------------------------------------
rep('    feat("agents answer from their own slice; different questions get different answers", ans1 != ans2 and len(ans1) > 40 and len(ans2) > 40 and ("Nothing in the book, course or chapter material answers that" in ans3),\n'
    '         "%s | %s | %s" % (ans1[:60], ans2[:60], ans3[:60]))\n',
    '    feat("agents answer from their own slice; different questions get different answers", ans1 != ans2 and len(ans1) > 40 and len(ans2) > 40 and ("Nothing in the book, course or chapter material answers that" in ans3),\n'
    '         "%s | %s | %s" % (ans1[:60], ans2[:60], ans3[:60]))\n'
    '    # 9.25.0: the audit\'s own form of F-B1. The check above varies the question and holds the agent fixed, which a\n'
    '    # page retrieving from the whole corpus passes just as well; what the audit actually did was put ONE question to\n'
    '    # two agents whose covers sets do not overlap at all and get the same sources back from both. So: the same\n'
    '    # question to two disjoint agents must not give the same answer, and the agent that does not own the subject\n'
    '    # must say so and offer to pass the question on rather than answer from material that is not its own.\n'
    '    def ask_of(ag, q):\n'
    '        before = pg.locator("#%s-log .msg" % ag["id"]).count(); pg.click(\'[data-agenttab="%s"]\' % ag["id"]); pg.fill("#%s-q" % ag["id"], q); pg.click(\'[data-ask="%s"]\' % ag["id"])\n'
    '        pg.wait_for_function("([id,n])=>{const m=document.querySelectorAll(\'#\'+id+\'-log .msg\');return m.length>=n+2&&!m[m.length-1].classList.contains(\'typing\')}", arg=[ag["id"], before], timeout=240000)\n'
    '        return pg.locator("#%s-log .msg" % ag["id"]).last.text_content()\n'
    '    _pairs = [(x, y) for x in d["agents"] for y in d["agents"] if x["id"] < y["id"] and not (set(x["covers"]) & set(y["covers"])) and x["covers"] and y["covers"]]\n'
    '    DISJ = "two agents whose subjects do not overlap do not give the same answer to the same question, and the one that does not own it hands it over"\n'
    '    if _pairs:\n'
    '        ax, ay = max(_pairs, key=lambda p: len(p[0]["covers"]) + len(p[1]["covers"]))\n'
    '        _topic = next(n_ for n_ in nodes if n_["id"] == ax["covers"][0])["label"]\n'
    '        _qd = "what is " + _topic.lower() + "?"\n'
    '        dx = ask_of(ax, _qd); dy = ask_of(ay, _qd)\n'
    '        _owner_said = ("not in my subject" in dy) or ("Nothing in the book, course or chapter material answers that" in dy)\n'
    '        feat(DISJ, dx != dy and len(dx) > 40 and _owner_said, "%s asked %r -> %s || %s -> %s" % (ax["id"], _qd, dx[:60], ay["id"], dy[:60]))\n'
    '    else:\n'
    '        feat(DISJ, False, "this chapter has no two agents with disjoint slices, so the rule cannot be tested here")\n'
    '    pg.click(\'[data-agenttab="%s"]\' % a["id"])\n',
    tag="disjoint agents answer differently")

# ---- 1  a course learning outcome is reachable, but not through an agent's slice -------------------------------------
rep('    q_out = pg.evaluate("async(id)=>{const a=D.agents.find(x=>x.id===id);const r=await rank(a,\'which course learning outcome is about choosing libraries?\',8);return r.top.map(x=>x.c.label).join(\' | \')}", a["id"])\n'
    '    feat("a course question reaches the course ontology", "LO-1" in q_out, q_out[:150])\n',
    '    # 9.25.0: a course learning outcome belongs to no concept of this chapter, so after the slice repair of template\n'
    '    # 9.24.0 it is in no subject agent\'s slice - correctly. The 9.24.0 form of this check required an agent to\n'
    '    # return it, which is the leak that repair removed, so it asserted the defect. Three things must hold instead:\n'
    '    # the agent does not reach it, the page-wide passage search does, and (below, with the guide) the student has a\n'
    '    # route to it from the page.\n'
    '    CQ = "which course learning outcome is about choosing libraries?"\n'
    '    q_out = pg.evaluate("async([id,q])=>{const a=D.agents.find(x=>x.id===id);const r=await rank(a,q,8);return r.top.map(x=>x.c.label).join(\' | \')}", [a["id"], CQ])\n'
    '    q_wide = pg.evaluate("async q=>{const r=await rank({covers:[]},q,8);return r.top.map(x=>x.c.label).join(\' | \')}", CQ)\n'
    '    feat("a subject agent does not answer a course-level question from material outside its own slice", "LO-1" not in q_out, q_out[:150])\n'
    '    feat("a course learning outcome is reachable: the page-wide passage search over the book, the course, this chapter and the research record finds it", "LO-1" in q_wide, q_wide[:150])\n',
    tag="course outcome reachable, not via an agent")

# ---- 6  the guide is the route a student has to a course-level question ----------------------------------------------
rep('    feat("the guide introduces the right agent and hands the question over", target in sugg and pg.locator(\'[data-conv="%s"]\' % target).is_visible(), "suggested: " + ", ".join(sugg))\n',
    '    feat("the guide introduces the right agent and hands the question over", target in sugg and pg.locator(\'[data-conv="%s"]\' % target).is_visible(), "suggested: " + ", ".join(sugg))\n'
    '    # 9.25.0: the student\'s own route to course-level material. No subject agent owns a course learning outcome\n'
    '    # after the slice repair, so the guide must put the course material in front of the student itself - template\n'
    '    # 9.25.0 shows the page-wide passage search beside the agents it introduces and answers from it when no agent\n'
    '    # qualifies at all. It must cite the outcome, say why no agent owns it, and never claim the material is absent.\n'
    '    pg.click(\'[data-agenttab="guide"]\'); _gl = pg.locator("#guide-log .msg").count(); pg.fill("#guide-q", CQ); pg.press("#guide-q", "Enter")\n'
    '    pg.wait_for_function("n=>{const m=document.querySelectorAll(\'#guide-log .msg\');return m.length>=n+2&&!m[m.length-1].classList.contains(\'typing\')}", arg=_gl, timeout=240000)\n'
    '    _ga = pg.locator("#guide-log .msg").last; _gtxt = _ga.text_content()\n'
    '    _gsrc = " | ".join(_ga.locator(".src").nth(k).text_content() for k in range(_ga.locator(".src").count()))\n'
    '    _g_cites = "LO-1" in (_gsrc + _gtxt)\n'
    '    _g_says_why = ("belongs to no single subject" in _gtxt) or ("No single subject of this chapter owns that" in _gtxt)\n'
    '    _g_not_denied = "it lies outside this chapter" not in _gtxt\n'
    '    feat("a student can reach a course learning outcome from the guide: it shows the page-wide passage search, says why no agent owns the question, and never claims the material is not here",\n'
    '         _g_cites and _g_says_why and _g_not_denied, ("cites %s | why %s | not-denied %s | " % (_g_cites, _g_says_why, _g_not_denied)) + _gtxt[:110].replace("\\n", " "))\n'
    '    pg.click(\'[data-agenttab="%s"]\' % target)  # the guide question above selected the guide; the follow-up block below needs the handed-over agent back in view\n',
    tag="guide route to a course outcome")

# ---- 7  the vocabulary tab explains every term, in this course's own words -------------------------------------------
rep('    feat("About: how it works, agents & tools with the corpus, mission & backlog with course outcomes, provenance & known limits", len(howto) > 400 and arch_rows == files and "Mission" in mission and "LO-1" in mission and limits >= 4, "corpus rows %d, limits %d" % (arch_rows, limits))\n',
    '    feat("About: how it works, agents & tools with the corpus, mission & backlog with course outcomes, provenance & known limits", len(howto) > 400 and arch_rows == files and "Mission" in mission and "LO-1" in mission and limits >= 4, "corpus rows %d, limits %d" % (arch_rows, limits))\n'
    '    # 9.25.0: the audit\'s F-D5 and the owner\'s standing rule - every term and tool the page uses must itself be\n'
    '    # explained, in comprehensive paragraphs of full sentences rather than one line. Each term gets its own\n'
    '    # heading, and each heading must be followed by a real explanation. The second assertion keeps the sibling\n'
    '    # Blockchain course\'s examples out of a Python course\'s page, which is what template 9.25.0 repaired.\n'
    '    view("words"); wtxt = pg.text_content(\'[data-pane="words"]\')\n'
    '    WTERMS = ["Ontology", "Knowledge graph", "Triple", "Taxonomy", "SPARQL", "Agent", "Semantic search", "Pyodide", "Class diagram", "Entity-relationship diagram"]\n'
    '    whead = pg.evaluate("()=>[...document.querySelectorAll(\'[data-pane=words] h3\')].map(e=>e.textContent.trim())")\n'
    '    wbody = pg.evaluate("()=>[...document.querySelectorAll(\'[data-pane=words] h3\')].map(e=>{let n=e.nextElementSibling,t=\'\';while(n&&n.tagName!==\'H3\'){t+=n.textContent+\' \';n=n.nextElementSibling}return t.trim()})")\n'
    '    w_missing = [t for t in WTERMS if not any(t.lower() in x.lower() for x in whead)]\n'
    '    w_thin = [whead[i] for i, t in enumerate(wbody) if len(t) < 200 or t.count(". ") < 1]\n'
    '    feat("the page explains its own vocabulary: every term and tool it uses has its own explanation, written as full sentences and not as a single line",\n'
    '         not w_missing and not w_thin and len(whead) >= len(WTERMS), "%d terms explained; missing %s; too thin %s" % (len(whead), w_missing, w_thin))\n'
    '    feat("the vocabulary is explained in this course\'s own terms, with no example borrowed from the sibling Blockchain course",\n'
    '         not re.search(r"(?i)bitcoin|satoshi|blockchain", wtxt), "%d characters of vocabulary" % len(wtxt))\n',
    tag="vocabulary tab explains every term")

# ---- 4  no visible SPARQL sample name carries a placeholder ----------------------------------------------------------
rep('    feat("choosing a SPARQL sample loads it at once; no Load sample button", sel_ok)\n',
    '    feat("choosing a SPARQL sample loads it at once; no Load sample button", sel_ok)\n'
    '    # 9.25.0: the audit\'s F-B6 - a sample whose visible option text still showed its raw {FIRST_LEAF} placeholder\n'
    '    # while the query behind it was substituted. This template has no placeholder to substitute, so the guard is\n'
    '    # cheap; its second half catches the fault this template did have, a sample name and query fixed to a class\n'
    '    # only chapter 1 defines, which answered "no" and taught nothing on the other four chapters.\n'
    '    samp_names = pg.evaluate("()=>[...document.querySelectorAll(\'#sqsamp option\')].map(o=>o.textContent)")\n'
    '    samp_ph = [s for s in samp_names if re.search(r"\\{[A-Za-z_]+\\}", s)]\n'
    '    ask_name = next((s for s in samp_names if "define a class labelled" in s), "")\n'
    '    ask_named = re.search(r\'"([^"]+)"\', ask_name)\n'
    '    node_labels = set(n_["label"].lower() for n_ in nodes)\n'
    '    feat("no visible SPARQL sample name carries a template placeholder, and the sample that asks whether the chapter defines a class names one this chapter really defines",\n'
    '         not samp_ph and bool(ask_named) and ask_named.group(1).lower() in node_labels,\n'
    '         "%d samples; placeholders %s; ASK names %r" % (len(samp_names), samp_ph, ask_named.group(1) if ask_named else None))\n',
    tag="no placeholder in a sample name")

# ---- 2  the taxonomy's individuals are counted with their layer turned on --------------------------------------------
rep('    n_all = pg.locator("#taxo g.on").count(); n_cls = pg.locator("#taxo g.on.k-class").count(); n_ind = pg.locator("#taxo g.on.k-individual").count(); n_book = pg.locator("#taxo g.on.k-book").count()\n',
    '    # 9.25.0: template 9.24.0 opens the taxonomy with the Classes layer alone (audit F-B3), so the layers this check\n'
    '    # is about - individuals and book concepts under their class - are off when the view opens and must be turned on\n'
    '    # before they can be counted. The layer-removal count further down still falls, because it unchecks from here.\n'
    '    pg.locator(\'[data-okind="individual"]\').first.check(); pg.locator(\'[data-okind="book"]\').first.check(); pg.wait_for_timeout(900)\n'
    '    n_all = pg.locator("#taxo g.on").count(); n_cls = pg.locator("#taxo g.on.k-class").count(); n_ind = pg.locator("#taxo g.on.k-individual").count(); n_book = pg.locator("#taxo g.on.k-book").count()\n',
    tag="taxonomy layers on before counting")

# ---- 3  the "All chapters" link is required exactly when a chapter index exists --------------------------------------
rep('    feat("a link \'All chapters\' leads back to the index (index.html in the same folder)", ix.count() == 1 and ix.get_attribute("href") == "index.html" and ix.is_visible())\n',
    '    # 9.25.0: repair 8 of template 9.24.0 (audit F-B5) shows this link only when a chapter index really sits beside\n'
    '    # the page. None does in this repository, and a link to a file that is not there is a dead link to a student, so\n'
    '    # the 9.22.0 form of this check - the link, unconditionally - asserted the defect. The conditional holds instead.\n'
    '    ix_named = pg.evaluate("()=>String(D.index_page||\'\')")  # the value the template itself decides by, not a copy of it\n    want_ix = bool(ix_named)\n'
    '    feat("a link \'All chapters\' is shown exactly when a chapter index sits beside the page, and never as a dead link",\n'
    '         (ix.count() == 1 and ix.get_attribute("href") == ix_named and ix.is_visible()) if want_ix else ix.count() == 0,\n'
    '         "index named by the page: %r" % ix_named)\n',
    tag="All chapters link is conditional")

open(out, "w", encoding="utf-8").write(h)
print("written", out, os.path.getsize(out), "bytes")
for t in APPLIED:
    print("   applied:", t)
