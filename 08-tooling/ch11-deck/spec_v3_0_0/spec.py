"""Chapter 11 deck spec 3.0.0 for the generic builder 08-tooling/chapter_deck_build_v2_5_0.py. Deck 3.0.0 of chapter 11 replaces deck 2.0.0 (built by the chapter's own builder
08-tooling/ch11-deck/deck_build_v2_0_0.py) to meet the six rulings of 2026-11-14: plain code without prompts, notes that carry the lecture, a Slide code tab, stories as prose.
The examples (examples_v3_0_0.py) and the visuals (visuals_v3_0_0.py) are those of 2.0.0 with the changes the rulings force; the words are content_v3_0_0.py; the notes are notes_v3_0_0.py."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import examples_v3_1_0 as X
import visuals_v3_0_0 as V
import content_v3_0_0 as T0
import notes_v3_1_0 as N0


class _T:
    """the content words with the notes of this version"""
    NOTES = N0.NOTES
    STORY_NOTES = N0.STORY_NOTES
    RESULT_SAYS = N0.RESULT_SAYS

    def __getattr__(self, k):
        return getattr(T0, k)


T = _T()

CH = 11
OUT_DECK = "03-materials/ch11/SEN0414_Ch11_OrganizingFiles_3e_v3_0_0.pptx"
OUT_MAN = "03-materials/ch11/page/chapter_code_ch11_v1_1_0.json"
IMAGE_FILES = ["story_images_v2_0_0.json"]
TITLE = "Chapter 11: Organizing Files"
SUBTITLE = "Chapter 11 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course"
CORE_TITLE = "SEN0414 Chapter 11: Organizing Files (lecture deck 3.0.0)"
WHEELS = {}
MANIFEST_VERSION = "1.1.0"
MANIFEST_ABOUT = ("The code examples of the chapter 11 deck, in the order of the code slides (order = slide order). The page's Slide code tab lists them by name in this order; "
                  "every example is self-contained, works in its own new temporary folder (tempfile.mkdtemp) and runs with the Python standard library only (os, shutil, tempfile, zipfile, re, pathlib); "
                  "it reads no keyboard and opens no window, and writes nothing outside its folder.")
LIBRARIES = "the Python standard library only"
PAGE_REQUIREMENTS = ["The Python standard library modules os, shutil, tempfile, zipfile, re and pathlib; every example works in its own temporary folder and writes nothing outside it"]
