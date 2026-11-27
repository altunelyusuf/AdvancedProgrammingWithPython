"""Chapter 25 deck visuals, version 4.0.0 (Lineage14): the executed result of every code example drawn as native tables and charts, and the picture that the downloader saved in its own folder.
Every number, string and picture shown is taken from the run of the example's own code (the namespace `ns` and the printed text `out` that the generic builder 08-tooling/chapter_deck_build_v2_11_0.py
gives each function); nothing is typed in by hand except plain-language names of boxes and columns. Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants.
All code slides of this chapter use the left layout, so every visual draws in the narrow area (3.25 in wide)."""
__version__ = "4.0.0"
import ast
import os
import re
import tempfile
from deck_kit_v2_2_0 import C, chart, picture, rect, table as _table, tb


def table(s, x, y, w, rows, colw, fs=10.5, **kw):
    return _table(s, x, y, w, rows, colw, fs=fs, **kw)


def need(h):
    def deco(f):
        f.need = h
        return f
    return deco


def note(s, x, y, w, text, h=0.24, fs=9):
    return tb(s, x, y, w, h, text, fs, C["muted"], italic=True, name="visual note")


def lines(out):
    """the printed lines without the line the picture helper prints about the file it saved"""
    return [ln for ln in out.rstrip("\n").split("\n") if ln.strip() and not ln.startswith("saved ")]


def after(line, sep):
    return line.split(sep, 1)[1].strip()


G, A, R = C["greenLight"], C["amberLight"], C["redLight"]
_KEEP = []


def pic(s, path, x, y, w, h, descr):
    """the picture the run made, drawn as it is, inside the box x, y, w, h"""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    fd, tmp = tempfile.mkstemp(suffix=".png", prefix="ch25_result_")
    os.close(fd)
    im.resize((im.width * 2, im.height * 2), Image.NEAREST).save(tmp)
    _KEEP.append(tmp)
    rect(s, x - 0.03, y - 0.03, w + 0.06, h + 0.06, C["line"], name="frame")
    return picture(s, tmp, x, y, w, h, descr, "result picture")


