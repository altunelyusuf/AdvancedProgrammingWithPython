#!/usr/bin/env python3
"""sen0414_lineage_exam_queue v1_0_0 - records, through the lineage route, the Owner's direction of 2026-10-28 14:21 Istanbul (relayed by the coordinator): the SEN0414 midterm exam is a DIFFERENT mission and waits as a queued lineage at LS_Opened (G104); the running chapter lineage is not touched. The mission statement is set from the VERIFIED gaps only; the lineage opens under the adaptive profile (printed by backlog_open_lineage_v1_1_0.py). A NEW file."""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
FW = "/home/claude/altunelyusuf/backlog-roadmap-framework/03-tooling/backlog_open_lineage_v1_1_0.py"
blk = subprocess.run([sys.executable, FW, "--profile", "Profile_Adaptive", "--lineage", "Lineage3", "--prefix", "ex"], capture_output=True, text=True).stdout
src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now()[:19]
GAPS = ("VERIFIED GAPS of chapters 1 to 8 for a midterm exam (read by the lineage agent on %s UTC from the register and the files, nothing built): "
 "(1) chapters 1 to 5: deck, page and research set each Done and controlled (Iteration 19), first page ABox present; open owner content item: stand-in pictures in chapter 2. "
 "(2) chapter 6: deck, page and research Done (Iteration 18); the Cross.B pilot (TK_Gap_CrossB_*) is Ready, never started, and reports CANNOT_RUN everywhere. "
 "(3) chapters 7 and 8: deck and page Done (Iteration 18) but NO research task in the register and NO first page ABox (the research documents v1_1_0 and v1_1_1 exist). "
 "(4) NOT MEASURED: the pages of chapters 1 to 8 against the leak probe v1_3_0 and the current page test; they were built under earlier templates. "
 "(5) exam inputs: 967 multiple-choice items in the chapter question banks of chapters 1 to 8 (answers evenly spread over the four letters), but only 403 (42 per cent) at Apply or Analyze and none at Evaluate or Create, so the Owner's majority at higher Bloom levels is NOT met; the chapter 8 bank is the smallest (69) and oldest; no fill-in or open items; no exam, QTI or CATS tooling and no Exam Studio conventions in this repository (the conventions: option banks randomised, correct letters evenly distributed, print-safe, no fabricated terms, items that need course knowledge)." % now)
STATEMENT = ("Give SEN0414 a midterm exam on chapters 1 to 8, printed with its answer key and exportable to CATS and QTI, whose items need the course's own knowledge, are grounded in the chapters' research and question banks, put the majority at the higher levels of Bloom's taxonomy, spread the correct letters evenly, randomise fill-in option banks and invent no terms.")
add = f"""
ex:Mission2 a backlog:Mission ;
    rdfs:label "Examine chapters 1 to 8 of SEN0414 with a midterm exam"@en ;
    backlog:missionFor ex:Backlog ;
    backlog:hasMissionStatement {W.lit(STATEMENT)} ;
    backlog:hasMissionOrigin {W.lit("The Owner's direction of 2026-10-28 14:21 Istanbul, relayed by the course coordinator: after the current chapters are completed the SEN0414 midterm exam is to be built, the midterm is next week; coverage chapters 1 to 8; delivery without a stated preference (default: printed paper with answer key, with CATS and QTI export). Recorded as relayed, not as a verbatim quotation. " + GAPS)} ;
    backlog:hasMissionOutcome {W.lit("An instructor holds a printable midterm paper with its answer key for chapters 1 to 8 and the same items as CATS and QTI files, each item traceable to a chapter's research or question bank.")} ;
    backlog:outcomeRationale {W.lit("A different purpose from the running chapter lineage (G104): it waits as a queued lineage at Opened and does not start or interrupt the chapter work. The statement is set from the verified gaps only (G, 2026-10-23): the existing banks are multiple choice only and 42 per cent at the higher levels, so the majority at higher levels is work to do, and the export and print conventions are not in this repository.")} ;
    backlog:decidedBy backlog:Owner ;
    backlog:missionSource "The Owner's direction of 2026-10-28 and the chapter question banks of 08-tooling/ch01-page to ch08-page." .

ex:Lineage3 a backlog:Lineage ;
    rdfs:label "Third lineage run for SEN0414: the midterm exam (queued)"@en ;
    backlog:lineageForMission ex:Mission2 ; backlog:lineageOrdinal 3 ; backlog:lineageArchived false ;
    backlog:hasLineageStatus backlog:LS_Opened .
"""
t += "\n" + add + "\n" + blk.replace("ex:Lineage3 backlog:openedWithProfile", "ex:Lineage3 backlog:openedWithProfile")
t += "\nex:Lineage3 backlog:hasAuditNote %s .\n" % W.lit("QUEUED on the Owner's direction of 2026-10-28 14:21 Istanbul (G104): opened at LS_Opened with its own mission; nothing of it starts and the running lineage ex:Lineage2 is not touched. PROFILE CHOSEN: the adaptive profile (Profile_Adaptive, profile revision 7), because (a) the Owner has ruled against none of the three profiles; (b) the standard profile owes every register-level check from the first commit and would refuse a lineage that sits at Opened with a mission and no goal, objective or scope yet (G166), and the agentic profile adds the accountability rule set on top of that standard asking; (c) the adaptive profile asks each obligation at the status that creates it, which is what a queued lineage needs; (d) it is NOT made the default: the Owner's direction of 2026-10-27 asks a live proof first, and this use is one more live use, not a change of default. The first lineage opened under it elsewhere is the live proof; if it fails here the lineage can be reopened under another profile before it starts (G89: only work not started is bound).")
print(os.path.basename(W.write_new(src, t, "queued lineage 3 (midterm exam of chapters 1 to 8) at LS_Opened under the adaptive profile, mission set from the verified gaps")))
