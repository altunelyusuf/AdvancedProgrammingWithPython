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

**Second correction (2026-11-09):** the deck's own story companion,
`08-tooling/sen0414_ch09_stories_v1_0_0.py` (self-check: 4 stories, 0 failures), already carries four
real, sourced stories matching the 4 story-image assets in `assets/ASSETS_PROVENANCE_v1_0_0.md` —
Kleene (1951), Thompson's 1968 regex-search algorithm, Wall/Perl (1987), and Secret Labs' `_sre.c`
engine (1999). My first two passes only used Kleene and Wall, and conflated Thompson's role with
McCulloch and Pitts' unrelated 1943 neuron model, which isn't part of this companion at all. Corrected
below to all four, in the order the chapter teaches them. The ancient-automata material you asked me
to fact-check (Hero of Alexandria, al-Jazari) stays, as short framing before Kleene — it's accurate and
you approved weaving it in — but it is not one of the deck's four story slides and needs no new image
asset; it is prose context, not a fifth slide, consistent with fitting new story material within the
chapter's existing scope rather than expanding it.

**Build status (2026-11-09, owner approved):** checked the actual deck and page against this draft —
both already carry the correct four stories (Kleene, Thompson/1968, Wall/Perl, `_sre.c`/1999), each with
its real asset and live link; nothing differed, so nothing was re-rendered and no new version was cut
(`cme_version_check_v1_0_0.py` exit 0). `ST3_ApprovalGate` and `ST3_RenderCh09` are Done in the lineage.
The ancient-automata framing stays unrendered — a new slide and new images would be needed, which is a
separate decision.

**Decision (2026-11-10):** attempted to source the two needed images from Wikimedia Commons; the
al-Jazari manuscript folio (`File:Al-Jazari - A Musical Toy.jpg`) was found and confirmed Public Domain
via the Commons API, but every download (api.php and direct file fetch, waits up to 60s) returned
HTTP 429 from this environment's shared proxy — no Hero image was even reached. Asked; owner decided to
drop the fifth slide for this week rather than hold the chapter on an external rate limit
(`ST3_AncientAutomataSlide`, Cancelled). Ch09 ships as its existing, already-correct four-story deck,
unchanged. `TK_Ret_Ch09_Research`/`_Verify` (the document/ABox retrofit) is still open, same as before,
and doesn't block anything delivered this week.

---

## 1. The story

