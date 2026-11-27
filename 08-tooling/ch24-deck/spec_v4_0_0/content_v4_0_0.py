"""Chapter 24 deck content, version 4.0.0 (SEN0414, Lineage14): the words of the deck "Make Python Talk". Parts, plan, concept slides in plain words (no everyday comparison), stories,
the native table of quiet surprises that the run itself measured, take-aways, practice and resources.
Slide numbers of the plan: 1 title, 2 route, 3 questions, 4-9 part 1, 10-15 part 2, 16-22 part 3, 23-31 part 4, 32-38 part 5, 39 compare, 40 practice, 41 summary, 42 resources.
The notes are in notes_v4_0_0.py."""
__version__ = "4.0.0"
import os

PARTS = {
    1: ("Part 1: The tools and the speech engine", "pyttsx3 asks the speech system to speak; say() queues, runAndWait() speaks", [
        ("versions", "Three packages and two programs, each with a printed version"),
        ("say", "say() queues text; the events come while runAndWait() runs"),
        ("twice", "A second runAndWait() in one process does not come back")]),
    2: ("Part 2: Voices, rate, volume and WAV files", "Properties change the voice, the speed and the loudness; the speech can go into a WAV file", [
        ("voices", "getProperty('voices') lists the voices; setProperty('voice', id) chooses one"),
        ("rate", "A higher rate makes the audio shorter; the volume sets the peak"),
        ("wav", "save_to_file() writes a WAV file when runAndWait() runs")]),
    3: ("Part 3: Whisper: speech to text", "Whisper models turn audio into text; ffmpeg reads the audio and a language is detected", [
        ("models", "Three models differ in parameters and file size; no graphics card here"),
        ("transcribe", "Bigger models make fewer wrong words on the same sentence"),
        ("language", "The language is detected; a model that is too small can be wrong")]),
    4: ("Part 4: Subtitle files and downloaded audio", "A writer turns segments into SRT, VTT or TSV; yt-dlp reads and downloads from a web page", [
        ("writers", "Three formats, one result; the times are written differently"),
        ("options", "Word times let a writer cut lines at a width"),
        ("download", "extract_info() reads the page; download() fetches and converts the audio")]),
    5: ("Part 5: The practice programs", "Guess the Number with a voice, 99 Bottles of Beer and the YouTube Transcriber", [
        ("guess", "Every message is printed and spoken; the speech goes into WAV files"),
        ("song", "99 verses become 11 minutes and 48 seconds of audio"),
        ("transcriber", "One function: download, transcribe, write the subtitle files")]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("analogy", "A1b"), ("story", "kempelen"), ("code", "pins"), ("code", "say"),
        ("divider", 2), ("analogy", "A2"), ("story", "voder"), ("code", "voices"), ("code", "rate"), ("code", "wav"),
        ("divider", 3), ("analogy", "A3"), ("story", "reddy"), ("code", "models"), ("code", "trans"), ("code", "ffmpeg"), ("code", "lang"),
        ("divider", 4), ("analogy", "A4"), ("analogy", "A4b"), ("analogy", "A4c"), ("story", "captions"), ("code", "cues"), ("code", "opt"), ("code", "ytm"), ("code", "ytd"),
        ("divider", 5), ("analogy", "A5"), ("story", "daisy"), ("code", "guess"), ("code", "song"), ("story", "gettysburg"), ("code", "tube"),
        ("compare", "quiet"), ("practice",), ("summary",), ("resources",)]

ROUTE_RUNS = {1: "versions, say and runAndWait", 2: "voices, rate and volume, WAV files", 3: "models, transcribe, ffmpeg, languages", 4: "subtitle writers, word times, metadata, download",
              5: "Guess the Number, 99 Bottles, the transcriber"}
ROUTE_TAIL = ("Summary and links", "what to remember, where next")

QUESTIONS = [
    ("1", "How does a program speak, and where does the sound go when the machine has no sound card?", "Parts 1 and 2 answer it; the summary repeats it on slide %d.", "summary"),
    ("2", "How does a program turn audio into text and subtitles, and which calls wait for ever or fail quietly?", "Part 3 and part 4 answer the first half; the table on slide %d and the questions on slide %d the second.", [("compare", "quiet"), ("practice",)]),
]
QUESTIONS_TAKEAWAY = "Every example runs on the chapter page; read its printed result first."

BOX_LABEL = "IN SHORT"
TABLE_HEAD = "What it is and does"
CONCEPTS_TAIL = "each explained in plain words"
ANALOGIES = [
    ("A1", "The tools: modules and programs", "Three Python packages do the work, and two programs outside Python, eSpeak NG and ffmpeg, help them.", [
        ("Make Python Talk", "The title of the chapter: a program speaks, writes what it hears, and makes subtitles."),
        ("pyttsx3", "The package that makes text into speech through the speech system of the machine."),
        ("whisper", "The module of the openai-whisper package that turns audio into text."),
        ("yt_dlp", "The module of the yt-dlp package that reads and downloads audio and video from web pages."),
        ("json", "The standard module that writes a dictionary as JSON text and reads it back."),
        ("pathlib", "The standard module for file and folder paths; it can check a downloaded file."),
        ("Whisper", "The speech recognition system of OpenAI; its models are files of numbers."),
        ("yt-dlp", "The program and package for downloading from video sites, a fork of youtube-dl."),
        ("eSpeak", "A small speech synthesizer that pyttsx3 uses on Linux."),
        ("FFmpeg", "A program that reads and converts audio and video; Whisper and yt-dlp call it."),
    ]),
    ("A1b", "Text to speech: the engine and its calls", "init() makes the engine, say() queues text and runAndWait() speaks it.", [
        ("Text-to-Speech Engine", "A program that makes spoken audio from text."),
        ("Generating Speech", "Three steps: make the engine, queue the text, run the queue."),
        ("pyttsx3.init()", "Returns the engine of the platform's speech system."),
        ("engine.say()", "Puts a text into the queue; it speaks nothing yet and returns None."),
        ("engine.runAndWait()", "Speaks everything in the queue and returns when the queue is empty."),
        ("hello_tts.py", "The book's first program: init(), say() and runAndWait()."),
        ("SAPI5", "The speech system of Windows, which pyttsx3 uses there."),
        ("NSSpeechSynthesizer", "The speech system of macOS, which pyttsx3 uses there."),
    ]),
    ("A2", "Voices, properties and WAV files", "getProperty() and setProperty() read and change the voice, the rate and the volume; save_to_file() writes the speech as a WAV file.", [
        ("engine.getProperty()", "Reads a property: 'voices', 'voice', 'rate' or 'volume'."),
        ("engine.setProperty()", "Changes a property for the speech that follows."),
        ("engine.setProperty('rate', 300)", "Sets the speed; the default is 200 words a minute, and a higher number is faster."),
        ("engine.setProperty('volume', 0.5)", "Sets the loudness between 0.0 and 1.0."),
        ("engine.setProperty('voice', voices[1].id)", "Chooses a voice from the list by its id."),
        ("Saving Speech Audio to WAV Files", "The speech can go into a file instead of the speaker."),
        ("engine.save_to_file()", "Queues a text and a file name; the file is written when runAndWait() runs."),
        ("hello.wav", "The book's file name for the saved speech."),
        ("WAV", "A file format for sound that holds the samples and a header with channels, size and rate."),
    ]),
    ("A3", "Whisper: models and transcription", "load_model() loads a model, transcribe() returns the text and its segments, and the models differ in size and speed.", [
        ("Speech Recognition", "Making text from spoken audio."),
        ("Table 24-1: properties of Whisper speech recognition models", "The models tiny, base, small, medium and large with their sizes and speeds."),
        ("whisper.load_model()", "Loads a model by name; the file is downloaded on the first use."),
        ("model.transcribe()", "Returns a dictionary with the text, the language and the segments."),
    ]),
    ("A4", "Subtitle files: SRT, VTT and TSV", "A writer from whisper.utils turns the segments of a result into SRT, VTT or TSV files.", [
        ("Creating Subtitle Files", "A subtitle file holds pieces of text with a start time and an end time."),
        ("whisper.utils.get_writer()", "Returns a function that writes a result in a format: srt, vtt, tsv, txt or json."),
        ("audio.srt", "The file the SRT writer makes for the name audio."),
        ("audio.vtt", "The file the VTT writer makes for the name audio."),
        ("audio.tsv", "The file the TSV writer makes; its times are milliseconds."),
        ("SRT (SubRip Subtitle)", "A text format with numbered cues; the times use a comma before the milliseconds."),
        ("VTT (Web Video Text Tracks)", "The web format for subtitles; it starts with WEBVTT and uses a point."),
    ]),
    ("A4b", "Downloading from a web page", "yt-dlp reads a page with extract_info() and fetches the audio with download().", [
        ("Downloading Videos from Websites", "yt-dlp finds the media on a page and downloads it."),
        ("yt_dlp.YoutubeDL()", "Makes the downloader object; a dictionary of options is its argument."),
        ("ydl.extract_info()", "Reads the page and returns its data; download=False fetches nothing."),
        ("ydl.sanitize_info()", "Turns the data into plain types so that it can be written as JSON."),
        ("json.dumps()", "Writes a dictionary as JSON text."),
        ("ydl.download()", "Downloads the files of a list of addresses."),
        ("metadata.json", "The book's file name for the saved page data."),
        ("downloaded_content.m4a", "The book's file name for the downloaded audio."),
    ]),
    ("A4c", "Downloading from a page: the options", "A dictionary of options says whether to download, where to save, which format and what to convert.", [
        ("'skip_download': True", "Read the page only; do not fetch the media."),
        ("'outtmpl': 'downloaded_content.%(ext)s'", "The file name pattern; %(ext)s becomes the real extension."),
        ("'format': 'm4a/bestaudio/best'", "Prefer m4a, then the best audio, then the best of all."),
        ("'postprocessors': FFmpegExtractAudio", "Calls ffmpeg after the download to keep only the audio."),
        ("'quiet': True", "Prints nothing while it works."),
    ]),
    ("A5", "The practice programs and the end of the chapter", "Three programs bring the parts together; the summary and the questions close the chapter.", [
        ("Practice Programs", "Three programs that use the calls of the chapter."),
        ("Adding Voice to Guess the Number", "The game from an earlier chapter, with every message spoken as well as printed."),
        ("Singing 99 Bottles of Beer", "A program that makes the verses of the song and speaks them."),
        ("YouTube Transcriber", "A program that downloads audio from addresses and writes subtitle files."),
        ("Summary", "The chapter in a few sentences."),
        ("Practice Questions", "Questions to check the chapter."),
    ]),
]

STORIES = {
    "kempelen": dict(
        title="Story: Kempelen published his speech research and a speaking machine in 1789", img="image_kempelen.jpg",
        prose=["Johann Wolfgang von Kempelen (1734-1804) was a Hungarian writer, architect, engineer and inventor, known for the chess playing hoax The Turk and for a speaking machine that a hand played.",
               "In 1789 he published a book with nearly twenty years of speech research, and an early version of the machine can still be seen in the Deutsches Museum in Munich.",
               "The picture shows a reconstruction. pyttsx3 asks the speech system of the machine to do by program what that device did by hand."],
        linktext="Wolfgang von Kempelen (Wikipedia)", link="https://en.wikipedia.org/wiki/Wolfgang_von_Kempelen"),
    "voder": dict(
        title="Story: The Voder spoke at the 1939 New York World's Fair", img="image_voder.jpg",
        prose=["Homer Dudley invented the Voder at Bell Telephone Laboratories in 1937 and 1938, and it was shown at the 1939 New York World's Fair and in San Francisco.",
               "An operator played it with a wrist bar, fifteen keys and a foot pedal; Helen Harper trained twenty operators and was noted for her skill.",
               "The picture shows the Voder with the crowd. The voice of pyttsx3 has a rate, a volume and a voice, which are the settings that the operator moved by hand."],
        linktext="Voder (Wikipedia)", link="https://en.wikipedia.org/wiki/Voder"),
    "reddy": dict(
        title="Story: Raj Reddy's group made computers understand connected speech", img="image_reddy.jpg",
        prose=["Raj Reddy, born on 13 June 1937, worked at Stanford and then at Carnegie Mellon University from 1969 on speech, language, vision and robotics.",
               "He and his colleagues made demonstrations such as voice control of a robot and large-vocabulary connected speech recognition.",
               "In 1994 he and Edward Feigenbaum received the ACM Turing Award. model.transcribe() in this part is a result of that line of work."],
        linktext="Raj Reddy (Wikipedia)", link="https://en.wikipedia.org/wiki/Raj_Reddy"),
    "captions": dict(
        title="Story: Closed captions were first shown in December 1971", img="image_captions.jpg",
        prose=["Closed captioning was first demonstrated in the United States in December 1971 at the First National Conference on Television for the Hearing Impaired in Knoxville, Tennessee.",
               "On 15 February 1972 ABC and the National Bureau of Standards showed captions inside a normal broadcast of The Mod Squad at Gallaudet College.",
               "Regular open-captioned broadcasts began on PBS with The French Chef in 1972. The SRT and VTT files of this part carry the same cues, with times."],
        linktext="Closed captioning (Wikipedia)", link="https://en.wikipedia.org/wiki/Closed_captioning"),
    "daisy": dict(
        title="Story: A computer sang Daisy Bell in 1961", img="image_ibm7090.jpg",
        prose=["Harry Dacre wrote the song Daisy Bell in 1892.",
               "It is the earliest song sung with computer speech synthesis, by an IBM 7090 in 1961.",
               "The picture shows that machine. The 99 verses of this part are spoken by a synthesizer too, and the program writes the sound into a WAV file."],
        linktext="Daisy Bell (Wikipedia)", link="https://en.wikipedia.org/wiki/Daisy_Bell"),
    "gettysburg": dict(
        title="Story: Lincoln spoke at Gettysburg on 19 November 1863", img="image_gettysburg.jpg",
        prose=["Abraham Lincoln spoke on the afternoon of 19 November 1863 at the dedication of the Soldiers' National Cemetery, four and a half months after the battle.",
               "Five manuscript copies are known, and the Bliss copy is the standard text of the address.",
               "The picture shows a copy. The transcriber of this part reads a public-domain recording of the address that the Internet Archive hosts; it stands in for a video site."],
        linktext="Gettysburg Address (Wikipedia)", link="https://en.wikipedia.org/wiki/Gettysburg_Address"),
}


def _measure():
    """measure the quiet surprises with the real packages, with the same helpers as the examples"""
    import lab24_v1_0_0 as L
    here = os.getcwd()
    L.begin()
    import pyttsx3
    from whisper.utils import get_writer
    init = "import pyttsx3; e = pyttsx3.init(); "
    twice = L.waits(init + "e.runAndWait(); e.runAndWait()")
    engine = pyttsx3.init()
    engine.save_to_file("Hello.", "hello.mp3")
    engine.runAndWait()
    L.wait_file("hello.mp3")
    head = open("hello.mp3", "rb").read(12)
    full = L.measure("volume", 1.0, L.FOX)[2]
    loud = L.measure("volume", 5, L.FOX)[2]
    import yt_dlp
    ydl = yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "noprogress": True, "skip_download": True})
    got = ydl.download("https://archive.org/details/gettysburg_shurtagal_librivox")
    os.chdir(here)
    return twice, head, full, loud, got


