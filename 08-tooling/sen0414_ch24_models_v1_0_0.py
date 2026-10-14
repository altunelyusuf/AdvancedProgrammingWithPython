#!/usr/bin/env python3
"""Chapter 24 (Text-to-Speech and Speech Recognition Engines): measures what Table 24-1 of the chapter states for the Whisper models - the size of the model file, the memory,
the runtime for a 10-word sample of about 3 seconds and for an 1,800-word sample of about 15 minutes - on this machine, with openai-whisper 20250625 on the CPU, and adds the word
error rate of each model on speech whose text is known: the 1,800 words read aloud by pyttsx3 (eSpeak NG 1.51) and four human readings of the Gettysburg Address (LibriVox
recordings, public domain, from archive.org) whose text is the Bliss copy printed by Wikipedia.
What is fetched at run time and kept in a cache folder (CH24_CACHE, default /home/claude/ch24_cache), never in the repository: the text of "Alice's Adventures in Wonderland"
(Project Gutenberg #11), the Bliss copy text (Wikipedia), the four 64 kbit/s MP3 files (archive.org); each is checked against the SHA-256 the study recorded.
What it does: for each model name it downloads the model file as load_model() does (the time of that first load is recorded when the file was absent), loads it on the CPU, transcribes
the 10-word sample once and the long sample once, transcribes the four human readings once each, and records seconds, the peak resident memory of the process, and the word error rate.
Every number is a SINGLE RUN on this machine (2 virtual CPUs, no GPU, 7 GB of memory, Ubuntu 24.04) with nothing else running; it is a MEASUREMENT of the day, not a benchmark.
The model large-v3 needs about 6 GB for its weights as 32-bit floats on the CPU: it is downloaded and its size read, and its loading is attempted under an address-space limit of
6.5 GB in a child process; the outcome (loaded or MemoryError) is recorded and a transcription of it is NOT EXECUTED unless the load succeeds.
NOT EXECUTED and said so: any GPU (device cuda), the author's laptop, the author's recordings.
Usage: sen0414_ch24_models_v1_0_0.py [model ...]  (default: tiny base small medium turbo large-v3)   -> ch24-page/model_runtimes_v1_0_0.json (merged per model)
Run it with /home/claude/venv314_ch24_latest/bin/python."""
__version__ = "1.0.0"
import datetime, hashlib, json, os, platform, re, resource, subprocess, sys, tempfile, time, urllib.request, wave
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "08-tooling", "ch24-page", "model_runtimes_v1_0_0.json")
CACHE = os.environ.get("CH24_CACHE", "/home/claude/ch24_cache"); os.makedirs(CACHE, exist_ok=True)
UA = {"User-Agent": "SEN0414-research/1.0 (academic course; altunel.yusuf@gmail.com)"}
ASSETS = {  # name -> (url, sha256)
    "alice.txt": ("https://www.gutenberg.org/cache/epub/11/pg11.txt", "01b38ea4c710a84bc18d0bd41271a5a1a92b94e97b2812f4dece97d4a694725e"),
    "Gettysburg_Address_Lincoln_64kb.mp3": ("https://archive.org/download/gettysburg_shurtagal_librivox/Gettysburg_Address_Lincoln_64kb.mp3", "d9f40f965d68153694417cc739c7690021aa39ba80f22d1c3927aeaa97e29dc0"),
    "gettysburg_address_64kb.mp3": ("https://archive.org/download/gettysburg_johng_librivox/gettysburg_address_64kb.mp3", "195ca28fe8aa7036485fdc7be99509b8988cd19f54d30b75cc1fb26b8500cb82"),
    "lincoln_gettysburg_address_64kb.mp3": ("https://archive.org/download/gettysburg_address4_librivox/lincoln_gettysburg_address_64kb.mp3", "ff307fc2579e31e1ccae7304455a525922e11a87aaa14ac688764ab347eb5a72"),
    "gettysburg_address_lincoln_64kb.mp3": ("https://archive.org/download/gettysburg_address_librivox/gettysburg_address_lincoln_64kb.mp3", "59d825396d35e13601bbdc79a4867f7a55b09a6c65f1792657a2c67ddf666ead"),
}
READERS = {"Gettysburg_Address_Lincoln_64kb.mp3": "gettysburg_shurtagal_librivox", "gettysburg_address_64kb.mp3": "gettysburg_johng_librivox",
           "lincoln_gettysburg_address_64kb.mp3": "gettysburg_address4_librivox", "gettysburg_address_lincoln_64kb.mp3": "gettysburg_address_librivox"}
