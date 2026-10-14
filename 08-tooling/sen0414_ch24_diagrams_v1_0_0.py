#!/usr/bin/env python3
"""SEN0414, chapter 24 (Text-to-Speech and Speech Recognition Engines, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the chapter (version 1.0.0).

A paragraph gets the diagram its narrative calls for - a workflow an activity diagram, the possible usages a use-case diagram, the life of a thing a state
diagram, an exchange between parties a sequence diagram, a topic and its parts a mind map - and the mapping from narrative pattern to diagram type lives in
the CME ontology (the narrative-to-diagram module of cme_standards_adoption_v1_3_0.ttl). Each entry names the concepts whose paragraphs it accompanies, the
narrative pattern, the passage it was read from, one sentence saying why the pattern fits, and the content in the element names the renderer expects. Every element
label is made of words that occur in the first paragraph and the definition of the accompanying concepts or their section; run_checks() measures that (the grounding
ratio, required to be 0.84 or more) besides the structural rules. The helper functions are those of sen0414_ch23_diagrams_v1_0_0.py, written again because a file of
another chapter is not edited; nodes_from_ttl() builds the node list from the chapter's RDODI v1_0_2 document and ABox.

Usage: python3 sen0414_ch24_diagrams_v1_0_0.py   (measures the grounding on the newest RDODI files of the chapter)
"""
__version__ = "1.0.0"
MIN_GROUNDING = 0.84

