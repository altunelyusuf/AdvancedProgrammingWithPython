#!/usr/bin/env python3
"""Chapter 22 (Recognizing Text in Images): runs one program, the pytesseract and Pillow behaviour the chapter teaches (a page of known text rendered here, image_to_string,
image_to_data confidences, get_languages, the lang argument, errors, the temporary file, character error rate), under every installed 3.14 patch release (3.14.0 to 3.14.6)
and, for comparison, under 3.15 (a beta), 3.13, 3.12 and 3.11, with the newest pytesseract and Pillow the index offers for each interpreter (`uv run --no-project --with
pytesseract --with pillow --no-build`), and records what each printed. It then runs a smaller program over the releases of the packages themselves: pytesseract 0.3.4 to
0.3.13 (on 3.11, 3.13 and 3.14.6) and Pillow 9.5.0 to 12.3.0 with pytesseract 0.3.13 (on 3.11), because the book pins pytesseract 0.3.10 (Appendix A), which cannot be
imported under 3.14. A release that cannot run is recorded as NOT EXECUTED with the last lines uv or Python printed. The page is drawn by the program (DejaVu Sans, a
font of the machine), nothing is fetched. The Tesseract on the PATH is the apt tesseract-ocr 5.3.4 with its English data for every row, so only the Python side varies. The
operating system is Ubuntu 24.04. Python runs in isolated mode, each interpreter by `uv run --no-project`.
Usage: sen0414_ch22_interpreters_v1_0_0.py   (needs uv on PATH)   -> ch22-page/interpreter_record_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "08-tooling", "ch22-page", "interpreter_record_v1_0_0.json")
PROG = r'''
import sys, os, io, json, re, hashlib, warnings, tempfile, shutil, importlib.metadata as md
from PIL import Image, ImageDraw, ImageFont
import pytesseract as tess
res = {}
def w(f):
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter('always')
        try: v = f()
        except BaseException as e: v = type(e).__name__ + ': ' + str(e).splitlines()[0][:110]
    return [v, sorted({x.category.__name__ for x in seen})]
res['series'] = sys.version.split()[0].rsplit('.', 1)[0] + '.x'
res['versions'] = [md.version('pytesseract'), md.version('pillow')]
F = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
TEXT = 'It was on a dreary night of November, that I beheld the accomplishment of my toils.'
def page(px=28):
    f = ImageFont.truetype(F, px); im = Image.new('L', (int(f.getlength(TEXT)) + 40, px * 2 + 20), 255); ImageDraw.Draw(im).text((20, 15), TEXT, font=f, fill=0); return im
def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1): cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]
def cer(ref, hyp): h = re.sub(r'\s+', ' ', hyp).strip(); return round(lev(ref, h) / len(ref), 4)
im = page()
res['page image size, mode'] = w(lambda: [list(im.size), im.mode])
res['image_to_string: type, CER against the known text'] = w(lambda: (lambda t: [type(t).__name__, cer(TEXT, t), t.endswith('\n')])(tess.image_to_string(im)))
res['image_to_string of a path equals that of the image'] = w(lambda: (im.save('p.png'), tess.image_to_string('p.png') == tess.image_to_string(im))[1])
res['image_to_string of an RGBA copy equals that of the image'] = w(lambda: tess.image_to_string(im.convert('RGBA')) == tess.image_to_string(im))
res['image_to_string lang=eng, config=--psm 7: CER'] = w(lambda: cer(TEXT, tess.image_to_string(im, lang='eng', config='--psm 7')))
res['image_to_data DICT: keys, words, mean conf, lowest conf'] = w(lambda: (lambda d: [list(d), sum(1 for t in d['text'] if t.strip()), round(sum(c for t, c in zip(d['text'], d['conf']) if t.strip()) / max(1, sum(1 for t in d['text'] if t.strip())), 1), min(c for t, c in zip(d['text'], d['conf']) if t.strip())])(tess.image_to_data(im, output_type=tess.Output.DICT)))
res['image_to_data conf type'] = w(lambda: sorted({type(c).__name__ for c in tess.image_to_data(im, output_type=tess.Output.DICT)['conf']}))
res['get_languages: result'] = w(lambda: tess.get_languages())
res['get_tesseract_version: type and text'] = w(lambda: [type(tess.get_tesseract_version()).__name__, str(tess.get_tesseract_version())])
res['image_to_boxes: lines'] = w(lambda: len(tess.image_to_boxes(im).strip().split('\n')))
res['image_to_osd on a page'] = w(lambda: tess.image_to_osd(im).split('\n')[1])
res['unknown language raises'] = w(lambda: tess.image_to_string(im, lang='xyz'))
res['an object that is not an image'] = w(lambda: tess.image_to_string(b'x'))
res['timeout too short'] = w(lambda: tess.image_to_string(im, timeout=0.01))
res['Output.BYTES type'] = w(lambda: type(tess.image_to_string(im, output_type=tess.Output.BYTES)).__name__)
res['image_to_pdf_or_hocr pdf: starts with'] = w(lambda: tess.image_to_pdf_or_hocr(im, extension='pdf')[:5].decode())
res['temporary files left in the temp folder after a call'] = w(lambda: (lambda b: (tess.image_to_string(im), len([f for f in os.listdir(tempfile.gettempdir()) if f.startswith('tess_')]) - b)[1])(len([f for f in os.listdir(tempfile.gettempdir()) if f.startswith('tess_')])))
res['cer of 8 px letters'] = w(lambda: cer(TEXT, tess.image_to_string(page(8))))
res['cer of 24 px letters rotated 4 degrees'] = w(lambda: cer(TEXT, tess.image_to_string(page(24).rotate(4, expand=True, fillcolor=255))))
print(json.dumps(res, sort_keys=True, default=repr))
'''
PTPROG = r'''
import sys, os, io, json, re, warnings, importlib.metadata as md
res = {'pytesseract': md.version('pytesseract'), 'python': sys.version.split()[0]}
def w(f):
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter('always')
        try: v = f()
        except BaseException as e: v = type(e).__name__ + ': ' + str(e).splitlines()[0][:100]
    return [v, sorted({str(x.message)[:100] for x in seen})]
res['import'] = w(lambda: __import__('pytesseract').__name__)
import pytesseract as tess
from PIL import Image, ImageDraw, ImageFont
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 28); im = Image.new('L', (260, 70), 255); ImageDraw.Draw(im).text((20, 15), 'Hello OCR 2026', font=f, fill=0)
res['image_to_string'] = w(lambda: tess.image_to_string(im))
res['image_to_string RGBA'] = w(lambda: tess.image_to_string(im.convert('RGBA')))
res['get_languages'] = w(lambda: tess.get_languages())
res['version'] = w(lambda: str(tess.get_tesseract_version()))
res['image_to_data DICT conf types'] = w(lambda: sorted({type(c).__name__ for c in tess.image_to_data(im, output_type=tess.Output.DICT)['conf']}))
res['image_to_string DICT keys'] = w(lambda: list(tess.image_to_string(im, output_type=tess.Output.DICT)))
res['timeout'] = w(lambda: tess.image_to_string(im, timeout=0.01))
res['numpy array'] = w(lambda: tess.image_to_string(__import__('numpy').asarray(im)))
print(json.dumps(res, sort_keys=True))
'''
INTERPRETERS = ["3.11", "3.12", "3.13", "3.14.0", "3.14.1", "3.14.2", "3.14.3", "3.14.4", "3.14.5", "3.14.6", "3.15"]
PYTESS = ["0.3.4", "0.3.7", "0.3.8", "0.3.9", "0.3.10", "0.3.12", "0.3.13"]
PILLOWS = ["9.5.0", "10.0.0", "10.1.0", "10.2.0", "10.3.0", "10.4.0", "11.0.0", "11.1.0", "11.2.1", "11.3.0", "12.0.0", "12.1.0", "12.2.0", "12.3.0"]
def uv(py, withs, code, timeout=900):
    env = dict(os.environ); env.pop("PYTHONPATH", None); env["TZ"] = "Europe/Istanbul"
    cmd = ["uv", "run", "--no-project", "--python", py, "--no-build"]
    for x in withs: cmd += ["--with", x]
    r = subprocess.run(cmd + ["python", "-I", "-c", code], capture_output=True, text=True, env=env, timeout=timeout, stdin=subprocess.DEVNULL)
    if r.returncode != 0:
        err = [l for l in r.stderr.strip().splitlines() if l.strip()]
        return {"NOT EXECUTED or failed": " | ".join(err[-3:])[:420]}
    return json.loads(r.stdout.strip().splitlines()[-1])
def compare(results):
    keys = sorted({k for r in results.values() for k in r if k not in ("series", "versions", "python", "pillow", "pytesseract")})
    differ = {}
    for k in keys:
        vals = {}
        for v, r in results.items():
            if "NOT EXECUTED or failed" in r: continue
            vals.setdefault(json.dumps(r.get(k), sort_keys=True), []).append(v)
        if len(vals) > 1: differ[k] = [[json.loads(a), b] for a, b in vals.items()]
    return keys, differ
if __name__ == "__main__":
    results = {}
    for py in INTERPRETERS:
        v = subprocess.run(["uv", "run", "--no-project", "--python", py, "python", "-c", "import sys; print(sys.version.split()[0])"], capture_output=True, text=True).stdout.strip()
        results[v or py] = uv(py, ["pytesseract", "pillow"], PROG); print(py, v, "ok" if "NOT EXECUTED or failed" not in results[v or py] else results[v or py]["NOT EXECUTED or failed"], flush=True)
    keys, differ = compare(results)
    pt = {}
    for v in PYTESS:
        for py in ("3.11", "3.13", "3.14.6"):
            k = "%s on %s" % (v, py); pt[k] = uv(py, ["pytesseract==" + v, "pillow", "numpy", "packaging"], PTPROG); print("pytesseract", k, "ok" if "NOT EXECUTED or failed" not in pt[k] else pt[k]["NOT EXECUTED or failed"], flush=True)
    pkeys, pdiffer = compare(pt)
    pil = {}
    for v in PILLOWS:
        pil[v] = uv("3.11", ["pytesseract==0.3.13", "pillow==" + v, "numpy"], PTPROG.replace("res = {'pytesseract'", "res = {'pillow': md.version('pillow'), 'pytesseract'")); print("pillow", v, "ok" if "NOT EXECUTED or failed" not in pil[v] else pil[v]["NOT EXECUTED or failed"], flush=True)
    lkeys, ldiffer = compare(pil)
    json.dump({"_version": "1.0.0", "observed": datetime.date.today().isoformat(), "_note": "Recorded by sen0414_ch22_interpreters_v1_0_0.py: one program (pytesseract calls, character error rate and confidences on a page the program draws, errors) under every installed Python 3.14 patch release and 3.15 beta, 3.13, 3.12 and 3.11, each with the newest pytesseract and Pillow wheels uv found; then pytesseract 0.3.4 to 0.3.13 on 3.11, 3.13 and 3.14.6, and Pillow 9.5.0 to 12.3.0 with pytesseract 0.3.13 on 3.11. The Tesseract on the PATH is the apt 5.3.4 with English data in every row. A run that failed is recorded with the last lines uv or Python printed and counts as NOT EXECUTED.",
               "program": PROG, "pytesseract program": PTPROG, "interpreters": list(results), "results": results, "items compared": len(keys), "differ": differ,
               "pytesseract releases": pt, "pytesseract items compared": len(pkeys), "pytesseract differ": pdiffer,
               "pillow releases": pil, "pillow items compared": len(lkeys), "pillow differ": ldiffer}, open(OUT, "w"), indent=1, ensure_ascii=False)
    print("recorded", len(results), "interpreters;", len(keys), "items; items that differ:", sorted(differ)); print("pytesseract runs:", len(pt), sorted(pdiffer)); print("pillow runs:", len(pil), sorted(ldiffer))
