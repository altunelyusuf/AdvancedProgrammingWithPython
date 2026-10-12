#!/usr/bin/env python3
"""SEN0414 chapter 15 (Google Sheets, 3rd edition) - the shared base of the corpus, version 1.0.0.

Holds the chapter's whole programs as text, the single source the deck and the page's Lab tab both read, in the shape of
sen0414_ch14_corpus_base_v1_0_0.py. Each program is a complete script that exits 0 and prints what it printed on 2026-10-12 under
Python 3.14.6 (uv) with ezsheets 2026.4.28. All twelve run offline: no program reaches Google or the network.

Google is not reached because no Google account, OAuth consent or live API call was available. Every program that uses a
spreadsheet starts with the same lines (PRE): the class G, a stand-in for Google's HTTP answers that was written for this study,
keeps every cell as text and does not parse a value, and sits under the real ezsheets and the real google-api-python-client; then
the program changes into a temporary folder and calls install(). So each output shows what the library asks for and what it does
with an answer, not what Google answers. The chapter's code is kept as printed apart from those lines and from the changes a
comment names. The two scripts of the online materials were also run unchanged on the real files; that record is in
ch15-page/live_observations_v1_0_0.json.

Fixture-based (read the CSV exports of the real public sheets, committed on 2026-10-01 in 08-tooling/ch15-page/fixtures; PRE finds the
folder from the environment variable CH15_FIX or by walking up from the current folder to 08-tooling/ch15-page/fixtures):
* PROJECT11AUDIT is Project 11, Step 1 whole, on the Boringcoin export (1,001 rows).
* PROJECT11TRANSACTION is Project 11, Step 2 whole, with the chapter's arguments set in the first line instead of the command line.
* BEANCOUNT is the third practice program, on the Bean Count export (15,001 rows).
Synthetic data, stand-in for Google: FORMS, CONVERTER, ATTRIBUTES, SHEETMOVES, ROWSCOLUMNS (ten rows with the columns of
produceSales3.xlsx), QUOTARETRY, REQUESTCOUNTS.
No stand-in and no data: ADDRESSES (pure functions of the library) and TOKENPICKLE (a tampered token file, in a temporary folder).

Sources read for this chapter, on 2026-10-12: the book chapter (automatetheboringstuff.com/3e/chapter15.html, sha256 76d2dc65...6d1b
as the book's ontology records), the pages of EZSheets, Google's Sheets, Drive, OAuth and Help documentation, the Python 3.14
documentation and the RFCs the research record lists.
"""
FAKE = r'''import json, re, itertools, urllib.parse as up, httplib2, ezsheets
from googleapiclient.discovery import build
class G:
  def __init__(s):
    s.ss = {}; s.n = itertools.count(1); s.sid = itertools.count(100); s.log = []; s.fail = []; s.files = {}; s.out = {}
  def sh(s, t, i, r=1000, c=26, sid=None): return {'p': {'sheetId': next(s.sid) if sid is None else sid, 'title': t, 'index': i, 'gridProperties': {'rowCount': r, 'columnCount': c}}, 'c': {}}
  def new(s, t='Untitled spreadsheet', id=None):
    i = id or 'ID%03d' % next(s.n); s.ss[i] = {'t': t, 'sh': [s.sh('Sheet1', 0, sid=0)]}; return i
  def load(s, id, title, rows):
    i = s.new(title, id); h = s.ss[i]['sh'][0]; h['p']['gridProperties'] = {'rowCount': len(rows), 'columnCount': max(map(len, rows))}
    for r, row in enumerate(rows, 1):
      for c, v in enumerate(row, 1): h['c'][(c, r)] = str(v)
    return i
  def cell(s, h, t): return [x for x in s.ss[h]['sh'] if x['p']['title'] == t][0]
  def reply(s, d, st=200): return httplib2.Response({'status': str(st), 'content-type': 'application/json'}), json.dumps(d).encode()
  def request(s, uri, method='GET', body=None, headers=None, **kw):
    u = up.urlparse(uri); p = up.unquote(u.path); q = up.parse_qs(u.query); b = json.loads(body) if body and body[:1] in (b'{', '{') else None
    s.log.append((method, p, u.query, b))
    if s.fail: st, nm = s.fail.pop(0); return s.reply({'error': {'code': st, 'status': nm, 'message': nm}}, st)
    if p == '/v4/spreadsheets': return s.reply({'spreadsheetId': s.new(b['properties']['title'])})
    if p.startswith('/drive/v3/files') or p.startswith('/upload/drive'): return s.drive(p, method, q, b, headers, body)
    m = re.match(r'/v4/spreadsheets/([^/:]+)(/values/(.+)|/sheets/(\d+):copyTo|:batchUpdate)?$', p)
    if m[1] not in s.ss: return s.reply({'error': {'code': 404, 'status': 'NOT_FOUND', 'message': 'Requested entity was not found.'}}, 404)
    x = s.ss[m[1]]
    if m[3]:
      t, a = m[3].rsplit('!', 1); c1, r1, c2, r2 = re.match(r'([A-Z]+)(\d+):([A-Z]+)(\d+)', a).groups(); c1, c2 = ezsheets.getColumnNumberOf(c1), ezsheets.getColumnNumberOf(c2); h = s.cell(m[1], t)
      if method == 'PUT':
        for i, line in enumerate(b['values']):
          for j, v in enumerate(line): h['c'][(c1 + j, int(r1) + i) if b['majorDimension'] == 'ROWS' else (c1 + i, int(r1) + j)] = '' if v is None else str(v)
        return s.reply({'updatedRange': m[3]})
      rows = [[h['c'].get((c, r), '') for c in range(c1, c2 + 1)] for r in range(int(r1), int(r2) + 1)]
      for r in rows:
        while r and r[-1] == '': r.pop()
      while rows and not rows[-1]: rows.pop()
      return s.reply(dict({'range': m[3], 'majorDimension': 'ROWS'}, **({'values': rows} if rows else {})))
    if m[4]:
      h = [z for z in x['sh'] if z['p']['sheetId'] == int(m[4])][0]; d = s.ss[b['destinationSpreadsheetId']]; n = json.loads(json.dumps(h['p'])); n.update(sheetId=next(s.sid), title='Copy of ' + n['title'], index=len(d['sh']))
      d['sh'].append({'p': n, 'c': dict(h['c'])}); return s.reply(n)
    if m[0].endswith(':batchUpdate'):
      for r in b['requests']:
        (k, v), = r.items()
        if k == 'updateSpreadsheetProperties': x['t'] = v['properties']['title']
        elif k == 'addSheet': x['sh'].insert(v['properties']['index'], s.sh(v['properties']['title'], 0))
        elif k == 'deleteSheet': x['sh'] = [z for z in x['sh'] if z['p']['sheetId'] != v['sheetId']]
        else:
          pr = v['properties']; h = [z for z in x['sh'] if z['p']['sheetId'] == pr['sheetId']][0]; h['p']['title'] = pr.get('title', h['p']['title']); h['p']['gridProperties'].update(pr.get('gridProperties', {}))
          if 'index' in pr: x['sh'].remove(h); x['sh'].insert(pr['index'] if pr['index'] <= h['p']['index'] else pr['index'] - 1, h)
        for i, z in enumerate(x['sh']): z['p']['index'] = i
      return s.reply({'replies': [{} for _ in b['requests']]})
    return s.reply({'properties': {'title': x['t']}, 'sheets': [{'properties': dict(z['p'])} for z in x['sh']]})
  def drive(s, p, method, q, b, headers, body):
    if p.startswith('/upload'):
      s.out['upload'] = (headers.get('content-type', '').split(';')[0], re.findall(rb'\x22name\x22: ?\x22([^\x22]*)\x22', body)[:1], len(body)); return s.reply({'id': s.new(s.out['upload'][1][0].decode())})
    if p.endswith('/export'):
      fid = p.split('/')[4]; s.out['export'] = (fid, q['mimeType'][0]); return httplib2.Response({'status': '200', 'content-type': q['mimeType'][0]}), b'EXPORT:' + fid.encode() + b':' + q['mimeType'][0].encode()
    if p == '/drive/v3/files' and method == 'GET': return s.reply({'files': [{'id': i, 'name': v['t']} for i, v in s.ss.items()]})
    fid = p.split('/')[4]
    if method == 'PATCH': s.ss[fid]['trashed'] = b['trashed']; return s.reply({'id': fid})
    del s.ss[fid]; return httplib2.Response({'status': '204'}), b''
def install():
  g = G(); ezsheets.SHEETS_SERVICE = build('sheets', 'v4', http=g, static_discovery=True); ezsheets.DRIVE_SERVICE = build('drive', 'v3', http=g, static_discovery=True); ezsheets.IS_INITIALIZED = True; ezsheets.IGNORE_QUOTA = True; return g'''
