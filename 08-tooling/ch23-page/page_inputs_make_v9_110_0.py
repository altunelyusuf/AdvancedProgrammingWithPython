#!/usr/bin/env python3
"""Writes the page inputs of the chapter 23 page v9.110.0 (Lineage14; built from the deck 4.0.0 and its chapter-code manifest 03-materials/ch23/page/chapter_code_ch23_v1_0_0.json):
  03-materials/ch23/page/chapter_code_ch23_v1_1_0.json   the manifest of the deck with a "recorded" reason on every example (15 of 15: a browser has no screen, mouse or keyboard to control)
  08-tooling/ch23-deck/examples_out_v9_110_0.json        one Lab / Playground cell per manifest example, same code, same order
  08-tooling/ch23-page/stories_img_v9_110_0.json         the six story pictures of the deck 4.0.0 (files and licences in 03-materials/ch23/assets/story_images_v1_0_0.json), keyed by the ids of sen0414_ch23_stories_v2_0_0.py
  08-tooling/ch23-page/standin_v1_0_1.json               standin 1.0.0 with a new notice and one note for each example of the deck
Refuses to overwrite an existing file. Usage: page_inputs_make_v9_110_0.py"""
__version__ = "9.110.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, "..", ".."))
sys.path.insert(0, os.path.join(R, "08-tooling/ch23-deck/spec_v4_0_0"))
def put(path, obj):
    if os.path.exists(path): sys.exit("refusing to overwrite " + path)
    json.dump(obj, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", os.path.relpath(path, R))
man = json.load(open(os.path.join(R, "03-materials/ch23/page/chapter_code_ch23_v1_0_0.json"), encoding="utf-8"))
BASE = "It controls a screen, a mouse and a keyboard, and a browser has none of them to control."
WHY = {
    "pins": BASE + " It also reads the installed packages of the machine that made the deck.",
    "session": BASE + " It also starts other Python processes with subprocess and a display program, and a browser cannot start a program.",
    "corners": BASE + " It also starts a second Python process and changes the size of the screen with xrandr.",
    "locate": BASE + " It also needs the Pillow picture of a real screenshot, which a browser cannot take.",
    "match": BASE + " It also starts Python processes with and without OpenCV, and a browser cannot start a program.",
    "clip": BASE + " It also needs the clipboard of a display and the program xclip.",
}
man2 = dict(man); man2["version"] = "1.1.0"; man2["_note"] = "Version 1.1.0 over 1.0.0: the same examples with a 'recorded' reason on all 15, because a browser has no screen, mouse or keyboard to control."
man2["examples"] = [dict(e, recorded=WHY.get(e["id"], BASE)) for e in man["examples"]]
put(os.path.join(R, "03-materials/ch23/page/chapter_code_ch23_v1_1_0.json"), man2)
ex = {"_version": "9.110.0", "_note": "Made from the chapter-code manifest 03-materials/ch23/page/chapter_code_ch23_v1_0_0.json (same code, same order): one cell per manifest example, name = the example's name."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
put(os.path.join(R, "08-tooling/ch23-deck/examples_out_v9_110_0.json"), ex)
lic = json.load(open(os.path.join(R, "03-materials/ch23/assets/story_images_v1_0_0.json"), encoding="utf-8"))
MAP = {"XWindow1984": "image_xwindow.png", "DeadMan1918": "image_sifa.jpg", "Mouse1968": "image_mouse.jpg", "Captcha2003": "image_captcha.png", "Qwerty1874": "image_qwerty.jpg", "CtrlAltDel1981": "image_ibm5150.jpg"}
si = {"_version": "9.110.0", "_note": "Story pictures for the chapter 23 page's Stories tab: files in 03-materials/ch23/assets, licences in story_images_v1_0_0.json there; the same mapping as the chapter 23 deck 4.0.0; credit = the deck's SlideCredit."}
for sid, fn in MAP.items(): si[sid] = [{"file": fn, "credit": lic[fn]["SlideCredit"]}]
put(os.path.join(H, "stories_img_v9_110_0.json"), si)
old = json.load(open(os.path.join(H, "standin_v1_0_0.json"), encoding="utf-8"))
tail = old["notice"].index(" The deck, whose text is the Lecture tab")
notice = (old["notice"][:tail] + " The deck, whose text is the Lecture tab, is the deck 4.0.0 (41 slides). Its 15 examples are those of the Chapter code tab; they ran for the deck under Python 3.14.6 with PyAutoGUI 0.9.54 on a private virtual X display (Xvfb), "
          "and none of them runs in a browser, so all 15 are shown as recorded, each with its reason. Windows, macOS and a real screen were never used.")
import notes_v4_0_0 as N
SUF = " Recorded under Python 3.14.6 with PyAutoGUI 0.9.54 on a virtual display; it does not run on this page."
notes = {e["name"]: N.RESULT_SAYS[e["id"]] + SUF for e in man["examples"]}
new = dict(old); new["notice"] = notice; new["example_notes"] = notes; new["_version"] = "1.0.1"
put(os.path.join(H, "standin_v1_0_1.json"), new)
