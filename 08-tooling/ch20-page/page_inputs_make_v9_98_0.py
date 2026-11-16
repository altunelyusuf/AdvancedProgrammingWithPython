#!/usr/bin/env python3
"""Writes the page inputs of the chapter 20 page v9.98.0 (the first page of the chapter built from the deck 2.0.0 and its chapter-code manifest):
  03-materials/ch20/page/chapter_code_ch20_v1_0_1.json   the manifest of v1.0.0 plus, on the 8 examples a browser cannot run, "recorded" (the reason), and a note on the example that runs on the subprocess stand-in
  08-tooling/ch20-deck/examples_out_v2_0_0.json          one Lab / Playground cell per manifest example, same code, same order
  08-tooling/ch20-page/stories_img_v9_98_0.json          the six story pictures of the deck 2.0.0 (files and licences in 03-materials/ch20/assets), credit = the deck's SlideCredit
  08-tooling/ch20-page/pywheels_v1_0_1.json              Pyodide packages ssl and requests, the boot of v1.0.0 and the subprocess stand-in of the chapter 19 page (installed only where the platform is emscripten)
  08-tooling/ch20-page/standin_v1_0_1.json               the stand-in file of v1.0.0 without its example_notes (they named the old deck's examples)
Refuses to overwrite an existing file. Usage: page_inputs_make_v9_98_0.py"""
__version__ = "9.98.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, "..", ".."))
def put(path, obj):
    if os.path.exists(path): sys.exit("refusing to overwrite " + path)
    json.dump(obj, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", os.path.relpath(path, R))
man = json.load(open(os.path.join(R, "03-materials/ch20/page/chapter_code_ch20_v1_0_0.json"), encoding="utf-8"))
lic = json.load(open(os.path.join(R, "03-materials/ch20/assets/story_images_v1_0_0.json"), encoding="utf-8"))
EZ = "This example imports ezgmail, which is licensed GPLv3+ and is not on this page (nor is Google's client library). Run shows the result recorded on the slide, which was computed with a stand-in for Google's service; no Gmail was reached."
SV = "This example starts a local mail server (aiosmtpd) in a thread and runs the openssl command, which a browser's Python cannot do (no sockets between programs, no threads, no processes). Run shows the result recorded on the slide; no real mail server was reached."
REC = {"setup": EZ, "send": EZ, "read": EZ, "reply": EZ, "download": EZ, "starttls": SV, "refusals": SV, "envelope": SV}
SUBNOTE = "On this page the program starts no real process: a browser cannot. A small stand-in for the subprocess module runs the child Python program inside the page; the result is the same as on a computer, but nothing outside the page was started."
man["version"] = "1.0.1"
man["_note"] = "1.0.1 over 1.0.0: the 8 examples that need ezgmail or a local mail server carry \"recorded\" (the page then shows the result recorded on the slide instead of running them); the example 'control' carries a note on the subprocess stand-in. Code and expected results are unchanged."
for e in man["examples"]:
    if e["id"] in REC: e["recorded"] = REC[e["id"]]
    if e["id"] == "control": e["note"] = SUBNOTE
assert sum(1 for e in man["examples"] if "recorded" in e) == 8
put(os.path.join(R, "03-materials/ch20/page/chapter_code_ch20_v1_0_1.json"), man)
ex = {"_version": "2.0.0", "_note": "Made from the chapter-code manifest 03-materials/ch20/page/chapter_code_ch20_v1_0_0.json (same code, same order): one cell per manifest example, name = the example's name."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
put(os.path.join(R, "08-tooling/ch20-deck/examples_out_v2_0_0.json"), ex)
MAP = {"Imap1986": "image_imap.jpg", "Tomlinson1971": "image_arpanet.jpg", "Postel1982": "image_smtp.jpg", "Thuerk1978": "image_dec.jpg", "Papworth1992": "image_sms.jpg", "Att2025": "image_att.jpg"}
si = {"_version": "9.98.0", "_note": "Story pictures for the chapter 20 page's Stories tab: files in 03-materials/ch20/assets, licences in story_images_v1_0_0.json there; the same mapping as the chapter 20 deck 2.0.0; credit = the deck's SlideCredit."}
for sid, fn in MAP.items(): si[sid] = [{"file": fn, "credit": lic[fn]["SlideCredit"]}]
put(os.path.join(H, "stories_img_v9_98_0.json"), si)
pw = json.load(open(os.path.join(H, "pywheels_v1_0_0.json"), encoding="utf-8"))
src = open(os.path.join(H, "..", "ch19-page", "standin_subprocess_v1_1_0.py"), encoding="utf-8").read()
pw["_version"] = "1.0.1"; pw["pyodide_packages"] = ["ssl", "requests"]
pw["boot_python"] = pw["boot_python"] + "import types\n_sm = types.ModuleType('_standin_subprocess')\nexec(compile(%r, '<standin_subprocess>', 'exec'), _sm.__dict__)\n_sm.install()\n" % src
pw["_note"] = "Version 1.0.1 over 1.0.0: also asks Pyodide for its requests package (the ntfy examples only build a request and run for real) and installs the subprocess stand-in (08-tooling/ch19-page/standin_subprocess_v1_1_0.py, unchanged) where the platform is emscripten. No wheel is embedded."
put(os.path.join(H, "pywheels_v1_0_1.json"), pw)
so = json.load(open(os.path.join(H, "standin_v1_0_0.json"), encoding="utf-8")); so["_version"] = "1.0.1"
so["example_notes"] = {}
so["_note"] = so["_note"] + " 1.0.1: the example_notes of 1.0.0 named the examples of the old deck (title, imap, shell, jsonlines) and are dropped; the chapter-code examples that cannot run carry their reason in the manifest (chapter_code_ch20_v1_0_1.json)."
put(os.path.join(H, "standin_v1_0_1.json"), so)
