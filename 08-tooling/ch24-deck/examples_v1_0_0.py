"""Chapter 24 deck examples: every console session, whole program (or excerpt), chart and table the lecture deck shows. Nothing here
carries a result; examples_run_v1_0_0.py runs it all under the interpreter given (the uv Python 3.14.6 of the chapter 24 research environment
/home/claude/venv314_ch24_latest: pyttsx3 2.99, openai-whisper 20250625, yt-dlp 2026.8.19, torch 2.14.1+cpu, NumPy 2.5.4; eSpeak NG 1.51 and ffmpeg 6.1.1 of Ubuntu 24.04 on the PATH)
and records the results. A console group is one session: its rows run in order in one namespace (the deck check re-runs them per slide, one namespace per slide). Every console row uses
the standard library only, writes no file and reads no clock and no network.

Programs: the programs written for the deck, the 'Cuts' (their lines fit a slide). Every Cut is run TWICE by the runner, which refuses it unless the two transcripts are equal and every
picture it saved is byte-identical, and it is run a third time by the program check. The 15 programs of the chapter's corpus (sen0414_ch24_corpus_base_v1_0_0.py) were run by the research on
14 October 2026 and are recorded in ch24-page/corpus_run_v1_0_0.json; this deck does not run them again, and where a slide uses one of their numbers it says Recorded.
NOTHING IS HEARD: the machine has no sound card (/dev/snd is absent), so pyttsx3 writes WAV files and no program plays a sound; no program uses a microphone, a GPU, Windows, macOS or a cloud
key. The programs that need audio from a public site use the public-domain LibriVox readings hosted by the Internet Archive (archive.org), which STAND IN FOR YouTube: nothing is downloaded from YouTube.
The Gettysburg reading is fetched once into /home/claude/ch24_cache and checked against its SHA-256 before it is used.
KIND says what a program's output depends on, so that honesty_check can require the matching words on the slide that shows it:
  standin         the output comes from a LOCAL STAND-IN: no sound card, so the speech goes to WAV files and nothing is played.
  standin_remote  the output also comes from archive.org, which stands in for YouTube; the slide must say so.
Counts that depend on timing are never printed; a program whose transcript differs between two runs is refused by the runner (Whisper is run with temperature=0.0 where its random
fallback would make the text differ between runs)."""
__version__ = "1.0.0"
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_HEAD = r'''import atexit, contextlib, itertools, importlib.metadata as md, io, os, sys, re, json, time, shutil, tempfile, warnings, subprocess, wave, array, hashlib, struct, zlib, urllib.request
warnings.simplefilter('ignore')
LATEST = os.environ.get('CH24_LATEST', sys.executable)
PINS = os.environ.get('CH24_PINS', '/home/claude/venv312_ch24_pins/bin/python')
BARE = os.environ.get('CH24_BARE', '/home/claude/venv314_ch24_bare/bin/python')
CACHE = os.environ.get('CH24_CACHE', '/home/claude/ch24_cache'); os.makedirs(CACHE, exist_ok=True)
UA = {'User-Agent': 'SEN0414-deck/1.0 (academic course; altunel.yusuf@gmail.com)'}
ASSETS = {'gettysburg_shurtagal.mp3': ('https://archive.org/download/gettysburg_shurtagal_librivox/Gettysburg_Address_Lincoln_64kb.mp3',
                                       'd9f40f965d68153694417cc739c7690021aa39ba80f22d1c3927aeaa97e29dc0')}
def sha(n): return hashlib.sha256(open(n, 'rb').read()).hexdigest()[:12]
def done(n):
    k = os.environ.get('CH24_KEEP')
    if k: shutil.copy(n, os.path.join(k, os.path.basename(n)))
    print('saved %s: %d bytes, sha256 %s' % (os.path.basename(n), os.path.getsize(n), sha(n)))
def fetch(name):
    p = os.path.join(CACHE, name); url, want = ASSETS[name]
    if not os.path.exists(p):
        open(p + '.part', 'wb').write(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read()); os.replace(p + '.part', p)
    if hashlib.sha256(open(p, 'rb').read()).hexdigest() != want: print('NOT EXECUTED: %s differs from the file the study recorded' % name); sys.exit(0)
    return p
def wavinfo(p):
    w = wave.open(p); n = w.getnframes(); a = array.array('h', w.readframes(n))
    return {'channels': w.getnchannels(), 'width': w.getsampwidth(), 'rate': w.getframerate(), 'frames': n, 'seconds': round(n / w.getframerate(), 2), 'peak': max(abs(x) for x in a) if len(a) else 0}
def samples(p):
    w = wave.open(p); return list(array.array('h', w.readframes(w.getnframes()))), w.getframerate()
def wait_file(p, limit=60, quiet=0.4):
    t0 = time.time(); last = -1; since = None
    while time.time() - t0 < limit:
        if os.path.exists(p):
            n = os.path.getsize(p)
            if n == last and n > 44:
                if since is not None and time.time() - since >= quiet: return True
            else: since = time.time(); last = n
        time.sleep(0.05)
    return os.path.exists(p)
def png(name, w, h, pix):
    raw = b''.join(b'\x00' + bytes(c for x in range(w) for c in pix(x, y)) for y in range(h))
    chunk = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d))
    open(name, 'wb').write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))
def strips(name, rows, w=480, hh=60, colors=((47, 109, 98), (217, 122, 20), (43, 38, 34))):
    # rows: list of (samples, seconds): each strip draws the peak of the samples under one pixel column, one time scale for all strips (the longest row fills the width)
    tmax = max(s for _, s in rows); cols = []
    for k, (a, s) in enumerate(rows):
        n = len(a); c = []
        for x in range(w):
            lo, hi = int(x * tmax / s * n / w), int((x + 1) * tmax / s * n / w)
            c.append(max((abs(v) for v in a[lo:max(hi, lo + 1)]), default=0) if lo < n else -1)
        cols.append(c)
    def pix(x, y):
        k, yy = divmod(y, hh + 4)
        if k >= len(rows) or yy >= hh: return (242, 236, 225)
        v = cols[k][x]
        if v < 0: return (242, 236, 225)
        half = hh // 2; ext = max(1, int(v / 32768 * half))
        return colors[k % len(colors)] if abs(yy - half) <= ext else (255, 255, 255)
    png(name, w, len(rows) * (hh + 4), pix); done(name)
def err(f, n=60):
    try: f()
    except BaseException as e: return ('%s: %s' % (type(e).__name__, (str(e).splitlines() or [''])[0][:n])) if n else type(e).__name__
    return 'ok'
def say_to(engine, text, path):
    with contextlib.redirect_stdout(io.StringIO()):
        engine.save_to_file(text, path); engine.runAndWait(); wait_file(path)
def wer(ref, hyp):                    # word error rate: edits needed to turn hyp into ref, over the words of ref
    r, h = words(ref), words(hyp); d = list(range(len(h) + 1))
    for i, a in enumerate(r, 1):
        c = [i]
        for j, b in enumerate(h, 1): c.append(min(d[j] + 1, c[j - 1] + 1, d[j - 1] + (a != b)))
        d = c
    return d[-1] / len(r)
CHILD = """import pyttsx3, sys, time
e = pyttsx3.init(); e.setProperty(sys.argv[1], eval(sys.argv[2]))
e.save_to_file(sys.argv[3], 'm.wav'); e.runAndWait(); time.sleep(0.8)"""
def measure(prop, value, text):
    subprocess.run([LATEST, '-W', 'ignore', '-c', CHILD, prop, str(value), text], capture_output=True)
    a, rate = samples('m.wav'); os.remove('m.wav')
    return a, round(len(a) / rate, 2), max(abs(v) for v in a)
_A = ' Dinosaurs are a diverse group of reptiles of the clade dinosauria. They first'
_B = ' appeared during the triassic period. Between 245 and 233.23 million years ago.'
A, B = _A, _B
HOME = os.path.expanduser('~')
def audio_opts(stem):                 # the options of the download slide, with the format bestaudio/best and a file name from the stem
    return {'quiet': True, 'no_warnings': True, 'noprogress': True, 'format': 'bestaudio/best', 'outtmpl': stem + '.%(ext)s',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a'}]}
CHAPTER = {'srt': '1\n00:00:00,000 --> 00:00:05,640\n%s\n\n2\n00:00:05,640 --> 00:00:14,960\n%s\n' % (_A.strip(), _B.strip()),
           'vtt': 'WEBVTT\n\n00:00.000 --> 00:05.640\n%s\n\n00:05.640 --> 00:14.960\n%s\n' % (_A.strip(), _B.strip()),
           'tsv': 'start\tend\ttext\n0\t5640\t%s\n5640\t14960\t%s\n' % (_A.strip(), _B.strip())}
CHAPTER_KEYS = ['id', 'title', 'formats', 'thumbnails', 'thumbnail', 'description', 'channel_id', 'channel_url', 'duration', 'view_count',
                'average_rating', 'age_limit', 'webpage_url']
def probe_audio(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_name:format=duration', '-of', 'json', path], capture_output=True, text=True)
    j = json.loads(r.stdout); return j['streams'][0]['codec_name'], round(float(j['format']['duration']), 1)
def words(t): return re.sub(r"[^a-z' ]+", ' ', t.lower()).split()
def cues_picture(segs, name='cues.png', w=480, secs=15.0):
    # one bar for each subtitle cue on a time axis of `secs` seconds: the picture of the start and end times a writer prints
    def px(x, y):
        t = x / w * secs
        for k, s in enumerate(segs):
            if s['start'] <= t < s['end'] and 20 * k + 10 <= y < 20 * k + 26: return ((47, 109, 98), (217, 122, 20))[k % 2]
        return (242, 236, 225) if y % 40 < 38 else (200, 190, 175)
    png(name, w, 20 * len(segs) + 20, px); done(name)
WORK = tempfile.mkdtemp(prefix='ch24cut'); os.chdir(WORK)
atexit.register(lambda: (os.chdir('/'), shutil.rmtree(WORK, True)))
# ---- shown from here ----
'''

