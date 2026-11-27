"""Chapter 24 deck examples, version 1.0.0 (SEN0414, Lineage14): the 16 code examples of the chapter 24 lecture deck (Make Python Talk), in slide order = page-tab order.
Every example runs the real pyttsx3, openai-whisper and yt-dlp of the chapter's interpreter (Python 3.14) with eSpeak NG and ffmpeg on the PATH. NOTHING IS HEARD: this machine has no sound card, so pyttsx3 writes WAV
files and no program plays a sound; no program uses a microphone, a GPU, Windows, macOS or a cloud key. The examples that need audio from a public site use a public-domain LibriVox reading hosted by the Internet
Archive (archive.org), which STANDS IN FOR YouTube: nothing is downloaded from YouTube. Windows (SAPI5) and macOS (NSSpeechSynthesizer) were not run.
The hidden `setup` lines (lab24) only start an empty working folder; `groups` are the code boxes of a slide with the explanation beside each; every box parses on its own and uses no lambda."""
__version__ = "1.0.0"

LAB = ["from lab24_v1_0_0 import *", "begin()"]

EXAMPLES = [
    # ------------------------------------------------------------ part 1: the tools and the engine
    dict(id="pins", name="The packages and the tools", title="Which versions run, and which tools are there?", part=1, visual="pins",
         setup=LAB, concepts=["pyttsx3", "whisper", "yt_dlp", "FFmpeg", "eSpeak"],
         groups=[
             (["import platform, importlib.metadata as md", "print(platform.python_version())",
               "names = ('pyttsx3', 'openai-whisper', 'yt-dlp', 'numpy')", "print([md.version(n) for n in names])"],
              "The versions are printed, not assumed: each of the three packages changes often."),
             (["import shutil, os", "print(shutil.which('ffmpeg') is not None)", "print(shutil.which('espeak-ng') is not None)",
               "print(os.path.exists('/dev/snd'))"],
              "ffmpeg and eSpeak are programs; this machine has no sound card (/dev/snd)."),
         ]),
    dict(id="say", name="Saying a sentence", title="say() queues; runAndWait() speaks", part=1, visual="say", layout="left",
         setup=LAB, concepts=["Text-to-Speech Engine", "pyttsx3.init()", "engine.say()", "engine.runAndWait()", "Generating Speech", "hello_tts.py"],
         groups=[
             (["import pyttsx3", "events = []", "def began(**kw): events.append('started')", "def ended(**kw): events.append('finished')",
               "engine = pyttsx3.init()", "engine.connect('started-utterance', began)", "engine.connect('finished-utterance', ended)",
               "queued = engine.say('Hello. How are you doing?')", "print('say() returned', queued, '| events', len(events))",
               "engine.runAndWait()", "print('after runAndWait:', events)"],
              "say() only queues the text and returns None; the events come while runAndWait() runs."),
             (["init = 'import pyttsx3; e = pyttsx3.init(); '", "once = init + 'e.runAndWait()'",
               "twice = init + 'e.runAndWait(); e.runAndWait()'", "print('once :', waits(once))", "print('twice:', waits(twice))"],
              "A second runAndWait() in the same process can wait for ever; a child process shows it."),
         ]),
    # ------------------------------------------------------------ part 2: voice, rate, volume and WAV files
    dict(id="voices", name="The voices of the engine", title="Voices: list, choose, save", part=2, visual="voices",
         setup=LAB, concepts=["engine.getProperty()", "engine.setProperty()", "engine.setProperty('voice', voices[1].id)", "SAPI5", "NSSpeechSynthesizer"],
         groups=[
             (["import pyttsx3", "engine = pyttsx3.init()", "voices = engine.getProperty('voices')", "first = voices[0]",
               "print(len(voices), first.name, first.gender, first.age)", "print(first.languages)", "print(engine.getProperty('voice'))"],
              "getProperty('voices') lists the voices of the platform's speech system; here eSpeak NG."),
             (["engine.setProperty('voice', voices[1].id)", "engine.save_to_file('Hello. How are you doing?', 'hello.wav')",
               "engine.runAndWait()", "print(voices[1].name, wavinfo('hello.wav')['seconds'], 's')"],
              "A voice is chosen by its id; the speech goes into a file because no sound is played here."),
         ]),
    dict(id="rate", name="Rate and volume", title="Rate and volume, measured in audio", part=2, visual="rate",
         setup=LAB, concepts=["engine.setProperty('rate', 300)", "engine.setProperty('volume', 0.5)"],
         groups=[
             (["for rate in (50, 100, 150, 200, 250, 300, 400):", "    audio, seconds, peak = measure('rate', rate, FOX)",
               "    print('%3d -> %.2f s' % (rate, seconds))"],
              "A fresh process says the same sentence at each rate and the seconds of audio are counted."),
             (["for volume in (1.0, 0.5, 0.1, 0.0, 5):", "    print(volume, measure('volume', volume, FOX)[2])",
               "slow, fast = measure('rate', 100, FOX), measure('rate', 300, FOX)", "strips('waves.png', [slow[:2], fast[:2]])"],
              "The peak of the samples follows the volume; the strips draw the sound at rate 100 and 300."),
         ]),
    dict(id="wav", name="Saving speech to a WAV file", title="save_to_file() writes a WAV file", part=2, visual="wav", layout="left",
         setup=LAB, concepts=["Saving Speech Audio to WAV Files", "engine.save_to_file()", "hello.wav", "WAV"],
         groups=[
             (["import pyttsx3, wave", "engine = pyttsx3.init()", "engine.save_to_file('Hello. How are you doing?', 'hello.wav')",
               "print('before runAndWait:', os.path.exists('hello.wav'))", "engine.runAndWait()", "w = wave.open('hello.wav')",
               "print(w.getnchannels(), w.getsampwidth(), w.getframerate())", "print(round(w.getnframes() / w.getframerate(), 2), 's')"],
              "Nothing is written until runAndWait(); then the header tells channels, sample size and rate."),
             (["engine.save_to_file('Hello.', 'hello.mp3')", "engine.runAndWait()", "wait_file('hello.mp3')",
               "head = open('hello.mp3', 'rb').read(12)", "print(head[:4], head[8:])", "a, rate = samples('hello.wav')",
               "strips('hello.png', [(a, len(a) / rate)])"],
              "A name that ends in .mp3 still holds a WAV file; the strip draws the speech."),
         ]),
    # ------------------------------------------------------------ part 3: Whisper
    dict(id="models", name="Whisper models", title="Three models: parameters and file sizes", part=3, visual="models", layout="left",
         setup=LAB, concepts=["Speech Recognition", "whisper.load_model()", "Table 24-1: properties of Whisper speech recognition models", "Whisper"],
         groups=[
             (["import torch, whisper", "print(len(whisper.available_models()), 'models')", "for name in ('tiny', 'base', 'small'):",
               "    model = whisper.load_model(name)", "    count = sum(p.numel() for p in model.parameters()) / 1e6",
               "    size = os.path.getsize(cached(name))", "    print('%-5s %5.1f M, %d bytes' % (name, count, size))"],
              "load_model() loads a model, and downloads its file on the first use."),
             (["print('cuda:', torch.cuda.is_available(), '| on', model.device)", "print(kind(whisper.load_model, 'tiny', device='cuda'))"],
              "Without a graphics card the model runs on the processor; asking for cuda fails."),
         ]),
    dict(id="trans", name="Transcribing speech", title="transcribe(): text, and how wrong it is", part=3, visual="trans", layout="left",
         setup=LAB, concepts=["model.transcribe()"],
         groups=[
             (["import pyttsx3, whisper", "engine = pyttsx3.init()", "say_to(engine, FOX, 'fox.wav')", "for name in ('tiny', 'base', 'small'):",
               "    model = whisper.load_model(name)", "    result = model.transcribe('fox.wav', temperature=0.0)", "    text = result['text']",
               "    print('%-5s %r WER %.1f' % (name, text, wer(FOX, text)))"],
              "The machine's own speech is written back by three models; WER counts the wrong words."),
             (["print('keys:', list(result))", "print('segment:', list(result['segments'][0])[:6])"],
              "The result is a dictionary: the text, the language and a list of segments with times."),
         ]),
    dict(id="ffmpeg", name="Reading audio needs ffmpeg", title="load_audio() calls the ffmpeg program", part=3, visual="ffmpeg", layout="left",
         setup=LAB, concepts=["whisper", "FFmpeg"],
         groups=[
             (["import pyttsx3, whisper", "engine = pyttsx3.init()", "say_to(engine, FOX, 'fox.wav')", "audio = whisper.load_audio('fox.wav')",
               "print(type(audio).__name__, audio.dtype, audio.shape)"],
              "load_audio() returns 16000 numbers for every second of sound."),
             (["path = os.environ['PATH']", "os.environ['PATH'] = '/nonexistent'", "print(trying(whisper.load_audio, 'fox.wav'))",
               "os.environ['PATH'] = path", "a = [int(v * 32767) for v in audio]", "strips('audio16k.png', [(a, len(a) / 16000)])"],
              "Without ffmpeg on the PATH the call fails; with it the strip shows the 16 kHz audio."),
         ]),
    dict(id="lang", name="Languages", title="Whisper hears the language itself", part=3, visual="lang", layout="left",
         setup=LAB, concepts=["model.transcribe()"],
         groups=[
             (["import pyttsx3, whisper", "SAY = {'tr': 'Merhaba, bugün hava çok güzel.',", "       'it': 'Buongiorno, come sta oggi?',",
               "       'en-us': 'Good morning, how are you today?'}", "engine = pyttsx3.init()",
               "ids = {v.languages[0]: v.id for v in engine.getProperty('voices')}", "models = {n: whisper.load_model(n) for n in ('tiny', 'base')}"],
              "Three sentences, each said by an eSpeak voice of its language."),
             (["for code, text in SAY.items():", "    engine.setProperty('voice', ids.get(code, code))", "    say_to(engine, text, code + '.wav')",
               "    row = {}", "    for n, m in models.items():", "        r = m.transcribe(code + '.wav', temperature=0.0)", "        row[n] = r['language']",
               "    print('%-5s heard as %s' % (code, row))", "print(trying(models['tiny'].transcribe, 'tr.wav', language='xx'))"],
              "The detected language is a code; a language that does not exist raises an error."),
         ]),
    dict(id="cues", name="Subtitle files", title="get_writer() writes SRT, VTT and TSV", part=4, visual="cues", layout="left",
         setup=LAB, concepts=["Creating Subtitle Files", "whisper.utils.get_writer()", "audio.srt", "audio.vtt", "audio.tsv", "SRT (SubRip Subtitle)",
                              "VTT (Web Video Text Tracks)"],
         groups=[
             (["from whisper.utils import get_writer", "segs = [{'id': 0, 'start': 0.0, 'end': 5.64, 'text': A},",
               "        {'id': 1, 'start': 5.64, 'end': 14.96, 'text': B}]", "book = {'text': A + B, 'language': 'en', 'segments': segs}",
               "for fmt in ('srt', 'vtt', 'tsv'):", "    get_writer(fmt, '.')(book, 'audio')", "    got = open('audio.' + fmt, encoding='utf-8').read()",
               "    same = got.strip() == CHAPTER[fmt].strip()", "    print(fmt, len(got), 'bytes, same as the book:', same)"],
              "One result is written in three formats; each equals the text of the book."),
             (["print('SRT time:', open('audio.srt').read().splitlines()[1])", "print('VTT time:', open('audio.vtt').read().splitlines()[2])",
               "print('TSV head:', open('audio.tsv').readline().split())", "print('docx writer:', trying(get_writer, 'docx', '.'))",
               "cues_picture(segs)"],
              "SRT uses a comma, VTT a point, and TSV milliseconds; there is no writer for docx."),
         ]),
    dict(id="opt", name="Writer options and word times", title="Word times make shorter cues", part=4, visual="opt", layout="left",
         setup=LAB, concepts=["whisper.utils.get_writer()"],
         groups=[
             (["import whisper", "from whisper.utils import get_writer", "audio = fetch('gettysburg_shurtagal.mp3')",
               "model = whisper.load_model('tiny')", "r = model.transcribe(audio, language='en')", "get_writer('srt', '.')(r, 'plain')",
               "n = len(open('plain.srt').read().strip().split('\\n\\n'))", "times = [t for s in r['segments'] for t in (s['start'], s['end'])]",
               "print('segments', len(r['segments']), '| blocks', n)"],
              "A public-domain reading of the Gettysburg Address stands in for a video."),
             (["w = model.transcribe(audio, language='en', word_timestamps=True)", "print('words in segment 1:', len(w['segments'][0]['words']))",
               "opts = {'max_line_width': 30, 'max_line_count': 2}", "get_writer('srt', '.')(w, 'wide', opts)",
               "blocks = open('wide.srt').read().strip().split('\\n\\n')", "print('max_line_width=30:', len(blocks), 'blocks; the first:')",
               "print(blocks[0])"],
              "With word times the writer can break lines at 30 characters and make more cues."),
         ]),
    dict(id="ytm", name="Metadata without a download", title="extract_info() reads the page, not the file", part=4, visual="ytm", layout="left",
         setup=LAB, concepts=["Downloading Videos from Websites", "yt_dlp.YoutubeDL()", "ydl.extract_info()", "ydl.sanitize_info()", "'skip_download': True",
                              "json.dumps()", "json", "metadata.json", "'quiet': True"],
         groups=[
             (["import yt_dlp", "URL = 'https://archive.org/details/gettysburg_shurtagal_librivox'", "options = {'quiet': True, 'skip_download': True}",
               "ydl = yt_dlp.YoutubeDL(options)", "info = ydl.extract_info(URL, download=False)", "print('title:', info['title'])",
               "print(info['extractor'], '| formats:', len(info['formats']))", "have = [k for k in CHAPTER_KEYS if k in info]",
               "print('of 13 keys of the chapter, here:', len(have))"],
              "The address is a page of the Internet Archive; the same call works for a video page."),
             (["gone = [k for k in CHAPTER_KEYS if k not in info]", "print('missing:', ', '.join(gone))", "clean = ydl.sanitize_info(info)",
               "open('metadata.json', 'w').write(json.dumps(clean))", "kept = json.load(open('metadata.json'))", "print('metadata.json:', len(kept), 'keys')"],
              "sanitize_info() makes the dictionary safe for json.dumps()."),
         ]),
    dict(id="ytd", name="Downloading audio", title="download() fetches the file and converts it", part=4, visual="ytd", layout="left",
         setup=LAB, concepts=["ydl.download()", "'outtmpl': 'downloaded_content.%(ext)s'", "'format': 'm4a/bestaudio/best'", "'postprocessors': FFmpegExtractAudio",
                              "downloaded_content.m4a", "pathlib"],
         groups=[
             (["import yt_dlp", "URL = 'https://archive.org/details/gettysburg_shurtagal_librivox'", "options = {'quiet': True, 'no_warnings': True,", "           'noprogress': True,", "           'outtmpl': 'downloaded_content.%(ext)s',",
               "           'format': 'm4a/bestaudio/best',", "           'postprocessors': [{'key': 'FFmpegExtractAudio',",
               "                               'preferredcodec': 'm4a'}]}",
               "with yt_dlp.YoutubeDL(options) as ydl:", "    print('download() returned', ydl.download([URL]))", "print(sorted(os.listdir('.')))",
               "codec, seconds = probe_audio('downloaded_content.m4a')", "print('codec', codec, '| seconds', seconds)"],
              "The options name the file, the best audio format and the conversion by ffmpeg."),
             (["gone = ['https://archive.org/details/no_such_item_ch24_zz']", "print('a string, not a list:', ydl.download(URL))",
               "print('an address that is nowhere:', kind(ydl.download, gone))"],
              "The book passes a list; this yt-dlp also accepts one string. A wrong address raises an error."),
         ]),
    # ------------------------------------------------------------ part 5: the practice programs
    dict(id="guess", name="Adding voice to Guess the Number", title="A game whose every message is spoken", part=5, visual="guess", layout="left",
         setup=LAB, concepts=["Adding Voice to Guess the Number", "Practice Programs"],
         groups=[
             (["import pyttsx3", "engine = pyttsx3.init()", "names = iter(['g1.wav', 'g2.wav', 'g3.wav', 'g4.wav'])", "def speak(text):",
               "    print(text)", "    engine.save_to_file(text, next(names))", "    engine.runAndWait()"],
              "speak() prints a message and says it; here each message becomes a WAV file."),
             (["def game(guesses, secret):", "    speak('I am thinking of a number between 1 and 20.')", "    for n, g in enumerate(guesses, 1):",
               "        if g == secret: return speak('You won in %d.' % n)", "        word = 'low' if g < secret else 'high'",
               "        speak('%d is too %s.' % (g, word))", "game([5, 18, 12], 12)", "print([wavinfo('g%d.wav' % k)['seconds'] for k in range(1, 5)])"],
              "The game is played with fixed guesses; the seconds of each spoken line are printed."),
         ]),
    dict(id="song", name="Singing 99 Bottles of Beer", title="One text of 99 verses, spoken", part=5, visual="song", layout="left",
         setup=LAB, concepts=["Singing 99 Bottles of Beer"],
         groups=[
             (["import pyttsx3", "def bottles(k):", "    if k == 0: return 'No more bottles'", "    return '1 bottle' if k == 1 else '%d bottles' % k",
               "def verse(n):", "    this, nxt = bottles(n), bottles(n - 1)", "    return (f'{this} of beer on the wall,\\n{this} of beer,\\n'",
               "            'Take one down, pass it around,\\n'", "            f'{nxt} of beer on the wall.')"],
              "Two helpers make the text of a verse."),
             (["engine = pyttsx3.init()", "for n in (3, 99):", "    text = '\\n\\n'.join(verse(k) for k in range(n, 0, -1))",
               "    name = 'song%d.wav' % n", "    say_to(engine, text, name)", "    print(n, 'verses:', wavinfo(name)['seconds'], 'seconds')",
               "a, rate = samples('song3.wav')", "strips('song.png', [(a, len(a) / rate)])"],
              "99 verses are about 12 minutes of audio."),
         ]),
    dict(id="tube", name="The YouTube Transcriber", title="Many addresses to subtitles: one function", part=5, visual="tube", layout="left",
         setup=LAB, concepts=["YouTube Transcriber", "Practice Programs", "yt-dlp", "Whisper"],
         groups=[
             (["import glob, yt_dlp, whisper", "def transcribe_urls(urls, formats=('srt',), model_name='tiny'):",
               "    model = whisper.load_model(model_name)", "    for k, url in enumerate(urls):", "        stem = 'video%d' % k",
               "        with yt_dlp.YoutubeDL(audio_opts(stem)) as ydl:", "            ydl.download([url])", "        audio = glob.glob(stem + '.*')[0]",
               "        r = model.transcribe(audio, language='en', temperature=0)", "        for f in formats: whisper.utils.get_writer(f, '.')(r, stem)",
               "        print(len(r['segments']), 'segments')"],
              "Download the audio, transcribe it, write subtitles."),
             (["URLS = ['https://archive.org/details/gettysburg_shurtagal_librivox',", "        'https://archive.org/details/gettysburg_johng_librivox']",
               "transcribe_urls(URLS, formats=('srt', 'vtt', 'txt'))", "bad = ['https://archive.org/details/no_such_item_ch24_zz']",
               "print('one bad address:', kind(transcribe_urls, bad))"],
              "Two readings, three formats; a bad address raises."),
         ]),
]

BY_ID = {e["id"]: e for e in EXAMPLES}


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def run_text(ex):
    """the hidden setup lines first (they give the example its own folder), then the shown code"""
    return "\n".join(ex.get("setup", []) + code_lines(ex)) + "\n"


def code_text(ex):
    return "\n".join(code_lines(ex)) + "\n"
