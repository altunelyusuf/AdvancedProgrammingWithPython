"""Chapter 17 content for the RDODI build, version 1.0.3: the same content as 1.0.2, with the executed claims made reproducible (2026-10-29, TK_Ret_Ch17_Research).
Finding (the controller's log control-iter20-logs/pre_Research_Ch17.log): the execution checks of 1.0.2 end exit 1 on a machine whose python3.14 does not hold pypdf 6.20.1,
python-docx 1.2.0, pdfminer.six 20260107, Pillow 12.3.0, cryptography 50.0.2 and lxml 6.1.3, because the claims were recorded in an interpreter that had them
(ModuleNotFoundError: No module named 'pypdf'); a machine that has the libraries at other versions would print other versions.
This version keeps everything of 1.0.2 (sources, findings, concepts, taxonomy, section bodies, the text of every claim, every expected result, the dates and versions) and changes
only HOW the claims are executed: each example, claim and behaviour runs in the isolated environment that sen0414_ch17_isolated_env_v1_0_0.py builds itself (a virtual environment with
the 10 pinned packages installed with no network from the wheels committed in 03-materials/ch17/assets and 03-materials/ch17/assets/env_wheels_v1_0_0, each checked against a
recorded SHA-256, and nothing else). The code of a claim is the code of 1.0.2 byte for byte; no expected result is changed; no claim is weakened or dropped. The claim that the
interpreter is 3.14 or newer is made of the interpreter that builds the environment and stays as it was.
1.0.0, 1.0.1 and 1.0.2 are committed and are not edited."""
import ast, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0414_ch17_rdodi_data_v1_0_2 import *   # noqa: F401,F403
import sen0414_ch17_rdodi_data_v1_0_2 as _P
__version__ = "1.0.3"

_ENV = "sen0414_ch17_isolated_env_v1_0_0"


def _code(expr):
    """the code string of an expression made by X(): (lambda g: (exec(<code>, g), g['out'])[1])({})"""
    return ast.literal_eval(ast.parse(expr, mode="eval").body.func.body.value.elts[0].args[0])


def X2(code):
    """the same example as one expression with no double quote and no line break, run in the isolated environment"""
    lit = "'" + code.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace('"', "\\x22") + "'"
    return "__import__('%s').out(%s)" % (_ENV, lit)


def _wrap(expr):
    c = _code(expr)
    assert _P.X(c) == expr, "the expression is not the one X() makes"
    return X2(c)


def _beh(code):
    return "import %s as _e; _e.run(%r)" % (_ENV, code)


TAX = [(t, m, l, e, d, (_wrap(io[0]), io[1]) if io else io) for t, m, l, e, d, io in _P.TAX]
CLAIMS = [(_wrap(e), w) for e, w in _P.CLAIMS]
BEH = [[what, _beh(code), want] for what, code, want in _P.BEH]
