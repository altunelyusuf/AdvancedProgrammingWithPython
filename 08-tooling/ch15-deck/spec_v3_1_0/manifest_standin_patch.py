"""Chapter 15, step after the generic builder: adds to the chapter-code manifest the three facts the generic builder does not write, the stand-in for Google (file, module, sha256) and its version under executed_with.
The generic builder writes `file: None` because the other chapters have no stand-in. Usage (from the repo root): python3 08-tooling/ch15-deck/spec_v3_1_0/manifest_standin_patch.py. Refuses to patch twice."""
import hashlib, json, sys
MAN = "03-materials/ch15/page/chapter_code_ch15_v1_2_0.json"
FILE = "03-materials/ch15/assets/google_standin_v1_0_0.py"
m = json.load(open(MAN, encoding="utf-8"))
if m["library"]["file"]:
    sys.exit("REFUSED: already patched")
m["library"]["file"] = FILE
m["library"]["module"] = "google_standin"
m["library"]["sha256"] = hashlib.sha256(open(FILE, "rb").read()).hexdigest()
m["executed_with"]["stand_in"] = "google_standin 1.0.0"
with open(MAN, "w", encoding="utf-8") as f:
    json.dump(m, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("patched", MAN, m["library"]["sha256"])
