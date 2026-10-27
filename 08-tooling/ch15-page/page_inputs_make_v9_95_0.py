#!/usr/bin/env python3
"""Writes the page inputs of the chapter 15 page v9.95.0 that are made from the deck's chapter-code manifest 03-materials/ch15/page/chapter_code_ch15_v1_0_0.json
(the manifest of the delivered deck v2_0_0) and from the deck's story pictures. All are NEW files; nothing committed is edited:
  08-tooling/ch15-deck/examples_out_v2_0_0.json     the Lab / Playground examples pane's examples: one cell per manifest example, same code, same order (over examples_out_v1_0_0.json,
                                                    the earlier deck's transcript, which stays; the page-data builder 2.25.0 reads the newest examples_out of the deck folder first)
  08-tooling/ch15-page/stories_img_v9_95_0.json     the five story pictures of the deck (files and licences in 03-materials/ch15/assets), credit = the deck's SlideCredit; the portrait is the crop
  08-tooling/sen0414_ch15_stories_v1_0_1.py         the story companion without the sixth story EzsheetsRelease2019 (it has no picture in the deck, which shows five stories; the page shows
                                                    the same five); made from v1_0_0 by removing that story, its link status and its date check, nothing else
  08-tooling/ch15-page/pywheels_v9_95_0.json        the 14 wheels (hashes checked against the manifest's library block) and a boot program that installs the stand-in module google_standin
                                                    (its text embedded, hash checked against the manifest) and puts the library back before every program
  08-tooling/ch15-page/standin_v9_95_0.json, limits_v9_95_0.json   notes and known limits for the new page, Pyodide recording
Refuses to overwrite an existing file. Usage: page_inputs_make_v9_95_0.py"""
__version__ = "9.95.0"
import hashlib, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, "..", ".."))
J = lambda p: json.load(open(os.path.join(R, p), encoding="utf-8"))
man = J("03-materials/ch15/page/chapter_code_ch15_v1_0_0.json"); lic = J("03-materials/ch15/assets/story_images_v2_0_0.json"); lib = man["library"]
def put(path, obj, raw=False):
    if os.path.exists(path): sys.exit("refusing to overwrite " + path)
    if raw: open(path, "w", encoding="utf-8").write(obj)
    else: json.dump(obj, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote", os.path.relpath(path, R))
# 1. the examples file from the manifest
ex = {"_version": "2.0.0", "_note": "Made from the chapter-code manifest 03-materials/ch15/page/chapter_code_ch15_v1_0_0.json (same code, same order): one cell per manifest example, name = the example's name. New file over examples_out_v1_0_0.json (the earlier deck's transcript), which stays unchanged; the page-data builder 2.25.0 reads the newest examples_out in the deck folder first."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
put(os.path.join(R, "08-tooling/ch15-deck/examples_out_v2_0_0.json"), ex)
# 2. the story pictures
MAP = {"GoogleSheetsXL2Web2006": "image_rochelle_crop.jpg", "NakamotoPaper2008": "image_bitcoin_paper.png", "OAuthBegins2006": "image_cook_oauth.jpg",
       "SheetsApiV3Turndown2021": "image_sheets_screen.jpg", "GoogleForms2008": "image_forms_screen.jpg"}
si = {"_version": "9.95.0", "_note": "Story pictures for the chapter 15 page's Stories tab (new file; the research recorded none): files in 03-materials/ch15/assets, licences in story_images_v2_0_0.json there; the same five stories and pictures as the chapter 15 deck 2.0.0 (08-tooling/ch15-deck/deck_content_v2_0_0.py), credit = the deck's SlideCredit; the portrait of Jonathan Rochelle is the landscape crop image_rochelle_crop.jpg (ASSETS_PROVENANCE_v1_0_1.md) so that the story text starts within the first screen."}
for sid, fn in MAP.items():
    src = fn if fn in lic else "image_rochelle_google.jpg"
    c = lic[src]["SlideCredit"]
    if fn != src: c = c.replace("Photo:", "Photo (cropped):")
    if not os.path.exists(os.path.join(R, "03-materials/ch15/assets", fn)): sys.exit("missing picture " + fn)
    si[sid] = [{"file": fn, "credit": c}]
put(os.path.join(H, "stories_img_v9_95_0.json"), si)
# 3. the story companion with five stories
s = open(os.path.join(R, "08-tooling/sen0414_ch15_stories_v1_0_0.py"), encoding="utf-8").read()
a = s.index('    {\n        "id": "EzsheetsRelease2019"'); b = s.index("]\n\nLINK_STATUS")
s2 = s[:a] + s[b:]
s2 = s2.replace(", 'EzsheetsRelease2019': 200}", "}").replace(', ("EzsheetsRelease2019", "2019")):', "):")
s2 = s2.replace('("SheetsApiV3Turndown2021", "2021"), ("GoogleForms2008", "2008")):', '("SheetsApiV3Turndown2021", "2021"), ("GoogleForms2008", "2008")):')
s2 = s2.replace('(version 1.0.0)', '(version 1.0.1)', 1).replace('__version__ = "1.0.0"', '__version__ = "1.0.1"')
s2 = s2.replace('Six stories for\nGoogle Sheets', 'Five stories for\nGoogle Sheets', 1)
s2 = s2.replace('"""SEN0414 chapter 15 - the story companion to the chapter corpus (version 1.0.1).\n', '"""SEN0414 chapter 15 - the story companion to the chapter corpus (version 1.0.1).\n\nVersion 1.0.1 is a NEW file over 1.0.0 (which stays): the sixth story, EzsheetsRelease2019, is not carried, because the chapter 15 deck 2.0.0 shows five stories (the sixth has no picture of Al Sweigart\nor EZSheets) and the page shows the same five; nothing else changed.\n', 1)
assert "EzsheetsRelease2019" in s2 and s2.count("EzsheetsRelease2019") <= 2, s2.count("EzsheetsRelease2019")
put(os.path.join(R, "08-tooling/sen0414_ch15_stories_v1_0_1.py"), s2, raw=True)
# 4. the wheels and the boot program
asset = lambda f: open(os.path.join(R, "03-materials/ch15/assets", f), "rb").read()
old = J("08-tooling/ch15-page/pywheels_v1_0_0.json")
names = [os.path.basename(f) for f in lib["data_files"]]
assert names == [w["file"] for w in old["wheels"]], "wheel list differs from pywheels_v1_0_0"
for w in old["wheels"]:
    h = hashlib.sha256(asset(w["file"])).hexdigest()
    if h != w["sha256"] or h != lib["wheel_sha256"][w["file"]]: sys.exit("hash differs for " + w["file"])
mod = open(os.path.join(R, lib["file"]), "rb").read()
if hashlib.sha256(mod).hexdigest() != lib["sha256"]: sys.exit("google_standin hash differs from the manifest")
boot = ("import os, sys, time, sysconfig\n"
        "_SITE = sysconfig.get_path('purelib')\n"
        "open(os.path.join(_SITE, 'google_standin.py'), 'w', encoding='utf-8').write(%r)\n"
        "import importlib; importlib.invalidate_caches()\n"
        "import google_standin, ezsheets\n"
        "_cwd0, _sleep0, _time0, _ez0, _gs0 = os.getcwd(), time.sleep, time.time, dict(vars(ezsheets)), dict(vars(google_standin))\n"
        "def _before_run():\n"
        "    # the browser keeps one Python for many programs, a fresh interpreter per program is what the study ran: put ezsheets, the stand-in module, the clock and the folder back as they were at start\n"
        "    os.chdir(_cwd0); time.sleep = _sleep0; time.time = _time0\n"
        "    sys.modules['ezsheets'] = ezsheets; sys.modules['google_standin'] = google_standin\n"
        "    for k in [k for k in vars(ezsheets) if k not in _ez0]: delattr(ezsheets, k)\n"
        "    vars(ezsheets).update(_ez0)\n"
        "    for k in [k for k in vars(google_standin) if k not in _gs0]: delattr(google_standin, k)\n"
        "    vars(google_standin).update(_gs0)\n"
        "    ezsheets._WRITE_REQUESTS.clear(); ezsheets._READ_REQUESTS.clear()\n") % mod.decode("utf-8")
pw = dict(old); pw["_version"] = "9.95.0"; pw["boot_python"] = boot
pw["_note"] = old["_note"] + " VERSION 9.95.0 (new file over 1.0.0): boot_python also writes the stand-in module google_standin (03-materials/ch15/assets/google_standin_v1_0_0.py, sha256 %s, the file named in the manifest's library block) into the browser Python's site-packages under that name and imports it (its speed patch replaces the skip of the older boot), because the 25 examples of the chapter-code tab import it; _before_run also puts the stand-in module back as it was. The wheels and Pyodide packages are those of 1.0.0, unchanged." % lib["sha256"]
put(os.path.join(H, "pywheels_v9_95_0.json"), pw)
# 5. stand-in note and limits
so = J("08-tooling/ch15-page/standin_v1_0_0.json")
so2 = dict(so); so2["_version"] = "9.95.0"
so2["markers"] = list(so["markers"]) + ["google_standin"]
so2["note"] = "Stand-in for Google: this example runs the real EZSheets library (and the real google-api-python-client) against a stand-in for Google written for this course (the class G of the research, or the module google_standin of the deck), which keeps every cell as text and parses nothing. Google was never reached, so the output shows what the library asks for and what it does with an answer, not what Google answers."
so2["example_notes"] = {e["name"]: "Stand-in for Google: this example runs the real EZSheets library against the module google_standin, which answers instead of Google and keeps every cell as text. Google was never reached." for e in man["examples"] if "google_standin" in e["code"]}
so2["_note"] = "New file over standin_v1_0_0.json (see page_inputs_make_v9_95_0.py): the marker google_standin and a note on every chapter example that imports the module. Read by sen0414_page_data_v2_25_0.py."
put(os.path.join(H, "standin_v9_95_0.json"), so2)
lim = list(J("08-tooling/ch15-page/limits_v1_0_0.json")["limits"])
lim[0] = lim[0].replace("against class G, a stand-in for Google written for this course", "against a stand-in for Google written for this course (class G in the research, the module google_standin in the deck's examples)")
lim[5] = (lim[5].split(" The page test compares")[0] + " The module google_standin (the stand-in of the deck's examples, sha256 %s) is installed into that browser Python when the page starts. "
          "The results shown on the page, the concept examples and the %d chapter examples, were recorded with that same runtime, Pyodide 0.28.2 (Python 3.13.2), not with the Python 3.14.6 of the research; the chapter-code manifest's expected results come from Python %s and were all re-run under Pyodide 0.28.2 in one interpreter in the manifest's order before the build (25 of 25 equal), so a statement of the research text about 3.14 is the research's and is not what this page prints. Six concept examples were changed in research version 1.0.2 where the browser cannot do what 3.14.6 did (a socket server, a second interpreter, webbrowser.get), and the unchanged record of those runs stays in the 1.0.1 files.") % (lib["sha256"][:16], len(man["examples"]), man["executed_with"]["python"])
put(os.path.join(H, "limits_v9_95_0.json"), {"_version": "9.95.0", "limits": lim})
