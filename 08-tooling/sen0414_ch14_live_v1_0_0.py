#!/usr/bin/env python3
"""Chapter 14 (Excel Spreadsheets): observes, once, what the public sources the chapter names answer today, runs the chapter's two
projects on the real files of the book's online materials, and writes what it saw with the date. A web site changes and the files of
the online materials may be replaced; the record is an observation of the day, not something the build can re-check, and no check
reads it.
What it does: fetches the chapter page and compares its SHA-256 with the digest the book's own ontology records; downloads the
online materials of the 3rd edition (the zip No Starch Press links from its book page) and the example3.xlsx and censuspopdata.xlsx
that automatetheboringstuff.com serves; runs Project 9 (the listing of the chapter, whole) on the real census file and Project 10 on
the real produce file, and the two scripts of the online materials as they are shipped; recalculates the produce file with
LibreOffice (headless) to learn what the cached results of its formulas are and compares them with Excel's own and with Python's
round(); reads PyPI for openpyxl; opens every source of the research record and checks that the passages the research relies on are
on the page. Nothing is posted, no login is used, every URL is asked once, and a browser-like User-Agent is sent only to nostarch.com
and microsoft.com, where the default one may be refused (the record shows what each answered).
Run it with the interpreter that has openpyxl, with requests and Beautiful Soup on the path (PYTHONPATH=<dir of requests, bs4>) and
with LibreOffice (soffice) installed.
Usage: sen0414_ch14_live_v1_0_0.py   -> ch14-page/live_observations_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, time, zipfile
import requests, bs4, openpyxl
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "08-tooling", "ch14-page", "live_observations_v1_0_0.json")
UA = {"User-Agent": "SEN0414-research/1.0 (teaching; altunel.yusuf@gmail.com)"}
BROWSER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0"}
obs = []
def see(what, f):
    try: v = f()
    except Exception as e: v = "raised %s: %s" % (type(e).__name__, str(e)[:160])
    obs.append({"what": what, "saw": v})
def get(u, **k):
    k.setdefault("headers", UA)
    return requests.get(u, timeout=90, **k)
def sha(b): return hashlib.sha256(b).hexdigest()
def norm(t): return re.sub(r"\s+", " ", t)
WORK = tempfile.mkdtemp()
PY = sys.executable

# 1. the chapter and the book's own record of it
ch = get("https://automatetheboringstuff.com/3e/chapter14.html")
DIGEST = "6965d2d535b879f1e68142300750e61e172af2f02b7c06b73eeb989d2177be5a"
ONTO = "/home/claude/Ontologies/automate-python-book-3e/01-ontologies/automate_python_3e_ch14_v1_0_0.ttl"
see("chapter 14 page: status, bytes, SHA-256, equal to the chapterDigest of the book ontology (read from its file when present)", lambda: [ch.status_code, len(ch.content), sha(ch.content), sha(ch.content) == DIGEST, (DIGEST in open(ONTO).read()) if os.path.exists(ONTO) else "ontology file not present on this machine"])
soup = bs4.BeautifulSoup(ch.text, "html.parser")
see("chapter 14 page: number of listings (pre elements), figures, and the figure image files with the HTTP status of each", lambda: [len(soup.find_all("pre")), len(soup.select("figure")), [(i["src"], get("https://automatetheboringstuff.com/3e/" + i["src"]).status_code) for i in soup.select("img.img1, img.img2")]])
see("chapter 14 page: alt text of the picture of Figure 14-6, 14-7 (they name cells other than the code writes)", lambda: [i.get("alt") for i in soup.select("img.img2") if "Tall row" in i.get("alt", "") or "merged" in i.get("alt", "")])

# 2. the online materials
Z = get("https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip", headers=BROWSER)
plain = requests.get("https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip", timeout=60, stream=True); plain.close()
see("online materials zip of the 3rd edition: status with a browser-like agent and with the requests library's own default agent, bytes, SHA-256", lambda: [Z.status_code, plain.status_code, len(Z.content), sha(Z.content)])
zf = zipfile.ZipFile(io.BytesIO(Z.content)); MAT = os.path.join(WORK, "mat"); os.makedirs(MAT)
base = "Automate_the_Boring_Stuff_3e_onlinematerials/"
for n in ("example3.xlsx", "censuspopdata.xlsx", "produceSales3.xlsx", "readCensusExcel.py", "updateProduce.py", "census2010.py"):
    open(os.path.join(MAT, n), "wb").write(zf.read(base + n))
see("online materials: the files of chapter 14 with their size, date inside the zip and SHA-256", lambda: [[n, zf.getinfo(base + n).file_size, "%04d-%02d-%02d" % zf.getinfo(base + n).date_time[:3], sha(zf.read(base + n))] for n in ("example3.xlsx", "censuspopdata.xlsx", "produceSales3.xlsx", "readCensusExcel.py", "updateProduce.py", "census2010.py")])
see("online materials: other spreadsheet-like members (the 2nd edition's CSV bundle)", lambda: [n for n in zf.namelist() if "excel" in n.lower() or n.lower().endswith((".xlsx", ".xls", ".csv"))])
ex = get("https://automatetheboringstuff.com/files/example3.xlsx"); cs = get("https://automatetheboringstuff.com/src/censuspopdata.xlsx")
see("example3.xlsx served by automatetheboringstuff.com/files: status, bytes, SHA-256, same file as the zip's", lambda: [ex.status_code, len(ex.content), sha(ex.content), ex.content == zf.read(base + "example3.xlsx")])
see("censuspopdata.xlsx served by automatetheboringstuff.com/src: status, bytes, SHA-256, same bytes as the zip's, same cells as the zip's", lambda: [cs.status_code, len(cs.content), sha(cs.content), cs.content == zf.read(base + "censuspopdata.xlsx"), [list(r) for r in openpyxl.load_workbook(io.BytesIO(cs.content), read_only=True).active.iter_rows(values_only=True)] == [list(r) for r in openpyxl.load_workbook(os.path.join(MAT, "censuspopdata.xlsx"), read_only=True).active.iter_rows(values_only=True)]])
for u in ("https://autbor.com/example3.xlsx", "https://autbor.com/produceSales3.xlsx", "https://automatetheboringstuff.com/files/produceSales3.xlsx"):
    see("the 3rd edition file asked of %s: status (the chapter says to download it from the online materials)" % u, lambda u=u: get(u).status_code)

# 3. the real example3.xlsx against Table 14-1 and the chapter's shell sessions
def real_example():
    wb = openpyxl.load_workbook(os.path.join(MAT, "example3.xlsx")); s = wb["Sheet1"]
    t = [[c.value.strftime("%m/%d/%Y %H:%M:%S") if hasattr(c.value, "strftime") else c.value for c in r] for r in s.iter_rows()]
    return [wb.sheetnames, wb.active.title, s.max_row, s.max_column, repr(s["A1"].value), t[0], t[4], t[6], [ws.dimensions for ws in wb], zipfile.ZipFile(os.path.join(MAT, "example3.xlsx")).read("docProps/app.xml").decode().split("<Application>")[1].split("</Application>")[0]]
see("real example3.xlsx: sheet names, active sheet, size, A1 as repr, rows 1, 5 and 7 of Table 14-1, dimensions of each sheet, the application that saved it", real_example)

# 4. Project 9 on the real census file, the chapter's listing whole
P9 = '''import openpyxl, pprint
print('Opening workbook...')
wb = openpyxl.load_workbook('censuspopdata.xlsx')
sheet = wb['Population by Census Tract']
county_data = {}
print('Reading rows...')
for row in range(2, sheet.max_row + 1):
    state  = sheet['B' + str(row)].value
    county = sheet['C' + str(row)].value
    pop    = sheet['D' + str(row)].value
    county_data.setdefault(state, {})
    county_data[state].setdefault(county, {'tracts': 0, 'pop': 0})
    county_data[state][county]['tracts'] += 1
    county_data[state][county]['pop'] += int(pop)
print('Writing results...')
result_file = open('census2010.py', 'w')
result_file.write('allData = ' + pprint.pformat(county_data))
result_file.close()
print('Done.')
'''
def project9():
    d = os.path.join(WORK, "p9"); os.makedirs(d); shutil.copy(os.path.join(MAT, "censuspopdata.xlsx"), d); open(os.path.join(d, "readCensusExcel.py"), "w").write(P9)
    t = time.perf_counter(); r = subprocess.run([PY, "readCensusExcel.py"], cwd=d, capture_output=True, text=True); dt = time.perf_counter() - t
    mine = open(os.path.join(d, "census2010.py"), "rb").read(); shipped = open(os.path.join(MAT, "census2010.py"), "rb").read()
    imp = subprocess.run([PY, "-c", "import census2010 as c; a = c.allData; print(a['AK']['Anchorage']); print(len(a), sum(len(v) for v in a.values()), sum(x['tracts'] for v in a.values() for x in v.values()), sum(x['pop'] for v in a.values() for x in v.values())); print(sorted(a)[:6], 'DC' in a, 'PR' in a)"], cwd=d, capture_output=True, text=True)
    return [r.returncode, r.stdout.split("\n"), "seconds under 20: %s" % (dt < 20), len(mine), len(shipped), mine == shipped.replace(b"\r\n", b"\n"), shipped.count(b"\r\n"), imp.stdout.split("\n")]
see("Project 9 (the chapter's listing whole) on the real censuspopdata.xlsx: exit code, output, bytes of census2010.py made and shipped, equal once the shipped CRLF are made LF, then the import session", project9)

# 5. Project 10 on the real produce file, then LibreOffice
P10 = '''import openpyxl
wb = openpyxl.load_workbook('produceSales3.xlsx')
sheet = wb['Sheet']
PRICE_UPDATES = {'Garlic': 3.07,
                 'Celery': 1.19,
                 'Lemon': 1.27}
for row_num in range(2, sheet.max_row + 1):  # Skip the first row.
    produce_name = sheet.cell(row=row_num, column=1).value
    if produce_name in PRICE_UPDATES:
        sheet.cell(row=row_num, column=2).value = PRICE_UPDATES[produce_name]
wb.save('updatedProduceSales3.xlsx')
'''
d10 = os.path.join(WORK, "p10"); os.makedirs(d10); shutil.copy(os.path.join(MAT, "produceSales3.xlsx"), d10); open(os.path.join(d10, "updateProduce.py"), "w").write(P10)
def project10():
    t = time.perf_counter(); r = subprocess.run([PY, "updateProduce.py"], cwd=d10, capture_output=True, text=True); dt = time.perf_counter() - t
    a = openpyxl.load_workbook(os.path.join(d10, "produceSales3.xlsx"))["Sheet"]; b = openpyxl.load_workbook(os.path.join(d10, "updatedProduceSales3.xlsx"))["Sheet"]
    ch = {}
    for rr in range(2, a.max_row + 1):
        if a.cell(rr, 2).value != b.cell(rr, 2).value: k = (a.cell(rr, 1).value, a.cell(rr, 2).value, b.cell(rr, 2).value); ch[k] = ch.get(k, 0) + 1
    ov = openpyxl.load_workbook(os.path.join(d10, "produceSales3.xlsx"), data_only=True)["Sheet"]; nv = openpyxl.load_workbook(os.path.join(d10, "updatedProduceSales3.xlsx"), data_only=True)["Sheet"]
    names = {}
    for rr in range(2, a.max_row + 1): names[a.cell(rr, 1).value] = names.get(a.cell(rr, 1).value, set()) | {a.cell(rr, 2).value}
    return [r.returncode, "seconds under 20: %s" % (dt < 20), a.max_row, sorted([list(map(str, k)) + [v] for k, v in ch.items()]), sum(ch.values()), "D2 cached in the original: %r, in the saved copy: %r" % (ov["D2"].value, nv["D2"].value), {k: sorted(names[k]) for k in ("Garlic", "Celery", "Lemon")}, a.freeze_panes, a.sheet_view.topLeftCell]
see("Project 10 (the chapter's listing whole) on the real produceSales3.xlsx: exit code, rows changed per item with old and new price, cached TOTAL before and after, the prices the file held for the three items, its saved scroll position", project10)
LO = shutil.which("soffice")
def lo_convert(src, outdir):
    os.makedirs(outdir, exist_ok=True); r = subprocess.run([LO, "--headless", "--convert-to", "xlsx", "--outdir", outdir, src], capture_output=True, text=True, timeout=300); return r.returncode
see("LibreOffice used for the recalculation (version line)", lambda: subprocess.run([LO, "--version"], capture_output=True, text=True).stdout.strip())
def recalc():
    rc = lo_convert(os.path.join(d10, "updatedProduceSales3.xlsx"), os.path.join(d10, "lo")); rc0 = lo_convert(os.path.join(d10, "produceSales3.xlsx"), os.path.join(d10, "lo0"))
    after = openpyxl.load_workbook(os.path.join(d10, "lo", "updatedProduceSales3.xlsx"), data_only=True)["Sheet"]; before = openpyxl.load_workbook(os.path.join(d10, "lo0", "produceSales3.xlsx"), data_only=True)["Sheet"]
    excel = openpyxl.load_workbook(os.path.join(d10, "produceSales3.xlsx"), data_only=True)["Sheet"]; f = openpyxl.load_workbook(os.path.join(d10, "produceSales3.xlsx"))["Sheet"]; upd = openpyxl.load_workbook(os.path.join(d10, "updatedProduceSales3.xlsx"))["Sheet"]
    n = f.max_row - 1; e_lo = e_py = u_py = 0
    for rr in range(2, f.max_row + 1):
        py = round(f.cell(rr, 2).value * f.cell(rr, 3).value, 2)
        if abs(excel.cell(rr, 4).value - before.cell(rr, 4).value) > 0.0051: e_lo += 1
        if abs(excel.cell(rr, 4).value - py) > 0.0051: e_py += 1
        if abs(after.cell(rr, 4).value - round(upd.cell(rr, 2).value * upd.cell(rr, 3).value, 2)) > 0.0051: u_py += 1
    return [rc, rc0, n, "rows where Excel's cached TOTAL differs from LibreOffice's recalculation: %d" % e_lo, "rows where Excel's cached TOTAL differs from Python round(B*C, 2): %d" % e_py, "rows where LibreOffice's recalculated TOTAL of the updated file differs from Python round(B*C, 2): %d" % u_py, [str(x) for x in (after["D2"].value, openpyxl.load_workbook(os.path.join(d10, "lo", "updatedProduceSales3.xlsx"))["Sheet"]["D2"].value)]]
see("recalculation of the produce file with LibreOffice: exit codes, rows, how often Excel's stored TOTAL, LibreOffice's TOTAL and Python's round() disagree", recalc)
def exact_halves():
    f = openpyxl.load_workbook(os.path.join(d10, "produceSales3.xlsx"))["Sheet"]; ex = openpyxl.load_workbook(os.path.join(d10, "produceSales3.xlsx"), data_only=True)["Sheet"]; k = 0; first = []
    for rr in range(2, f.max_row + 1):
        p = f.cell(rr, 2).value * f.cell(rr, 3).value
        if abs(ex.cell(rr, 4).value - round(p, 2)) > 0.0051 and len(first) < 3: first.append([f.cell(rr, 1).value, f.cell(rr, 2).value, f.cell(rr, 3).value, repr(p), ex.cell(rr, 4).value, round(p, 2)])
    return first
see("three rows where Excel's stored ROUND(B*C,2) and Python's round(B*C, 2) differ: item, price, pounds, the exact product as Python holds it, Excel's total, Python's total", exact_halves)
def wf():
    d = os.path.join(WORK, "wf"); os.makedirs(d); wb = openpyxl.Workbook(); s = wb.active; s["A1"] = 200; s["A2"] = 300; s["A3"] = "=SUM(A1:A2)"; wb.save(os.path.join(d, "writeFormula3.xlsx")); lo_convert(os.path.join(d, "writeFormula3.xlsx"), os.path.join(d, "lo"))
    w = openpyxl.load_workbook(os.path.join(d, "lo", "writeFormula3.xlsx")); v = openpyxl.load_workbook(os.path.join(d, "lo", "writeFormula3.xlsx"), data_only=True)
    return [openpyxl.load_workbook(os.path.join(d, "writeFormula3.xlsx"), data_only=True).active["A3"].value, w.active["A3"].value, v.active["A3"].value]
see("the chapter's writeFormula3.xlsx: data_only value as openpyxl saved it, then after LibreOffice opened and saved it (the chapter's 'open it in Excel and save it' step): formula string, formula result", wf)

# 6. the scripts of the online materials, as shipped
def shipped():
    out = []
    for n, extra in (("readCensusExcel.py", ["censuspopdata.xlsx"]), ("updateProduce.py", ["produceSales3.xlsx"])):
        d = os.path.join(WORK, "s_" + n); os.makedirs(d); shutil.copy(os.path.join(MAT, n), d)
        for e in extra: shutil.copy(os.path.join(MAT, e), d)
        r = subprocess.run([PY, "-W", "ignore", n], cwd=d, capture_output=True, text=True); out.append([n, r.returncode, r.stdout.strip().split("\n"), r.stderr.strip().split("\n")[-1]])
        src = open(os.path.join(MAT, n)).read(); out.append([n + " source uses", [w for w in ("get_sheet_by_name", "get_highest_row", "produceSales.xlsx", "produceSales3.xlsx", "censuspopdata.xlsx") if w in src]])
    return out
see("the two scripts of the online materials as shipped, run beside the real files: exit code, output, last line of the error, and the names they use", shipped)
see("online materials: census2010.py as shipped, first line and line ending", lambda: [open(os.path.join(MAT, "census2010.py"), "rb").read(70).decode(), b"\r\n" in open(os.path.join(MAT, "census2010.py"), "rb").read()])

# 7. errata and the book page
er = get("https://nostarch.com/download/errata/automate-the-boring-stuff-with-python-3e_errata_p2.pdf", headers=BROWSER)
def errata():
    p = os.path.join(WORK, "errata.pdf"); open(p, "wb").write(er.content); t = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout
    return [er.status_code, len(er.content), len(t), [w for w in ("Excel", "openpyxl", "spreadsheet", "Chapter 14", "Reference") if w.lower() in t.lower()]]
see("No Starch errata PDF for the 3rd edition (p2): status, bytes, text length, which of Excel, openpyxl, spreadsheet, Chapter 14, Reference it contains", errata)

# 8. PyPI
pj = get("https://pypi.org/pypi/openpyxl/json").json()
def pypi():
    rel = pj["releases"]; stable = sorted((v for v in rel if re.fullmatch(r"\d+\.\d+\.\d+", v) and rel[v]), key=lambda v: [int(x) for x in v.split(".")])
    last = stable[-1]; up = rel[last][0]["upload_time_iso_8601"][:10]; first = min(f["upload_time_iso_8601"] for v in rel for f in rel[v])[:10]
    cl = sorted((c for c in pj["info"]["classifiers"] if re.fullmatch(r"Programming Language :: Python :: 3\.\d+", c)), key=lambda c: int(c.rsplit(".", 1)[1]))
    return [pj["info"]["version"], last, up, pj["info"]["requires_python"], pj["info"]["license_expression"] if pj["info"].get("license_expression") else pj["info"].get("license"), cl[-1], len(stable), "first upload %s" % first, sorted(pj["info"]["requires_dist"] or []), [(v, rel[v][0]["upload_time_iso_8601"][:10]) for v in stable[-4:]], (datetime.date.today() - datetime.date.fromisoformat(up)).days // 365]
see("openpyxl on PyPI: current version, newest stable, its upload date, Requires-Python, licence, last Python classifier, stable releases, first upload, dependencies, last four releases, whole years since the newest", pypi)
dv = get("https://openpyxl.readthedocs.io/en/stable/"); dt = norm(bs4.BeautifulSoup(dv.text, "html.parser").get_text(" "))
see("openpyxl's stable documentation front page: version it names and its generated date (PyPI's newest is above)", lambda: [re.search(r"Version\s*:?\s*([\d.]+)", dt).group(1), re.search(r"Generated\s*:?\s*([A-Za-z]+ \d+, \d{4})", dt).group(1)])
for pk in ("xlrd", "xlsxwriter", "defusedxml", "pillow"):
    see("PyPI %s: newest version and its upload date" % pk, lambda pk=pk: (lambda j: [j["info"]["version"], max(f["upload_time_iso_8601"] for f in j["releases"][j["info"]["version"]])[:10]])(get("https://pypi.org/pypi/%s/json" % pk).json()))

# 9. the sources of the research record: opened, and the passages relied on found
SOURCES = [
 ("P01", "https://automatetheboringstuff.com/3e/chapter14.html", ["Excel Spreadsheets", "openpyxl.load_workbook()", "freeze_panes", "Practice Programs", "Blank Row Inserter"]),
 ("P02", "https://openpyxl.readthedocs.io/en/stable/", ["openpyxl", "defusedxml", "quadratic blowup"]),
 ("P03", "https://openpyxl.readthedocs.io/en/stable/tutorial.html", ["data_only", "read-only", "copy_worksheet", "create them all in memory", "shapes will be lost"]),
 ("P04", "https://openpyxl.readthedocs.io/en/stable/api/openpyxl.worksheet.worksheet.html", ["insert_rows", "freeze_panes", "merge_cells", "iter_rows", "max_row"]),
 ("P05", "https://openpyxl.readthedocs.io/en/stable/styles.html", ["Font", "Calibri", "cannot be changed"]),
 ("P06", "https://openpyxl.readthedocs.io/en/stable/charts/introduction.html", ["Reference", "Series", "add_chart"]),
 ("P07", "https://openpyxl.readthedocs.io/en/stable/charts/bar.html", ["BarChart", "Reference", "titles_from_data"]),
 ("P08", "https://openpyxl.readthedocs.io/en/stable/api/openpyxl.chart.reference.html", ["min_col", "min_row", "max_col", "max_row"]),
 ("P09", "https://openpyxl.readthedocs.io/en/stable/optimized.html", ["read-only", "write-only", "iter_rows"]),
 ("P10", "https://openpyxl.readthedocs.io/en/stable/changes.html", ["3.1.3", "3.1.0", "Python 3.6"]),
 ("P11", "https://pypi.org/project/openpyxl/", ["openpyxl", "3.1.5", "Python"]),
 ("P12", "https://foss.heptapod.net/openpyxl/openpyxl", ["openpyxl"]),
 ("P13", "https://docs.python.org/3.14/library/pprint.html", ["pformat", "sort_dicts"]),
 ("P14", "https://docs.python.org/3.14/library/stdtypes.html", ["setdefault"]),
 ("P15", "https://docs.python.org/3.14/library/sys.html", ["sys.argv", "script name"]),
 ("P16", "https://docs.python.org/3.14/reference/import.html", ["sys.path", "module"]),
 ("P17", "https://docs.python.org/3.14/tutorial/modules.html", ["sys.path", "directory containing the input script"]),
 ("P18", "https://docs.python.org/3.14/whatsnew/3.14.html", ["New In Python 3.14"]),
 ("P19", "https://docs.python.org/3.14/whatsnew/changelog.html", ["Python 3.14.6 final", "Python 3.14.0 final"]),
 ("P20", "https://docs.python.org/3.14/library/functions.html", ["round(", "encoding"]),
 ("P21", "https://peps.python.org/pep-0686/", ["UTF-8 mode", "3.15"]),
 ("P22", "https://docs.python.org/3.14/library/xml.html", ["billion laughs", "quadratic blowup", "Expat versions lower than 2.7.2"]),
 ("P23", "https://docs.python.org/3.14/tutorial/floatingpoint.html", ["round(", "binary"]),
 ("P24", "https://docs.python.org/3.14/library/ast.html", ["literal_eval"]),
 ("P25", "https://docs.python.org/3.14/library/datetime.html", ["datetime"]),
 ("P26", "https://support.microsoft.com/en-us/office/excel-specifications-and-limits-1672b34d-7043-467e-8e27-269d656771c3", ["1,048,576 rows by 16,384 columns", "Excel specifications and limits"]),
 ("P27", "https://support.microsoft.com/en-us/office/round-function-c018c5d8-40fb-4053-90b1-b3e7f61a213c", ["ROUND function rounds a number"]),
 ("P28", "https://support.microsoft.com/en-us/office/freeze-panes-to-lock-rows-and-columns-dab2ffc9-020d-4026-8121-67dd25f2508f", ["Freeze"]),
 ("P29", "https://www.libreoffice.org/", ["LibreOffice"]),
 ("P30", "https://help.libreoffice.org/latest/en-US/text/scalc/01/04060106.html", ["ROUND"]),
 ("P31", "https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html", ["--convert-to", "--headless"]),
 ("P32", "https://pypi.org/project/defusedxml/", ["defusedxml", "billion laughs"]),
 ("P33", "https://raw.githubusercontent.com/libexpat/libexpat/master/expat/Changes", ["billion laughs", "amplification"]),
 ("P34", "https://pillow.readthedocs.io/en/stable/", ["Pillow"]),
 ("P35", "https://xlsxwriter.readthedocs.io/introduction.html", ["XlsxWriter", "It cannot read or modify existing Excel XLSX files"]),
 ("P36", "https://xlrd.readthedocs.io/en/latest/", ["historical .xls format", "will no longer read anything other than .xls files"]),
 ("P37", "https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html", ["openpyxl", "read_excel"]),
 ("P38", "https://docs.astral.sh/uv/concepts/python-versions/", ["uv python install"]),
 ("P39", "https://pip.pypa.io/en/stable/user_guide/", ["pip install"]),
 ("P40", "https://www.python.org/downloads/release/python-3146/", ["Python 3.14.6"]),
 ("P41", "https://nostarch.com/automate-boring-stuff-python-3rd-edition", ["Automate the Boring Stuff"]),
 ("P42", "https://automatetheboringstuff.com/3e/", ["Chapter 14"]),
 ("P43", "https://www.census.gov/programs-surveys/geography/about/glossary.html", ["census tract"]),
 ("P44", "https://www.loc.gov/preservation/digital/formats/fdd/fdd000395.shtml", ["ISO/IEC 29500", "ECMA 376", "SpreadsheetML"]),
 ("P45", "https://xlsxwriter.readthedocs.io/working_with_formulas.html", ["stores the value 0 as the formula result"]),
]


def freeze_real():
    f = os.path.join(WORK, "frozen.xlsx"); src = os.path.join(MAT, "produceSales3.xlsx")
    wb = openpyxl.load_workbook(src); ws = wb["Sheet"]; before = (ws.freeze_panes, ws.sheet_view.topLeftCell)
    ws.freeze_panes = "A2"; wb.save(f)
    w2 = openpyxl.load_workbook(f)["Sheet"]
    return ["before: freeze_panes %r, topLeftCell %r" % before, "after saving with A2: freeze_panes %r, sheet view topLeftCell %r, pane topLeftCell %r, state %r" % (w2.freeze_panes, w2.sheet_view.topLeftCell, w2.sheet_view.pane.topLeftCell, w2.sheet_view.pane.state)]
see("the real produceSales3.xlsx frozen at A2 and saved: the pane and the scroll position the copy carries", freeze_real)
def memory():
    code = ("import tracemalloc, sys, openpyxl\n"
            "mode = sys.argv[1]; tracemalloc.start()\n"
            "wb = openpyxl.load_workbook(sys.argv[2], read_only=(mode == 'ro')); sh = wb.worksheets[0]\n"
            "n = 0\n"
            "if mode == 'ro':\n    for row in sh.iter_rows(min_row=2, values_only=True): n += 1\n"
            "else:\n    for r in range(2, sh.max_row + 1): sh['A' + str(r)].value; sh['B' + str(r)].value; sh['C' + str(r)].value; n += 1\n"
            "print(n, tracemalloc.get_traced_memory()[1] // 1000000)\n")
    res = {}
    for mode in ("book", "ro"):
        r = subprocess.run([PY, "-c", code, mode, os.path.join(MAT, "censuspopdata.xlsx")], capture_output=True, text=True)
        res[mode] = r.stdout.strip() or r.stderr.strip().splitlines()[-1]
    return ["rows read and peak megabytes traced by tracemalloc, by the book's loop over cells and by read_only iter_rows (seconds are not given: tracemalloc slows both)", res]
see("memory: the real census file read by a loop over cells as in Project 9 and by read-only iter_rows", memory)
def rendering():
    d = os.path.join(WORK, "render"); os.makedirs(d)
    wb = openpyxl.Workbook(); ws = wb.active
    ws["A1"] = "nameless"; ws["A1"].font = openpyxl.styles.Font(size=24, italic=True)
    ws["A2"] = "calibri"; ws["A2"].font = openpyxl.styles.Font(name="Calibri", size=24, italic=True)
    ws["A3"] = "plain"
    wb.save(os.path.join(d, "fonts.xlsx"))
    wb = openpyxl.Workbook(); ws = wb.active
    for i in range(1, 11): ws.cell(row=i, column=1, value=i * i)
    ch = openpyxl.chart.BarChart(); ch.title = "Squares chart title"
    ch.append(openpyxl.chart.Series(openpyxl.chart.Reference(ws, 1, 1, 1, 10), title="First series")); ws.add_chart(ch, "C5")
    wb.save(os.path.join(d, "chart.xlsx"))
    out = {}
    for n in ("fonts", "chart"):
        r = subprocess.run([LO, "--headless", "--convert-to", "pdf", "--outdir", d, os.path.join(d, n + ".xlsx")], capture_output=True, text=True, timeout=180)
        out[n + "_convert_exit"] = r.returncode
    out["pdffonts_of_fonts_xlsx"] = [l.split()[0] for l in subprocess.run(["pdffonts", os.path.join(d, "fonts.pdf")], capture_output=True, text=True).stdout.splitlines()[2:]]
    t = subprocess.run(["pdftotext", os.path.join(d, "chart.pdf"), "-"], capture_output=True, text=True).stdout.split()
    out["chart_pdf_text_has_title"] = "Squares" in t
    out["chart_pdf_value_axis_labels_0_to_120"] = all(x in t for x in ("0", "20", "40", "60", "80", "100", "120"))
    out["chart_pdf_legend_and_category_labels"] = ["First" in t and "series" in t, all(str(i) in t for i in range(1, 11))]
    return out
see("LibreOffice drew a workbook with fonts lacking a name or size (pdffonts of the PDF) and a bar chart made by openpyxl (pdftotext finds its title); Excel itself was not available", rendering)
def sources():
    out = []
    for pid, url, phrases in SOURCES:
        try:
            r = requests.get(url, timeout=60, headers=BROWSER if "nostarch.com" in url or "microsoft.com" in url else UA)
            t = r.text
            if "html" in r.headers.get("content-type", ""):
                s = bs4.BeautifulSoup(t, "html.parser")
                for x in s(["script", "style"]): x.decompose()
                t = s.get_text(" ")
            t = norm(t); out.append([pid, r.status_code, len(r.content), {p: (p.lower() in t.lower()) for p in phrases}])
        except Exception as e: out.append([pid, "unreachable: %s" % type(e).__name__, 0, {}])
    return out
see("every source of the research record opened: id, HTTP status, bytes, and whether each passage the research relies on is on the page", sources)
json.dump({"_version": "1.0.0", "observed": datetime.date.today().isoformat(), "with": "openpyxl %s, requests %s, beautifulsoup4 %s, Python %s" % (openpyxl.__version__, requests.__version__, bs4.__version__, sys.version.split()[0]),
           "_note": "Single requests made on the day named, through the build machine's proxy, to the public pages and files the chapter names; the chapter's projects were run on the real files of the online materials in a temporary folder. A record of one observation; web sites change and nothing re-checks it.", "items": obs}, open(OUT, "w"), indent=1, ensure_ascii=False)
print("observed", len(obs), "things on", datetime.date.today())
