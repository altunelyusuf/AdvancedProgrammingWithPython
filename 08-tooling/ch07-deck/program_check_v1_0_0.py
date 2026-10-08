#!/usr/bin/env python3
"""Chapter 7 program check. Every whole program (or excerpt) a slide shows is verified against the recording:
  (1) the label 'program <name>, lines a to b of n' must name a recorded program with n lines, and exactly those lines,
      in order, must be on the slide, verbatim (whitespace-normalised);
  (2) the program is run again now, here, with the recorded typed inputs fed through an echoing input() (the same shim
      the recording used), and its transcript must equal the recorded one;
  (3) that transcript must be on the same slide, verbatim.
Usage: program_check_v1_0_0.py <deck.pptx> <examples_out.json> [python]   Exit 0 when nothing mismatches."""
__version__ = "1.0.0"
import json
import re
import subprocess
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from deck_check_v1_0_0 import slides

CAP = re.compile(r"program ([A-Za-z0-9_.]+), lines (\d+) to (\d+) of (\d+)")
PRE = "import builtins\n_q = iter(%r)\ndef _input(prompt=''):\n    v = next(_q)\n    print(v)\n    return v\nbuiltins.input = _input\n"
norm = lambda t: re.sub(r"\s+", " ", t).strip()


def main(deck, rec_path, py):
    rec = json.load(open(rec_path))
    bad, n = [], 0
    for name, paras in slides(deck):
        flat = norm(" ".join(paras))
        for p in paras:
            m = CAP.search(p)
            if not m:
                continue
            pname, a, b, total = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
            n += 1
            pr = rec["_programs"].get(pname)
            if pr is None:
                bad.append((name, pname, "no such program in the recording"))
                continue
            lines = pr["code"].rstrip("\n").split("\n")
            if len(lines) != total:
                bad.append((name, pname, "label says %d lines, the program has %d" % (total, len(lines))))
            if norm(" ".join(lines[a - 1:b])) not in flat:
                bad.append((name, pname, "lines %d-%d are not on the slide verbatim" % (a, b)))
            r = subprocess.run([py, "-c", PRE % pr["inputs"] + pr["code"]], capture_output=True, text=True)
            got = r.stdout.rstrip("\n")
            if r.returncode or got != pr["transcript"]:
                bad.append((name, pname, "re-run prints %r, the recording says %r" % (got[:60], pr["transcript"][:60])))
            elif pr["transcript"].strip() and norm(pr["transcript"]) not in flat:
                bad.append((name, pname, "its transcript is not on the slide"))
    print("program_check %s: %d program panels verified (slice verbatim, re-run equal, transcript on the slide); %d mismatch(es)"
          % (__version__, n, len(bad)))
    for x in bad:
        print("  REFUSED", x)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else sys.executable))
