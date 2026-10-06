# SEN0414 chapter 4 deck v2.0.0 - the three-role review record

Same method and standard as chapters 1-3 (CME materials look-and-feel v1.0.0, shared renderer,
>>> chip). First cycle over the chapter-4 classroom redesign (25 slides).

## The academician's build notes
- Program-first by design: 17 whole programs with transcripts carry the chapter - def/call/
  return, parameters, the mutable-default trap AND its repair, the stack photographed from
  inside (inspect), the recursion rail, scope traced across three frames, the famous
  UnboundLocalError on its own slide, global/nonlocal, try inside-vs-outside, PEP 758's bare
  except pair, Collatz with fed input, input validation, deferred annotations.
- VERSION TRUTH, both directions: the chapter demos a 3.14-only feature (PEP 758), so the whole
  recording was re-executed under an installed Python 3.14.6 (examples_out_v1_2_0.json) and the
  checks run under that same interpreter; the slide says so, and the same file is a SyntaxError
  under 3.13 - both observed in this build.
- program_check stepped to v2.0.1: input-fed programs compare correctly (the recorder weaves
  typed input into transcripts; the checker now removes each woven input before comparing a
  fresh run's stdout). Chapters 2-3 re-verified under the new checker, unchanged.
- Three 5N1K stories with fact rows and live links: Wheeler's 1952 closed subroutine (the EDSAC
  photograph, CC BY 2.0), the Collatz conjecture honestly presented as open since 1937, and
  PEP 758's arrival demonstrated rather than quoted.

## The expert reviewer's checklist and findings
| check | result |
|---|---|
| Numbered slides; warm-ivory; agenda ranges; summary; takeaway strips | pass |
| Word gates; cue-style notes | pass |
| Whole programs labelled with name-and-lines; transcripts shown and re-executed | pass |
| No wrapped code (pre-build audit against the recording) | pass |
| Stories 5N1K; licences in ASSETS_PROVENANCE_v1_0_0.md | pass |
| deck_check (5 rows) + program_check v2.0.1 (17 panels) + layout check | 0 mismatches; clean |

## The undergraduate's read-through (contact sheets of slides 9, 10, 13, 20)
- FOUND and fixed: three panels wider or taller than their first placement (audit before
  render); input-program verification itself (the checker, not the slides, was wrong).
- The defaults slide finally shows the [1] / [1,2] / [1] sequence students never believe
  until they see it printed.
