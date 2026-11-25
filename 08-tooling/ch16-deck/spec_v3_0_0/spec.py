"""Chapter 16 deck spec 3.0.0 for the generic builder 08-tooling/chapter_deck_build_v2_9_0.py. It moves the chapter 16 deck 2.0.1 (built by the chapter's own builder 08-tooling/ch16-deck/deck_build_v2_0_1.py)
into a spec WITHOUT changing its content: the examples are examples_v3_0_0.py (equal to examples_v2_0_0.py), the visuals visuals_v3_0_0.py (equal to deck_visuals_v2_0_0.py), the words content_v3_0_0.py
(deck_content_v2_0_1.py plus the plan, parts and slide words that the old builder held inline). The rulings of 2026-11-14 and 2026-11-24 are met by the deck story that follows, not here."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import examples_v3_0_0 as X
import visuals_v3_0_0 as V
import content_v3_0_0 as T0
import notes_v3_0_0 as N0


class _T:
    """the content words with the notes of this version"""
    NOTES = N0.NOTES
    STORY_NOTES = N0.STORY_NOTES
    RESULT_SAYS = N0.RESULT_SAYS

    def __getattr__(self, k):
        return getattr(T0, k)


T = _T()

CH = 16
OUT_DECK = "03-materials/ch16/SEN0414_Ch16_SQLiteDatabases_3e_v3_0_0.pptx"
OUT_MAN = "03-materials/ch16/page/chapter_code_ch16_v1_1_0.json"
IMAGE_FILES = ["story_images_v2_0_1.json"]
TITLE = "Chapter 16: SQLite Databases"
SUBTITLE = "Chapter 16 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course"
CORE_TITLE = "SEN0414 Chapter 16: SQLite Databases (lecture deck 3.0.0)"
WHEELS = {}
MANIFEST_VERSION = "1.1.0"
MANIFEST_ABOUT = ("The code examples of the chapter 16 deck, in the order of the code slides (order = slide order). The page's chapter-code tab lists them by NAME in this order; every example is self-contained, "
                  "uses only the Python standard library (sqlite3, os, shutil, tempfile, contextlib), runs offline, reads no keyboard and opens no window. The databases live in memory or in a fresh temporary folder. "
                  "The book's own database sweigartcats.db is not used: the two practice programs run on small stand-in data typed into the example, with the same kinds of columns, and each slide says so. "
                  "Nothing an example prints depends on the SQLite version (a plan text is reduced to its first word, a file size to yes or no).")
LIBRARIES = "the Python standard library (sqlite3, os, shutil, tempfile, contextlib)"
PAGE_REQUIREMENTS = ["The Python standard library modules sqlite3, os, shutil, tempfile and contextlib, and the built-ins print, len, range, enumerate, sorted, list, dict, tuple, int, str, type, set, any, repr, isinstance",
                     "A writable temporary folder (the file examples); no subprocess, no keyboard input, no network, no browser window"]
