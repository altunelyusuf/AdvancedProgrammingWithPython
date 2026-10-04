"""Re-runs every program a deck shows that is meant to fail, and requires the error message on the slide to be the
message Python prints now.

ch03-deck/program_check_v1_0_0.py compares what a program writes to its normal output; it says nothing about what a
program writes to its error output, and the chapters on flow control and on loops teach partly by showing exactly
that - an unassigned name, a program that stops itself. This check closes that gap: for every program recorded with
"mayfail", it re-runs the program with the inputs its run used and requires the last line of the error output, and the
exit status, to be what the recorded run had, and the last line to appear on one of the deck's slides.

Usage: program_fail_check_v1_0_0.py <deck.pptx> <examples_out.json> <python>. Exits 1 when a message has changed or is
not on a slide.
"""
__version__ = "1.0.0"
import html, json, os, re, subprocess, sys, tempfile, zipfile

deck, rec, PY = sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3]
z = zipfile.ZipFile(deck)
names = sorted([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)], key=lambda n: int(re.findall(r"\d+", n)[0]))
texts = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", z.read(n).decode()))) for n in names]
PRE = "import builtins\n_q = iter(%r)\ndef _input(prompt=''):\n    v = next(_q)\n    print(prompt + v)\n    return v\nbuiltins.input = _input\n"
bad, total = [], 0
for prog, r in rec["_programs"].items():
    if not r.get("mayfail"): continue
    for run in r["runs"]:
        total += 1
        if run["inputs"]:
            out = subprocess.run([PY, "-c", PRE % run["inputs"] + r["code"]], capture_output=True, text=True)
        else:                       # as examples_run_v2_1_0.py ran it: from a file named after the program
            d = tempfile.mkdtemp(); open(os.path.join(d, prog), "w").write(r["code"])
            out = subprocess.run([PY, prog], capture_output=True, text=True, cwd=d)
        err = [l for l in out.stderr.rstrip("\n").split("\n") if l.strip()]
        last = err[-1] if err else ""
        if out.returncode == 0: bad.append((prog, "exited cleanly, but is recorded as failing"))
        if last != run["errlast"]: bad.append((prog, "message changed: %r is now %r" % (run["errlast"], last)))
        want = re.sub(r"\s+", " ", last).strip()
        if want and not any(want in t for t in texts): bad.append((prog, "message not on any slide: %r" % want[:90]))
print("%d failing program run(s) re-executed; %d not matching the slides" % (total, len(bad)))
for b in bad: print("  REFUSED", b)
sys.exit(1 if bad else 0)
