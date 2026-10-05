#!/usr/bin/env python3
"""SEN0414 page template 9.25.0, from 9.24.0 - the later repairs of SEN0401's chain that are genuine defects of THIS
template too, each one verified against this template's own bytes and this course's own data before it was ported,
plus two defects of this template that SEN0401's chain does not have.

WHY THERE IS ANYTHING LEFT TO PORT. The two courses share this template. SEN0414's 9.24.0 carries the first batch of
the adversarial audit's shared-template repairs (the same set as SEN0401's 9.28.0). SEN0401's chain then went on to
9.29.0 (four more repairs, found by its own page test after 9.28.0) and 9.32.0 (the guide's page-wide route, which
supersedes the intermediate 9.30.0 and 9.31.0 - both of those put an `await` inside the expression assigned to the
guide bubble's innerHTML after the typing class had already been cleared, so the bubble read "finding the right
person" while announcing itself finished). Those later repairs never reached this chain. Each candidate below was
checked here, not assumed from the sibling's header.

WHAT CHANGES, AND WHY

 1. THE RESOURCES PANE SHOWS EVERY CHECKED RESOURCE, NOT ONLY THE FIVE KINDS THE TABLE NAMES (SEN0401 9.29.0, its
    repair 1 - and a live defect of this course, not only of that one). The pane took its headings from RKIND, which
    named documentation, PEPs, interactive tools, videos and discussions, and silently dropped a link of any other
    kind: `const kinds=Object.keys(RKIND).filter(...)` can only ever list kinds the table already knows. Measured in
    this repository, not assumed: every one of chapters 1 to 5 carries exactly one resource of kind `deck` - the
    chapter's own lecture deck, the .pptx one directory above the page, with its slide count and its talk-track note
    - and the pane rendered none of them. The last full page test of chapter 1 recorded it as a failure in those
    words ("14 links, 30 search rows" against 15 resources in the page data). The kind table now names every kind
    the two courses really use, each with its own heading and the chapter deck among them, and a kind that is in the
    data but not in the table is still shown, under a heading built from the kind's own word, so no checked resource
    can be hidden by a missing table entry again. Nothing about the links themselves changes: each still opens in a
    new tab with rel="noopener", the pane still states the date they were checked, and it still says plainly that
    the searches below it are searches and not recommendations.
 2. THE TAXONOMY IS EXPLAINED IN ONE PARAGRAPH, NOT A SENTENCE ABOVE A PARAGRAPH (SEN0401 9.29.0, its repair 2).
    Repair 14 of this chain's 9.24.0 - the page explains its own vocabulary - added a one-sentence note saying what a
    taxonomy is and placed it above the paragraph that already explained the view, so the pane opened with two
    separate explanations of the same diagram, the first of them a single sentence. That is the shape the owner's own
    rule rejects twice over: explanations are comprehensive, cohesive paragraphs of full sentences, and a screen does
    not carry the same thing twice. Verified present here before porting (the one-sentence note, then the legend row,
    then the narrative), and verified to bite: the page test's narrative check reads the pane's first note and
    measured 109 characters where it requires more than 350. The sentence is now the opening of the one narrative
    paragraph, which keeps the link to "Words we use" and everything it already said about the root, the dashed book
    links, the layer boxes and Show all.
 3. A QUESTION'S STEM IS THE STEM ITS OWN BANK ITEM CARRIES (SEN0401 9.29.0, its repair 3). Repair 13 of this chain's
    9.24.0 qualifies a stem that more than one bank item shares with the concept it asks about, but it did so only on
    the way out of qMake: the bank in memory kept the bare stem, so the browser of questions, the generated question
    and the mock exam could show stems that match no item of the bank they came from. The qualification is now
    applied to the bank itself, once, as it is loaded. Stated honestly, because it was measured: this is a LATENT
    defect for SEN0414 as its banks stand today - chapters 1 to 5 hold 109, 131, 143, 142 and 128 items with zero
    shared stems between them, because this course's own stems already name their concept ("Integer: what does this
    program print?"), so bankStem returns every stem unchanged and the divergence cannot currently be observed. It is
    repaired here anyway, for two reasons that are not judgement calls: the two chains must not diverge in a file they
    share, and a future bank that gains two items with one stem would reintroduce the defect silently. bankStem is
    keyed on the stem it was given, so an already-qualified stem is returned untouched and nothing is qualified
    twice. The bank files on disk are not touched.
 4. THE GUIDE REACHES COURSE-LEVEL MATERIAL INSTEAD OF DENYING IT EXISTS (SEN0401 9.32.0, in its shippable form).
    Repair 1 of this chain's 9.24.0 restricted every subject agent's retrieval to the passages its own `covers` set
    reaches - the owner's standing rule and the audit's most serious finding. A course learning outcome, however, is
    a passage of the course ontology that belongs to no concept of the chapter, so after that repair it sits in no
    agent's slice, which is correct: an agent must not answer from material it does not own. The guide was left with
    nothing for such a question. Confirmed here, not taken on handover: this template's `route` is the identical
    code, down to the sentence "No agent here covers that - it lies outside this chapter's book, course and research
    material", which is false of exactly this case - the course ontology is one of the files this page embeds and the
    outcome is in the corpus. The page test of chapter 1 fails on it today, in its own words ("a course question
    reaches the course ontology"). The guide now carries both halves of the repair: under a sentence that says why -
    a question about the course itself belongs to no single subject of the chapter, so no agent owns it - it lists
    what the unrestricted page-wide search over the book, the course, this chapter, this page and the research record
    found for the same words, each passage cited and openable in the detail card, and names the page search (Ctrl+K)
    as the place the same search lives; and when no agent clears the guide's bar at all it answers from that same
    search instead of asserting the material is not here, saying nothing was found only when the search really found
    nothing. The whole answer is computed before the bubble is touched, so nothing can read a finished bubble that
    has not been written yet. No agent's ranking changes, no agent is given a passage outside its slice, and no new
    threshold is stipulated: the bar is the 0.33 the guide already applies to its best agent.
 5. THE PAGE EXPLAINS SEMANTIC SEARCH WITH AN EXAMPLE FROM THIS COURSE (a defect of this template alone). The "Words
    we use" text repair 14 of 9.24.0 brought over is byte-identical to SEN0401's - both blocks are the same 5,673
    characters - and its Semantic search paragraph teaches the idea with "how is new bitcoin created?" finding a
    passage that only ever says "mining". That is the sibling course's subject matter sitting in a Python course's
    page, where a student has met neither word; under scope discipline a SEN0401 example has no business in a SEN0414
    artifact. The paragraph now makes the same point with this course's own material - a question about adding an
    item to a list finding a passage that only says "append" - and explains the embedding and the keyword fallback as
    before. Nothing else in the vocabulary tab changes: it already explains ontology, knowledge graph, triple,
    taxonomy, SPARQL, agent, semantic search, Pyodide, class diagram and entity-relationship diagram.
 6. THE SPARQL SAMPLE ASKS ABOUT A CLASS THE CHAPTER IT IS ON REALLY DEFINES (a defect of this template alone, and
    this course's own form of the audit's F-B6). The audit found that SEN0401's sixth sample showed its raw
    {FIRST_LEAF} placeholder in the visible option while the query behind it was substituted correctly. That exact
    defect cannot occur here and is NOT ported: checked, not assumed - `SPQ_FIX` and `FIRST_LEAF` each occur zero
    times in course_page_template_v9_24_0.html, this template's sample list is literal, and no sample name contains a
    placeholder. Checking it, however, surfaced the reverse fault in the same sample: its name and its query were
    hard-coded to the class "Precedence", which only chapter 1 defines. Measured over this course's five built
    chapters - chapter 1 defines Precedence; chapters 2, 3, 4 and 5 do not - so on four of the five pages the one
    sample meant to demonstrate an ASK query asked whether the chapter defines a class belonging to a different
    chapter, and truthfully answered no, teaching nothing. The sample now names the chapter's own first leaf concept,
    in the visible name and in the query alike, exactly as the sibling chain's substitution does (Integer on chapter
    1, Boolean value on chapter 2, Loop on chapter 3, Def statement on chapter 4, Bug on chapter 5), so the sample
    demonstrates an ASK that answers yes on every chapter. A name built from the chapter's own data also cannot carry
    a placeholder, which is what the page test now asserts.
 7. THE VERSION MARKERS. The template, and the pages built from it, say 9.25.0.

NOT PORTED, EACH WITH ITS REASON

  * The audit's F-B6 itself (`SPQ_FIX` over a sample's visible name): there is nothing to substitute here. See 6.
  * Repair 13 of 9.24.0 / repair 14 of SEN0401's 9.28.0 (a shared question stem qualified by its concept) and repair
    15 / F-D5 (the "Words we use" vocabulary tab): both are already IN this template, applied by
    template_patch_v9_24_0.py as its items 13 and 14. Verified in the bytes - `bankStem` is defined and used, and the
    tab exists with ten terms - so what remained was the follow-on fix (3) and the scope-foreign example (5), not
    the repairs themselves.
  * SEN0401's 9.30.0 and 9.31.0: superseded by its own 9.32.0, which is the form ported in 4.

usage: template_patch_v9_25_0.py [IN.html OUT.html]"""
__version__ = "9.25.0"
import os, sys

