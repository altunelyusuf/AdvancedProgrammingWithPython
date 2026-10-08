# Chapter 6 deck and page assets - provenance and licences (v1.0.0)

Same regime as chapters 1-5 (CME materials look-and-feel standard v1.0.0). Downloaded with curl on 2026-10-08.

## The textbook's own figures

Source: Al Sweigart, *Automate the Boring Stuff with Python*, 3rd edition (No Starch Press, 2025), chapter 6, https://automatetheboringstuff.com/3e/chapter6.html ;
files fetched from https://automatetheboringstuff.com/3e/images/ (the figure numbers and captions were read off that page). Licence: the book's website states
Creative Commons BY-NC-SA (the course brief said CC BY-SA; chapter 7's provenance and the textbook ontology header record BY-NC-SA for the book's own material).
The figures are used unchanged, non-commercially, in course teaching, with the credit "Sweigart, ATBS 3e, CC BY-NC-SA" carried on the slide that shows
them. If a stricter reading of the licence is wanted, remove the book_fig_* files and the slides that show them; nothing else depends on them.

| file | what it is | where it is used |
|---|---|---|
| book_fig_000097.jpg | Figure 6-1: a list value stored in spam, showing which value each index refers to | deck, title of part 1 and the indexes slide; page, Learn section |
| book_fig_000098.jpg | Figure 6-2: variable assignment does not rewrite the value, it changes the reference | deck, title of part 4 |
| book_fig_000099.jpg | Figure 6-3: eggs and spam refer to the same list | deck, aliasing slide |
| book_fig_000100.jpg | Figure 6-4: lists contain references to values, not values | deck, title slide and title of part 3 |
| book_fig_000101.jpg | Figure 6-5: the Matrix screensaver program running in a console window | deck and page, the digital-rain story |

## External, free-licence photographs (attribution required, kept verbatim)

| file | source | licence | attribution |
|---|---|---|---|
| photo_edsger_dijkstra.jpg | Wikimedia Commons, "Edsger Dijkstra 1994.jpg" (Zurich, 1994), https://commons.wikimedia.org/wiki/File:Edsger_Dijkstra_1994.jpg ; the 1280-pixel rendition of the 3574-pixel original | CC BY-SA 4.0 | photo: Andreas F. Borchert |
| photo_ronald_fisher.jpg | Wikimedia Commons, "Ronald Aylmer Fisher 1952.jpg" (1952-07-01), https://commons.wikimedia.org/wiki/File:Ronald_Aylmer_Fisher_1952.jpg ; the 330-pixel rendition that Commons serves (the full-size file answered HTTP 429 from this host for the whole session) | CC BY-SA 4.0 | photo: Barry Eagel |
| photo_magic_8_ball.jpg | Flickr, "'It is certain.' ~ The Magic Eight Ball", user zaneology, Dallas, 2012, https://www.flickr.com/photos/zaneology/7246548230/ (the page states Creative Commons Attribution 2.0; the same file is on Commons as "\"It is certain.\" ~ The Magic Eight Ball (7246548230).jpg"). Fetched at 500 x 500 px from live.staticflickr.com; re-encoded once with Pillow (quality 95, baseline JFIF) because LibreOffice drew the original, a Photoshop-written JPEG, as a black rectangle - pixels unchanged otherwise | CC BY 2.0 | photo: Zaneology |

## Not used, and why

- Tim Peters (Timsort) - no free-licence portrait could be retrieved, so the Timsort story was dropped from the chapter's four stories.
- "Digital rain animation medium letters shine.gif" (Jahobr, CC0) was planned for the digital-rain story but Wikimedia answered HTTP 429 to every attempt; the story uses
  the book's own Figure 6-5 (the chapter's screensaver in a console) instead, with the book's licence and credit.
- No photograph of a scene from the film The Matrix is used (it is not freely licensed).
