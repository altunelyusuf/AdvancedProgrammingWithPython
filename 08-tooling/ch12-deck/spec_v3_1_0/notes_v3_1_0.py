"""Chapter 12 deck speaker notes, version 3.1.0: READER notes (handover of 2026-11-19, practice 3). The slides are handed to students together with their notes, so each note explains the slide's short wording in
fuller sentences, adds detail that the slide does not carry, and connects the slide to related slides and chapters. A note gives no direction to a presenter, has no think-of statement, no prompt marker, no
lambda and no everyday picture. The facts are those of the chapter's examples, of their runs and of the chapter research of deck 2.0.0. RESULT_SAYS: for each code slide, the first result balloon (what the run showed).
Slide numbers: 1 title, 2 route, 3 questions, 4 part 1, 5 A1, 6 vocab, 7 terminal_cd, 8 terminal_ls, 9 path_text, 10 path_which, 11 part 2, 12 A2, 13 venv_cfg, 14 venv_activate, 15 pip, 16 pip story, 17 part 3, 18 A3,
19 selfaware, 20 missingmod, 21 argv, 22 argparse_a, 23 argparse_b, 24 part 4, 25 A4, 26 quiet, 27 pipes story, 28 norton story, 29 chr, 30 colour, 31 helpers, 32 snowstorm, 33 part 5, 34 A5, 35 launchers,
36 launcher_text, 37 launcher_chmod, 38 shebang story, 39 desktop, 40 ccwd, 41 cliprec, 42 pyinstaller, 43 pyinfo, 44 deployable, 45 current, 46 summary, 47 practice, 48 resources."""
__version__ = "3.1.0"

