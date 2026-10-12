"""Chapter 16 deck examples: every console session, whole program (or excerpt), chart and table the lecture deck shows. Nothing here
carries a result; examples_run_v1_0_0.py runs it all under the interpreter given and records the results. A console group is one
session: its rows run in order in one namespace (the deck check re-runs them per slide, one namespace per slide). No console row
touches the network or the file system: every console works on a database in memory with the standard library only, so each can be
typed into a Python in a browser. Every row that would print a cursor (whose repr holds a memory address) goes through the helper
run, a lambda that executes the statement and returns fetchall(): an empty list means the statement returned no rows.

Programs come from sen0414_ch16_corpus_base_v1_0_0.py, all twelve. Where a corpus line or its output is wider than a slide can show
without wrapping, the deck shows a deck-written copy of the program (the SQL cut into pieces on several lines, or one value printed
per line): matchingMealIngredients is the corpus meal program with its SQL strings cut, and the others are named below. The corpus
originals are recorded and re-run too, and EQUIV lists the copies whose transcript must equal the original's, line for line.
KIND says what a program's output depends on, so that honesty_check can require the matching line on the slide that shows it:
  live  the program reads the book's own database sweigartcats.db (fetched at run time, sha256 beginning 41f0d0b5bc2e checked)
  none  the output depends on nothing outside the program: a database it builds itself, in memory or in a temporary folder"""
__version__ = "1.0.0"
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("base16", os.path.join(HERE, "..", "sen0414_ch16_corpus_base_v1_0_0.py"))
B = importlib.util.module_from_spec(_s)
_s.loader.exec_module(B)

OPEN = ["import sqlite3", "conn = sqlite3.connect(':memory:', isolation_level=None)",
        "run = lambda sql, *args: conn.execute(sql, args).fetchall()"]
DO = "do = lambda sql: conn.execute(sql).close()"      # runs a statement that returns no rows and prints nothing

CONSOLES = {
    "title": ["import platform, sqlite3", "platform.python_version()", "sqlite3.sqlite_version"],
    "table": OPEN[:2] + [DO, "run = lambda sql: conn.execute(sql).fetchall()",
                         "do('CREATE TABLE cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT')",
                         "do(\"INSERT INTO cats VALUES ('Zophie', '2021-01-24', 'black', 5.6)\")",
                         "do(\"INSERT INTO cats VALUES ('Miguel', '2016-12-24', 'siamese', 6.2)\")",
                         "run('SELECT * FROM cats')", "run('SELECT rowid, * FROM cats')", "run('SELECT rowid, oid, _rowid_ FROM cats LIMIT 1')"],
    "noserver": ["import sqlite3", "conn = sqlite3.connect(':memory:')", "conn.execute('GRANT SELECT ON cats TO bob')",
                 "conn.execute('CREATE USER bob')", "conn.execute('PRAGMA max_page_count').fetchone()", "4096 * 4294967294"],
    "connect": ["import sqlite3", "conn = sqlite3.connect(':memory:')", "conn.in_transaction",
                "conn.execute('SELECT sqlite_version()').fetchone()", "conn.close()", "conn.execute('SELECT 1')"],
    "values": ["import sqlite3", "conn = sqlite3.connect(':memory:')",
               "run = lambda sql, *args: conn.execute(sql, args).fetchall()",
               "run(\"SELECT date('2035-02-30'), date('31/10/2035')\")", "run('SELECT TRUE, FALSE')",
               "run('SELECT ?', 2 ** 63)", "run('SELECT ?', [1])"],
    "inject": ["import sqlite3", "conn = sqlite3.connect(':memory:')",
               "run = lambda sql, *args: conn.execute(sql, args).fetchall()",
               "run('CREATE TABLE cats (name TEXT)')",
               "run(\"INSERT INTO cats VALUES ('Zophie'), ('Toby')\")",
               "attack = \"x' OR '1'='1\"",
               "len(run(f\"SELECT * FROM cats WHERE name = '{attack}'\"))",
               "len(run('SELECT * FROM cats WHERE name = ?', attack))",
               "run('SELECT 1; DROP TABLE cats')"],
    "nulls": ["import sqlite3", "conn = sqlite3.connect(':memory:')", DO.replace("conn.execute(sql)", "conn.execute(sql)"),
              "run = lambda sql: conn.execute(sql).fetchall()", "do('CREATE TABLE c (name TEXT, fur TEXT)')",
              "do(\"INSERT INTO c VALUES ('Zophie', 'black'), ('Toby', 'black')\")",
              "do(\"INSERT INTO c VALUES ('Jacob', 'orange'), ('Mandy', NULL)\")",
              "run('SELECT name FROM c WHERE fur = NULL')", "run(\"SELECT name FROM c WHERE fur != 'black'\")",
              "run('SELECT name FROM c WHERE fur IS NULL')", "run('SELECT count(*), count(fur) FROM c')",
              "run('SELECT name FROM c WHERE fur = \"fur\"')", "run(\"SELECT 'a' LIKE 'A', 'a' GLOB 'A', '\u00c9' LIKE '\u00e9'\")"],
    "txn": ["import sqlite3", "conn = sqlite3.connect(':memory:', isolation_level=None)", DO,
            "run = lambda sql: conn.execute(sql).fetchall()", "do('CREATE TABLE t (a INTEGER NOT NULL)')", "do('BEGIN')",
            "do('INSERT INTO t VALUES (1)')", "conn.in_transaction", "conn.rollback()", "run('SELECT count(*) FROM t')",
            "do('BEGIN')", "do('INSERT INTO t VALUES (2)')", "conn.commit()", "run('SELECT count(*) FROM t')",
            "do('INSERT INTO t VALUES (3), (4), (NULL)')", "run('SELECT count(*) FROM t')"],
}

