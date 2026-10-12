"""Makes the stale fixtures the chapter 16 deck checks must refuse, from the deck itself; each is the finished deck with ONE text
run (or one chart value) on ONE named part changed to something plausible that is not what Python printed or what the deck must say:
  stale_expr     slide 6: the console result [(1, 1, 1)] shown as [(1, 1, 2)]
  stale_table    slide 10: the stored-as word 'blob' shown as 'text' (the table is computed from sqlite3)
  stale_chart    the native chart of slide 15: the two-index size 512 KiB shown as 513
  stale_program  slide 8: the transcript line 'unknown datatype for bad.a: "BOOLEAN"' shown for "DATE"
  stale_code     slide 11: the program line 'weight_kg + 0.1' shown as '+ 0.2'
  stale_tcap     slide 15: the plan line 'name LIKE '%42'  SCAN cats' shown as 'SEARCH cats'
  stale_diagram  slide 4: the diagram label 'Insert rows into a table' shown as 'Insert columns into a table'
  stale_label    slide 21: the sentence 'Shipped database: ...' removed (a LIVE result shown without saying so)
  stale_notexec  slide 23: the card 'NOT EXECUTED here' changed to 'Run here' (installers presented as if run)
  stale_once     slide 15: 'Single runs on 12 Oct 2026' changed to 'Runs on 12 Oct 2026' (timings without saying single run)
Each is refused by the check that owns it (deck_check, program_check, diagram_check, honesty_check); the build fails if one is not refused.
Usage: fixtures_make_v1_0_0.py <deck.pptx> <out-dir>"""
__version__ = "1.0.0"
import os, sys, zipfile
deck, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)


def edit(dst, part, old, new):
    zin = zipfile.ZipFile(deck); zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED); n = 0
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename == part:
            assert data.count(old.encode()) == 1, (part, old, data.count(old.encode()))
            data = data.replace(old.encode(), new.encode(), 1); n += 1
        zout.writestr(it, data)
    zout.close(); assert n == 1, (old, n)


def slide(n):
    return "ppt/slides/slide%d.xml" % n


f = lambda name: os.path.join(out, "fixture_stale_%s_v1_0_0.pptx" % name)
edit(f("expr"), slide(6), "<a:t>[(1, 1, 1)]</a:t>", "<a:t>[(1, 1, 2)]</a:t>")
edit(f("table"), slide(10), "<a:t>blob</a:t>", "<a:t>text</a:t>")
edit(f("chart"), "ppt/charts/chart1.xml", "<c:v>512</c:v>", "<c:v>513</c:v>")
edit(f("program"), slide(8), '<a:t>OperationalError unknown datatype for bad.a: "BOOLEAN"</a:t>', '<a:t>OperationalError unknown datatype for bad.a: "DATE"</a:t>')
edit(f("code"), slide(11), "weight_kg + 0.1 WHERE fur = ?'</a:t>", "weight_kg + 0.2 WHERE fur = ?'</a:t>")
edit(f("tcap"), slide(15), "<a:t>name LIKE '%42'                        SCAN cats</a:t>", "<a:t>name LIKE '%42'                        SEARCH cats</a:t>")
edit(f("diagram"), slide(4), "<a:t>Insert rows into a table</a:t>", "<a:t>Insert columns into a table</a:t>")
edit(f("label"), slide(21), "<a:t>Shipped database: sweigartcats.db of the book's", "<a:t>Database: db of the book's")
edit(f("notexec"), slide(23), "<a:t>NOT EXECUTED here</a:t>", "<a:t>Run here</a:t>")
edit(f("once"), slide(15), "Single runs on 12 Oct 2026", "Runs on 12 Oct 2026")
print("fixtures written to", out)
