# Chapter 3 deck and page assets - provenance and licences (v1.1.0)

Supersedes ASSETS_PROVENANCE_v1_0_0.md for the chapter 3 deck 5.0.0 (the older file stays as it is). The two photographs of v1.0.0 are used unchanged; one photograph is added.
The licence and credit of each Wikimedia file were read from the extmetadata of the Commons API by the sessions that first downloaded them (chapter 3 on 2026-10-12, chapter 7 on 2026-10-08).
The Commons API answered HTTP 429 to every request of this session (2026-10-25), so no new file was fetched; the new asset below is a byte-for-byte copy of an existing course asset.

| file | source | licence | credit carried on the slide | used in |
|---|---|---|---|---|
| photo_carl_gauss.jpg | Wikimedia Commons, "Carl Friedrich Gauss 1840 by Jensen.jpg" (portrait by Christian Albrecht Jensen, 1840) | Public domain | Carl Friedrich Gauss, portrait by Christian Albrecht Jensen, 1840. Public domain, Wikimedia Commons. | deck 5.0.0, story slide 8 |
| photo_edsger_dijkstra.jpg | Wikimedia Commons, "Edsger Wybe Dijkstra.jpg" | CC BY-SA 3.0 | Edsger W. Dijkstra. Photo: Hamilton Richards, CC BY-SA 3.0, Wikimedia Commons. | deck 5.0.0, story slide 17 |
| photo_guido_van_rossum_2014.jpg | the chapter 7 asset of the same name, copied unchanged (Wikimedia Commons, "Guido-portrait-2014-drc.jpg", https://commons.wikimedia.org/wiki/File:Guido-portrait-2014-drc.jpg, 1280 px rendering) | CC BY-SA 4.0 | Guido van Rossum, 2014. Photo: Daniel Stroud, CC BY-SA 4.0, Wikimedia Commons. | deck 5.0.0, story slide 12 |

## Story texts and links (checked 2026-10-25 from the build machine)

- Gauss: story companion 08-tooling/sen0414_ch03_stories_v1_0_0.py (legend, set in the 1780s, oldest print 1856, versions collected by Brian Hayes, American Scientist, 2006). Link https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss answered HTTP 200.
- Dijkstra: EWD831, 11 August 1982, "Why numbering should start at zero". The old story companion gives the place as Austin, Texas; Wikipedia (https://en.wikipedia.org/wiki/Edsger_W._Dijkstra, HTTP 200) says Dijkstra was a Burroughs research fellow from August 1973 and moved to the University of Texas at Austin in 1984, so the deck says: written in Nuenen, the Netherlands, kept in the EWD archive at the University of Texas at Austin. The EWD831 page itself (https://www.cs.utexas.edu/users/EWD/transcriptions/EWD08xx/EWD831.html) could not be reached from the build machine (connection failed); it is on the resources slide, and the story's link is the Wikipedia page.
- PEP 572: https://peps.python.org/pep-0572/ (HTTP 200): authors Chris Angelico, Tim Peters, Guido van Rossum; created 28-Feb-2018; Python-Version 3.8. Guido van Rossum stepped down as BDFL on 12 July 2018 (https://en.wikipedia.org/wiki/Guido_van_Rossum, HTTP 200).
- The Mersenne Twister story of the old deck (4.0.0) is not carried: it is not a concept of the chapter research, and no freely licensed picture could be obtained (Commons API HTTP 429; the Wikipedia article carries none).
