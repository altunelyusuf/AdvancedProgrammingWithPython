#!/usr/bin/env python3
"""backlog_make 1.0.0 (Lineage14, 2026-11-26): writes the backlog stage file (register 1.4.0) from tables. A lineage's own script, disclosed."""
import sys
EX="ex:"
EXE="ex:Executor_ClaudeCodeSession"
Q=lambda s:s.replace('"','\\"')
CH=["21","22","23","24","25"]
NEW=CH
NAME={"21":"Making Graphs and Manipulating Images","22":"Recognizing Text in Images","23":"Controlling the Keyboard and Mouse","24":"Text-to-Speech and Speech Recognition","25":"Threads"}
S=[]  # (id,label,cat,objs,dels,gherkin,artifact)
for n in NEW:
    S.append((f"Spec_{n}",f"Chapter {n} spec and chapter-code manifest for the generic deck builder 2.10.0","Cat_Maintenance",["SpecRuns"],[f"Spec_{n}"],
      f"Given the first-version chapter {n} ({NAME[n]}) deck, stories and examples, and no spec When a spec for the generic chapter deck builder 2.10.0 is written and run Then it builds a deck with the same story and example entries as the first-version deck, every difference is named and forced by a ruling, and the build exits 0",
      f"08-tooling/ch{n}-deck/ (new spec folder and the build log)"))
    S.append((f"Deck_{n}",f"Rebuild the chapter {n} deck on the rulings","Cat_Maintenance",
      ["DeckStandard","FitOverlaps","ReaderNotes","StoryProse","Balloons","DeckAnalogies","PhraseHits","DeckPrompts","MaterialConditions"],[f"Deck_{n}",f"Reader_{n}"],
      f"Given the chapter {n} spec When the deck is built and the deck checks run Then deck standard 1.3.0, fit, layout, notes, overlap, reader notes, story prose and the material check all pass, every code slide carries one story balloon and two result balloons, no analogy slide or think-of phrase remains and plain code parses without prompts",
      f"08-tooling/ch{n}-deck/ (new deck and the saved check logs)"))
for n in CH:
    S.append((f"Page_{n}",f"Build the chapter {n} page with a lambda-free A-box, the Slide code tab and the run-in-order menu item","Cat_Maintenance",
      ["RunInOrder","PageAbox","PagesPassing","CodeParses","PageLambda","PageAnalogies"],[f"Page_{n}",f"PageCode_{n}",f"NoAnalogies_{n}"],
      f"Given the chapter {n} deck manifest When the page is built from the generic template and its A-box is checked against the page shapes and the page test is run Then the run-in-order item runs the slide examples in slide order, the Slide code tab runs the deck code unchanged, no lambda and no analogy word remain, the A-box conforms and the page test passes",
      f"the chapter {n} page file, its A-box and its page-test log"))
    S.append((f"Release_{n}",f"Record the three reviews and release chapter {n}","Cat_Maintenance",["ReviewVerdicts","ReleaseRecords","MissionLecture"],[f"ReleaseRecord_{n}"],
      f"Given the chapter {n} deck and page with their check logs When the academician, the faculty reviewer and the undergraduate reader each record a verdict on each of 4 conditions Then the release record names every check log and all 12 verdicts before the chapter is released",
      f"reports/REPORT_Lineage14_ch{n}_release_and_review and REVIEW_RECORD_ch{n}_Lineage14"))
S.append(("OwnVersions","Give every changed file its own version and remove the older page drafts","Cat_LineageGovernance",["OwnVersions"],["OwnVersion"],
  "Given the files changed for chapters 21 to 25 When the version check is run on the repository root Then it exits 0 and no unreleased older page draft of these chapters remains","08-tooling/lineage14-closure/ version-check log"))
S.append(("Guards","Show by file listing that the guarded areas are untouched","Cat_LineageGovernance",["OutsideFiles","ContentChanged","ExamFiles","OtherChapterFiles","LabFiles","RdodiFiles"],[],
  "Given the lineage's commits since the objective stage When git lists the files changed Then no file of exam work, chapters 1 to 20, lab materials or an existing rdodi file appears, no file outside the allowed folders appears and no approved story or example entry differs from its earlier deck except where a ruling forces it","08-tooling/lineage14-closure/ guard listing log"))
