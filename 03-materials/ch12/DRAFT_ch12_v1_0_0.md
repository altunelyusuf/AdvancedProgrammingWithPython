# SEN0414 — Chapter 12 draft: Designing and Deploying Command Line Programs
*(3rd edition, "Automate the Boring Stuff with Python"; chapter_code_ch12_v1_0_0.json, deck SEN0414_Ch12_CommandLinePrograms_3e_v2_0_0.pptx, page sen0414_ch12_page_v9_96_0.html)*

**Status of this draft:** this chapter's deck and interactive page already exist, already passed the
iteration-20 structural retrofit in the closed Lineage2 (`TK_Ret_Ch12_Research`/`_Verify`/`_Page_Build`/
`_Page_Verify`/`_Deck_Build`/`_Deck_Verify`, all Done 2026-10-25/26), and were read again this turn
against the current standard (lineage `sen0414-ch11ch12-lineage`, task `TK4_StateCheck_Ch12`). No gap
was found: the deck's four story slides already match the self-checked companion script
`08-tooling/sen0414_ch12_stories_v1_0_1.py` (4 stories, 0 self-check failures) and their sourced assets
(`photo_doug_mcilroy.jpg`/`photo_dennis_ritchie_2011.jpg`, `image_midnight_commander.png`,
`image_pip_logo.png`); 22 of 23 code examples re-ran this turn and reproduced their recorded output
exactly — the one apparent mismatch (example 8, `os.name, sys.version_info and __file__`) was my own
test harness running the code as a saved script instead of as the book's interactive-session snippet;
re-run as `python3 -I -c "<code>"` it reproduces the recorded output exactly too. No legacy YA-suffixed
deck duplicates this chapter's subject. This draft is a write-up of what already works, not a
correction pass.

---

## 1. The story

Four stories, each already told on its own slide, placed through the chapter at the point its concept
first appears.

The first belongs to quiet output. Doug McIlroy, head from 1965 to 1986 of the Bell Labs Computing
Techniques Research Department — the birthplace of Unix — had proposed the concept of a pipe in a 1964
memo, the output of one program becoming the input of the next. In 1973 Ken Thompson added the
`pipe()` system call and pipes to the shell and several utilities of Version 3 Unix, in what McIlroy
called one feverish night, and the next day saw, in McIlroy's own words, an unforgettable orgy of
one-liners as everybody joined in the excitement of plumbing. In the 1978 *Bell System Technical
Journal* foreword, McIlroy and his two co-authors wrote down the maxims of the style: make each
program do one thing well, expect the output of every program to become the input to another, as yet
unknown, program — and do not clutter output with extraneous information. That last maxim is this
chapter's own advice to keep a command silent by default and print more only when `--verbose` asks for
it.

The second belongs to the launcher's own first line. Dennis Ritchie added kernel support for
interpreter directives at Bell Laboratories between Edition 7 and Edition 8 of Unix, and announced it
in an email dated Thursday, 10 January 1980: if a file being executed begins with the magic characters
`#!`, the rest of the line names the interpreter that runs it. He advised users to put `#! /bin/sh` at
the left margin of the first line of their shell scripts, noting a complete pathname was needed because
no search was done. Since Edition 8 was never publicly released, the feature reached most users through
Berkeley's BSD, appearing in 2.8BSD and enabled by default in 4.2BSD. Asked in 2009 what the
construction was called, Ritchie replied he could not recall it ever being given a proper name — the
later form `#!/usr/bin/env bash`, this chapter's own Ubuntu launcher's first line, adds the PATH search
his first version left out.

The third belongs to how a terminal program can feel. John Socha started work in 1984 on a file
manager for MS-DOS that he first called Visual DOS, and Peter Norton Computing released it as Norton
Commander in 1986. A user saw two panels of file lists side by side, with a list of commands along the
bottom of the screen, a built-in viewer and editor, all drawn with text characters on a plain MS-DOS
screen. Symantec bought Peter Norton Computing in 1990, and the last MS-DOS version, 5.51, came out on
1 July 1998. This chapter's Figure 12-1 shows Norton Commander as its example of a text-based user
interface — a style its own `snowstorm` program imitates with block characters and a cleared screen.

