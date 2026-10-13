# Chapter 20 page assets - provenance and licences (v1.0.0)

The chapter 20 page runs the chapter's Python in the browser (Pyodide 0.28.2, CPython 3.13.2). **No wheel and no book file is embedded.**

| item | on the page? | licence | why |
|---|---|---|---|
| Python standard library (email, imaplib, smtplib, json, secrets, hmac, ...) | yes, as Pyodide ships it | Python Software Foundation licence | the examples that run use it |
| Pyodide package `ssl` | yes, loaded from the Pyodide distribution (the same CDN as Pyodide) | Python Software Foundation licence | smtplib and the chapter's programs import ssl |
| ezgmail 2026.4.28 | no | GPLv3+ (PyPI classifier and metadata; published as a source distribution of 31,345 bytes, no wheel) | a copyleft licence; the course does not ship it inside a page, and it needs Google's client library |
| google-api-python-client 2.201.0 | no | Apache-2.0 | its wheel is 16,812,656 bytes, more than the 16 MB a page may hold |
| requests 2.34.2, aiosmtpd 1.4.6 | no | Apache-2.0 (requests), Apache-2.0 (aiosmtpd) | they need sockets and threads, which a browser's Python does not have |

The research and the deck ran these packages under Python 3.14.6 (08-tooling/ch20-page/third_party_record_v1_0_0.json). The 36 examples that need them are shown on the
page as recorded, not run, each with its reason (08-tooling/ch20-page/standin_v1_0_0.json). No file of the book's online materials is embedded (the zip has no file for
chapter 20). Photographs: see 08-tooling/ch20-page/stories_img_v1_0_0.json (none used).
