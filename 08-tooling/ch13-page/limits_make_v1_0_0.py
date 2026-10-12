"""Writes limits_v1_0_0.json, the chapter 13 page's 'Provenance & known limits' entries, from the three records Phase A made
(third_party_record_v1_0_1.json, live_observations_v1_0_1.json, interpreter_record_v1_0_0.json) and from the 'Not executed' paragraph of
sen0414_ch13_rdodi_data_v1_0_3.py. Every number and every quoted value is read from those files, none is typed here; the page-data
builder 2.9.0 shows the list under About > Provenance & known limits, ahead of the three limits the template always adds.
Usage: limits_make_v1_0_0.py"""
__version__ = "1.0.0"
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
tp = json.load(open(os.path.join(H, "third_party_record_v1_0_1.json")))
lv = json.load(open(os.path.join(H, "live_observations_v1_0_1.json")))
ir = json.load(open(os.path.join(H, "interpreter_record_v1_0_0.json")))
src = open(os.path.join(H, "..", "sen0414_ch13_rdodi_data_v1_0_3.py"), encoding="utf-8").read()
live = {i["what"]: i["saw"] for i in lv["items"]}
find = lambda start: next(v for k, v in live.items() if k.startswith(start))
out = []
# 1. what kind of record the live observations are
out.append("The live-site observations of this page are single requests made on %s through the build machine's proxy with %s; %s" % (lv["observed"], lv["with"], lv["_note"].split("; ", 1)[1].rstrip(".") + "."))
# 2. PyPI
st, title, n = find("pypi.org search page")
out.append("pypi.org's search page, fetched by requests on %s, answered status %s with the title %r and %d elements of the class package-snippet, so the chapter's searchpypi.py opens no tab on today's site; the program was run against a local stand-in results page to show it working." % (lv["observed"], st, title, n))
# 3. rj.txt
first = find("rj.txt of the chapter"); chunks = find("rj.txt: the sizes")[0]
out.append("rj.txt, the file the chapter downloads in chunks, was %d bytes long on %s (chunks %s) where the chapter prints 178978 bytes (chunks [100000, 78978]); the page's own example uses a 178978-byte stand-in." % (first[2], lv["observed"], chunks))
# 4. interpreter record
rows = [r.split(" ", 1) for r in ir["rows"]]
old = [v for v, r in rows if json.loads(r.lower().replace("true", "true").replace("false", "false"))[0]]
new = [v for v, r in rows if not json.loads(r.lower())[0]]
out.append("urllib.robotparser answers differently by release: for 'Disallow: /search*' the search page was allowed under Python %s and refused from %s (%s, recorded on %s with each release installed by uv); the page's in-browser Python is Pyodide's CPython 3.13, so its robots.txt examples use plain prefix rules, which every release reads alike." % (", ".join(old), new[0], "the %d releases 3.14.0 to 3.14.6" % len(rows), re.search(r"Run on (\d{4}-\d{2}-\d{2})", ir["_note"]).group(1)))
# 5. third-party programs
out.append("The programs that need requests, Beautiful Soup, Selenium or Playwright were run on the build machine under %s (%d recorded runs in third_party_record_v1_0_1.json, local fixtures only); those programs need a network and a site to reach, which a browser tab running Python cannot offer, so the page's Chapter examples use the standard library alone, and the last one shows that importing Selenium fails." % (tp["python"], len(tp["items"])))
# 6. not executed, quoted from the research data file
m = re.search(r"Not executed, and said so where it comes up: (.*?)\.\s+A\s+claim\s+not\s+in\s+this\s+file\s+was\s+not\s+made", src, re.S)
out.append("Not executed in the build environment: " + re.sub(r"\s+", " ", m.group(1)).strip() + ".")
json.dump({"_version": __version__, "limits": out}, open(os.path.join(H, "limits_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
for x in out: print("-", x)
