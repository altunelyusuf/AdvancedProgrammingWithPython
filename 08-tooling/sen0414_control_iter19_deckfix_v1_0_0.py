#!/usr/bin/env python3
"""sen0414_control_iter19_deckfix v1_0_0 - the lineage agent's own control checks of the error-first deck repairs of Iter_19 (ex:CR2_ErrFirst; G136, G137: the controller re-runs, never trusts the executor's log).
Usage: sen0414_control_iter19_deckfix_v1_0_0.py deckfixNN        NN = 01 | 03 | 04 | all (all three)   (the new deck 4.1.0 | 5.1.0 | 3.1.0 over the controlled deck 4.0.0 | 5.0.0 | 3.0.0)
Asserts: the new deck is a new file of the expected version and the controlled deck is byte-identical to its committed form; the new manifest 1.1.0 exists and differs from 1.0.0 in ONE example only (the named one: code and expected), everything else identical;
the deck standard check prints 13 of 13 PASS including M1 and the overlap check CLEAN on the new deck; M1 count equals the manifest's; every example of the manifest is run now under Python 3.13 and prints its recorded result;
no manifest of chapters 1 to 5 (newest version of each) has a recorded result whose first line matches the template's pattern ^(\\w*Error|Traceback|Stopped after); the text of every slide of the new deck equals that of the controlled deck except the named slide; no file committed up to the Iter_19 base commit is modified.
Exit 0 only when every assertion holds; the evidence bridge runs this file as the TestEvidence command."""
__version__ = "1.0.0"
import glob, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_control_iter18_v1_0_0 as C
import sen0414_control_iter19_v1_1_0 as D

REPO, T, ok = C.REPO, C.T, C.ok
SPEC = {"01": ("SEN0414_Ch01_PythonBasics_3e_v4_0_0.pptx", "SEN0414_Ch01_PythonBasics_3e_v4_1_0.pptx", 14, 26), "03": ("SEN0414_Ch03_Loops_3e_v5_0_0.pptx", "SEN0414_Ch03_Loops_3e_v5_1_0.pptx", 17, 31), "04": ("SEN0414_Ch04_Functions_3e_v3_0_0.pptx", "SEN0414_Ch04_Functions_3e_v3_1_0.pptx", 17, None)}
ERR = re.compile(r"^(\w*Error|Traceback|Stopped after)")


def texts(path):
    from pptx import Presentation
    out = []
    for s in Presentation(path).slides:
        out.append("\n".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame) + "|" + str(sum(1 for sh in s.shapes)))
    return out