CONSOLES = {
    "title": ["import platform, importlib.metadata as m", "platform.python_version()", "m.version('pyttsx3')", "m.version('openai-whisper')", "m.version('yt-dlp')",
              "m.version('numpy')"],
    "tools": ["import shutil, os, importlib.util as u", "shutil.which('ffmpeg')", "shutil.which('espeak-ng')", "os.path.exists('/dev/snd')",
              "u.find_spec('audioop') is None", "u.find_spec('wave') is None"],
}


def _cut(body):
    return _HEAD + body


SAY_BODY = r"""import pyttsx3
events = []
engine = pyttsx3.init()
for topic in ('started-utterance', 'finished-utterance'):
    engine.connect(topic, lambda topic=topic, **kw: events.append(topic))
r = engine.say('Hello. How are you doing?')
print('say() returned', r, '| events', len(events), '| busy', engine.isBusy())
engine.setProperty('rate', 300)
print('rate before runAndWait:', engine.getProperty('rate'))
engine.runAndWait()
print('events:', events)
print('rate after runAndWait:', engine.getProperty('rate'))
print('say(""):', repr(engine.say('')))
"""

PIN_BODY = r"""SAY = '''import pyttsx3, sys, time, wave
e = pyttsx3.init(); e.save_to_file(sys.argv[1], 'a.wav')
e.runAndWait(); time.sleep(1); w = wave.open('a.wav')
print(round(w.getnframes() / w.getframerate(), 2))'''
VER = 'import importlib.metadata as m; print(m.version("pyttsx3"))'
def run(py, *code):
    args = [py, '-W', 'ignore', '-c', *code]
    done = subprocess.run(args, capture_output=True, text=True)
    return done.stdout
for label, py in (('pinned', PINS), ('newest', LATEST)):
    v = run(py, VER).strip()
    for text in ('Hello. How are you doing?', 'One. Two. Three.'):
        seconds = run(py, SAY, text).split()[-1]
        print('%s %-4s %-27r -> %s s' % (label, v, text, seconds))
"""

