#!/usr/bin/env python3
"""Chapter 24 (Text-to-Speech and Speech Recognition Engines): observes, once, what the public sources the chapter names answer today, what the files the book ships hold, what the
package index says about pyttsx3, openai-whisper, yt-dlp and the packages around them, what the Appendix A of the book pins and what its Appendix B answers, what the model files of Whisper
weigh, what the book's own YouTube video answers to yt-dlp, and which tools of the machine the research programs use, and writes what it saw with the date. A web site changes and the files
of the online materials may be replaced; the record is an observation of the day, not something the build can re-check, and no check reads it.
What it does: fetches the chapter page and compares its SHA-256 with the digest the book's own ontology records; counts what is on the page (listings, tables, headings), asks every external
link of the chapter once without following a redirect; reads Appendix A for the packages the book pins and Appendix B for the answers to the chapter's seven questions; downloads the online
materials of the 3rd edition and looks for the files of chapter 24; reads the newest releases of pyttsx3, openai-whisper, yt-dlp, the PyPI project called whisper, faster-whisper,
SpeechRecognition, gTTS and vosk on PyPI and every release of pyttsx3 and openai-whisper; sends one HEAD request to each of the 14 model files that whisper 20250625 knows; opens every source
of the research record and checks that the passages the research relies on are on the page; asks yt-dlp for the metadata of the video the chapter names (no download: skip_download) and
compares its keys with the keys the chapter prints.
On the machine itself it asks which tools the research programs use (ffmpeg, ffprobe, espeak, espeak-ng, aplay, sox, uv) for their versions, and runs the engine experiment: pyttsx3 is started
with no eSpeak package, with the package the book names (espeak), with espeak-ng and with both, by removing and installing the apt packages in turn (the final state, both installed, is restored).
NOT EXECUTED and said so: the download of the video from YouTube (the chapter's listings 11 and 12 are not run against YouTube: the study asks for the metadata only, as listing 14 does), any
audio device, any GPU, Windows (SAPI5) and macOS (NSSpeechSynthesizer), a photograph from Wikimedia Commons (the pages answered 429 on 2026-10-13 and 2026-10-14).
Run it with an interpreter that has requests and Beautiful Soup (/home/claude/venv314_web/bin/python).
Usage: sen0414_ch24_live_v1_0_0.py   -> ch24-page/live_observations_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, time, zipfile
import requests, bs4
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "08-tooling", "ch24-page", "live_observations_v1_0_0.json")
UA = {"User-Agent": "SEN0414-research/1.0 (academic course; altunel.yusuf@gmail.com)"}
BROWSER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0"}
LATEST = os.environ.get("CH24_LATEST", "/home/claude/venv314_ch24_latest/bin/python")
PINS = os.environ.get("CH24_PINS", "/home/claude/venv312_ch24_pins/bin/python")
BARE = os.environ.get("CH24_BARE", "/home/claude/venv314_ch24_bare/bin/python")
obs = []
ONLY = os.environ.get("CH24_ONLY")   # development switch: run only the observations whose text contains this string (the output then goes to the folder named by CH24_ONLY_OUT)
def see(what, f):
    if ONLY and ONLY not in what: return
    try: v = f()
    except Exception as e: v = "raised %s: %s" % (type(e).__name__, str(e)[:200])
    obs.append({"what": what, "saw": v})
def get(u, **k):
    k.setdefault("headers", UA)
    for attempt in range(7):       # a site that answers 429 or drops the connection is asked again after a pause; the status of the last answer is the one recorded
        try:
            r = requests.get(u, timeout=90, **k)
            if r.status_code != 429: return r
        except requests.ConnectionError:
            if attempt == 6: raise
        time.sleep(25)
    return r
def sha(b): return hashlib.sha256(b).hexdigest()
def norm(t): return re.sub(r"\s+", " ", t)
def visible(r):
    s = bs4.BeautifulSoup(r.content.decode("utf-8", "replace"), "html.parser")
    for x in s(["script", "style"]): x.decompose()
    return norm(s.get_text(" "))
# (id, label, url, primary, phrases found on the page)
SOURCES = [
 ('P01', 'Automate the Boring Stuff with Python, 3rd edition - Chapter 24, Text-to-Speech and Speech Recognition Engines (Al Sweigart, No Starch Press, 2025)', 'https://automatetheboringstuff.com/3e/chapter24.html', True,
  ['pyttsx3', 'SAPI5', 'NSSpeechSynthesizer', 'sudo apt install espeak', 'runAndWait', 'save_to_file', 'openai-whisper', "'large-v3'", 'Table 24-1', 'get_writer', 'yt-dlp', 'sanitize()', 'skip_download', 'Make Python Talk', 'Guess the Number', '99 Bottles of Beer', 'YouTube Transcriber', 'whisper --help']),
 ('P02', 'Online materials of the 3rd edition, zip with 91 files (No Starch Press, 2025)', 'https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', False, []),
 ('P03', 'Automate the Boring Stuff with Python, 3rd edition - table of contents (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/', False, ['Text-to-Speech and Speech Recognition Engines']),
 ('P04', 'Automate the Boring Stuff with Python, 3rd edition - book page (No Starch Press, 2025)', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', False, ['Text-to-Speech and Speech Recognition Engines']),
 ('P05', 'Appendix A, Installing Third-Party Packages (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/appendixa.html', False, ['pyttsx3 == 2.98', 'openai-whisper==20231117', 'numpy<2', 'cu118', 'yt-dlp']),
 ('P06', 'Appendix B, Answers to the Practice Questions (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/appendixb.html', False, ["Whisper’s default model is 'base'", 'engine.setProperty', 'hundreds of video websites']),
 ('P07', 'Make Python Talk, the book the chapter recommends (Mark Liu, No Starch Press, 2021)', 'https://nostarch.com/make-python-talk', False, ['Make Python Talk', 'Mark Liu']),
 ('P08', 'wave - Read and write WAV files, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/wave.html', False, ['getframerate', 'getnframes', 'Wave_write', 'PCM']),
 ('P09', 'pathlib - Object-oriented filesystem paths, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/pathlib.html', False, ['Path.glob', 'recurse_symlinks', 'case_sensitive']),
 ('P10', 'json - JSON encoder and decoder, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/json.html', False, ['json.dumps', 'ensure_ascii', 'TypeError']),
 ('P11', 'subprocess - Subprocess management, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/subprocess.html', False, ['CalledProcessError', 'capture_output', 'stdout']),
 ('P12', 'shutil - High-level file operations, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/shutil.html', False, ['shutil.which', 'PATH']),
 ('P13', 'unittest.mock - mock object library, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/unittest.mock.html', False, ['MagicMock', 'patch', 'side_effect']),
 ('P14', "What's New In Python 3.13 - the modules removed by PEP 594 (Python Software Foundation, 2026)", 'https://docs.python.org/3.13/whatsnew/3.13.html', False, ['aifc', 'audioop', 'sunau', 'chunk', 'sndhdr']),
 ('P15', 'PEP 594 - Removing dead batteries from the standard library (Python Enhancement Proposals, 2026)', 'https://peps.python.org/pep-0594/', False, ['aifc', 'audioop', 'sunau', 'sndhdr', 'wave']),
 ('P16', 'pyttsx3 on the Python Package Index (Python Package Index, 2026)', 'https://pypi.org/pypi/pyttsx3/json', False, ['2.99', 'espeak', 'Text to Speech']),
 ('P17', 'pyttsx3 README on GitHub (pyttsx3 documentation, 2026)', 'https://raw.githubusercontent.com/nateshmbhat/pyttsx3/master/README.md', False, ['pyttsx3', 'espeak', 'offline']),
 ('P18', 'pyttsx3 documentation on Read the Docs (pyttsx3 documentation, 2026)', 'https://pyttsx3.readthedocs.io/en/latest/', False, ['pyttsx3', 'Engine', 'engine']),
 ('P19', 'pyttsx3 eSpeak driver source on GitHub (pyttsx3 source code, 2026)', 'https://raw.githubusercontent.com/nateshmbhat/pyttsx3/master/pyttsx3/drivers/espeak.py', False, ['_espeak', 'wave.open', 'aplay', 'startLoop', 'save_to_file']),
 ('P20', 'pyttsx3 NSSS driver source on GitHub (pyttsx3 source code, 2026)', 'https://raw.githubusercontent.com/nateshmbhat/pyttsx3/master/pyttsx3/drivers/nsss.py', False, ['NSSpeechSynthesizer', 'save_to_file', 'aiff']),
 ('P21', 'pyttsx3 SAPI5 driver source on GitHub (pyttsx3 source code, 2026)', 'https://raw.githubusercontent.com/nateshmbhat/pyttsx3/master/pyttsx3/drivers/sapi5.py', False, ['SAPI', 'SpeechLib', 'save_to_file', 'SSFMCreateForWrite']),
 ('P22', 'eSpeak NG README on GitHub (eSpeak NG developers, 2026)', 'https://raw.githubusercontent.com/espeak-ng/espeak-ng/master/README.md', False, ['eSpeak NG', 'text-to-speech', 'languages']),
 ('P23', 'eSpeak - speech synthesizer (Jonathan Duddington, project page)', 'https://espeak.sourceforge.net/', False, ['eSpeak', 'speech synthesizer', 'WAV']),
 ('P24', 'eSpeak in the Ubuntu 24.04 package archive (Canonical, 2026)', 'https://packages.ubuntu.com/noble/espeak', False, ['espeak', '1.48.15', 'libespeak1']),
 ('P25', 'ESpeak (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/ESpeak', False, ['eSpeak', 'formant synthesis', 'Jonathan Duddington']),
 ('P26', 'Speech Application Programming Interface, SAPI 5.4 (Microsoft Learn, 2026)', 'https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ms720163(v=vs.85)', False, ['SAPI', 'speech']),
 ('P27', 'NSSpeechSynthesizer (Apple Developer Documentation, 2026)', 'https://developer.apple.com/documentation/appkit/nsspeechsynthesizer', False, ['NSSpeechSynthesizer', 'speech']),
 ('P28', 'openai-whisper on the Python Package Index (Python Package Index, 2026)', 'https://pypi.org/pypi/openai-whisper/json', False, ['20250625', 'Robust Speech Recognition', 'ffmpeg']),
 ('P29', 'Whisper README on GitHub (OpenAI, 2026)', 'https://raw.githubusercontent.com/openai/whisper/main/README.md', False, ['tiny', 'turbo', 'ffmpeg', 'Required VRAM', 'whisper audio.flac', 'Relative speed']),
 ('P30', 'Whisper transcribe.py source on GitHub (OpenAI, 2026)', 'https://raw.githubusercontent.com/openai/whisper/main/whisper/transcribe.py', False, ['def transcribe', 'word_timestamps', 'condition_on_previous_text', 'no_speech_threshold', 'cli']),
 ('P31', 'Whisper utils.py source, the subtitle writers, on GitHub (OpenAI, 2026)', 'https://raw.githubusercontent.com/openai/whisper/main/whisper/utils.py', False, ['WriteSRT', 'WriteVTT', 'WriteTSV', 'get_writer', 'format_timestamp']),
 ('P32', 'Whisper audio.py source, the use of ffmpeg, on GitHub (OpenAI, 2026)', 'https://raw.githubusercontent.com/openai/whisper/main/whisper/audio.py', False, ['ffmpeg', 'SAMPLE_RATE', 'load_audio', 'Failed to load audio']),
 ('P33', 'Robust Speech Recognition via Large-Scale Weak Supervision (Radford, Kim, Xu, Brockman, McLeavey and Sutskever, arXiv, 2022)', 'https://arxiv.org/abs/2212.04356', False, ['680,000 hours', 'multilingual', 'weak supervision']),
 ('P34', 'Whisper (speech recognition system) (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Whisper_(speech_recognition_system)', False, ['OpenAI', 'September 2022', '680,000 hours']),
 ('P35', 'whisper on the Python Package Index, the project that is not OpenAI Whisper (Python Package Index, 2026)', 'https://pypi.org/pypi/whisper/json', False, ['whisper', 'Graphite']),
 ('P36', 'PyTorch, get started locally (PyTorch Foundation, 2026)', 'https://pytorch.org/get-started/locally/', False, ['CPU', 'CUDA', 'pip3 install torch']),
 ('P37', 'PyTorch wheel index for CUDA 11.8 (PyTorch Foundation, 2026)', 'https://download.pytorch.org/whl/cu118/', False, ['torch', 'torchvision']),
 ('P38', 'FFmpeg documentation, ffmpeg tool (FFmpeg developers, 2026)', 'https://ffmpeg.org/ffmpeg.html', False, ['-vn', 'audio', 'ffmpeg']),
 ('P39', 'Download FFmpeg (FFmpeg developers, 2026)', 'https://ffmpeg.org/download.html', False, ['Linux', 'Windows', 'macOS']),
 ('P40', 'yt-dlp on the Python Package Index (Python Package Index, 2026)', 'https://pypi.org/pypi/yt-dlp/json', False, ['2026.8.19', 'yt-dlp', 'youtube-dl']),
 ('P41', 'yt-dlp README on GitHub, including embedding yt-dlp in Python (yt-dlp developers, 2026)', 'https://raw.githubusercontent.com/yt-dlp/yt-dlp/master/README.md', False, ['EMBEDDING YT-DLP', 'YoutubeDL', 'sanitize_info', 'extract_info', 'FFmpegExtractAudio']),
 ('P42', 'yt-dlp YoutubeDL.py source on GitHub (yt-dlp developers, 2026)', 'https://raw.githubusercontent.com/yt-dlp/yt-dlp/master/yt_dlp/YoutubeDL.py', False, ['def sanitize_info', 'def download', 'def extract_info', 'def prepare_filename', 'outtmpl']),
 ('P43', 'yt-dlp supported sites (yt-dlp developers, 2026)', 'https://raw.githubusercontent.com/yt-dlp/yt-dlp/master/supportedsites.md', False, ['youtube', 'archive.org', 'Vimeo']),
 ('P44', 'Yt-dlp (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Yt-dlp', False, ['youtube-dl', 'fork', 'command-line']),
 ('P45', 'YouTube Terms of Service (Google, 2026)', 'https://www.youtube.com/t/terms', False, ['Permissions and Restrictions', 'download']),
 ('P46', 'WebVTT: The Web Video Text Tracks Format (W3C Candidate Recommendation Draft, 2026)', 'https://www.w3.org/TR/webvtt1/', False, ['WEBVTT', 'hours', 'cue', '-->']),
 ('P47', 'WebVTT API, Web Video Text Tracks Format (MDN Web Docs, 2026)', 'https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API/Web_Video_Text_Tracks_Format', False, ['WEBVTT', 'cue', 'timestamp']),
 ('P48', 'SubRip (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/SubRip', False, ['.srt', 'comma', 'subtitle']),
 ('P49', 'WebVTT (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/WebVTT', False, ['WebSRT', 'W3C', 'HTML5']),
 ('P50', 'Word error rate (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Word_error_rate', False, ['substitutions', 'deletions', 'insertions']),
 ('P51', 'Speech recognition (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Speech_recognition', False, ['Audrey', 'Bell Labs', 'hidden Markov']),
 ('P52', 'Speech synthesis (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Speech_synthesis', False, ['Voder', 'formant', 'concatenative']),
 ('P53', 'Daisy Bell (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Daisy_Bell', False, ['IBM 7090', 'Bell Labs', 'HAL']),
 ('P54', '99 Bottles of Beer (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/99_Bottles_of_Beer', False, ['99 Bottles of Beer', 'verse', 'song']),
 ('P55', 'LibriVox, about (LibriVox, 2026)', 'https://librivox.org/pages/about-librivox/', False, ['public domain', 'volunteers', 'audiobooks']),
 ('P56', 'The Gettysburg Address, a LibriVox recording on the Internet Archive (LibriVox and the Internet Archive, 2026)', 'https://archive.org/details/gettysburg_shurtagal_librivox', False, ['Gettysburg', 'LibriVox', 'public domain']),
 ('P57', "Alice's Adventures in Wonderland, Project Gutenberg ebook 11 (Project Gutenberg, 2026)", 'https://www.gutenberg.org/ebooks/11', False, ['Alice', 'Carroll', 'Public domain']),
 ('P58', 'Gettysburg Address (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Gettysburg_Address', False, ['Bliss copy', 'Four score and seven years ago', 'Abraham Lincoln']),
 ('P59', 'faster-whisper on the Python Package Index (Python Package Index, 2026)', 'https://pypi.org/pypi/faster-whisper/json', False, ['faster-whisper', 'CTranslate2', 'Whisper']),
 ('P60', 'whisper.cpp README on GitHub (ggml-org, 2026)', 'https://raw.githubusercontent.com/ggml-org/whisper.cpp/master/README.md', False, ['whisper.cpp', 'CPU', 'quantization']),
 ('P61', 'SpeechRecognition on the Python Package Index (Python Package Index, 2026)', 'https://pypi.org/pypi/SpeechRecognition/json', False, ['SpeechRecognition', 'Whisper']),
 ('P62', 'gTTS on the Python Package Index (Python Package Index, 2026)', 'https://pypi.org/pypi/gTTS/json', False, ['gTTS', 'Google Translate']),
 ('P63', 'Vosk on the Python Package Index (Python Package Index, 2026)', 'https://pypi.org/pypi/vosk/json', False, ['vosk', 'offline']),
 ('P64', 'Speech to text guide (OpenAI Platform documentation, 2026)', 'https://platform.openai.com/docs/guides/speech-to-text', False, ['whisper-1', 'transcriptions']),
 ('P65', 'Cloud Text-to-Speech documentation (Google Cloud, 2026)', 'https://cloud.google.com/text-to-speech/docs', False, ['Text-to-Speech', 'API']),
 ('P66', 'What is the Speech service (Microsoft Learn, 2026)', 'https://learn.microsoft.com/en-us/azure/ai-services/speech-service/overview', False, ['speech to text', 'text to speech']),
 ('P67', 'Article 50, Transparency obligations for providers and deployers of certain AI systems, EU AI Act (Future of Life Institute, 2026)', 'https://artificialintelligenceact.eu/article/50/', False, ['synthetic', 'audio', 'deep fake']),
 ('P68', 'whisper-large-v3 model card (Hugging Face, 2026)', 'https://huggingface.co/openai/whisper-large-v3', False, ['whisper-large-v3', '1550', 'hallucinat']),
 ('P69', 'uv documentation (Astral documentation, 2026)', 'https://docs.astral.sh/uv/', False, ['uv', 'Python']),
]
def sources():
    out = []
    for pid, label, url, prim, phrases in SOURCES:
        try:
            r = get(url, headers=BROWSER if ("nostarch.com" in url or "wikipedia.org" in url) else UA); ctype = r.headers.get("content-type", "")
            if "zip" in ctype or url.endswith((".zip", ".pdf")): t = ""
            else:
                t = r.content.decode("utf-8", "replace")
                if "html" in ctype:
                    s = bs4.BeautifulSoup(t, "html.parser")
                    for x in s(["script", "style"]): x.decompose()
                    t = s.get_text(" ")
            t = norm(t).replace("’", "'")
            out.append([pid, r.status_code, len(r.content), {p: (norm(p).replace("’", "'").lower() in t.lower()) for p in phrases}])
        except Exception as e: out.append([pid, "unreachable: %s" % type(e).__name__, 0, {}])
        time.sleep(0.7)
    return out
# 0. the chapter and the book's own record of it
ch = get("https://automatetheboringstuff.com/3e/chapter24.html")
DIGEST = "239d91a73d232342d42b8c6c514a603eb3562681904a53b29f83214ac5462b0b"
ONTO = "/home/claude/Ontologies/automate-python-book-3e/01-ontologies/automate_python_3e_ch24_v1_0_0.ttl"
see("chapter 24 page: status, bytes, SHA-256, equal to the chapterDigest of the book ontology (read from its file when present)", lambda: [ch.status_code, len(ch.content), sha(ch.content), sha(ch.content) == DIGEST, (DIGEST in open(ONTO).read()) if os.path.exists(ONTO) else "ontology file not present"])
soup = bs4.BeautifulSoup(ch.content.decode("utf-8"), "html.parser"); text = norm(soup.get_text(" "))
IMGS = [i["src"] for i in soup.find_all("img") if i.get("src") and "cover" not in i["src"]]
see("chapter 24 page: number of listings (pre elements), figure captions, tables, pictures other than book covers", lambda: [len(soup.find_all("pre")), sorted(set(re.findall(r"Figure 24-\d+", text))), sorted(set(re.findall(r"Table 24-\d+", text))), len(soup.find_all("table")), IMGS])
see("chapter 24 page: the headings of the chapter in order", lambda: [norm(h.get_text()) for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "span"]) if h.name != "span" or (h.get("class") and any("sans_futura" in c for c in h.get("class")))])
STATEMENTS = ("Both pyttsx3 and Whisper are free to use and don't require an internet connection", "sudo apt install espeak", "The name of the package is based on py for Python", "The computer voice speaks at a rate of 200 words per minute",
              "1,800 words into a 10-minute-long audio file in about two seconds", "you must also call the runAndWait() method before Python will create the .wav file", "can save .wav files only, not .mp3 files",
              "the whisper package on the PyPI website refers to something else", "'tiny', 'base', 'small', 'medium', or 'large-v3'", "To find the languages that Whisper supports, you can run whisper --help", "SRT is an older and more widespread standard",
              "TSV isn't an official subtitles format", "the 'base' model should be suitable and the 'medium' model is good enough", "All models produce errors, so the output should always undergo human review",
              "Whisper can accept any audio or video file, and converts it to the format it requires automatically", "By default, Whisper uses your CPU to transcribe text", "installing the latest version of yt-dlp",
              "by calling ydl.sanitize()", "The 'base' and 'medium' models create much higher-quality subtitles than YouTube's current autogenerated subtitles", "Whisper runs on your computer and doesn't connect to online servers except to download the model on first use")
see("chapter 24 page: statements the research relies on (each is on the page of the book: True)", lambda: {s: (norm(s).replace("’", "'").lower() in text.replace("’", "'").lower()) for s in STATEMENTS})
see("chapter 24 page: words the chapter never uses although the topic needs them (False means absent from the page)", lambda: {s: s.lower() in text.lower() for s in ("ffmpeg", "aplay", "ALSA", "sound card", "turbo", "large-v3-turbo", "hallucinat", "consent", "privacy", "copyright", "terms of service", "licence", "license", "word_timestamps", "initial_prompt", "wave module", "AIFF", "mono", "22050", "torch", "numpy", "faster-whisper", "whisper.cpp", "language='tr'", "Turkish", "microphone", "real time", "diariz", "Wayland", "pip install ffmpeg")})
ext = sorted({a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http") and "automatetheboringstuff.com" not in a["href"]})
def link_status():
    out = []
    for u in ext:
        try:
            r = requests.get(u, timeout=60, headers=BROWSER, allow_redirects=False); out.append([u, r.status_code, r.headers.get("Location", "")[:100]])
        except Exception as e: out.append([u, "unreachable: %s" % type(e).__name__, ""])
    return out
see("chapter 24 page: every external link of the chapter, asked once without following a redirect: URL, HTTP status, Location", link_status)
see("chapter 24 page: every URL that appears in the text of the chapter", lambda: sorted({u.rstrip(".,)") for u in re.findall(r"https?://[\w./?=&#%~:+-]+", text) if "automatetheboringstuff.com/3e/chapter24" not in u})[:20])
def appendix():
    a = get("https://automatetheboringstuff.com/3e/appendixa.html"); t = visible(a)
    return [a.status_code, re.findall(r"pyttsx3\s*==\s*[\d.]+", t), re.findall(r"openai-whisper==\d+", t), re.findall(r"numpy\s*<\s*2", t)[:1], re.findall(r"whl/cu\d+", t),
            re.findall(r"In addition, the automateboringstuff3 package always installs[^.]{0,200}\.", t)[:1], re.findall(r"The pytesseract package covered in Chapter 22 and the openai-whisper package covered in Chapter 24[^.]{0,200}\.", t)[:1], "ffmpeg" in t.lower(), "espeak" in t.lower(), "playsound" in t.lower()]
see("Appendix A of the book: status, the pin of pyttsx3, the pin of openai-whisper, the numpy<2 advice, the CUDA index, the sentence about packages always installed at the newest version, the sentence about Whisper, and whether ffmpeg or espeak is named", appendix)
def appendixb():
    a = get("https://automatetheboringstuff.com/3e/appendixb.html"); t = visible(a)
    i = t.find("Chapter 24 1."); j = t.find("INDEX", i)
    return [a.status_code, t[i:j][:1500]]
see("Appendix B of the book: the answers printed for the seven questions of chapter 24", appendixb)
def bookpage():
    r = get("https://nostarch.com/automate-boring-stuff-python-3rd-edition", headers=BROWSER); t = visible(r)
    return [r.status_code, len(r.content), {w: len(re.findall(w, t, re.I)) for w in ("Text-to-Speech and Speech Recognition Engines", "Whisper", "pyttsx3", "yt-dlp")}]
see("the book page at nostarch.com: how often words occur on the page", bookpage)
mat = get("https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip", headers=BROWSER)
see("online materials of the 3rd edition: status, bytes, SHA-256 of the zip", lambda: [mat.status_code, len(mat.content), sha(mat.content)])
def materials():
    z = zipfile.ZipFile(io.BytesIO(mat.content)); names = [n for n in z.namelist() if not n.endswith("/") and "__MACOSX" not in n and not n.split("/")[-1].startswith("._")]
    texts = {n.split("/")[-1]: z.read(n).decode("utf-8", "replace") for n in names if n.endswith(".py")}
    hits = lambda pat: sorted(k for k, v in texts.items() if re.search(pat, v))
    return {"files": len(names), "python files": len(texts), "python files that import pyttsx3": hits(r"pyttsx3"), "python files that import whisper": hits(r"import whisper|from whisper"), "python files that import yt_dlp": hits(r"yt_dlp"),
            "files with tts, speech, whisper, subtitle or srt in the name": sorted(n for n in names if re.search(r"tts|speech|whisper|subtitle|srt|vtt|wav", n, re.I)), "files named hello_tts.py, hello.wav, audio.srt or metadata.json": [n for n in ("hello_tts.py", "hello.wav", "audio.srt", "metadata.json") if n in [x.split("/")[-1] for x in names]]}
see("online materials: the files, and which of them use pyttsx3, Whisper or yt-dlp", materials)
def pypi():
    out = {}
    for n in ("pyttsx3", "openai-whisper", "yt-dlp", "whisper", "torch", "numba", "faster-whisper", "SpeechRecognition", "gTTS", "vosk"):
        j = get("https://pypi.org/pypi/%s/json" % n).json(); i = j["info"]; rel = j["releases"].get(i["version"], [])
        out[n] = {"version": i["version"], "uploaded": rel[0]["upload_time"][:10] if rel else None, "requires_python": i["requires_python"], "summary": (i["summary"] or "")[:110], "requires_dist": sorted((i["requires_dist"] or []))[:14], "yanked": bool(rel and rel[0].get("yanked")), "files": [f["filename"] for f in rel][:4]}
    return out
see("PyPI: the newest release, its upload date, Requires-Python, summary and dependencies of pyttsx3, openai-whisper, yt-dlp, the project called whisper, torch, numba, faster-whisper, SpeechRecognition, gTTS and vosk", pypi)
def releases(name):
    j = get("https://pypi.org/pypi/%s/json" % name).json(); rel = j["releases"]
    def ver(v): return [int(x) for x in re.findall(r"\d+", v)[:4]]
    vs = sorted(rel, key=ver)
    return {"releases": len(vs), "newest": vs[-1], "all": {v: rel[v][0]["upload_time"][:10] for v in vs if rel[v]}}
see("PyPI: every release of pyttsx3 with its upload date (the book pins 2.98)", lambda: releases("pyttsx3"))
see("PyPI: every release of openai-whisper with its upload date (the book pins 20231117)", lambda: releases("openai-whisper"))
see("PyPI: the number of releases of yt-dlp and the newest five with their upload dates", lambda: (lambda r: {"releases": r["releases"], "newest": r["newest"], "last five": dict(list(r["all"].items())[-5:])})(releases("yt-dlp")))
see("sources of the research record: for each, the HTTP status, the bytes, and whether each passage the research relies on is on the page", sources)
# the model files of whisper 20250625
def models():
    code = "import whisper, json; print(json.dumps(whisper._MODELS))"
    m = json.loads(subprocess.run([LATEST, "-W", "ignore", "-c", code], capture_output=True, text=True).stdout)
    out = {}
    for name, url in m.items():
        r = requests.head(url, timeout=60, allow_redirects=True, headers=UA); out[name] = [r.status_code, int(r.headers.get("content-length", 0)), url.split("/")[-2][:16]]
    return out
see("the 14 model files that openai-whisper 20250625 knows: HTTP status of a HEAD request, size in bytes, first 16 characters of the SHA-256 in the URL path (the chapter's Table 24-1 gives 74MB, 142MB, 472MB, 1.5GB and 3GB for tiny, base, small, medium and large-v3)", models)
def readme_lines():
    t = get("https://raw.githubusercontent.com/openai/whisper/main/README.md").text
    return {"table lines": [l.strip() for l in t.splitlines() if re.match(r"\|\s*(tiny|base|small|medium|large|turbo)", l)], "lines about the default model": [l.strip() for l in t.splitlines() if re.search(r"default", l, re.I)][:6], "lines about ffmpeg": [l.strip() for l in t.splitlines() if "ffmpeg" in l][:4], "lines about Python and PyTorch versions": [l.strip() for l in t.splitlines() if re.search(r"Python 3\.\d|PyTorch 1\.|python 3\.", l)][:4]}
see("Whisper README: the model table (size, required VRAM, relative speed), the lines about the default model, ffmpeg and the Python versions", readme_lines)
def pyp_whisper():
    j = get("https://pypi.org/pypi/whisper/json").json(); i = j["info"]
    return {"version": i["version"], "summary": i["summary"], "home_page": i.get("home_page") or (i.get("project_urls") or {}), "author": i["author"], "requires_dist": i["requires_dist"]}
see("PyPI: the project called whisper, which the chapter says 'refers to something else'", pyp_whisper)
VIDEO = '''
import yt_dlp, json, sys
o = {'quiet': True, 'no_warnings': True, 'skip_download': True}
with yt_dlp.YoutubeDL(o) as ydl:
    info = ydl.extract_info('https://www.youtube.com/watch?v=kSrnLbioN6w')
    j = ydl.sanitize_info(info)
    print(json.dumps({'title': j['title'], 'keys': list(j.keys()), 'duration': j['duration'], 'formats': len(j['formats']), 'upload_date': j.get('upload_date'), 'channel': j.get('channel'), 'has sanitize': hasattr(ydl, 'sanitize'), 'json size': len(json.dumps(j)), 'id': j['id'], 'extractor': j['extractor'], 'yt_dlp': yt_dlp.version.__version__}))
'''
def video():
    r = subprocess.run([LATEST, "-W", "ignore", "-c", VIDEO], capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL)
    if r.returncode: return "failed: " + (r.stderr.strip().splitlines() or [""])[-1][:300]
    d = json.loads(r.stdout.strip().splitlines()[-1])
    book = ['id', 'title', 'formats', 'thumbnails', 'thumbnail', 'description', 'channel_id', 'channel_url', 'duration', 'view_count', 'average_rating', 'age_limit', 'webpage_url']
    d["the keys the chapter prints, in the order it prints them, that the metadata has"] = [k in d["keys"] for k in book]
    d["the keys the chapter prints are the first keys of the dictionary, in the same order"] = d["keys"][:len(book)] == book
    d["number of keys"] = len(d["keys"]); d["keys"] = d["keys"][:40]
    return d
see("yt-dlp asked for the metadata of the video the chapter names (skip_download, no video downloaded): the title the chapter prints, the keys against the keys the chapter prints, whether ydl.sanitize exists", video)
def terms():
    t = visible(get("https://www.youtube.com/t/terms"))
    i = t.find("Permissions and Restrictions"); seg = t[i:i + 6000]
    m = re.search(r"You (are )?(may|not allowed)[^.]{0,80}(access|download)[^.]{0,260}\.", seg)
    return {"found 'Permissions and Restrictions'": i >= 0, "sentences with 'download'": [s.strip()[:330] for s in re.split(r"(?<=[.;])\s", seg) if "download" in s.lower()][:3]}
see("YouTube Terms of Service: the sentences with the word download in the section Permissions and Restrictions (the reason this study asks YouTube for metadata only and does not download a video from it)", terms)
# 1. the tools and the engine experiment on the machine
def run(cmd, env=None, timeout=300):
    e = dict(os.environ); e.update(env or {})
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, env=e, timeout=timeout, stdin=subprocess.DEVNULL); return (r.stdout + r.stderr).strip().splitlines()[0:1]
    except Exception as ex: return ["raised %s" % type(ex).__name__]
def tools():
    out = {}
    for t in ("ffmpeg", "ffprobe", "espeak", "espeak-ng", "aplay", "sox", "uv", "xvfb-run"): out[t] = shutil.which(t)
    for p in ("ffmpeg", "espeak", "espeak-ng", "libespeak1", "libespeak-ng1", "alsa-utils", "sox"): out["package " + p] = run(["dpkg-query", "-W", "-f", "${Package} ${Version}", p])
    out["ffmpeg -version"] = run(["ffmpeg", "-version"]); out["espeak --version"] = run(["espeak", "--version"]); out["espeak-ng --version"] = run(["espeak-ng", "--version"]); out["aplay -l"] = run(["aplay", "-l"]); out["/dev/snd present"] = os.path.exists("/dev/snd")
    out["espeak-ng voices listed"] = len(subprocess.run(["espeak-ng", "--voices"], capture_output=True, text=True).stdout.strip().splitlines()) - 1
    out["espeak voices listed"] = len(subprocess.run(["espeak", "--voices"], capture_output=True, text=True).stdout.strip().splitlines()) - 1
    out["python of LATEST"] = run([LATEST, "--version"]); out["python of PINS"] = run([PINS, "--version"]); out["cpu count"] = os.cpu_count()
    out["ffmpeg encoders aac, libmp3lame"] = [bool(re.search(r"\b%s\b" % e, subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True).stdout)) for e in ("aac", "libmp3lame")]
    return out
see("tools of the machine the research programs use: where they are and which versions", tools)
ENGINE_PROG = r'''
import json, os, sys, tempfile, wave, time
res = {}
try:
    import pyttsx3
    e = pyttsx3.init()
    res['init'] = 'ok'; res['driver class'] = type(e.proxy._driver).__name__
    import pyttsx3.drivers._espeak as es
    res['library file loaded'] = getattr(es.dll, '_name', None)
    res['voices'] = len(e.getProperty('voices'))
    d = tempfile.mkdtemp(); f = os.path.join(d, 'hello.wav'); e.save_to_file('Hello. How are you doing?', f); e.runAndWait()
    t0 = time.time()
    while not os.path.exists(f) and time.time() - t0 < 10: time.sleep(0.05)
    w = wave.open(f); res['wav'] = [w.getnchannels(), w.getsampwidth(), w.getframerate(), round(w.getnframes() / w.getframerate(), 2)]
    v = e.getProperty('voices')
    res['first voice'] = [v[0].name, v[0].gender, v[0].age, v[0].languages, v[0].id]
except BaseException as ex:
    res['init'] = type(ex).__name__ + ': ' + str(ex).splitlines()[0][:160] if str(ex) else type(ex).__name__
print(json.dumps(res))
'''
def engines():
    out = {}
    def trial():
        r = subprocess.run([LATEST, "-W", "ignore", "-c", ENGINE_PROG], capture_output=True, text=True, timeout=120, stdin=subprocess.DEVNULL)
        lines = [l for l in r.stdout.splitlines() if l.startswith("{")]
        return json.loads(lines[-1]) if lines else {"no result": (r.stderr.strip().splitlines() or ["no output"])[-1][:200]}
    def apt(*a):
        r = subprocess.run(["apt-get", "-y", "-qq"] + list(a), capture_output=True, text=True, timeout=900, stdin=subprocess.DEVNULL, env=dict(os.environ, DEBIAN_FRONTEND="noninteractive")); return r.returncode
    states = [("none (espeak and espeak-ng removed)", ["remove", "espeak", "libespeak1", "espeak-data", "espeak-ng", "libespeak-ng1", "espeak-ng-data"], None),
              ("espeak only, as the chapter says (sudo apt install espeak)", ["install", "espeak"], None),
              ("espeak-ng only", ["remove", "espeak", "libespeak1", "espeak-data"], None),
              ("both", ["install", "espeak-ng", "espeak"], None)]
    try:
        apt("remove", "espeak", "libespeak1", "espeak-data", "espeak-ng", "libespeak-ng1", "espeak-ng-data")
        out["none (espeak and espeak-ng removed)"] = trial()
        apt("install", "espeak"); out["espeak only, as the chapter says (sudo apt install espeak)"] = trial()
        apt("remove", "espeak", "libespeak1", "espeak-data"); apt("install", "espeak-ng", "libespeak-ng1"); out["espeak-ng only"] = trial()
    finally:
        apt("install", "espeak-ng", "espeak"); out["restored state: both"] = trial()
        out["packages after the experiment"] = [run(["dpkg-query", "-W", "-f", "${Package} ${Version}", p])[0] for p in ("espeak", "espeak-ng", "libespeak1", "libespeak-ng1")]
    return out
see("the engine experiment: pyttsx3 2.99 started (init, the library it loaded, voices, a saved WAV) with no eSpeak package, with the package the chapter names, with espeak-ng, with both (apt remove and install; the final state is restored)", engines)
def no_aplay():
    code = "import pyttsx3, os; e = pyttsx3.init(); e.say('Hello'); e.runAndWait(); print('returned without an exception')"
    env = dict(os.environ); d = tempfile.mkdtemp()
    for tool in ("aplay",):  # a PATH that holds no aplay: the system folders without it are rebuilt as a folder of links
        for p in ("python3",): pass
    bindir = tempfile.mkdtemp()
    for n in os.listdir("/usr/bin"):
        if n != "aplay":
            try: os.symlink("/usr/bin/" + n, os.path.join(bindir, n))
            except OSError: pass
    env["PATH"] = os.path.dirname(LATEST) + ":" + bindir
    r = subprocess.run([LATEST, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=120, stdin=subprocess.DEVNULL)
    r2 = subprocess.run([LATEST, "-W", "ignore", "-c", code], capture_output=True, text=True, timeout=120, stdin=subprocess.DEVNULL)
    return {"without aplay on the PATH: return code, last stdout line, stderr lines mentioning aplay or not found": [r.returncode, r.stdout.strip().splitlines()[-1:], [l[:120] for l in r.stderr.splitlines() if "aplay" in l or "not found" in l][:3]],
            "with aplay (no sound card): return code, last stdout line, stderr lines mentioning aplay": [r2.returncode, r2.stdout.strip().splitlines()[-1:], [l[:120] for l in r2.stderr.splitlines() if "aplay" in l][:3]]}
see("say() and runAndWait() in a PATH without aplay and with aplay on a machine with no sound card: does the program notice? (the espeak driver of pyttsx3 2.99 plays the WAV with the shell command aplay)", no_aplay)
see("the photograph: the pages of Wikipedia answered 429 for the Voder on 2026-10-14 and Wikimedia Commons answered 429 on 2026-10-13; no picture is fetched and no photograph is used", lambda: {"photograph used": False})
if ONLY: OUT = os.path.join(os.environ.get("CH24_ONLY_OUT", tempfile.gettempdir()), "live_partial.json")
json.dump({"_version": __version__, "observed": datetime.date.today().isoformat(), "with": "requests %s, beautifulsoup4 %s, Python %s" % (requests.__version__, bs4.__version__, sys.version.split()[0]),
           "_note": "Single requests made on the day named, through the build machine's proxy, to the public pages and files the chapter names; the PyPI JSON of ten packages; one HEAD request to each Whisper model file; the metadata (no video) of the video the chapter names; and experiments on the build machine (apt packages espeak and espeak-ng removed and installed in turn and restored, a PATH without aplay). Nothing was posted anywhere. Not executed: the download of a video from YouTube, an audio device, a GPU, Windows, macOS. github.com pages answer 403 through the proxy, so only raw.githubusercontent.com files were used.",
           "items": obs}, open(OUT, "w"), indent=1, ensure_ascii=False)
print(len(obs), "observations ->", OUT)
