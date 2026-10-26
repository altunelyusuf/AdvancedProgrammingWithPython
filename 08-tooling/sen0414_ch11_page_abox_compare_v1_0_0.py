#!/usr/bin/env python3
"""Chapter 11 has no OLD page ABox, so there is nothing to subtract. This compares the NEW page ABox (v9_96_0) with the things it must describe: the
page data (sections), the chapter-code manifest (examples), the widgets tested by page test 9.37.0, the domain ABox of the research (concepts) and the
quiz and objectives; and lists what each lacks. No file is written. Usage: sen0414_ch11_page_abox_compare_v1_0_0.py"""
import json, os, re, rdflib
from rdflib import RDF, RDFS
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = os.path.join(REPO, "03-materials", "ch11"); T = os.path.join(REPO, "08-tooling", "ch11-page")
g = rdflib.Graph().parse(os.path.join(P, "page", "sen0414_ch11_page_abox_v9_96_0.ttl"))
dom = rdflib.Graph().parse(os.path.join(P, "rdodi", "sen0414_ch11_domain_abox_v1_0_0.ttl"))
names = {str(s).rsplit("#", 1)[-1].rsplit("/", 1)[-1] for s in g.subjects(RDF.type, None)}
labels = {str(o).lower() for o in g.objects(None, RDFS.label)}
pd = json.load(open(os.path.join(T, "page_data_v9_96_0.json"), encoding="utf-8"))
man = json.load(open(os.path.join(P, "page", "chapter_code_ch11_v1_0_0.json"), encoding="utf-8"))
tr = json.load(open(os.path.join(T, "test_results_v9_96_0.json"), encoding="utf-8"))
nodes = pd.get("nodes", []); ids = [n.get("id") for n in nodes if isinstance(n, dict)]
print("page-data nodes:", len(ids), "| in page ABox:", sum(i in names for i in ids), "| missing:", [i for i in ids if i not in names][:30])
ex = man.get("examples", [])
exl = [e.get("title", "") if isinstance(e, dict) else str(e) for e in ex]
print("manifest examples:", len(ex), "| titles in page ABox labels:", sum(any(t.lower()[:30] in l for l in labels) for t in exl), "| missing:", [t for t in exl if not any(t.lower()[:30] in l for l in labels)])
dl = {str(s).rsplit("#", 1)[-1]: [str(x) for x in dom.objects(s, RDFS.label)] for s in dom.subjects(RDF.type, None)}
cn = [k for k in dl if k in names]
print("domain-ABox individuals:", len(dl), "| same name in page ABox:", len(cn))
dlab = {l.lower() for v in dl.values() for l in v}
print("domain labels:", len(dlab), "| found among page ABox labels:", len(dlab & labels), "| not found (first 25):", sorted(dlab - labels)[:25])
w = tr.get("widgets", {})
print("tested widgets in test results:", len(w), "| passed:", sum(1 for x in w.values() if x.get("passed") is True))
defs = " ".join(str(o).lower() for o in g.objects(None, rdflib.namespace.SKOS.definition))
ex_in = sum(1 for v in dl.values() for l in v if l.split(" evaluates to")[0].lower() in defs)
print("domain ABox expressions (label before 'evaluates to') found in page ABox definitions:", ex_in, "of", len(dl))
