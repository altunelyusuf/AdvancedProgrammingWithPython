"""Chapter 4 deck examples, version 3.2.0: the code examples of the chapter 4 lecture deck (Functions), in slide order, one code box per code slide.
A NEW file beside examples_v3_1_0.py (which stays as committed): the examples are read from it and re-shaped for the Chapter 8 way.
`code` is the whole example as a script that can be copied: four spaces per level, every compound statement over several lines, no prompt, no lambda.
`notes` are the short plain-language explanations placed beside the code box (one per code group of version 3.1.0, each with at least 8 words).
Change against 3.1.0: the example `stack` measured its depth with a lambda; it now uses a def function (same values). Nothing here carries a result:
deck_build_v3_2_0.py runs the code and takes every printed result from the run."""
__version__ = "3.2.0"
import importlib.util
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location("examples_v3_1_0", os.path.join(_here, "examples_v3_1_0.py"))
_old = importlib.util.module_from_spec(_sp)
sys.modules["examples_v3_1_0"] = _old
_sp.loader.exec_module(_old)

EXAMPLES = []
for _e in _old.EXAMPLES:
    _d = {k: v for k, v in _e.items() if k not in ("groups", "layout")}
    _d["code"] = [l for g, _n in _e["groups"] for l in g]
    _d["notes"] = [n for _g, n in _e["groups"]]
    EXAMPLES.append(_d)

BY_ID = {e["id"]: e for e in EXAMPLES}

_st = BY_ID["stack"]
_i = _st["code"].index("depth = lambda: len(inspect.stack()) - base - 1")
_st["code"][_i:_i + 1] = ["def depth():", "    return len(inspect.stack()) - base - 1"]


def code_lines(ex):
    return list(ex["code"])


def code_text(ex):
    return "\n".join(ex["code"])

_st["notes"][0] = "inspect.stack lists every waiting frame. depth counts them above the top level; the minus 1 leaves out the frame of depth itself."
