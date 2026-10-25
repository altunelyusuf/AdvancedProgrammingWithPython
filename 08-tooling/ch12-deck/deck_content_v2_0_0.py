"""Chapter 12 deck content, version 2.0.0: the words of the deck (analogies, stories, notes, take-aways, resources, tables).
Every concept label of the chapter research (sen0414_ch12_research_v1_0_2.ttl) has its everyday analogy here, under the research's own label, so the deck
check can find it; stories follow 5N1K with a dated, sourced account and a live link. Facts of the stories are those of 08-tooling/sen0414_ch12_stories_v1_0_0.py;
facts of the tables are the findings of the chapter research (03-materials/ch12/rdodi), named where they are used."""
__version__ = "2.0.0"

# ---- everyday analogies, grouped on the analogy slides: (slide id, title, headline analogy, [(research label or term, everyday picture)])
ANALOGIES = [
    ("A1", "Everyday pictures: starting a program", "The terminal is a drive-through window: you say a short order and the kitchen answers in text.", [
        ("A Program by Any Other Name", "One dish on many menus: dish, plate, course. Program, script and app name nearly the same thing."),
        ("Using the Terminal", "Speaking into the drive-through speaker: short orders, and the answer comes back as text."),
        ("Command line program", "A vending-machine button: you name the item and its options, and it does one job."),
    ]),
    ("A2", "Everyday pictures: environments and packages", "A virtual environment is a lunch box with its own compartments: what you pack stays apart from the shared kitchen.", [
        ("Virtual Environments", "A lunch box: your own compartments, so the shared kitchen stays untouched."),
        ("Installing Python Packages with pip", "An order form at the library: name the book and its edition, and it arrives on your shelf."),
    ]),
    ("A3", "Everyday pictures: programs that know themselves", "A self-aware program is a traveller who checks the weather and the passport before acting.", [
        ("Self-Aware Python Programs", "A traveller who reads the weather, the language and the passport before packing."),
        ("sys.argv", "The order slip: the words you wrote on it, in the order you wrote them."),
        ("argparse", "A form with labelled boxes: it fills in the blanks and refuses a wrong entry politely."),
        ("sys.exit", "A note on the door that says why the shop is closed, instead of a locked door and silence."),
    ]),
    ("A4", "Everyday pictures: how a program looks and sounds", "A text program is a shop window drawn in chalk: only characters, arranged to attract.", [
        ("Text-Based Program Design", "A road sign: short, readable at a glance, silent unless it matters."),
        ("Terminal presentation", "A chalk drawing on a pavement: only strokes, but colour and layout carry the message."),
        ("A Short Program: Snowstorm", "A flip book: clear the page, draw one frame, flip, and repeat."),
        ("os.system", "Passing a note through the kitchen hatch: Python writes the order, the shell cooks it."),
        ("chr", "A typewriter key: a number goes in, a character comes out."),
        ("bext.fg", "A coloured pen for the letters."),
        ("bext.bg", "A coloured sheet of paper behind the letters."),
        ("Pop-up Message Boxes with PyMsgBox", "A doorbell: it interrupts the person, so ring it only for what needs an answer."),
        ("playsound", "A kitchen timer: it announces the end with a sound instead of words."),
    ]),
    ("A5", "Everyday pictures: deploying", "Deploying is hanging a key on the hook by the door: anyone can reach the program by its name.", [
        ("Deploying Python Programs", "A key on a hook by the door: found by name, used with one move."),
        ("Deployment", "Moving a recipe into a food truck: the same dish, ready to serve at one tap."),
        ("A Short Program: Copying the Current Working Directory", "A courier who copies the address on the envelope: he moves, the sender stays at home."),
        ("A Short Program: Clipboard Recorder", "A security camera that logs a picture only when the scene changes."),
        ("Compiling Python Programs with PyInstaller", "A camping set that packs the stove with the food: heavier, but it needs nothing from the host."),
        ("Practice Program: Make Your Programs Deployable", "A tool belt: each tool you made earlier gets a loop, so you can grab it anywhere."),
    ]),
]