here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_24_0.html")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_25_0.html")
h = open(src, encoding="utf-8").read()
APPLIED = []


def rep(a, b, n=1, tag=""):
    global h
    assert h.count(a) == n, ("anchor not found %dx: %r (found %d)" % (n, a[:90], h.count(a)))
    h = h.replace(a, b)
    APPLIED.append(tag or a[:40])


# ---- 1  the resources pane shows every checked resource -------------------------------------------------------------
rep("RKIND={documentation:'\U0001F4D8 Documentation',pep:'\U0001F4DC PEPs',interactive:'\U0001F9EA Interactive tools',"
    "video:'\U0001F3A5 Videos',discussion:'\U0001F4AC Discussions'}",
    # 9.25.0 - every kind of resource the two courses really use has its own heading here, in the order the headings
    # are shown, the chapter's own lecture deck among them; a kind the data carries and this table does not is still
    # rendered, under a heading made from its own word, so a missing entry can hide nothing.
    "RKIND={deck:'\U0001F39E Chapter deck',documentation:'\U0001F4D8 Documentation',pep:'\U0001F4DC PEPs',"
    "standard:'\U0001F4D0 Standards and specifications',paper:'\U0001F4C4 Papers',"
    "reference:'\U0001F4DA Reference works',wiki:'\U0001F310 Community wikis',"
    "data:'\U0001F5C4 Data sources',tool:'\U0001F9F0 Tools',library:'\U0001F4E6 Libraries',"
    "interactive:'\U0001F9EA Interactive tools',video:'\U0001F3A5 Videos',discussion:'\U0001F4AC Discussions'}",
    tag="resources RKIND widened, chapter deck named")