PRE = FAKE + "\nimport os, tempfile, csv, sys\nFIX = os.environ.get('CH15_FIX') or next((p for p in (os.path.join(d, '08-tooling', 'ch15-page', 'fixtures') for d in [os.getcwd()] + list(__import__('pathlib').Path(os.getcwd()).parents)) if os.path.isdir(p)), '')\ndef rows_of(name): return [r for r in csv.reader(open(os.path.join(FIX, name), newline='', encoding='utf-8'))]\nBC = rows_of('boringcoin_sheet_export_2026_10_01_v1_0_0.csv'); BEAN = rows_of('bean_count_sheet_export_2026_10_01_v1_0_0.csv')\nos.chdir(tempfile.mkdtemp())\ng = install()\ndef sh(expr):\n    print('>>>', expr); v = eval(expr, globals()); print(repr(v))\nPRODUCE = [['PRODUCE', 'COST PER POUND', 'POUNDS SOLD', 'TOTAL'], ['Potatoes', '0.86', '21.6', '18.58'], ['Okra', '2.26', '38.6', '87.24'], ['Fava beans', '2.69', '5.8', '15.6'], ['Watermelon', '0.66', '7.3', '4.82'], ['Garlic', '1.19', '10', '11.9'], ['Parsnips', '2.27', '14.5', '32.92'], ['Lemon', '1.29', '7', '9.03'], ['Celery', '3.07', '4.5', '13.82'], ['Okra', '2.26', '40', '90.4'], ['Garlic', '1.19', '6', '7.14']]\ndef produce():\n    ss = ezsheets.Spreadsheet(g.load('PRODUCE', 'produceSales3', PRODUCE)); g.log.clear(); return ss.sheets[0]\n"

