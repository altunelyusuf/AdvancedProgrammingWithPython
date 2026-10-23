#!/usr/bin/env python3
"""sen0414_lineage_charset v1_0_0 - change route (rulings G104, G125, G136) for the owner's standing instruction of 2026-10-23 11:07 Istanbul, relayed by the coordinator:
"Repairs should change the priority of the PBIs or the tasks." Known case: the SEN0401 sibling found its page template placing the character-set declaration beyond the first 1,024 bytes (mojibake in prescan-only viewers);
measured here: the SEN0414 template 9.50.0 (the line the new template ports over), the sibling's 9.52.1 and the shipped pages 9.28.0 carry the same fault.
Events, one new register file each (the caller validates and commits and pushes each alone):  change | retract | backlog PREV | fill PREV
  change   - ChangeRequest ex:CR2_Charset (Pending) and ImpactAssessment ex:IA2_Charset with the measured facts.
  retract  - StageRevision from the Backlog stage: retracts ex:Out2_BacklogR1; status LS_Objectived.
  backlog  - Backlog output ex:Out2_BacklogR2; all admitted items re-admitted; repair story ST_Std_Charset with criterion and a controller task; charset requirement appended to the template and page-test tasks;
             page builds depend on the repair's verification; WSJF re-scoring of the open stories as dated records; ScopeChange; CR Accepted.
  fill     - closedAtCommit of ex:Out2_BacklogR2.
Usage: sen0414_lineage_charset_v1_0_0.py EVENT [PREV_COMMIT]"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
S = W.S; lit = W.lit; now = W.now
CR = "ex:CR2_Charset"; IA = "ex:IA2_Charset"; REV = "ex:Revision_Lineage2_Backlog2"
OLD = "ex:Out2_BacklogR1"; NEW = "ex:Out2_BacklogR2"
WHEN = "Friday 2026-10-23 11:07 Istanbul (08:07 UTC)"
OWNER = ("Owner's standing instruction of %s, relayed by the course coordinator and recorded as relayed (content, not a verbatim quotation): \"Repairs should change the priority of the PBIs or the tasks.\" "
         "When a repair or defect story enters the backlog, the open items are re-scored with the register's own ranking discipline (PriorityScore, inputs stated from observable facts), the new ranking is recorded as dated records, starts are ordered by it, "
         "and a repair outranks the work it blocks or that would ship the same defect. Known case to apply now: the SEN0401 sibling found that its page template placed the character-set declaration at byte ~13,600 (beyond the first 1,024 bytes), "
         "so pages show mojibake in prescan-only viewers; the SEN0414 template line and its pages 9.28.0 are to be checked for the same fault, a page task that would ship it is ranked behind the template task that places the declaration first in head, and the page test must check it." % WHEN)
FACTS = ("MEASURED FACTS (the lineage agent, read-only, 2026-10-23; byte offset of the first <meta charset=...> in the file): template 9.48.0 byte 13469, 9.49.0 byte 14037, 9.50.0 byte 15897 (the template line the new template 9.52.1 is ported over); "
         "the sibling's template 9.52.1 byte 13587 (head opens at byte 383), so porting the sibling's file would ship the fault; the shipped pages sen0414_ch06_page_v9_28_0.html, ch07 and ch08: byte 9293 each (head opens at byte 31). "
         "The page test 9.34.0 of this line has no check of the declaration (no occurrence of charset in the file). The HTML standard's encoding sniffing reads only the first 1,024 bytes for a declaration, so a declaration after that is not seen by a prescan-only viewer. "
         "The same holds for the shipped pages of the other chapters built from the same template; they are outside this iteration and are reported, not changed.")
RULE = ("CHARSET RULE (added to the page standard by this change): the page declares <meta charset=\"utf-8\"> as the FIRST child of <head>, so that its first byte lies below byte 1,024 of the file (the sibling's evidence needs the declaration within the first 1,024 bytes; the lineage's check requires it within the first 512). "
        "The template 9.52.1 places it first in head, before any comment, style or script; the builders keep it there; the page test 9.36.0 has a named feature P12 that reads the raw bytes of the built page (not the DOM) and fails when the declaration is absent or begins at or beyond byte 512; "
        "FORCE_STANDARD=1 and the declared standard both apply it, and it is never reported as SKIP for a page built from the new template.")
NOTE_TEMPLATE = " REPAIR REQUIREMENT (ex:CR2_Charset, owner's standing instruction of 2026-10-23 11:07 Istanbul): the template 9.50.0 and the sibling's 9.52.1 place the character-set declaration at byte 15897 and 13587; the NEW template 9.52.1 must place <meta charset=\"utf-8\"> as the first child of <head>, before any comment, style or script, below byte 512, and the builders must keep it there. " + FACTS
NOTE_PAGETEST = " REPAIR REQUIREMENT (ex:CR2_Charset, owner's standing instruction of 2026-10-23 11:07 Istanbul): add the named feature P12 to the NEW page test 9.36.0: it reads the raw bytes of the built page (not the DOM) and fails when no <meta charset> is present or its first byte lies at or beyond byte 512; it is applied to every page built from the new template, with the declared standard or FORCE_STANDARD=1, and is reported SKIP only for a page that does not declare the standard; prove it fails on the shipped pages (v9_28_0, byte 9293) and on a copy of the template 9.50.0 and passes on a page with the declaration first in head. " + FACTS
GH = ("Owner-directed repair (ex:CR2_Charset). Given the page template 9.50.0 (declaration at byte 15897), the sibling's 9.52.1 (byte 13587) and the shipped pages v9_28_0 (byte 9293), when the NEW template 9.52.1 and the NEW page test 9.36.0 are made, then ALL of: "
      "(1) the first <meta charset> in the new template 9.52.1 begins below byte 512 and is the first child of <head>; (2) a page of chapter 1 and one of chapter 10 built on it by the new builders also begin the declaration below byte 512; "
      "(3) the page test 9.36.0 has the named feature P12, which fails on the shipped pages of chapters 6, 7 and 8 (byte 9293) and passes on the built ones, with the raw bytes read; (4) no committed file is edited; results as printed, measured by the controller (the lineage agent) from the files, not from the executors' reports. " + RULE)
ST = "ST_Std_Charset"; TKV = "TK_Std_Charset_Verify"; AC = "AC2C_Charset"
# WSJF inputs (business value, time criticality, risk reduction) on the register's 1..20 scale, job size in hours of the story's tasks (their estimates in the register)
SCORES = {
    "ST_Std_Charset":   (8, 20, 20, 1.0, "the repair: a defect that every page built from the template ships (3 pages in this iteration, measured byte 15897 against a limit of 1024); it blocks 3 page stories (dependsOn) and is cheapest now, while the template and page-test tasks are being written"),
    "ST_Std_DeckTools": (13, 20, 8, 1.5, "the deck check blocks 3 deck verifications"),
    "ST_Std_PageTools": (13, 20, 13, 9.0, "template, page test and control block 3 page stories"),
    "ST_Std_Deck_Ch06": (20, 20, 3, 5.5, "chapter 6 first: the class of 2026-10-23"),
    "ST_Std_Page_Ch06": (20, 20, 3, 4.0, "chapter 6 first, after its deck"),
    "ST_Std_Deck_Ch07": (20, 13, 3, 5.5, "chapter 7 after chapter 6"),
    "ST_Std_Page_Ch07": (20, 13, 3, 4.0, "chapter 7 after its deck"),
    "ST_Std_Deck_Ch08": (20, 8, 3, 5.5, "chapter 8 after chapter 7"),
    "ST_Std_Page_Ch08": (20, 8, 3, 4.0, "chapter 8 after its deck"),
}


def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Repair: the character-set declaration of the page template and of the pages lies beyond the first 1,024 bytes; repairs re-rank the open work"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope2 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit(OWNER + " The scope does not move outward: the repair concerns files the scope already names (the new template 9.52.1 and the new page test 9.36.0, ex:Del2_StdTools); what is added is a requirement, a repair story with a controller task, a re-scoring of the open stories and a dependency of the page builds on the repair. Pending until the ScopeChange in the Backlog version."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the character-set repair changes in the iteration, with the facts measured before it is planned"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage2 ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(FACTS + " " + RULE + " WHAT MOVES: the Backlog stage of the second lineage is revised once (the digest moves because a story and a task are added); no task has begun, so nothing is re-dated; "
                    "the page builds of chapters 6, 7 and 8 gain a dependency on the repair's verification, which the controller records only when the template and the page test carry the rule; the open stories are re-scored with WSJF (inputs stated from observable facts) and the order of starts follows the score. "
                    "The six tasks that can start now (the three tooling tasks and the three deck builds) are independent of the repair and start at once; the repair is carried inside the template and page-test tasks (the requirement is added to their briefs) and controlled by TK_Std_Charset_Verify. "
                    "Not in the plan: the pages of other chapters built from the same template (reported, not changed); any edit of a committed file."))
    return t + cr + ia, "ChangeRequest ex:CR2_Charset (Pending) and ImpactAssessment ex:IA2_Charset for the owner's standing instruction of 2026-10-23 11:07 Istanbul (repairs re-rank the open work; the character-set declaration beyond byte 1024 in template 9.50.0, the sibling's 9.52.1 and the pages 9.28.0): measured facts and plan; no stage changed."


def ev_retract(t):
    t = S.set_status(t, "LS_Objectived")
    reason = (OWNER + " A story and a task are added to the lineage's closed Backlog stage, which moves its digest (G117, G125 route 2): this is a StageRevision from the Backlog stage, never from the Mission; the change request ex:CR2_Charset and the impact assessment ex:IA2_Charset were recorded first. "
              "This version retracts the Backlog output ex:Out2_BacklogR1 and rebuilds nothing; the next version closes the Backlog stage again as ex:Out2_BacklogR2 and re-admits every item, the stories and tasks of the iteration included, without re-dating them; a third version fills the commit. "
              "No task has begun, so nothing is lost by the retraction. The retracted output and its digest stay as history (L-112).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the second lineage from the Backlog stage: the character-set repair and the re-ranking of the open work"@en ;\n'
         '    backlog:revisesLineage ex:Lineage2 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n'
         '    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return t + b, "StageRevision of the second lineage from the Backlog stage (G125 route 2) for the character-set repair: the Backlog output Out2_BacklogR1 is retracted; nothing is rebuilt in this version."


def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision ;.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = S.set_status(t, "LS_Backlogged"); n = now()
    cnt = len(re.findall(r"admittedByOutput ex:Out2_BacklogR1\b", t)); assert cnt >= 20, cnt
    t = re.sub(r"admittedByOutput ex:Out2_BacklogR1\b", "admittedByOutput " + NEW, t)
    L = []
    # re-score the open stories: the old "not scored" pair is replaced by a dated PriorityScore
    for sid, (bv, tc, rr, size, why) in SCORES.items():
        if sid == ST:
            continue
        old = 'ex:%s a backlog:Story' % sid
        i = t.index("\n" + old) + 1; j = t.find("\nex:", i + 1); b = t[i:j]
        pair = re.search(r'backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Not scored: the owner directed[^"]*" ;', b); assert pair, sid
        t = t[:i] + b.replace(pair.group(0), "backlog:hasPriorityScore ex:Score2R_%s ;" % sid, 1) + t[j:]
    for sid, (bv, tc, rr, size, why) in SCORES.items():
        val = (bv + tc + rr) / size
        L.append('ex:Score2R_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n'
                 '    backlog:hasScoreRationale %s .\n' % (sid, val, n, lit(
                     "WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. Re-scored on %s under the owner's standing instruction that repairs re-rank the open work. "
                     "Inputs from observable facts: job size is the sum of the story's task estimates in this register; time criticality 20 = the class of 2026-10-23 or work that blocks it, 13 = blocks later work, 8 = later in the chapter order; %s. "
                     "The previous state was 'not scored' (a direct owner order); this record replaces that flag and ranks the starts." % (bv, tc, rr, size, val, WHEN, why))))
    # the repair
    tools = ["TS2_PageTemplate", "TS2_PageTest36", "TS2_PageBuilder"]
    L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label "The new template and the new page test place and check the character-set declaration below byte 512"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:hasGherkinText %s ;\n'
             '    backlog:measuredWithTool %s ;\n    backlog:measuredWithVersion %s ;\n    backlog:satisfiedByArtifact "the template 9.52.1 and the page test 9.36.0 cited by SHA-256, the byte offsets printed by the controller, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC2C_Passes, ex:TC2C_NotClaimed .\n' % (
        AC, lit(GH), ", ".join("ex:" + x for x in tools), lit(W.VER + "; byte offset read by the controller with python3 (raw bytes of the file)")))
    L.append('''ex:TC2C_Passes a backlog:TestCase ; rdfs:label "Read the raw bytes of the built pages and of the template and require the declaration below byte 512"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion ex:%(ac)s ; backlog:coversScenario ex:Scen2S_P_Passes ; backlog:runsOnData ex:Data2C_Passing ;
    backlog:hasCaseText "The controller reads the new template and the built pages as bytes and prints the offset of the first meta charset: below 512 and first in head; page test feature P12 passes." .
ex:TC2C_NotClaimed a backlog:TestCase ; rdfs:label "Run the page test feature on the shipped pages and the old template and require that it fails"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion ex:%(ac)s ; backlog:coversScenario ex:Scen2S_P_NotClaimed ; backlog:runsOnData ex:Data2C_Failing ;
    backlog:hasCaseText "Feature P12 of page test 9.36.0 on the shipped pages v9_28_0 (byte 9293) and on the template 9.50.0 (byte 15897) reports FAIL." .
ex:Data2C_Passing a backlog:TestData ; rdfs:label "The new template and pages built from it, declaration first in head"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasFixtureState "Template 9.52.1 and the scratch pages of chapters 1 and 10 built on it, whose first meta charset begins below byte 512." .
ex:Data2C_Failing a backlog:TestData ; rdfs:label "The shipped pages and the old template, declaration beyond byte 1024"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasFixtureState "The pages v9_28_0 of chapters 6, 7 and 8 (byte 9293) and the template 9.50.0 (byte 15897)." .
''' % dict(ac=AC))
    story = ('\nex:%(s)s a backlog:Story ; rdfs:label "Repair: the character-set declaration of the page template and pages is first in head, below byte 512, and the page test checks it"@en ; backlog:hasIdentifier "%(s)s" ;\n'
             '    backlog:hasTitle "Repair: the character-set declaration is first in head and checked"  ;\n    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_18 ; backlog:admittedByOutput %(n)s ;\n    backlog:hasInvestmentCategory backlog:Cat_Maintenance ;\n'
             '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability "pages whose text shows correctly in every viewer, also those that read only the first 1,024 bytes" ; backlog:soThat "the Turkish and technical characters of the chapter pages are never shown as mojibake" ;\n'
             '    backlog:satisfiesDeliverable ex:Del2_StdTools ; backlog:pursuesObjective ex:Obj2_StdPages ; backlog:hasAcceptanceCriterion ex:%(ac)s ;\n'
             '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n    backlog:decomposesInto ex:%(tk)s ;\n    backlog:hasState backlog:Ready ;\n'
             '    backlog:hasPriorityScore ex:Score2R_%(s)s ; backlog:standsAlone true ;\n    backlog:hasAuditNote %(note)s .\n') % dict(s=ST, n=NEW, ac=AC, tk=TKV, note=lit(OWNER + " " + FACTS + " " + RULE))
    L.append(story)
    L.append('\nex:%(tk)s a backlog:ExecutionTask ; rdfs:label "Control the character-set repair: byte offsets of the new template and the built pages and the page test feature P12"@en ; backlog:hasIdentifier "%(tk)s" ; backlog:hasTitle "Control the character-set repair" ;\n'
             '    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_18 ; backlog:admittedByOutput %(n)s ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n    backlog:hasInvestmentCategory backlog:Cat_Compliance ; backlog:hasTaskType backlog:TaskType_Verify ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Proposed ;\n'
             '    backlog:dependsOn ex:TK_Std_Template, ex:TK_Std_PageTest ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s score; scoring both would double-count." ;\n'
             '    backlog:hasAuditNote %(note)s .\n' % dict(tk=TKV, n=NEW, note=lit("Controller task (the lineage agent): after the template 9.52.1 and the page test 9.36.0 are Done, read the raw bytes of the template and of the pages of chapters 1 and 10 built on it and print the offset of the first meta charset (below 512, first child of head); run page test feature P12 on the shipped pages v9_28_0 (must FAIL) and on the built pages (must PASS). Planned session SEN0414-lineage (control); estimated start after the template and the page test, about 1 hour (estimate, G120). " + RULE)))
    for tk in ("TK_Std_Page_Ch06_Build", "TK_Std_Page_Ch07_Build", "TK_Std_Page_Ch08_Build"):
        L.append("ex:%s backlog:dependsOn ex:%s .\n" % (tk, TKV))
    L.append('ex:TK_Std_Template backlog:hasAuditNote %s .\nex:TK_Std_PageTest backlog:hasAuditNote %s .\n' % (lit(NOTE_TEMPLATE.strip()), lit(NOTE_PAGETEST.strip())))
    for x in (ST, TKV):
        L.append('ex:Refine2C_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_18 ;\n    backlog:hasRefinementOutcome %s .\n'
                 % (x, x, x, n, lit("Refined by the lineage agent from the owner's standing instruction of %s (ex:CR2_Charset) and the facts of ex:IA2_Charset: criterion with tools and versions, dependency on the template and the page test, controller task." % WHEN)))
    L.append('ex:Plan2C_%s a backlog:PlanningEvent ; rdfs:label "Planning of the character-set repair into iteration 18"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_18 ;\n    backlog:plansItem ex:%s ; backlog:producesTask ex:%s ;\n    backlog:refinementProduces ex:Spec2S_P, ex:Scen2S_P_Passes, ex:Scen2S_P_NotClaimed .\n' % (ST, n, ST, TKV))
    L.append("ex:Obj2_StdPages backlog:metricMovableBy ex:%s .\n" % ST)
    L.append("ex:Iter_18 backlog:hasMember ex:%s, ex:%s .\n" % (ST, TKV))
    L.append('ex:SC2_Charset a backlog:ScopeChange ;\n    rdfs:label "A repair story and its controller task admitted into the scope: the character-set declaration of the template and pages"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope2 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:%s ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        CR, ST, lit(OWNER + " The boundary does not move outward in deliverables (ex:Del2_StdTools names the template and the page test); the repair story is admitted as the owner's standing rule requires.")))
    t, k = re.subn(r'(ex:CR2_Charset a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert k == 1
    L.append('ex:CR2_Charset rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC2_Charset; it was Pending before. The owner\'s instruction is the direction."@en .\n' % n[:10])
    t += "\n" + "".join(L)
    out = ('\nex:Out2_BacklogR2 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the second lineage, rebuilt by the stage revision for the character-set repair"@en ;\n    backlog:belongsToLineage ex:Lineage2 ;\n'
           '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out2_ObjectiveR1 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % S.digest(t, "Backlog")
    return t + out, "second lineage, Backlog stage rebuilt for the character-set repair: repair story ST_Std_Charset with criterion and controller task, the requirement added to the template and page-test tasks, the page builds depend on the repair's verification, open stories re-scored with WSJF as dated records, ScopeChange, change request Accepted; the %d items are re-admitted by the new output, not re-dated." % cnt


def ev_fill(t, prev):
    t = W.fill_re(t, NEW, prev)
    return t, "closedAtCommit of the rebuilt Backlog output Out2_BacklogR2 set to the commit that closed it (%s); the revision is complete and no work is begun." % prev


def main():
    ev = sys.argv[1]; src = W.newest(); t = open(src, encoding="utf-8").read(); arg = sys.argv[2] if len(sys.argv) > 2 else None
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, arg), "fill": lambda: ev_fill(t, arg)}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(W.write_new(src, nt, comment)))


if __name__ == "__main__":
    main()
