#!/usr/bin/env python3
"""SEN0414 chapter 24 (Text-to-Speech and Speech Recognition Engines, 3rd edition) - the shared base of the corpus, version 1.0.0.

Holds the chapter's whole programs as text, the single source a deck or a page's Lab tab can read, in the shape of sen0414_ch23_corpus_base_v1_0_0.py.
Each program is a complete script that exits 0 and prints what it printed on 2026-10-14 under Python 3.14.6 (uv) in the environment /home/claude/venv314_ch24_latest
(pyttsx3 2.99, openai-whisper 20250625, yt-dlp 2026.8.19, torch 2.14.1+cpu, NumPy 2.5.4) on Ubuntu 24.04 with the REAL eSpeak NG 1.51 (apt) as the speech engine of pyttsx3 and the real
ffmpeg 6.1.1 (apt) for Whisper and yt-dlp. The interpreter that runs the file is the one that starts the programs (the variable CH24_LATEST overrides it for child processes).
What is NOT EXECUTED anywhere here, because it needs hardware or an account this machine lacks: any SOUND (this machine has no sound card, so say() runs through eSpeak and then the
shell command aplay fails to open an audio device: nothing is heard, and every program says so), any microphone, any GPU (device cuda), Windows (SAPI5) and macOS (NSSpeechSynthesizer),
and the download of a video from YouTube (the programs ask YouTube for METADATA only; audio is downloaded from archive.org, which hosts the public-domain LibriVox readings used here).
The files the programs need are FETCHED AT RUN TIME into the cache folder CH24_CACHE (default /home/claude/ch24_cache) and checked against the SHA-256 the study recorded: the text of
"Alice's Adventures in Wonderland" (Project Gutenberg #11) and four LibriVox readings of the Gettysburg Address (public domain, archive.org); a file that does not match stops the program
with "NOT EXECUTED" and the reason. The Whisper model files are fetched by Whisper itself on first use (tiny 72 MB, base 139 MB) into ~/.cache/whisper.
Every Whisper number in this file is a SINGLE RUN of one program on a machine with 2 virtual CPUs; seconds depend on the machine.
LOCAL STAND-IN: none of the programs uses a display; the synthesised speech goes to WAV files in a folder that is deleted, and nothing is played.
The record that reads the book's page and asks the public services is sen0414_ch24_live_v1_0_0.py; the one that replays the chapter's listings is sen0414_ch24_thirdparty_v1_0_0.py;
the one that times the models is sen0414_ch24_models_v1_0_0.py.
"""
__version__ = "1.0.0"
HEAD = r"""import io, os, sys, re, json, time, shutil, signal, tempfile, warnings, subprocess, wave, array, hashlib, urllib.request, importlib.metadata as md
warnings.simplefilter('ignore')
LATEST = os.environ.get('CH24_LATEST', sys.executable)
CACHE = os.environ.get('CH24_CACHE', '/home/claude/ch24_cache'); os.makedirs(CACHE, exist_ok=True)
UA = {'User-Agent': 'SEN0414-research/1.0 (academic course; altunel.yusuf@gmail.com)'}
ASSETS = {'alice.txt': ('https://www.gutenberg.org/cache/epub/11/pg11.txt', '01b38ea4c710a84bc18d0bd41271a5a1a92b94e97b2812f4dece97d4a694725e'),
          'gettysburg_shurtagal.mp3': ('https://archive.org/download/gettysburg_shurtagal_librivox/Gettysburg_Address_Lincoln_64kb.mp3', 'd9f40f965d68153694417cc739c7690021aa39ba80f22d1c3927aeaa97e29dc0')}
BLISS = 'Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal. Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure.'
def sha(b): return hashlib.sha256(b).hexdigest()
def fetch(name):
    p = os.path.join(CACHE, name); url, want = ASSETS[name]
    if not os.path.exists(p):
        open(p + '.part', 'wb').write(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read()); os.replace(p + '.part', p)
    if sha(open(p, 'rb').read()) != want: print('NOT EXECUTED: %s differs from the file the study recorded' % name); sys.exit(0)
    return p
def wavinfo(p):
    w = wave.open(p); n = w.getnframes(); a = array.array('h', w.readframes(n))
    return {'channels': w.getnchannels(), 'bytes per sample': w.getsampwidth(), 'sample rate': w.getframerate(), 'frames': n, 'seconds': round(n / w.getframerate(), 2), 'peak': max(abs(x) for x in a) if len(a) else 0}
def wait_file(p, limit=120, quiet=0.4):
    # the file exists AND has stopped growing for `quiet` seconds (pyttsx3's runAndWait() can return while the WAV is still being written: measured by the program saveToFileAndRace)
    t0 = time.time(); last = -1; since = None
    while time.time() - t0 < limit:
        if os.path.exists(p):
            n = os.path.getsize(p)
            if n == last and n > 44:
                if since is not None and time.time() - since >= quiet: return True
            else: since = time.time(); last = n
        time.sleep(0.05)
    return os.path.exists(p)
def say_to_wav(text, path, **props):
    import pyttsx3
    e = pyttsx3.init()
    for k, v in props.items(): e.setProperty(k, v)
    e.save_to_file(text, path); e.runAndWait(); wait_file(path); return path
def words(t):
    t = t.lower().replace('\u2014', ' ').replace('\u2013', ' ').replace('-', ' ').replace('\u2019', "'").replace('can not', 'cannot')
    return re.sub(r"[^a-z0-9' ]+", ' ', t).split()
def wer(ref, hyp):
    r, h = words(ref), words(hyp); prev = list(range(len(h) + 1))
    for i, a in enumerate(r, 1):
        cur = [i]
        for j, b in enumerate(h, 1): cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a != b)))
        prev = cur
    return round(prev[-1] / len(r), 4)
def err(f):
    try: return ('ok', f())
    except BaseException as e: return (type(e).__name__, (str(e).splitlines() or [''])[0][:150])
os.chdir(tempfile.mkdtemp(prefix='ch24work'))
"""
HELLO = HEAD + r'''# Chapter 24, "Generating Speech": the book's hello_tts.py (listing 1) run with the keyboard answer supplied by the program. NOT heard: this machine has no sound card.
import builtins
import pyttsx3
events = []
engine = pyttsx3.init()
for topic in ('started-utterance', 'started-word', 'finished-utterance', 'error'):
    engine.connect(topic, lambda topic=topic, **kw: events.append((topic, kw.get('name'), kw.get('location'))))
builtins.input = lambda prompt='': (print(prompt + 'fine'), 'fine')[1]          # the listing waits for the user's answer; the program gives it
t0 = time.time()
r1 = engine.say('Hello. How are you doing?')
print('say() returned', r1, 'after', round(time.time() - t0, 3), 'seconds; events so far:', len(events), '(say only queues the text)')
engine.runAndWait()                                                              # the computer speaks (not here: aplay finds no sound card)
feeling = input('>')
engine.say('Yes. I am feeling ' + feeling + ' as well.')
engine.runAndWait()
print('events in order (topic, word):', [(t, n) for t, n, _ in events if t != 'started-word'] + [('words', [n for t, n, _ in events if t == 'started-word'])])
print('say("") returns:', repr(engine.say('')), '| say(None) returns:', repr(engine.say(None)))
print('isBusy after the loops:', engine.isBusy())
print('nothing was heard: sound cards on this machine:', os.path.exists('/dev/snd'), '| aplay -l says:', subprocess.run(['aplay', '-l'], capture_output=True, text=True).stderr.strip().splitlines()[-1:])
'''
VOICES = HEAD + r'''# Chapter 24, "Generating Speech": getProperty and setProperty on the real eSpeak NG voices of this machine (listing 2, 3 and 4), and what the chapter does not say about when a property takes effect.
import pyttsx3
engine = pyttsx3.init()
print("volume:", engine.getProperty("volume"), "| rate:", engine.getProperty("rate"), '| voice id:', engine.getProperty('voice'))
voices = engine.getProperty('voices')
print('voices:', len(voices), '| type of the first:', type(voices[0]).__name__, '| printed object:', re.sub(r'0x[0-9a-f]+', '0xADDR', repr(voices[0])))
for v in voices[:3]: print(' ', v.name, v.gender, v.age, v.languages)
print('genders seen:', sorted({str(v.gender) for v in voices}), '| ages seen:', sorted({str(v.age) for v in voices}), '| voices with an empty languages list:', sum(1 for v in voices if not v.languages))
en = [v for v in voices if v.languages and v.languages[0].startswith('en')]
print('English voices:', len(en), '| first three ids:', [v.id for v in en[:3]])
print('property names: unknown ->', err(lambda: engine.getProperty('pitchh')), '|', err(lambda: engine.setProperty('colour', 1)))
engine.setProperty('rate', 300); engine.setProperty('volume', 0.5)
print('right after setProperty, before any runAndWait: rate', engine.getProperty('rate'), 'volume', engine.getProperty('volume'), '(setProperty only queues the change)')
def setf(k, val):
    engine.setProperty(k, val); engine.save_to_file('x', 'flush.wav'); engine.runAndWait(); wait_file('flush.wav'); os.remove('flush.wav'); return engine.getProperty(k)
print('voice set to voices[1].id:', setf('voice', voices[1].id), '| voices[1].id was', voices[1].id, '| and after that runAndWait had something to say: rate', engine.getProperty('rate'), 'volume', engine.getProperty('volume'))
print('a voice id that does not exist:', err(lambda: setf('voice', 'xx-nonexistent')))
print('rate as text:', err(lambda: setf('rate', 'fast')))
print('rate 3000, then 1:', [err(lambda r=r: setf('rate', r)) for r in (3000, 1)])
print('volume 5, then -1:', [err(lambda v=v: setf('volume', v)) for v in (5, -1)])
print('a property the chapter does not use, pitch: getProperty ->', err(lambda: engine.getProperty('pitch')))
print('the same Engine object comes back from init():', pyttsx3.init() is engine, '| module-level speak exists:', hasattr(pyttsx3, 'speak'))
'''
SAVE = HEAD + r'''# Chapter 24, "Saving Speech Audio to WAV Files" (listing 5): what save_to_file writes, what it needs, the .mp3 name, the 1,800 words, and the first-call race measured over fresh processes.
import pyttsx3
engine = pyttsx3.init()
engine.save_to_file('Hello. How are you doing?', 'hello.wav')
print('before runAndWait the file exists:', os.path.exists('hello.wav'))
engine.runAndWait(); wait_file('hello.wav')
print('hello.wav:', wavinfo('hello.wav'), '| bytes', os.path.getsize('hello.wav'))
engine.save_to_file('Hello.', 'hello.mp3'); engine.runAndWait(); wait_file('hello.mp3')
print('hello.mp3 begins with', open('hello.mp3', 'rb').read(12), '| ffprobe format:', subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=format_name', '-of', 'csv=p=0', 'hello.mp3'], capture_output=True, text=True).stdout.strip())
engine.save_to_file('Hello.', 'hello.aiff'); engine.runAndWait(); wait_file('hello.aiff')
print('hello.aiff begins with', open('hello.aiff', 'rb').read(12), '(the espeak driver ignores the extension)')
print('an empty text:', err(lambda: engine.save_to_file('', 'empty.wav')))
def child(code, limit=20):
    try:
        r = subprocess.run([LATEST, '-W', 'ignore', '-c', code], capture_output=True, text=True, timeout=limit, stdin=subprocess.DEVNULL); return 'returned, exit %d' % r.returncode
    except subprocess.TimeoutExpired: return 'NO RETURN: killed after %d seconds' % limit
PRE = 'import pyttsx3; e = pyttsx3.init(); e.save_to_file("Hello.", "a.wav"); e.runAndWait(); '
print('runAndWait() after an utterance, with only a property change to do:', child(PRE + 'e.setProperty("rate", 150); e.runAndWait()'))
print('runAndWait() twice, the first with only a property change and nothing to say:', child('import pyttsx3; e = pyttsx3.init(); e.setProperty("rate", 150); e.runAndWait(); e.runAndWait()'))
print('runAndWait() once, with only a property change and nothing to say:', child('import pyttsx3; e = pyttsx3.init(); e.setProperty("rate", 150); e.runAndWait()'))
print('save_to_file into a folder that does not exist, as the FIRST call of the process:', child('import pyttsx3; e = pyttsx3.init(); e.save_to_file("Hi", "/nonexistent/x.wav"); e.runAndWait()'))
print('save_to_file into a folder that does not exist, after a first utterance:', child(PRE + 'e.save_to_file("Hi", "/nonexistent/x.wav"); e.runAndWait()'))
alice = open(fetch('alice.txt'), encoding='utf-8-sig').read(); i = alice.index('Alice was beginning to get very tired')
w1800 = ' '.join(re.sub(r'\s+', ' ', alice[i:].replace('_', '')).split(' ')[:1800])
t0 = time.time(); engine.save_to_file(w1800, 'big.wav'); engine.runAndWait(); wait_file('big.wav', 300); dt = time.time() - t0
b = wavinfo('big.wav'); print('1800 words at the default rate: %.1f seconds of work gave %.1f seconds (%.1f minutes) of audio' % (dt, b['seconds'], b['seconds'] / 60), '| the chapter says 10 minutes in about two seconds')
RACE = "import pyttsx3, os, sys, time\nf = 'race.wav'\ne = pyttsx3.init(); e.save_to_file(sys.argv[1], f); e.runAndWait(); a = os.path.getsize(f) if os.path.exists(f) else 0; time.sleep(2.5); b = os.path.getsize(f) if os.path.exists(f) else 0; print(a, b)"
def trial(text, n):
    c = {'complete when runAndWait returned': 0, 'absent or still being written when it returned': 0, 'never written': 0}
    for _ in range(n):
        if os.path.exists('race.wav'): os.remove('race.wav')
        o = subprocess.run([LATEST, '-W', 'ignore', '-c', RACE, text], capture_output=True, text=True, timeout=60).stdout.strip().splitlines()[-1:]
        a, b = (int(x) for x in o[0].split()) if o else (0, 0)
        c['never written' if b == 0 else 'complete when runAndWait returned' if a == b else 'absent or still being written when it returned'] += 1
    return c
print('first save_to_file in a fresh process, 12 processes each (single run):')
print('  short text (5 words):', trial('Hello. How are you doing?', 12))
print('  longer text (33 words):', trial(' '.join(['Alice was beginning to get very tired of sitting by her sister on the bank'] * 3), 12))
'''
SWEEP = HEAD + r'''# Chapter 24, "Generating Speech": what the rate and the volume of listing 4 do to the audio, measured on WAV files (the chapter changes them but nobody can hear here).
import pyttsx3
T = 'The quick brown fox jumps over the yellow lazy dog.'
ONE = "import pyttsx3, sys, os, time\nk, v, path, text = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]\ne = pyttsx3.init(); e.setProperty(k, float(v) if k == 'volume' else int(v)); e.save_to_file(text, path); e.runAndWait()"
def fresh(k, v, path, text=T):
    # one fresh process per setting: the property is set before the first utterance of the process
    subprocess.run([LATEST, '-W', 'ignore', '-c', ONE, k, str(v), path, text], capture_output=True, text=True, timeout=120); wait_file(path); return wavinfo(path)
print('FRESH PROCESS for every setting (single run). rate -> seconds of audio for the 10-word sentence of the chapter, peak sample:')
base = {}
for r in (50, 100, 150, 200, 250, 300, 400):
    i = fresh('rate', r, 'r%d.wav' % r); base[r] = i['seconds']; print('  rate %3d: %5.2f s  (%.0f words per minute measured)  peak %d' % (r, i['seconds'], 10 / i['seconds'] * 60, i['peak']))
print('volume -> peak sample (32767 is the largest 16-bit value):')
for v in (1.0, 0.75, 0.5, 0.25, 0.1, 0.0):
    i = fresh('volume', v, 'v%s.wav' % v); full = wavinfo('r200.wav')['peak']; print('  volume %.2f: peak %5d  (%.0f%% of the peak at the default volume)' % (v, i['peak'], 100 * i['peak'] / full))
engine = pyttsx3.init(); same = 0; rows = []
for r in (50, 100, 150, 200, 250, 300, 400):
    engine.setProperty('rate', r); say_to_wav(T, 'in%d.wav' % r); s_ = wavinfo('in%d.wav' % r)['seconds']; rows.append((r, s_)); same += abs(s_ - base[r]) < 0.05
print('ONE process, setProperty before every save_to_file, the file waited for until it stopped growing: %d of 7 durations equal the fresh-process ones: %s' % (same, rows))
print('a property the chapter does not use, pitch: getProperty ->', err(lambda: engine.getProperty('pitch')), '| setProperty ->', err(lambda: engine.setProperty('pitch', 50)))
'''
WHISPER = HEAD + r'''# Chapter 24, "Speech Recognition" (listing 6): Whisper on the speech of listing 5 and on a human reading. The model files are downloaded by Whisper on first use.
import pyttsx3, whisper
print('openai-whisper', md.version('openai-whisper'), '| models it knows:', whisper.available_models())
say_to_wav('Hello. How are you doing?', 'hello.wav')
for name in ('tiny', 'base'):
    model = whisper.load_model(name)
    t0 = time.time(); result = model.transcribe('hello.wav'); dt = time.time() - t0
    print('%s: %r  language %s  %.1f s  keys %s  segment keys %s' % (name, result['text'], result['language'], dt, list(result), list(result['segments'][0])))
    print('  the chapter prints: Hello. How are you doing?  -> equal:', result['text'].strip() == 'Hello. How are you doing?')
model = whisper.load_model('tiny')
print('language="English":', repr(model.transcribe('hello.wav', language='English')['text']), '| language="en":', repr(model.transcribe('hello.wav', language='en')['text']))
print('language="Klingon":', err(lambda: model.transcribe('hello.wav', language='Klingon')))
from whisper.tokenizer import LANGUAGES
print('languages the tokenizer knows:', len(LANGUAGES), '| first five:', list(LANGUAGES.items())[:5])
print('load_model with no name:', err(lambda: whisper.load_model()))
print('device cuda on this machine:', err(lambda: whisper.load_model('tiny', device='cuda')))
print('torch.cuda.is_available():', __import__('torch').cuda.is_available(), '(NOT EXECUTED: any GPU)')
h = fetch('gettysburg_shurtagal.mp3')
t0 = time.time(); r = model.transcribe(h, language='en'); dt = time.time() - t0
print('a human reading (LibriVox, public domain), tiny: %.1f s for %.1f s of audio, %d segments, WER of its first 50 words against the Bliss copy %.3f' % (dt, r['segments'][-1]['end'], len(r['segments']), wer(BLISS, ' '.join(r['text'].split()[:50]))))
print('first segment:', {k: r['segments'][0][k] for k in ('start', 'end', 'text')})
sil = 'silence.wav'
with wave.open(sil, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000); w.writeframes(b'\x00\x00' * 16000 * 10)
rs = model.transcribe(sil, language='en'); print('ten seconds of digital silence ->', repr(rs['text']), 'segments:', len(rs['segments']))
import random; random.seed(7)
with wave.open('noise.wav', 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000); w.writeframes(array.array('h', [random.randint(-3000, 3000) for _ in range(16000 * 10)]).tobytes())
rn = model.transcribe('noise.wav', language='en'); print('ten seconds of white noise ->', repr(rn['text']), 'segments:', len(rn['segments']))
'''
FORMATS = HEAD + r'''# Chapter 24, "Speech Recognition": "Whisper can accept any audio or video file" - the same speech as WAV, MP3, OGG, FLAC and an MP4 and a Matroska file with a video track, and what happens without ffmpeg.
import pyttsx3, whisper
say_to_wav('The quick brown fox jumps over the yellow lazy dog.', 'fox.wav')
for name, cmd in (('fox.mp3', ['-c:a', 'libmp3lame']), ('fox.ogg', ['-c:a', 'libvorbis']), ('fox.flac', ['-c:a', 'flac']), ('fox.m4a', ['-c:a', 'aac'])):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'fox.wav'] + cmd + [name], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=blue:s=160x120:d=3', '-i', 'fox.wav', '-shortest', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', 'fox.mp4'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=red:s=160x120:d=3', '-i', 'fox.wav', '-shortest', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', 'fox.mkv'], check=True)
model = whisper.load_model('tiny')
for n in ('fox.wav', 'fox.mp3', 'fox.ogg', 'fox.flac', 'fox.m4a', 'fox.mp4', 'fox.mkv'):
    r = model.transcribe(n, language='en'); print('%-9s %7d bytes  ->  %r' % (n, os.path.getsize(n), r['text']))
print('a file that is not audio (a text file named x.wav):', err(lambda: (open('x.wav', 'w').write('hello'), model.transcribe('x.wav'))))
print('a file that does not exist:', err(lambda: model.transcribe('missing.wav')))
env = dict(os.environ); bindir = tempfile.mkdtemp()
for n in os.listdir('/usr/bin'):
    if n not in ('ffmpeg', 'ffprobe'):
        try: os.symlink('/usr/bin/' + n, os.path.join(bindir, n))
        except OSError: pass
env['PATH'] = os.path.dirname(sys.executable) + ':' + bindir
code = "import whisper\nm = whisper.load_model('tiny')\ntry:\n    m.transcribe('fox.wav')\nexcept BaseException as e:\n    print(type(e).__name__, str(e).splitlines()[0][:120])"
r = subprocess.run([sys.executable, '-W', 'ignore', '-c', code], capture_output=True, text=True, env=env, cwd=os.getcwd())
print('with no ffmpeg on the PATH:', (r.stdout.strip().splitlines() or r.stderr.strip().splitlines())[-1:])
w = whisper.audio.load_audio('fox.wav'); print('load_audio gives', type(w).__name__, w.dtype, w.shape, 'at', whisper.audio.SAMPLE_RATE, 'Hz (16 kHz mono float32, whatever the file was)')
'''
LANGS = HEAD + r'''# Chapter 24, "Speech Recognition": "work with most widely spoken human languages" - eSpeak NG speaks Turkish, German, French, Spanish, Chinese and English, and Whisper tiny and base are asked what language it is and what was said.
import pyttsx3, whisper
engine = pyttsx3.init()
vs = {v.languages[0]: v.id for v in engine.getProperty('voices') if v.languages}
SAY = {'tr': 'Merhaba, bug\u00fcn hava \u00e7ok g\u00fczel.', 'de': 'Guten Morgen, wie geht es Ihnen heute?', 'fr': 'Bonjour, comment allez-vous aujourd\u2019hui ?', 'es': 'Buenos d\u00edas, \u00bfc\u00f3mo est\u00e1 usted hoy?', 'cmn': '\u4eca\u5929\u5929\u6c14\u5f88\u597d\u3002', 'en-us': 'Good morning, how are you today?'}
for name in ('tiny', 'base'):
    model = whisper.load_model(name)
    for code, text in SAY.items():
        engine.setProperty('voice', vs.get(code, code)); f = 'l_%s.wav' % code; say_to_wav(text, f)
        r = model.transcribe(f); print('%-4s %-5s said %r -> language %s, text %r' % (name, code, text, r['language'], r['text'].strip()))
m = whisper.load_model('tiny'); a = whisper.load_audio('l_tr.wav'); a = whisper.pad_or_trim(a); mel = whisper.log_mel_spectrogram(a, n_mels=m.dims.n_mels).to(m.device)
_, probs = m.detect_language(mel); top = sorted(probs.items(), key=lambda kv: -kv[1])[:3]; print('detect_language on the Turkish speech, top three:', [(k, round(v, 3)) for k, v in top])
print('espeak-ng voices:', len(engine.getProperty('voices')), '| whisper languages:', len(whisper.tokenizer.LANGUAGES), '| whisper names accepted for Turkish:', [k for k in ('tr', 'turkish', 'Turkish', 'TURKISH', 'turk') if k.lower() in whisper.tokenizer.TO_LANGUAGE_CODE or k.lower() in whisper.tokenizer.LANGUAGES])
'''
SUBS = HEAD + r'''# Chapter 24, "Creating Subtitle Files" (listings 7 to 10): the five writers of Whisper given the two segments the chapter prints, compared with the chapter's own listings, and the real transcription of a reading.
import whisper
from whisper.utils import get_writer
book = {'text': ' Dinosaurs are a diverse group of reptiles of the clade dinosauria. They first appeared during the triassic period. Between 245 and 233.23 million years ago.', 'language': 'en',
        'segments': [{'id': 0, 'start': 0.0, 'end': 5.64, 'text': ' Dinosaurs are a diverse group of reptiles of the clade dinosauria. They first'}, {'id': 1, 'start': 5.64, 'end': 14.96, 'text': ' appeared during the triassic period. Between 245 and 233.23 million years ago.'}]}
BOOK = {'srt': '1\n00:00:00,000 --> 00:00:05,640\nDinosaurs are a diverse group of reptiles of the clade dinosauria. They first\n\n2\n00:00:05,640 --> 00:00:14,960\nappeared during the triassic period. Between 245 and 233.23 million years ago.\n',
        'vtt': 'WEBVTT\n\n00:00.000 --> 00:05.640\nDinosaurs are a diverse group of reptiles of the clade dinosauria. They first\n\n00:05.640 --> 00:14.960\nappeared during the triassic period. Between 245 and 233.23 million years ago.\n',
        'tsv': 'start\tend\ttext\n0\t5640\tDinosaurs are a diverse group of reptiles of the clade dinosauria. They first\n5640\t14960\tappeared during the triassic period. Between 245 and 233.23 million years ago.\n'}
for fmt in ('srt', 'vtt', 'tsv', 'txt', 'json'):
    w = get_writer(fmt, '.'); w(book, 'audio'); got = open('audio.' + fmt, encoding='utf-8').read()
    print('audio.%s  %4d bytes  equals the chapter\'s listing: %s' % (fmt, len(got), (got.strip() == BOOK[fmt].strip()) if fmt in BOOK else 'the chapter prints no listing'))
print(open('audio.txt').read().strip().splitlines())
print('json keys:', list(json.load(open('audio.json'))), '| the writers are functions of (result, audio_path[, options]):', 'WriteSRT' in dir(whisper.utils))
print('format the chapter does not name: ', err(lambda: get_writer('docx', '.')), '| "all":', type(get_writer('all', '.')).__name__)
print('folder that does not exist:', err(lambda: get_writer('srt', '/nonexistent/folder')(book, 'a')))
print('the audio name carries a folder and an extension: talks/hello.wav ->', (lambda: (get_writer('srt', '.')(book, 'talks/hello.wav'), sorted(f for f in os.listdir('.') if f.startswith('hello')))[1])())
book2 = dict(book); book2['segments'] = [dict(book['segments'][0], text=' a --> b')]; get_writer('srt', '.')(book2, 'arrow'); print('--> inside a text is written as:', open('arrow.srt').read().splitlines()[2])
book3 = dict(book); book3['segments'] = [dict(book['segments'][0], start=3601.5, end=3725.25)]; get_writer('vtt', '.')(book3, 'long'); get_writer('srt', '.')(book3, 'long'); print('times over an hour: vtt', open('long.vtt').read().splitlines()[2], '| srt', open('long.srt').read().splitlines()[1])
model = whisper.load_model('tiny'); h = fetch('gettysburg_shurtagal.mp3'); r = model.transcribe(h, language='en')
get_writer('srt', '.')(r, 'gettysburg'); get_writer('vtt', '.')(r, 'gettysburg')
srt = open('gettysburg.srt').read(); blocks = srt.strip().split('\n\n'); print('real reading: %d subtitle blocks; first block:' % len(blocks)); print(blocks[0])
ts = [s for seg in r['segments'] for s in (seg['start'], seg['end'])]; print('start and end times that are multiples of 0.02 s:', sum(1 for t in ts if abs(t / 0.02 - round(t / 0.02)) < 1e-6), 'of', len(ts))
rw = model.transcribe(h, language='en', word_timestamps=True); print('with word_timestamps=True the first segment holds', len(rw['segments'][0]['words']), 'words, the first:', {k: rw['segments'][0]['words'][0][k] for k in ('word', 'start', 'end')})
get_writer('srt', '.')(rw, 'words', {'max_line_width': 30, 'max_line_count': 2, 'highlight_words': False}); wb = open('words.srt').read().strip().split('\n\n'); print('with max_line_width=30, max_line_count=2: %d blocks (instead of %d); first block:' % (len(wb), len(blocks))); print(wb[0])
'''
CONVERT = HEAD + r'''# Chapter 24, "Creating Subtitle Files": SRT and VTT differ in three small ways; a converter in the standard library only, checked on the chapter's own listing 7 and 8, and a reader for TSV with the csv module as the chapter suggests.
import csv
SRT = '1\n00:00:00,000 --> 00:00:05,640\nDinosaurs are a diverse group of reptiles of the clade dinosauria. They first\n\n2\n00:00:05,640 --> 00:00:14,960\nappeared during the triassic period. Between 245 and 233.23 million years ago.\n'
VTT = 'WEBVTT\n\n00:00.000 --> 00:05.640\nDinosaurs are a diverse group of reptiles of the clade dinosauria. They first\n\n00:05.640 --> 00:14.960\nappeared during the triassic period. Between 245 and 233.23 million years ago.\n'
def parse_time(s):
    s = s.strip().replace(',', '.'); p = s.split(':'); sec = float(p[-1]); m = int(p[-2]); h = int(p[-3]) if len(p) == 3 else 0
    return h * 3600 + m * 60 + sec
def fmt_vtt(t):
    ms = round(t * 1000); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return ('%02d:' % h if h else '') + '%02d:%02d.%03d' % (m, s, ms)
def srt_to_vtt(srt):
    out = ['WEBVTT', '']
    for block in srt.strip().split('\n\n'):
        lines = block.split('\n'); a, b = lines[1].split(' --> ')
        out += [fmt_vtt(parse_time(a)) + ' --> ' + fmt_vtt(parse_time(b))] + lines[2:] + ['']
    return '\n'.join(out)
def vtt_cues(vtt):
    cues = []
    for block in vtt.strip().split('\n\n')[1:]:
        lines = block.split('\n'); a, b = lines[0].split(' --> '); cues.append((parse_time(a), parse_time(b), ' '.join(lines[1:])))
    return cues
conv = srt_to_vtt(SRT)
print('srt_to_vtt(listing 7) equals listing 8:', conv.strip() == VTT.strip())
print('cues read back from listing 8:', vtt_cues(VTT))
print('times over an hour:', fmt_vtt(3725.25), '| 59.9996 seconds ->', fmt_vtt(59.9996))
TSV = 'start\tend\ttext\n0\t5640\tDinosaurs are a diverse group of reptiles of the clade dinosauria. They first\n5640\t14960\tappeared during the triassic period. Between 245 and 233.23 million years ago.\n'
rows = list(csv.DictReader(TSV.splitlines(), delimiter='\t')); print('TSV with the csv module:', rows[1], '| milliseconds to seconds:', int(rows[1]['end']) / 1000)
print('the chapter\'s TSV listing separates columns with spaces; Whisper writes tabs:', '\t' in TSV, '| csv with the default comma gives', len(list(csv.reader(TSV.splitlines()))[1]), 'column')
import io as _io
print('SubRip block numbers start at 1 and end with a blank line; WebVTT has a WEBVTT header line and no numbers:', SRT.startswith('1\n'), VTT.startswith('WEBVTT'))
'''
OFFLINE = HEAD + r'''# Chapter 24, introduction and summary: "Both pyttsx3 and Whisper ... don't require an internet connection". The model is cached; the program then runs with every route to the internet pointed at an address that answers nothing, and once with no model file at all.
import whisper
say_to_wav('Hello. How are you doing?', 'hello.wav'); whisper.load_model('tiny')            # the first call downloads the model when it is absent
bad = dict(os.environ, HTTPS_PROXY='http://127.0.0.1:9', HTTP_PROXY='http://127.0.0.1:9', https_proxy='http://127.0.0.1:9', http_proxy='http://127.0.0.1:9', NO_PROXY='', no_proxy='')
code = "import whisper, pyttsx3\nm = whisper.load_model('tiny')\nprint(repr(m.transcribe('hello.wav')['text']))\ne = pyttsx3.init(); e.save_to_file('Hi', 'hi.wav'); e.runAndWait(); import os, time\nt = time.time()\nwhile not os.path.exists('hi.wav') and time.time() - t < 20: time.sleep(0.05)\nprint('pyttsx3 wrote', os.path.getsize('hi.wav'), 'bytes')"
r = subprocess.run([LATEST, '-W', 'ignore', '-c', code], capture_output=True, text=True, env=bad, timeout=300)
print('model cached, proxy variables pointing at 127.0.0.1:9 (nothing answers there): return code', r.returncode, '|', r.stdout.strip().splitlines(), '|', r.stderr.strip().splitlines()[-1:])
can_unshare = subprocess.run(['unshare', '-n', 'true'], capture_output=True).returncode == 0
if can_unshare:
    r = subprocess.run(['unshare', '-n', LATEST, '-W', 'ignore', '-c', code], capture_output=True, text=True, timeout=300); print('inside a network namespace with no interface (unshare -n): return code', r.returncode, '|', r.stdout.strip().splitlines(), '|', r.stderr.strip().splitlines()[-1:])
else: print('unshare -n is not allowed here: NOT EXECUTED (a network namespace with no interface)')
empty = tempfile.mkdtemp()
code2 = "import whisper\ntry:\n    whisper.load_model('tiny', download_root=%r)\nexcept BaseException as e:\n    print(type(e).__name__, str(e).splitlines()[0][:140])" % empty
r = subprocess.run([LATEST, '-W', 'ignore', '-c', code2], capture_output=True, text=True, env=bad, timeout=300); print('no model file in the folder and no route to the internet:', (r.stdout.strip().splitlines() or r.stderr.strip().splitlines())[-1:])
r = subprocess.run([LATEST, '-W', 'ignore', '-c', code2.replace("download_root=%r" % empty, "download_root=%r" % empty)], capture_output=True, text=True, timeout=300); print('the same with the internet (the file is downloaded into the empty folder):', (r.stdout.strip().splitlines() or ['loaded without an exception'])[-1:], [f for f in os.listdir(empty)], [os.path.getsize(os.path.join(empty, f)) for f in os.listdir(empty)])
'''
YTMETA = HEAD + r'''# Chapter 24, "Downloading Videos from Websites" (listing 14): the metadata of the video the chapter names, asked of YouTube WITHOUT downloading the video (skip_download), and the offline facts about yt-dlp's file names and sanitizing.
import yt_dlp
VIDEO = 'https://www.youtube.com/watch?v=kSrnLbioN6w'
options = {'quiet': True, 'no_warnings': True, 'skip_download': True}
with yt_dlp.YoutubeDL(options) as ydl:
    info = ydl.extract_info(VIDEO)
    json_info = ydl.sanitize_info(info)
    print('TITLE:', json_info['title'])
    print('KEYS:', list(json_info.keys())[:14], '... (%d keys)' % len(json_info))
    with open('metadata.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(json_info))
    print('duration', json_info['duration'], 'seconds | formats', len(json_info['formats']), '| metadata.json', os.path.getsize('metadata.json'), 'bytes')
    print('the chapter prose says ydl.sanitize(): exists?', hasattr(ydl, 'sanitize'), '| sanitize_info exists?', hasattr(ydl, 'sanitize_info'))
    book = ['id', 'title', 'formats', 'thumbnails', 'thumbnail', 'description', 'channel_id', 'channel_url', 'duration', 'view_count', 'average_rating', 'age_limit', 'webpage_url']
    print('keys printed by the chapter that this metadata has:', [k for k in book if k in json_info], '| missing:', [k for k in book if k not in json_info])
    print('the first 13 keys of today equal the chapter\'s first 13:', list(json_info.keys())[:13] == book)
    try: json.dumps(info); print('json.dumps(info) of the raw dictionary worked')
    except TypeError as e: print('json.dumps(info) of the raw dictionary raised TypeError:', str(e)[:80])
    fake = {'id': 'x', 'title': 'What? A: test | "quoted" <tag> / slash', 'ext': 'm4a', 'epoch': 0, 'extractor': 'youtube'}
    print('file name for a title with forbidden characters, with no outtmpl:', repr(ydl.prepare_filename(fake)))
with yt_dlp.YoutubeDL({'quiet': True, 'outtmpl': 'downloaded_content.%(ext)s'}) as y2:
    print('with outtmpl downloaded_content.%(ext)s:', y2.prepare_filename({'id': 'x', 'title': 't', 'ext': 'm4a', 'epoch': 0}))
print('yt-dlp version', yt_dlp.version.__version__, '| the video itself was NOT downloaded (not executed: a download from YouTube).')
'''
YTAUDIO = HEAD + r'''# Chapter 24, "Downloading Videos from Websites" (listings 12 and 13): the chapter's options dictionary, run on a public-domain LibriVox reading hosted by the Internet Archive instead of the YouTube video, then the glob of listing 13.
import yt_dlp
from pathlib import Path
URL = 'https://archive.org/details/gettysburg_shurtagal_librivox'
options = {'quiet': True, 'no_warnings': True, 'outtmpl': 'downloaded_content.%(ext)s', 'format': 'm4a/bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a'}]}
with yt_dlp.YoutubeDL(options) as ydl:
    rc = ydl.download([URL])
print('download returned', rc)
matching_filenames = list(Path().glob('downloaded_content.*'))
downloaded_filename = str(matching_filenames[0])
print('files:', sorted(str(p) for p in Path().glob('*')), '| listing 13 gives', repr(downloaded_filename))
p = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_name,sample_rate,channels:format=format_name,duration,bit_rate', '-of', 'json', downloaded_filename], capture_output=True, text=True); d = json.loads(p.stdout)
print('ffprobe: codec', d['streams'][0]['codec_name'], '| format', d['format']['format_name'], '| seconds', round(float(d['format']['duration']), 1), '| bit rate', d['format']['bit_rate'])
src = fetch('gettysburg_shurtagal.mp3'); p2 = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_name:format=duration', '-of', 'json', src], capture_output=True, text=True).stdout); print('the 64 kbit/s file on the archive is', p2['streams'][0]['codec_name'], 'of', round(float(p2['format']['duration']), 1), 's: the m4a is a re-encoding of it (m4a/bestaudio/best picked a format and FFmpegExtractAudio converted it)')
with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'skip_download': True}) as y: info = y.extract_info(URL)
print('formats offered by the archive item:', [(f['format_id'], f.get('ext'), f.get('abr')) for f in info['formats']], '| title:', info['title'], '| extractor:', info['extractor'])
print('download() with a string instead of a list:', err(lambda: yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}).download(URL)))
print('download() with an address that is nowhere:', err(lambda: yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}).download(['https://archive.org/details/this_item_does_not_exist_ch24'])))
import whisper
r = whisper.load_model('tiny').transcribe(downloaded_filename, language='en'); print('the downloaded m4a goes straight into Whisper tiny: %d words, WER of the first 50 words %.3f' % (len(r['text'].split()), wer(BLISS, ' '.join(r['text'].split()[:50]))))
'''
GUESS = HEAD + r'''# Chapter 24, "Adding Voice to Guess the Number" (listings 15 and 16): print() replaced by speak(), with the engine passed in so that the game can be tested without a voice, and the same game run with the real eSpeak NG writing every spoken line to a WAV file.
import random, pyttsx3
class Recorder:                                  # a stand-in engine for tests: it records what it was asked to say
    def __init__(self): self.said = []
    def say(self, t): self.said.append(t)
    def runAndWait(self): pass
def make_speak(engine):
    def speak(text):
        print(text)                              # to the screen ...
        engine.say(text); engine.runAndWait()    # ... and out loud
    return speak
def game(speak, guesses, secret):
    speak('I am thinking of a number between 1 and 20.')
    for n, g in enumerate(guesses, 1):
        if g < secret: speak('Your guess, %d, is too low.' % g)
        elif g > secret: speak('Your guess, %d, is too high.' % g)
        else: speak('Good job! You guessed my number in %d guesses!' % n); return n
rec = Recorder(); n = game(make_speak(rec), [10, 15, 12], 12)
print('with the Recorder stand-in, the game said:', rec.said, '| guesses:', n)
assert rec.said[1] == 'Your guess, 10, is too low.'
engine = pyttsx3.init(); spoken = []
class Writer:                                    # the real engine, but every line goes to a WAV file, because nothing can be played here
    def say(self, t): spoken.append(t); engine.save_to_file(t, 'line%02d.wav' % len(spoken))
    def runAndWait(self): engine.runAndWait(); wait_file('line%02d.wav' % len(spoken))
random.seed(24); secret = random.randint(1, 20); game(make_speak(Writer()), [5, 18, secret], secret)
print('secret', secret, '| WAV files:', [(f, wavinfo(f)['seconds']) for f in sorted(x for x in os.listdir('.') if x.startswith('line'))])
print('the chapter\'s own check that a guess is spoken as a number: "%d" of 42 ->' % 42, repr('Your guess, 42, is too low.'))
'''
BOTTLES = HEAD + r'''# Chapter 24, "Singing 99 Bottles of Beer": the lyrics as a function, the edge cases the chapter hints at (1 bottle, no more bottles), and the audio of a few verses and of the whole song measured with the real engine writing a WAV file.
import pyttsx3
def verse(n):
    def b(k): return 'No more bottles' if k == 0 else '1 bottle' if k == 1 else '%d bottles' % k
    nxt = b(n - 1).replace('No more', 'no more')
    return '%s of beer on the wall,\n%s of beer,\nTake one down, pass it around,\n%s of beer on the wall.' % (b(n), b(n), nxt[0].upper() + nxt[1:] if n - 1 == 0 else nxt)
print(verse(2)); print(); print(verse(1)); print()
song = '\n\n'.join(verse(n) for n in range(99, 0, -1))
print('whole song: %d verses, %d lines, %d words, %d characters' % (99, len(song.splitlines()) - 98, len(words(song)), len(song)))
engine = pyttsx3.init()
for n in (3, 99):
    t = '\n\n'.join(verse(k) for k in range(n, 0, -1)); t0 = time.time(); engine.save_to_file(t, 'song%d.wav' % n); engine.runAndWait(); wait_file('song%d.wav' % n, 600); dt = time.time() - t0
    i = wavinfo('song%d.wav' % n); print('%2d verses: %.1f s to make, %.1f s (%.1f min) of audio, %.1f MB' % (n, dt, i['seconds'], i['seconds'] / 60, os.path.getsize('song%d.wav' % n) / 1e6))
import whisper
m = whisper.load_model('tiny'); r = m.transcribe('song3.wav', language='en'); print('Whisper tiny hears the 3-verse WAV as:', repr(r['text'][:160]), '| WER', wer('\n\n'.join(verse(k) for k in range(3, 0, -1)), r['text']))
print('speak("No more bottles of beer on the wall") is the last line of the song: ', verse(1).splitlines()[-1])
'''
TRANSCRIBER = HEAD + r'''# Chapter 24, "YouTube Transcriber": the program the chapter asks for, written as a function that takes a list of addresses and a list of formats, run on two public-domain LibriVox readings hosted by the Internet Archive (no YouTube download: NOT EXECUTED).
import yt_dlp, whisper
from pathlib import Path
from whisper.utils import get_writer
def transcribe_urls(urls, formats=('srt',), model_name='tiny', folder='.'):
    model = whisper.load_model(model_name); done = []
    for k, url in enumerate(urls):
        stem = 'video%d' % k
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'outtmpl': stem + '.%(ext)s', 'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a'}]}) as ydl:
            ydl.download([url])
        audio = str(next(Path().glob(stem + '.*')))
        result = model.transcribe(audio, language='en')
        for f in formats: get_writer(f, folder)(result, stem)
        done.append((url, audio, result))
    return done
URLS = ['https://archive.org/details/gettysburg_shurtagal_librivox', 'https://archive.org/details/gettysburg_johng_librivox']
t0 = time.time(); done = transcribe_urls(URLS, formats=('srt', 'vtt', 'txt'))
print('two addresses, three formats, model tiny: %.1f s' % (time.time() - t0))
for url, audio, result in done:
    print(' ', url.rsplit('/', 1)[1], '->', audio, '| segments', len(result['segments']), '| words', len(result['text'].split()), '| WER against the Bliss copy (first 50 words) %.3f' % wer(BLISS, ' '.join(result['text'].split()[:50])))
print('files written:', sorted(f for f in os.listdir('.') if f.endswith(('.srt', '.vtt', '.txt'))))
print(open('video0.srt').read().split('\n\n')[0])
print('an address that cannot be downloaded stops the whole list: ', err(lambda: transcribe_urls(['https://archive.org/details/this_item_does_not_exist_ch24'])))
print('NOT EXECUTED: the same program against a YouTube address (the study asks YouTube for metadata only).')
'''
PROGRAMS = {
    'helloTts_v1_0_0.py': (HELLO, (), False),
    'voicesAndProperties_v1_0_0.py': (VOICES, (), False),
    'saveToFileAndRace_v1_0_0.py': (SAVE, (), True),
    'rateAndVolume_v1_0_0.py': (SWEEP, (), False),
    'whisperTranscribe_v1_0_0.py': (WHISPER, (), True),
    'audioFormatsAndFfmpeg_v1_0_0.py': (FORMATS, (), False),
    'languagesAndDetection_v1_0_0.py': (LANGS, (), False),
    'subtitleWriters_v1_0_0.py': (SUBS, (), True),
    'srtVttConverter_v1_0_0.py': (CONVERT, (), False),
    'offlineClaim_v1_0_0.py': (OFFLINE, (), False),
    'ytdlpMetadata_v1_0_0.py': (YTMETA, (), True),
    'ytdlpAudioFromArchive_v1_0_0.py': (YTAUDIO, (), True),
    'guessTheNumberWithVoice_v1_0_0.py': (GUESS, (), False),
    'ninetyNineBottles_v1_0_0.py': (BOTTLES, (), False),
    'youtubeTranscriber_v1_0_0.py': (TRANSCRIBER, (), True),
}
STAND_IN = {name: 'no sound card: the speech goes to WAV files, nothing is played; no display is used' for name in PROGRAMS}
FIXTURE_BASED = ['saveToFileAndRace_v1_0_0.py', 'whisperTranscribe_v1_0_0.py', 'subtitleWriters_v1_0_0.py', 'ytdlpMetadata_v1_0_0.py', 'ytdlpAudioFromArchive_v1_0_0.py', 'youtubeTranscriber_v1_0_0.py']