# Project 11, Step 1 whole: the audit of the Boringcoin ledger, run on the CSV export of the real sheet [fixture]
PROJECT11AUDIT = PRE + "ss = ezsheets.Spreadsheet(g.load('BOR', 'Boringcoin', BC))\naccounts = {}  # Keys are names, and values are amounts.\n\n# Each row is a transaction. Loop over each one:\nfor row in ss.sheets[0].getRows():\n    sender, recipient, amount = row[0], row[1], int(row[2])\n    if sender == 'PRE-MINE':\n        # The 'PRE-MINE' sender invents money out of thin air.\n        accounts.setdefault(recipient, 0)\n        accounts[recipient] += amount\n    else:\n        # Move funds from the sender to the recipient.\n        accounts.setdefault(sender, 0)\n        accounts.setdefault(recipient, 0)\n        accounts[sender] -= amount\n        accounts[recipient] += amount\nprint(accounts)\n\ntotal = 0\nfor amount in accounts.values():\n    total += amount\nprint('Total Boringcoins:', total)\nprint(len(BC), 'rows;', len(accounts), 'accounts;', sum(1 for r in BC if r[0] == 'PRE-MINE'), 'pre-mine rows')\n"

# Project 11, Step 2 whole: one transaction appended, with the chapter's arguments set in the first line [fixture]
PROJECT11TRANSACTION = PRE + "import sys\nsys.argv = ['addBoringcoinTransaction.py', 'Al Sweigart', 'Eve', '2000']\nif len(sys.argv) < 4:\n    print('Usage: python addBoringcoinTransaction.py sender recipient amount')\n    sys.exit()\n\n# Get the transaction info from the command line arguments:\nsender, recipient, amount = sys.argv[1:]\n\nss = ezsheets.Spreadsheet(g.load('BOR', 'Boringcoin', BC))\nsheet = ss.sheets[0]\n\n# Add one more row to the sheet for a new transaction:\nsheet.rowCount += 1\n\nsheet[1, sheet.rowCount] = sender\nsheet[2, sheet.rowCount] = recipient\nsheet[3, sheet.rowCount] = amount\nprint(len(BC), sheet.rowCount, sheet.getRow(sheet.rowCount)[:3], len(sheet.getRows()))\nprint([(m, p.rsplit('/', 1)[-1]) for m, p, q, b in g.log if m != 'GET'][-5:])\n"

