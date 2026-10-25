#!/usr/bin/env python3
"""sen0414_lineage_iter20 v1_0_0 - change route: PLAN Iteration 20 of the second lineage (the retrofit of chapters 10 to 25 to the written standard, and the Cross.B gap as a pilot), after the review that closed Iteration 19 (ex:RC2_Iter_19, register 2.233.0), on the direction of the course coordinator of 2026-10-25 and the owner's decision of 2026-10-23 (ex:CR2_Priority3: after chapters 1 to 9, return to ALL chapters, and after that build all remaining chapters).
What the planning does (facts measured by the lineage agent on 2026-10-25, see FACTS and the logs in 08-tooling/control-iter20-logs): the 16 retrofit stories of chapters 10 to 25 become Ready, scored (WSJF) and decomposed into six tasks each (deck build, deck verify, page build, research set and page ABox, research verify, page verify); the Cross.B gap story becomes Ready with four tasks as a PILOT on chapter 6 (specification, its control, build, its control); the remaining-chapters story is WITHDRAWN (Cancelled, with its rationale) because the measurement it waited for shows nothing remaining: all 25 chapters have research, deck and page; Iter_20 gets its start, end (seven days, G9) and sprint goal; the research criterion for chapters 10 to 25 is added and the exclusion is lifted for their new files only.
The lessons of Iteration 19 are written INTO the task notes (new tool files from the first save, page-ABox builder v1_1_13, the page ABox named above any older one, the story-layout probe on every story, the first-line error scan of the manifests, the executor's own probe as strict as the controller's). No rebaseline is written (an owner decision). No work is begun by this route: work begun is recorded at the real start of each executor session.
Events, one new register file each:  change | retract | backlog PREV | fill PREV.   Usage: sen0414_lineage_iter20_v1_0_0.py EVENT [PREV_COMMIT]"""
__version__ = "1.0.0"
import datetime, glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
S = W.S; lit = W.lit; now = W.now
REPO = W.REPO
CR = "ex:CR2_Iter20"; IA = "ex:IA2_Iter20"; REV = "ex:Revision_Lineage2_Backlog11"
OLD = "ex:Out2_BacklogR10"; NEW = "ex:Out2_BacklogR11"
CH = {"10": ("Reading and Writing Files", "ReadingWritingFiles"), "11": ("Organizing Files", "OrganizingFiles"), "12": ("Command Line Programs", "CommandLinePrograms"), "13": ("Web Scraping", "WebScraping"),
      "14": ("Excel Spreadsheets", "ExcelSpreadsheets"), "15": ("Google Sheets", "GoogleSheets"), "16": ("SQLite Databases", "SQLiteDatabases"), "17": ("PDF and Word Documents", "PDFAndWordDocuments"),
      "18": ("CSV, JSON and XML Files", "CSVJSONXML"), "19": ("Time, Scheduling and Launching Programs", "TimeSchedulingLaunching"), "20": ("Email, Texts and Push Notifications", "EmailTextsPush"),
      "21": ("Graphs and Images", "GraphsAndImages"), "22": ("Recognizing Text in Images", "RecognizingText"), "23": ("Controlling the Keyboard and Mouse", "KeyboardAndMouse"),
      "24": ("Text-to-Speech and Speech Recognition", "TextToSpeech"), "25": ("Threads", "Threads")}
TC = {c: 20 - (int(c) - 10) for c in CH}                      # time criticality: the owner's order of chapters (20 = first, ... 5 = last)
EST = {"Deck_Build": 5.0, "Deck_Verify": 0.5, "Page_Build": 3.5, "Research": 4.0, "Research_Verify": 0.5, "Page_Verify": 1.0}
SIZE = sum(EST.values())
CBEST = {"Spec": 3.0, "Spec_Verify": 0.5, "Build": 4.0, "Build_Verify": 1.0}; CBSIZE = sum(CBEST.values())
LOGS = os.path.join(REPO, "08-tooling", "control-iter20-logs")


def vk(p):
    m = re.findall(r"_v(\d+)_(\d+)_(\d+)\.", os.path.basename(p)); return [int(x) for x in m[-1]] if m else [0, 0, 0]


def newest(pat):
    fs = sorted(glob.glob(os.path.join(REPO, pat)), key=vk); return os.path.relpath(fs[-1], REPO) if fs else None


def measured(ch):
    """Facts measured from the repository and the controller's own pre-runs (logs in control-iter20-logs)."""
    std = open(os.path.join(LOGS, "pre_deck_std_ch%s.log" % ch), encoding="utf-8").read(); ovl = open(os.path.join(LOGS, "pre_deck_ovl_ch%s.log" % ch), encoding="utf-8").read()
    rs = open(os.path.join(LOGS, "pre_Research_Ch%s.log" % ch), encoding="utf-8").read()
    sm = re.search(r"SUMMARY PASS=(\d+) FAIL=(\d+) NOT_MEASURED=(\d+)", std); fl = re.search(r"failing: ([\w,]+)", std)
    d = dict(deckfail=int(sm.group(2)), failing=fl.group(1) if fl else "", ovl=re.search(r"RESULT (\w+) \((\d+) findings?\)", ovl).groups(), res="PASS" if "RESULT Research/Ch%s: PASS" % ch in rs else "FAIL",
             mism=len(re.findall(r"^  MISMATCH", rs, re.M)), execexit=re.search(r"execution checks \(([\w]+)\) exit (\d+)", rs).groups())
    d["deck"] = newest("08-tooling/ch%s-deck/*.pptx" % ch); d["page"] = newest("03-materials/ch%s/page/sen0414_ch%s_page_v*.html" % (ch, ch)); d["pabox"] = newest("03-materials/ch%s/page/sen0414_ch%s_page_abox_v*.ttl" % (ch, ch))
    d["data"] = newest("08-tooling/sen0414_ch%s_rdodi_data_v*.py" % ch); d["corpus"] = newest("08-tooling/sen0414_ch%s_corpus*_v*.py" % ch); d["stories"] = newest("08-tooling/sen0414_ch%s_stories_v*.py" % ch)
    d["rdodi"] = {k: newest("03-materials/ch%s/rdodi/sen0414_ch%s_%s_v*.ttl" % (ch, ch, k)) for k in ("document", "domain_tbox", "domain_abox", "domain_shacl", "research")}
    d["builder"] = newest("08-tooling/ch%s-deck/deck_build_v*.py" % ch)
    d["rr"] = d["deckfail"] + (2 if not d["pabox"] else 0) + (1 if d["res"] == "FAIL" else 0)
    return d


