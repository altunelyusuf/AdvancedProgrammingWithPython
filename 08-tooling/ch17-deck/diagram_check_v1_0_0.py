#!/usr/bin/env python3
"""Chapter 17 diagram check: the narrative diagrams on the finished slides are the grounded diagrams of
sen0414_ch17_diagrams_v1_0_0.py, and nothing else.
  1. The diagrams module's own checks pass on the chapter's nodes (read from the v1_0_1 RDODI document and ABox): structural
     rules, and grounding >= 0.84 for each diagram.
  2. Every diagram of the module is on exactly one slide, named by a caption 'diagram <id> - <pattern> pattern, <h> of <n>
     words grounded in the chapter's text'; the pattern, h and n must equal the module's, as measured now.
  3. Every label of the diagram (node, flow, state, transition, participant, message, actor, use case, root, branch, child) must
     be a paragraph of that slide, verbatim, as many times as the diagram holds it.
Usage: diagram_check_v1_0_0.py <deck.pptx>   (needs rdflib)   Exit 0 when nothing mismatches."""
__version__ = "1.0.0"
import collections
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from deck_check_v1_0_0 import slides

spec = importlib.util.spec_from_file_location("diagrams17", os.path.join(HERE, "..", "sen0414_ch17_diagrams_v1_0_0.py"))
DG = importlib.util.module_from_spec(spec)
spec.loader.exec_module(DG)
CAPRE = re.compile(r"^diagram ([A-Za-z]+) - (\w+) pattern, (\d+) of (\d+) words grounded")
norm = lambda t: re.sub(r"\s+", " ", t).strip()


def main(deck):
    nodes = DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))
    bad = list(DG.run_checks(nodes))
    by = {d["id"]: d for d in DG.DIAGRAMS}
    seen, nlabels = {}, 0
    for name, paras in slides(deck):
        plain = collections.Counter(norm(p) for p in paras)
        for p in paras:
            m = CAPRE.match(p)
            if not m:
                continue
            did = m.group(1)
            d = by.get(did)
            if d is None:
                bad.append((name, did, "not a diagram of the chapter"))
                continue
            if did in seen:
                bad.append((name, did, "drawn twice, also on %s" % seen[did]))
            seen[did] = name
            if (m.group(2), int(m.group(3)), int(m.group(4))) != (d["pattern"], d["grounding"][0], d["grounding"][1]):
                bad.append((name, did, "caption says %s %s of %s, the module measures %s %s of %s" %
                            (m.group(2), m.group(3), m.group(4), d["pattern"], d["grounding"][0], d["grounding"][1])))
            need = collections.Counter(norm(x) for x in DG._labels(d))
            for lab, k in need.items():
                nlabels += k
                if plain[lab] < k:
                    bad.append((name, did, "label %r is on the slide %d time(s), the diagram holds it %d time(s)" % (lab, plain[lab], k)))
    for did in by:
        if did not in seen:
            bad.append(("deck", did, "diagram is on no slide"))
    print("diagram_check %s: %d diagrams of the module, %d on slides, %d labels found verbatim, grounding %s; %d mismatch(es)"
          % (__version__, len(by), len(seen), nlabels,
             ", ".join("%s %d/%d" % (k, v["grounding"][0], v["grounding"][1]) for k, v in by.items()), len(bad)))
    for b in bad:
        print("  REFUSED", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
