#!/usr/bin/env python3
"""Chapter 15 (Google Sheets): runs the chapter's EZSheets programs, whole, under the given interpreter, against a stand-in for Google
that was written for this study, and writes or checks their recorded output.
Google's servers were not used by any program in this file. EZSheets reaches a Google account only after an OAuth consent in a browser,
and no account was available, so what was run is the real ezsheets 2026.4.28 (the newest release on 2026-10-12) with the real
google-api-python-client, which builds each request and reads each answer, and a stand-in at the HTTP layer (the class G below) that
answers the Sheets v4 and Drive v3 requests the library makes. The stand-in keeps every cell as text and does not parse a formula or a
number the way Google's USER_ENTERED option does, so nothing printed here says what Google answers; what is recorded is what the
library asks for (the requests it sends, in the stand-in's log) and what it does with an answer. A statement that depends on Google's
answer is NOT EXECUTED and is marked so in the data module. The Boringcoin sheet of Project 11 and the bean-count sheet are
read from the CSV exports in 08-tooling/ch15-page/fixtures (environment variable CH15_FIX); the produce sheet is a ten-row stand-in; the
real produceSales3.xlsx and the shipped scripts are run in sen0414_ch15_live_v1_0_0.py.
Usage: sen0414_ch15_thirdparty_v1_0_0.py write|check <python>
Record: 08-tooling/ch15-page/third_party_record_v1_0_0.json"""
__version__ = "1.0.0"
import json, os, subprocess, sys, tempfile
MODE, PY = sys.argv[1], sys.argv[2]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = os.path.join(REPO, "08-tooling", "ch15-page", "third_party_record_v1_0_0.json")
FIXDIR = os.path.join(REPO, "08-tooling", "ch15-page", "fixtures")
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
PRE = FAKE + r'''
import os, tempfile, csv, sys
FIX = os.environ.get('CH15_FIX') or next((p for p in (os.path.join(d, '08-tooling', 'ch15-page', 'fixtures') for d in [os.getcwd()] + list(__import__('pathlib').Path(os.getcwd()).parents)) if os.path.isdir(p)), '')
def rows_of(name): return [r for r in csv.reader(open(os.path.join(FIX, name), newline='', encoding='utf-8'))]
BC = rows_of('boringcoin_sheet_export_2026_10_01_v1_0_0.csv'); BEAN = rows_of('bean_count_sheet_export_2026_10_01_v1_0_0.csv')
os.chdir(tempfile.mkdtemp())
g = install()
def sh(expr):
    print('>>>', expr); v = eval(expr, globals()); print(repr(v))
PRODUCE = [['PRODUCE', 'COST PER POUND', 'POUNDS SOLD', 'TOTAL'], ['Potatoes', '0.86', '21.6', '18.58'], ['Okra', '2.26', '38.6', '87.24'], ['Fava beans', '2.69', '5.8', '15.6'], ['Watermelon', '0.66', '7.3', '4.82'], ['Garlic', '1.19', '10', '11.9'], ['Parsnips', '2.27', '14.5', '32.92'], ['Lemon', '1.29', '7', '9.03'], ['Celery', '3.07', '4.5', '13.82'], ['Okra', '2.26', '40', '90.4'], ['Garlic', '1.19', '6', '7.14']]
def produce():
    ss = ezsheets.Spreadsheet(g.load('PRODUCE', 'produceSales3', PRODUCE)); g.log.clear(); return ss.sheets[0]
'''
PROGS = [
("versions: the interpreter, ezsheets and what it installs with", r'''import sys, ezsheets, importlib.metadata as m
print(sys.version.split()[0]); print('ezsheets', ezsheets.__version__)
print(sorted(r.split()[0] for r in m.requires('ezsheets')))
md = m.metadata('ezsheets'); print(md['License'], md['Requires-Python'])
print(sorted(d.metadata['Name'] + ' ' + d.version for d in m.distributions() if d.metadata['Name'] in ('google-api-python-client', 'google-auth', 'google-auth-oauthlib', 'google-auth-httplib2', 'httplib2')))
'''),
("import ezsheets with no credentials file: no error at import, one at the first Spreadsheet()", r'''import os, tempfile
os.chdir(tempfile.mkdtemp())
import ezsheets
print('imported', ezsheets.__version__, 'initialised:', ezsheets.IS_INITIALIZED)
try:
    ezsheets.Spreadsheet()
except ezsheets.EZSheetsException as e:
    print(type(e).__name__, str(e)[:36])
'''),
("The API addresses the library builds its clients for", PRE + r'''print(ezsheets.SHEETS_SERVICE._baseUrl, ezsheets.DRIVE_SERVICE._baseUrl)
print(ezsheets.SCOPES_SHEETS); print(ezsheets.SCOPES_DRIVE)
'''),
("Creating a Spreadsheet and setting its title, as typed in the chapter's shell", PRE + r'''ss = ezsheets.Spreadsheet()
ss.title = 'Title of My New Spreadsheet'
sh('ss.title'); sh('ss.url'); sh('ss.id')
print([(m, p.split('/', 3)[-1], b) for m, p, q, b in g.log])
'''),
("Spreadsheet from a URL, from an id and from a title; the three forms of the chapter's listing", PRE + r'''g.load('1TzOJxhNKr15tzdZxTqtQ3EmDP6em_elnbtmZIcyu8vI', 'Education Data', [['TITLE', 'AUTHOR']])
ss2 = ezsheets.Spreadsheet('https://docs.google.com/spreadsheets/d/1TzOJxhNKr15tzdZxTqtQ3EmDP6em_elnbtmZIcyu8vI/')
ss3 = ezsheets.Spreadsheet('1TzOJxhNKr15tzdZxTqtQ3EmDP6em_elnbtmZIcyu8vI')
ss4 = ezsheets.Spreadsheet('Education Data')
sh('ss2 == ss3 == ss4'); sh('ss4.title')
print([(m, p, q) for m, p, q, b in g.log if p == '/drive/v3/files'])
'''),
("Spreadsheet by title: no match and two matches", PRE + r'''g.load('A1', 'Twin', [['x']]); g.load('A2', 'Twin', [['y']])
for name in ('Twin', 'Nothing'):
    try:
        ezsheets.Spreadsheet(name)
    except Exception as e:
        print(type(e).__name__, str(e)[:70])
'''),
("getIdFromUrl: how it cuts an id out of a URL", PRE + r'''import inspect
for u in ('https://docs.google.com/spreadsheets/d/1TzOJxhNKr15tzdZxTqtQ3EmDP6em_elnbtmZIcyu8vI/', 'https://docs.google.com/spreadsheets/d/1TzOJxhNKr15tzdZxTqtQ3EmDP6em_elnbtmZIcyu8vI', 'https://docs.google.com/spreadsheets/d/1TzOJxhNKr15tzdZxTqtQ3EmDP6em_elnbtmZIcyu8vI/edit#gid=0', 'https://docs.google.com/spreadsheets/u/3/d/1TzOJxhNKr15tzdZxTqtQ3EmDP6em_elnbtmZIcyu8vI/edit'):
    try:
        print(ezsheets.getIdFromUrl(u))
    except Exception as e:
        print(type(e).__name__, str(e)[:60])
src = inspect.getsource(ezsheets.Spreadsheet.__init__)
print('redirects followed for a URL that does not start with https://docs.google.com:', 'not spreadsheetId.lower().startswith(\'https://docs.google.com\')' in src)
print('http.client.HTTPConnection used:', 'http.client.HTTPConnection(' in src, '| HTTPSConnection used:', 'HTTPSConnection' in src, '| default port of HTTPConnection:', __import__('http.client').client.HTTPConnection('x').port)
'''),
("Uploading a file, listing spreadsheets, and the two errors of upload()", PRE + r'''open('my_spreadsheet.csv', 'w').write('a,b\n1,2\n'); open('notes.txt', 'w').write('x')
ss = ezsheets.upload('my_spreadsheet.csv')
print('name sent to Drive:', g.out['upload'][1][0].decode(), '| content type of the request:', g.out['upload'][0])  # the title Google stores is not known here
for name in ('missing.csv', 'notes.txt'):
    try:
        ezsheets.upload(name)
    except Exception as e:
        print(type(e).__name__, str(e).replace(os.getcwd(), '<cwd>')[:60])
'''),
("Attributes of a Spreadsheet after copying a sheet in, as typed in the chapter's shell", PRE + r'''example_ss = ezsheets.Spreadsheet(g.load('EXAMPLE', 'Sweigart Books (DO NOT DELETE)', [['TITLE', 'AUTHOR', 'YEAR PUBLISHED', 'URL']]))
example_ss.sheets[0].title = 'Books'
ss = ezsheets.Spreadsheet()
example_ss.sheets[0].copyTo(ss)
ss.sheets[0].delete()
sh('ss.title'); ss.title = 'Sweigart Books'
sh('ss.title'); sh('ss.sheetTitles'); sh('ss.sheets'); sh('ss[\'Copy of Books\']')
sh('ss.Sheet(\'New blank sheet\')'); sh('ss.sheetTitles')
ss.sheets[1].delete(); sh('ss.sheetTitles')
for a in ('id', 'url', 'sheetTitles'):
    try:
        setattr(ss, a, 'x')
    except AttributeError as e:
        print(e)
ss.sheets = 'a plain attribute'; sh('ss.sheets')
'''),
("refresh(): what it asks Google for", PRE + r'''ss = ezsheets.Spreadsheet(); ss.Sheet('Spam')
g.log.clear(); ss.refresh()
print([(m, p.split('/', 3)[-1][:40]) for m, p, q, b in g.log])
'''),
("The six download methods and the file names they give, as typed in the chapter's shell", PRE + r'''ss = ezsheets.Spreadsheet(g.load('EXAMPLE', 'Sweigart Books (DO NOT DELETE)', [['x']]))
for f in (ss.downloadAsExcel, ss.downloadAsODS, ss.downloadAsCSV, ss.downloadAsTSV, ss.downloadAsPDF, ss.downloadAsHTML):
    print(repr(f()), g.out['export'][1])
print(repr(ss.downloadAsExcel('a_different_filename.xlsx')))
print(sorted(os.listdir('.')))
print(ezsheets._makeFilenameSafe('a b/c:d*e?f<g>h|i'))
'''),
("downloadAs*: the file handle is not closed", PRE + r'''import warnings
ss = ezsheets.Spreadsheet()
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); ss.downloadAsCSV()
print([x.category.__name__ for x in w], str(w[0].message)[:30] if w else None)
'''),
("Deleting a spreadsheet: trash, then permanent, as typed in the chapter's shell", PRE + r'''ss = ezsheets.Spreadsheet(); ss.title = 'Delete me'
sh('list(ezsheets.listSpreadsheets().values())')
g.log.clear(); ss.delete()
print([(m, p.rsplit('/', 1)[0], b) for m, p, q, b in g.log])
sh('list(ezsheets.listSpreadsheets().values())')
print([q for m, p, q, b in g.log if m == 'GET' and p == '/drive/v3/files'][-1])
g.log.clear(); ss.delete(permanent=True)
print([(m, p.rsplit('/', 1)[0], b) for m, p, q, b in g.log])
sh('ezsheets.listSpreadsheets()')
'''),
("Sheets of a Spreadsheet: Sheet(), createSheet(), sheetTitles, as typed in the chapter's shell", PRE + r'''ss = ezsheets.Spreadsheet(); ss.title = 'Multiple Sheets'
sh('ss.sheetTitles'); sh("ss.Sheet('Spam')"); sh("ss.createSheet('Eggs')"); sh('ss.sheetTitles')
sh("ss.Sheet('Bacon', 0)"); sh('ss.sheetTitles'); sh('type(ss.sheets).__name__'); sh('len(ss)')
try:
    ss.sheets[0] = None
except TypeError as e:
    print(e)
'''),
("Moving sheets with index, as typed in the chapter's shell, and the values index refuses", PRE + r'''ss = ezsheets.Spreadsheet(); ss.Sheet('Spam'); ss.Sheet('Eggs'); ss.Sheet('Bacon', 0)
sh('ss.sheetTitles'); sh('ss.sheets[0].index'); ss.sheets[0].index = 2; sh('ss.sheetTitles'); ss.sheets[2].index = 0; sh('ss.sheetTitles')
for v in (9, -9, 'x'):
    try:
        ss.sheets[0].index = v
    except Exception as e:
        print(type(e).__name__, e)
ss.sheets[0].index = -1; sh('ss.sheetTitles')
'''),
("Deleting and clearing sheets, as typed in the chapter's shell", PRE + r'''ss = ezsheets.Spreadsheet(); ss.Sheet('Spam'); ss.Sheet('Eggs'); ss.Sheet('Bacon', 0)
ss.sheets[0].delete(); sh('ss.sheetTitles'); ss['Spam'].delete(); sh('ss.sheetTitles')
sheet = ss['Eggs']; sheet.delete(); sh('ss.sheetTitles')
ss.sheets[0]['A1'] = 'x'; g.log.clear(); ss.sheets[0].clear(); sh('ss.sheetTitles'); sh("ss.sheets[0]['A1']")
b = g.log[0][3]; print(g.log[0][0], g.log[0][1].rsplit('/', 1)[1], len(b['values']), len(b['values'][0]), len(json.dumps(b)))
try:
    ss.sheets[0].delete()
except ValueError as e:
    print(e)
'''),
("Reading and writing cells, as typed in the chapter's shell", PRE + r'''ss = ezsheets.Spreadsheet(); ss.title = 'My Spreadsheet'; sheet = ss.sheets[0]
sh('sheet.title'); sheet['A1'] = 'Name'; sheet['B1'] = 'Age'; sheet['C1'] = 'Favorite Movie'
sh("sheet['A1']"); sh("sheet['A2']"); sh('sheet[2, 1]')
sheet['A2'] = 'Alice'; sheet['B2'] = 30; sheet['C2'] = 'RoboCop'
sh("sheet['B2']"); sh("type(sheet['B2']).__name__")
g.log.clear(); sheet.refresh(); sh("sheet['B2']"); sh("sheet['a1']"); sh("sheet['ZZ999']")
print('requests of the refresh:', len([x for x in g.log if x[0] == 'GET']))
'''),
("What a write sends: range, valueInputOption and the body", PRE + r'''sheet = ezsheets.Spreadsheet().sheets[0]
g.log.clear(); sheet['B2'] = '=1+1'
m, p, q, b = g.log[-1]; print(m, p.rsplit('/', 1)[1], q, b)
'''),
("Addresses and column letters, as typed in the chapter's shell", PRE + r'''sh("ezsheets.convertAddress('A2')"); sh('ezsheets.convertAddress(1, 2)'); sh('ezsheets.getColumnLetterOf(2)'); sh("ezsheets.getColumnNumberOf('B')")
sh('ezsheets.getColumnLetterOf(999)'); sh("ezsheets.getColumnNumberOf('ZZZ')"); sh('ezsheets.convertAddress((2, 5))'); sh("ezsheets.getColumnNumberOf('zz')")
for f, a in ((ezsheets.getColumnLetterOf, 0), (ezsheets.getColumnLetterOf, 'A'), (ezsheets.getColumnNumberOf, 'A1'), (ezsheets.getColumnNumberOf, 5)):
    try:
        print(f(a))
    except Exception as e:
        print(f.__name__, repr(a), type(e).__name__)
'''),
("Round trip of column letters and numbers for 1 to 200000", PRE + r'''ok = all(ezsheets.getColumnNumberOf(ezsheets.getColumnLetterOf(n)) == n for n in range(1, 200001))
print(ok, ezsheets.getColumnLetterOf(200000), ezsheets.getColumnLetterOf(18279))
'''),
("Rows and columns of the produce sheet, as typed in the chapter's shell", PRE + r'''sheet = produce()
sh('sheet.getRow(1)'); sh('sheet.getRow(2)'); sh('sheet.getColumn(1)[:5]'); sh("sheet.getColumn('A') == sheet.getColumn(1)"); sh('sheet.getRow(3)')
vals = ['Pumpkin', '11.50', '20', '230']; sheet.updateRow(3, vals); sh('sheet.getRow(3)'); sh('vals')
columnOne = sheet.getColumn(1)
for i, value in enumerate(columnOne):
    columnOne[i] = value.upper()
g.log.clear(); sheet.updateColumn(1, columnOne); print(len(g.log), g.log[0][3]['majorDimension']); sh('sheet.getColumn(1)[:4]')
'''),
("Every row at once, as typed in the chapter's shell", PRE + r'''sheet = produce()
rows = sheet.getRows(); sh('rows[0]'); sh('rows[1]'); rows[1][0] = 'PUMPKIN'; sh('rows[10 - 1]')
rows[9][2] = '400'; rows[9][3] = '904'; sh('rows[9]')
g.log.clear(); sheet.updateRows(rows); print([(m, p.rsplit('/', 1)[1]) for m, p, q, b in g.log]); sh("sheet.getRow(10)"); sh('len(rows[0])')
'''),
("Sheet size, as typed in the chapter's shell, and what a smaller columnCount does to a cell outside", PRE + r'''sheet = produce(); sheet['F3'] = 'x'
sh('sheet.rowCount'); sh('sheet.columnCount'); sheet.columnCount = 4; sh('sheet.columnCount'); sh('len(sheet.getRow(3))'); sh("sheet['F3']")
sheet.refresh(); sh("sheet['F3']")
g.log.clear(); sheet.columnCount = 3; print([(m, p.rsplit('/', 1)[-1]) for m, p, q, b in g.log])
'''),
("Copying a sheet to another Spreadsheet, as typed in the chapter's shell", PRE + r'''ss1 = ezsheets.Spreadsheet(); ss1.title = 'First Spreadsheet'; ss1.sheets[0].title = 'Spam'
ss2 = ezsheets.Spreadsheet(); ss2.title = 'Second Spreadsheet'; ss2.sheets[0].title = 'Eggs'
sh('ss1[0]'); ss1[0].updateRow(1, ['Some', 'data', 'in', 'the', 'first', 'row'])
ss1[0].copyTo(ss2); sh('ss2.sheetTitles'); sh("ss2['Copy of Spam'].getRow(1)")
'''),
("Project 11, Step 1, whole (audit of the Boringcoin ledger), on the real export of the sheet", PRE + r'''ss = ezsheets.Spreadsheet(g.load('BOR', 'Boringcoin', BC))
accounts = {}  # Keys are names, and values are amounts.

# Each row is a transaction. Loop over each one:
for row in ss.sheets[0].getRows():
    sender, recipient, amount = row[0], row[1], int(row[2])
    if sender == 'PRE-MINE':
        # The 'PRE-MINE' sender invents money out of thin air.
        accounts.setdefault(recipient, 0)
        accounts[recipient] += amount
    else:
        # Move funds from the sender to the recipient.
        accounts.setdefault(sender, 0)
        accounts.setdefault(recipient, 0)
        accounts[sender] -= amount
        accounts[recipient] += amount
print(accounts)

total = 0
for amount in accounts.values():
    total += amount
print('Total Boringcoins:', total)
print(len(BC), 'rows;', len(accounts), 'accounts;', sum(1 for r in BC if r[0] == 'PRE-MINE'), 'pre-mine rows')
'''),
("Project 11, Step 2, whole (add a transaction), with the arguments of the chapter, on the real export", PRE + r'''import sys
sys.argv = ['addBoringcoinTransaction.py', 'Al Sweigart', 'Eve', '2000']
if len(sys.argv) < 4:
    print('Usage: python addBoringcoinTransaction.py sender recipient amount')
    sys.exit()

# Get the transaction info from the command line arguments:
sender, recipient, amount = sys.argv[1:]

ss = ezsheets.Spreadsheet(g.load('BOR', 'Boringcoin', BC))
sheet = ss.sheets[0]

# Add one more row to the sheet for a new transaction:
sheet.rowCount += 1

sheet[1, sheet.rowCount] = sender
sheet[2, sheet.rowCount] = recipient
sheet[3, sheet.rowCount] = amount
print(len(BC), sheet.rowCount, sheet.getRow(sheet.rowCount)[:3], len(sheet.getRows()))
print([(m, p.rsplit('/', 1)[-1]) for m, p, q, b in g.log if m != 'GET'][-5:])
'''),
("Project 11, Step 2 with the arguments unquoted or missing", PRE + r'''import shlex
for line in ('addBoringcoinTransaction.py "Al Sweigart" Eve 2000', 'addBoringcoinTransaction.py Al Sweigart Eve 2000', 'addBoringcoinTransaction.py Eve 2000'):
    sys.argv = shlex.split(line)
    if len(sys.argv) < 4:
        print('usage message'); continue
    try:
        sender, recipient, amount = sys.argv[1:]
        print((sender, recipient, amount))
    except ValueError as e:
        print(type(e).__name__, e)
'''),
("Two writers append to the Boringcoin sheet: the second one overwrites the row of the first", PRE + r'''ss = ezsheets.Spreadsheet(g.load('BOR', 'Boringcoin', BC[:4]))
a = ezsheets.Spreadsheet(ss.id).sheets[0]; b = ezsheets.Spreadsheet(ss.id).sheets[0]
for who, (s, r, n) in ((a, ('Al Sweigart', 'Eve', '2000')), (b, ('Eve', 'Bob', '5'))):
    who.rowCount += 1; who[1, who.rowCount] = s; who[2, who.rowCount] = r; who[3, who.rowCount] = n
fresh = ezsheets.Spreadsheet(ss.id).sheets[0]
print(fresh.rowCount, fresh.getRows()[4:])
'''),
("Project 11, Step 1 on a sheet with a trailing blank row", PRE + r'''ss = ezsheets.Spreadsheet(g.load('BOR', 'Boringcoin', BC[:4])); sheet = ss.sheets[0]; sheet.rowCount = 6
print(len(sheet.getRows()))
try:
    for row in ss.sheets[0].getRows():
        int(row[2])
except ValueError as e:
    print(type(e).__name__, e)
'''),
("Practice program: check the totals of the Bean Count sheet, on the real export", PRE + r'''ss = ezsheets.Spreadsheet(g.load('BEAN', 'Bean Count', BEAN)); sheet = ss.sheets[0]
g.log.clear()
rows = sheet.getRows()
bad = [n for n, r in enumerate(rows[1:], 2) if r[0] and int(r[0]) * int(r[1]) != int(r[2])]
print(len(rows), 'rows;', len(g.log), 'requests;', 'wrong totals at rows', bad)
for n in bad: print(rows[n - 1], int(rows[n - 1][0]) * int(rows[n - 1][1]))
'''),
("Practice program: read the email addresses of a Google Forms response sheet (synthetic)", PRE + r'''ss = ezsheets.Spreadsheet(g.load('FORM', 'Form responses (synthetic)', [['Timestamp', 'Name', 'Email address'], ['10/1/2026 10:00:00', 'Ada', 'ada@example.org'], ['10/1/2026 10:05:00', 'Alan', 'alan@example.org']]))
print([e for e in ss.sheets[0].getColumn(3)[1:] if e])
'''),
("Practice program: convert a CSV to a Google Sheet and back (the upload and the export request)", PRE + r'''open('data.csv', 'w').write('a,b\n1,2\n')
ss = ezsheets.upload('data.csv'); name = ss.downloadAsExcel('data.xlsx')
print(g.out['upload'][0], g.out['upload'][1], g.out['export'][1], name)
'''),
("Counting the requests: one per write, one per read, three for a size change", PRE + r'''sheet = ezsheets.Spreadsheet().sheets[0]
def n(f):
    g.log.clear(); f(); return sorted(x[0] + ' ' + ('values' if 'values' in x[1] else 'meta') for x in g.log)
print('100 writes, PUT requests:', n(lambda: [sheet.__setitem__((1, i), str(i)) for i in range(1, 101)]).count('PUT values'))
print('100 reads of a cell and 100 of a row, requests:', len(n(lambda: [(sheet[1, i], sheet.getRow(i)) for i in range(1, 101)])))
print(n(lambda: setattr(sheet, 'rowCount', sheet.rowCount + 1)))
print(n(lambda: setattr(sheet, 'title', 'T'))); print(n(sheet.refresh)); print(n(lambda: sheet.updateColumn(2, [str(i) for i in range(100)])))
'''),
("The size of the request that clear() sends", PRE + r'''ss = ezsheets.Spreadsheet(); sheet = ss.sheets[0]
g.log.clear(); sheet.clear(); small = len(json.dumps(g.log[0][3]))
sheet.resize(6, 23758); g.log.clear(); sheet.clear(); big = len(json.dumps(g.log[0][3]))
print(small, big, big < 2 * 1024 * 1024)
'''),
("Quota: the library's retry on RESOURCE_EXHAUSTED, with and without IGNORE_QUOTA, and another error", PRE + r'''import time
sleeps = []; time.sleep = sleeps.append
for flag in (False, True):
    g = install(); ezsheets.IGNORE_QUOTA = flag; sleeps.clear(); g.fail = [(429, 'RESOURCE_EXHAUSTED')] * 20
    try:
        ezsheets.Spreadsheet()
    except Exception as e:
        print(flag, type(e).__name__, len(g.log), sleeps)
g = install(); sleeps.clear(); g.fail = [(403, 'PERMISSION_DENIED')]
try:
    ezsheets.Spreadsheet()
except Exception as e:
    print('403', type(e).__name__, len(g.log), sleeps)
'''),
("Quota: the library's own throttle of 90 writes per 101 seconds, on a clock that advances 0.1 s per request", PRE + r'''import time
clock = [1000.0]; sleeps = []
ezsheets.time.time = lambda: clock[0]
def nap(s): sleeps.append(s); clock[0] += s
ezsheets.time.sleep = nap
ezsheets.IGNORE_QUOTA = False
print(ezsheets.WRITE_QUOTA, ezsheets.READ_QUOTA)
for i in range(120):
    ezsheets._logWriteRequest(); clock[0] += 0.1
print(len(sleeps), [round(s, 1) for s in sleeps][:3], round(clock[0] - 1000, 1))
'''),
("Dunder methods on sheets and spreadsheets: ==, in, find and update(None)", PRE + r'''ss1 = ezsheets.Spreadsheet(); ss2 = ezsheets.Spreadsheet(); ss3 = ezsheets.Spreadsheet(ss1.url)
print(ss1 == ss3, ss1 == ss2, ss1.sheets[0] == ss2.sheets[0], ss1.sheets[0] is ss3.sheets[0])
sheet = ss1.sheets[0]; sheet['A2'] = 'Alice'
print('Alice' in sheet, 'A2' in sheet, '1' in sheet, 12 in sheet)
print('find:', sheet.find('Alice'))
g.log.clear(); sheet.update('A2', None); print(repr(sheet['A2']), g.log[-1][3]['values'])
'''),
("updateRows grows the list the caller passed in", PRE + r'''sheet = ezsheets.Spreadsheet().sheets[0]
rows = [['a'], ['b']]; sheet.updateRows(rows); print(len(rows), len(rows[0]))
vals = ['x', 'y']; sheet.updateRow(1, vals); print(vals)
'''),
("A sheet title with a space or a quote in the range of a request", PRE + r'''ss = ezsheets.Spreadsheet(); sheet = ss.sheets[0]; sheet.title = 'My Sheet'
g.log.clear(); sheet['A1'] = 'x'; print(g.log[-1][1].rsplit('/', 1)[1])
import inspect; print([l.strip() for l in inspect.getsource(type(sheet).update).splitlines() if 'range' in l.lower()][:3])
'''),
("A stale OAuth token: refresh fails with invalid_grant (a local server plays Google's token endpoint)", r'''import os, tempfile, json
os.chdir(tempfile.mkdtemp())
json.dump({'installed': {'client_id': '1-x.apps.googleusercontent.com', 'project_id': 'p', 'auth_uri': 'https://accounts.google.com/o/oauth2/auth', 'token_uri': 'https://oauth2.googleapis.com/token', 'client_secret': 'S', 'redirect_uris': ['http://localhost']}}, open('client_secret_1-x.apps.googleusercontent.com.json', 'w'))
import pickle, threading, http.server, datetime
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(s):
        s.rfile.read(int(s.headers['content-length'])); s.send_response(400); s.send_header('content-type', 'application/json'); s.end_headers()
        s.wfile.write(json.dumps({'error': 'invalid_grant', 'error_description': 'Token has been expired or revoked.'}).encode())
    def log_message(s, *a): pass
srv = http.server.HTTPServer(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
from google.oauth2.credentials import Credentials
pickle.dump(Credentials(token='old', refresh_token='R', token_uri='http://127.0.0.1:%d/token' % srv.server_port, client_id='1-x', client_secret='S', expiry=datetime.datetime(2020, 1, 1)), open('token-sheets.pickle', 'wb'))
import ezsheets
try:
    ezsheets.init()
except Exception as e:
    print(type(e).__name__, e.args[0], '| sheets token kept:', os.path.exists('token-sheets.pickle'), '| drive token written:', os.path.exists('token-drive.pickle'))
'''),
("A token file is a pickle, and importing ezsheets loads it (a benign marker stands in for code)", r'''import os, tempfile, pickle
os.chdir(tempfile.mkdtemp())
class Evil:
    def __reduce__(self): return (exec, ("open('PWNED.txt', 'w').write('ran')",))
pickle.dump(Evil(), open('token-sheets.pickle', 'wb')); open('credentials-sheets.json', 'w').write('{}')
import ezsheets
print('marker written by import:', os.path.exists('PWNED.txt'), '| pickle protocol:', pickle.DEFAULT_PROTOCOL)
'''),
("Credentials file: none, one, several; and the defaults of init()", r'''import os, tempfile, inspect
os.chdir(tempfile.mkdtemp())
import ezsheets
print(inspect.signature(ezsheets.init))
for names in ((), ('client_secret_a.json', 'client_secret_b.json')):
    for n in names: open(n, 'w').write('{}')
    try:
        ezsheets.init()
    except ezsheets.EZSheetsException as e:
        print(len(names), str(e).replace(os.getcwd(), '<cwd>')[:80])
'''),
("A credentials file but no browser: the library raises when the first Spreadsheet is made", r'''import os, tempfile, json, webbrowser
os.chdir(tempfile.mkdtemp())
os.environ.pop('BROWSER', None)
json.dump({'installed': {'client_id': '1-x.apps.googleusercontent.com', 'project_id': 'p', 'auth_uri': 'https://accounts.google.com/o/oauth2/auth', 'token_uri': 'https://oauth2.googleapis.com/token', 'client_secret': 'S', 'redirect_uris': ['http://localhost']}}, open('client_secret_1-x.apps.googleusercontent.com.json', 'w'))
webbrowser.get = lambda *a, **k: (_ for _ in ()).throw(webbrowser.Error('could not locate runnable browser'))
import ezsheets
print('imported:', ezsheets.IS_INITIALIZED)
try:
    ezsheets.Spreadsheet()
except Exception as e:
    print(type(e).__name__, e)
'''),
("BROWSER=true with a credentials file: the import prints the authorization URL and waits on port 8080 (killed after the first line)", r'''import os, tempfile, json, subprocess, sys, socket, time, urllib.parse as up
os.chdir(tempfile.mkdtemp())
json.dump({'installed': {'client_id': '1-x.apps.googleusercontent.com', 'project_id': 'p', 'auth_uri': 'https://accounts.google.com/o/oauth2/auth', 'token_uri': 'https://oauth2.googleapis.com/token', 'client_secret': 'S', 'redirect_uris': ['http://localhost']}}, open('client_secret_1-x.apps.googleusercontent.com.json', 'w'))
def listening():
    s = socket.socket(); s.settimeout(2)
    try: s.connect(('127.0.0.1', 8080)); return True
    except OSError: return False
    finally: s.close()
before = listening()
p = subprocess.Popen([sys.executable, '-u', '-c', 'import ezsheets'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=dict(os.environ, BROWSER='true'))
line = p.stdout.readline().strip()
during = listening()
p.kill(); p.wait()
url = line[line.index('https://'):]
q = up.parse_qs(up.urlparse(url).query)
print(line[:line.index('https://')].strip(), '|', up.urlparse(url).netloc, q['redirect_uri'], q['code_challenge_method'], '| port 8080 before:', before, 'while the import waits:', during)
'''),
("The authorization URL the sign-in builds (client library, no network)", r'''import os, tempfile, json, urllib.parse as up
os.chdir(tempfile.mkdtemp())
json.dump({'installed': {'client_id': '1-x.apps.googleusercontent.com', 'project_id': 'p', 'auth_uri': 'https://accounts.google.com/o/oauth2/auth', 'token_uri': 'https://oauth2.googleapis.com/token', 'client_secret': 'S', 'redirect_uris': ['http://localhost']}}, open('c.json', 'w'))
from google_auth_oauthlib.flow import InstalledAppFlow
import ezsheets
f = InstalledAppFlow.from_client_secrets_file('c.json', ezsheets.SCOPES_SHEETS); f.redirect_uri = 'http://localhost:8080/'
url, state = f.authorization_url(); q = up.parse_qs(up.urlparse(url).query)
print(up.urlparse(url).netloc, sorted(q)); print(q['scope'], q['code_challenge_method'], q['access_type'], q['redirect_uri'])
'''),
("The raw REST request the library would send for one write (no network, no stand-in answer)", PRE + r'''req = ezsheets.SHEETS_SERVICE.spreadsheets().values().update(spreadsheetId='ABC', range='Sheet1!A1:B1', valueInputOption='RAW', body={'values': [['=1+1', '1/2']]})
print(req.method, req.uri); print(req.body); print(len(g.log))
'''),
("What the library does not close or check: pickle protocol, Python versions, release state", r'''import ezsheets, sys, importlib.metadata as m
md = m.metadata('ezsheets')
print(ezsheets.__version__, sys.version_info[:2], [c for c in md.get_all('Classifier') if 'Python ::' in c][-3:])
print(md['License'], md['Requires-Python'])
'''),
]
def run(code):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", CH15_FIX=FIXDIR)
    env.pop("PYTHONPATH", None); env.pop("BROWSER", None)
    r = subprocess.run([PY, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=600, cwd=tempfile.mkdtemp())
    return (r.stdout if r.returncode == 0 else r.stdout + "FAILED: " + (r.stderr.strip().splitlines() or ["?"])[-1]).rstrip("\n")
out = [{"what": w, "code": c, "output": run(c)} for w, c in PROGS]
if MODE == "write":
    json.dump({"_version": "1.0.0", "_note": "Recorded by sen0414_ch15_thirdparty_v1_0_0.py write; every output was printed by the program beside it under the interpreter named in the field python. No Google server was reached: the library ran against a stand-in at the HTTP layer (class G in each program, written for this study; it keeps cells as text and does not parse USER_ENTERED values), so an output shows what ezsheets asks for and what it does with an answer, not what Google answers. The Boringcoin and Bean Count data are the CSV exports of 2026-10-01 in ch15-page/fixtures.", "python": subprocess.run([PY, "-c", "import sys, ezsheets; print(sys.version.split()[0], 'ezsheets', ezsheets.__version__)"], capture_output=True, text=True, cwd=tempfile.mkdtemp()).stdout.strip(), "items": out}, open(REC, "w"), indent=1, ensure_ascii=False)
    print("recorded", len(out), "programs to", REC)
else:
    old = json.load(open(REC))["items"]; bad = [a["what"] for a, b in zip(old, out) if a["output"] != b["output"] or a["code"] != b["code"]]
    print("%d programs; %d differ" % (len(out), len(bad)))
    for b in bad: print("  DIFFERS", b)
    sys.exit(1 if bad else 0)
