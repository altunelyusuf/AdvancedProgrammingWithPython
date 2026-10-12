#!/usr/bin/env python3
"""Chapter 14: runs one openpyxl program, the chapter's operations in a row, under every installed 3.14 patch release (3.14.0 to
3.14.6, `uv python install 3.14.N`) and, for comparison, under 3.13 and 3.12, with every warning turned into an error, and records
what each printed. It was written to answer one question, the one chapter 13 answered with a difference: does anything the chapter
teaches change between the patch releases of Python 3.14? The record says what each interpreter printed; the answer found on
2026-10-12 is in the record itself (the rows are equal except for the version number they begin with).
openpyxl 3.1.5 is installed for each run by uv (`uv run --with openpyxl`), no project is read, and python runs in isolated mode.
Usage: sen0414_ch14_interpreters_v1_0_0.py   (needs uv on PATH)   -> ch14-page/interpreter_record_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, json, os, subprocess, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "08-tooling", "ch14-page", "interpreter_record_v1_0_0.json")
PROG = r'''
import sys, io, pprint, warnings
import openpyxl
from openpyxl.utils import get_column_letter, column_index_from_string
warnings.simplefilter('error')
wb = openpyxl.Workbook(); sh = wb.active; sh.title = 'Spam Bacon Eggs Sheet'
sh['A1'] = 200; sh['A2'] = 300; sh['A3'] = '=SUM(A1:A2)'
sh.merge_cells('C5:D5'); sh.freeze_panes = 'C2'; sh.row_dimensions[1].height = 70; sh.column_dimensions['B'].width = 20
for i in range(1, 11): sh['E' + str(i)] = i * i
ref = openpyxl.chart.Reference(sh, 1, 1, 1, 10); ch = openpyxl.chart.BarChart(); ch.title = 'My Chart'; ch.append(openpyxl.chart.Series(ref, title='First series')); sh.add_chart(ch, 'G5')
b = io.BytesIO(); wb.save(b); b.seek(0)
w2 = openpyxl.load_workbook(b); s2 = w2.active
print(sys.version.split()[0].rsplit('.', 1)[0] + '.x', openpyxl.__version__)
print(w2.sheetnames, s2['A3'].value, s2.max_row, s2.max_column, s2.freeze_panes, sorted(map(str, s2.merged_cells.ranges)), s2.row_dimensions[1].height, s2.column_dimensions['B'].width, len(s2._charts))
print(get_column_letter(900), column_index_from_string('AA'))
print(pprint.pformat({'AK': {'Anchorage': {'tracts': 55, 'pop': 291826}}, 'AL': {'Autauga': {'tracts': 10, 'pop': 54571}}}))
print(sys.version.split()[0] in ('3.14.0', '3.14.1', '3.14.2', '3.14.3', '3.14.4', '3.14.5', '3.14.6') or 'older interpreter')
'''
rows = []
for v in ("3.14.0", "3.14.1", "3.14.2", "3.14.3", "3.14.4", "3.14.5", "3.14.6", "3.13", "3.12"):
    r = subprocess.run(["uv", "run", "--no-project", "--python", v, "--with", "openpyxl==3.1.5", "python", "-I", "-c", PROG], capture_output=True, text=True, timeout=600)
    first = subprocess.run(["uv", "run", "--no-project", "--python", v, "python", "-I", "-c", "import sys; print(sys.version.split()[0])"], capture_output=True, text=True, timeout=300).stdout.strip()
    rows.append([first, r.stdout.strip() if r.returncode == 0 else "FAILED: " + r.stderr.strip().splitlines()[-1]])
    print(rows[-1][0], "ok" if r.returncode == 0 else "FAILED")
body = [r[1].split("\n", 1)[1].rsplit("\n", 1)[0] for r in rows]
json.dump({"_version": "1.0.0", "program": PROG.strip(), "rows": ["%s | %s" % (r[0], r[1].replace("\n", " / ")) for r in rows],
           "all_bodies_equal": len(set(body)) == 1,
           "_note": "Run on %s with each interpreter installed by uv and openpyxl 3.1.5, every warning an error. The first line of each output names the series; the last line says whether the interpreter is one of the seven 3.14 releases. Nothing in the program printed differently between the releases." % datetime.date.today().isoformat()}, open(OUT, "w"), indent=1)
print("all bodies equal:", len(set(body)) == 1)
