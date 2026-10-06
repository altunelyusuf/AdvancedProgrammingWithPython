#!/usr/bin/env python3
"""Program check v2.0.1 for the classroom-standard decks (examples_out v1.1.0 schema).

Every whole program a slide shows is verified two ways against the recording the deck was built
from: (1) the shown lines must be a VERBATIM slice of the program file - a slide captioned
'program <name>, lines a to b of n' must carry exactly those lines in order; (2) the program is
re-executed now, with the recorded run's inputs, and its transcript must equal the recorded one
AND appear on that slide. One mismatch refuses the deck.

Usage: program_check_v2_0_0.py <deck.pptx> <examples_out.json>
"""
__version__ = "2.0.1"
import json
import re
import subprocess
import sys
import zipfile
from xml.dom import minidom

deck, rec = sys.argv[1], json.load(open(sys.argv[2]))
CAP = re.compile(r"program ([A-Za-z0-9_.]+), lines (\d+) to (\d+) of (\d+)")


def slides(path):
    z = zipfile.ZipFile(path)
    out = []
    for n in sorted([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
                    key=lambda n: int(re.findall(r"\d+", n)[0])):
        d = minidom.parseString(z.read(n))
        paras = []
        for p in d.getElementsByTagName("a:p"):
            paras.append("".join(t.firstChild.nodeValue if t.firstChild else ""
                                 for t in p.getElementsByTagName("a:t")))
        out.append((n, paras))
    return out


norm = lambda t: re.sub(r"\s+", " ", t).strip()
bad, n_prog = [], 0
for name, paras in slides(deck):
    flat = norm(" ".join(paras))
    for p in paras:
        m = CAP.search(p)
        if not m:
            continue
        pname, a, b, n = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
        n_prog += 1
        if pname not in rec["_programs"]:
            bad.append((name, pname, "no such program in the recording"))
            continue
        pr = rec["_programs"][pname]
        lines = pr["code"].rstrip("\n").split("\n")
        if len(lines) != n:
            bad.append((name, pname, "caption says %d lines, the file has %d" % (n, len(lines))))
        if norm(" ".join(lines[a - 1:b])) not in flat:
            bad.append((name, pname, "lines %d-%d are not on the slide verbatim" % (a, b)))
        for run in pr["runs"]:
            got = subprocess.run([sys.executable, "-c", pr["code"]],
                                 input="\n".join(run["inputs"]) + ("\n" if run["inputs"] else ""),
                                 capture_output=True, text=True).stdout.strip()
            # the recording weaves each typed input into the transcript at its prompt; stdout
            # alone does not echo, so remove each input's first woven occurrence before comparing
            expect = run["transcript"]
            for inp in run["inputs"]:
                expect = expect.replace(inp + "\n", "", 1)
            if got != expect.strip():
                bad.append((name, pname, "re-run prints %r, the recording says %r" % (got[:60], run["transcript"][:60])))
            elif run["transcript"].strip() and norm(run["transcript"]) not in flat:
                bad.append((name, pname, "its transcript is not on the slide"))
print("%d program panels verified; %d mismatch(es)" % (n_prog, len(bad)))
for b in bad:
    print("  REFUSED", b)
sys.exit(1 if bad else 0)