# Practice program: the check of the Bean Count totals, run on the CSV export of the real sheet [fixture]
BEANCOUNT = PRE + "ss = ezsheets.Spreadsheet(g.load('BEAN', 'Bean Count', BEAN)); sheet = ss.sheets[0]\ng.log.clear()\nrows = sheet.getRows()\nbad = [n for n, r in enumerate(rows[1:], 2) if r[0] and int(r[0]) * int(r[1]) != int(r[2])]\nprint(len(rows), 'rows;', len(g.log), 'requests;', 'wrong totals at rows', bad)\nfor n in bad: print(rows[n - 1], int(rows[n - 1][0]) * int(rows[n - 1][1]))\n"

# Practice program: the email addresses of a response sheet (synthetic data) [synthetic]
FORMS = PRE + "ss = ezsheets.Spreadsheet(g.load('FORM', 'Form responses (synthetic)', [['Timestamp', 'Name', 'Email address'], ['10/1/2026 10:00:00', 'Ada', 'ada@example.org'], ['10/1/2026 10:05:00', 'Alan', 'alan@example.org']]))\nprint([e for e in ss.sheets[0].getColumn(3)[1:] if e])\n"

# Practice program: upload a file and download it in another format (the requests the library sends) [synthetic]
CONVERTER = PRE + "open('data.csv', 'w').write('a,b\\n1,2\\n')\nss = ezsheets.upload('data.csv'); name = ss.downloadAsExcel('data.xlsx')\nprint(g.out['upload'][0], g.out['upload'][1], g.out['export'][1], name)\n"

# The shell session of Spreadsheet Objects: title, id, url, sheetTitles, sheets, Sheet() [synthetic]
ATTRIBUTES = PRE + "example_ss = ezsheets.Spreadsheet(g.load('EXAMPLE', 'Sweigart Books (DO NOT DELETE)', [['TITLE', 'AUTHOR', 'YEAR PUBLISHED', 'URL']]))\nexample_ss.sheets[0].title = 'Books'\nss = ezsheets.Spreadsheet()\nexample_ss.sheets[0].copyTo(ss)\nss.sheets[0].delete()\nsh('ss.title'); ss.title = 'Sweigart Books'\nsh('ss.title'); sh('ss.sheetTitles'); sh('ss.sheets'); sh('ss[\\'Copy of Books\\']')\nsh('ss.Sheet(\\'New blank sheet\\')'); sh('ss.sheetTitles')\nss.sheets[1].delete(); sh('ss.sheetTitles')\nfor a in ('id', 'url', 'sheetTitles'):\n    try:\n        setattr(ss, a, 'x')\n    except AttributeError as e:\n        print(e)\nss.sheets = 'a plain attribute'; sh('ss.sheets')\n"