_TWICE, _HEAD, _FULL, _LOUD, _GOT = _measure()
COMPARES = {
    "quiet": dict(
        title="Four surprises, measured by the run", sub="Only the first call is visibly wrong; the others raise nothing at all",
        colw=[2.4, 1.3, 3.3, 2.7], rowh=0.5, fs=11,
        rows=[["Call", "An error?", "What the run saw", "What to do"],
              ["a second runAndWait()", "none", _TWICE, "call it once for each queue"],
              ["save_to_file('hello.mp3')", "none", "the file begins with %s and %s" % (_HEAD[:4].decode(), _HEAD[8:].decode()), "use the .wav name for a WAV file"],
              ["setProperty('volume', 5)", "none", "peak %d at 5 and %d at 1.0" % (_LOUD, _FULL), "keep the volume from 0.0 to 1.0"],
              ["download() with one string", "none", "returned %r; the book passes a list" % _GOT, "pass a list of addresses"]],
        takeaway="Nothing is raised: check the file, the peak and the return value yourself."),
}

TAKEAWAY = {
    "pins": "Print the versions; two programs outside Python are needed.",
    "say": "say() queues; runAndWait() speaks; twice does not come back.",
    "voices": "A voice is chosen by its id; the speech goes into a file.",
    "rate": "A higher rate makes shorter audio; the volume sets the peak.",
    "wav": "Nothing is written before runAndWait(); the name does not set the format.",
    "models": "Bigger models have more parameters; no graphics card here.",
    "trans": "Bigger models make fewer wrong words on the same sentence.",
    "ffmpeg": "load_audio() needs ffmpeg on the PATH.",
    "lang": "The language is detected; the tiny model was wrong more often.",
    "cues": "One result, three formats; SRT has a comma, VTT a point.",
    "opt": "Word times let the writer cut lines at a width.",
    "ytm": "extract_info() reads the page; sanitize_info() makes it JSON-safe.",
    "ytd": "The options name the file, the format and the conversion.",
    "guess": "Every message is printed and saved as a WAV file.",
    "song": "99 verses make 11 minutes and 48 seconds of audio.",
    "tube": "One function: download, transcribe, write the subtitles.",
}