# ---- stories (5N1K): each box is one label and at most 30 words
STORIES = {
    "pipes": dict(title="Story: the pipe and the quiet command, 1973", img="photo_doug_mcilroy.jpg",
                  who="Doug McIlroy, head of the Computing Techniques Research Department at Bell Labs, and Ken Thompson.",
                  what="The pipe: the output of one program becomes the input of the next.",
                  when="McIlroy proposed it in a 1964 memo; Thompson added pipes to Version 3 Unix in 1973.",
                  where="Bell Labs, the birthplace of Unix.",
                  why="Each program should do one thing well and feed another, as yet unknown, program.",
                  how="The 1978 maxims add: do not clutter output. So a command stays quiet unless --verbose asks.",
                  link="https://en.wikipedia.org/wiki/Pipeline_(Unix)", linktext="Pipeline (Unix) (Wikipedia)"),
    "norton": dict(title="Story: a text screen that felt like a desktop, 1986", img="image_midnight_commander.png",
                   who="John Socha wrote it; Peter Norton Computing released it.",
                   what="Norton Commander, a file manager with two panels drawn with text characters.",
                   when="Begun in 1984 as Visual DOS; released in 1986; last MS-DOS version 5.51 on 1 July 1998.",
                   where="On MS-DOS, a plain text screen. The chapter shows it as Figure 12-1.",
                   why="A text interface can offer panels, menus, a viewer and an editor, and is simpler to program than a graphical one.",
                   how="Two file lists side by side, a command bar below, a viewer on F3 and an editor on F4.",
                   link="https://en.wikipedia.org/wiki/Norton_Commander", linktext="Norton Commander (Wikipedia)"),
    "pip": dict(title="Story: pip began as pyinstall, September 2008", img="image_pip_logo.png",
                who="Ian Bicking, the author of virtualenv; later Carl Meyer wrote PEP 405.",
                what="An installer called pyinstall, renamed pip, and then venv in the standard library.",
                when="Announced 24 September 2008, renamed pip on 28 October 2008; PEP 405 created 13 June 2011.",
                where="Ian Bicking's blog, then the Python Enhancement Proposals on python.org.",
                why="He wanted a better installer than easy_install, and isolated environments for every project.",
                how="PEP 405 credits virtualenv and put isolated environments into Python 3.3 as the venv module.",
                link="https://en.wikipedia.org/wiki/Pip_(package_manager)", linktext="pip (package manager) (Wikipedia)"),
    "shebang": dict(title="Story: the #! line, announced by email, 1980", img="photo_dennis_ritchie_2011.jpg",
                    who="Dennis Ritchie of Bell Laboratories.",
                    what="The #! line: if a file starts with these two characters, the rest of the line names the interpreter.",
                    when="In an email dated Thursday, 10 January 1980.",
                    where="Bell Laboratories, between Edition 7 and Edition 8 Unix; it reached users through Berkeley BSD.",
                    why="Scripts could then be run by name, like any program. His advice: put #! /bin/sh first.",
                    how="The kernel reads the line and starts the named program. The launcher's #!/usr/bin/env bash adds a PATH search.",
                    link="https://en.wikipedia.org/wiki/Shebang_(Unix)", linktext="Shebang (Unix) (Wikipedia)"),
}
STORY_NOTES = {
    "pipes": "Doug McIlroy proposed the pipe in 1964 and Ken Thompson built it in one night in 1973. The 1978 maxims say: do not clutter output. That is why a command is quiet by default. Ask: who reads your program's output?",
    "norton": "Norton Commander shipped in 1986 with two panels drawn only with characters. The chapter's Figure 12-1 shows it. Our snowstorm is the same idea with block characters. Ask students what else a text screen could show.",
    "pip": "Ian Bicking announced pyinstall on 24 September 2008 and renamed it pip a month later. PEP 405 then made virtual environments part of Python 3.3. The two commands of this part are his two ideas side by side.",
    "shebang": "Dennis Ritchie announced the hash-bang line by email on 10 January 1980. Our Ubuntu launcher starts with it. Ask students why the file needs no dot sh ending.",
}

