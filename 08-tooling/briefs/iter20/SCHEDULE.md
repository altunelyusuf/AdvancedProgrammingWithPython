# Iteration 20: how the executors are started (for the coordinator; not part of any brief)

Register 2.237.0. 16 chapters (10 to 25) x 6 tasks + the Cross.B pilot (4 tasks). Rule: **at most three executor sessions at once**; the highest-ranked startable task takes a free place; **one page build at a time** (a page build holds the page-test lock for hours); the controller's page tests wait in the same lock queue; the Cross.B pilot takes a place only when no higher-ranked task can start. Rank = the story scores (chapter 10 highest ... chapter 25 lowest, Cross.B last).

## Start now (three decks side by side)
1. `08-tooling/briefs/iter20/BRIEF_TK_Ret_Ch10_Deck_Build.md`  (session SEN0414-I20-deck-ch10)
2. `08-tooling/briefs/iter20/BRIEF_TK_Ret_Ch11_Deck_Build.md`  (session SEN0414-I20-deck-ch11)
3. `08-tooling/briefs/iter20/BRIEF_TK_Ret_Ch12_Deck_Build.md`  (session SEN0414-I20-deck-ch12)

Tell the lineage agent the real start of each (UTC, no zone suffix); it records work begun with `sen0414_lineage_work_begun_v1_8_0.py`.

## Then, as each task is controlled (the lineage agent tells you "controlled, start X")
| Controlled | Starts next (if a place is free; otherwise the next row) |
|---|---|
| Deck ch10 | Page build ch10 (`BRIEF_TK_Ret_Ch10_Page_Build.md`) |
| Deck ch11 | Page build ch11 only after the page build ch10 is controlled; meanwhile the free place takes deck ch13 |
| Deck ch12 | deck ch13, then ch14, ... in chapter order |
| Page ch10 | Research ch10 (`BRIEF_TK_Ret_Ch10_Research.md`) and Page build ch11 (a page place and a research place are different kinds) |
| any freed place | the highest-ranked startable task: research of the lowest chapter whose page is controlled, else the page build of the lowest chapter whose deck is controlled, else the deck build of the lowest chapter without one |

In steady state the three places are: one deck, one page, one research session. The Cross.B pilot (`BRIEF_TK_Gap_CrossB_Spec.md`, then `BRIEF_TK_Gap_CrossB_Build.md` after its control) takes the place of a deck session only when all 16 decks have started.

All briefs are in `08-tooling/briefs/iter20/` (INDEX.md lists the session and whether a task can start). Briefs are passed unedited. Not a promise that all sixteen chapters finish inside the seven days (gap d of ex:IA2_Iter20); a chapter not Done at the review is carried by the change route.
