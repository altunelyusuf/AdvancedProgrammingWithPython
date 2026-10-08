# SEN0414 chapter 6 deck v2.0.0 - the three-role review record

Same method and standard as chapters 1-5 (CME materials look-and-feel v1.0.0, shared renderer, the >>> chip), first cycle over chapter 6
(Lists, "Automate the Boring Stuff with Python" 3rd edition). The speaker notes follow the owner's ruling of 2026-10-08: reader's prose in
full sentences, no presenter cues. Built with `build_v2_0_0.sh /root/.local/bin/python3.14 <out.pptx>`; the old v1.0.0 deck, folder files
and page files were not touched (the new files carry v2_0_0 names).

## The academician's build notes
- Arc (26 slides): the competency questions and the six-branch concept map; the list as a value (indexes with Dijkstra's story, slices); changing,
  combining, searching and ordering (the eight-ball story); loops, the removal trap, unpacking; names and copies (aliasing, shallow and deep);
  random choices and programs (the fair-shuffle story, the digital-rain story, Comma Code, Coin Flip Streaks); summary, resources, closing.
- Every result on a slide was executed under Python 3.14.6 (`examples_run_v2_0_0.py` -> `examples_out_v2_0_0.json`): 13 console groups of 94 rows
  and 4 whole programs with their transcripts. Seeds are fixed in the programs so each transcript is reproducible.
- Three native charts, each drawn only from an executed row: the letters in each supply name (`[4, 8, 13, 7]`), the first six squares
  (`[1, 4, 9, 16, 25, 36]`), and the deviation of six thousand shuffled deals from the expected one thousand per order (`[-29, -27, 9, 14, 45, -12]`).
- Four 5N1K stories with fact rows, live links, credit lines: Dijkstra's EWD831 (photo CC BY-SA 4.0), Fisher/Yates/Durstenfeld (photo CC BY-SA 4.0),
  the Magic 8 Ball (photo CC BY 2.0), the digital rain (the book's Figure 6-5, CC BY-NC-SA). Licences: `03-materials/ch06/assets/ASSETS_PROVENANCE_v1_0_0.md`.
- Everyday analogies carried on the slides: numbered lockers, a ruler, pencil on a shopping list, a shelf of books, pigeonholes, two keys to one
  locker, a photocopied folder, reading a list aloud, a coin-flipping arm.
- Notes: `notes()` takes the opening sentences of the slide's own concept explanation from the corpus, then what to look at, one thing to consider,
  and where the full text is; story slides carry the story, its lesson and its sources. 3,549 words over 26 slides, none under 44 words.
- Differences from chapter 5: reader's-prose notes (chapter 5 still carries the old cue form), four stories, an exported `lecture_v2_0_0.json`
  for the page's Lecture tab (`lecture_export_v2_0_0.py`), and `deck_build` refuses a console that cannot fit unwrapped with a 9% width margin.

## The expert reviewer's checklist (every line is a command and its measured output)
| check | command | result |
|---|---|---|
| 20-26 numbered slides | `deck_build_v2_0_0.py` | 26 slides (21 content, 3 section, 1 title, 1 closing) |
| Agenda with exact ranges | built from the slide positions | 7 rows: 3-4, 5-8, 9-12, 13-16, 17-19, 20-23, 24-26 |
| Takeaway strips, ledes | gate in the builder (24 / 34 words) | 17 takeaways, 13 ledes, 0 refused |
| Console rows re-run off the finished file | `ch02-deck/deck_check_v1_0_1.py` (python3.14) | 60 examples re-run; 0 mismatches |
| Programs: lines verbatim, transcript re-executed and on the slide | `ch02-deck/program_check_v2_0_1.py` | 4 program panels verified; 0 mismatches |
| No wrapped code | builder refuses < 7 pt (width factor 0.0092 per pt per character) | smallest console 7.1 pt; 0 refused |
| Paragraph order PowerPoint would repair | `ch05-deck/structure_check_v1_0_0.py` | 0 |
| Layout | `deck_layout_check_v1_0_0.py` | 26 slides, 0 overflow, 0 outside, notes on every slide: clean |
| Notes in the new standard | `deck_notes_check_v1_0_0.py` | 26 slides, 26 with notes written for the reader: PASS |
| Fit (pessimistic estimate) | `deck_fit_check_v1_0_0.py` | 0 frames overflowing; 6 pairs of frames overlapping (see below) |
| The checks discriminate | `fixtures_make_v2_0_0.py` and the four fixtures | stale console result: deck_check exit 1 (1 mismatch); stale transcript: program_check exit 1; edited program line: program_check exit 1; "SAY: " cue in a note: notes check exit 1 (FAIL, slide 4) |
| Question bank | `ch06-page/question_bank_check_v2_0_0.py` | 123 items, 69/69 concepts, 123 distinct stems, positions 31/31/30/31, 54 Apply programs run under 3.14.6 and 162 cross-version runs: PASS |

The six overlapping pairs that the fit check lists are the renderer's own designs and were read by hand: the caption that sits inside a program
panel (slides 12, 21, 22, 23 - the code box and its caption share the panel by design, the builder reserves 0.56 in for them), the title slide's
subtitle frame (a wide frame, short text, the picture is clear of the text) and the closing slide's "Questions?" beside the page number. The same
check lists 29 such pairs on chapter 5's deck and 30 on SEN0401's chapter 6.

## The undergraduate's read-through (four contact sheets, `contact_sheets_v2_0_0/`, rendered with LibreOffice and looked at)
Sheet 1 slides 1-7, sheet 2 slides 8-14, sheet 3 slides 15-20, sheet 4 slides 21-26.
- FOUND and fixed: the title slide's subtitle ran into the picture; photograph and figure captions wrapped into the next element (shortened, 2 lines
  allowed, next element moved down); the strips of chips wrapped into rows and ran over the takeaway (replaced by one pill each); the Comma Code
  comment wrapped inside the program panel (comment shortened, width margin raised to 9%); consoles with few rows drew at 8 pt with half
  an empty panel (font target raised to 12 pt, the builder shrinks only when it must); the shuffle chart's axis started at 920 and made
  equal bars look unequal (the series became the deviation from 1000, so the axis includes 0); the Magic 8 Ball photograph drew as a black box
  (a Photoshop-written JPEG, re-encoded once; its picture box was also stretched, now square); the Fisher photograph box did not match its aspect.
- Left as is, by choice: the console of the shuffle story is the smallest (7.1 pt) because its lines are 60 characters in a 4.4-in panel; a
  long WHO / WHERE cell of the fact row ends in an ellipsis (the renderer truncates, the full text is in the notes).
- Read as a student: each slide can be understood without its notes (lede, labelled consoles, a takeaway strip); the removal-trap slide, where the loop
  silently leaves two letters behind, and the two names, one list slide are the memorable ones.
