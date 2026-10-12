# Chapter 15 page assets - provenance and licences (v1.0.0)

The chapter 15 page runs the chapter's Python in the browser (Pyodide, CPython 3.13). Pyodide's own package list has neither
ezsheets nor google-api-python-client, so the page embeds the pure-Python wheels below and unpacks them into the browser's Python when
it starts (page template 9.44.0; page-data builder 2.13.0 reads them through 08-tooling/ch15-page/pywheels_v1_0_0.json and refuses a
file whose SHA-256 differs from the one recorded there). The page also loads these packages from Pyodide's own distribution first:
ssl, protobuf, cryptography, requests, pyparsing, cachetools, certifi, urllib3, idna, charset-normalizer, packaging. No example reaches Google: the library runs against a stand-in for Google written for the study (see the page's Provenance & known limits).

Downloaded on 2026-10-12 from PyPI with pip (the proxy of the build machine).

| file | project page | licence | SHA-256 |
|---|---|---|---|
| ezsheets-2026.4.28-py3-none-any.whl | https://pypi.org/project/ezsheets/2026.4.28/ | GPL-3.0-or-later | d6680fc5095fce09feda754ca430eb710dcec41728b665fdaea7326fcdf95ea3 |
| google_api_core-2.42.0-py3-none-any.whl | https://pypi.org/project/google-api-core/2.42.0/ | Apache-2.0 | b1bdf4f72dc4f910736ce4ba49038352effbbc309579215107649b22973a1317 |
| google_api_python_client-2.201.0-py3-none-any.whl | https://pypi.org/project/google-api-python-client/2.201.0/ | Apache-2.0 | 4b2de61537fd1e48c6ade72ac630d09a8139f9ac72bd70cf145e0d4ad7fe70ae |
| google_auth-2.61.0-py3-none-any.whl | https://pypi.org/project/google-auth/2.61.0/ | Apache-2.0 | ca60266a37475ae68b63bac007272f46094b3d571abe92aded329b6cfb568025 |
| google_auth_httplib2-0.4.4-py3-none-any.whl | https://pypi.org/project/google-auth-httplib2/0.4.4/ | Apache-2.0 | bbe5d7b2401bb3a4017f4720e1e91bd273ab9a2bb60b84e65edbc0de127852da |
| google_auth_oauthlib-1.5.0-py3-none-any.whl | https://pypi.org/project/google-auth-oauthlib/1.5.0/ | Apache-2.0 | 71625fdea21c6c03217eb9ff13741c3096e6d257ebca0ad084dbd6e9f4aa4ef4 |
| googleapis_common_protos-1.75.5-py3-none-any.whl | https://pypi.org/project/googleapis-common-protos/1.75.5/ | Apache-2.0 | d7285525c23039db98f2463e6d5a4f9b958b94d497f03a844ece3259c4e72d5d |
| httplib2-0.32.0-py3-none-any.whl | https://pypi.org/project/httplib2/0.32.0/ | MIT | dc6705cacdf3fb0a2aba7629fa33c90fd93e30035db0c157325826be177e4816 |
| oauthlib-4.0.0-py3-none-any.whl | https://pypi.org/project/oauthlib/4.0.0/ | BSD-3-Clause | 624c28c13a0a59cabf9747dfa52af63be3e512a7f2714df16e91b5b3a145e6cd |
| proto_plus-1.29.0-py3-none-any.whl | https://pypi.org/project/proto-plus/1.29.0/ | Apache-2.0 | 8acd070469a7aaf43f440b022ef9757c8cac1a9f866e933f59ae98669ddc6c8b |
| pyasn1-0.6.4-py3-none-any.whl | https://pypi.org/project/pyasn1/0.6.4/ | BSD-2-Clause | deda9277cfd454080ec40b207fb6df82206a3a2688735233cdcd8d3d565f088b |
| pyasn1_modules-0.4.2-py3-none-any.whl | https://pypi.org/project/pyasn1-modules/0.4.2/ | BSD-2-Clause | 29253a9207ce32b64c3ac6600edc75368f98473906e8fd1043bd6b5b1de2c14a |
| requests_oauthlib-2.0.0-py2.py3-none-any.whl | https://pypi.org/project/requests-oauthlib/2.0.0/ | ISC | 7dd8a5c40426b779b0868c404bdef9768deccf22749cde15852df527e6269b36 |
| uritemplate-4.2.0-py3-none-any.whl | https://pypi.org/project/uritemplate/4.2.0/ | BSD-3-Clause or Apache-2.0 | 962201ba1c4edcab02e60f9a0d3821e82dfc5d2d6662a21abd533879bdb8a686 |

## Two files that are not the PyPI files as they stand

- ezsheets-2026.4.28-py3-none-any.whl was built with pip wheel from ezsheets-2026.4.28.tar.gz (sha256 a7f6a9b1ee2dfd2eaa22945fcf0e3f927058e45bae70ece2a8dc53eeb054d161), the only file PyPI holds for that release; no code was changed. The source distribution is kept beside it.
- google_api_python_client-2.201.0-py3-none-any.whl is the PyPI wheel (sha256 2d9bf1ba3f12eee8ed3d0f1791ce0605d163432f496baa72d3677faa2cf097d6) with 603 of the discovery documents in googleapiclient/discovery_cache/documents removed; the two the library uses (sheets.v4.json and drive.v3.json) stay, and no code was changed. The full wheel is 16.8 MB, the pruned one 0.19 MB.

## Licence note

ezsheets is licensed GPL-3.0-or-later (its LICENSE.txt is inside the wheel's dist-info). The page embeds it unmodified and the corresponding source distribution is committed here; whether embedding a GPL-licensed library in a course page is acceptable is the owner's decision. The other wheels are Apache-2.0, MIT, BSD-style or ISC licensed, as the table says.
Photographs: none; the chapter's stories carry no photograph (see 08-tooling/ch15-page/stories_img_v1_0_0.json).