def fact(ch):
    m = measured(ch); title = CH[ch][0]
    return ("CHAPTER %d (%s) as it stands (measured 2026-10-25 UTC by the lineage agent): research 03-materials/ch%s/rdodi (document %s, domain TBox %s, ABox %s, SHACL %s, research %s); data module %s; corpus %s; stories %s; "
            "the earlier deck is %s (builder %s) - it lives in 08-tooling/ch%s-deck/, NOT in 03-materials, and stays there; newest page %s; page ABox: %s; chapter-code manifest: none. "
            "The deck standard check v1_0_0 on the earlier deck prints %d failing elements (%s; M1 and D10 not measured) and the overlap check ends %s (%s findings). "
            "The chapter check Research/Ch%s ends %s: the gates end OVERALL: PASS, Stage 4 is not run (no page ABox exists), Cross.B CANNOT_RUN; the execution checks of the data module end exit %s with %d MISMATCH line(s) (log 08-tooling/control-iter20-logs/pre_Research_Ch%s.log: read it first - the claims that print a mismatch here depend on what is installed on this machine or on a service)." % (
                int(ch), title, ch, *(re.search(r"_v(\d+_\d+_\d+)", m["rdodi"][k]).group(1) for k in ("document", "domain_tbox", "domain_abox", "domain_shacl", "research")), os.path.basename(m["data"] or "none"), os.path.basename(m["corpus"] or "none"), os.path.basename(m["stories"] or "none"),
                os.path.basename(m["deck"]), os.path.basename(m["builder"] or "none"), ch, os.path.basename(m["page"]), os.path.basename(m["pabox"]) if m["pabox"] else "NONE (the first page ABox of this chapter is built by the research task)",
                m["deckfail"], m["failing"], m["ovl"][0], m["ovl"][1], ch, m["res"], m["execexit"][1], m["mism"], ch))


DIRECTION = ("Direction of the course coordinator, 2026-10-25, recorded as relayed: the Iteration 19 close is accepted; run the Iteration 20 change route now without waiting for the owner: check the stories against the verified gaps, change request and impact assessment, re-rank in the owner's order, generate the briefs from the current generator with the lessons of Iteration 19 folded in "
             "(new tool files from the start, the page-ABox builder v1_1_13, the page-ABox version above the old one, the story-layout probe on every story, the first-line error scan on manifests, the executor's own probe as strict as the controller's); plan the batches so that at most three executors run at once (two cores; the serial page-test lock was the bottleneck of Iteration 19; decks and research in parallel, page tests the only serial part). "
             "The owner's decision of Friday 2026-10-23 16:06 Istanbul (13:06 UTC) (ex:CR2_Priority3), recorded as relayed, is the release: after chapters 7, 8 and 9, return to ALL chapters (chapters 1 to 5 are done and controlled), and after that build all remaining chapters.")


def facts_global():
    rows = []
    for c in CH:
        m = measured(c); rows.append("chapter %s: deck %d failing elements, overlap %s, research %s (%d mismatches)" % (c, m["deckfail"], m["ovl"][0], m["res"], m["mism"]))
    return ("MEASURED FACTS (the lineage agent, 2026-10-25, from the repository and from its own runs; logs 08-tooling/control-iter20-logs/): "
            "(1) THE STORY OF THE REMAINING CHAPTERS (ex:ST_Plan_Remaining) waited for a measurement 'when the retrofits finish': the repository holds, for each of the 25 chapters of the course (the 3rd edition's 24 chapters and the threads chapter 25 of the 2nd edition), research files, a deck and a page; no chapter lacks one of the three. The story has nothing to build and is withdrawn (Cancelled with its rationale); a chapter found lacking later is a new story by the change route. "
            "(2) DECKS of chapters 10 to 25 are NOT in 03-materials: each has one earlier deck 08-tooling/chNN-deck/sen0414_chNN_deck_v1_0_x.pptx (and its generator there); the deck standard check v1_0_0 prints 7 or 8 failing elements on every one (D1, D2, D3, D4, D5, D7, D11, and D12 for chapters 12 and 13; D10 and M1 not measured: no manifest), and the overlap check ends FINDINGS only for chapter 10 (2 findings). None has a chapter-code manifest. "
            "(3) PAGES: the newest pages are v9_28_0 to v9_35_0 (template 9.50.0 and older), with no chapter-code tab; no chapter 10 to 25 has a page ABox, so the gates' Stage 4 (A, B, cov, sub, src) and Cross.B have never run for them. "
            "(4) RESEARCH: the chapter check Research/Ch10 to Ch25 on the controller's machine ends PASS for chapters 10, 11, 12, 13 and 16 (the gates' Stages 1 to 3 and the execution checks pass) and FAIL for chapters 14, 15, 17, 18, 19, 20, 21, 22, 23, 24 and 25: the gates end OVERALL: PASS but the execution checks of the data module end with exit 1 (mismatches or a crash of the claim runner; chapter 14: openpyxl alone, Pillow absent, defusedxml absent; the claims were recorded on another environment). "
            "Per chapter: " + "; ".join(rows) + ". "
            "(5) THE CHAPTER CHECK has Deck and Page cases for some of these chapters; they were not run for chapters 10 to 25 here and are not part of the controller's measure (the controller measures with the deck standard check, the overlap check, the page tests 9.37.0 and 9.34.0 under the runner v1_1_0 and the chapter check Research/ChNN). "
            "(6) FROM ITERATION 19 (the lessons, measured in its work): a committed control or build tool was edited in place twice; a first page failed the page test on an example whose recorded result began with an error line (six pages and decks repaired); a first page put the story text below the fold at 1366x768 (two pages); a page-ABox builder stopped on a visual kind it did not know three times (names, floatbits); a research check passed only on an unloaded machine (a signal-timing claim); each is written into the task notes below.")


GAPS = ("GAPS SAID OPENLY: (a) the metrics Met2_StdDecks and Met2_StdPages count the decks and pages of chapters 6, 7 and 8 (target 3) and read 3 and 3; the retrofit of chapters 10 to 25 moves no number of them, as that of chapters 1 to 5 did not (ex:Finding2_Iter19_MetricScope); widening them is the Owner's decision and no rebaseline is written; the review of Iteration 20 reports the chapters as readings in the method text. "
        "(b) Cross.B of the research gates cannot run in any chapter (0 hybrid chains); the research criterion of the retrofit says: Cross.B must not FAIL, CANNOT_RUN is reported and is not a pass; the pilot of ex:ST_Plan_Gap_CrossB models the chains in ONE chapter (chapter 6); carrying the model to the other 24 chapters is a further item, not part of this iteration. "
        "(c) The execution checks of eleven chapters fail on this machine for reasons of the environment (installed packages, services, timing): a claim is made reproducible by an isolated environment the data module builds itself, or it is reported as printed (FAIL) and the criterion is NOT MET; no claim is weakened to pass, and a skip is not a pass. "
        "(d) The end of Iter_20 is the proposed end of seven days (G9); a rebaseline is an owner decision. 16 chapters at 14.5 h are 232 h, and the pilot 8.5 h: with at most three executors at once and the page tests serial on two cores the plan does not promise that all sixteen chapters finish inside it; a chapter that is not Done at the review is said to be not Done and is carried by the change route, not hidden. "
        "(e) The Deck and Page cases of the chapter check were not run for chapters 10 to 25.")
