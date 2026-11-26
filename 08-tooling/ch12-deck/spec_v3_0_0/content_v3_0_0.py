"""Chapter 12 deck content, version 3.0.0: the words of the deck for the generic builder (parts, plan, route, questions, plain meanings, stories, take-aways, tables, summary, practice, resources).
The chapter's content is that of deck 2.0.0 (deck_content_v2_0_0.py and the plan and parts of the chapter's own builder deck_build_v2_0_0.py); what the rulings force is changed: the everyday pictures
become plain meanings (no analogy anywhere; the box label is IN SHORT), the four stories are the same stories with the same facts and links, told as prose in paragraphs of at most 30 words, the
launchers and the vocabulary are tables without a picture, and the PyInstaller slide keeps its native chart. The notes are notes_v3_0_0.py."""
__version__ = "3.0.0"

BOX_LABEL = "IN SHORT"
TABLE_HEAD = "In short"
CONCEPTS_TAIL = "each with a plain meaning"

PARTS = {
    1: ("Part 1: Starting a program", "From a typed word to a running program: names, the terminal and PATH", [
        ("Program names", "Script, command and app name nearly the same thing."),
        ("Terminal", "A text window where you type short commands."),
        ("cd, pwd, ls", "Move, show the place, and list what is there."),
        ("PATH", "The list of folders searched, in order, for a program."),
    ]),
    2: ("Part 2: Isolating a program", "A virtual environment keeps one project's packages apart; pip fills it", [
        ("Virtual environment", "A folder that keeps one project's packages apart."),
        ("activate", "Puts the environment's folder first on PATH."),
        ("pip", "Installs packages into exactly the Python you name."),
        ("Version pin", "Two equals signs fix the version that is installed."),
    ]),
    3: ("Part 3: Programs that look around", "A program asks about its system and reads the words it was given", [
        ("os.name", "Tells which family of operating system runs the program."),
        ("sys.version_info", "Lets the program refuse a Python that is too old."),
        ("sys.argv", "The words typed after the name of the program."),
        ("argparse", "Declares the arguments once and checks them."),
    ]),
    4: ("Part 4: Designing the terminal output", "Quiet by default, characters for pictures, escape codes for colour", [
        ("Quiet default", "Print little, so that another program can read it."),
        ("chr and ord", "Convert between numbers and characters."),
        ("Escape codes", "Numbered signals that colour the text."),
        ("Snowstorm", "A flip-book animation drawn with block characters."),
    ]),
    5: ("Part 5: Deploying a program", "A launcher in a PATH folder, two small system programs, and a bundle", [
        ("Launcher", "A script in a PATH folder that starts the program."),
        ("chmod u+x", "Gives the owner the right to run the file."),
        ("ccwd, recorder", "Two small programs that touch the system."),
        ("PyInstaller", "Packs the interpreter and the script into one file."),
    ]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("compare", "vocab"), ("code", "terminal_cd"), ("code", "terminal_ls"), ("code", "path_text"), ("code", "path_which"),
        ("divider", 2), ("analogy", "A2"), ("code", "venv_cfg"), ("code", "venv_activate"), ("code", "pip"), ("story", "pip"),
        ("divider", 3), ("analogy", "A3"), ("code", "selfaware"), ("code", "missingmod"), ("code", "argv"), ("code", "argparse_a"), ("code", "argparse_b"),
        ("divider", 4), ("analogy", "A4"), ("code", "quiet"), ("story", "pipes"), ("story", "norton"), ("code", "chr"), ("code", "colour"), ("compare", "helpers"), ("code", "snowstorm"),
        ("divider", 5), ("analogy", "A5"), ("compare", "launchers"), ("code", "launcher_text"), ("code", "launcher_chmod"), ("story", "shebang"), ("code", "desktop"), ("code", "ccwd"), ("code", "cliprec"),
        ("code", "pyinstaller"), ("compare", "pyinfo"), ("code", "deployable"),
        ("current",), ("summary",), ("practice",), ("resources",)]

ROUTE_RUNS = {1: "cd, pwd, ls as os calls; PATH and which", 2: "pyvenv.cfg, activate, pip pins", 3: "os.name, version, sys.argv, argparse",
              4: "quiet mode, chr, escape codes, snowstorm", 5: "launcher, ccwd, recorder, PyInstaller"}

ROUTE_TAIL = ("Changes, summary, practice, resources", "what current Python adds")

QUESTIONS = [("1", "How does a typed command become a running program, and how does the program learn what it was given?",
              "Answer on slides %d to %d: PATH, the launcher, sys.argv and argparse.", [("code", "path_text"), ("code", "argparse_b")]),
             ("2", "Which printed outputs and launchers of the book differ in current Python or on a current system?",
              "Answer on slide %d: the changes, from the chapter research.", [("current",)])]

QUESTIONS_TAKEAWAY = "The terminal searches PATH; the program reads its arguments."

ANALOGIES = [
    ("A1", "In short: starting a program", "A program is started from a terminal, which finds it by searching the folders of PATH.", [
        ("A Program by Any Other Name", "Program, script and app name nearly the same thing; the words differ by how it is started."),
        ("Using the Terminal", "A text window where you type a short command and read the text that comes back."),
        ("Command line program", "A program that you start by name, with its options, and that does one job."),
    ]),
    ("A2", "In short: environments and packages", "A virtual environment keeps one project's packages apart from the rest of the system.", [
        ("Virtual Environments", "A folder with its own packages, so other projects and the system Python stay untouched."),
        ("Installing Python Packages with pip", "Names a package and its version and installs it into the Python you name."),
    ]),
    ("A3", "In short: programs that know themselves", "A program can ask where and on what it runs, and can read the words it was given.", [
        ("Self-Aware Python Programs", "A program that reads its system, its Python version and its file before it acts."),
        ("sys.argv", "The words typed after the program's name, in order, with the script's name first."),
        ("argparse", "Declares the arguments once, converts their types, fills defaults and refuses a wrong entry with a clear message."),
        ("sys.exit", "Ends the program and, given a text, prints it to standard error with exit code 1."),
    ]),
    ("A4", "In short: how a program looks and sounds", "A text program is designed to be typed and read: quiet by default, with characters and codes for the look.", [
        ("Text-Based Program Design", "Short output, readable at a glance, silent unless something matters."),
        ("Terminal presentation", "Layout and colour made only of characters and escape codes."),
        ("A Short Program: Snowstorm", "Clears the screen, draws one frame of block characters, and repeats."),
        ("os.system", "Hands a text to the shell to run, for example clear or cls."),
        ("chr", "Turns a number into the character that has that number."),
        ("bext.fg", "Sets the colour of the letters by name."),
        ("bext.bg", "Sets the colour behind the letters by name."),
        ("Pop-up Message Boxes with PyMsgBox", "Opens a window that asks the person for an answer; it interrupts, so use it only when an answer is needed."),
        ("playsound", "Plays a sound file and waits until it ends."),
    ]),
    ("A5", "In short: deploying a program", "Deploying makes a program reachable by its name from any folder.", [
        ("Deploying Python Programs", "Putting a launcher in a PATH folder, so that the program is found by name."),
        ("Deployment", "Moving a finished program to where it will be used, ready to start in one step."),
        ("A Short Program: Copying the Current Working Directory", "Copies the folder the terminal is in; os.chdir moves only the program, never the terminal."),
        ("A Short Program: Clipboard Recorder", "Checks the clipboard again and again and prints it only when it has changed."),
        ("Compiling Python Programs with PyInstaller", "Packs the interpreter with the script into one file that needs nothing installed, and is larger."),
        ("Practice Program: Make Your Programs Deployable", "Gives each earlier program a launcher, so that each runs from any folder."),
    ]),
]

STORIES = {
    "pip": dict(title="Story: pip began as pyinstall, September 2008", img="image_pip_logo.png",
                prose=["On 24 September 2008 Ian Bicking, the author of virtualenv, announced an installer called pyinstall on his blog.",
                       "He renamed it pip on 28 October 2008, wanting a better installer than easy_install and isolated environments.",
                       "Carl Meyer wrote PEP 405, created on 13 June 2011, which credits virtualenv and put isolated environments into Python 3.3 as venv.",
                       "python -m venv and pip install are those two ideas."],
                link="https://en.wikipedia.org/wiki/Pip_(package_manager)", linktext="pip (package manager) (Wikipedia)"),
    "pipes": dict(title="Story: the pipe and the quiet command, 1973", img="photo_doug_mcilroy.jpg",
                  prose=["In a 1964 memo, Doug McIlroy, head of the Computing Techniques Research Department at Bell Labs, proposed that programs should be coupled, the output of one feeding the next.",
                         "In 1973 Ken Thompson added pipes to Version 3 Unix at Bell Labs, the birthplace of Unix.",
                         "Each program should do one thing well and feed another, as yet unknown, program; the 1978 maxims add that output should not be cluttered.",
                         "So a command stays quiet unless --verbose asks, and the backup example of this part follows that rule."],
                  link="https://en.wikipedia.org/wiki/Pipeline_(Unix)", linktext="Pipeline (Unix) (Wikipedia)"),
    "norton": dict(title="Story: a text screen that felt like a desktop, 1986", img="image_midnight_commander.png",
                   prose=["John Socha began Norton Commander in 1984 as Visual DOS, and Peter Norton Computing released it in 1986.",
                          "On MS-DOS it drew two file lists side by side, a command bar below, a viewer on F3 and an editor on F4, all with plain text characters.",
                          "A text interface can offer panels, menus, a viewer and an editor, and it is simpler to program than a graphical one.",
                          "The last MS-DOS version, 5.51, came out on 1 July 1998; the chapter shows it as Figure 12-1, and the snowstorm uses block characters in the same way."],
                   link="https://en.wikipedia.org/wiki/Norton_Commander", linktext="Norton Commander (Wikipedia)"),
    "shebang": dict(title="Story: the #! line, announced by email, 1980", img="photo_dennis_ritchie_2011.jpg",
                    prose=["In an email dated Thursday, 10 January 1980, Dennis Ritchie of Bell Laboratories announced the #! line.",
                           "If a file starts with these two characters, the rest of the first line names the interpreter that runs it.",
                           "It came between Edition 7 and Edition 8 Unix and reached users through Berkeley BSD; scripts could then be run by name, as any program is.",
                           "His advice was to put #! /bin/sh first; the kernel reads the line and starts the named program, and the launcher's #!/usr/bin/env bash adds a PATH search."],
                    link="https://en.wikipedia.org/wiki/Shebang_(Unix)", linktext="Shebang (Unix) (Wikipedia)"),
}

TAKEAWAY = {
    "terminal_cd": "cd and pwd have twins in os.", "terminal_ls": "ls and dir have one twin: os.listdir.", "path_text": "PATH is text; the first folder with the name wins.", "path_which": "shutil.which walks PATH like the terminal.",
    "venv_cfg": "A venv is a folder and a settings file.", "venv_activate": "activate edits PATH for one terminal.", "pip": "Pin with ==; ask find_spec before you import.",
    "selfaware": "A program can ask where and on what it runs.", "missingmod": "Say what is missing; leave with a message.",
    "argv": "The shell cuts the words; argv keeps them.", "argparse_a": "Declare once; argparse parses and fills defaults.", "argparse_b": "A wrong word is refused with a clear message.",
    "quiet": "Quiet by default; -v for more, -q for none.", "chr": "chr: number to character; os.system: text to the shell.",
    "colour": "A colour name becomes an escape code.", "snowstorm": "Cell by cell: snow or space.",
    "launcher_text": "Three lines: interpreter, environment, program.", "launcher_chmod": "chmod u+x turns a file into a command.", "desktop": "A .desktop file puts the launcher in the menu.",
    "ccwd": "os.chdir moves only the program.", "cliprec": "Poll, print what changed, stop on CTRL-C.",
    "pyinstaller": "-m and --onefile; the build leaves three things.", "deployable": "One template, four commands.",
}

COMPARES = {
    "vocab": dict(title="A Program by Any Other Name", sub="Seven words for nearly the same thing",
                  rows=[["Word", "What it means", "Starts how"],
                        ["program", "Instructions a computer runs", "any of the ways below"],
                        ["script", "A program an interpreter runs from its source", "python yourScript.py"],
                        ["command", "A program started from a terminal, set by arguments", "ls, dir, cd, cp"],
                        ["shell script", "A text file of terminal commands", "a launcher file"],
                        ["application", "A program with a window of its own", "a double click"],
                        ["app", "An application on a phone or tablet", "a tap"],
                        ["web app", "A program that runs on a server, used in a browser", "an address"]],
                  colw=[1.7, 4.6, 2.7], rowh=0.45, fs=12, takeaway="A script is run from source; a command is started from a terminal."),
    "helpers": dict(title="Pop-ups, sound and colour: the helpers", sub="Most are third-party packages; the page does not run them",
                    rows=[["Helper", "What it does", "Comes with Python?"],
                          ["os.system", "Hands a text to the shell, such as clear", "Yes: the os module"],
                          ["chr", "Turns a number into a character", "Yes: a built-in"],
                          ["bext.fg and bext.bg", "Set the text and the background colour", "No: pip install bext"],
                          ["Pop-up Message Boxes with PyMsgBox", "alert, confirm, prompt and password dialogs", "No: needs Tkinter"],
                          ["playsound", "Plays an MP3 or WAV file and waits for the end", "No: playsound3"]],
                    colw=[2.6, 4.0, 2.4], rowh=0.55, fs=12, takeaway="Check the package name before you install: the chapter and PyPI differ."),
    "launchers": dict(title="Launcher files on three systems", sub="One idea in three spellings",
                      rows=[["System", "Launcher file", "Forwards the arguments with"],
                            ["Windows", "yourScript.bat in a PATH folder: @call activate.bat, @python script, @pause", "%*"],
                            ["macOS", "yourScript.command: a shell script, made executable with chmod u+x", "\"$@\""],
                            ["Ubuntu", "yourScript: a shell script with #!/usr/bin/env bash, plus a .desktop entry", "\"$@\""]],
                      colw=[1.2, 5.6, 2.2], rowh=0.7, fs=12, takeaway="Forward the arguments, or the script never receives them."),
    "pyinfo": dict(title="PyInstaller: what the one file costs", sub="Measured in the chapter research with PyInstaller 6.22.3 and Python 3.14.6",
                   chart=dict(label="size of the Hello, world executable, in megabytes", cats=["Measured on Ubuntu", "The chapter's text (Windows)"], series="megabytes", values=[12.95, 8.0], vmax=16, major=4),
                   rows=[["Fact", "Value"], ["Source file", "23 bytes"], ["Executable (Ubuntu)", "12,950,120 bytes"], ["Build time", "about 15 seconds"], ["Leaves", "build, dist, a spec file"], ["Works on", "one system, one Python"]],
                   colw=[1.6, 2.0], rowh=0.45, fs=11, takeaway="PyInstaller packs a copy of the interpreter with your script."),
}

CURRENT_SUB = "What differs from the book, from the chapter research"

CURRENT = [["What changed", "Today", "Example"],
           ["__file__ of a script is an absolute path (since 3.9)", "Path(__file__).parent finds files beside the program", "selfaware"],
           ["setuptools is no longer pre-installed in a venv (since 3.12)", "pip list shows only pip in a fresh environment", "venv_cfg"],
           ["A new venv holds a .gitignore file (since 3.13)", "The environment folder is not committed by mistake", "venv_cfg"],
           ["argparse colours its help text and can suggest a choice (since 3.14)", "Usage messages are easier to read", "argparse_b"],
           ["System Python is marked externally managed (PEP 668, Ubuntu 24.04)", "pip install there stops with an error: use a venv", "pip"],
           ["Bext hides the cursor with hide_cursor and show_cursor (Bext 0.1.1)", "The chapter lists hide and show", "colour"],
           ["automateboringstuff3 requires playsound 1.3.0 (2024.10.1)", "The chapter's prose names playsound3", ""]]

CURRENT_TAKEAWAY = "Run what the book printed; then check what changed."

SUMMARY_ANALOGY = "A summary keeps only the five ideas you need to take away from the lecture."

SUMMARY_POINTS = ["A program is started by a terminal that searches PATH.",
                  "A virtual environment keeps the packages of one project apart.",
                  "The program reads sys.argv; argparse parses it for you.",
                  "Text design: quiet by default, colour by escape code.",
                  "A launcher in a PATH folder, or PyInstaller, deploys it."]

SUMMARY_TAKEAWAY = "The terminal searches PATH; the program reads its arguments."

PRACTICE_SUB = "Predict first, then run what you can on the chapter page"

PRACTICE_ANALOGY = "Practice questions are short drills: predict the answer first, then run the code."

PRACTICE = ["Add /home/al/Scripts to the front of PATH. Which folder does shutil.which search first?",
            "What does shlex.split give for 'python3 snow.py \"big storm\" 20'? How long is argv?",
            "Add a --density option to the argparse example with a default of 4 and a type of int.",
            "Write the launcher line that forwards arguments, and say why the chapter's own line forwards none."]

PRACTICE_TAKEAWAY = "Each answer fits in a few lines you can run."

RESOURCES_SUB = "Reading and watching, chosen for this chapter; every link is live"

RESOURCES_TAKEAWAY = "Pick one link and read it before the next class."

RESOURCES = [
    ("Book: Automate the Boring Stuff, 3rd edition, chapter 12", "https://automatetheboringstuff.com/3e/chapter12.html", "automatetheboringstuff.com"),
    ("Python documentation: sys, system-specific parameters", "https://docs.python.org/3/library/sys.html", "docs.python.org"),
    ("Python documentation: os, operating system interfaces", "https://docs.python.org/3/library/os.html", "docs.python.org"),
    ("Python documentation: argparse", "https://docs.python.org/3/library/argparse.html", "docs.python.org"),
    ("Python documentation: venv", "https://docs.python.org/3/library/venv.html", "docs.python.org"),
    ("Python documentation: shutil.which and shlex.split", "https://docs.python.org/3/library/shutil.html", "docs.python.org"),
    ("PEP 405: Python Virtual Environments", "https://peps.python.org/pep-0405/", "peps.python.org"),
    ("PEP 668: externally managed environments", "https://peps.python.org/pep-0668/", "peps.python.org"),
    ("pip user guide: running pip as python -m pip", "https://pip.pypa.io/en/stable/user_guide/", "pip.pypa.io"),
    ("PyInstaller manual: using PyInstaller", "https://pyinstaller.org/en/stable/usage.html", "pyinstaller.org"),
    ("Bext on the Python Package Index", "https://pypi.org/project/Bext/", "pypi.org"),
    ("PyMsgBox on the Python Package Index", "https://pypi.org/project/PyMsgBox/", "pypi.org"),
    ("Video: AT&T Archives, The UNIX Operating System (1982)", "https://www.youtube.com/watch?v=tc4ROCJYbm0", "youtube.com"),
    ("Pipeline (Unix) on Wikipedia", "https://en.wikipedia.org/wiki/Pipeline_(Unix)", "wikipedia.org"),
]