# The shell session of Creating, Moving, and Deleting Sheets: index, and what it refuses [synthetic]
SHEETMOVES = PRE + "ss = ezsheets.Spreadsheet(); ss.Sheet('Spam'); ss.Sheet('Eggs'); ss.Sheet('Bacon', 0)\nsh('ss.sheetTitles'); sh('ss.sheets[0].index'); ss.sheets[0].index = 2; sh('ss.sheetTitles'); ss.sheets[2].index = 0; sh('ss.sheetTitles')\nfor v in (9, -9, 'x'):\n    try:\n        ss.sheets[0].index = v\n    except Exception as e:\n        print(type(e).__name__, e)\nss.sheets[0].index = -1; sh('ss.sheetTitles')\n"

# The shell session of Reading and Writing Data on a ten-row stand-in of produceSales3.xlsx [synthetic]
ROWSCOLUMNS = PRE + 'sheet = produce()\nsh(\'sheet.getRow(1)\'); sh(\'sheet.getRow(2)\'); sh(\'sheet.getColumn(1)[:5]\'); sh("sheet.getColumn(\'A\') == sheet.getColumn(1)"); sh(\'sheet.getRow(3)\')\nvals = [\'Pumpkin\', \'11.50\', \'20\', \'230\']; sheet.updateRow(3, vals); sh(\'sheet.getRow(3)\'); sh(\'vals\')\ncolumnOne = sheet.getColumn(1)\nfor i, value in enumerate(columnOne):\n    columnOne[i] = value.upper()\ng.log.clear(); sheet.updateColumn(1, columnOne); print(len(g.log), g.log[0][3][\'majorDimension\']); sh(\'sheet.getColumn(1)[:4]\')\n'

# convertAddress, getColumnLetterOf and getColumnNumberOf, as typed in the chapter, with the errors [none]
ADDRESSES = PRE + 'sh("ezsheets.convertAddress(\'A2\')"); sh(\'ezsheets.convertAddress(1, 2)\'); sh(\'ezsheets.getColumnLetterOf(2)\'); sh("ezsheets.getColumnNumberOf(\'B\')")\nsh(\'ezsheets.getColumnLetterOf(999)\'); sh("ezsheets.getColumnNumberOf(\'ZZZ\')"); sh(\'ezsheets.convertAddress((2, 5))\'); sh("ezsheets.getColumnNumberOf(\'zz\')")\nfor f, a in ((ezsheets.getColumnLetterOf, 0), (ezsheets.getColumnLetterOf, \'A\'), (ezsheets.getColumnNumberOf, \'A1\'), (ezsheets.getColumnNumberOf, 5)):\n    try:\n        print(f(a))\n    except Exception as e:\n        print(f.__name__, repr(a), type(e).__name__)\n'

# The library's retry on RESOURCE_EXHAUSTED, with and without IGNORE_QUOTA, and another error [synthetic]
QUOTARETRY = PRE + "import time\nsleeps = []; time.sleep = sleeps.append\nfor flag in (False, True):\n    g = install(); ezsheets.IGNORE_QUOTA = flag; sleeps.clear(); g.fail = [(429, 'RESOURCE_EXHAUSTED')] * 20\n    try:\n        ezsheets.Spreadsheet()\n    except Exception as e:\n        print(flag, type(e).__name__, len(g.log), sleeps)\ng = install(); sleeps.clear(); g.fail = [(403, 'PERMISSION_DENIED')]\ntry:\n    ezsheets.Spreadsheet()\nexcept Exception as e:\n    print('403', type(e).__name__, len(g.log), sleeps)\n"

