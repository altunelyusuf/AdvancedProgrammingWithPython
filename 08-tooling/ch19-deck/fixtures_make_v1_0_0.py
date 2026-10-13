"""Makes the stale fixtures the chapter 19 deck checks must refuse, from the deck itself; each is the finished deck with ONE text
run (or one chart value) on ONE named part changed to something plausible that is not what Python printed or what the deck must say:
  stale_expr       slide 10: the console result 'datetime.timedelta(days=62)' changed to days=61
  stale_table      slide 12: the table cell for the day of the year, 307, changed to 306
  stale_chart      the native chart of slide 23: the 688 Friday 13ths changed to 689
  stale_program    slide 12: the transcript line '2026-10-21 16:29:07+00:00' changed to 16:29:08
  stale_code       slide 12: the program line 'print(x.isoformat())' shown as 'print(x.isoformat(1))'
  stale_tcap       slide 23: the transcript line 'backward: 3485 dates, earliest 0001-04-13' shown with 3486
  stale_diagram    slide 8: the diagram label 'Subtract the last time to get the lap time' shown as 'Add the last time ...'
  stale_notexec    slide 13: the card 'NOT EXECUTED here' changed to 'Run here' (Python 3.15 presented as if run)
  stale_once       slide 9: 'Single run, research:' changed to 'Run, research:' (a measurement without saying single run)
  stale_emulated   slide 6: the heading 'EMULATED, not a changed clock' changed to 'A changed clock' (an emulation presented as real)
  stale_honest_not slide 12: the line 'Lines 1 to 5 (imports, ...' changed to 'NOT EXECUTED (imports, ...' on a slide the plan does not list
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

edit(f("expr"), slide(10), "datetime.timedelta(days=62)", "datetime.timedelta(days=61)")
edit(f("table"), slide(12), "<a:t>307</a:t>", "<a:t>306</a:t>")
edit(f("chart"), "ppt/charts/chart1.xml", "<c:v>688</c:v>", "<c:v>689</c:v>")
edit(f("program"), slide(12), "2026-10-21 16:29:07+00:00", "2026-10-21 16:29:08+00:00")
edit(f("code"), slide(12), "print(x.isoformat())", "print(x.isoformat(1))")
edit(f("tcap"), slide(23), "backward: 3485 dates, earliest 0001-04-13", "backward: 3486 dates, earliest 0001-04-13")
edit(f("diagram"), slide(8), "Subtract the last time to get the lap time", "Add the last time to get the lap time")
edit(f("notexec"), slide(13), "NOT EXECUTED here", "Run here")
edit(f("once"), slide(9), "Single run, research:", "Run, research:")
edit(f("emulated"), slide(6), "EMULATED, not a changed clock", "A changed clock")
edit(f("honest_not"), slide(12), "Lines 1 to 5 (imports,", "NOT EXECUTED (imports,")
print("made 11 stale fixtures in", out)
