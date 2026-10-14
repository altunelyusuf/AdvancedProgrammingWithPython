"""sen0414_lineage_outscope_stages v1_0_0 - the five stage events of the successor lineage ex:Lineage2 (Mission, Scope, Goal, Objective, Backlog),
called by sen0414_lineage_outscope. One stage per call, one commit per call. A stage output carries the digest the FRAMEWORK'S OWN tool computes
(backlog_pipeline_verify.state_digest, scoped to Lineage2) and closedAtCommit "PENDING" until the next stage's file replaces it with the real
hash of the commit that closed the stage (passed in by the caller after it has committed and pushed - never guessed).
"""
__version__ = "1.0.0"
import glob, importlib.util, json, os, re
import rdflib

FW = "/home/claude/Ontologies/backlog-roadmap-framework"
STAGES = ["Mission", "Scope", "Goal", "Objective", "Backlog"]
CLAUSE = "Every SEN0414 lecture deck teaches what the third edition of the course textbook teaches"
GAP = "ex:Gap_OutScope_Ch07_12"


def _pv():
    spec = importlib.util.spec_from_file_location("pv", FW + "/03-tooling/backlog_pipeline_verify_v1_8_0.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    tb = sorted(glob.glob(FW + "/01-ontologies/backlog_tbox_v*.ttl"))[-1]
    m.STAGE_TYPES = m._load_stage_types(tb, table="v1")
    return m


def digest(text, stage):
    pv = _pv()
    g = rdflib.Graph(); g.parse(data=text, format="turtle")
    lin = rdflib.URIRef("http://example.org/sen0414-slides-lineage#Lineage2")
    return pv.state_digest(g, "Stage_" + stage, lin)


def output(text, stage, prev_commit):
    """The stage output block, with the digest of the state the stage closed on (computed before the block is added)."""
    d = digest(text, stage)
    i = STAGES.index(stage)
    consumes = ("\n    backlog:consumesOutput ex:Out2_%s ;" % STAGES[i - 1]) if i else ""
    return ('\nex:Out2_%s a backlog:StageOutput ;\n    rdfs:label "Closure of the %s stage of the second lineage"@en ;\n    backlog:belongsToLineage ex:Lineage2 ;\n'
            '    backlog:outputOfStage backlog:Stage_%s ;%s\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (stage, stage, stage, consumes, d)


def fill_previous(text, stage, commit):
    """The previous stage's output gets the hash of the commit that closed it."""
    if not stage:
        return text
    pat = re.compile(r'(ex:Out2_%s a backlog:StageOutput ;.*?backlog:closedAtCommit )"PENDING"' % stage, re.S)
    assert pat.search(text), "no PENDING on Out2_" + stage
    return pat.sub(lambda m: m.group(1) + '"%s"' % commit, text, count=1)


def set_status(text, status):
    pat = re.compile(r'(ex:Lineage2 a backlog:Lineage ;.*?)(backlog:hasLineageStatus backlog:\w+ ;\s*)?(backlog:adoptsObligationSet)', re.S)
    m = pat.search(text); assert m
    return text[:m.start()] + m.group(1) + "backlog:hasLineageStatus backlog:%s ;\n    " % status + m.group(3) + text[m.end():]


# ---------------------------------------------------------------- stage content
def scope_block():
    return '''
ex:Area2_Admission a backlog:ScopeArea ;
    rdfs:label "The finished chapters 7 to 12 admitted into the register"@en ;
    backlog:belongsToLineage ex:Lineage2 ;
    backlog:areaLocation "07-lineage (this register); the finished files are in 03-materials and 08-tooling, chapters 7 to 12" ;
    backlog:areaMeasure "6 chapters, each with a deck, a research run and a page, recorded Done with their real finish dates and verified evidence" ;
    backlog:hasScopeLayer backlog:Layer_Work .

ex:Del2_Decks a backlog:ScopeDeliverable ;
    rdfs:label "The decks of chapters 7 to 12 recorded Done"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:derivesFromMissionClause "Every SEN0414 lecture deck teaches what the third edition of the course textbook teaches"^^xsd:string ;
    backlog:hasDeliverableText "The six renewed decks (chapters 7 to 12) are recorded Done, each with its real finish date from git and evidence that was run again and verified against the course repository." ;
    backlog:deliverableForArea ex:Area2_Admission ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Del2_Research a backlog:ScopeDeliverable ;
    rdfs:label "The research runs of chapters 7 to 12 recorded Done"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:derivesFromMissionClause "Every SEN0414 lecture deck teaches what the third edition of the course textbook teaches"^^xsd:string ;
    backlog:hasDeliverableText "The six RDODI research runs (chapters 7 to 12) are recorded Done, each with its real finish date from git and evidence that was run again and verified against the course repository." ;
    backlog:deliverableForArea ex:Area2_Admission ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Del2_Pages a backlog:ScopeDeliverable ;
    rdfs:label "The pages of chapters 7 to 12 recorded Done"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:derivesFromMissionClause "Every SEN0414 lecture deck teaches what the third edition of the course textbook teaches"^^xsd:string ;
    backlog:hasDeliverableText "The six interactive pages (chapters 7 to 12) are recorded Done, each with its real finish date from git and evidence that was run again and verified against the course repository." ;
    backlog:deliverableForArea ex:Area2_Admission ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .

ex:Excl2_NoRebuild a backlog:ScopeExclusion ;
    rdfs:label "No deck, research or page is built or rebuilt in this lineage"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:excludesConcern "Any change to the decks, research runs or pages of chapters 7 to 12: they enter this register exactly as they stand in the course repository." ;
    backlog:hasExclusionRationale "These chapters are finished. This lineage records them; it does not redo them, and a record that changed its subject would not be evidence of it." ;
    backlog:decidedBy backlog:Owner ; backlog:hasScopeLayer backlog:Layer_Work .
ex:Excl2_ReworkHeld a backlog:ScopeExclusion ;
    rdfs:label "The rework of chapters 1, 2 and 4 is not planned in this lineage"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:excludesConcern "The rework of the decks and pages of chapters 1, 2 and 4 with the teaching devices (ex:ST_ReworkOthers_Ch01_02_04): it is carried in as the open item it is, unplanned and unscored." ;
    backlog:hasExclusionRationale "The owner asked for it once chapter 3 has reached a maturity level he judges, which he has not yet done (the story's own recorded reason). It is neither finished nor planned, so this lineage carries it and does nothing with it until he decides." ;
    backlog:decidedBy backlog:Owner ; backlog:hasScopeLayer backlog:Layer_Work .

ex:Scope2 a backlog:ScopeStatement ;
    rdfs:label "Admit the finished chapters 7 to 12; hold what the owner has not released"@en ;
    backlog:belongsToLineage ex:Lineage2 ; backlog:scopeForMission ex:Mission ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:scopeCompletionState backlog:Proposed ;
    backlog:hasScopeStatementText "IN: the decks, research runs and pages of chapters 7 to 12 of the 3rd edition (18 stories), built and pushed before they were planned, recorded as finished with their real finish dates from git and evidence verified against the course repository (the out-scoping declaration ex:Gap_OutScope_Ch07_12 left them to this lineage). Also carried in unchanged, not worked: the three epics and the initiative that group the stories, and the rework of chapters 1, 2 and 4 (held for the owner's judgement of chapter 3). OUT: building or rebuilding any chapter; planning the held rework. Nothing else of the first lineage is open: chapters 1 to 6, 13 to 24 and multithreading are Done there with their own evidence." ;
    backlog:coversArea ex:Area2_Admission ;
    backlog:hasScopeExclusion ex:Excl2_NoRebuild, ex:Excl2_ReworkHeld ;
    backlog:producedByStage ex:Out2_Scope ;
    backlog:requiresDeliverable ex:Del2_Decks, ex:Del2_Research, ex:Del2_Pages .

ex:Blueprint2 a backlog:Blueprint ;
    rdfs:label "What the admission of finished chapters is about"@en ;
    backlog:belongsToLineage ex:Lineage2 ; backlog:blueprintFor ex:Scope2 ;
    backlog:hasDomainEntity ex:DE2_Deck, ex:DE2_ResearchRun, ex:DE2_InteractivePage .
ex:DE2_Deck a backlog:DomainEntity ; rdfs:label "Deck - a chapter's lecture slides"@en ; backlog:belongsToLineage ex:Lineage2 .
ex:DE2_ResearchRun a backlog:DomainEntity ; rdfs:label "Research run - an RDODI run on a chapter's subject"@en ; backlog:belongsToLineage ex:Lineage2 .
ex:DE2_InteractivePage a backlog:DomainEntity ; rdfs:label "Interactive page - a chapter's companion page"@en ; backlog:belongsToLineage ex:Lineage2 .
''' + "".join(
        'ex:Gap2_%s_%s a backlog:BlueprintGap ; rdfs:label "No coverage yet for the %s at the %s stage"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:gapForEntity ex:DE2_%s ; backlog:gapForStage backlog:Stage_%s ; backlog:hasGapReason "The entity is covered by the first lineage and by the admission of its finished chapters; this lineage plans no new work on it." .\n'
        % (e, st, h, human, e, st)
        for e, h in (("Deck", "Deck"), ("ResearchRun", "Research run"), ("InteractivePage", "Interactive page"))
        for st, human in (("Creation", "creation"), ("ActiveUse", "active use"), ("SuspensionException", "suspension or exception"), ("Termination", "termination")))


GOALS = [("G2_FinishedAdmitted", "The chapters built before they were planned are in the register as finished", "Facing_Mission", "", "GoalOrigin_Carried"),
         ("G2_EveryAdmittedChapterProven", "Every admitted chapter is recorded Done with evidence that was run again", "Facing_Scope", "", "GoalOrigin_Carried"),
         ("G2_DatesAreGitsDates", "No finish date of an admitted chapter is typed ahead of git", "Facing_Containment", "", "GoalOrigin_New"),
         ("G2_NothingRebuilt", "No admitted chapter is rebuilt to fit its record", "Facing_Exclusion", "\n    backlog:guardsExclusion ex:Excl2_NoRebuild, ex:Excl2_ReworkHeld ;", "GoalOrigin_New")]


def goal_block():
    L = []
    for i, label, f, g, origin in GOALS:
        gap = ("\n    backlog:goalAnswersGap %s ;" % GAP) if origin == "GoalOrigin_Carried" else ""
        L.append('\nex:%s a backlog:Goal ;\n    rdfs:label "%s"@en ;\n    backlog:belongsToLineage ex:Lineage2 ; backlog:derivesFromScope ex:Scope2 ; backlog:goalCoversArea ex:Area2_Admission ;%s\n'
                 '    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:%s ; backlog:hasGoalOrigin backlog:%s ;%s\n'
                 '    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ;\n'
                 '    backlog:hasGoalRationale "Derived from the scope of the second lineage and from the owner\'s rule of 2026-10-12: work finished before it was planned is out-scoped, the finished lineage closes, and a successor takes it in with its real dates." ;\n'
                 '    backlog:producedByStage ex:Out2_Goal .\n' % (i, label, g, f, origin, gap))
    L.append('''
ex:Spec2 a backlog:Specification ;
    rdfs:label "What an admitted chapter is"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:specifiesGoal ex:G2_FinishedAdmitted ;
    backlog:hasSpecificationText "A chapter is admitted as finished when each of its three stories (deck, research, page) is Done with a finish date that equals the last git commit of the files cited for it, an acceptance criterion, a test harness, a last-audit date, an execution modality and evidence that backlog_evidence_bridge verified against the course repository: a rerunnable chapter check that exits 0, and the built files cited by SHA-256. A story whose files cannot be verified is not Done." ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out2_Goal .
ex:Scen2_Verified a backlog:TestScenario ; rdfs:label "An admitted chapter's check passes and its files match their hashes"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec2 ;
    backlog:hasScenarioText "Given a finished chapter's deck, research and page in the course repository, when the chapter check is run and each cited file is hashed, then the check exits 0 and every hash equals the recorded one." .
ex:Scen2_ChangedFileRefused a backlog:TestScenario ; rdfs:label "A cited file that changed after it was recorded is refused"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec2 ;
    backlog:hasScenarioText "Given a cited file whose bytes differ from the recorded SHA-256, when the evidence bridge is run, then the evidence is not verified and the story cannot be Done." .
ex:Model2_UseCase a backlog:ModelArtifact ; rdfs:label "Who uses the admission of the finished chapters"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasModelKind backlog:Kind_UseCaseDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "The owner reads the register to learn which chapters are finished and on what evidence; the course session records each finished chapter with its git date and runs its check; the evidence bridge verifies the check and the file hashes; the framework's order check reads the chain and the admissions." ;
    backlog:describesItem ex:G2_FinishedAdmitted .
''')
    return "".join(L)


OBJS = [("Obj2_AdmittedDone", "G2_FinishedAdmitted", "Met2_AdmittedDone", "admitted stories of chapters 7 to 12 recorded Done", 0, 18, "Dir_Increase", True),
        ("Obj2_EvidenceVerified", "G2_EveryAdmittedChapterProven", "Met2_EvidenceVerified", "admitted stories whose evidence the evidence bridge verified", 0, 18, "Dir_Increase", True),
        ("Obj2_DatesFromGit", "G2_DatesAreGitsDates", "Met2_DatesFromGit", "admitted stories whose finish date equals the last git commit of their cited files", 0, 18, "Dir_Increase", True),
        ("Obj2_NothingRebuilt", "G2_NothingRebuilt", "Met2_Rebuilt", "files of chapters 7 to 12 changed by this lineage", 0, 0, "Dir_Hold", False)]


def objective_block(now_iso):
    L = []
    for i, g, m, what, b, t, d, movers in OBJS:
        gap = "\n    backlog:resolvesPartialScope %s ;" % GAP if i == "Obj2_AdmittedDone" else ""
        L.append('''
ex:%s a backlog:Objective ; rdfs:label "%s: from %d to %d"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:contributesToGoal ex:%s ; backlog:fillsScope ex:Scope2 ; backlog:hasSuccessMetric ex:%s ;%s
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of %s, read from this register after the evidence bridge has run against the course repository." ;
    backlog:hasBaselineValue "%d"^^xsd:decimal ; backlog:hasTargetValue "%d"^^xsd:decimal ; backlog:hasTargetDirection backlog:%s ;
    backlog:hasCheckpoint ex:CP2_%s ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out2_Objective .
ex:%s a backlog:Metric ; rdfs:label "%s"@en ; backlog:belongsToLineage ex:Lineage2 .
ex:CP2_%s a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the admission is recorded"@en ;
    backlog:checkpointCondition "Taken after the Backlog stage output of this lineage is closed and the evidence bridge has run, so the count is read from verified facts." ;
    backlog:expectedValue "%d"^^xsd:decimal .
ex:Obs20_%s a backlog:MetricObservation ; rdfs:label "Baseline, before any admission"@en ;
    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "Read from this register at the Objective stage of the second lineage: no story has been admitted as finished yet; the eighteen stories of chapters 7 to 12 still read Proposed." .
''' % (i, what.capitalize(), b, t, g, m, gap, what, b, t, d, i, m, what, i, t, i, m, i, b, now_iso))
    L.append('''
ex:Model2_Activity a backlog:ModelArtifact ; rdfs:label "How one finished chapter is admitted"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasModelKind backlog:Kind_ActivityDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "Per story, in order: read from git the files that carry the story and the commit that last changed them; hash each file; run the chapter check - BRANCH: a check that fails leaves the story out of Done and it is carried in unfinished; run the evidence bridge over the evidence; record the story Done with the git finish date, the criterion, the harness, the audit date and the modality; the Backlog output of this lineage admits it." ;
    backlog:describesItem ex:Obj2_AdmittedDone .
ex:Model2_Sequence a backlog:ModelArtifact ; rdfs:label "Who asks whom when an admitted chapter is verified"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasModelKind backlog:Kind_SequenceDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "The session asks git for the finish commit of each cited file and hashes the files; the evidence bridge runs the chapter check and compares each hash; the register records the bridge's verdict; the order check and the validator read the register." ;
    backlog:describesItem ex:Obj2_AdmittedDone .
''')
    return "".join(L)


def run(ev, t, args, G):
    now_iso = G["now"]()
    if ev == "mission":
        t = set_status(t, "LS_Opened")
        return t + output(t, "Mission", None), "second lineage opened under the same Mission (Mission stage closed; the Mission is continued unchanged)."
    prev = args[0]
    if ev == "scope":
        t = fill_previous(t, "Mission", prev)
        t = set_status(t, "LS_Scoped")
        t += scope_block()
        return t + output(t, "Scope", prev), "second lineage, Scope stage closed (admit the finished chapters 7-12; hold the rework of 1, 2 and 4)."
    if ev == "goal":
        t = fill_previous(t, "Scope", prev)
        t = set_status(t, "LS_Goaled")
        t += goal_block()
        return t + output(t, "Goal", prev), "second lineage, Goal stage closed."
    if ev == "objective":
        t = fill_previous(t, "Goal", prev)
        t = set_status(t, "LS_Objectived")
        t += objective_block(now_iso)
        return t + output(t, "Objective", prev), "second lineage, Objective stage closed."
    if ev == "fill":
        # args: STAGE HASH - the hash of the commit that closed the stage, written once that commit exists and is pushed
        return fill_previous(t, args[0], args[1]), "closedAtCommit of the %s stage output of the second lineage set to the commit that closed it." % args[0]
    if ev == "backlog":
        import sen0414_lineage_outscope_backlog_v1_0_0 as bk
        return bk.run(t, args, G, output, fill_previous, set_status)
    raise SystemExit("unknown event " + ev)
