#!/usr/bin/env python3
"""Chapter 15 study: runs the client-side code of the EZSheets library (release 2026.4.28, the newest on PyPI when read,
2026-10-01) against an in-memory stand-in for Google's servers, to check what the chapter prints and claims.
What is executed is the library's own Python code; what is NOT executed is anything on Google's side: the stand-in service
is written here (it keeps cells as text, trims trailing empty cells in a read, and numbers sheets), so a result that depends
on Google's behaviour is marked so in the chapter's data file. The library's Google client modules (apiclient,
google.auth, google_auth_oauthlib, googleapiclient) are replaced by empty stubs: no network is used once the source
distribution is downloaded. The library is licensed GPL-3.0; it is downloaded to a temporary folder, read and run there,
and not copied into the course repository.
Usage: sen0414_ch15_ezsheets_study_v1_0_0.py <python-interpreter-is-this-one>   Exits 1 when a stated result differs."""
__version__ = "1.0.0"
import hashlib, io, itertools, json, os, re, ssl, sys, tarfile, tempfile, types, urllib.request

URL = "https://files.pythonhosted.org/packages/13/b0/9b576e9d93ded6367c96ba9d3f3a9ec51c716f0d8c92edb25ae551e5ae05/ezsheets-2026.4.28.tar.gz"
SHA = "a7f6a9b1ee2dfd2eaa22945fcf0e3f927058e45bae70ece2a8dc53eeb054d161"
cafile = "/root/.ccr/ca-bundle.crt" if os.path.exists("/root/.ccr/ca-bundle.crt") else None
raw = urllib.request.urlopen(URL, timeout=60, context=ssl.create_default_context(cafile=cafile)).read()
assert hashlib.sha256(raw).hexdigest() == SHA, "the source distribution is not the one read"
tmp = tempfile.mkdtemp()
tarfile.open(fileobj=io.BytesIO(raw)).extractall(tmp, filter="data")
sys.path.insert(0, os.path.join(tmp, "ezsheets-2026.4.28", "src"))

def mod(name, **kw):
    m = types.ModuleType(name); m.__dict__.update(kw); sys.modules[name] = m; return m

class HttpError(Exception):
    def __init__(self, status, content): self.content = content; self.status = status

mod("apiclient"); mod("apiclient.http", MediaFileUpload=object, MediaIoBaseDownload=object)
mod("google"); mod("google.auth"); mod("google.auth.transport"); mod("google.auth.transport.requests", Request=object)
mod("google_auth_oauthlib"); mod("google_auth_oauthlib.flow", InstalledAppFlow=object)
mod("googleapiclient"); mod("googleapiclient.discovery", build=None); mod("googleapiclient.errors", HttpError=HttpError)
import ezsheets, time

class Req:
    def __init__(s, f): s.f = f
    def execute(s): return s.f()
class Chain:
    def __init__(s, **m): s.__dict__.update(m)

