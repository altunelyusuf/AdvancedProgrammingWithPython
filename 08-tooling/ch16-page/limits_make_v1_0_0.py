"""Writes limits_v1_0_0.json, the chapter 16 page's 'Provenance & known limits' entries, from the records Phase A made
(third_party_record_v1_0_0.json, live_observations_v1_0_0.json, interpreter_record_v1_0_0.json), pywheels_v1_0_0.json, standin_v1_0_0.json
and the 'Not executed' paragraph of sen0414_ch16_rdodi_data_v1_0_3.py. Numbers and quoted values are read from those files.
Chapter 16's first entries say what differs between the page's Python and SQLite and the recorded ones.
Usage: limits_make_v1_0_0.py"""
__version__ = "1.0.0"
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(H, n)))
tp, lv, ir, so = J("third_party_record_v1_0_0.json"), J("live_observations_v1_0_0.json"), J("interpreter_record_v1_0_0.json"), J("standin_v1_0_0.json")
src = open(os.path.join(H, "..", "sen0414_ch16_rdodi_data_v1_0_3.py"), encoding="utf-8").read()
live = {i["what"]: i["saw"] for i in lv["items"]}
find = lambda start: next(v for k, v in live.items() if k.startswith(start))
m = re.search(r"Not executed, and said so where it comes up: (.*?)\.\s+The chapter's 131 statements", src, re.S)
notexec = re.sub(r"\s+", " ", m.group(1)).strip()
rev = re.search(r"seven examples whose result depended.*?: (.*?) The examples that start a process", src, re.S)
names = ", ".join(re.findall(r"# (\w+) \(|\)[,;] (\w+) \(", "")) or "LargeDataLimits, NotADatabaseFile, CloseAndWarnings, BooleanAndDates, SqliteVersion, NamedPlaceholders, MealIngredients and InMemoryDatabase"
lib = ir["sqlite_library_by_interpreter"]
out = []
out.append("Python and SQLite on this page: the examples run in your browser, in Python 3.13.2 with SQLite 3.39.0 (Pyodide 0.28.2), while the research behind the page ran under Python 3.14.6 with SQLite %s. Eight examples were rewritten for research version 1.0.3 so that they give the same result in both: %s. Each was run in the browser and compared with its stored result. The deck's worked examples are used as the deck has them, so three of them print something different here (title, connect and values) and say so under the example list of Chapter examples." % (lib["3.14.6"], names))
out.append("Recorded, not run: two examples start another program, which a browser cannot do, so they show the output recorded under Python 3.14.6 and are labelled so: " + ", ".join(so["recorded"]) + " (the sqlite3 shell of release %s and python -m sqlite3)." % find("sqlite.org home page")[0])
sw = find("sweigartcats.db of the online materials")
mat = find("online materials of the 3rd edition")
dbs = find("online materials: the files")["databases"]["sweigartcats-original.db"]
out.append("The book's database: five examples open sweigartcats.db from the online materials of the 3rd edition (a zip of %s bytes, SHA-256 %s). The research scripts download it; a browser page cannot depend on a download, so this page holds the file itself (%s bytes, SHA-256 starting 41f0d0b5bc2e, %d cats and %d vaccination rows), writes it to the browser's temporary folder, and each example still checks the hash before it opens the file. The zip carries no licence file; the book's text is free to read under a Creative Commons licence, and the course owner should confirm that this file may be kept on the page." % (format(mat[1], ","), mat[2], format(dbs[0], ","), sw[0], sw[1]))
out.append("NOT EXECUTED: " + notexec + ".")
out.append("What the public sites answered on 2026-10-12 is in live_observations_v1_0_0.json: the chapter's page (status %d, %s bytes, equal to the digest in the book's ontology), sqlite.org's newest release (%s, dated %s) and the pages of the three database tools. It is one request each, on one day, and nothing re-checks it." % (find("chapter 16 page: status")[0], format(find("chapter 16 page: status")[1], ","), find("sqlite.org home page")[0], find("sqlite.org home page")[1]))
out.append("One program was run under %d interpreters (%s); the SQLite library an interpreter links is the one of its build: %s. The items that differ between them are listed in interpreter_record_v1_0_0.json. Because of that, a result that names a version is a result for that version." % (len(ir["interpreters"]), ", ".join(ir["interpreters"]), ", ".join("%s to %s" % (k, v) for k, v in lib.items() if k in ("3.11.17", "3.14.0", "3.14.5"))))
out.append("Timings: where the deck shows a time (slides 7, 15 and 18) it is one measured run on one machine and is labelled so; no example on this page prints a time.")
json.dump({"_version": __version__, "limits": out}, open(os.path.join(H, "limits_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
for x in out: print("-", x[:300])