rep("const kinds=Object.keys(RKIND).filter(k=>D.resources.some(r=>r.kind===k));",
    "const RKLAB=k=>RKIND[k]||('\U0001F517 '+String(k).charAt(0).toUpperCase()+String(k).slice(1));\n"
    " const kinds=[...Object.keys(RKIND).filter(k=>D.resources.some(r=>r.kind===k)),"
    "...[...new Set(D.resources.map(r=>r.kind))].filter(k=>!RKIND[k])];",
    tag="resources kinds include kinds the table does not name")

rep("kinds.map(k=>'<h3>'+RKIND[k]+'</h3>'+resList(D.resources.filter(r=>r.kind===k))).join('')",
    "kinds.map(k=>'<h3>'+RKLAB(k)+'</h3>'+resList(D.resources.filter(r=>r.kind===k))).join('')",
    tag="resources headings")

# ---- 2  the taxonomy is explained in one paragraph ------------------------------------------------------------------
rep("<h2>\U0001F333 Chapter taxonomy</h2><p class=\"note\">A taxonomy is the \\u201cis a kind of\\u201d part of the "
    "chapter\\u2019s ontology, drawn as one tree. '+WORDLINK+'</p><p class=\"legend\">",
    "<h2>\U0001F333 Chapter taxonomy</h2><p class=\"legend\">",
    tag="taxonomy duplicate note removed")