VOICES_BODY = r"""import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
first = voices[0]
print('voices:', len(voices), '| first:', first.name, first.gender, first.age)
print('  its languages:', first.languages)
print('genders:', {v.gender for v in voices}, 'ages:', {v.age for v in voices})
print('English voices:', sum(v.languages[0].startswith('en') for v in voices))
print('the engine starts with:', engine.getProperty('voice'))
print('voices[1]:', voices[1].id, '|', voices[1].name, voices[1].languages)
engine.setProperty('voice', voices[1].id)
engine.save_to_file('Hello. How are you doing?', 'hello.wav')
engine.runAndWait(); wait_file('hello.wav')
print('hello.wav with it:', wavinfo('hello.wav')['seconds'], 's')
"""

RATE_BODY = r"""FOX = 'The quick brown fox jumps over the yellow lazy dog.'
print('rate -> seconds of audio (a fresh process each)')
for rate in (50, 100, 150, 200, 250, 300, 400):
    audio, seconds, peak = measure('rate', rate, FOX)
    print('  %3d -> %.2f s' % (rate, seconds))
volumes = (1.0, 0.75, 0.5, 0.1, 0.0, 5)
peaks = [measure('volume', v, FOX)[2] for v in volumes]
print('volume', volumes)
print('peak  ', peaks)
slow, fast = measure('rate', 100, FOX), measure('rate', 300, FOX)
strips('waves.png', [(slow[0], slow[1]), (fast[0], fast[1])])
"""