BLISS_SHA = "43097ca1fb311f9923363dd463880dd6ea5ffe4a6d66e30a0567e87c5e009d4b"
def sha(b): return hashlib.sha256(b).hexdigest()
def fetch(name):
    p = os.path.join(CACHE, name); url, want = ASSETS[name]
    if not os.path.exists(p):
        open(p + ".part", "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read()); os.replace(p + ".part", p)
    assert sha(open(p, "rb").read()) == want, "%s differs from the file the study recorded" % name
    return p
def bliss():
    import html
    p = os.path.join(CACHE, "gettysburg_bliss.txt")
    if not os.path.exists(p):
        s = urllib.request.urlopen(urllib.request.Request("https://en.wikipedia.org/wiki/Gettysburg_Address", headers=UA), timeout=120).read().decode("utf-8")
        m = re.search(r'<blockquote[^>]*class="quotebox-quote[^"]*"[^>]*>(.*?)</blockquote>', s, re.S)
        open(p, "w").write(re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))).strip())
    t = open(p).read(); assert sha(t.encode()) == BLISS_SHA, "the Bliss text differs from the one the study recorded"
    return t
def alice_words(n=1800):
    t = open(fetch("alice.txt"), encoding="utf-8-sig").read().replace("\r", "")
    i = t.index("Alice was beginning to get very tired"); body = re.sub(r"\s+", " ", t[i:].replace("_", ""))
    body = body.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    w = body.split(" ")[:n]
    s = " ".join(w)
    return s
def norm_words(t):
    t = t.lower().replace("\u2014", " ").replace("\u2013", " ").replace("-", " ").replace("\u2019", "'").replace("can not", "cannot")
    return re.sub(r"[^a-z0-9' ]+", " ", t).split()
def wer(ref, hyp):
    r, h = norm_words(ref), norm_words(hyp); prev = list(range(len(h) + 1))
    for i, a in enumerate(r, 1):
        cur = [i]
        for j, b in enumerate(h, 1): cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a != b)))
        prev = cur
    return round(prev[-1] / len(r), 4), len(r)
def wavdur(p):
    w = wave.open(p); return round(w.getnframes() / w.getframerate(), 2)
S3 = "The quick brown fox jumps over the yellow lazy dog."
def make_wav(text, path, rate):
    import pyttsx3
    e = pyttsx3.init(); e.setProperty("rate", rate); e.save_to_file(text, path); e.runAndWait()
    # the first runAndWait() of a process can return before the file exists (measured by sen0414_ch24_corpus_base_v1_0_0.py, program saveToFileRace): wait for it
    t0 = time.time()
    while not os.path.exists(path) and time.time() - t0 < 300: time.sleep(0.05)
def cpu_model():
    for l in open("/proc/cpuinfo"):
        if l.startswith("model name"): return l.split(":", 1)[1].strip()
