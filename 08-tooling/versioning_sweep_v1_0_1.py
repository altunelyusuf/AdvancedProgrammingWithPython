#!/usr/bin/env python3
"""Configuration-management sweep for one course repository, applying the OE configuration ontology's
EngineeringArtefact rule: every artefact's file name embeds its version token, and the token matches the version
declared inside the file. Read from configuration_tbox_v2_7_0.ttl / configuration_abox_v2_7_0.ttl:
  CodeModuleConvention   {name}_v{M}_{m}_{p}.{ext}  (py, js, json, yaml)     HtmlArtifactConvention {name}_v{M}_{m}_{p}.html
  OntologyFileConvention {prefix}_v{M}_{m}_{p}.ttl  (versionInfo == token)  DocumentationFileConvention {name}_v{M}_{m}.md
For binaries the sweep does not own (the owner's documents and legacy slides) it renames only, content untouched.
For text files it owns it also writes the internal declaration; a changed file gets a new version (BP-D7).
Usage: versioning_sweep_v1_0_1.py <working-copy> <git-clone-for-history> [--apply]"""
__version__ = "1.0.1"
import os, re, subprocess, sys, json
WC, HIST = sys.argv[1], sys.argv[2]; APPLY = "--apply" in sys.argv
# Owner ruling, 2026-09-26T11:11:43: "keep GitHub compliancy, never touch them if it is risky" - these five names are fixed by git, GitHub or the
# OE publisher; they are neither renamed nor edited by this sweep.
TOOL_MANDATED = {".gitattributes", "README.md", "LICENSE", "VERSION.txt", "PUBLISH_RECORD.ttl"}
OWNER_INPUTS = ("00-course-profile/", "03-materials/slides/")                                      # the owner's files: rename only
TOK = re.compile(r"_v(\d+)_(\d+)(?:_(\d+))?(\.[A-Za-z0-9]+)$")
DECL = {".py": lambda v: '__version__ = "%s"' % v, ".js": lambda v: 'const VERSION = "%s";' % v}
def git(*a): return subprocess.run(["git", "-C", HIST] + list(a), capture_output=True, text=True).stdout
def contents(path):
    shas = set()
    for c in git("log", "--format=%H", "--", path).split():
        r = subprocess.run(["git", "-C", HIST, "rev-parse", "%s:%s" % (c, path)], capture_output=True, text=True)
        if r.returncode == 0: shas.add(r.stdout.strip())
    return max(1, len(shas))
def declared(path):
    ext = os.path.splitext(path)[1]; s = open(path, errors="ignore").read() if ext in (".py", ".js", ".json", ".md", ".html") else ""
    if ext == ".py": m = re.search(r'^__version__ = "([\d.]+)"', s, re.M)
    elif ext == ".js": m = re.search(r'^const VERSION = "([\d.]+)";', s, re.M)
    elif ext == ".json":
        try: d = json.loads(s); return d.get("_version") if isinstance(d, dict) else None
        except Exception: return None
    elif ext == ".md": m = re.search(r'^Version: ([\d.]+)\s*$', s, re.M)
    elif ext == ".html": m = re.search(r'<meta name="version" content="([\d.]+)">', s)
    elif ext == ".pptx": from pptx import Presentation; return Presentation(path).core_properties.version or None
    elif ext == ".docx": import docx; return docx.Document(path).core_properties.version or None
    else: return None
    return m.group(1) if m else None
def with_decl(path, v):
    ext = os.path.splitext(path)[1]; s = open(path).read() if ext not in (".pptx", ".docx") else ""
    if ext == ".py":
        s = re.sub(r'^__version__ = "[\d.]+"\n', "", s, flags=re.M)
        m = re.match(r'(#![^\n]*\n)?(\s*(?:"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\')\s*\n)?', s)
        s = s[:m.end()] + DECL[".py"](v) + "\n" + s[m.end():]
    elif ext == ".js":
        s = re.sub(r'^const VERSION = "[\d.]+";\n', "", s, flags=re.M); s = DECL[".js"](v) + "\n" + s
    elif ext == ".json":
        d = json.loads(s); d = d if isinstance(d, dict) else {"items": d}; d = {"_version": v, **{k: x for k, x in d.items() if k != "_version"}}
        s = json.dumps(d, indent=1, ensure_ascii=False) + "\n"
    elif ext in (".pptx", ".docx"):
        if ext == ".pptx": from pptx import Presentation; d = Presentation(path)
        else: import docx; d = docx.Document(path)
        d.core_properties.version = v; d.save(path); return
    elif ext == ".md":
        s = re.sub(r'^Version: [\d.]+\s*\n', "", s, flags=re.M); lines = s.split("\n", 1); s = lines[0] + "\n\nVersion: " + v + "\n" + (lines[1] if len(lines) > 1 else "")
    open(path, "w").write(s)
