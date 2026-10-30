#!/usr/bin/env python3
"""sen0414_lineage_bloom_rule v1_0_0 - records the Owner's Bloom reading (about 10:30 Istanbul, 2026-10-30, relayed) as his word on the mission of the exam lineage and on the stories it binds, and the controller's check of the revised design against it on
bridge-verified evidence. A NEW file; ONE new register version.   draft OUT.ttl | record BRIDGE.ttl"""
import hashlib, os, sys, datetime
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#")
CTL = "08-tooling/sen0414_control_bloom_v1_0_0.py"; F = "04-assessment/exams/exam_design_v1_1_0.json"
EV, EF = "Ev4c_Ctl_bloom", "Ev4c_CtlFile_bloom_0"
WORD = ("OWNER ANSWER of 2026-10-30 about 10:30 Istanbul (relayed by the course coordinator, recorded as relayed; asked with plain examples: recall 'what does len() return', use it 'what does this 4-line code print', work out why 'this code crashes on the second loop, why'): "
        "'B and C, but at least 8 work-out-why' per 30-item paper. Reading recorded: the higher levels are Apply and above (use it, work out why) for the majority of the 30 items, AND at least 8 of the 30 items are at Analyze or above (Bloom level 4 or higher), counted on the whole paper. "
        "This replaces the lineage agent's earlier assumption 'Apply and up' as the whole rule. The items per chapter 4,5,5,5,4,4,3 stay the lineage agent's default until he answers.")
NOTE_DES = ("CONTROL against the Owner's Bloom rule (lineage agent's own count, evidence " + EV + "): the revised design v1_1_0 has 21 of 30 items at Apply and above (70 per cent, a majority) and 10 of 30 at Analyze or above (Bloom 4 and 5: 8 + 2), which is not below 8: the design meets his rule as it stands.")
NOTE_ENG = ("The executor of TK4_Engine_Core was launched on the r5 brief (real start 2026-10-30T08:53:24Z), written before the Owner's Bloom reading; it names the majority only. The rule 'at least 8 of 30 at Bloom 4 or higher on the whole paper' is part of this task from the Owner's word and is in the r6 brief; the controller will check both counts at its control.")
NOTE_ITEMS = ("Briefs of the item pools are issued in a new folder (r6) that states the Owner's Bloom rule with each brief's own share: the pool for chapters 1 to 4 (19 of the paper's 30 items) holds at least 12 of its 30 items at Bloom 4 or higher so that at least 6 can be picked; the pool for chapters 6 to 8 (11 of the 30) holds at least 40 per cent at Bloom 4 or higher so that at least 3 can be picked; together at least 9, not below 8.")
def draft(out):
    h = hashlib.sha256(open(os.path.join(W.REPO, F), "rb").read()).hexdigest()
    open(out, "w", encoding="utf-8").write("@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0414-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
        'ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:hasTestId "bloom" ; backlog:hasTestSpec "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s" .\n'
        'ex:%s a backlog:ArtifactEvidence ; rdfs:label "exam_design_v1_1_0.json as controlled"@en ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" .\n' % (EV, W.lit("Control by the lineage agent: the revised design against the Owner's Bloom rule (majority at Apply and above, at least 8 of 30 at Analyze and above)"), CTL, CTL, EF, F, h))
def utc(x):
    return datetime.datetime.strptime(x[:19], "%Y-%m-%dT%H:%M:%S").astimezone().astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
def record(bridge):
    g = rdflib.Graph(); g.parse(bridge, format="turtle"); vd = {}
    for ev in set(g.subjects(B.evidenceVerified, None)):
        vd[str(ev).split("#")[-1]] = (bool(g.value(ev, B.evidenceVerified).toPython()), utc(str(g.value(ev, B.verifiedAt))), str(g.value(ev, B.hasVerificationMethod)))
    assert vd[EV][0] and vd[EF][0], "not verified"
    src = W.newest(); t = open(src, encoding="utf-8").read(); h = hashlib.sha256(open(os.path.join(W.REPO, F), "rb").read()).hexdigest(); L = []
    L.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:evidenceVerified true ; backlog:hasTestId "bloom" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (EV, W.lit("Control by the lineage agent: the revised design against the Owner's Bloom rule"), CTL, W.lit(vd[EV][2]), CTL, vd[EV][1]))
    L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label "exam_design_v1_1_0.json as controlled"@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (EF, F, h, W.lit(vd[EF][2]), vd[EF][1]))
    L.append("ex:ST4_DesignRev backlog:hasEvidence ex:%s, ex:%s .\n" % (EV, EF))
    L.append("ex:Mission4 backlog:hasAuditNote %s .\n" % W.lit(WORD))
    for k, nn in (("ST4_DesignRev", NOTE_DES), ("ST4_Engine", NOTE_ENG), ("TK4_Engine_Core", NOTE_ENG), ("ST4_Items", NOTE_ITEMS), ("TK4_Items_A", NOTE_ITEMS), ("TK4_Items_B", NOTE_ITEMS)):
        L.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(nn)))
    print(os.path.basename(W.write_new(src, t + "\n" + "".join(L), "The Owner's Bloom reading recorded as his word (majority at Apply and above and at least 8 of 30 at Analyze and above); the revised design meets it on bridge-verified evidence; the r6 briefs state it.")))
if __name__ == "__main__":
    draft(sys.argv[2]) if sys.argv[1] == "draft" else record(sys.argv[2])
