"""Chapter 19 deck visuals, version 2.0.0: the executed result of every code example drawn as a native table, a native chart or a drawn flow with arrows.
Every number, string and truth value shown is taken from the run of the example's own code (the namespace `ns` and the printed text `out` that the
generic builder 08-tooling/chapter_deck_build_v2_1_0.py passes in); nothing is typed in by hand except plain-language names of boxes and columns.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "2.0.0"
import ast
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from deck_kit_v2_0_0 import C, MONO, arrow, chart, label_shape as _label_shape, table as _table, tb, rect


def table(s, x, y, w, rows, colw, fs=10.5, **kw):
    return _table(s, x, y, w, rows, colw, fs=fs, **kw)


def need(h):
    def deco(f):
        f.need = h
        return f
    return deco


FILL = {"plain": C["card"], "red": C["redLight"], "amber": C["amberLight"], "teal": C["tealLight"], "green": C["greenLight"], "grey": C["grey"]}


def box(s, x, y, w, h, text, kind="plain", fs=10, mono=False):
    return _label_shape(s, x, y, w, h, text, FILL[kind], C["ink"], size=fs, line=C["line"], radius=0.12, font=MONO if mono else None)


def note(s, x, y, w, text, h=0.24, fs=9.5):
    return tb(s, x, y, w, h, text, fs, C["muted"], italic=True, name="visual note")


def flow(s, x, y, w, items, kinds=None, h=0.5, fs=9.5, gap=0.32, mono=False):
    n = len(items)
    bw = (w - gap * (n - 1)) / n
    for i, t in enumerate(items):
        xx = x + i * (bw + gap)
        box(s, xx, y, bw, h, t, kinds[i] if kinds else "plain", fs, mono)
        if i < n - 1:
            arrow(s, xx + bw + 0.02, y + h / 2, xx + bw + gap - 0.02, y + h / 2, C["muted"], 1.5)
    return bw


def lines(out):
    return out.rstrip("\n").split("\n")


def val(line):
    return line.split(": ", 1)[1] if ": " in line else line


def lit(text):
    return ast.literal_eval(text)


# ------------------------------------------------------------------ part 1: time as a number
@need(1.3)
def v_epoch(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["Moment (UTC)", "Seconds since the epoch", "Printed by the program"],
            ["a day in March 2026 (calendar.timegm)", str(ns["t"]), val(L[0])],
            ["second 0: the epoch itself", "0", val(L[1])],
            ["2**31 - 1: the last second of 32 signed bits", str(2 ** 31 - 1), val(L[2])],
            ["2**31 stored in 32 bits, read back as signed", str(-2 ** 31), val(L[3])]]
    table(s, x, y, w, rows, [3.6, 2.2, 3.4], rowh=0.3, mono_cols=(1, 2), cell_fill={(4, 2): C["redLight"], (4, 1): C["redLight"]}, fs=10)


@need(1.25)
def v_clocks(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["Clock", "Never goes back", "Can be set by hand"]]
    for ln in L[:3]:
        a, b, c = ln.split()
        rows.append([a + "()", b, c])
    table(s, x, y, w * 0.52, rows, [1.9, 1.5, 1.6], rowh=0.3, mono_cols=(0,), cell_fill={(1, 1): C["redLight"], (1, 2): C["amberLight"], (2, 1): C["greenLight"], (3, 1): C["greenLight"]}, fs=10)
    wb, mo = ns["wall"], ns["mono"]
    box(s, x + w * 0.57, y + 0.03, w * 0.43, 0.5, "wall clock set back 10 s:\nthe difference is %s" % (wb[1] - wb[0]), "red", 10, True)
    box(s, x + w * 0.57, y + 0.62, w * 0.43, 0.5, "monotonic clock, same 10 s:\nthe difference is %s" % (mo[1] - mo[0]), "green", 10, True)


@need(1.25)
def v_sleep(s, x, y, w, h, ns, out):
    L = lines(out)
    a, b = float(val(L[1])), float(val(L[2]))
    chart(s, "col", x, y, w * 0.5, max(h, 1.25), ["sleep after the work", "fixed tick"], [("seconds after 3600 rounds", [a, b])], fs=10, legend=False, gap=60)
    box(s, x + w * 0.55, y + 0.05, w * 0.45, 0.42, "3600 rounds of 'work, then sleep(1)'", "plain", 10)
    box(s, x + w * 0.55, y + 0.52, w * 0.45, 0.4, "late by %.2f seconds" % (a - b), "red", 11, True)
    note(s, x + w * 0.55, y + 0.95, w * 0.45, "sleep() itself returns " + str(ns["result"]) + ".", fs=9.5, h=0.24)


@need(1.45)
def v_stopwatch(s, x, y, w, h, ns, out):
    L = lines(out)
    laps, totals = [], []
    for ln in L:
        t, g = ln.split(": ")[1].split()
        totals.append(float(t))
        laps.append(float(g.strip("()")))
    chart(s, "col", x, y, w * 0.5, max(h, 1.45), ["Lap #%d" % (i + 1) for i in range(len(laps))], [("lap time (s)", laps)], fs=10, legend=False, gap=60)
    rows = [["Printed line", "Total", "Lap"]] + [[ln.split(":")[0], str(t), str(g)] for ln, t, g in zip(L, totals, laps)]
    table(s, x + w * 0.55, y + 0.05, w * 0.45, rows, [1.5, 1.0, 1.0], rowh=0.27, mono_cols=(0, 1, 2), fs=10)


# ------------------------------------------------------------------ part 2: dates and times of day
@need(1.3)
def v_durations(s, x, y, w, h, ns, out):
    L = lines(out)
    days, secs, total = L[0].split()
    rows = [["What the program built", "Result"],
            ["timedelta(days=11, hours=10, minutes=9, seconds=8): .days", days],
            ["the same timedelta: .seconds (the part left over, not a total)", secs],
            ["the same timedelta: .total_seconds()", total],
            ["timedelta(months=1)", "TypeError: no such unit"],
            ["2026-10-21 minus 365 * 30 days, then the year set to 1996", L[2].split()[0] + " and " + L[2].split()[1]]]
    table(s, x, y, w, rows, [6.4, 2.8], rowh=0.25, mono_cols=(1,), cell_fill={(4, 1): C["redLight"], (5, 1): C["amberLight"]}, fs=10)


@need(1.15)
def v_strftime(s, x, y, w, h, ns, out):
    L = lines(out)
    fm = ["%Y/%m/%d %H:%M:%S", "%I:%M %p", "%A, %B %d", "%j %w", "isoformat()", "fromisoformat()"]
    rows = [["Directives", "Printed"]] + [[a, b] for a, b in zip(fm, L)]
    table(s, x, y, w * 0.49, rows[:4], [1.9, 2.5], rowh=0.28, mono_cols=(0, 1), fs=10)
    table(s, x + w * 0.51, y, w * 0.49, [rows[0]] + rows[4:], [1.9, 2.5], rowh=0.28, mono_cols=(0, 1), fs=10)
    note(s, x, y + 1.18, w, "%%j is the day of the year (%s), %%w the weekday with Sunday as 0 (%s)." % tuple(L[3].split()), fs=9.5, h=0.22)


@need(1.1)
def v_strptime(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["Text", "Format", "Result"],
            ["October 21, 2026", "%B %d, %Y", "a datetime"],
            ["2026-10-21", "%B %d, %Y", "ValueError"],
            ["Oct 21, 2026", "%B %d, %Y", "ValueError"]]
    table(s, x, y, w * 0.5, rows, [1.6, 1.4, 1.3], rowh=0.28, mono_cols=(0, 1, 2), cell_fill={(2, 2): C["redLight"], (3, 2): C["redLight"], (1, 2): C["greenLight"]}, fs=10)
    pairs = [ln.split() for ln in L[3:]]
    rows2 = [["%y"] + [p[0] for p in pairs], ["year"] + [p[1] for p in pairs]]
    table(s, x + w * 0.52, y, w * 0.48, rows2, [0.7] + [0.7] * len(pairs), rowh=0.28, mono_cols=(0, 1, 2, 3, 4, 5), cell_fill={(1, 3): C["amberLight"], (1, 4): C["amberLight"]}, fs=10)
    note(s, x + w * 0.52, y + 0.62, w * 0.48, "Two-digit years: 69 to 99 are 1969 to 1999, 00 to 68 are 2000 to 2068.", h=0.4, fs=9.5)


@need(1.0)
def v_zones(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["Question", "Answer"], ["naive == aware (same fields)", L[0]], ["naive - aware", "TypeError"]]
    table(s, x, y, w * 0.42, rows, [2.2, 1.4], rowh=0.26, mono_cols=(1,), cell_fill={(1, 1): C["redLight"], (2, 1): C["redLight"]}, fs=9.5)
    rows2 = [["Zone", "Second 1,000,000 of the epoch there"]] + [ln.split(" ", 1) for ln in L[2:]]
    table(s, x + w * 0.45, y, w * 0.55, rows2, [1.8, 2.6], rowh=0.26, mono_cols=(0, 1), fs=9)


@need(1.25)
def v_dst(s, x, y, w, h, ns, out):
    from datetime import UTC
    wall = (ns["y"] - ns["x"]).total_seconds() / 3600.0
    real = (ns["y"].astimezone(UTC) - ns["x"].astimezone(UTC)).total_seconds() / 3600.0
    chart(s, "col", x, y, w * 0.4, max(h, 1.25), ["wall: x + 1 day", "real elapsed"], [("hours", [wall, real])], fs=10, legend=False, gap=60, vmax=26, major=4)
    f, g = ns["first"].astimezone(UTC).hour, ns["second"].astimezone(UTC).hour
    chart(s, "col", x + w * 0.42, y, w * 0.3, max(h, 1.25), ["fold=0", "fold=1"], [("UTC hour of 01:30", [f, g])], fs=10, legend=False, gap=60, vmax=8, major=2)
    box(s, x + w * 0.75, y + 0.1, w * 0.25, 0.55, "one clock reading,\ntwo moments", "amber", 10, True)
    box(s, x + w * 0.75, y + 0.72, w * 0.25, 0.45, "first == second: %s" % (ns["first"] == ns["second"]), "red", 10, True)


# ------------------------------------------------------------------ part 3: launching programs
@need(1.2)
def v_run(s, x, y, w, h, ns, out):
    L = lines(out)
    code, so, se = L[0].split(" ", 2)
    ty, rep = L[1].split(" ", 1)
    rows = [["Call", "returncode", "stdout", "stderr"],
            ["run(command, capture_output=True)", code, so, se],
            ["run(command, capture_output=True, text=True)", code, ty + " " + rep, "str"]]
    table(s, x, y, w, rows, [3.8, 1.2, 2.4, 1.8], rowh=0.34, mono_cols=(1, 2, 3), cell_fill={(1, 2): C["amberLight"], (2, 2): C["greenLight"]}, fs=10)
    note(s, x, y + 1.15, w, "Without text=True the output arrives as bytes; with it, as str.", fs=9.5, h=0.22)


@need(1.3)
def v_popen(s, x, y, w, h, ns, out):
    L = lines(out)
    flow(s, x, y + 0.02, w, ["Popen(['sleep', '0.4'])\nstarts at once", L[0], "wait() blocks\n" + L[1], L[2]], ["teal", "amber", "plain", "green"], h=0.55, fs=9.5, gap=0.35)
    rows = [["Call that fails", "Exception", "Message"]]
    for ln in L[3:]:
        a, b = ln.split(" ", 1)
        rows.append([{"FileNotFoundError": "a program that does not exist", "CalledProcessError": "check=True and exit status 1"}[a], a, b])
    table(s, x, y + 0.72, w, rows, [2.7, 2.3, 4.2], rowh=0.26, mono_cols=(1,), fs=9.5)


@need(1.45)
def v_exits(s, x, y, w, h, ns, out):
    L = lines(out)
    a = [int(v) for v in L[0].split()]
    b = [int(v) for v in L[1].split()]
    names = ["pass", "sys.exit(3)", "raise ValueError", "SIGKILL", "SIGTERM"]
    chart(s, "col", x, y, w * 0.62, max(h, 1.45), names, [("returncode", a + b)], fs=9, legend=False, gap=50)
    box(s, x + w * 0.66, y + 0.1, w * 0.34, 0.6, "0 means success;\nanything else means failure", "green", 10)
    box(s, x + w * 0.66, y + 0.8, w * 0.34, 0.6, "a negative number is the\nsignal that ended the child", "amber", 10)


@need(0.94)
def v_shell(s, x, y, w, h, ns, out):
    L = lines(out)
    r = [lit(l) for l in L]
    rows = [["Call", "What the shell ran", "Printed"],
            ["shell=True, f-string with the name", "two commands: echo, then echo INJECTED", repr(r[0])],
            ["shell=True, shlex.quote(name)", "one command with one argument", repr(r[1])],
            ["a list of arguments, no shell", "one program, one argument", repr(r[2])]]
    table(s, x, y, w, rows, [3.0, 3.1, 3.1], rowh=0.24, mono_cols=(2,), cell_fill={(1, 2): C["redLight"], (2, 2): C["greenLight"], (3, 2): C["greenLight"]}, fs=9)


# ------------------------------------------------------------------ part 4: scheduling
@need(0.95)
def v_sched(s, x, y, w, h, ns, out):
    order = ns["log"]
    flow(s, x, y + 0.03, w, ["run() starts"] + order + ["clock: %s s" % ns["now"][0]], ["teal"] + ["plain"] * len(order) + ["green"], h=0.5, fs=10, gap=0.3)
    note(s, x, y + 0.62, w, "Soonest first. 'five-0' and 'five' are both due at 5 seconds: the lower priority number (0) goes first.", fs=9.5, h=0.26)


@need(0.9)
def v_cron(s, x, y, w, h, ns, out):
    L = lines(out)
    st = ns["start"]
    rows = [["Cron fields: minute hour weekday", "Meaning", "Next run after " + st.strftime("%Y-%m-%d %H:%M %a")],
            ["30 9 1-5", "09:30 on weekdays", L[0]],
            ["0 0 5", "midnight on Fridays", L[1]]]
    table(s, x, y, w, rows, [3.0, 2.4, 3.8], rowh=0.28, mono_cols=(0, 2), cell_fill={(1, 2): C["greenLight"], (2, 2): C["greenLight"]}, fs=10)


# ------------------------------------------------------------------ part 5: practice programs
@need(1.0)
def v_countdown(s, x, y, w, h, ns, out):
    L = lines(out)
    nums = L[0].split()
    flow(s, x, y + 0.03, w, nums + ["alarm"], ["teal"] * len(nums) + ["amber"], h=0.5, fs=14, gap=0.22)
    note(s, x, y + 0.65, w, L[1] + ".", fs=10, h=0.3)


@need(1.25)
def v_pretty(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["Lap", "Total", "Lap time", "Printed line"]]
    for (n, t, g), ln in zip(ns["rows"], L):
        rows.append([str(n), str(t), str(g), ln])
    table(s, x, y, w, rows, [0.7, 1.1, 1.3, 4.4], rowh=0.25, mono_cols=(3,), fs=10)


@need(0.95)
def v_friday(s, x, y, w, h, ns, out):
    L = lines(out)
    f = ns["found"]
    rows = [f[:5], f[5:]]
    table(s, x, y, w, rows, [1] * 5, rowh=0.3, header=False, mono_cols=(0, 1, 2, 3, 4), fs=10)
    note(s, x, y + 0.68, w, "First and last: " + L[0] + " - " + L[1] + ". Every one is a day 13 that weekday() numbers 4.", fs=9.5, h=0.24)


VISUALS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("v_") and callable(v)}
