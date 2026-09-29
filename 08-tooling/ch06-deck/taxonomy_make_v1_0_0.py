"""Reads the chapter 6 taxonomy from the research, not from memory: the class tree and its human labels come from the domain TBox
(03-materials/ch06/rdodi/sen0414_ch06_domain_tbox_v1_0_0.ttl), the leaf definitions and exemplars from the research data file
(08-tooling/sen0414_ch06_rdodi_data_v1_0_0.py). The two must agree on every leaf's parent and top, or the script stops.
Usage: taxonomy_make_v1_0_0.py <out.json>"""
__version__ = "1.0.0"
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, ".."))
import sen0414_ch06_rdodi_data_v1_0_0 as R
TBOX = os.path.join(ROOT, "03-materials", "ch06", "rdodi", "sen0414_ch06_domain_tbox_v1_0_0.ttl")
label = {}; parent = {}
for ln in open(TBOX, encoding="utf-8"):
    m = re.match(r'chx:(\w+) a owl:Class ; rdfs:label "([^"]+)"@en(?: ; rdfs:subClassOf chx:(\w+))?', ln)
    if m:
        label[m.group(1)] = m.group(2)
        if m.group(3): parent[m.group(1)] = m.group(3)
tops = [c for c in label if c not in parent]
level = lambda c: 1 if c not in parent else 1 + level(parent[c])
order = [t for t in dict.fromkeys(x[0] for x in R.TAX)]      # the order the research lists them in
nodes = []
for top in order:
    nodes.append({"id": top, "label": label[top], "level": 1, "parent": None, "body": R.BODY[top]})
    for mid in dict.fromkeys(x[1] for x in R.TAX if x[0] == top):
        assert parent[mid] == top, (mid, parent[mid], top)
        nodes.append({"id": mid, "label": label[mid], "level": 2, "parent": top, "body": R.BODY[mid]})
        for t in R.TAX:
            if t[0] == top and t[1] == mid:
                assert parent[t[2]] == mid and level(t[2]) == 3, t[2]
                nodes.append({"id": t[2], "label": label[t[2]], "level": 3, "parent": mid, "body": R.BODY[t[2]], "example": t[3], "definition": t[4]})
assert sorted(tops) == sorted(order), (tops, order)
n1, n2, n3 = [sum(1 for n in nodes if n["level"] == k) for k in (1, 2, 3)]
assert (n1, n3) == (6, 38), (n1, n2, n3)
json.dump({"_version": __version__, "_source": "domain TBox labels and hierarchy; research data TAX, BODY", "nodes": nodes}, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
print("written", sys.argv[1], "-", n1, "top subjects,", n2, "middle groups,", n3, "leaves")
