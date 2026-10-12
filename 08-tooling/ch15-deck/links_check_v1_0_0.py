#!/usr/bin/env python3
"""Opens every link of the resources slide (links_v1_0_0.json, written by deck_build_v1_0_0.py) and every link of the stories'
fact rows with requests, and writes the status each answered to links_out_v1_0_0.json. A status of 400 or more, or no answer,
fails the check, because the slide says every link was opened on the day the deck was made.
Usage: links_check_v1_0_0.py   (needs requests; goes through the build machine's proxy)"""
__version__ = "1.0.0"
import datetime, json, os, sys
import requests
HERE = os.path.dirname(os.path.abspath(__file__))
links = json.load(open(os.path.join(HERE, "links_v1_0_0.json")))["links"]
plan = json.load(open(os.path.join(HERE, "deck_plan_v1_0_0.json")))
for sl in plan["slides"]:
    for it in sl["items"]:
        if it.get("t") == "factrow" and it["link"] not in links:
            links.append(it["link"])
rows, bad = [], 0
for u in links:
    try:
        r = requests.get(u, timeout=30, headers={"User-Agent": "Mozilla/5.0 (SEN0414 deck link check)"}, stream=True)
        st = r.status_code; r.close()
    except Exception as e:
        st = "%s" % type(e).__name__
    rows.append([u, st])
    if not isinstance(st, int) or st >= 400:
        bad += 1
    print("  %s  %s" % (st, u))
json.dump({"_version": __version__, "checked": datetime.date.today().isoformat(), "links": rows}, open(os.path.join(HERE, "links_out_v1_0_0.json"), "w"), indent=1)
print("links_check %s: %d link(s) opened, %d not answered with a status below 400" % (__version__, len(rows), bad))
sys.exit(1 if bad else 0)
