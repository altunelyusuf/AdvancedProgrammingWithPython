# Chapter 19 page assets - provenance and licences (v1.0.0)

The chapter 19 page runs the chapter's Python in the browser (Pyodide 0.28.2, CPython 3.13.2). Pyodide's own package list has none of schedule, pyperclip
and playsound3, and its tzdata is release 2025.2, so the page embeds the four wheels below (all pure Python or data, no compiled code) and unpacks them into the
browser's Python when it starts (page template 9.48.0; page-data builder 2.17.0 reads them through 08-tooling/ch19-page/pywheels_v1_0_0.json and refuses a
file whose SHA-256 differs from the one recorded there). They are the versions the research ran under Python 3.14.6. The tzdata wheel carries the time
zone database 2026.5 that the stored zone results were printed with.

Downloaded on 2026-10-13 from PyPI with pip (the proxy of the build machine); no wheel was changed.

| file | project page | licence | SHA-256 |
|---|---|---|---|
| playsound3-3.3.2-py3-none-any.whl | https://pypi.org/project/playsound3/3.3.2/ | MIT License | fde2ca4378ae7a34d125a5965799fb1eee2af9907dbec29d394e29d28ee4137b |
| pyperclip-1.11.0-py3-none-any.whl | https://pypi.org/project/pyperclip/1.11.0/ | BSD | 299403e9ff44581cb9ba2ffeed69c7aa96a008622ad0c46cb575ca75b5b84273 |
| schedule-1.2.2-py3-none-any.whl | https://pypi.org/project/schedule/1.2.2/ | MIT License | 5bef4a2a0183abf44046ae0d164cadcac21b1db011bdd8102e4a0c1e91e06a7d |
| tzdata-2026.5-py2.py3-none-any.whl | https://pypi.org/project/tzdata/2026.5/ | Apache-2.0 | b683bd1b6659ddcd810ff02ad09ba821d4bf1065072805063eb35c49617905ac |

The licences (MIT for schedule and playsound3, BSD for pyperclip, Apache-2.0 for tzdata) allow redistribution with the licence text, which is inside each
wheel's dist-info. No file of the book's online materials is embedded (calcProd.py, stopwatch.py and simplecountdown.py are written out by the examples
themselves where they are used). Photographs: see 08-tooling/ch19-page/stories_img_v1_0_1.json.