class Backend:
    """An in-memory stand-in for the Sheets and Drive services (written for this study)."""
    def __init__(s): s.ss = {}; s.ids = itertools.count(1); s.sids = itertools.count(1000); s.log = []
    def new(s, title):
        i = "ID%03d" % next(s.ids); s.ss[i] = {"title": title, "sheets": [s.mk("Sheet1", 0)], "trashed": False}; return i
    def mk(s, title, idx):
        return {"props": {"sheetId": next(s.sids), "title": title, "index": idx, "gridProperties": {"rowCount": 1000, "columnCount": 26}}, "cells": {}}
    def reindex(s, sp):
        for i, sh in enumerate(sp["sheets"]): sh["props"]["index"] = i
    def get(s, spreadsheetId):
        def f():
            s.log.append("get"); sp = s.ss[spreadsheetId]
            return {"properties": {"title": sp["title"]}, "sheets": [{"properties": json.loads(json.dumps(sh["props"]))} for sh in sp["sheets"]]}
        return Req(f)
    def batch(s, spreadsheetId, body):
        def f():
            s.log.append("batchUpdate"); sp = s.ss[spreadsheetId]
            for r in body["requests"]:
                (k, v), = r.items()
                if k == "updateSpreadsheetProperties": sp["title"] = v["properties"]["title"]
                elif k == "addSheet":
                    p = v["properties"]; sp["sheets"].insert(p["index"], s.mk(p["title"], p["index"])); s.reindex(sp)
                elif k == "updateSheetProperties":
                    p = v["properties"]; sh = [x for x in sp["sheets"] if x["props"]["sheetId"] == p["sheetId"]][0]
                    if "title" in p: sh["props"]["title"] = p["title"]
                    if "gridProperties" in p: sh["props"]["gridProperties"].update(p["gridProperties"])
                    if "index" in p:
                        old = sh["props"]["index"]; sp["sheets"].remove(sh)
                        sp["sheets"].insert(p["index"] if p["index"] <= old else p["index"] - 1, sh); s.reindex(sp)
                elif k == "deleteSheet":
                    sp["sheets"] = [x for x in sp["sheets"] if x["props"]["sheetId"] != v["sheetId"]]; s.reindex(sp)
            return {}
        return Req(f)
    def rng(s, r):
        t, a = r.rsplit("!", 1); m = re.match(r"([A-Z]+)(\d+):([A-Z]+)(\d+)", a)
        return t, ezsheets.getColumnNumberOf(m[1]), int(m[2]), ezsheets.getColumnNumberOf(m[3]), int(m[4])
    def vget(s, spreadsheetId, range, _r=range):
        def f():
            s.log.append("values.get"); t, c1, r1, c2, r2 = s.rng(range); sp = s.ss[spreadsheetId]
            sh = [x for x in sp["sheets"] if x["props"]["title"] == t][0]
            rows = [[sh["cells"].get((c, r), "") for c in _r(c1, c2 + 1)] for r in _r(r1, r2 + 1)]
            for r in rows:
                while r and r[-1] == "": r.pop()
            while rows and not rows[-1]: rows.pop()
            out = {"range": range, "majorDimension": "ROWS"}
            if rows: out["values"] = rows
            return out
        return Req(f)
    def vupd(s, spreadsheetId, range, valueInputOption, body):
        def f():
            s.log.append("values.update"); t, c1, r1, c2, r2 = s.rng(range); sp = s.ss[spreadsheetId]
            sh = [x for x in sp["sheets"] if x["props"]["title"] == t][0]
            for i, line in enumerate(body["values"]):
                for j, v in enumerate(line):
                    key = (c1 + j, r1 + i) if body["majorDimension"] == "ROWS" else (c1 + i, r1 + j)
                    sh["cells"][key] = "" if v is None else str(v)
            return {}
        return Req(f)
    def create(s, body):
        def f(): s.log.append("create"); return {"spreadsheetId": s.new(body["properties"]["title"])}
        return Req(f)
    def copyTo(s, spreadsheetId, sheetId, body):
        def f():
            s.log.append("copyTo"); src = s.ss[spreadsheetId]; sh = [x for x in src["sheets"] if x["props"]["sheetId"] == sheetId][0]
            d = s.ss[body["destinationSpreadsheetId"]]; n = json.loads(json.dumps(sh["props"])); n["sheetId"] = next(s.sids); n["title"] = "Copy of " + sh["props"]["title"]
            d["sheets"].append({"props": n, "cells": dict(sh["cells"])}); s.reindex(d); return {}
        return Req(f)

B = Backend()
ezsheets.SHEETS_SERVICE = Chain(spreadsheets=lambda: Chain(get=B.get, batchUpdate=B.batch, create=B.create,
    values=lambda: Chain(get=B.vget, update=B.vupd), sheets=lambda: Chain(copyTo=B.copyTo)))
ezsheets.IS_INITIALIZED = True
ezsheets.IGNORE_QUOTA = True  # only so that counting requests does not wait; the retry study below sets it explicitly
bad = []
def show(what, got, want):
    ok = got == want
    print(("ok  " if ok else "BAD ") + what + " -> " + repr(got))
    if not ok: bad.append((what, got, want))

