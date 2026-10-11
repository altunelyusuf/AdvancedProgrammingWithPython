#!/usr/bin/env python3
"""SEN0414, chapter 12 (Designing and Deploying Command Line Programs, Automate the Boring Stuff with Python, 3rd
edition) - the narrative diagrams of the chapter (version 1.0.0).

A paragraph gets the diagram its narrative calls for - a workflow an activity diagram, the possible usages a
use-case diagram, the life of a thing a state diagram, an exchange between parties a sequence diagram, a topic and
its parts a mind map - and the mapping from narrative pattern to diagram type lives in the CME ontology (the
narrative-to-diagram module of cme_standards_adoption_v1_3_0.ttl) so that it is reused by every course. Each entry
names the concepts whose paragraphs it accompanies, the narrative pattern it was recognised as, the passage it was
read from (also_from names further concepts whose explanations the content draws on), one sentence saying why the
pattern fits, and the diagram's content in the element names the renderer of that type expects. Every element label
is made of words that occur in the explanations of the accompanying concepts or their section; run_checks() measures
that (the grounding ratio) besides the structural rules. This module follows the layout of
sen0414_ch11_diagrams_v1_0_0.py (the helper functions below are the same rules, written again because a file of
another chapter is not edited).

Usage: import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"

DIAGRAMS = [
    {
        "id": "HowTheTerminalFindsAProgram",
        "pattern": "Workflow",
        "title": "How the terminal finds a typed program name",
        "concepts": ["PathSearchOrder", "RunFromTerminal", "WhichAndWhere"],
        "also_from": ["PathVariable", "NavigatingFolders", "PathEditing"],
        "read_from": "chapter 12, the PATH environment variable: Windows first checks the current working directory "
                     "and then the folders in PATH, macOS and Linux check only the folders in PATH, the first folder "
                     "holding the name wins, and subfolders are never searched",
        "why": "the passage describes what the terminal does, step by step, between a typed program name and a running "
               "program, with a different path on Windows and on macOS and Linux and a stop at the first match: a "
               "workflow with choices on the way",
        "data": {
            "nodes": [
                {"id": "typed", "label": "A program name is typed in the terminal"},
                {"id": "win", "label": "On Windows?", "kind": "decision"},
                {"id": "cwd", "label": "Windows looks in the current folder first"},
                {"id": "path", "label": "Search the folders listed in PATH, in order"},
                {"id": "hit", "label": "Is the name in this folder? (subfolders are never searched)", "kind": "decision"},
                {"id": "run", "label": "The first folder holding the name wins: the program runs"},
                {"id": "next", "label": "Search the next folder in PATH"},
            ],
            "flows": [["start", "typed"], ["typed", "win"], ["win", "cwd", "yes"], ["win", "path", "macOS, Linux"],
                      ["cwd", "path"], ["path", "hit"], ["hit", "run", "yes"], ["hit", "next", "no"],
                      ["next", "hit"], ["run", "end"]],
        },
    },
    {
        "id": "DeployingOnUbuntu",
        "pattern": "Workflow",
        "title": "Deploying a script on Ubuntu, from file to Dash",
        "concepts": ["ShellScriptLauncher", "ExecutePermission", "DesktopEntry", "ShebangLine"],
        "also_from": ["LauncherFiles", "LauncherMechanics", "DeployingPrograms", "PathEditing"],
        "read_from": "chapter 12, deploying on Ubuntu Linux: place yourScript.py in the Scripts folder, create a shell "
                     "script named yourScript that starts with #!/usr/bin/env bash and activates the virtual "
                     "environment, run chmod u+x yourScript, and create a .desktop file to run it from Dash",
        "why": "the passage is a numbered list of steps a user takes in order, with one choice at the end - run the "
               "launcher from a terminal by name, or also put it into Dash with a desktop file: a workflow",
        "data": {
            "nodes": [
                {"id": "place", "label": "Place yourScript.py in the Scripts folder on PATH"},
                {"id": "write", "label": "Create a shell script named yourScript, no extension"},
                {"id": "bang", "label": "First line #!/usr/bin/env bash; source the activate script"},
                {"id": "chmod", "label": "Run chmod u+x yourScript: the execute permission"},
                {"id": "dash", "label": "Run it from Dash too?", "kind": "decision"},
                {"id": "desk", "label": "Create yourScript.desktop in ~/.local/share/applications"},
                {"id": "term", "label": "Typing yourScript in any terminal runs it"},
            ],
            "flows": [["start", "place"], ["place", "write"], ["write", "bang"], ["bang", "chmod"], ["chmod", "dash"],
                      ["dash", "desk", "yes"], ["dash", "term", "no"], ["desk", "end"], ["term", "end"]],
        },
    },
    {
        "id": "VirtualEnvironmentLife",
        "pattern": "LifeCycle",
        "title": "A virtual environment's life, from creation to deletion",
        "concepts": ["CreatingAVenv", "ActivatingAVenv", "VenvDetection"],
        "also_from": ["VirtualEnvironments", "EnvironmentsAndPackages", "InstallAndUninstall"],
        "read_from": "chapter 12, virtual environments: python -m venv .venv creates the environment, activation puts "
                     "its folder first on PATH in one terminal window, deactivate undoes that, and deleting the .venv "
                     "folder removes the environment with its packages",
        "why": "the passage follows one environment through the states it passes - created, activated, deactivated, "
               "deleted - and names the command that moves it from each state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "created", "label": "Created: python -m venv .venv creates the .venv folder"},
                {"id": "active", "label": "Activation: its folder is first on PATH; (.venv) in the prompt"},
                {"id": "inactive", "label": "Deactivate: the terminal runs the original Python"},
                {"id": "deleted", "label": "Deleting the .venv folder removes the environment and its packages"},
            ],
            "initial": "created",
            "final": ["deleted"],
            "transitions": [
                ["created", "active", "source activate, or activate.bat on Windows"],
                ["active", "active", "python -m pip install adds a package"],
                ["active", "inactive", "deactivate, or closing the terminal window"],
                ["inactive", "active", "activation, in the current terminal window"],
                ["inactive", "deleted", "deleting the .venv folder"],
            ],
        },
    },
    {
        "id": "CcwdExchange",
        "pattern": "Interaction",
        "title": "What happens when ccwd .. is typed",
        "concepts": ["CcwdScript", "ProgramWorkingDirectory", "ArgvList"],
        "also_from": ["CcwdCommand", "ShortPrograms", "CommandLineArguments"],
        "read_from": "chapter 12, the ccwd program: the terminal runs ccwd.py, sys.argv holds the script name and the "
                     "argument, os.chdir() changes the program's own working directory, os.getcwd() is copied to the "
                     "clipboard with pyperclip, and the terminal is still in the folder it was in",
        "why": "the passage is an exchange between parties in an order that matters - the terminal starts the "
               "program, the program changes its own folder and writes to the clipboard, and the terminal is left "
               "where it was - an interaction",
        "data": {
            "participants": [
                {"id": "term", "label": "The terminal, in ~/Scripts"},
                {"id": "prog", "label": "ccwd.py"},
                {"id": "clip", "label": "The clipboard"},
            ],
            "messages": [
                ["term", "prog", "runs ccwd.py; sys.argv holds 'ccwd.py' and '..'"],
                ["prog", "prog", "os.chdir(sys.argv[1]) changes the program's own directory"],
                ["prog", "clip", "pyperclip.copy(os.getcwd()) copies the parent folder"],
                ["prog", "term", "the program ends; the terminal is still in ~/Scripts", "reply"],
            ],
        },
    },
    {
        "id": "WhatAProgramKnowsAboutItself",
        "pattern": "SetOfUses",
        "title": "What a self-aware program can find out about itself",
        "concepts": ["FileVariable", "InterpreterLocation", "VersionInfo", "OperatingSystemName", "MissingModule"],
        "also_from": ["SelfAwarePrograms", "ScriptLocation", "PlatformChecks", "ModuleChecks", "ExitWithMessage"],
        "read_from": "chapter 12, self-aware Python programs: __file__ gives the .py file's path, sys.executable and "
                     "sys.version the interpreter, sys.version_info its version as integers, os.name and sys.platform "
                     "the operating system, and a try block around an import catches ModuleNotFoundError",
        "why": "the passage lists independent questions a running program can ask with built-in values - where it "
               "is, what runs it, which version, which operating system, whether a module is installed - a set of "
               "uses of the same idea, not a sequence",
        "data": {
            "system": "BUILT-IN VALUES THE INTERPRETER SETS",
            "actors": [{"id": "prog", "label": "A running Python program"}],
            "usecases": [
                {"id": "file", "label": "Find its own .py file with __file__ and Path(__file__)"},
                {"id": "exe", "label": "Name the interpreter with sys.executable and sys.version"},
                {"id": "ver", "label": "Compare versions: sys.version_info >= (3, 9)"},
                {"id": "os", "label": "Tell the operating system: os.name, sys.platform"},
                {"id": "mod", "label": "Catch ModuleNotFoundError; sys.exit() with a message"},
            ],
            "links": [["prog", "file"], ["prog", "exe"], ["prog", "ver"], ["prog", "os"], ["prog", "mod"]],
        },
    },
    {
        "id": "CommandLineProgramsAtAGlance",
        "pattern": "TopicAndParts",
        "title": "Command line programs at a glance: five branches",
        "concepts": ["UsingTheTerminal", "EnvironmentsAndPackages", "SelfAwarePrograms", "TextBasedDesign",
                     "DeployingPrograms"],
        "also_from": ["ProgramVocabulary", "NavigatingFolders", "PathVariable", "VirtualEnvironments", "PipInstaller",
                      "ScriptLocation", "PlatformChecks", "ModuleChecks", "CommandLineArguments", "TerminalOutput",
                      "MessageBoxes", "LauncherFiles", "LauncherMechanics", "CompilingWithPyInstaller"],
        "read_from": "chapter 12, the opening of each of its main branches: the terminal and PATH, virtual "
                     "environments and pip, the built-in values that make a program self-aware, text-based program "
                     "design, and deploying a program with launcher files or PyInstaller",
        "why": "the chapter classifies one topic, running a program outside the code editor, by what each branch is "
               "about and lists examples under each - a topic and its parts, laid out to remember, with the one idea "
               "that holds for every part stated once at the root",
        "data": {
            "root": "Deployment: running a program outside the code editor",
            "branches": [
                {"label": "The terminal: folders, commands and PATH",
                 "children": ["cd, pwd, dir and ls move around and list folders",
                              "PATH is the list of folders searched for a program name",
                              "which and where report where a program name is found"]},
                {"label": "Virtual environments and pip",
                 "children": ["python -m venv .venv creates a separate installation",
                              "activation puts the environment first on PATH",
                              "python -m pip installs packages from PyPI"]},
                {"label": "Self-aware programs",
                 "children": ["__file__, sys.executable and sys.version_info",
                              "os.name and sys.platform tell the operating system",
                              "ModuleNotFoundError and sys.exit() report a missing module"]},
                {"label": "Text-based program design",
                 "children": ["short command names and sys.argv arguments",
                              "the clipboard, colour, clearing and quiet output",
                              "PyMsgBox dialog boxes in place of print() and input()"]},
                {"label": "Deploying programs",
                 "children": ["a batch file, a command file or a shell script launcher",
                              "the shebang line and chmod u+x",
                              "PyInstaller builds one executable file"]},
            ],
        },
    },
]

STOP = set("a an the of to in on and or is are be by it its for from with as at that this not yet no yes one every then".split())


def _labels(d):
    """every element label of a diagram, whatever its type"""
    x = d["data"]; out = []
    for n in x.get("nodes", []) + x.get("states", []) + x.get("actors", []) + x.get("usecases", []) + x.get("participants", []):
        out.append(n["label"] if isinstance(n, dict) else n)
    out += [f[2] for f in x.get("flows", []) + x.get("transitions", []) if len(f) > 2 and f[2]]
    out += [m[2] for m in x.get("messages", [])]
    for b in x.get("branches", []):
        out.append(b["label"]); out += b.get("children", [])
    if x.get("root"): out.append(x["root"])
    if x.get("system"): out.append(x["system"])
    return out


def grounding(d, nodes):
    """share of a diagram's content words that occur in the explanations of its concepts (and their section and subject)"""
    import re
    by = {n["id"]: n for n in nodes}
    ids = set(d["concepts"]) | set(d.get("also_from", []))
    for c in list(ids):
        n = by.get(c)
        while n and n.get("parent"):
            ids.add(n["parent"]); n = by.get(n["parent"])
    text = " ".join((by[c].get("body") or "") + " " + (by[c].get("definition") or "") + " " + by[c]["label"] for c in ids if c in by).lower()
    words = [w for w in re.findall(r"[a-z0-9][a-z0-9'-]*", " ".join(_labels(d)).lower()) if w not in STOP and len(w) > 1]
    hit = [w for w in words if w in text or w.rstrip("s") in text or (w + "s") in text]
    return len(hit), len(words), sorted(set(w for w in words if w not in hit))


