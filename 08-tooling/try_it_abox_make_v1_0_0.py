#!/usr/bin/env python3
"""Makes the next A-box version of a chapter whose concept panels run the book's code (Lineage11, change request CR11_ConceptPanels).
Reads 08-tooling/chNN-page/try_it_chNN_v1_0_0.json ({concept id: {code, setup, book}}), runs each code after its set-up under the given
Python with the same runner as page data 2.30.0 (the set-up first, then the code, the value of the last line), and writes
03-materials/chNN/rdodi/sen0414_chNN_domain_abox_v<NEW>.ttl: the newest A-box with the I/O example line of each listed concept replaced
(input = the book's code, output = what the page's runner gives: what it prints, then the value of its last line); every other line is copied unchanged. Refuses to overwrite.
Usage: try_it_abox_make_v1_0_0.py NN OLD_VERSION NEW_VERSION /path/to/python   e.g. 10 1_0_1 1_0_2 /usr/bin/python3.13"""
__version__ = "1.0.0"
import json, os, re, subprocess, sys, glob
NN, OLD, NEW, PY = sys.argv[1:5]
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
pd = open(os.path.join(R, "08-tooling/sen0414_page_data_v2_30_0.py"), encoding="utf-8").read()
EXEC = pd.split("EXEC = r'''", 1)[1].split("'''", 1)[0]
data = json.load(open(os.path.join(R, "08-tooling/ch%s-page/try_it_ch%s_v1_0_0.json" % (NN, NN)), encoding="utf-8"))
src = os.path.join(R, "03-materials/ch%s/rdodi/sen0414_ch%s_domain_abox_v%s.ttl" % (NN, NN, OLD))
dst = os.path.join(R, "03-materials/ch%s/rdodi/sen0414_ch%s_domain_abox_v%s.ttl" % (NN, NN, NEW))
if os.path.exists(dst): sys.exit("refusing to overwrite " + dst)
def esc(t): return t.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
lines = open(src, encoding="utf-8").read().split("\n"); out = []; done = set()
for ln in lines:
    m = re.match(r"^chx:IO_(\w+) a owl:NamedIndividual, rd:IOExample ;", ln)
    if m and m.group(1) in data:
        k = m.group(1); d = data[k]
        args = [PY, "-c", EXEC, d["code"], d["setup"], "page"]
        r = json.loads(subprocess.run(args, capture_output=True, text=True, timeout=90).stdout)["out"]
        label = d["code"] + " evaluates to " + r
        ln = 'chx:IO_%s a owl:NamedIndividual, rd:IOExample ; rdfs:label "%s"@en ; chx:input "%s" ; chx:output "%s" .' % (k, esc(label), esc(d["code"]), esc(r)); done.add(k)
    elif ln.startswith("    rdfs:label") and "owl:versionInfo" in ln:
        ln = ln.replace('owl:versionInfo "%s"' % OLD.replace("_", "."), 'owl:versionInfo "%s"' % NEW.replace("_", ".")).replace("/%s>" % OLD.replace("_", "."), "/%s>" % NEW.replace("_", "."))
    elif "dcterms:identifier" in ln and "_abox_v" in ln:
        ln = ln.replace("_abox_v" + OLD, "_abox_v" + NEW)
    out.append(ln)
miss = set(data) - done
if miss: sys.exit("no I/O example line for: %s" % sorted(miss))
open(dst, "w", encoding="utf-8").write("\n".join(out)); print("wrote %s: %d I/O examples replaced" % (os.path.relpath(dst, R), len(done)))
