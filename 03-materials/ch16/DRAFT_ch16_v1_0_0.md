# Chapter 16 Draft — SQLite Databases (v1.0.0)

**Status note:** Existing materials checked against live files (deck `SEN0414_Ch16_SQLiteDatabases_3e_v2_0_1.pptx` — the delivered version; `_v2_0_0.pptx` is superseded and not used — 54 slides; page `sen0414_ch16_page_v9_97_0.html`; manifest `chapter_code_ch16_v1_0_1.json`, 25 examples; stories `sen0414_ch16_stories_v1_0_0.py`, 6 stories). Chapter 16 went through two real repairs in October: the deck was re-committed intra-task from v2_0_0 to v2_0_1 (v2_0_1 is the controlled file), and the page failed an overflow check at 1366px (v9_96_0 → repaired to v9_97_0, now clean). No legacy duplicate deck exists for this chapter. This draft is for your reading and approval before any render step.

## 1. The story (6 beats, one per concept, sourced)

1. **Spring 2000 → 17 August 2000 — D. Richard Hipp (General Dynamics, under a US Navy contract).** Hipp designed SQLite while writing damage-control software for guided-missile destroyers that used an Informix back end on HP-UX; SQLite's first release followed on 17 August 2000, public domain. *Lesson: a database can be a library and a file, not a server.* (https://en.wikipedia.org/wiki/SQLite)
2. **June 1970 — Edgar F. Codd (IBM San Jose Research Lab).** Codd's paper "A Relational Model of Data for Large Shared Data Banks" (Communications of the ACM, Vol. 13 No. 6) replaced specialist, program-per-query data retrieval with the relational model — the model behind the chapter's joined `cats`/`vaccinations` tables. *Lesson: put each kind of fact in its own table and join them.* (https://www.ibm.com/history/relational-database)
3. **19 September 2006 — the Python developers.** Python 2.5 added the `sqlite3` module (built on `pysqlite`) to the standard library, so `import sqlite3` needs no install; the SQLite version itself depends on the Python build. *Lesson: Python ships the module, the build decides the SQLite.* (https://docs.python.org/3/whatsnew/2.5.html)
4. **10 October 2007 — Randall Munroe (xkcd #327, "Exploits of a Mom").** The comic's "Bobby Tables" attack — a name that closes a SQL statement and drops a table — is exactly what the chapter's `?` placeholder defends against; this draft's verification re-ran the attack (an f-string broke the query; a bound parameter did not). *Lesson: bind values with placeholders; never paste them into SQL.* (https://xkcd.com/327/)
5. **27 November 2021 — the SQLite developers (release 3.37.0).** STRICT tables made a column's declared type a rule rather than a preference; the chapter builds every table STRICT, and this draft's check confirmed `'Hello'` is refused in an INTEGER STRICT column but accepted (as text) in a plain one. *Lesson: declare STRICT so a column's type is a rule.* (https://sqlite.org/releaselog/3_37_0.html)
6. **1983 — Theo Haerder and Andreas Reuter.** Their paper "Principles of Transaction-Oriented Database Recovery" named the ACID properties (atomicity, consistency, isolation, durability); SQLite documents itself as transactional, and this draft's check confirmed a failed statement changed nothing while a committed row survived a file re-open. *Lesson: a transaction is all of its changes or none.* (https://en.wikipedia.org/wiki/ACID)

## 2. Explanations

Chapter 16 teaches SQLite via Python's `sqlite3`: connecting and closing, creating tables and reading schema, STRICT typing, inserting/reading rows, `rowid` semantics, `WHERE`/`ORDER BY`/`LIMIT`, `LIKE` vs. `GLOB`, `NULL` handling, `UPDATE`/`DELETE`/`RETURNING`, placeholders (positional and named) against SQL injection, transactions (`BEGIN`/commit/rollback, `with conn` semantics, `closing()`), altering/dropping tables, indexes, `VACUUM`, foreign keys and `PRAGMA foreign_keys`, `INNER`/`LEFT JOIN`, backing up a database (`backup()`, `iterdump()`, `shutil` file copy), and closes with two practice programs: a cat-vaccination checker and a meal-ingredients database.

## 3. Slide / page-tab outline (54 slides, 25 code examples — order follows the current, v2_0_1 deck)

| # | Slide | Title / content |
|---|-------|------------------|
| — | 1–6 | Title, agenda, stories 1–6 (narrative slides) |
| 1 | 7 | Connect, ask, close |
| — | 8–9 | (explanatory) |
| 2 | 10 | Create a table and read the schema |
| 3 | 11 | STRICT refuses what a plain table keeps |
| — | 12 | (explanatory) |
| 4 | 13 | Insert rows and read them back |
| 5 | 14 | The rowid is not a promise |
| — | 15–16 | (explanatory) |
| 6 | 17 | WHERE, ORDER BY and LIMIT |
| — | 18 | (explanatory) |
| 7 | 19 | LIKE ignores case, GLOB does not |
| 8 | 20 | NULL is not a value |
| — | 21 | (explanatory) |
| 9 | 22 | UPDATE, DELETE and RETURNING |
| 10 | 23 | Placeholders by position and by name |
| 11 | 24 | SQL injection and the placeholder |
| — | 25–27 | (explanatory / transaction intro) |
| 12 | 28 | BEGIN, commit and rollback |
| 13 | 29 | A failed statement changes nothing |
| — | 30 | (explanatory) |
| 14 | 31 | with conn: commit or roll back |
| 15 | 32 | with conn does not close; closing() does |
| — | 33 | (explanatory) |
| 16 | 34 | ALTER TABLE and DROP TABLE |
| — | 35 | (explanatory) |
| 17 | 36 | An index serves some searches |
| 18 | 37 | A database file and VACUUM |
| — | 38–40 | (explanatory / foreign-key intro) |
| 19 | 41 | A foreign key and its switch |
| 20 | 42 | INNER JOIN and LEFT JOIN |
| — | — | — |
| 21 | 43 | backup() copies a whole database |
| 22 | 44 | iterdump() turns a database into SQL |
| 23 | 45 | shutil copies a database file |
| — | 46–47 | (explanatory / practice intro) |
| 24 | 48 | Practice program: the cat vaccination checker |
| 25 | 49 | Practice program: the meal ingredients database |
| — | 50–52 | Summary, Practice Questions setup, chart |
| — | 53 | Practice Questions (4 drills + 1 program) |
| — | 54 | Resources: where to go next |

## 4. Resources slide (14 links, verified live on the current deck)

1. Book: Automate the Boring Stuff, 3e, ch.16 — https://automatetheboringstuff.com/3e/chapter16.html
2. SQLite: EXPLAIN QUERY PLAN — https://www.sqlite.org/eqp.html
3. Python docs: sqlite3 — https://docs.python.org/3/library/sqlite3.html
4. SQLite: appropriate uses — https://www.sqlite.org/whentouse.html
5. SQLite: datatypes — https://www.sqlite.org/datatype3.html
6. OWASP: SQL injection prevention — cheatsheetseries.owasp.org
7. SQLite: STRICT tables — https://www.sqlite.org/stricttables.html
8. xkcd 327: Exploits of a Mom — https://xkcd.com/327/
9. SQLite: foreign key support — https://www.sqlite.org/foreignkeys.html
10. IBM: the relational database — https://www.ibm.com/history/relational-database
11. SQLite: transactions — https://www.sqlite.org/lang_transaction.html
12. Wikipedia: Edgar F. Codd and the relational model — https://en.wikipedia.org/wiki/Edgar_F._Codd
13. SQLite: write-ahead logging — https://www.sqlite.org/wal.html
14. Practical SQL, 2nd edition (No Starch Press) — https://nostarch.com/practical-sql-2nd-edition

## 5. Open items

- No legacy duplicate deck to retire for this chapter.
- Deck version note: `SEN0414_Ch16_SQLiteDatabases_3e_v2_0_0.pptx` is superseded and not delivered; `_v2_0_1.pptx` is the controlled, current file. No action needed — flagging only so it isn't mistaken for a second live version.
- A `rdodi/` research/domain-ontology artifact subfolder exists (`03-materials/ch16/rdodi/`) from the earlier iteration-20 process; left untouched, out of this lineage's scope per your standing rule of not reopening closed, controller-confirmed work without a found defect.
- No structural gap found; both prior defects (page overflow, deck re-commit) are already resolved and confirmed by the controller's own re-runs.
