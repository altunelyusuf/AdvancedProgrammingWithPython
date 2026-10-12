#!/usr/bin/env python3
"""SEN0414 chapter 16 (SQLite Databases, 3rd edition) - the shared base of the corpus, version 1.0.0.

Holds the chapter's whole programs as text, the single source the deck and the page's Lab tab both read, in the shape of
sen0414_ch15_corpus_base_v1_0_0.py. Each program is a complete script that exits 0 and prints what it printed on 2026-10-12 under
Python 3.14.6 (uv), which links SQLite 3.53.1. Ten run on tables built in the program or in memory and need no network. Two read the
database the book ships, sweigartcats.db: they fetch the online-materials zip from nostarch.com on their first run (the zip and the
database are not kept in this repository), check that the sha256 of the file starts with 41f0d0b5bc2e, copy it into a temporary folder
and leave the original unchanged; they are marked LIVE below. The chapter's code is kept as printed apart from the changes a comment
or the next sentence names: the chapter's second table refers to cats(rowid), which SQLite cannot enforce, so the programs that
enforce a foreign key use an INTEGER PRIMARY KEY, and the text of the chapter's queries uses single quotes.

Shipped-database programs (LIVE): CATVACCINATIONCHECKER is the first practice program (the data errors and the missing vaccines of
sweigartcats.db), SHIPPEDDATABASE shows that the book's foreign key cannot be enforced and that iterdump() fails on the file.
Synthetic data: MEALINGREDIENTS (the second practice program, built here), FIRSTSESSION, STRICTTYPES, CRUDCATS, PLACEHOLDERS,
TRANSACTIONS, ROWIDS, INDEXPLANS, BACKUPDUMP, TWOWRITERS.

Sources read for this chapter, on 2026-10-12: the book chapter (automatetheboringstuff.com/3e/chapter16.html, sha256 b861ab33...39a4
as the book's ontology records), the pages of the SQLite documentation, the Python 3.14 documentation and the other sources the
research record lists.
"""
HEAD = "import os, tempfile, sqlite3\nos.chdir(tempfile.mkdtemp())\n"
REAL = ("import io, zipfile, hashlib, shutil, urllib.request\n"
        "def real_db():\n"
        "    p = os.environ.get('CH16_DB') or os.path.join(tempfile.gettempdir(), 'ch16_sweigartcats_41f0d0b5.db')\n"
        "    if not os.path.exists(p):\n"
        "        rq = urllib.request.Request('https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0'})\n"
        "        z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(rq, timeout=120).read()))\n"
        "        open(p + '.part', 'wb').write(z.read('Automate_the_Boring_Stuff_3e_onlinematerials/sweigartcats.db')); os.replace(p + '.part', p)\n"
        "    assert hashlib.sha256(open(p, 'rb').read()).hexdigest().startswith('41f0d0b5bc2e')\n"
        "    d = tempfile.mkdtemp(); shutil.copy(p, os.path.join(d, 'sweigartcats.db')); os.chdir(d); return 'sweigartcats.db'\n")