# ---- programs written for the deck ----------------------------------------------------------------------------------------------
_HEAD = B.HEAD
_REAL = B.REAL

MEAL3 = _HEAD + '''# The meal program of the corpus with its SQL cut into pieces that fit a slide; same statements, same output.
conn = sqlite3.connect('meals.db', isolation_level=None)
conn.execute('PRAGMA foreign_keys = ON')
conn.execute('CREATE TABLE meals (id INTEGER PRIMARY KEY,'
             ' name TEXT NOT NULL) STRICT')
conn.execute('CREATE TABLE ingredients (id INTEGER PRIMARY KEY,'
             ' meal_id INTEGER NOT NULL, ingredient TEXT NOT NULL,'
             ' grams REAL, FOREIGN KEY (meal_id) REFERENCES meals (id))'
             ' STRICT')
conn.execute("INSERT INTO meals (name) VALUES ('Pancakes'), ('Omelette')")
conn.executemany('INSERT INTO ingredients (meal_id, ingredient, grams)'
                 ' VALUES (?, ?, ?)',
                 [(1, 'flour', 200.0), (1, 'milk', 300.0), (1, 'egg', 100.0),
                  (2, 'egg', 150.0), (2, 'butter', 20.0)])
for row in conn.execute('SELECT meals.name, group_concat(ingredient, ", "),'
                        ' sum(grams) FROM meals JOIN ingredients'
                        ' ON meal_id = meals.id GROUP BY meals.id'):
    print(row)
try:
    conn.execute("INSERT INTO ingredients (meal_id, ingredient)"
                 " VALUES (99, 'salt')")
except sqlite3.IntegrityError as e:
    print(e)
print(conn.execute('PRAGMA foreign_key_check').fetchall())
print(conn.execute("SELECT name FROM meals WHERE id NOT IN"
                   " (SELECT meal_id FROM ingredients"
                   " WHERE ingredient = 'butter')").fetchall())
'''

SHIPPED3 = _HEAD + _REAL + '''# The shipped-database program of the corpus with one long printed line cut in two; every other statement is the same.
db = real_db()
conn = sqlite3.connect(db, isolation_level=None)
sql = conn.execute("SELECT sql FROM sqlite_schema"
                   " WHERE name = 'vaccinations'").fetchone()[0]
print(sql[:sql.index('FOREIGN')])
print(sql[sql.index('FOREIGN'):])
print('foreign_keys is', conn.execute('PRAGMA foreign_keys').fetchone()[0])
conn.execute('PRAGMA foreign_keys = ON')
try:
    conn.execute("INSERT INTO vaccinations VALUES"
                 " ('rabies', '2023-06-06', 'Dr. Echo', 1)")
except sqlite3.Error as e:
    print(type(e).__name__, e)
conn.execute('PRAGMA foreign_keys = OFF')
try:
    print(len(list(conn.iterdump())))
except sqlite3.Error as e:
    print('iterdump:', type(e).__name__, e)
print(conn.execute('PRAGMA integrity_check').fetchall())
conn.close()
'''