for k,lab,q in [("PageTest","Record the page test of the current pipeline on the five pages","Given the five new pages When the page test is run on each Then each log is kept beside its page and the count of passing pages is recorded"),
                ("MatchingCode","Measure that chapter code, page and lab libraries carry matching code for chapters 21 to 25","Given the manifests, pages and lab libraries of chapters 21 to 25 When the code of each example is compared Then every difference is listed and each is either removed or recorded for the lab lineage"),
                ("Links","Check the story pictures and links of chapters 21 to 25","Given the story slides of chapters 21 to 25 When each picture licence and each link is checked Then every broken or unlicensed item is listed and corrected in the deck story or recorded"),
                ("StoryRepeat","Run the story-repeat check of chapters 21 to 25 against every other chapter and read every hit","Given sen0414_story_repeat_check_v1_0_0.py When it is run for chapters 1 to 25 Then each shared link or name in chapters 21 to 25 is read and recorded as a different story or sent to the Owner as a candidate")]:
    S.append((f"Measure_{k}",lab,"Cat_LineageGovernance",["Unmeasured"],["Measures"],q,"08-tooling/lineage14-closure/ measurement log"))

DOD=[("ContentUnchanged","Content, stories and examples stay as approved","Compare, per chapter, the story ids and the number of examples in the new spec with the earlier deck and the stories file; list every difference.","NotYetEnforceable","Every difference is one a ruling forces and is named in the story's record.","The comparison is written in the Spec stories and its result then replaces this status."),
("DeckChecks","Every new deck passes the automatic deck conditions","Run 08-tooling/lineage12-opening/deckchecks_runner.sh NN DECK MANIFEST LOGDIR for each chapter.","Violated","Every check exits 0 on every chapter.","On 2026-11-26 the reader-note check finds 79 findings on the five first-version decks; the standard check cannot run before the chapter-code manifests exist (logs in 08-tooling/lineage14-opening/)."),
("MaterialCheck","Every new deck and page pass the material check","Run 08-tooling/cme_material_check_v1_0_2.py DECK PAGE for each chapter.","Violated","No failing condition on any chapter.","6 of 8 conditions fail on each of the five chapters on 2026-11-26 (30 of 40; logs material_ch*.log); it is re-run on every new deck and page."),
("RunOrderShape","Every chapter page has the run-in-order menu item","Run the page-shapes check with sen0414_page_shapes_v1_0_0.ttl on the built page A-box of each chapter.","Violated","PageRunInOrderMenuShape passes on all five pages.","None of the five pages has the item and no chapter has a page A-box file."),
("PageTest","Every new page passes the full page test","Run 08-tooling/sen0414_page_test_run_v1_1_0.py N VERSION for each chapter.","NotYetEnforceable","The full test passes on every page.","No new page exists yet; the test takes about 15 to 20 minutes per page."),
("OwnVersion","Every changed file has its own new version","Run python3 08-tooling/cme_version_check_v1_0_0.py . on the repository root.","Holds","Exit 0.","Exit 0 on 2026-11-26 before this register file; it is re-run in each stage."),
("OutsideFiles","No file outside chapters 21 to 25 and the lineage's own folders changes","git diff --name-only from the objective-stage commit, filtered against the allowed folders.","Holds","No file outside the allowed folders.","Only 07-lineage and 08-tooling/lineage14-opening changed so far."),
("StoryRepeat","No story of a chapter repeats in another chapter without the Owner","Run 08-tooling/sen0414_story_repeat_check_v1_0_0.py 1 25 and read every hit for chapters 21 to 25.","NotYetEnforceable","RESULT CLEAN for chapters 21 to 25 against every other chapter, or every hit recorded as a different story or sent to the Owner.","Not measured for these chapters yet; the measurement story records it."),
("MatchingCode","Chapter code, page and lab libraries carry matching code","Compare the manifest examples, the page frames and the lab library functions of chapters 21 to 25.","NotYetEnforceable","Every example matches or its difference is recorded for the lab lineage.","Not measured yet; the measurement story records it."),
("ReviewRecord","Each reviewed condition has a verdict from all three roles","Count the verdicts recorded per chapter against 12 conditions (4 conditions times 3 roles).","NotYetEnforceable","Every chapter has all its verdicts.","No verdict is recorded yet.")]

