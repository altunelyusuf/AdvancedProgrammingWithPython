"""Chapter 19 deck content, version 4.0.0 (SEN0414, Lineage13): the words of the deck. Derived from content 2.2.0 with one change, made to meet the ruling of 2026-11-24: the five analogy slides state what each concept is and does in plain words, with no everyday comparison; the notes are in notes_v4_0_0.py. Parts, plan, stories, take-aways, tables, practice and resources are unchanged. Earlier text of 2.0.0 follows.

Source of the plan: the owner-approved draft 03-materials/ch19/DRAFT_ch19_v1_0_0.md (approved 2026-11-12), with one addition and two differences, all reported in the lineage:
(a) a fifth concept slide (the practice programs) so that every research concept has its own line, 42 slides instead of 41;
(b) the 'schedule package' slide is built on the standard library (the sched module with a stand-in clock), because a stand-in clock shows the order exactly and needs no thread, which the page's Pyodide cannot start;
(c) the two short table slides (opening files; Task Scheduler, launchd and cron) are native comparison tables.
Every concept label of the chapter research (sen0414_ch19_research_v1_0_6.ttl, 40 labels) has its plain explanation here, under the research's own label.
The six stories follow the draft (facts read from the Wikipedia pages Unix time, Year 2038 problem, Cron, Leap second, Tz database and Gregorian calendar, with the numbers measured in
this study); each is told as who, what, when, where, why and how, with its live link."""
__version__ = "4.0.0"

