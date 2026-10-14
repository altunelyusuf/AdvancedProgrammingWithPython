# Threads page assets - provenance and licences (v1.0.0)

The Threads page (file slot 25, material of the 2nd edition's chapter 17) runs the page's own playground in the browser (Pyodide 0.28.2, CPython 3.13.2). **No wheel, no Pyodide package and no book file is embedded.**
A browser's Python cannot start programs or threads, so every example of the chapter is shown as recorded, not run.

| item | on the page? | licence | why |
|---|---|---|---|
| one PNG picture (skipped.png: the comics a downloader skipped) | yes, as a recorded picture, SHA-256 checked when the page is made | drawn by the deck's program fixedCut_v1_0_0.py with a small PNG writer written for the course (no Pillow) from a run against a local stand-in server; the course's own licence applies | the page shows what the recorded program drew |
| requests 2.34.2, beautifulsoup4 4.15.0 | no | not redistributed | the downloader examples need sockets and a server, which a browser's Python does not have |
| the free-threaded and other interpreter builds (3.14.6t, 3.13, 3.12, 3.11) | no | not redistributed | programs of the machine the research ran on |
| the book's online materials | no | **open question**: the licence of the book's downloadable files is not established | the page embeds no file of them |
| xkcd.com | no | never contacted | a local HTTP server on 127.0.0.1 stood in for it; no comic was fetched or shown |

Library and interpreter versions differ between the recording and the browser (the browser has Python 3.13.2 and none of the packages above).
