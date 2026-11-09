# SEN0414 — Chapter 10 draft: Reading and Writing Files
*(3rd edition, "Automate the Boring Stuff with Python"; chapter_code_ch10_v1_0_0.json, deck SEN0414_Ch10_ReadingWritingFiles_3e_v2_0_0.pptx, page sen0414_ch10_page_v9_95_0.html)*

**Status of this draft:** this chapter's deck (41 slides, 7 native charts, 4 story slides) and page
already went through the full Iteration-20 retrofit pipeline and were controlled and verified Done
(deck standard check 13/13 PASS, overlap check CLEAN, 18/18 examples reproduce their recorded output,
page test 9.37.0: 402 features passed/0 failed, chapter-check Research/Ch10: PASS). Read against the
current standard again this turn (`TK3_StateCheck_Ch10`) — the chapter's content has no open gap, but
this draft's own story section did: the first pass only wrote up one of the deck's four existing story
beats (JSON) and left the other three unused. Corrected below (2026-11-09) to all four, matching the
story companion `08-tooling/sen0414_ch10_stories_v1_0_0.py`. This draft exists so chapter 10 is
rendered from the same one-draft process as chapter 9, and so the story section is pinned to sourced
figures with live links, matching the current standard.

---

## 1. The story

**Correction to the first pass of this draft:** the deck already carries four story beats, not one —
recorded in `08-tooling/sen0414_ch10_stories_v1_0_0.py` (self-check: 4 stories, 0 failures) and matching
the four photo/logo assets in `assets/ASSETS_PROVENANCE_v1_0_0.md`. My first pass only wrote up the JSON
beat and treated the Thompson/Pike assets as spare. They aren't spare — they're already part of this
chapter's standard. All four, in the order the chapter teaches them:

The chapter opens on `Path` objects, and the reason a path is an object with its own methods rather
than a plain string traces to one proposal: on 30 July 2012, Antoine Pitrou wrote PEP 428, "The
pathlib module — object-oriented filesystem paths," arguing a filesystem path deserved to be its own
object rather than a string handed to separate `os.path` functions. The proposal was discussed through
2013 and shipped two years later, in Python 3.4 (March 2014) — bringing with it the `/` join operator
and the `parts`/`parent`/`stem`/`suffix` attributes this chapter's opening examples now treat as the
ordinary way to build and take apart a path.

A few examples later, the chapter reaches `open()`'s `encoding` argument — almost always `'utf-8'` by
the chapter's own count — and that format has an exact birthday. Rob Pike later wrote that UTF-8 was
"designed, in front of my eyes, on a placemat in a New Jersey diner one night in September" 1992, with
Ken Thompson working out the bit-packing by hand while Pike watched; the surviving source changes date
the first working code to 4 September 1992 and a proposal mailed to the X/Open committee four days
later. The two had been asked to review a rival encoding for the Plan 9 operating system they were
building at Bell Labs, found it couldn't recover a byte stream picked up mid-character, and designed a
fix overnight instead — by the end of that week, Plan 9 ran entirely on the format they'd sketched on
a placemat.

Further in, the chapter shows `shelve.open()` as the path of least resistance for saving a program's
own variables, and that shape is older still: Ken Thompson — already known for Unix and, two chapters
ago, for the regular-expression search algorithm — wrote the first `dbm`, a simple key-value store AT&T
released as part of Unix in 1979. `dbm` let a program store a string under a string key and get it
back by that key alone, no query language, no server — exactly the shape `shelve.open()` still presents
today, through whichever backend Python currently picks (`dbm.sqlite3` first since Python 3.13).

Only after `shelve` does the chapter reach JSON, offered as the plain alternative for data meant to
leave Python entirely. In 2001, Douglas Crockford and Chip Morningstar — working together at a small
consultancy called State Software — wanted a browser and a server to exchange data without reloading
the page. The accepted answer at the time was XML, but Crockford wanted the browser's own JavaScript
engine to read the data natively, so he stripped JavaScript's object-literal syntax down to its
smallest useful subset and gave it a name: JavaScript Object Notation, JSON. He didn't patent it or
found a working group — he registered json.org, put up a one-page spec on 12 November 2002, and let
the format speak for itself. When critics said he'd just reinvented part of what XML already did,
Crockford's answer became one of the format's most quoted lines: "the good thing about reinventing the
wheel is that you can get a round one." That deliberate minimalism — objects, arrays, strings, numbers,
booleans, null, nothing else — is exactly why `json.dump()` and `json.load()` are still this small and
stable a quarter-century later, and why the chapter sets JSON beside `shelve` as the option for when
the data needs to be read by another program or language.

**Pictures and sources (all four assets already on file, provenance in `assets/ASSETS_PROVENANCE_v1_0_0.md`):**
`logo_python.png` for the Pitrou/pathlib beat (no free personal photo of Pitrou was sourced, so the
chapter illustrates this one with the Python logo rather than a portrait) — live link
https://peps.python.org/pep-0428/; `assets/photo_rob_pike_oscon.jpg` and `assets/photo_ken_thompson_2019.jpg`
for the UTF-8 beat — live link https://doc.cat-v.org/bell_labs/utf-8_history; `assets/photo_ken_thompson_2019.jpg`
again for the dbm/shelve beat (same Thompson photo, two different stories) — live link
https://en.wikipedia.org/wiki/DBM_(computing); `assets/photo_douglas_crockford_2013.jpg` for the JSON
beat — live link https://en.wikipedia.org/wiki/JSON (or
https://twobithistory.org/2017/09/21/the-rise-and-rise-of-json.html, which names Morningstar and the
garage origin directly).

