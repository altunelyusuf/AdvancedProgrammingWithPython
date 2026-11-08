#!/usr/bin/env python3
"""Append the closure-by-narrowing record to the SEN0414 slides lineage (Lineage2)
and bump its version, per LINEAGE_OPERATING_DISCIPLINE_v163_0_5.md step 6 (G215):
'write the closure report, read each promised guard again, have the Owner confirm,
set the mission outcome, then run the archive in the next release.'
This step writes the closure comment and the outcome triples now; archival
(backlog_lineage_archive) is deferred to the next release as the discipline requires,
and Owner confirmation is requested in the same turn this script's output is reported.
Append-only: no existing line is edited or removed.
"""
import re
import sys
from pathlib import Path

SRC = Path("07-lineage/sen0414_slides_lineage_v2_401_0.ttl")
DST = Path("07-lineage/sen0414_slides_lineage_v2_402_0.ttl")
CLOSURE_DATE = "2026-11-08"

CLOSURE_COMMENT = (
    '    rdfs:comment "2.402.0 (2026-11-08): Closure-by-narrowing (G215, as-is fit-gap and '
    'impact analysis in CLOSURE_REPORT_sen0414_slides_lineage_Lineage2_v1_0_0.md): Lineage2\'s '
    'mission (every lecture deck teaches what the book teaches, in its order) is not accomplished '
    '(458 Done, 74 Ready, 18 InProgress, 12 Proposed, 11 Cancelled, 9 Suspended at measurement). '
    'The existing status vocabulary (LS_Achieved, LS_InProgress, LS_Abandoned) has no term for '
    'closed-by-narrowing-with-partial-accomplishment; LS_Abandoned is recorded below as the nearest '
    'existing term, flagged as an open question for the owner rather than decided silently (see '
    'closure report S4a). The open chapter scope (all remaining chapters, the '
    'Chapter-8-Friday-standard retrofit of chapters 1-25) is carried forward to the fresh, narrow '
    'lineage sen0414-ch09ch10-lineage, opened in the same step, under the same course-wide mission '
    'picture. The 16 exam/mock-exam InProgress and Ready items are NOT carried forward: the '
    'midterm was held in full attendance and exam work is held outside this repository (see '
    'closure report S2). The two chapter-retrofit InProgress stories (Chapter 4 Functions, Chapter '
    '6 Lists, to the Chapter-8-Friday standard) belong to the later retrofit lineage, not to this '
    'week\'s narrow lineage, and are NOT carried forward now. Of the 74 Ready items, only those '
    'naming chapter 9 or chapter 10 are carried forward: TK_Ret_Ch09_Research, '
    'TK_Ret_Ch09_Research_Verify and their story ST_CI5_Research_Ch09 (chapter 9, Text Pattern '
    'Matching with Regular Expressions, research set and first page ABox against the chapter '
    'check) — all other Ready items stay in Lineage2 pending the later retrofit/mock-exam '
    'lineages. Archival of this register (backlog_lineage_archive) runs in the next release, not '
    'inside this box, per discipline step 6; this version only records the closure."@en ;\n'
)

OUTCOME_TRIPLE = (
    "\nex:Lineage2 backlog:hasLineageStatus backlog:LS_Abandoned ; backlog:lineageArchived false ;\n"
    '    backlog:hasRationale "Closed by narrowing 2026-11-08 per CLOSURE_REPORT_sen0414_slides_'
    'lineage_Lineage2_v1_0_0.md: scope not exhausted, remainder carried to sen0414-ch09ch10-lineage '
    'under the unchanged course-wide mission picture; LS_Abandoned used for want of a closed-by-'
    'narrowing term (owner question raised); archival deferred to the next release (G215)."@en .\n'
)


def main() -> int:
    text = SRC.read_text(encoding="utf-8")
    m = re.search(r'owl:versionInfo "2\.401\.0" ;', text)
    if not m:
        print("REFUSED: expected owl:versionInfo \"2.401.0\" header not found; identity check failed (B4).", file=sys.stderr)
        return 1
    text = text.replace(
        'owl:versionInfo "2.401.0" ; owl:versionIRI <http://example.org/sen0414-slides-lineage/2.401.0> ; owl:priorVersion <http://example.org/sen0414-slides-lineage/2.400.0> ;',
        'owl:versionInfo "2.402.0" ; owl:versionIRI <http://example.org/sen0414-slides-lineage/2.402.0> ; owl:priorVersion <http://example.org/sen0414-slides-lineage/2.401.0> ;',
        1,
    )
    # Insert the new closure comment as the first rdfs:comment (most recent on top, matching existing convention)
    text = text.replace(
        '    rdfs:comment "2.401.0 (2026-11-02): Exam: mock-h resumed start 23:39:00Z for the linked set v1.1.0; controls of release and concept-link parts."@en ;\n',
        CLOSURE_COMMENT + '    rdfs:comment "2.401.0 (2026-11-02): Exam: mock-h resumed start 23:39:00Z for the linked set v1.1.0; controls of release and concept-link parts."@en ;\n',
        1,
    )
    text = text.rstrip("\n") + "\n" + OUTCOME_TRIPLE
    DST.write_text(text, encoding="utf-8")
    print(f"Wrote {DST} ({len(text)} bytes). Append-only: {SRC} untouched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