# ---- speaker notes, short (at most 60 words each)
NOTES = {
    "title": "Welcome. This chapter follows a typed command to a running program: the terminal, PATH, a virtual environment, the arguments, the look of the output, and the launcher. Every code slide shows the code, a plain explanation and the result drawn as a table, chart or diagram.",
    "route": "Five parts: starting a program, isolating it, letting it read its surroundings, designing its text output, and deploying it. Each code slide has its place in the chapter-code tab of the page, in this same order.",
    "questions": "Two questions to carry through the chapter. How does a typed command become a running program, and how does the program learn what it was given? And which outputs and launchers of the book differ in current Python?",
    "divider1": "Part one. Programs have many names. The terminal finds a program by searching the folders of PATH, from left to right. Predict which folder wins before you read the result.",
    "divider2": "Part two. A virtual environment keeps one project's packages apart from the rest. pip installs into exactly the Python you name. Notice how little a venv really is: a folder and a file.",
    "divider3": "Part three. A program can ask about its system, its version and its file, and it can read the words after its name. argparse does that reading for you and refuses wrong input.",
    "divider4": "Part four. A text program is designed for being typed and read. Quiet by default, colour by escape code, block characters for pictures. The snowstorm puts them together.",
    "divider5": "Part five. A program becomes a command when a launcher sits in a PATH folder. We build the Ubuntu launcher, two small programs that touch the system, and a bundle with PyInstaller.",
    "A1": "A drive-through is a good picture for the terminal: short orders, text answers. A command line program is a button on a vending machine. Ask students to add one more everyday picture of their own.",
    "A2": "A lunch box keeps your food apart from the shared kitchen, just as a virtual environment keeps your packages apart. Pip is the order form for new packages.",
    "A3": "Four small ideas. The program checks its surroundings, reads the words it was given, lets argparse fill the form, and leaves a clear note when it must stop.",
    "A4": "Text design in nine pictures. Notice that the pop-up and the sound are the two ways to interrupt a person. Use them only when you must.",
    "A5": "Deploying means reachable by name. Ccwd and the recorder are two tiny programs that touch the system. PyInstaller packs the interpreter along, so the file is large.",
    "vocab": "Seven words for nearly the same thing. A script is run from source by an interpreter. A command is a program you start from a terminal. Ask students which word fits their last project.",
    "terminal_cd": "The terminal commands cd and pwd have Python twins: os.chdir and os.getcwd. We run them in a throw-away folder. Predict what pwd prints inside Desktop.",
    "terminal_ls": "Ls and dir have one twin: os.listdir. The filter keeps names that end in dot exe, like dir star dot exe. Predict how many names each command shows.",
    "path_text": "PATH is just text. The terminal splits it at the colons and tries the folders in order. A folder put first wins. Predict the number of folders before you run it.",
    "path_which": "Shutil.which does the same walk the terminal does and returns the first hit. Who wins when two folders hold spam? And what does it return when nothing matches?",
    "venv_cfg": "A virtual environment is a folder with a small settings file and three parts: bin, lib and pyvenv.cfg. Each line of the file is one setting, so a dictionary can read it.",
    "venv_activate": "Activate only changes PATH, for one terminal window. The test sys.prefix not equal to sys.base_prefix tells a program whether it runs inside an environment.",
    "pip": "Pip pins a version with two equals signs. Run pip as python dash m pip, so it installs into the Python you mean. Find_spec asks whether a module can be imported before you try.",
    "selfaware": "A program can ask which family of system, which Python version and whether it came from a file. Dunder file is an absolute path since Python 3.9. Predict each answer.",
    "missingmod": "Catch ModuleNotFoundError and explain in your own words. Sys.exit with a text ends the program, prints the text to standard error and gives exit code 1. Here we catch it to show the value.",
    "argv": "The shell splits the line into words, and quotation marks keep two words together. Sys.argv holds the words, with the script name first. Predict the length of each list.",
    "argparse_a": "Once arguments multiply, declare them once with argparse. It converts types and fills in defaults. Predict the density for the second run.",
    "argparse_b": "A word that is not a number is refused by the int conversion. Argparse turns that into one clear message. In a terminal the exit code would be 2.",
    "quiet": "Quiet by default is the Unix habit. The minus v switch asks for more and minus q for none. The bars show how many lines each mode prints.",
    "chr": "Os.system hands a text to the shell. Cls on Windows, clear elsewhere. Chr turns a number into a character. The three block characters are the snow and the ground.",
    "colour": "Bext sets colours with names, but the terminal receives escape codes: 30 to 37 for text, 40 to 47 for background. This stand-in builds the same codes. Zero resets.",
    "snowstorm": "The snowstorm decides cell by cell whether there is snow. The density comes from the argument. The book clears the screen and repeats the frame; we print one seeded frame and count the flakes.",
    "tools": "Three of these helpers are not in the standard library. Pymsgbox needs Tkinter, bext needs a terminal and playsound needs a sound system. That is why the page does not run them.",
    "launchers": "One idea, three spellings. Windows uses a bat file and percent star. macOS and Linux use a shell script and dollar at in quotes. Forward the arguments, or the script never sees them.",
    "launcher_text": "The launcher starts with the hash-bang line, activates the environment and runs the script with all its arguments. Three lines, three jobs.",
    "launcher_chmod": "Chmod u plus x is what makes the file a command: the owner gets the x bit. Which then finds it by its bare name on PATH.",
    "desktop": "A desktop file is a small settings file. Configparser reads it. The Exec line is the launcher, wrapped in a terminal window so that the user sees the output.",
    "ccwd": "Os.chdir changes the folder of the running program only. The terminal that started it stays where it was. That is the chapter's point, and why ccwd copies the folder instead of moving there.",
    "cliprec": "The recorder polls again and again and prints only what changed. Control-C raises KeyboardInterrupt, which is not an Exception, so the except clause names it. It ends quietly.",
    "pyinstaller": "Pyinstaller needs its capital letters and two dashes. Python dash m Pyinstaller dash dash onefile builds one executable. It leaves build, dist and a spec file.",
    "pyinfo": "Pyinstaller packs a copy of the interpreter with the script, so even Hello world is megabytes. The output belongs to one operating system and one Python version. Mail providers may block it.",
    "deployable": "The practice program turns four old projects into commands. One template serves all. The only change per project is its name in the third line.",
    "current": "Python moves on. Dunder file is absolute since 3.9. No setuptools in new environments since 3.12. Python 3.13 adds a gitignore file. Python 3.14 colours argparse help. PEP 668 blocks pip in system Python.",
    "summary": "Five sentences to keep. The chart counts the code examples in each part of this deck.",
    "practice": "Four drills. Predict first, then run what you can on the page. Ask students to explain each answer in one sentence.",
    "resources": "Start with the book chapter, then the Python documentation, the two PEPs and the pip and PyInstaller manuals. The stories link to first-hand sources. Choose one link and read it before the next class.",
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

# ---- tables of the non-code slides
VOCAB = [["Word", "What it means", "Starts how"],
         ["program", "Instructions a computer runs", "any of the ways below"],
         ["script", "A program an interpreter runs from its source", "python yourScript.py"],
         ["command", "A program started from a terminal, set by arguments", "ls, dir, cd, cp"],
         ["shell script", "A text file of terminal commands", "a launcher file"],
         ["application", "A program with a window of its own", "a double click"],
         ["app", "An application on a phone or tablet", "a tap"],
         ["web app", "A program that runs on a server, used in a browser", "an address"]]

TOOLS = [["Helper", "What it does", "Comes with Python?"],
         ["os.system", "Hands a text to the shell, such as clear", "Yes: the os module"],
         ["chr", "Turns a number into a character", "Yes: a built-in"],
         ["bext.fg and bext.bg", "Set the text and the background colour", "No: pip install bext"],
         ["Pop-up Message Boxes with PyMsgBox", "alert, confirm, prompt and password dialogs", "No: needs Tkinter"],
         ["playsound", "Plays an MP3 or WAV file and waits for the end", "No: playsound3"]]

LAUNCHERS = [["System", "Launcher file", "Forwards the arguments with"],
             ["Windows", "yourScript.bat in a PATH folder: @call activate.bat, @python script, @pause", "%*"],
             ["macOS", "yourScript.command: a shell script, made executable with chmod u+x", "\"$@\""],
             ["Ubuntu", "yourScript: a shell script with #!/usr/bin/env bash, plus a .desktop entry", "\"$@\""]]

CURRENT = [["What changed", "Since", "What it means for the chapter"],
           ["__file__ of a script is an absolute path", "3.9", "Path(__file__).parent finds files beside the program"],
           ["setuptools is no longer pre-installed in a venv", "3.12", "pip list shows only pip in a fresh environment"],
           ["A new venv holds a .gitignore file", "3.13", "The environment folder is not committed by mistake"],
           ["argparse colours its help text and can suggest a choice", "3.14", "Usage messages are easier to read"],
           ["System Python is marked externally managed (PEP 668)", "Ubuntu 24.04", "pip install there stops with an error: use a venv"],
           ["Bext hides the cursor with hide_cursor and show_cursor", "Bext 0.1.1", "The chapter lists hide and show"],
           ["automateboringstuff3 requires playsound 1.3.0", "2024.10.1", "The chapter's prose names playsound3"]]

SUMMARY_POINTS = ["A program is started by a terminal that searches PATH.",
                  "A virtual environment keeps the packages of one project apart.",
                  "The program reads sys.argv; argparse parses it for you.",
                  "Text design: quiet by default, colour by escape code.",
                  "A launcher in a PATH folder, or PyInstaller, deploys it."]

PRACTICE = ["Add /home/al/Scripts to the front of PATH. Which folder does shutil.which search first?",
            "What does shlex.split give for 'python3 snow.py \"big storm\" 20'? How long is argv?",
            "Add a --density option to the argparse example with a default of 4 and a type of int.",
            "Write the launcher line that forwards arguments, and say why the chapter's own line forwards none."]

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
