"""Writes limits_v1_0_0.json, the chapter 23 page's 'Provenance & known limits' entries, from the records Phase A made
(live_observations_v1_0_0.json, interpreter_record_v1_0_0.json, third_party_record_v1_0_0.json), pywheels_v1_0_0.json, standin_v1_0_0.json
and the 'Not executed' sentence of sen0414_ch23_rdodi_data_v1_0_2.py. Numbers are read from those files. Usage: limits_make_v1_0_0.py"""
__version__ = "1.0.0"
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(H, n)))
lv, ir, pw, so, tp = J("live_observations_v1_0_0.json"), J("interpreter_record_v1_0_0.json"), J("pywheels_v1_0_0.json"), J("standin_v1_0_0.json"), J("third_party_record_v1_0_0.json")
src = open(os.path.join(H, "..", "sen0414_ch23_rdodi_data_v1_0_2.py"), encoding="utf-8").read()
live = {i["what"]: i["saw"] for i in lv["items"]}
find = lambda start: next(v for k, v in live.items() if k.startswith(start))
m = re.search(r"Not executed, and said so where it comes up: (.*?)\.\s+The chapter's \d+ listings", src, re.S)
notexec = re.sub(r"\s+", " ", m.group(1)).strip()
pg = find("chapter 23 page: status"); mat = find("online materials of the 3rd edition: status")
rec = so["recorded"]; pics = so["pictures"]
nint = len(ir["interpreters"])
out = []
out.append("Python and libraries on this page: the page's own playground runs in your browser, in Python 3.13.2, while the research ran Python 3.14.6 on Linux with PyAutoGUI 0.9.54, PyScreeze 1.0.1, PyMsgBox 2.0.1, Pillow 12.3.0, NumPy 2.5.4, OpenCV 5.0.0.93 and pyperclip 1.11.0 (and other releases where a section says so).")
out.append("Recorded, not run: all %d examples of the chapter. A browser's Python (its platform is 'emscripten') has no mouse or keyboard to control, no X server, no PyAutoGUI backend and cannot start the programs the examples need (Xvfb, child interpreters, windows); each example is shown with its output recorded under Python 3.14.6, labelled 'Recorded, not run on this page', with its reason: %s." % (len(rec), ", ".join(sorted(rec))))
out.append("Virtual display, not a real screen: every recorded program that moves the mouse, clicks, types, scrolls or reads the screen ran against a private virtual X display (Xvfb) with real X clients, a local stand-in for a screen; the events were seen there and nobody saw the screen. Nothing ran on Windows or macOS, on a real Wayland compositor, on a real or second monitor or with HiDPI scaling.")
out.append("Pictures: %d recorded pictures drawn or captured by the research programs on that virtual display (under %s) are shown beside their examples, labelled 'Recorded picture, not made on this page'; they are SHA-256 checked when the page is made." % (len(pics), ", ".join(sorted(pics))))
out.append("No wheel is embedded on this page and no file of the book's online materials (a zip of {:,} bytes holding %d files; spiralDraw.py is the one that uses PyAutoGUI). The licence of the zip and of its files is an open question for the owner (03-materials/ch23/assets/ASSETS_PROVENANCE_v1_0_0.md).".format(mat[1]) % find("online materials: the files")["files"])
out.append("NOT EXECUTED: " + notexec + ".")
out.append("What the public sites answered on 2026-10-13 is in live_observations_v1_0_0.json: the chapter's page (status %d, %s bytes, equal to the digest in the book's ontology) and the book's other pages and links; the repository of the Sushi Go Round bot answered 403 and the video link 429. The chapter speaks of PyAutoGUI 1.0.0, a release PyPI does not list (the newest is 0.9.54)." % (pg[0], "{:,}".format(pg[1])))
out.append("One program was run under %d interpreter rows (%s): %d of %d items differ between them (for example the events a click delivers and the box locateOnScreen finds, where an interpreter could not start Tk). The same chapter programs were also run with 14 combinations of PyAutoGUI and PyScreeze (%d of %d items differ), %d Pillow releases (%d of %d items differ) and %d PyMsgBox releases (%d of %d items differ); see interpreter_record_v1_0_0.json. The %d items of the third-party record were run with the newest releases and with the book's pins." % (nint, ", ".join(ir["interpreters"]), len(ir["differ"]), ir["items compared"], len(ir["package differ"]), ir["package items compared"], len(ir["pillow releases"]), len(ir["pillow differ"]), ir["pillow items compared"], len(ir["pymsgbox releases"]), len(ir["pymsgbox differ"]), ir["pymsgbox items compared"], len(tp["items"])))
json.dump({"_version": __version__, "limits": out}, open(os.path.join(H, "limits_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
for x in out: print("-", x[:220])
