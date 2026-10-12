#!/usr/bin/env python3
"""Chapter 15 (Google Sheets): observes, once, what the public sources the chapter names answer today, runs the chapter's two projects as
the book ships them, and writes what it saw with the date. A web site changes and the files of the online materials may be replaced;
the record is an observation of the day, not something the build can re-check, and no check reads it.
What it does: fetches the chapter page and compares its SHA-256 with the digest the book's own ontology records; checks the statements
of the chapter that Google's pages can answer (the 250 new spreadsheets a day, the 10 million cells); downloads the online materials of
the 3rd edition and runs auditBoringcoin.py and addBoringcoinTransaction.py as they are shipped, unchanged, with the real ezsheets
(the library resolves https://autbor.com/boringcoin itself over plain HTTP, and the Google API behind it is the stand-in written for
this study, loaded with the CSV export of the real Boringcoin sheet fetched a moment earlier); reads the real produceSales3.xlsx; downloads the
source distributions of five ezsheets releases and compares them; counts what the 2019 documentation page names of the library;
sends the requests that need no Google account (the Sheets and Drive endpoints without credentials, the token endpoint with a made-up
client, the authorization page with the URL the library builds) and records the answers; and opens every source of the research record
and checks that the passages the research relies on are on the page. Nothing is posted to a Google account, no login or consent is
used, every URL is asked once. NOT EXECUTED here, because it needs a Google account and an OAuth consent: any request with credentials.
Run it with the interpreter that has ezsheets, openpyxl, requests and Beautiful Soup, with pdftotext (poppler) installed.
Usage: sen0414_ch15_live_v1_0_0.py   -> ch15-page/live_observations_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, difflib, hashlib, io, json, os, re, subprocess, sys, tarfile, tempfile, zipfile
import requests, bs4, openpyxl
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "08-tooling", "ch15-page", "live_observations_v1_0_0.json")
FIXDIR = os.path.join(REPO, "08-tooling", "ch15-page", "fixtures")
UA = {"User-Agent": "SEN0414-research/1.0 (teaching; altunel.yusuf@gmail.com)"}
BROWSER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0"}
obs = []
def see(what, f):
    try: v = f()
    except Exception as e: v = "raised %s: %s" % (type(e).__name__, str(e)[:200])
    obs.append({"what": what, "saw": v})
def get(u, **k):
    k.setdefault("headers", UA)
    return requests.get(u, timeout=90, **k)
def sha(b): return hashlib.sha256(b).hexdigest()
def norm(t): return re.sub(r"\s+", " ", t)
WORK = tempfile.mkdtemp()
PY = sys.executable
FAKE = re.search(r"FAKE = r'''(.*?)'''\n", open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sen0414_ch15_thirdparty_v1_0_0.py"), encoding="utf-8").read(), re.S).group(1)
BORING_ID, BEAN_ID, BOOKS_ID = "1sVCG1b3pfOAzuaFItLj4I8aN8kjvVDO0S78SIP1KNZQ", "1jDZEdvSIh4TmZxccyy0ZXrH-ELlrwq8_YYiZrEOB4jg", "1TzOJxhNKr15tzdZxTqtQ3EmDP6em_elnbtmZIcyu8vI"

# 1. the chapter and the book's own record of it
ch = get("https://automatetheboringstuff.com/3e/chapter15.html")
DIGEST = "76d2dc655b248a48921855f81131b8e4eee296340ed77ae0423cd48b11166d1b"
ONTO = "/home/claude/Ontologies/automate-python-book-3e/01-ontologies/automate_python_3e_ch15_v1_0_0.ttl"
see("chapter 15 page: status, bytes, SHA-256, equal to the chapterDigest of the book ontology (read from its file when present)", lambda: [ch.status_code, len(ch.content), sha(ch.content), sha(ch.content) == DIGEST, (DIGEST in open(ONTO).read()) if os.path.exists(ONTO) else "ontology file not on this machine"])
soup = bs4.BeautifulSoup(ch.text, "html.parser"); text = norm(soup.get_text(" "))
see("chapter 15 page: number of listings (pre elements), figures, tables, and the figure image files with the HTTP status of each", lambda: [len(soup.find_all("pre")), len(soup.select("figure")), len(soup.find_all("table")), [(i["src"], get("https://automatetheboringstuff.com/3e/" + i["src"]).status_code) for i in soup.select("figure img")]])
see("chapter 15 page: alt text of the pictures (Figure 15-2 names A1 as AI)", lambda: [i.get("alt") for i in soup.select("figure img")])
see("chapter 15 page: the statements checked against Google's pages (each is on the page of the book: True)", lambda: {s: (s in text) for s in ("250 new spreadsheets a day", "up to 10 million cells", "two token JSON files", "token-sheets .pickle", "Generating token files is a one-time setup step", "you have to perform this setup only once", "Quota exceeded for quota group", "a few hundred requests per minute", "a new Google account")})
ext = sorted({a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http") and "automatetheboringstuff.com" not in a["href"]})
def link_status():
    out = []
    for u in ext:
        try:
            r = requests.get(u, timeout=60, headers=BROWSER, allow_redirects=False); out.append([u, r.status_code, r.headers.get("Location", "")[:100]])
        except Exception as e: out.append([u, "unreachable: %s" % type(e).__name__, ""])
    return out
see("chapter 15 page: every external link of the chapter, asked once without following a redirect: URL, HTTP status, Location", link_status)

# 2. the short links the projects use, over HTTP and HTTPS
def short(u):
    out = []
    for scheme in ("http", "https"):
        r = requests.get(scheme + "://" + u, timeout=60, headers=UA, allow_redirects=False); out.append([scheme, r.status_code, r.headers.get("Location")])
    return out
see("autbor.com/boringcoin asked over http and over https without following: status and Location", lambda: short("autbor.com/boringcoin"))
see("autbor.com/examplegs asked over http and over https without following: status and Location", lambda: short("autbor.com/examplegs"))

# 3. the public sheets as CSV
def export(i):
    return get("https://docs.google.com/spreadsheets/d/%s/export?format=csv" % i)
bc, bean, books = export(BORING_ID), export(BEAN_ID), export(BOOKS_ID)
FB = open(os.path.join(FIXDIR, "boringcoin_sheet_export_2026_10_01_v1_0_0.csv"), "rb").read(); FN = open(os.path.join(FIXDIR, "bean_count_sheet_export_2026_10_01_v1_0_0.csv"), "rb").read()
see("Boringcoin sheet exported as CSV today: status, bytes, SHA-256, identical to the committed export of 2026-10-01, lines", lambda: [bc.status_code, len(bc.content), sha(bc.content), bc.content == FB, bc.content.count(b"\n")])
see("Bean Count sheet exported as CSV today: status, bytes, SHA-256, identical to the committed export of 2026-10-01, lines", lambda: [bean.status_code, len(bean.content), sha(bean.content), bean.content == FN, bean.content.count(b"\n")])
see("Sweigart Books sheet (autbor.com/examplegs) exported as CSV today: status, bytes, header and first row", lambda: [books.status_code, len(books.content), books.text.splitlines()[0], books.text.splitlines()[1][:80]])

# 4. the online materials and the two shipped scripts
Z = get("https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip", headers=BROWSER)
see("online materials zip of the 3rd edition: status, bytes, SHA-256", lambda: [Z.status_code, len(Z.content), sha(Z.content)])
zf = zipfile.ZipFile(io.BytesIO(Z.content)); MAT = os.path.join(WORK, "mat"); os.makedirs(MAT)
base = "Automate_the_Boring_Stuff_3e_onlinematerials/"
for n in ("auditBoringcoin.py", "addBoringcoinTransaction.py", "produceSales3.xlsx"):
    open(os.path.join(MAT, n), "wb").write(zf.read(base + n))
see("online materials: the files of chapter 15 with size, date inside the zip and SHA-256", lambda: [[n, zf.getinfo(base + n).file_size, "%04d-%02d-%02d" % zf.getinfo(base + n).date_time[:3], sha(zf.read(base + n))] for n in ("auditBoringcoin.py", "addBoringcoinTransaction.py", "produceSales3.xlsx")])
PATCH = "import http.client\n_r = http.client.HTTPConnection.request\ndef _q(self, method, url, body=None, headers={}, **kw): return _r(self, method, url, body, dict(headers, Accept='*/*'), **kw)\nhttp.client.HTTPConnection.request = _q\n"
def shipped(script, argv, patch=False):
    code = FAKE + ("\n" + PATCH if patch else "") + "\nimport runpy, sys\ng = install()\nrows = [r for r in __import__('csv').reader(open(%r, newline='', encoding='utf-8'))]\ng.load(%r, 'Boringcoin', rows)\nsys.argv = %r\nrunpy.run_path(%r, run_name='__main__')\nprint('requests to the stand-in:', [(m, p.rsplit('/', 1)[-1]) for m, p, q, b in g.log if m != 'GET'][-5:], '| rows now:', g.ss[%r]['sh'][0]['p']['gridProperties']['rowCount'])\n" % (os.path.join(WORK, "bc.csv"), BORING_ID, [script] + argv, os.path.join(MAT, script), BORING_ID)
    r = subprocess.run([PY, "-W", "ignore", "-c", code], capture_output=True, text=True, cwd=tempfile.mkdtemp(), timeout=300)
    return [r.returncode, r.stdout[-1400:], r.stderr.strip().splitlines()[-1:] if r.returncode else ""]
open(os.path.join(WORK, "bc.csv"), "wb").write(bc.content)
def header_effect():
    import http.client
    out = {}
    for name, hdr in (("default headers of http.client (none beyond Host and Accept-Encoding)", {}), ("with an Accept header", {"Accept": "*/*"}), ("with a User-Agent", {"User-Agent": "x"})):
        st = []
        for _ in range(10):
            c = http.client.HTTPConnection("autbor.com"); c.request("GET", "/boringcoin", headers=hdr); r = c.getresponse(); st.append(r.status); r.read()
        out[name] = {str(s): st.count(s) for s in sorted(set(st))}
    return out
see("autbor.com/boringcoin asked ten times by http.client the way ezsheets asks (plain HTTP, GET, no User-Agent), with an Accept header, and with a User-Agent: count of each status", header_effect)
def attempts(script, argv, patch=False, n=5):
    rs = [shipped(script, argv, patch) for _ in range(n)]
    ok = [r for r in rs if r[0] == 0]
    return {"attempts": n, "exit_codes": [r[0] for r in rs], "errors_seen": sorted({r[2][0] for r in rs if r[0]}), "first_success": ok[0][1] if ok else None}
open(os.path.join(WORK, "bc.csv"), "wb").write(bc.content)
see("auditBoringcoin.py as shipped, unchanged, real ezsheets (it follows autbor.com/boringcoin itself over plain HTTP), Google behind it the stand-in loaded with today's export: five runs, exit codes, the errors, the output of the first success", lambda: attempts("auditBoringcoin.py", []))
see("the same with http.client.HTTPConnection.request patched in memory to send an Accept header (the shipped script and the library files untouched): five runs", lambda: attempts("auditBoringcoin.py", [], True))
see("addBoringcoinTransaction.py as shipped, with the arguments of the chapter and the Accept patch: five runs, exit codes, output of the first success (the writes go to the stand-in)", lambda: attempts("addBoringcoinTransaction.py", ["Al Sweigart", "Eve", "2000"], True))
see("addBoringcoinTransaction.py as shipped, with no arguments: exit code and output", lambda: shipped("addBoringcoinTransaction.py", []))
def produce():
    wb = openpyxl.load_workbook(os.path.join(MAT, "produceSales3.xlsx"), data_only=True); ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    return {"sheet": ws.title, "rows": ws.max_row, "columns": ws.max_column, "row1": rows[0], "row2": rows[1], "row3": rows[2], "row11": rows[10], "chapter_rows_10": "['OKRA', '2.26', '40', '90.4', '', '']",
            "note": "the xlsx has %d columns; the chapter prints 6 after the upload to Google Sheets, which is not executed here" % ws.max_column}
see("produceSales3.xlsx of the online materials read with openpyxl (cached values): shape and the rows the chapter prints", produce)

# 5. the library's releases
J = get("https://pypi.org/pypi/ezsheets/json").json()
see("ezsheets on PyPI: latest version, licence, requires-python, dependencies, number of releases, first and last upload date", lambda: [J["info"]["version"], J["info"]["license"], J["info"]["requires_python"], J["info"]["requires_dist"], len(J["releases"]), min(f["upload_time"] for fs in J["releases"].values() for f in fs)[:10], max(f["upload_time"] for fs in J["releases"].values() for f in fs)[:10]])
def sdist(v):
    f = [x for x in J["releases"][v] if x["packagetype"] == "sdist"][0]
    tf = tarfile.open(fileobj=io.BytesIO(requests.get(f["url"], timeout=120).content))
    name = [n for n in tf.getnames() if n.endswith("ezsheets/__init__.py")][0]
    return tf.extractfile(name).read().decode("utf-8").replace("\r\n", "\n"), f["upload_time"][:10], f["url"].rsplit("/", 1)[-1]
def releases():
    vs = ["2023.8.11", "2024.8.8", "2024.8.9", "2025.11.11", "2026.4.28"]; src = {v: sdist(v) for v in vs}; out = []; prev = None
    for v in vs:
        t, day, fn = src[v]
        d = [l for l in difflib.unified_diff(prev.splitlines(), t.splitlines(), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")] if prev else []
        out.append({"version": v, "uploaded": day, "file": fn, "init_sha256": sha(t.encode()), "changed_lines_vs_previous": len(d) if prev else None, "has_Spreadsheet_none_default": "def __init__(self, spreadsheetId=None)" in t, "has_Sheet_wrapper_without_return": ("def Sheet(self" in t and "self.createSheet(title, index, columnCount, rowCount)" in t and "return self.createSheet(" not in t), "converts_a_written_value_to_text_in_the_local_copy": "if isinstance(value, bool):\n                value = str(value).upper()" in t, "follows_redirects_with_HTTPConnection": "http.client.HTTPConnection(" in t, "diff_lines_other_than_version": [l for l in d if "__version__" not in l][:6] if prev else None})
        prev = t
    return out
see("source distributions of five ezsheets releases compared (CRLF normalised): upload day, hash of ezsheets/__init__.py, changed lines against the previous, and the markers the study relies on", releases)
def docsgap():
    import ezsheets
    t = norm(bs4.BeautifulSoup(get("https://ezsheets.readthedocs.io/en/latest/").text, "html.parser").get_text(" "))
    pub = sorted({n for n in dir(ezsheets.Spreadsheet) + dir(ezsheets.Sheet) + dir(ezsheets) if not n.startswith("_") and n[0].islower() and callable(getattr(ezsheets, n, None) or getattr(ezsheets.Spreadsheet, n, None) or getattr(ezsheets.Sheet, n, None))})
    return {"page_chars": len(t), "as_of": "as of November 2019" in t, "public_names_found_in_the_installed_module": len(pub), "named_on_the_page": [n for n in pub if re.search(r"\b%s\b" % n, t)], "not_named": [n for n in pub if not re.search(r"\b%s\b" % n, t)]}
see("2019 documentation page of ezsheets compared with the public names of the installed library", docsgap)

# 6. requests that need no Google account
def anon():
    out = {}
    r = requests.get("https://sheets.googleapis.com/v4/spreadsheets/%s" % BORING_ID, timeout=60); out["sheets_get_no_credentials"] = [r.status_code, r.json().get("error", {}).get("status")]
    r = requests.get("https://sheets.googleapis.com/v4/spreadsheets/%s?key=not-a-key" % BORING_ID, timeout=60); out["sheets_get_bad_key"] = [r.status_code, r.json().get("error", {}).get("status")]
    r = requests.get("https://www.googleapis.com/drive/v3/files", timeout=60); out["drive_files_list_no_credentials"] = [r.status_code, r.json().get("error", {}).get("status")]
    r = requests.post("https://oauth2.googleapis.com/token", data={"grant_type": "refresh_token", "refresh_token": "x", "client_id": "1-x.apps.googleusercontent.com", "client_secret": "S"}, timeout=60); out["token_endpoint_made_up_client"] = [r.status_code, r.json().get("error")]
    import googleapiclient, importlib.resources
    static = json.load(open(os.path.join(os.path.dirname(googleapiclient.__file__), "discovery_cache", "documents", "sheets.v4.json")))
    live = requests.get("https://sheets.googleapis.com/$discovery/rest?version=v4", timeout=60)
    out["discovery_document_sheets_v4"] = [live.status_code, live.json().get("revision") if live.ok else None, static.get("revision"), live.ok and live.json().get("revision") == static.get("revision")]
    from google_auth_oauthlib.flow import InstalledAppFlow
    import ezsheets
    cj = os.path.join(WORK, "c.json"); json.dump({"installed": {"client_id": "1-x.apps.googleusercontent.com", "project_id": "p", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "client_secret": "S", "redirect_uris": ["http://localhost"]}}, open(cj, "w"))
    f = InstalledAppFlow.from_client_secrets_file(cj, ezsheets.SCOPES_SHEETS); f.redirect_uri = "http://localhost:8080/"; url, _ = f.authorization_url()
    r = requests.get(url, timeout=60, allow_redirects=False); out["authorization_page_with_made_up_client"] = [r.status_code, r.headers.get("Location", "")[:90]]
    return out
see("endpoints that need no Google account, asked without credentials (NOT EXECUTED: any call with an OAuth token)", anon)

# 7. every source of the research record
SOURCES = [
    ('P01', 'https://automatetheboringstuff.com/3e/chapter15.html', ['EZSheets', 'Boringcoin', 'token-sheets', 'Practice Programs', 'Spreadsheets in the Trash folder are still listed']),
    ('P02', 'https://ezsheets.readthedocs.io/en/latest/', ['November 2019', 'EZSheets']),
    ('P03', 'https://pypi.org/pypi/ezsheets/json', ['2026.4.28', 'GPLv3', 'google-api-python-client']),
    ('P04', 'https://automatetheboringstuff.com/3e/', ['Google Sheets', 'Excel Spreadsheets']),
    ('P05', 'https://automatetheboringstuff.com/3e/appendixa.html', ['EZSheets', 'pip']),
    ('P06', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', ['672', 'Automate the Boring Stuff']),
    ('P07', 'https://developers.google.com/workspace/sheets/api/limits', ['300 per minute per project', 'Per minute per user per project', '429', 'exponential backoff', '2 MB']),
    ('P08', 'https://developers.google.com/workspace/sheets/api/guides/concepts', ['A1 notation', 'Single quotes are required for sheet names with spaces or special characters']),
    ('P09', 'https://developers.google.com/workspace/sheets/api/guides/values', ['USER_ENTERED', 'RAW', 'A1 notation']),
    ('P10', 'https://developers.google.com/workspace/sheets/api/guides/batchupdate', ['batchUpdate', 'updateSheetProperties']),
    ('P11', 'https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/update', ['valueInputOption']),
    ('P12', 'https://developers.google.com/workspace/sheets/api/reference/rest/v4/ValueInputOption', ['USER_ENTERED', 'RAW', 'as if the user typed']),
    ('P13', 'https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/get', ['valueRenderOption', 'FORMATTED_VALUE']),
    ('P14', 'https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.sheets/copyTo', ['destinationSpreadsheetId', 'sheetId']),
    ('P15', 'https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/batchUpdate', ['requests[]', 'batchUpdate']),
    ('P16', 'https://developers.google.com/workspace/sheets/api/scopes', ['drive.file', 'restricted', 'sensitive', 'https://www.googleapis.com/auth/spreadsheets']),
    ('P17', 'https://developers.google.com/workspace/sheets/api/quickstart/python', ['token.json', 'Python 3.10.7']),
    ('P18', 'https://developers.google.com/workspace/sheets/api/guides/performance', ['batch', 'fields']),
    ('P19', 'https://developers.google.com/workspace/sheets/api/guides/migration', ['v3', 'August 2, 2021']),
    ('P20', 'https://developers.google.com/workspace/drive/api/guides/ref-export-formats', ['text/csv', 'first-sheet only', 'application/pdf']),
    ('P21', 'https://developers.google.com/workspace/drive/api/reference/rest/v3/files/export', ['10 MB', 'mimeType']),
    ('P22', 'https://developers.google.com/workspace/drive/api/reference/rest/v3/files/list', ['trashed', 'nextPageToken']),
    ('P23', 'https://developers.google.com/workspace/drive/api/guides/manage-uploads', ['multipart', 'uploadType']),
    ('P24', 'https://developers.google.com/workspace/drive/api/guides/delete', ['trash', 'permanently']),
    ('P25', 'https://developers.google.com/workspace/drive/api/guides/limits', ['May 1, 2026', 'quota']),
    ('P26', 'https://support.google.com/drive/answer/37603', ['20 million cells', '100MB']),
    ('P27', 'https://developers.google.com/workspace/guides/configure-oauth-consent', ['Branding', 'Audience', 'Data Access']),
    ('P28', 'https://developers.google.com/identity/protocols/oauth2', ['7 days', 'Testing', 'refresh token']),
    ('P29', 'https://developers.google.com/identity/protocols/oauth2/native-app', ['loopback', 'code_challenge']),
    ('P30', 'https://support.google.com/cloud/answer/15549945', ['100 test users', 'seven days']),
    ('P31', 'https://cloud.google.com/resource-manager/docs/creating-managing-projects', ['project ID', 'project number']),
    ('P32', 'https://support.google.com/docs/answer/2917686', ['spreadsheet', 'responses']),
    ('P33', 'https://googleapis.github.io/google-api-python-client/docs/', ['Google API Client Library for Python']),
    ('P34', 'https://pypi.org/pypi/google-api-python-client/json', ['google-api-python-client', 'Apache']),
    ('P35', 'https://pypi.org/pypi/google-auth-oauthlib/json', ['google-auth-oauthlib']),
    ('P36', 'https://pypi.org/pypi/google-auth/json', ['google-auth']),
    ('P37', 'https://pypi.org/pypi/gspread/json', ['gspread']),
    ('P38', 'https://docs.gspread.org/en/latest/', ['gspread', 'Google Sheets']),
    ('P39', 'https://docs.python.org/3.14/library/pickle.html', ['not secure', 'Never unpickle']),
    ('P40', 'https://docs.python.org/3.14/library/csv.html', ['csv', 'newline']),
    ('P41', 'https://docs.python.org/3.14/library/shlex.html', ['split']),
    ('P42', 'https://docs.python.org/3.14/library/http.client.html', ['HTTPConnection', '80']),
    ('P43', 'https://docs.python.org/3.14/library/webbrowser.html', ['get', 'BROWSER']),
    ('P44', 'https://docs.python.org/3.14/library/exceptions.html', ['ValueError', 'IndexError']),
    ('P45', 'https://docs.python.org/3.14/library/warnings.html', ['ResourceWarning']),
    ('P46', 'https://docs.python.org/3.14/reference/datamodel.html', ['__contains__', '__eq__']),
    ('P47', 'https://docs.python.org/3.14/whatsnew/3.14.html', ['3.14']),
    ('P48', 'https://www.rfc-editor.org/rfc/rfc6749.txt', ['authorization code', 'refresh token']),
    ('P49', 'https://www.rfc-editor.org/rfc/rfc8252.txt', ['loopback', 'external user-agent']),
    ('P50', 'https://www.rfc-editor.org/rfc/rfc7636.txt', ['S256', 'code_verifier']),
    ('P51', 'https://oauth.net/about/introduction/', ['Blaine Cook', '2006']),
    ('P52', 'https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html', ['deserialization', 'untrusted']),
    ('P53', 'https://cwe.mitre.org/data/definitions/502.html', ['Deserialization of Untrusted Data']),
    ('P54', 'https://en.wikipedia.org/wiki/Google_Sheets', ['XL2Web', '2006']),
    ('P55', 'https://en.wikipedia.org/wiki/Google_Forms', ['2008']),
    ('P56', 'https://bitcoin.org/bitcoin.pdf', ['double-spending', 'Peer-to-Peer']),
    ('P57', 'https://www.metzdowd.com/pipermail/cryptography/2008-October/014810.html', ['electronic cash', 'Satoshi Nakamoto']),
    ('P58', 'https://docs.google.com/spreadsheets/d/1sVCG1b3pfOAzuaFItLj4I8aN8kjvVDO0S78SIP1KNZQ/export?format=csv', ['PRE-MINE', 'Al Sweigart']),
    ('P59', 'https://docs.google.com/spreadsheets/d/1jDZEdvSIh4TmZxccyy0ZXrH-ELlrwq8_YYiZrEOB4jg/export?format=csv', ['BEANS PER JAR', 'TOTAL BEANS']),
    ('P60', 'https://docs.google.com/spreadsheets/d/1TzOJxhNKr15tzdZxTqtQ3EmDP6em_elnbtmZIcyu8vI/export?format=csv', ['TITLE', 'AUTHOR', 'YEAR PUBLISHED']),
]
def sources():
    out = []
    for pid, url, phrases in SOURCES:
        try:
            r = requests.get(url, timeout=60, headers=BROWSER if "nostarch.com" in url else UA); t = r.text
            ctype = r.headers.get("content-type", "")
            if "pdf" in ctype:
                p = os.path.join(WORK, pid + ".pdf"); open(p, "wb").write(r.content)
                t = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout
            elif "html" in ctype:
                s = bs4.BeautifulSoup(t, "html.parser")
                for x in s(["script", "style"]): x.decompose()
                t = s.get_text(" ")
            t = norm(t); out.append([pid, r.status_code, len(r.content), {p: (p.lower() in t.lower()) for p in phrases}])
        except Exception as e: out.append([pid, "unreachable: %s" % type(e).__name__, 0, {}])
    return out
see("every source of the research record opened: id, HTTP status, bytes, and whether each passage the research relies on is on the page", sources)
json.dump({"_version": "1.0.0", "observed": datetime.date.today().isoformat(), "with": "ezsheets %s, openpyxl %s, requests %s, beautifulsoup4 %s, Python %s" % (__import__("ezsheets").__version__, openpyxl.__version__, requests.__version__, bs4.__version__, sys.version.split()[0]),
           "_note": "Single requests made on the day named, through the build machine's proxy, to the public pages and files the chapter names. No Google account, no OAuth consent and no token was used, so nothing that needs one was executed. The shipped scripts ran with the real ezsheets and a stand-in for Google's API (see sen0414_ch15_thirdparty_v1_0_0.py). A record of one observation; web sites change and nothing re-checks it.",
           "items": obs}, open(OUT, "w"), indent=1, ensure_ascii=False)
print("observed", len(obs), "things on", datetime.date.today())
