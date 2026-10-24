#!/usr/bin/env python3
"""sen0414_lineage_start_correct v1_0_0 - records in ONE new register version the disclosure and correction of a work-begun record that preceded the real start of its executor session.
Case: version 2.169.0 recorded TK_Std_Deck_Ch09_Build (session SEN0414-I18-deck-ch09) and its story as begun at 2026-10-23T14:54:59 UTC, but the coordinator had not started the executor; the real start
was reported later, and the start time is the clock reading of this writer. The structured values (startedAt, transitionedAt, instantiatedAt) are set to that reading, the notes are rewritten to state it,
and an audit note on the task, the story and the transition names the earlier record, the reason and the version that held it (committed versions are not edited; the earlier record stays in them).
Usage: sen0414_lineage_start_correct_v1_0_0.py"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
OLD = "2026-10-23T14:54:59"; TASK = "TK_Std_Deck_Ch09_Build"; STORY = "ST_Std_Deck_Ch09"


def main():
    src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now(); assert now > OLD
    n = 0
    for pat in ('startedAt "%s"' % OLD, 'transitionedAt "%s"' % OLD, 'instantiatedAt "%s"' % OLD):
        n += t.count(pat); t = t.replace(pat, pat.replace(OLD, now))
    assert n == 5, n
    a = t.index("\nex:Begin2T_%s a backlog:TransitionEvent" % TASK); b = t.index("\nex:Brief2_%s a" % TASK)
    seg = t[a:b].replace(OLD + " UTC", now + " UTC"); t = t[:a] + seg + t[b:]
    a = t.index("\nex:Begin2T_%s a backlog:TransitionEvent" % STORY); b = t.index("\n\n", a)
    seg = t[a:b].replace(OLD + " UTC", now + " UTC"); t = t[:a] + seg + t[b:]
    base = os.path.basename(src)
    why = ("CORRECTION of the work-begun record (disclosed, not hidden): version 2.169.0 recorded this work as begun at %s UTC, before any executor session had really started; the coordinator had not yet started the executor. "
           "The real start was reported afterwards and is the clock reading of the correcting writer, %s UTC; the structured start values are set to it. The earlier, wrong record stays in the committed versions up to %s. "
           "Cause: the work-begun tool was run when the brief was issued, not when the coordinator confirmed the start; from now on it is run only after the coordinator reports a real start." % (OLD, now, base))
    add = ""
    for x in (TASK, STORY, "Begin2T_" + TASK):
        add += "ex:%s backlog:hasAuditNote %s .\n" % (x, W.lit(why))
    out = W.write_new(src, t + "\n" + add, "Correction of the work-begun record of %s and its story: the record of 2.169.0 (%s UTC) preceded the real start of the executor session; the start is now %s UTC, disclosed in an audit note." % (TASK, OLD, now))
    print(now, os.path.basename(out))


if __name__ == "__main__":
    main()