WAV_BODY = r"""import pyttsx3
engine = pyttsx3.init()
engine.save_to_file('Hello. How are you doing?', 'hello.wav')
print('before runAndWait the file exists:', os.path.exists('hello.wav'))
engine.runAndWait(); wait_file('hello.wav')
w = wave.open('hello.wav')
print('channels', w.getnchannels(), '| bytes per sample', w.getsampwidth())
print('rate', w.getframerate(), '| frames', w.getnframes())
print('seconds', round(w.getnframes() / w.getframerate(), 2))
engine.save_to_file('Hello.', 'hello.mp3'); engine.runAndWait()
wait_file('hello.mp3'); head = open('hello.mp3', 'rb').read(12)
print('hello.mp3 begins with', head[:4], 'and', head[8:])
a, rate = samples('hello.wav')
strips('hello.png', [(a, len(a) / rate)])
"""

RACE_BODY = r"""def child(code, limit=5):
    try:
        args = [LATEST, '-W', 'ignore', '-c', code]
        r = subprocess.run(args, capture_output=True, timeout=limit)
        return 'returned, exit %d' % r.returncode
    except subprocess.TimeoutExpired:
        return 'not back after %d seconds' % limit
INIT = 'import pyttsx3; e = pyttsx3.init(); '
RATE = 'e.setProperty("rate", 150); e.runAndWait(); '
AGAIN = INIT + RATE + 'e.runAndWait()'
print('property change, runAndWait once:', child(INIT + RATE))
print('and a second runAndWait():', child(AGAIN))
FIRST = 'e.save_to_file("Hello.", "a.wav"); e.runAndWait(); '
MISSING = 'e.save_to_file("Hi", "/no/x.wav"); e.runAndWait()'
print('missing folder, first call:', child(INIT + MISSING))
print('missing folder after speech:', child(INIT + FIRST + MISSING))
"""

MODELS_BODY = r"""import torch, whisper
names = whisper.available_models()
print('whisper', md.version('openai-whisper'), '| models:', len(names))
for name in ('tiny', 'base', 'small'):
    model = whisper.load_model(name)
    millions = sum(p.numel() for p in model.parameters()) / 1e6
    size = os.path.getsize(HOME + '/.cache/whisper/%s.pt' % name)
    print('%-5s %5.1f M parameters, %d bytes' % (name, millions, size))
print('cuda available:', torch.cuda.is_available(), '| on', model.device)
cuda = lambda: whisper.load_model('tiny', device='cuda')
print('device="cuda":', err(cuda, 0))
"""

TRANS_BODY = r"""import pyttsx3, whisper
FOX = 'The quick brown fox jumps over the yellow lazy dog.'
engine = pyttsx3.init()
say_to(engine, FOX, 'fox.wav')
for name in ('tiny', 'base', 'small'):
    result = whisper.load_model(name).transcribe('fox.wav')
    text = result['text']
    print('%-5s %r WER %.1f' % (name, text, wer(FOX, text)))
print('result keys:', list(result))
print('segment keys:', list(result['segments'][0])[:6])
"""

FFMPEG_BODY = r"""import pyttsx3, whisper
FOX = 'The quick brown fox jumps over the yellow lazy dog.'
engine = pyttsx3.init()
say_to(engine, FOX, 'fox.wav')
print('ffmpeg on the PATH:', shutil.which('ffmpeg'))
audio = whisper.load_audio('fox.wav')
print('load_audio ->', type(audio).__name__, audio.dtype, audio.shape)
path = os.environ['PATH']; os.environ['PATH'] = '/nonexistent'
print('no ffmpeg:', err(lambda: whisper.load_audio('fox.wav')))
tiny = whisper.load_model('tiny')
print('transcribe:', err(lambda: tiny.transcribe('fox.wav')))
os.environ['PATH'] = path
a = [int(v * 32767) for v in audio]
strips('audio16k.png', [(a, len(a) / 16000)])
"""

LANG_BODY = r"""import pyttsx3, whisper
SAY = {'tr': 'Merhaba, bugün hava çok güzel.',
       'de': 'Guten Morgen, wie geht es Ihnen heute?',
       'fr': "Bonjour, comment allez-vous aujourd'hui ?",
       'es': 'Buenos días, ¿cómo está usted hoy?',
       'it': 'Buongiorno, come sta oggi?',
       'en-us': 'Good morning, how are you today?'}
engine = pyttsx3.init()
ids = {v.languages[0]: v.id for v in engine.getProperty('voices')}
models = {n: whisper.load_model(n) for n in ('tiny', 'base')}
hit = dict.fromkeys(models, 0)
for code, text in SAY.items():
    engine.setProperty('voice', ids.get(code, code))
    say_to(engine, text, code + '.wav'); row = {}
    for n, m in models.items():
        row[n] = m.transcribe(code + '.wav', temperature=0.0)['language']
        hit[n] += row[n] == code[:2]
    print('%-5s heard as %s' % (code, row))
print('right of %d:' % len(SAY), hit)
print('languages Whisper knows:', len(whisper.tokenizer.LANGUAGES))
bad = lambda: models['tiny'].transcribe('tr.wav', language='klingon')
print('klingon:', err(bad, 0))
"""

