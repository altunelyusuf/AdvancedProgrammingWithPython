"""Chapter 16 content for the RDODI build: sources, findings, taxonomy and section bodies.
The book's chapter was read on automatetheboringstuff.com on 2026-10-01 (the page was downloaded with curl through the agent proxy
because the page-to-text fetch tool was refused for lack of approval; its HTML was reduced to text and read whole, 14 section and 10 subsection headings and 49 code
blocks), and checked against the book's own chapter ontology at commit 89f68596 (14 sections). The Python documentation was read from the
CPython source tree at tag v3.14.4 (Doc/, commit 23116f9); PEP 249 and the SQLite documentation pages were read on 2026-10-01 from
peps.python.org and sqlite.org, which describe their current releases, while the machine runs SQLite 3.50.4 under Python 3.14.4.
The file sweigartcats.db of the chapter was not downloaded: a table of 18 cats copied from the rows the chapter prints stands in for it.
Every behaviour was executed under Python 3.14.4. A claim not in this file was not made.
Version 1.0.1: only the way the 32 one-expression examples pick their result changed. Version 1.0.0 ended each lambda with the tuple index [1];
the page's question maker changes numbers in a program, turned [1] into [0] and so asked for the address of a cursor object, which differs
from run to run. The examples now end with next(reversed((...))), which gives the same last item without a number in it; the printed
results are unchanged and are checked again by the checks script. Nothing else differs from 1.0.0."""
__version__ = "1.0.1"
CH = 16
DATE = '2026-10-01'
PYVER = '3.14.4'
TITLE = "SQLite databases for an advanced course: chapter 16 of the 3rd edition and today's Python"
QUESTION = ('What does chapter 16 of the 3rd edition teach about databases and the sqlite3 module, which of its printed outputs and programs still hold under Python 3.14.4 and '
 'SQLite 3.50.4, and what must an advanced course correct or add so that it matches current Python and SQLite?')
CQS = ('Which statements change the database, which only read it, and what decides whether a change is kept, undone or refused?',
 'Which claims and programs of the chapter differ in current Python and SQLite, and on what source?')
PUBS = [('P01',
  'Automate the Boring Stuff with Python, 3rd edition - Chapter 16, SQLite Databases (Al Sweigart, No Starch Press, 2025)',
  'https://automatetheboringstuff.com/3e/chapter16.html',
  True),
 ('P02',
  'sqlite3 - DB-API 2.0 interface for SQLite databases (Python 3.14.4 documentation source, Doc/library/sqlite3.rst)',
  'https://docs.python.org/3/library/sqlite3.html',
  False),
 ('P03', 'PEP 249 - Python Database API Specification v2.0 (Lemburg, 1999)', 'https://peps.python.org/pep-0249/', False),
 ('P04', "What's New In Python 3.13 - sqlite3 and build requirements (Python 3.14.4 documentation source)", 'https://docs.python.org/3/whatsnew/3.13.html', False),
 ('P05', 'Configure Python - build requirements, SQLite minimum version (Python 3.14.4 documentation source)', 'https://docs.python.org/3/using/configure.html', False),
 ('P06', 'SQLite documentation - STRICT Tables', 'https://www.sqlite.org/stricttables.html', False),
 ('P07', 'SQLite documentation - Datatypes In SQLite', 'https://www.sqlite.org/datatype3.html', False),
 ('P08', 'SQLite documentation - SQLite Foreign Key Support', 'https://www.sqlite.org/foreignkeys.html', False),
 ('P09', 'SQLite documentation - Quirks, Caveats, and Gotchas In SQLite', 'https://www.sqlite.org/quirks.html', False),
 ('P10', 'SQLite documentation - SQLite Autoincrement', 'https://www.sqlite.org/autoinc.html', False),
 ('P11', 'SQLite documentation - CREATE TABLE, ROWIDs and the INTEGER PRIMARY KEY', 'https://www.sqlite.org/lang_createtable.html', False),
 ('P12', 'SQLite documentation - VACUUM', 'https://www.sqlite.org/lang_vacuum.html', False),
 ('P13', 'SQLite documentation - Transaction', 'https://www.sqlite.org/lang_transaction.html', False),
 ('P14', 'SQLite documentation - Appropriate Uses For SQLite', 'https://www.sqlite.org/whentouse.html', False),
 ('P15', 'SQLite documentation - In-Memory Databases', 'https://www.sqlite.org/inmemorydb.html', False),
 ('P16', 'SQLite documentation - SQL Language Expressions, LIKE and GLOB', 'https://www.sqlite.org/lang_expr.html', False),
 ('P17', 'SQLite documentation - ALTER TABLE', 'https://www.sqlite.org/lang_altertable.html', False),
 ('P18', 'SQLite documentation - Write-Ahead Logging', 'https://www.sqlite.org/wal.html', False),
 ('P19', 'SQLite documentation - Command Line Shell For SQLite', 'https://www.sqlite.org/cli.html', False)]
CONCEPTS = [('Section', 'Spreadsheets vs. Databases'),
 ('Section', 'SQLite vs. Other SQL Databases'),
 ('Section', 'Creating Databases and Tables'),
 ('Section', 'CRUD Database Operations'),
 ('Section', 'Rolling Back Transactions'),
 ('Section', 'Backing Up Databases'),
 ('Section', 'Altering and Dropping Tables'),
 ('Section', 'Joining Multiple Tables with Foreign Keys'),
 ('Section', 'In-Memory Databases and Backups'),
 ('Section', 'Copying Databases'),
 ('Section', 'SQLite Apps'),
 ('Section', 'Summary'),
 ('Section', 'Practice Questions'),
 ('Section', 'Practice Programs'),
 ('Subsection', 'Connecting to Databases'),
 ('Subsection', 'Creating Tables'),
 ('Subsection', 'Defining Data Types'),
 ('Subsection', 'Listing Tables and Columns'),
 ('Subsection', 'Inserting Data into the Database'),
 ('Subsection', 'Reading Data from the Database'),
 ('Subsection', 'Updating Data in the Database'),
 ('Subsection', 'Deleting Data from the Database'),
 ('Subsection', 'Cat Vaccination Checker'),
 ('Subsection', 'Meal Ingredients Database'),
 ('Method', 'sqlite3.connect'),
 ('Method', 'execute'),
 ('Method', 'fetchall'),
 ('Method', 'commit'),
 ('Method', 'rollback'),
 ('Method', 'backup'),
 ('Method', 'iterdump'),
 ('Method', 'close'),
 ('Statement', 'CREATE TABLE'),
 ('Statement', 'INSERT'),
 ('Statement', 'SELECT'),
 ('Statement', 'UPDATE'),
 ('Statement', 'DELETE'),
 ('Statement', 'ALTER TABLE'),
 ('Statement', 'DROP TABLE'),
 ('Statement', 'CREATE INDEX'),
 ('Statement', 'DROP INDEX'),
 ('Statement', 'PRAGMA'),
 ('Statement', 'BEGIN'),
 ('Clause', 'WHERE'),
 ('Clause', 'ORDER BY'),
 ('Clause', 'LIMIT'),
 ('Clause', 'LIKE'),
 ('Clause', 'GLOB'),
 ('Clause', 'INNER JOIN'),
 ('Clause', 'FOREIGN KEY'),
 ('Clause', 'STRICT'),
 ('Concept', 'Primary key and rowid'),
 ('Concept', 'Transaction and ACID'),
 ('Concept', 'SQL injection'),
 ('Concept', 'Type affinity'),
 ('Concept', 'In-memory database')]
FINDINGS = [('F1',
  'Background',
  'Chapter 16 of the 3rd edition, SQLite Databases, sets spreadsheets against databases and SQLite against server databases; creates a database and a table with '
  'sqlite3.connect(), isolation_level=None and CREATE TABLE ... STRICT, lists the data types it names, reads sqlite_schema and PRAGMA TABLE_INFO; teaches CRUD with '
  'INSERT, SELECT, UPDATE and DELETE, transactions and the ACID properties, the ? placeholder against SQL injection, fetchall() and looping over a cursor, WHERE, LIKE '
  'and GLOB, ORDER BY, LIMIT and CREATE INDEX; BEGIN with commit() and rollback(); backups with backup(); ALTER TABLE and DROP TABLE; foreign keys and the inner join; '
  'in-memory databases; iterdump(); the sqlite3 command-line tool and three graphical apps; and closes with 16 practice questions and 2 practice programs.',
  ['P01']),
 ('F2',
  'Comparative analysis',
  'Every printed output of the chapter that does not depend on its downloaded file sweigartcats.db reproduces under Python 3.14.4 with SQLite 3.50.4: the tuples of '
  "PRAGMA TABLE_INFO(cats), [('cats',)] from sqlite_schema, the INSERT, SELECT, UPDATE and DELETE session, OperationalError: table cats already exists, DatabaseError: "
  'file is not a database, the rollback and commit session, the ALTER TABLE and DROP TABLE session, the inner join and the iterdump text; only the addresses in each '
  'Cursor repr, the placeholder version 3.xx.xx and the quoted table name in the dump text differ, the last of which appears after a table has been renamed, and the '
  'rowids and rows of the real file could not be compared, because the file was not downloaded and a table of 18 cats copied from the rows the chapter prints stood in '
  'for it.',
  ['P01', 'P02']),
 ('F3',
  'Comparative analysis',
  'The chapter opens every connection with isolation_level=None, which leaves SQLite in its own autocommit mode, and uses BEGIN with commit() and rollback(), which '
  'works as printed under 3.14.4; the documentation recommends since Python 3.12 the autocommit argument instead, False for the PEP 249 behaviour that keeps a '
  "transaction always open and True for SQLite's autocommit, keeps the older isolation_level behaviour as the default value LEGACY_TRANSACTION_CONTROL, and says "
  'isolation_level has no effect otherwise, and as executed a row inserted over a default connection was gone after close() and invisible to a second connection before; '
  'PEP 249 requires auto-commit to be off at first, more than one positional argument to connect() is deprecated since 3.13, and a connection deleted without close() '
  "emits a ResourceWarning since 3.13, which none of the chapter's sessions avoids.",
  ['P01', 'P02', 'P03', 'P04', 'P13']),
 ('F4',
  'Comparative analysis',
  'The chapter says SQLite has six data types and lists five, NULL, INT or INTEGER, REAL, TEXT and BLOB; SQLite names five storage classes, NULL, INTEGER, REAL, TEXT '
  "and BLOB, and a STRICT table accepts the six column types INT, INTEGER, REAL, TEXT, BLOB and ANY; as executed '42' is stored as the integer 42 in an INTEGER column "
  "and 'Hello' stays text in an ordinary table but raises IntegrityError: cannot store TEXT value in INTEGER column in a STRICT table; the chapter is right that STRICT "
  'needs SQLite 3.37.0, but not that this version is the one Python 3.11 and later use, since the build of Python 3.13 and later needs only SQLite 3.15.2 and '
  'sqlite3.sqlite_version names the library actually linked, 3.50.4 here, so STRICT depends on that library and not on the Python version.',
  ['P01', 'P02', 'P04', 'P05', 'P06', 'P07']),
 ('F5',
  'Comparative analysis',
  'The chapter presents the rowid as a primary key that is unique and does not change, but as executed the rowid 18 was given again to a new row after the row with '
  'rowid 18 was deleted, and after four deletions and VACUUM the remaining rows were renumbered from 5, 6, 7 to 1, 2, 3; with INTEGER PRIMARY KEY the freed number 2 was '
  'given again to a new row, and only AUTOINCREMENT gave the next number 3; the documentation says that VACUUM may change the rowids of a table without an explicit '
  'INTEGER PRIMARY KEY and that AUTOINCREMENT exists to prevent the reuse of rowids.',
  ['P01', 'P10', 'P11', 'P12']),
 ('F6',
  'Comparative analysis',
  "The chapter's foreign key FOREIGN KEY(cat_id) REFERENCES cats(rowid), and the same form in its second practice program, never works as a constraint: as executed with "
  'PRAGMA foreign_keys OFF the table is created and rows with cat_id 1 and with 999 are both accepted, and with ON every insert raises OperationalError: foreign key '
  'mismatch; the SQLite documentation says that the parent key must be a named column, not the rowid, and must be a PRIMARY KEY or UNIQUE; with a declared INTEGER '
  'PRIMARY KEY the same design enforced the key, since an insert of a missing parent, a delete of a parent that is in use and an update to a missing parent each raised '
  'IntegrityError: FOREIGN KEY constraint failed, and PRAGMA foreign_keys = OFF run inside a transaction left the setting at 1, as the documentation says.',
  ['P01', 'P02', 'P08']),
 ('F7',
  'Comparative analysis',
  "The chapter writes text values in double quotes, as in WHERE fur = 'black' written with double quotes, which works but which the SQLite documentation calls a "
  'misfeature: a double-quoted word is taken as a column name when a column has that name and as a string otherwise, so as executed a comparison with the word a in '
  'double quotes matched every row while the same word in single quotes matched none, and with Connection.setconfig(sqlite3.SQLITE_DBCONFIG_DQS_DML, False), available '
  "since Python 3.12, the chapter's kind of query raised OperationalError: no such column; single quotes for text and ? placeholders for values avoid the trap.",
  ['P01', 'P02', 'P09']),
 ('F8',
  'Comparative analysis',
  "Two statements of the chapter hold only in a qualified form: the text of a dump 'will almost certainly be larger than the original database' was not so as executed, "
  "for the dump of 18 rows was shorter than the database file, which is a whole number of 4096-byte pages and was 8192 bytes; and SQLite 'can't efficiently handle "
  "hundreds or thousands of simultaneous write operations' is the documented rule of one writer at a time, which as executed made a second writer fail with "
  'OperationalError: database is locked after its timeout while the first held BEGIN IMMEDIATE; the documentation adds that writers usually take turns and that '
  'write-ahead logging lets readers and the writer work together; and the command-line tool of the chapter prints rows with bars, while python -m sqlite3, added in '
  'Python 3.12, prints each row as a Python tuple.',
  ['P01', 'P02', 'P14', 'P18', 'P19']),
 ('F9',
  'Contemporary developments',
  'Current Python and SQLite give a student more than the chapter presents: executemany(), named placeholders with a dict, sqlite3.Row for access by column name, the '
  'Connection as a context manager that commits or rolls back and does not close, contextlib.closing, the iterdump() filter argument since 3.13, serialize(), '
  'setconfig() and python -m sqlite3 since 3.12, the left join, GROUP BY, the constraints UNIQUE, CHECK and DEFAULT, ON DELETE CASCADE, EXPLAIN QUERY PLAN and the rule '
  'that a connection may be used only by the thread that created it; the default adapter of dates to text is deprecated since 3.12, and as executed binding a '
  'datetime.date raised a DeprecationWarning.',
  ['P02', 'P04', 'P08', 'P13', 'P19']),
 ('F10',
  'Conclusion',
  'For an advanced course, chapter 16 is best taught by asking where each guarantee comes from: the printed sessions hold under 3.14.4 and show the CRUD statements '
  "well, but the rowid is not a permanent key, the chapter's foreign key does not constrain anything, the choice of isolation_level=None is one of three transaction "
  "modes, STRICT depends on the linked SQLite library, double-quoted text is a trap, values belong in ? placeholders even though the chapter's own f-string example is "
  'shown as the wrong way, and every connection should be closed; the course adds executemany, named placeholders, Row, the with statement, LEFT JOIN, GROUP BY, '
  'constraints and the one-writer rule.',
  ['P01', 'P02', 'P06', 'P08', 'P11', 'P13'])]