def run_checks(nodes=None, mapping=None):
    """structural rules and, with the chapter's nodes, the grounding ratio; with the CME mapping, the pattern is known and its type is assigned"""
    bad = []
    ids = [d["id"] for d in DIAGRAMS]
    if len(ids) != len(set(ids)): bad.append("duplicate diagram ids")
    by = {n["id"]: n for n in nodes} if nodes else None
    for d in DIAGRAMS:
        for f in ("pattern", "title", "concepts", "read_from", "why", "data"):
            if not d.get(f): bad.append("%s: missing %s" % (d["id"], f))
        if by:
            for c in d["concepts"] + d.get("also_from", []):
                if c not in by: bad.append("%s: unknown concept %s" % (d["id"], c))
        if mapping:
            m = mapping.get(d["pattern"])
            if not m: bad.append("%s: pattern %s is not in the CME mapping" % (d["id"], d["pattern"]))
            else:
                d["type"] = m["types"][0]
        x = d["data"]
        if "flows" in x:
            nid = set(n["id"] for n in x["nodes"]) | {"start", "end"}
            for f in x["flows"]:
                if f[0] not in nid or f[1] not in nid: bad.append("%s: flow names an unknown node %r" % (d["id"], f))
            if not any(f[0] == "start" for f in x["flows"]) or not any(f[1] == "end" for f in x["flows"]): bad.append("%s: no start or no end" % d["id"])
            for n in x["nodes"]:
                if n.get("kind") == "decision" and len([f for f in x["flows"] if f[0] == n["id"]]) < 2: bad.append("%s: decision %s has fewer than two outgoing flows" % (d["id"], n["id"]))
        if "transitions" in x:
            sid = set(s["id"] if isinstance(s, dict) else s for s in x["states"])
            if x["initial"] not in sid: bad.append("%s: initial state unknown" % d["id"])
            for f in x.get("final", []):
                if f not in sid: bad.append("%s: final state unknown" % d["id"])
            for tr in x["transitions"]:
                if tr[0] not in sid or tr[1] not in sid or not tr[2]: bad.append("%s: transition %r unknown state or unlabelled" % (d["id"], tr))
        if "usecases" in x:
            aid = set(a["id"] for a in x["actors"]); uid = set(u["id"] for u in x["usecases"])
            for a, u in x["links"]:
                if a not in aid or u not in uid: bad.append("%s: link %r names an unknown actor or use case" % (d["id"], (a, u)))
            if uid - set(u for _, u in x["links"]): bad.append("%s: a use case has no actor" % d["id"])
        if "messages" in x:
            pid = set(p["id"] for p in x["participants"])
            for m in x["messages"]:
                if m[0] not in pid or m[1] not in pid or not m[2]: bad.append("%s: message %r unknown participant or empty" % (d["id"], m))
        if "branches" in x:
            if len(x["branches"]) < 2: bad.append("%s: a mind map needs at least two branches" % d["id"])
        for lab in _labels(d):
            if len(lab) > 72: bad.append("%s: label over 72 characters: %r" % (d["id"], lab))
        if nodes:
            h, n, miss = grounding(d, nodes)
            d["grounding"] = [h, n]
            if n and h / n < 0.8: bad.append("%s: grounding %d/%d below 0.8; words not in the concepts' explanations: %s" % (d["id"], h, n, ", ".join(miss)))
    return bad


if __name__ == "__main__":
    import sys, json, glob, os
    here = os.path.dirname(os.path.abspath(__file__))
    f = sorted(glob.glob(os.path.join(here, "ch12-page", "page_data_v*.json")))
    if not f:
        print("no page_data yet; run sen0414_page_data first"); sys.exit(2)
    nodes = json.load(open(f[-1]))["nodes"]
    bad = run_checks(nodes)
    for d in DIAGRAMS: print("%-30s %-14s grounding %s" % (d["id"], d["pattern"], d.get("grounding")))
    print("\n".join(bad) or "all checks pass: %d diagrams" % len(DIAGRAMS)); sys.exit(1 if bad else 0)