CUES_BODY = r"""import whisper
from whisper.utils import get_writer
segs = [{'id': 0, 'start': 0.0, 'end': 5.64, 'text': A},
        {'id': 1, 'start': 5.64, 'end': 14.96, 'text': B}]
book = {'text': A + B, 'language': 'en', 'segments': segs}
for fmt in ('srt', 'vtt', 'tsv'):
    get_writer(fmt, '.')(book, 'audio')
    got = open('audio.' + fmt, encoding='utf-8').read()
    same = got.strip() == CHAPTER[fmt].strip()
    print('%s %4d bytes, same as the book: %s' % (fmt, len(got), same))
print('SRT time:', open('audio.srt').read().splitlines()[1])
print('VTT time:', open('audio.vtt').read().splitlines()[2])
print('TSV columns:', open('audio.tsv').read().splitlines()[0].split('\t'))
print('docx writer:', err(lambda: get_writer('docx', '.')))
cues_picture(segs)
"""

OPT_BODY = r"""import whisper
from whisper.utils import get_writer
audio = fetch('gettysburg_shurtagal.mp3')
model = whisper.load_model('tiny')
r = model.transcribe(audio, language='en')
get_writer('srt', '.')(r, 'plain')
n = len(open('plain.srt').read().strip().split('\n\n'))
times = [t for s in r['segments'] for t in (s['start'], s['end'])]
print('segments', len(r['segments']), '| blocks', n, '| times', len(times))
grid = sum(abs(t / 0.02 - round(t / 0.02)) < 1e-6 for t in times)
print('times that are multiples of 0.02 s:', grid, 'of', len(times))
w = model.transcribe(audio, language='en', word_timestamps=True)
print('words with times in segment 1:', len(w['segments'][0]['words']))
opts = {'max_line_width': 30, 'max_line_count': 2}
get_writer('srt', '.')(w, 'wide', opts)
blocks = open('wide.srt').read().strip().split('\n\n')
print('max_line_width=30:', len(blocks), 'blocks; the first:')
print(blocks[0])
"""

YTM_BODY = r"""import yt_dlp
URL = 'https://archive.org/details/gettysburg_shurtagal_librivox'
with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
    info = ydl.extract_info(URL, download=False)
    print('title:', info['title'], '| extractor:', info['extractor'])
    print('formats:', len(info['formats']), '| keys:', len(info))
    have = [k for k in CHAPTER_KEYS if k in info]
    print('of the 13 keys the chapter prints, here:', len(have))
    print('  missing:', ', '.join(k for k in CHAPTER_KEYS if k not in info))
    print('YoutubeDL has sanitize_info:', hasattr(ydl, 'sanitize_info'),
          '| sanitize:', hasattr(ydl, 'sanitize'))
    open('metadata.json', 'w').write(json.dumps(ydl.sanitize_info(info)))
kept = len(json.load(open('metadata.json')))
print('metadata.json holds', kept, 'keys, as JSON')
"""

YTD_BODY = r"""import yt_dlp
URL = 'https://archive.org/details/gettysburg_shurtagal_librivox'
options = {'quiet': True, 'no_warnings': True, 'noprogress': True,
           'outtmpl': 'downloaded_content.%(ext)s',
           'format': 'm4a/bestaudio/best',
           'postprocessors': [{'key': 'FFmpegExtractAudio',
                               'preferredcodec': 'm4a'}]}
with yt_dlp.YoutubeDL(options) as ydl:
    print('download() returned', ydl.download([URL]))
print('files:', sorted(os.listdir('.')))
codec, seconds = probe_audio('downloaded_content.m4a')
print('codec', codec, '| seconds', seconds)
NOWHERE = ['https://archive.org/details/no_such_item_ch24_zz']
with yt_dlp.YoutubeDL(dict(options, outtmpl='again.%(ext)s')) as ydl:
    print('a string instead of a list:', err(lambda: ydl.download(URL)))
    print('an address that is nowhere:', err(lambda: ydl.download(NOWHERE), 0))
"""

