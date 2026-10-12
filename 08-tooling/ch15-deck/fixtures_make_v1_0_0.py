"""Makes the stale fixtures the chapter 15 deck checks must refuse, from the deck itself; each is the finished deck with ONE text
run (or one chart value) on ONE named part changed to something plausible that is not what Python printed or what the deck must say:
  stale_expr     slide 10: the console result of col(27), 'AA', shown as 'AB'
  stale_table    slide 20: the audit balance of Miles Bron, 38,283, shown as 38,284 (the table is computed from the CSV export)
  stale_chart    the native chart of slide 17: the last pause 45 seconds shown as 46
  stale_program  slide 16: the transcript line 'True HttpError 9 [10, 15, ... 45]' shown as 'True HttpError 8 [...]'
  stale_code     slide 12: the program line '    columnOne[i] = value.upper()' shown as '.lower()'
  stale_tcap     slide 15: the transcript line '100 reads of a cell and 100 of a row, requests: 0' shown as 'requests: 1'
  stale_diagram  slide 4: the diagram label 'Create or upload spreadsheets' shown as 'Create or delete spreadsheets'
  stale_label    slide 12: the sentence 'Stand-in for Google: ...' removed (a stand-in output shown without saying so)
  stale_notexec  slide 6: the card 'NOT EXECUTED here' changed to 'Run here' (a Google step presented as if run)
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
edit(f("expr"), slide(10), "<a:t>'AA'</a:t>", "<a:t>'AB'</a:t>")
edit(f("table"), slide(20), "<a:t>38,283</a:t>", "<a:t>38,284</a:t>")
edit(f("chart"), "ppt/charts/chart1.xml", "<c:v>45</c:v>", "<c:v>46</c:v>")
edit(f("program"), slide(16), "<a:t>True HttpError 9 [10, 15, 20, 25, 30, 35, 40, 45]</a:t>", "<a:t>True HttpError 8 [10, 15, 20, 25, 30, 35, 40, 45]</a:t>")
edit(f("code"), slide(12), "<a:t>    columnOne[i] = value.upper()</a:t>", "<a:t>    columnOne[i] = value.lower()</a:t>")
edit(f("tcap"), slide(15), "<a:t>100 reads of a cell and 100 of a row, requests: 0</a:t>", "<a:t>100 reads of a cell and 100 of a row, requests: 1</a:t>")
edit(f("diagram"), slide(4), "<a:t>Create or upload spreadsheets</a:t>", "<a:t>Create or delete spreadsheets</a:t>")
edit(f("label"), slide(12), "<a:t>Stand-in for Google: this output comes from", "<a:t>Output: this output comes from")
edit(f("notexec"), slide(6), "<a:t>NOT EXECUTED here</a:t>", "<a:t>Run here</a:t>")
print("fixtures written to", out)