rep("<p class=\"note\">The chapter\\'s taxonomy as one tree, with its leaves. The root is the chapter;",
    "<p class=\"note\">A taxonomy is the \\u201cis a kind of\\u201d part of the chapter\\u2019s ontology, drawn here as "
    "one tree: the chapter\\'s taxonomy with its leaves. The root is the chapter;",
    tag="taxonomy narrative opening")

rep("A worked example is named by what it shows; its code is in the card on the right.</p>",
    "A worked example is named by what it shows; its code is in the card on the right. '+WORDLINK+'</p>",
    tag="taxonomy narrative keeps the words link")

# ---- 3  a question's stem is the stem its own bank item carries ------------------------------------------------------
rep("function bankStem(b){if((BSTEM[b.q]||0)<2)return b.q;const n=byId[b.concept];const k=b.q+'\\u0000'+b.concept;\n"
    " return b.q+(n?' \\u2014 '+n.label:'')+(BSEQ[k]>1?' ('+b._seq+')':'')}",
    "function bankStem(b){if((BSTEM[b.q]||0)<2)return b.q;const n=byId[b.concept];const k=b.q+'\\u0000'+b.concept;\n"
    " return b.q+(n?' \\u2014 '+n.label:'')+(BSEQ[k]>1?' ('+b._seq+')':'')}\n"
    "// 9.25.0 - the qualified stem is written into the bank itself, once, so every place that reads an item - the\n"
    "// browser of questions, a generated question, the mock exam - shows the stem the item carries. bankStem is\n"
    "// keyed on the stem it was given, so asked again for an already-qualified stem it returns it unchanged; with\n"
    "// this course's banks, whose stems are already distinct, every stem is returned untouched.\n"
    "BANK.forEach(b=>{b.q=bankStem(b)});",
    tag="bank stem written into the bank")

# ---- 4  the guide reaches course-level material instead of denying it exists ----------------------------------------
rep(" try{const g=(await routeScores(q)).filter(x=>x.best>0).slice(0,3);h.className='msg agent';\n"
    "  h.innerHTML=g.length&&g[0].best>=0.33?'These agents know most about that:'",
    # 9.25.0 - the bubble keeps its "finding the right person" text AND its typing class until the whole answer,
    # page-wide passages included, is ready: both are replaced in the same step, so nothing can read a finished
    # bubble that has not been written yet.
    " try{const g=(await routeScores(q)).filter(x=>x.best>0).slice(0,3);\n"
    "  const body=g.length&&g[0].best>=0.33?'These agents know most about that:'",
    tag="guide bubble written in one step")

rep("'</button></div>').join(''):'No agent here covers that - it lies outside this chapter\\u2019s book, course and "
    "research material.'}",
    "'</button></div>').join('')+await guidePassages(q,false):await guidePassages(q,true);\n"
    "  h.className='msg agent';h.innerHTML=body}",
    tag="guide answer reaches the page-wide passage search")

rep("async function route(){",
    # 9.25.0 - one helper for both cases. alone=true is the case where no agent's slice qualified at all: the guide
    # answers from the page-wide search itself. alone=false is the ordinary case: the agents are introduced first and
    # these passages are offered beside them, because an agent can clear the guide's bar on a book or research
    # passage that merely mentions one of its concepts while the passage the student wants - a course learning
    # outcome, which belongs to no concept and so to no slice - sits just below it.
    "async function guidePassages(q,alone){const {top}=await rank({covers:[]},q,5);const rows=top.filter(x=>x.score>0);\n"
    " const ok=rows.length&&rows[0].score>=0.33;\n"
    " if(!ok)return alone?'No agent here covers that, and a search of every passage of the book, the course, this "
    "chapter and the research record finds nothing about it either.':'';\n"
    " const lead=alone?'No single subject of this chapter owns that, so I will not hand it to an agent whose own "
    "material does not answer it. The course, the book and the research record this page carries do speak to it, "
    "though: these are the passages that match, and you can open any of them here.'\n"
    "  :'Whichever of them you ask, these passages of the book, the course, this chapter and the research record "
    "match your words as well. A question about the course itself - one of its learning outcomes, for instance - "
    "belongs to no single subject of this chapter, so no agent owns it and it is found here rather than with an "
    "agent.';\n"
    " return '<p class=\"note\">'+lead+' Open a passage to read it; the page search (Ctrl+K) runs the same search "
    "over all of them.</p>'+sourcesHtml(rows,'the page-wide passage search: every passage of the book, the course, "
    "this chapter, this page and the research record, ranked by meaning, with no agent\\u2019s slice applied - '"
    "+rows.length+' of '+KIT.chunks.length+' passages shown')}\n"
    "async function route(){",
    tag="guidePassages helper")

