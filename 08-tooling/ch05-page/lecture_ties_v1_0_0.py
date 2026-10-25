#!/usr/bin/env python3
"""Makes the chapter 5 page's Lecture tab (lecture_v2_0_0.json) from the speaker notes of the deck 3.0.0: the talk track is read by the unchanged tool
ch03-page/lecture_from_notes_v1_0_0.py (sentences that address the lecturer or point at the slide are dropped), then the slide-to-concept ties below are
added from the slide titles; every id is checked against the nodes of the chapter's newest page data. Usage: lecture_ties_v1_0_0.py <deck.pptx> <page_data.json> <out.json>"""
__version__ = "1.0.0"
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
TIE = {6: "BugModel", 7: "RaiseStatement", 8: "ExceptionMessage", 9: "TracebackReading", 10: "ExceptionNotes", 13: "AssertStatement", 14: "AssertVersusRaise",
       15: "OptimisedMode", 18: "LoggingVersusPrint", 19: "Logging", 20: "LoggingLevels", 21: "BasicConfig", 22: "LogFormat", 23: "LogToFile",
       24: "DisablingLogging", 25: "LazyFormatting", 28: "OffByOneRange", 29: "OffByOneRange", 30: "StringConcatenation", 31: "TypeMismatchComparison",
       32: "TypeMismatchComparison", 36: "StopControl", 37: "Debugger", 38: "BreakpointFunction", 39: "InstrumentChoice", 40: "ModernPractice"}
ids = {n["id"] for n in json.load(open(sys.argv[2]))["nodes"]}
bad = [v for v in TIE.values() if v not in ids]
if bad: raise SystemExit("REFUSED: unknown concept ids %r" % bad)
tmp = os.path.join(tempfile.mkdtemp(), "lec.json")
subprocess.run([sys.executable, os.path.join(HERE, "..", "ch03-page", "lecture_from_notes_v1_0_0.py"), sys.argv[1], sys.argv[2], tmp], check=True)
d = json.load(open(tmp))
for s in d["slides"]: s["concept"] = TIE.get(s["n"], "")
d["_version"] = "2.0.0"; d["_deck"] = os.path.basename(sys.argv[1])
d["_note"] = "2.0.0 (over 1.0.0, which stays as it is): made from the speaker notes of the deck 3.0.0 by lecture_ties_v1_0_0.py (with the unchanged lecture_from_notes_v1_0_0.py); %d slides tied to a concept by slide title, each id checked against the page data nodes." % len(TIE)
json.dump(d, open(sys.argv[3], "w"), indent=1, ensure_ascii=False)
print("written", sys.argv[3], len(d["slides"]), "slides,", sum(1 for s in d["slides"] if s["concept"]), "tied to a concept")