plan = []
for rel in sorted(x for x in git("ls-files").split("\n") if x):
    p = os.path.join(WC, rel); base = os.path.basename(rel)
    if not os.path.exists(p) or base in TOOL_MANDATED: continue
    if re.match(r"(page_data|test_results|test_results_abox|build_record|corpus_manifest)_v\d", base): continue  # generated: their generator writes them at the page's version
    if "/fixtures/fixture_stale_page_v2.html" in rel: plan.append(("retire", rel, None, None)); continue
    ext = os.path.splitext(base)[1]; m = TOK.search(base); owner = rel.startswith(OWNER_INPUTS)
    textual = ext in (".py", ".js", ".json", ".md") and not owner
    office = ext in (".pptx", ".docx") and not owner and "/fixtures/" not in rel and "fixture_" not in base   # ours: core properties carry the version
    if not m:
        n = contents(rel); stem = re.sub(r"\s+", "", base[: -len(ext)]).replace("_v9", "") if ext else base
        stem = re.sub(r"_v\d+$", "", stem)
        # earlier contents count as MINOR steps; adding the declaration is a fix with no vocabulary change, so PATCH (BP-D7)
        v = "1.%d.%d" % (n - 1, 1 if (textual or office) else 0)
        if ext == ".md": v = "1.%d" % (n - 1 + (1 if textual else 0)); new = "%s_v%s%s" % (stem, v.replace(".", "_"), ext)
        elif "fixture_stale_page" in stem: v = "9.0.0"; new = "fixture_stale_page_v9_0_0.html"
        else: new = "%s_v%s%s" % (stem, v.replace(".", "_"), ext)
        plan.append(("rename" + ("+declare" if (textual or office) else ""), rel, os.path.join(os.path.dirname(rel), new), v))
    elif textual or office:
        cur = ".".join(g for g in m.groups()[:3] if g is not None); d = declared(p)
        if d != cur:
            M, mi, pa = [int(g) if g else 0 for g in m.groups()[:3]]
            v = "%d.%d.%d" % (M, mi, pa + 1) if ext != ".md" else "%d.%d" % (M, mi + 1)   # declaration only: PATCH
            new = base[: m.start()] + "_v" + v.replace(".", "_") + ext
            plan.append(("bump+declare", rel, os.path.join(os.path.dirname(rel), new), v))
for a, old, new, v in plan: print("%-16s %-62s -> %s%s" % (a, old[-62:], os.path.basename(new) if new else "(retired)", "" if not v else "  [%s]" % v))
print("\n%d actions; tool-mandated names left for the owner: %s" % (len(plan), ", ".join(sorted(TOOL_MANDATED))))
if APPLY:
    renames = {}
    for a, old, new, v in plan:
        po = os.path.join(WC, old)
        if a == "retire": os.remove(po); continue
        pn = os.path.join(WC, new); os.rename(po, pn); renames[os.path.basename(old)] = os.path.basename(new)
        if "declare" in a: with_decl(pn, v if os.path.splitext(pn)[1] != ".md" else v)
    # references to renamed files, in files that describe the current state (historical records are left as they were, L-112)
    CURRENT = [os.path.join(dp, f) for dp, _, fs in os.walk(os.path.join(WC, "08-tooling")) for f in fs if f.endswith((".py", ".js", ".json", ".html")) and "/fixtures/" not in dp] + [os.path.join(WC, "03-materials", f) for f in os.listdir(os.path.join(WC, "03-materials")) if f.endswith(".ttl")]
    stems = {re.sub(r"\.(py|js)$", "", o): re.sub(r"\.(py|js)$", "", n) for o, n in renames.items() if o.endswith((".py", ".js"))}
    for f in CURRENT:
        s = open(f, errors="ignore").read(); o = s
        for a_, b_ in sorted(renames.items(), key=lambda x: -len(x[0])): s = s.replace(a_, b_)
        # a module named without its extension is only rewritten where Python imports it - never as an ordinary word
        for a_, b_ in sorted(stems.items(), key=lambda x: -len(x[0])): s = re.sub(r"(?<=\bimport )%s\b|(?<=\bfrom )%s\b" % (re.escape(a_), re.escape(a_)), b_, s)
        if s != o: open(f, "w").write(s); print("references updated:", os.path.relpath(f, WC))
    json.dump(renames, open(os.path.join(WC, "08-tooling", "renames_this_release.json"), "w"), indent=1)
