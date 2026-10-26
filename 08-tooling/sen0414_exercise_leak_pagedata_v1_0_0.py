#!/usr/bin/env python3
"""sen0414_exercise_leak_pagedata v1_0_0 - writes, from the data of a PAGE (the JSON of <script id="data">), a manifest-shaped file {"examples":[{name,code,expected}]} of every node's io program with its recorded output, for sen0414_exercise_leak_probe_v1_0_0.js (the page's blank exercises are made from these programs).
Usage: sen0414_exercise_leak_pagedata_v1_0_0.py PAGE.html OUT.json"""
import json, re, sys
t = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r'<script[^>]*id="data"[^>]*>(.*?)</script>', t, re.S); D = json.loads(m.group(1))
ex = []
def walk(o, path=""):
    if isinstance(o, dict):
        io = o.get("io")
        if isinstance(io, dict) and io.get("code") and "out" in io and not io.get("note"):
            ex.append({"name": o.get("id") or o.get("label") or path, "code": io["code"], "expected": str(io["out"])})
        for k, v in o.items(): walk(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, path + "/%d" % i)
walk(D)
seen = set(); u = []
for e in ex:
    if e["code"] not in seen: seen.add(e["code"]); u.append(e)
json.dump({"examples": u}, open(sys.argv[2], "w")); print(len(u), "programs from", sys.argv[1])
