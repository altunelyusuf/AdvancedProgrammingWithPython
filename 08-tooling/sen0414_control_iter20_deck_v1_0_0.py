#!/usr/bin/env python3
"""sen0414_control_iter20_deck v1_0_0 (a NEW file over sen0414_control_iter19_v1_1_0.py, which stays as committed; chapters 10 to 25: the earlier deck is the newest in 08-tooling/chNN-deck; the base is the register commit that planned Iter_20) - the lineage agent's own control checks of the Iter_19 executor results (G136, G137: the controller re-runs, never trusts the executor's log).
Usage: sen0414_control_iter19_v1_0_0.py CHECK      CHECK = deck01 | deck02 | deck03 | deck04 | deck05
deckNN controls the NEW deck of chapter NN of the retrofit: the newest deck of the chapter is a new file over the earlier newest deck (name above it), the deck standard check v1_0_0 prints 13 of 13 PASS (including M1), the overlap check v1_0_0 prints CLEAN, the manifest equals the deck's code boxes (M1) and its number of examples is the one the check counts,
every example of the manifest is run now under Python 3.13 and prints the recorded result, no file committed before the base commit of Iter_19 is modified by any later commit (only additions), the story pictures and their provenance record are in the repository, and every story slide names who, what, when, where, why and how (D5 of the check).
v1.1.0 (over 1.0.0, which stays as committed and ran for the decks of chapters 1 to 3): the story-picture assertion counts the pictures of the story slides (photo_* and logo_* assets; a story may be told with the Python logo, as the chapter 2 and chapter 4 decks do) against the number of story slides the deck check reports (D5), instead of three photographs; the chapter 4 deck, whose three stories use two photographs and a logo, failed the first form of the assertion.
Exit 0 only when every assertion holds; the evidence bridge runs this file as the TestEvidence command."""
__version__ = "1.0.0"
import glob, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_control_iter18_v1_0_0 as C

REPO, T = C.REPO, C.T
ok = C.ok
BASE = "a83369e"        # the register commit that planned Iter_20: every file committed up to it must stay byte-identical
OLD_NEWEST = lambda n: os.path.basename(sorted(glob.glob(os.path.join(REPO, "08-tooling/ch%s-deck/*.pptx" % n)), key=lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.pptx$", p).groups()])[-1])


def vkey(p):
    return [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.[a-z]+$", p).groups()]


def deck(n):
    decks = sorted(glob.glob(os.path.join(REPO, "03-materials/ch%s/SEN0414_Ch%s_*.pptx" % (n, n))), key=vkey)
    d = decks[-1]; rel = os.path.relpath(d, REPO)
    ok(os.path.basename(d) != OLD_NEWEST(n) and vkey(d) > vkey(OLD_NEWEST(n)), "the newest deck %s is a NEW file with a version above the earlier newest %s" % (os.path.basename(d), OLD_NEWEST(n)))
    mfs = sorted(glob.glob(os.path.join(REPO, "03-materials/ch%s/page/chapter_code_ch%s_v*.json" % (n, n))), key=vkey)
    ok(bool(mfs), "the chapter-code manifest exists: %s" % (os.path.relpath(mfs[-1], REPO) if mfs else "none"))
    if not mfs:
        print("RESULT FAIL (no manifest)"); sys.exit(1)
    mf = json.load(open(mfs[-1], encoding="utf-8")); ex = mf["examples"]
    rc, out = C.run([sys.executable, os.path.join(T, "sen0414_deck_standard_check_v1_0_0.py"), n, rel]); out_std = out; m = re.search(r"SUMMARY PASS=(\d+) FAIL=(\d+) NOT_MEASURED=(\d+)", out)
    ok(rc == 0 and bool(m) and m.groups() == ("13", "0", "0"), "deck standard check on %s: %s" % (os.path.basename(d), m.group(0) if m else out[-200:]))
    m1 = re.search(r"^M1 PASS .*?(\d+) of (\d+)", out, re.M)
    ok(bool(m1) and m1.group(1) == m1.group(2) == str(len(ex)), "M1: the chapter-code manifest equals the deck's code boxes (text, order): %s" % (m1.group(0)[:160] if m1 else "no M1 PASS line"))
    rc, out = C.run([sys.executable, os.path.join(T, "sen0414_deck_overlap_check_v1_0_0.py"), rel]); ok(rc == 0 and "RESULT CLEAN" in out, "deck overlap check: %s" % out.strip().splitlines()[-1])
    bad = []
    for e in ex:
        try:
            r = subprocess.run(["/usr/bin/python3.13", "-I", "-c", (mf.get("prelude") or "") + e["code"]], capture_output=True, text=True, timeout=60, input=e.get("stdin", ""))
            if not (r.returncode == 0 and r.stdout.strip() == e["expected"].strip()):
                bad.append(e["order"])
        except Exception:
            bad.append(e["order"])
    ok(len(ex) > 0 and not bad, "the manifest's %d examples were run now under Python %s: the output equals the recorded result in every one (differing: %s)" % (len(ex), subprocess.run(["/usr/bin/python3.13", "--version"], capture_output=True, text=True).stdout.strip(), bad))
    diff = subprocess.run(["git", "diff", "--name-status", BASE, "HEAD", "--", "03-materials/ch%s" % n, "08-tooling/ch%s-deck" % n, "08-tooling/ch%s-page" % n], capture_output=True, text=True, cwd=REPO).stdout.splitlines()
    ok(bool(diff) and all(l.startswith("A") for l in diff), "nochange: since the register commit %s the chapter folders have %d added files and no modified or deleted one (statuses: %s)" % (BASE, len(diff), sorted({l[0] for l in diff})))
    untracked = subprocess.run(["git", "status", "--porcelain", "--", "03-materials/ch%s" % n, "08-tooling/ch%s-deck" % n], capture_output=True, text=True, cwd=REPO).stdout.strip()
    ok(untracked == "", "everything of the chapter is committed (uncommitted: %s)" % (untracked.replace("\n", "; ")[:200] or "none"))
    prov = glob.glob(os.path.join(REPO, "03-materials/ch%s/assets/ASSETS_PROVENANCE_v*.md" % n)); pics = glob.glob(os.path.join(REPO, "03-materials/ch%s/assets/photo_*" % n)) + glob.glob(os.path.join(REPO, "03-materials/ch%s/assets/logo_*" % n))
    d5 = re.search(r"^D5 PASS .*?(\d+) of (\d+) story slides complete", out_std, re.M)
    ok(bool(d5) and d5.group(1) == d5.group(2) and bool(prov) and len(pics) >= int(d5.group(2)), "the story pictures (%d files: photographs and logos) cover the %s story slides of the deck and a provenance record (%s) is in the repository" % (len(pics), d5.group(2) if d5 else "?", os.path.basename(sorted(prov)[-1]) if prov else "none"))


def main():
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    assert re.fullmatch(r"deck(1[0-9]|2[0-5])", c), __doc__
    deck(c[4:])
    print("RESULT %s (%d failed assertion(s))" % ("FAIL" if C.BAD else "PASS", len(C.BAD))); sys.exit(1 if C.BAD else 0)


if __name__ == "__main__":
    main()