The fourth belongs to the installer the chapter's own commands depend on. Ian Bicking, who had already
written `virtualenv`, announced a new installer called `pyinstall` in a post titled "pyinstall: A New
Hope" on 24 September 2008, as an alternative to `easy_install`. On 28 October 2008 he renamed it, in a
post titled "pyinstall is dead, long live pip!" — pip, by Bicking's own account a recursive acronym for
"Pip Installs Packages," became the installer Python now ships with. Carl Meyer then wrote PEP 405,
created on 13 June 2011, which named Bicking's `virtualenv` as the tool that had shown the value of
isolated environments, and made them part of Python 3.3 as the `venv` module. This chapter's two
commands, `python -m venv .venv` and `python -m pip install`, are those two pieces of work side by
side.

**Pictures and sources (all of the deck's story assets already on file):** McIlroy/Thompson — no free
photo of McIlroy himself was sourced for the pipe story; live link
https://en.wikipedia.org/wiki/Pipeline_(Unix). Ritchie — `assets/photo_dennis_ritchie_2011.jpg`/`_crop.jpg`
(at the Japan Prize ceremony, May 2011), live link https://en.wikipedia.org/wiki/Shebang_(Unix). Socha/
Norton Commander — `assets/image_midnight_commander.png` (a contemporary open-source descendant's
screenshot stands in for the 1986 original, which has no free image on file), live link
https://en.wikipedia.org/wiki/Norton_Commander. Bicking/pip — `assets/image_pip_logo.png`, live link
https://en.wikipedia.org/wiki/Pip_(package_manager). `photo_doug_mcilroy.jpg`/`_crop.jpg` is on file and
used on the McIlroy/pipes story slide itself.

---

## 2. Explanations (what each block of the chapter earns, in plain language)

- **A program by any other name:** the same program is invoked differently depending on how the shell
  finds it (bare name via PATH, relative path, absolute path) — this sets up PATH before any code runs.
- **cd/pwd/ls as Python calls:** `os.chdir`, `os.getcwd`, `os.listdir`/`glob` map the shell commands a
  student already knows onto the calls this chapter actually teaches — deliberately reusing chapter
  11's `os`/`pathlib` vocabulary rather than introducing it fresh.
- **PATH and which:** PATH is "a text of folders, searched in order" — `shutil.which` is presented as
  *doing in Python* exactly what the shell does when you type a bare command name.
- **Virtual environments:** a venv is "a folder and a settings file" (`pyvenv.cfg`), not magic —
  `activate` is just a PATH edit, which is why the chapter can show its effect with `sys.prefix` vs.
  `sys.base_prefix` rather than asking students to trust it.
- **pip:** version pins (`package==1.17.4`) and `importlib.util.find_spec` (can this be imported,
  without importing it) are presented together as "ask before you leap" for dependencies.
- **Self-aware programs:** `os.name`, `sys.version_info`, `__file__`, `sys.argv` — a program that can
  describe its own environment before it does anything with it; `sys.exit` with a message is the
  chapter's standard for failing loudly rather than silently.
- **argparse:** declaring arguments once instead of hand-parsing `sys.argv`, and the "wrong word is
  refused" example exists specifically to show argparse's own error handling, not just its happy path.
- **Designing terminal output:** "quiet by default, `--verbose` for more" is the chapter's own applied
  version of the pipes story's maxim; `chr`/escape codes/colour are then built *after* that principle is
  set, so the visual layer doesn't overshadow the design decision underneath it.
- **Deployment, three systems:** the Ubuntu launcher (`#!/usr/bin/env bash`, `chmod u+x`, a `.desktop`
  entry) is shown in full, concrete detail, because it is the one students can actually run inside this
  course's own environment; PyInstaller is presented for the one-file case, with its real cost
  (interpreter bundled in) named rather than treated as free.
- **Capstone:** `ccwd` and the clipboard recorder are small enough to build end to end in one sitting;
  the practice program (make earlier projects deployable) closes the loop back to Part 1's "a program by
  any other name."

---

## 3. Slide / page-tab outline (existing deck order, slide order = page tab order; confirmation, not
a rebuild)

