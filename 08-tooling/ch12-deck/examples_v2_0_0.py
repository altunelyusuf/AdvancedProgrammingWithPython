"""Chapter 12 deck examples, version 2.0.0: the code examples of the chapter 12 lecture deck (Command Line Programs).
One example per code slide, in slide order. The `groups` are the code boxes of the slide (each with the plain-language
explanation that stands beside it); the lines of all groups of an example, in order, are the example's code: that text is
what the deck shows after the '>>> ' prompt of each line, what the chapter-code manifest lists and what the page runs.
Every example is self-contained (it imports what it uses), uses only the Python standard library, reads no keyboard, runs no
other program, leaves the current folder as it found it and prints an ordinary line first. A command line program is about
how a program is started, which a page cannot do: the examples therefore show each mechanism on text and on a throw-away
folder (the terminal commands as os calls, PATH as text, the launcher as a file) and say so beside the code.
Nothing here carries a result; deck_build_v2_0_0.py runs the code and takes every printed result from the run."""
__version__ = "2.0.0"

EXAMPLES = [
    dict(id="terminal_cd", name="cd and pwd as os calls", title="The terminal: cd and pwd as Python calls", part=1, visual="terminal_cd",
         concepts=["Using the Terminal", "Command line program"],
         groups=[
             (["import os, tempfile", "start = os.getcwd()", "with tempfile.TemporaryDirectory() as lab:", "    os.chdir(lab)", "    os.mkdir('Desktop')"],
              "Work in a throw-away folder, so nothing stays behind. os.mkdir makes a folder called Desktop."),
             (["    os.chdir('Desktop')  # cd Desktop", "    where = os.path.basename(os.getcwd())  # pwd", "    os.chdir('..')  # cd .."],
              "os.chdir is the cd command and os.getcwd is pwd. The program goes down into Desktop and back up."),
             (["    os.chdir(start)", "print('pwd ->', where)"],
              "Go back to the starting folder, then print what pwd showed inside Desktop."),
         ]),
    dict(id="terminal_ls", name="ls and dir as os.listdir", title="The terminal: ls and dir *.exe as Python calls", part=1, visual="terminal_ls",
         concepts=["Using the Terminal", "Command line program"],
         groups=[
             (["import os, tempfile", "with tempfile.TemporaryDirectory() as lab:", "    for name in ('spam.exe', 'eggs.exe', 'notes.txt'):", "        open(os.path.join(lab, name), 'w').close()"],
              "Make three empty files in a throw-away folder: two programs and a note."),
             (["    listing = sorted(os.listdir(lab))  # ls", "    programs = [n for n in listing if n.endswith('.exe')]  # dir *.exe", "print('ls ->', listing)", "print('dir *.exe ->', programs)"],
              "os.listdir lists the names like ls. The filter keeps only the names ending in .exe, like dir *.exe."),
         ]),
    dict(id="path_text", name="PATH is a text of folders", title="PATH: a text of folders, searched in order", part=1, visual="path_text",
         concepts=["Using the Terminal"],
         groups=[
             (["PATH = '/home/al/bin:/usr/local/bin:/usr/bin:/bin'", "folders = PATH.split(':')"],
              "PATH is one text of folders, separated by colons. split turns it into a list in search order."),
             (["print(len(folders), 'folders')", "print('/usr/bin is number', folders.index('/usr/bin') + 1)", "print(':'.join(['/home/al/Scripts'] + folders[:2]))"],
              "The terminal tries the folders from left to right. A folder put first, like /home/al/Scripts, wins."),
         ]),
    dict(id="path_which", name="shutil.which walks the folders", title="which: the first folder that holds the program", part=1, visual="path_which",
         concepts=["Using the Terminal"],
         groups=[
             (["import os, shutil, tempfile", "with tempfile.TemporaryDirectory() as lab:", "    for d in ('a', 'b'):", "        os.mkdir(lab + '/' + d)"],
              "Make two folders, a and b, inside a throw-away folder."),
             (["        prog = lab + '/' + d + '/spam'", "        open(prog, 'w').close()", "        os.chmod(prog, 0o744)"],
              "Each folder gets a program called spam. chmod gives the owner the right to run it."),
             (["    path = lab + '/a:' + lab + '/b'", "    where = os.path.relpath(shutil.which('spam', path=path), lab)", "print('first spam is in', where)", "print('eggs found:', shutil.which('eggs', path=path))"],
              "shutil.which does what the which command does: it walks the folders in order and returns the first match, or None."),
         ]),
    dict(id="venv_cfg", name="pyvenv.cfg is a settings file", title="Virtual environments: a folder and a settings file", part=2, visual="venv_cfg",
         concepts=["Virtual Environments"],
         groups=[
             (["cfg = 'home = /usr/bin\\ninclude-system-site-packages = false'", "settings = dict(line.split(' = ') for line in cfg.splitlines())", "print(settings)"],
              "A virtual environment is a folder with a small pyvenv.cfg file. Every line is one setting, so a dictionary can hold it."),
         ]),
    dict(id="venv_activate", name="activate edits PATH", title="activate puts the environment first on PATH", part=2, visual="venv_activate",
         concepts=["Virtual Environments"],
         groups=[
             (["import sys", "bin_dir = '/home/al/Scripts/.venv/bin'", "PATH = '/usr/local/bin:/usr/bin:/bin'", "print('after activate:', bin_dir + ':' + PATH)"],
              "activate puts the environment's bin folder first on PATH. Its python and pip are now found before the system ones."),
             (["print('inside a virtual environment:', sys.prefix != sys.base_prefix)"],
              "Outside an environment prefix and base_prefix are equal, so this test prints False. Inside one it prints True."),
         ]),
    dict(id="pip", name="pip requirement and find_spec", title="pip: pin a version, find a module", part=2, visual="pip",
         concepts=["Installing Python Packages with pip"],
         groups=[
             (["requirement = 'package_name==1.17.4'", "name, sep, version = requirement.partition('==')", "print(name, sep, version)"],
              "pip pins a version with two equals signs. partition cuts the text into name, separator and version."),
             (["import importlib.util, json", "print(type(json).__name__)", "print('pyperclip missing:', importlib.util.find_spec('pyperclip') is None)"],
              "A package is a module you import. find_spec asks whether Python can find one before the import fails."),
         ]),
    dict(id="selfaware", name="os.name, sys.version_info and __file__", title="Self-aware programs: system, version, file", part=3, visual="selfaware",
         concepts=["Self-Aware Python Programs"],
         groups=[
             (["import os, sys", "KINDS = {'nt': 'Windows', 'posix': 'macOS or Linux'}", "print('os.name is', os.name, '->', KINDS[os.name])"],
              "os.name tells the family of the operating system. sys.platform is finer: win32, darwin or linux."),
             (["print('Python 3.9 or newer:', sys.version_info >= (3, 9))", "print('version fields:', len(sys.version_info))", "print('started from a file:', '__file__' in globals())"],
              "sys.version_info compares like a tuple. A script started from a file has __file__; this listing has none, so it prints False."),
         ]),
    dict(id="missingmod", name="ModuleNotFoundError and sys.exit", title="Missing modules and sys.exit with a message", part=3, visual="missingmod",
         concepts=["Self-Aware Python Programs"],
         groups=[
             (["import sys", "try:", "    import nonexistentModule", "except ModuleNotFoundError as err:", "    print('Result: no module called', err.name)"],
              "Catch ModuleNotFoundError to say in your own words what is missing, instead of showing a traceback."),
             (["    try:", "        sys.exit('This program needs nonexistentModule.')", "    except SystemExit as stop:", "        print('exit message:', stop.code)"],
              "sys.exit with a text raises SystemExit. In a real run Python prints the text to standard error and ends with exit code 1."),
         ]),
    dict(id="argv", name="sys.argv and shlex.split", title="Command line arguments: sys.argv", part=3, visual="argv",
         concepts=["Command line program", "Text-Based Program Design"],
         groups=[
             (["import shlex", "typed = ['python3 yourScript.py hello world',", "         'python3 yourScript.py \"hello world\"',", "         'python3 yourScript.py']"],
              "Three ways to start the same script. The shell cuts each typed line into words before Python sees it."),
             (["for line in typed:", "    argv = shlex.split(line)[1:]", "    print(len(argv), argv)"],
              "shlex.split cuts a line the way a Unix shell does. Quotation marks keep two words together as one argument."),
         ]),
    dict(id="argparse_a", name="argparse declares the arguments", title="argparse: declare the arguments once", part=3, visual="argparse_a",
         concepts=["Command line program", "Text-Based Program Design"],
         groups=[
             (["import argparse", "p = argparse.ArgumentParser(prog='snowstorm', exit_on_error=False)", "p.add_argument('density', type=int, nargs='?', default=4)",
               "p.add_argument('-v', '--verbose', action='store_true')"],
              "Declare each argument once: an optional number that defaults to 4, and a -v switch. argparse does the parsing."),
             (["for argv in ([], ['20', '-v']):", "    print(argv, '->', vars(p.parse_args(argv)))"],
              "parse_args turns the list of words into named values and fills in the defaults."),
         ]),
    dict(id="argparse_b", name="argparse refuses a wrong word", title="argparse: a wrong word is refused", part=3, visual="argparse_b",
         concepts=["Command line program", "Text-Based Program Design"],
         groups=[
             (["import argparse", "p = argparse.ArgumentParser(prog='snowstorm', exit_on_error=False)", "p.add_argument('density', type=int)"],
              "The same parser, now with a required number. The declaration says the density must be an int."),
             (["try:", "    p.parse_args(['lots'])", "except argparse.ArgumentError as err:", "    print('Result: refused,', err)"],
              "A word that is not a number is refused with a clear message. In a terminal the program would also stop with exit code 2."),
         ]),
    dict(id="quiet", name="Quiet, default and verbose", title="Text-based design: quiet by default", part=4, visual="quiet",
         concepts=["Text-Based Program Design", "Command line program"],
         groups=[
             (["import argparse", "p = argparse.ArgumentParser(prog='backup', exit_on_error=False)", "p.add_argument('-v', '--verbose', action='store_true')",
               "p.add_argument('-q', '--quiet', action='store_true')"],
              "Two switches: -v asks for more output and -q for none. Without either, the command stays short."),
             (["steps = ['reading 3 files', 'zipping', 'saved backup.zip']", "report = lambda a: [] if a.quiet else steps if a.verbose else steps[-1:]"],
              "Quiet prints nothing, verbose every step, and the default only the last line, the result."),
             (["for argv in ([], ['-v'], ['-q']):", "    print(argv, '->', report(p.parse_args(argv)))"],
              "Run it three ways. Short default output is easy for another program to read."),
         ]),
    dict(id="chr", name="chr and the clear command", title="Terminal presentation: chr and os.system", part=4, visual="chr",
         concepts=["Terminal presentation", "os.system", "chr"],
         groups=[
             (["import os", "clear_command = 'cls' if os.name == 'nt' else 'clear'", "print('os.system would run:', clear_command)"],
              "os.system hands a text to the shell. Programs use it to clear the screen: cls on Windows, clear elsewhere. Here only the text is built."),
             (["TOP, BOTTOM, FULL = chr(9600), chr(9604), chr(9608)", "print([ord(c) for c in (TOP, BOTTOM, FULL)])", "print(TOP * 10 + BOTTOM * 10 + FULL * 10)"],
              "chr turns a number into a character and ord turns it back. Three block characters draw the snow and the ground."),
         ]),
    dict(id="colour", name="Colour names as escape codes", title="Colour in the terminal: what bext.fg and bext.bg send", part=4, visual="colour",
         concepts=["bext.fg", "bext.bg", "Terminal presentation"],
         groups=[
             (["COLORS = ['black', 'red', 'green', 'yellow',", "          'blue', 'purple', 'cyan', 'white']"],
              "The eight colour names of Bext, in the order of the numbers 0 to 7."),
             (["fg = lambda name: '\\x1b[%dm' % (30 + COLORS.index(name))", "bg = lambda name: '\\x1b[%dm' % (40 + COLORS.index(name))"],
              "bext.fg and bext.bg pick a colour by name. Underneath, the terminal receives numbered escape codes: 30 to 37 and 40 to 47."),
             (["print(repr(fg('red') + bg('blue') + 'hi' + '\\x1b[0m'))", "print([fg(c)[2:-1] for c in COLORS])"],
              "The terminal reads the code and switches colour; the reset code 0 switches back. This is a stand-in; the real Bext is not installed here."),
         ]),
    dict(id="snowstorm", name="One snowstorm frame", title="Snowstorm: one frame of the animation", part=4, visual="snowstorm",
         concepts=["A Short Program: Snowstorm", "Terminal presentation", "chr"],
         groups=[
             (["import random", "TOP, BOTTOM = chr(9600), chr(9604)", "argv = ['snowstorm.py', '20']", "DENSITY = int(argv[1]) if len(argv) > 1 else 4", "random.seed(12)"],
              "The argument, as in python snowstorm.py 20, sets the density: the percent of cells that hold snow. The default is 4. The seed fixes one frame."),
             (["def cell():", "    snow = random.randint(0, 99) < DENSITY", "    return random.choice([TOP, BOTTOM]) if snow else ' '"],
              "A cell holds snow when a random number from 0 to 99 is below the density."),
             (["rows = [''.join(cell() for x in range(40)) for y in range(5)]", "print('flakes per row:', [len(r) - r.count(' ') for r in rows])", "print('\\n'.join(rows))"],
              "Five rows of 40 cells. The book clears the screen and repeats the frame forever."),
         ]),
    dict(id="launcher_text", name="The launcher script, line by line", title="Deploying on Ubuntu: the launcher script", part=5, visual="launcher_text",
         concepts=["Deploying Python Programs", "Deployment"],
         groups=[
             (["launcher = '#!/usr/bin/env bash\\nsource ~/Scripts/.venv/bin/activate\\n'", "launcher += 'python3 ~/Scripts/yourScript.py \"$@\"\\n'"],
              "The launcher is a three-line shell script. Its first line names the interpreter; \"$@\" passes the arguments on."),
             (["for number, line in enumerate(launcher.splitlines(), 1):", "    print(number, line)", "print('interpreter:', launcher.splitlines()[0][2:].split())"],
              "Number the lines. Line 1 starts #!, which tells the system which program runs the file; env then finds bash on PATH."),
         ]),
    dict(id="launcher_chmod", name="chmod u+x makes it a command", title="Deploying on Ubuntu: chmod u+x", part=5, visual="launcher_chmod",
         concepts=["Deploying Python Programs", "Deployment"],
         groups=[
             (["import os, shutil, stat, tempfile", "from pathlib import Path", "with tempfile.TemporaryDirectory() as scripts:", "    path = Path(scripts, 'yourScript')"],
              "A throw-away Scripts folder holds the launcher file."),
             (["    path.write_text('#!/usr/bin/env bash\\n')", "    path.chmod(0o644)", "    before = stat.filemode(path.stat().st_mode)"],
              "Write the launcher. A new file can be read but not run."),
             (["    path.chmod(path.stat().st_mode | stat.S_IXUSR)  # chmod u+x", "    after = stat.filemode(path.stat().st_mode)", "    on_path = shutil.which('yourScript', path=scripts) == str(path)",
               "print(before, '->', after, '| found on PATH:', on_path)"],
              "chmod u+x gives the owner the right to run it. Then which finds the launcher by its bare name on PATH."),
         ]),
    dict(id="desktop", name="A .desktop entry with configparser", title="Deploying on Ubuntu: the .desktop entry", part=5, visual="desktop",
         concepts=["Deploying Python Programs"],
         groups=[
             (["import configparser", "entry = ('[Desktop Entry]\\n'", "         'Name=yourScript\\n'", "         'Exec=gnome-terminal -- /home/al/Scripts/yourScript\\n'",
               "         'Type=Application\\n')"],
              "A .desktop file is a small settings file that puts a program in the Ubuntu menu. Its Exec line says what to run."),
             (["c = configparser.ConfigParser()", "c.read_string(entry)", "print(dict(c['Desktop Entry']))"],
              "configparser reads this kind of file. Every key becomes an item of a dictionary."),
         ]),
    dict(id="ccwd", name="ccwd copies the working directory", title="ccwd: copying the current working directory", part=5, visual="ccwd",
         concepts=["A Short Program: Copying the Current Working Directory"],
         groups=[
             (["import os", "clipboard = []", "def ccwd(argv):", "    if len(argv) > 1:", "        os.chdir(argv[1])", "    clipboard.append(os.getcwd())"],
              "ccwd changes folder when it gets an argument, then copies the working directory. A list stands in for the clipboard."),
             (["start = os.getcwd()", "os.chdir('/tmp')", "terminal = os.getcwd()  # where the terminal stands", "ccwd(['ccwd.py', '..'])",
               "print('clipboard', clipboard[-1], '| terminal', terminal)", "os.chdir(start)"],
              "os.chdir moves only the running program. After ccwd .. the terminal itself has not moved."),
         ]),
    dict(id="cliprec", name="Clipboard recorder loop", title="Clipboard Recorder: print what changed", part=5, visual="cliprec",
         concepts=["A Short Program: Clipboard Recorder"],
         groups=[
             (["texts = ['ch11', 'ch11', 'ch12', 'ch12', 'ch13']", "previous_content, recorded = '', []", "try:",
               "    for content in texts:  # the book calls paste()"],
              "The real program calls pyperclip.paste again and again. Here a list of copied texts plays the clipboard."),
             (["        if content != previous_content:", "            print(content)", "            recorded.append(content)", "            previous_content = content"],
              "It prints a text only when it is new, and remembers the last one."),
             (["    raise KeyboardInterrupt  # the user presses CTRL-C", "except KeyboardInterrupt:", "    print('Result: stopped quietly;', len(recorded), 'recorded')"],
              "CTRL-C raises KeyboardInterrupt. The except clause catches it, so the program ends quietly."),
         ]),
    dict(id="pyinstaller", name="The PyInstaller command line", title="PyInstaller: one file, a whole interpreter", part=5, visual="pyinstaller",
         concepts=["Compiling Python Programs with PyInstaller", "Deployment"],
         groups=[
             (["import shlex", "command = 'python -m PyInstaller --onefile yourScript.py'", "words = shlex.split(command)", "print(len(words), 'words:', words)"],
              "The module name needs its two capital letters and --onefile its two dashes. shlex.split shows the words PyInstaller receives."),
             (["roles = {'-m': 'run a module', '--onefile': 'bundle into one file'}", "print({w: roles[w] for w in words if w in roles})"],
              "-m runs PyInstaller as a module and --onefile asks for one executable."),
             (["left = ['build/', 'dist/', 'yourScript.spec']", "print('the build leaves:', left)"],
              "The build leaves a build folder, a dist folder and a spec file."),
         ]),
    dict(id="deployable", name="Launchers for earlier projects", title="Practice program: make your programs deployable", part=5, visual="deployable",
         concepts=["Practice Program: Make Your Programs Deployable", "Deployment"],
         groups=[
             (["LINE = 'python3 ~/Scripts/{name}.py \"$@\"'  # third line of a launcher", "projects = {'zipBackup': 11, 'extractContacts': 9, 'wikiBullets': 8, 'chessboard': 7}"],
              "The practice program asks for four earlier projects to become commands. One template line serves them all."),
             (["for name, chapter in projects.items():", "    print(name.ljust(16), 'chapter', chapter, '|', LINE.format(name=name))"],
              "format fills the project name into the line. Each project then runs from any folder."),
         ]),
]
BY_ID = {e["id"]: e for e in EXAMPLES}


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def code_text(ex):
    return "\n".join(code_lines(ex))