GOAL = ("The decks, the chapter-code manifests and the interactive pages of chapters 10 to 25 are rebuilt as new files that meet the written teaching-material standard (the deck standard D1 to D12, measured by the independent deck check and overlap check; the page standard P1 to P11, measured by the page test 9.37.0 and 9.34.0, with the story-layout rule on every story), the research set and the page ABox of each chapter pass the chapter check Research/ChNN on the new page "
        "(the first page ABox of each of these chapters), the slide code of each chapter appears in the same order in the chapter-code tab of its page and runs there, in the owner's order of chapters, 10 first; Cross.B is made measurable in a pilot chapter; every file is verified by the lineage agent's own re-runs on the evidence bridge. Each unit that fails is named failing and is not Done. No existing file, gate, test or threshold is edited. Frozen at the planning ceremony.")
GH_RES = ("Given the research set of chapter N as it stands (documents, domain TBox, ABox, SHACL and research files; the chapter check Research/ChNN ends PASS or FAIL on the execution checks of the data module; NO page ABox exists, so Stage 4 and Cross.B have never run for the chapter) and the NEW page of the chapter (the page-build task of the same chapter, Done and controlled), "
          "when (A) where the chapter check ends FAIL on the execution checks (or on a gate), a NEW data module 08-tooling/sen0414_chNN_rdodi_data_vX_Y_Z.py is written from the chapter corpus and the existing research files so that every claim reproduces - a claim that depends on an installed package or a service is made reproducible by an isolated environment the data module builds itself, or it is reported as printed; no claim is weakened - and the chapter files are rebuilt from it by the generic builder (sen0414_rdodi_build_v1_2_0.py) as NEW versioned files in 03-materials/chNN/rdodi; where the chapter check ends PASS the research files are NOT rebuilt (nothing is changed for its own sake), and "
          "(B) the page-ABox builder v1_1_13 (08-tooling/sen0414_page_abox_build_v1_1_13.py; a NEW version file if it stops on a visual kind it does not know - v1_1_11 stopped on 'names', v1_1_12 on 'floatbits') builds the page ABox 03-materials/chNN/page/sen0414_chNN_page_abox_v9_95_0.ttl that describes the NEW page (its menus, tabs, panels, widgets and chapter-code examples as they are in that page), "
          "then ALL of: (1) every new file is new and every committed file (the older research files, the deck, the page, the manifest, the builders) is byte-identical; "
          "(2) every typed individual of the new page ABox (and of any new research ABox) has a label, a definition and a source where the gates ask for them, and content of at least five words that is substantive by the gate, written from the book's chapter, the deck, the page and the existing content; where research files are rebuilt, the set of individuals, classes, links and sources of the old files is a subset of the new files' or each missing one has a stated reason (the controller compares the sets); "
          "(3) the chapter check Research/ChNN ends exit 0 with 'RESULT Research/ChNN: PASS': the gates 'OVERALL: PASS' with Stage4.A, B, cov, sub and src passing on the NEW page ABox, HermiT consistent, the execution checks with 0 mismatches ON THE CONTROLLER'S MACHINE; Cross.B must not FAIL; it reports CANNOT_RUN (0 hybrid chains) and is reported openly as such and NOT counted as a pass (the pilot ex:ST_Plan_Gap_CrossB models the chains in one chapter); "
          "(4) the deck, the page and the manifest of the chapter are not changed (the page file keeps its SHA-256) and the page test 9.37.0 still ends exit 0 on the page; "
          "(5) the chapter checks Research/Ch01 to Research/Ch09 and the Research checks of the chapters retrofitted before still end PASS (a signal-timing claim may fail under load: report it, do not work around it); no committed file is edited; results as printed, measured by the controller by its own re-runs.")
LESSONS = {
    "all": ("LESSONS OF ITERATION 19 (the rules of this iteration): (1) A committed file is never edited - and that includes your OWN tool scripts, builders, data modules, test drivers and logs: every new version of any of them is a NEW file with a new version number FROM THE FIRST SAVE (do not save vX, commit it and then edit it; the controller found two such in-place edits by git and they were disclosed in the register); only a file you have not yet committed may be regenerated. "
            "(2) Report negative results first and as printed; a skip is not a pass; Cross.B CANNOT_RUN is not a pass. (3) The machine has two cores shared by up to three executors: every browser test runs under `flock /tmp/page_test.lock`; no build or corpus run beside a browser test of yours; a timing-sensitive check can fail under load - say so, rerun on a quiet machine, keep the failing log. "
            "(4) Everything you cite in your report is a commit you made and a file that exists; the controller re-runs every claim, so a report that says more than the files show is NOT MET."),
    "Deck_Build": ("DECK LESSONS: (a) FIRST-LINE ERROR SCAN: the page template draws a result as a chart or a table, but an output whose FIRST line matches ^(\\w*Error|Traceback|Stopped after) is drawn as text and the page test 9.37.0 (P2) then fails that example for want of a visual (six decks of chapters 1, 3 and 4 had to be repaired for this). Write every example whose purpose is to raise an error so that it prints an ordinary line FIRST (a heading line such as 'Result: ...' or the value before the error), and run `python3 08-tooling/sen0414_manifest_error_first_scan_v1_0_0.py 03-materials/chNN/page/chapter_code_chNN_v1_0_0.json` - it must print RESULT: PASS - before you report. "
                   "(b) The examples of the manifest run under Python 3.13 (the controller's interpreter for them) and print exactly the recorded result: run all of them and compare, and say how you did. (c) Story pictures are real pictures with a recorded licence, embedded in the deck; every story names who, what, when, where, why and how and has a live link. (d) The deck and its manifest are final when you report: the page task copies the manifest; a later deck repair costs a new deck, a new manifest and a rebuilt page. (e) Run the overlap check and fix every finding in a NEW deck version; report CLEAN or the findings as printed."),
    "Page_Build": ("PAGE LESSONS: (a) STORY LAYOUT, measured on EVERY story: the photograph of a story is lower than the viewport and the narrative paragraph begins within the first screen of the story. Run `flock /tmp/page_test.lock python3 08-tooling/sen0414_story_layout_probe_v1_0_0.py PAGE.html 08-tooling/chNN-page/story_layout_YOUR_RUN.log` on your page: it checks every story card at 1366x768, 1400x900 and 390x844, the FIRST story as the reader sees it when the Stories tab opens (no scrolling), the later ones with the card scrolled to the top. It is the controller's rule; your own probe must be at least as strict - a looser rule of your own does not count, a stricter one is welcome. Portrait photographs (a head and shoulders) must be cropped or sized so that they do not fill the phone screen. "
                   "(b) The first-line error scan of the manifest (`sen0414_manifest_error_first_scan_v1_0_0.py`, see the deck lesson) must print PASS on the manifest you build from; if it does not, STOP and report - the deck is repaired by a new deck version and a new manifest, never by editing. (c) The Lab / Playground examples pane takes its examples from a NEW examples file made FROM THE MANIFEST (same code, same order), not from an older examples file. (d) The page file names: `03-materials/chNN/page/sen0414_chNN_page_v9_95_0.html` and the page inputs under the v9_95_0 name; if you need another version name, STOP and report. (e) Run page tests 9.37.0 and 9.34.0 on the page, serially under the lock, and keep every log, the failing ones too."),
    "Research": ("RESEARCH LESSONS: (a) The page-ABox builder is `08-tooling/sen0414_page_abox_build_v1_1_13.py`; it knows every visual kind of chapters 1 to 9. If it stops on a visual kind of YOUR page, write `sen0414_page_abox_build_v1_1_14.py` as a NEW file over v1_1_13 (never edit v1_1_13) and say which kind. (b) NAME THE PAGE ABOX `03-materials/chNN/page/sen0414_chNN_page_abox_v9_95_0.ttl`: the gate ranks page ABoxes by version, and the chapter check must pick the one that describes the new page. No older page ABox exists for this chapter; the name keeps that true for the next version too. "
                 "(c) COMPARE old and new with a script of your own (a NEW tool file) before you report, and list every difference with its reason: individuals, classes, links, sources, labels. In chapters 1 to 5 the new page showed static examples where the old widgets had step-through primitives and some widgets lost links; each such loss was stated and judged. State yours. (d) The execution checks of this chapter fail on the controller's machine today (log 08-tooling/control-iter20-logs/pre_Research_ChNN.log): read the mismatches first. A claim whose output depends on an installed package, a service, the clock or the machine's load must be made reproducible - for example by running it in an isolated virtual environment that the data module builds itself, with a stated package version, or with a wide time limit - or be reported as printed; do not weaken the claim, do not delete it, do not skip it. A signal-timing claim that waits 0.3 s and demands an answer in 3 s fails under load: use limits that load cannot break. "
                 "(e) The controller runs the chapter check on its machine with the python3.14 on its path; your claims must pass there, under the load of other sessions."),
}


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)


