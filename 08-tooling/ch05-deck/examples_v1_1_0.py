__version__ = "1.1.0"
# Every expression and every whole program the SEN0414 chapter 5 LECTURE deck (version 1.1.0) shows.
# Outputs come from executing them (examples_run_v1_1_0.py), never from typing.
#
# What is new against 1.0.0: the chapter corpus now carries one input-output example for each concept that has one,
# already executed by the corpus's own checker. Those expressions are read straight out of the corpus here, so the
# deck shows the same example the interactive page shows for the same concept, and the deck checker re-runs it.
# The whole programs of version 1.0.0 are kept unchanged and are reused, with the leaf concept each one belongs to.
import os, re, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from examples_v1_0_0 import EX as EX_V1, PROGRAMS                      # the programs of deck version 1.0.0, unchanged


def _corpus():
    folder = os.path.dirname(HERE)
    best, key = None, None
    for n in os.listdir(folder):
        m = re.fullmatch(r"sen0414_ch05_corpus_v(\d+_\d+_\d+)\.py", n)
        if m:
            k = tuple(int(p) for p in m.group(1).split("_"))
            if key is None or k > key:
                best, key = os.path.join(folder, n), k
    spec = importlib.util.spec_from_file_location("ch05corpus", best)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_C = _corpus()
CONCEPT_EX = {n[0]: n[4][2][0] for n in _C.NODES if n[4] and n[4][2]}
EX = dict(EX_V1)
EX["concepts"] = [CONCEPT_EX[k] for k in sorted(CONCEPT_EX)]
EX["_concept_order"] = sorted(CONCEPT_EX)

LEAF_PROGRAM = {
    "RaiseStatement": "boxprint_v1_0_0.py",
    "ExceptionUnwinding": "unwinding_v1_0_0.py",
    "ExceptionNotes": "notes_v1_0_0.py",
    "AssertStatement": "assertdemo_v1_0_0.py",
    "AssertMessage": "assertmsg_v1_0_0.py",
    "OptimisedMode": "optimised_v1_0_0.py",
    "BasicConfig": "levelsdemo_v1_0_0.py",
    "LogToFile": "filelog_v1_0_0.py",
    "ForceReconfigure": "force_v1_0_0.py",
    "DisablingLogging": "disable_v1_0_0.py",
    "LazyFormatting": "lazy_v1_0_0.py",
    "OffByOneRange": "factorial_bug_v1_0_0.py",
    "AccumulatorStart": "factorial_fixed_v1_0_0.py",
    "StringConcatenation": "adding_bug_v1_0_0.py",
    "LogicError": "adding_fixed_v1_0_0.py",
    "TypeMismatchComparison": "cointoss_bug_v1_0_0.py",
    "Breakpoint": "debugdemo_v1_0_0.py",
}
assert set(LEAF_PROGRAM.values()) == set(PROGRAMS), sorted(set(PROGRAMS) ^ set(LEAF_PROGRAM.values()))
