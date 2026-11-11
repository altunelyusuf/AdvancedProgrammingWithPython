# Chapter 15 Draft — Google Sheets (v1.0.0)

**Status note:** Existing materials checked against live files (deck `SEN0414_Ch15_GoogleSheets_3e_v2_0_0.pptx`, 53 slides; page `sen0414_ch15_page_v9_96_1.html`; manifest `chapter_code_ch15_v1_0_0.json`, 25 examples; stories `sen0414_ch15_stories_v1_0_1.py`, 5 stories). Chapter 15's materials went through a real repair cycle in October (page v9_96_0 failed the leak probe on all five seeds; repaired to v9_96_1, which now passes every check). No legacy duplicate deck exists for this chapter. This draft is for your reading and approval before any render step.

## 1. The story (5 beats, one per concept, sourced)

1. **6 June 2006 — Jonathan Rochelle & Farzad Khosrowshahi (2Web Technologies, then Google).** Google Sheets began as XL2Web, 2Web Technologies' web spreadsheet, acquired by Google in 2006 and relaunched as Google Labs Spreadsheets, opened to a first-come-first-served test group on 6 June 2006. *Lesson: a browser spreadsheet is a service you call, not a file.* (https://en.wikipedia.org/wiki/Google_Sheets)
2. **31 October 2008, 14:10 ET — Satoshi Nakamoto, cryptography mailing list.** Nakamoto's message announced a peer-to-peer electronic cash system with no trusted third party, no mint, and proof-of-work-minted coins — the properties the chapter's "Boringcoin" ledger program (an audited spreadsheet) stands in for. *Lesson: a ledger of rows is easy to audit and just as easy to forge.* (https://www.metzdowd.com/pipermail/cryptography/2008-October/014810.html)
3. **November 2006 → October 2012 — Blaine Cook, Chris Messina, David Recordon, Larry Halff → RFC 6749.** OAuth began from Cook's work on Twitter's OpenID and a CitizenSpace meeting where the group found no open standard for API access delegation; a 2007 draft became IETF RFC 6749 in 2012. Its authorization code and refresh token are exactly what the chapter's token files hold. *Lesson: the token files exist so a script never learns your password.* (https://oauth.net/about/introduction/)
4. **2 August 2021 — the Google Sheets API team.** Google's migration guide retired Sheets API v3 on this date in favor of the JSON-based v4; EZSheets calls v4 at `sheets.googleapis.com`. *Lesson: a library is only as stable as the web service behind it.* (https://developers.google.com/workspace/sheets/api/guides/migration)
5. **2008 — Google, as part of Google Docs.** Google Forms launched in 2008 as a collaborative survey tool whose responses write into a spreadsheet of the owner's choosing — the spreadsheet the chapter's first Forms practice program opens with EZSheets. *Lesson: a form is a front door that writes rows for your script to read.* (https://en.wikipedia.org/wiki/Google_Forms)

## 2. Explanations

Chapter 15 teaches EZSheets end-to-end: installing/setting up EZSheets and its OAuth sign-in (token files, scopes, the CSRF/PKCE-style challenge, pickle's code-execution risk when loading credentials, token expiry/renewal), Spreadsheet objects (create/list/open by id or address, settable vs. read-only attributes, upload/download in six formats, Trash vs. permanent delete), Sheet objects (cell read/write, column-letter addressing, `getRow`/`getColumn`/`updateRow`, per-cell vs. per-column request cost, create/move/delete/copy/clear sheets, library quirks), Google Forms (collecting responses into a sheet), and Google Sheets quotas (the library's wait-and-retry behavior). It closes with Project 11, a two-step Bean Count ledger audit exercise exploring race conditions (two programs appending a row at once) and total-checking.

## 3. Slide / page-tab outline (53 slides, 25 code examples — order follows the current deck)

| # | Slide | Title / content |
|---|-------|------------------|
| — | 1–6 | Title, agenda, stories 1–5 (narrative slides) |
| 1 | 7 | Before the sign-in: version, state, scopes |
| 2 | 8 | What a token file holds |
| — | 9 | (explanatory, no code) |
| 3 | 10 | The sign-in address the library builds |
| — | 11 | (explanatory) |
| 4 | 12 | The challenge: a hash of a secret |
| 5 | 13 | Loading a pickle can run code |
| 6 | 14 | Valid, expired and renewable tokens |
| — | 15–16 | (explanatory / transition) |
| 7 | 17 | Create a spreadsheet and list spreadsheets |
| 8 | 18 | Open one spreadsheet by id and by address |
| 9 | 19 | Spreadsheet attributes you can and cannot set |
| — | 20–21 | (explanatory) |
| 10 | 22 | Upload a file and download in six formats |
| 11 | 23 | Delete: to the Trash, or for good |
| — | 24–25 | (explanatory) |
| 12 | 26 | Read and write a cell |
| 13 | 27 | Addresses and column letters |
| — | 28 | (explanatory) |
| 14 | 29 | Rows and columns: getRow, getColumn, updateRow |
| 15 | 30 | One request per cell, or one for the column |
| — | 31–32 | (explanatory) |
| 16 | 33 | Create, move and delete sheets |
| 17 | 34 | Copy a sheet and clear a sheet |
| 18 | 35 | Surprises of the library |
| — | 36–37 | (explanatory / transition to Forms) |
| 19 | 38 | Collect e-mail addresses from form answers |
| — | 39 | (explanatory) |
| 20 | 40 | Quota errors: the library waits and retries |
| — | 41–42 | (explanatory / Project 11 intro) |
| 21 | 43 | Project 11, step 1: audit the ledger |
| 22 | 44 | The audit stops at an empty row |
| 23 | 45 | Project 11, step 2: add a transaction |
| 24 | 46 | Two programs add a row at the same time |
| — | 47 | (explanatory) |
| 25 | 48 | Finding mistakes: check the totals |
| — | 49–51 | Summary, Practice Questions setup, chart |
| — | 52 | Practice Questions (4 drills + 1 program) |
| — | 53 | Resources: where to go next |

## 4. Resources slide (14 links, verified live on the current deck)

1. Book: Automate the Boring Stuff, 3e, ch.15 — https://automatetheboringstuff.com/3e/chapter15.html
2. Google Identity: OAuth 2.0 for desktop apps — developers.google.com
3. EZSheets documentation — https://ezsheets.readthedocs.io/en/latest/
4. RFC 7636: Proof Key for Code Exchange — https://www.rfc-editor.org/rfc/rfc7636.txt
5. EZSheets on PyPI — https://pypi.org/project/ezsheets/
6. Python docs: pickle — https://docs.python.org/3/library/pickle.html
7. Google Sheets API: usage limits — developers.google.com
8. OWASP: Deserialization Cheat Sheet — cheatsheetseries.owasp.org
9. Google Sheets API: reading and writing values — developers.google.com
10. gspread documentation — https://docs.gspread.org/en/latest/
11. Google Sheets API: choose scopes — https://developers.google.com/workspace/sheets/api/scopes
12. Introduction to OAuth — https://oauth.net/about/introduction/
13. Google Sheets API: migrate from v3 — developers.google.com
14. Bitcoin: A Peer-to-Peer Electronic Cash System — https://bitcoin.org/bitcoin.pdf

## 5. Open items

- No legacy duplicate deck to retire for this chapter.
- A `rdodi/` research/domain-ontology artifact subfolder exists (`03-materials/ch15/rdodi/`) from the earlier iteration-20 process; left untouched, out of this lineage's scope per your standing rule of not reopening closed, controller-confirmed work without a found defect.
- No structural gap found; the already-Done repair (page v9_96_0 → v9_96_1) is the only prior defect, and it is resolved and confirmed.
