"""Chapter 15 deck spec 3.0.0 for the generic builder 08-tooling/chapter_deck_build_v2_10_0.py. Deck 3.0.0 of chapter 15 replaces deck 2.0.0 (built by the chapter's own builder deck_build_v2_0_0.py) to meet the rulings of 2026-11-14 and 2026-11-24: one thing per slide, notes for the reader, plain meanings instead of everyday pictures, code without prompts or lambda, stories as prose. The chapter's content, stories and examples are those of deck 2.0.0."""
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

CH = 15
OUT_DECK = "03-materials/ch15/SEN0414_Ch15_GoogleSheets_3e_v3_0_0.pptx"
OUT_MAN = "03-materials/ch15/page/chapter_code_ch15_v1_1_0.json"
IMAGE_FILES = ["story_images_v2_0_0.json"]
TITLE = "Chapter 15: Google Sheets"
SUBTITLE = "Chapter 15 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course"
CORE_TITLE = "SEN0414 Chapter 15: Google Sheets (lecture deck 3.0.0)"
WHEELS = {"ezsheets-2026.4.28-py3-none-any.whl": "d6680fc5095fce09feda754ca430eb710dcec41728b665fdaea7326fcdf95ea3",
          "google_api_core-2.42.0-py3-none-any.whl": "b1bdf4f72dc4f910736ce4ba49038352effbbc309579215107649b22973a1317",
          "google_api_python_client-2.201.0-py3-none-any.whl": "4b2de61537fd1e48c6ade72ac630d09a8139f9ac72bd70cf145e0d4ad7fe70ae",
          "google_auth-2.61.0-py3-none-any.whl": "ca60266a37475ae68b63bac007272f46094b3d571abe92aded329b6cfb568025",
          "google_auth_httplib2-0.4.4-py3-none-any.whl": "bbe5d7b2401bb3a4017f4720e1e91bd273ab9a2bb60b84e65edbc0de127852da",
          "google_auth_oauthlib-1.5.0-py3-none-any.whl": "71625fdea21c6c03217eb9ff13741c3096e6d257ebca0ad084dbd6e9f4aa4ef4",
          "googleapis_common_protos-1.75.5-py3-none-any.whl": "d7285525c23039db98f2463e6d5a4f9b958b94d497f03a844ece3259c4e72d5d",
          "httplib2-0.32.0-py3-none-any.whl": "dc6705cacdf3fb0a2aba7629fa33c90fd93e30035db0c157325826be177e4816",
          "oauthlib-4.0.0-py3-none-any.whl": "624c28c13a0a59cabf9747dfa52af63be3e512a7f2714df16e91b5b3a145e6cd",
          "proto_plus-1.29.0-py3-none-any.whl": "8acd070469a7aaf43f440b022ef9757c8cac1a9f866e933f59ae98669ddc6c8b",
          "pyasn1-0.6.4-py3-none-any.whl": "deda9277cfd454080ec40b207fb6df82206a3a2688735233cdcd8d3d565f088b",
          "pyasn1_modules-0.4.2-py3-none-any.whl": "29253a9207ce32b64c3ac6600edc75368f98473906e8fd1043bd6b5b1de2c14a",
          "requests_oauthlib-2.0.0-py2.py3-none-any.whl": "7dd8a5c40426b779b0868c404bdef9768deccf22749cde15852df527e6269b36",
          "uritemplate-4.2.0-py3-none-any.whl": "962201ba1c4edcab02e60f9a0d3821e82dfc5d2d6662a21abd533879bdb8a686"}
MANIFEST_VERSION = "1.1.0"
MANIFEST_ABOUT = ("The code examples of the chapter 15 deck, in the order of the code slides (order = slide order). The page's chapter-code tab lists them by name in this order; every example is self-contained, runs offline, reads no keyboard and opens no window. "
                  "GOOGLE WAS NEVER REACHED: every example that touches a spreadsheet runs the real ezsheets library and the real google-api-python-client against the module google_standin, a stand-in for Google's answers that keeps every cell as text and parses nothing; "
                  "so a result shows what the library asks for and what it does with an answer, not what Google answers. The chapter's public sheets (Boringcoin, Bean Count, produceSales3, Sweigart Books) are replaced by small stand-ins typed into the example, with the same columns, and each slide says so.")
LIBRARIES = "ezsheets 2026.4.28, google-api-python-client 2.201.0 and the Python standard library, with the stand-in google_standin 1.0.0"
PAGE_REQUIREMENTS = [
                     "The page installs the module google_standin (file above) into its browser Python under that name, and unpacks the pure-Python wheels listed in data_files (ezsheets 2026.4.28 and the Google client libraries; the wheels are those of the page 03-materials/ch15/page/sen0414_ch15_page_v9_30_0.html, 08-tooling/ch15-page/pywheels_v1_0_0.json) before the first example runs; Pyodide's own packages ssl, protobuf, cryptography, requests, pyparsing, cachetools, certifi, urllib3, idna, charset-normalizer and packaging are loaded first",
                     "the standard library modules json, pickle, hashlib, base64, datetime, types, time, os, tempfile, sys and urllib.parse, and the built-ins print, len, range, enumerate, sorted, set, list, dict, int, str, type, sum",
                     "A writable temporary folder (the upload example); no subprocess, no keyboard input, no network, no browser window"
]