TAX = [('DatabaseIdea',
  'Comparison',
  'SpreadsheetVersusTable',
  "conn.execute('SELECT * FROM cats').fetchall()",
  'A database table is like a spreadsheet laid out as a list of records: one row per record and one named column per kind of value, but every row has the same columns, '
  'a query instead of a cell position finds the data, and sqlite3 returns each row as a tuple.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), type(c.execute('SELECT * FROM "
   "cats').fetchone()).__name__))))(__import__('sqlite3').connect(':memory:'))",
   "'tuple'")),
 ('DatabaseIdea',
  'Comparison',
  'RowidKey',
  'SELECT rowid, * FROM cats',
  'Every ordinary SQLite table has a hidden integer key called rowid that SELECT * leaves out; it tells rows apart even when all their values are equal, but a number '
  'freed by deleting the last row is given out again, and VACUUM may renumber the rows of a table that has no INTEGER PRIMARY KEY, so a key that must never change is '
  'declared INTEGER PRIMARY KEY, with AUTOINCREMENT to forbid reuse.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE t (n TEXT); INSERT INTO t VALUES (\\'a\\'), (\\'b\\'), (\\'c\\'); DELETE FROM t WHERE rowid = 3; INSERT INTO "
   "t VALUES (\\'d\\');'), c.execute('SELECT rowid, n FROM t').fetchall()))))(__import__('sqlite3').connect(':memory:'))",
   "[(1, 'a'), (2, 'b'), (3, 'd')]")),
 ('DatabaseIdea',
  'Engine',
  'EmbeddedSingleFile',
  "sqlite3.connect('example.db')",
  "SQLite is a library that runs inside the Python program and keeps the whole database in one ordinary file that begins with the text 'SQLite format 3'; there is no "
  'server process, no installation, no network connection and no users or GRANT statements.',
  ("(lambda p: next(reversed((__import__('sqlite3').connect(p).execute('CREATE TABLE t (a)'), open(p, 'rb').read(15)))))(__import__('tempfile').mkdtemp() + "
   "'/example.db')",
   "b'SQLite format 3'")),
 ('DatabaseIdea',
  'Engine',
  'WriterLimit',
  "conn.execute('BEGIN IMMEDIATE')",
  'SQLite allows one writer at a time per database file: a second connection that wants to write waits for the connect timeout, five seconds by default, and then raises '
  'OperationalError: database is locked, which suits most programs but not hundreds of simultaneous writers.',
  None),
 ('ConnectionAndSchema',
  'Connecting',
  'ConnectCall',
  "conn = sqlite3.connect('example.db', isolation_level=None)",
  "sqlite3.connect opens a database file, creating an empty one when it does not exist, or the name ':memory:' for a private database in memory, and returns a "
  'Connection; a file that is not a SQLite database raises DatabaseError: file is not a database when the first query runs.',
  ("(lambda c: c.execute('PRAGMA database_list').fetchall())(__import__('sqlite3').connect(':memory:'))", "[(0, 'main', '')]")),
 ('ConnectionAndSchema',
  'Connecting',
  'ConnectionClose',
  'conn.close()',
  'close ends the connection and, in the default and the isolation_level=None modes, commits nothing for you; using a closed connection raises ProgrammingError, and '
  'since Python 3.13 a connection deleted without a close call emits a ResourceWarning.',
  None),
 ('ConnectionAndSchema',
  'Typing',
  'StorageClasses',
  'SELECT typeof(1), typeof(1.5)',
  'SQLite stores every value in one of five storage classes, NULL, INTEGER, REAL, TEXT and BLOB, which sqlite3 maps to None, int, float, str and bytes; there is no '
  'Boolean, so True is stored as the integer 1, and there is no date type.',
  ("(lambda c: c.execute('SELECT typeof(NULL), typeof(1), typeof(1.5), typeof(\\'a\\'), typeof(x\\'00\\')').fetchone())(__import__('sqlite3').connect(':memory:'))",
   "('null', 'integer', 'real', 'text', 'blob')")),
 ('ConnectionAndSchema',
  'Typing',
  'TypeAffinity',
  "INSERT INTO loose VALUES ('42'), ('Hello')",
  "In an ordinary table a column has only a type affinity: a value that can be converted losslessly to the column's type is converted, so '42' is stored as the integer "
  "42 in an INTEGER column, and a value that cannot be converted, such as 'Hello', is stored as it is without any error.",
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE loose (n INTEGER); INSERT INTO loose VALUES (\\'42\\'), (\\'Hello\\'), (3.0), (3.5);'), c.execute('SELECT n, "
   "typeof(n) FROM loose').fetchall()))))(__import__('sqlite3').connect(':memory:'))",
   "[(42, 'integer'), ('Hello', 'text'), (3, 'integer'), (3.5, 'real')]")),
 ('ConnectionAndSchema',
  'Typing',
  'StrictTable',
  'CREATE TABLE cats (name TEXT NOT NULL, weight_kg REAL) STRICT',
  'The STRICT table option, available from SQLite 3.37.0, requires every column to have one of the types INT, INTEGER, REAL, TEXT, BLOB or ANY and raises IntegrityError '
  "for a value that cannot be converted to the column's type, while still converting values that can, so '42' becomes the integer 42.",
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE s (n INTEGER) STRICT; INSERT INTO s VALUES (\\'42\\');'), c.execute('SELECT n, typeof(n) FROM "
   "s').fetchall()))))(__import__('sqlite3').connect(':memory:'))",
   "[(42, 'integer')]")),
 ('ConnectionAndSchema',
  'Typing',
  'DateAsText',
  'birthdate TEXT',
  'SQLite has no date or time type, so dates are kept as TEXT in the forms YYYY-MM-DD, YYYY-MM-DD HH:MM:SS and similar; text in the form YYYY-MM-DD sorts and compares '
  'in date order, and the SQL functions date() and datetime() calculate with it.',
  ("(lambda c: c.execute('SELECT date(\\'2035-10-31\\', \\'+1 day\\'), \\'2024-03-19\\' < \\'2024-12-09\\', datetime(\\'2035-10-31 16:30:00\\', \\'+1 "
   "hour\\')').fetchone())(__import__('sqlite3').connect(':memory:'))",
   "('2035-11-01', 1, '2035-10-31 17:30:00')")),
 ('ConnectionAndSchema',
  'Schema',
  'CreateTable',
  'CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT',
  'CREATE TABLE names a table and lists its columns with their types and constraints such as NOT NULL; without IF NOT EXISTS a second creation raises OperationalError: '
  'table cats already exists, and SQL keywords may be written in lower case.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE IF NOT EXISTS t (a INTEGER NOT NULL, b TEXT) STRICT; CREATE TABLE IF NOT EXISTS t (a INTEGER NOT NULL, b "
   "TEXT) STRICT;'), c.execute('SELECT name FROM sqlite_schema').fetchall()))))(__import__('sqlite3').connect(':memory:'))",
   "[('t',)]")),
 ('ConnectionAndSchema',
  'Schema',
  'SchemaTable',
  "SELECT name FROM sqlite_schema WHERE type = 'table'",
  'Every SQLite database has a built-in table sqlite_schema that holds one row for each table and index with its type, name and the SQL that created it, so a query on '
  'it lists the tables and the indexes of a table; it is read, never written.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8); CREATE INDEX idx_name ON cats (name);'), c.execute('SELECT type, name FROM "
   "sqlite_schema ORDER BY type, name').fetchall()))))(__import__('sqlite3').connect(':memory:'))",
   "[('index', 'idx_name'), ('table', 'cats')]")),
 ('ConnectionAndSchema',
  'Schema',
  'TableInfo',
  'PRAGMA TABLE_INFO(cats)',
  'PRAGMA table_info(table) returns one tuple for each column: its position counted from 0, its name, its declared type, 1 when it is NOT NULL, its default value and 1 '
  'when it is part of the primary key.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), c.execute('PRAGMA "
   "table_info(cats)').fetchall()))))(__import__('sqlite3').connect(':memory:'))",
   "[(0, 'name', 'TEXT', 1, None, 0), (1, 'fur', 'TEXT', 0, None, 0), (2, 'weight_kg', 'REAL', 0, None, 0)]")),
 ('CrudOperations',
  'Writing',
  'InsertStatement',
  "INSERT INTO cats VALUES ('Zophie', '2021-01-24', 'black', 5.6)",
  "INSERT INTO table VALUES (...) adds one row whose values are listed in the order of the table's columns; the cursor it returns reports rowcount, the rows added, and "
  'lastrowid, the rowid of the new row.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), (lambda k: (k.rowcount, k.lastrowid))(c.execute('INSERT INTO cats VALUES "
   "(\\'Sassy\\', \\'black\\', 7.5)'))))))(__import__('sqlite3').connect(':memory:'))",
   '(1, 4)')),
 ('CrudOperations',
  'Writing',
  'Placeholders',
  "conn.execute('INSERT INTO cats VALUES (?, ?, ?, ?)', [name, bday, fur, weight])",
  'A ? placeholder, or a :name placeholder with a dict, marks where a Python value goes and the module binds the value separately from the SQL text, so a value can '
  "never change the meaning of the query; building the SQL with an f-string lets input such as x' OR '1'='1 do exactly that.",
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), (lambda e: (len(c.execute('SELECT * FROM cats WHERE name = \\'' + e + "
   "'\\'').fetchall()), len(c.execute('SELECT * FROM cats WHERE name = ?', (e,)).fetchall())))('x\\' OR \\'1\\'=\\'1')))))(__import__('sqlite3').connect(':memory:'))",
   '(3, 0)')),
 ('CrudOperations',
  'Writing',
  'ManyRows',
  "conn.executemany('INSERT INTO cats VALUES (?, ?, ?)', rows)",
  'executemany runs one parameterised INSERT, UPDATE or DELETE once for every item of an iterable of parameters, in a single call and a single transaction, and its '
  'cursor reports the total rows changed.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), c.executemany('INSERT INTO cats VALUES (?, ?, ?)', [('Iris', 'bengal', "
   "6.8), ('Ruby', 'bengal', 5.0)]).rowcount))))(__import__('sqlite3').connect(':memory:'))",
   '2')),
 ('CrudOperations',
  'Writing',
  'UpdateStatement',
  "UPDATE cats SET fur = 'gray tabby' WHERE rowid = 1",
  'UPDATE table SET column = value WHERE condition changes every row for which the condition is true, and every row of the table when the WHERE clause is forgotten, '
  'which is why the clause is written even for a change meant for all rows, as WHERE 1.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), (c.execute('UPDATE cats SET fur = \\'gray\\' WHERE rowid = 1').rowcount, "
   "c.execute('UPDATE cats SET fur = \\'gray\\'').rowcount)))))(__import__('sqlite3').connect(':memory:'))",
   '(1, 3)')),
 ('CrudOperations',
  'Writing',
  'DeleteStatement',
  'DELETE FROM cats WHERE rowid = 1',
  'DELETE FROM table WHERE condition removes every row for which the condition is true, and all rows when the WHERE clause is missing; it reports the rows removed in '
  'rowcount.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), c.execute('DELETE FROM cats WHERE fur = "
   "\\'black\\'').rowcount))))(__import__('sqlite3').connect(':memory:'))",
   '2')),
 ('CrudOperations',
  'Reading',
  'SelectStatement',
  'SELECT rowid, name FROM cats',
  'SELECT columns FROM table reads rows; * means every column except rowid, and naming rowid asks for it explicitly.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), c.execute('SELECT rowid, name FROM "
   "cats').fetchall()))))(__import__('sqlite3').connect(':memory:'))",
   "[(1, 'Zophie'), (2, 'Miguel'), (3, 'Toby')]")),
 ('CrudOperations',
  'Reading',
  'FetchAndIterate',
  "for row in conn.execute('SELECT * FROM cats'):",
  'execute returns a cursor that yields tuples once: fetchone takes the next row, fetchmany(n) the next n, fetchall everything left as a list, and a for loop over the '
  'cursor needs no fetchall; a cursor that has been read to the end gives nothing more.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), (lambda k: (k.fetchone(), k.fetchmany(1), k.fetchall(), "
   "k.fetchall()))(c.execute('SELECT name FROM cats'))))))(__import__('sqlite3').connect(':memory:'))",
   "(('Zophie',), [('Miguel',)], [('Toby',)], [])")),
 ('CrudOperations',
  'Reading',
  'WhereFilter',
  "SELECT * FROM cats WHERE fur = 'black' OR birthdate >= '2024-01-01'",
  'A WHERE clause keeps only the rows for which its condition is true; it uses =, !=, <, >, <=, >=, AND, OR and NOT, where a single = tests equality, and it is written '
  'before ORDER BY and LIMIT.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), c.execute('SELECT name FROM cats WHERE fur = \\'black\\' AND weight_kg > "
   "6').fetchall()))))(__import__('sqlite3').connect(':memory:'))",
   "[('Toby',)]")),
 ('CrudOperations',
  'Reading',
  'LikeAndGlob',
  "SELECT name FROM cats WHERE name LIKE '%y'",
  'LIKE matches text with % for any run of characters and ignores case for ASCII letters only; GLOB does the same with * and _-free patterns but is case sensitive.',
  ("(lambda c: c.execute('SELECT \\'Toby\\' LIKE \\'%OB%\\', \\'Toby\\' GLOB \\'*OB*\\', \\'Toby\\' GLOB "
   "\\'*ob*\\'').fetchone())(__import__('sqlite3').connect(':memory:'))",
   '(1, 0, 1)')),
 ('CrudOperations',
  'Reading',
  'OrderByClause',
  'SELECT * FROM cats ORDER BY fur ASC, birthdate DESC',
  'ORDER BY sorts the result by one or more columns, ascending unless DESC follows the column, and a later column orders the rows that are equal in the earlier one; '
  'rows come in no promised order without it.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), c.execute('SELECT name, fur FROM cats ORDER BY fur ASC, weight_kg "
   "DESC').fetchall()))))(__import__('sqlite3').connect(':memory:'))",
   "[('Toby', 'black'), ('Zophie', 'black'), ('Miguel', 'siamese')]")),
 ('CrudOperations',
  'Reading',
  'LimitClause',
  'SELECT * FROM cats ORDER BY birthdate LIMIT 4',
  'LIMIT n makes the database stop after n rows instead of reading everything and slicing the list in Python; it is written after WHERE and ORDER BY.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), c.execute('SELECT name FROM cats ORDER BY weight_kg DESC LIMIT "
   "2').fetchall()))))(__import__('sqlite3').connect(':memory:'))",
   "[('Toby',), ('Miguel',)]")),
 ('CrudOperations',
  'Reading',
  'GroupAndCount',
  'SELECT fur, count(*) FROM cats GROUP BY fur',
  'GROUP BY puts rows with the same value in one group so that aggregate functions such as count, avg, min and max are computed per group; the chapter leaves it out as '
  'one of the clauses beyond its scope.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), c.execute('SELECT fur, count(*), round(avg(weight_kg), 2) FROM cats GROUP "
   "BY fur ORDER BY fur').fetchall()))))(__import__('sqlite3').connect(':memory:'))",
   "[('black', 2, 6.2), ('siamese', 1, 6.2)]")),
 ('CrudOperations',
  'Reading',
  'RowFactory',
  'conn.row_factory = sqlite3.Row',
  'Setting row_factory to sqlite3.Row makes each row answer to column names as well as to positions, with case-insensitive names and a keys() list, where the default '
  'row is a plain tuple that only knows positions.',
  ("(lambda c: next(reversed((setattr(c, 'row_factory', __import__('sqlite3').Row), (lambda r: (r['name'], r['WEIGHT_KG'], r.keys()))(c.execute('SELECT \\'Zophie\\' AS "
   "name, 5.6 AS weight_kg').fetchone())))))(__import__('sqlite3').connect(':memory:'))",
   "('Zophie', 5.6, ['name', 'weight_kg'])")),
 ('CrudOperations',
  'Speed',
  'CreateIndex',
  'CREATE INDEX idx_name ON cats (name)',
  'CREATE INDEX name ON table (column) builds a sorted structure that lets a WHERE on that column search instead of scanning the table, at the price of more storage and '
  'slightly slower inserts and updates; DROP INDEX removes it and EXPLAIN QUERY PLAN tells whether a query uses it.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8); CREATE INDEX idx_name ON cats (name);'), c.execute('SELECT name FROM "
   "sqlite_schema WHERE type = \\'index\\' AND tbl_name = \\'cats\\'').fetchall()))))(__import__('sqlite3').connect(':memory:'))",
   "[('idx_name',)]")),
 ('TransactionControl',
  'Boundaries',
  'BeginCommitRollback',
  "conn.execute('BEGIN')",
  'BEGIN opens a transaction, commit makes all its changes permanent and rollback discards them, so several statements either all take effect or none does; with '
  'isolation_level=None a statement outside BEGIN is its own transaction and rollback then has nothing to undo.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), (c.execute('BEGIN'), c.execute('INSERT INTO cats VALUES (\\'Socks\\', "
   "\\'white\\', 4.2)'), c.rollback(), c.execute('SELECT count(*) FROM cats').fetchone()[0], c.execute('BEGIN'), c.execute('INSERT INTO cats VALUES (\\'Socks\\', "
   "\\'white\\', 4.2)'), c.commit(), c.execute('SELECT count(*) FROM cats').fetchone()[0])[3::4]))))(__import__('sqlite3').connect(':memory:', isolation_level=None))",
   '(3, 4)')),
 ('TransactionControl',
  'Boundaries',
  'AutocommitModes',
  "sqlite3.connect('example.db', autocommit=False)",
  'The autocommit argument chooses the transaction behaviour: False keeps a transaction always open until commit or rollback and is the one the documentation '
  "recommends, True gives SQLite's own autocommit where commit and rollback do nothing, and the default LEGACY_TRANSACTION_CONTROL lets isolation_level decide, where "
  'None, as in the chapter, means no transaction is opened implicitly.',
  ("tuple(__import__('sqlite3').connect(':memory:', autocommit=a).in_transaction for a in (False, True))", '(True, False)')),
 ('TransactionControl',
  'Boundaries',
  'ContextManagerTransaction',
  'with conn: conn.execute(...)',
  'Using a connection in a with statement commits the open transaction when the block ends normally and rolls it back when the block raises, and it does not close the '
  'connection; contextlib.closing closes it.',
  None),
 ('TransactionControl',
  'Guarantees',
  'AcidProperties',
  'BEGIN; INSERT ...; COMMIT',
  'A transaction is atomic (all or nothing), consistent (constraints such as NOT NULL, UNIQUE and CHECK hold at its end), isolated (others do not see its partial work) '
  'and durable (once committed it survives a crash); a statement that breaks a constraint raises IntegrityError and its changes are undone.',
  None),
 ('TableStructure',
  'Changing',
  'RenameTableColumn',
  'ALTER TABLE cats RENAME TO felines',
  "ALTER TABLE ... RENAME TO changes a table's name and ALTER TABLE ... RENAME COLUMN a TO b a column's name, keeping the data; queries in the program that use the old "
  'names must be changed to match.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), (c.execute('ALTER TABLE cats RENAME TO felines'), c.execute('ALTER TABLE "
   "felines RENAME COLUMN fur TO description'), c.execute('PRAGMA table_info(felines)').fetchall()[1], c.execute('SELECT name FROM sqlite_schema WHERE type = "
   "\\'table\\'').fetchall())[2:]))))(__import__('sqlite3').connect(':memory:'))",
   "((1, 'description', 'TEXT', 0, None, 0), [('felines',)])")),
 ('TableStructure',
  'Changing',
  'AddDropColumn',
  'ALTER TABLE felines ADD COLUMN is_loved INTEGER DEFAULT 1',
  'ALTER TABLE ... ADD COLUMN appends a column that existing rows receive as its default value, and ALTER TABLE ... DROP COLUMN removes a column together with its data, '
  'but only a column that is not a primary key, not UNIQUE, not indexed and not used by another part of the schema.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), (c.execute('ALTER TABLE cats ADD COLUMN is_loved INTEGER DEFAULT 1'), "
   "c.execute('SELECT * FROM cats LIMIT 1').fetchall(), c.execute('ALTER TABLE cats DROP COLUMN is_loved'), len(c.execute('PRAGMA "
   "table_info(cats)').fetchall()))[1::2]))))(__import__('sqlite3').connect(':memory:'))",
   "([('Zophie', 'black', 5.6, 1)], 3)")),
 ('TableStructure',
  'Changing',
  'DropTable',
  'DROP TABLE felines',
  'DROP TABLE deletes a table with all its rows and cannot be undone except from a backup; DROP TABLE IF EXISTS does not complain about a missing table.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', "
   "\\'black\\', 5.6), (\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), (c.execute('DROP TABLE cats'), c.execute('DROP TABLE IF EXISTS cats'), "
   "c.execute('SELECT name FROM sqlite_schema WHERE type = \\'table\\'').fetchall())[2]))))(__import__('sqlite3').connect(':memory:'))",
   '[]')),
 ('TableStructure',
  'Linking',
  'ForeignKey',
  'FOREIGN KEY(cat_id) REFERENCES cats(id)',
  'A foreign key is a column of one table whose values must match the parent key of another table, so varying amounts of data, such as many vaccinations for one cat, '
  'become rows of a second table that point back to the first; the parent key must be a named PRIMARY KEY or UNIQUE column, and the rowid cannot be named as one.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (id INTEGER PRIMARY KEY, name TEXT NOT NULL, birthdate TEXT) STRICT; CREATE TABLE vaccinations (vaccine "
   "TEXT, date_administered TEXT, cat_id INTEGER, FOREIGN KEY(cat_id) REFERENCES cats(id)) STRICT; INSERT INTO cats(name) VALUES (\\'Zophie\\'); INSERT INTO "
   "vaccinations VALUES (\\'rabies\\', \\'2023-06-06\\', 1), (\\'FeLV\\', \\'2023-06-06\\', 99);'), c.execute('PRAGMA "
   "foreign_key_check').fetchall()))))(__import__('sqlite3').connect(':memory:'))",
   "[('vaccinations', 2, 'cats', 0)]")),
 ('TableStructure',
  'Linking',
  'InnerJoin',
  'SELECT * FROM cats INNER JOIN vaccinations ON cats.id = vaccinations.cat_id',
  'An inner join returns one combined row for every pair of rows, one from each table, for which the ON condition holds, so rows without a partner in the other table do '
  'not appear.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (id INTEGER PRIMARY KEY, name TEXT NOT NULL, birthdate TEXT) STRICT; CREATE TABLE vaccinations (vaccine "
   "TEXT, date_administered TEXT, cat_id INTEGER, FOREIGN KEY(cat_id) REFERENCES cats(id)) STRICT; INSERT INTO cats(name) VALUES (\\'Zophie\\'), (\\'Miguel\\'); INSERT "
   "INTO vaccinations VALUES (\\'rabies\\', \\'2023-06-06\\', 1), (\\'FeLV\\', \\'2023-06-06\\', 1);'), c.execute('SELECT cats.name, vaccinations.vaccine FROM cats "
   "INNER JOIN vaccinations ON cats.id = vaccinations.cat_id ORDER BY vaccinations.rowid').fetchall()))))(__import__('sqlite3').connect(':memory:'))",
   "[('Zophie', 'rabies'), ('Zophie', 'FeLV')]")),
 ('TableStructure',
  'Linking',
  'LeftJoin',
  'SELECT cats.name FROM cats LEFT JOIN vaccinations ON ... WHERE vaccinations.vaccine IS NULL',
  "A left join keeps every row of the left table and fills the columns of the right table with NULL where no row matches, so testing the right table's column with IS "
  'NULL finds the rows that have no partner, such as the cats with no vaccination at all.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (id INTEGER PRIMARY KEY, name TEXT NOT NULL, birthdate TEXT) STRICT; CREATE TABLE vaccinations (vaccine "
   "TEXT, date_administered TEXT, cat_id INTEGER, FOREIGN KEY(cat_id) REFERENCES cats(id)) STRICT; INSERT INTO cats(name) VALUES (\\'Zophie\\'), (\\'Miguel\\'); INSERT "
   "INTO vaccinations VALUES (\\'rabies\\', \\'2023-06-06\\', 1);'), c.execute('SELECT cats.name FROM cats LEFT JOIN vaccinations ON cats.id = vaccinations.cat_id WHERE "
   "vaccinations.vaccine IS NULL').fetchall()))))(__import__('sqlite3').connect(':memory:'))",
   "[('Miguel',)]")),
 ('TableStructure',
  'Linking',
  'ForeignKeyEnforcement',
  'PRAGMA foreign_keys = ON',
  'SQLite checks foreign keys only after PRAGMA foreign_keys = ON has been run on that connection, which must be done outside a transaction; while it is off, a row that '
  'points to a missing parent is accepted silently.',
  ("(lambda c: (c.execute('PRAGMA foreign_keys').fetchone(), c.execute('PRAGMA foreign_keys = ON'), c.execute('PRAGMA "
   "foreign_keys').fetchone())[::2])(__import__('sqlite3').connect(':memory:'))",
   '((0,), (1,))')),
 ('CopiesAndTools',
  'Copying',
  'InMemoryDatabase',
  "sqlite3.connect(':memory:')",
  "The name ':memory:' gives a database that lives only in RAM, is fast, and is gone when the connection closes or the program ends; every connection to ':memory:' gets "
  'its own separate database.',
  ("(lambda a, b: next(reversed((a.execute('CREATE TABLE t (x)'), b.execute('SELECT name FROM sqlite_schema').fetchall()))))(__import__('sqlite3').connect(':memory:'), "
   "__import__('sqlite3').connect(':memory:'))",
   '[]')),
 ('CopiesAndTools',
  'Copying',
  'BackupMethod',
  'conn.backup(backup_conn)',
  'source.backup(target) copies a whole database, also while it is in use, into the database of another connection, which can be a file, so it saves an in-memory '
  'database to disk or loads a file into memory; copying the file with shutil.copy is safe only while no program uses it.',
  ("(lambda a, b: (a.executescript('CREATE TABLE cats (name TEXT NOT NULL, fur TEXT, weight_kg REAL) STRICT; INSERT INTO cats VALUES (\\'Zophie\\', \\'black\\', 5.6), "
   "(\\'Miguel\\', \\'siamese\\', 6.2), (\\'Toby\\', \\'black\\', 6.8);'), a.backup(b), b.execute('SELECT count(*) FROM "
   "cats').fetchone())[2])(__import__('sqlite3').connect(':memory:'), __import__('sqlite3').connect(':memory:'))",
   '(3,)')),
 ('CopiesAndTools',
  'Copying',
  'DumpMethod',
  'for line in conn.iterdump():',
  'iterdump yields the text of the SQL statements that would re-create the database, so writing them to a file gives a readable copy that executescript can load again; '
  'for a small database the text can be shorter than the database file, whose size is a whole number of pages.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE t (a TEXT); INSERT INTO t VALUES (\\'x\\');'), "
   "list(c.iterdump())))))(__import__('sqlite3').connect(':memory:'))",
   '[\'BEGIN TRANSACTION;\', \'CREATE TABLE t (a TEXT);\', \'INSERT INTO "t" VALUES(\\\'x\\\');\', \'COMMIT;\']')),
 ('CopiesAndTools',
  'Tools',
  'SqliteApps',
  'python -m sqlite3 example.db',
  'The sqlite3 command-line program, and since Python 3.12 the same kind of shell started with python -m sqlite3, run SQL typed at a prompt, and graphical programs such '
  'as DB Browser for SQLite, SQLite Studio and DBeaver show the tables; SQL typed into the command-line shell ends with a semicolon.',
  None),
 ('ChapterPractice',
  'Programs',
  'VaccinationChecker',
  'SELECT cats.name FROM cats LEFT JOIN vaccinations ...',
  "The first practice program lists the cats that lack any of the vaccines rabies, FeLV and FVRCP and finds vaccinations dated before the cat's birthday; both are "
  "answered by queries over the two tables, here with a small table written for this study because the chapter's sweigartcats.db was not downloaded.",
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE cats (id INTEGER PRIMARY KEY, name TEXT NOT NULL, birthdate TEXT) STRICT; CREATE TABLE vaccinations (vaccine "
   "TEXT, date_administered TEXT, cat_id INTEGER, FOREIGN KEY(cat_id) REFERENCES cats(id)) STRICT; INSERT INTO cats(name, birthdate) VALUES (\\'Zophie\\', "
   "\\'2021-01-24\\'), (\\'Miguel\\', \\'2016-12-24\\'), (\\'Toby\\', \\'2021-05-17\\'); INSERT INTO vaccinations VALUES (\\'rabies\\', \\'2023-06-06\\', 1), "
   "(\\'FeLV\\', \\'2023-06-06\\', 1), (\\'FVRCP\\', \\'2023-06-06\\', 1), (\\'rabies\\', \\'2017-01-01\\', 2), (\\'FeLV\\', \\'2021-01-01\\', 3), (\\'rabies\\', "
   "\\'2022-01-01\\', 3), (\\'FVRCP\\', \\'2022-01-01\\', 3);'), (c.execute('SELECT cats.name FROM cats WHERE (SELECT count(DISTINCT vaccine) FROM vaccinations WHERE "
   "cat_id = cats.id AND vaccine IN (\\'rabies\\', \\'FeLV\\', \\'FVRCP\\')) < 3 ORDER BY cats.id').fetchall(), c.execute('SELECT cats.name, vaccinations.vaccine FROM "
   'cats JOIN vaccinations ON vaccinations.cat_id = cats.id WHERE vaccinations.date_administered < '
   "cats.birthdate').fetchall())))))(__import__('sqlite3').connect(':memory:'))",
   "([('Miguel',)], [('Toby', 'FeLV')])")),
 ('ChapterPractice',
  'Programs',
  'MealIngredients',
  'meal:ingredient1,ingredient2',
  "The second practice program keeps meals and their ingredients in two linked tables and answers a typed name with the meal's ingredients, or with every meal that uses "
  'the ingredient; the two CREATE TABLE statements the chapter gives reference meals(rowid), which SQLite rejects once foreign keys are on, so a solution declares an '
  'INTEGER PRIMARY KEY in meals.',
  ("(lambda c: next(reversed((c.executescript('CREATE TABLE meals (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE) STRICT; CREATE TABLE ingredients (name TEXT NOT "
   "NULL, meal_id INTEGER NOT NULL, FOREIGN KEY(meal_id) REFERENCES meals(id)) STRICT; INSERT INTO meals(name) VALUES (\\'onigiri\\'), (\\'chicken and rice\\'); INSERT "
   "INTO ingredients VALUES (\\'rice\\', 1), (\\'nori\\', 1), (\\'salt\\', 1), (\\'chicken\\', 2), (\\'rice\\', 2);'), ([r[0] for r in c.execute('SELECT "
   "ingredients.name FROM ingredients JOIN meals ON meals.id = ingredients.meal_id WHERE meals.name = ? ORDER BY ingredients.rowid', ('onigiri',))], [r[0] for r in "
   "c.execute('SELECT meals.name FROM meals JOIN ingredients ON meals.id = ingredients.meal_id WHERE ingredients.name = ? ORDER BY meals.id', "
   "('rice',))])))))(__import__('sqlite3').connect(':memory:'))",
   "(['rice', 'nori', 'salt'], ['onigiri', 'chicken and rice'])")),
 ('ChapterPractice',
  'Questions',
  'PracticeQuestions',
  'SELECT typeof(5), typeof(5.0)',
  'The 16 practice questions ask for the commands and terms of the chapter: connect, CREATE TABLE, isolation_level=None, INTEGER against REAL, STRICT, SELECT *, CRUD, '
  "ACID, INSERT, DELETE, an UPDATE without WHERE, an index, a foreign key, DROP TABLE, ':memory:' and backup.",
  ("(lambda c: c.execute('SELECT typeof(5), typeof(5.0), 5 = 5.0').fetchone())(__import__('sqlite3').connect(':memory:'))", "('integer', 'real', 1)"))]
