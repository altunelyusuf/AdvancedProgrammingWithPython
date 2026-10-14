#!/usr/bin/env python3
"""Chapter 25 program check (the chapter 23 check, with a second kind of picture: the PHOTOGRAPHS of the stories, which no program saves). Every whole program (or excerpt) a slide shows is verified against the recording:
  (1) the label 'program <name>, lines a to b of n' must name a recorded program with n lines, and exactly those lines, in order, must be on the
      slide, verbatim (whitespace-normalised);
  (2) the program is run again now, here, with CH23_KEEP naming a temporary folder, and its transcript must equal the recorded one, with exit 0;
  (3) that transcript must be on the same slide, verbatim;
  (4) a panel labelled 'transcript of program <name>' (a transcript shown without its code) names a recorded program, which is run again and must
      print the recorded transcript, which must be on that slide;
  (5) PICTURES. A caption 'image <file> made by <program>' on a slide names a picture the recording holds, made by that program. The program is run
      again (the run of (2) is reused) and saves the picture again; the slide must carry, as one of its pictures, a file that is BYTE-IDENTICAL to what
      the program has just saved (the check says 'byte-identical') or, when the bytes differ, whose decoded pixels (mode, size and every pixel) are equal
      ('pixel-identical'); a picture that is neither is refused. The recorded SHA-256 of the file, the one the transcript printed, must equal that of
      the file just saved, and every picture on a slide must be named by a caption on it (no picture without a program).
  (6) PHOTOGRAPHS. A paragraph 'photo <file>: <credit>' on a slide names a file of photos/ (recorded with its author, licence and SHA-256 in photos_v1_0_0.json, which
      says what was fetched from Wikimedia Commons on which day and what was done to it). The paragraph must begin with the recorded credit line (title, author, licence, source),
      the file on disk must still have the recorded SHA-256, and the slide must carry, as one of its pictures, a file BYTE-IDENTICAL to it or PIXEL-IDENTICAL (re-encoded, the
      same decoded pixels). A picture with neither kind of caption is refused. A photograph is not re-fetched by this check: its source page is opened by links_check.
No program of this chapter reaches a person or a service: the two downloaders ask an HTTP server of their own on 127.0.0.1 (a local stand-in; xkcd.com is never contacted) and the others
use the standard library only. Each program is run again here under the interpreter given.
Usage: program_check_v1_0_0.py <deck.pptx> <examples_out.json> [python]   Exit 0 when nothing mismatches."""
__version__ = "1.0.0"
import hashlib
import json
import os
import re
import sys
import tempfile
import zipfile
from xml.dom import minidom

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck_check_v1_0_0 import slides
from progrun_v1_0_0 import run_program

CAP = re.compile(r"program ([A-Za-z0-9_.]+), lines (\d+) to (\d+) of (\d+)")
TCAP = re.compile(r"transcript of program ([A-Za-z0-9_.]+)")
IMG = re.compile(r"image ([A-Za-z0-9_]+\.png) made by ([A-Za-z0-9_.]+\.py)")
PHO = re.compile(r"^photo ([A-Za-z0-9_]+\.(?:png|jpg)): (.*)$")
HERE = os.path.dirname(os.path.abspath(__file__))
norm = lambda t: re.sub(r"\s+", " ", t).strip()


def pictures(deck):
    """slide number -> the list of media files (name, bytes) that the slide places as pictures, from its XML and its relationships"""
    z = zipfile.ZipFile(deck)
    out = {}
    for n in z.namelist():
        m = re.match(r"ppt/slides/slide(\d+)\.xml$", n)
        if not m:
            continue
        rels = minidom.parseString(z.read("ppt/slides/_rels/slide%s.xml.rels" % m.group(1)))
        target = {r.getAttribute("Id"): r.getAttribute("Target") for r in rels.getElementsByTagName("Relationship")}
        d = minidom.parseString(z.read(n))
        pics = []
        for pic in d.getElementsByTagName("p:pic"):
            for b in pic.getElementsByTagName("a:blip"):
                t = target[b.getAttribute("r:embed")]
                path = os.path.normpath(os.path.join("ppt/slides", t)).replace(os.sep, "/")
                pics.append((path, z.read(path)))
        out[int(m.group(1))] = pics
    return out


def pixels(data):
    from PIL import Image
    import io
    im = Image.open(io.BytesIO(data))
    im.load()
    return im.mode, im.size, im.convert("RGBA").tobytes()