NOTES = {
    "title": "This chapter of the book, Command-Line Programs, explains how a program is started from a terminal, how it finds its files, its Python and its arguments, how it prints to the screen, and how it is "
             "installed so that it starts by name from any folder. The deck has twenty-three code examples that run on the chapter page, four true stories about the tools, and a table or chart where a comparison helps. "
             "Slide 2 lays out the five parts. Chapter 11 comes before it with files and folders, and chapter 13 follows with web scraping.",
    "route": "The table is the map of the chapter. Each row is one of the five parts, with the slides it covers and what you will run in it. The last row covers the changes against the book, the summary, the practice "
             "questions and the links. The same twenty-three examples are listed in the Slide code tab of the chapter page, in this order, so a slide and its tab can be opened side by side. Part 1 starts on slide 4, "
             "and each later part begins with a divider slide that names its four ideas.",
    "questions": "Two questions run through the chapter, and the deck answers them at the end. The first asks how a typed command becomes a running program and how the program learns what it was given; the answer is "
                 "the PATH list on slide 9 and the argument list on slides 21 to 23. The second asks where the book's printed outputs and launchers differ from current Python or from a current system; slide 45 lists "
                 "those changes from the chapter research. Keeping both questions in mind makes each later slide easier to place.",
    "divider1": "Part 1 is about starting a program. The terminal is a text window; its commands cd, pwd and ls move, show the place and list the files; and PATH is the list of folders that the terminal searches, in order, "
                "for the name you typed. The four cards are the ideas of the part. Slides 5 to 10 cover them, and part 5 later puts a launcher into one of those PATH folders.",
    "divider2": "Part 2 is about keeping one project's packages apart. A virtual environment is a folder with its own Python settings and packages; activate puts that folder first on PATH; pip installs packages into exactly the "
                "Python you name; and two equals signs pin a version. The four cards are the ideas of the part. Slides 12 to 16 cover them, and part 1 earlier explains the PATH that activate edits.",
    "divider3": "Part 3 is about programs that look around before they act. os.name tells the family of operating system, sys.version_info tells the Python version, sys.argv holds the words typed after the program's name, and "
                "argparse declares those words once and checks them. The four cards are the ideas of the part. Slides 18 to 23 cover them, and part 4 uses the same arguments to make a program quiet or talkative.",
    "divider4": "Part 4 is about how a text program looks. It prints little by default, so that another program can read its output; chr and ord convert between numbers and characters; escape codes colour the text; and the "
                "snowstorm draws an animation from block characters. The four cards are the ideas of the part. Slides 25 to 32 cover them, and part 3 earlier gives the arguments that switch the output on or off.",
    "divider5": "Part 5 is about deploying a program. A launcher is a small script in a PATH folder that starts your program; chmod u+x gives the owner the right to run a file; ccwd and the clipboard recorder are two small "
                "programs that touch the system; and PyInstaller packs the interpreter and the script into one file. The four cards are the ideas of the part. Slides 34 to 44 cover them, and part 1 earlier explains PATH.",
    "A1": "A program is started from a terminal, and the terminal finds it by searching the folders of PATH. The cards give a plain meaning to each idea. A program, a script and a command are nearly the same thing, and the "
          "words differ by how the program is started. The terminal is a text window for short commands. A command line program is started by name, takes options, and does one job. Slide 6 compares the seven words, "
          "and slides 7 to 10 show the terminal in code.",
    "compare_vocab": "Seven words name nearly the same thing, and the table sorts them by what each one means and how it is started. A script is run from its source by an interpreter, a command is started from a terminal and shaped "
             "by its arguments, and a shell script is a text file of terminal commands. An application has a window of its own, an app is the phone or tablet version, and a web app runs on a server. The book calls most "
             "of its programs scripts, and this chapter turns them into commands. Remember the first two rows; they matter most here. Compare this table with slide 35, where the same difference shows in three launcher files.",
    "terminal_cd": "The terminal always has a current folder. The command cd changes it, and pwd prints it. The os module has a twin for each: os.chdir moves, and os.getcwd returns the place. The example creates a temporary "
                   "lab folder, makes a Desktop folder in it, moves in, reads the folder's name, moves back out and returns to where it started, so it leaves nothing behind. The comment on each line names the terminal command "
                   "it repeats. Slide 40 returns to this: os.chdir moves only the program, never the terminal that started it.",
    "terminal_ls": "The command ls on macOS and Linux, and dir on Windows, list the files of the current folder. In Python one call does both jobs: os.listdir returns the names, and a filter on the ending, such as "
                   "endswith('.exe'), repeats the wildcard of dir *.exe. The example makes three empty files in a temporary folder, lists them sorted, and then keeps only the programs. The result is two lists. "
                   "Chapter 11 shows the longer way with pathlib; this slide shows that the terminal's listing is an ordinary list of strings.",
    "path_text": "PATH is one long text of folders separated by a colon on macOS and Linux, and by a semicolon on Windows. When you type a name, the terminal tries the first folder, then the next, and the first folder that "
                 "holds the name wins. The example splits a PATH text into its folders, counts them, finds the position of /usr/bin, and builds a new PATH with one more folder at the front. Because the front folder is "
                 "searched first, adding your own Scripts folder there lets your launchers be found before anything else. See slide 10, where shutil.which repeats this search in code.",
    "path_which": "The function shutil.which does what the terminal does: it walks the PATH folders in order and returns the full path of the first match, or None when there is none. The example builds two folders, a and "
                  "b, each holding a program named spam, and gives which an explicit PATH text. The answer is the program in folder a, because a comes first. A name that is in no folder, eggs, returns None, which is the "
                  "terminal's 'command not found'. Slide 14 shows how activate changes this order.",
    "A2": "A virtual environment keeps one project's packages apart from the rest of the system. The cards give a plain meaning to each idea. A virtual environment is a folder with its own packages, so other projects and the "
          "system Python stay untouched. The command pip names a package and its version and installs it into the Python you name. Two projects can then need different versions of the same package without a clash. "
          "Slides 13 to 15 show the folder, the activation and the installation in code.",
    "venv_cfg": "A virtual environment is a folder, and one small text file inside it, pyvenv.cfg, records its settings: the home folder of the Python that made it, and whether the system's packages are visible. The example "
                "writes such a file and reads it back as a dictionary of settings. With include-system-site-packages set to false, the environment sees only its own packages, which is what keeps a project apart. "
                "Slide 45 lists what current Python changes in a fresh environment, such as the missing setuptools and the .gitignore file.",
    "venv_activate": "Activating an environment does not start a new Python. It edits the PATH of one terminal, putting the environment's bin folder first, so that the name python is found there before the system's. The "
                     "example builds the new PATH text and shows the environment folder at the front. It also asks whether the program is running inside an environment, and here the answer is False because the example "
                     "runs outside one. Closing the terminal ends the activation; nothing is changed for other terminals or for the system.",
    "pip": "The command pip installs a package, and two equals signs pin its version, as in package_name==1.17.4. The example splits such a pin into its name and version. Before importing a module, the program can ask "
           "importlib.util.find_spec whether the module can be found, and it gets None when it cannot. Here pyperclip is reported missing, so the program can say what to install instead of failing with a traceback. "
           "On a current Ubuntu system pip refuses to install into the system Python; use an environment, as slide 45 notes.",
    "A3": "A program can ask where and on what it runs, and it can read the words it was given. The cards give a plain meaning to each idea. A self-aware program reads its system, its Python version and its file before it "
          "acts. The list sys.argv holds the words typed after the program's name. The module argparse declares the arguments once, converts their types, fills defaults and refuses a wrong entry. The call sys.exit ends "
          "the program and prints a given text to standard error. Slides 19 to 23 show each in code.",
    "selfaware": "A program can learn about its surroundings. os.name is posix on macOS and Linux and nt on Windows; sys.version_info holds the Python version as fields, so the program can refuse a version that is too old; "
                 "and __file__ names the file only when the program was started from one. The example prints all four answers: a posix system, a Python that is new enough, five version fields, and False for the last, "
                 "because the example runs from a string, not from a file. Use these checks at the start, before the program does real work. Compare slide 20, where a missing module is reported, and see slide 22 for the arguments.",
    "missingmod": "When a module is missing, a program is more helpful if it says what to install than if it stops with a long traceback. The example tries to import a module that does not exist, catches the ImportError, "
                  "and passes a text to sys.exit. A text given to sys.exit is printed to standard error and ends the program with exit code 1, which another program can detect. The example reports both the result and "
                  "the exit message. Compare slide 15, where find_spec asks the question before importing.",
    "argv": "The shell cuts what you typed into words, and a pair of quotation marks keeps two words together as one. The program receives the words in the list sys.argv, with the script's own name first. The example "
            "shows three lines: two words give a list of three, quoted words give a list of two, and no words give a list of one. The length of argv is therefore always at least one. Slide 22 shows how argparse "
            "does this work for you.",
    "argparse_a": "The module argparse declares each argument once: its name, its type and its default. The example declares a density that is an integer with default 4 and a verbose flag that is off by default. With no words, "
                  "the defaults are used; with the words 20 and -v, the density becomes the integer 20 and verbose becomes True. The parser converts the text to the type, so the rest of the program receives numbers, "
                  "not strings. It also writes the help text from the declarations. Slide 23 shows what happens with a wrong word.",
    "argparse_b": "When a word does not fit the declared type, argparse does not guess. The example gives the text lots where an integer is declared, and the parser refuses with a clear message that names the argument, "
                  "'argument density: invalid int value'. Normally the parser then prints the usage and ends the program with exit code 2; the example catches that ending so the message can be shown here. "
                  "Declaring arguments once is therefore both shorter and safer than checking sys.argv by hand, as slide 21 did.",
    "A4": "A text program is designed to be typed and read: quiet by default, with characters and codes for its look. The cards give a plain meaning to each idea. Text-based design means short output that is readable at a "
          "glance. Presentation means layout and colour made only of characters and escape codes. The snowstorm is a short program that clears the screen and draws one frame after another. The helpers os.system, chr, "
          "bext, PyMsgBox and playsound each do one small job. Slides 26 to 32 show them.",
    "quiet": "A command line program should print little by default, because its output may be read by another program or by a person in a hurry. The example is a backup command that returns its messages as a list: "
             "with no options it returns one line, with -v it adds the steps, and with -q it returns nothing. The function report is an ordinary function of the arguments, so a verbose flag and a quiet flag can "
             "change the output without changing the work. This is the rule of the story on slide 27: do one thing, and do not clutter the output.",
    "chr": "The call chr turns a number into the character that has that number, and ord does the reverse. The numbers 9600, 9604 and 9608 are the upper half block, the lower half block and the full block, and "
           "ten of each in a row make a bar that the terminal can print. The call os.system hands a text to the shell, such as clear on macOS and Linux or cls on Windows; the example only reports what it would run, "
           "so that the page stays safe. The snowstorm on slide 32 draws with these block characters.",
    "colour": "A terminal colours text by receiving an escape code, which is the character number 27 followed by a bracket, a number and the letter m. The example shows the text that results when the foreground is red "
              "and the background is blue: code 31, code 44, the word, and code 0 that resets the colours. The list below it shows the eight foreground numbers from 30 to 37. A library such as bext only "
              "turns a colour name into these numbers. Because the code is ordinary text, a program that writes to a file gets the codes too. See slide 29 for chr, and compare slide 31 for where bext comes from.",
    "snowstorm": "The snowstorm is drawn cell by cell: each cell of a small grid is snow or a space, and two cells above one another are combined into one block character, so that a row of text shows two rows of "
                 "snow. The example draws five rows from a fixed seed, so every run gives the same picture, and it counts the flakes of each row. The real program repeats the drawing with a pause and clears the "
                 "screen between frames; one frame is enough to show the idea. The block characters are those of slide 29.",
    "A5": "Deploying makes a program reachable by its name from any folder. The cards give a plain meaning to each idea. Deploying means putting a launcher in a PATH folder so that the program is found by name. A "
          "deployment is the move of a finished program to where it will be used. The two short programs of the chapter, ccwd and the clipboard recorder, touch the system. PyInstaller packs the interpreter "
          "with the script into one larger file. The practice program gives each earlier program a launcher. Slides 35 to 44 show them.",
    "compare_launchers": "A launcher is a small file that starts your program and forwards the arguments to it. The table shows one idea in three spellings. On Windows it is a .bat file that calls activate.bat, runs the script "
                 "and pauses, and the arguments are forwarded with %*. On macOS it is a .command shell script, and on Ubuntu a shell script with a #! first line plus an optional .desktop entry; both forward the "
                 "arguments with \"$@\". If the forwarding is left out, the program receives none of the words typed after its name. Slide 36 shows the Ubuntu version line by line, and slide 14 shows the same idea of editing PATH.",
    "compare_helpers": "Five helpers appear in this part, and the table sorts them by what each does and whether it comes with Python. os.system and chr are part of the standard library and the language. The "
                       "others are third-party packages that the page does not run: bext sets the text and background colour and is installed with pip install bext; PyMsgBox opens small dialog windows and needs Tkinter; "
                       "and playsound plays a sound file and waits for the end. Check the package name before installing, because the chapter's prose and the Python Package Index differ for playsound. See slides 29 and 30 for the two that need no installation.",
    "launcher_text": "On Ubuntu and macOS the launcher is a three-line shell script. The first line names the interpreter, #!/usr/bin/env bash; the second activates the virtual environment; the third runs the Python program "
                     "and passes on every argument with \"$@\". The example prints the three numbered lines and splits the first line to show which interpreter it names. Because the first line starts with #!, the "
                     "system, not you, chooses the program that runs the file; slide 38 tells how that line came about.",
    "launcher_chmod": "A file becomes a command when its owner may execute it. The command chmod u+x adds the execute right for the owner; the example shows the permission text changing from -rw-r--r-- to -rwxr--r--, "
                      "which adds one x. The example then checks that shutil.which finds the file once its folder is on PATH. Both conditions are needed: the right to run, and a folder on PATH. If either is "
                      "missing, the terminal reports permission denied or command not found. Also see slide 9 for the PATH folders.",
    "desktop": "A .desktop file puts a launcher into the menu of an Ubuntu desktop. It is a small settings text with a name, the command to run and a type. The example reads such a text into a dictionary and "
               "shows the three entries; the command is gnome-terminal followed by the launcher, so that a window opens for a program that prints text. The file has no effect on how the program works. It only "
               "adds a menu entry, and the launcher on slide 36 stays the one that does the work.",
    "ccwd": "The program ccwd copies the folder the terminal is in to the clipboard. The example shows the fact that surprises: the program may change its own folder with os.chdir, but the terminal that started "
            "it stays where it was. The first value is the folder that was put on the clipboard, and the second is the terminal's folder after the program ends; the program has no way to move the terminal. "
            "That is why a command such as cd must be built into the shell itself. This returns to the cd of slide 7.",
    "cliprec": "The clipboard recorder checks the clipboard again and again and prints it only when it has changed. The example uses a list of three values that stand for the clipboard, so that it runs anywhere. "
               "It remembers the last value, prints each new one, and stops quietly when the person presses CTRL-C, which Python raises as KeyboardInterrupt. Three values were recorded. Printing only what "
               "changed keeps the output short, in the spirit of slide 26.",
    "pyinstaller": "PyInstaller packs your script and a copy of the Python interpreter into one file, so that a person without Python can run it. The command has five words: python, -m, PyInstaller, --onefile and the "
                   "script. The example splits that command and explains the two options. After a build, three things are left in the folder: build, dist with the executable, and a .spec file with the "
                   "settings. Slide 43 gives the measured size of the result.",
    "compare_pyinfo": "The one file has a cost. In the chapter research, a Hello, world program of 23 bytes became an executable of 12,950,120 bytes on Ubuntu, which is 12.95 megabytes, and the chapter's own text mentions "
              "about 8 megabytes on Windows. The build took about 15 seconds with PyInstaller 6.22.3 and Python 3.14.6. The chart shows the two sizes in megabytes, and the table lists the facts. The result "
              "works only on the system and the Python version that built it, because it holds a copy of that interpreter. Compare slide 44, where launchers deploy without a copy of the interpreter.",
    "deployable": "The practice program gives every earlier program a launcher from one template. The example prints four commands, each with the chapter it came from: zipBackup from chapter 11, "
                  "extractContacts from chapter 9, wikiBullets from chapter 8 and chessboard from chapter 7. The template is the same three-line launcher of slide 36 with only the script name changed. Once "
                  "each launcher is in a PATH folder, each program starts by name from any folder, and the arguments are forwarded.",
    "current": "The table lists what differs from the book, from the chapter research. For example, the __file__ of a script is an absolute path since Python 3.9, setuptools is no longer pre-installed in a "
               "virtual environment since 3.12, and a new environment holds a .gitignore file since 3.13. The help text of argparse is coloured since 3.14, and Ubuntu 24.04 marks the system Python as "
               "externally managed, so pip install there stops with an error. The third column names the slide whose example the change touches. Run what the book printed first, then check what changed. Also see slides 13, 15 and 23 for the examples.",
    "summary": "Five ideas are enough to carry away from this chapter. The terminal starts a program by searching the folders of PATH in order. A virtual environment keeps one project's packages apart, and activate edits "
               "PATH for that terminal. The program reads its words from sys.argv, and argparse parses and checks them. A text program is quiet by default and colours its text with escape codes. A launcher in a PATH folder, "
               "or PyInstaller, deploys it. Each idea has one slide in this deck, in the same order. Also see the questions of slide 3, which these five ideas answer.",
    "practice": "The four questions are short drills: predict the answer first, then run what you can on the chapter page. The first asks which folder is searched first after a new folder is put in front of PATH. "
                "The second asks what shlex.split gives for a command with quoted words, and how long argv is. The third adds an option to the argparse example, with a default and a type. The fourth asks for "
                "the launcher line that forwards arguments. The answers use slides 9, 21, 22 and 36.",
    "resources": "The links lead to the book chapter, to the Python documentation for sys, os, argparse, venv and shutil, to the two PEPs on virtual environments, to the pip and PyInstaller manuals, to the Bext and "
                 "PyMsgBox pages, to a 1982 film about Unix, and to the article on Unix pipelines. Choose one and read it before the next class. Each link is live on the slide. Use the documentation for the "
                 "exact behaviour of a call and the PEPs for the reason a rule exists. Compare slide 3: the links answer the same two questions in more depth, and see slide 45 for what changed.",
}

