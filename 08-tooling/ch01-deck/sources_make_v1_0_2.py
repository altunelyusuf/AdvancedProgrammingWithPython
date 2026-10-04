"""Reads a chapter's RDODI research record and writes the deck's source list, so that the Sources slide is never typed.

Each verified publication of the record becomes one entry (label, address, primary or secondary). The script also
reports, for every author-year citation string that actually appears in the chapter corpus's prose - the strings the
deck quotes on its slides - whether it resolves in the research record, by looking for the leading surname and the year
together. An unresolved citation is printed and recorded in the output rather than silently accepted, so the gap is
visible to whoever reads the build log.

1.0.2 collects the citation strings from the corpus prose itself rather than from a citation table, because chapter 2
and chapter 3 hold their table in a dictionary while chapter 1 holds it in plain module variables; the prose is what
the slides quote, so the prose is the right place to read them from.
1.0.1 reported an unresolved citation instead of refusing to write the list: chapter 2 and chapter 3 write the compact
author-year form into their research records ("cited as Sweigart, 2025"), while the chapter 1 record names its
publications in full ("Al Sweigart, No Starch Press, 2025") and leaves the compact form to the chapter corpus.

Usage: sources_make_v1_0_2.py <research.ttl> <corpus.py> <out.json>
"""
__version__ = "1.0.2"
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
cites = sorted({c for n in mod.NODES for f, t in n[5] for c in re.findall(r"\([A-Z][A-Za-z.' ]*?(?: et al\.| and [A-Za-z ]+)?, \d{4}\)", t)})
assert cites, "no author-year citation string found in the prose of " + CORPUS

def resolves(c):
    inner = c.strip("()")
    if inner in text: return True
    surname, year = inner.rsplit(",", 1)
    surname = surname.replace(" et al.", "").split(" and ")[0].strip()
    return surname in text and year.strip() in text

unresolved = [c for c in cites if not resolves(c)]
json.dump({"_version": __version__, "_research": os.path.basename(TTL), "_corpus": os.path.basename(CORPUS),
           "citations": cites, "unresolved": unresolved, "sources": rows}, open(OUT, "w"), indent=1, ensure_ascii=False)
print("written", OUT, "-", len(rows), "verified publications;", len(cites) - len(unresolved), "of", len(cites),
      "citation strings resolve in", os.path.basename(TTL), ("- UNRESOLVED: " + ", ".join(unresolved)) if unresolved else "")
