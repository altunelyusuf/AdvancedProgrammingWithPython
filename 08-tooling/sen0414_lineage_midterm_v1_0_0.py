#!/usr/bin/env python3
"""sen0414_lineage_midterm v1_0_0 - urgency ceremony for the Owner's instruction of 2026-11-01 12:13 Istanbul (confirmed 12:26: 'today we should finish both the Midterms and midterm scope work'):
bring SEN0414 chapters 1 to 7 to the Chapter 8 Friday standard (chapter 8 is done). Same route as the Chapter 8 emergency (ceremony G158, framework tool backlog_urgency_v1_0_0): one new register version with the
stories ST_MS_Ch01..07 (one task to build deck+manifest+page, one to verify), criteria, scores (re-ranked), refinements and the box Iter_MS, then one UrgentInterruption for each running lineage.
Usage: sen0414_lineage_midterm_v1_0_0.py declare
       NOW=2026-11-01T09:27:37 sen0414_lineage_midterm_v1_0_0.py begun ch07=09:27:37 ch04=09:27:38 ch01=09:27:39"""
__version__ = "1.0.0"
import hashlib, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
import sen0414_lineage_brief_midterm_v1_0_0 as B
URG = "/home/claude/altunelyusuf/backlog-roadmap-framework/03-tooling/backlog_urgency_v1_0_0.py"
GATE = "/home/claude/altunelyusuf/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_6_0.py"
NS = "http://example.org/sen0414-slides-lineage#"
BRIEFS = "08-tooling/briefs/midterm/r1"
WHEN = "2026-11-01 12:13 Istanbul (09:13Z), confirmed 12:26"
ORDER = ["07", "04", "01", "05", "02", "03", "06"]          # by gap size and exam value
TC = dict(zip(ORDER, [20, 19, 18, 16, 15, 14, 12]))
RR = {"01": 4, "02": 5, "03": 4, "04": 7, "05": 6, "06": 5, "07": 7}   # failing elements counted in the measured fit-gap logs (deck check + controller C1-C8), see logs
lit = W.lit
OWNER = ("OWNER INSTRUCTION of " + WHEN + ", relayed by the course coordinator and recorded as relayed. 12:13: 'Do you think the files you provided are ready to share? The source codes in the slides should match with the interactive page of that chapter's Chapter Examples in the Lab. "
         "You need to bring the files to the quality level of the files we have generated in our last Friday work and adapt all Midterm scope to this level before sharing them.' 12:26: 'Simplify the tasks of the agents to concentrate on the issues we have solved on Friday, and pass the useless effort spent to remeasure the already succeeded parts.' "
         "Pacing (12:2x): 'Today we should finish both the Midterms and midterm scope work.' Midterm scope for the lineage agent = SEN0414 chapters 1 to 8 (chapter 5 assumed in, his 'Chapter 1-4 & 5-8'); chapter 8 is already at the standard. "
         "Friday fixes to apply per chapter: no '>>>' prompts, no untaught lambda, indented code, slides that teach alone, 5N1K as storytelling without labels, slide code equal to the page's Chapter Examples tab in slide order, page full screen + resizable panel + a Lecture tab matching the deck. "
         "Route: URGENCY CEREMONY (framework ruling G158, same route as the Chapter 8 emergency of 2026-10-30): the Owner set a same-day target and ranked this above all other work; not change management. The chapter 8 held repair TK_CI5_Page_Ch08_Repair and the exam repairs are re-ranked behind it; nothing is waived, no gate weakened.")
RULE = ("Route: URGENT INTERRUPTION (G158): the items are not admitted by a scope change; the running lineages are paused by the recorded interruption; the interruption ends when the urgent items are Done or Cancelled, and each lineage resumes with an impact assessment. "
        "Re-ranking by WSJF (business value 20; time criticality 20 down to 12 in the order chapter 7, 4, 1, 5, 2, 3, 6 = gap size and exam value; risk reduction = failing elements measured in the as-is fit-gap).")
