#!/usr/bin/env python3
"""Chapter 24 (Text-to-Speech and Speech Recognition Engines): runs one program, what pyttsx3 (with the real eSpeak NG 1.51 on the machine), yt-dlp and Whisper (the tiny model on the CPU)
do and what the standard library offers for audio, under every installed 3.14 patch release (3.14.0 to 3.14.6) and, for comparison, under 3.15 (a beta), 3.13, 3.12 and 3.11, with
the newest packages the index offers for each interpreter (`uv run --no-project --with pyttsx3 --with yt-dlp`, and a second run that adds `--with openai-whisper` and the CPU wheels
of PyTorch), and records what each printed. It then runs smaller programs over the releases of the packages themselves: all 22 releases of pyttsx3 (on 3.14.6), all 13 releases of
openai-whisper (on 3.12, because the old source distributions need an older setuptools, which the run supplies), and the last stable release of each year of yt-dlp with the newest
(on 3.14.6), because the book pins pyttsx3 2.98 and openai-whisper 20231117 (Appendix A) and yt-dlp is always installed at its newest. A release that cannot run is recorded as
NOT EXECUTED with the last lines uv or Python printed.
The operating system is Ubuntu 24.04; eSpeak NG 1.51, espeak 1.48.15 and ffmpeg 6.1.1 come from apt; there is no sound card and no GPU (the CPU wheels of PyTorch are used), and the
speech is written to WAV files and never played. Nothing leaves the machine except the downloads of packages and of the 72 MB tiny model (cached after the first run).
Usage: sen0414_ch24_interpreters_v1_0_0.py   (needs uv on PATH)   -> ch24-page/interpreter_record_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, json, os, re, subprocess, sys, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "08-tooling", "ch24-page", "interpreter_record_v1_0_0.json")
COMMON = r"""
import sys, os, io, json, re, time, wave, array, tempfile, warnings, importlib, importlib.metadata as md
res = {}
def w(f):
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter('always')
        try: v = f()
        except BaseException as e: v = type(e).__name__ + ': ' + (str(e).splitlines() or [''])[0][:110]
    return [v, sorted({x.category.__name__ for x in seen if x.category.__name__ != 'ResourceWarning'})]
def ver(n):
    try: return md.version(n)
    except md.PackageNotFoundError: return None
res['series'] = sys.version.split()[0].rsplit('.', 1)[0] + '.x'
os.chdir(tempfile.mkdtemp())
def wavfile(p):
    x = wave.open(p); n = x.getnframes(); a = array.array('h', x.readframes(n)); return [x.getnchannels(), x.getsampwidth(), x.getframerate(), n, max(abs(v) for v in a)]
def wait(p, limit=60, quiet=0.4):
    # the file exists and has stopped growing (runAndWait() of pyttsx3 can return while the WAV is still being written)
    t = time.time(); last = -1; since = None
    while time.time() - t < limit:
        if os.path.exists(p):
            n = os.path.getsize(p)
            if n == last and n > 44:
                if since is not None and time.time() - since >= quiet: return
            else: since = time.time(); last = n
        time.sleep(0.05)
"""
TTSPROG = COMMON + r"""
res['versions'] = {n: ver(n) for n in ('pyttsx3', 'yt-dlp')}
res['modules removed by PEP 594 that can be imported (aifc, audioop, sunau, chunk, sndhdr, wave)'] = {m: (lambda m: (importlib.import_module(m), True)[1] if True else None)(m) if importlib.util.find_spec(m) else False for m in ('aifc', 'audioop', 'sunau', 'chunk', 'sndhdr', 'wave')}
res['importing aifc'] = w(lambda: importlib.import_module('aifc').__name__)
import pyttsx3
res['pyttsx3.init()'] = w(lambda: type(pyttsx3.init()).__name__)
e = pyttsx3.init()
res['driver class'] = w(lambda: type(e.proxy._driver).__name__)
res['volume, rate, voice id'] = w(lambda: [e.getProperty('volume'), e.getProperty('rate'), e.getProperty('voice')])
res['voices: count, type, first name, gender, age, languages'] = w(lambda: (lambda v: [len(v), type(v[0]).__name__, v[0].name, v[0].gender, v[0].age, v[0].languages])(e.getProperty('voices')))
res['say() of an empty text returns'] = w(lambda: e.say(''))
ev = []
for t in ('started-utterance', 'started-word', 'finished-utterance', 'error'): e.connect(t, lambda t=t, **k: ev.append(t))
e.save_to_file('Hello. How are you doing?', 'hello.wav'); e.runAndWait(); wait('hello.wav')
res['save_to_file: channels, sample width, rate, frames, peak'] = w(lambda: wavfile('hello.wav'))
res['events of that save_to_file, in order, words counted once'] = w(lambda: [x for i, x in enumerate(ev) if x != 'started-word' or ev[i - 1] != 'started-word'])
res['file name with .mp3 starts with'] = w(lambda: (e.save_to_file('Hello', 'a.mp3'), e.runAndWait(), wait('a.mp3'), open('a.mp3', 'rb').read(4))[3])
import yt_dlp
with yt_dlp.YoutubeDL({'quiet': True}) as y:
    res['yt-dlp: sanitize_info, sanitize exist'] = [hasattr(y, 'sanitize_info'), hasattr(y, 'sanitize')]
    res['yt-dlp: file name of a title with ? : | " / < >'] = w(lambda: y.prepare_filename({'id': 'x', 'title': 'What? A: B | "C" / <D>', 'ext': 'm4a', 'epoch': 0, 'extractor': 'youtube'}))
    res['yt-dlp: download() takes a string (the address of a nowhere)'] = w(lambda: type(y).download.__doc__ is None or True)
