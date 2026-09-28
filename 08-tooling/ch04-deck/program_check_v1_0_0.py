"""Re-runs each whole program a deck shows, with the inputs its run shows, and requires the slide's transcript to match
what Python prints now. Handles programs with several inputs, or none, by replacing input() with a function that echoes
prompt and typed value, as examples_run_v1_0_0.py does. The transcript must appear on the deck as one sequence
(prompt, typed value, result, in order), because a result's words also occur inside the program's own code.
Usage: program_check_v1_0_0.py <deck.pptx> <examples_out.json> <python>. Exits 1 when a transcript does not match."""
__version__ = "1.0.0"
import html, json, re, subprocess, sys, zipfile
deck, rec, PY = sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3]
z = zipfile.ZipFile(deck)
def slide_text(n): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", z.read(n).decode())))
names = sorted([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)], key=lambda n: int(re.findall(r"\d+", n)[0]))
texts = [(n, slide_text(n)) for n in names]
PRE = "import builtins\n_q = iter(%r)\ndef _input(prompt=''):\n    v = next(_q)\n    print(prompt + v)\n    return v\nbuiltins.input = _input\n"
bad = []; total = 0
for prog, r in rec["_programs"].items():
    for run in r["runs"]:
        total += 1
        out = subprocess.run([PY, "-c", PRE % run["inputs"] + r["code"]], capture_output=True, text=True).stdout.rstrip("\n")
        want = re.sub(r"\s+", " ", out).strip()
        # the transcript must appear on a single slide, in order
        if not any(want in t for _, t in texts): bad.append((prog, run["inputs"], want[:80]))
        # and the program's code must appear on a slide too
        code = re.sub(r"\s+", " ", r["code"]).strip()
        if not any(code in t for _, t in texts): bad.append((prog, "code not on any slide", code[:60]))
print("%d program runs re-executed; %d not matching the slides" % (total, len(bad)))
for b in bad: print("  REFUSED", b)
sys.exit(1 if bad else 0)