def first_note(t, name):
    i, j = blk(t, name); m = re.search(r'backlog:hasAuditNote "((?:[^"\\]|\\.)*)"', t[i:j]); assert m, name
    return m.group(1).replace('\\"', '"').replace("\\\\", "\\")


def adapt(note, ch):
    title, short = CH[ch]; m = measured(ch)
    s = note.replace("chapter 5 (Debugging)", "chapter %d (%s)" % (int(ch), title)).replace("chapter 5", "chapter %d" % int(ch)).replace("ch05", "ch" + ch).replace("Ch05", "Ch" + ch).replace("SEN0414-I19", "SEN0414-I20")
    s = s.replace("(above 9_28_0; the pages of chapters 6 to 9 are v9_90_0)", "(the new page is **v9_95_0**: `03-materials/ch%s/page/sen0414_ch%s_page_v9_95_0.html`, above the chapter's newest page %s; the pages of chapters 1 to 9 are v9_90_0 to v9_92_0)" % (ch, ch, os.path.basename(m["page"])))
    s = s.replace("named as the chapter's earlier decks are named", "named like the decks of chapters 6 to 9: `03-materials/ch%s/SEN0414_Ch%s_%s_3e_v2_0_0.pptx`" % (ch, ch, short))
    s = s.replace("and run the chapter check Page/Ch09", "and run the chapter check Page/Ch%s if it has the case for the chapter (the controller does not rely on it; report what it prints)" % ch)
    s = s.replace("Research/Ch06 to Research/Ch09 still end PASS", "Research/Ch01 to Research/Ch09 and the Research checks of the chapters retrofitted before still end PASS")
    assert "chapter 5" not in s and "ch05" not in s, ch
    return s


def research_note(ch):
    title, short = CH[ch]
    return ("Make the research set of chapter %d (%s) pass the chapter check Research/Ch%s, with its FIRST page ABox, which describes the NEW page. Read the criterion (ex:AC2F_RetrofitResearch20) and the precedents first: the chapters 1 to 5 of Iteration 19 (research task commits of chapters 2 to 5: `git log --oneline -- 03-materials/ch05/rdodi 03-materials/ch05/page 08-tooling/ch05-research`; the comparison tools 08-tooling/sen0414_ch0N_page_abox_compare_v1_0_0.py; the data module 08-tooling/sen0414_ch05_rdodi_data_v1_3_0.py and its restore script), chapter 6 (data module 08-tooling/sen0414_ch06_rdodi_data_v2_2_0.py, page ABox 03-materials/ch06/page/sen0414_ch06_page_abox_v1_4_0.ttl) and chapter 7 (data module v1_3_0, how a data module is made from a corpus). "
            "THE DIFFERENCE FROM CHAPTERS 1 TO 5: this chapter has no page ABox yet (the gates' Stage 4 and Cross.B have never run for it); its research files may already pass (see the facts) - then they are NOT rebuilt - or its execution checks fail on this machine (see the facts and the log): then a NEW data version and NEW files are needed. "
            "Nothing is invented: content comes from the book's chapter, the deck, the page and the existing files. A committed file is never edited. STOP and report if the task cannot be satisfied without editing a committed file, a gate, a test or a threshold beyond the named new files. Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN); Cross.B CANNOT_RUN is reported as such and is not a pass. The machine has 2 cores shared by up to three executors: no build beside a browser test. "
            "Planned session SEN0414-I20-research-ch%s; estimated 4.0 hours (an estimate, G120: nobody has witnessed a start; the real start is recorded at work begun). Starts when the page of the chapter is controlled (the page ABox describes the new page)." % (int(ch), title, ch, ch))