GUESS_BODY = r"""import pyttsx3
class Recorder:                       # a stand-in engine for tests
    def __init__(self): self.said = []
    def say(self, text): self.said.append(text)
    def runAndWait(self): pass
def make_speak(engine):
    def speak(text):                  # to the screen, then aloud
        print(text); engine.say(text); engine.runAndWait()
    return speak
def game(speak, guesses, secret):
    speak('I am thinking of a number between 1 and 20.')
    for n, g in enumerate(guesses, 1):
        if g == secret: return speak('Good job! You won in %d.' % n)
        speak('%d is too %s.' % (g, 'low' if g < secret else 'high'))
rec = Recorder(); game(make_speak(rec), [10, 15, 12], 12)
print('Recorder:', len(rec.said), 'lines;', rec.said[1])
engine = pyttsx3.init(); lines = itertools.count(1)
class Writer:                         # the real engine
    def say(self, text): say_to(engine, text, 'line%d.wav' % next(lines))
    def runAndWait(self): pass
game(make_speak(Writer()), [5, 18, 12], 12)
print('secs', [wavinfo('line%d.wav' % k)['seconds'] for k in range(1, 5)])
"""

SONG_BODY = r"""import pyttsx3
def bottles(k):
    if k == 0: return 'No more bottles'
    return '1 bottle' if k == 1 else '%d bottles' % k
def verse(n):
    this, nxt = bottles(n), bottles(n - 1)
    return '\n'.join([this + ' of beer on the wall,', this + ' of beer,',
                      'Take one down, pass it around,',
                      nxt + ' of beer on the wall.'])
print(verse(2)); print(verse(1))
song = '\n\n'.join(verse(n) for n in range(99, 0, -1))
lines = [l for l in song.splitlines() if l]
print('99 verses:', len(lines), 'lines,', len(song.split()), 'words')
print('and', len(song), 'characters')
engine = pyttsx3.init()
for n in (3, 99):
    name = 'song%d.wav' % n
    say_to(engine, '\n\n'.join(verse(k) for k in range(n, 0, -1)), name)
    s = wavinfo(name)['seconds']
    size = os.path.getsize(name) / 1e6
    print('%2d verses: %.1f s, %.1f min, %.1f MB' % (n, s, s / 60, size))
a, rate = samples('song3.wav'); strips('song.png', [(a, len(a) / rate)])
"""

LOOP_BODY = r"""import glob, yt_dlp, whisper
from whisper.utils import get_writer
def transcribe_urls(urls, formats=('srt',), model_name='tiny'):
    model = whisper.load_model(model_name); results = []
    for k, url in enumerate(urls):
        stem = 'video%d' % k
        with yt_dlp.YoutubeDL(audio_opts(stem)) as ydl:
            ydl.download([url])
        audio = glob.glob(stem + '.*')[0]
        result = model.transcribe(audio, language='en', temperature=0.0)
        for f in formats: get_writer(f, '.')(result, stem)
        results.append((audio, result))
    return results
URLS = ['https://archive.org/details/gettysburg_shurtagal_librivox',
        'https://archive.org/details/gettysburg_johng_librivox']
for audio, r in transcribe_urls(URLS, formats=('srt', 'vtt', 'txt')):
    print(len(r['segments']), 'segments', len(r['text'].split()), 'words')
BAD = ['https://archive.org/details/no_such_item_ch24_zz']
print('one bad address:', err(lambda: transcribe_urls(BAD), 0))
"""