o=[]
o.append('''@prefix backlog: <http://example.org/backlog#> .
@prefix ex:      <http://example.org/sen0414-ch2125corr-lineage#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<http://example.org/sen0414-ch2125corr-lineage> a owl:Ontology ;
    rdfs:label "Fresh narrow lineage: SEN0414 Chapters 21 to 25 corrections"@en ;
    owl:versionInfo "1.4.0" ; owl:versionIRI <http://example.org/sen0414-ch2125corr-lineage/1.4.0> ;
    owl:priorVersion <http://example.org/sen0414-ch2125corr-lineage/1.3.0> ; dcterms:identifier "sen0414_ch2125corr_lineage" ;
    rdfs:comment """1.4.0 (2026-11-26): Backlog stage of Lineage14: the register root, the backlog, %d stories with acceptance criteria and links to the objectives they move and the deliverables they satisfy, and the lineage's own Definition of Done. Tasks follow in the planning stage, where each is produced by a planning event. CORRECTION OF 1.3.0 (appended, never edited): the spec objective of 1.3.0 said that none of the five chapters has a spec folder and set the target at 5. Both were wrong: specs exist (chapter 16 spec_v4_0_0, chapter 17 spec_v4_0_0, chapter 18 spec_v3_0_0, chapter 19 spec, chapter 20 spec_v2_0_1) and the newest decks were built from them by the generic builder versions 2.9.0, 2.6.0, 2.4.0, 2.2.0 and 2.3.0. The baseline 0 stays true read as chapters whose newest deck is built by the current generic builder 2.10.0; the target is 3, the chapters 21 to 25 that are re-cut, because chapters 16 and 17 need no re-cut (mission: reduce rework). The wrong text stays visible in 1.3.0.""" @en .
''' % len(S))
o[0]=o[0].replace('""" @en .','"""@en .')