# 1. cells and strings
ss = ezsheets.Spreadsheet(); sh = ss.sheets[0]
show("a new spreadsheet has the title and one sheet", (ss.title, ss.sheetTitles, type(ss.sheets).__name__), ("Untitled spreadsheet", ("Sheet1",), "tuple"))
show("default size of a new sheet", (sh.rowCount, sh.columnCount), (1000, 26))
sh["A1"] = "Name"; sh["B1"] = "Age"
show("A1, empty A2 and the (column, row) form of B1", (sh["A1"], sh["A2"], sh[2, 1]), ("Name", "", "Age"))
sh["B2"] = 30
show("a number just written is read back as given", sh["B2"], 30)
sh.refresh()
show("after a refresh it is the text the service keeps", sh["B2"], "30")
# 2. Sheet() versus createSheet()
r1 = ss.Sheet("Spam"); r2 = ss.createSheet("Eggs")
show("Spreadsheet.Sheet() returns / createSheet() returns", (r1, type(r2).__name__), (None, "Sheet"))
show("sheet titles in order", ss.sheetTitles, ("Sheet1", "Spam", "Eggs"))
ss.Sheet("Bacon", 0)
show("a sheet created at index 0", ss.sheetTitles, ("Bacon", "Sheet1", "Spam", "Eggs"))
ss.sheets[0].index = 2
show("moving index 0 to index 2", ss.sheetTitles, ("Sheet1", "Spam", "Bacon", "Eggs"))
ss.sheets[2].index = 0
show("moving index 2 back to 0", ss.sheetTitles, ("Bacon", "Sheet1", "Spam", "Eggs"))
ss.sheets[0].delete(); ss["Spam"].delete()
show("deleting by index and by title", ss.sheetTitles, ("Sheet1", "Eggs"))
ss["Eggs"].delete()
try: ss.sheets[0].delete(); got = "deleted"
except ValueError as e: got = str(e)
show("the last sheet cannot be deleted", got, "Cannot delete all sheets; spreadsheets must have at least one sheet")
ss.sheets[0].clear()
show("clear() keeps the sheet", ss.sheetTitles, ("Sheet1",))
# 3. rows, columns, padding and the caller's list
ss = ezsheets.Spreadsheet(); sh = ss.sheets[0]
vals = ["Pumpkin", "11.50", "20", "230"]
sh.updateRow(3, vals)
show("updateRow pads the caller's own list to the column count", (len(vals), vals[:5]), (26, ["Pumpkin", "11.50", "20", "230", ""]))
show("getRow(3) has one text per column", (len(sh.getRow(3)), sh.getRow(3)[:5]), (26, ["Pumpkin", "11.50", "20", "230", ""]))
col = sh.getColumn("A"); show("getColumn('A') has one text per row", (len(col), col[:3]), (1000, ["", "", "Pumpkin"]))
sh.columnCount = 4
show("setting columnCount = 4 cuts the row", (sh.columnCount, len(sh.getRow(3))), (4, 4))
B.log.clear(); sh.rowCount += 1
show("rowCount += 1 makes requests: reads then one write", (sorted(B.log), sh.rowCount), (["batchUpdate", "get", "values.get"], 1001))
B.log.clear(); sh[1, sh.rowCount] = "a"; sh[2, sh.rowCount] = "b"; sh[3, sh.rowCount] = "c"
show("three single-cell writes are three requests", B.log, ["values.update"] * 3)
B.log.clear(); sh.getRows(); sh.getColumn(1); sh["A1"]
show("reads from a loaded sheet make no request", B.log, [])
B.log.clear()
for i in range(1, 101): sh[1, i] = str(i)
show("100 single-cell writes are 100 requests", len(B.log), 100)
B.log.clear(); sh.updateColumn(2, [str(i) for i in range(1, 101)])
show("one updateColumn for 100 cells is one request", B.log, ["values.update"])
B.log.clear(); ss.refresh()
show("refresh of a one-sheet spreadsheet makes two reads", sorted(B.log), ["get", "values.get"])
errs = []
for f in (lambda: sh.getRow(0), lambda: sh[0, 1], lambda: sh.get("A0")):
    try: f(); errs.append("no error")
    except IndexError: errs.append("IndexError")