SUMMARY_ANALOGY = "Four claims: queue then run, files not sound, bigger models are better, check the quiet calls."
SUMMARY_POINTS = [
    "say() queues text and runAndWait() speaks it; save_to_file() writes a WAV file when it runs.",
    "Rate, volume and voice are properties; the run measured their effect in the audio itself.",
    "load_model() and transcribe() turn audio into text; larger models make fewer wrong words.",
    "A writer makes SRT, VTT or TSV; yt-dlp reads and downloads audio, and several calls fail quietly.",
]
SUMMARY_TAKEAWAY = "Two questions of slide 3: how a program speaks, how it writes what it hears."

PRACTICE_SUB = "Use the slide of the part named in each question"
PRACTICE_ANALOGY = "Each practice question has a short answer; run the code on the chapter page to check it."
PRACTICE = [
    "What does say() do before runAndWait() runs, and what happens at a second runAndWait()? Use part 1.",
    "How does the audio change with the rate, and what does a volume above 1.0 do? Use part 2.",
    "Which of tiny, base and small made the fewest wrong words, and what does load_audio() need? Use part 3.",
    "How do SRT and VTT write the same time, and what does download() return for a list? Use part 4.",
    "What does the game make of each message it speaks, and what files does the transcriber write? Use part 5.",
]
PRACTICE_TAKEAWAY = "Run the examples on the chapter page to check each answer."

