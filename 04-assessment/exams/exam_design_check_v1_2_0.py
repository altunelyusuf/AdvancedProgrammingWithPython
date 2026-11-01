#!/usr/bin/env python3
"""Checks of exam_design_v1_2_0 (json and md): the five-question paper. New file over exam_design_check_v1_1_0.py, which stays unchanged.
Everything stated as a sum is recomputed from the sub-question table; the SEN0401 sheet module is read and the design's 31 units are built in its
layout; the abbreviation scan (rule N3) is tested on fixtures of known answer; a check that cannot run FAILS (CANNOT_RUN is not a pass).
Exit 0 only if every check passes."""
import ast, hashlib, json, os, re, shutil, subprocess, sys
sys.dont_write_bytecode = True
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SHEET_DIR = os.environ.get("SEN0401_EXAM_DIR", "/home/claude/sen0401/08-tooling/exam")
M0, M1 = "sen0401_exam_answersheet_v1_0_0.py", "sen0401_exam_answersheet_v1_1_0.py"
T17 = {"mcq","multi","judge","match","order","repair","blank","cloze","predict","program","short","write","ask","string","graph","object","sparql"}
FORMATS = {"Q1": {"predict","mcq"}, "Q2": {"blank","cloze"}, "Q3": {"match","mcq"}, "Q4": {"order","mcq"}, "Q5": {"mcq"}}
fails = []
def ck(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + (" - " + info if info else ""))
    if not ok: fails.append(name)

# ---- rule N3: abbreviation scan (a library function, tested on fixtures below)
def abbreviation_scan(text, registry, exceptions=()):
    """text in print order; registry {short: full}. Returns the list of short forms used before (or without) their expansion 'full (SHORT)'."""
    bad = []
    seen = set()
    for m in re.finditer(r"\b[A-Z]{2,}\b", text):
        s = m.group(0)
        if s in exceptions or s in seen: continue
        seen.add(s)
        full = registry.get(s)
        pre = text[:m.start()].rstrip()
        # allowed first occurrence: directly inside the expansion "full form (SHORT)"
        if full is None: bad.append(s); continue
        if not (text[max(0, m.start() - len(full) - 2):m.start()].lower() == (full + " (").lower()): bad.append(s)
    return bad
REG = {"IDE": "integrated development environment", "CSV": "comma-separated values"}
ABBR_FIXTURES = [
    ("good: expanded at first use", "Open the integrated development environment (IDE) and then run the IDE again.", [], ),
    ("bad: bare at first use", "Open the IDE and then run it.", ["IDE"]),
    ("bad: expansion comes after the first use", "Use the IDE, that is the integrated development environment (IDE).", ["IDE"]),
    ("bad: short form not in the registry", "Read the XML file.", ["XML"]),
    ("good: two short forms, both expanded", "A comma-separated values (CSV) file opens in an integrated development environment (IDE).", []),
    ("good: option letter and form mark are exceptions", "Choose A, B or the form mark FM.", []),
]

jp = os.path.join(R, "04-assessment/exams/exam_design_v1_2_0.json"); mp = jp[:-5] + ".md"
ck("json and md exist", os.path.isfile(jp) and os.path.isfile(mp))
j = json.load(open(jp, encoding="utf-8")); md = open(mp, encoding="utf-8").read()
ck("top-level keys exactly", list(j) == ["decisions","item_types_kept","item_types_dropped","cover","questions","sub_questions","item_fields","abbreviation_rule","blueprint","page_budget","answer_sheet","key","outputs","grading","owner_decisions","supersedes"], str(list(j)))
ck("every decision has topic, decision, reason non-empty", all(set(d) == {"topic","decision","reason"} and all(d[k].strip() for k in d) for d in j["decisions"]), str(len(j["decisions"])))
ck("md states the decision count of the json", ("(%d decisions" % len(j["decisions"])) in md)
kept = [t["type"] for t in j["item_types_kept"]]; dropped = [t["type"] for t in j["item_types_dropped"]]
ck("kept + dropped = the 17 types, disjoint; kept are the six", set(kept) | set(dropped) == T17 and not set(kept) & set(dropped) and set(kept) == {"mcq","match","order","blank","cloze","predict"})

