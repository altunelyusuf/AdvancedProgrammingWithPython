"""Chapter 24 lab helpers, version 1.0.0 (SEN0414, Lineage14): the hidden helpers of the chapter 24 deck examples (Make Python Talk).
They only measure and record: they read WAV files, draw strips of sound waves as PNG pictures with the standard library, measure a property in a child process, and fetch the one public-domain
reading (LibriVox, hosted by the Internet Archive) that stands in for a video site. Nothing is played: this machine has no sound card, so pyttsx3 writes WAV files. The request to archive.org
names the course and the GitHub account, nothing else. begin() gives every example its own empty working folder."""
__version__ = "1.0.0"
import array
import contextlib
import hashlib
import io
import itertools
import importlib.metadata as md
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request
import warnings
import wave
import zlib

warnings.simplefilter("ignore")
LATEST = sys.executable
HOME = os.path.expanduser("~")
CACHE = os.environ.get("CH24_CACHE", "/home/claude/ch24_cache")
os.makedirs(CACHE, exist_ok=True)
UA = {"User-Agent": "SEN0414-course-materials/1.0 (course materials; contact via GitHub altunelyusuf)"}
ASSETS = {"gettysburg_shurtagal.mp3": ("https://archive.org/download/gettysburg_shurtagal_librivox/Gettysburg_Address_Lincoln_64kb.mp3",
                                       "d9f40f965d68153694417cc739c7690021aa39ba80f22d1c3927aeaa97e29dc0")}
FOX = "The quick brown fox jumps over the yellow lazy dog."
_A = " Dinosaurs are a diverse group of reptiles of the clade dinosauria. They first"
_B = " appeared during the triassic period. Between 245 and 233.23 million years ago."
A, B = _A, _B


def sha(name):
    return hashlib.sha256(open(name, "rb").read()).hexdigest()[:12]


def done(name):
    keep = os.environ.get("CH24_KEEP")
    if keep:
        shutil.copy(name, os.path.join(keep, os.path.basename(name)))
    print("saved %s: %d bytes, sha256 %s" % (os.path.basename(name), os.path.getsize(name), sha(name)))


def fetch(name):
    """the one reading the examples use, fetched once and checked against its SHA-256"""
    path = os.path.join(CACHE, name)
    url, want = ASSETS[name]
    if not os.path.exists(path):
        data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read()
        open(path + ".part", "wb").write(data)
        os.replace(path + ".part", path)
    if hashlib.sha256(open(path, "rb").read()).hexdigest() != want:
        raise SystemExit("the reading differs from the file that was recorded")
    return path


def cached(model):
    return os.path.join(HOME, ".cache", "whisper", model + ".pt")


def wait_file(path, limit=60, quiet=0.4):
    """a WAV file is complete when its size has stopped changing"""
    start = time.time()
    last, since = -1, None
    while time.time() - start < limit:
        if os.path.exists(path):
            size = os.path.getsize(path)
            if size == last and size > 44:
                if since is not None and time.time() - since >= quiet:
                    return True
            else:
                since = time.time()
                last = size
        time.sleep(0.05)
    return os.path.exists(path)


def wavinfo(path):
    wait_file(path)
    w = wave.open(path)
    n = w.getnframes()
    a = array.array("h", w.readframes(n))
    return {"channels": w.getnchannels(), "width": w.getsampwidth(), "rate": w.getframerate(), "frames": n,
            "seconds": round(n / w.getframerate(), 2), "peak": max((abs(x) for x in a), default=0)}


def samples(path):
    w = wave.open(path)
    return list(array.array("h", w.readframes(w.getnframes()))), w.getframerate()


def png(name, w, h, pix):
    raw = b"".join(b"\x00" + bytes(c for x in range(w) for c in pix(x, y)) for y in range(h))

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
    head = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    open(name, "wb").write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", head) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def strips(name, rows, w=480, hh=60, colors=((47, 109, 98), (217, 122, 20), (43, 38, 34))):
    """rows: (samples, seconds) pairs; each strip draws the peak under every pixel column, on one time scale for all strips"""
    tmax = max(s for _, s in rows)
    cols = []
    for a, secs in rows:
        n = len(a)
        c = []
        for x in range(w):
            lo, hi = int(x * tmax / secs * n / w), int((x + 1) * tmax / secs * n / w)
            c.append(max((abs(v) for v in a[lo:max(hi, lo + 1)]), default=0) if lo < n else -1)
        cols.append(c)

    def pix(x, y):
        k, yy = divmod(y, hh + 4)
        if k >= len(rows) or yy >= hh:
            return (242, 236, 225)
        v = cols[k][x]
        if v < 0:
            return (242, 236, 225)
        half = hh // 2
        ext = max(1, int(v / 32768 * half))
        return colors[k % len(colors)] if abs(yy - half) <= ext else (255, 255, 255)
    png(name, w, len(rows) * (hh + 4), pix)
    done(name)


