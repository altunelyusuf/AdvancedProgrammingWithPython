# Report: the repair of the Definition of Done (1.22.0) and what it left open (2026-11-26)

## What happened on 2026-11-20 (register 1.22.0)
The newest framework check (backlog_next_act 1.2.0, shape DoneNeedsRunningCriterionShape, G237) refused ten Done stories because the Definition of Done DoD10 had no criterion that runs. I repaired it by giving DoD10 four criteria: DeckChecks and OwnVersion (run by named tools, recorded `Holds`), StoryRepeat (run, recorded `Violated`: two story candidates in chapter 10 awaited the owner) and ContentUnchanged (cannot be machine-run: it needs the owner's reading, recorded `NotYetEnforceable`). The check passed and the lineage stayed open.

## What I found today, from the archived register
Neither of the last two criteria was ever updated. The lineage was closed (1.50.0) and archived (1.52.0) with DoD10_StoryRepeat still `Violated` and DoD10_ContentUnchanged still `NotYetEnforceable`, and I wrote that all conditions held. That statement was wrong. It repeats my own root cause 7 (status stated, not computed from the register).

## The facts today
- **StoryRepeat now holds.** The two chapter 10 candidates (UTF-8 against chapter 8, JSON against chapter 7) are no longer in chapter 10: its stories are ThompsonDbm1979, MsDos2BackslashPaths1983, KildallDriveLetters1974 and PitrouPathlib2012. The whole-course check (`sen0414_story_repeat_check_v1_0_0.py 1 25`) gives "2 to read": chapter 3 against chapter 2 and chapter 14 against chapter 2, none in chapters 10, 11, 16 or 17. The chapter 17 DocxNameTrap2014 story and chapter 16 PythonGainsSqlite2006 overlap 0.135 and were not judged.
- **ContentUnchanged is open.** It needs the owner to read the re-cut story prose and balloon sentences against the approved drafts. He has not.

## What this changes
The closure rests on nine measured objectives, all met, and those stand. The Definition of Done did not fully hold at closure: one criterion was stale and one never run. The closure is therefore full achievement of the mission's measured objectives with the owner's reading still outstanding, not an unqualified close.

## Repair proposed
1. Record the correction in the live register against the archive entry: StoryRepeat `Holds` on 2026-11-26 with the run named; ContentUnchanged still waiting for the owner's reading.
2. The owner reads, or rules that the reading is not needed; either answer is then recorded.
3. The framework part (a closure that ignores a Violated criterion) is point 4 of the handover to BRSF.
