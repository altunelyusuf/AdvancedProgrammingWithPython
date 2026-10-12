#!/usr/bin/env python3
"""Chapter 15 honesty check. Google was never reached while this deck was made, so the deck itself must say so wherever it shows
output that did not come from Google. From the finished .pptx, the recording (examples_out) and the plan's meta:
  1. every slide that shows a program (label 'program <name>, lines ...' or 'transcript of program <name>') whose recorded kind is
     'standin' or 'fixture' must carry the words 'Stand-in for Google' on that slide;
  2. a slide that shows a program of kind 'fixture' must also carry the words 'recorded fixture';
  3. every slide the plan lists under meta.notExecuted must carry the words 'NOT EXECUTED', and no other slide may;
  4. the title slide must say that Google was never reached.
Usage: honesty_check_v1_0_0.py <deck.pptx> <examples_out.json> <deck_plan.json>   Exit 0 when nothing is refused."""
__version__ = "1.0.0"
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck_check_v1_0_0 import slides
CAP = re.compile(r"(?:program|transcript of program) ([A-Za-z0-9_.]+?)(?:,| *$)")


def main(deck, rec_path, plan_path):
    rec = json.load(open(rec_path))["_programs"]
    ne = set(json.load(open(plan_path))["meta"]["notExecuted"])
    bad, n_prog = [], 0
    for idx, (name, paras) in enumerate(slides(deck), 1):
        text = "\n".join(paras); low = text.lower()
        kinds = set()
        for p in paras:
            m = re.search(r"(?:transcript of program|program) ([A-Za-z0-9_]+_v\d_\d_\d\.py)", p)
            if m:
                if m.group(1) not in rec:
                    bad.append((idx, "names unrecorded program " + m.group(1)))
                else:
                    kinds.add(rec[m.group(1)]["kind"]); n_prog += 1
        if kinds & {"standin", "fixture"} and "stand-in for google" not in low:
            bad.append((idx, "shows a stand-in program but does not say 'Stand-in for Google'"))
        if "fixture" in kinds and "recorded fixture" not in low:
            bad.append((idx, "shows a fixture program but does not say 'recorded fixture'"))
        has = "NOT EXECUTED" in text
        if idx in ne and not has:
            bad.append((idx, "is listed as NOT EXECUTED but the slide does not say so"))
        if has and idx not in ne:
            bad.append((idx, "says NOT EXECUTED but is not listed in the plan"))
        if idx == 1 and "never reached" not in low:
            bad.append((idx, "the title slide does not say Google was never reached"))
    print("honesty_check %s: %d program(s) shown, %d slide(s) marked NOT EXECUTED; %d refusal(s)" % (__version__, n_prog, len(ne), len(bad)))
    for b in bad:
        print("  REFUSED slide %d: %s" % b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