ERRORS = []
CLAIMS = [("(__import__('sqlite3').paramstyle, __import__('sqlite3').apilevel)", "('qmark', '2.0')"),
 ("(lambda s: (s.LEGACY_TRANSACTION_CONTROL, s.connect(':memory:').autocommit, s.connect(':memory:').isolation_level))(__import__('sqlite3'))", "(-1, -1, '')"),
 ("__import__('sqlite3').connect(':memory:', isolation_level=None).isolation_level", 'None'),
 ("__import__('sqlite3').sqlite_version_info >= (3, 37, 0)", 'True'),
 ("[hasattr(__import__('sqlite3').Connection, m) for m in ('backup', 'iterdump', 'executemany', 'executescript', 'setconfig', 'serialize', 'blobopen')]",
  '[True, True, True, True, True, True, True]'),
 ("[c.__name__ for c in __import__('sqlite3').IntegrityError.__mro__[:5]]", "['IntegrityError', 'DatabaseError', 'Error', 'Exception', 'BaseException']"),
 ("__import__('sqlite3').connect(':memory:').execute('PRAGMA foreign_keys').fetchone()", '(0,)'),
 ("(lambda c: (c.execute('SELECT 1, 2').fetchone(), c.execute('SELECT 1, 2').description[0][0]))(__import__('sqlite3').connect(':memory:'))", "((1, 2), '1')"),
 ("(lambda c: (c.execute('CREATE TABLE t (a)'), c.execute('SELECT name FROM sqlite_master').fetchall())[1])(__import__('sqlite3').connect(':memory:'))", "[('t',)]"),
 ("(lambda c: (c.execute('SELECT 5 = 5.0, 5 == 5.0, typeof(5), typeof(5.0)').fetchone()))(__import__('sqlite3').connect(':memory:'))", "(1, 1, 'integer', 'real')")]
