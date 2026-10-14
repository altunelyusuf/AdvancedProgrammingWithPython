"""Writes limits_v1_0_0.json, the chapter 24 page's 'Provenance & known limits' entries, from the records the research made
(live_observations_v1_0_0.json, interpreter_record_v1_0_0.json, third_party_record_v1_0_0.json, model_runtimes_v1_0_0.json), pywheels_v1_0_0.json, standin_v1_0_0.json
and the 'Not executed' sentence of sen0414_ch24_rdodi_data_v1_0_2.py. Numbers are read from those files. Usage: limits_make_v1_0_0.py"""
__version__ = "1.0.0"
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(H, n)))
lv, ir, pw, so, tp = J("live_observations_v1_0_0.json"), J("interpreter_record_v1_0_0.json"), J("pywheels_v1_0_0.json"), J("standin_v1_0_0.json"), J("third_party_record_v1_0_0.json")
src = open(os.path.join(H, "..", "sen0414_ch24_rdodi_data_v1_0_2.py"), encoding="utf-8").read()
live = {i["what"]: i["saw"] for i in lv["items"]}
find = lambda start: next(v for k, v in live.items() if k.startswith(start))
m = re.search(r"Not executed, and said so where it comes up: (.*?)\.\s+The chapter's \d+ listings", src, re.S)
notexec = re.sub(r"\s+", " ", m.group(1)).strip()
pg = find("chapter 24 page: status"); mat = find("online materials of the 3rd edition: status"); files = find("online materials: the files")
rec = so["recorded"]; pics = so["pictures"]
nint = len(ir["interpreters"]); t = tp["tally"]
out = []
out.append("Python and libraries on this page: the page's own playground runs in your browser, in Python 3.13.2, while the research ran Python 3.14.6 on Linux with pyttsx3 2.99, openai-whisper 20250625, yt-dlp 2026.8.19, torch 2.14.1 (CPU), NumPy 2.5.4, eSpeak NG 1.51 and ffmpeg 6.1.1 (and other releases where a section says so).")
out.append("Recorded, not run: all %d examples of the chapter. A browser's Python (its platform is 'emscripten') has no speech engine and no ffmpeg, does not have pyttsx3, Whisper or yt-dlp and cannot start programs (it raises OSError 'emscripten does not support processes'); each example is shown with its output recorded under Python 3.14.6, labelled 'Recorded, not run on this page', with its reason: %s." % (len(rec), ", ".join(sorted(rec))))
out.append("Stand-ins: no sound card was present, so nothing was heard and the speech went to WAV files, a local stand-in for a loudspeaker; archive.org public-domain audio (LibriVox readings of the Gettysburg Address) stands in for YouTube, from which the research never downloaded anything.")
out.append("Pictures: %d recorded pictures drawn by the deck's programs from audio that eSpeak NG spoke (under %s) are shown beside their examples, labelled 'Recorded picture, not made on this page'; they are SHA-256 checked when the page is made." % (len(pics), ", ".join(sorted(pics))))
out.append("No wheel is embedded on this page, no Whisper model file and no file of the book's online materials (a zip of {:,} bytes holding %d files; hello_tts.py is the one that imports pyttsx3). The licence of the zip and of its files is an open question for the owner (03-materials/ch24/assets/ASSETS_PROVENANCE_v1_0_0.md).".format(mat[1]) % files["files"])
out.append("Findings, not successes: transcription with the Whisper models medium and turbo was killed at about 6 GB of memory on the research machine, and large-v3 (3,087,371,615 bytes) does not load there; tiny, base and small ran (model_runtimes_v1_0_0.json).")
out.append("NOT EXECUTED: " + notexec + ".")
out.append("What the public sites answered on 2026-10-14 is in live_observations_v1_0_0.json: the chapter's page (status %d, %s bytes, equal to the digest in the book's ontology) and the book's other pages, PyPI and the Whisper model files; YouTube asked for metadata answered with a bot check and nothing was downloaded from it. The chapter pins pyttsx3 2.98 and openai-whisper 20231117 (Appendix A); the newest releases are 2.99 and 20250625." % (pg[0], "{:,}".format(pg[1])))
out.append("One program was run under %d interpreters (%s): %d of %d items differ between them (the modules PEP 594 removed); the Whisper program under the same %d interpreters (%d of %d items differ). Releases: %d of pyttsx3 (%d of %d items differ), %d of openai-whisper (%d of %d items differ) and %d of yt-dlp (%d of %d items differ); see interpreter_record_v1_0_0.json. The chapter's 17 listings were replayed as %d printed statements in four environments (%d, %d, %d and %d of them match the book: newest, pinned, empty and no ffmpeg)." % (nint, ", ".join(ir["interpreters"]), len(ir["differ"]), ir["items compared"], len(ir["whisper interpreters"]), len(ir["whisper differ"]), ir["whisper items compared"], len(ir["pyttsx3 releases"]), len(ir["pyttsx3 differ"]), ir["pyttsx3 items compared"], len(ir["openai-whisper releases"]), len(ir["openai-whisper differ"]), ir["openai-whisper items compared"], len(ir["yt-dlp releases"]), len(ir["yt-dlp differ"]), ir["yt-dlp items compared"], t["row LATEST"]["statements"], t["row LATEST"]["matched the book"], t["row PINS"]["matched the book"], t["row BARE"]["matched the book"], t["row NOFFMPEG"]["matched the book"]))
json.dump({"_version": __version__, "limits": out}, open(os.path.join(H, "limits_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
for x in out: print("-", x[:200])
