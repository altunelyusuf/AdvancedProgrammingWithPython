# SEN0414 chapter 3 deck v4.0.0 - the three-role review record

Same method and standard as chapters 1-2 (CME materials look-and-feel v1.0.0, shared renderer,
>>> chip). First cycle over the chapter-3 classroom redesign (21 slides).

## The academician's build notes
- Arc: repeating (the Gauss legend, honestly labelled as a traced legend, with the loop and the
  closed form agreeing on 5050; while-vs-for shown as two whole programs printing the SAME
  transcript; Dijkstra's EWD831 under range's half-open rule; laziness measured) -> sequences
  (lists/tuples/dicts under one loop; enumerate and zip ending hand-counting) -> loop control
  (break, nested loops, and the iter/next machinery under every for) -> modules (the Mersenne
  Twister's 1997 birth inside random; namespaces; import errors read aloud).
- Three 5N1K stories with fact rows, live links and licensed portraits: Gauss (Jensen 1840,
  PD), Dijkstra (Hamilton Richards, CC BY-SA 3.0), and Matsumoto-Nishimura's generator.
- Environment truth: the whole recording re-executed on the build interpreter
  (examples_out_v2_1_0.json, 31 sessions and 41 programs under 3.13.16) before building.
- Checker reuse across chapters: ../ch02-deck/deck_check_v1_0_1.py (58 console rows) and
  ../ch02-deck/program_check_v2_0_0.py (8 program panels: verbatim slices + transcripts
  re-executed) both pass with 0 mismatches; layout check clean.

## The expert reviewer's checklist and findings
| check | result |
|---|---|
| Numbered slides; warm-ivory; agenda ranges; summary; takeaway strips | pass |
| Word gates; cue-style notes | pass |
| Consoles and whole programs labelled, results/transcripts shown | pass |
| No wrapped code (width and height gates; a pre-build audit sizes every panel) | pass |
| Stories 5N1K; licences in ASSETS_PROVENANCE_v1_0_0.md | pass |
| deck_check + program_check + layout check | 0 mismatches; clean |

## The undergraduate's read-through (contact sheets of slides 5, 7)
- FOUND and fixed: four panels sized under their line counts (the audit script now computes
  every panel's minimum from the recording before any build); narrow program captions wrapped
  in the pessimistic model (compact caption box deepened, font stepped to 7.5).
- The while/for pair with identical green transcripts is the chapter's thesis in one slide.