PARTS = {
    1: ("Part 1: Time as a number (the time module)", "A moment is a count of seconds from one agreed starting point", [
        ("epoch", "The starting point every timestamp counts from"),
        ("clocks", "time() can be set by hand; monotonic() cannot"),
        ("sleep", "Pauses a program; promises only 'at least'"),
        ("stopwatch", "Laps from one clock, printed as they happen")]),
    2: ("Part 2: Dates and times of day (the datetime module)", "A date, a time of day, and the length of time between two of them", [
        ("timedelta", "A length of time: days, seconds, never months"),
        ("strftime", "Turns a datetime into text with directives"),
        ("strptime", "Turns text into a datetime, or raises ValueError"),
        ("zoneinfo", "Time zone rules, so that a day can have 23 hours")]),
    3: ("Part 3: Launching other programs (subprocess)", "Ask another program to do a job, then read what it says", [
        ("run()", "Launch, wait, collect the output"),
        ("Popen()", "Launch now and carry on; wait for it later"),
        ("exit code", "0 is success; a negative number is a signal"),
        ("arguments", "A list of arguments, not one string for a shell")]),
    4: ("Part 4: Scheduling tasks", "Work that happens later, or again and again", [
        ("sched", "An in-process list of jobs ordered by time"),
        ("priority", "Equal times: the lower number goes first"),
        ("cron", "Five fields say when a job runs"),
        ("native tools", "Task Scheduler, launchd and cron start jobs for you")]),
    5: ("Part 5: Practice programs", "Three small programs that combine the parts", [
        ("countdown", "Count down, then sound an alarm"),
        ("stopwatch", "Laps again, with columns that line up"),
        ("Friday the 13th", "Step through the days with a date and a timedelta")]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("story", "epoch"), ("code", "epoch"), ("code", "clocks"), ("story", "y2038"), ("code", "sleep"), ("code", "stopwatch"),
        ("divider", 2), ("analogy", "A2"), ("story", "gregorian"), ("code", "durations"), ("code", "strftime"), ("code", "strptime"), ("story", "leap"), ("code", "zones"), ("code", "dst"), ("story", "tzdb"),
        ("divider", 3), ("analogy", "A3"), ("code", "run"), ("code", "popen"), ("code", "exits"), ("code", "shell"), ("compare", "open"),
        ("divider", 4), ("analogy", "A4"), ("story", "cron"), ("code", "sched"), ("code", "cron"), ("compare", "native"),
        ("divider", 5), ("analogy", "A5"), ("code", "countdown"), ("code", "pretty"), ("code", "friday"), ("practice",),
        ("summary",), ("resources",)]

ROUTE_RUNS = {1: "epoch, clocks, sleep, a stopwatch", 2: "durations, text both ways, zones, DST", 3: "run, Popen, exit codes, shell safety",
              4: "sched, cron fields, system schedulers", 5: "countdown, stopwatch, Friday the 13th"}
ROUTE_TAIL = ("Summary and links", "what to remember, where next")

QUESTIONS = [
    ("1", "How does a program measure, store and print a moment without being wrong about clocks, zones and calendars?", "The five points come back on slide %d.", "summary"),
    ("2", "How does a program start other programs, and run its own jobs later, without a shell surprise?", "Check yourself with the questions on slide %d.", "practice"),
]
QUESTIONS_TAKEAWAY = "Every example runs on the chapter page; read its printed result first."

# ---- plain concept slides (no everyday comparison, ruling of 2026-11-24): (slide id, title, headline in one plain sentence, [(research label, what it is and does)])
BOX_LABEL = "IN SHORT"
TABLE_HEAD = "What it is and does"
CONCEPTS_TAIL = "each explained in plain words"
ANALOGIES = [
    ("A1", "The time module and the stopwatch", "A timestamp is one number: the seconds counted from the epoch, 1 January 1970 UTC.", [
        ("The time Module", "The standard-library module with the wall clock, the monotonic clocks, sleep and the conversions."),
        ("Returning the Epoch Timestamp", "time.time() returns the seconds since the epoch as a float, the same number in every time zone."),
        ("Pausing Programs", "time.sleep(n) pauses the program for at least n seconds and returns None."),
        ("time", "The module that holds the clocks: time(), monotonic(), perf_counter() and sleep()."),
        ("Step 1: Set Up the Program to Track Times", "The stopwatch reads a clock once at the start and keeps that reading."),
        ("Step 2: Track and Print Lap Times", "A lap is the clock now minus the clock at the last lap, printed at each press."),
        ("stopwatch.py", "The finished stopwatch of the book, a program file that runs from the command line."),
        ("Ideas for Similar Programs (stopwatch)", "The same two readings time any job: a download, a typing test or a function call."),
    ]),
    ("A2", "The datetime module: dates, times and durations", "A datetime holds a date and a time of day; a timedelta holds a length of time.", [
        ("The datetime Module", "The standard-library module with date, time, datetime, timedelta and timezone."),
        ("datetime", "One object with year, month, day, hour, minute and second, with or without a time zone."),
        ("Representing Duration", "A timedelta stores days, seconds and microseconds, so it measures a length, not a date."),
        ("Pausing Until a Specific Date", "A loop compares datetime.now() with a target moment and sleeps until it is reached."),
        ("Converting datetime Objects into Strings", "strftime() writes a datetime as text, using the directives of its format string."),
        ("Converting Strings into datetime Objects", "strptime() reads text with a format and raises ValueError when they differ."),
        ("Table 19-1: strftime() directives", "The list of format codes: %Y is the year, %m the month, %d the day, %H the hour."),
    ]),
    ("A3", "Launching programs with subprocess", "subprocess.run() starts another program, waits for it and returns its result.", [
        ("Launching Other Programs from Python", "A Python program can start any other program of the machine and read what it prints."),
        ("subprocess", "The standard-library module that starts child processes: run(), Popen() and the helpers."),
        ("Passing Command Line Arguments to Processes", "The arguments go in a list, one item for each argument, so no shell has to split a string."),
        ("Receiving Output Text from Launched Commands", "capture_output=True collects stdout and stderr; text=True gives strings, not bytes."),
        ("Opening Files with Default Applications", "Each system has its own way to open a file with the program registered for it."),
        ("webbrowser", "The module whose open() shows a web page in the default browser on every system."),
        ("hello.txt", "A small text file of the book that the examples open with its default application."),
        ("Figure 19-1: a screenshot of six overlapping calculator programs", "Six child processes started together each open their own window."),
    ]),
    ("A4", "Scheduling tasks with system schedulers", "A scheduler starts a job at the times it is given, so the job need not wait in memory.", [
        ("Running Task Scheduler, launchd, and cron", "Windows, macOS and Linux each have a system scheduler that starts programs at set times."),
        ("calcProd.py", "A small program of the book that multiplies the numbers on the clipboard; the schedulers run it."),
        ("pyperclip", "A third-party module that reads and writes the clipboard from Python, on every system."),
        ("calcProd.py (online materials)", "The same program, supplied as a file in the online materials of the book."),
    ]),
    ("A5", "The practice programs: timer, laps, Fridays", "Each practice program combines calls of the earlier parts: a clock, a pause and a date.", [
        ("Practice Programs", "Three programs: a countdown timer, a prettified stopwatch and a Friday the 13th finder."),
        ("Step 1: Count Down", "A loop prints the remaining seconds and pauses one second at each step."),
        ("Step 2: Play the Sound File", "After the loop, one call plays a sound file as the alarm."),
        ("Ideas for Similar Programs (countdown)", "The same loop makes a timer for any wait: tea, a talk or a break."),
        ("simplecountdown.py", "The countdown timer of the book as a program file."),
        ("playsound3", "A third-party module whose playsound() plays a sound file with the system player."),
        ("alarm.wav", "The sound file of the alarm, played when the countdown ends."),
        ("Prettified Stopwatch", "The stopwatch with its laps padded to fixed widths, so the columns line up."),
        ("Friday the 13th Finder", "A loop steps one day at a time with a timedelta and keeps the dates that fit."),
    ]),
]

# ---- the stories (5N1K); the picture of each is a record of story_images_v1_0_0.json
STORIES = {
    "epoch": dict(
        title="Story: Unix chose its 1970 epoch after two earlier ones", img="image_pdp11.jpg",
        who="The Unix engineers at Bell Labs, whose Programmer's Manual described the time call.",
        what="Time counted in sixtieths of a second from 1971, then from 1972; 1970 came later.",
        when="First edition 3 November 1971, third edition 15 March 1972; the 1970 epoch afterwards.",
        where="In the Unix Programmer's Manual; the third edition says the time is stored in 32 bits.",
        why="Sixtieths of a second in 32 bits last about 2.3 years, so the unit became seconds.",
        how="gmtime(0) gives 1970-01-01 00:00:00 and timegm of it gives 0: the epoch is a convention.",
        linktext="Unix time (Wikipedia)", link="https://en.wikipedia.org/wiki/Unix_time"),
    "y2038": dict(
        title="Story: A counter that wraps on 19 January 2038", img="image_y2038_commons.png",
        who="Programs and devices that keep Unix time in a signed 32-bit integer.",
        what="The second after 03:14:07 UTC on 19 January 2038 does not fit; the counter becomes negative.",
        when="On 19 January 2038, with warnings long before.",
        where="In any system with a 32-bit time; this study's machine used 8 bytes, datetime reaches year 9999.",
        why="A signed 32-bit number has no room for the next value, so it reads as a date in December 1901.",
        how="Example 1 shows 2**31 - 1 as 2038-01-19T03:14:07 and -2**31 as 1901-12-13T20:45:52.",
        linktext="Year 2038 problem (Wikipedia)", link="https://en.wikipedia.org/wiki/Year_2038_problem"),
    "gregorian": dict(
        title="Story: In October 1582 ten days did not happen", img="image_oct1582.jpg",
        who="Pope Gregory XIII, who issued the bull Inter gravissimas.",
        what="A calendar reform that advanced the date by 10 days to bring Easter back to its season.",
        when="Bull dated 24 February 1582; Thursday 4 October 1582 was followed by Friday 15 October.",
        where="In the Gregorian calendar, which is named after him.",
        why="The calendar had drifted from the seasons, and Easter drifted with it.",
        how="Python dates are proleptic: date(1582, 10, 5) exists and is a Tuesday, because the reform is ignored.",
        linktext="Gregorian calendar (Wikipedia)", link="https://en.wikipedia.org/wiki/Gregorian_calendar"),
    "leap": dict(
        title="Story: Twenty-seven leap seconds since 1972", img="image_clock.jpg",
        who="The timekeepers of the BIPM and the General Conference on Weights and Measures.",
        what="Leap seconds: 27 added since 1972, the last on 31 December 2016; UTC and TAI differ by 37 seconds.",
        when="From 1972 to 31 December 2016; a 2022 resolution looks ahead to 2035.",
        where="Resolution 4 of the 27th General Conference, 2022: the allowed UT1-UTC difference will grow.",
        why="UTC is kept close to the Earth's rotation, and the rotation is not steady.",
        how="POSIX gives every day 86400 seconds, so 23:59:60 has no timestamp; datetime refuses a 60th second.",
        linktext="Leap second (Wikipedia)", link="https://en.wikipedia.org/wiki/Leap_second"),
    "tzdb": dict(
        title="Story: A lawsuit shut down the tz database in 2011", img="image_tzmap.jpg",
        who="Arthur David Olson, its founder; Paul Eggert, who designed the names; ICANN and the EFF.",
        what="A lawsuit over atlas data closed the database's mailing list and FTP site.",
        when="Filed 30 September 2011; closed 6 October; ICANN took over 14 October; resolved 22 February 2012.",
        where="The tz database, with roots in 1986 or earlier; Python's zoneinfo reads it.",
        why="Astrolabe sued Olson and others over copyright in atlas data.",
        how="Here tzdata is 2026.5 and the system copy 2026c; Istanbul was +02:00 in January 1970, +03:00 in 2026.",
        linktext="Tz database (Wikipedia)", link="https://en.wikipedia.org/wiki/Tz_database"),
    "cron": dict(
        title="Story: Cron woke every minute until Purdue's event list", img="image_vax.jpg",
        who="Robert Brown, a Purdue graduate student, who read the paper of Franta and Maly.",
        what="An event-list cron that sleeps until the next job; the old one woke every minute.",
        when="In the late 1970s, after the 1977 paper.",
        where="At Purdue University, on a time-shared VAX with 100 users.",
        why="Version 7 cron used resources with or without work and overloaded the machine when shared.",
        how="Cron 3.0pl1 here started a job with PATH=/usr/bin:/bin, in /root, with no terminal.",
        linktext="Cron (Wikipedia)", link="https://en.wikipedia.org/wiki/Cron"),
}
# ---- the two native comparison tables
COMPARES = {
    "open": dict(
        title="Opening files and web pages with the default program", sub="A short slide: three jobs, three calls, and where each works",
        colw=[2.4, 3.6, 3.0], rowh=0.55, fs=11,
        rows=[["The job", "The call", "Where it works"],
              ["Open a web page", "webbrowser.open(url)", "Windows, macOS and Linux; True if a browser started"],
              ["Open a file in its default application", "os.startfile(path)", "Windows only"],
              ["Open a file in its default application", "subprocess.run(['open', path])", "macOS"],
              ["Open a file in its default application", "subprocess.run(['xdg-open', path])", "Linux desktops"],
              ["Run a program and wait for it", "subprocess.run([program, argument])", "everywhere; see the earlier slides"]],
        takeaway="Not run here: a machine without a screen has no default application to open."),
    "native": dict(
        title="Running Task Scheduler, launchd and cron", sub="Each system starts your program for you; the program does not wait in memory",
        colw=[2.0, 2.4, 2.5, 2.5], rowh=0.58, fs=11,
        rows=[["", "Task Scheduler", "launchd", "cron"],
              ["Runs on", "Windows", "macOS", "Linux and other Unix"],
              ["Where the schedule lives", "the Task Scheduler app, or the schtasks command", "property-list files, loaded with launchctl", "a crontab file, edited with crontab -e"],
              ["How you say when", "triggers: a time, a logon, an event", "keys such as StartCalendarInterval", "five fields: minute hour day month weekday"],
              ["Shown in this deck", "-", "-", "the cron-fields slide"]],
        takeaway="One schedule format per system; the cron slide reads the five fields."),
}

# ---- one take-away line for every code slide
TAKEAWAY = {
    "epoch": "A timestamp is a count of seconds from one agreed moment.",
    "clocks": "monotonic() for how long; time() for what time it is.",
    "sleep": "sleep() waits at least that long; a loop that sleeps after its work drifts.",
    "stopwatch": "Each lap is the clock now minus the clock at the last lap.",
    "durations": "A timedelta has days and seconds; months are not a unit.",
    "strftime": "Directives such as %Y and %d write the text you ask for.",
    "strptime": "The format must match the text exactly, or ValueError.",
    "zones": "Name the zone; a naive and an aware time cannot be compared.",
    "dst": "A day can have 23 hours; compare moments in UTC.",
    "run": "capture_output=True and text=True give you the output as a string.",
    "popen": "Popen returns at once; poll() looks, wait() waits.",
    "exits": "0 means success; a negative code is the signal that ended the child.",
    "shell": "Pass a list of arguments and no shell, and nothing is read as a command.",
    "sched": "sched runs jobs soonest first; equal times go by priority.",
    "cron": "Five fields say when: minute, hour, day of month, month, weekday.",
    "countdown": "Count down in a loop, then play the sound.",
    "pretty": "rjust() makes the columns line up.",
    "friday": "weekday() is 4 for Friday; step with a timedelta.",
}

SUMMARY_ANALOGY = "Five points: a timestamp counts seconds, datetime holds dates, a moment needs a zone, subprocess takes a list, a scheduler starts jobs."
SUMMARY_POINTS = [
    "A timestamp counts seconds from the epoch; 32 bits run out in 2038.",
    "Use monotonic() for how long; sleep() promises only 'at least'.",
    "datetime holds dates and durations; strftime and strptime convert text.",
    "A moment needs a zone, and a day can have 23 hours.",
    "subprocess takes a list of arguments; the exit code says how it went.",
]
SUMMARY_TAKEAWAY = "Two questions of slide 3: measure a moment correctly, and start jobs safely."

PRACTICE_SUB = "Use the slide of the part named in each question"
PRACTICE_ANALOGY = "Each practice question has a short answer; run the code on the chapter page to check it."
PRACTICE = [
    "What does time.sleep() return, and why does 'work, then sleep(1)' in a loop drift? Use the sleep slide.",
    "Why can you not subtract a naive datetime from an aware one, and how long is the day the clocks change?",
    "What do strptime() and strftime() do, and what happens when the format does not match?",
    "What does run() return, and what do a returncode of 0 and of -9 tell you? Use the exit-codes slide.",
    "Which five fields does a cron entry have, and which day of the week is 0?",
]
PRACTICE_TAKEAWAY = "Run the examples on the chapter page to check each answer."

RESOURCES_SUB = "The chapter, the documentation, and the pages behind the stories"
RESOURCES_TAKEAWAY = "Every link was opened on 2026-11-12 and answered."
RESOURCES = [
    ("Gregorian calendar (Wikipedia)", "https://en.wikipedia.org/wiki/Gregorian_calendar", "en.wikipedia.org"),
    ("Book: Automate the Boring Stuff, 3rd edition, chapter 19", "https://automatetheboringstuff.com/3e/chapter19.html", "automatetheboringstuff.com"),
    ("Python documentation: time", "https://docs.python.org/3.14/library/time.html", "docs.python.org"),
    ("Python documentation: datetime", "https://docs.python.org/3.14/library/datetime.html", "docs.python.org"),
    ("Python documentation: zoneinfo", "https://docs.python.org/3.14/library/zoneinfo.html", "docs.python.org"),
    ("Python documentation: subprocess", "https://docs.python.org/3.14/library/subprocess.html", "docs.python.org"),
    ("POSIX: seconds since the epoch", "https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap04.html", "pubs.opengroup.org"),
    ("The crontab manual (Debian)", "https://manpages.debian.org/bookworm/cron/crontab.5.en.html", "manpages.debian.org"),
    ("Unix time (Wikipedia)", "https://en.wikipedia.org/wiki/Unix_time", "en.wikipedia.org"),
    ("Year 2038 problem (Wikipedia)", "https://en.wikipedia.org/wiki/Year_2038_problem", "en.wikipedia.org"),
    ("Cron (Wikipedia)", "https://en.wikipedia.org/wiki/Cron", "en.wikipedia.org"),
    ("Tz database (Wikipedia)", "https://en.wikipedia.org/wiki/Tz_database", "en.wikipedia.org"),
    ("schedule on PyPI", "https://pypi.org/pypi/schedule/json", "pypi.org"),
    ("tzdata on PyPI", "https://pypi.org/pypi/tzdata/json", "pypi.org"),
]


# ---- stories told as natural prose, three short paragraphs each (owner's rule: 5N1K human storytelling, never WHO/WHAT labels); the six facts stay in the records above
STORY_PROSE = {
 "epoch": ["In 1971 the Unix engineers at Bell Labs wrote a manual that counted time in sixtieths of a second from 1971; the third edition, in March 1972, counted from 1972.",
           "That edition said the time is stored in 32 bits, and sixtieths of a second in 32 bits last only about 2.3 years, so the unit became whole seconds.",
           "Only afterwards did 1970 become the epoch. gmtime(0) gives 1970-01-01 00:00:00: an epoch is a convention people chose, not a law of nature."],
 "y2038": ["Programs and devices that keep Unix time in a signed 32-bit integer have a deadline: at 03:14:07 UTC on 19 January 2038 the next second no longer fits.",
           "The counter turns negative, so the clock reads a date in December 1901. Systems with 8-byte times are safe, and datetime reaches year 9999.",
           "Example 1 shows it: 2**31 - 1 prints as 2038-01-19T03:14:07 and -2**31 prints as 1901-12-13T20:45:52. Warnings came long before."],
 "gregorian": ["Pope Gregory XIII issued the bull Inter gravissimas, dated 24 February 1582, because the calendar had drifted from the seasons and Easter had drifted with it.",
               "The Gregorian calendar, named after him, advanced the date by 10 days: Thursday 4 October 1582 was followed by Friday 15 October.",
               "Python dates are proleptic, so the reform is ignored: date(1582, 10, 5) exists, and it is a Tuesday."],
 "leap": ["The timekeepers of the BIPM and the General Conference on Weights and Measures keep UTC close to the Earth's rotation, and that rotation is not steady.",
          "So they added 27 leap seconds from 1972 to 31 December 2016, and UTC and TAI now differ by 37 seconds. A 2022 resolution looks ahead to 2035.",
          "POSIX gives every day 86400 seconds, so 23:59:60 has no timestamp, and Python's datetime refuses a 60th second."],
 "tzdb": ["Arthur David Olson founded the tz database and Paul Eggert designed its names. On 30 September 2011 Astrolabe sued Olson and others over copyright in atlas data.",
          "The mailing list and FTP site closed on 6 October; ICANN took over on 14 October, with the EFF involved, and the case was resolved on 22 February 2012.",
          "Python's zoneinfo reads this database. Here tzdata is 2026.5 and the system copy 2026c; Istanbul was +02:00 in January 1970 and +03:00 in 2026."],
 "cron": ["Robert Brown, a Purdue graduate student, read the 1977 paper of Franta and Maly. At Purdue a time-shared VAX with 100 users was being overloaded.",
          "Version 7 cron woke every minute, with or without work. Brown wrote a cron with an event list that sleeps until the next job.",
          "Cron 3.0pl1 here started a job with PATH=/usr/bin:/bin, in /root, with no terminal, so a job does not inherit your shell."],
}
for _k, _v in STORY_PROSE.items():
    STORIES[_k]["prose"] = _v
