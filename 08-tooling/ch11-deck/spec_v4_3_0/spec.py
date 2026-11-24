"""Chapter 11 deck spec 4.3.0 (Lineage11: the hidden Windows set-up of source 1.3.0 added to every example; earlier 4.2.0 (for deck 4.1.0: source 1.2.0 with the imports each code needs, three titles that now match their code, notes 4.0.0 written for the one-box code and the real output; manifest 1.4.0). visuals 4.1.0 (the copytree comparison read the entries relative to their folder twice and showed "same names: False"). Earlier text: Chapter 11 deck spec 4.1.0 (a copy of 4.0.0 that writes manifest 1.3.0 with the hidden setup of each example; the deck file is unchanged). Earlier text: Chapter 11 deck spec 4.0.0 for the generic builder 08-tooling/chapter_deck_build_v2_7_0.py (Lineage11). Deck 4.0.0 holds the code of the single source 03-materials/ch11/source/ch11_code_source_v1_1_0.json: each code in ONE box, the sample files made by hidden setup lines, the book's own code. Chapter 3.0.0 text follows, kept as a record: Chapter 11 deck spec 3.0.0 for the generic builder 08-tooling/chapter_deck_build_v2_5_0.py. Deck 3.0.0 of chapter 11 replaces deck 2.0.0 (built by the chapter's own builder
08-tooling/ch11-deck/deck_build_v2_0_0.py) to meet the six rulings of 2026-11-14: plain code without prompts, notes that carry the lecture, a Slide code tab, stories as prose.
The examples (examples_v3_0_0.py) and the visuals (visuals_v3_0_0.py) are those of 2.0.0 with the changes the rulings force; the words are content_v3_0_0.py; the notes are notes_v3_0_0.py."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(1, os.path.join(os.path.dirname(_HERE), 'spec_v3_0_0'))   # the content words and the notes that did not change stay in the 3.0.0 files
import examples_v4_3_0 as X
import visuals_v4_1_0 as V
import content_v3_0_0 as T0
import notes_v4_3_0 as N0


class _T:
    """the content words with the notes of this version"""
    NOTES = N0.NOTES
    STORY_NOTES = N0.STORY_NOTES
    RESULT_SAYS = N0.RESULT_SAYS
    TAKEAWAY = {**T0.TAKEAWAY, **N0.TAKEAWAY}

    def __getattr__(self, k):
        return getattr(T0, k)


T = _T()

CH = 11
OUT_DECK = "03-materials/ch11/SEN0414_Ch11_OrganizingFiles_3e_v4_2_0.pptx"
OUT_MAN = "03-materials/ch11/page/chapter_code_ch11_v1_5_0.json"
IMAGE_FILES = ["story_images_v2_0_0.json"]
TITLE = "Chapter 11: Organizing Files"
SUBTITLE = "Chapter 11 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course"
CORE_TITLE = "SEN0414 Chapter 11: Organizing Files (lecture deck 4.1.0)"
WHEELS = {}
MANIFEST_VERSION = "1.5.0"
MANIFEST_ABOUT = ("The code examples of the chapter 11 deck, in the order of the code slides (order = slide order). The page's Slide code tab lists them by name in this order; "
                  "every example is self-contained, works in its own new temporary folder (tempfile.mkdtemp) and runs with the Python standard library only (os, shutil, tempfile, zipfile, re, pathlib); "
                  "it reads no keyboard and opens no window, and writes nothing outside its folder. Each example carries its hidden setup lines (made sample files in a new temporary folder); the page runs setup then code and shows only the code.")
LIBRARIES = "the Python standard library only"
PAGE_REQUIREMENTS = ["The Python standard library modules os, shutil, tempfile, zipfile, re and pathlib; every example works in its own temporary folder and writes nothing outside it"]
