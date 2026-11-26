#!/usr/bin/env python3
"""Writes the page inputs of the chapter 22 page v9.109.0 (Lineage14; built from the deck 4.0.0 and its chapter-code manifest 03-materials/ch22/page/chapter_code_ch22_v2_0_0.json):
  03-materials/ch22/page/chapter_code_ch22_v2_1_0.json   the manifest of the deck with a "recorded" reason on every example that a browser cannot run (14 of 15: Tesseract, pdftotext and NAPS2 are programs, not Python modules)
  08-tooling/ch22-deck/examples_out_v9_109_0.json        one Lab / Playground cell per manifest example, same code, same order
  08-tooling/ch22-page/stories_img_v9_109_0.json         the five story pictures of the deck 4.0.0 (files and licences in 03-materials/ch22/assets/story_images_v1_0_0.json), keyed by the ids of sen0414_ch22_stories_v1_0_1.py
  08-tooling/ch22-page/standin_v1_0_1.json               standin 1.0.0 with a new notice and one note for each example of the deck
Refuses to overwrite an existing file. Usage: page_inputs_make_v9_109_0.py"""
__version__ = "9.109.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, "..", ".."))
def put(path, obj):
    if os.path.exists(path): sys.exit("refusing to overwrite " + path)
    json.dump(obj, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", os.path.relpath(path, R))
man = json.load(open(os.path.join(R, "03-materials/ch22/page/chapter_code_ch22_v2_0_0.json"), encoding="utf-8"))
TESS = "It calls the program Tesseract, which is not a Python module and which a browser does not have."
WHY = {
    "engine": TESS, "read": TESS, "lines": TESS, "data": TESS, "size": TESS, "tilt": TESS, "noise": TESS, "clean": TESS, "config": TESS, "lang": TESS,
    "pdf": TESS + " It also starts pdftotext with subprocess, and a browser cannot start a program.",
    "naps": "It starts another program, NAPS2, with subprocess, and a browser cannot start a program; on the machine of the deck NAPS2 is not installed either, so the recorded result is the error.",
    "screen": TESS + " The screen is emulated by a small class, because the real screenshot of pyautogui needs a display.",
    "scraper": TESS + " The screen is emulated by a small class, because the real screenshot of pyautogui needs a display, and it writes a file.",
}
man2 = dict(man); man2["version"] = "2.1.0"; man2["_note"] = "Version 2.1.0 over 2.0.0: the same examples with a 'recorded' reason on the 14 that a browser cannot run; 'The difflib one (mistakes) runs in the browser'."
man2["examples"] = [dict(e, **({"recorded": WHY[e["id"]]} if e["id"] in WHY else {})) for e in man["examples"]]
put(os.path.join(R, "03-materials/ch22/page/chapter_code_ch22_v2_1_0.json"), man2)
ex = {"_version": "9.109.0", "_note": "Made from the chapter-code manifest 03-materials/ch22/page/chapter_code_ch22_v2_0_0.json (same code, same order): one cell per manifest example, name = the example's name."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
put(os.path.join(R, "08-tooling/ch22-deck/examples_out_v9_109_0.json"), ex)
lic = json.load(open(os.path.join(R, "03-materials/ch22/assets/story_images_v1_0_0.json"), encoding="utf-8"))
MAP = {"Goldberg1931": "image_goldberg.jpg", "Kurzweil1976": "image_kurzweil.jpg", "Tesseract1985": "image_tesseract.jpg", "Recaptcha2009": "image_recaptcha.jpg", "Frankenstein1831": "image_frankenstein.jpg"}
si = {"_version": "9.109.0", "_note": "Story pictures for the chapter 22 page's Stories tab: files in 03-materials/ch22/assets, licences in story_images_v1_0_0.json there; the same mapping as the chapter 22 deck 4.0.0; credit = the deck's SlideCredit."}
for sid, fn in MAP.items(): si[sid] = [{"file": fn, "credit": lic[fn]["SlideCredit"]}]
put(os.path.join(H, "stories_img_v9_109_0.json"), si)
old = json.load(open(os.path.join(H, "standin_v1_0_0.json"), encoding="utf-8"))
tail = old["notice"].index(" The deck, whose text is the Lecture tab")
notice = (old["notice"][:tail] + " The 15 examples of the Chapter code tab are those of the lecture deck 4.0.0 and ran for it with Python 3.12.3, Pillow 13.0.0, NumPy 2.5.5 and the real Tesseract 5.3.4: 14 of them need a program that a browser does not have "
          "(Tesseract, pdftotext or NAPS2) and are shown as recorded, and the one that only compares texts with difflib runs in the browser. The two screen examples use a screen that the example itself draws (EMULATED), because the screenshot of PyAutoGUI needs a display; NAPS2 is not installed on that machine, "
          "so its example shows the error that Python raises. The Lecture tab holds the text of the deck 4.0.0; the concept examples above keep their recording under Python 3.14.6.")
NOTES = {
    "The engine and its languages": "The version and the number of languages are those of the machine that made the deck: Tesseract 5.3.4 with 22 language files. In your browser the call fails, because there is no Tesseract program there.",
    "Reading one line of text": "The picture is drawn by the example with the font of Pillow; the same text comes back with a line break at its end. The result shown is the recorded one.",
    "Lines, breaks and the data behind a line": "One capital I of the second line was read as a vertical bar, and a blank line came between the second and the third line; another version of Tesseract can read this picture differently.",
    "Words, boxes and confidence": "The confidence is 96 for every word; the left and top numbers depend on the font that drew the line and on the version of Pillow.",
    "Text that is too small": "The limit of 9 pixels belongs to this font and to Tesseract 5.3.4; another font or version can move it by a pixel or two.",
    "A page that is crooked": "The reading weakens from 6 degrees and fails at 9 for this sentence and this font; a longer text or a page with several lines may behave differently.",
    "Noise on the picture": "The noise comes from NumPy's random generator with the seed 1, so the numbers repeat; the limit of 100 belongs to this sentence and this font.",
    "Cleaning a picture before reading it": "Two of the three steps helped and the black-and-white step made the reading worse; always test a step on the picture at hand.",
    "Cleaning a picture before reading": "Two of the three steps helped and the black-and-white step made the reading worse; always test a step on the picture at hand.",
    "Telling Tesseract what to expect": "The whitelist keeps only digits and hyphens, so the spaces and the letters are gone from the second result.",
    "Languages other than English": "The font DejaVu Sans is needed for the accented letters, and the German and French language files must be installed; the error of lang='xyz' names the missing file.",
    "Finding the mistakes of a reading": "This example runs in your browser and prints the same as the slide: four differences and the similarity 0.86.",
    "A searchable PDF": "The PDF starts with %PDF-; pdftotext reads its invisible text layer. The bytes of a PDF differ between versions, so only its beginning is shown.",
    "Running NAPS2 from Python": "NAPS2 was not installed on the machine of the deck, so the recorded result is FileNotFoundError; with NAPS2 installed the program would start.",
    "Reading the screen": "The screen is a small class that draws two lines of text; the real pyautogui.screenshot() needs a display.",
    "Practice program: browser text scraper": "Each emulated page is drawn, cropped and read, and its text is appended to output.txt; the real program takes a screenshot of the browser instead.",
}
keep = {e["name"] for e in man["examples"]}
notes = {k: v for k, v in NOTES.items() if k in keep}
miss = sorted(keep - set(notes))
if miss: sys.exit("no note for: %r" % miss)
new = dict(old); new["notice"] = notice; new["example_notes"] = notes; new["_version"] = "1.0.1"
put(os.path.join(H, "standin_v1_0_1.json"), new)
