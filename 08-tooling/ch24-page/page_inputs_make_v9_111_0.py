#!/usr/bin/env python3
"""Writes the page inputs of the chapter 24 page v9.111.0 (Lineage14; built from the deck 4.0.0 and its chapter-code manifest 03-materials/ch24/page/chapter_code_ch24_v1_0_0.json):
  03-materials/ch24/page/chapter_code_ch24_v1_1_0.json   the manifest of the deck with a "recorded" reason on every example (16 of 16: a browser has no speech system, no ffmpeg and cannot start programs)
  08-tooling/ch24-deck/examples_out_v9_111_0.json        one Lab / Playground cell per manifest example, same code, same order
  08-tooling/ch24-page/stories_img_v9_111_0.json         the six story pictures of the deck 4.0.0 (files and licences in 03-materials/ch24/assets/story_images_v1_0_0.json), keyed by the ids of sen0414_ch24_stories_v2_0_0.py
  08-tooling/ch24-page/standin_v1_0_1.json               standin 1.0.0 with a new notice, one note for each example of the deck, and picture captions without the numbers of the first run
Refuses to overwrite an existing file. Usage: page_inputs_make_v9_111_0.py"""
__version__ = "9.111.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, "..", ".."))
sys.path.insert(0, os.path.join(R, "08-tooling/ch24-deck/spec_v4_0_0"))
def put(path, obj):
    if os.path.exists(path): sys.exit("refusing to overwrite " + path)
    json.dump(obj, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", os.path.relpath(path, R))
man = json.load(open(os.path.join(R, "03-materials/ch24/page/chapter_code_ch24_v1_0_0.json"), encoding="utf-8"))
BASE = "It needs a speech system, ffmpeg and packages that a browser does not have, and a browser cannot start a program."
WHY = {
    "pins": "It reads the installed packages and the programs on the PATH of the machine that made the deck, and a browser has none of them.",
    "say": BASE + " It also starts child processes that call runAndWait() twice.",
    "voices": BASE + " The voices it lists are those of eSpeak NG.",
    "rate": BASE + " It also measures the audio of each setting in a fresh process.",
    "wav": BASE + " It also reads the WAV file that the engine wrote.",
    "models": "It loads three Whisper models, which are files of 75 to 484 megabytes, and a browser has neither torch nor the model files.",
    "trans": "It transcribes audio with three Whisper models, and a browser has neither Whisper nor the speech of eSpeak NG to transcribe.",
    "ffmpeg": "It starts the program ffmpeg through Whisper's load_audio(), and a browser cannot start a program.",
    "lang": "It transcribes three sentences with two Whisper models, and a browser has neither Whisper nor eSpeak NG.",
    "cues": "It writes subtitle files with whisper.utils, which a browser does not have.",
    "opt": "It transcribes a recording with Whisper and writes subtitle files, and a browser has neither Whisper nor the recording.",
    "ytm": "It reads a page of the Internet Archive with yt-dlp, which a browser does not have and which would need the network.",
    "ytd": "It downloads audio with yt-dlp and converts it with ffmpeg, which a browser does not have and cannot start.",
    "guess": BASE + " It also writes four WAV files.",
    "song": BASE + " It also writes the WAV files of 3 and of 99 verses.",
    "tube": "It downloads audio with yt-dlp, transcribes it with Whisper and writes subtitle files, and a browser has none of them.",
}
man2 = dict(man); man2["version"] = "1.1.0"; man2["_note"] = "Version 1.1.0 over 1.0.0: the same examples with a 'recorded' reason on all 16, because a browser has no speech system, no ffmpeg and cannot start programs."
man2["examples"] = [dict(e, recorded=WHY[e["id"]]) for e in man["examples"]]
put(os.path.join(R, "03-materials/ch24/page/chapter_code_ch24_v1_1_0.json"), man2)
ex = {"_version": "9.111.0", "_note": "Made from the chapter-code manifest 03-materials/ch24/page/chapter_code_ch24_v1_0_0.json (same code, same order): one cell per manifest example, name = the example's name."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
put(os.path.join(R, "08-tooling/ch24-deck/examples_out_v9_111_0.json"), ex)
lic = json.load(open(os.path.join(R, "03-materials/ch24/assets/story_images_v1_0_0.json"), encoding="utf-8"))
MAP = {"Kempelen1789": "image_kempelen.jpg", "Voder1939": "image_voder.jpg", "Reddy1969": "image_reddy.jpg", "Captions1971": "image_captions.jpg", "DaisyBell1961": "image_ibm7090.jpg", "Gettysburg1863": "image_gettysburg.jpg"}
si = {"_version": "9.111.0", "_note": "Story pictures for the chapter 24 page's Stories tab: files in 03-materials/ch24/assets, licences in story_images_v1_0_0.json there; the same mapping as the chapter 24 deck 4.0.0; credit = the deck's SlideCredit."}
for sid, fn in MAP.items(): si[sid] = [{"file": fn, "credit": lic[fn]["SlideCredit"]}]
put(os.path.join(H, "stories_img_v9_111_0.json"), si)
old = json.load(open(os.path.join(H, "standin_v1_0_0.json"), encoding="utf-8"))
notice = ("Python and libraries on this page: the page's own programs (the playground) run in your browser, in Python 3.13.2, while the chapter's examples ran under Python 3.14.6 on Linux with pyttsx3 2.99, openai-whisper 20250625, yt-dlp 2026.11.23, torch 2.15.0 (CPU), NumPy 2.5.4, eSpeak NG 1.51 and ffmpeg 6.1.1. "
          "Some recorded examples also ran under Python 3.12.3 with pyttsx3 2.98 (the pinned release of the book) and under a Python 3.14.6 with no packages. A browser has no eSpeak NG or ffmpeg, cannot start programs and does not have pyttsx3, Whisper or yt-dlp, so none of the 74 examples of the chapter runs here: every one is shown as recorded under Python 3.14.6, not run, each with its reason. "
          "Stand-ins: there is no sound card, so nothing was heard and the speech went to WAV files, a local stand-in for a loudspeaker; a public-domain reading of the Gettysburg Address from the Internet Archive stands in for YouTube, from which nothing was downloaded. "
          "The five pictures under five concepts were drawn by programs of the first deck from audio that eSpeak NG spoke; they were not made on this page. "
          "The deck, whose text is the Lecture tab, is the deck 4.0.0 (42 slides). Its 16 examples are those of the Chapter code tab; they ran for the deck under Python 3.14.6 on this machine, and none of them runs in a browser, so all 16 are shown as recorded, each with its reason. "
          "Windows, macOS, a sound card, a microphone and a graphics card were never used.")
import notes_v4_0_0 as N
SUF = " Recorded under Python 3.14.6 with pyttsx3 2.99, openai-whisper 20250625 and yt-dlp 2026.11.23; it does not run on this page."
notes = {e["name"]: N.RESULT_SAYS[e["id"]] + SUF for e in man["examples"]}
pics = json.loads(json.dumps(old["pictures"]))
def cut(k, a, b):
    c = pics[k][0]["caption"]; assert a in c, (k, a); pics[k][0]["caption"] = c.replace(a, b)
cut("WavFormat", ", 1.54 s.", ".")
cut("FfmpegRequired", " (43129 samples)", "")
cut("SongAudio", " (18.3 s)", "")
for k in pics:
    cut(k, "from audio that eSpeak NG 1.51 spoke through pyttsx3 2.99 under Python 3.14.6;", "from audio that eSpeak NG 1.51 spoke through pyttsx3 2.99 under Python 3.14.6 for the first deck;")
new = dict(old); new["notice"] = notice; new["example_notes"] = notes; new["pictures"] = pics; new["_version"] = "1.0.1"
put(os.path.join(H, "standin_v1_0_1.json"), new)
