#!/usr/bin/env python3
"""Chapter 16 (SQLite Databases): observes, once, what the public sources the chapter names answer today, and writes what it saw with the
date. A web site changes and the files of the online materials may be replaced; the record is an observation of the day, not something
the build can re-check, and no check reads it.
What it does: fetches the chapter page and compares its SHA-256 with the digest the book's own ontology records; counts what is on the
page (listings, figures with the HTTP status of each image, tables) and asks every external link of the chapter once without following
a redirect; downloads the online materials of the 3rd edition and records the two database files in them; reads the newest SQLite
release and the SHA3-256 of the Linux tools bundle on sqlite.org, and downloads the bundle to check it; reads what the Python
documentation says of the sqlite3 module and which Python release it describes; opens the three GUI apps' pages the chapter names;
reads xkcd's strip 327; and opens every source of the research record and checks that the passages the research relies on are on the
page. Nothing is posted anywhere and every URL is asked once. NOT EXECUTED: installing or running the three GUI apps.
Run it with an interpreter that has requests and Beautiful Soup, with pdftotext (poppler) installed.
Usage: sen0414_ch16_live_v1_0_0.py   -> ch16-page/live_observations_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, hashlib, io, json, os, re, subprocess, sys, tempfile, zipfile
import requests, bs4
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "08-tooling", "ch16-page", "live_observations_v1_0_0.json")
UA = {"User-Agent": "SEN0414-research/1.0 (teaching; altunel.yusuf@gmail.com)"}
BROWSER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0"}
obs = []
def see(what, f):
    try: v = f()
    except Exception as e: v = "raised %s: %s" % (type(e).__name__, str(e)[:200])
    obs.append({"what": what, "saw": v})
def get(u, **k):
    k.setdefault("headers", BROWSER)
    return requests.get(u, timeout=90, **k)
def sha(b): return hashlib.sha256(b).hexdigest()
def norm(t): return re.sub(r"\s+", " ", t)
def visible(r):
    s = bs4.BeautifulSoup(r.text, "html.parser")
    for x in s(["script", "style"]): x.decompose()
    return norm(s.get_text(" "))
WORK = tempfile.mkdtemp()

# 1. the chapter and the book's own record of it
ch = get("https://automatetheboringstuff.com/3e/chapter16.html", headers=UA)
DIGEST = "b861ab3300b167a8ecb9c5882052315f3362cc74477f647462eb6d198b5b39a4"
ONTO = "/home/claude/Ontologies/automate-python-book-3e/01-ontologies/automate_python_3e_ch16_v1_0_0.ttl"
see("chapter 16 page: status, bytes, SHA-256, equal to the chapterDigest of the book ontology (read from its file when present)", lambda: [ch.status_code, len(ch.content), sha(ch.content), sha(ch.content) == DIGEST, (DIGEST in open(ONTO).read()) if os.path.exists(ONTO) else "ontology file not present"])
soup = bs4.BeautifulSoup(ch.text, "html.parser"); text = norm(soup.get_text(" "))
see("chapter 16 page: number of listings (pre elements), figure captions, tables, images and the HTTP status of each image file", lambda: [len(soup.find_all("pre")), sorted(set(re.findall(r"Figure 16-\d+", text))), len(soup.find_all("table")), [(i["src"], get("https://automatetheboringstuff.com/3e/" + i["src"]).status_code) for i in soup.find_all("img") if i.get("src")]])
see("chapter 16 page: alt text of the pictures", lambda: [i.get("alt") for i in soup.find_all("img")])
STATEMENTS = ("There are six data types in SQLite", "sqlite _version", "I have about 300 cats", "('Colin', '2016-12-24', 'siamese', 6.2)", "which is used by Python 3.11 and later", "has even passed tests that simulate the computer losing power", "SQLite is public domain software", "most widely deployed database software", "hundreds or thousands of simultaneous write operations", "sudo apt install sqlite3", "REFERENCES cats(rowid)", "REFERENCES meals (rowid)", "SQLite Studio (https://sqlitestudio.pl)")
see("chapter 16 page: statements the research relies on (each is on the page of the book: True)", lambda: {s: (norm(s) in text or norm(s) in norm(ch.text)) for s in STATEMENTS})
ext = sorted({a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http") and "automatetheboringstuff.com" not in a["href"]})
def link_status():
    out = []
    for u in ext:
        try:
            r = requests.get(u, timeout=60, headers=BROWSER, allow_redirects=False); out.append([u, r.status_code, r.headers.get("Location", "")[:100]])
        except Exception as e: out.append([u, "unreachable: %s" % type(e).__name__, ""])
    return out
see("chapter 16 page: every external link of the chapter, asked once without following a redirect: URL, HTTP status, Location", link_status)
plain = [m for m in re.findall(r"https?://[\w./?=&#%~:+-]+", text)]
see("chapter 16 page: every URL that appears in the text of the chapter, asked once (a status of 200 means the page the chapter names is there)", lambda: sorted({u.rstrip(".,)") for u in plain if "automatetheboringstuff.com/3e/chapter16" not in u}))

# 2. the online materials
mat = get("https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip")
see("online materials of the 3rd edition: status, bytes, SHA-256 of the zip", lambda: [mat.status_code, len(mat.content), sha(mat.content)])
def materials():
    z = zipfile.ZipFile(io.BytesIO(mat.content)); names = [n for n in z.namelist() if not n.endswith("/") and "/._" not in n and not n.split("/")[-1].startswith("._")]
    db = {n.split("/")[-1]: [len(z.read(n)), sha(z.read(n))] for n in names if n.endswith(".db")}
    return {"files": len(names), "databases": db, "entries naming sweigart, sql, sqlite, chapter16 or ch16": [n for n in names if re.search(r"sweigart|sql|chapter16|ch16", n, re.I)][:20]}
see("online materials: the files (without the macOS resource forks) and the database files with their sizes and SHA-256", materials)
def dbfacts():
    import sqlite3
    z = zipfile.ZipFile(io.BytesIO(mat.content)); p = os.path.join(WORK, "s.db"); open(p, "wb").write(z.read("Automate_the_Boring_Stuff_3e_onlinematerials/sweigartcats.db"))
    c = sqlite3.connect("file:" + p + "?mode=ro", uri=True)
    return [c.execute("SELECT count(*) FROM cats").fetchone()[0], c.execute("SELECT count(*) FROM vaccinations").fetchone()[0], c.execute("SELECT rowid, name, fur FROM cats WHERE rowid = 1").fetchone(), c.execute("SELECT rowid FROM cats WHERE name = 'Mango'").fetchone()[0], [r[0] for r in c.execute("SELECT sql FROM sqlite_schema ORDER BY rowid")]]
see("sweigartcats.db of the online materials: rows of cats and vaccinations, row 1, the rowid of Mango, the stored schema text", dbfacts)

# 3. SQLite itself
idx = get("https://www.sqlite.org/index.html", headers=UA)
see("sqlite.org home page: the latest release and its date", lambda: re.search(r"Version (\d+\.\d+\.\d+) \((\d{4}-\d\d-\d\d)\)", visible(idx)).groups())
dl = get("https://sqlite.org/download.html", headers=UA)
def tools():
    t = dl.text; m = re.search(r"(sqlite-tools-linux-x64-3540000\.zip)[^<]*?\(([\d.]+ \w+)\)\s*<?[^S]*?SHA3-256:\s*([0-9a-f]{64})", re.sub(r"<[^>]+>", " ", t), re.S)
    z = get("https://sqlite.org/2026/sqlite-tools-linux-x64-3540000.zip", headers=UA).content
    return [m.group(1), m.group(3) if m else None, hashlib.sha3_256(z).hexdigest(), len(z), bool(m) and hashlib.sha3_256(z).hexdigest() == m.group(3)]
see("sqlite.org download page: the Linux tools bundle, the SHA3-256 the page gives, the one computed on the download, the size, equal", tools)
see("sqlite.org: the pages that give the figures the research uses (largest database, the date of release 3.37.0, the rowid aliases)", lambda: {"limits: 281 terabytes": "281 terabytes" in visible(get("https://www.sqlite.org/limits.html", headers=UA)), "3.37.0 released 2021-11-27 with STRICT tables": "2021-11-27" in visible(get("https://sqlite.org/releaselog/3_37_0.html", headers=UA)), "rowid, oid, _rowid_": all(x in get("https://www.sqlite.org/rowidtable.html", headers=UA).text for x in ("oid", "_rowid_"))})

# 4. Python's documentation
py = get("https://docs.python.org/3.14/library/sqlite3.html", headers=UA)
pv = visible(py)
see("Python documentation of sqlite3: the release the page describes, the default of isolation_level in the signature, the sentence on closing, the first line of the iterdump entry", lambda: [re.search(r"Python » (3\.\d+\.\d+) Documentation", pv).group(1), re.search(r"isolation_level = '(\w+)'", pv).group(1), "ResourceWarning is emitted if close() is not called" in pv, "Return an iterator to dump the database as SQL source code" in pv])
see("Python documentation: the SQLite version a build of Python 3.14 needs", lambda: re.search(r"SQLite (\d+\.\d+\.\d+)", visible(get("https://docs.python.org/3.14/using/configure.html", headers=UA))).group(1))
pyd = get("https://www.python.org/downloads/", headers=UA)
see("python.org downloads page: the newest release it offers", lambda: re.findall(r"Download Python (3\.\d+\.\d+)", visible(pyd))[:3])

# 5. the apps the chapter names, the strip it does not
for name, u, needle in (("DB Browser for SQLite", "https://sqlitebrowser.org/", "DB4S"), ("SQLiteStudio", "https://sqlitestudio.pl/", "SQLiteStudio"), ("DBeaver Community", "https://dbeaver.io/", "DBeaver")):
    def app(u=u, needle=needle):
        r = get(u, headers=BROWSER); t = visible(r); title = bs4.BeautifulSoup(r.text, "html.parser").title
        return [r.status_code, title.get_text().strip() if title else None, needle in t, "formerly known as SQLiteStudio" in t, t[:200]]
    see("page of %s as the chapter names it: status, title, whether the name appears, whether it says 'formerly known as SQLiteStudio', the first 200 characters" % name, app)
see("xkcd 327 (info.0.json): number, date, title, alt text", lambda: (lambda j: [j["num"], "%s-%02d-%02d" % (j["year"], int(j["month"]), int(j["day"])), j["title"], j["alt"]])(get("https://xkcd.com/327/info.0.json", headers=UA).json()))

# 6. every source of the research record
SOURCES = [
    ('P01', 'https://automatetheboringstuff.com/3e/chapter16.html', ['There are six data types in SQLite', 'name LIKE', 'SQLite added the STRICT keyword in version 3.37.0']),
    ('P02', 'https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', []),
    ('P03', 'https://automatetheboringstuff.com/3e/', ['Chapter 16 - SQLite Databases']),
    ('P04', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', ['Automate the Boring Stuff with Python']),
    ('P05', 'https://nostarch.com/practical-sql-2nd-edition', ['Practical SQL']),
    ('P06', 'https://docs.python.org/3.14/library/sqlite3.html', ['autocommit', 'iterdump', 'sqlite_version']),
    ('P07', 'https://sqlite.org/docs.html', ['SQL Syntax', 'Pragmas']),
    ('P08', 'https://www.sqlite.org/datatype3.html', ['more general dynamic type system', 'Type Affinity']),
    ('P09', 'https://www.sqlite.org/stricttables.html', ['STRICT Tables', 'ANY']),
    ('P10', 'https://www.sqlite.org/lang_createtable.html', ['ROWIDs and the INTEGER PRIMARY KEY', 'IF NOT EXISTS']),
    ('P11', 'https://www.sqlite.org/foreignkeys.html', ['disabled by default (for backwards compatibility)', 'foreign key mismatch']),
    ('P12', 'https://www.sqlite.org/quirks.html', ['Double-quoted String Literals Are Accepted', 'Flexible Typing']),
    ('P13', 'https://www.sqlite.org/lang_expr.html', ['The LIKE, GLOB, REGEXP, MATCH', 'case-insensitive']),
    ('P14', 'https://www.sqlite.org/lang_altertable.html', ['ALTER TABLE RENAME COLUMN', 'ALTER TABLE DROP COLUMN']),
    ('P15', 'https://www.sqlite.org/lang_transaction.html', ['BEGIN IMMEDIATE', 'ROLLBACK']),
    ('P16', 'https://www.sqlite.org/lang_vacuum.html', ['may change the ROWIDs of entries in any tables that do not have an explicit INTEGER PRIMARY KEY']),
    ('P17', 'https://www.sqlite.org/autoinc.html', ['AUTOINCREMENT keyword imposes extra CPU, memory, disk space, and disk I/O overhead']),
    ('P18', 'https://www.sqlite.org/rowidtable.html', ['rowid table', 'unique']),
    ('P19', 'https://www.sqlite.org/inmemorydb.html', [':memory:', 'cache=shared']),
    ('P20', 'https://www.sqlite.org/wal.html', ['Write-Ahead Logging', 'readers do not block writers']),
    ('P21', 'https://www.sqlite.org/cli.html', ['.tables', '.dump']),
    ('P22', 'https://www.sqlite.org/whentouse.html', ['Client/Server', 'Application file format']),
    ('P23', 'https://www.sqlite.org/mostdeployed.html', ['more than all other database engines combined']),
    ('P24', 'https://www.sqlite.org/testing.html', ['power failure in the middle of a database update', 'Crash and power loss tests']),
    ('P25', 'https://www.sqlite.org/transactional.html', ['SQLite implements serializable transactions that are atomic, consistent, isolated, and durable']),
    ('P26', 'https://www.sqlite.org/atomiccommit.html', ['Atomic Commit In SQLite']),
    ('P27', 'https://www.sqlite.org/lockingv3.html', ['RESERVED', 'SHARED']),
    ('P28', 'https://www.sqlite.org/pragma.html', ['foreign_key_check', 'journal_mode']),
    ('P29', 'https://www.sqlite.org/lang_select.html', ['The LIMIT clause', 'The ORDER BY clause']),
    ('P30', 'https://www.sqlite.org/optoverview.html', ['The LIKE Optimization', 'built-in NOCASE collating sequence']),
    ('P31', 'https://www.sqlite.org/lang_createindex.html', ['CREATE INDEX']),
    ('P32', 'https://www.sqlite.org/eqp.html', ['EXPLAIN QUERY PLAN', 'SCAN']),
    ('P33', 'https://www.sqlite.org/backup.html', ['Online Backup API']),
    ('P34', 'https://www.sqlite.org/compile.html', ['SQLITE_DQS']),
    ('P35', 'https://www.sqlite.org/limits.html', ['Maximum Number Of Pages In A Database File', '281 terabytes']),
    ('P36', 'https://www.sqlite.org/copyright.html', ['SQLite is in the Public Domain']),
    ('P37', 'https://www.sqlite.org/about.html', ['Single-file database', 'Public domain']),
    ('P38', 'https://www.sqlite.org/lang_datefunc.html', ['YYYY-MM-DD HH:MM:SS.SSS']),
    ('P39', 'https://www.sqlite.org/lang_insert.html', ['INSERT']),
    ('P40', 'https://www.sqlite.org/lang_returning.html', ['RETURNING']),
    ('P41', 'https://www.sqlite.org/lang_keywords.html', ['single quotes']),
    ('P42', 'https://www.sqlite.org/fileformat2.html', ['page size']),
    ('P43', 'https://www.sqlite.org/different.html', ['Manifest typing', 'Zero-configuration']),
    ('P44', 'https://www.sqlite.org/serverless.html', ['serverless']),
    ('P45', 'https://www.sqlite.org/howtocorrupt.html', ['How To Corrupt An SQLite Database File']),
    ('P46', 'https://www.sqlite.org/famous.html', ['Airbus confirms that SQLite is being used in the flight software for the A350 XWB']),
    ('P47', 'https://sqlite.org/releaselog/3_37_0.html', ['STRICT tables provide a prescriptive style of data type management']),
    ('P48', 'https://www.sqlite.org/index.html', ['Version 3.54.0 (2026-10-09)']),
    ('P49', 'https://sqlite.org/download.html', ['sqlite-tools-linux-x64-3540000.zip']),
    ('P50', 'https://www.sqlite.org/threadsafe.html', ['Serialized']),
    ('P51', 'https://www.sqlite.org/uri.html', ['mode=ro']),
    ('P52', 'https://docs.python.org/3.14/using/configure.html', ['SQLite']),
    ('P53', 'https://docs.python.org/3.14/whatsnew/3.14.html', ['sqlite3']),
    ('P54', 'https://docs.python.org/3.14/whatsnew/3.13.html', ['sqlite3']),
    ('P55', 'https://docs.python.org/3.14/whatsnew/3.12.html', ['autocommit']),
    ('P56', 'https://docs.python.org/3.14/whatsnew/2.5.html', ['pysqlite']),
    ('P57', 'https://docs.python.org/3.14/library/pprint.html', ['pprint']),
    ('P58', 'https://docs.python.org/3.14/library/shutil.html', ['shutil.copy']),
    ('P59', 'https://docs.python.org/3.14/library/contextlib.html', ['closing']),
    ('P60', 'https://peps.python.org/pep-0249/', ['Database API Specification 2.0', 'paramstyle']),
    ('P61', 'https://sqlitebrowser.org/', ['DB Browser for SQLite (DB4S) is a high quality, visual, open source tool']),
    ('P62', 'https://sqlitestudio.pl/', ['Letos was formerly known as SQLiteStudio']),
    ('P63', 'https://dbeaver.io/', ['DBeaver']),
    ('P64', 'https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html', ['Prepared Statements']),
    ('P65', 'https://cwe.mitre.org/data/definitions/89.html', ['SQL Injection']),
    ('P66', 'https://xkcd.com/327/', ["Her daughter is named Help I'm trapped in a driver's license factory"]),
    ('P67', 'https://en.wikipedia.org/wiki/SQLite', ['D. Richard Hipp']),
    ('P68', 'https://en.wikipedia.org/wiki/SQL', ['Chamberlin', 'Boyce']),
    ('P69', 'https://en.wikipedia.org/wiki/Relational_model', ['Codd']),
    ('P70', 'https://en.wikipedia.org/wiki/D._Richard_Hipp', ['SQLite']),
    ('P71', 'https://en.wikipedia.org/wiki/ACID', ['Atomicity', 'Durability']),
    ('P72', 'https://en.wikipedia.org/wiki/CRUD', ['Create, read, update']),
    ('P73', 'https://www.engineering.upenn.edu/~zives/03f/cis550/codd.pdf', ['Relational Model of Data for Large Shared Data Banks']),
    ('P74', 'https://www.ibm.com/history/relational-database', ['Codd']),
    ('P75', 'https://en.wikipedia.org/wiki/SQL_injection', ['xkcd']),
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
            elif "zip" in ctype or url.endswith(".zip"):
                t = ""
            elif "html" in ctype:
                s = bs4.BeautifulSoup(t, "html.parser")
                for x in s(["script", "style"]): x.decompose()
                t = s.get_text(" ")
            t = norm(t); out.append([pid, r.status_code, len(r.content), {p: (p.lower() in t.lower()) for p in phrases}])
        except Exception as e: out.append([pid, "unreachable: %s" % type(e).__name__, 0, {}])
    return out
see("every source of the research record opened: id, HTTP status, bytes, and whether each passage the research relies on is on the page", sources)
json.dump({"_version": "1.0.0", "observed": datetime.date.today().isoformat(), "with": "requests %s, beautifulsoup4 %s, Python %s" % (requests.__version__, bs4.__version__, sys.version.split()[0]),
           "_note": "Single requests made on the day named, through the build machine's proxy, to the public pages and files the chapter names. The GUI apps were not installed or run. A record of one observation; web sites change and nothing re-checks it.",
           "items": obs}, open(OUT, "w"), indent=1, ensure_ascii=False)
print("observed", len(obs), "things on", datetime.date.today())
