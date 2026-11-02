#!/usr/bin/env python3
"""sen0414_lineage_exam_ownerurgency v1_0_0 - ONE new register file: records the Owner's urgency order of 2026-11-02 19:07 Istanbul (16:07Z), verbatim, as the Owner's urgency decision on the open interruption Urgent_4. Usage: python3 sen0414_lineage_exam_ownerurgency_v1_0_0.py"""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
src = W.newest(); t = open(src, encoding="utf-8").read()
NSU = "http://example.org/sen0414-slides-lineage#"
OWN = ("OWNER URGENCY DECISION, 2026-11-02 19:07 Istanbul (16:07Z), verbatim as relayed by the coordinator: \"I set an urgency case. Pause the lineage and finish the exams.\" "
       "Recorded as the Owner's decision on the already open interruption Urgent_4 (the urgency tool refuses a second interruption on one lineage, see the refusal log 08-tooling/control-exam-logs/urgency_declare_v4_0_0_refusal.log): "
       "the exam work (ST4_V4Simple and its tasks, the earlier ST4_Q5Free) stays named as urgent items of Urgent_4; all other SEN0414 lineage work stays paused (the four chapter items of the chapter stories ST_MS_Ch04 and ST_MS_Ch06 are held Suspended under the open interruption Urgent_3 of the chapter lineage; nothing else of this lineage is started). "
       "Ceremony redone from a fresh git pull before this record: OE_Operating_Discipline_v2_37_0.md (302 lines) and LINEAGE_OPERATING_DISCIPLINE_v153_0_0.md read in full, no change to this work. "
       "To let the exam executors have the CPU, register validations run at nice 10 and the register is committed in the smallest lawful steps; no obligation is waived and no gate is weakened, and the Done records of the exam tasks are written after the files are delivered and controlled, as the rules allow.")
add = "<%sUrgent_4> backlog:hasAuditNote %s .\nex:ST4_V4Simple backlog:hasAuditNote %s .\n" % (NSU, W.lit(OWN), W.lit("2026-11-02T16:07:00Z the Owner's urgency order (19:07 Istanbul) applies to this story: see the note on Urgent_4."))
print(os.path.basename(W.write_new(src, t + "\n" + add, "Exam: the Owner's urgency order of 2026-11-02 19:07 Istanbul recorded on Urgent_4.")))