RESOURCES_SUB = "The chapter, the documentation, and the pages behind the stories"
RESOURCES_TAKEAWAY = "13 of 16 pages opened on 2026-11-27; see the notes."
RESOURCES_ROWS = 8
RESOURCES = [
    ("Book: Automate the Boring Stuff, 3rd edition, chapter 24", "https://automatetheboringstuff.com/3e/chapter24.html", "automatetheboringstuff.com"),
    ("pyttsx3 documentation", "https://pyttsx3.readthedocs.io/en/latest/", "pyttsx3.readthedocs.io"),
    ("pyttsx3 on PyPI", "https://pypi.org/pypi/pyttsx3/json", "pypi.org"),
    ("Whisper on GitHub", "https://github.com/openai/whisper", "github.com"),
    ("openai-whisper on PyPI", "https://pypi.org/pypi/openai-whisper/json", "pypi.org"),
    ("yt-dlp on GitHub", "https://github.com/yt-dlp/yt-dlp", "github.com"),
    ("yt-dlp on PyPI", "https://pypi.org/pypi/yt-dlp/json", "pypi.org"),
    ("FFmpeg", "https://ffmpeg.org/", "ffmpeg.org"),
    ("eSpeak NG on GitHub", "https://github.com/espeak-ng/espeak-ng", "github.com"),
    ("The Gettysburg Address reading (Internet Archive)", "https://archive.org/details/gettysburg_shurtagal_librivox", "archive.org"),
    ("Wolfgang von Kempelen (Wikipedia)", "https://en.wikipedia.org/wiki/Wolfgang_von_Kempelen", "en.wikipedia.org"),
    ("Voder (Wikipedia)", "https://en.wikipedia.org/wiki/Voder", "en.wikipedia.org"),
    ("Raj Reddy (Wikipedia)", "https://en.wikipedia.org/wiki/Raj_Reddy", "en.wikipedia.org"),
    ("Closed captioning (Wikipedia)", "https://en.wikipedia.org/wiki/Closed_captioning", "en.wikipedia.org"),
    ("Daisy Bell (Wikipedia)", "https://en.wikipedia.org/wiki/Daisy_Bell", "en.wikipedia.org"),
    ("Gettysburg Address (Wikipedia)", "https://en.wikipedia.org/wiki/Gettysburg_Address", "en.wikipedia.org"),
]
