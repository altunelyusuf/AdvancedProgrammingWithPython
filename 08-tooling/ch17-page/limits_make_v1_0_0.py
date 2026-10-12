"""Writes limits_v1_0_0.json, the chapter 17 page's 'Provenance & known limits' entries, from the records Phase A made
(live_observations_v1_0_0.json, interpreter_record_v1_0_0.json), pywheels_v1_0_0.json, standin_v1_0_0.json and the 'Not executed'
sentence of sen0414_ch17_rdodi_data_v1_0_2.py. Numbers are read from those files. Usage: limits_make_v1_0_0.py"""
__version__ = "1.0.0"
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(H, n)))
lv, ir, pw, so = J("live_observations_v1_0_0.json"), J("interpreter_record_v1_0_0.json"), J("pywheels_v1_0_0.json"), J("standin_v1_0_0.json")
src = open(os.path.join(H, "..", "sen0414_ch17_rdodi_data_v1_0_2.py"), encoding="utf-8").read()
live = {i["what"]: i["saw"] for i in lv["items"]}
find = lambda start: next(v for k, v in live.items() if k.startswith(start))
m = re.search(r"Not executed, and said so where it comes up: (.*?)\.\s+The chapter's 91 interactive statements", src, re.S)
notexec = re.sub(r"\s+", " ", m.group(1)).strip()
wc = find("the worst case")
pg = find("chapter 17 page: status")
mat = find("online materials of the 3rd edition")
out = []
out.append("Python and libraries on this page: the examples run in your browser, in Python 3.13.2 with pypdf 6.20.1 and python-docx 1.2.0 (the versions the research ran) on Pyodide's own lxml 6.0.0, Pillow 11.3.0 and cryptography 45.0.5, while the research ran under Python 3.14.6 with lxml 6.1.3, Pillow 12.3.0 and cryptography 50.0.2. Every example was run in the browser and compared with its stored result. Three examples were rewritten for research version 1.0.2 so that they give the same result there: DamagedInput (the pdfminer.six part is left to the description and pypdf's logged warning is silenced), ImagesNeedPillow (the modules it removes are put back) and WriteNeedsBinaryFile (pypdf's logged warning is silenced while it runs).")
out.append("Recorded, not run: two examples need something a browser cannot give and show the output recorded under Python 3.14.6, labelled so: " + ", ".join(so["recorded"]) + ". pdfminer.six is not embedded (its wheel is 6.6 MB of character-map data); the second one starts a second Python in which the cryptography package is made unavailable.")
out.append("The two libraries: %s are embedded as the PyPI wheels, unchanged, and unpacked in the browser; their licences are %s (recorded in 03-materials/ch17/assets/ASSETS_PROVENANCE_v1_0_0.md). No file of the book's online materials (a zip of %s bytes) is on the page: every example builds its own PDF and Word files, so there is no licence question about a shipped file." % (", ".join("%s (%s)" % (w["file"].split("-")[0], w["licence"]) for w in pw["wheels"]), " and ".join(w["licence"] for w in pw["wheels"]), format(mat[1], ",")))
out.append("NOT EXECUTED: " + notexec + ".")
out.append("The PDF Password Breaker: its worst case (the book's dictionary of %s words, both cases of each, %s attempts, a password that is not in it) was run to the end on a file written by pypdf %s: %s seconds for RC4, the default of encrypt(), and %s seconds for AES-256, the two started together on a machine with two cores. Each is one measured run on one machine and the page does not repeat it; the deck labels it so on slide 16." % (format(wc[0]["words"], ","), format(wc[0]["attempts"], ","), wc[0]["pypdf"], wc[0]["seconds"], wc[1]["seconds"]))
out.append("What the public sites answered on 2026-10-12 is in live_observations_v1_0_0.json: the chapter's page (status %d, %s bytes, equal to the digest in the book's ontology), the newest PyPI releases (pypdf %s, python-docx %s) and the pages of the stories. It is one request each, on one day, and nothing re-checks it." % (pg[0], format(pg[1], ","), find("PyPI: newest release")["pypdf"][0], find("PyPI: newest release")["python-docx"][0]))
out.append("One program was run under %d interpreters (%s) with the same package versions; the items that differ between them are listed in interpreter_record_v1_0_0.json. The book's Appendix A pins pypdf 5.0.1 and python-docx 1.1.2, and the chapter's statements were also replayed with those; a result that names a version is a result for that version." % (len(ir["interpreters"]), ", ".join(ir["interpreters"])))
json.dump({"_version": __version__, "limits": out}, open(os.path.join(H, "limits_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
for x in out: print("-", x[:220])
