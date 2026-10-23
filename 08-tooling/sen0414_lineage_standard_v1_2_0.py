#!/usr/bin/env python3
"""sen0414_lineage_standard v1_2_0 (over v1_1_0: the backlog event adds the design-level class model that the data concern of the new stories owes; events change, retract, scope, goal and objective are those of v1_1_0) - change route (rulings G105, G120, G125, G127, G133, G136, G137) for the owner's request of 2026-10-23 08:57 Istanbul (05:57 UTC): the decks and the interactive pages of
chapters 6 (Lists), 7 (Dictionaries and Structuring Data) and 8 (Strings and Text Editing) of SEN0414 must meet the same written teaching-material standard as the sibling course SEN0401 chapters 5 and 6,
above all: the code on the slides appears exactly, in the same order, in a chapter-code tab of the page that can run it.
Modelled on the sibling's change route (sen0401_lineage_remedy56 / remedy56_rev), written for this register: the successor lineage ex:Lineage2 (Backlogged) takes the new deliverables by a
StageRevision from its Scope stage; the Done stories of chapters 7 and 8 (Lineage2) and of chapter 6 (the achieved first lineage) are never edited (G125): the new work is new stories.
One call = one new register file = one event; the caller validates (backlog_validate_v1_17_0.py) and commits and pushes each alone.
Events, in order:  change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV      (PREV = the commit that closed the previous event)
Nothing is begun here: work begun is recorded at the real start of each executor session, by its own later version.
Usage: sen0414_lineage_standard_v1_2_0.py EVENT [PREV_COMMIT]"""
__version__ = "1.2.0"
import datetime, glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_outscope_stages_v1_1_0 as S
import importlib.util
import rdflib

FW = "/home/claude/altunelyusuf/backlog-roadmap-framework"      # the framework checkout of this machine (the stage writer v1_1_0 names a path that does not exist here, and the digest tool v1_8_0 is superseded by v1_9_0)


