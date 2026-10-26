#!/usr/bin/env python3
"""Asks every external link of the chapter 18 deck 2.0.1 (the resources slide and the story links of deck_content_v2_0_1.py) with a plain GET and prints the HTTP status;
exit 0 only when every link answers 200 (a redirect is followed and its final status counts). Usage: python3 links_check_v2_0_1.py [out.json]"""
__version__ = "2.0.1"
import importlib.util, json, os, sys, urllib.error, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("deck_content", os.path.join(HERE, "deck_content_v2_0_1.py"))
T = importlib.util.module_from_spec(sp)
sp.loader.exec_module(T)
links = [(t, u) for t, u, _ in T.RESOURCES] + [(s["linktext"], s["link"]) for s in T.STORIES.values()]
res, bad = {}, 0
for t, u in links:
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0 SEN0414-course"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            code = r.status
    except urllib.error.HTTPError as e:
        code = e.code
    except Exception as e:
        code = type(e).__name__
    res[u] = code
    bad += code != 200
    print(code, u)
if len(sys.argv) > 1:
    json.dump(res, open(sys.argv[1], "w"), indent=1)
print("%d links, %d not answering 200" % (len(links), bad))
sys.exit(1 if bad else 0)