if __name__ == "__main__":
    # Usage: /home/claude/venv314_ch24_latest/bin/python sen0414_ch24_corpus_base_v1_0_0.py [--record] [name ...]   (exits 1 if a program does not exit 0)
    # --record also writes what every program printed to ch24-page/corpus_run_v1_0_0.json (single run; the lines of aplay/ALSA and the driver's "Audio saved to" lines are dropped)
    import os, subprocess, sys, json, datetime, platform
    args = sys.argv[1:]; record = "--record" in args; only = [a for a in args if a != "--record"]
    bad = 0; rec = {}
    for name, (code, needs, live) in PROGRAMS.items():
        if only and not any(o in name for o in only): continue
        env = dict(os.environ, CH24_LATEST=sys.executable)
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", code], capture_output=True, text=True, timeout=1800, stdin=subprocess.DEVNULL, env=env)
        bad += r.returncode != 0
        keep = lambda t: "\n".join(l for l in t.rstrip().splitlines() if "ALSA" not in l and "aplay" not in l and not l.startswith("Audio saved to") and not l.startswith("[download]"))
        rec[name] = {"exit code": r.returncode, "stdout": keep(r.stdout), "stderr lines": keep(r.stderr)[-1500:], "local stand-in": STAND_IN[name], "uses the network": live}
        print("=== %s (exit %d) [local stand-in: %s]" % (name, r.returncode, STAND_IN[name])); print(rec[name]["stdout"][:6000]); print(rec[name]["stderr lines"])
    print("%d programs, %d did not exit 0" % (len(rec), bad))
    if record:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch24-page", "corpus_run_v1_0_0.json")
        json.dump({"_version": __version__, "observed": datetime.date.today().isoformat(), "python": sys.version.split()[0], "platform": platform.platform(),
                   "_note": "SINGLE RUN of the programs of sen0414_ch24_corpus_base_v1_0_0.py with " + sys.executable + " (pyttsx3 2.99 with eSpeak NG 1.51, openai-whisper 20250625, yt-dlp 2026.8.19); no sound card: nothing was heard, the speech went to WAV files; Windows, macOS, a GPU and YouTube downloads were NOT EXECUTED.",
                   "programs": rec}, open(out, "w"), indent=1, ensure_ascii=False)
        print("->", out)
    sys.exit(1 if bad else 0)
