# Handover to the SEN0414 session: Chapters 9 and 10 this week, in a fresh narrow lineage

**Date:** 2026-11-08. **To:** the new SEN0414 session. **Read this one file; it is self-contained.**
Keep the OE operating discipline and the BRSF lineage discipline exactly as the owner's standing instruction says: read the latest files from their GitHub folders each turn and read one in full only when its version changed. Do not trust memory or summaries.

## 1. What the owner wants, in his words and order

1. **This week is urgent: the Chapter 9 and Chapter 10 materials, each a deck (PPT) and an interactive HTML page, ready by the evening of 2026-11-12.** Chapters 1-8 were the midterm scope and are consumed.
2. Then the other chapters, until the end of the semester.
3. Previous chapters are corrected only after the current work is finished. Do not touch Chapters 1-8 this week.
4. Course material development has been taking too much time and effort. Part of your job is to make it faster, not only to deliver.

## 2. Your lineage: a fresh, narrow one

The owner decided to open a fresh lineage for this course. He prefers simple narrow lineages whose mission is the smallest slice that can be closed, with the course-wide mission kept separate. Suggested mission, for you to settle in the Mission stage: *Chapters 9 and 10 of the third edition are taught with a deck and an interactive page, each produced from one owner-approved chapter draft, ready for the lecture of the week of 2026-11-12.* Later chapter pairs get their own narrow lineages; the retrofit of the earlier chapters is a later one.

The running lineage must end first, because the owner's rule is one lineage at a time and a lineage is closed by a closure report, not abandoned. Measured on 2026-11-08: it is `07-lineage/sen0414_slides_lineage_v2_401_0.ttl`, 5.4 MB, 363 files in `07-lineage`; items: 458 Done, 74 Ready, 18 InProgress, 12 Proposed, 11 Cancelled, 9 Suspended. Its mission (every lecture deck teaches what the book teaches, in its order) is not accomplished, so it ends as cancelled-by-narrowing: run the as-is fit-gap and impact analysis, write the closure report, carry the open chapter scope forward as the fresh lineage's scope, and archive in the next release. Do this in the same step as opening the fresh lineage; do not let it delay the chapter work.

Read before you carry anything forward: of the 18 InProgress items, most are exam and mock-exam items (the exam set v4.0.0, new items for the six blocks, the mock page, the delivery set v3.0.0). The midterm was held in full attendance, and exam work is held outside this repository. Do not carry those forward; say so in the closure report. Two InProgress stories are chapter retrofits (Chapter 4, Functions, and Chapter 6, Lists, to the "Chapter 8 Friday standard"): they belong to the later retrofit lineage, not to this week. Of the 74 Ready items, keep only those that serve Chapters 9-10 now.

## 3. The state of Chapters 9 and 10 (read from this repository on 2026-11-08)

They are not unbuilt. `03-materials/ch09` and `ch10` each hold a deck, a `page/` folder, an `assets/` folder and an `rdodi/` folder, and each page has been through five builds (Chapter 9 up to 9.90.0, Chapter 10 up to 9.95.0). Chapters 11-18 also have decks; Chapters 19-25 have only empty folders. There is also a `slides/` folder of older decks with a different naming ("YA" suffix) that duplicates chapters already covered; do not use it, and say whether it can be retired. So the work is to check what exists against the owner's current teaching emphasis and standards and fix the gaps, not to start from nothing. Say plainly what you find stale or missing before you build.

## 4. The way to work: the draft first

The slowness has one measured pattern: pages went through five full builds each because layout was built before the content was settled. The owner agreed to this order:

1. Write one plain-text chapter draft: the story (5N1K as human storytelling with real names, a real picture source and a live link), the explanations, the slide outline, the page tabs in slide order, each code example with its executed result, the resources slide. The owner reads and approves it. Ask no question the draft can answer.
2. Only after approval, render the deck, the page and the document from that one draft.
3. A correction after approval goes to the draft and is re-rendered, never patched in one output.
Forecast, not a deadline: draft for the owner's reading by 2026-11-10, so that rendering and checking have two days.

A generic pipeline that does this for any course is being built elsewhere; do not wait for it. Do the same steps by hand with the current builders this week.

## 5. Version rule (the owner's ruling of 2026-11-08)

A file's version must not move because another file was released. Each deck, page and document continues from **its own** last version, with the step sized by the change: patch for a wording or value corrected, minor for something added, major for something removed or changed in meaning. Template, data and builder versions are recorded inside the page as inputs and are not counted in its number. No released file is renamed. This repository now holds `08-tooling/cme_version_check_v1_0_0.py` and `08-tooling/cme_version_baseline_SEN0414_v1_0_0.json`: run `python3 08-tooling/cme_version_check_v1_0_0.py . --baseline 08-tooling/cme_version_baseline_SEN0414_v1_0_0.json --declare <dir>=<size>` before each release. It refuses a file that is not one own step from its predecessor; whether the declared size fits the change is for the reviewer to read.

## 6. Your own questions

List only your own questions to the owner, one at a time, with options.
