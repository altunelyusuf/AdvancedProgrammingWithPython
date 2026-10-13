# Chapter 21 page assets - provenance and licences (v1.0.0)

The chapter 21 page runs the chapter's Python in the browser (Pyodide 0.28.2, CPython 3.13.2). **No wheel and no book file is embedded.**

| item | on the page? | licence | why |
|---|---|---|---|
| Pyodide packages `pillow` (11.3.0) and `matplotlib` (3.8.4) | yes, loaded from the Pyodide distribution (the same CDN as Pyodide) | Pillow: MIT-CMU (HPND); Matplotlib: Matplotlib licence (PSF-based) - as the upstream projects state; to be re-checked by the owner | the 30 examples that run use them |
| ten PNG pictures (swatches, boxTuple, rotateSheet, drawing, howdy, line, scatter, bar, pie, accumulated) | yes, as recorded pictures, SHA-256 checked when the page is made | made by the research programs (Pillow 12.3.0, Matplotlib 3.11.2, Python 3.14.6) from colours, shapes and numbers written for the course; the course's own licence applies | the page shows what the recorded programs drew; the page does not draw them again |
| the book's online materials (a zip of 7,759,877 bytes: zophie.png, catlogo.png and others) | no | **open question**: the licence of the zip, of the cat picture and of the logo is not established | 19 examples that read them are shown as recorded, not run |
| pictures derived from the cat picture or logo (face, tiled, mask pair, PNG vs JPEG, logo, seating cards) | no | **open question**, same | left out of the page; they stay in the deck, which uses them for teaching only |
| DejaVu or any other font file | no | not needed | the two examples that need a TrueType font are recorded |

Library versions differ between the recording (Pillow 12.3.0, Matplotlib 3.11.2) and the browser (Pillow 11.3.0, Matplotlib 3.8.4): values were compared, not bytes.
