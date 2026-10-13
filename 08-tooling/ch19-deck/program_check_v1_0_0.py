#!/usr/bin/env python3
"""Chapter 19 program check (the chapter 15 check, with the programs run the way the recording ran them - progrun_v1_0_0 - and
with every recorded program required to have exited 0). Every whole program (or excerpt) a slide shows is verified against the
recording:
  (1) the label 'program <name>, lines a to b of n' must name a recorded program with n lines, and exactly those lines, in
      order, must be on the slide, verbatim (whitespace-normalised);
  (2) the program is run again now, here, with the recorded typed inputs, and its transcript must equal the recorded one;
  (3) that transcript must be on the same slide, verbatim;
  (4) a panel labelled 'transcript of program <name>' (a transcript shown without its code, or beside it) names a recorded
      program, which is run again and must print the recorded transcript, which must be on that slide.
No program of this chapter is LIVE (none reads the network or a fetched file); each is run again here under the interpreter given, so a program that depends on the clock or the zone would be refused.
Usage: program_check_v1_0_0.py <deck.pptx> <examples_out.json> [python]   Exit 0 when nothing mismatches."""
__version__ = "1.0.0"
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck_check_v1_0_0 import slides
from progrun_v1_0_0 import run_program

CAP = re.compile(r"program ([A-Za-z0-9_.]+), lines (\d+) to (\d+) of (\d+)")
TCAP = re.compile(r"transcript of program ([A-Za-z0-9_.]+)")
norm = lambda t: re.sub(r"\s+", " ", t).strip()


def main(deck, rec_path, py):
    rec = json.load(open(rec_path))
    bad, n, ran = [], 0, {}

    def rerun(pname):
        if pname not in ran:
            pr = rec["_programs"][pname]
            r = run_program(py, pr["code"], pr["inputs"], pr.get("needs", ()))
            ran[pname] = (r.returncode, r.stdout.rstrip("\n"))
        return ran[pname]

    for name, pr in rec["_programs"].items():
        if pr.get("exit", 0) != 0:
            bad.append(("recording", name, "the recorded program exited %r" % pr.get("exit")))
    for name, paras in slides(deck):
        flat = norm(" ".join(paras))
        for p in paras:
            t = TCAP.search(p)
            if t:
                n += 1
                pr = rec["_programs"].get(t.group(1))
                if pr is None:
                    bad.append((name, t.group(1), "no such program in the recording"))
                    continue
                code, got = rerun(t.group(1))
                if code or got != pr["transcript"]:
                    bad.append((name, t.group(1), "re-run (exit %d) prints %r, the recording says %r" % (code, got[:60], pr["transcript"][:60])))
                elif norm(pr["transcript"]) not in flat:
                    bad.append((name, t.group(1), "its transcript is not on the slide"))
                continue
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
            code, got = rerun(pname)
            if code or got != pr["transcript"]:
                bad.append((name, pname, "re-run (exit %d) prints %r, the recording says %r" % (code, got[:60], pr["transcript"][:60])))
            elif pr["transcript"].strip() and norm(pr["transcript"]) not in flat:
                bad.append((name, pname, "its transcript is not on the slide"))
    print("program_check %s: %d program panels verified (slice verbatim, re-run equal with exit 0, transcript on the slide); "
          "%d distinct program(s) re-run; %d mismatch(es)" % (__version__, n, len(ran), len(bad)))
    for x in bad:
        print("  REFUSED", x)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else sys.executable))
