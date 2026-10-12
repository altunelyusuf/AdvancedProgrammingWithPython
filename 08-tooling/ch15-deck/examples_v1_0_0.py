"""Chapter 15 deck examples: every console session, whole program, chart and table the lecture deck shows. Nothing here carries a
result; examples_run_v1_0_0.py runs it all under the interpreter given and records the results. A console group is one session:
its rows run in order in one namespace (as the deck check re-runs them per slide, one namespace per slide). No console row touches
the network or the file system, and every console row uses the standard library only, so each of them can be typed into a Python
in a browser. A row that needs a line break inside a string writes it as an escaped \\n.

Programs come from sen0414_ch15_corpus_base_v1_0_0.py, all twelve. Eleven of them begin with the lines PRE (the class G, a stand-in
for Google's HTTP answers written for the study, under the real ezsheets and the real google-api-python-client); the twelfth,
tokenPickleRunsCode, needs no Google at all, and addressesAndLetters uses pure functions of the library. Six programs are written for the deck
(they use the same PRE): project11AuditThree and project11TransactionCost (the corpus audit and the corpus transaction program with
their long prints replaced by lines that fit a slide; the corpus originals are recorded and re-run too),
getIdFromUrl (no stand-in: a pure function of the library), downloadName, writeThenRead and appendRace. KIND says what each
program's output is, so that program_check can require the matching honesty label on the slide that shows it:
  standin  the output comes from the real library talking to the stand-in G, not to Google
  fixture  as standin, and the rows read are the CSV export of a real public sheet, committed on 2026-10-01
  none     the output does not depend on Google or its stand-in
Nothing here, and nothing on a slide, was answered by Google."""
__version__ = "1.0.0"
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("base15", os.path.join(HERE, "..", "sen0414_ch15_corpus_base_v1_0_0.py"))
B = importlib.util.module_from_spec(_s)
_s.loader.exec_module(B)
PRE = B.PRE

CONSOLES = {
    "title": ["import platform", "platform.python_version()"],
    "letters": ["L = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'",
                "col = lambda n: col((n-1)//26) + L[(n-1)%26] if n else ''",
                "col(2)", "col(27)", "col(999)", "col(18278)", "sum(26 ** k for k in (1, 2, 3))"],
    "pickle": ["import pickle",
               "class Evil: __reduce__ = lambda self: (eval, ('6 * 7',))",
               "data = pickle.dumps(Evil())",
               "pickle.loads(data)"],
    "pkce": ["import hashlib, base64",
             "v = b'dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk'",
             "d = hashlib.sha256(v).digest()",
             "base64.urlsafe_b64encode(d).rstrip(b'=')"],
    "backoff": ["pauses = list(range(10, 50, 5))", "pauses", "sum(pauses)", "len(pauses) + 1"],
}

# ---- programs written for the deck ---------------------------------------------------------------------------------------------
_audit = B.PROJECT11AUDIT
_old = "print(accounts)\n"
assert _audit.count(_old) == 1
AUDIT3 = _audit.replace(_old, "print(len(accounts), 'accounts; the first three:')\nfor name, amount in list(accounts.items())[:3]:\n    print(' ', name, amount)\n")

_tx = B.PROJECT11TRANSACTION
_tx_a = "sheet.rowCount += 1\n"
_tx_p1 = "print(len(BC), sheet.rowCount, sheet.getRow(sheet.rowCount)[:3], len(sheet.getRows()))\n"
_tx_p2 = "print([(m, p.rsplit('/', 1)[-1]) for m, p, q, b in g.log if m != 'GET'][-5:])\n"
for _x in (_tx_a, _tx_p1, _tx_p2):
    assert _tx.count(_x) == 1, _x
TRANSACTION3 = (_tx.replace(_tx_a, "g.log.clear()\n" + _tx_a).replace(_tx_p1, "print(sheet.rowCount, sheet.getRow(sheet.rowCount)[:3])\n")
                .replace(_tx_p2, "print(len(g.log), 'requests:', [m for m, p, q, b in g.log])\n"))