PROGRAMS = {
    "sayCut_v1_0_0.py": (_cut(SAY_BODY), (), True),
    "pinCut_v1_0_0.py": (_cut(PIN_BODY), (), True),
    "voicesCut_v1_0_0.py": (_cut(VOICES_BODY), (), True),
    "rateCut_v1_0_0.py": (_cut(RATE_BODY), (), True),
    "wavCut_v1_0_0.py": (_cut(WAV_BODY), (), True),
    "raceCut_v1_0_0.py": (_cut(RACE_BODY), (), True),
    "modelsCut_v1_0_0.py": (_cut(MODELS_BODY), (), True),
    "transcribeCut_v1_0_0.py": (_cut(TRANS_BODY), (), True),
    "ffmpegCut_v1_0_0.py": (_cut(FFMPEG_BODY), (), True),
    "langCut_v1_0_0.py": (_cut(LANG_BODY), (), True),
    "cuesCut_v1_0_0.py": (_cut(CUES_BODY), (), True),
    "optionsCut_v1_0_0.py": (_cut(OPT_BODY), (), True),
    "ytMetaCut_v1_0_0.py": (_cut(YTM_BODY), (), True),
    "ytDownCut_v1_0_0.py": (_cut(YTD_BODY), (), True),
    "guessCut_v1_0_0.py": (_cut(GUESS_BODY), (), True),
    "songCut_v1_0_0.py": (_cut(SONG_BODY), (), True),
    "loopCut_v1_0_0.py": (_cut(LOOP_BODY), (), True),
}
REMOTE = {"optionsCut_v1_0_0.py", "ytMetaCut_v1_0_0.py", "ytDownCut_v1_0_0.py", "loopCut_v1_0_0.py"}
PLAIN = {"modelsCut_v1_0_0.py", "cuesCut_v1_0_0.py"}  # these two speak nothing: they need no stand-in words on their slides
KIND = {n: ("standin_remote" if n in REMOTE else "plain" if n in PLAIN else "standin") for n in PROGRAMS}
# the words that must stand on a slide that shows the program (honesty_check): a program that writes speech needs 'No sound card'; one that reads archive.org needs 'archive.org' and 'stands in for YouTube'
STANDKEY = {n: (("archive.org", "stands in for YouTube") if n in REMOTE else () if n in PLAIN else ("No sound card", "local stand-in")) for n in PROGRAMS}
# the pictures a slide shows: file name -> the program that makes it
IMAGES = {"waves.png": "rateCut_v1_0_0.py", "hello.png": "wavCut_v1_0_0.py", "audio16k.png": "ffmpegCut_v1_0_0.py", "cues.png": "cuesCut_v1_0_0.py",
          "song.png": "songCut_v1_0_0.py"}
EQUIV = {}
SUBSET = {}

CHARTS = {
    "rateSeconds": {
        "setup": "import json, os, re\nR = json.load(open(os.path.join(HERE, 'examples_out_v1_0_0.json')))['_programs']['rateCut_v1_0_0.py']['transcript']\n"
                 "ROWS = [('rate %s' % m.group(1), float(m.group(2))) for m in re.finditer(r'^ +(\\d+) -> ([0-9.]+) s$', R, re.M)]\n",
        "expr": "ROWS"},
    "werByModel": {
        "setup": "import json, os, re\nR = json.load(open(os.path.join(HERE, 'examples_out_v1_0_0.json')))['_programs']['transcribeCut_v1_0_0.py']['transcript']\n"
                 "ROWS = [(m.group(1), float(m.group(2))) for m in re.finditer(r'^(tiny|base|small) .* WER ([0-9.]+)$', R, re.M)]\n",
        "expr": "ROWS"},
}

_PROBE = r'''
import json, sys, shutil, importlib.metadata as md, importlib.util, warnings
warnings.simplefilter('ignore')
r = {'Python': sys.version.split()[0]}
def v(n):
    try: return md.version(n)
    except md.PackageNotFoundError: return 'none'
r['pyttsx3'] = v('pyttsx3'); r['openai-whisper'] = v('openai-whisper'); r['yt-dlp'] = v('yt-dlp'); r['NumPy'] = v('numpy')
r['ffmpeg'] = 'found' if shutil.which('ffmpeg') else 'none'
try:
    import pyttsx3; pyttsx3.init(); r['init'] = 'Engine'
except BaseException as e:
    r['init'] = type(e).__name__
r['whisper'] = 'found' if importlib.util.find_spec('whisper') else 'none'
print(json.dumps(r))
'''
INTERPS = [("newest", "/home/claude/venv314_ch24_latest/bin/python", "full"), ("pinned", "/home/claude/venv312_ch24_pins/bin/python", "full"),
           ("no ffmpeg", "/home/claude/venv314_ch24_latest/bin/python", "noffmpeg"), ("empty", "/home/claude/venv314_ch24_bare/bin/python", "full")]
_ROWS = [("Python", "Python"), ("pyttsx3", "pyttsx3"), ("openai-whisper", "openai-whisper"), ("yt-dlp", "yt-dlp"), ("NumPy", "NumPy"), ("ffmpeg", "ffmpeg"),
         ("pyttsx3.init()", "init"), ("whisper found", "whisper")]