---

## 2. Explanations

- **Paths, not strings:** `pathlib.Path` and `/` replace manual string-joining of folder names — the
  chapter's first six examples build this up: constructing a path, finding where you are, inspecting
  a path's parts, making folders, globbing, and reading a path's facts (size, existence, modified
  time) before ever opening a file.
- **Whole-file vs. streamed reading:** `.read_text()`/`.write_text()` for "I just want the string";
  `open()`/`.read()`/`.readline()`/`.readlines()`/`.seek()` for anything that needs to process a file
  incrementally or revisit a position in it.
- **`with` as the point of the whole section:** every example from here on uses `with open(...) as f:`
  — the chapter frames this as "the file closes itself even if the code inside raises," not as a
  syntax rule to memorize.
- **Write modes `w`, `a`, `x`:** one idea (what happens to existing content) with three names —
  overwrite, append, refuse-if-exists — and `x` is worth lingering on since it is the one mode that
  prevents silent data loss.
- **`encoding=`:** introduced as "say what you mean," not as an edge case — the chapter ties it to
  real symptoms (`UnicodeDecodeError`) rather than presenting it as boilerplate.
- **`shelf` then `json`:** `shelf` is shown first because it is the path of least resistance (pickle
  any Python object, keyed like a dict) — then `json` is introduced as the plain, portable alternative
  for when the data needs to leave Python entirely (another program, another language, the network).
  This ordering is deliberate: it lets the story above land as the answer to "why would I ever choose
  the less convenient option," not as an isolated fact.
- **Practice programs and the capstone:** Mad Libs and Regex Search are small, single-idea practice
  programs; Project 4 (the multiple-choice quiz generator, steps 1–2) is the chapter's capstone,
  combining file writing, string templating and the chapter 9 regex skill it deliberately reuses.

---

## 3. Slide / page-tab outline (existing deck order, unchanged — confirmation, not a rebuild)

| # | Slide | Code example (name, from the manifest) |
|---|---|---|
| 1 | Building paths with Path and / | *Building paths with Path and /* |
| 2 | Working directory, home, absolute and relative | *Working directory, home, absolute and relative* |
| 3 | The parts of a filepath | *The parts of a filepath* |
| 4 | Creating new folders | *Creating new folders* |
| 5 | Finding files with glob patterns | *Finding files with glob patterns* |
| 6 | Checking a path and reading file facts | *Checking a path and reading file facts* |
| 7 | Whole-file reading and writing | *Whole-file reading and writing* |
| 8 | open, read and close | *open, read and close* |
| 9 | read, readline, readlines and seek | *read, readline, readlines and seek* |
| 10 | The with statement | *The with statement* |
| 11 | Write modes w, a and x | *Write modes w, a and x* |
| 12 | The encoding argument | *The encoding argument* |
| 13 | Saving variables with a shelf | *Saving variables with a shelf* |
| 14 | json as the plain alternative | *json as the plain alternative* |
| 15 | Practice program: Mad Libs | *Practice program: Mad Libs* |
| 16 | Practice program: Regex Search | *Practice program: Regex Search* |
| 17 | Project 4, step 1: one quiz question | *Project 4, step 1: one quiz question* |
| 18 | Project 4, step 2: quiz and answer-key files | *Project 4, step 2: quiz and answer-key files* |

All 18 examples that touch files first move into a fresh scratch folder (`tempfile.mkdtemp`), so no
printed result holds a real path — already the case, already correct, unchanged. Story slides sit
after the opening path examples and before/around the `shelf`/`json` pair, per the deck's 4
story-image assets.

---

## 4. Resources slide

- **Python docs:** `pathlib` — https://docs.python.org/3/library/pathlib.html; `json` —
  https://docs.python.org/3/library/json.html; `shelve`/`dbm` —
  https://docs.python.org/3/library/shelve.html
- **Seminal work (pathlib):** PEP 428, "The pathlib module" — https://peps.python.org/pep-0428/
- **Seminal/community (JSON):** the JSON specification itself — https://www.json.org/
- **Story sources:** https://en.wikipedia.org/wiki/DBM_(computing) (dbm/shelve);
  https://doc.cat-v.org/bell_labs/utf-8_history (UTF-8); https://peps.python.org/pep-0428/ (pathlib);
  https://twobithistory.org/2017/09/21/the-rise-and-rise-of-json.html (JSON)
- **Tutorial/video:** Corey Schafer, "Python Tutorial: File Objects" (YouTube) — matches this
  chapter's open/read/write scope.

---

## 5. Open items (not blocking the render; named so they are not lost)

1. **No content gap found.** Chapter 10's code/page content is already at the current standard; this
   draft's correction was to its own story section (above) and the resources slide, not the chapter
   itself.
2. **Legacy duplicate — closed (2026-11-09):** you decided to retire it now. `Chapter8ReadingAndWritingFiles_YA_v1_0_0.pptx`
   has been removed from `03-materials/slides/` (recoverable from git history); `ST3_YaRetirement` is Done
   (same decision as chapter 9's duplicate).
