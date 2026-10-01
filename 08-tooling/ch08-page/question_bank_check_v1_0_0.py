"""Checker for question_bank_v1_0_0.json (SEN0414 chapter 8). Runs every item that has a program under Python 3.14.4 and compares
what it prints with the marked option; checks the shape of every item, that its concept exists on the page and that the four
options are distinct. Items without a program (Remember, Understand) are checked for shape only."""
import glob, json, os, subprocess, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); PY = "/tmp/claude-0/core/v314/bin/python"; errors = []
bank = json.load(open(os.path.join(HERE, "question_bank_v1_0_0.json"), encoding="utf-8"))
pd = sorted(glob.glob(os.path.join(HERE, "page_data_v*.json")), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])[-1]
ids = {n["id"] for n in json.load(open(pd, encoding="utf-8"))["nodes"]}
quiz_q = {i["q"].strip() for i in json.load(open(os.path.join(HERE, "quiz_v1_0_0.json"), encoding="utf-8"))["items"]}
ran = 0
for k, it in enumerate(bank):
    t = "item %d (%s)" % (k, it.get("concept"))
    if set(it) - {"concept", "level", "q", "code", "options", "answer", "why"} or not {"concept", "level", "q", "options", "answer", "why"} <= set(it): errors.append(t + ": keys"); continue
    if it["concept"] not in ids: errors.append(t + ": unknown concept")
    if it["level"] not in {"Remember", "Understand", "Apply", "Analyze"}: errors.append(t + ": level")
    o = it["options"]
    if not (isinstance(o, list) and len(o) == 4 and len(set(o)) == 4 and all(isinstance(x, str) and x.strip() and "\n" not in x for x in o)): errors.append(t + ": options"); continue
    if not (isinstance(it["answer"], int) and 0 <= it["answer"] < 4): errors.append(t + ": answer"); continue
    if it["q"].strip() in quiz_q: errors.append(t + ": duplicates a quiz item")
    if it.get("code"):
        r = subprocess.run([PY, "-c", it["code"]], capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL); ran += 1
        if r.returncode or r.stdout.strip() != o[it["answer"]]: errors.append("%s: real result %r != option %r" % (t, r.stdout.strip(), o[it["answer"]]))
print("items: %d; concepts: %d; programs run under 3.14.4: %d; answer positions %s" % (len(bank), len({i["concept"] for i in bank}), ran, dict(sorted(collections.Counter(i["answer"] for i in bank).items()))))
if errors:
    print("FAIL"); [print(" -", e) for e in errors]; sys.exit(1)
print("PASS")
