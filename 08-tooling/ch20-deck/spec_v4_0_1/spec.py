"""Chapter 20 deck spec 4.0.1 for the generic builder 08-tooling/chapter_deck_build_v2_10_0.py (Lineage13). Deck 4.0.1 replaces deck 4.0.0 (the AT&T story has a sourced photograph; everything else is as in 4.0.0, whose examples and visuals this spec reuses): the five concept slides state what each concept is and does, the notes are written for the reader and name what the run printed, and every code slide carries two result balloons."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "spec_v4_0_0"))
sys.path.insert(0, _HERE)
import examples_v2_0_0 as X
import visuals_v4_0_0 as V
import content_v4_0_1 as T0
import notes_v4_0_1 as N0


class _T:
    """the content words with the notes of this version"""
    NOTES = N0.NOTES
    STORY_NOTES = N0.STORY_NOTES
    RESULT_SAYS = N0.RESULT_SAYS

    def __getattr__(self, k):
        return getattr(T0, k)


T = _T()

CH = 20
OUT_DECK = "03-materials/ch20/SEN0414_Ch20_EmailTextsPushNotifications_3e_v4_0_1.pptx"
OUT_MAN = "03-materials/ch20/page/chapter_code_ch20_v1_2_1.json"
IMAGE_FILES = ["story_images_v1_1_0.json"]
TITLE = "Chapter 20: Sending Email, Texts and Push Notifications"
SUBTITLE = "The Gmail API, mail as a protocol with smtplib, texts by email gateway, push notifications with ntfy"
CORE_TITLE = "SEN0414 Chapter 20: Sending Email, Texts and Push Notifications (lecture deck 4.0.1)"
WHEELS = {}
MANIFEST_VERSION = "1.2.1"
MANIFEST_ABOUT = ("The code examples of the chapter 20 deck, in the order of the code slides (order = slide order). Every example is self-contained and runs offline, reads no keyboard "
                  "and opens no window. Google's service is replaced by unittest.mock.MagicMock (ezgmail.SERVICE_GMAIL), the mail server by a local aiosmtpd server "
                  "(plain and with STARTTLS, using a one-day certificate made by openssl), and the ntfy server by a local http.server recorder; the slide says so (EMULATED). "
                  "The ntfy answer of the polling example and the weather forecast of the umbrella example are typed in, so that the run never changes. No example needs an account.")
LIBRARIES = "ezgmail, requests, aiosmtpd (installed with pip), and the standard library"
PAGE_REQUIREMENTS = ["the packages ezgmail, requests and aiosmtpd, and the standard library modules email, smtplib, ssl, subprocess, http.server, threading, hmac, secrets, json, datetime, html.parser",
                     "on the page (Pyodide) there are no sockets, threads or subprocesses: the examples that start a server, a thread or the openssl command are shown as recorded results, and the chapter-code tab says which"]
