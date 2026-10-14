"""SEN0414 chapter 24 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Six stories for text-to-speech and speech recognition,
written fresh for this chapter from Wikipedia pages opened on 2026-10-14 (the HTTP status each link answered to a plain GET on that day is in LINK_STATUS, and
`python3 sen0414_ch24_stories_v1_0_0.py links` asks again):

* Voder1939 - Homer Dudley's keyboard-operated voice synthesizer, the Voder, was exhibited at the 1939 New York World's Fair.
* Audrey1952 - Bell Labs researchers Stephen Balashek, R. Biddulph and K. H. Davis built Audrey for single-speaker digit recognition in 1952.
* DaisyBell1961 - an IBM 7090 at Bell Labs was programmed to sing "Daisy Bell" in 1961; Arthur C. Clarke saw it in 1962 and HAL 9000 sings it in 2001.
* ESpeak1995 - Jonathan Duddington released the Speak synthesizer for RISC OS in 1995; Speak 1.05 was released under the GPLv2 on 17 February 2006.
* SubRip2000 - SubRip, by Brain and Zuggy, was released on 3 March 2000 and gave the .srt format its name.
* Whisper2022 - OpenAI first released Whisper as open-source software in September 2022, trained on 680,000 hours of labelled audio.

Photograph: see ch24-page/stories_img_v1_0_0.json. The requests to Wikimedia returned 429 on the days this study asked, so no photograph is used and nothing is claimed about licences.
Every sentence that says "In this study" was run on 2026-10-14 under Python 3.14.6 in /home/claude/venv314_ch24_latest (pyttsx3 2.99 with eSpeak NG 1.51, openai-whisper 20250625), with no sound card:
nothing was heard, the speech went to WAV files.
Usage: import STORIES; run the file for self-checks, or with the argument links to ask every link again.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "Voder1939",
        "title": "A keyboard-operated voice synthesizer was shown at the 1939 World's Fair",
        "when": "1939",
        "who": "Homer Dudley of Bell Labs, who developed the Voder after his work on the vocoder",
        "where": "The 1939 New York World's Fair",
        "link": "https://en.wikipedia.org/wiki/Speech_synthesis",
        "concepts": ["VoiceObjects", "PersistentVoice"],
        "story": ("Wikipedia's article on speech synthesis says that Homer Dudley developed, after his work on the vocoder, a keyboard-operated voice synthesizer called the Voder (Voice Demonstrator), which he exhibited at the 1939 New York World's Fair. "
                  "A person played it with keys; nothing in it read text. "
                  "In this study pyttsx3 2.99 with eSpeak NG 1.51 listed 131 voices, each a Voice object with a name, a gender, an age and a list of languages, and all 131 said Male with the age None, so a voice is a language and a set of rules, not a person."),
        "lesson": "A voice list names languages, not speakers",
        "source": ("Wikipedia, 'Speech synthesis' (Homer Dudley, the Voder, the 1939 New York World's Fair), read 2026-10-14; "
                   "this study's leaves VoiceObjects and PersistentVoice."),
    },
    {
        "id": "Audrey1952",
        "title": "Audrey recognised the digits of one speaker in 1952",
        "when": "1952",
        "who": "Bell Labs researchers Stephen Balashek, R. Biddulph and K. H. Davis",
        "where": "Bell Labs; the system located the formants in the power spectrum of each utterance",
        "link": "https://en.wikipedia.org/wiki/Speech_recognition",
        "concepts": ["LanguagesAndDetection", "ModelWerTable"],
        "story": ("Wikipedia's article on speech recognition says that in 1952 Bell Labs researchers Stephen Balashek, R. Biddulph and K. H. Davis built Audrey for single-speaker digit recognition, and that the system located the formants in the power spectrum of each utterance. "
                  "It knew one speaker and the ten digits. "
                  "In this study Whisper tiny named the language of the same eSpeak sentence correctly for 3 of 6 languages and base for 4 of 6, and heard the ten-word fox sentence with a word error rate of 0.3 (tiny), 0.2 (base) and 0.1 (small)."),
        "lesson": "Recognition grew from ten digits to a hundred languages",
        "source": ("Wikipedia, 'Speech recognition' (Audrey, 1952; Balashek, Biddulph and Davis), read 2026-10-14; "
                   "this study's leaves LanguagesAndDetection and ModelWerTable."),
    },
    {
        "id": "DaisyBell1961",
        "title": "A computer sang Daisy Bell in 1961",
        "when": "1961",
        "who": "An IBM 7090 at Bell Labs, programmed to sing; Arthur C. Clarke saw a demonstration there in 1962",
        "where": "Bell Labs; the song is the one HAL 9000 sings during its deactivation in 2001: A Space Odyssey (1968)",
        "link": "https://en.wikipedia.org/wiki/Daisy_Bell",
        "concepts": ["SongLyrics", "SongAudio"],
        "story": ("Wikipedia's article on Daisy Bell says that in 1961 an IBM 7090 at Bell Labs was programmed to sing the song, one of the earliest demonstrations of computer speech synthesis. "
                  "Arthur C. Clarke saw a demonstration at Bell Labs in 1962 and referred to it in the 1968 novel and film 2001: A Space Odyssey, in which the HAL 9000 computer sings it during its gradual deactivation. "
                  "In this study the chapter's song program for 99 bottles of beer made 396 lines and 2,377 words, and pyttsx3 wrote them as 699.3 seconds of audio in 7.5 seconds of work, without a note of music."),
        "lesson": "Speaking a song is not singing it",
        "source": ("Wikipedia, 'Daisy Bell' (the IBM 7090 of 1961, Clarke in 1962, HAL 9000), read 2026-10-14; "
                   "this study's leaves SongLyrics and SongAudio."),
    },
    {
        "id": "ESpeak1995",
        "title": "A small synthesizer for RISC OS became the engine under pyttsx3 on Linux",
        "when": "1995",
        "who": "Jonathan Duddington, who released Speak in 1995; later the eSpeak NG developers",
        "where": "RISC OS computers in 1995; Linux with Speak 1.05 under the GPLv2 on 17 February 2006",
        "link": "https://en.wikipedia.org/wiki/ESpeak",
        "concepts": ["EspeakDependency", "LinuxEspeak"],
        "story": ("Wikipedia's article on eSpeak says that in 1995 Jonathan Duddington released the Speak speech synthesizer for RISC OS computers supporting British English, and that on 17 February 2006 Speak 1.05 was released under the GPLv2 license, initially for Linux. "
                  "Development continued until it was renamed eSpeak, and eSpeak NG continues it. "
                  "In this study pyttsx3 2.99 started with eSpeak NG 1.51 and saved a WAV, but with only the package the chapter names (espeak 1.48.15) its init raised ValueError for the voice gmw/en, and with neither it raised RuntimeError."),
        "lesson": "The package the book names no longer starts pyttsx3",
        "source": ("Wikipedia, 'ESpeak' (Speak of 1995 for RISC OS, Speak 1.05 under the GPLv2 on 17 February 2006), read 2026-10-14; "
                   "this study's leaves EspeakDependency and LinuxEspeak."),
    },
    {
        "id": "SubRip2000",
        "title": "A Windows tool released in 2000 named the SRT subtitle file",
        "when": "2000",
        "who": "Brain and Zuggy, the developers of SubRip",
        "where": "Microsoft Windows; SubRip was released on 3 March 2000 and its text format uses the extension .srt",
        "link": "https://en.wikipedia.org/wiki/SubRip",
        "concepts": ["SrtListing", "ReadBackCues"],
        "story": ("Wikipedia's article on SubRip says the program, developed by Brain and Zuggy for Microsoft Windows, was released on 3 March 2000, and that the SubRip Text file format has the filename extension .srt and the internet media type application/x-subrip. "
                  "Its blocks are a number, a time range and text. "
                  "In this study Whisper's SRT writer produced the chapter's 223-byte listing exactly for the two segments the book prints, wrote times with a comma before the milliseconds (01:00:01,500), and its WebVTT writer used a full stop (01:00:01.500)."),
        "lesson": "One comma separates SRT from WebVTT",
        "source": ("Wikipedia, 'SubRip' (Brain and Zuggy, released 3 March 2000, the extension .srt), read 2026-10-14; "
                   "this study's leaves SrtListing and ReadBackCues."),
    },
    {
        "id": "Whisper2022",
        "title": "Whisper was released as open-source software in September 2022",
        "when": "2022",
        "who": "OpenAI, which trained Whisper on 680,000 hours of labelled audio-transcript pairs",
        "where": "Released as open-source software in September 2022; the training data held 117,000 hours in 96 non-English languages",
        "link": "https://en.wikipedia.org/wiki/Whisper_(speech_recognition_system)",
        "concepts": ["ModelFiles", "WhisperPackage"],
        "story": ("Wikipedia's article on Whisper says it was created by OpenAI and first released as open-source software in September 2022, and that its training dataset consists of 680,000 hours of labeled audio-transcript pairs sourced from the internet, including 117,000 hours in 96 non-English languages. "
                  "The weights are files that the package downloads on first use. "
                  "In this study the file of the tiny model had 75,572,083 bytes and that of the base model 145,262,807 bytes, where the chapter's table says 74MB and 142MB, and the large-v3 file had 3,087,371,615 bytes."),
        "lesson": "A model is a file that the package downloads",
        "source": ("Wikipedia, 'Whisper (speech recognition system)' (released in September 2022; 680,000 hours; 117,000 hours in 96 non-English languages), read 2026-10-14; "
                   "this study's leaves ModelFiles and WhisperPackage."),
    },
]

LINK_STATUS = {'Voder1939': 200, 'Audrey1952': 200, 'DaisyBell1961': 200, 'ESpeak1995': 200, 'SubRip2000': 200, 'Whisper2022': 200}


def run_checks():
    bad = []
    ids = [x["id"] for x in STORIES]
    if len(ids) != len(set(ids)):
        bad.append("duplicate story ids")
    for x in STORIES:
        for f in ("who", "where", "link", "when", "title", "lesson", "source", "story"):
            if not str(x.get(f, "")).strip():
                bad.append("%s: missing %s (5N1K)" % (x["id"], f))
        if not x.get("link", "").startswith("http"):
            bad.append("%s: link is not a URL" % x["id"])
        if len(x["lesson"].split()) > 14:
            bad.append("%s: lesson over 14 words" % x["id"])
        if not (2 <= x["story"].count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % x["id"])
        if LINK_STATUS and LINK_STATUS.get(x["id"]) != 200:
            bad.append("%s: link status %r, not 200" % (x["id"], LINK_STATUS.get(x["id"])))
        if not LINK_STATUS:
            bad.append("LINK_STATUS is empty")
    by = {x["id"]: x for x in STORIES}
    for sid, year in (("Voder1939", "1939"), ("Audrey1952", "1952"), ("DaisyBell1961", "1961"), ("ESpeak1995", "1995"), ("SubRip2000", "2000"), ("Whisper2022", "2022")):
        if year not in by[sid]["story"] and year not in by[sid]["when"]:
            bad.append("%s: date missing from story" % sid)
        if year not in by[sid]["when"]:
            bad.append("%s: year %s not in when" % (sid, year))
    return bad


def ask_links():
    import urllib.request, urllib.error
    out = {}
    for x in STORIES:
        req = urllib.request.Request(x["link"], headers={"User-Agent": "sen0414-study/1.0 (altunel.yusuf@gmail.com)"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out[x["id"]] = r.status
        except urllib.error.HTTPError as e:
            out[x["id"]] = e.code
        except Exception as e:
            out[x["id"]] = type(e).__name__
    return out


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "links":
        print(ask_links())
    else:
        b = run_checks()
        print(len(STORIES), "stories; self-check failures:", len(b))
        for x in b:
            print("  ", x)
