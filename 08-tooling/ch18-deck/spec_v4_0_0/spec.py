"""Chapter 18 deck spec 4.0.0 for the generic builder 08-tooling/chapter_deck_build_v2_10_0.py (Lineage13). Deck 4.0.0 replaces deck 3.0.0: the six concept slides state what each concept is and does (no everyday analogy), the notes speak to the reader and link to related slides, every code slide carries two result balloons, and the text frames of slide 43 no longer overlap. The examples are examples_v2_0_0.py (unchanged); the visuals are visuals_v4_0_0.py (one slide changed); the words are content_v4_0_0.py; the notes are notes_v4_0_0.py."""
import hashlib
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import examples_v2_0_0 as X
import visuals_v4_0_0 as V
import content_v4_0_0 as T0
import notes_v4_0_0 as N0


class _T:
    """the content words with the notes of this version"""
    NOTES = N0.NOTES
    STORY_NOTES = N0.STORY_NOTES
    RESULT_SAYS = N0.RESULT_SAYS

    def __getattr__(self, k):
        return getattr(T0, k)


T = _T()

CH = 18
OUT_DECK = "03-materials/ch18/SEN0414_Ch18_CSVJSONXML_3e_v4_0_0.pptx"
OUT_MAN = "03-materials/ch18/page/chapter_code_ch18_v1_2_0.json"
IMAGE_FILES = ["story_images_v2_0_3.json"]
TITLE = "Chapter 18: CSV, JSON and XML Files"
SUBTITLE = "Chapter 18 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course"
CORE_TITLE = "SEN0414 Chapter 18: CSV, JSON and XML Files (lecture deck 4.0.0)"
_ASSETS = os.path.normpath(os.path.join(_HERE, "..", "..", "..", "03-materials", "ch18", "assets"))
WHEELS = {w: hashlib.sha256(open(os.path.join(_ASSETS, w), "rb").read()).hexdigest() for w in sorted(os.listdir(_ASSETS)) if w.endswith(".whl")}
MANIFEST_VERSION = "1.2.0"
MANIFEST_ABOUT = ("The code examples of the chapter 18 deck, in the order of the code slides (order = slide order). The page's Slide code tab lists them by name in this order; "
                  "every example is self-contained, uses the Python standard library (csv, json, xml.etree.ElementTree, io, os, tempfile) and, in three places, xmltodict, defusedxml and openpyxl, runs offline, "
                  "reads no keyboard and opens no window. The data lives in memory (io.StringIO, io.BytesIO) or in a fresh temporary folder. The book's own files (example.csv, exampleWithHeader3.csv, example3.xlsx, "
                  "my_data.xml, the removeCsvHeader folder) are not used: each example builds a small stand-in, and the slide says so. The Windows line-end example is a stand-in too: an io.TextIOWrapper "
                  "asked for CRLF plays Windows. What an example prints is the same under xmltodict 0.13.0 and 1.0.4 (the examples avoid what differs: entities are only parsed by defusedxml and ElementTree).")
LIBRARIES = "xmltodict 1.0.4, defusedxml 0.7.1, openpyxl 3.1.5 (also checked with xmltodict 0.13.0), and the standard library"
PAGE_REQUIREMENTS = ["xmltodict 1.0.4, defusedxml 0.7.1, openpyxl 3.1.5 and its one dependency et_xmlfile 2.0.0, the pure-Python wheels that the page embeds (03-materials/ch18/assets) and installs into its browser Python before the first example runs",
                     "the standard library modules csv, json, io, os, tempfile and xml.etree.ElementTree, and the built-ins print, len, range, enumerate, sorted, list, dict, tuple, int, str, type, set, repr, hasattr, next, getattr, open",
                     "A writable temporary folder (the file examples); no subprocess, no keyboard input, no network, no browser window"]