def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Plan Iteration 20: the retrofit of chapters 10 to 25 to the written standard, the Cross.B gap as a pilot, and the withdrawal of the story of the remaining chapters"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope2 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit(DIRECTION + " The scope does not move outward: the planned stories were admitted at the owner's decision (ex:CR2_Priority3); this change plans them, adds the tasks, one criterion for the research set of chapters 10 to 25, and withdraws the story that has nothing left to build."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What planning Iteration 20 changes, with the facts measured before it is planned"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage2 ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(facts_global() + " " + GAPS + " WHAT MOVES: the Backlog stage is revised once more (G125 route 2). Iter_20 gets its start (the planning ceremony), its end (seven days, G9), its sprint goal, the sixteen stories of chapters 10 to 25 (Ready, scored, six tasks each: 96 tasks) and the Cross.B story (Ready, scored, four tasks): 100 tasks; "
                    "the story ex:ST_Plan_Remaining is withdrawn (Cancelled) on the measurement of fact 1; the retrofit criterion ex:AC2F_Retrofit is restated for these chapters and ex:AC2F_RetrofitResearch20 is added; ex:AC2F_CrossB is planned as a pilot on chapter 6; the exclusion ex:Excl2_NoRebuild is lifted for the NEW files of chapters 10 to 25 and the pilot only. "
                    "RE-RANKING of the open items (WSJF: business value 20; time criticality 20 for chapter 10 down to 5 for chapter 25, the owner's order of chapters; risk reduction = the deck-standard elements measured failing + 2 for Stage 4 never run (no page ABox) + 1 where the chapter check fails on the execution checks; job size 14.5 h): the order is chapter 10, 11, ..., 25; inside a chapter the order of the dependencies (deck, deck control, page, research set and page ABox, research control, page control); the Cross.B pilot after chapter 25 (business value 8, time criticality 4, risk reduction 1, job size 8.5 h). "
                    "BATCHES (the plan of the controller, not a promise): at most THREE executor sessions at once; the next startable task of the highest-ranked chapter takes a free place; deck builds and research sets run side by side, page builds one at a time (they hold the page-test lock for hours), the controller's page tests wait in the same queue; the Cross.B pilot takes a place only when no higher-ranked task can start. Not in the plan: a rebaseline, a waiver, an edit of a gate or test, a new metric."))
    return t + cr + ia, "ChangeRequest ex:CR2_Iter20 (Pending) and ImpactAssessment ex:IA2_Iter20: plan the retrofit of chapters 10 to 25 and the Cross.B pilot as Iteration 20, withdraw the story of the remaining chapters; no stage changed."