Machines that could only ever behave in a fixed, finite repertoire of ways existed long before anyone
had a name for what kind of machine that was. Around the first century CE, the Alexandrian engineer
Hero built a self-propelled cart whose entire routine — how far it rolled, when it turned, even
reversing itself — was set by the order twine was wound around its axle. Eleven centuries later, in
1206, the engineer al-Jazari built automated musicians on a boat whose drummer could be made to play
entirely different rhythms by moving the pegs on a rotating drum. Neither man had, or needed, any
mathematics for what he'd built; the pegs and cams simply were the program, and nobody could yet say
exactly what kind of machine that made, or where its limits were. *(Framing only — not one of the
deck's four story slides, no new image asset needed; see the note below.)*

That question got a precise answer in 1951. Working for the RAND Corporation in Santa Monica, the
mathematician Stephen Cole Kleene wrote "Representation of Events in Nerve Nets and Finite Automata,"
defining what he called a regular event: a set of symbol sequences built from single symbols by
exactly three operations — concatenation, union and repetition. The union is exactly the pipe this
chapter calls alternation, `Cat(erpillar|astrophe|ch|egory)`, and the repetition is exactly the `*`
and `+` quantifiers; every pattern string this chapter writes is, formally, one more instance of the
object Kleene named seventy-four years before Python compiled it. Kleene, born in Hartford,
Connecticut in 1909, spent almost his whole career at the University of Wisconsin–Madison and died in
1994; he never touched a text editor — this was pure theory of computation, worked out for the
abstract neuron model McCulloch and Pitts had published in 1943, decades before anyone pointed the
algebra at a string of characters on a screen. His "regular events" also turned out to sit at the very
bottom rung of the Chomsky hierarchy of formal languages (1956): regular languages, Type-3, the
simplest class, recognizable by a finite automaton with no memory at all — which is the honest, proven
reason regex can't match balanced parentheses or a programming language's full grammar; it's a
theorem, not a limitation of Python's `re` module.

Seventeen years later, in June 1968, Ken Thompson published "Regular Expression Search Algorithm" in
*Communications of the ACM*, describing an algorithm that compiles a regular expression into machine
code once and then uses that compiled form to search text — simulating a non-deterministic finite
automaton to do it. Thompson had already built that same two-step shape into the QED text editor he
wrote for Bell Labs, the first editor to add regular expressions to a text search at all, and later
received a US patent for the technique. The chapter's own `re.compile()` for a `Pattern` object,
followed by `.search()` for a `Match`, is the same two steps fifty-seven years later — a method call
apart now instead of a step in an editor's command loop.

The shorthand a student actually types — `\d`, `\w`, `\s` — came later still, and from a different
direction entirely. Larry Wall released Perl 1.0 on 18 December 1987 while working as a programmer at
Unisys, and Perl 2, in June 1988, shipped a markedly better regex engine built around exactly these
backslash classes, together with their capitalized opposites. Perl's regex strength carried it to wide
popularity as a web scripting language through the 1990s, and the shorthand travelled with it into
most regex engines written afterward — which is why Python's own `re` documentation still opens by
saying it provides matching operations similar to those found in Perl, one sentence that ties this
chapter's `\d+\s\w+` straight back to 1987.

The engine actually doing the work underneath `re`, though, is younger than any of that. Python's
`_sre.c`, the C source behind every `Pattern` and `Match` object this chapter hands back, carries a
history log inside its own comments opening on 24 October 1999, crediting the initials "fl" for most
of the early engine and naming a small Swedish company, Secret Labs AB, as copyright holder. The same
log records Hewlett-Packard funding the work needed to fold the engine into Python 1.6 and Guido van
Rossum himself fixing a memory leak in `sub()` and `subn()`. Every `mo.group()` and `mo.span()` this
chapter calls reaches, underneath, into an engine whose own change log is now a quarter of a century
old.

**Pictures and sources (three of the deck's four story-image assets already on file, per
`assets/ASSETS_PROVENANCE_v1_0_0.md`):** Kleene — `assets/photo_stephen_kleene.jpg`, live link
https://en.wikipedia.org/wiki/Stephen_Cole_Kleene. Thompson — `assets/photo_ken_thompson_2019.jpg`,
live link (the 1968 paper itself) https://cacmb4.acm.org/magazines/1968/6/12736-programming-techniques-regular-expression-search-algorithm.
Wall/Perl — `assets/photo_larry_wall_2007.jpg`, live link https://en.wikipedia.org/wiki/Perl. The
fourth asset, `logo_python.png`, illustrates the `_sre.c`/Secret Labs beat (no personal photo exists
for this one — it's a company, not a person); live link
https://chromium.googlesource.com/external/github.com/python/cpython/+/v3.7.0/Modules/_sre.c. The
ancient-automata framing paragraph above uses no asset of its own; if you'd like it illustrated too, it
would need a fifth slide and a new image search (Hero's cart and al-Jazari's drum are not yet on file),
which I'd treat as a separate scope decision rather than default into, given the render date.

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
change. The deck's 4 story slides carry all four beats above — Kleene, Thompson, Wall/Perl,
Secret Labs/`_sre.c` — placed through the chapter per the story companion's `concepts` field
(`Alternation`, `CompileAndSearch`, `ShorthandClasses`, `MatchObjectAccess`), i.e. near the pipe/groups
examples, the `compile()`/`search()` examples, the shorthand-class examples, and the Match-object
examples respectively — not bunched at the open.

---

## 4. Resources slide

- **Python docs:** `re` module — https://docs.python.org/3/library/re.html
- **Community:** regex101.com (interactive tester the deck's examples can be pasted into) —
  https://regex101.com/
- **Seminal work (Kleene):** S. C. Kleene, RM-704, *Representation of Events in Nerve Nets and Finite
  Automata* (RAND Corporation, 1951) — https://en.wikipedia.org/wiki/Stephen_Cole_Kleene
- **Seminal work (Thompson):** Ken Thompson, "Regular Expression Search Algorithm," *CACM* 11(6), June
  1968 — https://cacmb4.acm.org/magazines/1968/6/12736-programming-techniques-regular-expression-search-algorithm
- **Formal placement:** regular languages as the Type-3 (simplest) class of the Chomsky hierarchy —
  any standard automata-theory reference (e.g. Sipser, *Introduction to the Theory of Computation*).
- **Perl/shorthand-class history:** https://en.wikipedia.org/wiki/Perl (Perl 1.0, 18 December 1987)
- **The `_sre.c` engine:** CPython source history — https://chromium.googlesource.com/external/github.com/python/cpython/+/v3.7.0/Modules/_sre.c
- **Ancient automata referenced in the framing:** Prof. Noel Sharkey's reconstruction and analysis of
  historical programmable machines — techradar.com; background on Ismail al-Jazari's 1206
  peg-drum automated musicians — Wikipedia, "Al-Jazari."
- **Tutorial/video:** Corey Schafer, "Python Tutorial: re Module" (YouTube) — a widely used, current,
  free walkthrough matching this chapter's scope.

---

## 4a. A correctness check on the story, done at your request

You asked me to check whether the story misdirects students into thinking regular expressions were
"invented in the 20th century," pointing to algebra's much older history — Babylonian equation-solving
and al-Khwārizmī, the 9th-century Baghdad mathematician whose book title gave us the word "algebra"
itself (and whose name gave us "algorithm"). You then asked a second, related question: whether
ancient mechanically-working autonomous machines exist that are, in effect, finite automata, even
though nobody at the time could have named them that.

On the first question: al-Khwārizmī is correctly called the father of algebra — the discipline of
solving equations by named, systematic methods — and that lineage really does run back through him
to Babylonian mathematics. But a *regular expression* is a different, specific, 20th-century
mathematical object: a notation for the patterns a finite-memory machine can recognize, which Kleene
named and formalized in 1951–56 by analogy ("an algebra of regular events"), not by extending
al-Khwārizmī's algebra of equations. No source ties the two together — searched for one directly and
found none; the word "algebra" is the only thing they share. Telling students al-Khwārizmī anticipated
regex, or that regex descends from Babylonian mathematics, would be the misreading, not a fix for one.

On the second question: yes, correct, and that's now the fix worked into the story itself above
(Hero's cart, al-Jazari's peg-drum musicians) rather than kept separate here — a cam drum or peg
sequence is, structurally, a finite automaton with no memory beyond its current position, running
for two thousand years before anyone could say so or state its limits precisely. What belongs here,
and doesn't duplicate the story, is just the one remaining loose thread: if you'd like a one-line
etymological aside noting that the word "algebra" itself (not regex) comes from al-Khwārizmī's
*al-jabr*, I can add that too, clearly marked as being about the word only.

## 5. Open items (not blocking the render; named so they are not lost)

1. **Carried-forward gap:** `TK_Ret_Ch09_Research` / `_Verify` (research set + page ABox against the
   current chapter-check standard) are still `Ready`, not `Done`. This is ontology/back-end work, not
   visible on the deck or page, and does not block teaching from this draft — but it is open and
   should be scheduled once chapters 9-10 ship.
2. **Legacy duplicate — closed (2026-11-09):** you decided to retire it now. `Chapter7PatternMatchingWithRegularExpressions_YA_v1_0_0.pptx`
   has been removed from `03-materials/slides/` (recoverable from git history); `ST3_YaRetirement` is Done.
