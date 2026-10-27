#!/usr/bin/env python3
"""Writes standin_v9_95_0.json and limits_v9_95_0.json of the chapter 18 page v9.95.0 (new files over standin_v1_0_0 and limits_v1_0_0, which stay).
Why new: the page-data builder 2.25.0 now records the observed programs under the page's own runtime, Pyodide 0.28.2 (Python 3.13.2), not under Python 3.14.6;
and the chapter's example names changed with the deck 2.0.1 (the old standin file names examples of the earlier deck). Consequences, measured:
  - SerializationErrorNotes runs in the page and prints None for both notes (Python 3.13 has no notes): it is no longer 'recorded, not run'; a note above the example says so (marker __notes__).
  - DefaultEncodingIsLocale starts child interpreters, which Pyodide cannot (OSError errno 138, 'emscripten does not support processes'): it stays 'recorded, not run'; the text gives the result of
    the same program on the build machine under Python 3.13.16 (run now by this script, not typed).
Refuses to overwrite. Usage: page_text_make_v9_95_0.py"""
__version__ = "9.95.0"
import json, os, subprocess, sys, rdflib
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, "..", ".."))
J = lambda n: json.load(open(os.path.join(H, n), encoding="utf-8"))
g = rdflib.Graph(); g.parse(os.path.join(R, "03-materials/ch18/rdodi/sen0414_ch18_domain_abox_v1_0_2.ttl"))
expr = str(g.value(rdflib.URIRef("http://example.org/sen0414/ch18#IO_DefaultEncodingIsLocale"), rdflib.URIRef("http://example.org/sen0414/ch18#input")))
r = subprocess.run([sys.executable, "-c", "print(repr(eval(%r, {})))" % expr], capture_output=True, text=True, timeout=120)
if r.returncode: sys.exit("the program failed on the build machine: " + r.stderr[-300:])
real = r.stdout.strip(); pyv = "%d.%d.%d" % sys.version_info[:3]
if not pyv.startswith("3.13."): sys.exit("expected Python 3.13 on the build machine, got " + pyv)
old_so, old_li = J("standin_v1_0_0.json"), J("limits_v1_0_0.json")
so = {"_version": "9.95.0", "markers": ["__notes__"],
      "note": "Python 3.13, the Python of this page, gives a JSON error no notes, so both notes below are None. Python 3.14 adds notes such as 'when serializing list item 1' to the same error; the research recorded them under 3.14.6.",
      "recorded": {"DefaultEncodingIsLocale": "This example starts other Python programs (child interpreters) to show the encoding under different locale settings, which a browser cannot do: in the page's own Python the attempt ends with the error shown below. The same program run on the build machine under Python %s printed %s." % (pyv, real)},
      "notice": "Python and libraries on this page: the examples run in your browser, in Python 3.13.2 (Pyodide 0.28.2) with xmltodict 1.0.4, defusedxml 0.7.1 and openpyxl 3.1.5 (embedded as wheels) on Pyodide's own lxml 6.0.0. The results shown on the page were recorded with that same runtime, not with the Python 3.14.6 and lxml 6.1.3 of the research, so a printed result here can differ from a 3.14 statement in the research text. One example needs something a browser cannot give (other Python programs with other locale settings) and is shown as recorded, not run. Not executed at all: Microsoft Excel itself (LibreOffice stood in for it), a real Windows computer (the line-end translation of Windows text mode was reproduced with io.TextIOWrapper and is called EMULATED where it is shown), Python 3.14.7, 3.14.8 and the final 3.15.0, and the language-model clean-up. Memory and time figures are MEASURED once, on one machine, and are single runs, not results of the program.",
      "example_notes": {},
      "_note": "New file over standin_v1_0_0.json (see page_text_make_v9_95_0.py). Read by sen0414_page_data_v2_25_0.py."}
li = list(old_li["limits"])
li[0] = "Python and libraries on this page: the examples run in your browser, in Python 3.13.2 (Pyodide 0.28.2) with xmltodict 1.0.4, defusedxml 0.7.1 and openpyxl 3.1.5 (embedded as wheels) on Pyodide's own lxml 6.0.0. The results shown on the page, the concept examples and the 27 chapter examples, were recorded with that same runtime (the chapter-code manifest's expected results come from a Pyodide run), while the research ran Python 3.14.6 with lxml 6.1.3; a statement of the research text about 3.14 is the research's and is not what this page prints."
li[1] = "Recorded, not run: one example needs something a browser cannot give, DefaultEncodingIsLocale, which starts other Python programs with other locale settings; the page shows what it printed on the build machine under Python %s. The example SerializationErrorNotes runs in the page and prints no notes, because Python 3.13 attaches none to a JSON error (Python 3.14 does)." % pyv
lim = {"_version": "9.95.0", "limits": li}
for fn, o in (("standin_v9_95_0.json", so), ("limits_v9_95_0.json", lim)):
    p = os.path.join(H, fn)
    if os.path.exists(p): sys.exit("refusing to overwrite " + p)
    json.dump(o, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", fn)
print("build machine Python", pyv, "->", real)
