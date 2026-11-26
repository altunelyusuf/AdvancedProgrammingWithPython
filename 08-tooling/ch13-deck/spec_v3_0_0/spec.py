"""Chapter 13 deck spec 3.0.0 for the generic builder 08-tooling/chapter_deck_build_v2_10_0.py. Deck 3.0.0 of chapter 13 replaces deck 2.0.0 (built by the chapter's own builder deck_build_v2_0_0.py) to meet the
rulings of 2026-11-14 and 2026-11-24: one thing per slide, notes for the reader, plain meanings instead of everyday pictures, code without prompts or lambda, stories as prose. The chapter's content, stories and examples are those of deck 2.0.0."""
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

CH = 13
OUT_DECK = "03-materials/ch13/SEN0414_Ch13_WebScraping_3e_v3_0_0.pptx"
OUT_MAN = "03-materials/ch13/page/chapter_code_ch13_v1_1_0.json"
IMAGE_FILES = ["story_images_v3_0_0.json"]
TITLE = "Chapter 13: Web Scraping"
SUBTITLE = "Chapter 13 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course"
CORE_TITLE = "SEN0414 Chapter 13: Web Scraping (lecture deck 3.0.0)"
WHEELS = {}
MANIFEST_VERSION = "1.1.0"
MANIFEST_ABOUT = ("The code examples of the chapter 13 deck, in the order of the code slides (order = slide order). The page's Slide code tab lists them by name in this order; "
                  "every example is self-contained and runs with the Python standard library only, opens no network connection, reads no keyboard and opens no window (a page in a browser cannot reach the web, "
                  "so the third-party tools of the chapter are shown by their standard-library counterparts and by small stand-ins, named beside the code).")
LIBRARIES = "the Python standard library"
PAGE_REQUIREMENTS = ["The Python standard library modules urllib.parse, urllib.request (urlopen on a data: address), urllib.robotparser, http, webbrowser (the examples replace webbrowser.open by a recording function), json, os, tempfile, re, contextlib, html.parser and xml.etree.ElementTree (imported by the examples that use them)",
                     "A writable temporary folder (the chunks example); no subprocess, no keyboard input, no network, no browser window"]
