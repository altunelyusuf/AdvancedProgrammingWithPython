# SEN0414 — Chapter 9 draft: Text Pattern Matching with Regular Expressions
*(3rd edition, "Automate the Boring Stuff with Python"; chapter_code_ch09_v1_0_0.json, deck SEN0414_Ch09_RegularExpressions_3e_v2_0_0.pptx, page sen0414_ch09_page_v9_90_0.html)*

**Status of this draft:** this chapter's deck (48 slides, 7 native charts, 4 story slides) and
interactive page already exist and were read against the current standard this turn (lineage
`sen0414-ch09ch10-lineage`, task `TK3_StateCheck_Ch09`). Nothing here starts from nothing — this
draft is the single approved source the next render should come from, consolidating what already
works and fixing the two gaps found: the story slot (below) was not yet pinned to real, sourced
figures with a live link, and the chapter's research/ABox retrofit against the current chapter-check
standard is still open (`TK_Ret_Ch09_Research`, carried into this lineage). Please read and correct —
nothing is rendered again until you approve this.

---

## 1. The story

In 1943, the neuroscientist Warren McCulloch and the logician Walter Pitts published the first
mathematical model of an artificial neuron — not a working machine, just a notation for thinking
about what networks of simple on/off units could, in principle, do. An American mathematician named
Stephen Kleene picked up that question in the early 1950s, working at the RAND Corporation, and asked
it more precisely: exactly which patterns can such a network ever recognize? To answer it, he needed
a way to write those patterns down algebraically rather than draw a diagram for every one of them. In
a 1951 research memorandum, polished into its final published form by 1956, he called the patterns
"regular events" and gave them a compact symbolic notation — the first regular expression. Kleene
never touched a text editor; he was doing pure theory of computation, decades before anyone thought
to point this algebra at a string of characters on a screen.

That jump — from an abstract theory of neural networks to a tool programmers actually type — took
another generation. By the 1990s, Larry Wall had built that same notation directly into the working
syntax of Perl, turning Kleene's algebra into something a line of code could execute. Python's `re`
module is a direct descendant of that Perl syntax: the `.`, `*`, `+`, character classes and groups a
student types in this chapter are, almost unchanged, Kleene's 1951 algebra, inherited through Perl.
It's worth pausing on that lineage when the chapter reaches `compile()` and `search()` — the dense
little punctuation a beginner finds intimidating is, quite literally, seventy-year-old mathematics
doing exactly the job it was invented for.

**Picture and source (asset already on file):** `assets/photo_stephen_kleene.jpg` — provenance in
`assets/ASSETS_PROVENANCE_v1_0_0.md`. **Live link:**
https://student.cs.uwaterloo.ca/~cs360/Hall/kleene.html (Univ. of Waterloo's Theory of Computing Hall
of Fame entry; cites Kleene's 1956 paper directly). Second picture on file,
`assets/photo_larry_wall_2007.jpg`, for the Perl half of the story.

*(The deck's third story asset, `assets/photo_ken_thompson_2019.jpg`, is Ken Thompson — his 1968 `ed`
and `grep` work is the direct bridge between Kleene's algebra and Unix text tools, and belongs on the
slide between the Kleene and Wall slides if a third story beat is wanted; keeping it as background
only, inside the two-beat story above, unless you want three.)*

---

## 2. Explanations (what each block of the chapter earns, in plain language)

- **Why not just string methods:** `isdecimal()`/slicing can check one fixed shape (12-character
  dashed phone numbers); the moment a pattern has variation, hand-written checks grow one `if` per
  variant. This is the motivating gap regular expressions close.
- **The core workflow:** `re.compile(pattern)` once, then `.search()`/`.match()`/`.fullmatch()` on as
  many strings as needed; a `Match` object (not a string) comes back, and `.group()` pulls the text
  out.
- **Grouping:** parentheses both capture a sub-match *and* scope an alternative or a repeat; numbered
  groups are positional and fragile to reorder, which motivates named groups (`(?P<name>...)`) and
  back-references.
- **Character classes and shorthand:** `[...]`, `\d`, `\w`, `\s` and the dot are all the same idea —
  "one character from this set" — at different levels of abbreviation.
- **Repeats:** `?`, `*`, `+`, `{m,n}` are one idea (how many times) with greedy as the default and `?`
  suffixed to make any of them non-greedy; this is where most beginner regex bugs live, so the
  greedy-vs-non-greedy example is worth lingering on.