# How many requests a write, a read and a size change cost [synthetic]
REQUESTCOUNTS = PRE + "sheet = ezsheets.Spreadsheet().sheets[0]\ndef n(f):\n    g.log.clear(); f(); return sorted(x[0] + ' ' + ('values' if 'values' in x[1] else 'meta') for x in g.log)\nprint('100 writes, PUT requests:', n(lambda: [sheet.__setitem__((1, i), str(i)) for i in range(1, 101)]).count('PUT values'))\nprint('100 reads of a cell and 100 of a row, requests:', len(n(lambda: [(sheet[1, i], sheet.getRow(i)) for i in range(1, 101)])))\nprint(n(lambda: setattr(sheet, 'rowCount', sheet.rowCount + 1)))\nprint(n(lambda: setattr(sheet, 'title', 'T'))); print(n(sheet.refresh)); print(n(lambda: sheet.updateColumn(2, [str(i) for i in range(100)])))\n"

# A token file is a pickle: importing ezsheets loads it (a harmless marker stands in for code) [none]
TOKENPICKLE = 'import os, tempfile, pickle\nos.chdir(tempfile.mkdtemp())\nclass Evil:\n    def __reduce__(self): return (exec, ("open(\'PWNED.txt\', \'w\').write(\'ran\')",))\npickle.dump(Evil(), open(\'token-sheets.pickle\', \'wb\')); open(\'credentials-sheets.json\', \'w\').write(\'{}\')\nimport ezsheets\nprint(\'marker written by import:\', os.path.exists(\'PWNED.txt\'), \'| pickle protocol:\', pickle.DEFAULT_PROTOCOL)\n'

PROGRAMS = {
    'project11AuditBoringcoin_v1_0_0.py': (PROJECT11AUDIT, (), False),
    'project11AddTransaction_v1_0_0.py': (PROJECT11TRANSACTION, (), False),
    'practiceBeanCountCheck_v1_0_0.py': (BEANCOUNT, (), False),
    'practiceFormsEmails_v1_0_0.py': (FORMS, (), False),
    'practiceFormatConverter_v1_0_0.py': (CONVERTER, (), False),
    'spreadsheetAttributes_v1_0_0.py': (ATTRIBUTES, (), False),
    'movingSheets_v1_0_0.py': (SHEETMOVES, (), False),
    'rowsAndColumns_v1_0_0.py': (ROWSCOLUMNS, (), False),
    'addressesAndLetters_v1_0_0.py': (ADDRESSES, (), False),
    'quotaRetry_v1_0_0.py': (QUOTARETRY, (), False),
    'requestCounts_v1_0_0.py': (REQUESTCOUNTS, (), False),
    'tokenPickleRunsCode_v1_0_0.py': (TOKENPICKLE, (), False),
}
FIXTURE_BASED = ['project11AuditBoringcoin_v1_0_0.py', 'project11AddTransaction_v1_0_0.py', 'practiceBeanCountCheck_v1_0_0.py']

if __name__ == "__main__":
    # Usage: sen0414_ch15_corpus_base_v1_0_0.py   (run it with the interpreter that has ezsheets; exits 1 if a program does not exit 0)
    import os, subprocess, sys
    fix = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "08-tooling", "ch15-page", "fixtures")
    bad = 0
    for name, (code, needs, live) in PROGRAMS.items():
        env = dict(os.environ, CH15_FIX=fix); env.pop("BROWSER", None)
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=300, cwd=os.path.dirname(fix))
        bad += r.returncode != 0
        print("=== %s (exit %d)%s%s" % (name, r.returncode, " LIVE" if live else "", " FIXTURE" if name in FIXTURE_BASED else "")); print(r.stdout.rstrip()[:600]); print(r.stderr[-300:].rstrip())
    print("%d programs, %d did not exit 0" % (len(PROGRAMS), bad)); sys.exit(1 if bad else 0)
