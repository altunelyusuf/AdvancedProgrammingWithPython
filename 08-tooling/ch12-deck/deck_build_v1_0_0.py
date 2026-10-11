#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 12 (Designing and Deploying Command Line Programs) on the CME
classroom standard.

Same regime as chapters 10 and 11: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the
resources, full-sentence takeaway strips, stories with fact rows (no photographs this chapter either - Wikimedia
Commons was still 429-rate-limited from this session's egress IP on 2026-10-11), consoles and whole programs with
their results as Python printed them. Every console result and program transcript comes from examples_out_v1_0_0.json
(made by examples_run_v1_0_0.py); the speaker notes are prose for the reader. The measured PyInstaller numbers on the
PyInstaller slide come from the chapter's research record (finding F7), not from a program of this deck, because a
PyInstaller build needs a package download and fifteen seconds; the slide says so.

Usage: python3 deck_build_v1_0_0.py   (writes deck_plan_v1_0_0.json beside itself)
"""
__version__ = "1.0.0"
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ST = load("stories4112", os.path.join(HERE, "..", "sen0414_ch12_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
PD = sorted(__import__("glob").glob(os.path.join(HERE, "..", "ch12-page", "page_data_v*.json")),
            key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
NODES = {n["id"]: n for n in json.load(open(PD[-1]))["nodes"]} if PD else {}
RES = json.load(open(os.path.join(HERE, "..", "ch12-page", "resources_v1_0_0.json")))["links"]
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
CQ1 = ("How does a typed command reach a Python program - through the terminal's search of PATH, a launcher script, a "
       "virtual environment and sys.argv - and where along that way can it go wrong?")
CQ2 = ("Which printed outputs, commands and programs of the chapter differ in current Python or on a current system, "
       "and on what source?")


def lines_of(rows):
    return sum(1 + (1 if out.strip() else 0) for _, out in rows)


def con(group, x, y, w, fs=11, label=None, cap=True, rows=None):
    """A console panel sized from its rows; returns (item, bottom y)."""
    rr = rows if rows is not None else G[group]
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    fs = min(fs, round((w - 0.4) / (maxlen * 0.0088), 1))
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1f in" % (group, w))
    L = lines_of(rr)
    h = round(L * fs * 1.32 / 72.0 + 0.36 + 0.02 * max(0, L - 1), 2)
    it = {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rr, "fs": fs}
    if cap:
        it["cap"] = CAP
    if label:
        if len(label) > (w - 0.1) / 0.083:
            raise SystemExit("REFUSED: label %r is too long for a %.1f in panel" % (label, w))
        it["label"] = label
    return it, round(y + h + (0.26 if cap else 0), 2)


def prog(pname, x, y, w, fs=8, lines=None, show_out=True):
    """A chapter program (or an honest excerpt) with its transcript, sized from its text; returns (item, bottom y).
    The excerpt is a verbatim slice and the label above the panel names it ('program <name>, lines a to b of n'),
    as program_check_v1_0_0.py verifies. The transcript, when shown, sits in the same panel."""
    pr = PROGS[pname]
    all_lines = pr["code"].rstrip("\n").split("\n")
    a, b = (1, len(all_lines)) if lines is None else lines
    shown = all_lines[a - 1:b]
    out = pr["transcript"] if show_out else ""
    outlines = (out.count("\n") + 1) if out else 0
    maxlen = max(max(len(l) for l in shown), max((len(t) for t in out.split("\n")), default=0) + 8)
    fs = min(fs, round((w - 0.4) / (maxlen * 0.0088), 1))
    if fs < 7:
        raise SystemExit("REFUSED: program %s cannot fit unwrapped in %.1f in (fs %.1f)" % (pname, w, fs))
    L = len(shown) + outlines
    h = round(L * fs * 1.32 / 72.0 + 0.40 + 0.02 * max(0, L - 1), 2)
    label = "program %s, lines %d to %d of %d - Python %s" % (pname, a, b, len(all_lines), PYV)
    if len(label) > (w - 0.1) / 0.083:
        label = "program %s, lines %d to %d of %d" % (pname, a, b, len(all_lines))
    if len(label) > (w - 0.1) / 0.083:
        raise SystemExit("REFUSED: caption %r is too long for a %.1f in panel" % (label, w))
    it = {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": shown, "fs": fs, "compact": bool(out),
          "out": out if out else None, "outLabel": "prints", "label": label}
    return it, round(y + h, 2)


def transcript(pname, x, y, w, h, fs=9, label="what the run printed"):
    """The transcript of a program beside its code: a panel holding only the lines the run printed."""
    out = PROGS[pname]["transcript"]
    fs = min(fs, round((w - 0.4) / ((max(len(t) for t in out.split("\n")) + 7) * 0.0088), 1))
    if fs < 7:
        raise SystemExit("REFUSED: transcript of %s cannot fit unwrapped in %.1f in (fs %.1f)" % (pname, w, fs))
    if len(label) > (w - 0.1) / 0.083:
        raise SystemExit("REFUSED: label %r is too long for a %.1f in panel" % (label, w))
    return {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": [], "fs": fs, "compact": True, "out": out,
            "outLabel": "prints", "label": label}


def factrow(sid, x=0.5, y=4.42, w=9.0):
    st = STORY[sid]
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    return {"t": "factrow", "x": x, "y": y, "w": w, "who": st["who"], "where": st["where"],
            "when": st["when"], "link": st["link"], "linkText": host}


def story_notes(sid):
    st = STORY[sid]
    return st["story"] + " The account rests on these sources. " + st["source"]


def card(head, body, x, y, w, h, fs=11.5, accent=None):
    it = {"t": "card", "head": head, "body": body, "x": x, "y": y, "w": w, "h": h, "fs": fs}
    if accent:
        it["accent"] = accent
    return it


S = []


def content(title, sub, items, notes, take, lede=None):
    if lede and len(lede.split()) > 34:
        raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
    if len(take.split()) > 24 or not take.endswith("."):
        raise SystemExit("REFUSED: takeaway %r is not a short full sentence" % take)
    if len(title) > 53:
        raise SystemExit("REFUSED: title %r is longer than 53 characters" % title)
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes, "take": take, "bg": "light"}
    if lede:
        sl["lede"] = lede
    S.append(sl)


# ---- 1 title ---------------------------------------------------------------------------------------------------
S.append({"kind": "title", "title": "Chapter 12: Command Line Programs",
          "sub": "Designing and deploying them: the terminal, PATH, virtual environments, sys.argv, launchers and PyInstaller",
          "items": [{"t": "code", "x": 6.0, "y": 0.85, "w": 3.5, "h": 0.95, "fs": 11, "cap": CAP, "rows": G["title"]}],
          "notes": "Every program so far has been started from the code editor. This chapter takes programs out of the "
                   "editor and into the terminal: how the terminal finds a program, how a virtual environment keeps "
                   "each program's packages apart, how a program reads the words typed after its name, how its text "
                   "interface should behave, and how a small launcher file or PyInstaller turns a script into a "
                   "command anyone can run. Every example on these slides was run under Python 3.14.6 on Ubuntu, and "
                   "the result printed beside it is the result Python gave on that machine.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "Five parts; every range is a run of slides you can jump to",
          "items": [], "notes": "", "take": "Five parts, from a typed command to a deployed program.",
          "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.2, "fs": 13, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 11.5,
          "items": ["6 branches", "%d concepts" % len(NODES), "%d console rows" % sum(len(v) for v in G.values()),
                    "%d programs run" % len(PROGS), "Python %s" % PYV]}],
        "The first question is the chapter's spine: a typed name is looked up in the folders of PATH, it usually "
        "finds a small launcher file, the launcher activates a virtual environment and starts the interpreter, and "
        "the interpreter hands the typed words to the program in sys.argv. Each step can fail in its own way, and "
        "this deck runs every step to show where. The second question is the deck's watch-out: the chapter was "
        "written for Python 3.13 and three operating systems, and a few of its printed lines differ on Python 3.14 "
        "or Ubuntu today, from the packages a new environment holds to an en dash where a hyphen belongs. The chips "
        "give the size of the chapter.",
        "A typed name passes PATH, a launcher, a venv and sys.argv before it runs.")

# ---- 4 terminal ---------------------------------------------------------------------------------------------------
c, bot = con("terminal", 0.5, 1.5, 9.0, fs=10, label="os.chdir and os.listdir do in Python what cd and dir or ls do in the terminal")
content("The terminal: cd, pwd, dir and ls", "A terminal has a current working directory; a program has one of its own",
        [c,
         {"t": "chips", "x": 0.5, "y": bot + 0.12, "w": 9.0, "h": 0.5, "fs": 9,
          "items": ["program", "script", "command", "shell script", "application", "web app"]}],
        "The terminal has a current working directory, shown in its prompt: cd followed by a path changes it, pwd on "
        "macOS and Linux or cd alone on Windows shows it, and dir on Windows or ls on macOS and Linux lists what it "
        "holds. A Python program does the same with os.chdir(), os.getcwd() and os.listdir(), as this console shows, "
        "and dir *.exe becomes a test on the .exe ending. A program in the current folder runs as example.exe on "
        "Windows but must be typed as ./example on macOS and Linux. The chips are six of the chapter's seven words for a "
        "program, the seventh being app: a script is run by an interpreter from its source, a command is run from a terminal with its "
        "options given up front, and a shell script is a file of terminal commands, the form of every launcher "
        "later in this deck.",
        "cd, pwd, dir and ls have Python twins: os.chdir, os.getcwd and os.listdir.")

# ---- 5 PATH -----------------------------------------------------------------------------------------------------
c, bot = con("pathsearch", 0.5, 1.5, 9.0, fs=7, label="the first PATH folder holding the name wins; a subfolder of a PATH folder is never searched")
content("PATH: how the terminal finds a program", "A list of folders, searched in order; the first match runs",
        [c,
         card("Windows, macOS and Linux differ", "Windows looks in the current folder first, then PATH; macOS and "
              "Linux look only in PATH, so ./example is needed there.", 0.5, bot + 0.06, 9.0,
              4.98 - bot - 0.06, fs=10.5)],
        "PATH is an environment variable holding a list of folders, separated by colons on macOS and Linux and by "
        "semicolons on Windows. When a name is typed, the terminal looks in each folder in order and runs the first "
        "match, which is why which python3 or where python is the way to find out which program a name really "
        "starts. The console builds a small PATH of two folders, a and b, and shutil.which, Python's own which, "
        "finds spam in b although a holds a spam of its own one level down, because folders inside a PATH folder "
        "are never searched. Adding a folder to PATH is the chapter's first step towards deployment: once the "
        "Scripts folder is on PATH, any launcher placed there runs by its bare name from any folder.",
        "The first PATH folder that holds the name wins; subfolders never count.")

# ---- 6 virtual environments ----------------------------------------------------------------------------------------
p1, bot = prog("venvTour_v1_0_0.py", 0.5, 1.5, 9.0, fs=8, lines=(9, 14), show_out=False)
p2 = transcript("venvTour_v1_0_0.py", 0.5, bot + 0.38, 9.0, 4.95 - bot - 0.38, fs=9,
                label="prints: the new .venv folder, its settings, pip list inside it, and the prefix test")
content("Virtual environments: python -m venv .venv", "A separate Python with its own packages, one per project",
        [p1, p2],
        "python -m venv .venv makes a separate Python installation in a hidden folder named .venv, with its own set "
        "of installed packages, so two programs that need different versions of one package can each have their "
        "own. This program really creates one. The folder holds bin with the activate script, pyvenv.cfg, which "
        "keeps the original installation's packages out, and, new since Python 3.13, a .gitignore. Inside it pip "
        "list shows pip alone: the chapter's own listing also shows setuptools, which Python stopped installing "
        "into new environments in version 3.12. Activation, with source activate on macOS and Linux or activate.bat "
        "on Windows, puts the environment's folder first on PATH in that one terminal window; the last two lines are "
        "the test a running program can make itself, sys.prefix != sys.base_prefix, False outside and True inside.",
        "A new venv holds only pip; inside it sys.prefix != sys.base_prefix.")

# ---- 7 story: Bicking -----------------------------------------------------------------------------------------------
content("pip began as pyinstall in September 2008", STORY["BickingPip2008"]["when"],
        [card("Ian Bicking, then Carl Meyer", "Bicking, who had already written virtualenv, announced pyinstall on "
              "24 September 2008 and renamed it pip five weeks later; Carl Meyer's PEP 405 of 2011 made venv part "
              "of Python 3.3.", 0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "24 Sep 2008: 'pyinstall: A New Hope'",
             "28 Oct 2008: renamed pip, Pip Installs Packages",
             "13 Jun 2011: PEP 405 credits virtualenv",
             "Python 3.3 ships the venv module"]},
         factrow("BickingPip2008")],
        story_notes("BickingPip2008"),
        "venv and pip grew from Ian Bicking's virtualenv and pyinstall.")

# ---- 8 pip ------------------------------------------------------------------------------------------------------
c, bot = con("pip", 0.5, 1.5, 4.6, fs=11, label="a pin names one version; an import gives a module")
content("pip: install, pin, list and uninstall", "Run it as python -m pip, so it installs into the Python you run",
        [c,
         {"t": "boxes", "x": 5.3, "y": 1.5, "w": 4.2, "h": 3.4, "cols": 1, "fs": 11, "subfs": 9.5, "accent": [0],
          "items": [{"label": "python -m pip install package_name", "sub": "adds a package from PyPI"},
                    {"label": "install -U  /  install name==1.17.4", "sub": "upgrades it, or installs one version"},
                    {"label": "python -m pip list", "sub": "every installed package and its version"},
                    {"label": "python -m pip uninstall package_name", "sub": "removes it again"}]}],
        "pip, a recursive acronym for pip installs packages, downloads third-party packages from PyPI, the Python "
        "Package Index. A package is code published there and a module is one .py file, so pip installs packages "
        "and import imports modules, which is why json, a standard library module, has the type module. The chapter "
        "runs pip as python -m pip rather than as pip, because that installs into exactly the Python that python "
        "starts, never into another installation whose pip happens to come first on PATH; the online chapter prints "
        "that -m with an en dash in several places, which Python reads as a file name, so type a plain hyphen. On "
        "the machine that built this deck pyperclip is not installed in the base Python, so the chapter's clipboard "
        "programs need it installed into their environment first.",
        "pip installs packages from PyPI; run it as python -m pip, with a plain hyphen.")

# ---- 9 self-aware ------------------------------------------------------------------------------------------------
c, bot = con("selfaware", 0.5, 1.5, 4.6, fs=10, label="what the running Python says about itself")
content("Self-aware programs: system and version", "Built-in values the interpreter sets: os.name, sys.platform, sys.version_info",
        [c,
         card("A missing comma", "The chapter prints list(sys.version_info) as [3, 13, 1 'final', 0]; "
              "a comma is missing after the 1. Tuples compare item by item, so sys.version_info >= (3, 9) is the "
              "clean version test.", 5.3, 1.5, 4.2, 3.4, fs=12)],
        "The interpreter sets several values that let a program learn about itself. os.name is 'nt' on Windows and "
        "'posix' on macOS and Linux, sys.platform is 'win32', 'darwin' or 'linux', and sys.version_info holds the "
        "version as integers, so comparing it with a tuple such as (3, 9) is a direct version check. __file__, the "
        "path of the running .py file, exists only when code comes from a file, so in this console, which runs code "
        "typed in, it is absent, and sys.prefix equals sys.base_prefix because this Python is not a virtual "
        "environment. The chapter's own printed list of version numbers lacks one comma, a typing slip rather than "
        "a different value.",
        "os.name, sys.platform and sys.version_info adapt one script to each system.")

# ---- 10 missing modules and exit -----------------------------------------------------------------------------------
c, bot = prog("selfAware_v1_0_0.py", 0.5, 1.5, 9.0, fs=8, lines=(6, 15), show_out=False)
p2 = transcript("selfAware_v1_0_0.py", 0.5, bot + 0.38, 9.0, 4.95 - bot - 0.38, fs=8,
                label="prints: the script run from its file - __file__, the checks, then sys.exit with a message")
content("Missing modules and sys.exit with a message", "Catch ModuleNotFoundError; stop with a message the user can act on",
        [c, p2],
        "Putting an import statement in a try block and catching ModuleNotFoundError lets a program say in its own "
        "words that a package is missing, instead of stopping with a traceback, and sys.exit() then ends it. "
        "sys.exit() works by raising SystemExit, which is deliberately not a subclass of Exception, so a broad except "
        "Exception does not swallow it. The program writes such a script to a file and runs it: __file__ is an "
        "absolute path although the script was started by a relative name, the version and system checks pass, and "
        "the missing module ends the run with the message on standard error and exit code 1, the number a launcher "
        "or another program can test.",
        "Catch ModuleNotFoundError; sys.exit(message) writes to stderr, exit code 1.")

# ---- 11 sys.argv ---------------------------------------------------------------------------------------------------
p1, bot = prog("argvAndQuoting_v1_0_0.py", 0.5, 1.5, 9.0, fs=8.5)
content("Command line arguments: sys.argv", "The script's name first, then the typed words, split at spaces",
        [p1],
        "The words typed after a command are its command line arguments, and a Python script receives them in the "
        "list sys.argv: the script's own file name first, then each word, split at spaces. This program starts the "
        "chapter's yourScript.py three times, and the first line is exactly the chapter's example, ['yourScript.py', "
        "'hello', 'world']. Quotation marks keep a space inside one argument, so the second run gets 'hello world' "
        "as a single item; shlex.split, used here to split each typed line, follows the same rules as a POSIX shell. "
        "With no words typed, sys.argv still holds the script's name, which is why the chapter's programs test "
        "len(sys.argv) > 1 before reading an argument.",
        "sys.argv holds the script name, then the typed words; quotes keep spaces.")

# ---- 12 argparse ----------------------------------------------------------------------------------------------------
c, bot = con("argparse", 0.5, 1.5, 9.0, fs=8, label="argparse declares each argument once; a bad value raises ArgumentError, not a deep traceback")
p2 = transcript("argparseSnowstorm_v1_0_0.py", 0.5, bot + 0.38, 9.0, 4.95 - bot - 0.38, fs=8,
                label="transcript of program argparseSnowstorm_v1_0_0.py: a bad value exits with code 2")
content("argparse: when the arguments multiply", "The module the chapter recommends and leaves to its documentation",
        [c, p2],
        "Reading sys.argv by hand is right for one or two arguments, but the chapter warns that combinations soon pile "
        "up: does spam eggs mean eggs spam, what if two exclusive options are both given? Its advice is Python's "
        "argparse module, which it leaves to the documentation, so this deck shows it. Each argument is declared "
        "once, here the snowstorm's density as an optional integer defaulting to 4 and a --verbose switch, and "
        "parse_args turns a list of words into named values, converting the type on the way. In the console the "
        "parser was made with exit_on_error=False, so a word that is not a number raises ArgumentError; run as a "
        "real command, the same parser prints a usage error and exits with code 2, the convention for a command "
        "line mistake.",
        "argparse parses, converts, defaults and reports errors for you.")

# ---- 13 story: Socha -------------------------------------------------------------------------------------------------
content("A text interface that felt like a desktop, 1986", STORY["SochaNortonCommander1986"]["when"],
        [card("John Socha, Norton Commander", "Socha began a two-panel file manager for MS-DOS in 1984, called Visual "
              "DOS, and Peter Norton Computing released it in 1986 as Norton Commander, the chapter's Figure 12-1.",
              0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "1984: work begins as Visual DOS, or VDOS",
             "1986: released by Peter Norton Computing",
             "Two panels of files, commands along the bottom",
             "1990: Symantec buys Peter Norton Computing"]},
         factrow("SochaNortonCommander1986")],
        story_notes("SochaNortonCommander1986"),
        "A text interface can be rich: Norton Commander drew a desktop in text.")

# ---- 14 clearing and block characters ------------------------------------------------------------------------------
c, bot = con("clearing", 0.5, 1.5, 4.8, fs=12, label="the clear() one-liner, and the snowstorm's three blocks")
content("Terminal output: clearing, blocks and colour", "A conditional expression picks cls or clear; chr() gives the block characters",
        [c,
         card("Colour with Bext", "bext.fg('red') and bext.bg('blue') colour the text; 'reset' restores it. Bext 0.1.1 "
              "names the cursor functions hide_cursor() and show_cursor(), not the hide() and show() the chapter "
              "lists. It works in a terminal, not in Mu.", 5.5, 1.5, 4.0, 3.4, fs=11.5)],
        "A text program can clear its window with a one-line function: os.system('cls' if os.name == 'nt' else "
        "'clear') runs cls on Windows and clear on macOS and Linux, choosing with a conditional expression, value1 if "
        "condition else value2, which gives 'clear' on this machine. The snowstorm program draws with three block "
        "characters, the top half block, the bottom half block and the full block, which chr() returns for 9600, "
        "9604 and 9608. Colour comes from the third-party Bext package, built on Colorama; installed for this deck, "
        "its version 0.1.1 has the colour, clear, size, title, goto and get_key functions the chapter lists, but "
        "calls its cursor functions hide_cursor and show_cursor. The chapter's warning stands: a light or dark "
        "terminal theme changes how colours look, and too much colour makes a program hard to read.",
        "cls or clear by a conditional expression; chr gives blocks; Bext, colour.")

# ---- 15 snowstorm ------------------------------------------------------------------------------------------------
p1, bot = prog("snowstormFrame_v1_0_0.py", 0.5, 1.5, 5.45, fs=8, lines=(7, 22), show_out=False)
p2 = transcript("snowstormFrame_v1_0_0.py", 6.1, 1.5, 3.4, 3.45, fs=9, label="one frame, density 20")
content("Snowstorm: one frame of the animation", "The density comes from sys.argv; each frame is cleared, printed and held 0.2 s",
        [p1, p2],
        "snowstorm.py starts with a density of 4 percent and, when an argument is given, replaces it with "
        "int(sys.argv[1]), so python snowstorm.py 20 makes a heavier storm without touching the code; this run sets "
        "sys.argv to exactly that list. Two nested loops print 6 rows of 40 cells, each either a random half block "
        "or a space, with end='' so a row stays on one line, then two rows of full blocks for the ground. The "
        "chapter's program repeats this forever, clearing the terminal before each frame and pausing 0.2 seconds "
        "after it, a flipbook animation stopped with CTRL-C; this run prints one seeded frame so the slide can be "
        "checked. The same clear, print and pause loop makes the dashboard the chapter suggests.",
        "One argument changes the storm; clear, print and pause in a loop make it move.")

# ---- 16 story: McIlroy --------------------------------------------------------------------------------------------
content("Pipes, 1973: why a command should be quiet", STORY["McIlroyPipes1973"]["when"],
        [card("Doug McIlroy and Ken Thompson", "McIlroy proposed the pipe in a 1964 memo; in 1973 Thompson added "
              "pipes to Version 3 Unix in one night, and in 1978 McIlroy wrote: don't clutter output with extraneous "
              "information.", 0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "1964: McIlroy's memo proposes the pipe",
             "1973: Thompson adds pipe() to Version 3 Unix",
             "Version 4: the | notation",
             "1978: the maxims in the Bell System journal"]},
         factrow("McIlroyPipes1973")],
        story_notes("McIlroyPipes1973"),
        "Output may feed another program, so a command stays quiet unless asked.")

# ---- 17 sound, quiet and message boxes -----------------------------------------------------------------------------
content("Sound, quiet output and message boxes", "Say little by default; PyMsgBox can replace print() and input()",
        [{"t": "boxes", "x": 0.5, "y": 1.5, "w": 9.0, "h": 1.5, "cols": 3, "fs": 12, "subfs": 10, "accent": [1],
          "items": [{"label": "playsound3.playsound('hello.mp3')", "sub": "plays a sound and blocks until it ends"},
                    {"label": "--verbose  /  --quiet", "sub": "more output on request, or none; silence by default"},
                    {"label": "the exit code", "sub": "success or failure without a word of text"}]},
         {"t": "boxes", "x": 0.5, "y": 3.2, "w": 9.0, "h": 1.7, "cols": 4, "fs": 12, "subfs": 10, "accent": [],
          "items": [{"label": "pymsgbox.alert(text)", "sub": "waits for OK; returns 'OK'"},
                    {"label": "pymsgbox.confirm(text)", "sub": "returns 'OK' or 'Cancel'"},
                    {"label": "pymsgbox.prompt(text)", "sub": "returns the typed text, or None"},
                    {"label": "pymsgbox.password(text)", "sub": "the same, typing hidden by asterisks"}]}],
        "The playsound3 package plays an MP3 or WAV file and does not return until it ends, so a long sound halts the "
        "program for a while; sound can announce that a task finished, but it is easily overused and wasted on a "
        "muted computer. The same restraint applies to text: under the Unix philosophy a command prints only what "
        "another command could use, reports success or failure through its exit code, and offers --verbose for more "
        "or --quiet for none. For an occasional message or answer the PyMsgBox package shows small Tkinter dialogs "
        "whose functions mirror JavaScript's and block like input(). None of these ran on the machine that built "
        "this deck, which has no speaker and no display; the book's automateboringstuff3 package also pins the older "
        "playsound 1.3.0 rather than the playsound3 its prose teaches.",
        "Quiet by default, sound sparingly, a dialog box when there is no terminal.")

# ---- 18 launcher files ---------------------------------------------------------------------------------------------
c, bot = con("launcher", 0.5, 2.85, 9.0, fs=8, label="a launcher's mode, its first line, and a desktop entry read as key=value lines")
content("Launcher files on three systems", "A small text file per system activates the environment and runs the script",
        [{"t": "boxes", "x": 0.5, "y": 1.45, "w": 9.0, "h": 1.0, "cols": 3, "fs": 11.5, "subfs": 9, "accent": [2],
          "items": [{"label": "Windows: yourScript.bat", "sub": "@call activate.bat, @python ... %*, @pause; Run dialog"},
                    {"label": "macOS: yourScript.command", "sub": "source activate, python3 ...; chmod u+x; Spotlight"},
                    {"label": "Ubuntu: yourScript", "sub": "#!/usr/bin/env bash, source, python3; chmod u+x; Dash"}]},
         c],
        "Deployment puts each script in a Scripts folder on PATH, with one small launcher per operating system that "
        "activates the folder's virtual environment, runs the script with that environment's Python and deactivates. "
        "On Windows it is a batch file run from the Run dialog, on macOS a .command file run from Spotlight, and on "
        "Ubuntu a shell script with no extension, plus a .desktop file to reach it from Dash. On macOS and Linux "
        "chmod u+x adds the owner's execute bit, turning -rw-r--r-- into -rwxr--r--, and the Ubuntu launcher's first "
        "line, #!/usr/bin/env bash, names the program that reads the rest. The desktop entry is plain key=value text, "
        "and its Exec line must spell out /home/al because ~ is not expanded there.",
        "One launcher per system; chmod u+x and #! make it run on macOS and Linux.")

# ---- 19 story: Ritchie ----------------------------------------------------------------------------------------------
content("The #! line, announced on 10 January 1980", STORY["RitchieShebang1980"]["when"],
        [card("Dennis Ritchie, Bell Laboratories", "Ritchie added #! to the Unix kernel between Editions 7 and 8 and "
              "announced it by email: the rest of the first line names the interpreter. BSD carried it to "
              "everyone.", 0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "10 Jan 1980: Ritchie's email announces #!",
             "#! /bin/sh: a full path, no search",
             "2.8BSD, then on by default in 4.2BSD",
             "#!/usr/bin/env bash adds the PATH search"]},
         factrow("RitchieShebang1980")],
        story_notes("RitchieShebang1980"),
        "The launcher's first line is Ritchie's 1980 #!; env adds a PATH search.")

# ---- 20 the Ubuntu launcher, run ---------------------------------------------------------------------------------
p1, bot = prog("linuxLauncher_v1_0_0.py", 0.5, 1.5, 9.0, fs=8, lines=(4, 10), show_out=False)
p2 = transcript("linuxLauncher_v1_0_0.py", 0.5, bot + 0.38, 9.0, 4.95 - bot - 0.38, fs=9.5,
                label="prints: found on PATH, made executable, run by name - with and without \"$@\"")
content("The Ubuntu launcher, run", "The chapter's launcher has nothing after the script's path",
        [p1, p2],
        "This program carries out the chapter's Ubuntu deployment for real: a Scripts folder with a virtual "
        "environment, yourScript.py, and the launcher exactly as printed, with a plain hyphen where the online "
        "chapter's read line has an en dash, which bash rejects as not a valid identifier. After chmod u+x and with "
        "the folder on PATH, shutil.which finds the launcher and typing yourScript spam eggs runs it, inside the "
        "environment. But the script receives no arguments: the launcher's python3 line has nothing after the "
        "script's path, so spam and eggs are dropped, while a copy with \"$@\" added forwards both, as %* does in the "
        "Windows batch file. The chapter's macOS and Linux ccwd launchers have the same gap, so ccwd .. deployed "
        "there would copy the current folder, not its parent.",
        "Without \"$@\" (or %* on Windows) a launcher drops the typed arguments.")

# ---- 21 ccwd ----------------------------------------------------------------------------------------------------------
p1, bot = prog("ccwd_v1_0_0.py", 0.5, 1.5, 5.2, fs=9.5, lines=(6, 10), show_out=False)
c3 = card("No clipboard here", "A stand-in pyperclip.py with the same copy() and paste() keeps the text "
          "in a file; ccwd.py itself runs unchanged.", 5.9, 1.5, 3.6, 1.85, fs=11)
p2 = transcript("ccwd_v1_0_0.py", 0.5, 3.75, 9.0, 1.2, fs=10,
                label="prints: what ccwd copied, and where the shell that ran it still is")
content("ccwd: copying the current working directory", "Four lines; os.chdir moves only the program, never its terminal",
        [p1, p2, c3],
        "ccwd, short for copy current working directory, is four lines: import pyperclip, os and sys; change to "
        "sys.argv[1] if an argument was given; copy os.getcwd() to the clipboard. A short name like this is the "
        "chapter's advice for a command typed many times a day, checked first with which or where. Run from a bash "
        "shell sitting in ~/Scripts, it copied ~/Scripts, and with .. it copied the home folder, yet the shell's own "
        "pwd afterwards still printed ~/Scripts: every program has its own working directory, and os.chdir() moves "
        "only that one. The program prints nothing, so its batch file needs no @pause.",
        "ccwd .. copies the parent folder; the terminal that ran it stays where it was.")

# ---- 22 clipboard recorder ------------------------------------------------------------------------------------------
p1 = transcript("clipRecorder_v1_0_0.py", 0.5, 1.5, 9.0, 1.3, fs=10,
                label="transcript of program clipRecorder_v1_0_0.py: cliprec.py run unchanged")
c, bot = con("clipboard", 0.5, 3.13, 9.0, fs=8, label="print only what changed; 100 checks a second; CTRL-C is not an Exception")
content("Clipboard Recorder: polling and CTRL-C", "Print new clipboard text once; end quietly on KeyboardInterrupt",
        [p1, c],
        "cliprec.py turns copying many links into a two-step job: it reads the clipboard in an endless "
        "loop, prints the text only when it differs from previous_content, and sleeps 0.01 seconds between reads, "
        "a hundred checks a second instead of tens of thousands. The chapter's own program ran unchanged against a "
        "stand-in clipboard serving three links, two of them copied twice, and printed each once. The loop sits in a "
        "try block, and pressing CTRL-C raises KeyboardInterrupt, which the except clause catches with pass, so the "
        "program ends with exit code 0 and no traceback; the stand-in raises it when its links run out. "
        "KeyboardInterrupt derives from BaseException, not Exception, so a broad except Exception would let CTRL-C "
        "through, which is why the clause names it.",
        "Compare with the last text, sleep briefly, catch KeyboardInterrupt by name.")

# ---- 23 PyInstaller ----------------------------------------------------------------------------------------------------
c, bot = con("pyinstaller", 0.5, 1.5, 5.0, fs=11, label="the module's name has two capital letters")
content("PyInstaller: one file, a whole interpreter", "python -m PyInstaller --onefile yourScript.py builds one executable",
        [c,
         {"t": "stat", "x": 5.8, "y": 1.5, "w": 3.7, "h": 3.4, "vert": True, "items": [
             {"n": "12,950,120", "label": "bytes: dist/hello for a 23-byte Hello, world (Linux)"},
             {"n": "~15 s", "label": "to build with PyInstaller 6.22.3, Python 3.14.6"}]},
         card("Measured once, not on every build", "The numbers come from the chapter's research record: a build "
              "needs a download and fifteen seconds, too much to repeat each time this deck is made.", 0.5, bot + 0.1,
              5.0, 4.95 - bot - 0.1, fs=10.5)],
        "PyInstaller makes a program that runs on a computer without Python: python -m PyInstaller --onefile "
        "yourScript.py, with --onefile's two dashes and PyInstaller's two capital letters, since the lower-case "
        "module name fails exactly as this console shows. It leaves a build folder, which can be deleted, a .spec "
        "file and a dist folder with the executable. It does not compile to machine code: it packs a copy of the "
        "interpreter with the script, so the chapter's Hello, world is close to 8MB on Windows, and the build made "
        "for this course on Ubuntu was 12,950,120 bytes. PyInstaller builds only for the operating system and Python "
        "version it runs under, so a Windows executable needs a Windows build.",
        "PyInstaller bundles the interpreter: megabytes, built per system.")

# ---- 24 summary -----------------------------------------------------------------------------------------------------
content("The chapter in five lines", "One line for each part of the route",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.5, "fs": 11.5, "items": [
            "The terminal searches the PATH folders in order for a typed name; the first match runs.",
            "python -m venv .venv makes a separate Python; python -m pip fills it from PyPI.",
            "sys.argv, argparse, os.name and sys.exit let a program read its words and report back.",
            "A text program stays quiet by default, clears with cls or clear, and colours with Bext.",
            "A launcher on PATH or a PyInstaller build deploys it; \"$@\" or %* forwards the arguments."]}],
        "These five lines answer the route one part at a time. The first covers the terminal and PATH, the second "
        "virtual environments and pip, the third self-aware programs and command line arguments, the fourth "
        "text-based design, and the fifth deployment with launchers or PyInstaller, including the one gap in the "
        "chapter's macOS and Linux launchers. Together they answer the first question of the chapter, how a typed "
        "name becomes a running program, and the slides of each part answer the second, where the chapter's printed "
        "lines differ today.",
        "If a line feels unproven, its slides hold the example.")

# ---- 25 resources ----------------------------------------------------------------------------------------------------
def rows(kinds):
    return [[r["title"].split(":")[0] if "textbook" not in r["why"].lower() else "The textbook, chapter 12 - free online", r["url"]]
            for r in RES if r["kind"] in kinds and not r["url"].startswith("..")]


_docs = rows(("documentation",))
_peps = rows(("pep",))


def pick(*keys):
    out = []
    for k in keys:
        out.append(next(d for d in _docs + _peps if k.lower() in d[0].lower()))
    return out


_read = pick("textbook", "venv", "argparse")
_ref = pick("sys —", "pip documentation", "Using PyInstaller")
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9.5, "groups": [
            {"head": "Read", "rows": _read},
            {"head": "Reference", "rows": _ref},
            {"head": "History", "rows": [
                ["Pipeline (Unix), Wikipedia", STORY["McIlroyPipes1973"]["link"]],
                ["Shebang (Unix), Wikipedia", STORY["RitchieShebang1980"]["link"]],
                ["Norton Commander, Wikipedia", STORY["SochaNortonCommander1986"]["link"]],
                ["pip (package manager), Wikipedia", STORY["BickingPip2008"]["link"]]]}]}],
        "Every link on this slide was opened on the day the deck was made. The textbook chapter is free to read "
        "online and has every launcher file and both short programs in full, the venv and argparse documentation "
        "covers what this deck added to the chapter, and the reference links are the official pages behind sys.argv, "
        "sys.exit, python -m pip and PyInstaller's options. The history links are the sources behind the four stories "
        "of this chapter: pipes, the #! line, Norton Commander and pip.",
        "Textbook, documentation and history, opened the day this deck was built.")

# ---- 26 closing -------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "A typed name runs the first match in the PATH folders, never a subfolder.",
            "A virtual environment is a separate Python; activation puts it first on PATH.",
            "sys.argv holds the script name and the typed words; argparse checks and converts them.",
            "A launcher needs chmod u+x on macOS and Linux, and \"$@\" to forward arguments."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 13, "big": True,
          "items": ["%d rows run" % sum(len(v) for v in G.values()), "%d programs run" % len(PROGS),
                    "%d true stories" % len(ST.STORIES)]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the "
        "examples yourself, you have the chapter. The next chapter starts Part II of the book, with programs that "
        "fetch and read web pages, and every one of them can be deployed the way this chapter showed.",
        "Questions are welcome; bring one launcher that did not run and say why.")

# ---- agenda -----------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("The terminal and PATH", "The terminal: cd, pwd, dir and ls", "PATH: how the terminal finds a program"),
          ("Virtual environments and pip", "Virtual environments: python -m venv .venv", "pip: install, pin, list and uninstall"),
          ("Self-aware programs and command line arguments", "Self-aware programs: system and version", "argparse: when the arguments multiply"),
          ("Text-based design: output, the snowstorm, quiet commands and dialogs", "A text interface that felt like a desktop, 1986", "Sound, quiet output and message boxes"),
          ("Deploying: launchers, ccwd, the Clipboard Recorder and PyInstaller", "Launcher files on three systems", "PyInstaller: one file, a whole interpreter"),
          ("Summary and resources", "The chapter in five lines", "Where to go from here")]
_rows = []
for name, a, b in _parts:
    _rows.append("%s (slides %d-%d)" % (name, _t[a], _t[b]))
_ends = [_t[b] for _, _, b in _parts]
_starts = [_t[a] for _, a, _ in _parts]
if _starts[0] != 4 or any(_starts[i + 1] != _ends[i] + 1 for i in range(len(_parts) - 1)) or _ends[-1] != len(S) - 1:
    raise SystemExit("REFUSED: agenda ranges are not contiguous: %r %r (len S=%d)" % (_starts, _ends, len(S)))
_nconsole = sum(1 for s in S for i in s["items"] if i.get("t") in ("code", "prog"))
S[1]["items"] = [
    {"t": "numlist", "x": 0.5, "y": 1.5, "w": 6.3, "h": 3.4, "fs": 11, "items": _rows},
    {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
        {"n": str(len(S)), "label": "slides, numbered bottom-right"},
        {"n": str(len(ST.STORIES)), "label": "true stories, each with who, where, when and a link"},
        {"n": str(_nconsole), "label": "consoles and programs, all run before they were shown"}]}]
S[1]["sub"] = "Six parts; every range is a run of slides you can jump to"
S[1]["take"] = "Six parts, from a typed command to a deployed program."
S[1]["notes"] = ("The route has six parts. It starts with the terminal and the PATH variable that lets it find a "
                 "program, moves to virtual environments and pip, then to programs that know about themselves and read "
                 "their command line arguments, then to the design of a text interface, with the snowstorm animation, "
                 "and then to deployment with launcher files, the chapter's two short programs and PyInstaller, and "
                 "ends with the summary and resources. The ranges name the exact slides, so you can return to the part "
                 "you need, and four of the slides are true stories that explain where a piece of this chapter's "
                 "vocabulary came from.")

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
for s in S:
    for i in s["items"]:
        if i.get("t") == "bullets" and len(i["items"]) > 5:
            raise SystemExit("REFUSED: too many bullets on %r" % s["title"])
if not 20 <= len(S) <= 26:
    raise SystemExit("REFUSED: %d slides" % len(S))
plan = {"meta": {"title": "Chapter 12: Command Line Programs", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S)}, "slides": S}
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides")