o.append('''
ex:Register_Ch2125corr a backlog:Backlog ; backlog:isRegisterRoot true ; rdfs:label "Chapters 21 to 25 corrections register"@en .
ex:Backlog14 a backlog:Backlog ;
    backlog:memberOfContainer ex:Register_Ch2125corr ;
    backlog:backlogForMission ex:Mission14 ;
    backlog:belongsToLineage ex:Lineage14 ;
    rdfs:label "Chapters 21 to 25 corrections backlog"@en .
ex:DoD14 a backlog:DefinitionOfDone ;
    backlog:belongsToLineage ex:Lineage14 ;
    rdfs:comment "Written for this lineage. A story is Done only when each acceptance criterion has a check run in the current turn with its output saved in the repository, a verify task re-runs it from the files and not from the builder's report, and a check that cannot be run or a result that is not shown leaves the story open." ;
    rdfs:label "Definition of Done of the chapters 21 to 25 corrections lineage"@en .
''')
for k,lab,cq,st,exp,com in DOD:
    o.append(f'''ex:DoD14 backlog:hasDoDCriterion ex:DoD14_{k} .
ex:DoD14_{k} a backlog:DoDCriterion ;
    backlog:hasCheckQuery "{Q(cq)}" ;
    backlog:hasCriterionStatus backlog:{st} ;
    backlog:hasExpectedResult "{Q(exp)}" ;
    rdfs:comment "{Q(com)}" ;
    rdfs:label "{Q(lab)}"@en .
''')
o.append('''ex:Executor_ClaudeCodeSession a backlog:Executor_SingleAgent ; rdfs:label "The Claude session that carries out the work"@en .
ex:Register_Ch2125corr backlog:hasIdentifier "Register_SEN0414_Ch2125corr" ; backlog:belongsToLineage ex:Lineage14 ; backlog:hasCommitment ex:Commit14 .
ex:Backlog14 backlog:hasIdentifier "Backlog_SEN0414_Ch2125corr" ; backlog:hasCommitment ex:Commit14 .
ex:Commit14 a backlog:Commitment ; rdfs:label "This register commits to chapters 21 to 25 that meet the rulings"@en ;
    backlog:commitsToGoal ex:G14_Mission ; backlog:commitsToObjective ex:Obj14_MissionLecture ; backlog:commitsToDefinitionOfDone ex:DoD14 .
ex:Mission14 backlog:missionFor ex:Register_Ch2125corr .
ex:Register_Ch2125corr backlog:appliesDefinitionOfDone ex:DoD14 .
ex:Backlog14 backlog:appliesDefinitionOfDone ex:DoD14 .
ex:Blueprint14 a backlog:Blueprint ; rdfs:label "What the chapters 21 to 25 corrections are about"@en ;
    backlog:belongsToLineage ex:Lineage14 ; backlog:blueprintFor ex:Backlog14 ;
    backlog:hasDomainEntity ex:DE14_Deck , ex:DE14_Page , ex:DE14_Spec , ex:DE14_Review .
ex:Blueprint14Root a backlog:Blueprint ; rdfs:label "What the chapters 21 to 25 corrections are about (register root)"@en ;
    backlog:belongsToLineage ex:Lineage14 ; backlog:blueprintFor ex:Register_Ch2125corr ;
    backlog:hasDomainEntity ex:DE14_Deck , ex:DE14_Page , ex:DE14_Spec , ex:DE14_Review .
ex:DE14_Deck a backlog:DomainEntity ; rdfs:label "Deck - a chapter's lecture slides with notes and balloons"@en ; backlog:belongsToLineage ex:Lineage14 .
ex:DE14_Page a backlog:DomainEntity ; rdfs:label "Page - a chapter's interactive page that runs the slide code"@en ; backlog:belongsToLineage ex:Lineage14 .
ex:DE14_Spec a backlog:DomainEntity ; rdfs:label "Spec - a chapter's description that the generic deck builder runs"@en ; backlog:belongsToLineage ex:Lineage14 .
ex:DE14_Review a backlog:DomainEntity ; rdfs:label "Review - a recorded verdict of one of the three roles on one condition"@en ; backlog:belongsToLineage ex:Lineage14 .
ex:Session14_Backlog a backlog:RegisterSession ; rdfs:label "The session that wrote the backlog stage"@en ;
    backlog:sessionFor ex:Backlog14 , ex:Register_Ch2125corr ; backlog:sessionConductedBy "claude-session" ;
    backlog:sessionStartedAt "2026-11-26T17:35:00"^^xsd:dateTime ; backlog:sessionEndedAt "2026-11-26T17:55:00"^^xsd:dateTime ;
    backlog:stateVerifiedAtStart true ;
    backlog:hasSessionScopeNote "Set out to write the Backlog stage only (stories, acceptance criteria, Definition of Done, links to objectives and deliverables, and the links to the 27 objectives). Left alone: tasks and planning events (planning stage), packages and sprints, and every file outside 07-lineage and 08-tooling/lineage14-opening. Verified first: the objective stage 1.3.0 check passed and the working tree was clean at b8c3839." .
''')
for sid,lab,cat,objs,dels,g,art in S:
    s=f"ex:ST14_{sid}"
    o.append(f'''
ex:Backlog14 backlog:hasBacklogMember {s} .
{s} backlog:hasIdentifier "ST14_{sid}" ; backlog:responsible {EXE} ; backlog:hasInvestmentCategory backlog:{cat} ; backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored at planning, when the packages and sprints are cut." .
''')
    for ob in objs: o.append(f"{s} backlog:pursuesObjective ex:Obj14_{ob} .\n")
    o.append(f'''{s} a backlog:Story ;
    backlog:appliesDefinitionOfDone ex:DoD14 ;
    backlog:memberOfContainer ex:Backlog14 ;
    backlog:belongsToLineage ex:Lineage14 ;
    backlog:hasAcceptanceCriterion ex:AC14_{sid} ;
    backlog:hasState backlog:Proposed ;
    backlog:standsAlone true ;
    rdfs:label "{Q(lab)}"@en .
''')
    for ob in objs: o.append(f"ex:Obj14_{ob} backlog:metricMovableBy {s} .\n")
    for d in dels: o.append(f"{s} backlog:satisfiesDeliverable ex:Del14_{d} .\n")
    o.append(f'''ex:AC14_{sid} a backlog:AcceptanceCriterion ;
    backlog:belongsToLineage ex:Lineage14 ;
    backlog:hasGherkinText "{Q(g)}" ;
    backlog:satisfiedByArtifact "{Q(art)}" ;
    rdfs:label "{Q(lab)}: acceptance"@en .
''')
open(sys.argv[1],"w").write("".join(o))
print(len(S),"stories")
