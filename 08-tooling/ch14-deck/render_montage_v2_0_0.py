#!/usr/bin/env python3
"""Renders a deck to pictures for the builder's own look at it (LibreOffice to PDF, pdftoppm to PNG, four slides per contact sheet). Not a check of the standard.
Usage: python3 render_montage_v2_0_0.py DECK.pptx OUTDIR [DPI]   writes OUTDIR/s-NN.png and OUTDIR/mNN.png"""
__version__ = "2.0.0"
import glob, os, subprocess, sys
from PIL import Image
deck, out = sys.argv[1], sys.argv[2]; dpi = sys.argv[3] if len(sys.argv) > 3 else "80"
os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(out, "*.png")) + glob.glob(os.path.join(out, "*.pdf")):
    os.remove(f)
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", out, deck], capture_output=True, timeout=600)
pdf = os.path.join(out, os.path.splitext(os.path.basename(deck))[0] + ".pdf")
subprocess.run(["pdftoppm", "-r", dpi, "-png", pdf, os.path.join(out, "s")], check=True)
fs = sorted(glob.glob(os.path.join(out, "s-*.png")))
for k in range(0, len(fs), 4):
    ims = [Image.open(f) for f in fs[k:k + 4]]
    w, h = ims[0].size
    m = Image.new("RGB", (w * 2, h * 2), "white")
    for i, im in enumerate(ims):
        m.paste(im, ((i % 2) * w, (i // 2) * h))
    m.save(os.path.join(out, "m%02d.png" % (k // 4 + 1)))
print(len(fs), "slides")
