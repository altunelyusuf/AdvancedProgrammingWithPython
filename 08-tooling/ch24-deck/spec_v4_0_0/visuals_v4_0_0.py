"""Chapter 24 deck visuals, version 4.0.0 (Lineage14): the executed result of every code example drawn as native tables and charts, and the pictures that the run itself made (the strips of
sound waves and the picture of the subtitle cues that an example saved in its own folder).
Every number, string and picture shown is taken from the run of the example's own code (the namespace `ns` and the printed text `out` that the generic builder 08-tooling/chapter_deck_build_v2_11_0.py
gives each function); nothing is typed in by hand except plain-language names of boxes and columns. Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "4.0.0"
import ast
import os
import re
import tempfile
from deck_kit_v2_2_0 import C, MONO, chart, label_shape as _label_shape, picture, rect, table as _table, tb


def table(s, x, y, w, rows, colw, fs=10.5, **kw):
    return _table(s, x, y, w, rows, colw, fs=fs, **kw)


def need(h):
    def deco(f):
        f.need = h
        return f
    return deco


def note(s, x, y, w, text, h=0.24, fs=9.5):
    return tb(s, x, y, w, h, text, fs, C["muted"], italic=True, name="visual note")


def lines(out):
    """the printed lines without the lines that the helpers and the speech engine print about files they saved"""
    return [ln for ln in out.rstrip("\n").split("\n") if ln.strip() and not ln.startswith("saved ") and not ln.startswith("Audio saved")]


def lit(text):
    return ast.literal_eval(text)


_KEEP = []


def pic(s, path, x, y, w, h, descr):
    """the picture the run made, drawn as it is, inside the box x, y, w, h"""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    fd, tmp = tempfile.mkstemp(suffix=".png", prefix="ch24_result_")
    os.close(fd)
    im.resize((im.width * 2, im.height * 2), Image.NEAREST).save(tmp)
    _KEEP.append(tmp)
    rect(s, x - 0.03, y - 0.03, w + 0.06, h + 0.06, C["line"], name="frame")
    return picture(s, tmp, x, y, w, h, descr, "result picture")


def reading(s, x, y, w, rows, rowh=0.27, fs=10, fills=None, head=("What the run printed", "Value")):
    return table(s, x, y, w, [list(head)] + rows, [w * 0.36, w * 0.64], rowh=rowh, mono_cols=(1,), cell_fill=fills, fs=fs)


G, A, R = C["greenLight"], C["amberLight"], C["redLight"]


def after(line, sep):
    return line.split(sep, 1)[1].strip()


@need(1.8)
def v_pins(s, x, y, w, h, ns, out):
    L = lines(out)
    pk = lit(L[1])
    rows = [["Python", L[0]], ["pyttsx3", pk[0]], ["openai-whisper", pk[1]], ["yt-dlp", pk[2]], ["numpy", pk[3]]]
    reading(s, x, y, w * 0.5, rows, rowh=0.28, fs=10, head=("Package", "Version"), fills={(2, 1): G, (3, 1): G, (4, 1): G})
    tools = [["ffmpeg on the PATH", L[2]], ["eSpeak NG on the PATH", L[3]], ["a sound device", L[4]]]
    reading(s, x + w * 0.55, y, w * 0.45, tools, rowh=0.3, fs=10, head=("Outside Python", "Found"), fills={(1, 1): G, (2, 1): G, (3, 1): R})
    note(s, x + w * 0.55, y + 1.3, w * 0.45, "No sound device: the speech goes into files.", h=0.3)


@need(1.8)
def v_pins(s, x, y, w, h, ns, out):
    L = lines(out)
    pk = lit(L[1])
    rows = [["Python", L[0]], ["pyttsx3", pk[0]], ["openai-whisper", pk[1]], ["yt-dlp", pk[2]], ["numpy", pk[3]]]
    reading(s, x, y, w * 0.5, rows, rowh=0.28, fs=10, head=("Package", "Version"), fills={(2, 1): G, (3, 1): G, (4, 1): G})
    tools = [["ffmpeg on the PATH", L[2]], ["eSpeak NG on the PATH", L[3]], ["a sound device", L[4]]]
    reading(s, x + w * 0.55, y, w * 0.45, tools, rowh=0.3, fs=10, head=("Outside Python", "Found"), fills={(1, 1): G, (2, 1): G, (3, 1): R})
    note(s, x + w * 0.55, y + 1.3, w * 0.45, "No sound device: the speech goes into files.", h=0.3)


@need(1.8)
def v_voices(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["voices, the first one", L[0]], ["its languages", L[1]], ["the engine starts with", L[2]], ["voices[1], saved as hello.wav", L[3]]]
    reading(s, x, y, w, rows, rowh=0.36, fs=10.5, fills={(4, 1): G})


@need(2.3)
def v_rate(s, x, y, w, h, ns, out):
    rate = [(int(m.group(1)), float(m.group(2))) for m in re.finditer(r"^ *(\d+) -> ([0-9.]+) s$", out, re.M)]
    vol = [(m.group(1), int(m.group(2))) for m in re.finditer(r"^([0-9.]+) (\d+)$", out, re.M)]
    chart(s, "col", x, y, w * 0.5, 2.1, ["%d" % r for r, _ in rate], [("seconds of audio", [v for _, v in rate])], fs=9, legend=False, gap=40, axis_title="seconds, by rate")
    rows = [[v, str(p)] for v, p in vol]
    table(s, x + w * 0.54, y + 0.05, w * 0.46, [["Volume", "Peak of the samples"]] + rows, [w * 0.2, w * 0.26], rowh=0.3, mono_cols=(0, 1), cell_fill={(5, 1): A}, fs=10)


def rows_h(rows, w, fs, col=0.64, base=0.2):
    """the height of one row for the longest value, so that nothing spills out of its cell"""
    per = max(8, int(w * col * 72 / (0.56 * fs)))
    lines_n = max(-(-len(str(r[-1])) // per) for r in rows)
    return base + 0.15 * max(lines_n, 1) * fs / 9.0


def nrw(s, x, y, w, rows, fs=9, fills=None, head=("What the run printed", "Value"), col=0.62):
    """a two-column reading for the narrow area (3.25 in wide) of a left layout"""
    rh = max(0.26, rows_h(rows, w, fs, col))
    table(s, x, y, w, [list(head)] + rows, [w * (1 - col), w * col], rowh=rh, mono_cols=(1,), cell_fill=fills, fs=fs)
    return y + rh * (len(rows) + 1)


def strip_block(s, x, y, w, path, h, descr, caption):
    pic(s, path, x, y, w, h, descr)
    note(s, x, y + h + 0.04, w, caption, h=0.24, fs=8.5)
    return y + h + 0.32


@need(1.2)
def v_say(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["say() returned", L[0].replace("say() returned ", "")], ["after runAndWait()", after(L[1], ":")], ["runAndWait() once", after(L[2], ":")], ["runAndWait() twice", after(L[3], ":")]]
    nrw(s, x, y, w, rows, fs=9.5, fills={(1, 1): A, (2, 1): G, (3, 1): G, (4, 1): R})


@need(1.2)
def v_wav(s, x, y, w, h, ns, out):
    L = lines(out)
    yy = strip_block(s, x, y, w, "hello.png", 0.62, "the samples of hello.wav drawn as a strip", "The samples of hello.wav")
    rows = [["file before runAndWait()", after(L[0], ":")], ["channels, bytes, rate", L[1]], ["length", L[2]], ["hello.mp3 begins with", L[3]]]
    nrw(s, x, yy + 0.05, w, rows, fs=9, fills={(1, 1): A, (4, 1): A})


@need(1.2)
def v_models(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = []
    for ln in L[1:4]:
        m = re.match(r"(\w+) +([0-9.]+) M, (\d+) bytes", ln)
        rows.append((m.group(1), float(m.group(2)), int(m.group(3))))
    chart(s, "col", x, y, w, 1.55, [r[0] for r in rows], [("millions of parameters", [r[1] for r in rows])], fs=9, legend=False, gap=50, axis_title="millions of parameters")
    body = [[r[0], "%.1f M" % r[1], "%.1f MB" % (r[2] / 1e6)] for r in rows]
    table(s, x, y + 1.65, w, [["Model", "Parameters", "File"]] + body, [w * 0.25, w * 0.35, w * 0.4], rowh=0.27, mono_cols=(1, 2), fs=9)
    nrw(s, x, y + 2.95, w, [["cuda available", L[4].split("|")[0].replace("cuda:", "").strip()], ["device='cuda'", L[5]]], fs=9, fills={(2, 1): R}, head=("On this machine", "Value"))


@need(1.2)
def v_trans(s, x, y, w, h, ns, out):
    rows = []
    for ln in lines(out):
        m = re.match(r"(\w+) +(.*) WER ([0-9.]+)$", ln)
        if m:
            rows.append((m.group(1), m.group(2), float(m.group(3))))
    chart(s, "col", x, y, w, 1.5, [r[0] for r in rows], [("word error rate", [r[2] for r in rows])], fs=9, legend=False, gap=50, axis_title="word error rate")
    body = [[r[0], r[1].strip("'\" ")] for r in rows]
    nrw(s, x, y + 1.6, w, body, fs=8.5, fills={(1, 1): R, (2, 1): A, (3, 1): G}, head=("Model", "What it wrote"), col=0.74)


@need(1.2)
def v_ffmpeg(s, x, y, w, h, ns, out):
    L = lines(out)
    yy = strip_block(s, x, y, w, "audio16k.png", 0.62, "the samples of the sentence at 16000 numbers a second", "The audio as Whisper reads it")
    rows = [["load_audio() returned", L[0]], ["without ffmpeg on the PATH", L[1]]]
    nrw(s, x, yy + 0.05, w, rows, fs=9, fills={(2, 1): R}, col=0.6)


@need(1.2)
def v_lang(s, x, y, w, h, ns, out):
    rows = []
    for ln in lines(out):
        m = re.match(r"(\S+) +heard as (\{.*\})", ln)
        if m:
            d = lit(m.group(2))
            rows.append([m.group(1), d["tiny"], d["base"]])
    fills = {}
    for i, r in enumerate(rows, 1):
        for j in (1, 2):
            fills[(i, j)] = G if r[j] == r[0][:2] else R
    table(s, x, y, w, [["Said in", "tiny heard", "base heard"]] + rows, [w * 0.3, w * 0.35, w * 0.35], rowh=0.3, mono_cols=(0, 1, 2), cell_fill=fills, fs=9.5)
    bad = [ln for ln in lines(out) if "Unsupported" in ln][0]
    nrw(s, x, y + 0.3 * (len(rows) + 1) + 0.15, w, [["language klingon", bad]], fs=9, fills={(1, 1): R}, head=("A language that does not exist", "Error"), col=0.6)
    note(s, x, y + 2.7, w, "Green: the language that was said. Red: another one.", h=0.4, fs=9)


@need(1.2)
def v_cues(s, x, y, w, h, ns, out):
    L = lines(out)
    yy = strip_block(s, x, y, w, "cues.png", 0.55, "the two cues on a time axis", "The two cues on a time axis")
    rows = [["srt vs the book", after(L[0], "bytes,")], ["vtt vs the book", after(L[1], "bytes,")], ["tsv vs the book", after(L[2], "bytes,")],
            ["SRT time", L[3].split(": ", 1)[1]], ["VTT time", L[4].split(": ", 1)[1]], ["docx writer", L[6].split(": ", 1)[1]]]
    nrw(s, x, yy + 0.05, w, rows, fs=8.5, fills={(1, 1): G, (2, 1): G, (3, 1): G, (6, 1): R}, col=0.64)


@need(1.2)
def v_opt(s, x, y, w, h, ns, out):
    L = lines(out)
    first = " ".join(L[4:])
    rows = [["segments, blocks", L[0].replace("segments ", "")], ["words in segment 1", after(L[1], ":")], ["blocks at width 30", L[2].replace("max_line_width=30: ", "").split(";")[0]],
            ["the first block", first]]
    nrw(s, x, y, w, rows, fs=9, fills={(3, 1): G}, col=0.6)


@need(1.2)
def v_ytm(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["title", after(L[0], ":")], ["extractor, formats", L[1]], ["of the 13 keys, here", after(L[2], "here:")], ["keys missing", after(L[3], ":")], ["metadata.json", after(L[4], ":")]]
    nrw(s, x, y, w, rows, fs=9, fills={(4, 1): A}, col=0.6)


@need(1.2)
def v_ytd(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["download() returned", L[0].replace("download() returned ", "")], ["the folder holds", L[1]], ["ffprobe says", L[2]], ["a string, not a list", after(L[3], ":")],
            ["an address that is nowhere", after(L[4], ":")]]
    nrw(s, x, y, w, rows, fs=9, fills={(4, 1): A, (5, 1): R}, col=0.6)


@need(1.2)
def v_guess(s, x, y, w, h, ns, out):
    L = lines(out)
    secs = lit(L[-1])
    chart(s, "col", x, y, w, 1.6, ["line %d" % k for k in range(1, len(secs) + 1)], [("seconds", secs)], fs=9, legend=False, gap=50, axis_title="seconds of speech")
    rows = [["messages spoken", "%d, as WAV files" % len(secs)], ["the first", L[0]], ["the last", L[-2]]]
    nrw(s, x, y + 1.7, w, rows, fs=9, fills={(1, 1): G}, col=0.6)


@need(1.2)
def v_song(s, x, y, w, h, ns, out):
    L = lines(out)
    secs = float(L[1].split()[2])
    yy = strip_block(s, x, y, w, "song.png", 0.5, "three verses as a strip of sound waves", "Three verses as a strip")
    rows = [["3 verses, spoken", after(L[0], ":")], ["99 verses, spoken", after(L[1], ":")], ["99 verses in minutes", "%d min %d s" % (secs // 60, round(secs % 60))]]
    nrw(s, x, yy + 0.05, w, rows, fs=9, fills={(2, 1): A, (3, 1): A}, col=0.6)


@need(1.2)
def v_tube(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["first reading", L[0]], ["second reading", L[1]], ["one bad address", after(L[2], ":")]]
    nrw(s, x, y, w, rows, fs=10, fills={(3, 1): R}, col=0.6)


VISUALS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("v_") and callable(v)}