# ---- 5  semantic search is explained with an example from this course -----------------------------------------------
rep("<p>Semantic search ranks passages by what they mean rather than by the words they happen to share with your "
    "question, which is what lets \\u201chow is new bitcoin created?\\u201d find a passage that only ever says "
    "\\u201cmining\\u201d.",
    # 9.25.0 - the example is this course's own. "how is new bitcoin created?" belongs to the sibling Blockchain
    # course, whose template this text was shared from, and names two things a Python student has never met here.
    "<p>Semantic search ranks passages by what they mean rather than by the words they happen to share with your "
    "question, which is what lets \\u201chow do I add an item to the end of a list?\\u201d find a passage that only "
    "ever says \\u201cappend\\u201d.",
    tag="words: semantic search example is a Python one")

# ---- 6  the ASK sample names a class this chapter really defines ----------------------------------------------------
rep("[\'Does the chapter define a class labelled \"Precedence\"?\',PFX+\'ASK { GRAPH ?g { ?c a owl:Class ; "
    "rdfs:label ?l . FILTER(LCASE(STR(?l)) = \"precedence\") } }\']];",
    # 9.25.0 - the name and the query were fixed to "Precedence", a class only chapter 1 defines, so on chapters 2 to
    # 5 the one ASK sample asked about another chapter's class and answered no. Both halves now name this chapter's
    # own first leaf concept, read from the page data, so the sample demonstrates an ASK that answers yes wherever it
    # is shown - and a name built from the chapter's own data can carry no placeholder.
    "[\'Does the chapter define a class labelled \"\'+FIRST_LEAF_LABEL+\'\"?\',PFX+\'ASK { GRAPH ?g { ?c a owl:Class ; "
    "rdfs:label ?l . FILTER(LCASE(STR(?l)) = \"\'+FIRST_LEAF+\'\") } }\']];",
    tag="ASK sample names this chapter's own first leaf")

rep("const PFX='PREFIX rdfs:",
    "// 9.25.0 - the leaf concept the ASK sample asks about is this chapter's own, not a sibling chapter's.\n"
    "const FIRST_LEAF_LABEL=String(((D.nodes.find(n=>+n.level>=3)||D.nodes[0]||{}).label)||'').replace(/\"/g,'');\n"
    "const FIRST_LEAF=FIRST_LEAF_LABEL.toLowerCase();\n"
    "const PFX='PREFIX rdfs:",
    tag="FIRST_LEAF read from the page data")

# ---- 7  the version markers -----------------------------------------------------------------------------------------
rep("<!-- course_page_template version 9.24.0:",
    "<!-- course_page_template version 9.25.0: the Resources pane shows every kind of checked resource, the chapter's "
    "own lecture deck included; the taxonomy is explained in one paragraph instead of a sentence above a paragraph; a "
    "question's stem is written into the bank itself; the guide shows the page-wide passage search over the book, the "
    "course, this chapter and the research record beside the agents it introduces and answers from it when no agent's "
    "slice qualifies, so a question about the course itself reaches the course material; semantic search is explained "
    "with a Python example; the ASK sample names a class this chapter really defines. Earlier: -->"
    "<!-- course_page_template version 9.24.0:",
    tag="version comment")

# The page's own <meta name="version"> is the build's __PAGEVERSION__ placeholder, filled from PAGE_VER, so the
# template carries no second version string to bump here.

open(out, "w", encoding="utf-8").write(h)
print("written", out, os.path.getsize(out), "bytes")
for t in APPLIED:
    print("   applied:", t)
