"""SEN0414 chapter 12 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Four
stories for Designing and Deploying Command Line Programs, written fresh for this chapter from sources read on
2026-10-11:

* McIlroyPipes1973 - Doug McIlroy proposed the pipe in a 1964 memo, and Ken Thompson
  added pipes to Version 3 Unix at Bell Labs in 1973 'in one feverish night'; McIlroy's 1978 maxims for the Unix
  philosophy, among them 'Don't clutter output with extraneous information', are the rule behind the chapter's advice
  to keep a command quiet unless --verbose asks for more.
* RitchieShebang1980 - Dennis Ritchie announced kernel support for #! at Bell Labs in an email dated 10 January 1980,
  telling users to put #! /bin/sh at the start of their shell scripts; the line the chapter's Ubuntu launcher starts
  with, #!/usr/bin/env bash, is that feature.
* SochaNortonCommander1986 - John Socha began a two-panel file manager for MS-DOS in 1984, first called Visual DOS,
  which Peter Norton Computing released as Norton Commander in 1986; it is the text-based user interface of the
  chapter's Figure 12-1.
* BickingPip2008 - Ian Bicking, who had already written virtualenv, announced pyinstall on 24 September 2008 and
  renamed it pip on 28 October 2008; PEP 405 (Carl Meyer, created 13 June 2011) made virtual environments part of
  Python 3.3 as the venv module, crediting virtualenv.

No photographs: Wikimedia Commons answered HTTP 429 from this session's egress IP on 2026-10-11 (see
ch12-page/stories_img_v1_0_0.json). Usage: import STORIES; run the file for self-checks.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "McIlroyPipes1973",
        "title": "Pipes and the quiet command: Bell Labs, 1973",
        "when": "1973",
        "who": "Doug McIlroy and Ken Thompson",
        "where": "Bell Labs, Version 3 Unix",
        "link": "https://en.wikipedia.org/wiki/Pipeline_(Unix)",
        "concepts": ["SoundAndTextNotification"],
        "story": ("Doug McIlroy, head from 1965 to 1986 of the Bell Labs Computing Techniques Research Department, the "
                   "birthplace of Unix, had proposed the concept of a pipe in a 1964 memo, the output of one program "
                   "becoming the input of the next. In 1973 Ken Thompson added the pipe() system call and pipes to the shell and "
                   "several utilities of Version 3 Unix, in what McIlroy called one feverish night, and the next day "
                   "saw, in McIlroy's words, an unforgettable orgy of one-liners as everybody joined in the "
                   "excitement of plumbing. In the 1978 Bell System Technical Journal foreword, McIlroy and his two "
                   "co-authors wrote down the maxims of the style: make each program do one thing well, expect "
                   "the output of every program to become the input to another, as yet unknown, program, and do not "
                   "clutter output with extraneous information. That last maxim is the chapter's advice to keep a "
                   "command silent by default and print more only when --verbose asks for it."),
        "lesson": "Quiet by default: every command's output may feed another, McIlroy, 1973",
        "source": ("'Douglas McIlroy', Wikipedia (head of the Computing Techniques Research Department, 1965-1986); "
                    "'Pipeline (Unix)', Wikipedia, en.wikipedia.org/wiki/Pipeline_(Unix) (McIlroy's 1964 memo; Thompson's "
                    "pipe() in Version 3 Unix, 1973; the | notation in Version 4); 'Unix philosophy', Wikipedia "
                    "(M. D. McIlroy, E. N. Pinson and B. A. Tague, 'Unix Time-Sharing System: Foreword', Bell System "
                    "Technical Journal, 8 July 1978, pp. 1902-1903)."),
    },
    {
        "id": "RitchieShebang1980",
        "title": "The #! line was announced by email on 10 January 1980",
        "when": "1980-01-10",
        "who": "Dennis Ritchie",
        "where": "Bell Laboratories, between Edition 7 and Edition 8 Unix",
        "link": "https://en.wikipedia.org/wiki/Shebang_(Unix)",
        "concepts": ["ShebangLine"],
        "story": ("Dennis Ritchie added kernel support for interpreter directives at Bell Laboratories between "
                   "Edition 7 and Edition 8 of Unix, and announced it in an email dated Thursday, 10 January 1980: if "
                   "a file being executed begins with the magic characters #!, the rest of the line names the "
                   "interpreter that runs it. He advised users to put #! /bin/sh at the left margin of the first line "
                   "of their shell scripts, noting that a complete pathname was needed because no search was done. "
                   "Since Edition 8 was never publicly released, the feature reached most users through Berkeley's "
                   "BSD, appearing in 2.8BSD and enabled by default in 4.2BSD. Asked in 2009 what the construction "
                   "was called, Ritchie replied that he could not recall it ever being given a proper name; the "
                   "later form #!/usr/bin/env bash, the first line of the chapter's Ubuntu launcher, adds the PATH "
                   "search his first version left out."),
        "lesson": "The launcher's first line is Ritchie's 1980 #! feature, searching PATH through env",
        "source": ("'Shebang (Unix)', Wikipedia, en.wikipedia.org/wiki/Shebang_(Unix) (Dennis Ritchie's email of "
                    "10 January 1980; 2.8BSD and 4.2BSD; Ritchie's 2009 reply on the name; the /usr/bin/env form)."),
    },
    {
        "id": "SochaNortonCommander1986",
        "title": "The text interface of Figure 12-1 shipped in 1986",
        "when": "1986",
        "who": "John Socha",
        "where": "Peter Norton Computing, for MS-DOS",
        "link": "https://en.wikipedia.org/wiki/Norton_Commander",
        "concepts": ["TextUserInterface"],
        "story": ("John Socha started work in 1984 on a file manager for MS-DOS that he first called Visual DOS, or "
                   "VDOS, and Peter Norton Computing released it as Norton Commander in 1986. After starting it, a "
                   "user saw two panels of file lists side by side, with a list of commands along the bottom of the "
                   "screen, a built-in viewer on F3 and an editor on F4, all drawn with text characters on a plain "
                   "MS-DOS screen. Symantec bought Peter Norton Computing in 1990, and the last MS-DOS version, 5.51, "
                   "came out on 1 July 1998. The chapter shows Norton Commander in Figure 12-1 as its example of a "
                   "text-based user interface, a style its own snowstorm program imitates with block characters and "
                   "a cleared screen."),
        "lesson": "A text interface can feel like a desktop: Socha's Norton Commander, 1986",
        "source": ("'Norton Commander', Wikipedia, en.wikipedia.org/wiki/Norton_Commander (John Socha, work begun 1984 as "
                    "Visual DOS; initial release 1986 by Peter Norton Computing; two panels; Symantec acquisition 1990; "
                    "version 5.51 on 1 July 1998)."),
    },
    {
        "id": "BickingPip2008",
        "title": "pip was announced as pyinstall on 24 September 2008",
        "when": "2008-09-24",
        "who": "Ian Bicking; later Carl Meyer for PEP 405",
        "where": "Ian Bicking's blog; the Python Enhancement Proposals",
        "link": "https://en.wikipedia.org/wiki/Pip_(package_manager)",
        "concepts": ["RunningPipAsAModule", "CreatingAVenv"],
        "story": ("Ian Bicking, who had already written virtualenv, announced a new installer called pyinstall in a "
                   "post titled 'pyinstall: A New Hope' on 24 September 2008, as an alternative to easy_install. On "
                   "28 October 2008 he renamed it in a post titled 'pyinstall is dead, long live pip!', and pip, by "
                   "Bicking's own account a recursive acronym for Pip Installs Packages, became the installer Python "
                   "now ships with. Carl Meyer then wrote PEP 405, created on 13 June 2011, which named Bicking's "
                   "virtualenv as the tool that had shown the value of isolated environments and made them part of "
                   "Python 3.3 as the venv module. The chapter's two commands, python -m venv .venv and python -m pip "
                   "install, are those two pieces of work side by side."),
        "lesson": "venv and pip grew from Ian Bicking's virtualenv and his 2008 pyinstall",
        "source": ("'pip (package manager)', Wikipedia, en.wikipedia.org/wiki/Pip_(package_manager) (Ian Bicking, "
                    "'pyinstall: A New Hope', 24 September 2008; 'pyinstall is dead, long live pip!', 28 October 2008); "
                    "PEP 405, Python Virtual Environments, Carl Meyer, created 13 June 2011, Python 3.3, "
                    "peps.python.org/pep-0405/."),
    },
]


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
    by = {x["id"]: x for x in STORIES}
    for sid, year in (("McIlroyPipes1973", "1973"), ("RitchieShebang1980", "1980"),
                      ("SochaNortonCommander1986", "1986"), ("BickingPip2008", "2008")):
        if year not in by[sid]["story"] or year not in by[sid]["when"]:
            bad.append("%s: date missing from story" % sid)
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
