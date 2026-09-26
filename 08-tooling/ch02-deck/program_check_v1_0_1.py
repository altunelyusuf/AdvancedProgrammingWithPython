"""Re-runs each whole program shown on a deck with the inputs its slide shows, and requires the slide's
transcript to match what Python prints now. Complements deck_check_v1_0_1.py, which covers '>>>' lines."""
__version__ = "1.0.1"
import json, subprocess, sys, zipfile, re
deck, rec = sys.argv[1], json.load(open(sys.argv[2]))
z = zipfile.ZipFile(deck); text = " ".join(re.sub(r"<[^>]+>", " ", z.read(n).decode()) for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n))
text = re.sub(r"\s+", " ", text); bad = []
for prog, r in rec["_programs"].items():
    for inp, _ in r["runs"]:
        out = subprocess.run([sys.executable, "-c", r["code"]], input=inp + "\n", capture_output=True, text=True).stdout.strip()
        prompt, res = out.split(": ", 1)
        # the transcript must appear as one sequence - prompt, typed input, result - not merely somewhere,
        # because a result's words also occur inside the program's own code on the slide
        if re.sub(r"\s+", " ", "%s: %s %s" % (prompt, inp, res)) not in text: bad.append((prog, inp, res))
print("%d program runs re-executed; %d not matching the slides" % (sum(len(r["runs"]) for r in rec["_programs"].values()), len(bad)))
for b in bad: print("  REFUSED", b)
sys.exit(1 if bad else 0)
