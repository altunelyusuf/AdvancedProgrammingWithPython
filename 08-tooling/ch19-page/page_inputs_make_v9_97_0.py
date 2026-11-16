#!/usr/bin/env python3
"""Writes the page inputs of the chapter 19 page v9.97.0 (the first page of the chapter built from the deck 2.2.0 and its chapter-code manifest 03-materials/ch19/page/chapter_code_ch19_v1_1_0.json):
  08-tooling/ch19-deck/examples_out_v2_2_0.json   one Lab / Playground cell per manifest example, same code, same order (new file over examples_out_v1_0_0.json, which stays)
  08-tooling/ch19-page/stories_img_v9_97_0.json   the six story pictures of the deck 2.2.0 (files and licences in 03-materials/ch19/assets), credit = the deck's SlideCredit
  08-tooling/ch19-page/pywheels_v1_0_1.json       the four wheels of v1.0.0 plus a boot snippet that installs standin_subprocess_v1_1_0.py where the browser cannot start processes
  08-tooling/ch19-page/standin_v9_97_0.json       the stand-in file of v1.0.0 plus a note on each chapter example that runs on the subprocess stand-in
  08-tooling/ch19-page/limits_v9_97_0.json        the limits of v1.0.0 plus the sentence on the subprocess stand-in
Refuses to overwrite an existing file. Usage: page_inputs_make_v9_97_0.py"""
__version__ = "9.97.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, "..", ".."))
man = json.load(open(os.path.join(R, "03-materials/ch19/page/chapter_code_ch19_v1_1_0.json"), encoding="utf-8"))
lic = json.load(open(os.path.join(R, "03-materials/ch19/assets/story_images_v1_0_0.json"), encoding="utf-8"))
J = lambda n: json.load(open(os.path.join(H, n), encoding="utf-8"))
def put(path, obj):
    if os.path.exists(path): sys.exit("refusing to overwrite " + path)
    json.dump(obj, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", os.path.relpath(path, R))
ex = {"_version": "2.2.0", "_note": "Made from the chapter-code manifest 03-materials/ch19/page/chapter_code_ch19_v1_1_0.json (same code, same order): one cell per manifest example, name = the example's name."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
put(os.path.join(R, "08-tooling/ch19-deck/examples_out_v2_2_0.json"), ex)
MAP = {"UnixEpoch1971": "image_pdp11.jpg", "Year2038Wrap": "image_y2038.jpg", "CronPurdue1977": "image_vax.jpg", "LeapSecond1972": "image_clock.jpg", "TzLawsuit2011": "image_tzmap.jpg", "Gregorian1582": "image_oct1582.jpg"}
si = {"_version": "9.97.0", "_note": "Story pictures for the chapter 19 page's Stories tab: files in 03-materials/ch19/assets, licences in story_images_v1_0_0.json there; the same mapping as the chapter 19 deck 2.2.0; credit = the deck's SlideCredit."}
for sid, fn in MAP.items(): si[sid] = [{"file": fn, "credit": lic[fn]["SlideCredit"]}]
put(os.path.join(H, "stories_img_v9_97_0.json"), si)
pw = J("pywheels_v1_0_0.json"); src = open(os.path.join(H, "standin_subprocess_v1_1_0.py"), encoding="utf-8").read()
pw["_version"] = "1.0.1"
pw["boot_python"] = pw["boot_python"] + "import types\n_sm = types.ModuleType('_standin_subprocess')\nexec(compile(%r, '<standin_subprocess>', 'exec'), _sm.__dict__)\n_sm.install()\n" % src
pw["_note"] = pw["_note"] + " Version 1.0.1 adds the subprocess stand-in (08-tooling/ch19-page/standin_subprocess_v1_1_0.py), installed only where the platform is emscripten."
put(os.path.join(H, "pywheels_v1_0_1.json"), pw)
NOTE = "On this page the program starts no real process: a browser cannot. A small stand-in for the subprocess module runs the child Python program inside the page and emulates echo, sleep, true, false and a shell line of echo commands. The result is the same as on a computer, but nothing outside the page was started."
so = J("standin_v1_0_0.json"); so["_version"] = "9.97.0"
so["example_notes"] = {n: NOTE for n in ("subprocess.run", "subprocess.Popen", "Exit codes", "Shell safety")}
so["_note"] = "New file over standin_v1_0_0.json: adds the note on the four chapter examples that run on the subprocess stand-in."
put(os.path.join(H, "standin_v9_97_0.json"), so)
li = J("limits_v1_0_0.json"); li["_version"] = "9.97.0"
li["limits"].append("Stand-in for subprocess: four chapter examples (subprocess.run, subprocess.Popen, Exit codes, Shell safety) start other programs, which a browser cannot do. On this page a small stand-in for the subprocess module, shown in the page's boot code, runs the child Python program inside the page and emulates echo, sleep, true, false and a shell line of echo commands; the results shown equal the results recorded on a computer, and each of the four examples carries a note saying so. It is not a shell and not a process: nothing outside the page is started.")
put(os.path.join(H, "limits_v9_97_0.json"), li)
