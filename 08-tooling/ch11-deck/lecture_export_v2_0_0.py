#!/usr/bin/env python3
"""Exports the chapter 11 deck 2.0.0 (41 slides) slide titles and speaker notes to ../ch11-page/lecture_v2_0_0.json, the Lecture tab of the
chapter 11 page v9.95.0 (new file over lecture_v1_0_0.json, which describes the earlier 23-slide deck). Each slide is linked to the concept it teaches;
every concept id is checked against the concept ids of the chapter's page data (the newest page_data json that holds nodes).
Usage: lecture_export_v2_0_0.py <deck.pptx> <python-version>"""
__version__ = "2.0.0"
import glob, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
_pf = sorted(glob.glob(os.path.join(HERE, "..", "ch11-page", "page_data_v*.json")),
             key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
IDS = {n["id"] for n in json.load(open(_pf[-1]))["nodes"]} if _pf else set()
CONCEPT = {4: "CopyingAndMoving", 6: "CopyFile", 7: "CopyFolderTree", 8: "CopyWithMetadata", 9: "MoveFileOrFolder",
           10: "Deleting", 12: "DeleteFile", 13: "DeleteFolderTree", 14: "DryRun", 15: "RecycleBin",
           17: "FolderTrees", 19: "ListDirectory", 20: "WalkTree", 24: "ZipArchives", 26: "CreateZip", 27: "AppendToZip",
           28: "ExtractAll", 29: "MakeArchive", 32: "Programs", 34: "BackupProject", 35: "SelectiveCopy",
           36: "LargeFiles", 37: "DateRenaming"}
bad = [v for v in CONCEPT.values() if v not in IDS]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = "Chapter 11: Organizing Files" if i == 1 else next(t for t in texts if t not in (">>>",))
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(),
                "concept": CONCEPT.get(i, ""), "visual": ""})
json.dump({"_version": __version__, "_deck": "2.0.0", "_python": sys.argv[2], "slides": out},
          open(os.path.join(HERE, "..", "ch11-page", "lecture_v2_0_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("lecture_v2_0_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