TABLES = {
    "environments": {
        "setup": "import json, os, shutil, subprocess, tempfile\nPROBE = %r\nINTERPS = %r\nROWS = %r\nres = []\n"
                 "nof = tempfile.mkdtemp()\nfor tool in ('espeak-ng', 'aplay'):\n    os.symlink(shutil.which(tool), os.path.join(nof, tool))\n"
                 "for label, p, mode in INTERPS:\n    env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH',)}\n"
                 "    if mode == 'noffmpeg': env['PATH'] = nof\n"
                 "    r = subprocess.run([p, '-c', PROBE], capture_output=True, text=True, env=env, stdin=subprocess.DEVNULL)\n"
                 "    assert r.returncode == 0, (label, r.stderr[-300:])\n    res.append(json.loads(r.stdout.strip().splitlines()[-1]))\n"
                 "def fmt(v):\n    return v.replace('ModuleNotFoundError', 'ModuleNotFound').replace('RuntimeError', 'RuntimeErr')\n" % (_PROBE, INTERPS, _ROWS),
        "expr": "[['check'] + [l for l, p, m in INTERPS]] + [[label] + [fmt(x.get(key, '-')) for x in res] for label, key in ROWS]"},
    "releases": {
        "setup": "import json, os\nD = json.load(open(os.path.join(HERE, '..', 'ch24-page', 'interpreter_record_v1_0_0.json')))\n"
                 "def kind(v):\n    f = v.get('NOT EXECUTED or failed')\n    if f is None: return 'ran'\n    if 'SIGSEGV' in f: return 'segfault'\n"
                 "    if 'sw_vers' in f: return 'macOS only'\n    if 'unsatisfiable' in f: return 'no install'\n    if 'imghdr' in f: return 'no imghdr'\n    return 'import err'\n"
                 "def tally(key, label, python):\n    ks = [kind(v) for v in D[key].values()]\n"
                 "    return [label, python, str(len(ks)), str(ks.count('ran')), ', '.join('%d %s' % (ks.count(k), k) for k in dict.fromkeys(ks) if k != 'ran')]\n",
        "expr": "[['package', 'Python', 'releases', 'ran', 'the others']] + [tally('pyttsx3 releases', 'pyttsx3', '3.14.6'), tally('openai-whisper releases', 'openai-whisper', '3.12.3'), tally('yt-dlp releases', 'yt-dlp (stable)', '3.14.6')]"},
    "models": {
        "setup": "import json, os\nM = json.load(open(os.path.join(HERE, '..', 'ch24-page', 'model_runtimes_v1_0_0.json')))['results']\n"
                 "BOOK = {'tiny': ('74MB', '1.9s'), 'base': ('142MB', '3.0s'), 'small': ('472MB', '9.6s'), 'medium': ('1.5GB', '28.6s'), 'large-v3': ('3GB', '51.9s')}\n"
                 "def row(n):\n    m = M[n]; b = BOOK[n]\n    if '10-word sample' not in m:\n"
                 "        return [n, b[0], b[1], '%.1f MB' % (m['file bytes'] / 1e6) if 'file bytes' in m else '-', '-', 'killed (-9)' if 'return code -9' in str(m) else 'does not load']\n"
                 "    return [n, b[0], b[1], '%.1f MB' % (m['file bytes'] / 1e6), '%.1f s' % m['10-word sample']['transcribe seconds'], '%d MiB' % m['peak resident memory of the process, MiB (ru_maxrss)']]\n",
        "expr": "[['model', 'file (book)', '10 words (book)', 'file (here)', '10 words (here)', 'memory (here)']] + [row(n) for n in BOOK]"},
    "configurations": {
        "setup": "import json, os\nT = json.load(open(os.path.join(HERE, '..', 'ch24-page', 'third_party_record_v1_0_0.json')))['items']\n"
                 "CF = list(T[0]['output'])\nROW = {'LATEST': 'newest', 'PINS': 'pinned', 'BARE': 'empty', 'NOFFMPEG': 'no ffmpeg'}\n"
                 "def n(i):\n    s = [x for l in T[i]['output']['results'] for x in l['statements']]\n    return '%d of %d' % (sum(bool(x['as printed'].get('matches the book')) and 'not executed' not in x['as printed'] for x in s), len(s))\n"
                 "def ran(i):\n    s = [x for l in T[i]['output']['results'] for x in l['statements']]\n    return '%d' % sum(not x['as printed'].get('raised') and 'not executed' not in x['as printed'] for x in s)\n"
                 "def pkg(c, k):\n    v = T[0]['output'][c][k]\n    return '-' if v is None else str(v)\n",
        "expr": "[['row', 'Python', 'pyttsx3', 'openai-whisper', 'ffmpeg', 'ran without an exception', 'statements = book']] + "
                "[[ROW[c], pkg(c, 'python'), pkg(c, 'pyttsx3'), pkg(c, 'openai-whisper'), 'yes' if pkg(c, 'ffmpeg on the PATH') != '-' else 'no', ran(2 + i), n(2 + i)] for i, c in enumerate(CF)]"},
}
