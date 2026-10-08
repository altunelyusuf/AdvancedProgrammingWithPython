# SEN0414 chapter pages 9.27.0 - the two-fold standard, ported from the proven series (templates 9.26.0-9.40.0)

The owner's directive of 2026-10-06 ("the visualizations and styling in two-folds": decks and pages one look) and the
four reviews of 2026-10-07 were answered first on the sibling course's chapter-1 page, one template version per subject,
each measured and shipped there. This release carries the same series onto this course's own template line - the twelve
count-asserted patches re-applied to `course_page_template_v9_25_0.html` (every occurrence count held: the two lines
differed by 59 lines of course constants), then three subjects this course needed on top:

| this course's version | subject (first shipped on the sibling line as) |
|---|---|
| 9.26.0 | the CME look-and-feel tokens and the Stories tab (9.33.0) |
| 9.27.0 | Learn sections: concept pills, enrich on reveal, neighbourhood map, story chips (9.34.0) |
| 9.28.0 | concept map with sections/concepts views, filters, find, focus (9.35.0) |
| 9.29.0 | ontology-graph syntax and behaviour layers from the executed examples (9.36.0) |
| 9.30.0 | the chapter ERD (9.37.0) |
| 9.31.0 | fit to the screen (9.38.0) |
| 9.32.0 | the page-machinery chips leave the concepts (9.39.0) |
| 9.33.0 | ERD connections on by default, sections tinted by subject (9.40.0) |
| 9.34.0 | the reading area: one breadcrumb row, no folds, visuals on reveal, (i)+card notes (9.41.0) |
| 9.35.0 | relocate on the ERD (9.42.0) |
| 9.36.0 | relocate on every diagram (9.43.0) |
| 9.37.0 | the narrative diagrams typed by the CME mapping (9.44.0) |
| 9.38.0 | **this course:** the exam identity read from the configuration - the template had the instructor's public key baked in, and the pair was re-provisioned after the environment move, so release codes made by the current key never unlocked (measured: the full test's unlock never showed the report) |
| 9.39.0 | **this course, and the sibling's next:** the agents' knowledge graph skips the embedded CME standard - measured: "standard: learning outcomes (course part)" outranked the course's own outcome for every wording of the course question |
| 9.40.0 | **this course, and the sibling's next:** a chosen entity's ERD labels search further for a free spot - measured: 10 of 14 labels of a 14-relationship section drawn over one another |

## What the pages now carry
- 15 stories (sen0414_chNN_stories_v1_0_0.py, 5N1K-checked) with the decks' seven photographs (chNN-page/stories_img_v1_0_0.json, credits from the deck builders' placements and ASSETS_PROVENANCE).
- 30 narrative diagrams (sen0414_chNN_diagrams_v1_0_0.py, six per chapter: activity, use-case, state, sequence, mind map and one more), every element label grounded in the concepts' own explanations at 0.85 or better by measure; typed from the CME mapping (cme 0.16.0, read at the recorded digests); the chapter's `cme:NarrativeDiagram` individuals as a corpus block.
- Configuration 1.4.0 (materials 1.37.0, the re-provisioned public key, corpus.standards), data 2.6.0, build 4.9.0, test 9.26.0 (the sibling's 9.32.0 given this course's names, with this course's own vocabulary checks kept and the story READ link compared as written), test_config 1.0.0 for each chapter.
- 9.41.0 (this course): a concept instance whose own name is a line of code ("def hello():", 64 of chapter 4's 94 individuals) is named by its class in the taxonomy and its code shown in the card - the audit rule F-B4 reaching the instances no owner edge links; measured: 17 code-labelled boxes on chapter 4's individuals layer, now 0.

## Verification (08-tooling/chNN-page/, PAGE_VER 9_27_0)
sen0414_page_test_v9_26_0.py: 239-277 recorded checks per chapter (features and widgets), 0 failures in all five
(test_results_v9_27_0.json). The sibling's smoke test and book-corpus check were tried on these pages and NOT shipped:
their expectations are the sibling course's (a proof-of-work playground, its Code Lab snippet shapes, its book-passage
ownership), so their failures measure the tools, not the pages; adapting them to this course is the next step, and two
of their findings deserve a look then (chapter 3: a bank program naming randint without its import; chapter 4: a bank
program calling a positional-only parameter by name) - the full test's own re-run of every written item passed.

## Found while building
- The Ontologies checkout here is shallow; the textbook ontology's pinned commit had to be fetched by its tag
  (`automate-python-book-3e-v0.20.0`) before a page could be built - the bytes are the ones the released pages carry (sha
  dc4be1b3…).
- The materials register had named pages 9.24.0 while the released pages were 9.26.0; 1.37.0 names 9.27.0.
- The 9.26-9.32 audit repairs of the sibling line (the book-layer query shape, the mobile progress badge) remain a separate
  thread, as the handover said; the exam-identity repair could not wait and is 9.38.0 here.
