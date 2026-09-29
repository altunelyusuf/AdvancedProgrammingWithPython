<!-- version: 1.0 -->
# Teaching devices for SEN0414 decks and pages: a proposal (version 1.0)

**Status: PROPOSED to the course owner (lesson L-116).** Nothing here is a ruling. It records what chapter 3 (deck 2.0.0, page 9.6.0) was built with, so the owner can accept, change or reject it before it is applied to chapters 1, 2 and 4.

## Why

The owner's review of 2026-09-29: the decks read as source-code listings, lack the narrative the pages have, and use little of what a presentation can do. The remedy chosen for chapter 3 is a small set of named *devices*. Each device has one purpose, one PowerPoint form and one page form. Where a device draws data, the same executed specification feeds both forms, so a slide and the page cannot disagree.

## How the taxonomy is grounded

- **Widget primitives and discourse features** come from RDODI (`rdodi-ecosystem/06-widget-stage/01-vocabularies`): primitives such as `GuidedNarrativeWalkthrough`, `CoupledVariableExplorer`, `OverviewDetailBrushing`, `DynamicQueryContinuous`, `MultiClassSelectorDistinct`; features such as `OrderedArgument`, `KCategoryEnumeration`, `AsymmetricContrast`, `CrossAttributeRelation`. The page records each visual widget with its primitive and feature (page record 2.3.0).
- **The pairing of a device with a primitive is the author's reading**, not an RDODI ruling. RDODI's feature detection for `OrderedArgument` is itself marked interpretive, so the pairing is a proposal.
- **Devices with no RDODI primitive** are marked "none". They are lecture techniques (talk track, click builds, transitions) that a page cannot show.

## The taxonomy

| # | Device | Use it when the content is | RDODI primitive / feature (proposed pairing) | PowerPoint form | Page form | In chapter 3 |
|---|---|---|---|---|---|---|
| 1 | Hook | a reason to care, before any definition | none | dark slide with one question, fade transition | none yet | built |
| 2 | Predict first | behaviour a learner can guess | CoupledVariableExplorer / AsymmetricContrast | question slide, answer on click | predict widget (edit, run, compare) | built |
| 3 | Trace table | a process whose state changes pass by pass | GuidedNarrativeWalkthrough / OrderedArgument | native table, one row per click | stepper with previous, next, play | built, from a recorded run |
| 4 | Pass strip | a loop that ends in different ways | GuidedNarrativeWalkthrough / OrderedArgument | one box per pass, builds left to right | same run in the stepper | built |
| 5 | Number line | a set of values a call makes | CoupledVariableExplorer / CrossAttributeRelation | native line, dots, stop marker | SVG line | built, from `range()` |
| 6 | Pair lanes | two sequences combined into pairs | CoupledVariableExplorer / CrossAttributeRelation | two lanes, links, error line | SVG lanes | built, from `enumerate` and `zip` |
| 7 | Path flowchart | a choice between branches | DynamicQueryContinuous / OrderedArgument | native flowchart | slider and highlighted lines | page only so far |
| 8 | Two-run contrast | the same code behaving two ways | MultiClassSelectorDistinct / AsymmetricContrast | two runs of one program on successive slides | run selector | built |
| 9 | Chapter map | a set of named kinds | OverviewDetailBrushing / KCategoryEnumeration | map slide, section markers | taxonomy and explorer | built |
| 10 | Hazard callout | a mistake learners really make | none | coloured card naming the mistake, beside the run that shows it | detail card | built |
| 11 | Retrieval | recall a few slides later | none | question slide, answer on click | quiz | built |
| 12 | Talk track | what the lecturer says | none | speaker notes on every slide | none (the page's text carries it) | built (all 30 slides) |
| 13 | Click build | an argument with steps | GuidedNarrativeWalkthrough / OrderedArgument | fade entrance per click | step reveal | built (76 click steps) |
| 14 | Live code | code the learner should change | CoupledVariableExplorer / AsymmetricContrast | not possible | Pyodide playground | page only |

## Choosing a device by content kind (proposed rule)

| Content kind | Default device | Second device |
|---|---|---|
| A process over time (loops, calls, recursion) | 3 or 4 | 8 |
| A set of values (ranges, slices) | 5 | 2 |
| A correspondence between sequences (zip, enumerate, dict items) | 6 | 2 |
| A choice between branches | 7 | 2 |
| A set of kinds, forms or modes | 9 | 11 |
| A hazard or a rule with an exception | 10 | 2 |
| A definition | 1, then one worked example | 11 |

## Obligations that come with a device (proposed)

1. A device that draws data draws it from an executed specification, never typed by hand.
2. The deck's checks re-run each specification under the interpreter the course teaches and refuse a slide whose value differs (`visual_check_v1_0_0.py`); a stale fixture must be refused.
3. Every trace names a program the deck's own program check re-runs, so a trace and a transcript cannot describe different runs.
4. The page tests each visual kind in the browser and records it with its primitive and feature.

## What is not decided

1. Whether the pairings of device and RDODI primitive are the ones the owner wants recorded in the page ABox.
2. Whether devices 7 and 14 should get a slide form (7 is drawable; 14 cannot run in PowerPoint).
3. When chapter 3 counts as mature. Chapters 1, 2 and 4 wait for that judgement, and SEN0401 is a separate course with its own repository.

## Known limits

- PowerPoint animations cannot be seen in the LibreOffice renderer used here, so the click builds were checked in the file's XML, not on screen.
- The trace tracer follows a while loop's test and a for loop's first line; a program with several loops in one function needs a marker per loop.
