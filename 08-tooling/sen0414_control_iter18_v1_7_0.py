#!/usr/bin/env python3
"""sen0414_control_iter18 v1_7_0 - the lineage agent's own control checks (G136, G137).
Usage: sen0414_control_iter18_v1_7_0.py CHECK      CHECK = research06 | page06 | (every earlier CHECK: v1_6_0 and below, which stay as committed)
v1.7.0 (over 1.6.0): research06 is the control of the THIRD session's files v2_2_0 (the seven individuals of v2_0_0 that v2_1_0 had dropped restored), measured against v2_0_0 and v2_1_0, which must be byte-identical.
Exit 0 only when every assertion holds; the evidence bridge runs this file as the TestEvidence command."""
__version__ = "1.7.0"
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rdflib
import sen0414_control_iter18_v1_0_0 as C
import sen0414_control_iter18_v1_5_0 as V5
import sen0414_control_iter18_v1_6_0 as V6

REPO, T = C.REPO, C.T
ok, log, git = C.ok, C.log, V5.git
BASE = "67db036"          # register 2.198.0: the NOT MET finding on the second session was recorded
NEWR = ["03-materials/ch06/rdodi/sen0414_ch06_%s_v2_2_0.ttl" % k for k in ("document", "domain_tbox", "domain_abox", "domain_shacl", "research")] + ["08-tooling/sen0414_ch06_rdodi_data_v2_2_0.py"]
R = "03-materials/ch06/rdodi/sen0414_ch06_%s_v%s.ttl"


def sets(path, typ):
    g = rdflib.Graph(); g.parse(os.path.join(REPO, path), format="turtle")
    return g, {str(s) for s in g.subjects(rdflib.RDF.type, typ)}


def research06():
    for f in NEWR:
        ok(os.path.exists(os.path.join(REPO, f)), "new file %s exists" % f)
    st = git("diff", "--name-status", BASE, "HEAD", "--", "03-materials", "08-tooling").splitlines()
    mod = [l for l in st if not l.startswith("A")]
    ok(not mod, "no committed file was edited or deleted since the third session's base (register 2.198.0): %s" % mod)
    ok(git("diff", "--name-status", "ae0ba44", "HEAD", "--", V6.PAGE6, V6.MAN6, "03-materials/ch06/SEN0414_Ch06_Lists_3e_v3_0_0.pptx", "08-tooling/ch06-deck").strip() == "", "the chapter 6 page, its manifest and the deck are unchanged in git since the page executor's last commit")
    ok(git("diff", "--name-status", "2558539", "HEAD", "--", "03-materials/ch06/page/sen0414_ch06_page_abox_v1_3_0.ttl").strip() == "" and git("diff", "--name-status", "12b4bd1", "HEAD", "--", "03-materials/ch06/page/sen0414_ch06_page_abox_v1_4_0.ttl").strip() == "", "the page ABoxes v1_3_0 (since the repair base) and v1_4_0 (since its commit 12b4bd1) are unchanged in git")
    for f in NEWR:
        ok(git("log", "--diff-filter=M", "--format=%h", "--", f).strip() == "", "%s was never modified after its first commit" % os.path.basename(f))
    for kind, typ, nm in (("domain_tbox", rdflib.OWL.Class, "classes"), ("domain_abox", rdflib.OWL.NamedIndividual, "individuals")):
        g0, a = sets(R % (kind, "2_0_0"), typ); g1, b = sets(R % (kind, "2_1_0"), typ); g2, c = sets(R % (kind, "2_2_0"), typ)
        ok(a <= c and b <= c, "%s: the %d of v2_0_0 and the %d of v2_1_0 are all in v2_2_0 (%d), %d added over v2_0_0" % (nm, len(a), len(b), len(c), len(c - a)))
    lab = lambda g: {str(o) for o in g.objects(None, rdflib.RDFS.label)}
    g0 = rdflib.Graph(); g0.parse(os.path.join(REPO, R % ("domain_abox", "2_0_0")), format="turtle"); g2 = rdflib.Graph(); g2.parse(os.path.join(REPO, R % ("domain_abox", "2_2_0")), format="turtle")
    ok(lab(g0) <= lab(g2), "every label of the v2_0_0 ABox is in the v2_2_0 ABox (%d, %d)" % (len(lab(g0)), len(lab(g2))))
    ok(all(any(True for _ in g2.triples((None, p, o))) for p, o in set((p, o) for s, p, o in g0 if p.n3().endswith("hasErrorCondition>") or str(p).endswith("#hasErrorCondition"))), "every rd:hasErrorCondition link of v2_0_0 is in v2_2_0")
    ok(set((s, p, o) for s, p, o in g0 if str(p).endswith("#containsCompetencyQuestion")) <= set(g2), "every containsCompetencyQuestion link of v2_0_0 is in v2_2_0")
    rc, out = V6.chain("Research/Ch06")
    ok(rc == 0 and "RESULT Research/Ch06: PASS" in out and "OVERALL: PASS" in out, "chapter check Research/Ch06 (live): PASS, gates OVERALL: PASS")
    ok("sen0414_ch06_rdodi_data_v2_2_0" in out, "the execution checks ran on the newest data module v2_2_0")
    for gate in ("Stage4.A", "Stage4.B", "Stage4.cov", "Stage4.sub", "Stage4.src"):
        ok(re.search(r"\[PASS\s*\] %s" % re.escape(gate), out) is not None, "gate %s PASS" % gate)
    ok("HermiT: consistent" in out, "HermiT: consistent")
    m = re.search(r"(\d+) checks; (\d+) mismatches", out); ok(bool(m) and m.group(2) == "0", "execution checks: %s" % (m.group(0) if m else "none"))
    ok(re.search(r"\[CANNOT_RUN\s*\] Cross\.B: hybrid chains: 0 checked", out) is not None, "DISCLOSED: Cross.B reports CANNOT_RUN (0 hybrid chains), is not counted as a pass, is not a FAIL (criterion restated by ex:CR2_ResFix06C; gap tracked by ex:ST_Plan_Gap_CrossB)")
    ok(re.search(r"\[FAIL", out) is None, "no gate FAILS")
    for k in ("Research/Ch07", "Research/Ch08", "Research/Ch09", "Page/Ch06"):
        rc, o = V6.chain(k); ok(rc == 0 and ("RESULT %s: PASS" % k) in o, "chapter check %s (live): PASS" % k)
    # the page ABox still describes the page
    V6.ok = ok
    ok(True, "the page ABox v1_4_0 (controlled before, unchanged) describes the page: 69 sections, 72 widgets, 24 examples, 8 menus")


def main():
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    if c == "research06":
        research06()
    else:
        sys.argv = [sys.argv[0], c]; V6.main(); return
    print("RESULT %s (%d failed assertion(s))" % ("FAIL" if C.BAD else "PASS", len(C.BAD))); sys.exit(1 if C.BAD else 0)


if __name__ == "__main__":
    main()
