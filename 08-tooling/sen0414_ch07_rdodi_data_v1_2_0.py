"""Chapter 7 content for the RDODI build, version 1.2.0: renews 1.1.0 with one finding corrected.

Measured while verifying the built page (deep passage search): the corpus's own concept "The dict
constructor" (sen0414_ch07_corpus_text_a_v1_0_0.py, DictionaryConstructors) cites the same source
this module already lists as P02 (docs.python.org/3/library/stdtypes.html, "mapping types dict"), but
no finding's text ever used the words "dict() constructor" - a semantic search over the finding texts
for that phrase found nothing to surface, even though the source backing it was already in P02's list.
F7 ("Contemporary developments", which already names what current Python gives dictionaries beyond the
chapter) is amended to name the constructor explicitly, still citing only sources already in the list
(P02, where class dict(**kwarg) / dict(mapping, **kwarg) / dict(iterable, **kwarg) are documented). No
other finding, source or concept changes; this module imports 1.1.0 and overrides FINDINGS alone."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0414_ch07_rdodi_data_v1_1_0 import *   # noqa: F401,F403
from sen0414_ch07_rdodi_data_v1_1_0 import FINDINGS as _F110
__version__ = "1.2.0"

FINDINGS = [
    (fid, kind, (text + " The dict() constructor itself - keyword arguments, a list of pairs, another mapping or zip of two lists - is also not in the chapter's own text." if fid == "F7" else text), cites)
    for (fid, kind, text, cites) in _F110
]
