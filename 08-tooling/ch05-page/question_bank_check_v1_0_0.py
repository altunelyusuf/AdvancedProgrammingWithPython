"""Checker for question_bank_v1_0_0.json (SEN0414 chapter 5)."""
import json, os, subprocess, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
PY = "/tmp/claude-0/core/v314/bin/python"
LEVELS = {"Remember", "Understand", "Apply", "Analyze"}
NOOUT = "(no output)"
errors = []

def err(msg):
    errors.append(msg)

bank = json.load(open(os.path.join(HERE, "question_bank_v1_0_0.json"), encoding="utf-8"))
nodes = json.load(open(os.path.join(HERE, "page_data_v9_9_0.json"), encoding="utf-8"))["nodes"]
quiz = json.load(open(os.path.join(HERE, "quiz_v1_0_0.json"), encoding="utf-8"))["items"]
quiz_q = {i["q"].strip() for i in quiz}
ids = {n["id"] for n in nodes}
io_ids = {n["id"] for n in nodes if "io" in n}

if not isinstance(bank, list):
    err("bank is not a list"); bank = []

per = collections.defaultdict(list)
for k, it in enumerate(bank):
    tag = f"item {k} ({it.get('concept')})"
    if not isinstance(it, dict):
        err(f"{tag}: not an object"); continue
    allowed = {"concept", "level", "q", "code", "options", "answer", "why"}
    if set(it) - allowed: err(f"{tag}: extra keys {set(it) - allowed}")
    if not {"concept", "level", "q", "options", "answer", "why"} <= set(it):
        err(f"{tag}: missing keys"); continue
    if it["concept"] not in ids: err(f"{tag}: unknown concept")
    per[it["concept"]].append(it)
    if it["level"] not in LEVELS: err(f"{tag}: bad level")
    for f in ("q", "why"):
        if not isinstance(it[f], str) or not it[f].strip() or "\n" in it[f] or "\r" in it[f]:
            err(f"{tag}: {f} must be a non-empty single line")
    o = it["options"]
    if not (isinstance(o, list) and len(o) == 4 and all(isinstance(x, str) and x.strip() and "\n" not in x for x in o)):
        err(f"{tag}: options must be 4 single-line strings"); continue
    if len(set(o)) != 4: err(f"{tag}: options not distinct")
    if any("all of the above" in x.lower() for x in o): err(f"{tag}: 'all of the above'")
    if not (isinstance(it["answer"], int) and not isinstance(it["answer"], bool) and 0 <= it["answer"] < 4):
        err(f"{tag}: bad answer index"); continue
    if "code" in it and not isinstance(it["code"], str): err(f"{tag}: code not a string")
    if it["q"].strip() in quiz_q: err(f"{tag}: duplicates existing quiz item")

for nid in sorted(ids):
    if not per[nid]: err(f"concept {nid}: no item")
for nid in sorted(io_ids):
    if not any(i["level"] == "Apply" and i.get("code") for i in per[nid]):
        err(f"io concept {nid}: no Apply item with code")
    if len(per[nid]) < 2: err(f"io concept {nid}: fewer than 2 items")

# answer balance
cnt = collections.Counter(i["answer"] for i in bank if isinstance(i.get("answer"), int))
for p in range(4):
    share = cnt[p] / max(len(bank), 1)
    if not 0.20 <= share <= 0.30: err(f"answer index {p} share {share:.2%} outside 20-30%")

# run Apply code
ran = 0
for k, it in enumerate(bank):
    if it.get("level") != "Apply" or not it.get("code"):
        continue
    tag = f"item {k} ({it['concept']})"
    try:
        r = subprocess.run([PY, "-c", it["code"]], capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        err(f"{tag}: timeout"); continue
    ran += 1
    if r.returncode == 0:
        actual = r.stdout.strip() or NOOUT
    else:
        lines = [l for l in r.stderr.strip().splitlines() if l.strip()]
        actual = lines[-1].split(":")[0].strip() if lines else "?"
    exp = it["options"][it["answer"]]
    if actual != exp:
        err(f"{tag}: real result {actual!r} != option {exp!r}")

lv = collections.Counter(i.get("level") for i in bank)
print(f"items: {len(bank)}; concepts covered: {sum(1 for n in ids if per[n])}/{len(ids)}; io concepts: {len(io_ids)}")
print("levels:", dict(sorted(lv.items())))
print("answer positions:", {p: cnt[p] for p in range(4)})
print(f"apply programs run: {ran}")
if errors:
    print(f"FAIL: {len(errors)} problem(s)")
    for e in errors: print(" -", e)
    sys.exit(1)
print("PASS")