STORY_NOTES = {
    "pip": "This story gives the origin of pip and of the venv module. Ian Bicking announced pyinstall on 24 September 2008 and renamed it pip on 28 October 2008. Carl Meyer wrote PEP 405, which carried the idea "
           "of virtualenv into Python 3.3 as venv. The two commands of this part, python -m venv and pip install, are those two ideas. The link at the bottom leads to the article on pip, and the picture is "
           "the help screen of pip. Remember the dates as the order: the installer first, the isolated environment later.",
    "pipes": "This story explains why a command stays quiet. Doug McIlroy proposed in 1964 that programs be coupled, one feeding the next, and Ken Thompson added pipes to Unix in 1973. The maxims that followed "
             "say that each program does one thing well and that its output is not cluttered, because the next program reads it. The backup example of slide 26 follows that rule with its -v and -q options. "
             "The picture is a portrait of McIlroy, and the link leads to the article on pipelines.",
    "norton": "This story shows that a text screen can feel like a desktop. Norton Commander, begun by John Socha in 1984 and released in 1986, drew two file lists, a command bar, a viewer on F3 and an editor on "
              "F4 with plain characters. The picture is Midnight Commander, a later program of the same kind on Ubuntu. A text interface is simpler to program than a graphical one, which is the reason the "
              "snowstorm of slide 32 can be drawn with block characters. The link leads to the article on Norton Commander.",
    "shebang": "This story tells where the first line of a launcher comes from. Dennis Ritchie announced the #! line by email on 10 January 1980: the two characters at the start of a file tell the system which "
               "program should run the rest. The line reached users through Berkeley BSD, and from then on a script could be started by name like any program. The launcher of slide 36 starts with it, "
               "and adds env so that the interpreter is found on PATH. The picture is a portrait of Ritchie.",
}

