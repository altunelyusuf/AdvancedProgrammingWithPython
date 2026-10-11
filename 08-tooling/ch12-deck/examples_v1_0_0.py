"""Chapter 12 deck examples: every console session and whole program the lecture deck shows and the page's Lab tab
offers. Nothing here carries a result; examples_run_v1_0_0.py runs it all under the interpreter given and records
the results. A console group is one session: its rows run in order in one namespace (as the deck check re-runs
them per slide). Every filesystem-touching group resets a single fixed folder, /tmp/ch12_lab, and chdirs into it
as its own first row, then refers only to relative names from then on, so no row's recorded result ever embeds a
random temporary path. No row raises SystemExit or KeyboardInterrupt, which the session runner (it catches Exception)
would not survive: argparse runs with exit_on_error=False so a bad argument raises ArgumentError instead of exiting,
and sys.exit() is shown by a whole program (selfAware) instead of a console row. A row that needs a line break inside
a string writes it as an escaped \\n, so the stored row text itself never holds a newline character."""
__version__ = "1.0.0"
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("base12", os.path.join(HERE, "..", "sen0414_ch12_corpus_base_v1_0_0.py"))
B = importlib.util.module_from_spec(_s)
_s.loader.exec_module(B)

_RESET = "import os, shutil; shutil.rmtree('/tmp/ch12_lab', ignore_errors=True); os.makedirs('/tmp/ch12_lab'); os.chdir('/tmp/ch12_lab')"

CONSOLES = {
    "title": ["'python3 snowstorm.py 20'.split()[1:]"],
    "terminal": [_RESET,
                 "os.path.basename(os.getcwd())",
                 "os.mkdir('Desktop'); os.chdir('Desktop')",
                 "os.path.basename(os.getcwd())",
                 "os.chdir('..')",
                 "for n in ('spam.exe', 'eggs.exe', 'notes.txt'): open(n, 'w').close()",
                 "sorted(os.listdir('.'))",
                 "sorted(n for n in os.listdir('.') if n.endswith('.exe'))"],
    "pathsearch": [_RESET,
                   "PATH = '/home/al/.local/bin:/home/al/bin:/usr/local/bin:/usr/bin:/bin'",
                   "PATH.split(':').index('/usr/bin')",
                   "':'.join(['/home/al/Scripts'] + PATH.split(':')[:2])",
                   "for d in ('a/sub', 'b'): os.makedirs(d)",
                   "for d in ('a/sub', 'b'): open(d + '/spam', 'w').close(); os.chmod(d + '/spam', 0o744)",
                   "shutil.which('spam', path='a:b')",
                   "shutil.which('spam', path='a') is None"],
    "pip": ["'package_name==1.17.4'.partition('==')",
            "import json",
            "type(json).__name__",
            "import importlib.util",
            "importlib.util.find_spec('pyperclip') is None"],
    "selfaware": ["import os, sys",
                  "os.name",
                  "sys.platform",
                  "sys.version_info >= (3, 9)",
                  "list(sys.version_info)",
                  "'__file__' in globals()",
                  "sys.prefix != sys.base_prefix"],
    "argv": ["import shlex",
             "'python3 yourScript.py hello world'.split()[1:]",
             "shlex.split('python3 yourScript.py \"hello world\"')[1:]",
             "argv = ['snowstorm.py', '20']",
             "int(argv[1]) if len(argv) > 1 else 4",
             "argv = ['snowstorm.py']",
             "int(argv[1]) if len(argv) > 1 else 4"],
    "argparse": ["import argparse",
                 "p = argparse.ArgumentParser(prog='snowstorm', exit_on_error=False)",
                 "_ = p.add_argument('density', type=int, nargs='?', default=4)",
                 "_ = p.add_argument('-v', '--verbose', action='store_true')",
                 "vars(p.parse_args([]))",
                 "vars(p.parse_args(['20', '-v']))",
                 "p.parse_args(['lots'])"],
    "clearing": ["import os",
                 "'cls' if os.name == 'nt' else 'clear'",
                 "TOP, BOTTOM, FULL = chr(9600), chr(9604), chr(9608)",
                 "[TOP, BOTTOM, FULL]",
                 "[ord(c) for c in (TOP, BOTTOM, FULL)]",
                 "FULL * 20"],
    "clipboard": ["seen = ['a', 'a', 'b', 'b', 'a']",
                  "[x for i, x in enumerate(seen) if i == 0 or x != seen[i - 1]]",
                  "1 / 0.01",
                  "issubclass(KeyboardInterrupt, Exception)"],
    "launcher": ["import stat, configparser",
                 "stat.filemode(0o100644 | stat.S_IXUSR)",
                 "'#!/usr/bin/env bash'[2:].split()",
                 "c = configparser.ConfigParser()",
                 "c.read_string('[Desktop Entry]\\nName=yourScript\\nExec=gnome-terminal -- /home/al/Scripts/yourScript\\nType=Application\\n')",
                 "c['Desktop Entry']['Exec']"],
    "pyinstaller": ["import importlib.util",
                    "importlib.util.find_spec('PyInstaller') is None",
                    "import pyinstaller"],
}

# name -> (code, stdin text or None)
PROGRAMS = {name: (code, None) for name, (code, _, _) in B.PROGRAMS.items()}
