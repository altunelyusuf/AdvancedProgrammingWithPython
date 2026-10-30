#!/usr/bin/env python3
"""Structure and source checks of exam_design_v1_1_0 (json and md). New file over exam_design_check_v1_0_0.py, which stays unchanged.
The same assertions as v1.0.0 on the new design, plus: every item type maps onto a unit kind that exists in the SEN0401 sheet module (read from the module),
no item type needs free writing, the arithmetic is recomputed, the sheet modules still have the recorded SHA-256, the sheet layout of the design's own
specification builds, and the item validator's self-test is run. A check that cannot run FAILS (CANNOT_RUN is not a pass). Exit 0 only if every check passes."""
import ast, hashlib, json, os, re, subprocess, sys
sys.dont_write_bytecode = True
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SHEET_DIR = os.environ.get("SEN0401_EXAM_DIR", "/home/claude/sen0401/08-tooling/exam")
M0, M1 = "sen0401_exam_answersheet_v1_0_0.py", "sen0401_exam_answersheet_v1_1_0.py"
T17 = {"mcq","multi","judge","match","order","repair","blank","cloze","predict","program","short","write","ask","string","graph","object","sparql"}
fails = []
def ck(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + (" - " + info if info else ""))
    if not ok: fails.append(name)

jp = os.path.join(R, "04-assessment/exams/exam_design_v1_1_0.json"); mp = jp[:-5] + ".md"
ck("json and md exist", os.path.isfile(jp) and os.path.isfile(mp))
j = json.load(open(jp, encoding="utf-8")); md = open(mp, encoding="utf-8").read()
ck("top-level keys exactly (v1_0_0 keys plus owner_decisions and supersedes)", list(j) == ["decisions","item_types_kept","item_types_dropped","blueprint","page_budget","answer_sheet","grading","owner_decisions","supersedes"], str(list(j)))
ck("every decision has topic, decision, reason non-empty", all(set(d) == {"topic","decision","reason"} and all(d[k].strip() for k in d) for d in j["decisions"]), str(len(j["decisions"])))
ck("md states the decision count of the json", ("(%d decisions" % len(j["decisions"])) in md)
kept = [t["type"] for t in j["item_types_kept"]]; dropped = [t["type"] for t in j["item_types_dropped"]]
ck("types valid, with why", all(set(t) == {"type","why"} and t["why"].strip() and t["type"] in T17 for t in j["item_types_kept"] + j["item_types_dropped"]))
ck("kept + dropped = the 17 types, disjoint", set(kept) | set(dropped) == T17 and not set(kept) & set(dropped) and len(kept) + len(dropped) == 17)
ck("kept types are exactly mcq, match, order, blank, cloze, predict; short is dropped", set(kept) == {"mcq","match","order","blank","cloze","predict"} and "short" in dropped and "write" in dropped and "program" in dropped)

b = j["blueprint"]
ck("blueprint keys", set(b) == {"items","minutes","share_apply_or_above","letters","chapters","types","cross_chapter_items","bloom_levels","arithmetic"})
ck("minutes 60, share in (50,100]", b["minutes"] == 60 and 50 < b["share_apply_or_above"] <= 100)
ck("chapters sum to items, no chapter 5", sum(b["chapters"].values()) == b["items"] and "5" not in b["chapters"] and set(b["chapters"]) == {"1","2","3","4","6","7","8"})
ck("types sum to items, all kept", sum(b["types"].values()) == b["items"] and set(b["types"]) <= set(kept))
lv = b["letters"]; ck("letters differ by at most one", max(lv.values()) - min(lv.values()) <= 1 and set(lv) == set("ABCD"), str(lv))
ck("lettered items = mcq + predict (all predict by letter)", sum(lv.values()) == b["types"]["mcq"] + b["types"]["predict"])
ck("cross-chapter items between 1 and items", 1 <= b["cross_chapter_items"] <= b["items"])

