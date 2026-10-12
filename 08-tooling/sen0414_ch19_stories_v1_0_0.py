"""SEN0414 chapter 19 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Six stories for
keeping time, scheduling tasks and launching programs, written fresh for this chapter from pages opened on 2026-10-13 (the HTTP status each
link answered to a plain GET on that day is in LINK_STATUS, and `python3 sen0414_ch19_stories_v1_0_0.py links` asks again):

* UnixEpoch1971 - the first edition of the Unix Programmer's Manual (3 November 1971) counted from 1 January 1971 in sixtieths of a second; the third
  edition (15 March 1972) counted from 1 January 1972 and said a 32-bit count 'guarantees a crisis every 2.26 years'; the epoch of 1 January 1970
  'was selected arbitrarily' (Wikipedia, 'Unix time').
* Year2038Wrap - a signed 32-bit time_t overflows at 03:14:07 UTC on 19 January 2038 (Wikipedia, 'Year 2038 problem').
* CronPurdue1977 - cron in Version 7 Unix slept one minute and rescanned; an experiment at Purdue in the late 1970s put 100 users on a time-shared
  VAX and showed the load, and the graduate student Robert Brown built an event-list version after reading Franta and Maly (Wikipedia, 'Cron').
* LeapSecond1972 - leap seconds began in 1972, 27 have been added, the last on 31 December 2016, and the CGPM decided in 2022 to increase the
  maximum difference UT1-UTC in or before 2035 (Wikipedia, 'Leap second'; BIPM, Resolution 4 of the 27th CGPM).
* TzLawsuit2011 - a copyright lawsuit filed on 30 September 2011 shut down the tz database's mailing list on 6 October 2011, ICANN took over on
  14 October 2011, and the lawsuit ended on 22 February 2012 (Wikipedia, 'Tz database').
* Gregorian1582 - the bull Inter gravissimas of 24 February 1582 made Thursday 4 October 1582 be followed by Friday 15 October 1582, a day
  that Python's date type does not skip (Wikipedia, 'Gregorian calendar'; the Python documentation of datetime).

Photograph: see ch19-page/stories_img_v1_0_0.json for what was fetched and under which licence, or why no photograph is used.
A claim the research first planned and dropped: the exact date on which the first Unix cron was written, for which no page opened on the day
gives a date that another source of the study confirms.
Usage: import STORIES; run the file for self-checks, or with the argument links to ask every link again.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "UnixEpoch1971",
        "title": "Unix counted from 1971, then 1972, before the epoch of 1970 was chosen",
        "when": "3 November 1971 and 15 March 1972, and the epoch of 1 January 1970 afterwards",
        "who": "The Unix engineers at Bell Labs, whose Programmer's Manual described the time call",
        "where": "The first and third editions of the Unix Programmer's Manual, the time system call",
        "link": "https://en.wikipedia.org/wiki/Unix_time",
        "concepts": ["EpochZero", "FloatPrecision"],
        "story": ("Wikipedia's article on Unix time cites the first edition of the Unix Programmer's Manual, dated 3 November 1971, which says time returns the time since 00:00:00, Jan. 1, 1971, "
                  "measured in sixtieths of a second. The third edition, dated 15 March 1972, counts from Jan. 1, 1972, and adds that the time is stored in 32 bits, which guarantees a crisis every 2.26 years. "
                  "Counting sixtieths of a second in 32 bits runs out after 2**32 / 60 seconds, which is 2.27 years by this study's arithmetic. "
                  "The article says the current epoch of 1 January 1970 was selected arbitrarily by Unix engineers because it was a convenient date to work with, and the precision was changed to seconds to avoid short-term overflow. "
                  "In this study time.gmtime(0) gave 1970-01-01 00:00:00 and calendar.timegm of that moment gave 0."),
        "lesson": "An epoch is a convention that engineers chose; do not treat it as nature",
        "source": ("Wikipedia, 'Unix time' (the epoch selected arbitrarily; the manual of 3 November 1971 with the epoch of 1971; the manual of 15 March 1972 with the epoch of 1972 and 2.26 years), read 2026-10-13; "
                   "this study's leaves EpochZero and FloatPrecision."),
    },
    {
        "id": "Year2038Wrap",
        "title": "A counter that wraps at 03:14:07 UTC on 19 January 2038",
        "when": "19 January 2038, with the first warnings long before",
        "who": "Programs and devices that keep Unix time in a signed 32-bit integer",
        "where": "Embedded systems, file formats and old C programs; Python on 64-bit platforms is not among them",
        "link": "https://en.wikipedia.org/wiki/Year_2038_problem",
        "concepts": ["Year2038", "DatetimeRange"],
        "story": ("Wikipedia's article on the year 2038 problem says some computer systems cannot represent times after 03:14:07 UTC on 19 January 2038, because they count Unix time in a signed 32-bit integer. "
                  "The next second does not fit, and the counter wraps to a negative number, which such a system reads as a date in December 1901. "
                  "In this study 2**31 - 1 was 2038-01-19T03:14:07 UTC, 2**31 packed in 32 bits and read back as signed was -2147483648, and that is 20:45:52 UTC on 13 December 1901. "
                  "The time_t of the machine in this study had 8 bytes, and the datetime module accepted timestamps up to the end of the year 9999."),
        "lesson": "Know how many bits your timestamp has before 2038 teaches you",
        "source": ("Wikipedia, 'Year 2038 problem' (03:14:07 UTC on 19 January 2038, signed 32-bit integers), read 2026-10-13; "
                   "this study's leaves Year2038 and DatetimeRange."),
    },
    {
        "id": "CronPurdue1977",
        "title": "Cron woke every minute until Purdue students gave it an event list",
        "when": "Version 7 Unix, then an experiment at Purdue in the late 1970s that drew on a 1977 paper",
        "who": "Robert Brown, a Purdue graduate student, after the paper of Franta and Maly",
        "where": "A time-shared VAX at Purdue University with 100 users, and the cron of Version 7 Unix",
        "link": "https://en.wikipedia.org/wiki/Cron",
        "concepts": ["CronFields", "CronEnvironment"],
        "story": ("Wikipedia's article on cron says the cron of Version 7 Unix was a daemon that read its crontab, ran the commands due at that minute as root, slept for one minute and repeated. "
                  "It was robust but consumed resources whether or not there was work, and an experiment at Purdue University in the late 1970s to give cron's service to all 100 users of a time-shared VAX put too much load on the system. "
                  "A Purdue graduate student, Robert Brown, recognised the parallel between cron and discrete event simulators after reading the article of Franta and Maly and built an event-list implementation. "
                  "On this study's machine cron 3.0pl1 started a Python job at the turn of a minute with PATH=/usr/bin:/bin, the working directory /root and no terminal."),
        "lesson": "A scheduler is a daemon, and the job does not inherit your shell",
        "source": ("Wikipedia, 'Cron' (Version 7 algorithm; Purdue in the late 1970s; Robert Brown and the Franta-Maly event list manager), read 2026-10-13; "
                   "this study's real cron run (live record) and leaves CronFields and CronEnvironment."),
    },
    {
        "id": "LeapSecond1972",
        "title": "Twenty-seven leap seconds since 1972, and a decision to stop adding them",
        "when": "1972 to 31 December 2016, and the resolution of 2022 that looks to 2035",
        "who": "The timekeepers of the BIPM and the General Conference on Weights and Measures",
        "where": "UTC, the time scale that civil clocks follow, kept near the rotation of the Earth",
        "link": "https://en.wikipedia.org/wiki/Leap_second",
        "concepts": ["PosixFormula", "GapAndFold"],
        "story": ("Wikipedia's article on the leap second says it was introduced in 1972, when UTC already lagged TAI by 10 seconds, that 27 leap seconds have been added since, the most recent on 31 December 2016, and that UTC and TAI now differ by 37 seconds. "
                  "Resolution 4 of the 27th General Conference on Weights and Measures, in 2022, decides that the maximum value of the difference UT1-UTC will be increased in, or before, 2035. "
                  "POSIX never counted a leap second: its expression gives every day 86400 seconds, and in this study calendar.timegm saw one second between 23:59:59 on 31 December 2016 and the next midnight, while datetime refused a 60th second. "
                  "The time of 23:59:60 therefore has no epoch timestamp of its own."),
        "lesson": "Epoch seconds are not SI seconds; leap seconds are skipped",
        "source": ("Wikipedia, 'Leap second' (introduced 1972; 27 leap seconds; latest 31 December 2016; UTC-TAI 37 s), read 2026-10-13; BIPM, Resolution 4 of the 27th CGPM (2022), read 2026-10-13; "
                   "POSIX 4.19; this study's leaf PosixFormula."),
    },
    {
        "id": "TzLawsuit2011",
        "title": "A lawsuit shut down the time zone database's mailing list and site in 2011",
        "when": "30 September 2011 to 22 February 2012",
        "who": "Arthur David Olson, founder of the database, Paul Eggert, and the people who kept it, the Electronic Frontier Foundation and ICANN",
        "where": "The tz database, the source of America/Los_Angeles and Europe/Istanbul in zoneinfo",
        "link": "https://en.wikipedia.org/wiki/Tz_database",
        "concepts": ["ZoneInfoZones", "FromTimestampZones"],
        "story": ("Wikipedia's article on the tz database says its origins go back to 1986 or earlier, that Arthur David Olson is the founding contributor and that Paul Eggert designed the names such as America/New_York. "
                  "On 30 September 2011 a lawsuit, Astrolabe against Olson and others, was filed over copyright in atlas data, and on 6 October 2011 the database's mailing list and FTP site were shut down. "
                  "ICANN took responsibility for the database on 14 October 2011, and the lawsuit was resolved on 22 February 2012 after the Electronic Frontier Foundation took part. "
                  "Python's zoneinfo reads this database: in this study the tzdata package was 2026.5, the system copy 2026c, and Istanbul was +02:00 in January 1970 and +03:00 in 2026."),
        "lesson": "Time zone rules are data that people maintain; keep tzdata current",
        "source": ("Wikipedia, 'Tz database' (the lawsuit of 30 September 2011, the shutdown of 6 October 2011, ICANN on 14 October 2011, the resolution of 22 February 2012), read 2026-10-13; "
                   "this study's leaves ZoneInfoZones and FromTimestampZones."),
    },
    {
        "id": "Gregorian1582",
        "title": "In October 1582 ten days did not happen, and Python does not skip them",
        "when": "24 February 1582 for the bull, and October 1582 for the ten days",
        "who": "Pope Gregory XIII, who issued the bull Inter gravissimas",
        "where": "The Catholic countries that adopted the Gregorian calendar first; others followed centuries later",
        "link": "https://en.wikipedia.org/wiki/Gregorian_calendar",
        "concepts": ["GregorianCalendar", "WeekdayOfDate"],
        "story": ("Wikipedia's article on the Gregorian calendar says it was instituted by the papal bull Inter gravissimas dated 24 February 1582 by Pope Gregory XIII, after whom it is named. "
                  "To bring Easter back to the season of its introduction the reform advanced the date by 10 days, so Thursday 4 October 1582 was followed by Friday 15 October 1582. "
                  "The Python documentation calls date an idealized naive date, assuming the current Gregorian calendar always was, and always will be, in effect. "
                  "In this study date(1582, 10, 5) existed and was a Tuesday, and date(1582, 10, 15) was a Friday, as in the history."),
        "lesson": "Python dates are proleptic; before 1582 they are not the dates people used",
        "source": ("Wikipedia, 'Gregorian calendar' (the bull of 24 February 1582; Thursday 4 October 1582 followed by Friday 15 October 1582), read 2026-10-13; Python 3.14 documentation of datetime; "
                   "this study's leaves GregorianCalendar and WeekdayOfDate."),
    },
]

LINK_STATUS = {'UnixEpoch1971': 200, 'Year2038Wrap': 200, 'CronPurdue1977': 200, 'LeapSecond1972': 200, 'TzLawsuit2011': 200, 'Gregorian1582': 200}


def run_checks():
    bad = []
    ids = [x["id"] for x in STORIES]
    if len(ids) != len(set(ids)):
        bad.append("duplicate story ids")
    for x in STORIES:
        for f in ("who", "where", "link", "when", "title", "lesson", "source", "story"):
            if not str(x.get(f, "")).strip():
                bad.append("%s: missing %s (5N1K)" % (x["id"], f))
        if not x.get("link", "").startswith("http"):
            bad.append("%s: link is not a URL" % x["id"])
        if len(x["lesson"].split()) > 14:
            bad.append("%s: lesson over 14 words" % x["id"])
        if not (2 <= x["story"].count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % x["id"])
        if LINK_STATUS and LINK_STATUS.get(x["id"]) != 200:
            bad.append("%s: link status %r, not 200" % (x["id"], LINK_STATUS.get(x["id"])))
        if not LINK_STATUS:
            bad.append("LINK_STATUS is empty")
    by = {x["id"]: x for x in STORIES}
    for sid, year in (("UnixEpoch1971", "1971"), ("Year2038Wrap", "2038"), ("CronPurdue1977", "1977"), ("LeapSecond1972", "1972"), ("TzLawsuit2011", "2011"), ("Gregorian1582", "1582")):
        if year not in by[sid]["story"] and year not in by[sid]["when"]:
            bad.append("%s: date missing from story" % sid)
        if year not in by[sid]["when"] and year not in by[sid]["story"]:
            bad.append("%s: year %s not in when" % (sid, year))
    return bad


def ask_links():
    import urllib.request, urllib.error
    out = {}
    for x in STORIES:
        req = urllib.request.Request(x["link"], headers={"User-Agent": "SEN0414-research/1.0 (teaching; altunel.yusuf@gmail.com)"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out[x["id"]] = r.status
        except urllib.error.HTTPError as e:
            out[x["id"]] = e.code
        except Exception as e:
            out[x["id"]] = type(e).__name__
    return out


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "links":
        print(ask_links())
    else:
        b = run_checks()
        print(len(STORIES), "stories; self-check failures:", len(b))
        for x in b:
            print("  ", x)
