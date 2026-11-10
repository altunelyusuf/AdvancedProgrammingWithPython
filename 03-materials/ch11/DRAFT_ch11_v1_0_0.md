# SEN0414 — Chapter 11 draft: Organizing Files
*(3rd edition, "Automate the Boring Stuff with Python"; chapter_code_ch11_v1_0_0.json, deck SEN0414_Ch11_OrganizingFiles_3e_v2_0_0.pptx, page sen0414_ch11_page_v9_96_0.html)*

**Status of this draft:** this chapter's deck and interactive page already exist, already passed the
iteration-20 structural retrofit in the closed Lineage2 (`TK_Ret_Ch11_Research`/`_Verify`/`_Page_Build`/
`_Page_Verify`/`_Deck_Build`/`_Deck_Verify`, all Done 2026-10-26), and were read again this turn against
the current standard (lineage `sen0414-ch11ch12-lineage`, task `TK4_StateCheck_Ch11`). Unlike chapter 9,
no gap was found: the deck's four story slides already match the self-checked companion script
`08-tooling/sen0414_ch11_stories_v1_0_1.py` (4 stories, 0 self-check failures) and each story's sourced
asset in `assets/ASSETS_PROVENANCE_v1_0_0.md`/`v1_1_0.md`; all 19 code examples re-ran this turn under
Python 3.13 and reproduced their recorded output exactly. This draft is a write-up of what already
works, for your reading and approval, not a correction pass.

**One open item carried from the state check (not blocking):** `03-materials/slides/Chapter9OrganizingFiles_YA_v1_0_0.pptx`
duplicates this chapter's subject under the old edition's numbering — the same situation as the
chapter-9/10 YA decks you retired last week. Left as your decision (section 5 below), not acted on here.

---

## 1. The story

Four stories, each already told on its own slide, placed through the chapter at the point its concept
first appears — not bunched at the open.

The first belongs to deletion. In 1983 Apple hired Susan Kare, who had no formal training in computer
graphics at all, to draw the small pictures the first Macintosh would need for its own commands.
Working on a 32-by-32 pixel grid that lead software architect Andy Hertzfeld had proposed, she first
blocked the squares out by hand on graph paper before redrawing each one electronically in an icon
editor Hertzfeld built on the Macintosh prototype itself. Among the icons Kare drew that year was the
trash can, the picture that shipped on the Macintosh's own desktop in 1984 and has stood for a
reversible delete on a graphical desktop ever since. The third-party `send2trash` module this chapter
names moves a file to exactly that bin instead of deleting it outright — the one operation in this
whole chapter a user can still undo by hand.

The second belongs to the folder tree itself. R.C. Daley of MIT's Project MAC, with P.G. Neumann of
Bell Labs, presented "A General Purpose File System for Secondary Storage" at the 1965 Fall Joint
Computer Conference, laying out Multics's own tree-structured file system — folders holding folders
holding files — built for a system meant to be shared by many users and administered in pieces at
once. Ken Thompson and Dennis Ritchie, together with Doug McIlroy and J.F. Ossanna, had all worked on
Multics at Bell Labs before the project's own slow progress pushed Bell Labs out of it, and the small
operating system the four built next, Unix, kept the identical tree of folders inside folders at its
very core. Every folder `os.walk` visits today, descending from one folder into its own subfolders in
turn, walks the same shape Daley and Neumann described in 1965.

The third belongs to the ZIP format. Phil Katz had already been sued by Systems Enhancement
Associates, which claimed his own PKARC archiver copied its ARC format too closely; rather than fight
over one more compatible format, Katz and Gary Conway of Infinity Design Concepts designed a new one
of their own, and on 14 February 1989 PKWARE and Infinity Design Concepts issued a joint press release
placing the .ZIP format in the public domain, free for any program to read or write. The first
specification, APPNOTE.TXT, shipped that same year inside Katz's own PKZIP 0.9. Every `zipfile.ZipFile`
this chapter opens, in mode `'w'`, `'a'` or `'r'`, reads and writes exactly the public-domain structure
that one press release described.

