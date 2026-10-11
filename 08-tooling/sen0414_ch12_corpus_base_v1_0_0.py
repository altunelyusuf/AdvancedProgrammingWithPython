#!/usr/bin/env python3
"""SEN0414 chapter 12 (Designing and Deploying Command Line Programs, 3rd edition) - the shared base of the corpus,
version 1.0.0.

Holds the chapter's whole programs as text, the single source the deck and the page's Lab tab both read, in the shape of
sen0414_ch11_corpus_base_v1_0_0.py (written fresh for this chapter, not copied from another chapter's base).

A command line program is about how a program is started, so most programs below start another program: each writes the
chapter's own script into a temporary folder it creates and removes itself, and runs it with subprocess, using
sys.executable (the very interpreter running the program) where the chapter types python or python3. Printed paths have
the temporary folder replaced by ~, the home folder the chapter's own launchers use, so a re-run prints the same text.

* ARGV_AND_QUOTING runs the chapter's yourScript.py three ways: python3 yourScript.py hello world, with the two words
  in quotation marks, and with no argument, splitting each typed line with shlex.split as a POSIX shell would.
* SNOWSTORM_FRAME is the chapter's snowstorm.py with two changes, both stated in its own comments: sys.argv is set as if
  the program had been started with python snowstorm.py 20, and one seeded frame of 6 rows is printed instead of an
  endless loop of cleared 20-row frames (clear() and time.sleep(0.2) are what repeat it), so the slide can be checked.
* SELF_AWARE runs a script that prints __file__, the version check, os.name and sys.platform, and then stops through the
  chapter's own ModuleNotFoundError check with sys.exit(message); the parent prints the stderr text and the exit code.
* VENV_TOUR creates a real virtual environment with python -m venv .venv, lists what the folder holds, reads pyvenv.cfg,
  runs pip list inside it and asks both interpreters whether they are in an environment (sys.prefix != sys.base_prefix).
* LINUX_LAUNCHER is the chapter's Ubuntu deployment, executed: a Scripts folder with a venv, yourScript.py, the launcher
  yourScript exactly as the chapter prints it (with a hyphen where the online text has an en dash), chmod u+x, the
  folder put on PATH, and the launcher run by name with two arguments; a second launcher with "$@" added shows the
  arguments that the chapter's own launcher does not forward. HOME is set to the temporary folder so ~ expands there.
* CCWD runs the chapter's four-line ccwd.py unchanged. This machine has no clipboard (pyperclip 1.11.0 raised
  PyperclipException here), so a stand-in pyperclip.py with the same copy() and paste() keeps the text in a file beside
  the script; a bash shell started in ~/Scripts runs ccwd .. and then pwd, showing that the shell did not move.
* CLIP_RECORDER runs the chapter's cliprec.py unchanged against a stand-in pyperclip whose paste() serves the texts a
  user copies, one per call, and raises KeyboardInterrupt when they run out - what pressing CTRL-C does.
* ARGPARSE_SNOWSTORM is this course's addition: the snowstorm's density argument declared with argparse, the module the
  chapter recommends and leaves to its documentation, run with no argument, with 20 -v, and with a word that is not a
  number, which argparse refuses with a usage message on stderr and exit code 2.

Sources read for this chapter, on 2026-10-11: the book chapter (automatetheboringstuff.com/3e/chapter12.html); the Python
3.14 documentation (sys, os, venv, argparse, shutil, shlex). Every behaviour quoted is executed (python3.14 against the
programs below).
"""
__version__ = "1.0.0"

# ---------------------------------------------------------------------------------------------------------------------------------
# sys.argv: the chapter's yourScript.py, started three ways.
# ---------------------------------------------------------------------------------------------------------------------------------
ARGV_AND_QUOTING = r"""import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as scripts:
    Path(scripts, 'yourScript.py').write_text('import sys\nprint(sys.argv)\n')
    for typed in ('python3 yourScript.py hello world',
                  'python3 yourScript.py "hello world"',
                  'python3 yourScript.py'):
        words = shlex.split(typed)          # the shell splits the typed line into words
        words[0] = sys.executable           # python3: this machine's own interpreter
        run = subprocess.run(words, cwd=scripts, capture_output=True, text=True)
        print(typed.ljust(36), '->', run.stdout.strip())
"""

# ---------------------------------------------------------------------------------------------------------------------------------
# The chapter's snowstorm.py, one seeded frame.
# ---------------------------------------------------------------------------------------------------------------------------------
SNOWSTORM_FRAME = r"""import os, random, time, sys

TOP    = chr(9600)  # Character 9600 is the top half block
BOTTOM = chr(9604)  # Character 9604 is the bottom half block
FULL   = chr(9608)  # Character 9608 is the full block

sys.argv = ['snowstorm.py', '20']  # as if started with: python snowstorm.py 20

# Set the snowstorm density to the command line argument:
DENSITY = 4  # Default snow density is 4%
if len(sys.argv) > 1:
    DENSITY = int(sys.argv[1])

random.seed(12)  # one fixed frame; the chapter loops forever
for y in range(6):
    for x in range(40):
        if random.randint(0, 99) < DENSITY:
            print(random.choice([TOP, BOTTOM]), end='')  # Print snow
        else:
            print(' ', end='')  # Print empty space
    print()  # Print a newline.
print(FULL * 40 + '\n' + FULL * 40)  # the snow-covered ground
print('(Ctrl-C to stop.)')
"""

