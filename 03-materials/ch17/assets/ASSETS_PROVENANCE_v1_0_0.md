# Chapter 17 page assets - provenance and licences (v1.0.0)

The chapter 17 page runs the chapter's Python in the browser (Pyodide 0.28.2, CPython 3.13.2). Pyodide's own package list has neither pypdf nor
python-docx, so the page embeds the two pure-Python wheels below and unpacks them into the browser's Python when it starts (page template 9.45.0;
page-data builder 2.15.0 reads them through 08-tooling/ch17-page/pywheels_v1_0_0.json and refuses a file whose SHA-256 differs from the one
recorded there). The page loads these packages from Pyodide's own distribution first: lxml (6.0.0), Pillow (11.3.0), cryptography (45.0.5)
and typing_extensions (4.14.1); the research ran lxml 6.1.3, Pillow 12.3.0 and cryptography 50.0.2, the page's examples were checked in the
browser against the stored results. pdfminer.six (MIT) is not embedded: its wheel is 6.6 MB of character-map data, so its one example is shown as recorded.

Downloaded on 2026-10-12 from PyPI with pip (the proxy of the build machine); neither wheel was changed.

| file | project page | licence | SHA-256 |
|---|---|---|---|
| pypdf-6.20.1-py3-none-any.whl | https://pypi.org/project/pypdf/6.20.1/ | BSD-3-Clause | aa5a55ddcffdc5e5ab291d5decb23f6383f4e56f8e3263dc39af41fff03885ad |
| python_docx-1.2.0-py3-none-any.whl | https://pypi.org/project/python-docx/1.2.0/ | MIT | 3fd478f3250fbbbfd3b94fe1e985955737c145627498896a8a6bf81f4baf66c7 |

Both licences (BSD-3-Clause, MIT) allow redistribution with the licence text, which is inside each wheel's dist-info. No file of the book's online
materials is embedded: every example of the chapter builds its own PDF and Word files in memory or in a temporary folder.
Photographs: none; the chapter's stories carry no photograph (see 08-tooling/ch17-page/stories_img_v1_0_0.json).