res['yt-dlp: FFmpegExtractAudio post-processor exists'] = w(lambda: hasattr(importlib.import_module('yt_dlp.postprocessor'), 'FFmpegExtractAudioPP'))
print(json.dumps(res, sort_keys=True, default=repr))
"""
WHPROG = COMMON + r"""
import whisper
res['versions'] = {n: ver(n) for n in ('openai-whisper', 'torch', 'numpy', 'numba', 'pyttsx3')}
res['torch: cuda available, threads'] = w(lambda: [__import__('torch').cuda.is_available(), __import__('torch').get_num_threads()])
res['available_models'] = w(lambda: whisper.available_models())
import pyttsx3
e = pyttsx3.init(); e.save_to_file('The quick brown fox jumps over the yellow lazy dog.', 'fox.wav'); e.runAndWait(); wait('fox.wav')
m = whisper.load_model('tiny')
res['load_model: parameters, default of name'] = w(lambda: str(__import__('inspect').signature(whisper.load_model)))
res['model: dims n_mels, multilingual, parameters'] = w(lambda: [m.dims.n_mels, m.is_multilingual, sum(p.numel() for p in m.parameters())])
res['transcribe of fox.wav: text, language'] = w(lambda: (lambda r: [r['text'], r['language']])(m.transcribe('fox.wav')))
r = m.transcribe('fox.wav')
res['result keys, first segment keys'] = w(lambda: [list(r), list(r['segments'][0])])
res['first segment start, end'] = w(lambda: [r['segments'][0]['start'], r['segments'][0]['end']])
from whisper.utils import get_writer
res['get_writer(srt) call signature'] = w(lambda: str(__import__('inspect').signature(get_writer('srt', '.').__call__)))
res['the chapter\'s write_function(result, "audio") works; audio.srt'] = w(lambda: (get_writer('srt', '.')(r, 'audio'), open('audio.srt').read())[1])
res['the chapter\'s write_function(result, "audio") for vtt, tsv, txt, json: files'] = w(lambda: [(get_writer(f, '.')(r, 'audio'), os.path.exists('audio.' + f))[1] for f in ('vtt', 'tsv', 'txt', 'json')])
res['language="English" accepted'] = w(lambda: m.transcribe('fox.wav', language='English')['text'])
res['language="Klingon"'] = w(lambda: m.transcribe('fox.wav', language='Klingon'))
res['languages known to the tokenizer'] = w(lambda: len(whisper.tokenizer.LANGUAGES))
res['whisper.utils.get_writer formats'] = w(lambda: sorted(re.findall(r"'(\w+)'", __import__('inspect').getsource(get_writer))) )
res['cli default of --model'] = w(lambda: re.findall(r'"--model".*?default=([^,\)]+)', __import__('inspect').getsource(whisper.transcribe.cli), re.S)[:1])
res['cli default of --language'] = w(lambda: re.findall(r'"--language".*?default=([^,\)]+)', __import__('inspect').getsource(whisper.transcribe.cli), re.S)[:1])
print(json.dumps(res, sort_keys=True, default=repr))
"""
PTPROG = COMMON + r"""
res['pyttsx3'] = ver('pyttsx3'); res['python'] = sys.version.split()[0]
import pyttsx3
res['init'] = w(lambda: type(pyttsx3.init()).__name__)
e = pyttsx3.init()
res['module-level speak() exists'] = hasattr(pyttsx3, 'speak')
res['voices: count and first'] = w(lambda: (lambda v: [len(v), v[0].name, v[0].languages])(e.getProperty('voices')))
res['volume, rate'] = w(lambda: [e.getProperty('volume'), e.getProperty('rate')])
res['say(empty)'] = w(lambda: e.say(''))
res['save_to_file then runAndWait: wav'] = w(lambda: (e.save_to_file('Hello. How are you doing?', 'hello.wav'), e.runAndWait(), wait('hello.wav'), wavfile('hello.wav'))[3])
res['engine has connect, stop, isBusy, startLoop, iterate'] = [hasattr(e, n) for n in ('connect', 'stop', 'isBusy', 'startLoop', 'iterate')]
res['drivers in the package'] = sorted(f[:-3] for f in os.listdir(os.path.join(os.path.dirname(pyttsx3.__file__), 'drivers')) if f.endswith('.py') and not f.startswith('_'))
res['requires'] = ver('pyttsx3') and sorted(re.split(r'[;>=<! ]', r)[0] for r in (md.requires('pyttsx3') or []))
print(json.dumps(res, sort_keys=True, default=repr))
"""
WPROG = COMMON + r"""
import inspect, whisper
res['openai-whisper'] = ver('openai-whisper'); res['python'] = sys.version.split()[0]; res['torch'] = ver('torch'); res['numpy'] = ver('numpy')
res['available_models'] = w(lambda: len(whisper.available_models()))
res['load_model signature'] = w(lambda: str(inspect.signature(whisper.load_model)))
res['transcribe: number of parameters'] = w(lambda: len(inspect.signature(whisper.transcribe).parameters))
res['transcribe has word_timestamps, clip_timestamps, hallucination_silence_threshold, carry_initial_prompt'] = w(lambda: [n in inspect.signature(whisper.transcribe).parameters for n in ('word_timestamps', 'clip_timestamps', 'hallucination_silence_threshold', 'carry_initial_prompt')])
from whisper.utils import get_writer
res['writer call signature'] = w(lambda: str(inspect.signature(get_writer('srt', '.').__call__)))
src = inspect.getsource(whisper.transcribe.cli) if hasattr(whisper.transcribe, 'cli') else ''
res['cli default of --model'] = w(lambda: re.findall(r'"--model".*?default=([^,\)]+)', src, re.S)[:1])
res['languages in the tokenizer'] = w(lambda: len(whisper.tokenizer.LANGUAGES))
import pyttsx3
e = pyttsx3.init(); e.save_to_file('The quick brown fox jumps over the yellow lazy dog.', 'fox.wav'); e.runAndWait(); wait('fox.wav')
m = whisper.load_model('tiny')
res['tiny: parameters'] = w(lambda: sum(p.numel() for p in m.parameters()))
res['tiny transcribes fox.wav as'] = w(lambda: (lambda r: [r['text'], list(r)])(m.transcribe('fox.wav')))
res['the chapter\'s two lines write_function(result, "audio")'] = w(lambda: (get_writer('srt', '.')(m.transcribe('fox.wav'), 'audio'), os.path.exists('audio.srt'))[1])
print(json.dumps(res, sort_keys=True, default=repr))
"""
YPROG = COMMON + r"""
import yt_dlp
res['yt-dlp'] = ver('yt-dlp'); res['python'] = sys.version.split()[0]
with yt_dlp.YoutubeDL({'quiet': True}) as y:
    res['sanitize_info, sanitize exist'] = [hasattr(y, 'sanitize_info'), hasattr(y, 'sanitize')]
    res['sanitize_info of a dict with a function inside'] = w(lambda: json.dumps(y.sanitize_info({'id': 'x', 'f': (lambda: 1), 'n': 1})))
    res['file name of a title with ? : | " / < >'] = w(lambda: y.prepare_filename({'id': 'x', 'title': 'What? A: B | "C" / <D>', 'ext': 'm4a', 'epoch': 0, 'extractor': 'youtube'}))
    res['file name with outtmpl downloaded_content.%(ext)s'] = w(lambda: (y.params.update({'outtmpl': {'default': 'downloaded_content.%(ext)s'}}), y.prepare_filename({'id': 'x', 'title': 't', 'ext': 'm4a', 'epoch': 0}))[1])