BODY = {'AcidProperties': 'The chapter names atomic, consistent, isolated and durable as the ACID test and says SQLite has passed tests that simulate losing power; as executed '
                   'a NOT NULL, UNIQUE or CHECK violation raised IntegrityError and a block with one good and one bad insert left 0 rows, so the good insert was undone '
                   'too, while INSERT OR IGNORE skipped a bad row with rowcount 0 (Sweigart, 2025) (SQLite developers, 2026).',
 'AddDropColumn': "ADD COLUMN is_loved INTEGER DEFAULT 1 gave every existing row the value 1 and a fifth column (4, 'is_loved', 'INTEGER', 0, '1', 0); a NOT NULL column "
                  'without a default was refused with OperationalError: Cannot add a NOT NULL column with default value NULL, and DROP COLUMN returned the table to four '
                  'columns, but dropping the indexed weight_kg failed with OperationalError: error in index idx_w after drop column: no such column: weight_kg '
                  '(Sweigart, 2025) (SQLite developers, 2026).',
 'AutocommitModes': 'The chapter uses isolation_level=None; the documentation recommends the autocommit argument, and as executed autocommit=False kept a transaction '
                    'open from the start and let rollback() undo an insert, autocommit=True made commit() and rollback() do nothing, and in the default mode a row '
                    'inserted and not committed was lost by close() and was invisible to another connection before; the default may change in a future Python version '
                    '(Sweigart, 2025) (Python Software Foundation, 2026) (Lemburg, 1999) (SQLite developers, 2026).',
 'BackupMethod': 'src.backup(dst) copied the 18-row file database into a second file, from memory to file test.db, and from a file into memory, where the first three '
                 'rows read back as the chapter prints; with pages=1 the progress function was called with (0, 1, 2) and (101, 0, 2), 101 being SQLITE_DONE, and copying '
                 'the file with shutil.copy is safe only while nothing uses it (Sweigart, 2025) (Python Software Foundation, 2026).',
 'BeginCommitRollback': 'With isolation_level=None a statement alone is its own transaction; BEGIN opened one, in_transaction became True, rollback() undid two inserts '
                        'and left the table empty of Socks and Fluffy, and after BEGIN, two inserts and commit() both were there, as the chapter prints; a rollback() '
                        "with no BEGIN undid nothing, for the row 'Gone' stayed (Sweigart, 2025) (Python Software Foundation, 2026).",
 'Boundaries': "The chapter shows BEGIN, commit() and rollback(), and the connection's mode decides when a transaction begins and ends (Sweigart, 2025) (Python Software "
               'Foundation, 2026).',
 'Changing': 'ALTER TABLE and DROP TABLE change the structure and not the rows (Sweigart, 2025).',
 'ChapterPractice': 'The chapter ends with 16 practice questions and 2 practice programs (Sweigart, 2025).',
 'Comparison': 'The chapter compares a spreadsheet with a database table and introduces the key that names a row (Sweigart, 2025).',
 'ConnectCall': "sqlite3.connect('example.db', isolation_level=None) returns a Connection and creates an empty file when none exists, which as executed it did for a "
                'missing.db that did not exist before; a file that is not a database raised DatabaseError: file is not a database only when the first query ran; '
                "':memory:' has no file, and PRAGMA database_list showed [(0, 'main', '')]; the documentation deprecates passing the arguments after the first by "
                'position, which raised a DeprecationWarning as executed, and the chapter writes isolation_level as a keyword, the form that stays valid (Sweigart, '
                '2025) (Python Software Foundation, 2026).',
 'Connecting': 'A program reaches a database through a Connection made by sqlite3.connect (Sweigart, 2025).',
 'ConnectionAndSchema': 'The second part of the chapter opens a database, chooses the types of its columns and describes the tables it holds (Sweigart, 2025).',
 'ConnectionClose': 'The chapter says to call conn.close() when done and that the program closes the connection at its end; as executed a statement on a closed '
                    'connection raised ProgrammingError: Cannot operate on a closed database., a connection that was deleted without close() raised a ResourceWarning, '
                    "which the chapter's sessions would show under Python 3.13 and later, and with contextlib.closing the connection was closed at the end of the with "
                    "block, which the connection's own with statement does not do (Sweigart, 2025) (Python Software Foundation, 2026).",
 'ContextManagerTransaction': 'A with statement on the connection committed the row added in its block, rolled back both rows of a block that raised IntegrityError: '
                              "UNIQUE constraint failed: lang.name, leaving only 'Python', and did not close the connection, since a statement still ran afterwards; the "
                              'chapter does not show this form (Python Software Foundation, 2026).',
 'CopiesAndTools': 'A database can be kept in memory, copied to a file, written out as SQL and looked at with other programs (Sweigart, 2025).',
 'Copying': 'The chapter gives three ways to copy a database: an in-memory database saved with backup(), a copy of the file, and iterdump() (Sweigart, 2025).',
 'CreateIndex': "CREATE INDEX idx_name ON cats (name) made sqlite_schema list ('idx_name',) for the table, EXPLAIN QUERY PLAN for WHERE name = 'Toby' changed from SCAN "
                'cats to SEARCH cats USING INDEX idx_name (name=?), a query on the unindexed fur column still scanned, and DROP INDEX idx_name left only idx_birthdate, '
                'but the same EXPLAIN text run again on that connection still printed the old SEARCH plan, while the text with one more space printed SCAN cats and so '
                "did a connection made with cached_statements=0, so a plan read from a cached statement can be stale; the chapter's advice to test whether an index "
                'helps is sound, since an index costs storage and slows writes (Sweigart, 2025) (SQLite developers, 2026).',
 'CreateTable': "CREATE TABLE IF NOT EXISTS lists the table's columns, types and constraints; as executed the second creation of cats without IF NOT EXISTS raised "
                'OperationalError: table cats already exists, the statement written in lower case ran unchanged, and with IF NOT EXISTS a second creation changed '
                'nothing, so sqlite_schema still listed one table (Sweigart, 2025).',
 'CrudOperations': 'CRUD, the four basic operations, are carried out with INSERT, SELECT, UPDATE and DELETE (Sweigart, 2025).',
 'DatabaseIdea': 'The first part of Chapter 16 sets the table, the row and the key of a database against the spreadsheet, and presents SQLite as the engine, with the '
                 'limits that follow from running inside the program (Sweigart, 2025).',
 'DateAsText': "The chapter's Table 16-1 recommends YYYY-MM-DD, YYYY-MM-DD HH:MM:SS and the forms with fractions of a second; as executed date('2035-10-31', '+1 day') "
               "gave '2035-11-01', the text comparison '2024-03-19' < '2024-12-09' gave 1 and datetime('2035-10-31 16:30:00', '+1 hour') gave '2035-10-31 17:30:00'; a "
               "datetime.date bound as a parameter was stored as '2035-10-31' but raised a DeprecationWarning, since the default adapters are deprecated since Python "
               '3.12 (Sweigart, 2025) (Python Software Foundation, 2026).',
 'DeleteStatement': 'DELETE FROM cats WHERE rowid = 1 removed one row and a later SELECT for it gave []; with WHERE 1 it removed all 18 rows, and as executed the '
                    'connection counted 76 changes in total for the whole session (Sweigart, 2025) (Python Software Foundation, 2026).',
 'DropTable': 'DROP TABLE felines left [] in sqlite_schema, a second DROP TABLE raised OperationalError: no such table: felines, and DROP TABLE IF EXISTS did not; the '
              "chapter's last advice, to limit how often tables are changed because the program's queries must follow, is sound (Sweigart, 2025).",
 'DumpMethod': "iterdump() gave 21 lines for the 18 rows, from 'BEGIN TRANSACTION;' through the CREATE TABLE statement and one INSERT INTO statement per row, the first "
               "being INSERT INTO cats with Zophie's values, to 'COMMIT;', and executescript() of those lines rebuilt 18 rows with the same CREATE TABLE text; the "
               "chapter's dump prints the table name in quotes, CREATE TABLE with the name cats quoted, which as executed appears in the dump only after a table has "
               'been renamed, for a renamed and renamed-back cats printed quoted and a fresh one did not; the filter argument of Python 3.13 limits the dump to objects '
               "matching a pattern, and the chapter's claim that the dump is larger than the database did not hold for this small database, where the dump was shorter "
               'than the 8192-byte file (Sweigart, 2025) (Python Software Foundation, 2026).',
 'EmbeddedSingleFile': 'SQLite runs inside the Python program, needs no installation, server or network, and keeps the database in one file that can be copied like any '
                       "file, and as executed the file made by the chapter's kind of CREATE TABLE begins with the 15 bytes b'SQLite format 3'; the chapter adds that "
                       'SQLite has no GRANT or REVOKE and does not strictly enforce column types, the second of which STRICT tables change (Sweigart, 2025) (SQLite '
                       'developers, 2026).',
 'Engine': 'The chapter lists what makes SQLite different from server databases and where it is weakest (Sweigart, 2025).',
 'FetchAndIterate': "fetchall() returns a list of tuples, and a for loop over the cursor needs no fetchall; as executed fetchone() gave ('Celine',), fetchmany(2) the "
                    'next two, fetchall() the remaining 15 and a further fetchall() gave [], because a cursor is used up once it has been read (Sweigart, 2025) (Python '
                    'Software Foundation, 2026).',
 'ForeignKey': "The chapter's vaccinations table declares FOREIGN KEY(cat_id) REFERENCES cats(rowid), and as executed that declaration never constrains anything: with "
               'PRAGMA foreign_keys OFF the insert of cat_id 999 was accepted, and with ON every insert failed with OperationalError: foreign key mismatch, naming the '
               'child and the parent table, because the parent key must be a named column and not the rowid; with cats(id) and id INTEGER PRIMARY KEY, PRAGMA '
               "foreign_key_check found the orphan [('vaccinations', 2, 'cats', 0)], and with enforcement on an insert of 999, a delete of a used cat and an update to 5 "
               'each raised IntegrityError: FOREIGN KEY constraint failed (Sweigart, 2025) (SQLite developers, 2026).',
 'ForeignKeyEnforcement': 'The chapter says the safety features are off by default and turned on with PRAGMA foreign_keys = ON, and as executed the setting read (0,) on '
                          'a new connection and (1,) after the pragma; run inside a transaction it stayed at 1 after PRAGMA foreign_keys = OFF, and with ON DELETE '
                          'CASCADE deleting a parent removed its child rows (Sweigart, 2025) (SQLite developers, 2026).',
 'GroupAndCount': 'GROUP BY, which the chapter lists among the clauses it leaves out, counted the 18 cats as black 5, bengal 3 and white 3 for the three largest groups, '
                  "and SELECT fur, count(*), round(avg(weight_kg), 2) gave [('black', 2, 6.2), ('siamese', 1, 6.2)] on a three-cat table (Sweigart, 2025) (Python "
                  'Software Foundation, 2026).',
 'Guarantees': 'The ACID properties say what a transaction promises (Sweigart, 2025).',
 'InMemoryDatabase': "The name ':memory:' gave a database that, as executed, was separate for each connection: a table made through one connection was absent, "
                     'OperationalError: no such table: t, through another; it is lost when the program ends, so the chapter advises saving it with backup() and wrapping '
                     'the code in try and except (Sweigart, 2025) (SQLite developers, 2026).',
 'InnerJoin': "INNER JOIN cats ON cats.rowid = vaccinations.cat_id returned one row for each vaccination, four of them for the sample data, with Zophie's columns "
              'repeated for her two vaccinations and no row for a cat with no vaccination, as the chapter prints (Sweigart, 2025).',
 'InsertStatement': "INSERT INTO cats VALUES ('Zophie', '2021-01-24', 'black', 5.6) adds one row; as executed the cursor reported rowcount 1 and lastrowid 19 after the "
                    '18th cat, and a value listed in the wrong order would land in the wrong column, since VALUES has no names unless the columns are listed (Sweigart, '
                    '2025) (Python Software Foundation, 2026).',
 'LeftJoin': 'The chapter does not show the left join, which keeps the left rows with no partner: as executed it found the cats without any vaccination, Miguel, Jacob '
             'and Toby being the first three in the 18-row table, where the inner join shows none of them (Sweigart, 2025) (Python Software Foundation, 2026).',
 'LikeAndGlob': "LIKE '%y' matched 5 names of the 18 cats, LIKE 'Ja%' matched Jacob and Jasmine, and LIKE '%OB%' matched Jacob and Toby because LIKE ignores case, where "
                "GLOB '*M*' matched Miguel and Mango and GLOB '*m*' only Jasmine; the case rule covers ASCII letters only, for 'a' LIKE 'A' was 1 and 'æ' LIKE 'Æ' was 0 "
                '(Sweigart, 2025) (SQLite developers, 2026).',
 'LimitClause': "LIMIT 3 returned the same three rows as slicing the fetched list with [:3], True as executed, and WHERE fur = 'black' ORDER BY birthdate LIMIT 2 gave "
                'Thor and Hope, the two oldest black cats; the database stops early where the slice reads every row first (Sweigart, 2025).',
 'Linking': 'A foreign key links the rows of one table to those of another, and a join reads them together (Sweigart, 2025).',
 'ManyRows': 'The chapter inserts one row at a time; executemany() runs one parameterised statement for a whole list of rows, and as executed it added 2 rows and '
             'reported rowcount 2 (Sweigart, 2025) (Python Software Foundation, 2026).',
 'MealIngredients': 'The second program stores meals and ingredients; the two CREATE TABLE statements the chapter gives use meals(rowid), and as executed a solution '
                    "that declares id INTEGER PRIMARY KEY in meals enforced the link, printed the chapter's transcript for onigiri, chicken and rice, and 'rice' listed "
                    'onigiri and then chicken and rice, and a meal entered twice printed Not added: UNIQUE constraint failed: meals.name (Sweigart, 2025).',
 'OrderByClause': 'ORDER BY fur, birthdate put the three bengal cats first, in date order, and ORDER BY fur ASC, birthdate DESC reversed the dates inside each color, '
                  'giving Ruby, Elton, Iris, Toby as the first four; ORDER BY comes after WHERE, and a query without it promises no order (Sweigart, 2025).',
 'Placeholders': "The chapter shows an f-string query as the wrong way and a ? with a list as the right way, and as executed the input x' OR '1'='1 returned all 3 rows "
                 'through the f-string and 0 rows through the placeholder; a dict with :name placeholders also works, and execute refused more than one statement, a '
                 'wrong number of values, a dict for ? placeholders, a sequence for named ones (an error since Python 3.14) and a dict as a value, each with '
                 'ProgrammingError (Sweigart, 2025) (Python Software Foundation, 2026).',
 'PracticeQuestions': 'The 16 questions ask for connect and CREATE TABLE, autocommit mode, INTEGER against REAL, strict mode, SELECT *, CRUD, ACID, INSERT, DELETE, '
                      "UPDATE without WHERE, an index, a foreign key, DROP TABLE, the ':memory:' name and copying a database; as executed 5 = 5.0 was 1 while typeof(5) "
                      "was 'integer' and typeof(5.0) was 'real', which is the difference of question 4 (Sweigart, 2025).",
 'Programs': 'The two practice programs put several tables and queries to work (Sweigart, 2025).',
 'Questions': 'The practice questions ask for the terms and commands of the chapter (Sweigart, 2025).',
 'Reading': 'SELECT reads rows, and the clauses after it filter, order and limit them (Sweigart, 2025).',
 'RenameTableColumn': "ALTER TABLE cats RENAME TO felines changed the table's name in sqlite_schema to 'felines', and RENAME COLUMN fur TO description changed the tuple "
                      "of the third column from (2, 'fur', 'TEXT', 0, None, 0) to (2, 'description', 'TEXT', 0, None, 0), as the chapter prints (Sweigart, 2025) (SQLite "
                      'developers, 2026).',
 'RowFactory': "The chapter reads columns by tuple index; with row_factory set to sqlite3.Row the same row answered to r['name'], to r['WEIGHT_KG'] in any case and to "
               "keys(), ['name', 'weight_kg'], and stayed indexable by position (Sweigart, 2025) (Python Software Foundation, 2026).",
 'RowidKey': "The chapter says each record has a primary key, called rowid in SQLite, that 'is unique and doesn't change'; SELECT * leaves it out, SELECT rowid, * shows "
             'it, and the rule holds only while rows are not deleted and the file is not compacted: after the row with the highest rowid was deleted, the next INSERT '
             "received the same number, [(1, 'a'), (2, 'b'), (3, 'd')], and after four deletions and VACUUM the rows numbered 5, 6, 7 became 1, 2, 3; with id INTEGER "
             'PRIMARY KEY the freed 2 was given again, and with AUTOINCREMENT the next row got 3, all as executed (Sweigart, 2025) (SQLite developers, 2026).',
 'Schema': 'A database describes itself in a built-in table and in PRAGMA statements (Sweigart, 2025).',
 'SchemaTable': "sqlite_schema lists the database's objects, and as executed SELECT type, name FROM sqlite_schema ORDER BY type, name gave [('index', 'idx_name'), "
                "('table', 'cats')] for a table and one index; the older name sqlite_master lists the same table, and the chapter's warning not to change this table is "
                'sound (Sweigart, 2025) (Python Software Foundation, 2026).',
 'SelectStatement': "SELECT * returns the columns except rowid, SELECT rowid, name returned [(1, 'Zophie'), (2, 'Miguel')] for the first two cats, and each row is a "
                    "tuple in the order of the table's columns (Sweigart, 2025).",
 'Speed': 'An index makes reading by a column faster at a price in writing (Sweigart, 2025).',
 'SpreadsheetVersusTable': "The chapter treats a table as a spreadsheet of records, with the cats table 'essentially the same as' a list of tuples, and as executed the "
                           'rows sqlite3 returns are tuples, so fetchone() on SELECT * gave a tuple; the difference it stresses is that databases have a stricter '
                           'structure than a spreadsheet, which is why a formatted fill-in form does not belong in one (Sweigart, 2025) (Python Software Foundation, '
                           '2026).',
 'SqliteApps': 'The chapter installs the sqlite3 command and names DB Browser for SQLite, SQLite Studio and DBeaver Community; none of these was run here, and no '
               'sqlite3 command is installed on the machine that built this page; the shell that comes with Python, python -m sqlite3 file statement, added in Python '
               "3.12, was run and printed the row as a Python tuple, ('Zophie', 4.7), where the chapter's tool prints Zophie|2021-01-24|gray tabby|4.7 (Sweigart, 2025) "
               '(Python Software Foundation, 2026) (SQLite developers, 2026).',
 'StorageClasses': 'The chapter names NULL, INTEGER, REAL, TEXT and BLOB next to None, int, float, str and bytes and says it lists six types, where SQLite names five '
                   "storage classes; as executed typeof() gave ('null', 'integer', 'real', 'text', 'blob'), a Python True was stored as the integer 1, and there is no "
                   'Boolean or date class, as the chapter says (Sweigart, 2025) (SQLite developers, 2026).',
 'StrictTable': "STRICT makes the column types rules: as executed '42' became (42, 'integer'), 'Hello' raised IntegrityError: cannot store TEXT value in INTEGER column "
                'strict_t.n, and a column without a type raised OperationalError: missing datatype for untyped.a; the allowed types are INT, INTEGER, REAL, TEXT, BLOB '
                'and ANY; the chapter is right that STRICT needs SQLite 3.37.0, but the version of SQLite depends on the library linked, sqlite3.sqlite_version being '
                '3.50.4 here, and not on the Python version as the chapter implies, since Python 3.13 and later need only SQLite 3.15.2 to be built (Sweigart, 2025) '
                '(Python Software Foundation, 2026) (SQLite developers, 2026).',
 'TableInfo': "PRAGMA TABLE_INFO(cats) gave the six-item tuple of each column, as the chapter prints it, [(0, 'name', 'TEXT', 1, None, 0), (1, 'birthdate', 'TEXT', 0, "
              "None, 0), (2, 'fur', 'TEXT', 0, None, 0), (3, 'weight_kg', 'REAL', 0, None, 0)], with 1 for NOT NULL and the last item 1 for a primary key (Sweigart, "
              '2025).',
 'TableStructure': 'Tables can be changed after they exist and linked to each other (Sweigart, 2025).',
 'Tools': 'Other programs show what is in a SQLite file without Python code (Sweigart, 2025).',
 'TransactionControl': 'A transaction groups statements so that they are kept together or undone together, and the connection decides when one starts (Sweigart, 2025).',
 'TypeAffinity': "In an ordinary table a column has an affinity and not a rule: as executed the values '42', 'Hello', 3.0 and 3.5 put into an INTEGER column were stored "
                 "as (42, 'integer'), ('Hello', 'text'), (3, 'integer') and (3.5, 'real'), so the text that cannot be converted is kept without any error, as the "
                 'chapter says (Sweigart, 2025) (SQLite developers, 2026).',
 'Typing': 'Column types decide how SQLite converts and checks the values that are stored (Sweigart, 2025).',
 'UpdateStatement': 'UPDATE changes every row for which WHERE is true and every row when it is missing, which as executed changed 1 row with WHERE rowid = 1 and all 18 '
                    "with no WHERE, leaving one distinct fur; the chapter's advice to write WHERE 1 to mean every row was run and changed 18 rows, and an update that "
                    'matches nothing reported 0 (Sweigart, 2025) (Python Software Foundation, 2026).',
 'VaccinationChecker': "The first program asks for the cats lacking rabies, FeLV or FVRCP and for vaccinations dated before the cat's birthday; the downloaded file was "
                       'not available, so over the 18 rows and a few vaccinations written for this study the query found 16 cats lacking some of the three vaccines, the '
                       "first being Miguel, Jacob and Toby, and one vaccination before birth, Thor's rabies on 2012-01-01 against a birthday of 2013-05-14, with the "
                       'comparison made on dates in YYYY-MM-DD text (Sweigart, 2025).',
 'WhereFilter': "WHERE fur = 'black' returned the five black cats, and WHERE fur = 'black' OR birthdate >= '2024-01-01' returned the ten cats the chapter prints, "
                "because dates in the form YYYY-MM-DD compare in date order; the chapter's example with double quotes works, but a double-quoted word is a column name "
                'when one has that name, so comparing a column a with the word a in double quotes matched every row while the word in single quotes matched none, and '
                "with setconfig(SQLITE_DBCONFIG_DQS_DML, False) the chapter's kind of query raised OperationalError (Sweigart, 2025) (SQLite developers, 2026).",
 'WriterLimit': 'The chapter names one disadvantage, that SQLite cannot efficiently handle hundreds or thousands of simultaneous writes; the documentation states the '
                'rule behind it, one writer at a time, and as executed a second connection that tried to write while the first held BEGIN IMMEDIATE waited its timeout '
                'of 0.2 second and then raised OperationalError: database is locked, while a reader still saw 0 rows; the default wait is 5 seconds, and write-ahead '
                'logging, which PRAGMA journal_mode=WAL switched on in the run, lets readers and the writer work together (Sweigart, 2025) (Python Software Foundation, '
                '2026) (SQLite developers, 2026).',
 'Writing': 'INSERT, UPDATE and DELETE change the database, and placeholders keep values out of the SQL text (Sweigart, 2025).'}