| # | Slide | Code example (name, from the manifest) |
|---|---|---|
| 1 | A Program by Any Other Name | — |
| 2 | The terminal: cd and pwd as Python calls | *cd and pwd as os calls* |
| 3 | The terminal: ls and dir *.exe as Python calls | *ls and dir as os.listdir* |
| 4 | PATH: a text of folders, searched in order | *PATH is a text of folders* |
| 5 | which: the first folder that holds the program | *shutil.which walks the folders* |
| 6 | Virtual environments: a folder and a settings file | *pyvenv.cfg is a settings file* |
| 7 | activate puts the environment first on PATH | *activate edits PATH* |
| 8 | pip: pin a version, find a module | *pip requirement and find_spec* |
| 9 | **Story: pip began as pyinstall, September 2008** | — |
| 10 | Self-aware programs: system, version, file | *os.name, sys.version_info and __file__* |
| 11 | Missing modules and sys.exit with a message | *ModuleNotFoundError and sys.exit* |
| 12 | Command line arguments: sys.argv | *sys.argv and shlex.split* |
| 13 | argparse: declare the arguments once | *argparse declares the arguments* |
| 14 | argparse: a wrong word is refused | *argparse refuses a wrong word* |
| 15 | Text-based design: quiet by default | *Quiet, default and verbose* |
| 16 | **Story: the pipe and the quiet command, 1973** | — |
| 17 | **Story: a text screen that felt like a desktop, 1986** | — |
| 18 | Terminal presentation: chr and os.system | *chr and the clear command* |
| 19 | Colour in the terminal: what bext.fg and bext.bg send | *Colour names as escape codes* |
| 20 | Snowstorm: one frame of the animation | *One snowstorm frame* |
| 21 | Deploying on Ubuntu: the launcher script | *The launcher script, line by line* |
| 22 | Deploying on Ubuntu: chmod u+x | *chmod u+x makes it a command* |
| 23 | **Story: the #! line, announced by email, 1980** | — |
| 24 | Deploying on Ubuntu: the .desktop entry | *A .desktop entry with configparser* |
| 25 | ccwd: copying the current working directory | *ccwd copies the working directory* |
| 26 | Clipboard Recorder: print what changed | *Clipboard recorder loop* |
| 27 | PyInstaller: one file, a whole interpreter | *The PyInstaller command line* |
| 28 | Practice program: make your programs deployable | *Launchers for earlier projects* |

22 of 23 code examples re-ran this turn (Python 3.13, each in its own temporary folder) and reproduced
`chapter_code_ch12_v1_0_0.json`'s recorded output exactly; example 8 reproduces it too once run the same
way the book runs it (`python3 -I -c "<code>"`, matching an interactive session, rather than as a saved
script, where `__file__` is naturally present and the printed line would read differently) — no change
needed to the example or its recorded result. The deck's 4 story slides sit where the explanation above
puts them: after pip (Bicking), then pipes and Norton Commander back to back right after the "quiet by
default" design slide, then the `#!` story right at the Ubuntu-launcher slides — not bunched at the
chapter's open.

---

## 4. Resources slide

- **Book:** Automate the Boring Stuff, 3rd edition, chapter 12 — https://automatetheboringstuff.com/3e/chapter12.html
- **Python docs:** `sys` — https://docs.python.org/3/library/sys.html; `os` — https://docs.python.org/3/library/os.html; `argparse` — https://docs.python.org/3/library/argparse.html; `venv` — https://docs.python.org/3/library/venv.html; `shutil.which`/`shlex.split` — https://docs.python.org/3/library/shutil.html
- **PEP 668:** externally managed environments — https://peps.python.org/pep-0668/
- **pip user guide:** running pip as `python -m pip` — https://pip.pypa.io/en/stable/user_guide/
- **PyInstaller manual:** https://pyinstaller.org/en/stable/usage.html
- **Third-party packages used:** `Bext` on PyPI — https://pypi.org/project/Bext/; `PyMsgBox` on PyPI — https://pypi.org/project/PyMsgBox/
- **Video:** AT&T Archives, "The UNIX Operating System" (1982) — background on the pipes/Unix-philosophy story.

No correctness check was needed here — nothing about the four stories or their dates was in question
this time.

---

## 5. Open items (not blocking the render; named so they are not lost)

1. **No legacy duplicate found:** unlike chapter 11 (and chapters 9-10 last week), no YA-suffixed
   legacy deck under the old edition's numbering covers command-line programs, terminal use, or
   deployment. Nothing to decide here.
2. **No research/ABox retrofit gap:** chapter 12's structural retrofit (`TK_Ret_Ch12_Research`/`_Verify`/
   `_Page_Build`/`_Page_Verify`/`_Deck_Build`/`_Deck_Verify`) is already Done (2026-10-25/26). Nothing
   carried forward.