def one(name):
    import torch, whisper
    rec = {"model": name}
    url = whisper._MODELS[name]; rec["file url"] = url; rec["sha256 in the url"] = url.split("/")[-2]
    root = os.path.join(os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache")), "whisper"); f = os.path.join(root, os.path.basename(url))
    rec["file present before the run"] = os.path.exists(f)
    if name == "large-v3":
        # the weights as 32-bit floats do not fit in the memory of this machine: download the file, then try to load it in a child under an address-space limit
        t0 = time.time()
        if not os.path.exists(f): whisper._download(url, root, False)
        rec["download seconds"] = round(time.time() - t0, 1); rec["file bytes"] = os.path.getsize(f)
        code = "import resource, sys, time; resource.setrlimit(resource.RLIMIT_AS, (6500000000, 6500000000)); import whisper\ntry:\n    t=time.time(); m = whisper.load_model('large-v3', device='cpu'); print('loaded', round(time.time()-t,1))\nexcept BaseException as e:\n    print(type(e).__name__, str(e)[:100])\n"
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", code], capture_output=True, text=True, timeout=1500)
        rec["load attempt under an address-space limit of 6.5 GB"] = (r.stdout.strip().splitlines() or [r.stderr.strip().splitlines()[-1:]])[-1] if (r.stdout.strip() or r.stderr.strip()) else "no output"
        rec["return code"] = r.returncode
        return rec
    t0 = time.time(); model = whisper.load_model(name, device="cpu"); rec["first load seconds (includes the download when the file was absent)"] = round(time.time() - t0, 1)
    rec["file bytes"] = os.path.getsize(f); rec["parameters"] = sum(p.numel() for p in model.parameters()); rec["multilingual"] = model.is_multilingual
    t0 = time.time(); model2 = whisper.load_model(name, device="cpu"); rec["second load seconds (file cached)"] = round(time.time() - t0, 1); del model2
    d = tempfile.mkdtemp()
    s3 = os.path.join(d, "s3.wav"); make_wav(S3, s3, 200)
    t0 = time.time(); r = model.transcribe(s3, language=None if model.is_multilingual else "en"); rec["10-word sample"] = {"audio seconds": wavdur(s3), "words in the text": len(S3.split()), "transcribe seconds": round(time.time() - t0, 1), "text": r["text"], "language": r["language"], "WER": wer(S3, r["text"])[0]}
    long_text = alice_words(1800); long_wav = os.path.join(CACHE, "alice_1800_rate120.wav")
    if not os.path.exists(long_wav):
        t0 = time.time(); make_wav(long_text, long_wav, 120); rec["pyttsx3 seconds to write the 1800-word file at rate 120"] = round(time.time() - t0, 1)
    rec["1800-word file"] = {"words": len(long_text.split()), "audio seconds": wavdur(long_wav), "sha256": sha(open(long_wav, "rb").read())[:16]}
    t0 = time.time(); r = model.transcribe(long_wav, language="en"); dt = time.time() - t0
    w, n = wer(long_text, r["text"]); rec["1800-word sample"] = {"transcribe seconds": round(dt, 1), "seconds per audio second": round(dt / wavdur(long_wav), 3), "segments": len(r["segments"]), "WER": w, "reference words": n, "words returned": len(norm_words(r["text"]))}
    ref = bliss(); rows = []
    for fn, ident in READERS.items():
        p = fetch(fn); dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.split("\n")[0] or 0)
        t0 = time.time(); r = model.transcribe(p, language="en"); dt = time.time() - t0
        rows.append({"reading": ident, "audio seconds": round(dur, 1), "transcribe seconds": round(dt, 1), "WER": wer(ref, r["text"])[0], "reference words": len(norm_words(ref)), "words returned": len(norm_words(r["text"]))})
    rec["four human readings of the Gettysburg Address"] = rows
    rec["peak resident memory of the process, MiB (ru_maxrss)"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
    return rec
if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--one":
        print("RESULT " + json.dumps(one(sys.argv[2]), ensure_ascii=False)); sys.exit(0)
    names = sys.argv[1:] or ["tiny", "base", "small", "medium", "turbo", "large-v3"]
    import importlib.metadata as md, torch
    data = json.load(open(OUT)) if os.path.exists(OUT) else {"results": {}}
    data.update({"_version": __version__, "observed": datetime.date.today().isoformat(),
                 "_note": "SINGLE RUNS of sen0414_ch24_models_v1_0_0.py on one machine; nothing else was meant to run during a run. Seconds are wall-clock; each model ran in its own process (so the peak memory is its own). WER is the word error rate against the known text after lower-casing and dropping punctuation. The 1800-word sample is Alice's Adventures in Wonderland read by pyttsx3 (eSpeak NG) at rate 120; the human readings are four LibriVox recordings of the Gettysburg Address (public domain). NOT EXECUTED: a GPU, the author's laptop, large-v3 transcription (memory).",
                 "machine": {"cpu": cpu_model(), "cpu count": os.cpu_count(), "torch threads": torch.get_num_threads(), "memory MiB": int(open("/proc/meminfo").readline().split()[1]) // 1024, "platform": platform.platform(),
                             "python": sys.version.split()[0], "torch": torch.__version__, "openai-whisper": md.version("openai-whisper"), "cuda available": torch.cuda.is_available()}})
    for n in names:
        r = subprocess.run([sys.executable, "-W", "ignore", os.path.abspath(__file__), "--one", n], capture_output=True, text=True, timeout=14400)
        line = [l for l in r.stdout.splitlines() if l.startswith("RESULT ")]
        data["results"][n] = json.loads(line[0][7:]) if line else {"model": n, "NOT EXECUTED or failed": "the child process ended with return code %d (%s); last stderr line: %s" % (r.returncode, "killed by SIGKILL, which on this machine is the memory-cgroup out-of-memory killer (dmesg: Memory cgroup out of memory, anon-rss about 6 GB)" if r.returncode == -9 else "not a kill", (r.stderr.strip().splitlines() or ["no output"])[-1][:200])}
        json.dump(data, open(OUT, "w"), indent=1, ensure_ascii=False); print(n, "done", flush=True)
    print("->", OUT)
