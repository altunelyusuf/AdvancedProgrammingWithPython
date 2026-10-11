"""Chapter 10 deck examples: every console session and whole program the lecture deck shows and the page's Lab tab
offers. Nothing here carries a result; examples_run_v1_0_0.py runs it all under the interpreter given and records
the results. A console group is one session: its rows run in order in one namespace (as the deck check re-runs
them per slide). Every filesystem-touching group resets a single fixed folder, /tmp/ch10_lab, and chdirs into it
as its own first row, then refers only to relative names from then on, so no row's recorded result ever embeds a
random temporary path - the one thing that would make a re-run's result differ from the recording."""
__version__ = "1.0.0"
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("base10", os.path.join(HERE, "..", "sen0414_ch10_corpus_base_v1_0_0.py"))
B = importlib.util.module_from_spec(_s)
_s.loader.exec_module(B)

_RESET = "import os, shutil; shutil.rmtree('/tmp/ch10_lab', ignore_errors=True); os.makedirs('/tmp/ch10_lab'); os.chdir('/tmp/ch10_lab')"

CONSOLES = {
    "title": ["from pathlib import Path", "Path('spam', 'bacon', 'eggs')"],
    "pathobjects": ["from pathlib import Path, PureWindowsPath",
                     "Path('spam', 'bacon', 'eggs')",
                     "str(Path('spam', 'bacon', 'eggs'))",
                     "str(PureWindowsPath('spam', 'bacon', 'eggs'))",
                     "Path('spam') / 'bacon' / 'eggs'",
                     "'spam' / 'bacon'"],
    "workinglocations": [_RESET,
                          "from pathlib import Path",
                          "Path.cwd().is_absolute()",
                          "Path.home().is_absolute()",
                          "Path('spam/bacon/eggs').is_absolute()",
                          "Path('./spam.txt') == Path('spam.txt')"],
    "pathanatomy": ["from pathlib import PureWindowsPath, PurePosixPath",
                     "p = PureWindowsPath('C:/Users/Al/spam.txt')",
                     "(p.name, p.stem, p.suffix, p.drive)",
                     "p.parent",
                     "p.parts",
                     "p.parents[1]",
                     "p.with_suffix('.csv')",
                     "PurePosixPath('/home/al/reports/spam.txt').relative_to('/home/al')"],
    "folders": [_RESET,
                "from pathlib import Path",
                "Path('delicious/walnut/waffles').mkdir(parents=True)",
                "sorted(p.name for p in Path('.').rglob('*'))",
                "for n in ('project1.txt', 'project2.txt', 'projectX.txt', 'project10.txt'): Path(n).write_text('x')",
                "sorted(Path('.').glob('project?.txt'))",
                "sorted(str(p) for p in Path('.').glob('*.txt'))"],
    "fileinfo": [_RESET,
                 "from pathlib import Path",
                 "import time",
                 "Path('f.txt').write_text('Hello, world!')",
                 "[(q.exists(), q.is_file(), q.is_dir()) for q in (Path('.'), Path('f.txt'), Path('nothing'))]",
                 "Path('f.txt').stat().st_size",
                 "os.utime('f.txt', (1712627129, 1712627129))",
                 "Path('f.txt').stat().st_mtime",
                 "time.asctime(time.gmtime(Path('f.txt').stat().st_mtime))"],
    "wholefile": [_RESET,
                  "from pathlib import Path",
                  "Path('spam.txt').write_text('Hello, world!')",
                  "Path('spam.txt').read_text()",
                  "Path('spam.txt').write_text('caf\\u00e9', encoding='utf-8')",
                  "Path('spam.txt').stat().st_size",
                  "Path('b.bin').write_bytes(bytes([0, 1, 255]))",
                  "Path('b.bin').read_bytes()"],
    "openedfiles": [_RESET,
                    "bacon_file = open('bacon.txt', 'w', encoding='UTF-8')",
                    "bacon_file.write('Hello, world!\\n')",
                    "bacon_file.write('Bacon is not a vegetable.')",
                    "bacon_file.close()",
                    "open('bacon.txt', encoding='UTF-8').read()",
                    "g = open('bacon.txt', encoding='UTF-8')",
                    "g.readlines()",
                    "g.read()",
                    "g.seek(0)",
                    "g.readline()",
                    "g.close()",
                    "open('bacon.txt', 'x')"],
    "textencoding": [_RESET,
                      "from pathlib import Path",
                      "open('a.txt', 'wb').write('caf\\u00e9'.encode('utf-8'))",
                      "open('a.txt', encoding='utf-8').read()",
                      "open('a.txt', encoding='ascii').read()",
                      "open('a.txt', encoding='ascii', errors='replace').read()",
                      "Path('n.txt').write_text('a\\nb', newline='\\r\\n')",
                      "Path('n.txt').read_bytes()",
                      "Path('n.txt').read_text(newline='')"],
    "autoclose": [_RESET,
                  "with open('data.txt', 'w', encoding='UTF-8') as file_obj: file_obj.write('abc')",
                  "file_obj.closed",
                  "file_obj.write('more')"],
    "shelves": [_RESET,
                "import shelve, dbm",
                "shelf_file = shelve.open('mydata')",
                "shelf_file['cats'] = ['Zophie', 'Pooka', 'Simon']",
                "shelf_file.close()",
                "shelf_file = shelve.open('mydata')",
                "list(shelf_file.keys())",
                "shelf_file['cats']",
                "shelf_file.close()",
                "dbm.whichdb('mydata')"],
    "jsonsaving": ["import json",
                   "json.dumps({'cats': ['Zophie'], 'pair': (1, 2), 5: 'five'})",
                   "json.loads(json.dumps({'pair': (1, 2)}))"],
}

# name -> (code, stdin text or None)
PROGRAMS = {
    "madLibs_v1_0_0.py": (B.MAD_LIBS, B.MAD_LIBS_INPUT),
    "regexSearchFiles_v1_0_0.py": (B.REGEX_SEARCH_FILES, B.REGEX_SEARCH_FILES_INPUT),
    "capitalsQuiz_v1_0_0.py": (B.CAPITALS_QUIZ, None),
}