def main(deck, rec_path, py):
    import PIL  # the pixel comparison needs Pillow: fail loudly instead of treating a re-encoded picture as stale
    rec = json.load(open(rec_path))
    bad, n, ran = [], 0, {}
    keepdirs = {}

    def rerun(pname):
        if pname not in ran:
            pr = rec["_programs"][pname]
            kd = tempfile.mkdtemp(prefix="ch25keep_")
            r = run_program(py, pr["code"], pr["inputs"], pr.get("needs", ()), keep=kd)
            ran[pname] = (r.returncode, r.stdout.rstrip("\n"))
            keepdirs[pname] = kd
        return ran[pname]

    for name, pr in rec["_programs"].items():
        if pr.get("exit", 0) != 0:
            bad.append(("recording", name, "the recorded program exited %r" % pr.get("exit")))
    pics = pictures(deck)
    PH = {x["file"]: x for x in json.load(open(os.path.join(HERE, "photos_v1_0_0.json")))["photos"]}
    n_img = n_byte = n_pix = n_pho = 0
    for idx, (name, paras) in enumerate(slides(deck), 1):
        flat = norm(" ".join(paras))
        for p in paras:
            t = TCAP.search(p)
            if t:
                n += 1
                pr = rec["_programs"].get(t.group(1))
                if pr is None:
                    bad.append((name, t.group(1), "no such program in the recording"))
                    continue
                code, got = rerun(t.group(1))
                if code or got != pr["transcript"]:
                    bad.append((name, t.group(1), "re-run (exit %d) prints %r, the recording says %r" % (code, got[:60], pr["transcript"][:60])))
                elif norm(pr["transcript"]) not in flat:
                    bad.append((name, t.group(1), "its transcript is not on the slide"))
                continue
            m = CAP.search(p)
            if not m:
                continue
            pname, a, b, total = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
            n += 1
            pr = rec["_programs"].get(pname)
            if pr is None:
                bad.append((name, pname, "no such program in the recording"))
                continue
            lines = pr["code"].rstrip("\n").split("\n")
            if len(lines) != total:
                bad.append((name, pname, "label says %d lines, the program has %d" % (total, len(lines))))
            if norm(" ".join(lines[a - 1:b])) not in flat:
                bad.append((name, pname, "lines %d-%d are not on the slide verbatim" % (a, b)))
            code, got = rerun(pname)
            if code or got != pr["transcript"]:
                bad.append((name, pname, "re-run (exit %d) prints %r, the recording says %r" % (code, got[:60], pr["transcript"][:60])))
            elif pr["transcript"].strip() and norm(pr["transcript"]) not in flat:
                bad.append((name, pname, "its transcript is not on the slide"))
        claimed = []
        for p in paras:
            for fn, pn in IMG.findall(p):
                n_img += 1
                info = rec["_images"].get(fn)
                if info is None or info["program"] != pn:
                    bad.append((name, fn, "the recording holds no picture %s made by %s" % (fn, pn)))
                    continue
                code, got = rerun(pn)
                fresh = os.path.join(keepdirs[pn], fn)
                if code or not os.path.exists(fresh):
                    bad.append((name, fn, "the program %s did not save %s when run again (exit %d)" % (pn, fn, code)))
                    continue
                want = open(fresh, "rb").read()
                if hashlib.sha256(want).hexdigest() != info["sha256"]:
                    bad.append((name, fn, "the picture saved now has SHA-256 %s, the recording says %s" % (hashlib.sha256(want).hexdigest()[:12], info["sha256"][:12])))
                    continue
                if hashlib.sha256(want).hexdigest()[:12] not in pr_transcript(rec, pn):
                    bad.append((name, fn, "the transcript of %s does not print the hash of %s" % (pn, fn)))
                match = None
                for path, blob in pics.get(idx, []):
                    if blob == want:
                        match = ("byte-identical", path)
                        break
                if match is None:
                    for path, blob in pics.get(idx, []):
                        try:
                            if pixels(blob) == pixels(want):
                                match = ("pixel-identical", path)
                                break
                        except Exception:
                            pass
                if match is None:
                    bad.append((name, fn, "no picture on the slide is byte- or pixel-identical to what %s saves now" % pn))
                else:
                    claimed.append(match[1])
                    n_byte += match[0] == "byte-identical"
                    n_pix += match[0] == "pixel-identical"
        for p in paras:
            m = PHO.match(p)
            if not m:
                continue
            fn, rest = m.group(1), m.group(2)
            n_img += 1
            n_pho += 1
            info = PH.get(fn)
            if info is None:
                bad.append((name, fn, "photos_v1_0_0.json holds no photograph %s" % fn))
                continue
            if not rest.startswith(info["credit"]):
                bad.append((name, fn, "the caption does not begin with the recorded credit %r (it says %r)" % (info["credit"], rest[:80])))
                continue
            want = open(os.path.join(HERE, "photos", fn), "rb").read()
            if hashlib.sha256(want).hexdigest() != info["sha256"]:
                bad.append((name, fn, "the file photos/%s no longer has the recorded SHA-256" % fn))
                continue
            match = None
            for path, blob in pics.get(idx, []):
                if blob == want:
                    match = ("byte-identical", path)
                    break
            if match is None:
                for path, blob in pics.get(idx, []):
                    try:
                        if pixels(blob) == pixels(want):
                            match = ("pixel-identical", path)
                            break
                    except Exception:
                        pass
            if match is None:
                bad.append((name, fn, "no picture on the slide is byte- or pixel-identical to photos/%s" % fn))
            else:
                claimed.append(match[1])
                n_byte += match[0] == "byte-identical"
                n_pix += match[0] == "pixel-identical"
        loose = [p for p, _ in pics.get(idx, []) if p not in claimed]
        if loose:
            bad.append((name, "picture", "%d picture(s) on the slide are named by no caption 'image <file> made by <program>' or 'photo <file>: <credit>'" % len(loose)))
    print("program_check %s: %d program panels verified (slice verbatim, re-run equal with exit 0, transcript on the slide); %d distinct program(s) re-run; "
          "%d picture(s) checked, %d of them photographs against photos/ (%d byte-identical, %d pixel-identical; the rest against what their programs save now); %d mismatch(es)"
          % (__version__, n, len(ran), n_img, n_pho, n_byte, n_pix, len(bad)))
    for x in bad:
        print("  REFUSED", x)
    return 1 if bad else 0


def pr_transcript(rec, pn):
    return rec["_programs"][pn]["transcript"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else sys.executable))