def _pv():
    spec = importlib.util.spec_from_file_location("pv", FW + "/03-tooling/backlog_pipeline_verify_v1_9_0.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    tb = sorted(glob.glob(FW + "/01-ontologies/backlog_tbox_v*.ttl"), key=lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()])[-1]
    m.STAGE_TYPES = m._load_stage_types(tb, table="v1")      # this register declares no later digest table, so the validator reads table v1
    return m


S._pv = _pv

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIN = os.path.join(REPO, "07-lineage")
BASE = "http://example.org/sen0414-slides-lineage"
EXEC = "ex:Executor_ClaudeCodeSession"
ITER = "ex:Iter_18"; REV = "ex:Revision_Lineage2_Scope1"; CR = "ex:CR2_Standard"; IA = "ex:IA2_Standard"; SCOPE = "ex:Scope2"
ACTIVE = ["ex:Out2_Scope", "ex:Out2_Goal", "ex:Out2_Objective", "ex:Out2_Backlog"]
OUT = {"Scope": "Out2_ScopeR1", "Goal": "Out2_GoalR1", "Objective": "Out2_ObjectiveR1", "Backlog": "Out2_BacklogR1"}
NEWB = "ex:" + OUT["Backlog"]; OLDB = "ex:Out2_Backlog"
ITER_DAYS = 7
CHS = (("06", "6", "Lists"), ("07", "7", "Dictionaries and Structuring Data"), ("08", "8", "Strings and Text Editing"))
WHEN = "Friday 2026-10-23 08:57 Istanbul (05:57 UTC)"


def ver(p):
    return [int(v) for v in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]


def newest():
    return sorted(glob.glob(os.path.join(LIN, "sen0414_slides_lineage_v*.ttl")), key=ver)[-1]


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def lit(s):
    return '"%s"' % esc(s)


def write_new(src, text, comment):
    v = ver(src); cur = "%d.%d.%d" % tuple(v); nxt = "%d.%d.0" % (v[0], v[1] + 1)
    t = re.sub(r'owl:versionInfo "%s" ; owl:versionIRI <[^>]*> ; owl:priorVersion <[^>]*> ;' % re.escape(cur),
               'owl:versionInfo "%s" ; owl:versionIRI <%s/%s> ; owl:priorVersion <%s/%s> ;' % (nxt, BASE, nxt, BASE, cur), text, count=1)
    assert t != text, "header not found"
    ident = 'dcterms:identifier "sen0414_slides_lineage" ;'
    assert ident in t
    t2 = t.replace(ident, ident + '\n    rdfs:comment "%s (%s): %s"@en ;' % (nxt, now()[:10], esc(comment)), 1)
    out = os.path.join(LIN, "sen0414_slides_lineage_v%s.ttl" % nxt.replace(".", "_"))
    assert not os.path.exists(out), out
    open(out, "w", encoding="utf-8").write(t2)
    return out


def fill_re(t, name, commit):
    pat = re.compile(r'(%s a backlog:StageOutput ;.*?backlog:closedAtCommit )"PENDING"' % re.escape(name), re.S)
    assert pat.search(t), "no PENDING on " + name
    return pat.sub(lambda m: m.group(1) + '"%s"' % commit, t, count=1)


def out_new(t, stage, consumes):
    return ('\nex:%s a backlog:StageOutput ;\n    rdfs:label "Closure of the %s stage of the second lineage, rebuilt by the stage revision for the teaching-material standard of chapters 6 to 8"@en ;\n    backlog:belongsToLineage ex:Lineage2 ;\n'
            '    backlog:outputOfStage backlog:Stage_%s ;\n    backlog:consumesOutput ex:%s ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (OUT[stage], stage, stage, consumes, S.digest(t, stage))


# ------------------------------------------------------------------ the owner's words, the facts, the standard
OWNER_ACT = ("Owner's request of %s, relayed by the course coordinator in the assignment to the lineage agent and recorded here as relayed (a statement of its content, not a verbatim quotation, because the lineage agent holds the assignment, not a transcript of the owner's message): "
             "the PPT decks and interactive HTML pages of SEN0414 chapters 6 (Lists), 7 (Dictionaries) and 8 must meet the same standards as the sibling course SEN0401 chapters 5 and 6 just delivered, especially that the code on the slides appears exactly, in the same order, "
             "in a special 'chapter code' tab of the page that can run it. The request is urgent: the owner's class material is needed as soon as possible, and decks and pages ship chapter by chapter as each is controlled. "
             "The request is direction from the owner and authorises the scope; the length of the iteration remains his to decide. Under the standing rule that work following the owner's direction is recorded as owner-directed, it is not listed as an open owner confirmation." % WHEN)
FACTS = ("MEASURED FACTS (the lineage agent, read-only, 2026-10-23; tools: python-pptx 1.0.2 and Playwright 1.56.0; the deck figures come from a straight substitution port of the sibling's deck standard check made in the lineage agent's scratch folder, outside the repository, "
         "so the independent tool the first task writes must reproduce or explain every number below; a difference is reported, not adjusted). "
         "DECKS. Chapter 6 (03-materials/ch06/SEN0414_Ch06_Lists_3e_v2_0_0.pptx): 26 slides, 12 code slides, 3 native charts, 27 research concepts; elements failing: D1 (25 of 26 slides numbered; the first is not), D2 (longest box 102 words, 17 boxes over 30), "
         "D3 (3 of 12 code slides carry both the explanation and a visual result), D4 (12 of 27 key concepts have an analogy), D5 (0 of 4 story slides complete), D7 (25 slides with notes over 60 words, longest 240), D10 (0 of 3 dividers complete), D11 (15 of 27 concepts on a slide = 55.6 percent); D6, D8, D9, D12 pass. "
         "Chapter 7 (03-materials/ch07/SEN0414_Ch07_Dictionaries_3e_v1_0_0.pptx): 26 slides, 9 code slides, 1 native chart, 34 concepts; D1, D2 (longest 130 words), D3 (0 of 9), D4 (0 of 34), D5 (0 of 4), D7 (longest note 168 words), D11 (17 of 34 = 50.0 percent) fail; D10 not measured (no divider found); D6, D8, D9, D12 pass. "
         "Chapter 8 (the only deck, 08-tooling/ch08-deck/sen0414_ch08_deck_v1_0_0.pptx; 03-materials/ch08 holds no deck): 25 slides, 13 code slides, 0 native charts, 57 concepts; D1, D2 (longest 90 words), D3 (0 of 13), D4 (0 of 57), D5 (0 of 4), D7 (longest note 140), D11 (31 of 57 = 54.4 percent) fail; D10 not measured; D6, D8, D9, D12 pass. "
         "Discrepancy to be settled by the independent tool and not adjusted: the owner's own measurement of the chapter 8 deck reported a failure of D8 (resources slide); the port reads D8 PASS (a resources slide, slide 24, with 11 external links). "
         "PAGES (the shipped pages sen0414_chNN_page_v9_28_0.html, template line 9.50.0, page test 9.34.0). None of the three pages has a chapter-code tab (0 elements with data-pane chaptercode or data-cc-item), none has a panel level (0 elements with data-panel), none declares the page standard (no meta page-standard); "
         "at the first view the page does not scroll sideways at 390 px or at 1366 px (scrollWidth equals clientWidth in both), so the P1 overflow measure is not among the findings of this reading; the other page measures (P2 to P11) are taken by the page test the second task writes. "
         "TOOLS. The SEN0414 line has the template 9.50.0 (course_page_template_v9_50_0.html), the page builder v4_17_0, the page-data builder v2_24_0 and the page test 9.34.0 (with the exam-release checks, run by sen0414_page_test_run_v1_0_0.py against a TEST release key); "
         "it has no deck standard check, no deck overlap check and no chapter-code tab. The sibling course SEN0401 holds the finished versions of all of these (deck standard check v1_0_0, deck overlap check v1_0_0, page test 9.36.0, template 9.52.1, page builder v4_15_0, page-data builder v2_24_0), "
         "from the same ancestry as this line; they are ported as new-named copies, never edited. The chapter check v1_1_0 of this register reads the build checks of chapters 7 to 12 (chapter 6 has no entry in it).")
STD_D = ("DECK STANDARD (checked by the deck standard check, python-pptx 1.0.2, one named result per element): D1 every slide is numbered; D2 no text box over 30 words; D3 every code slide has a plain-language explanation beside the code and the executed result as a visual (a native chart, a table or a drawn diagram), not REPL text; "
         "D4 every key concept of the chapter has an everyday analogy slide or box (the key concepts are listed in the chapter research); D5 every story has who, what, when, where, why and how, a real picture and a live link; D6 every chart is a native chart object, no chart picture; D7 speaker notes at most 60 words per slide; "
         "D8 a resources slide with links; D9 one background scheme, no dark/light switching mid-deck; D10 every divider names its concepts with one line of meaning and one visual; D11 coverage: the share of the chapter research concepts that appear on a slide, stated as measured, not below 90 percent; D12 no code line wraps.")
STD_P = ("PAGE STANDARD (checked by the page test 9.36.0, Playwright 1.56.0): P1 no horizontal overflow at 390 px and at 1366 px; P2 the chapter-code tab lists the deck's examples by NAME in the deck's slide order, each runnable in the page with the chapter library defined in the page and its result visualised, "
         "and the code lives in the editor, not in the list; P3 tabs and left tree are synchronised and their label sets are disjoint or the tab bar is one row; P4 no third level of tabs, and one more level of panels so that one panel holds one concept; P5 a panel is at most 1.0 screen high at 1366x768; "
         "P6 no list repeated on one screen; P7 every diagram has zoom; P8 the top-level menu is uncrowded (at most 8 top-level tabs); P9 a text-size control and an adaptive layout at 390, 768 and 1366 px; P10 executed code results are visualised; P11 the page declares the standard and the examples equal the deck's code manifest.")
DOMC = ("DOM CONTRACT shared by the template, the page test and the page tasks (so the independent test can find what the template builds): the chapter-code tab is the tab with attribute data-pane=\"chaptercode\"; its list items have data-cc-item, the NAME of the example in data-cc-name and the deck's order number in data-cc-order; "
        "an item opens the example in the editor element data-cc-editor with a run button data-cc-run and a result element data-cc-result; the left tree items have role=treeitem and the tabs role=tab; one concept panel is an element with data-panel; the playground list items have data-pg-item and show names only; "
        "a page that follows the standard declares <meta name=\"page-standard\" content=\"9.52\">.")
CODE_SAME = ("THE OWNER'S CENTRAL REQUIREMENT: the code on the slides appears exactly, in the same order, in the chapter-code tab of the page, and runs there. The manifest 03-materials/chNN/page/chapter_code_chNN_v1_0_0.json is written from the deck (order, name, code, slide number, expected result); "
             "the deck check proves the manifest equals the deck's code boxes (text and order) and the page test proves the tab equals the manifest (names, order, code) and that each example runs and shows its result.")
COMMON = ("A committed file is never edited: every output is a new file with a new version number. STOP and report if the task cannot be satisfied without editing a committed file, a gate, a test or a threshold beyond the named new files. Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN); a skip is not a pass. "
          "The machine has 2 cores: browser tests run one at a time and no build runs beside them.")
VER = ("deck standard check v1_0_0 (python-pptx 1.0.2); deck overlap check v1_0_0; page test 9.36.0 (Playwright 1.56.0, new file over 9.34.0: every feature of 9.34.0 unchanged, the page-standard features added); page test 9.34.0; page template 9.52.1 (new file over 9.50.0); "
       "page builder v4_18_0 and page-data builder v2_25_0 (new files over v4_17_0 and v2_24_0); chapter check v1_1_0 of this register; RDODI gates v1_1_1; Playwright 1.56.0")
TOOLS = [("TS2_DeckStdCheck", "sen0414_deck_standard_check_v1_0_0.py", "deck standard check v1_0_0 (python-pptx 1.0.2; the elements D1 to D12, one named result each; port of the sibling's check)"),
         ("TS2_DeckOverlap", "sen0414_deck_overlap_check_v1_0_0.py", "deck overlap check v1_0_0 (shapes overlapping on a slide; port of the sibling's check)"),
         ("TS2_PageTest36", "sen0414_page_test_v9_36_0.py", "page test 9.36.0 (Playwright 1.56.0; new file over 9.34.0: all features of 9.34.0 unchanged, plus the features P1 to P6, P8, P9, P11 of the page standard)"),
         ("TS2_PageTemplate", "course_page_template_v9_52_1.html", "page template 9.52.1 (new file over 9.50.0: panel level, tab/tree rule, chapter-code tab, playground by name)"),
         ("TS2_PageBuilder", "sen0414_page_build_v4_18_0.py", "page builder v4_18_0 (new file over v4_17_0)"),
         ("TS2_PageData", "sen0414_page_data_v2_25_0.py", "page-data builder v2_25_0 (new file over v2_24_0: the chapter-code manifest and the panel data)"),
         ("TS2_PageTest34", "sen0414_page_test_v9_34_0.py", "page test 9.34.0 (the existing test of this line, run through sen0414_page_test_run_v1_0_0.py)"),
         ("TS2_ChapterCheck", "sen0414_lineage_chapter_check_v1_1_0.py", "chapter check v1_1_0 of this register (Research, Deck and Page of chapters 7 to 12)"),
         ("TS2_RdodiGates", "sen0414_rdodi_gates_v1_1_1.py", "RDODI gates v1_1_1 (Stages 1 to 3 of the chapter research)")]
NEWT = ["TS2_DeckStdCheck", "TS2_DeckOverlap", "TS2_PageTest36", "TS2_PageTemplate", "TS2_PageBuilder", "TS2_PageData"]
BASET = ["TS2_PageTest34", "TS2_ChapterCheck", "TS2_RdodiGates"]
SIB = "/home/claude/sen0401/08-tooling/"

PLAN = ("PLAN. Route: the deliverable (rebuilt decks and pages of chapters 6, 7 and 8, a chapter-code tab, a panel level, and the tools that measure the standard) is new content beside units that are Done "
        "(ST_Deck_Ch07, ST_Deck_Ch08, ST_Page_Ch07, ST_Page_Ch08 in this lineage; ST_Deck_Ch06 and ST_Page_Ch06 in the achieved first lineage): they stay Done and are not edited (G125, G133). The scope of this lineage excludes any change to the decks and pages of chapters 7 to 12 (ex:Excl2_NoRebuild), "
        "so new deliverables are a StageRevision from the Scope stage (G127), the route the sibling's register took for the same kind of request: this change request with its impact assessment first, then the retraction, four stage versions and a fill (seven versions), then the planning of the iteration and the brief per task. "
        "Order, as the owner's request and the tools demand: (1) the tooling port first - the deck standard check and deck overlap check (ST_Std_DeckTools), the page test 9.36.0, the page template 9.52.1 with its two builders and the regression control (ST_Std_PageTools); "
        "(2) then per chapter a deck story and a page story, chapter 6 first, then 7, then 8; the deck story of a chapter writes the chapter-code manifest the page story reads; chapters build in parallel where files do not collide (each chapter owns its own folders); "
        "a Verify task per deliverable is the controller's: it re-runs the checks, renders every slide, and records Done or NOT MET plainly. "
        "Stories (one acceptance criterion per unit, G133; each criterion names its tool and version, G136): ST_Std_DeckTools, ST_Std_PageTools, ST_Std_Deck_Ch06, ST_Std_Page_Ch06, ST_Std_Deck_Ch07, ST_Std_Page_Ch07, ST_Std_Deck_Ch08, ST_Std_Page_Ch08; 16 tasks, each naming its executor session. "
        "Iteration: a new iteration Iter_18 of constant length: 7 days (the class cadence: iteration end before the Friday class at 14:00 Istanbul), from the instant of the planning ceremony; the iterations of the first lineage were of changing length (end dates one to seven weeks out), "
        "so the length is the lineage agent's proposal to the owner, stated as a stipulation and kept constant from here on (G9). Estimated starts follow G120: hours after the executors begin (T0); nobody has witnessed a start; the real start is recorded at work begun. "
        "Not in the plan: any chapter other than 6, 7 and 8; the held rework of chapters 1, 2 and 4 (ex:Excl2_ReworkHeld stays); the Mission outcome and the Achieved status (the owner's act); any change to a gate, a test, a template or a threshold other than the NEW files named in the tasks.")


# ------------------------------------------------------------------ tasks and stories
def T(tid, title, ttype, deps, sess, est, hrs, note):
    return (tid, title, ttype, deps, sess, est, hrs, note)


TASKS = [
    T("TK_Std_DeckCheck", "Port the deck standard check and the deck overlap check to this course and measure the three existing decks with them", "Build", [], "SEN0414-I18-deckcheck", "T0", 1.5,
      "Write the NEW files 08-tooling/sen0414_deck_standard_check_v1_0_0.py and 08-tooling/sen0414_deck_overlap_check_v1_0_0.py as new-named copies of the sibling's tools (read-only sources: %ssen0401_deck_standard_check_v1_0_0.py and %sdeck_overlap_check_v1_0_0.py; only the root, the prefix, the brand mark and the file names change; any other change is stated and justified). "
      "One named, exit-coded result per element D1 to D12 for a deck given by chapter number, printing the measured number for each. %s Define each element's measure in the file header (as the sibling's header does). "
      "Prove them by running the deck check on the three existing decks (chapter 6: 03-materials/ch06/SEN0414_Ch06_Lists_3e_v2_0_0.pptx; chapter 7: 03-materials/ch07/SEN0414_Ch07_Dictionaries_3e_v1_0_0.pptx; chapter 8: 08-tooling/ch08-deck/sen0414_ch08_deck_v1_0_0.pptx) and the overlap check on the same decks: "
      "they must reproduce the measured facts of ex:IA2_Standard (slide counts, code slides, native charts, concept counts, the failing elements) or explain every difference, and settle the discrepancy on D8 of the chapter 8 deck by reading the slide. Keep the logs. "
      "Do not judge any deck you build: you build no deck in this iteration. The checks must also measure the code manifest equality (deck code boxes equal the manifest file, text and order) once a manifest exists. %s" % (SIB, SIB, STD_D, COMMON)),
    T("TK_Std_PageTest", "Write page test 9.36.0 with the page-standard features and measure the three existing pages with it", "Build", [], "SEN0414-I18-pagetest", "T0", 3.0,
      "Write the NEW file 08-tooling/sen0414_page_test_v9_36_0.py from sen0414_page_test_v9_34_0.py (which stays byte-identical), taking the page-standard features from the sibling's page test 9.36.0 (read-only: %ssen0401_page_test_v9_36_0.py): every feature of 9.34.0 stays textually identical; "
      "add the features P1, P2, P3, P4, P5, P6, P8, P9 and P11 of the page standard, which apply to a page that declares the standard (meta page-standard 9.52) and are reported as SKIP with the reason 'page does not declare the standard' otherwise; an environment switch FORCE_STANDARD=1 applies them to any page. "
      "%s %s %s Show: a unified diff against 9.34.0, and the proof that the set of old feature texts is equal. Baseline: run it with FORCE_STANDARD=1 on the three existing pages (chapters 6, 7 and 8, page v9_28_0, through sen0414_page_test_run_v1_0_0.py, the TEST release key) and keep the logs: "
      "the failing features must name the measured defects (no chapter-code tab, no panel level, no declared standard, and whatever else the run finds). %s" % (SIB, STD_P, DOMC, CODE_SAME, COMMON)),
    T("TK_Std_Template", "Make page template 9.52.1 for this course with the panel level, the tab and tree rule, the chapter-code tab and the playground by name, and the two builders", "Build", [], "SEN0414-I18-template", "T0", 5.0,
      "Write the NEW files 08-tooling/course_page_template_v9_52_1.html (from course_page_template_v9_50_0.html, which stays byte-identical), 08-tooling/sen0414_page_build_v4_18_0.py (from v4_17_0) and 08-tooling/sen0414_page_data_v2_25_0.py (from v2_24_0), "
      "porting the new features from the sibling's finished files (read-only: %scourse_page_template_v9_52_1.html, sen0401_page_build_v4_15_0.py, sen0401_page_data_v2_24_0.py; the lines share their ancestry, so the port is a merge of the differences between the sibling's 9.50.x and 9.52.1 onto this line, keeping this line's own features such as the exam-release, quiz and mentions). "
      "The template must: (1) show the playground as a list of NAMES that fits its container at 390 and 1366 px, the code opening in the editor; (2) add the chapter-code tab fed by the chapter-code manifest of the page data (an ordered list of named examples, each runnable with the chapter library defined in the page; FIRST establish as a fact how this line's page runs code today and what runtime the chapter library needs, and report it); "
      "(3) add one more level to the hierarchy: a group holds panels, one concept per panel, the panel at most one screen high; (4) tabs show only the sub-menus of the selected tree item, never the tree's own folder labels again, and never a third tab level (a breadcrumb instead); "
      "(5) keep every existing behaviour, id and test hook of 9.50.0 and add the DOM contract. %s The page-data builder reads the manifest 03-materials/chNN/page/chapter_code_chNN_v*.json (written by the deck task of that chapter; if it is absent the page has no chapter-code tab) and the panel structure from the research. "
      "Build scratch copies of chapters 1 and 10 on the new template with the new builders outside the repository and show they build. Do NOT write the page test or judge your own work: the independent test is TK_Std_PageTest. %s" % (SIB, DOMC, COMMON)),
    T("TK_Std_Regress", "Measure the new template against the old page test on a control set of pages built from it", "Verify", ["TK_Std_Template", "TK_Std_PageTest"], "SEN0414-lineage (control)", "T0+5h", 1.0,
      "After the template (TK_Std_Template) and the page test 9.36.0 (TK_Std_PageTest) are Done: build the pages of chapters 1 and 10 into a scratch folder on the template 9.52.1 with the new builders and run the page test 9.34.0 on each (serially, every run kept), and 9.36.0 with FORCE_STANDARD=1: "
      "each result must equal or beat the stored result of the shipped page (08-tooling/ch01-page and ch10-page test_results). Justification of the control set: the new template is a new file used only by pages built from it; the shipped pages stay on their files and are not rebuilt, "
      "so their results cannot move; the set shows the new template keeps the behaviour the old test measures. This is the controller's task: the lineage agent runs it. %s" % COMMON),
]
for nn, ch, ti in CHS:
    TASKS += [
        T("TK_Std_Deck_Ch%s_Build" % nn, "Rebuild the deck of chapter %s (%s) against the deck standard and give it its chapter-code manifest" % (ch, ti), "Build", [], "SEN0414-I18-deck-ch%s" % nn, "T0", 5.0,
          "Build the deck of chapter %s as a NEW file with a new version number from the chapter research (03-materials/ch%s/rdodi, the newest research) and the earlier deck's assets, to the deck standard; the new deck goes to 03-materials/ch%s/ named as the chapter's earlier decks are named%s. "
          "The owner's teaching-material rules: full sentences are fine but no long paragraphs (no text box over 30 words); explanation beside every code listing; the executed result shown as a visualization (native chart, table or drawn diagram) next to each listing; an everyday analogy for each key concept; "
          "5N1K stories with real names, a real picture and a live link; native charts only; numbered slides; a resources slide; short speaker notes (at most 60 words); one smooth colour scheme; dividers that name their concepts with a line of meaning and a visual; coverage of the research concepts not below 90 percent. %s %s "
          "ALSO write the chapter-code manifest 03-materials/ch%s/page/chapter_code_ch%s_v1_0_0.json: the ordered list of the deck's code examples (order number = slide order, a short NAME, the code exactly as on the slide, the slide number, the expected result), because the page tab must list the same examples in the same order. "
          "The deck generator is a NEW tool file in 08-tooling/ch%s-deck; the checker is the independent TK_Std_DeckCheck (not yours): run it when it exists and report every element as printed. %s"
          % (ch, nn, nn, ("; the earlier chapter 8 deck lives in 08-tooling/ch08-deck/ and stays where it is" if nn == "08" else ""), STD_D, CODE_SAME, nn, nn, nn, COMMON)),
        T("TK_Std_Deck_Ch%s_Verify" % nn, "Verify the deck of chapter %s against the deck standard" % ch, "Verify", ["TK_Std_Deck_Ch%s_Build" % nn, "TK_Std_DeckCheck"], "SEN0414-lineage (control)", "T0+5h", 0.5,
          "Run the deck standard check v1_0_0 and the deck overlap check v1_0_0 for chapter %s, the chapter's own build checks (the chapter check v1_1_0 where it covers the chapter), and read the deck slide by slide, rendering every slide to an image for visual review "
          "(the reading by the three roles of the owner's preference - teaching academician, reviewing faculty specialist, student - is recorded as a reading, not as a tool result); record every result as printed: Done or NOT MET, no waiver." % ch),
    ]
for nn, ch, ti in CHS:
    off = {"06": 0.0, "07": 1.5, "08": 3.0}[nn]
    TASKS += [
        T("TK_Std_Page_Ch%s_Build" % nn, "Rebuild the page of chapter %s (%s) on the new template with the chapter-code tab" % (ch, ti), "Build",
          ["TK_Std_Template", "TK_Std_PageTest", "TK_Std_Deck_Ch%s_Verify" % nn], "SEN0414-I18-page-ch%s" % nn, "T0+%gh" % (5.5 + off), 3.0,
          "Build the page of chapter %s as a NEW file with a new page version (above 9_28_0) on the template 9.52.1 with the page builder v4_18_0 and the page-data builder v2_25_0 (state how you passed the template), from the chapter research, the deck's lecture export and stories, and the deck's chapter-code manifest. "
          "Run the page tests 9.36.0 and 9.34.0 (the runner sen0414_page_test_run_v1_0_0.py), serially, store the result as a new test_results file in 08-tooling/ch%s-page, and run the chapter check Page/Ch%s. %s %s %s %s"
          % (ch, nn, nn, STD_P, DOMC, CODE_SAME, COMMON)),
        T("TK_Std_Page_Ch%s_Verify" % nn, "Verify the page of chapter %s against the page standard" % ch, "Verify", ["TK_Std_Page_Ch%s_Build" % nn], "SEN0414-lineage (control)", "T0+%gh" % (8.5 + off), 1.0,
          "Re-run serially the page tests 9.36.0 and 9.34.0, the chapter checks Research, Deck and Page for chapter %s where they cover it, the deck match check and the manifest equality (the chapter-code tab equals the deck's code, text and order); "
          "open the page at 390, 768 and 1366 px and look at every tab; record every result as printed: Done or NOT MET, no waiver." % ch),
    ]
IDS = {t[0]: t for t in TASKS}
STORIES = [
    ("ST_Std_DeckTools", "The deck standard and the deck overlap check are measured by new tools, as new files, without moving any existing gate", "Del2_StdTools", "Obj2_StdDecks", ["AC2S_DeckCheck"], ["TK_Std_DeckCheck"]),
    ("ST_Std_PageTools", "The page standard is measured by a new page test and built by a new page template with its builders, as new files with the old ones kept", "Del2_StdTools", "Obj2_StdPages",
     ["AC2S_PageTest", "AC2S_Template", "AC2S_Regress"], ["TK_Std_PageTest", "TK_Std_Template", "TK_Std_Regress"]),
]
for nn, ch, ti in CHS:
    STORIES += [("ST_Std_Deck_Ch%s" % nn, "The deck of chapter %s (%s) meets the deck standard and is ready to teach" % (ch, ti), "Del2_StdDecks", "Obj2_StdDecks", ["AC2S_Deck_Ch%s" % nn], ["TK_Std_Deck_Ch%s_Build" % nn, "TK_Std_Deck_Ch%s_Verify" % nn]),
                ("ST_Std_Page_Ch%s" % nn, "The page of chapter %s (%s) meets the page standard and is ready to use, with the deck's code in its chapter-code tab" % (ch, ti), "Del2_StdPages", "Obj2_StdPages", ["AC2S_Page_Ch%s" % nn], ["TK_Std_Page_Ch%s_Build" % nn, "TK_Std_Page_Ch%s_Verify" % nn])]


# ------------------------------------------------------------------ events
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Bring the decks and interactive pages of chapters 6, 7 and 8 to the written teaching-material standard, with the slide code in a chapter-code tab of the page"@en ;\n'
          '    backlog:requestsChangeTo %s ; backlog:hasChangeDirection backlog:Direction_Grow ;\n'
          '    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (CR, SCOPE, lit(
        OWNER_ACT + " The change grows the scope: this lineage admitted the finished chapters 7 to 12 exactly as they stand and excluded any rebuild; the owner now asks for new decks and pages of chapters 6, 7 and 8 and for the tools that measure the standard, "
        "as new files beside the Done ones. Pending until the ScopeChange that admits the stories is recorded in the Backlog version."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What bringing the chapter 6, 7 and 8 decks and pages to the written standard costs, with the facts measured before it is started"@en ;\n'
          '    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage2 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(
        FACTS + " WRITTEN STANDARD (the owner's standing teaching-material rules; the sibling's measured standard, reused): " + STD_D + " " + STD_P + " " + DOMC + " " + CODE_SAME + " " + PLAN +
        " What moves: the digests of the Scope, Goal, Objective and Backlog stages of the second lineage move once, when the stages are closed again; its status steps back to Opened and forward again through the revision; no Done story is re-dated or re-opened; the first lineage is not touched, "
        "and its Done chapter 6 stories stay as they are. Risks: the new template is a new file used only by pages built from it, so the shipped pages are compared with their stored results again only through the control set of TK_Std_Regress; "
        "a deck may not reach full concept coverage, in which case the coverage is stated as measured and not claimed; the machine has two cores, so browser tests run one at a time and the page tasks queue behind each other. A criterion that fails is named failing and its story is not Done; nothing is waived."))
    return t + cr + ia, ("ChangeRequest ex:CR2_Standard (Pending) and ImpactAssessment ex:IA2_Standard for the owner's request of 2026-10-23 08:57 Istanbul on the chapter 6, 7 and 8 decks and pages: measured facts, written standard, plan; no stage changed in this version.")


