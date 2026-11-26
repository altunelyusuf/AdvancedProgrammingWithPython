#!/usr/bin/env python3
"""Exports the chapter 20 deck 4.0.1 (42 slides) slide titles and speaker notes to ../ch20-page/lecture_v4_0_1.json, the Lecture tab of the chapter 20 page v9.101.0
(new file over lecture_v1_0_1.json, which describes a 26-slide deck that no longer exists; Lineage13). A code slide is linked to a page concept by hand (the chapter-code
manifest names book topics, whose labels differ from the page concepts) 03-materials/ch20/page/chapter_code_ch20_v1_2_1.json; every concept id is checked against the concept ids of the chapter's page data (the newest page_data json that holds nodes).
Other slides carry no concept. Usage: lecture_export_v4_0_1.py <deck.pptx> <python-version>"""
__version__ = "4.0.1"
import glob, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(HERE))
_pf = sorted(glob.glob(os.path.join(HERE, "..", "ch20-page", "page_data_v*.json")), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
NODES = json.load(open(_pf[-1]))["nodes"] if _pf else []
IDS = {n["id"] for n in NODES}; BYLABEL = {n["label"].lower(): n["id"] for n in NODES}
man = json.load(open(os.path.join(R, "03-materials/ch20/page/chapter_code_ch20_v1_2_1.json"), encoding="utf-8"))
# each code slide is linked by hand to the page concept that its example shows (slide of the code slide: concept id); every id is checked below against the ids of the page data
CONCEPT = {7: "CredentialsAndToken", 8: "SendCall", 9: "ThreadVersusMessage", 10: "ReplyThreading", 11: "FilenameTraversal", 16: "EmailMessageBuild", 17: "HeaderEncoding", 18: "StarttlsSession",
           19: "RefusedRecipients", 20: "EnvelopeVersusHeader", 25: "GatewayAddress", 26: "Gsm7Length", 27: "AttNotice", 28: "DomainStatus", 31: "PostBody", 32: "MetadataHeaders",
           33: "JsonLines", 34: "TopicSecrecy", 37: "AutoUnsubscriber", 38: "UmbrellaReminder", 39: "EmailControlLoop"}
bad = sorted({v for v in CONCEPT.values() if v not in IDS})
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = "Chapter 20: Sending Email, Texts and Push Notifications" if i == 1 else next(t for t in texts if t != ">>>")
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(), "concept": CONCEPT.get(i, ""), "visual": ""})
json.dump({"_version": __version__, "_deck": "4.0.1", "_python": sys.argv[2], "slides": out},
          open(os.path.join(HERE, "..", "ch20-page", "lecture_v4_0_1.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("lecture_v4_0_1.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
