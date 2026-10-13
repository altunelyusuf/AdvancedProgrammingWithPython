"""Writes limits_v1_0_0.json, the chapter 21 page's 'Provenance & known limits' entries, from the records Phase A made
(live_observations_v1_0_0.json, interpreter_record_v1_0_0.json, third_party_record_v1_0_0.json), pywheels_v1_0_0.json, standin_v1_0_0.json
and the 'Not executed' sentence of sen0414_ch21_rdodi_data_v1_0_2.py. Numbers are read from those files. Usage: limits_make_v1_0_0.py"""
__version__ = "1.0.0"
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(H, n)))
lv, ir, pw, so, tp = J("live_observations_v1_0_0.json"), J("interpreter_record_v1_0_0.json"), J("pywheels_v1_0_0.json"), J("standin_v1_0_0.json"), J("third_party_record_v1_0_0.json")
src = open(os.path.join(H, "..", "sen0414_ch21_rdodi_data_v1_0_2.py"), encoding="utf-8").read()
live = {i["what"]: i["saw"] for i in lv["items"]}
find = lambda start: next(v for k, v in live.items() if k.startswith(start))
m = re.search(r"Not executed, and said so where it comes up: (.*?)\.\s+The chapter's \d+ interactive statements", src, re.S)
notexec = re.sub(r"\s+", " ", m.group(1)).strip()
pg = find("chapter 21 page: status"); mat = find("online materials of the 3rd edition: status")
rec = so["recorded"]; pics = so["pictures"]
nint = len(ir["interpreters"])
out = []
out.append("Python and libraries on this page: the examples run in your browser, in Python 3.13.2 with Pyodide's Pillow 11.3.0 and Matplotlib 3.8.4, while the research ran Python 3.14.6 on Linux with Pillow 12.3.0 and Matplotlib 3.11.2. Each example that runs was compared with its recorded result by value (sizes, modes, pixel values, properties), not byte by byte, because the library versions differ.")
out.append("Recorded, not run: %d examples need the book's files (the zip, which is not embedded), a font file, a program of their own (a viewer, a child process), a real or virtual display, or print something that differs between the recording's libraries and the browser's (for example NumPy integer width in a bar chart, the type that pie() returns, the backend name); each is shown with its output recorded under Python 3.14.6, labelled 'Recorded, not run on this page', with its reason: %s." % (len(rec), ", ".join(sorted(rec))))
out.append("Pictures: %d recorded pictures made by the research programs (%s) are shown beside their examples, labelled 'Recorded picture, not made on this page'; they are SHA-256 checked when the page is made. Examples that run in the browser draw their own pictures where they show them." % (len(pics), ", ".join(sorted(pics))))
out.append("The clipboard and viewer examples ran in the recording against a virtual X display (Xvfb) with the real xclip, viewer and Tk, not on a real screen; the Matplotlib window was not seen on a real screen. Nothing ran on Windows or macOS.")
out.append("No wheel is embedded on this page and no file of the book's online materials (a zip of {:,} bytes holding %d files; zophie.png and catlogo.png are among them). The licence of the zip, of the cat picture and of the logo is an open question for the owner; pictures derived from them are not on this page (03-materials/ch21/assets/ASSETS_PROVENANCE_v1_0_0.md).".format(mat[1]) % find("online materials: the files")["files"])
out.append("NOT EXECUTED: " + notexec + ".")
out.append("What the public sites answered on 2026-10-13 is in live_observations_v1_0_0.json: the chapter's page (status %d, %s bytes, equal to the digest in the book's ontology) and the book's other pages and links. The book pins Matplotlib as matplotlib==3.92 in Appendix A, a release that does not exist; the study used 3.9.2 as the pinned environment." % (pg[0], "{:,}".format(pg[1])))
out.append("One program was run under %d interpreters (%s): %d of %d items differ between them. The same chapter programs were also run under %d Pillow releases (%d of %d items differ, for example whether Image.open(...).filename is absolute, ImageDraw.textsize, getsize and getdata) and %d Matplotlib releases (%d of %d items differ: the default colour cycle and what pie() returns); see interpreter_record_v1_0_0.json. The %d items of the third-party record were run with the newest releases and with the book's pins." % (nint, ", ".join(ir["interpreters"]), len(ir["differ"]), ir["items compared"], len(ir["pillow releases"]), len(ir["pillow differ"]), ir["pillow items compared"], len(ir["matplotlib releases"]), len(ir["matplotlib differ"]), ir["matplotlib items compared"], len(tp["items"])))
json.dump({"_version": __version__, "limits": out}, open(os.path.join(H, "limits_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
for x in out: print("-", x[:200])