VERIFY = ("Control by the lineage agent on its OWN re-runs, never the executor's output: deck standard check v1_1_0 (13 of 13), teaching check T1-T6, overlap check, the controller's checks C1-C8 (prompts, lambda, indentation, label words, notes 40-60 words, compile, numbered, manifest equals the code boxes in order), "
          "the page test 9.38.0 and 9.37.0 under the page-test lock (repeated runs printed as they come), the leak probe, Playground width probe, story-layout probe, chapter check, the chapter-code tab against the manifest, the slides rendered and read. A failing run is a result, not a pass. Estimated 1.7 hours.")

def fitgap(ch):
    return "As-is fit-gap (measured 2026-11-01 by the lineage agent, logs 08-tooling/control-u8-logs/deckcheck_ch01_08 and fitgap_ch01_08): " + B.gap(ch).replace("\n", " ")[:3000]

def build(src):
    t0 = open(src, encoding="utf-8").read(); now = W.now(); out = []; tasks = []; members = []
    for ch in ORDER:
        sid, bt, vt, ac = "ST_MS_Ch" + ch, "TK_MS_Ch%s_Build" % ch, "TK_MS_Ch%s_Verify" % ch, "AC2M_Ch" + ch
        h = B.HOURS[ch]; size = h + 1.7; v = (20 + TC[ch] + RR[ch]) / size
        out.append(f'ex:{ac} a backlog:AcceptanceCriterion ; rdfs:label {lit("Chapter %s (%s): deck, manifest and page meet the Chapter 8 Friday standard" % (ch, B.TITLE[ch]))}@en ; backlog:belongsToLineage ex:Lineage2 ;\n'
                   f'    backlog:hasGherkinText {lit("Given the newest deck and page of SEN0414 Chapter %s, when the new deck, manifest and page are built as new files, then ALL of: (1) deck check v1_1_0 reports 13 of 13, the teaching check T1-T6 and the overlap check report every element met; (2) the controller's own checks find no prompt, no lambda, every body line indented deeper than its header in multiples of four spaces, no label words, notes of 40 to 60 words, every box compiles (a deliberate-error box says so); (3) the manifest lists the code boxes in slide order and the page's chapter-code tab equals it; (4) the page test 9.38.0 and 9.37.0, leak, Playground width and story-layout probes and the chapter check report as printed, every diagram has full screen and a resizable panel, no lambda or prompt in the page code; (5) no committed file is edited; NOT_MEASURED and CANNOT_RUN are not passes." % ch)} ;\n'
                   f'    backlog:measuredWithTool ex:TS2_DeckStdCheck, ex:TS2_DeckOverlap, ex:TS2_PageTest36, ex:TS2_ChapterCheck ;\n'
                   f'    backlog:measuredWithVersion "existing checks run unchanged (deck check v1_1_0, teaching check v1_0_0, overlap check v1_0_0, page tests 9.37.0 and 9.38.0, leak probe v1_3_0, chapter check v1_2_0); Playwright 1.56.0; python-pptx 1.0.2" ;\n'
                   f'    backlog:satisfiedByArtifact "the new files cited by SHA-256, the logs of the controller\'s own runs" ;\n    backlog:coveredByCase ex:TC2M_Ch{ch}_Passes .\n')
        out.append(f'ex:TC2M_Ch{ch}_Passes a backlog:TestCase ; rdfs:label {lit("Run the Friday-standard checks on the new files of chapter %s and require no failure and no skip" % ch)}@en ; backlog:belongsToLineage ex:Lineage2 ;\n'
                   f'    backlog:exercisesCriterion ex:{ac} ; backlog:coversScenario ex:Scen2S_D_Passes ; backlog:runsOnData ex:Data2S_D_Passing ;\n    backlog:hasCaseText "Run the checks of the criterion over the new files on the controller\'s own machine; they report no failure and exit 0, or the failing elements are named." .\n')
        out.append(f'ex:{sid} a backlog:Story ; rdfs:label {lit("Chapter %s (%s) deck, manifest and page at the Chapter 8 Friday standard" % (ch, B.TITLE[ch]))}@en ; backlog:hasIdentifier "{sid}" ; backlog:hasTitle {lit("Chapter %s (%s) deck, manifest and page at the Chapter 8 Friday standard" % (ch, B.TITLE[ch]))} ;\n'
                   f'    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_MS ; backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
                   f'    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability {lit("the deck and page of Chapter %s teach on their own, the deck code equals the page's Chapter Examples tab in slide order, and every diagram has full screen and a resizable panel" % ch)} ; backlog:soThat "the instructor can share the midterm-scope materials with the students" ;\n'
                   f'    backlog:satisfiesDeliverable ex:Del2_StdDecks, ex:Del2_StdPages ; backlog:pursuesObjective ex:Obj2_StdDecks, ex:Obj2_StdPages ; backlog:hasAcceptanceCriterion ex:{ac} ;\n'
                   f'    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ; backlog:decomposesInto ex:{bt}, ex:{vt} ;\n'
                   f'    backlog:hasState backlog:Ready ; backlog:hasPriorityScore ex:Score1_{sid} ;\n    backlog:hasAuditNote {lit(OWNER)} ,\n        {lit(RULE)} ,\n        {lit(fitgap(ch))} .\n')
        bf = os.path.join(BRIEFS, "BRIEF_TK_MS_Ch%s_Build.md" % ch)
        bnote = ("Executor brief: %s (generated by sen0414_lineage_brief_midterm_v1_0_0.py from the measured logs; the coordinator passes it unedited). Bring chapter %s to the Chapter 8 Friday standard: new deck, new manifest (pushed first), new page on template 9.53.1, as new files; fix only the measured gaps, reuse the Chapter 8 tools, run the existing gates once at the end. Planned session SEN0414-MS-ch%s. Estimated %.1f hours (an estimate, G120: nobody has witnessed a start; the real start is recorded at work begun)." % (bf, ch, ch, h))
        out.append(f'ex:{bt} a backlog:ExecutionTask ; rdfs:label {lit("Build deck, manifest and page of Chapter %s at the Chapter 8 Friday standard (midterm scope)" % ch)}@en ; backlog:hasIdentifier "{bt}" ; backlog:hasTitle {lit("Build deck, manifest and page of Chapter %s at the Chapter 8 Friday standard (midterm scope)" % ch)} ;\n'
                   f'    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_MS ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasTaskType backlog:TaskType_Build ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Ready ;\n'
                   f'    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote {lit(bnote)} .\n')
        out.append(f'ex:{vt} a backlog:ExecutionTask ; rdfs:label {lit("Verify Chapter %s on the controller's own re-runs (midterm scope)" % ch)}@en ; backlog:hasIdentifier "{vt}" ; backlog:hasTitle {lit("Verify Chapter %s on the controller's own re-runs (midterm scope)" % ch)} ;\n'
                   f'    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_MS ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n    backlog:hasInvestmentCategory backlog:Cat_Compliance ; backlog:hasTaskType backlog:TaskType_Verify ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Ready ;\n'
                   f'    backlog:dependsOn ex:{bt} ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote {lit(VERIFY)} .\n')
        out.append(f'ex:Score1_{sid} a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ; backlog:hasScoreValue "{v:.2f}"^^xsd:decimal ; backlog:scoredAt "{now}"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n'
                   f'    backlog:hasScoreRationale {lit("WSJF = (business value 20 + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. Urgent item (ex:%s): the Owner set a same-day target; time criticality follows the order chapter 7, 4, 1, 5, 2, 3, 6 (gap size and exam value); risk reduction is the number of failing elements counted in the measured as-is fit-gap; job size is build %.1f h plus control 1.7 h (estimates, G120)." % (TC[ch], RR[ch], size, v, sid, h))} .\n')
        for x in (sid, bt, vt):
            out.append(f'ex:Refine_MS_{x} a backlog:RefinementEvent ; rdfs:label "Refinement that made {x} ready"@en ;\n    backlog:refines ex:{x} ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "{now}"^^xsd:dateTime ; backlog:refinedBy backlog:Builder ;\n'
                       + (f'    backlog:groomsForIteration ex:Iter_MS ;\n' if x != sid else '') +
                       f'    backlog:hasRefinementOutcome {lit("Refined by the lineage agent from the Owner's instruction of " + WHEN + ": criterion with its checks, measured as-is fit-gap, requirements in the task text, estimate, brief generated from the measured logs. Startable at once.")} .\n')
        members += [sid, bt, vt]; tasks += [bt, vt]
    out.append(f'ex:Iter_MS a backlog:Iteration ; rdfs:label "Urgent box: SEN0414 chapters 1 to 7 to the Chapter 8 Friday standard, today"@en ; backlog:hasIdentifier "Iter_MS" ; backlog:belongsToLineage ex:Lineage2 ;\n'
               f'    backlog:iterationStart "{now}"^^xsd:dateTime ; backlog:iterationEnd "2026-11-01T21:00:00"^^xsd:dateTime ;\n'
               f'    backlog:hasDurationSource {lit("Stated by the Owner, not proposed: 'Today we should finish both the Midterms and midterm scope work' (2026-11-01, 12:2x Istanbul); the box ends at midnight Istanbul (21:00Z) of that day. The lineage agent could not prove that it fits (about 27 executor-hours over three to four parallel slots plus control); what does not finish is said openly and moves only by an Owner rebaseline.")} ;\n'
               f'    backlog:hasSprintGoal {lit("Chapters 1 to 7 have new decks, manifests and pages at the Chapter 8 Friday standard, controlled on the controller's own re-runs, ready for the Owner's review.")} ;\n'
               f'    backlog:hasMember {", ".join("ex:" + m for m in members)} .\n')
    out.append(f'ex:PC_MS_Iter_MS a backlog:SprintPlanningCeremony ; rdfs:label "Planning of the urgent midterm-scope box"@en ; backlog:ceremonyFor ex:Iter_MS ; backlog:heldAt "{now}"^^xsd:dateTime ; backlog:hasWorkKind backlog:WorkKind_Planning ;\n'
               f'    backlog:includesPlanningEvent {", ".join("ex:Plan_MS_ST_MS_Ch" + c for c in ORDER)} ;\n    rdfs:comment "Held {now} UTC by the lineage agent on the Owner\'s instruction: seven stories and their tasks committed to this box, ranked chapter 7, 4, 1, 5, 2, 3, 6."@en .\n')
    for c in ORDER:
        out.append(f'ex:Plan_MS_ST_MS_Ch{c} a backlog:PlanningEvent ; rdfs:label "Planning of ST_MS_Ch{c} into the urgent box"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:plannedAt "{now}"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_MS ;\n'
                   f'    backlog:plansItem ex:ST_MS_Ch{c} ; backlog:producesTask ex:TK_MS_Ch{c}_Build, ex:TK_MS_Ch{c}_Verify ;\n    backlog:refinementProduces ex:Spec2S_D, ex:Scen2S_D_Passes, ex:Scen2S_D_NotClaimed .\n')
    for l in ("Lineage2", "Lineage4"):
        out.append(f'ex:{l} backlog:hasAuditNote {lit(OWNER)} .\n')
    return W.write_new(src, t0 + "\n" + "\n".join(out), "Urgency ceremony for the Owner's instruction of " + WHEN + " (SEN0414 chapters 1 to 7 to the Chapter 8 Friday standard, today): urgent stories ST_MS_Ch01..07 with tasks, criteria, re-ranked scores and the as-is fit-gap; one UrgentInterruption for each running lineage; the held repair TK_CI5_Page_Ch08_Repair stays held and is cancelled by its own change route.")

def declare():
    src = W.newest(); out = build(src); print(os.path.basename(out))
    reason = ("Owner's instruction of " + WHEN + ": the SEN0414 midterm-scope chapters 1 to 7 must reach the Chapter 8 Friday standard today; all other work, including the exam lineage's tasks and chapters 9 and later, waits (the exam lineage has no started item).")
    items = ["ST_MS_Ch" + c for c in ORDER] + ["TK_MS_Ch%s_%s" % (c, k) for c in ORDER for k in ("Build", "Verify")]
    for lin in ("Lineage2", "Lineage4"):
        cmd = [sys.executable, URG, "declare", out, "--lineage", NS + lin, "--reason", reason, "--until", "2026-11-01T21:00:00Z"] + sum([["--urgent", NS + i] for i in items], [])
        r = subprocess.run(cmd, capture_output=True, text=True); print(r.stdout.strip(), r.stderr.strip())
        if r.returncode: sys.exit(r.returncode)

def begun(args):
    src = W.newest(); t = open(src, encoding="utf-8").read(); L = []; first = None
    def blk(name):
        i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i); return i, (len(t) if j < 0 else j)
    gf = src + ".gate.tmp"; open(gf, "w", encoding="utf-8").write(t)
    try:
        for a in args:
            ch, hh = a.split("="); k = "TK_MS_%s_Build" % ("Ch" + ch[2:])
            r = subprocess.run([sys.executable, GATE, gf, "--lineage", "Lineage2", "--item", k], capture_output=True, text=True)
            assert "VERDICT     : READY" in r.stdout, k + ": " + r.stdout[-300:]
    finally:
        os.remove(gf)
    for a in args:
        ch, hh = a.split("="); n = ch[2:]; k = "TK_MS_Ch%s_Build" % n; sid = "ST_MS_Ch" + n; at = "2026-11-01T" + hh; s = "SEN0414-MS-" + ch
        i, j = blk(k); b = t[i:j]; assert "backlog:hasState backlog:Ready" in b and "startedAt" not in b, k
        t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % at, 1) + t[j:]
        i, j = blk(sid); b = t[i:j]; assert "backlog:hasState backlog:Ready" in b, sid
        t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % at, 1) + t[j:]
        bf = os.path.join(BRIEFS, "BRIEF_TK_MS_Ch%s_Build.md" % n); sha = hashlib.sha256(open(os.path.join(W.REPO, bf), "rb").read()).hexdigest()
        L.append(f'ex:EI_MS_{k} a backlog:ExecutorInstance ; rdfs:label "Executor session {s}"@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion {lit("brief %s (sen0414_lineage_brief_midterm_v1_0_0), session %s" % (bf, s))} ; backlog:instantiatedAt "{at}"^^xsd:dateTime ;\n    rdfs:comment "Started at the real instant the coordinator gave (date -u); retired when the session reports."@en .\n')
        L.append(f'ex:Brief_MS_{k} a backlog:ExecutorBrief ; rdfs:label "Brief of {k}"@en ; backlog:briefFor ex:{k} ; backlog:briefCriterion ex:AC2M_Ch{n} ; backlog:briefedExecutorInstance ex:EI_MS_{k} ;\n    rdfs:comment {lit("Passed unedited by the coordinator; file %s, SHA-256 %s." % (bf, sha))}@en .\n')
        L.append(f'ex:Begin_MS_{k} a backlog:TransitionEvent ; rdfs:label "{k} started by executor session {s}"@en ; backlog:transitionedItem ex:{k} ; backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "{at}"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote {lit("Work begun at %s UTC after the urgent interruption was recorded and the start gate said READY. Executor session %s, started with the brief %s. The record was written after the real start; the real instant is the one the coordinator gave from date -u. The lineage agent does not do this work." % (at, s, bf))} .\n')
        L.append(f'ex:Begin_MS_{sid} a backlog:TransitionEvent ; rdfs:label "{sid} started with its first task"@en ; backlog:transitionedItem ex:{sid} ; backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "{at}"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "The story starts with the real start of its first task {k} at {at} UTC." .\n')
        L.append(f'ex:{k} backlog:hasAuditNote "Work begun {at} UTC by executor session {s}." .\n')
    out = W.write_new(src, t + "\n" + "".join(L), "Work begun on " + ", ".join("TK_MS_Ch%s_Build" % a.split("=")[0][2:] for a in args) + " (executor sessions SEN0414-MS-chNN, real starts from the coordinator); stories InProgress.")
    print(os.path.basename(out))

if __name__ == "__main__":
    if sys.argv[1:2] == ["declare"]: declare()
    elif sys.argv[1:2] == ["begun"]: begun(sys.argv[2:])
    else: sys.exit(__doc__)
