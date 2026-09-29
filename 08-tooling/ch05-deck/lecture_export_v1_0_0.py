"""Turns the deck's talk track (lecture_out_v1_0_0.json, written by deck_v1_0_0.js) into the text the chapter page shows on its Lecture tab.
The talk track is written for a lecturer at a projector; the page has no clicks and no slide numbers, so sentences that address the lecturer or
point at the slide or its builds are dropped: any sentence containing 'click', 'slide', 'Ask', 'Give them', 'Answer aloud', 'Teach', 'students', 'the room', 'Program written for this course', 'send them', or a pointer to the layout ('on the left', 'on the right', 'the code card', 'the box', 'the panel', 'the grid', 'the table'). Nothing is rewritten: what remains is the
lecturer's own sentences. Usage: lecture_export_v1_0_0.py <lecture_out.json> <out.json>"""
__version__ = "1.0.0"
import json, re, sys
src = json.load(open(sys.argv[1])); DROP = re.compile(r"\b(click|clicks|slide|slides|Ask|Give them|Answer aloud|Teach|students|the room|Program written for this course|send them|on the left|on the right|the code card|the box|the panel|the grid|the table)\b", re.I)
out = []
for s in src["slides"]:
    sents = re.split(r"(?<=[.?!])\s+(?=[A-Z‘“'\"])", s["say"].strip())
    keep = [x for x in sents if x and not DROP.search(x)]
    out.append({"n": s["n"], "title": s["title"], "say": " ".join(keep) or s["title"], "concept": s["concept"], "visual": s["visual"]})
json.dump({"_version": __version__, "_deck": src["version"], "_python": src["python"], "slides": out}, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
print("written", sys.argv[2], len(out), "slides;", sum(1 for a, b in zip(src["slides"], out) if a["say"] != b["say"]), "with sentences dropped")
