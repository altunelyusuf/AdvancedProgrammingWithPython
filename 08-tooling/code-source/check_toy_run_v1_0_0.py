#!/usr/bin/env python3
"""Runs code_check 1.0.0 on a good toy (deck, page, manifest made from the toy source) and on broken copies, one per condition. Expects exit 0 on the good one and exit 2 naming the right condition on each broken one."""
import copy, json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(HERE)
from pptx import Presentation
from pptx.util import Inches
src = json.load(open(os.path.join(HERE, "toy_source_v1_0_0.json")))
W = tempfile.mkdtemp()

def make(srcd, tag, split=None, edit=None):
    subprocess.run([sys.executable, os.path.join(T, "code_source_make_v1_1_0.py"), srcd, os.path.join(W, tag)], check=True, capture_output=True)

def deck(path, boxes_for):
    p = Presentation(); lay = p.slide_layouts[6]
    for _ in range(min(e["slide"] for e in src["examples"]) - 1):
        p.slides.add_slide(lay)
    for e in src["examples"]:
        s = p.slides.add_slide(lay)
        for chunk in boxes_for(e):
            tb = s.shapes.add_textbox(Inches(0.5), Inches(1), Inches(5), Inches(1)); tf = tb.text_frame
            for i, l in enumerate(chunk):
                para = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); r = para.add_run(); r.text = l; r.font.name = "Courier New"
    p.save(path)

def page(path, man):
    open(path, "w", encoding="utf-8").write("<html><script>var DATA=" + json.dumps(man) + ";</script></html>")

def run(label, expect, *args, frag=""):
    r = subprocess.run([sys.executable, os.path.join(T, "code_check_v1_0_0.py"), *args], capture_output=True, text=True)
    last = r.stdout.strip().splitlines()
    ok = (r.returncode == 0) if expect is None else (r.returncode == 2 and any(("FAIL " + expect) in l and frag in l for l in last))
    print(("PASS" if ok else "WRONG"), label, "-> exit", r.returncode, "|", "; ".join(last))
    return ok

sp = os.path.join(W, "src.json"); json.dump(src, open(sp, "w"))
make(sp, "m"); man = json.load(open(os.path.join(W, "m", "examples_list_ch10.json")))
mp = os.path.join(W, "man.json"); json.dump(man, open(mp, "w"))
dg = os.path.join(W, "deck_good.pptx"); deck(dg, lambda e: [e["code"]])
pg = os.path.join(W, "page_good.html"); page(pg, man)
res = [run("good toy: manifest, deck, page, run", None, sp, "--manifest", mp, "--deck", dg, "--page", pg)]
ds = os.path.join(W, "deck_split.pptx"); deck(ds, lambda e: [e["code"][:1], e["code"][1:]])
res.append(run("broken: code split over two boxes", "C2", sp, "--manifest", mp, "--deck", ds, frag="2 code boxes"))
de = os.path.join(W, "deck_edit.pptx"); deck(de, lambda e: [[l.replace("print", "show") for l in e["code"]]])
res.append(run("broken: slide code differs from source", "C2", sp, "--manifest", mp, "--deck", de, frag="differs from the source code"))
m2 = copy.deepcopy(man); m2[1]["code"] += "\nx = 1"; m2p = os.path.join(W, "man2.json"); json.dump(m2, open(m2p, "w"))
res.append(run("broken: manifest differs from source", "C1", sp, "--manifest", m2p))
p2 = os.path.join(W, "page_bad.html"); page(p2, m2)
res.append(run("broken: page differs from source", "C3", sp, "--manifest", mp, "--page", p2))
s3 = copy.deepcopy(src); s3["examples"][2]["code"].append("raise ValueError('boom')"); s3p = os.path.join(W, "src3.json"); json.dump(s3, open(s3p, "w"))
m3 = copy.deepcopy(man); m3[2]["code"] = "\n".join(s3["examples"][2]["code"]); m3p = os.path.join(W, "man3.json"); json.dump(m3, open(m3p, "w"))
res.append(run("broken: an example does not run", "C4", s3p, "--manifest", m3p))
print("ALL AS EXPECTED" if all(res) else "SOME WRONG"); sys.exit(0 if all(res) else 1)
