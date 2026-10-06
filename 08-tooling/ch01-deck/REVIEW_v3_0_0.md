# SEN0414 chapter 1 deck v3.0.0 - the three-role review record

The owner's three-role method, carried over from the SEN0401 chapters: an experienced
programming-teaching academician prepares, an expert faculty specialist reviews, an
undergraduate reads for comprehension. First cycle over the chapter-1 classroom redesign
(23 slides), which brings SEN0414 onto the CME materials look-and-feel standard v1.0.0 - the
same warm-ivory tokens as the SEN0401 decks, drawn by this repo's shared renderer
08-tooling/deck_render_v1_0_0.js with the course's own >>> chip.

## The academician's build notes
- Arc: values and types (the REPL loop; type(); 2**100 exact; int/float mixing) -> operations
  (the -3 ** 2 trap, division three ways, 0.1 + 0.2 shown honestly, string algebra with its
  TypeErrors as first-class results) -> names and functions (variables, NameError as an honest
  answer, the free toolbox, conversions that refuse) -> the environment (CPython interrogated
  live, version tuple from the build interpreter itself, PEP 703's lock question answered by
  THIS interpreter, modules).
- Three 5N1K stories with fact rows and live links: Python's 1989 Christmas birth (Guido's
  CC BY-SA portrait, credit on-slide), the free-online textbook (the course pins the 3rd
  edition), and PEP 703 free-threading - with the gil console reading the interpreter's own
  answer.
- Environment rows are environment-TRUTH: the examples were re-executed on this build box
  (examples_out_v1_2_0.json, Python 3.13.16) so version and GIL answers are what the machine
  actually said, and deck_check re-runs every '>>>' row off the finished file.
- The resources slide links only sources the chapter's own sources file records and checked.

## The expert reviewer's checklist and findings
| check | result |
|---|---|
| Numbered slides; warm-ivory; agenda with exact ranges; summary; takeaway strips | pass |
| Word gates; cue-style notes (SAY/ASK/FULL TEXT) | pass |
| Every console labelled, result shown; errors exactly as Python raised them | pass |
| No wrapped code (width AND height gates in the builder) | pass |
| Stories 5N1K; licences on-slide and in ASSETS_PROVENANCE_v1_0_0.md | pass |
| deck_check (63 examples re-run off the finished file) and layout check | 0 mismatches; clean |

## The undergraduate's read-through (contact sheets of slides 1, 2, 6, 10, 15, 19)
- FOUND and fixed: one console sized under its line count; the title-slide console was silently
  dropped by the renderer's title path (title slides now accept code panels); version strings
  were pinned to a stale interpreter (now derived from the run itself).
- The precedence slide's -9 next to 9 does in one glance what a paragraph never could.
- The PEP 703 slide turns "modern practice" from a bullet into a measurement.
