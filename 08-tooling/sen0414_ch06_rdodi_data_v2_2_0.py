"""Chapter 6 content for the RDODI build, version 2.2.0: restores what 2.1.0 dropped (2026-10-25).
Finding (controller, 2026-10-24): the domain ABox v2_1_0 holds 98 individuals where v2_0_0 holds 105, and the statement of 2.1.0 that nothing is removed is wrong.
Missing in 2.1.0: the six error conditions Err_Index, Err_IndexMethod, Err_MultipleAssignment, Err_MutableImmutable, Err_RandomChoice, Err_SortMethod with their
rd:hasErrorCondition links, the competency question CQ3 with its link from the competency list, the label of the resolution environment naming the three interpreters
(CPython 3.12.3, 3.13.16 and 3.14.6), the hasOwner links between concepts and the hasOwner property, the disjointness axioms of the TBox and the human class labels of 2.0.0.
This version keeps everything of 2.1.0 (TAX, BODY, sources, findings, claims, behaviours are those of 2.1.0, which are those of 2.0.0). The generic builder (1.2.0) cannot write the error conditions, CQ3 or hasOwner; sen0414_ch06_restore_v2_2_0.py runs the builder on this module and then adds every
triple of the v2_0_0 TBox and ABox (and every label of the v2_0_0 document) that the build lacks, so the 2.2.0 files are the 2.1.0 content plus the 2.0.0 content.
v2_0_0 and v2_1_0 are committed and are not edited."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0414_ch06_rdodi_data_v2_1_0 import *   # noqa: F401,F403
__version__ = "2.2.0"
