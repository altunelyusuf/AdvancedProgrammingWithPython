"""Chapter 15 content for the RDODI build, version 1.0.4: the content and the isolated-environment execution of 1.0.3, built with the chapter's own build runner (2026-10-27, TK_Ret_Ch15_Research).
Why a new version: the research files v1_0_3 (committed in the first step of this task) were built with the generic builder alone. The sections of this chapter have two paragraphs each, and the generic
builder's q() writes a line break raw into a one-line Turtle literal, so sen0414_ch15_document_v1_0_3.ttl does not parse (BadSyntax, newline found in string literal, line 29) and the gate Stage3.F stops on it.
The chapter's own runner sen0414_ch15_build_run_v1_0_0.py (committed earlier, used for 1.0.1 and 1.0.2) writes the break as \n; 1.0.4 is built with it. The committed v1_0_3 files are not edited; they stay as the record of the fault,
and the newest files (v1_0_4) are the research set.
Everything else is 1.0.3 unchanged: the same sources, findings, concepts, taxonomy, section bodies, claims and expected results; the claims that use the library run in the isolated environment of
sen0414_ch15_isolated_env_v1_0_0.py. No claim is weakened or dropped."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0414_ch15_rdodi_data_v1_0_3 import *   # noqa: F401,F403
__version__ = "1.0.4"
