# Chapter 19 Draft — Keeping Time, Scheduling Tasks and Launching Programs (v1.0.0)

**Status note:** checked against live files on 2026-11-12: deck `sen0414_ch19_deck_v1_0_0.pptx (26 slides, in 08-tooling/ch19-deck)`, page `sen0414_ch19_page_v9_34_0.html`, no chapter-code manifest, stories script v1_0_0 (6 stories, self-check clean, no link shared with chapters 1 to 18; the story-repeat check `sen0414_story_repeat_check_v1_0_0.py` is clean). The deck standard check v1.0.0 fails D1 D2 D3 D4 D5 D7 D11; D10 and M1 not measured. This chapter never received the retrofit that chapters 9 to 18 received, so this draft is the plan of a new deck, page and manifest, built after your approval. Nothing has been built.

## 1. The story (6 beats, one per concept, sourced)

1. **3 November 1971 and 15 March 1972, and the epoch of 1 January 1970 afterwards — The Unix engineers at Bell Labs, whose Programmer's Manual described the time call.** Wikipedia's article on Unix time cites the first edition of the Unix Programmer's Manual, dated 3 November 1971, which says time returns the time since 00:00:00, Jan. 1, 1971, measured in sixtieths of a second. The third edition, dated 15 March 1972, counts from Jan. 1, 1972, and adds that the time is stored in 32 bits, which guarantees a crisis every 2.26 years. Counting sixtieths of a second in 32 bits runs out after 2**32 / 60 seconds, which is 2.27 years by this study's arithmetic. The article says the current epoch of 1 January 1970 was selected arbitrarily by Unix engineers because it was a convenient date to work with, and the precision was changed to seconds to avoid short-term overflow. In this study time.gmtime(0) gave 1970-01-01 00:00:00 and calendar.timegm of that moment gave 0. *Lesson: An epoch is a convention that engineers chose; do not treat it as nature.* (https://en.wikipedia.org/wiki/Unix_time)

2. **19 January 2038, with the first warnings long before — Programs and devices that keep Unix time in a signed 32-bit integer.** Wikipedia's article on the year 2038 problem says some computer systems cannot represent times after 03:14:07 UTC on 19 January 2038, because they count Unix time in a signed 32-bit integer. The next second does not fit, and the counter wraps to a negative number, which such a system reads as a date in December 1901. In this study 2**31 - 1 was 2038-01-19T03:14:07 UTC, 2**31 packed in 32 bits and read back as signed was -2147483648, and that is 20:45:52 UTC on 13 December 1901. The time_t of the machine in this study had 8 bytes, and the datetime module accepted timestamps up to the end of the year 9999. *Lesson: Know how many bits your timestamp has before 2038 teaches you.* (https://en.wikipedia.org/wiki/Year_2038_problem)

3. **Version 7 Unix, then an experiment at Purdue in the late 1970s that drew on a 1977 paper — Robert Brown, a Purdue graduate student, after the paper of Franta and Maly.** Wikipedia's article on cron says the cron of Version 7 Unix was a daemon that read its crontab, ran the commands due at that minute as root, slept for one minute and repeated. It was robust but consumed resources whether or not there was work, and an experiment at Purdue University in the late 1970s to give cron's service to all 100 users of a time-shared VAX put too much load on the system. A Purdue graduate student, Robert Brown, recognised the parallel between cron and discrete event simulators after reading the article of Franta and Maly and built an event-list implementation. On this study's machine cron 3.0pl1 started a Python job at the turn of a minute with PATH=/usr/bin:/bin, the working directory /root and no terminal. *Lesson: A scheduler is a daemon, and the job does not inherit your shell.* (https://en.wikipedia.org/wiki/Cron)

4. **1972 to 31 December 2016, and the resolution of 2022 that looks to 2035 — The timekeepers of the BIPM and the General Conference on Weights and Measures.** Wikipedia's article on the leap second says it was introduced in 1972, when UTC already lagged TAI by 10 seconds, that 27 leap seconds have been added since, the most recent on 31 December 2016, and that UTC and TAI now differ by 37 seconds. Resolution 4 of the 27th General Conference on Weights and Measures, in 2022, decides that the maximum value of the difference UT1-UTC will be increased in, or before, 2035. POSIX never counted a leap second: its expression gives every day 86400 seconds, and in this study calendar.timegm saw one second between 23:59:59 on 31 December 2016 and the next midnight, while datetime refused a 60th second. The time of 23:59:60 therefore has no epoch timestamp of its own. *Lesson: Epoch seconds are not SI seconds; leap seconds are skipped.* (https://en.wikipedia.org/wiki/Leap_second)

5. **30 September 2011 to 22 February 2012 — Arthur David Olson, founder of the database, Paul Eggert, and the people who kept it, the Electronic Frontier Foundation and ICANN.** Wikipedia's article on the tz database says its origins go back to 1986 or earlier, that Arthur David Olson is the founding contributor and that Paul Eggert designed the names such as America/New_York. On 30 September 2011 a lawsuit, Astrolabe against Olson and others, was filed over copyright in atlas data, and on 6 October 2011 the database's mailing list and FTP site were shut down. ICANN took responsibility for the database on 14 October 2011, and the lawsuit was resolved on 22 February 2012 after the Electronic Frontier Foundation took part. Python's zoneinfo reads this database: in this study the tzdata package was 2026.5, the system copy 2026c, and Istanbul was +02:00 in January 1970 and +03:00 in 2026. *Lesson: Time zone rules are data that people maintain; keep tzdata current.* (https://en.wikipedia.org/wiki/Tz_database)

6. **24 February 1582 for the bull, and October 1582 for the ten days — Pope Gregory XIII, who issued the bull Inter gravissimas.** Wikipedia's article on the Gregorian calendar says it was instituted by the papal bull Inter gravissimas dated 24 February 1582 by Pope Gregory XIII, after whom it is named. To bring Easter back to the season of its introduction the reform advanced the date by 10 days, so Thursday 4 October 1582 was followed by Friday 15 October 1582. The Python documentation calls date an idealized naive date, assuming the current Gregorian calendar always was, and always will be, in effect. In this study date(1582, 10, 5) existed and was a Tuesday, and date(1582, 10, 15) was a Friday, as in the history. *Lesson: Python dates are proleptic; before 1582 they are not the dates people used.* (https://en.wikipedia.org/wiki/Gregorian_calendar)

Pictures: each story slide gets a real picture from Wikimedia Commons or another free source whose licence is read at build; where no free picture of the person or object exists, the slide says so and shows a document picture, never an invented one. Each story is told as who, what, when, where, why and how, with its live link and a lesson of at most 14 words.

## 2. Slide / page-tab outline (18 code examples; the example number is the page-tab order)

| Slide | Title | Code example |
|---|---|---|
| 1 | >>> |  |
| 2 | Today's route |  |
| 3 | Two questions this chapter answers |  |
| 4 | Part 1: Time as a number (the time module) |  |
| 5 | Everyday pictures: the time module |  |
| 6 | Story: Unix counted from 1971, then 1972, before the epoch of 1970 was chosen |  |
| 7 | Returning the epoch timestamp: time.time() and the number behind a date | 1 |
| 8 | Clocks and what each measures: time.time(), perf_counter(), monotonic() | 2 |
| 9 | Story: A counter that wraps at 03:14:07 UTC on 19 January 2038 |  |
| 10 | Pausing programs: time.sleep() and what it does not promise | 3 |
| 11 | A first stopwatch with perf_counter() | 4 |
| 12 | Part 2: Dates and times of day (the datetime module) |  |
| 13 | Everyday pictures: the datetime module |  |
| 14 | Story: In October 1582 ten days did not happen, and Python does not skip them |  |
| 15 | datetime: dates, times, timedelta and duration arithmetic | 5 |
| 16 | datetime to string: strftime() and its directives (Table 19-1) | 6 |
| 17 | String to datetime: strptime() and its errors | 7 |
| 18 | Story: Twenty-seven leap seconds since 1972, and a decision to stop adding them |  |
| 19 | Time zones with zoneinfo | 8 |
| 20 | Daylight saving time: a day with 23 or 25 hours | 9 |
| 21 | Story: A lawsuit shut down the time zone database's mailing list and site in 2011 |  |
| 22 | Part 3: Launching other programs (subprocess) |  |
| 23 | Everyday pictures: subprocess |  |
| 24 | subprocess.run(): launch a program and read its output | 10 |
| 25 | subprocess.Popen(): start now, wait later | 11 |
| 26 | Exit codes and signals | 12 |
| 27 | Shell safety: lists of arguments, not strings | 13 |
| 28 | Opening files with their default applications, and webbrowser: a short slide |  |
| 29 | Part 4: Scheduling tasks |  |
| 30 | Everyday pictures: scheduling |  |
| 31 | Story: Cron woke every minute until Purdue students gave it an event list |  |
| 32 | In-process scheduling with the schedule package | 14 |
| 33 | Cron fields: when does a job next run? | 15 |
| 34 | Running Task Scheduler, launchd and cron: a native comparison table |  |
| 35 | Part 5: Practice programs |  |
| 36 | Practice: countdown timer | 16 |
| 37 | Practice: prettified stopwatch | 17 |
| 38 | Practice: Friday the 13th finder | 18 |
| 39 | Practice questions |  |
| 40 | Summary |  |
| 41 | Resources |  |

Total 41 slides. Each code example sits on its own slide with a short explanation beside the code and the executed result drawn as a visual (a native chart or table where the result is numbers; no picture of a chart); the example list is exactly the page tabs, in this order. Every slide is numbered, text boxes stay at or below 30 words and speaker notes at or below 60 words. Examples are run under the chapter's pinned Python and packages and nothing needing an account is run against a real service: the Gmail steps use the stand-in the research set already has, and the ntfy steps a local recorder.

### Everyday pictures (analogies), one slide at the start of each part

- **Part 1 — the time module:** a wall clock shows the time of day, a stopwatch counts how long, a kilometre-zero stone is the point every distance is counted from: the epoch is the stone, the timestamp is the distance, perf_counter() is the stopwatch.
- **Part 2 — the datetime module:** a calendar page is a date, a clock face is a time, a flight's duration is a timedelta, a boarding pass printed in another city's time is a time zone.
- **Part 3 — subprocess:** asking a colleague to do a job and bring back the result is run(); handing them the job and carrying on is Popen(); the colleague's 'done' or 'could not' is the exit code; giving a colleague a typed-out sentence to obey is the shell, giving a list of arguments is the safe way.
- **Part 4 — scheduling:** an alarm clock is one task at one time, a repeating alarm is a schedule, a caretaker who checks a list every minute is cron.

The analogy slides cover the key concepts of the chapter's research set (36); concepts not named above are carried by an analogy box on the slide that teaches them, and the deck standard check D4 and D11 count them.

## 3. Resources slide (14 links, as the current deck has them, unchanged)

1. https://en.wikipedia.org/wiki/Gregorian_calendar  (answered 200 on 2026-11-12)
2. https://automatetheboringstuff.com/3e/chapter19.html  (answered 200 on 2026-11-12)
3. https://docs.python.org/3.14/library/time.html  (answered 200 on 2026-11-12)
4. https://docs.python.org/3.14/library/datetime.html  (answered 200 on 2026-11-12)
5. https://docs.python.org/3.14/library/zoneinfo.html  (answered 200 on 2026-11-12)
6. https://docs.python.org/3.14/library/subprocess.html  (answered 200 on 2026-11-12)
7. https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap04.html  (answered 200 on 2026-11-12)
8. https://manpages.debian.org/bookworm/cron/crontab.5.en.html  (answered 200 on 2026-11-12)
9. https://en.wikipedia.org/wiki/Unix_time  (answered 200 on 2026-11-12)
10. https://en.wikipedia.org/wiki/Year_2038_problem  (answered 200 on 2026-11-12)
11. https://en.wikipedia.org/wiki/Cron  (answered 200 on 2026-11-12)
12. https://en.wikipedia.org/wiki/Tz_database  (answered 200 on 2026-11-12)
13. https://pypi.org/pypi/schedule/json  (answered 200 on 2026-11-12)
14. https://pypi.org/pypi/tzdata/json  (answered 200 on 2026-11-12)

## 4. Open items

- **What the build changes:** deck from 26 slides to about 41, one example per slide, analogies, story pictures, short notes; a chapter-code manifest of 18 examples; page rebuilt on the current template with the stories and chapter-code tab. The research-artifact folder `rdodi/` is not touched.
- **Resources:** unchanged from the current deck. Your standing wish for a resources slide with community, corpus, seminal works, tutorials and videos is only partly met by these links (no video, no community link). Say if you want videos and a community link added; each would be found and checked live before it goes in.
- **Known limits:** the page test on this machine stops at 70 features when the browser tab crashes (the accepted pages do the same); the build will report what ran and what did not.