DIAGRAMS = [
    {
        "id": "SpeakingAndSavingASentence",
        "pattern": "Workflow",
        "title": "From a sentence to a WAV file with pyttsx3",
        "concepts": ["SayQueuesText", "RunAndWaitLoop", "WavFormat", "FirstCallRace"],
        "also_from": ["SpeakingText", "SavingWavFiles", "ExtensionIgnored"],
        "read_from": "chapter 24, Generating Speech and Saving Speech Audio to WAV Files: say() adds text to the queue, save_to_file() adds a file name and runAndWait() does the work",
        "why": "the passage is a sequence of steps with one test on whether the file is complete that leads on or back to waiting: a workflow",
        "data": {
            "nodes": [
                {"id": "init", "label": "Call pyttsx3.init() to start the engine"},
                {"id": "say", "label": "Call save_to_file() with the text and the file name"},
                {"id": "run", "label": "Call runAndWait() to process the queue"},
                {"id": "done", "label": "Is the file complete?", "kind": "decision"},
                {"id": "open", "label": "Open the WAV file with the wave module"},
                {"id": "wait", "label": "Wait until the size of the file is stable"},
            ],
            "flows": [["start", "init"], ["init", "say"], ["say", "run"], ["run", "done"], ["done", "open", "yes"], ["done", "wait", "no"], ["wait", "done"], ["open", "end"]],
        },
    },
    {
        "id": "FromAudioToSubtitles",
        "pattern": "Workflow",
        "title": "From an audio file to subtitle files with Whisper",
        "concepts": ["FfmpegRequired", "ResultStructure", "GetWriter", "SrtListing"],
        "also_from": ["Transcribing", "WhisperSetup", "SubtitleFormats", "WriterOptions"],
        "read_from": "chapter 24, Speech Recognition and Creating Subtitle Files: load_model() loads a model, transcribe() returns the result and get_writer() writes it as a subtitle file",
        "why": "the passage is a sequence of steps in which each call needs what the one before it returned: a workflow",
        "data": {
            "nodes": [
                {"id": "load", "label": "Call whisper.load_model() to load a model"},
                {"id": "ff", "label": "Is ffmpeg on the PATH?", "kind": "decision"},
                {"id": "err", "label": "The call raises FileNotFoundError"},
                {"id": "tr", "label": "Call transcribe() on the audio file"},
                {"id": "wr", "label": "Call get_writer() to write the subtitle file"},
            ],
            "flows": [["start", "load"], ["load", "ff"], ["ff", "tr", "yes"], ["ff", "err", "no"], ["tr", "wr"], ["wr", "end"], ["err", "end"]],
        },
    },
    {
        "id": "TheLoopOfTheTranscriber",
        "pattern": "Interaction",
        "title": "The transcriber loop: the script, yt-dlp, Whisper and the writers",
        "concepts": ["TranscribeLoop", "ThreeFormats", "FailureStopsList", "DownloadCall"],
        "also_from": ["YoutubeTranscriber", "ExtractAudioPostprocessor", "ResultStructure"],
        "read_from": "chapter 24, Practice Programs: for each address the program downloads the audio, transcribes it and writes the subtitle files",
        "why": "the passage is an exchange between the script, the downloader, the model and the writers in an order that matters - the audio exists before it is transcribed: an interaction",
        "data": {
            "participants": [
                {"id": "script", "label": "The script"},
                {"id": "ydl", "label": "yt-dlp"},
                {"id": "model", "label": "Whisper"},
                {"id": "wr", "label": "The writers"},
            ],
            "messages": [
                ["script", "ydl", "Calls download() with the address"],
                ["ydl", "script", "Returns the audio file", "reply"],
                ["script", "model", "Calls transcribe() on the audio"],
                ["model", "script", "Returns the result", "reply"],
                ["script", "wr", "Writes an SRT, a VTT and a TXT file"],
            ],
        },
    },
    {
        "id": "ThePinnedReleaseAndTheNewest",
        "pattern": "Interaction",
        "title": "A reader installing the release the book pins and the newest one",
        "concepts": ["Pyttsx3Package", "PinnedReleaseTruncates", "PinnedInstallFails", "EspeakDependency"],
        "also_from": ["EngineSetup", "WhisperSetup", "WhisperReleases"],
        "read_from": "chapter 24 and Appendix A: the book pins pyttsx3 and openai-whisper to releases and the newest releases behave differently",
        "why": "the passage is an exchange between the reader, the package index and the engine in which the pin and the newest release answer differently: an interaction",
        "data": {
            "participants": [
                {"id": "reader", "label": "The reader"},
                {"id": "pypi", "label": "PyPI"},
                {"id": "eng", "label": "The engine"},
            ],
            "messages": [
                ["reader", "pypi", "Installs the pinned release of pyttsx3"],
                ["pypi", "reader", "Delivers pyttsx3 2.98", "reply"],
                ["reader", "eng", "Saves the sentence Hello. How are you doing?"],
                ["eng", "reader", "Truncates the file", "reply"],
                ["reader", "pypi", "Installs pyttsx3 2.99"],
            ],
        },
    },
    {
        "id": "TheLifeOfAnUtterance",
        "pattern": "LifeCycle",
        "title": "The life of an utterance in the pyttsx3 queue",
        "concepts": ["SayQueuesText", "RunAndWaitLoop", "SetPropertyQueued", "NoSoundCard"],
        "also_from": ["SpeakingText", "VoicesAndProperties", "EmptyTextRefused"],
        "read_from": "chapter 24, Generating Speech: say() queues the text, runAndWait() starts the utterance and the events report that it started and finished",
        "why": "the passage follows one utterance through the states it is in and names the call or event that moves it from each state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "queued", "label": "The text is in the queue"},
                {"id": "started", "label": "The utterance has started"},
                {"id": "finished", "label": "The utterance has finished"},
            ],
            "initial": "queued",
            "final": ["finished"],
            "transitions": [
                ["queued", "started", "runAndWait() fires started-utterance"],
                ["started", "finished", "The engine fires finished-utterance"],
            ],
        },
    },
    {
        "id": "WhatYouCanDoWithTheEngines",
        "pattern": "SetOfUses",
        "title": "What a script can do with the engines of the chapter",
        "concepts": ["VoiceObjects", "RateDuration", "WavFormat", "ResultStructure", "SrtListing", "InfoDictionary", "DownloadCall"],
        "also_from": ["VolumeScale", "GetWriter", "TsvListing", "LanguagesAndDetection", "ModelWerTable"],
        "read_from": "chapter 24: list the voices, change the rate, save speech as a WAV file, transcribe audio, write subtitle files, read the metadata of a video and download audio",
        "why": "the chapter lists independent things a script can ask the libraries to do - speak, save, transcribe, subtitle, read, download - a set of uses, not a sequence",
        "data": {
            "system": "THEENGINES",
            "actors": [{"id": "script", "label": "A script"}],
            "usecases": [
                {"id": "voices", "label": "List the voices of the engine"},
                {"id": "rate", "label": "Change the rate of the speech"},
                {"id": "wav", "label": "Save speech as a WAV file"},
                {"id": "text", "label": "Transcribe audio with transcribe()"},
                {"id": "srt", "label": "Write a subtitle file"},
                {"id": "info", "label": "Read the metadata of a video"},
                {"id": "dl", "label": "Download audio with download()"},
            ],
            "links": [["script", "voices"], ["script", "rate"], ["script", "wav"], ["script", "text"], ["script", "srt"], ["script", "info"], ["script", "dl"]],
        },
    },
    {
        "id": "TextToSpeechAndSpeechRecognitionAtAGlance",
        "pattern": "TopicAndParts",
        "title": "Text-to-speech and speech recognition at a glance: six branches",
        "concepts": ["TextToSpeechEngine", "SavedSpeechAndRecognition", "SubtitleFiles", "DownloadingVideosFromWebsites", "PracticeProgramsAndAnswers", "EnvironmentAndEvidence"],
        "also_from": ["EngineSetup", "SpeakingText", "SavingWavFiles", "WhisperSetup", "ModelsAndTable", "SubtitleFormats", "WhisperWriters", "SpeechAccuracy", "YtDlpBasics",
                      "RightsAndEthics", "DriftOfDownloaders", "NinetyNineBottles", "Interpreters", "Platforms", "HonestyOfTheStudy", "RateDuration", "ModelFiles", "ModelWerTable",
                      "TimestampGrid", "YouTubeTerms", "NotExecutedList", "Pep594Modules", "PyttsxReleases", "VoiceObjects"],
        "read_from": "chapter 24, the opening of each of its main parts: the text-to-speech engine, saved speech and recognition, subtitle files, downloading, the practice programs and the evidence",
        "why": "the chapter classifies one topic, speech by program, by what each part is about and lists examples under each - a topic and its parts, with the one idea that holds for every part stated at the root",
        "data": {
            "root": "A script turns text into speech and speech into text",
            "branches": [
                {"label": "Text-to-speech engine",
                 "children": ["pyttsx3 queues text with say()", "runAndWait() processes the queue", "The rate and the volume are properties"]},
                {"label": "Saved speech and recognition",
                 "children": ["save_to_file() writes a WAV file", "Whisper needs ffmpeg", "The models differ in size and time"]},
                {"label": "Subtitle files",
                 "children": ["The writers make SRT, VTT and TSV files", "The times are on a grid", "The word error rate measures accuracy"]},
                {"label": "Downloading videos",
                 "children": ["yt-dlp downloads audio", "The terms of the site limit downloading", "Downloaders change with the releases"]},
                {"label": "Practice programs",
                 "children": ["The guessing game speaks", "The song has 99 verses", "The transcriber loop stops at a bad address"]},
                {"label": "Environment and evidence",
                 "children": ["The study ran Python 3.14.6", "Windows and macOS were not executed", "Every number is from a single run"]},
            ],
        },
    },
]
STOP = set("a an the of to in on and or is are be by it its for from with as at that this not yet no yes one every then".split())