res['FFmpegExtractAudio exists'] = w(lambda: hasattr(importlib.import_module('yt_dlp.postprocessor'), 'FFmpegExtractAudioPP'))
res['number of extractors'] = w(lambda: len(importlib.import_module('yt_dlp.extractor').gen_extractor_classes()))
res['archive.org extractor'] = w(lambda: any(c.__name__ == 'ArchiveOrgIE' for c in importlib.import_module('yt_dlp.extractor').gen_extractor_classes()))
print(json.dumps(res, sort_keys=True, default=repr))
"""
INTERPRETERS = ["3.11", "3.12", "3.13", "3.14.0", "3.14.1", "3.14.2", "3.14.3", "3.14.4", "3.14.5", "3.14.6", "3.15"]
WH = ["--extra-index-url", "https://download.pytorch.org/whl/cpu", "--index-strategy", "unsafe-best-match"]
def uv(py, withs, code, timeout=1500, extra=()):
    env = dict(os.environ); env.pop("PYTHONPATH", None); env["TZ"] = "Europe/Istanbul"; env.pop("DISPLAY", None)
    cmd = ["uv", "run", "--no-project", "--python", py] + list(extra)
    for x in withs: cmd += ["--with", x]
    out = open(os.path.join(os.environ.get("TMPDIR", "/tmp"), "ch24_interp.out"), "w+"); err = open(os.path.join(os.environ.get("TMPDIR", "/tmp"), "ch24_interp.err"), "w+")
    try: r = subprocess.run(cmd + ["python", "-I", "-W", "ignore", "-c", code], stdout=out, stderr=err, env=env, timeout=timeout, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired: return {"NOT EXECUTED or failed": "timed out after %d s" % timeout}
    out.seek(0); err.seek(0); so = out.read(); se = err.read()
    if extra: subprocess.run(["uv", "cache", "clean"], capture_output=True)   # the PyTorch wheels fill the disk of this machine otherwise (12 GB for the 11 interpreters)
    lines = [l for l in so.strip().splitlines() if l.startswith("{")]
    if r.returncode != 0 or not lines:
        e = [l for l in se.strip().splitlines() if l.strip() and "ALSA" not in l and "UV_NATIVE_TLS" not in l]
        why = "exit code %d%s" % (r.returncode, " (SIGSEGV: the program was killed by a segmentation fault)" if r.returncode in (139, -11) else "")
        return {"NOT EXECUTED or failed": (why + " | " + " | ".join(e[-3:]))[:520]}
    return json.loads(lines[-1])
def compare(results, skip=("series", "versions", "python", "pyttsx3", "openai-whisper", "yt-dlp", "torch", "numpy")):
    keys = sorted({k for r in results.values() for k in r if k not in skip})
    differ = {}
    for k in keys:
        vals = {}
        for v, r in results.items():
            if "NOT EXECUTED or failed" in r: continue
            vals.setdefault(json.dumps(r.get(k), sort_keys=True), []).append(v)
        if len(vals) > 1: differ[k] = [[json.loads(a), b] for a, b in vals.items()]
    return keys, differ
def pypi_versions(name):
    j = json.load(urllib.request.urlopen("https://pypi.org/pypi/%s/json" % name, timeout=60)); rel = j["releases"]
    def ver(v): return [int(x) for x in re.findall(r"\d+", v)[:4]]
    return sorted((v for v in rel if rel[v] and not any(f.get("yanked") for f in rel[v])), key=ver), {v: rel[v][0]["upload_time"][:10] for v in rel if rel[v]}
if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    data = json.load(open(OUT)) if os.path.exists(OUT) else {}
    if step in ("all", "tts"):
        tts = {}
        for py in INTERPRETERS:
            v = subprocess.run(["uv", "run", "--no-project", "--python", py, "python", "-c", "import sys; print(sys.version.split()[0])"], capture_output=True, text=True).stdout.strip()
            tts[v or py] = uv(py, ["pyttsx3", "yt-dlp"], TTSPROG); print("tts", py, v, "ok" if "NOT EXECUTED or failed" not in tts[v or py] else tts[v or py]["NOT EXECUTED or failed"], flush=True)
        k, d = compare(tts); data.update({"interpreters": list(tts), "results": tts, "items compared": len(k), "differ": d})
        json.dump(data, open(OUT, "w"), indent=1, ensure_ascii=False)
    if step in ("all", "whisper"):
        wh = {}
        for py in INTERPRETERS:
            v = subprocess.run(["uv", "run", "--no-project", "--python", py, "python", "-c", "import sys; print(sys.version.split()[0])"], capture_output=True, text=True).stdout.strip()
            wh[v or py] = uv(py, ["pyttsx3", "openai-whisper", "yt-dlp"], WHPROG, extra=WH); print("whisper", py, v, "ok" if "NOT EXECUTED or failed" not in wh[v or py] else wh[v or py]["NOT EXECUTED or failed"], flush=True)
        k, d = compare(wh); data.update({"whisper interpreters": list(wh), "whisper results": wh, "whisper items compared": len(k), "whisper differ": d})
        json.dump(data, open(OUT, "w"), indent=1, ensure_ascii=False)
    if step in ("all", "pyttsx3"):
        vs, dates = pypi_versions("pyttsx3"); pt = {}
        for v in vs:
            pt[v] = uv("3.14.6", ["pyttsx3==" + v], PTPROG); print("pyttsx3", v, "ok" if "NOT EXECUTED or failed" not in pt[v] else pt[v]["NOT EXECUTED or failed"], flush=True)
        k, d = compare(pt); data.update({"pyttsx3 releases": pt, "pyttsx3 release dates": dates, "pyttsx3 items compared": len(k), "pyttsx3 differ": d})
        json.dump(data, open(OUT, "w"), indent=1, ensure_ascii=False)
    if step in ("all", "whisper-releases"):
        vs, dates = pypi_versions("openai-whisper"); wr = {}
        for v in vs:
            wr[v] = uv("3.12", ["openai-whisper==" + v, "pyttsx3", "setuptools<81", "wheel"], WPROG, extra=WH + ["--no-build-isolation-package", "openai-whisper"]); print("openai-whisper", v, "ok" if "NOT EXECUTED or failed" not in wr[v] else wr[v]["NOT EXECUTED or failed"], flush=True)
        k, d = compare(wr); data.update({"openai-whisper releases": wr, "openai-whisper release dates": dates, "openai-whisper items compared": len(k), "openai-whisper differ": d})
        json.dump(data, open(OUT, "w"), indent=1, ensure_ascii=False)
    if step in ("all", "yt-dlp"):
        vs, dates = pypi_versions("yt-dlp"); stable = [v for v in vs if re.fullmatch(r"\d{4}\.\d{1,2}\.\d{1,2}", v)]
        pick = []
        for y in range(2021, 2027):
            ys = [v for v in stable if v.startswith(str(y) + ".")]
            if ys: pick.append(ys[-1])
        yt = {}
        for v in pick:
            yt[v] = uv("3.14.6", ["yt-dlp==" + v], YPROG); print("yt-dlp", v, "ok" if "NOT EXECUTED or failed" not in yt[v] else yt[v]["NOT EXECUTED or failed"], flush=True)
        k, d = compare(yt); data.update({"yt-dlp releases": yt, "yt-dlp release dates": {v: dates[v] for v in pick}, "yt-dlp stable releases": len(stable), "yt-dlp items compared": len(k), "yt-dlp differ": d})
    data.update({"_version": "1.0.0", "observed": datetime.date.today().isoformat(),
                 "_note": "Recorded by sen0414_ch24_interpreters_v1_0_0.py: one program (pyttsx3 with the real eSpeak NG, the wave module, yt-dlp offline, Whisper tiny on the CPU) under every installed Python 3.14 patch release and the 3.15 beta, 3.13, 3.12 and 3.11, with the newest packages for each; the same checks across all releases of pyttsx3 and openai-whisper and the last stable release of each year of yt-dlp. A result is what the program printed on the day on this machine (Ubuntu 24.04, Europe/Istanbul, no sound card, no GPU); a row that cannot run says NOT EXECUTED or failed and why. Windows and macOS were not executed.",
                 "tts program": TTSPROG, "whisper program": WHPROG, "pyttsx3 program": PTPROG, "openai-whisper program": WPROG, "yt-dlp program": YPROG})
    json.dump(data, open(OUT, "w"), indent=1, ensure_ascii=False)
    print("recorded:", {k: (len(v) if isinstance(v, (dict, list)) else v) for k, v in data.items() if k.endswith(("releases", "interpreters", "results", "compared"))})
    for k in ("differ", "whisper differ", "pyttsx3 differ", "openai-whisper differ", "yt-dlp differ"):
        if k in data: print(k, sorted(data[k]))
