"""Chapter 17 deck spec 4.0.0 (Lineage10: no everyday analogies: content 4.0.0 and notes 4.0.0, built by the generic builder 2.9.0; earlier 3.0.0: for the generic builder 08-tooling/chapter_deck_build_v2_6_0.py. Deck 3.0.0 of chapter 17 replaces deck 2.1.0 (built by the chapter's own builder 08-tooling/ch17-deck/deck_build_v2_1_0.py)
to meet the six rulings of 2026-11-14 and the handover of 2026-11-19: plain code without prompts or lambda, notes for the reader, stories as prose, speech balloons on the existing slides.
The examples are examples_v3_0_0.py (spec_v3_0_0) and the visuals visuals_v4_0_0.py (the note of slide 7 kept inside the slide), the words content_v4_0_0.py, the notes notes_v4_0_0.py."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(1, os.path.join(_HERE, "..", "spec_v3_0_0"))
import examples_v3_0_0 as X
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

CH = 17
OUT_DECK = "03-materials/ch17/SEN0414_Ch17_PDFAndWordDocuments_3e_v4_0_0.pptx"
OUT_MAN = "03-materials/ch17/page/chapter_code_ch17_v1_2_0.json"
IMAGE_FILES = ["story_images_v2_1_0.json"]
TITLE = "Chapter 17: PDF and Word Documents"
SUBTITLE = "Chapter 17 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course"
CORE_TITLE = "SEN0414 Chapter 17: PDF and Word Documents (lecture deck 4.0.0)"
WHEELS = {}
MANIFEST_VERSION = "1.2.0"
MANIFEST_ABOUT = ("The code examples of the chapter 17 deck, in the order of the code slides (order = slide order). The page's Slide code tab lists them by name in this order; "
                  "every example is self-contained, keeps its documents in memory (io.BytesIO) or in its own new temporary folder (tempfile.mkdtemp), and runs with pypdf, python-docx and Pillow and the Python standard library; "
                  "it reads no keyboard and opens no window, and writes nothing outside its folder.")
LIBRARIES = "pypdf, python-docx and Pillow, with the Python standard library"
PAGE_REQUIREMENTS = ["The packages pypdf, python-docx and Pillow with the Python standard library; every example keeps its documents in memory or in its own temporary folder and writes nothing outside it"]
