"""SEN0414 chapter 24 - the story companion to the chapter corpus (version 2.0.0, over 1.0.0).

Six real, dated, sourced stories, one live link each, checked by this file's own run_checks(). Version 2.0.0 carries the story text of the lecture deck
4.0.0 of chapter 24 (SEN0414_Ch24_MakePythonTalk_3e_v4_0_0.pptx), so the page and the deck tell the same story. LINK_STATUS is the HTTP status that each
link answered to a plain GET on 2026-11-27 with the identifying agent "SEN0414-course-materials/1.0 (course materials; contact via GitHub altunelyusuf)";
`python3 sen0414_ch24_stories_v2_0_0.py links` asks again.
Pictures: see ch24-page/stories_img_v9_111_0.json and 03-materials/ch24/assets/story_images_v1_0_0.json (files, licences, credits).
Usage: import STORIES; run the file for the self-check, or with the argument links to ask every link again.
"""
__version__ = "2.0.0"

STORIES = [{'id': 'Kempelen1789',
  'lesson': 'Speech by machine is more than two centuries old',
  'link': 'https://en.wikipedia.org/wiki/Wolfgang_von_Kempelen',
  'source': "Wikipedia, 'Wolfgang von Kempelen', read 2026-11-27.",
  'story': 'In 1789 Johann Wolfgang von Kempelen published a book with nearly twenty years of speech research and a speaking machine that a hand '
           'played. He was also known for the chess playing hoax The Turk. An early version of the machine can still be seen in the Deutsches Museum '
           'in Munich. The picture shows a reconstruction. pyttsx3 asks the speech system of the machine to do by program what that device did by '
           'hand.',
  'title': 'A speaking machine and a book of speech research appeared in 1789',
  'when': '1789',
  'where': 'Vienna; an early version of the machine is in the Deutsches Museum in Munich',
  'who': 'Johann Wolfgang von Kempelen, a Hungarian writer, architect, engineer and inventor'},
 {'id': 'Voder1939',
  'lesson': 'A voice is a set of settings',
  'link': 'https://en.wikipedia.org/wiki/Voder',
  'source': "Wikipedia, 'Voder', read 2026-11-27.",
  'story': "Homer Dudley invented the Voder at Bell Telephone Laboratories in 1937 and 1938, and it was shown at the 1939 New York World's Fair and "
           'in San Francisco. An operator played it with a wrist bar, fifteen keys and a foot pedal. Helen Harper trained twenty operators and was '
           'noted for her skill. The picture shows the Voder with the crowd. The voice of pyttsx3 has a rate, a volume and a voice, which are the '
           'settings that the operator moved by hand.',
  'title': "The Voder spoke at the 1939 New York World's Fair",
  'when': '1939',
  'where': "New York World's Fair and San Francisco",
  'who': 'Homer Dudley of Bell Telephone Laboratories, and the operator Helen Harper'},
 {'id': 'Reddy1969',
  'lesson': 'Recognition grew from decades of research',
  'link': 'https://en.wikipedia.org/wiki/Raj_Reddy',
  'source': "Wikipedia, 'Raj Reddy', read 2026-11-27.",
  'story': 'Raj Reddy, born on 13 June 1937, worked at Stanford and then at Carnegie Mellon University from 1969 on speech, language, vision and '
           'robotics. He and his colleagues made demonstrations such as voice control of a robot and large-vocabulary connected speech recognition. '
           'In 1994 he and Edward Feigenbaum received the ACM Turing Award. model.transcribe() in this chapter is a result of that line of work.',
  'title': "Raj Reddy's group made computers understand connected speech",
  'when': '1969',
  'where': 'Stanford, then Carnegie Mellon University from 1969',
  'who': 'Raj Reddy of Stanford and Carnegie Mellon University, with his colleagues'},
 {'id': 'Captions1971',
  'lesson': 'Captions are text with times',
  'link': 'https://en.wikipedia.org/wiki/Closed_captioning',
  'source': "Wikipedia, 'Closed captioning', read 2026-11-27.",
  'story': 'Closed captioning was first demonstrated in the United States in December 1971 at the First National Conference on Television for the '
           'Hearing Impaired in Knoxville, Tennessee. On 15 February 1972 ABC and the National Bureau of Standards showed captions inside a normal '
           'broadcast of The Mod Squad at Gallaudet College. Regular open-captioned broadcasts began on PBS with The French Chef in 1972. The SRT '
           'and VTT files of this chapter carry the same cues, with times.',
  'title': 'Closed captions were first shown in December 1971',
  'when': '1971',
  'where': 'Knoxville, Tennessee; Gallaudet College; PBS',
  'who': 'The organisers of the First National Conference on Television for the Hearing Impaired, ABC and the National Bureau of Standards'},
 {'id': 'DaisyBell1961',
  'lesson': 'A song can be made by program',
  'link': 'https://en.wikipedia.org/wiki/Daisy_Bell',
  'source': "Wikipedia, 'Daisy Bell', read 2026-11-27.",
  'story': 'Harry Dacre wrote the song Daisy Bell in 1892. It is the earliest song sung with computer speech synthesis, by an IBM 7090 in 1961. The '
           'picture shows that machine. The 99 verses of this chapter are spoken by a synthesizer too, and the program writes the sound into a WAV '
           'file.',
  'title': 'A computer sang Daisy Bell in 1961',
  'when': '1961',
  'where': 'The picture shows an IBM 7090 at NASA Ames',
  'who': 'Harry Dacre, who wrote the song in 1892, and the IBM 7090 that sang it'},
 {'id': 'Gettysburg1863',
  'lesson': 'A recording can be transcribed by program',
  'link': 'https://en.wikipedia.org/wiki/Gettysburg_Address',
  'source': "Wikipedia, 'Gettysburg Address', read 2026-11-27.",
  'story': "Abraham Lincoln spoke on the afternoon of 19 November 1863 at the dedication of the Soldiers' National Cemetery, four and a half months "
           'after the battle. Five manuscript copies are known, and the Bliss copy is the standard text of the address. The picture shows a copy. '
           'The transcriber of this chapter reads a public-domain recording of the address that the Internet Archive hosts; it stands in for a video '
           'site.',
  'title': 'Lincoln spoke at Gettysburg on 19 November 1863',
  'when': '1863',
  'where': "Gettysburg, Pennsylvania, at the Soldiers' National Cemetery",
  'who': 'Abraham Lincoln'}]

LINK_STATUS = {'Kempelen1789': 200, 'Voder1939': 200, 'Reddy1969': 200, 'Captions1971': 200, 'DaisyBell1961': 200, 'Gettysburg1863': 200}

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
        if LINK_STATUS.get(x["id"]) != 200:
            bad.append("%s: link status %r, not 200" % (x["id"], LINK_STATUS.get(x["id"])))
    for x in STORIES:
        if x["when"] not in x["story"] and x["when"] not in x["title"]:
            bad.append("%s: year %s not in story or title" % (x["id"], x["when"]))
    return bad


def ask_links():
    import urllib.request, urllib.error
    out = {}
    for x in STORIES:
        req = urllib.request.Request(x["link"], headers={"User-Agent": "SEN0414-course-materials/1.0 (course materials; contact via GitHub altunelyusuf)"})
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