def trying(fn, *args, **kw):
    """call fn and say what happened: ok, or the kind of error and the first line of its message"""
    try:
        fn(*args, **kw)
    except BaseException as e:
        first = (str(e).splitlines() or [""])[0][:60]
        return "%s: %s" % (type(e).__name__, first) if first else type(e).__name__
    return "ok"


def kind(fn, *args, **kw):
    """call fn and give only the kind of error"""
    try:
        fn(*args, **kw)
    except BaseException as e:
        return type(e).__name__
    return "ok"


def say_to(engine, text, path):
    with contextlib.redirect_stdout(io.StringIO()):
        engine.save_to_file(text, path)
        engine.runAndWait()
        wait_file(path)


def words(text):
    return re.sub(r"[^a-z' ]+", " ", text.lower()).split()


def wer(ref, hyp):
    """word error rate: the edits that turn hyp into ref, over the words of ref"""
    r, h = words(ref), words(hyp)
    d = list(range(len(h) + 1))
    for i, a in enumerate(r, 1):
        c = [i]
        for j, b in enumerate(h, 1):
            c.append(min(d[j] + 1, c[j - 1] + 1, d[j - 1] + (a != b)))
        d = c
    return d[-1] / len(r)


_CHILD = """import pyttsx3, sys, time
e = pyttsx3.init(); e.setProperty(sys.argv[1], eval(sys.argv[2]))
e.save_to_file(sys.argv[3], 'm.wav'); e.runAndWait(); time.sleep(0.8)"""


def measure(prop, value, text):
    """say text with one property changed, in a fresh process; returns the samples, the seconds and the peak"""
    subprocess.run([LATEST, "-W", "ignore", "-c", _CHILD, prop, str(value), text], capture_output=True)
    a, rate = samples("m.wav")
    os.remove("m.wav")
    return a, round(len(a) / rate, 2), max(abs(v) for v in a)


def waits(code, limit=5):
    """run code in a child process and say whether it came back"""
    try:
        r = subprocess.run([LATEST, "-W", "ignore", "-c", code], capture_output=True, timeout=limit)
        return "returned, exit %d" % r.returncode
    except subprocess.TimeoutExpired:
        return "not back after %d seconds" % limit


def probe_audio(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name:format=duration", "-of", "json", path],
                       capture_output=True, text=True)
    j = json.loads(r.stdout)
    return j["streams"][0]["codec_name"], round(float(j["format"]["duration"]), 1)


def cues_picture(segs, name="cues.png", w=480, secs=15.0):
    """one bar for each subtitle cue on a time axis: the picture of the start and end times a writer prints"""
    def px(x, y):
        t = x / w * secs
        for k, s in enumerate(segs):
            if s["start"] <= t < s["end"] and 20 * k + 10 <= y < 20 * k + 26:
                return ((47, 109, 98), (217, 122, 20))[k % 2]
        return (242, 236, 225) if y % 40 < 38 else (200, 190, 175)
    png(name, w, 20 * len(segs) + 20, px)
    done(name)


def audio_opts(stem):
    return {"quiet": True, "no_warnings": True, "noprogress": True, "format": "bestaudio/best", "outtmpl": stem + ".%(ext)s",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "m4a"}]}


CHAPTER_KEYS = ["id", "title", "formats", "thumbnails", "thumbnail", "description", "channel_id", "channel_url", "duration", "view_count",
                "average_rating", "age_limit", "webpage_url"]
CHAPTER = {"srt": "1\n00:00:00,000 --> 00:00:05,640\n%s\n\n2\n00:00:05,640 --> 00:00:14,960\n%s\n" % (_A.strip(), _B.strip()),
           "vtt": "WEBVTT\n\n00:00.000 --> 00:05.640\n%s\n\n00:05.640 --> 00:14.960\n%s\n" % (_A.strip(), _B.strip()),
           "tsv": "start\tend\ttext\n0\t5640\t%s\n5640\t14960\t%s\n" % (_A.strip(), _B.strip())}


def begin():
    """each example works in its own empty folder; the builder keeps it so that a result visual can read the files the example saved"""
    os.chdir(tempfile.mkdtemp(prefix="ch24work"))
