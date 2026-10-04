"""Reads a chapter's RDODI research record and writes the deck's source list, so that the Sources slide is never typed.

Each verified publication of the record becomes one entry (label, address, primary or secondary). The script also
checks that every author-year citation string the chapter corpus puts into its prose - the strings the deck quotes on
its slides - is still present in the research record, and refuses to write the list if one is not, because a citation
that resolves to nothing is worse than no citation.

Usage: sources_make_v1_0_0.py <research.ttl> <corpus.py> <out.json>
"""
__version__ = "1.0.0"
import importlib.util, json, os, re, sys

TTL, CORPUS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(TTL).read()
rows = []
for m in re.finditer(r'a res:Publication ;\s*rdfs:label "(.*?)"@en ;\s*dcterms:source "(.*?)"\^\^xsd:anyURI ;\s*'
                     r'res:hasVerificationStatus res:(\w+)[^.]*?sourceRole "(\w+)"', text, re.S):
    label, url, status, role = m.group(1), m.group(2), m.group(3), m.group(4)
    assert status == "Status_Verified", (label, status)
    rows.append({"label": label, "url": url, "role": role})
assert rows, "no verified publication found in " + TTL

spec = importlib.util.spec_from_file_location("_corpus", os.path.abspath(CORPUS))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
cites = sorted(set((getattr(mod, "_CITE", None) or getattr(mod, "CITES", None) or {}).values())) or \
        sorted({c for n in mod.NODES for f, t in n[5] for c in re.findall(r"\((?:[A-Z][^()]*?), \d{4}\)", t)})
missing = [c for c in cites if c.strip("()") not in text and c not in text]
assert not missing, ("citation strings that do not resolve in the research record", missing)

json.dump({"_version": __version__, "_research": os.path.basename(TTL), "citations": cites, "sources": rows},
          open(OUT, "w"), indent=1, ensure_ascii=False)
print("written", OUT, "-", len(rows), "verified publications;", len(cites), "citation strings all resolve in", os.path.basename(TTL))
