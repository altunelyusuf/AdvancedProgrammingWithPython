# SEN0414 — Chapter 10 draft: Reading and Writing Files
*(3rd edition, "Automate the Boring Stuff with Python"; chapter_code_ch10_v1_0_0.json, deck SEN0414_Ch10_ReadingWritingFiles_3e_v2_0_0.pptx, page sen0414_ch10_page_v9_95_0.html)*

**Status of this draft:** this chapter's deck (41 slides, 7 native charts, 4 story slides) and page
already went through the full Iteration-20 retrofit pipeline and were controlled and verified Done
(deck standard check 13/13 PASS, overlap check CLEAN, 18/18 examples reproduce their recorded output,
page test 9.37.0: 402 features passed/0 failed, chapter-check Research/Ch10: PASS). Read against the
current standard again this turn (`TK3_StateCheck_Ch10`) — no open gap found. This draft exists so
chapter 10 is rendered from the same one-draft process as chapter 9, and so the story slot below is
pinned to sourced figures with a live link, matching the current standard.

---

## 1. The story

In 2001, Douglas Crockford and Chip Morningstar — co-founders of a small technology consultancy
called State Software — were gathered in Morningstar's garage, testing an early idea for what we'd
now call a single-user, multi-person web application, years before the rest of the web caught up to
the idea. They needed something ordinary web pages of the time struggled with: a simple way to move
structured data back and forth between a browser's JavaScript and a server. The accepted answer in
2001 was XML, but Crockford didn't want a parsing library — he wanted the browser's own JavaScript
engine to read the data natively, with nothing extra installed. So he looked at JavaScript's own
object literal syntax, stripped it down to the smallest subset that could represent any data
structure, and gave that subset a name: JavaScript Object Notation, JSON.

He didn't patent it or found a working group. He registered the domain json.org, put up a one-page
specification, and let the format speak for itself. When critics pointed out that he'd just
reinvented part of what XML already did, Crockford's answer became one of the format's most quoted
lines: "the good thing about reinventing the wheel is that you can get a round one." That
deliberate minimalism — no schemas, no namespaces, just objects, arrays, strings, numbers, booleans
and null — is exactly why `json.dump()` and `json.load()` in this chapter are as small and stable as
they are twenty-five years later, and why JSON ended up as the plain, portable alternative this
chapter offers once `shelf` has shown students the more convenient, Python-only option.

**Picture and source (asset already on file):** `assets/photo_douglas_crockford_2013.jpg` — provenance
in `assets/ASSETS_PROVENANCE_v1_0_0.md`. **Live link:**
https://twobithistory.org/2017/09/21/the-rise-and-rise-of-json.html (names Morningstar and the garage
origin directly) and https://www.json.org/ for the one-page spec itself.

*(The deck's other two story assets — `assets/photo_rob_pike_oscon.jpg` and
`assets/photo_ken_thompson_2019.jpg` — fit the file-path/`pathlib`-flavoured opening half of the
chapter if a second story beat is wanted there: both co-created Unix's own path and file-handling
conventions this chapter's `Path` examples still follow. Left as background unless a second beat is
wanted; the JSON story alone covers the chapter's two halves — paths/files, then structured
storage — well enough on its own.)*

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
  https://docs.python.org/3/library/json.html
- **Seminal/community:** the JSON specification itself — https://www.json.org/
- **Story source:** https://twobithistory.org/2017/09/21/the-rise-and-rise-of-json.html
- **Tutorial/video:** Corey Schafer, "Python Tutorial: File Objects" (YouTube) — matches this
  chapter's open/read/write scope.

---

## 5. Open items (not blocking the render; named so they are not lost)

1. **No content gap found.** Chapter 10 is already at the current standard; this draft mainly adds
   the sourced story and resources above.
2. **Legacy duplicate — closed (2026-11-09):** you decided to retire it now. `Chapter8ReadingAndWritingFiles_YA_v1_0_0.pptx`
   has been removed from `03-materials/slides/` (recoverable from git history); `ST3_YaRetirement` is Done
   (same decision as chapter 9's duplicate).
