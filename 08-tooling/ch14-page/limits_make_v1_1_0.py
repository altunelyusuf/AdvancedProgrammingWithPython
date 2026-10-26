"""Version 1.1.0 (over 1.0.0): reads interpreter_record_v1_1_0.json (with the Pyodide row) and says that the stored outputs of the examples were recorded in the page's own Python.
Writes limits_v1_1_0.json, the chapter 14 page's 'Provenance & known limits' entries, from the records Phase A made
(third_party_record_v1_0_0.json, live_observations_v1_0_0.json, interpreter_record_v1_0_0.json), pywheels_v1_0_0.json and the
'Not executed' paragraph of sen0414_ch14_rdodi_data_v1_0_2.py. Numbers and quoted values are read from those files.
Usage: limits_make_v1_1_0.py"""
__version__ = "1.1.0"
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
tp = json.load(open(os.path.join(H, "third_party_record_v1_0_0.json")))
lv = json.load(open(os.path.join(H, "live_observations_v1_0_0.json")))
ir = json.load(open(os.path.join(H, "interpreter_record_v1_1_0.json")))
pw = json.load(open(os.path.join(H, "pywheels_v1_0_0.json")))
src = open(os.path.join(H, "..", "sen0414_ch14_rdodi_data_v1_0_2.py"), encoding="utf-8").read()
live = {i["what"]: i["saw"] for i in lv["items"]}
find = lambda start: next(v for k, v in live.items() if k.startswith(start))
out = []
out.append("The live observations of this page are single requests made on %s through the build machine's proxy with %s, plus runs of the chapter's projects on the real files of the online materials; web sites change and nothing re-checks them." % (lv["observed"], lv["with"]))
pyp = find("openpyxl on PyPI")
out.append("openpyxl's newest stable release on PyPI on %s was %s, uploaded %s (Requires-Python %s, licence %s); its documentation front page names %s, generated %s. The page's examples were recorded under openpyxl %s." % (lv["observed"], pyp[0], pyp[2], pyp[3], pyp[4], find("openpyxl's stable documentation")[0], find("openpyxl's stable documentation")[1], pyp[0]))
f, = [r for r in ir["rows"]][:1]
out.append("One openpyxl program printed the same under each of the seven 3.14 releases, 3.13, 3.12 and the page's own runtime, Pyodide 0.28.2 (CPython 3.13.2) (the releases recorded %s with each interpreter installed by uv, every warning an error; bodies equal: %s)." % (re.search(r"Run on (\d{4}-\d{2}-\d{2})", ir["_note"]).group(1), ir["all_bodies_equal"]))
out.append("The programs that need openpyxl were run on the build machine under %s (%d recorded runs in third_party_record_v1_0_0.json) with workbooks built in a temporary folder." % (tp["python"], len(tp["items"])))
ws = ", ".join("%s %s (sha256 %s...)" % (w["file"].split("-")[0], w["file"].split("-")[1], w["sha256"][:12]) for w in pw["wheels"])
out.append("The page's in-browser Python is Pyodide's CPython 3.13, whose package list has no openpyxl, so the page carries %d wheels of its own, downloaded from PyPI and checked by SHA-256 (%s; both MIT licence; et_xmlfile also ships the Python licence for code derived from the standard library), and installs them into the browser Python when it starts; the comparison of every example's output with the stored output, recorded in that same Python (Pyodide 0.28.2, CPython 3.13.2), are part of the page test." % (len(pw["wheels"]), ws))
out.append("Every stored input-output example of the chapter was re-run in the page's own browser Python (Pyodide, CPython 3.13) by the page test and compared with the value recorded in that same Python (Pyodide 0.28.2, CPython 3.13.2, with the page's two wheels); two stored values differ from those a Python 3.14.6 run gave: Cached value loss gives (500, None), because the 3.13 library writes the empty value element in the form the example's replacement expects, and Hiding rows columns shows the column element with a space before the closing slash; the one example that started a second interpreter with subprocess (import census2010) cannot run in a browser, so research version 1.0.2 changed it to import in the same process and the starting of a real interpreter stays recorded in the document's executed behaviours.")
m = re.search(r"Not executed, and said so where it comes up: (.*?)\.\s+A\s+claim\s+not\s+in\s+this\s+file\s+was\s+not\s+made", src, re.S)
t = re.sub(r"\s+", " ", m.group(1)).strip()
t2 = t.replace("the in-browser Python (Pyodide) re-run of the stored examples, ", "")
assert t2 != t
out.append("Not executed in the build environment: " + t2 + ".")
json.dump({"_version": __version__, "limits": out}, open(os.path.join(H, "limits_v1_1_0.json"), "w"), indent=1, ensure_ascii=False)
for x in out: print("-", x)