The fourth belongs to the compression underneath it. Jean-Loup Gailly, who had already written the
compression half of gzip, and Mark Adler, who wrote the matching decompression half, joined their work
into a single free library they called zlib, built first for Thomas Boutell's own libpng image library
rather than for any archiver at all, and released zlib 0.9 on 1 May 1995 — a clean-room implementation
of the DEFLATE algorithm that owed nothing to Phil Katz's own patented code, free to embed in any
program at all. Python's own `zipfile` module links against exactly this library whenever a write names
`compress_type=zipfile.ZIP_DEFLATED`.

**Pictures and sources (all four of the deck's story-image assets already on file):** Kare —
`assets/photo_kare.jpg`, live link https://www.smithsonianmag.com/innovation/how-susan-kare-designed-user-friendly-icons-for-first-macintosh-180973286/.
Daley/Neumann — `assets/photo_neumann.jpg` (Peter G. Neumann; R.C. Daley has no free portrait), live
link https://multicians.org/history.html. Katz — `assets/photo_katz.jpg` (the PKZIP floppy disk, the
product of the 1989 release; no free portrait of Katz himself was found), live link
https://en.wikipedia.org/wiki/ZIP_(file_format). Adler — `assets/photo_adler.jpg`/`photo_adler_crop.jpg`
(Jean-Loup Gailly has no free portrait), live link https://en.wikipedia.org/wiki/Zlib.

---

## 2. Explanations (what each block of the chapter earns, in plain language)

- **Copying vs. moving:** `shutil.copy`/`copy2`/`copytree` leave the original in place; `shutil.move`
  does not — the everyday-pictures slide (duplicating a key vs. handing over the only one) is the
  anchor for this distinction before any code.
- **copy vs. copy2:** `copy2` is `copy` plus preserved metadata (the file's modification time); worth
  calling out explicitly since the difference is invisible unless a student checks the timestamp.
- **Deleting is the risky operation of the chapter:** `os.unlink`/`os.rmdir`/`shutil.rmtree` cannot be
  undone — the "print first, delete later" pattern (build the list of what would be deleted, print it,
  only then act) is presented as the professional habit, not an afterthought, and `send2trash` is the
  one safety net among them.
- **Three ways to list a folder:** `os.listdir` (plain names), `pathlib.Path.iterdir` (path objects),
  `glob` (pattern matching) — same job, different shapes of answer, chosen by what the caller needs
  next.
- **os.walk's three-tuple:** `(dirpath, dirnames, filenames)` at every level it visits — the folder
  sizes example (summing bytes while walking) is the first place a student uses all three parts of the
  tuple together rather than just the filenames.
- **Path.mkdir with parents=True:** one call instead of checking and creating each ancestor folder by
  hand; `exist_ok=True` as the partner flag for "don't fail if it's already there."
- **ZIP files as a module, not a format to hand-parse:** `zipfile.ZipFile` in modes `'r'`/`'w'`/`'a'`/`'x'`
  mirrors the file-mode letters already learned for plain files, which is the bridge this section
  leans on.
- **extractall vs. extract:** the whole archive at once vs. one named member — and why extracting
  an archive from an untrusted source into a fresh, disposable folder is the safe default.
- **make_archive/unpack_archive as the shutil-level shortcut:** one call that wraps the same zipfile
  machinery just taught, for when a student just wants "zip this folder" without building the
  ZipFile loop by hand.
- **Capstone:** Project 5 (back a folder up into a numbered ZIP) uses copying, walking, and archiving
  together; the three practice programs each isolate one more real task (copy by extension, find big
  files, swap date formats) built from the same primitives.

---

## 3. Slide / page-tab outline (existing deck order, slide order = page tab order; confirmation, not
a rebuild)

