#!/usr/bin/env python3
"""Exports the chapter 12 deck 2.0.0 (48 slides) slide titles and speaker notes to ../ch12-page/lecture_v2_0_0.json, the Lecture tab of the
chapter 12 page v9.95.0 (new file over lecture_v1_0_0.json, which describes the earlier deck). Each slide is linked to the concept it teaches;
every concept id is checked against the concept ids of the chapter's page data (the newest page_data json that holds nodes).
Usage: lecture_export_v2_0_0.py <deck.pptx> <python-version>"""
__version__ = "2.0.0"
import glob, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
_pf = sorted(glob.glob(os.path.join(HERE, "..", "ch12-page", "page_data_v*.json")),
             key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
IDS = {n["id"] for n in json.load(open(_pf[-1]))["nodes"]} if _pf else set()
CONCEPT = {4: "Terminal", 6: "ProgramVocabulary", 7: "ChangeDirectory", 8: "ListDirectory", 9: "PathVariable", 10: "WhichAndWhere",
           11: "Environments", 13: "CreatingAVenv", 14: "ActivatingAVenv", 15: "RunningPipAsAModule", 16: "PipInstaller",
           18: "SelfAware", 19: "PlatformChecks", 20: "ExitWithMessage", 21: "ArgvList", 22: "ArgparseModule", 23: "ArgparseModule",
           24: "TerminalOutput", 26: "TextDesign", 27: "SoundAndTextNotification", 28: "TextUserInterface", 29: "TerminalClearing",
           30: "ColorfulText", 31: "MessageBoxes", 32: "SnowstormProgram", 33: "Deployment", 35: "LauncherFiles",
           36: "ShellScriptLauncher", 37: "ExecutePermission", 38: "ShebangLine", 39: "DesktopEntry", 40: "CcwdCommand",
           41: "ClipboardRecorder", 42: "CompilingWithPyInstaller", 43: "BundledInterpreter", 44: "DeployablePrograms",
           47: "PracticeQuestions"}
bad = [v for v in CONCEPT.values() if v not in IDS]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = "Chapter 12: Command Line Programs" if i == 1 else next(t for t in texts if t not in (">>>",))
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(),
                "concept": CONCEPT.get(i, ""), "visual": ""})
json.dump({"_version": __version__, "_deck": "2.0.0", "_python": sys.argv[2], "slides": out},
          open(os.path.join(HERE, "..", "ch12-page", "lecture_v2_0_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("lecture_v2_0_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
