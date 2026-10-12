#!/usr/bin/env python3
"""Chapter 16 honesty check. The deck shows output of three kinds that a reader must be able to tell apart, and shows nothing it did not
run without saying so. From the finished .pptx, the recording (examples_out) and the plan's meta:
  1. every slide that shows a program (label 'program <name>, lines ...' or 'transcript of program <name>') whose recorded kind is
     'live' - one that reads the book's own database - must carry the words 'sweigartcats.db' and 'sha256 41f0d0b5bc2e' on that slide;
  2. every slide the plan lists under meta.notExecuted must carry the words 'NOT EXECUTED', and no other slide may;
  3. every slide the plan lists under meta.measured (a time measured once, by the research or by this deck) must carry the words
     'single run', and no slide that is not listed may show a time in seconds or milliseconds after the digits of a measurement
     ('0.0033 ms', '10.27 ms', '52.6 s'), because a time that is not marked as one run would read as a result of the program;
  4. the title slide must say that every output was printed by the Python it shows.
Usage: honesty_check_v1_0_0.py <deck.pptx> <examples_out.json> <deck_plan.json>   Exit 0 when nothing is refused."""
__version__ = "1.0.0"
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck_check_v1_0_0 import slides
CAP = re.compile(r"(?:transcript of program|program) ([A-Za-z0-9_]+_v\d_\d_\d\.py)")
TIME = re.compile(r"\b\d+(?:\.\d+)? ?(?:ms|s)\b(?![a-zA-Z])")


def main(deck, rec_path, plan_path):
    rec = json.load(open(rec_path))["_programs"]
    meta = json.load(open(plan_path))["meta"]
    ne, ms = set(meta["notExecuted"]), set(meta["measured"])
    bad, n_prog = [], 0
    for idx, (name, paras) in enumerate(slides(deck), 1):
        text = "\n".join(paras); low = text.lower()
        kinds = set()
        for p in paras:
            m = CAP.search(p)
            if m:
                if m.group(1) not in rec:
                    bad.append((idx, "names unrecorded program " + m.group(1)))
                else:
                    kinds.add(rec[m.group(1)]["kind"]); n_prog += 1
        if "live" in kinds and not ("sweigartcats.db" in text and "sha256 41f0d0b5bc2e" in text):
            bad.append((idx, "shows a program that reads the book's database but does not say 'sweigartcats.db' and 'sha256 41f0d0b5bc2e'"))
        has = "NOT EXECUTED" in text
        if idx in ne and not has:
            bad.append((idx, "is listed as NOT EXECUTED but the slide does not say so"))
        if has and idx not in ne:
            bad.append((idx, "says NOT EXECUTED but is not listed in the plan"))
        once = "single run" in low
        if idx in ms and not once:
            bad.append((idx, "shows a measured time but does not say 'single run'"))
        if idx not in ms and idx > 1 and any(TIME.search(p) for p in paras if not p.startswith(">>>")):
            bad.append((idx, "shows a time (%s) but is not listed as measured" % next(TIME.search(p).group(0) for p in paras if TIME.search(p))))
        if idx == 1 and "printed by the python above" not in low:
            bad.append((idx, "the title slide does not say that every output was printed by the Python it shows"))
    print("honesty_check %s: %d program(s) shown, %d slide(s) marked NOT EXECUTED, %d slide(s) with single-run times; %d refusal(s)"
          % (__version__, n_prog, len(ne), len(ms), len(bad)))
    for b in bad:
        print("  REFUSED slide %d: %s" % b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
