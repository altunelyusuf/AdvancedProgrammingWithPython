# Chapter 22 page assets - provenance and licences (v1.0.0)

The chapter 22 page runs the chapter's Python in the browser (Pyodide 0.28.2, CPython 3.13.2). There is no Tesseract program, no PyAutoGUI display and no
ImageMagick in a browser, so the examples that read text from a picture, call another program or read the screen are shown as recorded, not run.

| item | on the page? | licence | why |
|---|---|---|---|
| pytesseract-0.3.13-py3-none-any.whl (https://pypi.org/project/pytesseract/0.3.13/) | yes, embedded and unpacked in the browser's Python | Apache License 2.0 | so that the chapter's programs can import pytesseract; SHA-256 7a99c6c2ac598360693d83a416e36e0b33a67638bb9d77fdcac094a3589d4b34; the builder refuses a file that differs |
| Pyodide packages `pillow` 11.3.0, `numpy` 2.2.5, `packaging` 24.2 | yes, loaded from the Pyodide distribution (the same CDN as Pyodide) | as the upstream projects state (Pillow: MIT-CMU; NumPy: BSD-3-Clause; packaging: Apache-2.0 or BSD-2-Clause); to be re-checked by the owner | the programs' own imports |
| seven PNG pictures (hurts, cleaned, cleanCv, columns, readsLine, germanLine, pagesPicked) | yes, as recorded pictures, SHA-256 checked when the page is made | drawn by the research programs (Pillow 12.3.0, Python 3.14.6) from sentences written for the course and from the study's own text; the course's own licence applies; the programs name the fonts they used (DejaVu, URW Nimbus Roman, URW Z003, IPAGothic), and the licence of those fonts for pictures of their glyphs is an open question | the page shows what the recorded programs drew |
| the book's online materials (a zip of 7,759,877 bytes: ocr-example.png, frankenstein.png, frankenstein_jpn.png, preprocess_ocr.py and others) | no | **open question**: the licence of the zip and of its pictures is not established | the programs that read them are shown as recorded, not run |
| pictures made from the book's pictures (the four-line page, the Frankenstein line, the word boxes, the hyphens, the low-confidence word, the Japanese line, the screen shot) | no | **open question**, same | left out of the page; they stay in the deck, which uses them for teaching only |
| Tesseract 5.3.4, 5.5.3 and 4.1.1, language data files, NAPS2 8.5.1, OCRmyPDF 17.13.0, PyAutoGUI 0.9.54 | no | not redistributed | they are programs of the machine the research ran on; the page cannot start them |

Library versions differ between the recording (Pillow 12.3.0, NumPy 2.5.4) and the browser (Pillow 11.3.0, NumPy 2.2.5): values were compared, not bytes.