show("row 0 and column 0 raise IndexError", errs, ["IndexError"] * 3)
rows = [["a"], ["b"]]; B.log.clear(); sh.updateRows(rows)
show("updateRows grows the caller's list of rows to the sheet's size and pads each row", (len(rows), len(rows[0]), sh.columnCount, len(sh.getRows()), B.log), (sh.rowCount, sh.columnCount, sh.columnCount, sh.rowCount, ["values.update"]))
# 4. copy
ss2 = ezsheets.Spreadsheet(); ss2.sheets[0].title = "Eggs"; ss.sheets[0].title = "Spam"; ss.sheets[0].copyTo(ss2)
show("copyTo names the copy", ss2.sheetTitles, ("Eggs", "Copy of Spam"))
# 5. addresses and ids
show("convertAddress and column letters", (ezsheets.convertAddress("A2"), ezsheets.convertAddress(1, 2), ezsheets.getColumnLetterOf(999), ezsheets.getColumnNumberOf("ZZZ")), ((1, 2), "A2", "ALK", 18278))
def mine_letters(n):
    letters = ""
    while n > 0:
        n, r = divmod(n, 26)
        if r == 0:
            r = 26; n -= 1
        letters = chr(64 + r) + letters
    return letters
def mine_number(s):
    n = 0
    for ch in s.upper(): n = n * 26 + ord(ch) - 64
    return n
show("the course's column functions equal the library's for 1 to 200000", all(ezsheets.getColumnLetterOf(n) == mine_letters(n) and ezsheets.getColumnNumberOf(mine_letters(n)) == n == mine_number(mine_letters(n)) for n in range(1, 200001)), True)
ID = "1TzOJxhNKr15tzdZxTqtQ3EmDP6em_elnbtmZIcyu8vI"
show("getIdFromUrl with and without the closing slash", (ezsheets.getIdFromUrl("https://docs.google.com/spreadsheets/d/" + ID + "/edit#gid=0/"), ezsheets.getIdFromUrl("https://docs.google.com/spreadsheets/d/" + ID + "/"), ezsheets.getIdFromUrl("https://docs.google.com/spreadsheets/d/" + ID)), (ID, ID, ID[:-1]))
show("the file name made from a title", ezsheets._makeFilenameSafe("Sweigart Books (DO NOT DELETE)"), "Sweigart_Books_(DO_NOT_DELETE)")
# 6. quota errors
sleeps = []; real_sleep = time.sleep; time.sleep = sleeps.append; calls = []
def failing(spreadsheetId):
    def f(): calls.append(1); raise HttpError(429, json.dumps({"error": {"status": "RESOURCE_EXHAUSTED"}}).encode())
    return Req(f)
ezsheets.SHEETS_SERVICE = Chain(spreadsheets=lambda: Chain(get=failing))
for flag in (False, True):
    ezsheets.IGNORE_QUOTA = flag; sleeps.clear(); calls.clear()
    try: ezsheets._makeRequest("get", spreadsheetId="x"); got = "no error"
    except HttpError: got = "HttpError"
    show("quota error with IGNORE_QUOTA = %s: outcome, attempts, pauses in seconds" % flag, (got, len(calls), list(sleeps)), ("HttpError", 9, [10, 15, 20, 25, 30, 35, 40, 45]))
def notfound(spreadsheetId):
    def f(): calls.append(1); raise HttpError(404, json.dumps({"error": {"status": "NOT_FOUND"}}).encode())
    return Req(f)
ezsheets.SHEETS_SERVICE = Chain(spreadsheets=lambda: Chain(get=notfound)); sleeps.clear(); calls.clear()
try: ezsheets._makeRequest("get", spreadsheetId="x")
except HttpError: pass
show("another error is raised at once", (len(calls), list(sleeps)), (1, []))
time.sleep = real_sleep
show("the library's own throttle limits", (ezsheets.READ_QUOTA, ezsheets.WRITE_QUOTA), (90, 90))
print("%d differ" % len(bad))
sys.exit(1 if bad else 0)
