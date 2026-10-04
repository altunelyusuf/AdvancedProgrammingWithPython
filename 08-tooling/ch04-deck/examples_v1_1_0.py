__version__ = "1.1.0"
# Every expression and every whole program the SEN0414 chapter 4 LECTURE deck (version 1.1.0) shows.
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
        m = re.fullmatch(r"sen0414_ch04_corpus_v(\d+_\d+_\d+)\.py", n)
        if m:
            k = tuple(int(p) for p in m.group(1).split("_"))
            if key is None or k > key:
                best, key = os.path.join(folder, n), k
    spec = importlib.util.spec_from_file_location("ch04corpus", best)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_C = _corpus()
# concept id -> the expression the corpus gives that concept as its input-output example
CONCEPT_EX = {n[0]: n[4][2][0] for n in _C.NODES if n[4] and n[4][2]}
EX = dict(EX_V1)
EX["concepts"] = [CONCEPT_EX[k] for k in sorted(CONCEPT_EX)]
EX["_concept_order"] = sorted(CONCEPT_EX)

# which leaf concept each whole program is the worked example of; the deck puts the program on that concept's slide,
# and program_check refuses the deck if a program's code or its transcript is not on a slide.
LEAF_PROGRAM = {
    "DefStatement": "hello_v1_0_0.py",
    "Deduplication": "pasted_v1_0_0.py",
    "ParameterAndArgument": "params_v1_0_0.py",
    "NamedParameter": "named_v1_0_0.py",
    # the positional-only concept is drawn as an executed table of real calls instead, so the program that shows both
    # kinds of parameter sits on the keyword-only concept next to it
    "KeywordOnlyParameter": "kinds_v1_0_0.py",
    "ReturnStatement": "returns_v1_0_0.py",
    "DefaultArgument": "defaults_v1_0_0.py",
    # the call-stack concept is drawn as an executed stack diagram, so the program that reads the stack back sits on
    # the concept about inspecting it
    "StackInspection": "stack_v1_0_0.py",
    "Recursion": "recursion_v1_0_0.py",
    "SameNameVariables": "scopes_v1_0_0.py",
    "GlobalStatement": "globalstmt_v1_0_0.py",
    "SymbolTable": "symtable_v1_0_0.py",
    "UnboundLocalError": "unbound_v1_0_0.py",
    "NonlocalStatement": "nonlocal_v1_0_0.py",
    "TryExcept": "inside_v1_0_0.py",
    "ErrorInCall": "outside_v1_0_0.py",
    "MultipleExceptTypes": "except758_v1_0_0.py",
    "DeferredAnnotations": "annotations_v1_0_0.py",
    "CollatzSequence": "collatz_v1_0_0.py",
    "InputValidation": "validated_v1_0_0.py",
}
assert set(LEAF_PROGRAM.values()) == set(PROGRAMS), sorted(set(PROGRAMS) ^ set(LEAF_PROGRAM.values()))