RESULT_SAYS = {
    "terminal_cd": "The program moved in and out, and pwd gave Desktop.",
    "terminal_ls": "One call gave all names; a filter gave the programs.",
    "path_text": "Four folders; /usr/bin is third; the new folder is first.",
    "path_which": "The first match is in folder a; eggs is not found.",
    "venv_cfg": "The settings file reads back as two entries.",
    "venv_activate": "The environment folder is first on the new PATH.",
    "pip": "The pin splits in two; pyperclip is reported missing.",
    "selfaware": "A posix system, a new enough Python, five fields.",
    "missingmod": "The program names what is missing and leaves.",
    "argv": "Three, two and one word; the script name is first.",
    "argparse_a": "Defaults fill in; 20 became an integer.",
    "argparse_b": "The word lots is refused with a clear message.",
    "quiet": "One line, three lines, or none.",
    "chr": "Three block numbers make a bar of ten of each.",
    "colour": "One code for red, one for blue, one to reset.",
    "snowstorm": "Five rows of snow; the flakes of each row are counted.",
    "launcher_text": "Three numbered lines; the first names bash.",
    "launcher_chmod": "One x is added; the file is found on PATH.",
    "desktop": "Three entries: name, command, type.",
    "ccwd": "The clipboard holds the folder; the terminal stayed.",
    "cliprec": "Three values recorded; CTRL-C ended it quietly.",
    "pyinstaller": "Five words; two options; three things left behind.",
    "deployable": "Four commands, each with a launcher line.",
}