FIRSTSESSION = HEAD + '''# The chapter's first session: connect, create a STRICT table, list the tables and the columns.
conn = sqlite3.connect('example.db', isolation_level=None)
conn.execute('CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT')
print(conn.execute("SELECT name FROM sqlite_schema WHERE type = 'table'").fetchall())
for row in conn.execute('PRAGMA table_info(cats)'):
    print(row)
conn.execute('CREATE TABLE IF NOT EXISTS cats (name TEXT)')   # the second statement does nothing: the table exists
print(conn.execute('SELECT sql FROM sqlite_schema').fetchone()[0])
conn.close()
print(os.path.getsize('example.db') > 0)
'''
STRICTTYPES = HEAD + '''# A STRICT table refuses a wrong type and converts a convertible one; an ordinary table only has an affinity.
conn = sqlite3.connect(':memory:', isolation_level=None)
conn.execute('CREATE TABLE s (i INTEGER) STRICT')
conn.execute('CREATE TABLE plain (i INTEGER)')
for value in ('Hello', 3.5, '42', 42.0, None):
    for table in ('s', 'plain'):
        try:
            conn.execute('INSERT INTO %s VALUES (?)' % table, (value,))
        except sqlite3.IntegrityError as e:
            print(table, repr(value), 'refused:', e)
print(conn.execute('SELECT i, typeof(i) FROM s').fetchall())
print(conn.execute('SELECT i, typeof(i) FROM plain').fetchall())
try:
    conn.execute('CREATE TABLE bad (a BOOLEAN) STRICT')
except sqlite3.Error as e:
    print(type(e).__name__, e)
'''
CRUDCATS = HEAD + '''# Create, read, update and delete with placeholders; RETURNING and lastrowid; the row counts.
conn = sqlite3.connect(':memory:', isolation_level=None)
conn.execute('CREATE TABLE cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT')
conn.executemany('INSERT INTO cats VALUES (?, ?, ?, ?)', [('Zophie', '2021-01-24', 'black', 5.6), ('Miguel', '2016-12-24', 'siamese', 6.2),
                                                         ('Jacob', '2022-02-20', 'orange and white', 5.5), ('Toby', '2021-05-17', 'black', 6.8)])
print(conn.execute('SELECT rowid, name FROM cats ORDER BY weight_kg DESC LIMIT 2').fetchall())
cur = conn.execute('UPDATE cats SET weight_kg = weight_kg + 0.1 WHERE fur = ?', ('black',))
print('updated', cur.rowcount)
print(conn.execute('DELETE FROM cats WHERE name = ? RETURNING rowid, name', ('Jacob',)).fetchall())
print(conn.execute('INSERT INTO cats (name) VALUES (?)', ('Mango',)).lastrowid)
print(conn.execute('SELECT * FROM cats WHERE name LIKE ? ORDER BY name', ('%o%',)).fetchall())
print(conn.execute('SELECT count(*), count(fur), round(avg(weight_kg), 2) FROM cats').fetchone())
'''
PLACEHOLDERS = HEAD + '''# SQL injection: pasted text changes the query, a bound value does not; execute() refuses a second statement.
conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE cats (name TEXT)')
conn.executemany('INSERT INTO cats VALUES (?)', [('Zophie',), ('Toby',), ('Jacob',), ('Miguel',)])
attack = "x' OR '1'='1"
print(len(conn.execute(f"SELECT * FROM cats WHERE name = '{attack}'").fetchall()), 'rows with the f-string')
print(len(conn.execute('SELECT * FROM cats WHERE name = ?', (attack,)).fetchall()), 'rows with the placeholder')
try:
    conn.execute("SELECT 1; DROP TABLE cats")
except sqlite3.Error as e:
    print(type(e).__name__, e)
print(conn.execute('SELECT count(*) FROM cats').fetchone())
for statement, args in (('SELECT ?, ?', (1,)), ('SELECT :a', [1]), ('SELECT :a', {'b': 1})):
    try:
        conn.execute(statement, args)
    except sqlite3.Error as e:
        print(type(e).__name__, str(e)[:70])
'''
TRANSACTIONS = HEAD + '''# commit() and rollback() under the default mode, with autocommit=False and with autocommit=True; the context manager.
for label, kw in (('default', {}), ('autocommit=False', {'autocommit': False}), ('autocommit=True', {'autocommit': True})):
    conn = sqlite3.connect(':memory:', **kw)
    conn.execute('CREATE TABLE t (a)')
    conn.commit()
    conn.execute('INSERT INTO t VALUES (1)')
    inside = conn.in_transaction
    conn.rollback()
    print(label, '| in a transaction before rollback:', inside, '| rows after rollback:', conn.execute('SELECT count(*) FROM t').fetchone()[0])
    conn.close()
conn = sqlite3.connect(':memory:', isolation_level=None)
conn.execute('CREATE TABLE t (a INTEGER NOT NULL)')
try:
    with conn:
        conn.execute('BEGIN'); conn.execute('INSERT INTO t VALUES (1)'); conn.execute('INSERT INTO t VALUES (NULL)')
except sqlite3.IntegrityError as e:
    print(e)
print('rows after the failed block:', conn.execute('SELECT count(*) FROM t').fetchone()[0])
try:
    conn.execute('INSERT INTO t VALUES (1), (2), (NULL)')
except sqlite3.IntegrityError:
    print('one statement is atomic, rows:', conn.execute('SELECT count(*) FROM t').fetchone()[0])
'''
ROWIDS = HEAD + '''# The rowid is not a promise: the largest one is handed out again and VACUUM renumbers a table without a primary key.
conn = sqlite3.connect(':memory:', isolation_level=None)
conn.execute('CREATE TABLE t (v)'); conn.execute('CREATE TABLE k (id INTEGER PRIMARY KEY AUTOINCREMENT, v)')
for table in ('t', 'k'):
    for v in 'abcd':
        conn.execute('INSERT INTO %s (v) VALUES (?)' % table, (v,))
    conn.execute('DELETE FROM %s WHERE rowid = 4' % table)
    print(table, 'next rowid after deleting 4:', conn.execute('INSERT INTO %s (v) VALUES (?)' % table, ('e',)).lastrowid)
conn.execute('DELETE FROM t WHERE rowid IN (1, 2)')
print('before VACUUM', conn.execute('SELECT rowid, v FROM t').fetchall())
conn.execute('VACUUM')
print('after VACUUM ', conn.execute('SELECT rowid, v FROM t').fetchall())
print(sorted(r[0] for r in conn.execute('SELECT name FROM sqlite_schema WHERE name LIKE ?', ('sqlite_%',))))
'''
INDEXPLANS = HEAD + '''# The query plan of a search on an indexed column: equality and GLOB use the index, LIKE does not.
conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE cats (name TEXT, fur TEXT)')
conn.executemany('INSERT INTO cats VALUES (?, ?)', [('Cat%04d' % i, 'black') for i in range(1000)])
conn.execute('CREATE INDEX idx_name ON cats (name)')
for where in ("name = 'Cat0042'", "name GLOB 'Cat00*'", "name >= 'Cat00' AND name < 'Cat01'", "name LIKE 'Cat00%'", "name LIKE '%42'", "fur = 'black'"):
    print('%-38s %s' % (where, conn.execute('EXPLAIN QUERY PLAN SELECT * FROM cats WHERE ' + where).fetchall()[0][3]))
print(conn.execute('SELECT count(*) FROM cats WHERE name LIKE ?', ('Cat00%',)).fetchone())
'''
BACKUPDUMP = HEAD + '''# backup() copies into another connection, iterdump() gives the SQL text, a memory database can be saved to a file.
mem = sqlite3.connect(':memory:')
mem.execute('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT) STRICT')
mem.executemany('INSERT INTO cats VALUES (?, ?)', [('Zophie', 'black'), ('Toby', 'black')]); mem.commit()
disk = sqlite3.connect('copy.db'); mem.backup(disk); disk.close()
print(sqlite3.connect('copy.db').execute('SELECT * FROM cats').fetchall(), os.path.getsize('copy.db'))
for line in mem.iterdump():
    print(line)
try:
    mem.backup(mem)
except ValueError as e:
    print(e)
copy = sqlite3.connect(':memory:'); copy.executescript('\\n'.join(mem.iterdump()))
print(copy.execute('SELECT count(*) FROM cats').fetchone())
'''
TWOWRITERS = HEAD + '''# Two connections to one file: the second writer meets 'database is locked'; in WAL mode a reader is not blocked.
a = sqlite3.connect('shared.db', timeout=0, isolation_level=None); b = sqlite3.connect('shared.db', timeout=0, isolation_level=None)
a.execute('CREATE TABLE t (n)')
print('journal mode', a.execute('PRAGMA journal_mode').fetchone()[0])
a.execute('BEGIN IMMEDIATE'); a.execute('INSERT INTO t VALUES (1)')
try:
    b.execute('INSERT INTO t VALUES (2)')
except sqlite3.OperationalError as e:
    print('second writer:', e)
try:
    print('reader in delete mode:', b.execute('SELECT count(*) FROM t').fetchone())
except sqlite3.OperationalError as e:
    print('reader in delete mode:', e)
a.execute('COMMIT')
print('journal mode', a.execute('PRAGMA journal_mode = WAL').fetchone()[0])
a.execute('BEGIN IMMEDIATE'); a.execute('INSERT INTO t VALUES (3)')
print('reader in WAL mode:', b.execute('SELECT count(*) FROM t').fetchone())
a.execute('COMMIT'); print('after commit:', b.execute('SELECT count(*) FROM t').fetchone())
print(sorted(os.listdir('.')))
a.close(); b.close()
'''
MEALINGREDIENTS = HEAD + '''# The second practice program, built here: meals and their ingredients linked by a real foreign key, read back with a join.
conn = sqlite3.connect('meals.db', isolation_level=None)
conn.execute('PRAGMA foreign_keys = ON')
conn.execute('CREATE TABLE meals (id INTEGER PRIMARY KEY, name TEXT NOT NULL) STRICT')
conn.execute('CREATE TABLE ingredients (id INTEGER PRIMARY KEY, meal_id INTEGER NOT NULL, ingredient TEXT NOT NULL, grams REAL, FOREIGN KEY (meal_id) REFERENCES meals (id)) STRICT')
conn.execute("INSERT INTO meals (name) VALUES ('Pancakes'), ('Omelette')")
conn.executemany('INSERT INTO ingredients (meal_id, ingredient, grams) VALUES (?, ?, ?)',
                 [(1, 'flour', 200.0), (1, 'milk', 300.0), (1, 'egg', 100.0), (2, 'egg', 150.0), (2, 'butter', 20.0)])
for row in conn.execute('SELECT meals.name, group_concat(ingredient, ", "), sum(grams) FROM meals JOIN ingredients ON meal_id = meals.id GROUP BY meals.id'):
    print(row)
try:
    conn.execute("INSERT INTO ingredients (meal_id, ingredient) VALUES (99, 'salt')")
except sqlite3.IntegrityError as e:
    print(e)
print(conn.execute('PRAGMA foreign_key_check').fetchall())
print(conn.execute("SELECT name FROM meals WHERE id NOT IN (SELECT meal_id FROM ingredients WHERE ingredient = 'butter')").fetchall())
'''
CATVACCINATIONCHECKER = HEAD + REAL + '''# The first practice program on the book's own database: vaccinations dated before the birth, and cats missing a vaccine.
db = real_db()
conn = sqlite3.connect(db)
print(conn.execute('SELECT count(*) FROM cats').fetchone(), conn.execute('SELECT count(*) FROM vaccinations').fetchone())
early = conn.execute('SELECT v.rowid, c.name, c.birthdate, v.vaccine, v.date_administered FROM vaccinations v JOIN cats c ON v.cat_id = c.rowid WHERE v.date_administered < c.birthdate ORDER BY v.rowid').fetchall()
print('given before birth:', early)
missing = conn.execute("SELECT c.rowid, c.name, group_concat(DISTINCT v.vaccine) FROM cats c LEFT JOIN vaccinations v ON v.cat_id = c.rowid GROUP BY c.rowid HAVING count(DISTINCT v.vaccine) < 3 ORDER BY c.rowid").fetchall()
print('missing a vaccine:', [(r[0], r[1]) for r in missing])
print(conn.execute('SELECT vaccine, count(*) FROM vaccinations GROUP BY vaccine ORDER BY vaccine').fetchall())
print(conn.execute('SELECT name, count(*) FROM cats GROUP BY name HAVING count(*) > 1').fetchall())
conn.close()
'''
SHIPPEDDATABASE = HEAD + REAL + '''# The shipped database: its foreign key to cats(rowid) cannot be enforced, and iterdump() fails on it from Python 3.13.
db = real_db()
conn = sqlite3.connect(db, isolation_level=None)
print(conn.execute("SELECT sql FROM sqlite_schema WHERE name = 'vaccinations'").fetchone()[0])
print('foreign_keys is', conn.execute('PRAGMA foreign_keys').fetchone()[0], '| journal mode', conn.execute('PRAGMA journal_mode').fetchone()[0])
conn.execute('PRAGMA foreign_keys = ON')
try:
    conn.execute("INSERT INTO vaccinations VALUES ('rabies', '2023-06-06', 'Dr. Echo', 1)")
except sqlite3.Error as e:
    print(type(e).__name__, e)
conn.execute('PRAGMA foreign_keys = OFF')
try:
    print(len(list(conn.iterdump())))
except sqlite3.Error as e:
    print('iterdump:', type(e).__name__, e)
print(conn.execute('PRAGMA integrity_check').fetchall(), conn.execute('SELECT count(*) FROM sqlite_schema').fetchone())
conn.close()
'''
PROGRAMS = {
    'firstSession_v1_0_0.py': (FIRSTSESSION, (), False),
    'strictTypes_v1_0_0.py': (STRICTTYPES, (), False),
    'crudCats_v1_0_0.py': (CRUDCATS, (), False),
    'placeholdersAndInjection_v1_0_0.py': (PLACEHOLDERS, (), False),
    'transactions_v1_0_0.py': (TRANSACTIONS, (), False),
    'rowids_v1_0_0.py': (ROWIDS, (), False),
    'indexPlans_v1_0_0.py': (INDEXPLANS, (), False),
    'backupAndDump_v1_0_0.py': (BACKUPDUMP, (), False),
    'twoWriters_v1_0_0.py': (TWOWRITERS, (), False),
    'practiceMealIngredients_v1_0_0.py': (MEALINGREDIENTS, (), False),
    'practiceCatVaccinationChecker_v1_0_0.py': (CATVACCINATIONCHECKER, (), True),
    'shippedDatabase_v1_0_0.py': (SHIPPEDDATABASE, (), True),
}
FIXTURE_BASED = []

if __name__ == "__main__":
    # Usage: sen0414_ch16_corpus_base_v1_0_0.py   (run it with Python 3.12 or later; exits 1 if a program does not exit 0)
    import os, subprocess, sys
    bad = 0
    for name, (code, needs, live) in PROGRAMS.items():
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", code], capture_output=True, text=True, timeout=300)
        bad += r.returncode != 0
        print("=== %s (exit %d)%s" % (name, r.returncode, " LIVE" if live else "")); print(r.stdout.rstrip()[:900]); print(r.stderr[-300:].rstrip())
    print("%d programs, %d did not exit 0" % (len(PROGRAMS), bad)); sys.exit(1 if bad else 0)
