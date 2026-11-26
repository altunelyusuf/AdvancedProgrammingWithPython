#!/usr/bin/env python3
"""measure_links 1.0.0 (Lineage13, 2026-11-26): asks every external link of the decks of chapters 18, 19 and 20 with a plain GET (a redirect is followed, the final status counts) and checks the story pictures:
each story image file exists in the chapter's assets, and its record names the licence, the credit, the source and the retrieval date. Links: chapter 18 from the spec 4.0.0 words (resources and story links), chapters 19 and 20 from
their links files. A lineage's own script, disclosed (a tool gap handed to BRSF). Usage: measure_links_v1_0_0.py OUT.json"""
__version__ = "1.0.0"
import json, os, sys, time, urllib.error, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H))
sys.path.insert(0, os.path.join(R, "08-tooling/ch18-deck/spec_v4_0_0"))
import content_v4_0_0 as C18
links = {18: [u for _, u, _ in C18.RESOURCES] + [s["link"] for s in C18.STORIES.values()],
         19: json.load(open(os.path.join(R, "08-tooling/ch19-deck/links_v1_0_0.json")))["links"],
         20: json.load(open(os.path.join(R, "08-tooling/ch20-deck/links_v1_0_1.json")))["links"]}
imgs = {18: ({s["img"] for s in C18.STORIES.values()}, "03-materials/ch18/assets/story_images_v2_0_3.json"),
        19: (None, "03-materials/ch19/assets/story_images_v1_0_0.json"), 20: (None, "03-materials/ch20/assets/story_images_v1_0_0.json")}
res = {"links": {}, "pictures": {}}; bad = 0
for ch, us in links.items():
    for u in dict.fromkeys(us):
        code = None
        for attempt in range(2):
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0 SEN0414-course"})
            try:
                with urllib.request.urlopen(req, timeout=45) as r: code = r.status
            except urllib.error.HTTPError as e: code = e.code
            except Exception as e: code = type(e).__name__
            if code == 200 or attempt: break
            time.sleep(3)
        res["links"][u] = code; bad += code != 200
        print("link", ch, code, u, flush=True)
for ch, (names, rec) in imgs.items():
    d = json.load(open(os.path.join(R, rec))); adir = os.path.dirname(os.path.join(R, rec))
    for f, v in d.items():
        if f.startswith("_") or (names is not None and f not in names): continue
        miss = [k for k in ("LicenseShortName", "Credit", "SlideCredit", "source_url", "file_page", "retrieved") if not v.get(k)]
        ok = os.path.exists(os.path.join(adir, f)) and not miss
        res["pictures"][f] = {"chapter": ch, "file_exists": os.path.exists(os.path.join(adir, f)), "missing_fields": miss, "licence": v.get("LicenseShortName"), "retrieved": v.get("retrieved")}
        bad += not ok
        print("picture", ch, "ok" if ok else "PROBLEM", f, v.get("LicenseShortName"), miss)
json.dump(res, open(sys.argv[1], "w"), indent=1)
print("links asked:", len(res["links"]), "answering 200:", sum(1 for c in res["links"].values() if c == 200), "| pictures checked:", len(res["pictures"]), "complete:", sum(1 for p in res["pictures"].values() if p["file_exists"] and not p["missing_fields"]))
