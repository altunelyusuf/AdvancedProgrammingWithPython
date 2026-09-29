"""Turns the chapter 6 deck's talk track (lecture_out, written by deck_v1_0_0.js) into the text the chapter page shows on its Lecture tab, and exports the executed visual
specifications the slides draw. Same rule as chapter 5: the talk track is written for a lecturer at a projector, so any sentence that addresses the lecturer or points at the slide,
its builds or its layout is dropped ('click', 'slide', 'Ask', 'Give them', 'Answer aloud', 'Teach', 'students', 'the room', 'Program written for this course', 'send them',
'on the left', 'on the right', 'the code card', 'the box', 'the panel', 'the grid', 'the table'). Nothing is rewritten. Extensions over chapter 5: every slide also carries the
leaves it teaches ('covers') and the visuals it draws ('visuals'); the export is refused unless the slides together teach all 38 leaves of the chapter's taxonomy and every
visual named exists; the visuals file holds the visuals the slides draw plus the description of each kind of visual ('_kinds').
Usage: lecture_export_v1_0_0.py <lecture_out.json> <visuals_out.json> <taxonomy_out.json> <lecture_page.json> <visuals_page.json>"""
__version__ = "1.0.0"
import json, re, sys
lo, vo, tx, lp, vp = sys.argv[1:6]
src = json.load(open(lo)); VIS = json.load(open(vo)); TAX = json.load(open(tx))
DROP = re.compile(r"\b(click|clicks|slide|slides|Ask|Give them|Answer aloud|Teach|students|the room|Program written for this course|send them|on the left|on the right|the code card|the box|the panel|the grid|the table)\b", re.I)
leaves = {n["id"] for n in TAX["nodes"] if n["level"] == 3}; assert len(leaves) == 38, len(leaves)
out = []; covered = set(); used = []
for s in src["slides"]:
    sents = re.split(r"(?<=[.?!])\s+(?=[A-Z‘“'\"])", s["say"].strip())
    keep = [x for x in sents if x and not DROP.search(x)]
    out.append({"n": s["n"], "title": s["title"], "say": " ".join(keep) or s["title"], "concept": s["concept"], "covers": s["covers"], "visual": s["visual"], "visuals": s["visuals"]})
    covered |= ({s["concept"]} | set(s["covers"])) & leaves
    for v in s["visuals"]:
        assert v in VIS and not v.startswith("_"), ("no such visual", v)
        if v not in used: used.append(v)
missing = sorted(leaves - covered)
if missing: print("REFUSED: leaves no slide teaches:", missing); sys.exit(1)
json.dump({"_version": __version__, "_deck": src["version"], "_python": src["python"], "slides": out}, open(lp, "w"), indent=1, ensure_ascii=False)
V = {"_version": "1.0.0", "_python": VIS["_meta"]["python"], "_note": "Written from ch06-deck/visuals_out_v1_0_0.json, the executed specifications the deck also draws; only the visuals a slide draws are included. _kinds says what each kind of visual is."}
V["_kinds"] = {k: VIS["_kinds"][k] for k in sorted({VIS[v]["kind"] for v in used})}
for v in used: V[v] = VIS[v]
json.dump(V, open(vp, "w"), indent=1, ensure_ascii=False)
print("written %s: %d slides, %d with sentences dropped, all %d leaves taught; written %s: %d visuals" % (lp, len(out), sum(1 for a, b in zip(src["slides"], out) if a["say"] != b["say"]), len(leaves), vp, len(used)))
