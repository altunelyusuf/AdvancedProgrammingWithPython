#!/usr/bin/env python3
"""Chapter 21: runs one program, the Pillow and Matplotlib behaviour the chapter teaches (colour names, crop, paste, resize, rotate, flip, putpixel, ImageDraw,
text, Agg figures, pie and bar), under every installed 3.14 patch release (3.14.0 to 3.14.6) and, for comparison, under 3.15 (a beta, 3.15.0b4), 3.13, 3.12 and
3.11, with the newest Pillow and Matplotlib the index offers for each interpreter (`uv run --no-project --with pillow --with matplotlib --no-build`), and records
what each printed. It then runs two smaller programs over the releases of the packages themselves: Pillow 9.5.0 to 12.3.0 and Matplotlib 3.7.5 to 3.11.2, on the
interpreters that have a wheel for the release (3.11 for the old ones, 3.14.6 for the Matplotlib releases that have a 3.14 wheel), because the book pins Pillow
10.4.0 and Matplotlib 3.9.2 (written "matplotlib==3.92") and neither has a CPython 3.14 wheel. A release without a wheel for the interpreter is recorded as NOT
EXECUTED with the reason uv gave. Pictures in the programs are made by the program (a gradient), nothing is fetched. The operating system is Ubuntu 24.04. Python
runs in isolated mode, each interpreter by `uv run --no-project`.
Usage: sen0414_ch21_interpreters_v1_0_0.py   (needs uv on PATH)   -> ch21-page/interpreter_record_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "08-tooling", "ch21-page", "interpreter_record_v1_0_0.json")
PROG = r'''
import sys, os, io, json, hashlib, warnings, importlib.metadata as md
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageColor, ImageDraw, ImageFont
res = {}
def w(f):
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter('always')
        try: v = f()
        except BaseException as e: v = type(e).__name__ + ': ' + str(e)[:110]
    return [v, sorted({x.category.__name__ for x in seen})]
res['series'] = sys.version.split()[0].rsplit('.', 1)[0] + '.x'
res['versions'] = [md.version('pillow'), md.version('matplotlib'), md.version('numpy')]
def grad():
    im = Image.new('RGB', (60, 40))
    for x in range(60):
        for y in range(40): im.putpixel((x, y), (x * 4 % 256, y * 6 % 256, (x + y) * 3 % 256))
    return im
def sha(im): return hashlib.sha256(im.tobytes()).hexdigest()[:12]
res['getcolor green, lime, CornflowerBlue, #CCDDEE, case'] = w(lambda: [ImageColor.getcolor(n, 'RGBA') for n in ('green', 'lime', 'CornflowerBlue', '#CCDDEE', 'RED')])
res['getcolor transparent'] = w(lambda: ImageColor.getcolor('transparent', 'RGBA'))
res['colormap entries'] = w(lambda: len(ImageColor.colormap))
res['new image size, mode, first pixel'] = w(lambda: [Image.new('RGBA', (100, 200)).size, Image.new('RGBA', (100, 200)).getpixel((0, 0)), Image.new('RGBA', (1, 1), 'purple').getpixel((0, 0))])
g = grad()
res['gradient pixels hash'] = w(lambda: sha(g))
res['crop (10,5,40,35) size and hash'] = w(lambda: [g.crop((10, 5, 40, 35)).size, sha(g.crop((10, 5, 40, 35)))])
res['crop with right < left'] = w(lambda: g.crop((40, 5, 10, 35)))
res['crop beyond the image: size, outside pixel'] = w(lambda: [g.crop((50, 30, 70, 50)).size, g.crop((50, 30, 70, 50)).getpixel((19, 19))])
res['paste returns'] = w(lambda: g.copy().paste(g.crop((0, 0, 10, 10)), (0, 0)))
res['resize float size'] = w(lambda: g.resize((30.5, 20)))
res['resize (30,20) hash, default filter'] = w(lambda: [sha(g.resize((30, 20))), sha(g.resize((30, 20), Image.Resampling.NEAREST)), sha(g.resize((30, 20), Image.Resampling.BICUBIC))])
res['rotate 90, 6 with expand, sizes'] = w(lambda: [g.rotate(90).size, g.rotate(90, expand=True).size, g.rotate(6, expand=True).size])
res['rotate 6 corner pixel on RGB and on RGBA'] = w(lambda: [g.rotate(6).getpixel((0, 0)), g.convert('RGBA').rotate(6).getpixel((0, 0))])
res['rotate 6 expand hash'] = w(lambda: sha(g.rotate(6, expand=True)))
res['flip with Image.FLIP_LEFT_RIGHT, Transpose.FLIP_LEFT_RIGHT'] = w(lambda: [sha(g.transpose(Image.FLIP_LEFT_RIGHT)), sha(g.transpose(Image.Transpose.FLIP_LEFT_RIGHT))])
res['putpixel with a colour name'] = w(lambda: g.copy().putpixel((0, 0), 'red'))
res['getpixel out of range, negative'] = w(lambda: [g.getpixel((-1, 0)), 'ok'])
res['getpixel (60,0)'] = w(lambda: g.getpixel((60, 0)))
res['save RGBA as JPEG'] = w(lambda: g.convert('RGBA').save(io.BytesIO(), 'JPEG'))
res['save to an unknown extension'] = w(lambda: g.save('x.unknownext'))
def sizes():
    b = io.BytesIO(); g.save(b, 'PNG'); c = io.BytesIO(); g.save(c, 'JPEG'); return [len(b.getvalue()), len(c.getvalue())]
res['PNG and JPEG bytes of the gradient'] = w(sizes)
def draw():
    im = Image.new('RGBA', (200, 200), 'blue'); d = ImageDraw.Draw(im)
    d.line([(0, 0), (199, 0), (199, 199), (0, 199), (0, 0)], fill='black')
    d.rectangle((20, 30, 60, 60), fill='red'); d.ellipse((120, 30, 160, 60), fill='yellow'); d.polygon([(57, 87), (79, 62), (94, 85), (120, 90), (103, 113)], fill='brown')
    return [sha(im), sum(1 for p in im.getdata() if p == (255, 0, 0, 255)), sum(1 for x in range(200) for y in range(200) if im.getpixel((x, y)) == (255, 0, 0, 255))]
res['drawing hash, red pixels counted twice'] = w(draw)
res['rectangle with the corners reversed'] = w(lambda: ImageDraw.Draw(Image.new('RGB', (50, 50))).rectangle((30, 30, 10, 10)))
def font():
    f = ImageFont.load_default(); return [type(f).__name__, hasattr(ImageDraw.ImageDraw, 'textsize'), hasattr(ImageFont.ImageFont, 'getsize'), hasattr(f, 'getbbox'), hasattr(ImageDraw.ImageDraw, 'textbbox')]
res['default font: class, textsize, getsize, getbbox, textbbox'] = w(font)
res['truetype arial.ttf (not on this machine)'] = w(lambda: ImageFont.truetype('arial.ttf', 32))
res['truetype DejaVuSans.ttf by name: class, size'] = w(lambda: [type(ImageFont.truetype('DejaVuSans.ttf', 32)).__name__, ImageFont.truetype('DejaVuSans.ttf', 32).size])
res['text bbox of Howdy at (100,150), DejaVu 32'] = w(lambda: ImageDraw.Draw(Image.new('RGB', (200, 200))).textbbox((100, 150), 'Howdy', font=ImageFont.truetype('DejaVuSans.ttf', 32)))
def fig():
    plt.close('all'); plt.plot([1, 2, 3], [2, 4, 3]); plt.plot([1, 2, 3], [1, 2, 3]); b = io.BytesIO(); plt.savefig(b, format='png'); im = Image.open(io.BytesIO(b.getvalue()))
    r = [im.size, im.mode, len(plt.gcf().axes[0].lines), matplotlib.get_backend(), len(set(im.convert('RGB').getdata())) > 20]; plt.close('all'); return r
res['figure: png size, mode, lines, backend, colours'] = w(fig)
res['figure default size, dpi, line colours'] = w(lambda: [list(plt.figure().get_size_inches()), plt.gcf().dpi, matplotlib.rcParams['axes.prop_cycle'].by_key()['color'][:2], plt.close('all')][:3])
def pie():
    plt.close('all'); r = plt.pie([10, 20, 30, 40], labels=list('ABCD'), autopct='%1.1f%%'); out = [type(r).__name__, len(r), [t.get_text() for t in r[2]]]; plt.close('all'); return out
res['pie: return type, items, autopct texts'] = w(pie)
def pie2():
    plt.close('all'); r = plt.pie([10, 20, 30, 40], labels=list('ABCD')); out = [type(r).__name__, len(r)]; plt.close('all'); return out
res['pie without autopct: return type, items'] = w(pie2)
def bar():
    plt.close('all'); r = plt.bar(['a', 'b', 'c'], [3, 1, 2]); out = [type(r).__name__, [type(h.get_height()).__name__ for h in r], [h.get_height() for h in r], [t.get_text() for t in plt.gca().get_xticklabels()]]; plt.close('all'); return out
res['bar: container, height types, heights, tick labels'] = w(bar)
def labels():
    plt.close('all'); a = plt.xlabel('X'); b = plt.title('T'); l = plt.legend(['a']); out = [type(a).__name__, type(b).__name__, type(l).__name__, repr(a)]; plt.close('all'); return out
res['xlabel, title, legend return types and repr'] = w(labels)
def show():
    plt.close('all'); plt.plot([1, 2]); r = plt.show(); n = len(plt.get_fignums()); plt.close('all'); return [r, n]
res['show on Agg: return, figures left'] = w(show)
res['int(300 / 1088 * 816), round'] = w(lambda: [300 / 1088 * 816, int(300 / 1088 * 816), round(300 / 1088 * 816)])
print(json.dumps(res, sort_keys=True, default=repr))
'''
PILPROG = r'''
import sys, os, io, json, warnings, tempfile, importlib.metadata as md
from PIL import Image, ImageDraw, ImageFont, ImageColor
res = {'pillow': md.version('pillow'), 'python': sys.version.split()[0]}
def w(f):
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter('always')
        try: v = f()
        except BaseException as e: v = type(e).__name__ + ': ' + str(e)[:100]
    return [v, sorted({str(x.message)[:110] for x in seen})]
d = tempfile.mkdtemp(); p = os.path.join(d, 'z.png'); Image.new('RGB', (30, 20), 'red').save(p)
os.chdir(d)
res['Image.open("z.png").filename is absolute'] = w(lambda: [Image.open('z.png').filename == p, Image.open('z.png').filename == 'z.png'])
res['Image.FLIP_LEFT_RIGHT'] = w(lambda: str(Image.FLIP_LEFT_RIGHT))
res['Image.Transpose'] = w(lambda: str(Image.Transpose.FLIP_LEFT_RIGHT))
res['ImageDraw.textsize'] = w(lambda: hasattr(ImageDraw.ImageDraw, 'textsize'))
res['ImageFont.getsize'] = w(lambda: hasattr(ImageFont.FreeTypeFont, 'getsize'))
res['load_default class'] = w(lambda: type(ImageFont.load_default()).__name__)
res['load_default(size=20) accepted'] = w(lambda: type(ImageFont.load_default(size=20)).__name__)
res['getdata'] = w(lambda: list(Image.new('RGB', (2, 1), 'red').getdata()))
res['getcolor green'] = w(lambda: ImageColor.getcolor('green', 'RGBA'))
res['colormap entries'] = w(lambda: len(ImageColor.colormap))
res['rotate 6 corner RGB'] = w(lambda: Image.new('RGB', (30, 20), 'red').rotate(6).getpixel((0, 0)))
res['default resize filter'] = w(lambda: str(Image.new('RGB', (4, 4)).resize((2, 2)).info) + str(getattr(Image, 'Resampling', None) is not None))
res['png dpi after save without dpi'] = w(lambda: (Image.new('RGB', (4, 4)).save('a.png'), Image.open('a.png').info.get('dpi'))[1])
res['save RGBA as JPEG'] = w(lambda: Image.new('RGBA', (4, 4)).save('a.jpg'))
res['ImageDraw rectangle reversed'] = w(lambda: ImageDraw.Draw(Image.new('RGB', (50, 50))).rectangle((30, 30, 10, 10)))
res['textbbox exists'] = w(lambda: hasattr(ImageDraw.ImageDraw, 'textbbox'))
print(json.dumps(res, sort_keys=True))
'''
MPLPROG = r'''
import sys, os, io, json, warnings, importlib.metadata as md
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
res = {'matplotlib': md.version('matplotlib'), 'python': sys.version.split()[0], 'numpy': md.version('numpy')}
def w(f):
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter('always')
        try: v = f()
        except BaseException as e: v = type(e).__name__ + ': ' + str(e)[:100]
    return [v, sorted({str(x.message)[:110] for x in seen})]
res['pie return type and items'] = w(lambda: (lambda r: [type(r).__name__, len(r)])(plt.pie([1, 2, 3], autopct='%1.0f%%')))
res['savefig of a line graph'] = w(lambda: (plt.close('all'), plt.plot([1, 2, 3]), plt.savefig(io.BytesIO(), format='png'), 'saved')[3])
res['legend'] = w(lambda: (plt.close('all'), plt.plot([1, 2, 3], label='a'), type(plt.legend()).__name__)[2])
res['bar height type'] = w(lambda: (plt.close('all'), type(plt.bar(['a', 'b'], [3, 1])[0].get_height()).__name__)[1])
res['show on Agg'] = w(lambda: (plt.close('all'), plt.plot([1]), plt.show())[2])
res['default figsize and dpi'] = w(lambda: (plt.close('all'), [list(plt.figure().get_size_inches()), plt.gcf().dpi])[1])
res['default colour cycle'] = w(lambda: matplotlib.rcParams['axes.prop_cycle'].by_key()['color'][:2])
res['xlabel return'] = w(lambda: (plt.close('all'), repr(plt.xlabel('X')))[1])
print(json.dumps(res, sort_keys=True))
'''
INTERPRETERS = ["3.11", "3.12", "3.13", "3.14.0", "3.14.1", "3.14.2", "3.14.3", "3.14.4", "3.14.5", "3.14.6", "3.15"]
PILLOWS = ["9.5.0", "10.0.0", "10.1.0", "10.2.0", "10.3.0", "10.4.0", "11.0.0", "11.1.0", "11.2.1", "11.3.0", "12.0.0", "12.1.0", "12.2.0", "12.3.0"]
MPLS = [("3.7.5", "3.11", "numpy<2"), ("3.8.4", "3.11", "numpy<2"), ("3.9.2", "3.11", "numpy<2.3"), ("3.9.2", "3.13", "numpy<2.3"), ("3.10.0", "3.13", "numpy"), ("3.10.8", "3.13", "numpy"),
        ("3.11.0", "3.13", "numpy"), ("3.11.2", "3.13", "numpy"), ("3.10.6", "3.14.6", "numpy"), ("3.10.8", "3.14.6", "numpy"), ("3.11.0", "3.14.6", "numpy"), ("3.11.2", "3.14.6", "numpy"),
        ("3.9.2", "3.14.6", "numpy"), ("3.10.0", "3.14.6", "numpy")]
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
    keys = sorted({k for r in results.values() for k in r if k not in ("series", "versions", "python", "pillow", "matplotlib", "numpy")})
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
        results[v or py] = uv(py, ["pillow", "matplotlib"], PROG); print(py, v, "ok" if "NOT EXECUTED or failed" not in results[v or py] else results[v or py]["NOT EXECUTED or failed"], flush=True)
    keys, differ = compare(results)
    pil = {}
    for v in PILLOWS:
        pil[v] = uv("3.11", ["pillow==" + v], PILPROG); print("pillow", v, "ok" if "NOT EXECUTED or failed" not in pil[v] else pil[v]["NOT EXECUTED or failed"], flush=True)
    pkeys, pdiffer = compare(pil)
    mpl = {}
    for v, py, np_ in MPLS:
        k = "%s on %s" % (v, py)
        mpl[k] = uv(py, ["matplotlib==" + v, np_], MPLPROG); print("matplotlib", k, "ok" if "NOT EXECUTED or failed" not in mpl[k] else mpl[k]["NOT EXECUTED or failed"], flush=True)
    mkeys, mdiffer = compare(mpl)
    json.dump({"_version": "1.0.0", "observed": datetime.date.today().isoformat(), "_note": "Recorded by sen0414_ch21_interpreters_v1_0_0.py: one program (Pillow colours, crop, paste, resize, rotate, flip, putpixel, ImageDraw, fonts and Matplotlib Agg figures, pie, bar, against pictures made by the program) under every installed Python 3.14 patch release and 3.15 beta, 3.13, 3.12 and 3.11, each with the newest Pillow and Matplotlib wheels uv found for it; then the releases of Pillow 9.5.0 to 12.3.0 on 3.11 and of Matplotlib 3.7.5 to 3.11.2 on the interpreters that have a wheel. A run that failed is recorded with the last lines uv or Python printed and counts as NOT EXECUTED.",
               "program": PROG, "pillow program": PILPROG, "matplotlib program": MPLPROG,
               "interpreters": list(results), "results": results, "items compared": len(keys), "differ": differ,
               "pillow releases": pil, "pillow items compared": len(pkeys), "pillow differ": pdiffer,
               "matplotlib releases": mpl, "matplotlib items compared": len(mkeys), "matplotlib differ": mdiffer}, open(OUT, "w"), indent=1, ensure_ascii=False)
    print("recorded", len(results), "interpreters;", len(keys), "items; items that differ:", sorted(differ))
    print("pillow releases:", len(pil), "items that differ:", sorted(pdiffer)); print("matplotlib runs:", len(mpl), "items that differ:", sorted(mdiffer))
