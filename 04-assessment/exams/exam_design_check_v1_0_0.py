#!/usr/bin/env python3
"""Structure and source checks of exam_design_v1_0_0 (json and md). Exit 0 only if every check passes."""
import json, re, os, sys, subprocess
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
T17 = {"mcq","multi","judge","match","order","repair","blank","cloze","predict","program","short","write","ask","string","graph","object","sparql"}
SEC = {"mcq_plain":60,"mcq_code":100,"match":240,"order":120,"blank":60,"cloze":45,"predict":120,"short":240}
fails = []
def ck(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + (" - " + info if info else ""))
    if not ok: fails.append(name)
jp = os.path.join(R, "04-assessment/exams/exam_design_v1_0_0.json"); mp = jp[:-5] + ".md"
ck("json and md exist", os.path.isfile(jp) and os.path.isfile(mp))
j = json.load(open(jp)); md = open(mp).read()
ck("top-level keys exactly", list(j) == ["decisions","item_types_kept","item_types_dropped","blueprint","page_budget","answer_sheet","grading"], str(list(j)))
ck("every decision has topic, decision, reason non-empty", all(set(d) == {"topic","decision","reason"} and all(d[k].strip() for k in d) for d in j["decisions"]), str(len(j["decisions"])))
kept = [t["type"] for t in j["item_types_kept"]]; dropped = [t["type"] for t in j["item_types_dropped"]]
ck("types valid, with why", all(set(t) == {"type","why"} and t["why"].strip() and t["type"] in T17 for t in j["item_types_kept"] + j["item_types_dropped"]))
ck("kept + dropped = the 17 types, disjoint", set(kept) | set(dropped) == T17 and not set(kept) & set(dropped) and len(kept) + len(dropped) == 17)
b = j["blueprint"]
ck("blueprint keys", set(b) == {"items","minutes","share_apply_or_above","letters","chapters","types","cross_chapter_items"})
ck("minutes 60, share in (50,100]", b["minutes"] == 60 and 50 < b["share_apply_or_above"] <= 100)
ck("chapters sum to items, no chapter 5", sum(b["chapters"].values()) == b["items"] and "5" not in b["chapters"] and set(b["chapters"]) == {"1","2","3","4","6","7","8"})
ck("types sum to items, all kept", sum(b["types"].values()) == b["items"] and set(b["types"]) <= set(kept))
lv = b["letters"]; ck("letters differ by at most one", max(lv.values()) - min(lv.values()) <= 1 and set(lv) == set("ABCD"), str(lv))
ck("lettered items = mcq + 3 predict by letter", sum(lv.values()) == b["types"]["mcq"] + 3)
ck("cross-chapter items between 1 and items", 1 <= b["cross_chapter_items"] <= b["items"])
secs = 8*SEC["mcq_plain"] + 6*SEC["mcq_code"] + 2*SEC["match"] + 2*SEC["order"] + 3*SEC["blank"] + 2*SEC["cloze"] + 5*SEC["predict"] + 2*SEC["short"]
ck("summed answer time <= 90 per cent of 60 minutes", secs <= 0.9*3600 and 8 + 6 == b["types"]["mcq"], "%d s of %d" % (secs, 3240))
pts = 14*3 + 5*4 + 2*5 + 2*4 + 9 + 5 + 2*3
ck("points total 100", pts == 100, str(pts))
pb = j["page_budget"]; ck("page budget", set(pb) == {"pages_per_student","sheets_per_student","reasoning"} and pb["reasoning"].strip() and pb["sheets_per_student"]*2 >= pb["pages_per_student"])
a = j["answer_sheet"]; ck("answer_sheet keys", set(a) == {"layout","mark_style","geometry","student_id_line","version_mark"} and set(a["geometry"]) == {"markers","cell_mm","resolution_dpi"})
ck("geometry markers inside page and 4 of them", len(a["geometry"]["markers"]) == 4 and all(0 < m["centre_mm"][0] < 210 and 0 < m["centre_mm"][1] < 297 for m in a["geometry"]["markers"]))
ck("resolution at least 200", a["geometry"]["resolution_dpi"] >= 200)
g = j["grading"]; ck("grading keys", set(g) == {"read_by_machine","read_by_hand","unreadable_rule","double_mark_rule","key_application","second_check"} and all(v.strip() for v in g.values()))
paths = set(re.findall(r"`([^`\s]+\.(?:json|ttl|py|html|js|md))`", md)); paths = {p for p in paths if "/" in p and "NN" not in p}
paths |= {"03-materials/ch%02d/page/chapter_code_ch%02d_v1_0_0.json" % (n, n) for n in (1,2,3,4,6,7,8)}
miss = []
for p in sorted(paths):
    q = os.path.join(R, p.replace("`", ""))
    if not os.path.isfile(q): q = os.path.join(R, "08-tooling", p)
    if not os.path.isfile(q): miss.append(p)
ck("every cited source exists", not miss, "%d cited, missing %s" % (len(paths), miss))
st = subprocess.run(["git","-C",R,"status","--porcelain","--","03-materials"],capture_output=True,text=True).stdout.strip()
ck("nothing changed under 03-materials", st == "", st)
print("RESULT", "FAIL" if fails else "PASS", fails)
sys.exit(1 if fails else 0)
