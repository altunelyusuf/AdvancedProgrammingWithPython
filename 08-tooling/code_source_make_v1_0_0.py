#!/usr/bin/env python3
"""Single-source step, version 1.0.0 (Lineage11, story ST11_Make).

One source file per chapter holds every code example once. This step makes, from that file only:
  1. the chapter-code manifest (the list the page runs: order, id, name, slide, concepts, code, expected),
  2. the examples module for the generic chapter deck builder (one code box per example),
  3. the Slide code tab text (every example, in slide order, the same lines as the slide).
The slide, the page example and the tab therefore cannot differ. The step holds no chapter-specific text.

Source file (JSON):
  {"chapter": 10, "title": "...", "examples": [
     {"id": "...", "name": "...", "slide": 7, "concepts": ["..."], "book": "section or block the code comes from",
      "setup": ["hidden lines: sample files, temporary folder"], "code": ["the lines shown and copied"],
      "explain": "one plain sentence beside the code", "expected": "result text, filled by a run"}]}

Usage:  python3 code_source_make_v1_0_0.py SOURCE.json OUT_DIR [--manifest-version X.Y.Z]
Writes OUT_DIR/chapter_code_chNN_vX.json, OUT_DIR/examples_gen.py, OUT_DIR/slide_code_tab.py. Running twice gives identical files.
"""
__version__ = "1.0.0"
import json
import os
import re
import sys

PROMPT = re.compile(r"^\s*(>>>|\.\.\.|>>)")


def load(path):
    src = json.load(open(path, encoding="utf-8"))
    problems = []
    seen = set()
    for i, e in enumerate(src["examples"]):
        where = "example %d (%s)" % (i + 1, e.get("id"))
        for k in ("id", "name", "slide", "code", "book"):
            if not e.get(k):
                problems.append("%s: missing %s" % (where, k))
        if e.get("id") in seen:
            problems.append("%s: id repeated" % where)
        seen.add(e.get("id"))
        if not isinstance(e.get("code"), list) or not all(isinstance(l, str) for l in e.get("code", [])):
            problems.append("%s: code must be a list of lines" % where)
            continue
        if any(PROMPT.match(l) for l in e["code"]):
            problems.append("%s: a line starts with an interpreter prompt" % where)
        if any("lambda" in l for l in e["code"]):
            problems.append("%s: lambda is not taught here" % where)
    slides = [e.get("slide") for e in src["examples"]]
    if slides != sorted(slides):
        problems.append("examples are not in slide order")
    if problems:
        raise SystemExit("source refused:\n  " + "\n  ".join(problems))
    return src


def manifest(src, version):
    ex = []
    for n, e in enumerate(src["examples"], 1):
        ex.append({"order": n, "id": e["id"], "name": e["name"], "slide": e["slide"], "concepts": e.get("concepts", []),
                   "code": "\n".join(e["code"]), "expected": e.get("expected", "")})
    return ex


def examples_module(src):
    out = ['"""Examples module made by code_source_make %s from the chapter %s single source. Do not edit: change the source and run the step again.' % (__version__, src["chapter"]),
           'One code box per example. The `setup` lines are run first and are never shown."""',
           "__version__ = %r" % __version__, "", "EXAMPLES = ["]
    for e in src["examples"]:
        out.append("    dict(id=%r, name=%r, title=%r, part=%r, visual=%r, concepts=%r, setup=%r,\n         groups=[(%r, %r)])," % (
            e["id"], e["name"], e.get("title", e["name"]), e.get("part", 1), e.get("visual", e["id"]), e.get("concepts", []),
            e.get("setup", []), e["code"], e.get("explain", "")))
    out += ["]", "BY_ID = {e['id']: e for e in EXAMPLES}", "",
            "def code_lines(ex):", "    return [l for g, _ in ex['groups'] for l in g]", "",
            "def code_text(ex):", "    return '\\n'.join(code_lines(ex))", "",
            "def run_text(ex):", "    return '\\n'.join(list(ex.get('setup', [])) + code_lines(ex))", ""]
    return "\n".join(out)


def tab(src):
    parts = []
    for n, e in enumerate(src["examples"], 1):
        parts.append("# --- %d. %s (slide %s) ---" % (n, e["name"], e["slide"]))
        parts.extend(e["code"])
        parts.append("")
    return "\n".join(parts)


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text if text.endswith("\n") else text + "\n")


def main(argv):
    ver = "1.0.0"
    if "--manifest-version" in argv:
        i = argv.index("--manifest-version")
        ver = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    src_path, out = argv[1], argv[2]
    src = load(src_path)
    os.makedirs(out, exist_ok=True)
    nn = "%02d" % int(src["chapter"])
    write(os.path.join(out, "chapter_code_ch%s_v%s.json" % (nn, ver.replace(".", "_"))), json.dumps(manifest(src, ver), indent=1, ensure_ascii=False))
    write(os.path.join(out, "examples_gen.py"), examples_module(src))
    write(os.path.join(out, "slide_code_tab.py"), tab(src))
    print("made %d examples for chapter %s in %s" % (len(src["examples"]), nn, out))


if __name__ == "__main__":
    main(sys.argv)
