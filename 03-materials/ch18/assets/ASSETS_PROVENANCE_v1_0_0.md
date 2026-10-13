# Chapter 18 page assets - provenance and licences (v1.0.0)

The chapter 18 page runs the chapter's Python in the browser (Pyodide 0.28.2, CPython 3.13.2). Pyodide's own package list has none of xmltodict,
defusedxml and openpyxl, so the page embeds the four pure-Python wheels below and unpacks them into the browser's Python when it starts (page template
9.47.0; page-data builder 2.16.0 reads them through 08-tooling/ch18-page/pywheels_v1_0_0.json and refuses a file whose SHA-256 differs from the one
recorded there). The page loads lxml (6.0.0) from Pyodide's own distribution; the research ran lxml 6.1.3, and the page's examples were checked in the
browser against the stored results.

Downloaded on 2026-10-12 from PyPI with pip (the proxy of the build machine); no wheel was changed. The openpyxl and et_xmlfile wheels are the files
committed in 03-materials/ch14/assets, byte for byte.

| file | project page | licence | SHA-256 |
|---|---|---|---|
| defusedxml-0.7.1-py2.py3-none-any.whl | https://pypi.org/project/defusedxml/0.7.1/ | PSFL | a352e7e428770286cc899e2542b6cdaedb2b4953ff269a210103ec58f6198a61 |
| et_xmlfile-2.0.0-py3-none-any.whl | https://pypi.org/project/et_xmlfile/2.0.0/ | MIT | 7a91720bc756843502c3b7504c77b8fe44217c85c537d85037f0f536151b2caa |
| openpyxl-3.1.5-py2.py3-none-any.whl | https://pypi.org/project/openpyxl/3.1.5/ | MIT | 5282c12b107bffeef825f4617dc029afaf41d0ea60823bbb665ef3079dc79de2 |
| xmltodict-1.0.4-py3-none-any.whl | https://pypi.org/project/xmltodict/1.0.4/ | MIT | a4a00d300b0e1c59fc2bfccb53d7b2e88c32f200df138a0dd2229f842497026a |

The licences (MIT for xmltodict, openpyxl and et_xmlfile; the Python Software Foundation licence for defusedxml) allow redistribution with the licence text,
which is inside each wheel's dist-info (et_xmlfile also ships LICENCE.python, the Python Software Foundation licence for code derived from the standard
library). No file of the book's online materials is embedded: every example of the chapter builds its own CSV, JSON, XML and workbook files in memory.
Photographs: see 08-tooling/ch18-page/stories_img_v1_0_1.json.
