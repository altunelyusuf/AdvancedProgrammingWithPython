# Lineage14 — chapter 24 release record and three-role review (2026-11-27)

Released: deck 4.0.0 (`03-materials/ch24/SEN0414_Ch24_MakePythonTalk_3e_v4_0_0.pptx`, 42 slides, 16 code slides, 5 native charts), chapter-code manifest 1.1.0, page 9.111.0, page A-box 9.111.0, domain A-box 1.0.3, lecture file 4.0.0, stories 2.0.1, deck builder 2.11.0, page builder 4.19.0. Reading of "21–25": the five incoming chapters; the early chapters follow after this lineage.

## What was measured (logs in `08-tooling/lineage14-opening/ch24_deck_4_0_0/` and `ch24_page_9_111_0/`)
| Check | Result |
|---|---|
| Deck checks (standard, fit, layout, notes, overlap, reader notes, story prose) | all zero |
| Material check (deck and page) | 8 of 8 pass, no lambda on the page |
| Page test 9.42.0 on 9.111.0 | 412 pass, 0 fail, widgets 104 of 104 |
| Page shapes | conform |
| Lambda-free A-box | 74 of 74 equal |
| Story-repeat control | clean |
| Links | 13 of 16 answered 200; the three github.com pages answered 403 from the session's access policy and could not be checked |
| Version check | exit 0 |

## Faults found, and what was done
1. Wikimedia refused further requests ("too many") for about an hour; the last pictures came in standard thumbnail sizes after waiting, with the same identifying agent throughout.
2. The Daisy Bell picture first chosen showed an IBM 704; Wikipedia names an IBM 7090, so the 7090 picture was fetched and the 704 one removed.
3. Notes quoted numbers of an earlier run (word error rates, sample counts, durations). They were compared with the final run and corrected; two builds in a row gave the same results.
4. Five slides failed the deck checks (two short titles, an overflowing text, a table touching the slide number, two notes without a connection phrase); fixed and rebuilt.
5. The lambda-free A-box maker dropped the statement before `out = …` when both stood on one line (4 of 74 inputs differed); fixed. One input held a lambda inside a program text run by a child process; it became a def. Some inputs need a pinned-release environment (Python 3.12 with pyttsx3 2.98 and openai-whisper 20231117) and an empty one; both were created.
6. The page builder refused the page because SRT times (`-->`) unbalanced its comment guard; builder 4.19.0 writes that sign as an escape (JSON escape in page data, Turtle escape in the corpus blocks).
7. The first page-data run wrote its working files into the repository root; they were moved out and the page data was made again from a clean folder.
8. The Stories tab had no jump links because the stories listed no concepts; stories 2.0.1 names two concepts each.

## Honest limits
Owner has not opened deck or page. LibreOffice rendering only. The examples ran on this machine only, with no sound card, Windows or macOS. An archive.org reading stands in for YouTube; nothing was downloaded from YouTube. Story facts were read from Wikipedia pages (HTML) with the identifying agent. The deck has 42 slides against the agreed about 34 to 40. The five concept pictures under the page's concepts come from the first deck's run; their captions were cleared of the numbers that differ. Build environments gained packages (torch, whisper, yt-dlp, pyttsx3, rdflib, python-pptx, two pinned/empty Python environments) and the apt tools espeak-ng and ffmpeg; a symbolic link AdvancedProgrammingWithPython points to the repository because inputs of the first research name that path.