# ---- the five questions and the sub-question table, recomputed
subs = j["sub_questions"]; qs = j["questions"]; b = j["blueprint"]; ar = b["arithmetic"]
ck("five questions Q1 to Q5; Q1 to Q4 25 points, Q5 10 points and the only bonus", [q["question"] for q in qs] == ["Q1","Q2","Q3","Q4","Q5"] and [q["points"] for q in qs] == [25,25,25,25,10] and [q["bonus"] for q in qs] == [False]*4 + [True])
cnt = {q["question"]: sum(1 for x in subs if x["question"] == q["question"]) for q in qs}
ck("sub-questions 6, 7, 7, 6, 4 = 30", [cnt[q] for q in cnt] == [6,7,7,6,4] and len(subs) == 30 == b["items"], str(cnt))
ck("sub-question ids unique; sub letters a, b, c ... in order without gaps within each question", len({x["id"] for x in subs}) == 30 and all([x["sub"] for x in subs if x["question"] == q] == list("abcdefg"[:cnt[q]]) for q in cnt) and all(x["id"] == x["question"] + x["sub"] for x in subs))
ck("points are whole numbers >= 1 and add to 25, 25, 25, 25, 10 per question", all(isinstance(x["points"], int) and x["points"] >= 1 for x in subs) and [sum(x["points"] for x in subs if x["question"] == q["question"]) for q in qs] == [25,25,25,25,10], str({q["question"]: sum(x["points"] for x in subs if x["question"] == q["question"]) for q in qs}))
ck("every sub-question type is allowed in the format of its question and is a kept type", all(x["type"] in FORMATS[x["question"]] and x["type"] in kept for x in subs))
ck("every question lists exactly its sub-questions, points per sub and types", all(q["sub_ids"] == [x["id"] for x in subs if x["question"] == q["question"]] and q["points_per_sub"] == [x["points"] for x in subs if x["question"] == q["question"]] and set(q["types"]) == FORMATS[q["question"]] for q in qs))
ck("N4: every sub-question asks use, reason or effect; counts stated", all(x["asks"] in ("use","reason","effect") for x in subs) and b["asks"] == {a: sum(1 for x in subs if x["asks"] == a) for a in ("use","reason","effect")}, str(b["asks"]))
ck("N1: no sub-question at Bloom level 1 (Remember)", all(x["bloom"] >= 2 for x in subs) and b["bloom_levels"]["1"] == 0)
bl = {str(k): sum(1 for x in subs if x["bloom"] == k) for k in range(1, 7)}
ck("Bloom counts recomputed and stated", bl == b["bloom_levels"] and sum(bl.values()) == 30, str(bl))
ap = sum(1 for x in subs if x["bloom"] >= 3); an = sum(1 for x in subs if x["bloom"] >= 4)
ck("Bloom rule by count: majority at Apply and above; at least 8 of 30 at Analyze and above", ap > 15 and an >= 8 and ap == ar["apply_or_above_items"] and an == ar["analyze_or_above_items"], "Apply+ %d, Analyze+ %d" % (ap, an))
base = [x for x in subs if x["question"] != "Q5"]
app = sum(x["points"] for x in base if x["bloom"] >= 3); anp = sum(x["points"] for x in base if x["bloom"] >= 4)
ck("Bloom rule by points: at least half of the 100 base points at Apply and above", sum(x["points"] for x in base) == 100 and app >= 50 and app == ar["apply_or_above_points_of_100"] and anp == ar["analyze_or_above_points_of_100"], "Apply+ %d, Analyze+ %d of 100" % (app, anp))
ck("base points 100 and bonus 10 stated and recomputed", ar["base_points"] == 100 == b["base_points"] and ar["bonus_points"] == 10 == b["bonus_points"])
# chapters
ch = b["chapters"]; mat = b["chapter_matrix"]
ck("chapters 1 to 8 with chapter 5 in; weights sum to 30", set(ch) == set("12345678") and sum(ch.values()) == 30 and ch["5"] >= 1)
rec = {c: sum(1 for x in subs if x["chapter"] == int(c)) for c in ch}
ck("chapter weights equal the recount of the sub-question table, and the matrix agrees", rec == ch and all(mat[q][c] == sum(1 for x in subs if x["question"] == q and x["chapter"] == int(c)) for q in mat for c in ch), str(rec))
ck("cross-chapter >= 9 and indirect >= 6, recomputed", sum(1 for x in subs if x["cross_chapter"]) == b["cross_chapter_items"] >= 9 and sum(1 for x in subs if x["indirect"]) == b["indirect_items"] >= 6, "%d and %d" % (b["cross_chapter_items"], b["indirect_items"]))
# types and letters
tc = {}
for x in subs: tc[x["type"]] = tc.get(x["type"], 0) + 1
ck("types count recomputed", tc == b["types"], str(tc))
lv = b["letters"]; nch = sum(1 for x in subs if x["unit_kind"] == "choice")
ck("letters differ by at most one and cover the choice sub-questions", set(lv) == set("ABCD") and max(lv.values()) - min(lv.values()) <= 1 and sum(lv.values()) == nch == tc["mcq"] + tc["predict"], str(lv))
# time
RATE = ar["rates_seconds"]
ck("seconds of every sub-question follow the rate of its time class", all(x["seconds"] == RATE[x["time_class"]] for x in subs))
al = ar["allowances_seconds"]
units = len(subs) + 1
total = sum(x["seconds"] for x in subs) + al["tip_reading_per_sub"] * 30 + al["shared_stem_per_question"] * 5 + al["cover_and_instructions"] + al["sheet_filling_per_unit"] * units
ck("summed time recomputed, <= 90 per cent of 60 minutes (3240 s)", total == ar["total_seconds"] and total <= 0.9 * b["minutes"] * 60 and ar["limit_seconds"] == 3240 and round(100.0 * total / 3600, 1) == ar["time_share_percent"], "%d s of 3240, %.1f per cent of 3600" % (total, 100.0 * total / 3600))
ck("the rates are those of v1_1_0 (plain 60, with code 100, predict 120; 240/5, 120/4, 90/3, 120/5)", RATE == {"mcq_plain":60,"mcq_code":100,"predict":120,"match_premise":240//5,"order_step":120//4,"blank_gap":90//3,"cloze_gap":120//5})

# ---- sheet module
m0p, m1p = os.path.join(SHEET_DIR, M0), os.path.join(SHEET_DIR, M1)
have = os.path.isfile(m0p) and os.path.isfile(m1p)
ck("SEN0401 sheet and reader found (CANNOT_RUN would fail)", have, SHEET_DIR)
kinds = set()
if have:
    tree = ast.parse(open(m0p, encoding="utf-8").read())
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "BLOCK_MAX" for t in n.targets): kinds = set(ast.literal_eval(n.value))
a = j["answer_sheet"]
ck("unit kinds in the design equal the kinds defined in the module", kinds == set(a["unit_kinds"]) and bool(kinds), "module: %s" % sorted(kinds))
tm = a["type_map"]
ck("every kept type maps onto a unit kind that exists; none maps to human; sub-question unit kinds follow the map", set(tm) == set(kept) and all(v["unit_kind"] in kinds and v["unit_kind"] != "human" for v in tm.values()) and all(x["unit_kind"] == tm[x["type"]]["unit_kind"] for x in subs))
uk = {}
for x in subs: uk[x["unit_kind"]] = uk.get(x["unit_kind"], 0) + 1
uk["bank"] = uk.get("bank", 0) + 1
ck("units: one per sub-question plus F = 31, by kind recomputed", units == ar["total_units"] == 31 and uk == ar["units_by_kind"] and len(a["units"]) == 31 and a["units"][0]["no"] == "F", str(uk))
ru = a["reuse"]
ck("reuse record: two modules with SHA-256, vendoring and change rule stated", [m["file"] for m in ru["modules"]] == [M0, M1] and all(re.fullmatch(r"[0-9a-f]{64}", m["sha256"]) for m in ru["modules"]) and "byte-identical" in ru["how_obtained"] and ru["if_source_changes"].strip() != "")
if have:
    for m in ru["modules"]:
        d = hashlib.sha256(open(os.path.join(SHEET_DIR, m["file"]), "rb").read()).hexdigest()
        ck("source %s has the recorded SHA-256" % m["file"], d == m["sha256"], d)
def layout_pages():
    sys.path.insert(0, SHEET_DIR)
    import sen0401_exam_answersheet_v1_0_0 as A
    us = []
    for u in a["units"]:
        if u["no"] == "F": us.append({"no": "F", "kind": "bank", "digits": 2}); continue
        if u["kind"] == "bank": us.append({"no": u["no"], "kind": "bank", "digits": 2})
        else: us.append({"no": u["no"], "kind": u["kind"], "opts": u["opts"]})
    lay = A.build_layout({"paper_kind": "Midterm", "paper_version": 1, "form_code": A.make_code(1010, 4), "units": us})
    placed = [u["no"] for bl_ in lay["blocks"] for u in bl_["units"]]
    return placed, lay["pages"], [u["no"] for u in us], len(lay["blocks"])
try:
    placed, pages, want, nblocks = layout_pages()
    ck("the 31 units build in the module's layout: all placed once, in paper order, pages = measured", placed == want and len(placed) == 31 and pages == a["sheet_pages_measured"] == ar["sheet_pages_measured"], "%d units, %d blocks, %d page(s)" % (len(placed), nblocks, pages))
except Exception as e:
    ck("the 31 units build in the module's layout (CANNOT_RUN)", False, repr(e))
ck("sheet unit numbers follow the sub-question ids (question digit and letter)", [u["no"] for u in a["units"][1:]] == [x["id"][1:] for x in subs])

# ---- page budget, recomputed
pb = j["page_budget"]
ls = sum(r["lines"] for r in pb["estimate_rows"])
qp = -(-ls // pb["lines_per_page_relaxed"])
ck("page budget: lines summed, question pages = ceil(lines / lines per page), total = cover + question pages + sheet pages = 6 (3 sheets)", ls == pb["lines_estimate"] == ar["paper_lines_estimate"] and qp == pb["question_pages_estimate"] and pb["pages_total"] == pb["cover_pages"] + qp + pb["sheet_pages_measured"] == 6 and pb["sheets_per_student"] * 2 >= pb["pages_total"], "%d lines, %d question pages, %d in all" % (ls, qp, pb["pages_total"]))
ck("four pages in total is shown impossible: 2 question pages hold fewer lines than needed even at the densest 112 lines", pb["four_pages_possible"] is False and 2 * pb["lines_per_page_dense_v1_1_0"] < ls, "%d < %d" % (2 * pb["lines_per_page_dense_v1_1_0"], ls))
ck("levers named in order, the type size is not a lever, the measure names its tool and its NOT_MEASURED part", [l["order"] for l in pb["levers"]] == [1,2,3] and "10 point" in pb["never_levers"] and "soffice" in pb["measure"]["tool"] and "pdfinfo" in pb["measure"]["tool"] and "NOT_MEASURED" in pb["measure"]["not_measured"])
tools = {t: shutil.which(t) for t in ("soffice", "pdfinfo", "pdftotext")}
ck("the measuring tools named in the design exist in this environment (the engine can run them)", all(tools.values()), str({k: bool(v) for k, v in tools.items()}))
try:
    import docx  # noqa
    ck("python-docx is importable for the .docx outputs", True)
except Exception as e:
    ck("python-docx is importable for the .docx outputs", False, repr(e))

# ---- new item fields, abbreviations
nf = [f["field"] for f in j["item_fields"]["new"]]
ck("new item fields are question, sub, tip, terms, asks", nf == ["question","sub","tip","terms","asks"])
ar_rule = j["abbreviation_rule"]
ck("abbreviation rule states registry, scan and an example in full form", all(ar_rule[k].strip() for k in ("registry","scan","example")) and "integrated development environment (IDE)" == ar_rule["example"])
okfx = True
for name, text, want_bad in ABBR_FIXTURES:
    got = abbreviation_scan(text, REG, exceptions={"A", "B", "FM"})
    ok = got == want_bad; okfx &= ok
    print("  fixture %-52s expected %-8s actual %-8s %s" % (name, want_bad, got, "ok" if ok else "MISMATCH"))
ck("abbreviation scan: all %d fixtures of known answer as expected" % len(ABBR_FIXTURES), okfx)
ck("cover: at least ten fields filled, inputs not guessed (year, term, date, time), no template .docx in the exams folder", len(j["cover"]["fields_filled"]) >= 10 and set(j["cover"]["inputs_not_decided_here"]) == {"academic year","term","date","time"} and not any(f.endswith(".docx") and "template" in f for f in os.listdir(os.path.join(R, "04-assessment/exams"))))

# ---- owner decisions, assumptions, gap
od = j["owner_decisions"]
ck("owner_decisions keys; decided items have date and reason; every assumption has an effect; every open question has a default and an effect", set(od) == {"decided","assumptions","open","open_gaps"} and all(re.fullmatch(r"\d{4}-\d\d-\d\d", d["date"]) and d["reason"].strip() for d in od["decided"]) and all(x["assumption"].strip() and x["if_other"].strip() for x in od["assumptions"]) and all(x["recommended_default"].strip() and x["if_answer_changes"].strip() for x in od["open"]))
ck("every assumption id A1.. in the json appears in the md", all(x["id"] in md for x in od["assumptions"]) and len(od["assumptions"]) >= 10)
cp5 = [f for f in os.listdir(os.path.join(R, "04-assessment/exams")) if f.startswith("critical_points_ch05")]
ck("chapter 5 critical-points gap is recorded while no such file exists", bool(cp5) or any("chapter 5" in g["gap"] for g in od["open_gaps"]), "files: %s" % cp5)
for k in ("key","outputs","grading","supersedes","cover"): ck("section %s present and non-empty" % k, bool(j[k]))
ck("supersedes names v1_1_0 and the replaced sections", "exam_design_v1_1_0" in j["supersedes"]["file"] and len(j["supersedes"]["replaced"]) >= 4)

# ---- cited sources exist
paths = set(re.findall(r"`([^`\s]+\.(?:json|ttl|py|html|js|md))`", md)); paths = {p for p in paths if "/" in p}
miss = [p for p in sorted(paths) if not os.path.isfile(p if os.path.isabs(p) else os.path.join(R, p))]
ck("every cited source exists", not miss, "%d cited, missing %s" % (len(paths), miss))
vr = subprocess.run([sys.executable, "-B", os.path.join(R, "04-assessment/exams/exam_item_check_v1_0_0.py"), "selftest"], capture_output=True, text=True)
ck("item validator v1_0_0 self-test still exits 0 and prints RESULT PASS", vr.returncode == 0 and "RESULT PASS" in vr.stdout and "MISMATCH" not in vr.stdout, vr.stdout.strip().splitlines()[-1] if vr.stdout.strip() else vr.stderr[-200:])
st = subprocess.run(["git","-C",R,"status","--porcelain","--","03-materials"],capture_output=True,text=True).stdout.strip()
ck("nothing changed under 03-materials", st == "", st)
old = ["04-assessment/exams/exam_design_v1_0_0.md","04-assessment/exams/exam_design_v1_0_0.json","04-assessment/exams/exam_design_check_v1_0_0.py","04-assessment/exams/exam_design_v1_1_0.md","04-assessment/exams/exam_design_v1_1_0.json","04-assessment/exams/exam_design_check_v1_1_0.py"]
df = subprocess.run(["git","-C",R,"status","--porcelain","--"] + old,capture_output=True,text=True).stdout.strip()
ck("v1_0_0 and v1_1_0 design and check files unchanged", df == "", df)
print("RESULT", "FAIL" if fails else "PASS", fails)
sys.exit(1 if fails else 0)