CAT3 = _HEAD + _REAL + '''# The cat vaccination checker of the corpus with its long queries cut and one result printed per line.
db = real_db()
conn = sqlite3.connect(db)
q = lambda sql: conn.execute(sql).fetchall()
print(q('SELECT count(*) FROM cats')[0][0], 'cats,',
      q('SELECT count(*) FROM vaccinations')[0][0], 'vaccinations')
early = q('SELECT c.name, c.birthdate, v.vaccine, v.date_administered'
          ' FROM vaccinations v JOIN cats c ON v.cat_id = c.rowid'
          ' WHERE v.date_administered < c.birthdate ORDER BY v.rowid')
for row in early:
    print('given before birth:', row)
missing = q('SELECT c.rowid, c.name FROM cats c'
            ' LEFT JOIN vaccinations v ON v.cat_id = c.rowid'
            ' GROUP BY c.rowid HAVING count(DISTINCT v.vaccine) < 3'
            ' ORDER BY c.rowid')
print('missing a vaccine:', ', '.join(name for _, name in missing))
print(q('SELECT vaccine, count(*) FROM vaccinations GROUP BY vaccine'))
print(q('SELECT name, count(*) FROM cats GROUP BY name HAVING count(*) > 1'))
conn.close()
'''

PROGRAMS = dict(B.PROGRAMS)
PROGRAMS["matchingMealIngredients_v1_0_0.py"] = (MEAL3, (), False)
PROGRAMS["shippedDatabaseCut_v1_0_0.py"] = (SHIPPED3, (), True)
PROGRAMS["catCheckerCut_v1_0_0.py"] = (CAT3, (), True)

# copies whose transcript must equal the original's, line for line (the others differ in how they print, by design)
EQUIV = {"matchingMealIngredients_v1_0_0.py": "practiceMealIngredients_v1_0_0.py"}

KIND = {n: "none" for n in PROGRAMS}
for n in ("practiceCatVaccinationChecker_v1_0_0.py", "shippedDatabase_v1_0_0.py", "shippedDatabaseCut_v1_0_0.py", "catCheckerCut_v1_0_0.py"):
    KIND[n] = "live"

# ---- charts and tables: each a setup and one expression --------------------------------------------------------------------------
_SIZE = ("import sqlite3\n"
         "def kib(indexes):\n"
         "    c = sqlite3.connect(':memory:'); c.execute('CREATE TABLE cats (name TEXT, fur TEXT)')\n"
         "    c.executemany('INSERT INTO cats VALUES (?, ?)', [('Cat%05d' % i, 'black') for i in range(10000)])\n"
         "    for k in range(indexes): c.execute('CREATE INDEX i%d ON cats (%s)' % (k, 'name' if k == 0 else 'fur'))\n"
         "    return c.execute('PRAGMA page_count').fetchone()[0] * c.execute('PRAGMA page_size').fetchone()[0] / 1024\n")
CHARTS = {
    "indexSize": {"setup": _SIZE, "expr": "[['no index', kib(0)], ['index on name', kib(1)], ['two indexes', kib(2)]]"},
}
_TYPES = ("import sqlite3\n"
          "c = sqlite3.connect(':memory:')\n"
          "c.execute('CREATE TABLE v (x)')\n"
          "def row(value):\n"
          "    c.execute('DELETE FROM v'); c.execute('INSERT INTO v VALUES (?)', (value,))\n"
          "    stored, back = c.execute('SELECT typeof(x), x FROM v').fetchone()\n"
          "    return [repr(value), stored, type(back).__name__]\n")
TABLES = {
    "storageClasses": {
        "setup": _TYPES,
        "expr": "[['Python value', 'Stored as', 'Read back as']] + [row(v) for v in (None, 1, 1.5, 'a', b'\\x00', True)]",
    }
}
