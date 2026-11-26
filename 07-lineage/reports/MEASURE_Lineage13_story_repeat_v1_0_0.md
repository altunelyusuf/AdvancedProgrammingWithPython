# Lineage13 measurement: story repeat over chapters 16 to 20 (2026-11-26)

Check: `08-tooling/sen0414_story_repeat_check_v1_0_0.py 1 25` (log `08-tooling/lineage13-opening/story_repeat/story_repeat_1_25.log`). It compares each story with the stories of earlier chapters by shared link, shared names of people or bodies, and word overlap (listed for reading from 0.25). It is a lower bound: it cannot know a story told in other words from another source.

Result for chapters 16 to 20 (29 stories): no shared link; highest word overlap 0.135 (chapter 17 DocxNameTrap2014 with chapter 16 PythonGainsSqlite2006), none near 0.25. Two shared names were read against the stories themselves:

| Story | Shared name with | Reading | Verdict |
|---|---|---|---|
| Chapter 18, XML 1.0 becomes a W3C Recommendation (1998) | Chapter 8, nine companies agree on one table of characters (1991): Sun Microsystems | The company is named in both; one is the standard of XML under Jon Bosak, the other the founding of the Unicode consortium | different stories |
| Chapter 19, Unix counted from 1971 | Chapter 5, the most effective debugging tool (1979), and chapter 8, the placemat encoding (1992): Bell Labs | The laboratory is named in each; the three stories are about a time call, a debugging sentence and an encoding | different stories |

Outside this lineage: the one repeat candidate of the check is chapters 2 and 3 (PEP 572, same link), already carried as a disclosure; chapter 21 (Pil1995) and chapter 18 (ElementTreeOrigin2001) share Fredrik Lundh, which belongs to the lineage that takes chapter 21.

Conclusion: no story of chapters 16 to 20 repeats a story of another chapter; no candidate for the Owner. The Definition of Done criterion StoryRepeat holds for these five chapters.