def ev_retract(t):
    t = S.set_status(t, "LS_Opened")
    reason = (OWNER_ACT + " The work adds deliverables (rebuilt decks and pages of chapters 6, 7 and 8, a page template, a page test and a deck check, all as new files); the lineage is in its closed Backlog stage and its scope excludes any rebuild of the decks and pages of chapters 7 to 12, "
              "so a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The change request ex:CR2_Standard and the impact assessment ex:IA2_Standard were recorded first. "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the goals, objectives, stories and tasks already in the register, Done ones included, re-enter by admission and are not re-dated. "
              "The retracted outputs and their digests stay as history (L-112). The interim versions are the declared transition (G129). Recorded as decided by the lineage agent role: the route is what the owner's request needs; the stage revision itself he did not decide.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the second lineage from the Scope stage: the chapter 6, 7 and 8 decks and pages are brought to the written standard"@en ;\n'
         '    backlog:revisesLineage ex:Lineage2 ; backlog:revisesFromStage backlog:Stage_Scope ;\n    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n'
         '    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, IA, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the second lineage from the Scope stage (ruling G127) for the chapter 6, 7 and 8 standard: the Scope, Goal, Objective and Backlog outputs are retracted; nothing is rebuilt in this version."


def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = S.set_status(t, "LS_Scoped")
    cl = S.CLAUSE
    tools_txt = ("A deck standard check and a deck overlap check, a page test 9.36.0 with the page-standard features, and a page template 9.52.1 with its page builder and page-data builder, all as NEW files with the existing ones kept byte-identical, "
                 "so that the written standard (D1 to D12, P1 to P11) is measured by a tool the builder of a deck or page does not run on itself.")
    decks_txt = "The decks of chapters 6, 7 and 8 rebuilt to the deck standard as new files, each with its chapter-code manifest (the code of the slides, in slide order), ready to teach. The earlier decks stay as they are."
    pages_txt = "The pages of chapters 6, 7 and 8 rebuilt to the page standard as new files on the template 9.52.1, with the chapter-code tab that lists the deck's code by name in the deck's order and runs it. The earlier pages stay as they are."
    L = ['''
ex:Area2_Standard a backlog:ScopeArea ;
    rdfs:label "The decks and interactive pages of chapters 6, 7 and 8, and the tools that measure the teaching-material standard"@en ;
    backlog:belongsToLineage ex:Lineage2 ;
    backlog:areaLocation "03-materials: the deck and page folders of chapters 6, 7 and 8; 08-tooling: the new deck checks, page test, template and builders as new files" ;
    backlog:areaMeasure "chapters of 3 whose deck and page meet the written teaching-material standard: 0 of 3 today (chapters 6, 7, 8); after the work 3" ;
    backlog:hasScopeLayer backlog:Layer_Work .
ex:Del2_StdTools a backlog:ScopeDeliverable ;
    rdfs:label "A deck standard check, a deck overlap check, a page test with the page-standard features, and a page template 9.52.1 with its builders, as new files with the old ones kept"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:derivesFromMissionClause %s^^xsd:string ;
    backlog:hasDeliverableText %s ;
    backlog:deliverableForArea ex:Area2_Standard ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Del2_StdDecks a backlog:ScopeDeliverable ;
    rdfs:label "The decks of chapters 6, 7 and 8 rebuilt to the deck standard, each with its chapter-code manifest"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:derivesFromMissionClause %s^^xsd:string ;
    backlog:hasDeliverableText %s ;
    backlog:deliverableForArea ex:Area2_Standard ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Del2_StdPages a backlog:ScopeDeliverable ;
    rdfs:label "The pages of chapters 6, 7 and 8 rebuilt to the page standard, with the chapter-code tab in the deck's order"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:derivesFromMissionClause %s^^xsd:string ;
    backlog:hasDeliverableText %s ;
    backlog:deliverableForArea ex:Area2_Standard ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Scope2 backlog:requiresDeliverable ex:Del2_StdTools, ex:Del2_StdDecks, ex:Del2_StdPages ;
    backlog:coversArea ex:Area2_Standard ;
    rdfs:seeAlso ex:CR2_Standard, ex:IA2_Standard .
ex:Scope2 rdfs:comment %s@en .
ex:Excl2_NoRebuild rdfs:comment %s@en .
''' % (lit(cl), lit(tools_txt), lit(cl), lit(decks_txt), lit(cl), lit(pages_txt),
       lit("Revised %s from the Scope stage (ruling G127) for the owner's request of %s (ex:CR2_Standard): IN now also the rebuilt decks and pages of chapters 6, 7 and 8 and the tools that measure the standard, as new files; the earlier decks and pages and every Done story stay unchanged. "
           "The statement above is history and stays (L-112); this comment is the current boundary." % (now()[:10], WHEN)),
       lit("Lifted on %s, for the owner's request of %s (ex:CR2_Standard) and ONLY for the NEW files of the decks and pages of chapters 6, 7 and 8 and of the tools named in ex:Del2_StdTools: no existing deck, research run or page is changed, and chapters 9 to 12 stay excluded. "
           "The rationale above is history and stays: a record that changed its subject would not be evidence of it, so the new files are new stories beside the Done ones." % (now()[:10], WHEN)))]
    t += "".join(L)
    return t + out_new(t, "Scope", "Out2_Mission"), "second lineage, Scope stage rebuilt by the stage revision for the chapter 6, 7 and 8 standard: three deliverables (tools; decks; pages), their area, and the exclusion of any rebuild lifted for the named new files only."


def ev_goal(t, prev):
    t = fill_re(t, "ex:" + OUT["Scope"], prev); t = S.set_status(t, "LS_Goaled")
    GL = [("G2_StdDecks", "The decks of chapters 6, 7 and 8 are rich, presentable and understandable, to the written deck standard", "Del2_StdDecks"),
          ("G2_StdPages", "The pages of chapters 6, 7 and 8 are usable in class: the slide code lists by name in the deck's order and runs, one concept per panel, no duplicated menu", "Del2_StdPages")]
    L = []
    for gid, label, dl in GL:
        L.append('\nex:%s a backlog:Goal ;\n    rdfs:label %s@en ;\n    backlog:belongsToLineage ex:Lineage2 ; backlog:derivesFromScope ex:Scope2 ; backlog:goalCoversArea ex:Area2_Standard ;\n    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalOrigin backlog:GoalOrigin_New ;\n'
                 '    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;\n    backlog:hasGoalRationale %s ;\n    backlog:producedByStage ex:%s .\n'
                 % (gid, lit(label), lit("Derived from the revised scope (ex:%s) and from the owner's request of %s, recorded in ex:CR2_Standard: the SEN0414 chapter 6, 7 and 8 decks and pages meet the same standards as the sibling course's chapters 5 and 6, "
                                         "especially that the slide code appears in the same order in a chapter-code tab of the page that can run it." % (dl, WHEN)), OUT["Goal"]))
        L.append('ex:%s rdfs:comment "Drafted by the lineage agent on 2026-10-23 from the owner\'s request of %s (ex:CR2_Standard); the intent origin is therefore Derived."@en .\n' % (gid, WHEN))
    for k, gid, what, w2, text in (("D", "G2_StdDecks", "a deck meets the teaching standard", "deck", STD_D), ("P", "G2_StdPages", "a page meets the teaching standard", "page", STD_P + " " + CODE_SAME)):
        L.append('''
ex:Spec2S_%(k)s a backlog:Specification ;
    rdfs:label "What it is for %(w)s"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:specifiesGoal ex:%(g)s ;
    backlog:hasSpecificationText %(tx)s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:%(o)s .
ex:Scen2S_%(k)s_Passes a backlog:TestScenario ; rdfs:label "A rebuilt chapter %(w2)s passes every element of the standard when measured"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec2S_%(k)s ;
    backlog:hasScenarioText "Given the rebuilt file of chapter 6, 7 or 8, when the check of the standard is run, then every element is met, nothing is skipped, and the run exits 0." .
ex:Scen2S_%(k)s_NotClaimed a backlog:TestScenario ; rdfs:label "An existing chapter %(w2)s that fails an element is named failing and not claimed"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec2S_%(k)s ;
    backlog:hasScenarioText "Given the existing chapter 6, 7 or 8 file (measured 2026-10-23), when the check of the standard is run on it, then the failing elements are named and the story carries no passing result for it." .
''' % dict(k=k, g=gid, w=what, w2=w2, tx=lit(text), o=OUT["Goal"]))
    L.append('''
ex:Model2S_UseCase a backlog:ModelArtifact ; rdfs:label "Who uses the rebuilt chapter 6, 7 and 8 materials"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasModelKind backlog:Kind_UseCaseDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "The instructor presents the deck of the chapter in class and opens the page of the chapter on the same code, in the same order, with the same look; a student runs each deck example from the chapter-code tab on a phone or a laptop, changes it and sees the result visualised, and finds one concept per panel without scrolling through a stack of concepts; independent checks (the deck standard check, the page test 9.36.0) measure the standard; the evidence bridge verifies the runs; the owner reads the register to see which chapter materials are ready." ;
    backlog:describesItem ex:G2_StdPages .
''')
    t += "".join(L)
    return t + out_new(t, "Goal", OUT["Scope"]), "second lineage, Goal stage rebuilt for the chapter 6, 7 and 8 standard: a goal for the decks and a goal for the pages, each with a specification (the standard) and a nominal and a rejection scenario; the use case model."


def ev_objective(t, prev):
    t = fill_re(t, "ex:" + OUT["Goal"], prev); t = S.set_status(t, "LS_Objectived"); n = now(); L = []
    for oid, gid, mid, what, base, tg in (("Obj2_StdDecks", "G2_StdDecks", "Met2_StdDecks", "decks of chapters 6, 7 and 8 that pass every element of the deck standard check", 0, 3),
                                          ("Obj2_StdPages", "G2_StdPages", "Met2_StdPages", "pages of chapters 6, 7 and 8 that pass the page test 9.36.0 and the page test 9.34.0", 0, 3)):
        L.append('''
ex:%(i)s a backlog:Objective ; rdfs:label "%(Wh)s: from 0 to 3"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:contributesToGoal ex:%(g)s ; backlog:fillsScope ex:Scope2 ; backlog:hasSuccessMetric ex:%(m)s ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of %(w)s, read from the runs of the checks on the newest files after the evidence bridge has run them." ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "3"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP2S_%(i)s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:%(o)s .
ex:%(m)s a backlog:Metric ; rdfs:label "%(w)s"@en ; backlog:belongsToLineage ex:Lineage2 .
ex:CP2S_%(i)s a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the chapter 6, 7 and 8 materials are controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criteria of chapters 6, 7 and 8 on the rebuilt files, so the count is read from verified runs." ;
    backlog:expectedValue "3"^^xsd:decimal .
ex:Obs22_%(i)s a backlog:MetricObservation ; rdfs:label "Baseline, before any work on the standard"@en ;
    backlog:observesMetric ex:%(m)s ; backlog:observationFor ex:%(i)s ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%(now)s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "Baseline from the measured facts of 2026-10-23 recorded in ex:IA2_Standard (python-pptx 1.0.2, Playwright 1.56.0): the existing decks and pages of chapters 6, 7 and 8 fail the standard (no chapter-code tab, no panel level, code slides without a visual result, analogies for 0 to 44 percent of key concepts, coverage 50 to 56 percent): 0 of 3 pass." .
ex:%(i)s rdfs:comment "Drafted by the lineage agent on 2026-10-23 from the owner's request of %(wh)s (ex:CR2_Standard); the intent origin is therefore Derived."@en .
''' % dict(i=oid, g=gid, m=mid, w=esc(what), Wh=esc(what[0].upper() + what[1:]), now=n, wh=WHEN, o=OUT["Objective"]))
    t += "".join(L)
    return t + out_new(t, "Objective", OUT["Goal"]), "second lineage, Objective stage rebuilt for the chapter 6, 7 and 8 standard: two objectives (decks and pages that pass the standard, 0 to 3) with metrics, checkpoints and a baseline reading of 2026-10-23."


def gh_tool(c):
    if c == "AC2S_DeckCheck":
        return ("Owner-directed work (ex:CR2_Standard). Given the existing decks of chapters 6, 7 and 8, when the NEW files sen0414_deck_standard_check_v1_0_0.py and sen0414_deck_overlap_check_v1_0_0.py are written and run on them, then ALL of: (1) the files are new and no committed file is edited; "
                "(2) the deck check reports one named exit-coded result for each element D1 to D12 of the deck standard and prints the measured number; (3) on the existing decks it reproduces the measured facts of ex:IA2_Standard - chapter 6: 26 slides, 12 code slides, 3 native charts, 27 research concepts, failing D1, D2, D3, D4, D5, D7, D10, D11; "
                "chapter 7: 26 slides, 9 code slides, 1 native chart, 34 concepts, failing D1, D2, D3, D4, D5, D7, D11, D10 not measured; chapter 8: 25 slides, 13 code slides, 0 native charts, 57 concepts, the same failing set as chapter 7 - or explains every difference by reading the deck, "
                "settles the D8 discrepancy of the chapter 8 deck, and exits non-zero on all three; (4) the header defines each measure; (5) the check measures that a chapter-code manifest equals the deck's code boxes in text and order; (6) the logs of the runs are kept; results as printed; if any element fails the file is named failing. " + STD_D)
    if c == "AC2S_PageTest":
        return ("Owner-directed work (ex:CR2_Standard). Given the page test 9.34.0 (SHA-256 recorded by the executor) and the existing pages of chapters 6, 7 and 8, when the NEW file sen0414_page_test_v9_36_0.py is written, then ALL of: (1) the file is new and 9.34.0 is byte-identical; "
                "(2) every feature text of 9.34.0 is present unchanged (a diff shows only added code and the version line and comments); (3) the added features P1, P2, P3, P4, P5, P6, P8, P9, P11 apply to a page that declares the standard and are reported SKIP with the reason otherwise; FORCE_STANDARD=1 applies them to any page; "
                "(4) with FORCE_STANDARD=1 on the existing pages of chapters 6, 7 and 8 the run fails the features that name the measured defects (no chapter-code tab, no panel level, no declared standard) and ends without a crash; (5) the logs are kept; results as printed. " + STD_P + " " + DOMC)
    if c == "AC2S_Template":
        return ("Owner-directed work (ex:CR2_Standard). Given the page template 9.50.0, the page builder v4_17_0 and the page-data builder v2_24_0 (all byte-identical after the task), when the NEW files course_page_template_v9_52_1.html, sen0414_page_build_v4_18_0.py and sen0414_page_data_v2_25_0.py are made, then ALL of: "
                "(1) the files are new, the old ones byte-identical; (2) the template implements the DOM contract and keeps every id and hook of 9.50.0; the report states as a fact how the page runs code today and what runtime the chapter-library examples need; "
                "(3) a scratch page of chapter 1 and of chapter 10 built on 9.52.1 declares the page standard and the page test 9.36.0 passes P1, P3, P4, P5, P6, P8, P9 on them (the chapter-code tab features apply when a manifest exists); (4) no gate, test or threshold is changed; results as printed. " + DOMC)
    if c == "AC2S_Regress":
        return ("Owner-directed work (ex:CR2_Standard). Given the template 9.52.1, the builders v4_18_0 and v2_25_0 and the page tests, when the pages of chapters 1 and 10 are built into a scratch folder on the new template and the page test 9.34.0 is run on each, serially, then ALL of: "
                "(1) each run ends exit 0 with no failed feature and widgets, features and gates not below the stored result of the shipped page, skipped features not more and each of them one the stored result skips; (2) every run is kept as a log; (3) no committed file is edited, the scratch pages are not shipped; results as printed. "
                "Control set justified: the new template is a new file used only by pages built from it; the shipped pages stay on their files, so their results cannot move.")
    raise KeyError(c)


def gh_deck(nn):
    ch = nn.lstrip("0")
    return ("Owner-directed work (ex:CR2_Standard): the owner asks that the chapter %s deck meet the same standards as the sibling course's chapters 5 and 6. Given the existing deck of chapter %s and its research, when the deck is rebuilt as a new file with a new version number and its chapter-code manifest written, then ALL of: "
            "(1) the deck standard check v1_0_0 for chapter %s reports every element D1 to D12 met and exits 0; (2) the deck overlap check v1_0_0 reports no overlap; (3) the chapter-code manifest chapter_code_ch%s_v1_0_0.json lists the deck's code examples in slide order, by name, and its code and order equal the deck's code boxes (measured by the deck check); "
            "(4) the chapter's own build checks that exist for it pass (the chapter check v1_1_0 Deck/Ch%s where it covers the chapter); (5) no committed file is edited; results as printed; if any element fails the deck is named failing and this criterion has no passing result. " % (ch, ch, ch, nn, nn) + STD_D)


def gh_page(nn):
    ch = nn.lstrip("0")
    return ("Owner-directed work (ex:CR2_Standard): the owner asks that the chapter %s page meet the same standards as the sibling course's chapters 5 and 6, above all that the slide code appears in the same order in a chapter-code tab that runs it. Given the existing page of chapter %s and the rebuilt deck of chapter %s, "
            "when the page is rebuilt as a new file with a new page version on the template 9.52.1 with the builders v4_18_0 and v2_25_0, then ALL of: (1) the page test 9.36.0 runs all its added features with no skip and passes them (P1, P2, P3, P4, P5, P6, P8, P9, P11), exit 0; "
            "(2) the page test 9.34.0 reports no failure and widgets, features and gates not below the stored result of the existing page, skipped not more; (3) the chapter-code tab equals the deck's chapter-code manifest in names, code and order and each example runs in the page and shows its result (measured by the page test); "
            "(4) the chapter checks that exist for the chapter (Research, Page) pass; (5) no committed file is edited, no gate, test or threshold changed beyond the new files; the stored page-test result is a new file; results as printed; if any element fails the page is named failing and this criterion has no passing result. " % (ch, ch, ch) + STD_P + " " + CODE_SAME)


def task_block(tid, title, ttype, deps, sess, est, hrs, note):
    full = note + " Planned session %s; estimated start %s after the executors begin, about %s hours (an estimate, G120: nobody has witnessed a start; the real start is recorded at work begun)." % (sess, est, hrs)
    return ('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n'
            '    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer %s ; backlog:admittedByOutput %s ; backlog:responsible %s ;\n'
            '    backlog:hasInvestmentCategory backlog:Cat_%s ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:%s ;\n%s'
            '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n'
            '    backlog:hasAuditNote %s .\n') % (tid, lit(title), tid, lit(title), ITER, NEWB, EXEC, "NewCapability" if ttype == "Build" else "Compliance", ttype, "Ready" if ttype == "Build" else "Proposed",
                                                 ("    backlog:dependsOn %s ;\n" % ", ".join("ex:" + d for d in deps)) if deps else "", lit(full))


def story_block(sid, title, deliv, obj, crits, tasks, note):
    return ('\nex:%s a backlog:Story ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n'
            '    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer %s ; backlog:admittedByOutput %s ;\n'
            '    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
            '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability %s ; backlog:soThat %s ;\n'
            '    backlog:satisfiesDeliverable ex:%s ; backlog:pursuesObjective ex:%s ; backlog:hasAcceptanceCriterion %s ;\n'
            '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ; backlog:responsible %s ;\n'
            '    backlog:decomposesInto %s ;\n    backlog:hasState backlog:Ready ;\n'
            '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Not scored: the owner directed this work on 2026-10-23 and needs the class material as soon as possible, so there is no ranking left to compute." ;\n'
            '    backlog:hasAuditNote %s .\n') % (sid, lit(title), sid, lit(title), ITER, NEWB, lit(title[0].lower() + title[1:]), lit("the instructor can teach chapters 6, 7 and 8 from decks and pages that meet the written standard, with the slide code runnable in the page in the deck's order"),
                                                 deliv, obj, ", ".join("ex:" + c for c in crits), EXEC, ", ".join("ex:" + x for x in tasks), lit(note))


def ev_backlog(t, prev):
    t = fill_re(t, "ex:" + OUT["Objective"], prev); t = S.set_status(t, "LS_Backlogged"); n = now()
    cnt = len(re.findall(r"admittedByOutput ex:Out2_Backlog\b(?!R)", t)); assert cnt >= 20, cnt
    t = re.sub(r"admittedByOutput ex:Out2_Backlog\b(?!R)", "admittedByOutput " + NEWB, t)
    L = []
    for ts, fn, what in TOOLS:
        L.append('ex:%s a backlog:ToolScript ; rdfs:label %s@en ; backlog:scriptFileName "%s" ; backlog:acceptsGraphPath false .\n' % (ts, lit(what), fn))
    labels = {"AC2S_DeckCheck": "The deck standard check and the deck overlap check are new files that reproduce the measured facts of the three existing decks and measure D1 to D12",
              "AC2S_PageTest": "The page test 9.36.0 is a new file that keeps every feature of 9.34.0 and fails the existing pages of chapters 6, 7 and 8 on the measured defects",
              "AC2S_Template": "The page template 9.52.1 and its two builders are new files that implement the panel level, the tab and tree rule, the chapter-code tab and the playground by name",
              "AC2S_Regress": "The new template gives the old page test the stored result on a control set of pages built from it"}
    tools_of = {"AC2S_DeckCheck": ["TS2_DeckStdCheck", "TS2_DeckOverlap"], "AC2S_PageTest": ["TS2_PageTest36", "TS2_PageTest34"], "AC2S_Template": ["TS2_PageTemplate", "TS2_PageBuilder", "TS2_PageData", "TS2_PageTest36"],
                "AC2S_Regress": ["TS2_PageTemplate", "TS2_PageTest34", "TS2_PageTest36"]}
    cases = {"AC2S_DeckCheck": "TC2S_Tool", "AC2S_PageTest": "TC2S_Tool", "AC2S_Template": "TC2S_Tool", "AC2S_Regress": "TC2S_Tool"}
    for nn, ch, ti in CHS:
        labels["AC2S_Deck_Ch%s" % nn] = "The deck of chapter %s meets every element of the deck standard, with its chapter-code manifest" % ch
        tools_of["AC2S_Deck_Ch%s" % nn] = ["TS2_DeckStdCheck", "TS2_DeckOverlap", "TS2_ChapterCheck"]; cases["AC2S_Deck_Ch%s" % nn] = "TC2S_D"
        labels["AC2S_Page_Ch%s" % nn] = "The page of chapter %s meets the page standard with the chapter-code tab in the deck's order" % ch
        tools_of["AC2S_Page_Ch%s" % nn] = NEWT + BASET; cases["AC2S_Page_Ch%s" % nn] = "TC2S_P"
    for c, lab in labels.items():
        gt = gh_tool(c) if c in ("AC2S_DeckCheck", "AC2S_PageTest", "AC2S_Template", "AC2S_Regress") else (gh_deck(c[-2:]) if "_Deck_" in c else gh_page(c[-2:]))
        k = cases[c]
        L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool %s ;\n    backlog:measuredWithVersion %s ;\n'
                 '    backlog:satisfiedByArtifact "the new files cited by SHA-256, the logs of the runs and the diffs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:%s_Passes, ex:%s_NotClaimed .\n'
                 % (c, lit(lab), lit(gt), ", ".join("ex:" + x for x in tools_of[c]), lit(VER), k, k))
    for tid, title, ttype, deps, sess, est, hrs, note in TASKS:
        L.append(task_block(tid, title, ttype, deps, sess, est, hrs, note))
    for sid, title, deliv, obj, crits, tks in STORIES:
        L.append(story_block(sid, title, deliv, obj, crits, tks, OWNER_ACT + " One criterion per unit (G133). The Done stories of chapters 6, 7 and 8 (ST_Deck_Ch06, ST_Page_Ch06 in the first lineage; ST_Deck_Ch07, ST_Page_Ch07, ST_Deck_Ch08, ST_Page_Ch08 here) stay Done and are not edited (G125). " + FACTS))
    for k, ac in (("Tool", [c for c in labels if "_Deck_" not in c and "_Page_" not in c]), ("D", ["AC2S_Deck_Ch%s" % c[0] for c in CHS]), ("P", ["AC2S_Page_Ch%s" % c[0] for c in CHS])):
        L.append('''
ex:TC2S_%(k)s_Passes a backlog:TestCase ; rdfs:label "Run the checks of the criteria on the new files and require no failure and no skip"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Scen2S_%(s)s_Passes ; backlog:runsOnData ex:Data2S_%(k)s_Passing ;
    backlog:hasCaseText "Run the checks of the criterion over the newest files; they report no failure and exit 0 (the bridge runs recorded in this register are these runs)." .
ex:TC2S_%(k)s_NotClaimed a backlog:TestCase ; rdfs:label "Run the checks on an existing file that fails and require that no pass is claimed"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Scen2S_%(s)s_NotClaimed ; backlog:runsOnData ex:Data2S_%(k)s_Failing ;
    backlog:hasCaseText "Run the checks over the existing deck or page of chapter 6, 7 or 8 (measured 2026-10-23); the failing elements are named and the file carries no passing result." .
ex:Data2S_%(k)s_Passing a backlog:TestData ; rdfs:label "The rebuilt files whose checks pass when run"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasFixtureState "The newest rebuilt files, for which every check of the criterion exits zero when the bridge runs it, and whose cited files equal their recorded SHA-256." .
ex:Data2S_%(k)s_Failing a backlog:TestData ; rdfs:label "The existing chapter 6, 7 and 8 files whose checks fail when run"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasFixtureState "The decks and pages of chapters 6, 7 and 8 as they stood on 2026-10-23 (the decks named in ex:IA2_Standard, the pages v9_28_0) with the measured defects of ex:IA2_Standard." .
''' % dict(k=k, s="D" if k in ("Tool", "D") else "P", cr=", ".join("ex:" + c for c in ac)))
    L.append('''
ex:Model2S_Class a backlog:ModelArtifact ; rdfs:label "How a chapter's slide code, its manifest and the page's chapter-code tab are stored"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasModelKind backlog:Kind_ClassDiagram ; backlog:hasModelLevel backlog:Level_Design ;
    backlog:declaresState "A Chapter has one Deck file and one Page file, each a new file with a new version number. A Deck holds code boxes, one per code slide listing, in slide order. A ChapterCodeManifest (03-materials/chNN/page/chapter_code_chNN_v1_0_0.json) is written from the Deck and holds one CodeExample per code box: order number, name, code exactly as on the slide, slide number and expected result. The Page holds one chapter-code tab whose items are the CodeExamples of the manifest, equal in name, code and order, each runnable in the Page with the chapter library defined in the Page, with its result visualised. The deck standard check proves Manifest equals Deck; the page test proves Tab equals Manifest. A Done story of a chapter is never edited: a new file is a new story." ;
    backlog:describesItem ex:G2_StdPages .
''')
    sid_all = [s[0] for s in STORIES]; tk_all = [x[0] for x in TASKS]
    for x in sid_all + tk_all:
        L.append('ex:Refine2S_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration %s ;\n    backlog:hasRefinementOutcome %s .\n'
                 % (x, x, x, n, ITER, lit("Refined by the lineage agent from the owner's request of %s (ex:CR2_Standard) and the measured facts of ex:IA2_Standard: acceptance criteria with tools and versions, dependencies, estimated start, and a brief to be generated from the register; startable when its dependencies are Done." % WHEN)))
    for sid, title, deliv, obj, crits, tks in STORIES:
        kk = "P" if "Page" in sid else "D"
        L.append('ex:Plan2S_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 18"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec2S_%s, ex:Scen2S_%s_Passes, ex:Scen2S_%s_NotClaimed .\n'
                 % (sid, sid, n, ITER, sid, ", ".join("ex:" + x for x in tks), kk, kk, kk))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    L.append("ex:Obj2_StdDecks backlog:metricMovableBy %s .\nex:Obj2_StdPages backlog:metricMovableBy %s .\n" % (
        ", ".join(["ex:ST_Std_Deck_Ch%s" % c[0] for c in CHS] + ["ex:ST_Std_DeckTools"]), ", ".join(["ex:ST_Std_Page_Ch%s" % c[0] for c in CHS] + ["ex:ST_Std_PageTools"])))
    start = datetime.datetime.strptime(n, "%Y-%m-%dT%H:%M:%S"); end = (start + datetime.timedelta(days=ITER_DAYS)).strftime("%Y-%m-%dT%H:%M:%S")
    SG = ("The decks and the interactive pages of chapters 6, 7 and 8 are rebuilt as new files that meet the written teaching-material standard (the deck standard D1 to D12 and the page standard P1 to P11), measured by an independent deck check and the page test 9.36.0 "
          "and verified by the evidence bridge, chapter 6 first, then 7, then 8; the slide code of each chapter appears in the same order in the chapter-code tab of its page and runs there. Each unit that fails is named failing and is not Done. "
          "No existing file, gate, test or threshold is edited. Frozen at the planning ceremony.")
    DS = ("Proposed by the lineage agent on %s: the start is the instant of the planning ceremony ex:PC2_Iter_18; the length is %d days, constant from this iteration on (G9) - a stipulation, not a measurement: it is the class cadence (the iteration ends before the Friday class at 14:00 Istanbul, "
          "here %s), and the iterations of the first lineage had no constant length (their ends lay one to seven weeks out), so this length is the lineage agent's proposal for the owner to confirm or change. "
          "Justification of the work inside it (estimates, not measurements). At T0 the three tooling tasks and the three deck builds are independent builds with python-pptx and light rendering: the deck check about 1.5 h, the page test about 3 h, the template and builders about 5 h, each deck about 5 h. "
          "The heavy part is the browser tests, which run one at a time on the two cores. CRITICAL PATH per chapter: deck (5 h) -> its verification (0.5 h) -> page (about 3 h, also needs the template and the page test) -> its verification (about 1 h). "
          "Chapter 6: page ready about T0+9.5 h; chapter 7 starts its page 1.5 h later and chapter 8 3 h later because their tests queue behind the earlier ones: about T0+11 h and T0+12.5 h if nothing fails. "
          "The margin to the end of the iteration is several days, enough for repeated page tasks; the urgency is the owner's, so the order is chapter 6 first and each chapter ships as soon as it is controlled." % (n, ITER_DAYS, end))
    L.append('ex:Iter_18 a backlog:Iteration ; rdfs:label "Iteration 18: the chapter 6, 7 and 8 decks and interactive pages brought to the written standard"@en ; backlog:hasIdentifier "Iter_18" ; backlog:belongsToLineage ex:Lineage2 ;\n'
             '    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (
        n, end, lit(DS), lit(SG), ", ".join("ex:" + x for x in sid_all + tk_all)))
    L.append('ex:PB2S_Iter_18 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 18 when it was planned"@en ; backlog:baselineFor ex:Iter_18 ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "%s"^^xsd:dateTime .\n' % (n, n, end))
    L.append('ex:PC2_Iter_18 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 18: the chapter 6, 7 and 8 standard"@en ; backlog:ceremonyFor ex:Iter_18 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent %s ;\n    rdfs:comment %s@en .\n' % (
        n, ", ".join("ex:Plan2S_" + s for s in sid_all), lit("Held %s by the lineage agent, after the owner's request of %s (ex:CR2_Standard): the eight stories and their 16 tasks are committed to this iteration, whose goal is frozen at its start. No executor has started; work begun is recorded at the real start of each executor session, with its brief." % (n, WHEN))))
    L.append('ex:SC2_Standard a backlog:ScopeChange ;\n    rdfs:label "Scope grown by the chapter 6, 7 and 8 decks and pages brought to the written standard, and the tools that measure it"@en ;\n    backlog:fulfillsRequest ex:CR2_Standard ; backlog:changesScope ex:Scope2 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        ", ".join("ex:" + s for s in sid_all), lit(OWNER_ACT + " The boundary moved outward by eight stories; the exclusion of any rebuild (ex:Excl2_NoRebuild) is lifted only for the new files named in ex:Del2_StdTools, ex:Del2_StdDecks and ex:Del2_StdPages; nothing existing is edited or weakened.")))
    t, kk = re.subn(r'(ex:CR2_Standard a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('ex:CR2_Standard rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC2_Standard and the eight stories it admits; it was Pending before. The owner\'s request of %s is the direction and authorises the scope; the length of the iteration is still his."@en .\n' % (n[:10], WHEN))
    t += "\n" + "".join(L)
    return t + out_new(t, "Backlog", OUT["Objective"]), ("second lineage, Backlog stage rebuilt for the chapter 6, 7 and 8 standard: eight stories (tools; deck and page of chapters 6, 7 and 8) with 16 tasks and dependencies, twelve criteria with tools and versions, refinement and planning events, "
                                                          "the new iteration Iter_18 of constant length with sprint goal, plan baseline and ceremony, and the ScopeChange that admits the stories; the change request is Accepted; the %d carried items are re-admitted by the rebuilt output, not re-dated." % cnt)


def ev_fill(t, prev):
    t = fill_re(t, NEWB, prev)
    return t, "closedAtCommit of the rebuilt Backlog output ex:%s set to the commit that closed it (%s); the revision is complete and no work is begun." % (OUT["Backlog"], prev)


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    ev = sys.argv[1]; src = newest(); t = open(src, encoding="utf-8").read()
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, arg), "goal": lambda: ev_goal(t, arg), "objective": lambda: ev_objective(t, arg),
          "backlog": lambda: ev_backlog(t, arg), "fill": lambda: ev_fill(t, arg)}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(write_new(src, nt, comment)))


if __name__ == "__main__":
    main()