- **Anchors and boundaries:** `^`/`$` anchor to the string, `\b` anchors to a word edge — the
  distinction matters because `\b` is about context, not position.
- **Look-ahead/look-behind:** a way to require context without consuming it — introduced only after
  groups and anchors, since it is notation built on both.
- **findall/finditer/sub/split:** the four things you actually do once a pattern is right — find all,
  find all lazily, replace, cut.
- **Flags (`IGNORECASE`, `DOTALL`, `VERBOSE`) and combining them:** `VERBOSE` is presented as how a
  professional keeps a real pattern (like the phone/e-mail one) readable, not a toy.
- **Capstone:** the phone-and-e-mail pattern is built up group-by-group from everything above, then
  used in a small project, closing the loop from "can't express this with string methods" back to a
  real, working extraction tool.

---

## 3. Slide / page-tab outline (existing deck order, slide order = page tab order; unchanged — this
is a confirmation, not a rebuild)

| # | Slide | Code example (name, from the manifest) |
|---|---|---|
| 1 | A phone number checked by hand (the motivating gap) | *A phone number checked by hand* |
| 2 | compile, search and the Match object | *compile, search and the Match object* |
| 3 | match, search and fullmatch | *match, search and fullmatch* |
| 4 | Groups and numbers | *Groups and numbers* |
| 5 | The pipe: alternatives | *The pipe: alternatives* |
| 6 | Named groups and back references | *Named groups and back references* |
| 7 | Character sets | *Character sets* |
| 8 | Shorthand classes and the dot | *Shorthand classes and the dot* |
| 9 | Optional, star and plus | *Optional, star and plus* |
| 10 | Exact counts with curly brackets | *Exact counts with curly brackets* |
| 11 | Greedy and non-greedy matching | *Greedy and non-greedy matching* |
| 12 | Start and end anchors | *Start and end anchors* |
| 13 | Word boundaries | *Word boundaries* |
| 14 | Look-ahead and look-behind | *Look-ahead and look-behind* |
| 15 | findall and its shapes | *findall and its shapes* |
| 16 | finditer and split | *finditer and split* |
| 17 | Substituting with sub | *Substituting with sub* |
| 18 | sub with a function, escape and subn | *sub with a function, escape and subn* |
| 19 | Ignore case and DOTALL | *Ignore case and DOTALL* |
| 20 | Verbose mode | *Verbose mode* |
| 21 | Combined flags | *Combined flags* |
| 22 | The phone pattern, group by group | *The phone pattern, group by group* |
| 23 | Project 3: phone numbers and e-mails | *Project 3: phone numbers and e-mails* |
| 24 | Strong-password check | *Strong-password check* |
| 25 | regex_strip() | *regex_strip()* |

All 25 examples already run under the standard library only and reproduce their recorded output
(e.g. example 1 prints `True False` then the two matched phone numbers); nothing here needs a code
change. Story slides sit at the open (Kleene) and a mid-chapter beat (Wall), per the deck's 4
story-image assets.

---

## 4. Resources slide

- **Python docs:** `re` module — https://docs.python.org/3/library/re.html
- **Community:** regex101.com (interactive tester the deck's examples can be pasted into) —
  https://regex101.com/
- **Seminal work:** S. C. Kleene, *Representation of Events in Nerve Nets and Finite Automata* (1956)
  — cited via the Waterloo Hall-of-Fame page above.
- **Tutorial/video:** Corey Schafer, "Python Tutorial: re Module" (YouTube) — a widely used, current,
  free walkthrough matching this chapter's scope.

---

## 5. Open items (not blocking the render; named so they are not lost)

1. **Carried-forward gap:** `TK_Ret_Ch09_Research` / `_Verify` (research set + page ABox against the
   current chapter-check standard) are still `Ready`, not `Done`. This is ontology/back-end work, not
   visible on the deck or page, and does not block teaching from this draft — but it is open and
   should be scheduled once chapters 9-10 ship.
2. **Legacy duplicate:** `03-materials/slides/Chapter7PatternMatchingWithRegularExpressions_YA_v1_0_0.pptx`
   duplicates this chapter under the old edition's numbering. Recommend retiring it; this is named as
   an owner decision in the lineage backlog (`ST3_YaRetirement`), not acted on here.
