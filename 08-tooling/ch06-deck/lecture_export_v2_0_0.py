"""Writes the text the chapter page shows on its Lecture tab from the chapter 6 deck plan, version 2.0.0.
Unlike chapter 5's lecture_export_v1_0_0.py, which cut presenter cues out of a talk track, the notes of deck version 2.0.0
are already reader's prose (deck_notes_check_v1_0_0.py refuses anything else), so each slide's note is exported whole as
'say', beside its title, the concept it is about and an empty visual, the shape the page reads.
Usage: lecture_export_v2_0_0.py <deck_plan.json> <out.json>"""
__version__ = "2.0.0"
import json, sys
plan = json.load(open(sys.argv[1]))
out = [{"n": i, "title": s["title"], "say": s["notes"].strip(), "concept": s.get("concept", ""), "visual": ""}
       for i, s in enumerate(plan["slides"], 1)]
json.dump({"_version": __version__, "_deck": plan["meta"]["version"], "_python": plan["meta"]["python"], "slides": out},
          open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
print("written", sys.argv[2], len(out), "slides")
