"""Chapter 10 deck spec 3.0.0 for the generic builder 08-tooling/chapter_deck_build_v2_6_0.py. Deck 3.0.0 of chapter 10 replaces deck 2.0.0 (built by the chapter's own builder 08-tooling/ch10-deck/deck_build_v2_0_0.py)
to meet the six rulings of 2026-11-14 and the handover of 2026-11-19: plain code without prompts or lambda, notes for the reader, stories as prose, speech balloons on the existing slides.
The examples are examples_v3_0_0.py, the visuals visuals_v3_0_0.py, the words content_v3_0_0.py, the notes notes_v3_0_0.py."""
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

CH = 10
OUT_DECK = "03-materials/ch10/SEN0414_Ch10_ReadingWritingFiles_3e_v3_0_0.pptx"
OUT_MAN = "03-materials/ch10/page/chapter_code_ch10_v1_1_0.json"
IMAGE_FILES = ["story_images_v3_0_0.json"]
TITLE = "Chapter 10: Reading and Writing Files"
SUBTITLE = "Chapter 10 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course"
CORE_TITLE = "SEN0414 Chapter 10: Reading and Writing Files (lecture deck 3.0.0)"
WHEELS = {}
MANIFEST_VERSION = "1.1.0"
MANIFEST_ABOUT = ("The code examples of the chapter 10 deck, in the order of the code slides (order = slide order). The page's Slide code tab lists them by name in this order; "
                  "every example is self-contained, works in its own new temporary folder (tempfile.mkdtemp) where it touches files and runs with the Python standard library only (os, tempfile, pathlib, re, random, shelve, json); "
                  "it reads no keyboard and opens no window, and writes nothing outside its folder.")
LIBRARIES = "the Python standard library only"
PAGE_REQUIREMENTS = ["The Python standard library modules os, tempfile, pathlib, re, random, shelve and json; every example works in its own temporary folder and writes nothing outside it"]
