# Chapter 24 page assets - provenance and licences (v1.0.0)

The chapter 24 page runs the page's own playground in the browser (Pyodide 0.28.2, CPython 3.13.2). **No wheel, no Pyodide package, no model file and no book file is embedded.**
A browser has no speech engine, cannot start programs and does not have pyttsx3, Whisper or yt-dlp, so every example of the chapter is shown as recorded, not run.

| item | on the page? | licence | why |
|---|---|---|---|
| five PNG pictures (waves, hello, audio16k, cues, song) | yes, as recorded pictures, SHA-256 checked when the page is made | drawn by the deck's own programs with a small PNG writer written for the course (no Pillow), from audio that eSpeak NG 1.51 spoke through pyttsx3 2.99 and, for audio16k, that ffmpeg 6.1.1 resampled; the course's own licence applies to the drawings; eSpeak NG is GPL-3.0-or-later and the pictures show waveforms of its output only, which is not the program; whether a waveform of GPL software output carries any obligation is an open question of low risk | the page shows what the recorded programs drew |
| pyttsx3 2.99, openai-whisper 20250625, yt-dlp 2026.8.19, torch 2.14.1, NumPy 2.5.4 | no | not redistributed | not available to a browser's Python |
| the Whisper model files (tiny to large-v3, 75 MB to 3 GB) | no | not redistributed | far too large for a page, and not loadable in a browser's Python here |
| eSpeak NG, ffmpeg, aplay | no | not redistributed | programs of the machine the research ran on |
| the book's online materials (a zip of 7,759,877 bytes with 91 files; hello_tts.py is the one that imports pyttsx3) | no | **open question**: the licence of the zip and of its files is not established | the page embeds no file of them |
| LibriVox recordings of the Gettysburg Address on archive.org (the stand-in for YouTube) | no | public-domain recordings, not embedded; the research read their metadata and transcribed them locally | only the recorded results are shown |

Library versions differ between the recording and the browser (the browser has none of the packages above).