| # | Slide | Code example (name, from the manifest) |
|---|---|---|
| 1 | shutil.copy: one file to a folder or a new name | *shutil.copy: one file* |
| 2 | shutil.copytree: a folder with everything in it | *shutil.copytree: a whole folder* |
| 3 | copy and copy2: what happens to the time stamp | *copy2 keeps the time stamp* |
| 4 | shutil.move: move, rename, overwrite | *shutil.move: move and rename* |
| 5 | os.unlink and os.rmdir: one file, one empty folder | *os.unlink and os.rmdir* |
| 6 | shutil.rmtree: a folder and everything inside | *shutil.rmtree* |
| 7 | Safe deletion: print first, delete later | *A dry run before deleting* |
| 8 | send2trash: the recycle bin | — |
| 9 | **Story: the recycle bin is a 1983 drawing** | — |
| 10 | Listing one folder: listdir, iterdir, glob | *Listing one folder* |
| 11 | os.walk: the folder, its subfolders, its files | *os.walk visits every folder* |
| 12 | Counting bytes per folder while walking | *Folder sizes with os.walk* |
| 13 | Path.mkdir: making folders, also in a chain | *Path.mkdir with parents* |
| 14 | **Story: the folder tree is a 1965 Multics design** | — |
| 15 | zipfile.ZipFile: write a file into an archive | *Writing a ZIP file* |
| 16 | ZIP modes: read, append, exclusive | *ZIP modes: append and refuse* |
| 17 | extractall and extract: unpacking an archive | *Extracting from a ZIP* |
| 18 | shutil.make_archive and unpack_archive | *make_archive and unpack_archive* |
| 19 | **Story: the ZIP format was given away on 14 February 1989** | — |
| 20 | **Story: the engine under ZIP_DEFLATED shipped on 1 May 1995** | — |
| 21 | Project 5: back a folder up into a numbered ZIP | *Project 5: backupToZip* |
| 22 | Practice program: copy every PDF of a tree | *Practice 1: copy by extension* |
| 23 | Practice program: find the big files | *Practice 2: the big files* |
| 24 | Practice program: American dates to European dates | *Practice 3: swap day and month* |

All 19 code examples re-ran this turn (Python 3.13, standard library only, each in its own temporary
folder) and reproduced the output recorded in `chapter_code_ch11_v1_0_0.json` exactly — no change
needed. The deck's 4 story slides sit where the explanation just above puts them: after deletion
(Kare/recycle-bin), after the folder-tree section (Daley–Neumann/Multics), and both ZIP-format stories
back to back right after the archiving mechanics, before the project — not bunched at the chapter's
open.

---

## 4. Resources slide

- **Book:** Automate the Boring Stuff, 3rd edition, chapter 11 — https://automatetheboringstuff.com/3e/chapter11.html
- **Community/tool:** `send2trash` on PyPI — https://pypi.org/project/Send2Trash/
- **Python docs:** `shutil` — https://docs.python.org/3/library/shutil.html; `os.walk` — https://docs.python.org/3/library/os.html#os.walk; `zipfile` — https://docs.python.org/3/library/zipfile.html; `pathlib` — https://docs.python.org/3/library/pathlib.html
- **ZIP format spec (APPNOTE.TXT):** pkware.cachefly.net
- **zlib home page:** https://www.zlib.net/
- **Seminal/background:** "ZIP (file format)," Wikipedia — https://en.wikipedia.org/wiki/ZIP_(file_format); "Multics History" — https://multicians.org/history.html; Susan Kare's Macintosh icons, Smithsonian Magazine.
- **Current Python:** What's new in Python 3.14 — https://docs.python.org/3/whatsnew/3.14.html

No correctness check was needed here (unlike chapter 9) — nothing about the four stories or their dates
was in question this time.

---

## 5. Open items (not blocking the render; named so they are not lost)

1. **Legacy duplicate — your decision:** `Chapter9OrganizingFiles_YA_v1_0_0.pptx` (old-edition
   numbering) duplicates this chapter's subject. Last week you retired the equivalent chapter-9/10 YA
   decks (`Chapter7PatternMatchingWithRegularExpressions_YA_v1_0_0.pptx`,
   `Chapter8ReadingAndWritingFiles_YA_v1_0_0.pptx`); same question here for this one file
   (`ST4_YaRetirement`, currently Proposed). No equivalent file exists for chapter 12.
2. **No research/ABox retrofit gap:** unlike chapter 9's still-open `TK_Ret_Ch09_Research`/`_Verify`,
   chapter 11's structural retrofit (`TK_Ret_Ch11_Research`/`_Verify`/`_Page_Build`/`_Page_Verify`/
   `_Deck_Build`/`_Deck_Verify`) is already Done (2026-10-26). Nothing carried forward.
