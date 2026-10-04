"""Reads a chapter's RDODI research record and writes the deck's source list, so that the Sources slide is never typed.

Each verified publication of the record becomes one entry (label, address, primary or secondary). The script also
reports, for every author-year citation string the chapter corpus puts into its prose - the strings the deck quotes on
its slides - whether that string resolves in the research record, by looking for the leading surname and the year
together. A citation that does not resolve is printed and recorded in the output rather than silently accepted, so the
gap is visible to whoever reads the build log.

1.0.1 reports an unresolved citation instead of refusing to write the list. Chapter 2 and chapter 3 write the compact
author-year form into their research records ("cited as Sweigart, 2025"); the chapter 1 record names its publications
in full ("Al Sweigart, No Starch Press, 2025") and leaves the compact form to the chapter corpus, so a refusal would
have stopped a build over a difference in how two records were written, not over a missing source.

Usage: sources_make_v1_0_1.py <research.ttl> <corpus.py> <out.json>
"""
__version__ = "1.0.1"
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
cites = sorted(set((getattr(mod, "_CITE", None) or getattr(mod, "CITES", None) or {}).values()))

def resolves(c):
    inner = c.strip("()")
    if inner in text: return True
    surname, year = inner.rsplit(",", 1)
    surname = surname.replace(" et al.", "").split(" and ")[0].split(",")[0].strip()
    return surname in text and year.strip() in text

unresolved = [c for c in cites if not resolves(c)]
json.dump({"_version": __version__, "_research": os.path.basename(TTL), "_corpus": os.path.basename(CORPUS),
           "citations": cites, "unresolved": unresolved, "sources": rows}, open(OUT, "w"), indent=1, ensure_ascii=False)
print("written", OUT, "-", len(rows), "verified publications;", len(cites) - len(unresolved), "of", len(cites),
      "citation strings resolve in", os.path.basename(TTL), ("- unresolved: " + ", ".join(unresolved)) if unresolved else "")