ar = b["arithmetic"]; rows = ar["rows"]
ck("each row: seconds and points are consistent with items", all(r["items"] > 0 and r["seconds_each"] > 0 and r["points"] > 0 for r in rows))
ck("rows sum to the blueprint types", all(sum(r["items"] for r in rows if r["type"] == t) == n for t, n in b["types"].items()) and {r["type"] for r in rows} == set(b["types"]), str({t: sum(r["items"] for r in rows if r["type"] == t) for t in b["types"]}))
secs = sum(r["items"] * r["seconds_each"] for r in rows)
ck("summed answer time recomputed, <= 90 per cent of 60 minutes", secs == ar["total_seconds"] and secs <= 0.9 * b["minutes"] * 60 and ar["limit_seconds"] == 3240 and round(100.0 * secs / 3600, 1) == ar["time_share_percent"], "%d s of %d, %.1f per cent" % (secs, 3240, 100.0 * secs / 3600))
pts = sum(r["points"] for r in rows)
ck("points total 100, recomputed", pts == ar["total_points"] == 100, str(pts))
bl = b["bloom_levels"]; hi = sum(v for k, v in bl.items() if int(k) >= 3)
ck("Bloom levels sum to items; levels 3 to 6 above 50 per cent and equal to the stated share", sum(bl.values()) == b["items"] and set(bl) == set("123456") and hi == ar["apply_or_above_items"] and 100.0 * hi / b["items"] > 50 and round(100.0 * hi / b["items"]) == b["share_apply_or_above"], "%d of %d" % (hi, b["items"]))
an = sum(v for k, v in bl.items() if int(k) >= 4)
ck("Analyze-and-up figure is stated correctly", an == ar["analyze_or_above_items"] and round(100.0 * an / b["items"], 1) == ar["analyze_or_above_percent"], "%d of %d" % (an, b["items"]))
ck("total items and lettered items in the arithmetic", ar["total_items"] == sum(r["items"] for r in rows) == b["items"] and ar["lettered_items"] == sum(lv.values()))

# ---- the sheet module: unit kinds read from the module text, no import needed for this part
m0p, m1p = os.path.join(SHEET_DIR, M0), os.path.join(SHEET_DIR, M1)
have = os.path.isfile(m0p) and os.path.isfile(m1p)
ck("SEN0401 sheet and reader found (CANNOT_RUN would fail)", have, SHEET_DIR)
kinds = set()
if have:
    tree = ast.parse(open(m0p, encoding="utf-8").read())
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "BLOCK_MAX" for t in n.targets):
            kinds = set(ast.literal_eval(n.value))
a = j["answer_sheet"]
ck("answer_sheet keys", {"layout","mark_style","geometry","student_id_line","version_mark","reuse","unit_kinds","type_map","read_by_machine_answers","held_for_a_person","dropped_from_v1_0_0"} <= set(a) and all(str(a[k]).strip() for k in a))
ck("unit kinds in the design equal the kinds defined in the module", kinds == set(a["unit_kinds"]) and bool(kinds), "module: %s" % sorted(kinds))
tm = a["type_map"]
ck("every kept item type maps onto a unit kind that exists in the module", set(tm) == set(kept) and all(v["unit_kind"] in kinds for v in tm.values()), str({k: v["unit_kind"] for k, v in tm.items()}))
ck("no item type needs free writing (no type maps to the unit kind human)", all(v["unit_kind"] != "human" for v in tm.values()) and "human" in kinds)
ck("arithmetic unit kinds agree with the type map", all(r["unit_kind"] == tm[r["type"]]["unit_kind"] for r in rows))
fixed = {"mcq": 1, "predict": 1, "match": 5, "order": 4, "blank": 3}
ck("sheet units per row follow the type map", all(r["units"] == r["items"] * fixed[r["type"]] for r in rows if r["type"] in fixed) and next(r for r in rows if r["type"] == "cloze")["units"] == 5)
tu = sum(r["units"] for r in rows) + ar["form_unit"]["units"]
ck("total sheet units recomputed", tu == ar["total_units"], str(tu))
ru = a["reuse"]
ck("reuse record: two modules, SHA-256 recorded, vendoring and change rule stated", [m["file"] for m in ru["modules"]] == [M0, M1] and all(re.fullmatch(r"[0-9a-f]{64}", m["sha256"]) for m in ru["modules"]) and "byte-identical" in ru["how_obtained"] and ru["if_source_changes"].strip() != "")
if have:
    for m in ru["modules"]:
        d = hashlib.sha256(open(os.path.join(SHEET_DIR, m["file"]), "rb").read()).hexdigest()
        ck("source %s has the recorded SHA-256" % m["file"], d == m["sha256"], d)
# ---- the design's own sheet specification must build in the module's layout
def layout_pages():
    sys.path.insert(0, SHEET_DIR)
    import sen0401_exam_answersheet_v1_0_0 as A
    units = [{"no": "F", "kind": "bank", "digits": 2}]
    n = 0
    for t in ("mcq", "predict"):
        for _ in range(b["types"][t]): n += 1; units.append({"no": str(n), "kind": "choice", "opts": tm[t]["options"]})
    for t, gl in (("blank", [3, 3, 3]), ("cloze", [3, 2])):
        for g in gl:
            n += 1
            for c in "abc"[:g]: units.append({"no": "%d%s" % (n, c), "kind": "bank", "digits": 2})
    for t in ("match", "order"):
        for _ in range(b["types"][t]):
            n += 1
            for c in "abcde"[:fixed[t]]: units.append({"no": "%d%s" % (n, c), "kind": t, "opts": tm[t]["options"]})
    spec = {"paper_kind": "Midterm", "paper_version": 1, "form_code": A.make_code(1010, 4), "units": units}
    lay = A.build_layout(spec)
    placed = [u["no"] for bl_ in lay["blocks"] for u in bl_["units"]]
    return n, len(units), placed, lay["pages"], [u["no"] for u in units]
