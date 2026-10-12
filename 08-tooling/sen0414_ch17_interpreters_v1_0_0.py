#!/usr/bin/env python3
"""Chapter 17: runs one pypdf, python-docx and pdfminer.six program, the chapter's operations in a row, under every installed 3.14 patch
release (3.14.0 to 3.14.6, `uv python install 3.14.N`) and, for comparison, under 3.13, 3.12 and 3.11, and records what each printed. It answers
the question chapters 13 to 16 answered with a difference: does anything the chapter teaches change between the patch releases of Python 3.14,
and between 3.14 and the releases before it? The three packages are the same in every run (pypdf 6.20.1, python-docx 1.2.0, pdfminer.six
20260107, with Pillow and cryptography), put in place for each interpreter by `uv run --with`, so a difference comes from the interpreter and
from the wheels built for it (lxml, Pillow, cryptography), not from the packages the chapter names.
The program needs the shipped chapter PDF and demo.docx (fetched and checked by the helper code of sen0414_ch17_thirdparty_v1_0_0.py, kept in
the system temp directory). python runs in isolated mode, each interpreter by `uv run --no-project`.
Usage: sen0414_ch17_interpreters_v1_0_0.py   (needs uv on PATH)   -> ch17-page/interpreter_record_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "08-tooling", "ch17-page", "interpreter_record_v1_0_0.json")
GET = re.search(r"GET = r'''(.*?)'''\n", open(os.path.join(HERE, "sen0414_ch17_thirdparty_v1_0_0.py"), encoding="utf-8").read(), re.S).group(1)
PROG = GET + r'''
import warnings, gc, logging, hashlib, importlib.metadata as md
logging.disable(logging.CRITICAL)
import pypdf, docx, pdfminer.high_level as hl
d = work('Recursion_Chapter1.pdf', 'demo.docx', 'zophie.png', 'watermark.pdf')
res = {}
def w(f):
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter('always')
        try: v = f()
        except Exception as e: v = type(e).__name__ + ': ' + str(e)[:60]
        gc.collect()
    return [v, sorted({x.category.__name__ for x in seen})]
res['series'] = sys.version.split()[0].rsplit('.', 1)[0] + '.x'
res['versions'] = {n: md.version(n) for n in ('pypdf', 'python-docx', 'pdfminer.six', 'pillow', 'cryptography', 'lxml')}
res['import warnings'] = w(lambda: [__import__('importlib').reload(pypdf), __import__('importlib').reload(docx)] and 'reloaded')
R = pypdf.PdfReader('Recursion_Chapter1.pdf')
res['pages'] = len(R.pages)
res['text sha256 (pypdf, all pages)'] = w(lambda: hashlib.sha256(''.join(p.extract_text() for p in R.pages).encode()).hexdigest()[:16])
res['text sha256 (pdfminer.six)'] = w(lambda: hashlib.sha256(hl.extract_text('Recursion_Chapter1.pdf').encode()).hexdigest()[:16])
res['images per page'] = w(lambda: [len(p.images) for p in R.pages])
res['image bytes of page 1'] = w(lambda: sum(len(i.data) for i in R.pages[0].images))
def ops():
    out = {}
    x = pypdf.PdfWriter(); x.append('Recursion_Chapter1.pdf', (0, 5)); out['append (0, 5)'] = len(x.pages)
    x = pypdf.PdfWriter(); x.append('Recursion_Chapter1.pdf', (0, 5, 2)); out['append (0, 5, 2)'] = len(x.pages)
    x = pypdf.PdfWriter(); x.append('Recursion_Chapter1.pdf', [0, 5]); out['append [0, 5]'] = len(x.pages)
    x.merge(1, 'Recursion_Chapter1.pdf', pages=(0, 2)); out['merge pages=(0, 2)'] = len(x.pages)
    x.pages[0].rotate(90); out['rotation'] = x.pages[0].rotation
    x.add_blank_page(); x.insert_blank_page(index=1); out['with blanks'] = len(x.pages)
    wm = pypdf.PdfReader('watermark.pdf').pages[0]
    for p in x.pages[:2]: p.merge_page(wm, over=False)
    x.encrypt('swordfish', algorithm='AES-256'); x.write('o.pdf')
    y = pypdf.PdfReader('o.pdf'); out['encrypted'] = [y.is_encrypted, y.trailer['/Encrypt']['/V'], y.trailer['/Encrypt']['/R'], y.decrypt('bad').name, y.decrypt('swordfish').name, len(y.pages)]
    return out
res['pypdf operations'] = w(ops)
def dx():
    out = {}
    D = docx.Document('demo.docx'); out['demo'] = [len(D.paragraphs), len(D.paragraphs[1].runs), [r.text for r in D.paragraphs[1].runs]]
    D.paragraphs[0].style = 'Normal'; D.paragraphs[1].runs[0].style = 'Quote Char'; D.paragraphs[1].runs[1].underline = True; D.save('restyled.docx')
    out['restyled'] = [docx.Document('restyled.docx').paragraphs[0].style.name, docx.Document('restyled.docx').paragraphs[1].runs[1].underline]
    N = docx.Document(); out['new'] = [len(N.styles), N.core_properties.author]
    N.add_paragraph('Hello, world!'); N.add_heading('H', 0); N.paragraphs[0].runs[0].add_break(docx.enum.text.WD_BREAK.PAGE)
    s = N.add_picture('zophie.png', width=docx.shared.Inches(1), height=docx.shared.Cm(4)); out['picture'] = [s.width, s.height]
    N.save('n.docx'); out['saved'] = [len(docx.Document('n.docx').paragraphs), len(docx.Document('n.docx').inline_shapes)]
    return out
res['python-docx operations'] = w(dx)
res['docx run attribute silently ignored'] = w(lambda: (lambda r: (setattr(r, 'strike', True), r.font.strike)[1])(docx.Document().add_paragraph('a').add_run('b')))
res['docx style by id'] = w(lambda: (lambda p: (setattr(p, 'style', 'MacroText'), p.style.name)[1])(docx.Document().add_paragraph('a')))
res['pypdf merge with the tuple as chapter prints'] = w(lambda: (lambda x: (x.append('Recursion_Chapter1.pdf', (0, 5)), x.merge(2, 'Recursion_Chapter1.pdf', (0, 5)), len(x.pages))[2])(pypdf.PdfWriter()))
for key in sorted(res): print(key, '=', json.dumps(res[key], ensure_ascii=False, sort_keys=True))
'''
UVWITH = ["--with", "pypdf==6.20.1", "--with", "python-docx==1.2.0", "--with", "pdfminer.six==20260107", "--with", "pillow", "--with", "cryptography"]
def uv(v, prog):
    return subprocess.run(["uv", "run", "--no-project", "--python", v] + UVWITH + ["python", "-I", "-c", prog], capture_output=True, text=True, timeout=1800, env={k: x for k, x in os.environ.items() if k not in ("UV_NATIVE_TLS",)})
rows = []; parsed = {}
for v in ("3.14.0", "3.14.1", "3.14.2", "3.14.3", "3.14.4", "3.14.5", "3.14.6", "3.13", "3.12", "3.11"):
    r = uv(v, PROG)
    first = subprocess.run(["uv", "run", "--no-project", "--python", v, "python", "-I", "-c", "import sys; print(sys.version.split()[0])"], capture_output=True, text=True, timeout=300).stdout.strip()
    out = r.stdout.strip() if r.returncode == 0 else "FAILED: " + (r.stderr.strip().splitlines() or ["?"])[-1]
    rows.append([first, out]); print(first, "ok" if r.returncode == 0 else out)
    if r.returncode == 0: parsed[first] = dict(l.split(" = ", 1) for l in out.split("\n"))
keys = sorted(next(iter(parsed.values())))
differ = {k: {v: p.get(k) for v, p in parsed.items()} for k in keys if len({p.get(k) for p in parsed.values()}) > 1 and k != "series"}
same = [k for k in keys if k not in differ and k != "series"]
json.dump({"_version": "1.0.0", "program_after_the_helper_code": PROG[len(GET):].strip(), "interpreters": sorted(parsed), "packages": "pypdf 6.20.1, python-docx 1.2.0, pdfminer.six 20260107, newest pillow and cryptography, put in place for each interpreter by uv run --with",
           "items_that_differ_between_interpreters": differ, "items_equal_in_all": same,
           "rows": ["%s | %s" % (r[0], r[1].replace("\n", " / ")) for r in rows],
           "_note": "Run on %s with each interpreter installed by uv; python runs in isolated mode. Each warning is recorded, not turned into an error. The packages are the same for every interpreter; the wheels of lxml, Pillow and cryptography are the ones built for it (see the versions field of each row)." % datetime.date.today().isoformat()},
          open(OUT, "w"), indent=1, ensure_ascii=False)
print("interpreters:", len(parsed), "| items that differ:", sorted(differ), "| equal in all:", len(same))
