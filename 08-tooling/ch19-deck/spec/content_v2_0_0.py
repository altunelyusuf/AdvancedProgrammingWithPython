"""Chapter 19 deck content, version 2.0.0: the words of the deck (analogies, stories, notes, take-aways, resources, tables).
Source of the plan: the owner-approved draft 03-materials/ch19/DRAFT_ch19_v1_0_0.md (approved 2026-11-12), with one addition and two differences, all reported in the lineage:
(a) a fifth analogy slide (the practice programs) so that every research concept has its everyday picture, 42 slides instead of 41;
(b) the 'schedule package' slide is built on the standard library (the sched module with a stand-in clock), because a stand-in clock shows the order exactly and needs no thread, which the page's Pyodide cannot start;
(c) the two short table slides (opening files; Task Scheduler, launchd and cron) are native comparison tables.
Every concept label of the chapter research (sen0414_ch19_research_v1_0_6.ttl, 40 labels) has its everyday analogy here, under the research's own label.
The six stories follow the draft (facts read from the Wikipedia pages Unix time, Year 2038 problem, Cron, Leap second, Tz database and Gregorian calendar, with the numbers measured in
this study); each is told as who, what, when, where, why and how, with its live link."""
__version__ = "2.0.0"

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

# ---- everyday analogies, grouped on the analogy slides: (slide id, title, headline analogy, [(research label, everyday picture)])
ANALOGIES = [
    ("A1", "Everyday pictures: the time module", "A kilometre-zero stone is the epoch: every distance on the road is counted from it.", [
        ("The time Module", "A wall clock and a stopwatch in one drawer."),
        ("Returning the Epoch Timestamp", "Reading the distance from the stone: one number, whatever the city."),
        ("Pausing Programs", "An alarm clock that wakes you after at least that long, never sooner."),
        ("time", "The drawer itself: clocks, a stopwatch and a pause button."),
        ("Step 1: Set Up the Program to Track Times", "Pressing the stopwatch and writing down the start."),
        ("Step 2: Track and Print Lap Times", "Pressing lap each time a runner passes, and printing the split."),
        ("stopwatch.py", "The finished stopwatch, ready to run from a file."),
        ("Ideas for Similar Programs (stopwatch)", "The same stopwatch timing a kettle, a typing test or a download."),
    ]),
    ("A2", "Everyday pictures: the datetime module", "A boarding pass shows a date, a time and the city whose clock it uses.", [
        ("The datetime Module", "A calendar page and a clock face on the same card."),
        ("datetime", "That card: year, month, day, hour, minute and second together."),
        ("Representing Duration", "A flight's length: hours and minutes, not a date."),
        ("Pausing Until a Specific Date", "Setting an alarm for tomorrow's seven o'clock, not for in 600 minutes."),
        ("Converting datetime Objects into Strings", "Writing the boarding pass out in the format the airport wants."),
        ("Converting Strings into datetime Objects", "Reading a handwritten date and refusing it if the format is wrong."),
        ("Table 19-1: strftime() directives", "The key to the airport's format codes: %Y is the year, %d the day."),
    ]),
    ("A3", "Everyday pictures: subprocess", "run() is asking a colleague to do a job and bring back the result.", [
        ("Launching Other Programs from Python", "Asking a colleague to do a job instead of doing it yourself."),
        ("subprocess", "The internal phone that reaches every colleague."),
        ("Passing Command Line Arguments to Processes", "Handing over the job as a list of items, not one spoken sentence."),
        ("Receiving Output Text from Launched Commands", "The colleague's note back: what was said, and whether it worked."),
        ("Opening Files with Default Applications", "Handing a letter to the person at the desk who always opens letters."),
        ("webbrowser", "A courier who only ever goes to web addresses."),
        ("hello.txt", "A small note left on the desk for the application to open."),
        ("Figure 19-1: a screenshot of six overlapping calculator programs", "Six colleagues all started at once: six windows open on the desk."),
    ]),
    ("A4", "Everyday pictures: scheduling", "A caretaker who checks a list every minute is cron; a repeating alarm is a schedule.", [
        ("Running Task Scheduler, launchd, and cron", "The building's caretaker: told once, then comes back at the set times."),
        ("calcProd.py", "A small job written on the caretaker's list."),
        ("pyperclip", "A clipboard that every program in the building can read and write."),
        ("calcProd.py (online materials)", "The same job, supplied as a file."),
    ]),
    ("A5", "Everyday pictures: the practice programs", "A kitchen timer counts down and rings; a stopwatch counts up and notes the laps.", [
        ("Practice Programs", "Three small recipes that use everything from the earlier parts."),
        ("Step 1: Count Down", "Turning the kitchen timer's dial and watching the numbers fall."),
        ("Step 2: Play the Sound File", "The bell at the end of the countdown."),
        ("Ideas for Similar Programs (countdown)", "The same timer for tea, for a talk, for a break."),
        ("simplecountdown.py", "The timer recipe as a file."),
        ("playsound3", "The bell: one call that plays a sound file."),
        ("alarm.wav", "The sound of the bell, stored as a file."),
        ("Prettified Stopwatch", "The stopwatch with its laps written in neat columns."),
        ("Friday the 13th Finder", "Turning calendar pages one day at a time, looking for a pattern."),
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
        title="Story: A counter that wraps on 19 January 2038", img="image_y2038.jpg",
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
        how="Python dates are proleptic: date(1582, 10, 5) exists and is a Tuesday, as if the reform never happened.",
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
STORY_NOTES = {
    "epoch": "The Unix manuals counted time from 1971, then 1972, in sixtieths of a second; 1970 and seconds came afterwards. The picture shows a PDP-11, the kind of machine Unix ran on, in a museum. Lesson: an epoch is a convention engineers chose.",
    "y2038": "A signed 32-bit counter runs out at 03:14:07 UTC on 19 January 2038 and wraps to December 1901. The picture is a diagram of that wrap. Lesson: know how many bits your timestamp has.",
    "gregorian": "After 4 October 1582 came 15 October. The picture is a calendar of October 1582 with the days missing. Python's date is proleptic: it applies today's calendar backwards. Lesson: before 1582 Python dates are not the dates people used.",
    "leap": "Twenty-seven leap seconds were added from 1972 to 2016, and POSIX time skips them. The picture shows an atomic clock, the kind that keeps the seconds. Lesson: epoch seconds are not SI seconds.",
    "tzdb": "The time zone rules are data that people maintain, and a lawsuit once shut the database down. The picture is a map of the world's time zones. Lesson: keep tzdata up to date.",
    "cron": "Version 7 cron woke every minute; the Purdue version kept an event list. The picture shows a VAX computer of the kind the story is about. Lesson: a scheduler is a daemon, and the job does not inherit your shell.",
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

# ---- speaker notes, at most 60 words each
NOTES = {
    "title": "Welcome. Chapter 19 is about time and about other programs. Every example runs on the chapter page, in the order of this deck. Clocks and sleeps use a stand-in clock where waiting would be slow; the slide says so.",
    "route": "Five parts. Time as a number, dates and times of day, launching other programs, scheduling, and three practice programs. The table gives the slides and the number of examples in each part.",
    "questions": "Two questions to carry through. How does a program measure and print a moment without being wrong? And how does it start other programs and run jobs later, safely? The summary and the practice questions return to them.",
    "divider1": "Part one. A timestamp is a count of seconds from the epoch. time() can be set by hand, monotonic() cannot, sleep() promises only at least, and a stopwatch needs one clock.",
    "divider2": "Part two. datetime holds dates, times and durations. strftime writes text, strptime reads it. A time zone turns a moment into a clock reading, and a day can have 23 hours.",
    "divider3": "Part three. subprocess asks another program to do a job. run waits, Popen does not, the exit code says how it went, and a list of arguments is safer than a string for a shell.",
    "divider4": "Part four. Scheduling means later or again. sched keeps a list of jobs in order, cron fields say when a job runs, and the system schedulers start your program for you.",
    "divider5": "Part five. Three small programs: a countdown, a prettified stopwatch and a Friday the 13th finder. Each one uses calls from the earlier parts.",
    "A1": "A kilometre-zero stone is the epoch, the timestamp is the distance, and perf_counter is the stopwatch. Sleep wakes you after at least that long. The stopwatch needs one clock for every lap.",
    "A2": "A boarding pass holds a date, a time and a city's clock. A flight's length is a timedelta. Writing and reading the pass use format codes; a wrong code is refused.",
    "A3": "run is asking a colleague to do a job and bring back the result. Popen hands over the job and carries on. The exit code is the colleague's reply. A list of items is safer than a spoken sentence.",
    "A4": "A caretaker who checks a list every minute is cron. Told once, it comes back at the set times. calcProd and pyperclip are the small job and the shared clipboard from the chapter.",
    "A5": "A kitchen timer counts down and rings. A stopwatch counts up and notes laps. A Friday the 13th finder turns calendar pages one day at a time.",
    "epoch": "calendar.timegm turns a date into seconds since 1 January 1970 UTC. Second 0 is the epoch; 2**31 - 1 is the last second a signed 32-bit number holds, and the next one reads as 1901.",
    "clocks": "time() follows the wall clock, which can be set back. monotonic() and perf_counter() never go back. Use monotonic() for how long, time() for what time. The set-back numbers are a stand-in, not a real change.",
    "sleep": "sleep returns None and promises at least that long. Sleeping a second after each piece of work drifts: three thousand six hundred rounds end 72 seconds late. A fixed tick does not drift.",
    "stopwatch": "A stand-in clock moves by given gaps, so the laps are exact. Each lap is the clock now minus the last lap; the total is the clock now minus the start. The real program waits for the Enter key.",
    "durations": "A timedelta keeps days, seconds and microseconds, never months. days and seconds are parts; total_seconds is the whole. Subtract 365 times 30 days and you land a week away from the same date in 1996.",
    "strftime": "strftime writes a datetime as text from directives: %Y year, %m month, %d day, %H hour, %I and %p twelve-hour time, %A and %B names, %j day of the year. isoformat is the standard text.",
    "strptime": "strptime reads text with a format and raises ValueError when they differ. A two-digit year is read with a pivot: 69 to 99 are 1969 to 1999, and 00 to 68 are 2000 to 2068.",
    "zones": "A naive datetime has no zone; an aware one has. They cannot be compared or subtracted. ZoneInfo turns one moment into the clock reading of any zone: second one million shows three readings.",
    "dst": "Adding one day to noon in New York on 7 March gives noon the next day, but only 23 hours passed. At the autumn change 01:30 happens twice; fold tells which. Compare moments in UTC.",
    "run": "run launches a program, waits and returns a result. capture_output collects stdout and stderr as bytes; text=True gives str. returncode 0 means success. The child here is Python itself, so the example runs anywhere.",
    "popen": "Popen starts the program and returns at once. poll returns None while it runs; wait blocks and returns the exit code. A missing program raises FileNotFoundError; check=True raises CalledProcessError for a non-zero code.",
    "exits": "0 is success, any other number a failure. An uncaught exception ends with 1. On Linux and macOS a negative return code is the signal that ended the child: minus 9 for KILL, minus 15 for TERM.",
    "shell": "A string given to a shell can carry a second command. shlex.quote protects one value. A list of arguments with no shell is safest, because nothing is parsed as commands.",
    "compare_open": "Opening a file in its default program differs by system. webbrowser.open works everywhere. os.startfile is Windows only. open on macOS and xdg-open on Linux are programs you launch with subprocess. Not run here.",
    "compare_native": "Each system has its own scheduler. Task Scheduler on Windows, launchd on macOS, cron on Linux. They start your program at set times, so it does not have to wait in memory.",
    "sched": "sched keeps events in order of time, then priority. The stand-in clock is advanced instead of sleeping, so run finishes at once and shows the order. The real clock would sleep until each job is due.",
    "cron": "A cron entry has five fields: minute, hour, day of month, month, weekday. This small matcher knows only a star and lists, and counts Sunday as 0. It steps a minute at a time until every field matches.",
    "countdown": "Project 15 counts down and then plays a sound. A number stands in for the clock, so the run is instant. The real program sleeps one second per count and calls playsound3 for the alarm.",
    "pretty": "rjust pads each number to a fixed width so the columns line up. The same laps as the first stopwatch, now in neat columns.",
    "friday": "Step one day at a time from a start date with a timedelta. A date is a Friday the 13th when day is 13 and weekday is 4, because Monday is 0. Ten dates are collected.",
    "practice": "Predict first, then run what you can on the chapter page. Each question points to the part where the idea was shown.",
    "summary": "Five sentences. A timestamp counts seconds from the epoch. datetime holds dates and durations. A moment needs a zone. subprocess takes a list of arguments. A scheduler starts your program for you.",
    "resources": "Links to read next: the chapter, the documentation of the modules, the POSIX definition of epoch seconds, the crontab manual and the pages behind the stories.",
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

SUMMARY_ANALOGY = "A day's plan: a clock to read, a calendar to write in, colleagues to call, a caretaker to remind you."
SUMMARY_POINTS = [
    "A timestamp counts seconds from the epoch; 32 bits run out in 2038.",
    "Use monotonic() for how long; sleep() promises only 'at least'.",
    "datetime holds dates and durations; strftime and strptime convert text.",
    "A moment needs a zone, and a day can have 23 hours.",
    "subprocess takes a list of arguments; the exit code says how it went.",
]
SUMMARY_TAKEAWAY = "Two questions of slide 3: measure a moment correctly, and start jobs safely."

PRACTICE_SUB = "Use the slide of the part named in each question"
PRACTICE_ANALOGY = "Predict first, as you would guess the weather before you look out of the window."
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
