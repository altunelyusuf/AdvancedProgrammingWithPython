# Addendum to the briefs r1 (chapters 5, 2, 3, 6): lessons of the first wave, 2026-11-01

Pass this file with the r1 brief of your chapter. It adds; it changes no requirement of the brief.

1. Page data: build the page data from the SAME ontology and research files the chapter's newest committed page was built from. Taking "the newest" research files changed labels and failed 2 agent-citation checks on Chapter 1 (v9_93_0); the repair v9_93_1 used the older files. Check the agent-citation features of page test 9.38.0 before you commit the page as final.
2. Story pictures: the story-layout probe fails on a tall photo (Chapter 7, v9_91_0). Crop a copy of the same free-licence photo before the first probe run.
3. Lambda: if the chapter's own ontology or research teaches lambda, STOP and tell the coordinator. Only Chapter 4 does, and the Owner decided for it (2026-11-01): teach it, accept the deck-check D5 finding there. Chapter 5, 2, 3 and 6 get no such exception.
4. Do not edit a tool or data file you have already committed; a change is a new version (two Chapter 1 tool files were edited after their first commit and had to be disclosed).
5. Push the manifest first, then the deck, then the page; commit each verified step at once.
6. Run the page tests (9.38.0 then 9.37.0) once each on the final page under `flock /tmp/page_test.lock`; the lock is shared with the controller's own runs, so expect to wait. Do not run them on drafts.
7. Page-text prompts: descriptive sentences in research text that merely mention the interpreter prompt are not copyable code; do not rewrite research for them. The page's own code, exercises and Playground starter must have none.
8. Disk: the machine has about 2 GB free; stop below 0.8 GB, delete scratch (rendered slide images, temporary page copies) as soon as read.