def ev_retract(t):
    t = S.set_status(t, "LS_Objectived")
    reason = (DIRECTION + " Stories become Ready with scores and tasks, a criterion is added and another restated, a story is withdrawn: the closed Backlog stage's digest moves (G117, G125 route 2): a StageRevision from the Backlog stage, never from the Mission; the change request " + CR[3:] + " and the impact assessment " + IA[3:] + " were recorded first. "
              "This version retracts the Backlog output " + OLD[3:] + " and rebuilds nothing; the next version closes the Backlog stage again as " + NEW[3:] + " and re-admits every item without re-dating any; a third version fills the commit. The retracted output and its digest stay as history (L-112).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the second lineage from the Backlog stage: Iteration 20 planned for the retrofit of chapters 10 to 25 and the Cross.B pilot"@en ;\n'
         '    backlog:revisesLineage ex:Lineage2 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n'
         '    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return t + b, "StageRevision of the second lineage from the Backlog stage (G125 route 2) for the planning of Iteration 20: the Backlog output Out2_BacklogR10 is retracted; nothing is rebuilt in this version."


def task_block(tid, label, typ, cat, deps, audit, sess, est, start_note):
    return ('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n'
            '    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_20 ; backlog:admittedByOutput %s ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n'
            '    backlog:hasInvestmentCategory backlog:%s ; backlog:hasTaskType backlog:%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Ready ;\n'
            '    backlog:dependsOn %s ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote %s .\n') % (
        tid, lit(label), tid, lit(label), NEW, cat, typ, ", ".join(deps), lit(audit + " Estimated %.1f hours (an estimate, G120: nobody has witnessed a start; the real start is recorded at work begun). %s" % (est, start_note)))


def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision ;.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = S.set_status(t, "LS_Backlogged"); n = now(); L = []
    cnt = len(re.findall(r"admittedByOutput ex:Out2_BacklogR10\b", t)); assert cnt >= 100, cnt
    t = re.sub(r"admittedByOutput ex:Out2_BacklogR10\b", "admittedByOutput " + NEW, t)
    end = (datetime.datetime.strptime(n, "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
    REPAIRED = ["TK_Std_TemplateFix_Verify", "TK_Std_Runner_Verify", "TK_Std_Regress", "TK_Std_Charset_Verify", "TK_Std_PageTest37_Verify"]
    for x in REPAIRED + ["TK_Std_DeckCheck", "TK_Std_ResearchCh06_Verify"]:
        assert ("\nex:%s a backlog:ExecutionTask" % x) in t, x
    base05 = {k: first_note(t, "TK_Ret_Ch05_" + k) for k in EST}
    members = []; plans = []; rank = []
    for ch, (title, short) in CH.items():
        sid = "ST_Plan_Retrofit_Ch" + ch; base = "ex:TK_Ret_Ch%s_" % ch; m = measured(ch); facts = fact(ch)
        notes = {"Deck_Build": adapt(base05["Deck_Build"], ch) + " " + LESSONS["Deck_Build"], "Page_Build": adapt(base05["Page_Build"], ch) + " " + LESSONS["Page_Build"],
                 "Research": research_note(ch) + " " + LESSONS["Research"], "Deck_Verify": adapt(base05["Deck_Verify"], ch), "Research_Verify": adapt(base05["Research_Verify"], ch), "Page_Verify": adapt(base05["Page_Verify"], ch)}
        notes["Deck_Verify"] += " Also run the first-line error scan (sen0414_manifest_error_first_scan_v1_0_0.py) on the manifest and the deck-check's M1."
        notes["Page_Verify"] += " Also run the story-layout probe (sen0414_story_layout_probe_v1_0_0.py) on every story at 1366x768, 1400x900 and 390x844 and compare with the executor's own."
        specs = [("Deck_Build", "Rebuild the deck of chapter %d (%s) against the deck standard and give it its chapter-code manifest" % (int(ch), title), "TaskType_Build", "Cat_NewCapability", ["ex:TK_Std_DeckCheck"], "SEN0414-I20-deck-ch" + ch, "Starts first in the chapter: the later tasks depend on its control."),
                 ("Deck_Verify", "Verify the deck of chapter %d against the deck standard" % int(ch), "TaskType_Verify", "Cat_Compliance", [base + "Deck_Build", "ex:TK_Std_DeckCheck"], "SEN0414-lineage (control)", ""),
                 ("Page_Build", "Rebuild the page of chapter %d (%s) on the new template with the chapter-code tab" % (int(ch), title), "TaskType_Build", "Cat_NewCapability", [base + "Deck_Verify"] + ["ex:" + x for x in REPAIRED], "SEN0414-I20-page-ch" + ch, "Starts when the deck of the chapter is controlled."),
                 ("Research", "Make the research set and the first page ABox of chapter %d (%s) pass the chapter check on the new page" % (int(ch), title), "TaskType_Build", "Cat_Maintenance", [base + "Page_Build", "ex:TK_Std_ResearchCh06_Verify"], "SEN0414-I20-research-ch" + ch, "Starts when the page of the chapter is controlled (the page ABox describes the new page); the research set itself may be prepared earlier but its page ABox is built last."),
                 ("Research_Verify", "Verify the research set and the page ABox of chapter %d" % int(ch), "TaskType_Verify", "Cat_Compliance", [base + "Research"], "SEN0414-lineage (control)", ""),
                 ("Page_Verify", "Verify the page of chapter %d against the page standard" % int(ch), "TaskType_Verify", "Cat_Compliance", [base + "Page_Build", base + "Research_Verify", "ex:TK_Std_PageTest37_Verify"], "SEN0414-lineage (control)", "")]
        tks = []
        for key, label, typ, cat, deps, sess, sn in specs:
            tid = "TK_Ret_Ch%s_%s" % (ch, key); audit = notes[key] + (" Planned session %s." % sess)
            if key in ("Deck_Build", "Page_Build", "Research"):
                audit = audit
            L.append(task_block(tid, label, typ, cat, deps, audit, sess, EST[key], sn)); tks.append("ex:" + tid)
            if key in ("Deck_Build", "Page_Build", "Research"):
                L.append('ex:%s backlog:hasAuditNote %s .\n' % (tid, lit("Facts for this task, measured 2026-10-25 UTC by the lineage agent: " + facts + " " + LESSONS["all"])))
        members += [sid] + [x[3:] for x in tks]
        i, j = blk(t, sid); b = t[i:j]
        old = 'backlog:hasState backlog:Proposed ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored when its own iteration is planned." ;'
        assert old in b, sid
        b = b.replace(old, 'backlog:decomposesInto %s ;\n    backlog:hasState backlog:Ready ;\n    backlog:hasPriorityScore ex:Score30_%s ;' % (", ".join(tks), sid))
        b = b.replace(" (planned)", "").replace("backlog:hasAcceptanceCriterion ex:AC2F_Retrofit ;", "backlog:hasAcceptanceCriterion ex:AC2F_Retrofit, ex:AC2F_RetrofitResearch20 ;")
        t = t[:i] + b + t[j:]
        val = (20 + TC[ch] + m["rr"]) / SIZE; rank.append((val, ch))
        L.append('ex:Score30_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
            sid, val, n, lit("WSJF = (business value 20 + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. Inputs from observable facts: job size is the sum of the story's task estimates in this register (%s); time criticality %d = place %d in the owner's order of chapters of Iteration 20 (20 = chapter 10, 5 = chapter 25); risk reduction %d = the deck-standard elements measured failing (%d) + 2 for Stage 4 never run (no page ABox) + %d where the chapter check fails on the execution checks (measured 2026-10-25 UTC). Scored on %s UTC at the planning of Iteration 20 (ex:CR2_Iter20); the earlier planned-and-unscored state is history." % (
                TC[ch], m["rr"], SIZE, val, ", ".join("%s %.1f h" % (k, v) for k, v in EST.items()), TC[ch], int(ch) - 9, m["rr"], m["deckfail"], 1 if m["res"] == "FAIL" else 0, n))))
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (sid, lit("PLANNED INTO ITERATION 20 on %s UTC (ex:CR2_Iter20, planning ceremony ex:PC2_Iter_20): Ready, scored, decomposed into six tasks (deck build, deck verify, page build, research set and page ABox, research verify, page verify). %s %s No executor has started; work begun is recorded at the real start of each executor session." % (n, facts, GAPS))))
        plans.append('ex:Plan2R20_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 20"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_20 ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec2S_D, ex:Scen2S_D_Passes, ex:Scen2S_D_NotClaimed, ex:Spec2S_P, ex:Scen2S_P_Passes, ex:Scen2S_P_NotClaimed .\n' % (sid, sid, n, sid, ", ".join(tks)))
    # the Cross.B pilot
    sid = "ST_Plan_Gap_CrossB"; base = "ex:TK_Gap_CrossB_"
    cbn = {
        "Spec": ("Specify the hybrid chains of a chapter as the gate Cross.B measures them, for the pilot chapter 6. Read the gate first: `08-tooling/sen0414_rdodi_gates_v1_1_1.py`, function gate_provenance (Cross.B): what it calls a hybrid chain (a chain that crosses the research document, the domain ontology and the page ABox), which links it follows, what it counts as checked and as broken, and why it prints CANNOT_RUN with 0 chains. Then write the specification as SHACL and data, not as markdown (rulings are never kept as markdown): a NEW file `08-tooling/crossb/crossb_chain_shapes_v1_0_0.ttl` (SHACL shapes of a hybrid chain exactly as the gate reads it) and a NEW file `08-tooling/crossb/crossb_chain_model_v1_0_0.json` (for chapter 6: the proposed chains as ordered lists of the existing individuals of its research files and its page ABox 03-materials/ch06/page/sen0414_ch06_page_abox_v1_4_0.ttl, each chain with the links that would be added, and the count of chains). A chain uses only links to existing individuals (links are links, never text); nothing is invented; no gate, test or threshold is edited; if the gate cannot count any chain without an edit of the gate, STOP and report with the line numbers. Report what the gate would print for the proposed chains by running the gate on a scratch copy of the graph (no committed file is touched)."),
        "Spec_Verify": ("Control of the specification: read the gate's gate_provenance, re-derive the definition of a hybrid chain from the gate's code, check that every chain of the model uses existing individuals and only the links the gate follows, and run the gate on a scratch copy with the chains added; the decision 'what a hybrid chain of this course is' is taken by the controller by this reading and recorded in the register with its reasons (the rule: the gate's own definition; the owner decided that decisions rest on rules and provable facts). Done or NOT MET, no waiver."),
        "Build": ("Build the hybrid chains of the pilot chapter 6 as NEW files: a NEW version of the chapter 6 research ABox and/or page ABox (for example `03-materials/ch06/page/sen0414_ch06_page_abox_v1_5_0.ttl` over v1_4_0 - a NEW file, the committed one byte-identical) that adds the links of the controlled specification, built by a NEW builder file (the page-ABox builder v1_1_13 is the newest; a change is a NEW version file), then run the chapter check Research/Ch06: it must end PASS with Cross.B printing a number of chains checked ABOVE ZERO and none broken, instead of CANNOT_RUN, and Stage4.A, B, cov, sub and src still passing; Research/Ch01 to Research/Ch09 still PASS. No gate, test or threshold is edited; no existing individual, class or link of chapter 6 is removed (compare old and new with a script of your own and list every difference). Report as printed."),
        "Build_Verify": ("Control of the pilot: re-run the chapter check Research/Ch06 and Research/Ch01 to Research/Ch09 on the controller's own account, read Cross.B (above zero, none broken) and Stage 4, compare the old and new sets of individuals, classes, links, sources and labels of chapter 6 (a difference without a stated reason is NOT MET), check that every committed file is byte-identical. Done or NOT MET, no waiver; Cross.B for the other 24 chapters stays CANNOT_RUN and is said so.")}
    cbs = [("Spec", "Specify the hybrid chains of the gate Cross.B for the pilot chapter 6", "TaskType_Build", "Cat_Maintenance", ["ex:TK_Std_ResearchCh06_Verify"], "SEN0414-I20-crossb-spec", "Takes a place only when no higher-ranked task can start."),
           ("Spec_Verify", "Verify the specification of the hybrid chains and decide what a hybrid chain of this course is", "TaskType_Verify", "Cat_Compliance", [base + "Spec"], "SEN0414-lineage (control)", ""),
           ("Build", "Model the hybrid chains in new chapter 6 ABox files so that Cross.B measures them", "TaskType_Build", "Cat_Maintenance", [base + "Spec_Verify"], "SEN0414-I20-crossb-build", "Starts when the specification is controlled."),
           ("Build_Verify", "Verify the pilot: Cross.B above zero and none broken in chapter 6", "TaskType_Verify", "Cat_Compliance", [base + "Build"], "SEN0414-lineage (control)", "")]
    tks = []
    for key, label, typ, cat, deps, sess, sn in cbs:
        tid = "TK_Gap_CrossB_" + key
        L.append(task_block(tid, label, typ, cat, deps, cbn[key] + " " + LESSONS["all"] + " Planned session %s." % sess, sess, CBEST[key], sn)); tks.append("ex:" + tid)
    members += [sid] + [x[3:] for x in tks]
    i, j = blk(t, sid); b = t[i:j]
    old = 'backlog:hasState backlog:Proposed ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored when its own iteration is planned." ;'
    assert old in b, sid
    b = b.replace(old, 'backlog:decomposesInto %s ;\n    backlog:hasState backlog:Ready ;\n    backlog:hasPriorityScore ex:Score30_%s ;' % (", ".join(tks), sid)).replace(" (planned)", "")
    t = t[:i] + b + t[j:]
    cbv = (8 + 4 + 1) / CBSIZE
    L.append('ex:Score30_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
        sid, cbv, n, lit("WSJF = (business value 8 + time criticality 4 + risk reduction 1) / job size %.1f h = %.2f. Business value 8: a maintenance story on the gates, not new teaching material; time criticality 4: it is planned after the owner's order of chapters; risk reduction 1: one gate element (Cross.B) has never produced a measured result in this course; job size is the sum of its task estimates (%s). Scored on %s UTC at the planning of Iteration 20." % (
            CBSIZE, cbv, ", ".join("%s %.1f h" % (k, v) for k, v in CBEST.items()), n))))
    L.append('ex:%s backlog:hasAuditNote %s .\n' % (sid, lit("PLANNED INTO ITERATION 20 on %s UTC (ex:CR2_Iter20, planning ceremony ex:PC2_Iter_20) AS A PILOT ON CHAPTER 6: Ready, scored, four tasks (specification, its control, build, its control). The decision 'what a hybrid chain of this course is' is taken by the controller from the gate's own definition (task TK_Gap_CrossB_Spec_Verify), by rule, without waiting for the owner. The model is carried to the other 24 chapters only by a further item. %s" % (n, GAPS))))
    plans.append('ex:Plan2R20_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 20"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_20 ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec2S_D, ex:Scen2S_D_Passes, ex:Scen2S_D_NotClaimed, ex:Spec2S_P, ex:Scen2S_P_Passes, ex:Scen2S_P_NotClaimed .\n' % (sid, sid, n, sid, ", ".join(tks)))
    for m_ in members:
        L.append('ex:Refine6_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_20 ;\n    backlog:hasRefinementOutcome %s .\n' % (
            m_, m_, m_, n, lit("Refined by the lineage agent from the owner decision of Friday 2026-10-23 16:06 Istanbul (13:06 UTC) (ex:CR2_Priority3), the direction of the course coordinator of 2026-10-25 and the measured facts of ex:IA2_Iter20: criterion with tools and versions, dependencies, estimates, the lessons of Iteration 19, a brief to be generated from the register; startable when its dependencies are Done.")))
    # the withdrawal of ST_Plan_Remaining
    rid = "ST_Plan_Remaining"; i, j = blk(t, rid); b = t[i:j]
    old = 'backlog:hasState backlog:Proposed ;'
    assert old in b
    why = ("Withdrawn on %s UTC by the change route ex:CR2_Iter20: the story waited for a measurement ('the list of chapters still lacking research, deck or page is measured when the retrofits finish'). Measured 2026-10-25: the repository holds research files (03-materials/chNN/rdodi), a deck (03-materials/chNN or 08-tooling/chNN-deck) and a page (03-materials/chNN/page) for each of the 25 chapters of the course (the 3rd edition's 24 chapters and the threads chapter 25 of the 2nd edition); no chapter lacks one of the three, so there is nothing to build from scratch. The standard-conformance of chapters 10 to 25 is the work of the 16 retrofit stories. If a chapter outside these 25 is named, or one is found lacking, a new story is made by the change route. Not a waiver: the work the story named is measured empty." % n)
    b = b.replace(old, 'backlog:hasState backlog:Cancelled ; backlog:hasRationale %s ;' % lit(why), 1)
    t = t[:i] + b + t[j:]
    L.append('ex:Withdraw2R20_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_WithdrawProposed ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (rid, lit(rid + " withdrawn"), rid, n, lit(why)))
    # Iter_20
    i, j = blk(t, "Iter_20")
    t = t[:i] + ('ex:Iter_20 a backlog:Iteration ; rdfs:label "Iteration 20: the chapter 10 to 25 decks, pages and research sets brought to the written standard, and the Cross.B pilot"@en ; backlog:hasIdentifier "Iter_20" ; backlog:belongsToLineage ex:Lineage2 ;\n'
                 '    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember ex:ST_Plan_Remaining, %s .\n') % (
        n, end, lit("Proposed by the lineage agent on %s: the start is the instant of the planning ceremony ex:PC2_Iter_20; the length is 7 days, constant (G9) - a stipulation, not a measurement (the class cadence). Justification of the work inside it (estimates, G120): 14.5 h per chapter (%s), 232 h for chapters 10 to 25, and 8.5 h for the Cross.B pilot; the heavy part is the browser tests, serial on the two cores, with at most three executors at once. This is NOT a promise that all sixteen chapters finish inside the seven days (gap d of ex:IA2_Iter20); chapter 10 first, and each chapter ships as soon as it is controlled." % (n, ", ".join("%s %.1f h" % (k, v) for k, v in EST.items()))),
        lit(GOAL), ", ".join("ex:" + m_ for m_ in members)) + t[j:]
    L.append('\nex:PC2_Iter_20 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 20: the chapter 10 to 25 retrofit and the Cross.B pilot"@en ; backlog:ceremonyFor ex:Iter_20 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent %s ;\n    rdfs:comment %s@en .\n' % (
        n, ", ".join(["ex:Plan2R20_ST_Plan_Retrofit_Ch" + c for c in CH] + ["ex:Plan2R20_ST_Plan_Gap_CrossB"]), lit("Held %s UTC by the lineage agent, after the review that closed Iteration 19 (ex:RC2_Iter_19) and on the direction of the course coordinator (ex:CR2_Iter20): the seventeen stories and their 100 tasks are committed to this iteration, whose goal is frozen at its start; the story ex:ST_Plan_Remaining is withdrawn. No executor has started; work begun is recorded at the real start of each executor session." % n)))
    L.extend("\n" + p for p in plans)
    L.append('\nex:PB2S_Iter_20 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 20 when it was planned"@en ; backlog:baselineFor ex:Iter_20 ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "%s"^^xsd:dateTime .\n' % (n, n, end))
    # criteria
    L.append('ex:AC2F_Retrofit backlog:hasAuditNote %s .\n' % lit("RESTATED %s UTC (ex:CR2_Iter20): the criterion is planned into Iteration 20 for chapters 10 to 25 on the same terms as for chapters 1 to 5 (the deck standard check, the deck overlap check, the page test 9.37.0 and 9.34.0 under the runner v1_1_0; the chapter-code manifest 03-materials/chNN/page/chapter_code_chNN_v1_0_0.json equals the deck's code boxes, text and order; the first-line error scan of the manifest passes; the story-layout rule holds for every story at 1366x768, 1400x900 and 390x844); the new deck of a chapter 10 to 25 goes to 03-materials/chNN (the earlier deck stays in 08-tooling/chNN-deck); the research set is the criterion ex:AC2F_RetrofitResearch20; no committed file is edited." % n))
    L.append('\nex:AC2F_RetrofitResearch20 a backlog:AcceptanceCriterion ; rdfs:label "The research set and the first page ABox of a retrofitted chapter 10 to 25 pass the chapter check Research on the new page"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool ex:TS2_RdodiGates, ex:TS2_ChapterCheck, ex:TS2_PageAboxBuild13 ;\n    backlog:measuredWithVersion "chapter check v1_1_0; RDODI gates v1_1_1; RDODI checks v1_2_0; generic builder v1_2_0; page-ABox builder v1_1_13 (or a newer new-file version); the page test 9.37.0; Python 3.14, HermiT" ;\n    backlog:satisfiedByArtifact "the new files cited by SHA-256, the controller\'s own runs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC2R6_Passes, ex:TC2R6_NotClaimed, ex:TC2R6B_PageAbox .\n' % lit(GH_RES))
    L.append('ex:TS2_PageAboxBuild13 a backlog:ToolScript ; rdfs:label "page-ABox builder v1_1_13 (new file over v1_1_12; knows the visual kinds names and floatbits)"@en ; backlog:scriptFileName "sen0414_page_abox_build_v1_1_13.py" ; backlog:acceptsGraphPath false .\n')
    i, j = blk(t, "AC2F_CrossB"); b = t[i:j]; assert "PLANNED, NOT STARTED (ex:CR2_ResFix06C). Given" in b
    t = t[:i] + b.replace("PLANNED, NOT STARTED (ex:CR2_ResFix06C). Given", "Planned into Iteration 20 (ex:CR2_Iter20) as a PILOT on chapter 6. Given", 1) + t[j:]
    L.append('ex:AC2F_CrossB backlog:hasAuditNote %s .\n' % lit("RESTATED %s UTC (ex:CR2_Iter20): the criterion is met for the PILOT chapter 6 only (the chapter's chains are modelled in new ABox files, Cross.B prints a number of chains above zero and none broken); the other 24 chapters stay CANNOT_RUN and are said so; the decision what a hybrid chain of this course is is taken from the gate's own definition by the controller (task TK_Gap_CrossB_Spec_Verify). Not a waiver: the scope is stated, not reduced silently." % n))
    L.append('ex:Excl2_NoRebuild rdfs:comment "Lifted on %s UTC (ex:CR2_Iter20) for chapters 10 to 25, ONLY for the NEW files of their decks, chapter-code manifests, pages, research sets, data modules and page ABoxes (the retrofit of Iteration 20), and for the NEW chapter 6 ABox files of the Cross.B pilot: no existing deck, research run, page or page ABox of these chapters is changed."@en .\n' % n)
    L.append('ex:SC2_Iter20 a backlog:ScopeChange ;\n    rdfs:label "One hundred tasks and one criterion admitted for the retrofit of chapters 10 to 25 and the Cross.B pilot in Iter_20; the story of the remaining chapters withdrawn"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope2 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        CR, ", ".join("ex:" + m_ for m_ in members if m_.startswith("TK_")), lit(DIRECTION + " The boundary does not move outward in deliverables; the stories were admitted by the owner's decision, these are their tasks.")))
    t, k = re.subn(r'(ex:CR2_Iter20 a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m_: m_.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert k == 1
    L.append('ex:CR2_Iter20 rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC2_Iter20; it was Pending before. The release is the owner\'s decision of 2026-10-23 (ex:CR2_Priority3) and the coordinator\'s direction; the owner is not waited for."@en .\n' % n[:10])
    t += "\n" + "".join(L)
    out = ('\n%s a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the second lineage, rebuilt for the planning of Iteration 20"@en ;\n    backlog:belongsToLineage ex:Lineage2 ;\n'
           '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out2_ObjectiveR1 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (NEW, S.digest(t, "Backlog"))
    return t + out, "second lineage, Backlog stage rebuilt: Iteration 20 planned (chapters 10 to 25: sixteen Ready scored stories, 96 tasks; the Cross.B pilot: Ready, scored, four tasks; ceremony, baseline, goal), the story of the remaining chapters withdrawn on the measurement that nothing remains, the research criterion for chapters 10 to 25 added, the exclusion lifted for their new files, ScopeChange, change request Accepted, every item re-admitted."


def ev_fill(t, prev):
    t = W.fill_re(t, NEW, prev)
    return t, "closedAtCommit of the rebuilt Backlog output Out2_BacklogR11 set to the commit that closed it (%s); the revision is complete and no work is begun in this version." % prev


def main():
    ev = sys.argv[1]; src = W.newest(); t = open(src, encoding="utf-8").read(); arg = sys.argv[2] if len(sys.argv) > 2 else None
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, arg), "fill": lambda: ev_fill(t, arg)}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(W.write_new(src, nt, comment)))


if __name__ == "__main__":
    main()