# ---------------------------------------------------------------------------------------------------------------------------------
# Self-aware programs: __file__, the version, the operating system, a missing module and sys.exit.
# ---------------------------------------------------------------------------------------------------------------------------------
SELF_AWARE = r"""import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = '''import os, sys
from pathlib import Path
print('__file__ absolute:', Path(__file__).is_absolute(), Path(__file__).name)
print('Python 3.9 or newer:', sys.version_info >= (3, 9))
print('os.name:', os.name, '  sys.platform:', sys.platform)
try:
    import nonexistentModule
except ModuleNotFoundError:
    sys.exit('This program needs nonexistentModule: python -m pip install it.')
print('never printed')
'''
with tempfile.TemporaryDirectory() as scripts:
    Path(scripts, 'yourScript.py').write_text(SCRIPT)
    run = subprocess.run([sys.executable, 'yourScript.py'], cwd=scripts,
                         capture_output=True, text=True)
    print(run.stdout, end='')
    print('stderr:', run.stderr.strip())
    print('exit code:', run.returncode)
"""

# ---------------------------------------------------------------------------------------------------------------------------------
# A virtual environment, created and looked at.
# ---------------------------------------------------------------------------------------------------------------------------------
VENV_TOUR = r"""import os
import subprocess
import sys
import tempfile
from pathlib import Path

ASK = 'import sys; print(sys.prefix != sys.base_prefix)'
with tempfile.TemporaryDirectory() as scripts:
    subprocess.run([sys.executable, '-m', 'venv', '.venv'], cwd=scripts, check=True)
    venv = Path(scripts, '.venv')
    print('.venv holds:', sorted(p.name for p in venv.iterdir()))
    print('activate:', (venv / 'bin' / 'activate').exists())
    cfg = (venv / 'pyvenv.cfg').read_text().splitlines()
    print([line for line in cfg if line.startswith('include')])
    quiet = dict(os.environ, PIP_DISABLE_PIP_VERSION_CHECK='1')
    pip = subprocess.run([venv / 'bin' / 'python', '-m', 'pip', 'list', '--format=freeze'],
                         capture_output=True, text=True, env=quiet)
    print('pip list in the new .venv:', [line.split('==')[0] for line in pip.stdout.split()])
    for python in (sys.executable, venv / 'bin' / 'python'):
        inside = subprocess.run([python, '-c', ASK], capture_output=True, text=True).stdout.strip()
        print('in a virtual environment:', inside)
"""

# ---------------------------------------------------------------------------------------------------------------------------------
# The chapter's Ubuntu deployment, executed.
# ---------------------------------------------------------------------------------------------------------------------------------
LINUX_LAUNCHER = r"""import os, shutil, subprocess, sys, tempfile
from pathlib import Path

SCRIPT = 'import sys\nprint(sys.argv[1:], sys.prefix != sys.base_prefix)\n'
LAUNCHER = '''#!/usr/bin/env bash
source ~/Scripts/.venv/bin/activate
python3 ~/Scripts/yourScript.py
read -p "Press any key to continue..." -n1 -s
deactivate
'''
with tempfile.TemporaryDirectory() as home:
    scripts = Path(home, 'Scripts')
    scripts.mkdir()
    subprocess.run([sys.executable, '-m', 'venv', '.venv'], cwd=scripts, check=True)
    (scripts / 'yourScript.py').write_text(SCRIPT)
    for name, text in (('yourScript', LAUNCHER),
                       ('yourScriptArgs', LAUNCHER.replace('yourScript.py', 'yourScript.py "$@"'))):
        (scripts / name).write_text(text)
        subprocess.run(['chmod', 'u+x', name], cwd=scripts, check=True)
    env = dict(os.environ, HOME=home, PATH=str(scripts) + os.pathsep + os.environ['PATH'])
    found = shutil.which('yourScript', path=env['PATH'])
    print('which yourScript ->', found.replace(home, '~'))
    print('mode after chmod u+x:', subprocess.run(['stat', '-c', '%A', found], capture_output=True, text=True).stdout.strip())
    for name in ('yourScript', 'yourScriptArgs'):
        run = subprocess.run([name, 'spam', 'eggs'], env=env, capture_output=True, text=True, stdin=subprocess.DEVNULL)
        print(name, 'spam eggs -> arguments, in .venv:', run.stdout.strip())
"""