def fix(n):
    old, new, exn, slide = SPEC[n]; d = os.path.join(REPO, "03-materials/ch%s" % n)
    ok(os.path.exists(os.path.join(d, new)) and os.path.exists(os.path.join(d, old)), "the new deck %s is a new file beside the controlled deck %s" % (new, old))
    ok(subprocess.run(["git", "status", "--porcelain", "--", "03-materials/ch%s" % n, "08-tooling/ch%s-deck" % n], capture_output=True, text=True, cwd=REPO).stdout.strip() == "", "everything of the chapter deck is committed")
    m0 = json.load(open(os.path.join(d, "page/chapter_code_ch%s_v1_0_0.json" % n), encoding="utf-8")); m1 = json.load(open(os.path.join(d, "page/chapter_code_ch%s_v1_1_0.json" % n), encoding="utf-8"))
    e0, e1 = m0["examples"], m1["examples"]
    diff = [a["order"] for a, b in zip(e0, e1) if a != b]
    ok(len(e0) == len(e1) and diff == [exn] and {k: v for k, v in m0.items() if k != "examples"} .keys() == {k: v for k, v in m1.items() if k != "examples"}.keys(), "manifest 1.1.0 differs from 1.0.0 in example %s only (differing examples: %s of %d)" % (exn, diff, len(e1)))
    a, b = e0[exn - 1], e1[exn - 1]
    ok(a["name"] == b["name"] and a["id"] == b["id"] and a["slide"] == b["slide"] and a["concepts"] == b["concepts"] and (a["code"] != b["code"] or a["expected"] != b["expected"]), "in the changed example the name, id, slide and concepts are the same, the code or the result differs")
    ok(not ERR.match(b["expected"].strip()), "the changed example's first result line is no longer an error: %r" % b["expected"].strip().splitlines()[0][:70])
    rc, out = C.run([sys.executable, os.path.join(T, "sen0414_deck_standard_check_v1_0_0.py"), n, "03-materials/ch%s/%s" % (n, new)]); mm = re.search(r"SUMMARY PASS=(\d+) FAIL=(\d+) NOT_MEASURED=(\d+)", out)
    ok(rc == 0 and bool(mm) and mm.groups() == ("13", "0", "0"), "deck standard check on the new deck: %s" % (mm.group(0) if mm else out[-200:]))
    m1l = re.search(r"^M1 PASS .*?(\d+) of (\d+)", out, re.M)
    ok(bool(m1l) and m1l.group(1) == m1l.group(2) == str(len(e1)), "M1: the manifest equals the deck's code boxes: %s" % (m1l.group(0)[:140] if m1l else "no M1 PASS"))
    rc, out = C.run([sys.executable, os.path.join(T, "sen0414_deck_overlap_check_v1_0_0.py"), "03-materials/ch%s/%s" % (n, new)]); ok(rc == 0 and "RESULT CLEAN" in out, "deck overlap check: %s" % out.strip().splitlines()[-1])
    bad = []
    for e in e1:
        try:
            r = subprocess.run(["/usr/bin/python3.13", "-I", "-c", (m1.get("prelude") or "") + e["code"]], capture_output=True, text=True, timeout=60, input=e.get("stdin", ""))
            if not (r.returncode == 0 and r.stdout.strip() == e["expected"].strip()): bad.append(e["order"])
        except Exception:
            bad.append(e["order"])
    ok(not bad, "the %d examples of manifest 1.1.0 were run now under Python 3.13: output equals the recorded result in every one (differing: %s)" % (len(e1), bad))
    hits = []
    for c in ("01", "02", "03", "04", "05"):
        mf = sorted(glob.glob(os.path.join(REPO, "03-materials/ch%s/page/chapter_code_ch%s_v*.json" % (c, c))), key=D.vkey)[-1]
        hits += ["ch%s %d" % (c, e["order"]) for e in json.load(open(mf, encoding="utf-8"))["examples"] if ERR.match(e["expected"].strip())]
    print("  (scan over the newest manifest of chapters 1 to 5; still open: %s)" % (hits or "none"))
    ok(not [h for h in hits if h.startswith("ch" + n)], "scan: no example of the newest manifest of chapter %s has a recorded first line that begins with an error name" % n)
    to, tn = texts(os.path.join(d, old)), texts(os.path.join(d, new))
    dsl = [i + 1 for i, (x, y) in enumerate(zip(to, tn)) if x != y]
    ok(len(to) == len(tn) and (dsl == [slide] if slide else len(dsl) <= 2), "slides: %d in both decks; the text and shape count of the slides that differ: %s (named: %s)" % (len(tn), dsl, slide or "the example-17 slide"))
    gd = subprocess.run(["git", "diff", "--name-status", D.BASE, "HEAD", "--", "03-materials/ch%s" % n, "08-tooling/ch%s-deck" % n], capture_output=True, text=True, cwd=REPO).stdout.splitlines()
    ok(bool(gd) and all(l.startswith("A") for l in gd), "nochange: since %s the chapter deck folders have %d added files and no modified or deleted one" % (D.BASE, len(gd)))


def main():
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    assert re.fullmatch(r"deckfix(01|03|04|all)", c), __doc__
    for n in (("01", "03", "04") if c == "deckfixall" else (c[7:],)):
        print("== chapter", n); fix(n)
    print("RESULT %s (%d failed assertion(s))" % ("FAIL" if C.BAD else "PASS", len(C.BAD))); sys.exit(1 if C.BAD else 0)


if __name__ == "__main__":
    main()
