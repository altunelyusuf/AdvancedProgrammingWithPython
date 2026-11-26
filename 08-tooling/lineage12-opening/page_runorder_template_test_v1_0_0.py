#!/usr/bin/env python3
"""Lineage12 story ST12_Template_RunOrder, task 3: does a page made from a template carry the run-in-order menu item in its description?
For each template version: read the menu (VIEWS) exactly as sen0414_page_abox_build reads it, write the menu items the builder writes for it
(label '<item> menu item', part of pg:GroupedTopBar), add them to the newest chapter 12 page A-box without its own menu items, and run
PageRunInOrderMenuShape (03-materials/sen0414_page_shapes_v1_0_0.ttl). Also run the builder's own sentence logic for the item.
Usage: python3 page_runorder_template_test_v1_0_0.py"""
import re, glob, sys, os
from rdflib import Graph
import pyshacl
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
S = Graph(); S.parse(os.path.join(R, "03-materials", "sen0414_page_shapes_v1_0_0.ttl"), format="turtle")
fs = sorted(glob.glob(os.path.join(R, "03-materials", "ch12", "page", "sen0414_ch12_page_abox_v*.ttl")), key=lambda p: [int(x) for x in re.findall(r"v(\d+)_(\d+)_(\d+)", p)[-1]])
base = fs[-1]
txt = open(base, encoding="utf-8").read()
# drop the page's own pg:Menu_* individuals so only the template's menu is tested
blocks = re.split(r"\n(?=pg:)", txt)
kept = [b for b in blocks if not re.match(r"pg:Menu_\w+ ", b)]
rest = "\n".join(kept)
print("base A-box:", os.path.basename(base), "menu individuals removed:", len(blocks) - len(kept))
ok_all = True
for tv in ("9_54_1", "9_55_0"):
    html = open(os.path.join(R, "08-tooling", "course_page_template_v%s.html" % tv), encoding="utf-8").read()
    views = re.search(r"const VIEWS=\[(.*?)\];", html).group(1)
    V = [(k, re.sub(r"^[^A-Za-z]+", "", l)) for k, l in re.findall(r"\['(\w+)','([^']*)'\]", views)]
    ttl = "".join('pg:Menu_%s a ipo:Menu ; rdfs:label "%s menu item" ; dcterms:isPartOf pg:GroupedTopBar .\n' % (k, l) for k, l in V)
    d = Graph(); d.parse(data=rest + "\n" + ttl, format="turtle")
    conforms, _, rep = pyshacl.validate(d, shacl_graph=S, advanced=True, inference="none")
    print("template %s: menu = %s -> PageRunInOrderMenuShape conforms=%s" % (tv, [l for k, l in V], conforms))
    if tv == "9_55_0": ok_all = conforms
    else: ok_all = ok_all and (not conforms)
print("RESULT", "PASS (old template fails, new template conforms)" if ok_all else "FAIL")
sys.exit(0 if ok_all else 1)