def _labels(d):
    """every element label of a diagram, whatever its type"""
    x = d["data"]; out = []
    for n in x.get("nodes", []) + x.get("states", []) + x.get("actors", []) + x.get("usecases", []) + x.get("participants", []):
        out.append(n["label"] if isinstance(n, dict) else n)
    out += [f[2] for f in x.get("flows", []) + x.get("transitions", []) if len(f) > 2 and f[2]]
    out += [m[2] for m in x.get("messages", [])]
    for b in x.get("branches", []):
        out.append(b["label"]); out += b.get("children", [])
    if x.get("root"): out.append(x["root"])
    if x.get("system"): out.append(x["system"])
    return out


def grounding(d, nodes):
    """share of a diagram's content words that occur in the explanations of its concepts (and their section and subject)"""
    import re
    by = {n["id"]: n for n in nodes}
    ids = set(d["concepts"]) | set(d.get("also_from", []))
    for c in list(ids):
        n = by.get(c)
        while n and n.get("parent"):
            ids.add(n["parent"]); n = by.get(n["parent"])
    text = " ".join((by[c].get("body") or "") + " " + (by[c].get("definition") or "") + " " + by[c]["label"] for c in ids if c in by).lower()
    words = [w for w in re.findall(r"[a-z0-9][a-z0-9'-]*", " ".join(_labels(d)).lower()) if w not in STOP and len(w) > 1]
    hit = [w for w in words if w in text or w.rstrip("s") in text or (w + "s") in text]
    return len(hit), len(words), sorted(set(w for w in words if w not in hit))


