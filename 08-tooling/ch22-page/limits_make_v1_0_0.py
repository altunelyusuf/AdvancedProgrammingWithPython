"""Writes limits_v1_0_0.json, the chapter 22 page's 'Provenance & known limits' entries, from the records Phase A made
(live_observations_v1_0_0.json, interpreter_record_v1_0_0.json, third_party_record_v1_0_0.json), pywheels_v1_0_0.json, standin_v1_0_0.json
and the 'Not executed' sentence of sen0414_ch22_rdodi_data_v1_0_2.py. Numbers are read from those files. Usage: limits_make_v1_0_0.py"""
__version__ = "1.0.0"
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(H, n)))
lv, ir, pw, so, tp = J("live_observations_v1_0_0.json"), J("interpreter_record_v1_0_0.json"), J("pywheels_v1_0_0.json"), J("standin_v1_0_0.json"), J("third_party_record_v1_0_0.json")
src = open(os.path.join(H, "..", "sen0414_ch22_rdodi_data_v1_0_2.py"), encoding="utf-8").read()
live = {i["what"]: i["saw"] for i in lv["items"]}
find = lambda start: next(v for k, v in live.items() if k.startswith(start))
m = re.search(r"Not executed, and said so where it comes up: (.*?)\.\s+The chapter's \d+ interactive statements", src, re.S)
notexec = re.sub(r"\s+", " ", m.group(1)).strip()
pg = find("chapter 22 page: status"); mat = find("online materials of the 3rd edition: status")
rec = so["recorded"]; pics = so["pictures"]
nint = len(ir["interpreters"])
out = []
out.append("Python and libraries on this page: the examples that run do so in your browser, in Python 3.13.2 with Pyodide's Pillow 11.3.0 and NumPy 2.2.5 and the pytesseract 0.3.13 wheel this page carries, while the research ran Python 3.14.6 on Linux with pytesseract 0.3.13, Pillow 12.3.0, NumPy 2.5.4, OpenCV 5.0.0.93, PyAutoGUI 0.9.54 and the real Tesseract (the apt 5.3.4, and 5.5.3 and 4.1.1 built from source), NAPS2 8.5.1 and OCRmyPDF 17.13.0. Each example that runs was compared with its recorded result by value.")
out.append("Recorded, not run: %d examples need the Tesseract program, another program (NAPS2, OCRmyPDF, apt, Python itself), the language data files of the machine, a font file, the zip of the book's online materials, or print what Python 3.14 or Pillow 12 print and the browser's older ones do not; a browser's Python cannot start a program or download that zip. Each is shown with its output recorded under Python 3.14.6, labelled 'Recorded, not run on this page', with its reason: %s." % (len(rec), ", ".join(sorted(rec))))
out.append("Pictures: %d recorded pictures drawn by the research programs (under %s) are shown beside their examples, labelled 'Recorded picture, not made on this page'; they are SHA-256 checked when the page is made, and none is made from a picture of the book." % (len(pics), ", ".join(sorted(pics))))
out.append("The screen-reading program ran in the recording on a virtual X display (Xvfb) with ImageMagick's display and PyAutoGUI, a local stand-in for a screen; nobody saw the picture and no real screen or browser was read. Nothing ran on Windows or macOS and no scanner was used.")
out.append("The page embeds one wheel, pytesseract 0.3.13 (%s, SHA-256 checked), and no file of the book's online materials (a zip of {:,} bytes holding %d files; ocr-example.png, frankenstein.png and frankenstein_jpn.png are among them). The licence of the zip and of its pictures is an open question for the owner; pictures made from them are not on this page (03-materials/ch22/assets/ASSETS_PROVENANCE_v1_0_0.md).".format(mat[1]) % (pw["wheels"][0]["licence"], find("online materials: the files")["files"]))
out.append("NOT EXECUTED: " + notexec + ".")
out.append("What the public sites answered on 2026-10-13 is in live_observations_v1_0_0.json: the chapter's page (status %d, %s bytes, equal to the digest in the book's ontology) and the book's other pages and links. The book pins pytesseract==0.3.10 in Appendix A, which imports pkgutil.find_loader, a function Python 3.14 removed; PyPI lists no 0.3.11 or 0.3.12." % (pg[0], "{:,}".format(pg[1])))
out.append("One program was run under %d interpreters (%s): %d of %d items differ between them. Small programs were also run under %d Pillow releases (%d of %d items differ) and pytesseract releases on three interpreters (%d runs; %d of %d items differ, for example the type of the confidences image_to_data returns); see interpreter_record_v1_0_0.json. The %d items of the third-party record were run with the newest releases and with the book's pins." % (nint, ", ".join(ir["interpreters"]), len(ir["differ"]), ir["items compared"], len(ir["pillow releases"]), len(ir["pillow differ"]), ir["pillow items compared"], len(ir["pytesseract releases"]), len(ir["pytesseract differ"]), ir["pytesseract items compared"], len(tp["items"])))
json.dump({"_version": __version__, "limits": out}, open(os.path.join(H, "limits_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
for x in out: print("-", x[:220])