# ---------------------------------------------------------------------------------------------------------------------------------
# The chapter's ccwd.py, run unchanged.
# ---------------------------------------------------------------------------------------------------------------------------------
CCWD = r"""import subprocess
import sys
import tempfile
from pathlib import Path

CCWD = '''import pyperclip, os, sys
if len(sys.argv) > 1:
    os.chdir(sys.argv[1])
pyperclip.copy(os.getcwd())
'''
STAND_IN = '''from pathlib import Path   # no clipboard on this machine: the text is kept in a file
CLIP = Path(__file__).with_name('clipboard.txt')
def copy(text): CLIP.write_text(text)
def paste(): return CLIP.read_text()
'''
with tempfile.TemporaryDirectory() as home:
    home = str(Path(home).resolve())
    scripts = Path(home, 'Scripts')
    scripts.mkdir()
    (scripts / 'ccwd.py').write_text(CCWD)
    (scripts / 'pyperclip.py').write_text(STAND_IN)
    for args in ('', ' ..'):
        shell = subprocess.run(['bash', '-c', '"$0" ccwd.py' + args + '; pwd', sys.executable],
                               cwd=scripts, capture_output=True, text=True)
        copied = (scripts / 'clipboard.txt').read_text()
        print(('ccwd' + args).ljust(8), '-> clipboard:', copied.replace(home, '~'),
              '| the shell is still in', shell.stdout.strip().replace(home, '~'))
"""

# ---------------------------------------------------------------------------------------------------------------------------------
# The chapter's cliprec.py, run unchanged against copied texts.
# ---------------------------------------------------------------------------------------------------------------------------------
CLIP_RECORDER = r"""import subprocess
import sys
import tempfile
from pathlib import Path

CLIPREC = '''import pyperclip, time

print('Recording clipboard... (Ctrl-C to stop)')
previous_content = ''
try:
    while True:
        content = pyperclip.paste()  # Get clipboard contents.

        if content != previous_content:
            # If it's different from the previous, print it:
            print(content)
            previous_content = content

        time.sleep(0.01)  # Pause to avoid hogging the CPU.
except KeyboardInterrupt:
    pass
'''
STAND_IN = '''COPIED = iter(['https://automatetheboringstuff.com/3e/chapter11.html',
               'https://automatetheboringstuff.com/3e/chapter11.html',
               'https://automatetheboringstuff.com/3e/chapter12.html',
               'https://automatetheboringstuff.com/3e/chapter12.html',
               'https://automatetheboringstuff.com/3e/chapter13.html'])
def paste():
    try:
        return next(COPIED)        # what the user has copied, one read at a time
    except StopIteration:
        raise KeyboardInterrupt    # the user presses CTRL-C
'''
with tempfile.TemporaryDirectory() as scripts:
    Path(scripts, 'cliprec.py').write_text(CLIPREC)
    Path(scripts, 'pyperclip.py').write_text(STAND_IN)
    run = subprocess.run([sys.executable, 'cliprec.py'], cwd=scripts, capture_output=True, text=True)
    print(run.stdout, end='')
    print('exit code:', run.returncode, '| traceback printed:', 'Traceback' in run.stderr)
"""

# ---------------------------------------------------------------------------------------------------------------------------------
# The course's addition: the snowstorm's argument declared with argparse.
# ---------------------------------------------------------------------------------------------------------------------------------
ARGPARSE_SNOWSTORM = r"""import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = '''import argparse
parser = argparse.ArgumentParser(prog='snowstorm', description='A text snowstorm.')
parser.add_argument('density', type=int, nargs='?', default=4, help='percent of snow')
parser.add_argument('-v', '--verbose', action='store_true', help='say more')
args = parser.parse_args()
print('density', args.density, 'verbose', args.verbose)
'''
with tempfile.TemporaryDirectory() as scripts:
    Path(scripts, 'snowstorm.py').write_text(SCRIPT)
    plain = dict(os.environ, NO_COLOR='1')
    for args in ([], ['20', '-v'], ['lots']):
        run = subprocess.run([sys.executable, 'snowstorm.py', *args], cwd=scripts,
                             capture_output=True, text=True, env=plain)
        said = run.stdout.strip() or run.stderr.strip().splitlines()[-1]
        print(('snowstorm ' + ' '.join(args)).ljust(17), '-> exit', run.returncode, '|', said)
"""

PROGRAMS = {
    "argvAndQuoting_v1_0_0.py": (ARGV_AND_QUOTING, None, None),
    "snowstormFrame_v1_0_0.py": (SNOWSTORM_FRAME, None, None),
    "selfAware_v1_0_0.py": (SELF_AWARE, None, None),
    "venvTour_v1_0_0.py": (VENV_TOUR, None, None),
    "linuxLauncher_v1_0_0.py": (LINUX_LAUNCHER, None, None),
    "ccwd_v1_0_0.py": (CCWD, None, None),
    "clipRecorder_v1_0_0.py": (CLIP_RECORDER, None, None),
    "argparseSnowstorm_v1_0_0.py": (ARGPARSE_SNOWSTORM, None, None),
}

if __name__ == "__main__":
    import subprocess, sys
    for name, (code, _, _) in PROGRAMS.items():
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        print("=== %s (exit %d)" % (name, r.returncode)); print(r.stdout.rstrip()); print(r.stderr[-300:].rstrip())
