"""Chapter 12 deck spec 3.1.0 for the generic builder 08-tooling/chapter_deck_build_v2_10_0.py. Deck 3.1.0 of chapter 12 replaces deck 2.0.0 (built by the chapter's own builder deck_build_v2_0_0.py) to meet the
rulings of 2026-11-14 and 2026-11-24: one thing per slide, notes for the reader, plain meanings instead of everyday pictures, code without prompts or lambda, stories as prose. The chapter's content, stories and examples are those of deck 2.0.0."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import examples_v3_1_0 as X
import visuals_v3_1_0 as V
import content_v3_1_0 as T0
import notes_v3_1_0 as N0


class _T:
    """the content words with the notes of this version"""
    NOTES = N0.NOTES
    STORY_NOTES = N0.STORY_NOTES
    RESULT_SAYS = N0.RESULT_SAYS

    def __getattr__(self, k):
        return getattr(T0, k)


T = _T()

CH = 12
OUT_DECK = "03-materials/ch12/SEN0414_Ch12_CommandLinePrograms_3e_v3_1_0.pptx"
OUT_MAN = "03-materials/ch12/page/chapter_code_ch12_v1_2_0.json"
IMAGE_FILES = ["story_images_v2_0_0.json"]
TITLE = "Chapter 12: Command-Line Programs"
SUBTITLE = "Chapter 12 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course"
CORE_TITLE = "SEN0414 Chapter 12: Command-Line Programs (lecture deck 3.1.0)"
WHEELS = {}
MANIFEST_VERSION = "1.2.0"
MANIFEST_ABOUT = ("The code examples of the chapter 12 deck, in the order of the code slides (order = slide order). The page's Slide code tab lists them by name in this order; "
                  "every example is self-contained, works in its own new temporary folder or on text in memory, and runs with the Python standard library; it reads no keyboard, opens no window and writes nothing outside its folder.")
LIBRARIES = "the Python standard library"
PAGE_REQUIREMENTS = ["The Python standard library only; every example works in its own temporary folder or on text in memory and writes nothing outside it"]