def run_checks(nodes=None, mapping=None):
    """structural rules and, with the chapter's nodes, the grounding ratio; with the CME mapping, the pattern is known and its type is assigned"""
    bad = []
    ids = [d["id"] for d in DIAGRAMS]
    if len(ids) != len(set(ids)): bad.append("duplicate diagram ids")
    by = {n["id"]: n for n in nodes} if nodes else None
    for d in DIAGRAMS:
        for f in ("pattern", "title", "concepts", "read_from", "why", "data"):
            if not d.get(f): bad.append("%s: missing %s" % (d["id"], f))
        if by:
            for c in d["concepts"] + d.get("also_from", []):
                if c not in by: bad.append("%s: unknown concept %s" % (d["id"], c))
        if mapping:
            m = mapping.get(d["pattern"])
            if not m: bad.append("%s: pattern %s is not in the CME mapping" % (d["id"], d["pattern"]))
            else:
                d["type"] = m["types"][0]
        x = d["data"]
        if "flows" in x:
            nid = set(n["id"] for n in x["nodes"]) | {"start", "end"}
            for f in x["flows"]:
                if f[0] not in nid or f[1] not in nid: bad.append("%s: flow names an unknown node %r" % (d["id"], f))
            if not any(f[0] == "start" for f in x["flows"]) or not any(f[1] == "end" for f in x["flows"]): bad.append("%s: no start or no end" % d["id"])
            for n in x["nodes"]:
                if n.get("kind") == "decision" and len([f for f in x["flows"] if f[0] == n["id"]]) < 2: bad.append("%s: decision %s has fewer than two outgoing flows" % (d["id"], n["id"]))
        if "transitions" in x:
            sid = set(s["id"] if isinstance(s, dict) else s for s in x["states"])
            if x["initial"] not in sid: bad.append("%s: initial state unknown" % d["id"])
            for f in x.get("final", []):
                if f not in sid: bad.append("%s: final state unknown" % d["id"])
            for tr in x["transitions"]:
                if tr[0] not in sid or tr[1] not in sid or not tr[2]: bad.append("%s: transition %r unknown state or unlabelled" % (d["id"], tr))
        if "usecases" in x:
            aid = set(a["id"] for a in x["actors"]); uid = set(u["id"] for u in x["usecases"])
            for a, u in x["links"]:
                if a not in aid or u not in uid: bad.append("%s: link %r names an unknown actor or use case" % (d["id"], (a, u)))
            if uid - set(u for _, u in x["links"]): bad.append("%s: a use case has no actor" % d["id"])
        if "messages" in x:
            pid = set(p["id"] for p in x["participants"])
            for m in x["messages"]:
                if m[0] not in pid or m[1] not in pid or not m[2]: bad.append("%s: message %r unknown participant or empty" % (d["id"], m))
        if "branches" in x:
            if len(x["branches"]) < 2: bad.append("%s: a mind map needs at least two branches" % d["id"])
        for lab in _labels(d):
            if len(lab) > 72: bad.append("%s: label over 72 characters: %r" % (d["id"], lab))
        if nodes:
            h, n, miss = grounding(d, nodes)
            d["grounding"] = [h, n]
            if n and h / n < MIN_GROUNDING: bad.append("%s: grounding %d/%d below %.2f; words not in the concepts' explanations: %s" % (d["id"], h, n, MIN_GROUNDING, ", ".join(miss)))
    return bad


def nodes_from_ttl(root):
    """the chapter's nodes read from the v1_0_2 document and ABox: id = class name, parent by the section tree, body = first paragraph, definition = the ABox individual's definition"""
    import os, re
    from rdflib import Graph, Namespace, RDFS, URIRef
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    DOC = Namespace("http://example.org/rdodi/document-ontology#")
    CHX = "http://example.org/sen0414/ch24#"
    d = os.path.join(root, "03-materials", "ch24", "rdodi")
    g = Graph(); g.parse(os.path.join(d, "sen0414_ch24_document_v1_0_2.ttl"))
    a = Graph(); a.parse(os.path.join(d, "sen0414_ch24_domain_abox_v1_0_2.ttl"))
    nodes = {}
    for s in g.subjects(DOC.sectionTitle, None):
        if not str(s).startswith(CHX + "S_"): continue
        cid = str(s)[len(CHX) + 2:]
        body = str(g.value(s, SKOS.definition) or "")
        nodes[cid] = {"id": cid, "label": str(g.value(s, RDFS.label)), "body": body.split("\n\n")[0], "definition": "", "parent": None, "_s": s}
    for cid, n in nodes.items():
        for p in list(g.subjects(DOC.hasSection, n["_s"])) + list(g.objects(n["_s"], DOC.hasParentSection)):
            q = str(p)[len(CHX) + 2:]
            if q in nodes: n["parent"] = q
        x = a.value(URIRef(CHX + "X_" + cid), SKOS.definition)
        if x: n["definition"] = str(x)
        del n["_s"]
    return list(nodes.values())


if __name__ == "__main__":
    import sys, os
    here = os.path.dirname(os.path.abspath(__file__))
    nodes = nodes_from_ttl(os.path.dirname(here))
    bad = run_checks(nodes)
    for d in DIAGRAMS: print("%-26s %-12s grounding %s" % (d["id"], d["pattern"], d.get("grounding")))
    print("\n".join(bad) or "all checks pass: %d diagrams, nodes %d" % (len(DIAGRAMS), len(nodes))); sys.exit(1 if bad else 0)
