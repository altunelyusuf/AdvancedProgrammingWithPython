#!/usr/bin/env python3
"""Chapter 25 honesty check. Windows, macOS, the free-threaded build of Python 3.13, a C extension that re-enables the GIL, more than 2 CPUs, the real xkcd.com and runs under load
were never executed; the downloader programs of the deck run against a local stand-in (an HTTP server of the program on 127.0.0.1) and never contact xkcd.com; every timing of the
research is a single recorded run that the deck does not measure again and is marked Recorded; what could not be run is marked NOT EXECUTED. A reader must be able to tell these
apart from the output of a program that ran as shown. From the finished .pptx, the recording (examples_out) and the plan's meta:
  1. every slide that shows a program (label 'program <name>, lines ...' or 'transcript of program <name>') whose recorded kind is 'standin' must carry,
     on that slide, each phrase of the program's recorded standkey ('127.0.0.1', 'xkcd.com is never contacted') and the words 'local stand-in'; every slide the plan lists under
     meta.standin must show such a program, and no slide that shows none may call itself a stand-in;
  2. every slide the plan lists under meta.notExecuted must carry the words 'NOT EXECUTED', and no other slide may;
  3. every slide the plan lists under meta.recorded (a measurement or a page reading of the research of 14 October 2026 that this deck does not run again) must carry the word
     'Recorded', and no other slide may;
  4. the title slide must say that every output was printed by the Python above and that Windows, macOS, more than 2 CPUs and the real xkcd.com were never used, and it
     must not say 'NOT EXECUTED' (it is not a slide of results);
  5. every picture a slide shows must be named by a caption 'image <file> made by <program>' that the recording knows (program_check compares the pixels) or by a caption
     'photo <file>: <credit>' for a photograph that photos_v1_0_0.json knows (program_check compares the file and the credit).
Usage: honesty_check_v1_0_0.py <deck.pptx> <examples_out.json> <deck_plan.json>   Exit 0 when nothing is refused."""
__version__ = "1.0.0"
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck_check_v1_0_0 import slides
IMG = re.compile(r"image ([A-Za-z0-9_]+\.png) made by ([A-Za-z0-9_.]+\.py)")
PHO = re.compile(r"^photo ([A-Za-z0-9_]+\.(?:png|jpg)): ")
CAP = re.compile(r"(?:transcript of program|program) ([A-Za-z0-9_]+_v\d_\d_\d\.py)")


def main(deck, rec_path, plan_path):
    full = json.load(open(rec_path)); rec = full["_programs"]; imgs = full["_images"]
    meta = json.load(open(plan_path))["meta"]
    photos = {x["file"] for x in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos_v1_0_0.json")))["photos"]}
    ne, rc, si = set(meta["notExecuted"]), set(meta["recorded"]), {int(k) for k in meta["standin"]}
    bad, n_prog, n_stand = [], 0, 0
    for idx, (name, paras) in enumerate(slides(deck), 1):
        text = "\n".join(paras)
        kinds, need = set(), set()
        for p in paras:
            m = CAP.search(p)
            if m:
                if m.group(1) not in rec:
                    bad.append((idx, "names unrecorded program " + m.group(1)))
                else:
                    kinds.add(rec[m.group(1)]["kind"]); n_prog += 1
                    need.update(rec[m.group(1)].get("standkey") or [])
        if "standin" in kinds:
            n_stand += 1
            miss = sorted(w for w in need if w not in text)
            if not need or miss:
                bad.append((idx, "shows a program that runs against a stand-in but does not say %s" % (miss or "which one")))
            if "local stand-in" not in text:
                bad.append((idx, "shows a program that runs against a stand-in but does not say 'local stand-in'"))
        if idx in si and "standin" not in kinds:
            bad.append((idx, "is listed as a stand-in slide but shows no program that runs against one"))
        if "standin" not in kinds and re.search(r"stand-in for|local stand-in", text, re.I) and idx not in (1,) and idx not in rc and idx not in ne:
            bad.append((idx, "calls something a stand-in but shows no program that runs against one"))
        for p in paras:
            for fn, pr in IMG.findall(p):
                if fn not in imgs or imgs[fn]["program"] != pr:
                    bad.append((idx, "names the picture %s of program %s, which the recording does not know" % (fn, pr)))
        for p in paras:
            m = PHO.match(p)
            if m and (m.group(1) not in photos or "Wikimedia Commons" not in p):
                bad.append((idx, "names the photograph %s, which photos_v1_0_0.json does not know or does not credit to Wikimedia Commons" % m.group(1)))
        has = "NOT EXECUTED" in text
        if idx in ne and not has:
            bad.append((idx, "is listed as NOT EXECUTED but the slide does not say so"))
        if has and idx not in ne:
            bad.append((idx, "says NOT EXECUTED but is not listed in the plan"))
        rec_w = re.search(r"\bRecorded\b", text) is not None
        if idx in rc and not rec_w:
            bad.append((idx, "is listed as Recorded but the slide does not say so"))
        if rec_w and idx not in rc:
            bad.append((idx, "says Recorded but is not listed in the plan"))
        if idx == 1:
            low = text.lower()
            if "printed by the python above" not in low:
                bad.append((idx, "the title slide does not say that every output was printed by the Python it shows"))
            if "never used" not in low:
                bad.append((idx, "the title slide does not say that Windows, macOS, more than 2 CPUs and the real xkcd.com were never used"))
            if "NOT EXECUTED" in text:
                bad.append((idx, "the title slide says NOT EXECUTED, which belongs to the slides of results"))
    print("honesty_check %s: %d program(s) shown, %d slide(s) with a stand-in program, %d slide(s) marked NOT EXECUTED, %d slide(s) Recorded; %d refusal(s)"
          % (__version__, n_prog, n_stand, len(ne), len(rc), len(bad)))
    for b in bad:
        print("  REFUSED slide %d: %s" % b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