def rows_h(rows, w, fs, col=0.64, base=0.2):
    """the height of one row for the longest value, so that nothing spills out of its cell"""
    per = max(8, int(w * col * 72 / (0.56 * fs)))
    lines_n = max(-(-len(str(r[-1])) // per) for r in rows)
    return base + 0.15 * max(lines_n, 1) * fs / 9.0


def nrw(s, x, y, w, rows, fs=9, fills=None, head=("What the run printed", "Value"), col=0.62):
    """a two-column reading for the narrow area (3.25 in wide) of a left layout; returns the y below it"""
    rh = max(0.26, rows_h(rows, w, fs, col))
    table(s, x, y, w, [list(head)] + rows, [w * (1 - col), w * col], rowh=rh, mono_cols=(1,), cell_fill=fills, fs=fs)
    return y + rh * (len(rows) + 1)


@need(1.2)
def v_start(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["1st line", L[0]], ["2nd line", L[1]], ["3rd line", L[2]], ["thread name, active threads", L[3].split(") ")[0] + ")"], ["name of the main thread", L[3].split(") ")[1]]]
    nrw(s, x, y, w, rows, fs=9, fills={(3, 1): A})


@need(1.2)
def v_args(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["go(' & ')", L[0]], ["go('& ')", L[1]], ["a call as the target", L[2]], ["is_alive()", after(L[3], ":")]]
    nrw(s, x, y, w, rows, fs=9, fills={(3, 1): R, (4, 1): R})


@need(1.2)
def v_life(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["start() twice", after(L[0], ":")], ["the thread's error", after(L[1], ":")], ["the main thread", L[2]]]
    nrw(s, x, y, w, rows, fs=9, fills={(1, 1): R, (2, 1): A, (3, 1): G})


@need(1.2)
def v_join(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["join(0.1) returned", L[0].split(" returned ")[1]], ["join()", L[1].replace("join() waited | ", "")], ["join() before start()", after(L[2], ":")]]
    nrw(s, x, y, w, rows, fs=9, fills={(1, 1): A, (2, 1): G, (3, 1): R})


@need(1.2)
def v_daemon(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["daemon=True prints", after(L[0], "prints")], ["daemon=False prints", after(L[1], "prints")], ["daemon set while running", after(L[2], ":")]]
    nrw(s, x, y, w, rows, fs=9, fills={(1, 1): A, (2, 1): G, (3, 1): R})


@need(1.2)
def v_printed(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["join() before start()", after(L[0], ":")], ["comic pages requested", after(L[1], ":")]]
    yy = nrw(s, x, y, w, rows, fs=9, fills={(1, 1): R, (2, 1): R})
    note(s, x, yy + 0.08, w, "The comic site's stand-in was never asked.", h=0.3)


@need(3.4)
def v_fixed(s, x, y, w, h, ns, out):
    L = lines(out)
    ph = 2.5
    pw = ph * 220 / 308
    pic(s, "skipped.png", x + (w - pw) / 2, y, pw, ph, "the comic numbers 1 to 139, green when asked for and orange when never asked for")
    note(s, x, y + ph + 0.05, w, "Orange: never asked for (9, 19, 29 ...)", h=0.24, fs=8.5)
    rows = [["numbers asked for", L[0].split(" | ")[0].replace("requested ", "")], ["never asked for", L[0].split(" | ")[1].replace("never requested ", "")]]
    nrw(s, x, y + ph + 0.33, w, rows, fs=9, fills={(2, 1): R})


@need(1.8)
def v_lost(s, x, y, w, h, ns, out):
    L = lines(out)
    no = ast.literal_eval(after(L[0], ":"))
    yes = ast.literal_eval(after(L[1], ":"))
    chart(s, "col", x, y, w, 1.9, ["no 1", "no 2", "no 3", "lock 1", "lock 2", "lock 3"], [("the counter at the end", no + yes)], fs=9, legend=False, gap=40, vmax=3, major=1, axis_title="final value of the counter")
    note(s, x, y + 1.95, w, "Two threads each add 1: the right value is 2.", h=0.3)


@need(1.2)
def v_lock(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["total of 4 x 100000", after(L[0], ":")], ["Lock taken again", after(L[1], ":")], ["RLock taken again", after(L[2], ":")]]
    nrw(s, x, y, w, rows, fs=9, fills={(1, 1): G, (2, 1): R, (3, 1): G})


@need(1.0)
def v_dead(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["thread 1 alive after 0.5 s", after(L[0], ":").split()[0]], ["thread 2 alive after 0.5 s", after(L[0], ":").split()[1]]]
    yy = nrw(s, x, y, w, rows, fs=9.5, fills={(1, 1): R, (2, 1): R})
    note(s, x, yy + 0.08, w, "Each waits for the lock that the other holds.", h=0.3)


@need(1.8)
def v_sem(s, x, y, w, h, ns, out):
    L = lines(out)
    two, six = int(after(L[0], ":")), int(after(L[1], ":"))
    chart(s, "col", x, y, w, 1.9, ["Semaphore(2)", "Semaphore(6)"], [("most threads inside at once", [two, six])], fs=9, legend=False, gap=60, vmax=7, major=1, axis_title="most threads inside at once")
    note(s, x, y + 1.95, w, "Six threads; each stays 0.1 s in the block.", h=0.3)


@need(1.2)
def v_queue(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["consumer received", after(L[0], "received")], ["Event before set()", after(L[1], ":")], ["Event after set()", after(L[2], ":")]]
    nrw(s, x, y, w, rows, fs=9, fills={(1, 1): G, (2, 1): A, (3, 1): G})


@need(1.2)
def v_pool(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["map()", after(L[0], ":")], ["as_completed()", after(L[1], ":")], ["names, 2 workers", after(L[2], ":")], ["default pool", after(L[3], ":")]]
    nrw(s, x, y, w, rows, fs=9, fills={(1, 1): G, (2, 1): A, (4, 1): A})


@need(1.2)
def v_future(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["exception()", after(L[0], ":")], ["result() raises", after(L[1], ":")], ["shutdown(cancel_futures)", after(L[2], "cancelled")]]
    nrw(s, x, y, w, rows, fs=9, fills={(1, 1): R, (2, 1): R, (3, 1): G})


@need(1.2)
def v_gil(s, x, y, w, h, ns, out):
    L = lines(out)
    std = after(L[1], ":").split()
    rows = [["standard build", "GIL on: %s, flag %s" % (std[0], std[1])], ["free-threaded", "GIL on: %s" % after(L[2], ":")], ["with PYTHON_GIL=1", "GIL on: %s" % after(L[3], ":")]]
    nrw(s, x, y, w, rows, fs=9, head=("Python 3.14.6", "Printed"), fills={(1, 1): R, (2, 1): G, (3, 1): R})


@need(1.2)
def v_proc(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["after a child process", after(L[0], ":")], ["after a thread", after(L[1], ":")], ["start method", after(L[2], ":")], ["poll() while it sleeps", after(L[3], ":")], ["wait()", after(L[4], ":")]]
    nrw(s, x, y, w, rows, fs=9, fills={(1, 1): A, (2, 1): G})


@need(1.2)
def v_async(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["5 awaits of 0.2 s", after(L[0], "under 0.6 s:")], ["5 blocking calls of 0.2 s", after(L[1], "under 0.6 s:")], ["5 on threads (to_thread)", after(L[2], "under 0.6 s:")]]
    nrw(s, x, y, w, rows, fs=9, head=("Finished under 0.6 s?", "Printed"), fills={(1, 1): G, (2, 1): R, (3, 1): G})


VISUALS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("v_") and callable(v)}