try:
    n, nu, placed, pages, want = layout_pages()
    ck("design specification builds in the module's layout: positions 1 to %d, all %d units placed once, pages = measured" % (n, nu), n == b["items"] and nu == ar["total_units"] and placed == want and pages == ar["sheet_pages_measured"], "%d units, %d pages" % (len(placed), pages))
except Exception as e:
    ck("design specification builds in the module's layout (CANNOT_RUN)", False, repr(e))

pb = j["page_budget"]; ck("page budget", set(pb) == {"pages_per_student","sheets_per_student","reasoning"} and pb["reasoning"].strip() and pb["sheets_per_student"]*2 >= pb["pages_per_student"] and pb["pages_per_student"] == ar["paper_pages_estimate"] + ar["sheet_pages_measured"] and -(-ar["paper_lines_estimate"] // ar["lines_per_page"]) <= ar["paper_pages_estimate"])
ck("answer_sheet geometry from the module", a["geometry"]["reading_dpi"] == 150 and a["geometry"]["bubble_radius_pt"] == 5.5 and a["geometry"]["pitch_pt"] == 19.0 and len(a["geometry"]["page_pt"]) == 2)
g = j["grading"]; ck("grading keys", set(g) == {"read_by_machine","read_by_hand","unreadable_rule","double_mark_rule","key_application","second_check"} and all(v.strip() for v in g.values()))
od = j["owner_decisions"]
ck("owner_decisions: every decided item has a reason and a date", set(od) == {"decided","open"} and od["decided"] and all(d["reason"].strip() and d["decision"].strip() and re.fullmatch(r"\d{4}-\d\d-\d\d", d["date"]) for d in od["decided"]))
qs = " | ".join(o["question"].lower() for o in od["open"])
ck("owner_decisions.open: items per paper, Bloom reading and chapter weights each asked, every question with assumption, default and effect", all(o["recommended_default"].strip() and o["if_answer_changes"].strip() and o["assumption"].strip() for o in od["open"]) and all(k in qs for k in ("items does one paper", "bloom", "chapter weights")))
sp = j["supersedes"]; ck("supersedes names v1_0_0 and the replaced sections", "exam_design_v1_0_0" in sp["file"] and {"section 7 (answer sheet and geometry)", "section 9 (reading, assessing, grading)"} <= set(sp["replaced"]))

# ---- cited sources exist
paths = set(re.findall(r"`([^`\s]+\.(?:json|ttl|py|html|js|md))`", md)); paths = {p for p in paths if "/" in p and "NN" not in p}
miss = []
for p in sorted(paths):
    q = p if os.path.isabs(p) else os.path.join(R, p)
    if not os.path.isfile(q) and not os.path.isabs(p): q = os.path.join(R, "08-tooling", p)
    if not os.path.isfile(q): miss.append(p)
ck("every cited source exists", not miss, "%d cited, missing %s" % (len(paths), miss))
# ---- the item validator
vr = subprocess.run([sys.executable, "-B", os.path.join(R, "04-assessment/exams/exam_item_check_v1_0_0.py"), "selftest"], capture_output=True, text=True)
ck("item validator self-test exits 0 and prints RESULT PASS", vr.returncode == 0 and "RESULT PASS" in vr.stdout and "MISMATCH" not in vr.stdout, vr.stdout.strip().splitlines()[-1] if vr.stdout.strip() else vr.stderr[-200:])
# ---- nothing committed was edited
st = subprocess.run(["git","-C",R,"status","--porcelain","--","03-materials"],capture_output=True,text=True).stdout.strip()
ck("nothing changed under 03-materials", st == "", st)
old = ["04-assessment/exams/exam_design_v1_0_0.md", "04-assessment/exams/exam_design_v1_0_0.json", "04-assessment/exams/exam_design_check_v1_0_0.py"]
df = subprocess.run(["git","-C",R,"status","--porcelain","--"] + old,capture_output=True,text=True).stdout.strip()
ck("v1_0_0 design files unchanged", df == "", df)
print("RESULT", "FAIL" if fails else "PASS", fails)
sys.exit(1 if fails else 0)
