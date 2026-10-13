"""Writes limits_v1_0_0.json, the chapter 18 page's 'Provenance & known limits' entries, from the records Phase A made
(live_observations_v1_0_0.json, interpreter_record_v1_0_0.json, third_party_record_v1_0_0.json), pywheels_v1_0_0.json, standin_v1_0_0.json and the
'Not executed' sentence of sen0414_ch18_rdodi_data_v1_0_2.py. Numbers are read from those files. Usage: limits_make_v1_0_0.py"""
__version__ = "1.0.0"
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(H, n)))
lv, ir, pw, so, tp = J("live_observations_v1_0_0.json"), J("interpreter_record_v1_0_0.json"), J("pywheels_v1_0_0.json"), J("standin_v1_0_0.json"), J("third_party_record_v1_0_0.json")
src = open(os.path.join(H, "..", "sen0414_ch18_rdodi_data_v1_0_2.py"), encoding="utf-8").read()
live = {i["what"]: i["saw"] for i in lv["items"]}
find = lambda start: next(v for k, v in live.items() if k.startswith(start))
m = re.search(r"Not executed, and said so where it comes up: (.*?)\.\s+The chapter's 97 interactive statements", src, re.S)
notexec = re.sub(r"\s+", " ", m.group(1)).strip()
pg = find("chapter 18 page: status"); mat = find("online materials of the 3rd edition: status")
pypi = find("PyPI: newest release of each package")
meas = {}
for i in tp["items"]:
    for l in i["output"].split("\n"):
        if l.startswith("MEASURED peak memory: list(reader)"): meas["loop"] = l
        if l.startswith("MEASURED ElementTree parse (whole tree)"): meas["et"] = l
        if l.startswith("MEASURED minidom"): meas["dom"] = l
        if l.startswith("MEASURED SAX"): meas["sax"] = l
        if l.startswith("MEASURED seconds 0.12 (billion"): meas["bl"] = l
assert len(meas) == 5, meas
nint = len(ir["interpreters"]); ndiff = len(ir["differ"])
out = []
out.append("Python and libraries on this page: the examples run in your browser, in Python 3.13.2 with xmltodict 1.0.4, defusedxml 0.7.1 and openpyxl 3.1.5 (the versions the research ran, embedded as wheels) on Pyodide's own lxml 6.0.0, while the research ran Python 3.14.6 with lxml 6.1.3. Each concept example and each chapter example was run in the browser and compared with its recorded result.")
out.append("Recorded, not run: two examples need something a browser cannot give and show the output recorded under Python 3.14.6, labelled so: " + ", ".join(so["recorded"]) + ". The first starts other Python programs with other locale settings; the second shows the notes that Python 3.14 adds to a JSON error, which Python 3.13 does not have.")
out.append("The four libraries: %s are embedded as the PyPI wheels, unchanged, and unpacked in the browser; their licences are %s (recorded in 03-materials/ch18/assets/ASSETS_PROVENANCE_v1_0_0.md). No file of the book's online materials (a zip of %s bytes) is on this page: every example builds its own CSV, JSON and XML text in memory or in a temporary folder." % (", ".join(w["file"] for w in pw["wheels"]), ", ".join(sorted({w["licence"] for w in pw["wheels"]})), "{:,}".format(mat[1])))
out.append("NOT EXECUTED: " + notexec + ". Wherever a page of this site shows a line ending translated as Windows does it, that is EMULATED with io.TextIOWrapper, and says so.")
out.append("MEASURED, single runs on the machine of the day, not results of a program on this page: " + "; ".join(x[len("MEASURED "):] for x in (meas["loop"], meas["et"], meas["dom"], meas["sax"], meas["bl"])) + ".")
out.append("What the public sites answered on 2026-10-12 is in live_observations_v1_0_0.json: the chapter's page (status %d, %s bytes, equal to the digest in the book's ontology), the newest PyPI releases (xmltodict %s, openpyxl %s, defusedxml %s) and the pages of the stories." % (pg[0], "{:,}".format(pg[1]), pypi["xmltodict"][0], pypi["openpyxl"][0], pypi["defusedxml"][0]))
out.append("One program was run under %d interpreters (%s) with the same package versions; the %d items that differ between them are listed in interpreter_record_v1_0_0.json (for example the quoting constants of 3.11, the message of an empty quotechar in 3.14, the notes on a JSON error in 3.14). The book's Appendix A pins xmltodict 0.13.0 and openpyxl 3.1.5, and the chapter's statements were also replayed with those versions." % (nint, ", ".join(ir["interpreters"]), ndiff))
json.dump({"_version": __version__, "limits": out}, open(os.path.join(H, "limits_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
for x in out: print("-", x[:200])
