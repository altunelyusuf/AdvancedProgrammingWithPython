#!/usr/bin/env python3
"""sen0414_lineage_restore_exclusions v1_0_0 - writes the next version of the SEN0414 slide lineage with the
two scope exclusions' rationales restored to the owner's original 2026-09-24 text.

Why: backlog-roadmap-framework ruled (response of 2026-10-12, v1.382.0, L-112) that a record of a past decision is
not edited to match a later one; the lift is recorded by the owner-decided ScopeChange, which v2.41.0 already
carries. The original text is read from the oldest lineage version on disk (v2_39_0), never retyped.
"""
__version__ = "1.0.0"
import glob, os, re, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIN = os.path.join(REPO, "07-lineage")
B = rdflib.Namespace("http://example.org/backlog#")
EX = rdflib.Namespace("http://example.org/sen0414-slides-lineage#")


def ver(p):
    return [int(v) for v in re.search(r"_v(\d+_\d+_\d+)\.ttl$", p).group(1).split("_")]


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


files = sorted(glob.glob(os.path.join(LIN, "sen0414_slides_lineage_v*.ttl")), key=ver)
old, src = files[0], files[-1]
cur = ".".join(map(str, ver(src)))
nxt = ".".join(map(str, [ver(src)[0], ver(src)[1] + 1, 0]))
out = os.path.join(LIN, "sen0414_slides_lineage_v%s.ttl" % nxt.replace(".", "_"))
if os.path.exists(out):
    sys.exit("refusing to overwrite " + out)
g0 = rdflib.Graph(); g0.parse(old)
gc = rdflib.Graph(); gc.parse(src)
t = open(src, encoding="utf-8").read()
for ex in ("Excl_CommandLine", "Excl_Untaught"):
    orig = str(g0.value(EX[ex], B.hasExclusionRationale))
    now = str(gc.value(EX[ex], B.hasExclusionRationale))
    assert orig != now, ex + " already original"
    lit = '"%s"' % esc(now)
    assert t.count("backlog:hasExclusionRationale " + lit) == 1, ex + " literal not found once"
    t = t.replace("backlog:hasExclusionRationale " + lit, "backlog:hasExclusionRationale " + '"%s"' % esc(orig))
base = "http://example.org/sen0414-slides-lineage"
t, n = re.subn(r'owl:versionInfo "%s" ; owl:versionIRI <[^>]*> ; owl:priorVersion <[^>]*> ;' % re.escape(cur),
               'owl:versionInfo "%s" ; owl:versionIRI <%s/%s> ; owl:priorVersion <%s/%s> ;' % (nxt, base, nxt, base, cur), t, count=1)
assert n == 1
c = ("%s (2026-10-12): the two scope exclusions' rationales are restored to the owner's original 2026-09-24 text, as backlog-roadmap-framework ruled "
     "(v1.382.0, L-112: a record of a past decision is not edited to match a later one). The lift of both is recorded by ex:SC_Chapters12_15to18_20to23, "
     "an Owner-decided ScopeChange, introduced in %s; the dated sentences that the 2.40.0 text had appended are gone from the exclusions and remain readable in 2.40.0 and 2.41.0." % (nxt, cur))
t = t.replace('dcterms:identifier "sen0414_slides_lineage" ;', 'dcterms:identifier "sen0414_slides_lineage" ;\n    rdfs:comment "%s"@en ;' % c.replace('"', "'"), 1)
rdflib.Graph().parse(data=t, format="turtle")
open(out, "w", encoding="utf-8").write(t)
print(os.path.basename(out), "written from", os.path.basename(src))
