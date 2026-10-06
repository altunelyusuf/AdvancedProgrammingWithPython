# SEN0414 chapter 2 deck v3.0.0 - the three-role review record

Same method and standard as chapter 1 (CME materials look-and-feel v1.0.0, shared renderer,
>>> chip). First cycle over the chapter-2 classroom redesign (22 slides).

## The academician's build notes
- Arc: Boole's two-valued algebra (his PD portrait; bool, comparisons, chaining, truthiness) ->
  combining conditions (truth tables sampled; short-circuiting shown surviving a 1/0, console
  AND program) -> branching (the two five-line indentation programs printing different stories;
  the whole password program with its transcript; elif ladders) -> patterns, style, errors
  (match's 2021 arrival with the command and guard programs; the walrus probed at its edges;
  four error types as first-class results).
- WHOLE PROGRAMS join the discipline: each panel is captioned 'program <name>, lines a to b of
  n' and program_check_v2_0_0.py (new) re-executes every one with its recorded inputs,
  requiring the shown lines to be a verbatim slice AND the transcript to match both the
  recording and the slide. deck_check_v1_0_1.py still re-runs every '>>>' row.
- Environment truth held again: Python 3.14 unified two ZeroDivisionError messages, so the
  recording was re-executed on the build interpreter (examples_out_v1_2_0.json, 3.13.16) and
  the slides show what THIS machine actually printed.
- Three 5N1K stories with fact rows and live links: George Boole (1847/1854), the indentation
  design decision (Python's own design FAQ, ABC lineage), and match's acceptance (PEPs 634-636,
  February 2021, shipped in 3.10).

## The expert reviewer's checklist and findings
| check | result |
|---|---|
| Numbered slides; warm-ivory; agenda ranges; summary; takeaway strips | pass |
| Word gates; cue-style notes | pass |
| Consoles AND whole programs labelled, results/transcripts shown; errors as raised | pass |
| No wrapped code (width and height gates, transcript lines counted) | pass |
| Stories 5N1K; licences in ASSETS_PROVENANCE_v1_0_0.md | pass |
| deck_check (44 examples), program_check (9 panels), layout check | 0 mismatches; clean |

## The undergraduate's read-through (contact sheets of slides 6, 11, 13, 16)
- FOUND and fixed: five consoles and two program panels sized under their line counts
  (transcript lines now counted in the gate); two stale 3.14-era error messages caught by the
  checker and resolved by re-recording, never by editing text.
- The side-by-side indentation programs settle the chapter's most argued point in one glance.
- The password panel's green transcript under the code is the pattern students asked for:
  the program and what it actually printed, together.
