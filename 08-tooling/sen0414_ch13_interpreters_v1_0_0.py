#!/usr/bin/env python3
"""Chapter 13: runs one small robots.txt program under every installed 3.14 patch release (3.14.0 to 3.14.6, installed with
`uv python install 3.14.N`) and records what urllib.robotparser answered, because the answer changed inside the 3.14 series:
the changelog of Python 3.14.5 lists gh-138907, 'Support RFC 9309 in urllib.robotparser'.
Usage: sen0414_ch13_interpreters_v1_0_0.py   (needs uv on PATH)   -> ch13-page/interpreter_record_v1_0_0.json"""
__version__ = "1.0.0"
import json, os, subprocess, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "08-tooling", "ch13-page", "interpreter_record_v1_0_0.json")
PROG = r'''
import sys, urllib.robotparser as rp
def can(rules, agent, url):
    r = rp.RobotFileParser(); r.parse(rules); return r.can_fetch(agent, url)
star = ['User-agent: *', 'Disallow: /search*']
gif = ['User-agent: *', 'Disallow: /*.gif$']
allow = ['User-agent: *', 'Disallow: /docs/', 'Allow: /docs/public/']
print(sys.version.split()[0], [can(star, '*', 'https://pypi.org/search/?q=boring+stuff'), can(star, '*', 'https://pypi.org/project/pyautogui/'),
      can(gif, '*', 'https://x.example/a/b.gif'), can(gif, '*', 'https://x.example/a/b.gif.txt'), can(allow, '*', 'https://x.example/docs/public/a'), can(allow, '*', 'https://x.example/docs/secret/a')])
'''
rows = []
for v in ("3.14.0", "3.14.1", "3.14.2", "3.14.3", "3.14.4", "3.14.5", "3.14.6"):
    r = subprocess.run(["uv", "run", "--no-project", "--python", v, "python", "-I", "-c", PROG], capture_output=True, text=True, timeout=300)
    rows.append(r.stdout.strip() or "FAILED: " + r.stderr.strip().splitlines()[-1])
    print(rows[-1])
json.dump({"_version": "1.0.0", "program": PROG.strip(), "columns": ["search page with Disallow: /search*", "project page", "/*.gif$ against b.gif", "/*.gif$ against b.gif.txt", "Allow: /docs/public/ against /docs/public/a", "Disallow: /docs/ against /docs/secret/a"], "rows": rows,
           "_note": "Run on %s with each CPython 3.14 patch release installed by uv. The Python 3.14 changelog places gh-138907 (Support RFC 9309 in urllib.robotparser) in 3.14.5." % __import__("datetime").date.today().isoformat()}, open(OUT, "w"), indent=1)
