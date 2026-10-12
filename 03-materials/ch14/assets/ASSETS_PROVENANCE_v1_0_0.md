# Chapter 14 page assets - provenance and licences (v1.0.0)

The chapter 14 page runs the chapter's Python in the browser (Pyodide, CPython 3.13). Pyodide's own package list has no
openpyxl (checked in pyodide-lock.json of Pyodide 0.28.2), so the page embeds the two pure-Python wheels below and unpacks
them into the browser's Python when it starts (page template 9.43.0; page-data builder 2.12.0 reads them through
08-tooling/ch14-page/pywheels_v1_0_0.json and refuses a file whose SHA-256 differs from the one recorded there).

Downloaded on 2026-10-12 from PyPI with pip (the proxy of the build machine); both projects are MIT-licensed (et_xmlfile's wheel also ships a LICENCE.python file, the Python Software Foundation licence for code it derives from the standard library).

| file | project page | licence | SHA-256 |
|---|---|---|---|
| openpyxl-3.1.5-py2.py3-none-any.whl | https://pypi.org/project/openpyxl/3.1.5/ | MIT | 5282c12b107bffeef825f4617dc029afaf41d0ea60823bbb665ef3079dc79de2 |
| et_xmlfile-2.0.0-py3-none-any.whl | https://pypi.org/project/et-xmlfile/2.0.0/ | MIT | 7a91720bc756843502c3b7504c77b8fe44217c85c537d85037f0f536151b2caa |

openpyxl 3.1.5 is the release the chapter's examples were recorded under (Python 3.14.6). Photographs: none; the chapter's
stories carry no photograph (see 08-tooling/ch14-page/stories_img_v1_0_0.json).
