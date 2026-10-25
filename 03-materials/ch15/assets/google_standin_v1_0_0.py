"""google_standin, version 1.0.0: a STAND-IN FOR GOOGLE for the chapter 15 deck (Google Sheets) and the page that runs the deck's examples.

Google was never reached. EZSheets reaches a Google account only after an OAuth consent in a browser, and no Google account, no consent and no cloud
project were available. This module therefore plays Google's answers at the HTTP layer: class G keeps every cell as TEXT, parses nothing (Google would
parse a typed value, a date or a formula) and answers the requests that the real ezsheets library and the real google-api-python-client build. So an
output shows what the library asks for and what it does with an answer, not what Google answers. install() plugs a new G into ezsheets and returns it.
g.load(id, title, rows) makes a spreadsheet with that id, title and rows; g.log lists the requests (method, path, query, body); g.fail holds
(status, name) answers to give next, for example (429, 'RESOURCE_EXHAUSTED'). uninstall() puts the library back into its state before any sign-in.
The text of class G and of install() is that of the stand-in of the earlier chapter 15 work (08-tooling/sen0414_ch15_rdodi_data_v1_0_2.py, FAKE), unchanged; uninstall() is new.
Needs: ezsheets 2026.4.28, google-api-python-client 2.201.0 (static discovery documents of sheets v4 and drive v3), httplib2."""
__version__ = "1.0.0"
# Speed patch (it changes no result): google-api-python-client writes a help text for every method of every resource it builds, which takes seconds in a browser's Python
# and is never printed by an example; the page of the earlier chapter 15 work skipped it the same way (08-tooling/ch15-page/pywheels_v1_0_0.json, boot_python).
import googleapiclient.schema as _schema
_schema.Schemas.prettyPrintSchema = lambda self, schema: ''
_schema.Schemas.prettyPrintByName = lambda self, name: ''
import json, re, itertools, urllib.parse as up, httplib2, ezsheets
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
  g = G(); ezsheets.SHEETS_SERVICE = build('sheets', 'v4', http=g, static_discovery=True); ezsheets.DRIVE_SERVICE = build('drive', 'v3', http=g, static_discovery=True); ezsheets.IS_INITIALIZED = True; ezsheets.IGNORE_QUOTA = True; return g
def uninstall():
  ezsheets.SHEETS_SERVICE = None; ezsheets.DRIVE_SERVICE = None; ezsheets.IS_INITIALIZED = False; ezsheets.IGNORE_QUOTA = False