BEH = [["the chapter's first session: connect, create a STRICT table, list tables and columns, see the errors and lower-case keywords",
  'import sqlite3, tempfile, os\n'
  'os.chdir(tempfile.mkdtemp())\n'
  "conn = sqlite3.connect('example.db', isolation_level=None)\n"
  "cur = conn.execute('CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT')\n"
  'print(type(cur).__name__)\n'
  'print(conn.execute(\'SELECT name FROM sqlite_schema WHERE type="table"\').fetchall())\n'
  "print(conn.execute('PRAGMA TABLE_INFO(cats)').fetchall())\n"
  'try:\n'
  "    conn.execute('CREATE TABLE cats (name TEXT)')\n"
  'except sqlite3.OperationalError as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))\n"
  "print(type(conn.execute('create table if not exists cats (name text not null, birthdate text, fur text, weight_kg real) strict')).__name__)\n"
  'conn.close()\n'
  "open('bad.db', 'w').write('this is not a database at all, padding padding padding padding')\n"
  "bad = sqlite3.connect('bad.db')\n"
  'try:\n'
  "    bad.execute('SELECT * FROM cats')\n"
  'except sqlite3.DatabaseError as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))\n"
  'bad.close()\n'
  "print(os.path.exists('example.db'), os.path.exists('missing.db'))\n"
  "sqlite3.connect('missing.db').close()\n"
  "print(os.path.exists('missing.db'))",
  'Cursor\n'
  "[('cats',)]\n"
  "[(0, 'name', 'TEXT', 1, None, 0), (1, 'birthdate', 'TEXT', 0, None, 0), (2, 'fur', 'TEXT', 0, None, 0), (3, 'weight_kg', 'REAL', 0, None, 0)]\n"
  'OperationalError: table cats already exists\n'
  'Cursor\n'
  'DatabaseError: file is not a database\n'
  'True False\n'
  'True'],
 ['type affinity in an ordinary table against STRICT mode, and the types a Python value becomes',
  'import sqlite3\n'
  "c = sqlite3.connect(':memory:')\n"
  "c.execute('CREATE TABLE loose (n INTEGER)')\n"
  "c.executemany('INSERT INTO loose VALUES (?)', [('42',), ('Hello',), (3.0,), (3.5,)])\n"
  "print(c.execute('SELECT n, typeof(n) FROM loose').fetchall())\n"
  "c.execute('CREATE TABLE strict_t (n INTEGER) STRICT')\n"
  'c.execute("INSERT INTO strict_t VALUES (\'42\')")\n'
  "print(c.execute('SELECT n, typeof(n) FROM strict_t').fetchall())\n"
  'try:\n'
  '    c.execute("INSERT INTO strict_t VALUES (\'Hello\')")\n'
  'except sqlite3.IntegrityError as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))\n"
  'try:\n'
  "    c.execute('CREATE TABLE untyped (a) STRICT')\n"
  'except sqlite3.OperationalError as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))\n"
  "c.execute('CREATE TABLE anyt (v)')\n"
  "c.executemany('INSERT INTO anyt VALUES (?)', [(None,), (1,), (1.5,), ('a',), (b'\\x00',), (True,)])\n"
  "print(c.execute('SELECT typeof(v), v FROM anyt').fetchall())\n"
  'print(sqlite3.sqlite_version_info >= (3, 37, 0))\n'
  'c.close()',
  "[(42, 'integer'), ('Hello', 'text'), (3, 'integer'), (3.5, 'real')]\n"
  "[(42, 'integer')]\n"
  'IntegrityError: cannot store TEXT value in INTEGER column strict_t.n\n'
  'OperationalError: missing datatype for untyped.a\n'
  "[('null', None), ('integer', 1), ('real', 1.5), ('text', 'a'), ('blob', b'\\x00'), ('integer', 1)]\n"
  'True'],
 ['placeholders against string formatting, named placeholders, and what execute refuses',
  'import sqlite3, warnings, datetime\n'
  "c = sqlite3.connect(':memory:')\n"
  "c.execute('CREATE TABLE cats (name TEXT, fur TEXT)')\n"
  "c.executemany('INSERT INTO cats VALUES (?, ?)', [('Zophie', 'black'), ('Toby', 'black'), ('Miguel', 'siamese')])\n"
  'evil = "x\' OR \'1\'=\'1"\n'
  'print(len(c.execute(f"SELECT * FROM cats WHERE name = \'{evil}\'").fetchall()), len(c.execute(\'SELECT * FROM cats WHERE name = ?\', (evil,)).fetchall()))\n'
  "print(c.execute('SELECT name FROM cats WHERE fur = :fur AND name != :skip', {'fur': 'black', 'skip': 'Toby'}).fetchall())\n"
  "for args in (('SELECT 1; DROP TABLE cats',), ('SELECT name FROM cats WHERE fur = ?', ('a', 'b')), ('SELECT :a', (1,)), ('SELECT ?', {'a': 1})):\n"
  '    try:\n'
  '        c.execute(*args)\n'
  '    except sqlite3.ProgrammingError as e:\n'
  "        print(type(e).__name__ + ': ' + str(e))\n"
  'try:\n'
  "    c.execute('SELECT ?', ({},))\n"
  'except sqlite3.ProgrammingError as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))\n"
  "print(c.execute('SELECT count(*) FROM cats').fetchone())\n"
  'with warnings.catch_warnings(record=True) as w:\n'
  "    warnings.simplefilter('always')\n"
  "    print(c.execute('SELECT ?', (datetime.date(2035, 10, 31),)).fetchone(), [x.category.__name__ for x in w])\n"
  'print(sqlite3.paramstyle, sqlite3.apilevel)\n'
  'c.close()',
  '3 0\n'
  "[('Zophie',)]\n"
  'ProgrammingError: You can only execute one statement at a time.\n'
  'ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 2 supplied.\n'
  "ProgrammingError: Binding 1 (':a') is a named parameter, but you supplied a sequence which requires nameless (qmark) placeholders.\n"
  'ProgrammingError: Binding 1 has no name, but you supplied a dictionary (which has only names).\n'
  "ProgrammingError: Error binding parameter 1: type 'dict' is not supported\n"
  '(3,)\n'
  "('2035-10-31',) ['DeprecationWarning']\n"
  'qmark 2.0'],
 ["the chapter's CRUD statements on a table of 18 cats, with counts and the WHERE 1 habit",
  'import sqlite3\n'
  'CATS = [("Zophie","2021-01-24","black",5.6),("Miguel","2016-12-24","siamese",6.2),("Jacob","2022-02-20","orange and '
  'white",5.5),("Toby","2021-05-17","black",6.8),("Taffy","2024-12-09","white",7.0),("Hollie","2024-08-07","calico",6.0),("Lewis","2024-03-19","orange '
  'tabby",5.1),("Thor","2013-05-14","black",5.2),("Shell","2024-06-16","tortoiseshell",6.5),("Jasmine","2024-09-05","orange '
  'tabby",6.3),("Sassy","2017-08-20","black",7.5),("Hope","2016-05-22","black",7.6),("Iris","2017-07-13","bengal",6.8),("Ruby","2023-12-22","bengal",5.0),("Elton","2020-05-28","bengal",5.4),("Celine","2015-04-18","white",7.3),("Daisy","2019-03-19","white",6.0),("Mango","2017-02-12","tuxedo",6.8)]\n'
  "def make(path=':memory:', **kw):\n"
  '    c = sqlite3.connect(path, isolation_level=None, **kw)\n'
  "    c.execute('CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT')\n"
  "    c.executemany('INSERT INTO cats VALUES (?, ?, ?, ?)', CATS)\n"
  '    return c\n'
  'c = make()\n'
  "print(c.execute('SELECT * FROM cats LIMIT 2').fetchall())\n"
  "print(c.execute('SELECT rowid, name FROM cats LIMIT 2').fetchall())\n"
  'cur = c.execute("INSERT INTO cats VALUES (\'Socks\', \'2022-04-04\', \'white\', 4.2)")\n'
  'print(cur.rowcount, cur.lastrowid)\n'
  'print(c.execute("UPDATE cats SET fur = \'gray tabby\' WHERE rowid = 1").rowcount, c.execute(\'SELECT * FROM cats WHERE rowid = 1\').fetchall())\n'
  'print(c.execute("UPDATE cats SET fur = \'black\', weight_kg = 6 WHERE rowid = 1").rowcount, c.execute(\'SELECT * FROM cats WHERE rowid = 1\').fetchall())\n'
  'print(c.execute("UPDATE cats SET fur = \'orange and white\' WHERE fur = \'white and orange\'").rowcount)\n'
  "print(c.execute('DELETE FROM cats WHERE rowid = 1').rowcount, c.execute('SELECT * FROM cats WHERE rowid = 1').fetchall())\n"
  "print(c.execute('UPDATE cats SET weight_kg = weight_kg + 1 WHERE 1').rowcount)\n"
  'print(c.execute("UPDATE cats SET fur = \'x\'").rowcount, c.execute(\'SELECT count(DISTINCT fur) FROM cats\').fetchone())\n'
  "print(c.execute('DELETE FROM cats WHERE 1').rowcount, c.execute('SELECT count(*) FROM cats').fetchone())\n"
  'print(c.total_changes)\n'
  'c.close()',
  "[('Zophie', '2021-01-24', 'black', 5.6), ('Miguel', '2016-12-24', 'siamese', 6.2)]\n"
  "[(1, 'Zophie'), (2, 'Miguel')]\n"
  '1 19\n'
  "1 [('Zophie', '2021-01-24', 'gray tabby', 5.6)]\n"
  "1 [('Zophie', '2021-01-24', 'black', 6.0)]\n"
  '0\n'
  '1 []\n'
  '18\n'
  '18 (1,)\n'
  '18 (0,)\n'
  '76'],
 ["the chapter's filters, LIKE, GLOB, ordering and LIMIT on the same 18 cats",
  'import sqlite3\n'
  'CATS = [("Zophie","2021-01-24","black",5.6),("Miguel","2016-12-24","siamese",6.2),("Jacob","2022-02-20","orange and '
  'white",5.5),("Toby","2021-05-17","black",6.8),("Taffy","2024-12-09","white",7.0),("Hollie","2024-08-07","calico",6.0),("Lewis","2024-03-19","orange '
  'tabby",5.1),("Thor","2013-05-14","black",5.2),("Shell","2024-06-16","tortoiseshell",6.5),("Jasmine","2024-09-05","orange '
  'tabby",6.3),("Sassy","2017-08-20","black",7.5),("Hope","2016-05-22","black",7.6),("Iris","2017-07-13","bengal",6.8),("Ruby","2023-12-22","bengal",5.0),("Elton","2020-05-28","bengal",5.4),("Celine","2015-04-18","white",7.3),("Daisy","2019-03-19","white",6.0),("Mango","2017-02-12","tuxedo",6.8)]\n'
  "def make(path=':memory:', **kw):\n"
  '    c = sqlite3.connect(path, isolation_level=None, **kw)\n'
  "    c.execute('CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT')\n"
  "    c.executemany('INSERT INTO cats VALUES (?, ?, ?, ?)', CATS)\n"
  '    return c\n'
  'c = make()\n'
  'q = lambda sql: c.execute(sql).fetchall()\n'
  'print(q("SELECT name FROM cats WHERE fur = \'black\'"))\n'
  'print(q("SELECT name FROM cats WHERE fur = \'black\' OR birthdate >= \'2024-01-01\'"))\n'
  'print(q("SELECT rowid, name FROM cats WHERE name LIKE \'%y\'"))\n'
  'print(q("SELECT rowid, name FROM cats WHERE name LIKE \'Ja%\'"))\n'
  'print(q("SELECT rowid, name FROM cats WHERE name LIKE \'%OB%\'"))\n'
  'print(q("SELECT rowid, name FROM cats WHERE name GLOB \'*M*\'"), q("SELECT name FROM cats WHERE name GLOB \'*m*\'"))\n'
  'print(q("SELECT \'a\' LIKE \'A\', \'æ\' LIKE \'Æ\'"))\n'
  "print(q('SELECT name, fur FROM cats ORDER BY fur, birthdate')[:5])\n"
  "print(q('SELECT name, fur, birthdate FROM cats ORDER BY fur ASC, birthdate DESC')[:4])\n"
  "print(q('SELECT * FROM cats LIMIT 3') == q('SELECT * FROM cats')[:3])\n"
  'print(q("SELECT name, fur FROM cats WHERE fur = \'black\' ORDER BY birthdate LIMIT 2"))\n'
  "print(q('SELECT fur, count(*) FROM cats GROUP BY fur ORDER BY count(*) DESC, fur')[:3])\n"
  'print(q("SELECT name FROM cats WHERE weight_kg BETWEEN 3 AND 5.5 AND birthdate < \'2023-10-01\' ORDER BY name"))\n'
  "cur = c.execute('SELECT name FROM cats ORDER BY name')\n"
  'print(cur.fetchone(), cur.fetchmany(2), len(cur.fetchall()), cur.fetchall())\n'
  "for row in c.execute('SELECT * FROM cats LIMIT 1'):\n"
  "    print('Row data:', row, row[0])\n"
  'c.close()',
  "[('Zophie',), ('Toby',), ('Thor',), ('Sassy',), ('Hope',)]\n"
  "[('Zophie',), ('Toby',), ('Taffy',), ('Hollie',), ('Lewis',), ('Thor',), ('Shell',), ('Jasmine',), ('Sassy',), ('Hope',)]\n"
  "[(4, 'Toby'), (5, 'Taffy'), (11, 'Sassy'), (14, 'Ruby'), (17, 'Daisy')]\n"
  "[(3, 'Jacob'), (10, 'Jasmine')]\n"
  "[(3, 'Jacob'), (4, 'Toby')]\n"
  "[(2, 'Miguel'), (18, 'Mango')] [('Jasmine',)]\n"
  '[(1, 0)]\n'
  "[('Iris', 'bengal'), ('Elton', 'bengal'), ('Ruby', 'bengal'), ('Thor', 'black'), ('Hope', 'black')]\n"
  "[('Ruby', 'bengal', '2023-12-22'), ('Elton', 'bengal', '2020-05-28'), ('Iris', 'bengal', '2017-07-13'), ('Toby', 'black', '2021-05-17')]\n"
  'True\n'
  "[('Thor', 'black'), ('Hope', 'black')]\n"
  "[('black', 5), ('bengal', 3), ('white', 3)]\n"
  "[('Elton',), ('Jacob',), ('Thor',)]\n"
  "('Celine',) [('Daisy',), ('Elton',)] 15 []\n"
  "Row data: ('Zophie', '2021-01-24', 'black', 5.6) Zophie"],
 ['an index: the query plan before and after, dropping it, and the statement cache that keeps an old plan',
  'import sqlite3\n'
  'CATS = [("Zophie","2021-01-24","black",5.6),("Miguel","2016-12-24","siamese",6.2),("Jacob","2022-02-20","orange and '
  'white",5.5),("Toby","2021-05-17","black",6.8),("Taffy","2024-12-09","white",7.0),("Hollie","2024-08-07","calico",6.0),("Lewis","2024-03-19","orange '
  'tabby",5.1),("Thor","2013-05-14","black",5.2),("Shell","2024-06-16","tortoiseshell",6.5),("Jasmine","2024-09-05","orange '
  'tabby",6.3),("Sassy","2017-08-20","black",7.5),("Hope","2016-05-22","black",7.6),("Iris","2017-07-13","bengal",6.8),("Ruby","2023-12-22","bengal",5.0),("Elton","2020-05-28","bengal",5.4),("Celine","2015-04-18","white",7.3),("Daisy","2019-03-19","white",6.0),("Mango","2017-02-12","tuxedo",6.8)]\n'
  "def make(path=':memory:', **kw):\n"
  '    c = sqlite3.connect(path, isolation_level=None, **kw)\n'
  "    c.execute('CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT')\n"
  "    c.executemany('INSERT INTO cats VALUES (?, ?, ?, ?)', CATS)\n"
  '    return c\n'
  'c = make()\n'
  "plan = lambda sql: ' | '.join(r[3] for r in c.execute('EXPLAIN QUERY PLAN ' + sql))\n"
  'q = "SELECT * FROM cats WHERE name = \'Toby\'"\n'
  'print(plan(q))\n'
  "c.execute('CREATE INDEX idx_name ON cats (name)')\n"
  "c.execute('CREATE INDEX idx_birthdate ON cats (birthdate)')\n"
  'print(c.execute("SELECT name FROM sqlite_schema WHERE type = \'index\' AND tbl_name = \'cats\' ORDER BY name").fetchall())\n'
  'print(plan(q))\n'
  'print(plan("SELECT * FROM cats WHERE fur = \'black\'"))\n'
  "c.execute('DROP INDEX idx_name')\n"
  'print(c.execute("SELECT name FROM sqlite_schema WHERE type = \'index\'").fetchall())\n'
  'print(plan(q))\n'
  "print(plan(q + ' '))\n"
  'c.close()\n'
  'd = make(cached_statements=0)\n'
  "plan = lambda sql: ' | '.join(r[3] for r in d.execute('EXPLAIN QUERY PLAN ' + sql))\n"
  "d.execute('CREATE INDEX idx_name ON cats (name)')\n"
  'print(plan(q))\n'
  "d.execute('DROP INDEX idx_name')\n"
  'print(plan(q))\n'
  'd.close()',
  'SCAN cats\n'
  "[('idx_birthdate',), ('idx_name',)]\n"
  'SEARCH cats USING INDEX idx_name (name=?)\n'
  'SCAN cats\n'
  "[('idx_birthdate',)]\n"
  'SEARCH cats USING INDEX idx_name (name=?)\n'
  'SCAN cats\n'
  'SEARCH cats USING INDEX idx_name (name=?)\n'
  'SCAN cats'],
 ['rowid is not a permanent number: reuse after deleting the last row, renumbering by VACUUM, and what INTEGER PRIMARY KEY and AUTOINCREMENT change',
  'import sqlite3\n'
  'CATS = [("Zophie","2021-01-24","black",5.6),("Miguel","2016-12-24","siamese",6.2),("Jacob","2022-02-20","orange and '
  'white",5.5),("Toby","2021-05-17","black",6.8),("Taffy","2024-12-09","white",7.0),("Hollie","2024-08-07","calico",6.0),("Lewis","2024-03-19","orange '
  'tabby",5.1),("Thor","2013-05-14","black",5.2),("Shell","2024-06-16","tortoiseshell",6.5),("Jasmine","2024-09-05","orange '
  'tabby",6.3),("Sassy","2017-08-20","black",7.5),("Hope","2016-05-22","black",7.6),("Iris","2017-07-13","bengal",6.8),("Ruby","2023-12-22","bengal",5.0),("Elton","2020-05-28","bengal",5.4),("Celine","2015-04-18","white",7.3),("Daisy","2019-03-19","white",6.0),("Mango","2017-02-12","tuxedo",6.8)]\n'
  "def make(path=':memory:', **kw):\n"
  '    c = sqlite3.connect(path, isolation_level=None, **kw)\n'
  "    c.execute('CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT')\n"
  "    c.executemany('INSERT INTO cats VALUES (?, ?, ?, ?)', CATS)\n"
  '    return c\n'
  'c = make()\n'
  "print(c.execute('SELECT max(rowid) FROM cats').fetchone())\n"
  "c.execute('DELETE FROM cats WHERE rowid = 18')\n"
  'c.execute("INSERT INTO cats VALUES (\'New\', \'2025-01-01\', \'grey\', 4.0)")\n'
  'print(c.execute("SELECT rowid FROM cats WHERE name = \'New\'").fetchone(), c.execute("SELECT rowid FROM cats WHERE name = \'Miguel\'").fetchone())\n'
  "c.execute('DELETE FROM cats WHERE rowid < 5')\n"
  "print(c.execute('SELECT rowid FROM cats LIMIT 3').fetchall())\n"
  "c.execute('VACUUM')\n"
  "print(c.execute('SELECT rowid FROM cats LIMIT 3').fetchall())\n"
  "for ddl in ('id INTEGER PRIMARY KEY', 'id INTEGER PRIMARY KEY AUTOINCREMENT'):\n"
  "    c.execute('CREATE TABLE t (%s, name TEXT) STRICT' % ddl)\n"
  '    c.execute("INSERT INTO t(name) VALUES (\'a\')")\n'
  '    c.execute("INSERT INTO t(name) VALUES (\'b\')")\n'
  "    c.execute('DELETE FROM t WHERE id = 2')\n"
  '    c.execute("INSERT INTO t(name) VALUES (\'c\')")\n'
  "    print(ddl, c.execute('SELECT * FROM t').fetchall(), c.execute('PRAGMA table_info(t)').fetchall()[0])\n"
  "    c.execute('DROP TABLE t')\n"
  "print(c.execute('SELECT * FROM cats LIMIT 1').fetchall(), c.execute('SELECT rowid, * FROM cats LIMIT 1').fetchall())\n"
  'c.close()',
  '(18,)\n'
  '(18,) (2,)\n'
  '[(5,), (6,), (7,)]\n'
  '[(1,), (2,), (3,)]\n'
  "id INTEGER PRIMARY KEY [(1, 'a'), (2, 'c')] (0, 'id', 'INTEGER', 0, None, 1)\n"
  "id INTEGER PRIMARY KEY AUTOINCREMENT [(1, 'a'), (3, 'c')] (0, 'id', 'INTEGER', 0, None, 1)\n"
  "[('Taffy', '2024-12-09', 'white', 7.0)] [(1, 'Taffy', '2024-12-09', 'white', 7.0)]"],
 ["transactions: the chapter's rollback and commit, SQLite's autocommit, the legacy default, autocommit=False and the with statement",
  'import sqlite3, tempfile, os\n'
  "c = sqlite3.connect(':memory:', isolation_level=None)\n"
  "c.execute('CREATE TABLE cats (name TEXT, fur TEXT, weight_kg REAL)')\n"
  'print(c.in_transaction)\n'
  "c.execute('BEGIN')\n"
  'print(c.in_transaction)\n'
  'c.execute("INSERT INTO cats VALUES (\'Socks\', \'white\', 4.2)")\n'
  'c.execute("INSERT INTO cats VALUES (\'Fluffy\', \'gray\', 4.5)")\n'
  'c.rollback()\n'
  "print(c.in_transaction, c.execute('SELECT * FROM cats').fetchall())\n"
  "c.execute('BEGIN')\n"
  'c.execute("INSERT INTO cats VALUES (\'Socks\', \'white\', 4.2)")\n'
  'c.execute("INSERT INTO cats VALUES (\'Fluffy\', \'gray\', 4.5)")\n'
  'c.commit()\n'
  "print(c.execute('SELECT name FROM cats').fetchall())\n"
  'c.execute("INSERT INTO cats VALUES (\'Gone\', \'x\', 1.0)")\n'
  'c.rollback()\n'
  'print(c.execute("SELECT name FROM cats WHERE name = \'Gone\'").fetchall())\n'
  'c.close()\n'
  "p = os.path.join(tempfile.mkdtemp(), 't.db')\n"
  'a = sqlite3.connect(p)\n'
  "a.execute('CREATE TABLE t (x)')\n"
  'a.commit()\n'
  'print(repr(a.isolation_level), a.autocommit == sqlite3.LEGACY_TRANSACTION_CONTROL)\n'
  "a.execute('INSERT INTO t VALUES (1)')\n"
  'print(a.in_transaction)\n'
  'b = sqlite3.connect(p)\n'
  "print(b.execute('SELECT count(*) FROM t').fetchone())\n"
  'a.close()\n'
  "print(b.execute('SELECT count(*) FROM t').fetchone())\n"
  'a = sqlite3.connect(p, autocommit=False)\n'
  'print(a.in_transaction, a.autocommit)\n'
  "a.execute('INSERT INTO t VALUES (2)')\n"
  'a.rollback()\n'
  "print(a.execute('SELECT count(*) FROM t').fetchone())\n"
  "a.execute('INSERT INTO t VALUES (3)')\n"
  'a.commit()\n'
  "print(b.execute('SELECT count(*) FROM t').fetchone())\n"
  'a.close()\n'
  'a = sqlite3.connect(p, autocommit=True)\n'
  "a.execute('INSERT INTO t VALUES (4)')\n"
  'a.rollback()\n'
  "print(a.execute('SELECT count(*) FROM t').fetchone())\n"
  'a.close()\n'
  "m = sqlite3.connect(':memory:')\n"
  "m.execute('CREATE TABLE lang (id INTEGER PRIMARY KEY, name TEXT UNIQUE)')\n"
  'with m:\n'
  '    m.execute("INSERT INTO lang (name) VALUES (\'Python\')")\n'
  'try:\n'
  '    with m:\n'
  '        m.execute("INSERT INTO lang (name) VALUES (\'Go\')")\n'
  '        m.execute("INSERT INTO lang (name) VALUES (\'Python\')")\n'
  'except sqlite3.IntegrityError as e:\n'
  "    print(type(e).__name__ + ': ' + str(e), e.sqlite_errorname)\n"
  "print(m.execute('SELECT name FROM lang').fetchall())\n"
  "m.execute('SELECT 1')\n"
  'try:\n'
  '    m.close()\n'
  "    m.execute('SELECT 1')\n"
  'except sqlite3.ProgrammingError as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))\n"
  'b.close()',
  'False\n'
  'True\n'
  'False []\n'
  "[('Socks',), ('Fluffy',)]\n"
  "[('Gone',)]\n"
  "'' True\n"
  'True\n'
  '(0,)\n'
  '(0,)\n'
  'True False\n'
  '(0,)\n'
  '(1,)\n'
  '(2,)\n'
  'IntegrityError: UNIQUE constraint failed: lang.name SQLITE_CONSTRAINT_UNIQUE\n'
  "[('Python',)]\n"
  'ProgrammingError: Cannot operate on a closed database.'],
 ['constraints and atomicity: a failed statement undoes the whole transaction',
  'import sqlite3\n'
  "c = sqlite3.connect(':memory:')\n"
  'c.execute(\'CREATE TABLE u (email TEXT UNIQUE, age INTEGER CHECK (age >= 0), name TEXT NOT NULL DEFAULT "none")\')\n'
  'c.execute("INSERT INTO u (email, age) VALUES (\'a@x\', 3)")\n'
  "print(c.execute('SELECT * FROM u').fetchall())\n"
  "for v in (('a@x', 4), ('b@x', -1)):\n"
  '    try:\n'
  "        c.execute('INSERT INTO u (email, age) VALUES (?, ?)', v)\n"
  '    except sqlite3.IntegrityError as e:\n'
  '        print(e, e.sqlite_errorname)\n'
  'try:\n'
  "    c.execute('INSERT INTO u (email, age, name) VALUES (?, ?, NULL)', ('c@x', 1))\n"
  'except sqlite3.IntegrityError as e:\n'
  '    print(e, e.sqlite_errorname)\n'
  "cc = sqlite3.connect(':memory:')\n"
  "cc.execute('CREATE TABLE t (a NOT NULL)')\n"
  'try:\n'
  '    with cc:\n'
  "        cc.execute('INSERT INTO t VALUES (1)')\n"
  "        cc.execute('INSERT INTO t VALUES (NULL)')\n"
  'except sqlite3.IntegrityError as e:\n'
  '    print(e)\n'
  "print(cc.execute('SELECT count(*) FROM t').fetchone())\n"
  "print(cc.execute('INSERT OR IGNORE INTO t VALUES (NULL)').rowcount)\n"
  'cc.close()\n'
  'c.close()',
  "[('a@x', 3, 'none')]\n"
  'UNIQUE constraint failed: u.email SQLITE_CONSTRAINT_UNIQUE\n'
  'CHECK constraint failed: age >= 0 SQLITE_CONSTRAINT_CHECK\n'
  'NOT NULL constraint failed: u.name SQLITE_CONSTRAINT_NOTNULL\n'
  'NOT NULL constraint failed: t.a\n'
  '(0,)\n'
  '0'],
 ["foreign keys: the chapter's REFERENCES cats(rowid) with enforcement off and on, and a declared parent key",
  'import sqlite3\n'
  'CATS = [("Zophie","2021-01-24","black",5.6),("Miguel","2016-12-24","siamese",6.2),("Jacob","2022-02-20","orange and '
  'white",5.5),("Toby","2021-05-17","black",6.8),("Taffy","2024-12-09","white",7.0),("Hollie","2024-08-07","calico",6.0),("Lewis","2024-03-19","orange '
  'tabby",5.1),("Thor","2013-05-14","black",5.2),("Shell","2024-06-16","tortoiseshell",6.5),("Jasmine","2024-09-05","orange '
  'tabby",6.3),("Sassy","2017-08-20","black",7.5),("Hope","2016-05-22","black",7.6),("Iris","2017-07-13","bengal",6.8),("Ruby","2023-12-22","bengal",5.0),("Elton","2020-05-28","bengal",5.4),("Celine","2015-04-18","white",7.3),("Daisy","2019-03-19","white",6.0),("Mango","2017-02-12","tuxedo",6.8)]\n'
  "def make(path=':memory:', **kw):\n"
  '    c = sqlite3.connect(path, isolation_level=None, **kw)\n'
  "    c.execute('CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT')\n"
  "    c.executemany('INSERT INTO cats VALUES (?, ?, ?, ?)', CATS)\n"
  '    return c\n'
  "ddl = 'CREATE TABLE vaccinations (vaccine TEXT, date_administered TEXT, administered_by TEXT, cat_id INTEGER, FOREIGN KEY(cat_id) REFERENCES cats(rowid)) STRICT'\n"
  "for pragma in ('OFF', 'ON'):\n"
  '    c = make()\n'
  "    c.execute('PRAGMA foreign_keys = ' + pragma)\n"
  '    c.execute(ddl)\n'
  '    for cat_id in (1, 999):\n'
  '        try:\n'
  '            print(pragma, cat_id, c.execute("INSERT INTO vaccinations VALUES (\'rabies\', \'2023-06-06\', \'Dr. Echo\', ?)", (cat_id,)).rowcount)\n'
  '        except sqlite3.OperationalError as e:\n'
  "            print(pragma, cat_id, type(e).__name__ + ': ' + str(e))\n"
  "    print(c.execute('SELECT * FROM cats INNER JOIN vaccinations ON cats.rowid = vaccinations.cat_id').fetchall())\n"
  '    c.close()\n'
  "c = sqlite3.connect(':memory:', isolation_level=None)\n"
  "c.execute('PRAGMA foreign_keys = ON')\n"
  "c.execute('CREATE TABLE cats (id INTEGER PRIMARY KEY, name TEXT NOT NULL) STRICT')\n"
  "c.execute('CREATE TABLE vaccinations (vaccine TEXT, cat_id INTEGER, FOREIGN KEY(cat_id) REFERENCES cats(id)) STRICT')\n"
  'c.execute("INSERT INTO cats (name) VALUES (\'Zophie\')")\n'
  'print(c.execute("INSERT INTO vaccinations VALUES (\'rabies\', 1)").rowcount)\n'
  'for sql in ("INSERT INTO vaccinations VALUES (\'rabies\', 999)", \'DELETE FROM cats WHERE id = 1\', \'UPDATE vaccinations SET cat_id = 5\'):\n'
  '    try:\n'
  '        c.execute(sql)\n'
  '    except sqlite3.IntegrityError as e:\n'
  "        print(sql[:26], type(e).__name__ + ': ' + str(e), e.sqlite_errorname)\n"
  "c.execute('BEGIN')\n"
  "c.execute('PRAGMA foreign_keys = OFF')\n"
  "print(c.execute('PRAGMA foreign_keys').fetchone())\n"
  "c.execute('COMMIT')\n"
  "c.execute('PRAGMA foreign_keys = OFF')\n"
  "print(c.execute('PRAGMA foreign_keys').fetchone())\n"
  "c.execute('CREATE TABLE p (id INTEGER PRIMARY KEY) STRICT')\n"
  "c.execute('CREATE TABLE ch (p_id INTEGER REFERENCES p(id) ON DELETE CASCADE) STRICT')\n"
  "c.execute('PRAGMA foreign_keys = ON')\n"
  "c.execute('INSERT INTO p VALUES (1)')\n"
  "c.execute('INSERT INTO ch VALUES (1)')\n"
  "c.execute('DELETE FROM p WHERE id = 1')\n"
  "print(c.execute('SELECT count(*) FROM ch').fetchone())\n"
  'c.close()',
  'OFF 1 1\n'
  'OFF 999 1\n'
  "[('Zophie', '2021-01-24', 'black', 5.6, 'rabies', '2023-06-06', 'Dr. Echo', 1)]\n"
  'ON 1 OperationalError: foreign key mismatch - "vaccinations" referencing "cats"\n'
  'ON 999 OperationalError: foreign key mismatch - "vaccinations" referencing "cats"\n'
  '[]\n'
  '1\n'
  'INSERT INTO vaccinations V IntegrityError: FOREIGN KEY constraint failed SQLITE_CONSTRAINT_FOREIGNKEY\n'
  'DELETE FROM cats WHERE id  IntegrityError: FOREIGN KEY constraint failed SQLITE_CONSTRAINT_FOREIGNKEY\n'
  'UPDATE vaccinations SET ca IntegrityError: FOREIGN KEY constraint failed SQLITE_CONSTRAINT_FOREIGNKEY\n'
  '(1,)\n'
  '(0,)\n'
  '(0,)'],
 ["the chapter's ALTER TABLE and DROP TABLE session on a copy of the cats table",
  'import sqlite3\n'
  'CATS = [("Zophie","2021-01-24","black",5.6),("Miguel","2016-12-24","siamese",6.2),("Jacob","2022-02-20","orange and '
  'white",5.5),("Toby","2021-05-17","black",6.8),("Taffy","2024-12-09","white",7.0),("Hollie","2024-08-07","calico",6.0),("Lewis","2024-03-19","orange '
  'tabby",5.1),("Thor","2013-05-14","black",5.2),("Shell","2024-06-16","tortoiseshell",6.5),("Jasmine","2024-09-05","orange '
  'tabby",6.3),("Sassy","2017-08-20","black",7.5),("Hope","2016-05-22","black",7.6),("Iris","2017-07-13","bengal",6.8),("Ruby","2023-12-22","bengal",5.0),("Elton","2020-05-28","bengal",5.4),("Celine","2015-04-18","white",7.3),("Daisy","2019-03-19","white",6.0),("Mango","2017-02-12","tuxedo",6.8)]\n'
  "def make(path=':memory:', **kw):\n"
  '    c = sqlite3.connect(path, isolation_level=None, **kw)\n'
  "    c.execute('CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT')\n"
  "    c.executemany('INSERT INTO cats VALUES (?, ?, ?, ?)', CATS)\n"
  '    return c\n'
  'c = make()\n'
  'print(c.execute("SELECT name FROM sqlite_schema WHERE type=\'table\'").fetchall())\n'
  "c.execute('ALTER TABLE cats RENAME TO felines')\n"
  'print(c.execute("SELECT name FROM sqlite_schema WHERE type=\'table\'").fetchall())\n'
  "print(c.execute('PRAGMA TABLE_INFO(felines)').fetchall()[2])\n"
  "c.execute('ALTER TABLE felines RENAME COLUMN fur TO description')\n"
  "print(c.execute('PRAGMA TABLE_INFO(felines)').fetchall()[2])\n"
  "c.execute('ALTER TABLE felines ADD COLUMN is_loved INTEGER DEFAULT 1')\n"
  "print(c.execute('SELECT * FROM felines LIMIT 3').fetchall())\n"
  "print(c.execute('PRAGMA TABLE_INFO(felines)').fetchall()[4])\n"
  'try:\n'
  "    c.execute('ALTER TABLE felines ADD COLUMN x INTEGER NOT NULL')\n"
  'except sqlite3.OperationalError as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))\n"
  "c.execute('ALTER TABLE felines DROP COLUMN is_loved')\n"
  "print(len(c.execute('PRAGMA TABLE_INFO(felines)').fetchall()))\n"
  "c.execute('CREATE INDEX idx_w ON felines (weight_kg)')\n"
  'try:\n'
  "    c.execute('ALTER TABLE felines DROP COLUMN weight_kg')\n"
  'except sqlite3.OperationalError as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))\n"
  "c.execute('DROP TABLE felines')\n"
  'print(c.execute("SELECT name FROM sqlite_schema WHERE type=\'table\'").fetchall())\n'
  'try:\n'
  "    c.execute('DROP TABLE felines')\n"
  'except sqlite3.OperationalError as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))\n"
  "c.execute('DROP TABLE IF EXISTS felines')\n"
  'c.close()',
  "[('cats',)]\n"
  "[('felines',)]\n"
  "(2, 'fur', 'TEXT', 0, None, 0)\n"
  "(2, 'description', 'TEXT', 0, None, 0)\n"
  "[('Zophie', '2021-01-24', 'black', 5.6, 1), ('Miguel', '2016-12-24', 'siamese', 6.2, 1), ('Jacob', '2022-02-20', 'orange and white', 5.5, 1)]\n"
  "(4, 'is_loved', 'INTEGER', 0, '1', 0)\n"
  'OperationalError: Cannot add a NOT NULL column with default value NULL\n'
  '4\n'
  'OperationalError: error in index idx_w after drop column: no such column: weight_kg\n'
  '[]\n'
  'OperationalError: no such table: felines'],
 ["joins over two tables: the chapter's inner join, cats without vaccinations, and vaccinations dated before birth",
  'import sqlite3\n'
  'CATS = [("Zophie","2021-01-24","black",5.6),("Miguel","2016-12-24","siamese",6.2),("Jacob","2022-02-20","orange and '
  'white",5.5),("Toby","2021-05-17","black",6.8),("Taffy","2024-12-09","white",7.0),("Hollie","2024-08-07","calico",6.0),("Lewis","2024-03-19","orange '
  'tabby",5.1),("Thor","2013-05-14","black",5.2),("Shell","2024-06-16","tortoiseshell",6.5),("Jasmine","2024-09-05","orange '
  'tabby",6.3),("Sassy","2017-08-20","black",7.5),("Hope","2016-05-22","black",7.6),("Iris","2017-07-13","bengal",6.8),("Ruby","2023-12-22","bengal",5.0),("Elton","2020-05-28","bengal",5.4),("Celine","2015-04-18","white",7.3),("Daisy","2019-03-19","white",6.0),("Mango","2017-02-12","tuxedo",6.8)]\n'
  "def make(path=':memory:', **kw):\n"
  '    c = sqlite3.connect(path, isolation_level=None, **kw)\n'
  "    c.execute('CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT')\n"
  "    c.executemany('INSERT INTO cats VALUES (?, ?, ?, ?)', CATS)\n"
  '    return c\n'
  'c = make()\n'
  "c.execute('CREATE TABLE IF NOT EXISTS vaccinations (vaccine TEXT, date_administered TEXT, administered_by TEXT, cat_id INTEGER) STRICT')\n"
  "c.executemany('INSERT INTO vaccinations VALUES (?, ?, ?, ?)', [('rabies', '2023-06-06', 'Dr. Echo', 1), ('FeLV', '2023-06-06', 'Dr. Echo', 1), ('rabies', "
  "'2023-07-11', 'Dr. Echo', 18), ('FeLV', '2012-01-01', 'Dr. Echo', 8)])\n"
  "for row in c.execute('SELECT * FROM cats INNER JOIN vaccinations ON cats.rowid = vaccinations.cat_id'):\n"
  '    print(row)\n'
  "print(c.execute('SELECT cats.name FROM cats LEFT JOIN vaccinations ON cats.rowid = vaccinations.cat_id WHERE vaccinations.vaccine IS NULL LIMIT 3').fetchall())\n"
  "print(c.execute('SELECT cats.name, vaccinations.vaccine FROM cats JOIN vaccinations ON cats.rowid = vaccinations.cat_id WHERE vaccinations.date_administered < "
  "cats.birthdate').fetchall())\n"
  'c.close()',
  "('Zophie', '2021-01-24', 'black', 5.6, 'rabies', '2023-06-06', 'Dr. Echo', 1)\n"
  "('Zophie', '2021-01-24', 'black', 5.6, 'FeLV', '2023-06-06', 'Dr. Echo', 1)\n"
  "('Mango', '2017-02-12', 'tuxedo', 6.8, 'rabies', '2023-07-11', 'Dr. Echo', 18)\n"
  "('Thor', '2013-05-14', 'black', 5.2, 'FeLV', '2012-01-01', 'Dr. Echo', 8)\n"
  "[('Miguel',), ('Jacob',), ('Toby',)]\n"
  "[('Thor', 'FeLV')]"],
 ['in-memory databases, backup to a file and back, progress steps, a dump that re-creates the database, and dump size against file size',
  'import sqlite3\n'
  'CATS = [("Zophie","2021-01-24","black",5.6),("Miguel","2016-12-24","siamese",6.2),("Jacob","2022-02-20","orange and '
  'white",5.5),("Toby","2021-05-17","black",6.8),("Taffy","2024-12-09","white",7.0),("Hollie","2024-08-07","calico",6.0),("Lewis","2024-03-19","orange '
  'tabby",5.1),("Thor","2013-05-14","black",5.2),("Shell","2024-06-16","tortoiseshell",6.5),("Jasmine","2024-09-05","orange '
  'tabby",6.3),("Sassy","2017-08-20","black",7.5),("Hope","2016-05-22","black",7.6),("Iris","2017-07-13","bengal",6.8),("Ruby","2023-12-22","bengal",5.0),("Elton","2020-05-28","bengal",5.4),("Celine","2015-04-18","white",7.3),("Daisy","2019-03-19","white",6.0),("Mango","2017-02-12","tuxedo",6.8)]\n'
  "def make(path=':memory:', **kw):\n"
  '    c = sqlite3.connect(path, isolation_level=None, **kw)\n'
  "    c.execute('CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT')\n"
  "    c.executemany('INSERT INTO cats VALUES (?, ?, ?, ?)', CATS)\n"
  '    return c\n'
  'import os, tempfile\n'
  'os.chdir(tempfile.mkdtemp())\n'
  "src = make('cats.db')\n"
  "bk = sqlite3.connect('backup.db', isolation_level=None)\n"
  'src.backup(bk)\n'
  "print(bk.execute('SELECT count(*) FROM cats').fetchone(), os.path.exists('backup.db'))\n"
  'bk.close()\n'
  "mem = sqlite3.connect(':memory:', isolation_level=None)\n"
  "mem.execute('CREATE TABLE test (name TEXT, number REAL)')\n"
  'mem.execute("INSERT INTO test VALUES (\'foo\', 3.14)")\n'
  "f = sqlite3.connect('test.db', isolation_level=None)\n"
  'mem.backup(f)\n'
  "print(f.execute('SELECT * FROM test').fetchall())\n"
  'f.close()\n'
  'mem.close()\n'
  "m = sqlite3.connect(':memory:', isolation_level=None)\n"
  'src.backup(m)\n'
  "print(m.execute('SELECT * FROM cats LIMIT 3').fetchall())\n"
  'steps = []\n'
  "x = sqlite3.connect(':memory:')\n"
  'src.backup(x, pages=1, progress=lambda status, remaining, total: steps.append((status, remaining, total)))\n'
  'print(steps)\n'
  'x.close()\n'
  "a = sqlite3.connect(':memory:')\n"
  "b = sqlite3.connect(':memory:')\n"
  "a.execute('CREATE TABLE t (x)')\n"
  'try:\n'
  "    b.execute('SELECT * FROM t')\n"
  'except sqlite3.OperationalError as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))\n"
  'a.close()\n'
  'b.close()\n'
  'lines = list(src.iterdump())\n'
  'print(len(lines), lines[0], lines[1], lines[2], lines[-1])\n'
  "g = sqlite3.connect(':memory:')\n"
  "g.executescript('\\n'.join(lines))\n"
  "print(g.execute('SELECT count(*) FROM cats').fetchone(), g.execute('SELECT sql FROM sqlite_schema').fetchone())\n"
  "print(list(src.iterdump(filter='ca%'))[:2] == lines[:2])\n"
  "with open('queries.txt', 'w', encoding='utf-8') as fo:\n"
  '    for line in src.iterdump():\n'
  "        fo.write(line + '\\n')\n"
  "print(os.path.getsize('queries.txt') < os.path.getsize('cats.db'), os.path.getsize('cats.db') % 4096)\n"
  'print(src.serialize()[:15])\n'
  'for c in (m, g, src):\n'
  '    c.close()',
  '(18,) True\n'
  "[('foo', 3.14)]\n"
  "[('Zophie', '2021-01-24', 'black', 5.6), ('Miguel', '2016-12-24', 'siamese', 6.2), ('Jacob', '2022-02-20', 'orange and white', 5.5)]\n"
  '[(0, 1, 2), (101, 0, 2)]\n'
  'OperationalError: no such table: t\n'
  '21 BEGIN TRANSACTION; CREATE TABLE cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT; INSERT INTO "cats" '
  "VALUES('Zophie','2021-01-24','black',5.6); COMMIT;\n"
  "(18,) ('CREATE TABLE cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT',)\n"
  'True\n'
  'True 0\n'
  "b'SQLite format 3'"],
 ["the dump text of a table that was renamed and renamed back quotes its name, as the chapter's dump does",
  'import sqlite3\n'
  "c = sqlite3.connect(':memory:')\n"
  "c.execute('CREATE TABLE cats (name TEXT NOT NULL, weight_kg REAL) STRICT')\n"
  'print(list(c.iterdump())[1])\n'
  "c.execute('ALTER TABLE cats RENAME TO felines')\n"
  "c.execute('ALTER TABLE felines RENAME TO cats')\n"
  'print(list(c.iterdump())[1])\n'
  'c.close()',
  'CREATE TABLE cats (name TEXT NOT NULL, weight_kg REAL) STRICT;\nCREATE TABLE "cats" (name TEXT NOT NULL, weight_kg REAL) STRICT;'],
 ['double-quoted strings are read as strings only when no column has that name, and can be switched off',
  'import sqlite3\n'
  "c = sqlite3.connect(':memory:')\n"
  "c.execute('CREATE TABLE t (a)')\n"
  'c.execute("INSERT INTO t VALUES (\'x\')")\n'
  'c.execute("INSERT INTO t VALUES (\'y\')")\n'
  'print(c.execute(\'SELECT a FROM t WHERE a = "x"\').fetchall())\n'
  'print(c.execute(\'SELECT a FROM t WHERE a = "a"\').fetchall())\n'
  'print(c.execute("SELECT a FROM t WHERE a = \'a\'").fetchall())\n'
  'print(c.execute(\'SELECT "nocolumn"\').fetchall())\n'
  'c.setconfig(sqlite3.SQLITE_DBCONFIG_DQS_DML, False)\n'
  'try:\n'
  '    c.execute(\'SELECT a FROM t WHERE a = "x"\')\n'
  'except sqlite3.OperationalError as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))\n"
  'print(c.execute("SELECT a FROM t WHERE a = \'x\'").fetchall())\n'
  'c.close()',
  '[(\'x\',)]\n[(\'x\',), (\'y\',)]\n[]\n[(\'nocolumn\',)]\nOperationalError: no such column: "x" - should this be a string literal in single-quotes?\n[(\'x\',)]'],
 ['one writer at a time: a second connection waits and then fails with database is locked',
  'import sqlite3, os, tempfile, time\n'
  "p = os.path.join(tempfile.mkdtemp(), 'w.db')\n"
  'a = sqlite3.connect(p, isolation_level=None, timeout=0.2)\n'
  'b = sqlite3.connect(p, isolation_level=None, timeout=0.2)\n'
  "a.execute('CREATE TABLE t (x)')\n"
  "a.execute('BEGIN IMMEDIATE')\n"
  "a.execute('INSERT INTO t VALUES (1)')\n"
  't0 = time.time()\n'
  'try:\n'
  "    b.execute('INSERT INTO t VALUES (2)')\n"
  'except sqlite3.OperationalError as e:\n'
  "    print(type(e).__name__ + ': ' + str(e), time.time() - t0 >= 0.2)\n"
  "print(b.execute('SELECT count(*) FROM t').fetchone())\n"
  'a.commit()\n'
  "print(b.execute('INSERT INTO t VALUES (2)').rowcount, b.execute('SELECT count(*) FROM t').fetchone())\n"
  "print(a.execute('PRAGMA journal_mode=WAL').fetchone())\n"
  'a.close()\n'
  'b.close()',
  "OperationalError: database is locked True\n(0,)\n1 (2,)\n('wal',)"],
 ['a connection belongs to its thread, is closed explicitly, and warns when it is not (Python 3.13 and later)',
  'import sqlite3, threading, warnings, gc\n'
  "c = sqlite3.connect(':memory:')\n"
  'out = []\n'
  'def use():\n'
  '    try:\n'
  "        c.execute('SELECT 1')\n"
  '    except sqlite3.ProgrammingError as e:\n'
  '        out.append(str(e)[:70])\n'
  't = threading.Thread(target=use)\n'
  't.start()\n'
  't.join()\n'
  'print(out)\n'
  'c.close()\n'
  'with warnings.catch_warnings(record=True) as w:\n'
  "    warnings.simplefilter('always')\n"
  "    x = sqlite3.connect(':memory:')\n"
  '    del x\n'
  '    gc.collect()\n'
  '    print([(i.category.__name__, str(i.message)[:26]) for i in w])\n'
  'with warnings.catch_warnings(record=True) as w:\n'
  "    warnings.simplefilter('always')\n"
  "    sqlite3.connect(':memory:', 5.0).close()\n"
  '    print(sorted({i.category.__name__ for i in w}))\n'
  'from contextlib import closing\n'
  "with closing(sqlite3.connect(':memory:')) as k:\n"
  "    print(k.execute('SELECT 1').fetchone())\n"
  'try:\n'
  "    k.execute('SELECT 1')\n"
  'except sqlite3.ProgrammingError as e:\n'
  '    print(str(e))\n'
  'print(sqlite3.threadsafety, sqlite3.paramstyle, sqlite3.apilevel, sqlite3.LEGACY_TRANSACTION_CONTROL)',
  "['SQLite objects created in a thread can only be used in that same threa']\n"
  "[('ResourceWarning', 'unclosed database in <sqli')]\n"
  "['DeprecationWarning']\n"
  '(1,)\n'
  'Cannot operate on a closed database.\n'
  '3 qmark 2.0 -1'],
 ['the SQLite shell of the standard library: python -m sqlite3 with a file and a statement',
  'import subprocess, sys, tempfile, os\n'
  'd = tempfile.mkdtemp()\n'
  "db = os.path.join(d, 'example.db')\n"
  'def shell(sql):\n'
  "    r = subprocess.run([sys.executable, '-m', 'sqlite3', db, sql], capture_output=True, text=True)\n"
  "    return r.returncode, r.stdout.strip().split('\\n'), r.stderr.strip()[:40]\n"
  "print(shell('CREATE TABLE cats (name TEXT NOT NULL, weight_kg REAL) STRICT'))\n"
  'print(shell("INSERT INTO cats VALUES (\'Zophie\', 4.7)"))\n'
  "print(shell('SELECT * FROM cats'))\n"
  "print(__import__('sqlite3').sqlite_version in subprocess.run([sys.executable, '-m', 'sqlite3', '-v'], capture_output=True, text=True).stdout)",
  '(0, [\'\'], \'\')\n(0, [\'\'], \'\')\n(0, ["(\'Zophie\', 4.7)"], \'\')\nTrue'],
 ['practice program 1 over the 18 cats: missing vaccines and dates before birth, as queries',
  'import sqlite3\n'
  'CATS = [("Zophie","2021-01-24","black",5.6),("Miguel","2016-12-24","siamese",6.2),("Jacob","2022-02-20","orange and '
  'white",5.5),("Toby","2021-05-17","black",6.8),("Taffy","2024-12-09","white",7.0),("Hollie","2024-08-07","calico",6.0),("Lewis","2024-03-19","orange '
  'tabby",5.1),("Thor","2013-05-14","black",5.2),("Shell","2024-06-16","tortoiseshell",6.5),("Jasmine","2024-09-05","orange '
  'tabby",6.3),("Sassy","2017-08-20","black",7.5),("Hope","2016-05-22","black",7.6),("Iris","2017-07-13","bengal",6.8),("Ruby","2023-12-22","bengal",5.0),("Elton","2020-05-28","bengal",5.4),("Celine","2015-04-18","white",7.3),("Daisy","2019-03-19","white",6.0),("Mango","2017-02-12","tuxedo",6.8)]\n'
  "def make(path=':memory:', **kw):\n"
  '    c = sqlite3.connect(path, isolation_level=None, **kw)\n'
  "    c.execute('CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT')\n"
  "    c.executemany('INSERT INTO cats VALUES (?, ?, ?, ?)', CATS)\n"
  '    return c\n'
  'c = make()\n'
  "c.execute('CREATE TABLE IF NOT EXISTS vaccinations (vaccine TEXT, date_administered TEXT, administered_by TEXT, cat_id INTEGER) STRICT')\n"
  "rows = [('rabies', '2023-06-06', 'Dr. Echo', 1), ('FeLV', '2023-06-06', 'Dr. Echo', 1), ('FVRCP', '2023-06-06', 'Dr. Echo', 1), ('rabies', '2012-01-01', 'Dr. Echo', "
  "8), ('FeLV', '2014-01-01', 'Dr. Echo', 8), ('FVRCP', '2014-01-01', 'Dr. Echo', 8)]\n"
  "c.executemany('INSERT INTO vaccinations VALUES (?, ?, ?, ?)', rows)\n"
  "need = ('rabies', 'FeLV', 'FVRCP')\n"
  'lacking = c.execute("SELECT cats.name FROM cats WHERE (SELECT count(DISTINCT vaccine) FROM vaccinations WHERE cat_id = cats.rowid AND vaccine IN (?, ?, ?)) < 3 ORDER '
  'BY cats.rowid", need).fetchall()\n'
  'print(len(lacking), lacking[:3])\n'
  "early = c.execute('SELECT cats.name, vaccinations.vaccine, vaccinations.date_administered, cats.birthdate FROM cats JOIN vaccinations ON vaccinations.cat_id = "
  "cats.rowid WHERE vaccinations.date_administered < cats.birthdate').fetchall()\n"
  'print(early)\n'
  'c.close()',
  "16 [('Miguel',), ('Jacob',), ('Toby',)]\n[('Thor', 'rabies', '2012-01-01', '2013-05-14')]"],
 ['practice program 2, the meal and ingredient database, run on scripted input',
  'import builtins\n'
  "lines = iter(['onigiri:rice,nori,salt,sesame seeds', 'chicken and rice:chicken,rice,cream of chicken soup', 'onigiri', 'chicken', 'rice', 'onigiri:oops', 'sushi', "
  "'quit'])\n"
  "def fake_input(prompt=''):\n"
  '    v = next(lines)\n'
  '    print(prompt + v)\n'
  '    return v\n'
  'builtins.input = fake_input\n'
  'exec(compile("import sqlite3\\nconn = sqlite3.connect(\':memory:\', autocommit=True)\\nconn.execute(\'PRAGMA foreign_keys = ON\')\\nconn.execute(\'CREATE TABLE IF '
  "NOT EXISTS meals (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE) STRICT')\\nconn.execute('CREATE TABLE IF NOT EXISTS ingredients (name TEXT NOT NULL, meal_id "
  "INTEGER NOT NULL, FOREIGN KEY(meal_id) REFERENCES meals(id)) STRICT')\\nwhile True:\\n    line = input('> ').strip()\\n    if line == 'quit':\\n        break\\n    "
  "if ':' in line:\\n        meal, _, rest = line.partition(':')\\n        meal = meal.strip()\\n        items = [item.strip() for item in rest.split(',') if "
  "item.strip()]\\n        conn.execute('BEGIN')\\n        try:\\n            meal_id = conn.execute('INSERT INTO meals (name) VALUES (?)', "
  "[meal]).lastrowid\\n            conn.executemany('INSERT INTO ingredients (name, meal_id) VALUES (?, ?)', [(item, meal_id) for item in items])\\n            "
  "conn.execute('COMMIT')\\n            print('Meal added:', meal)\\n        except sqlite3.IntegrityError as error:\\n            "
  "conn.execute('ROLLBACK')\\n            print('Not added:', error)\\n        continue\\n    found = conn.execute('SELECT ingredients.name FROM ingredients JOIN meals "
  "ON meals.id = ingredients.meal_id WHERE meals.name = ? ORDER BY ingredients.rowid', [line]).fetchall()\\n    if found:\\n        print('Ingredients of ' + line + "
  "':')\\n        for (item,) in found:\\n            print('  ' + item)\\n    used = conn.execute('SELECT meals.name FROM meals JOIN ingredients ON meals.id = "
  "ingredients.meal_id WHERE ingredients.name = ? ORDER BY meals.id', [line]).fetchall()\\n    if used:\\n        print('Meals that use ' + line + ':')\\n        for "
  '(name,) in used:\\n            print(\'  \' + name)\\n    if not found and not used:\\n        print(\'Nothing known about \' + line)\\nconn.close()\\n", \'meal\', '
  "'exec'), {'__name__': '__main__'})\n",
  '> onigiri:rice,nori,salt,sesame seeds\n'
  'Meal added: onigiri\n'
  '> chicken and rice:chicken,rice,cream of chicken soup\n'
  'Meal added: chicken and rice\n'
  '> onigiri\n'
  'Ingredients of onigiri:\n'
  '  rice\n'
  '  nori\n'
  '  salt\n'
  '  sesame seeds\n'
  '> chicken\n'
  'Meals that use chicken:\n'
  '  chicken and rice\n'
  '> rice\n'
  'Meals that use rice:\n'
  '  onigiri\n'
  '  chicken and rice\n'
  '> onigiri:oops\n'
  'Not added: UNIQUE constraint failed: meals.name\n'
  '> sushi\n'
  'Nothing known about sushi\n'
  '> quit']]
