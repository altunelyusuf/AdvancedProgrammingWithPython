#!/usr/bin/env python3
"""Compares the stories of the given chapters with the stories of the chapters before them, by shared link, by shared names of people or bodies and by word overlap (Jaccard of the significant words of title, who, when and story).
A shared link is a repeat candidate; a shared name or a word overlap of 0.25 or more is listed to be read by a person. A lower bound only: it cannot know a story told in other words from another source.
Usage: sen0414_story_repeat_check_v1_0_0.py FIRST LAST     (reads the newest sen0414_chNN_stories_v*.py of chapters 1..LAST, from this folder)  Exit 0 when no repeat candidate by link and no overlap >= 0.25."""
__version__ = "1.0.0"
import glob, importlib.util, os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) != 3: sys.exit(__doc__)
A, Z = int(sys.argv[1]), int(sys.argv[2])
def newest(n):
    fs = set(glob.glob(os.path.join(H, "sen0414_ch%02d_stories_v*.py" % n)) + glob.glob(os.path.join(H, "sen0414_ch%d_stories_v*.py" % n)))
    return sorted(fs, key=lambda f: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", f)[0]])[-1]
def load(f):
    sp = importlib.util.spec_from_file_location("m", f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
S = {n: load(newest(n)).STORIES for n in range(1, Z + 1)}
stop = set("the a of and in to is was for on with as by at that this it from or an are be which his her their its had has have not but they were been who when".split())
toks = lambda s: {w for w in re.findall(r"[a-z0-9']{4,}", (s["title"] + " " + s["who"] + " " + s["when"] + " " + s["story"]).lower()) if w not in stop}
names = lambda s: set(re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", s["who"]))
bad = 0
for n in range(A, Z + 1):
    for s in S[n]:
        best = (0, None)
        for m in range(1, n):
            for o in S[m]:
                if o["link"] == s["link"]:
                    print("REPEAT CANDIDATE (same link) ch%d %s = ch%d %s %s" % (n, s["id"], m, o["id"], s["link"])); bad += 1
                sn = names(s) & names(o)
                if sn: print("shared name ch%d %s ~ ch%d %s: %s" % (n, s["id"], m, o["id"], sorted(sn)))
                a, b = toks(s), toks(o); j = len(a & b) / len(a | b)
                if j > best[0]: best = (j, "ch%d %s" % (m, o["id"]))
        print("ch%d %-24s best overlap %.3f with %s" % (n, s["id"], best[0], best[1]))
        if best[0] >= 0.25: bad += 1
print("RESULT %s" % ("CLEAN" if not bad else "%d to read" % bad)); sys.exit(1 if bad else 0)
