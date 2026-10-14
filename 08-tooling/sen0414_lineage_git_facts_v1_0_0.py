#!/usr/bin/env python3
"""sen0414_lineage_git_facts v1_0_0 - reads, for the eighteen stories of chapters 7 to 12, the facts the register needs from git and from the files:
which built files carry each story, their SHA-256, the commits that first added and last changed them, and the UTC time of that last change,
which is the story's real finish (the moment its cited files, a .docx rendering apart, reached the form that is cited). Writes FACTS.json; changes nothing in the repository.

Usage: sen0414_lineage_git_facts_v1_0_0.py OUT.json
"""
__version__ = "1.0.0"
import glob, hashlib, json, os, re, subprocess, sys, datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = {7: "03-materials/ch07/SEN0414_Ch07_Dictionaries_3e_v1_0_0.pptx"}
for n in range(8, 13):
    DECK[n] = "08-tooling/ch%02d-deck/sen0414_ch%02d_deck_v1_0_0.pptx" % (n, n)


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True, check=True).stdout.strip()


def sha(p):
    return hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()


def newest(pattern):
    fs = glob.glob(os.path.join(REPO, pattern))
    key = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.", p).groups()]
    return os.path.relpath(sorted(fs, key=key)[-1], REPO)


def art(path):
    assert git("status", "--porcelain", "--", path) == "", "uncommitted change in " + path
    first = git("log", "--diff-filter=A", "--format=%h", "--", path).splitlines()[-1]
    last, lt = git("log", "-1", "--format=%h %aI", "--", path).split()
    lu = datetime.datetime.fromisoformat(lt).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    return {"path": path, "sha256": sha(path), "first_commit": first, "last_commit": last, "last_commit_utc": lu}


def main():
    out = {"head": git("rev-parse", "--short", "HEAD"), "stories": {}}
    for n in range(7, 13):
        rd = "03-materials/ch%02d/rdodi/sen0414_ch%02d_" % (n, n)
        page = "03-materials/ch%02d/page/sen0414_ch%02d_page_v9_28_0.html" % (n, n)
        sets = {"Deck": [DECK[n]],
                "Research": [newest(rd + "research_v*.ttl"), newest(rd + "document_v*.ttl"), newest(rd + "document_v*.docx"),
                             newest(rd + "domain_tbox_v*.ttl"), newest(rd + "domain_abox_v*.ttl"), newest(rd + "domain_shacl_v*.ttl")],
                "Page": [page]}
        for kind, paths in sets.items():
            a = [art(p) for p in paths]
            # a rendering of the document to .docx is cited as evidence but does not decide when the research finished
            fin = max(x["last_commit_utc"] for x in a if not x["path"].endswith(".docx"))
            out["stories"]["ST_%s_Ch%02d" % (kind, n)] = {"artifacts": a, "finished": fin}
    json.dump(out, open(sys.argv[1], "w"), indent=1)
    for k, v in out["stories"].items():
        print(k, v["finished"], [os.path.basename(x["path"]) for x in v["artifacts"]][:2])


if __name__ == "__main__":
    main()
