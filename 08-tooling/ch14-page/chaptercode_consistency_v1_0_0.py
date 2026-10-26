#!/usr/bin/env python3
"""Chapter-code consistency of a built page against its page data and the chapter-code manifest (same checks as the log chaptercode_consistency_v9_96_0.log; written as a file).
Usage: chaptercode_consistency_v1_0_0.py PAGE_VER   e.g. 9_97_0  (chapter 14)"""
import json, re, sys
pv = sys.argv[1]; R = "/home/claude/AdvancedProgrammingWithPython/"
page = open(R + "03-materials/ch14/page/sen0414_ch14_page_v%s.html" % pv, encoding="utf-8").read()
pd = json.load(open(R + "08-tooling/ch14-page/page_data_v%s.json" % pv)); man = json.load(open(R + "03-materials/ch14/page/chapter_code_ch14_v1_0_0.json"))
ex = man["examples"]; cc = pd["chaptercode"]["examples"]
print("meta page-standard:", re.findall(r'name="page-standard" content="([^"]+)"', page))
print("data-pane=chaptercode present:", 'data-pane="chaptercode"' in page)
eq = [(e["order"], e["name"], e["code"]) for e in cc] == [(e.get("order", i + 1), e["name"], e["code"]) for i, e in enumerate(ex)]
print("page_data examples == manifest (order,name,code):", eq, len(cc), len(ex))
data = re.search(r'<script[^>]*id="data"[^>]*>(.*?)</script>', page, re.S).group(1); D = json.loads(data); pcc = D["chaptercode"]["examples"]
miss = [e["name"] for e in ex if e["code"] not in [p["code"] for p in pcc]]
print("manifest code strings found verbatim in the page's data: %d of %d missing: %s" % (len(ex) - len(miss), len(ex), miss))
o = [e["order"] for e in cc]; print("orders strictly increasing:", all(a < b for a, b in zip(o, o[1:])), "names unique:", len({e['name'].lower() for e in cc}) == len(cc))
s = [e.get("slide") for e in cc if e.get("slide") is not None]; print("slide numbers non-decreasing:", all(a <= b for a, b in zip(s, s[1:])))
sys.exit(0 if eq and not miss else 1)
