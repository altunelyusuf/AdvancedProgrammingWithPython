"""Makes the stale fixtures the chapter 14 deck checks must refuse, from the deck itself; each is the finished deck with ONE text
run (or one chart value) on ONE named part changed to something plausible that is not what Python printed:
  stale_expr     slide 7: the console result of get_column_letter(27), 'AA', shown as 'AB'
  stale_table    slide 10: the county tally cell 3,141 (Aleutians East) shown as 3,142
  stale_chart    the native chart of slide 21: the square 81 shown as 80
  stale_program  slide 9: the transcript line 'The 2010 population of Anchorage was 12515' shown as 12516
  stale_code     slide 12: the program line 'if produce_name in PRICE_UPDATES:' shown as 'PRICE_UPDATE:'
  stale_tcap     slide 23: the live transcript line '200 9904' (status and size from the book's site) shown as '200 9905'
  stale_diagram  slide 6: the diagram label 'Read the value attribute of the Cell' shown as '... of the Row'
Each is refused by the check that owns it (deck_check, program_check, diagram_check); the build fails if one is not refused.
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
edit(f("expr"), slide(7), "<a:t>'AA'</a:t>", "<a:t>'AB'</a:t>")
edit(f("table"), slide(10), "<a:t>3,141</a:t>", "<a:t>3,142</a:t>")
edit(f("chart"), "ppt/charts/chart1.xml", "<c:v>81</c:v>", "<c:v>80</c:v>")
edit(f("program"), slide(9), "<a:t>The 2010 population of Anchorage was 12515</a:t>", "<a:t>The 2010 population of Anchorage was 12516</a:t>")
edit(f("code"), slide(12), "<a:t> PRICE_UPDATES:</a:t>", "<a:t> PRICE_UPDATE:</a:t>")
edit(f("tcap"), slide(23), "<a:t>200 9904</a:t>", "<a:t>200 9905</a:t>")
edit(f("diagram"), slide(6), "<a:t>Read the value attribute of the Cell</a:t>", "<a:t>Read the value attribute of the Row</a:t>")
print("fixtures written to", out)