IDURL = ("import os, tempfile\nos.chdir(tempfile.mkdtemp())\nimport ezsheets\nID = '1TzOJxhNKr15tzdZxTqtQ3EmDP6em_elnbtmZIcyu8vI'\n"
         "BASE = 'https://docs.google.com/spreadsheets/d/'\nfor tail in ('/edit#gid=0', '/', ''):\n    print(repr(tail), ezsheets.getIdFromUrl(BASE + ID + tail) == ID)\n"
         "print(ezsheets.getIdFromUrl(BASE + ID)[-4:], ID[-4:])\ntry:\n    ezsheets.getIdFromUrl('https://docs.google.com/spreadsheets/u/3/d/' + ID)\n"
         "except ValueError as e:\n    print('ValueError', e)\n")
DOWNLOADNAME = PRE + "ss = ezsheets.Spreadsheet(g.load('X', 'Sweigart Books (DO NOT DELETE)', [['TITLE']]))\nprint(ss.downloadAsExcel())\n"
WRITEREAD = (PRE + "sheet = produce()\nsheet['B2'] = 30\nprint(repr(sheet['B2']))\nm, p, q, b = g.log[-1]\nprint(m, p.rsplit('/', 1)[-1], q, b)\n"
             "sheet.refresh()\nprint(repr(sheet['B2']))\n")
RACE = (PRE + "a = ezsheets.Spreadsheet(g.load('BOR', 'Boringcoin', BC)).sheets[0]\nb = ezsheets.Spreadsheet('BOR').sheets[0]\n"
        "for who, sheet in (('first', a), ('second', b)):\n    sheet.rowCount += 1\n    sheet[1, sheet.rowCount] = who\n"
        "    print(who, 'writes to row', sheet.rowCount)\na.refresh()\nprint(a.rowCount, a.getRow(1002)[0])\n")

# name -> (code, packages it needs beyond the interpreter's own, live?)  - no program is live: none reaches the network
PROGRAMS = dict(B.PROGRAMS)
PROGRAMS["project11AuditThree_v1_0_0.py"] = (AUDIT3, (), False)
PROGRAMS["project11TransactionCost_v1_0_0.py"] = (TRANSACTION3, (), False)
PROGRAMS["getIdFromUrl_v1_0_0.py"] = (IDURL, (), False)
PROGRAMS["downloadName_v1_0_0.py"] = (DOWNLOADNAME, (), False)
PROGRAMS["writeThenRead_v1_0_0.py"] = (WRITEREAD, (), False)
PROGRAMS["appendRace_v1_0_0.py"] = (RACE, (), False)

KIND = {n: "standin" for n in PROGRAMS}
for n in B.FIXTURE_BASED:
    KIND[n] = "fixture"
KIND["project11AuditThree_v1_0_0.py"] = "fixture"
KIND["project11TransactionCost_v1_0_0.py"] = "fixture"
KIND["appendRace_v1_0_0.py"] = "fixture"
for n in ("tokenPickleRunsCode_v1_0_0.py", "addressesAndLetters_v1_0_0.py", "getIdFromUrl_v1_0_0.py"):
    KIND[n] = "none"

# ---- a chart and a table, each a setup and one expression (they read the committed CSV export through the name HERE) -----------------
_LEDGER = ("import csv, os\nrows = list(csv.reader(open(os.path.join(HERE, '..', 'ch15-page', 'fixtures', "
           "'boringcoin_sheet_export_2026_10_01_v1_0_0.csv'), newline='', encoding='utf-8')))\n"
           "accounts = {}\nfor row in rows:\n    sender, recipient, amount = row[0], row[1], int(row[2])\n    if sender == 'PRE-MINE':\n"
           "        accounts.setdefault(recipient, 0)\n        accounts[recipient] += amount\n    else:\n"
           "        accounts.setdefault(sender, 0)\n        accounts.setdefault(recipient, 0)\n        accounts[sender] -= amount\n"
           "        accounts[recipient] += amount\n")
TABLES = {
    "ledgerBalances": {
        "setup": _LEDGER,
        "expr": "[['Account', 'Balance']] + [[n, '{:,}'.format(a)] for n, a in list(accounts.items())[:6]] + "
                "[['The other %d accounts' % (len(accounts) - 6), '{:,}'.format(sum(list(accounts.values())[6:]))], "
                "['Total, %d accounts' % len(accounts), '{:,}'.format(sum(accounts.values()))]]",
    }
}
CHARTS = {
    "pauses": {
        "setup": "import json\n",
        "expr": "[[str(i + 1), p] for i, p in enumerate(range(10, 50, 5))]",
    }
}
