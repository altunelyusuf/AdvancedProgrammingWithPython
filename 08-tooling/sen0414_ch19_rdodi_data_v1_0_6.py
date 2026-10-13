"""Chapter 19 content for the RDODI build: sources, findings, taxonomy and section bodies.
The book's chapter was read on automatetheboringstuff.com on 2026-10-13 (an HTTP fetch of https://automatetheboringstuff.com/3e/chapter19.html;
the page returned 200, 88,909 bytes, and its sha256, 067b9119b1a4c68cf65acedab9e68df264d609e72345fdbb112bcfd6db475db7, equals the chapterDigest the
book's own chapter ontology records; the commit the course pins was not opened). The online materials of the 3rd edition (the zip No Starch Press
links from its book page, 7,759,877 bytes, sha256 dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916) were downloaded and the three files chapter 19
uses were opened and their sha256 recorded (calcProd.py, stopwatch.py and simplecountdown.py); neither the zip nor the files are kept in this repository, and the scripts
fetch them and check the hashes. The zip holds no alarm.wav, no hello.txt, no program for the practice programs and no document about Task Scheduler, launchd or cron,
so the study made those from the chapter's own listings and says so where it matters. The Python 3.14 documentation of time, datetime, zoneinfo, subprocess,
threading, sched, asyncio, signal, webbrowser, os, shlex, calendar and plistlib, the PEPs, POSIX, the RFCs, the manual pages of cron, systemd and launchd,
PyPI, the pages of the stories and the other sources were opened on the same day. Every behaviour was executed under Python 3.14.6 (the newest
3.14 release uv offered; python.org lists 3.14.8 and 3.15.0) installed with uv on Ubuntu 24.04 (Linux, the zone of the shell Europe/Istanbul, the system zone UTC,
the system tz database 2026c) in dedicated environments with pyperclip 1.11.0, playsound3 3.3.2, tzdata 2026.5 and schedule 1.2.2, and the chapter's statements were also
replayed with the versions Appendix A of the book pins (playsound3 2.4.0). Cron 3.0pl1 was installed with apt and run for real on the machine.
Not executed, and said so where it comes up: a Windows computer (calc.exe, notepad, mspaint, the start command, Task Scheduler and schtasks), a Mac
(the open command for an application, launchd and launchctl), a systemd timer (PID 1 here is not systemd; systemd-analyze only normalised expressions), a desktop
session in which xdg-open or a browser could open anything, the sound (no audio device) and a clipboard program, the names of months and days in a locale other
than C, Python 3.14.7, 3.14.8 and the final 3.15.0 (uv offered only 3.15.0b4), the commit the course pins, and the ping to nostarch.com (the container's network lost the packets).
The chapter's 75 interactive statements are replayed by sen0414_ch19_thirdparty_v1_0_0.py into 08-tooling/ch19-page/third_party_record_v1_0_0.json;
what the public sites and the shipped files did on the day, and what cron did on the machine, is in ch19-page/live_observations_v1_0_0.json; what one program printed under eleven interpreters
(3.11, 3.12, 3.13, the seven 3.14 releases 3.14.0 to 3.14.6 and 3.15.0b4) is in ch19-page/interpreter_record_v1_0_0.json. A claim not in this file was not made."""
__version__ = "1.0.6"
# 1.0.0 to 1.0.4 of the chapter 19 data module are already committed (the earlier builds of the chapter); this version rebuilds the chapter at the standard of
# chapters 13 to 18: two cross-referenced paragraphs per section, the shipped files opened, the chapter's statements replayed, cron run for real, and the public sources as they
# answered on 2026-10-13. The data module is 1.0.5 because 1.0.0 to 1.0.4 are already committed.
# 1.0.6 (2026-10-13): one example, ArgumentList, read the text a child program printed with eval(); it now reads it with ast.literal_eval() (and imports ast),
# which gives the same value and does not run what it reads. The result of the example is unchanged. Nothing else changed: the sections, the findings, the claims
# and the stored results are those of 1.0.5.
CH = 19
DATE = "2026-10-13"
PYVER = "3.14.6"
TITLE = "Keeping time, scheduling tasks and launching programs for an advanced course: chapter 19 and today's time, datetime, zoneinfo, subprocess, cron and Python"
QUESTION = "What does chapter 19 of the 3rd edition teach about reading the clock, dates and durations, launching other programs and scheduling them, which of its printed outputs, programs and statements still hold under Python 3.14.6 (with pyperclip 1.11.0, playsound3 3.3.2 and schedule 1.2.2, and with the versions its Appendix A pins), and what must an advanced course correct or add so that it matches the current time, datetime, zoneinfo and subprocess modules, the time zone database and the real behaviour of the operating system's schedulers?"
CQS = ("Which clock answers which question, which moments and durations can a datetime hold and which does it refuse or misread, and how does a program launch, wait for, stop and schedule another program on an operating system where the commands of the book do not exist?",
       "Which printed outputs, programs, numbers and statements of the chapter differ in current releases of Python, in the zone and the clock of the author, in the files the book ships or in the pages it points to, and on what source?")
PUBS = [
 ('P01', 'Automate the Boring Stuff with Python, 3rd edition - Chapter 19, Keeping Time, Scheduling Tasks, and Launching Programs (Al Sweigart, No Starch Press, 2025)', 'https://automatetheboringstuff.com/3e/chapter19.html', True),
 ('P02', 'Online materials of the 3rd edition, zip with calcProd.py, stopwatch.py, simplecountdown.py and 88 other files (No Starch Press, 2025)', 'https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', False),
 ('P03', 'Automate the Boring Stuff with Python, 3rd edition - table of contents (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/', False),
 ('P04', 'Automate the Boring Stuff with Python, 3rd edition - book page (No Starch Press, 2025)', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', False),
 ('P05', 'Appendix A, Installing Third-Party Modules, with the versions the book pins (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/appendixa.html', False),
 ('P06', 'Appendix B, Answers to the Practice Questions (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/appendixb.html', False),
 ('P07', 'simplecountdown.py as served at autbor.com (Al Sweigart, 2025)', 'https://autbor.com/simplecountdown.py', False),
 ('P08', 'strftime.org, the page the chapter names for the strftime directives, now the BairesDev strftime cheatsheet (BairesDev, 2026)', 'https://strftime.org', False),
 ('P09', 'Beyond the Basic Stuff with Python, Chapter 13, Performance Measurement and Big O (Al Sweigart, No Starch Press, 2020)', 'https://inventwithpython.com/beyond/chapter13.html', False),
 ('P10', 'time - Time access and conversions (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/time.html', False),
 ('P11', 'datetime - Basic date and time types (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/datetime.html', False),
 ('P12', 'zoneinfo - IANA time zone support (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/zoneinfo.html', False),
 ('P13', 'subprocess - Subprocess management (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/subprocess.html', False),
 ('P14', 'threading - Thread-based parallelism, Timer objects (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/threading.html', False),
 ('P15', 'sched - Event scheduler (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/sched.html', False),
 ('P16', 'asyncio - Event loop, call_later and call_at (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/asyncio-eventloop.html', False),
 ('P17', 'signal - Set handlers for asynchronous events (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/signal.html', False),
 ('P18', 'webbrowser - Convenient web-browser controller (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/webbrowser.html', False),
 ('P19', 'os - Miscellaneous operating system interfaces, startfile (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/os.html', False),
 ('P20', 'shlex - Simple lexical analysis, quote and split (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/shlex.html', False),
 ('P21', 'calendar - General calendar-related functions, timegm and isleap (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/calendar.html', False),
 ('P22', 'Built-in Types, integer string conversion length limitation (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/stdtypes.html', False),
 ('P23', 'plistlib - Generate and parse Apple plist files (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/plistlib.html', False),
 ('P24', 'timeit - Measure execution time of small code snippets (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/timeit.html', False),
 ('P25', 'Built-in Functions, round (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/functions.html', False),
 ('P26', "What's New In Python 3.14 (Python 3.14 documentation)", 'https://docs.python.org/3.14/whatsnew/3.14.html', False),
 ('P27', "What's New In Python 3.12 (Python documentation)", 'https://docs.python.org/3.12/whatsnew/3.12.html', False),
 ('P28', "What's New In Python 3.11 (Python documentation)", 'https://docs.python.org/3.11/whatsnew/3.11.html', False),
 ('P29', "What's New In Python 3.15 (Python documentation)", 'https://docs.python.org/3.15/whatsnew/3.15.html', False),
 ('P30', 'PEP 418 - Add monotonic time, performance counter, and process time functions (Victor Stinner, Python Software Foundation, 2012)', 'https://peps.python.org/pep-0418/', False),
 ('P31', 'PEP 475 - Retry system calls failing with EINTR (Charles-Francois Natali and Victor Stinner, Python Software Foundation, 2014)', 'https://peps.python.org/pep-0475/', False),
 ('P32', 'PEP 495 - Local Time Disambiguation (Alexander Belopolsky and Tim Peters, Python Software Foundation, 2015)', 'https://peps.python.org/pep-0495/', False),
 ('P33', 'PEP 615 - Support for the IANA Time Zone Database in the Standard Library (Paul Ganssle, Python Software Foundation, 2020)', 'https://peps.python.org/pep-0615/', False),
 ('P34', 'The Open Group Base Specifications Issue 8, 4.19 Seconds Since the Epoch (IEEE and The Open Group, 2024)', 'https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap04.html', False),
 ('P35', 'The Open Group Base Specifications Issue 8, crontab - schedule periodic background work (IEEE and The Open Group, 2024)', 'https://pubs.opengroup.org/onlinepubs/9799919799/utilities/crontab.html', False),
 ('P36', 'RFC 3339 - Date and Time on the Internet: Timestamps (Graham Klyne and Chris Newman, IETF, 2002)', 'https://www.rfc-editor.org/rfc/rfc3339', False),
 ('P37', 'RFC 9557 - Date and Time on the Internet: Timestamps with Additional Information (Ujjwal Sharma and Carsten Bormann, IETF, 2024)', 'https://www.rfc-editor.org/rfc/rfc9557', False),
 ('P38', 'RFC 6557 - Procedures for Maintaining the Time Zone Database (Eric Lear and Paul Eggert, IETF, 2012)', 'https://www.rfc-editor.org/rfc/rfc6557', False),
 ('P39', 'Time Zone Database (Internet Assigned Numbers Authority, 2026)', 'https://www.iana.org/time-zones', False),
 ('P40', 'crontab(5), Debian cron manual page (Paul Vixie and Debian, 2026)', 'https://manpages.debian.org/bookworm/cron/crontab.5.en.html', False),
 ('P41', 'schtasks create (Microsoft Learn, 2026)', 'https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-create', False),
 ('P42', 'launchd.plist(5) manual page (Apple, 2026)', 'https://keith.github.io/xcode-man-pages/launchd.plist.5.html', False),
 ('P43', 'systemd.timer (freedesktop.org, 2026)', 'https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html', False),
 ('P44', 'systemd.time, calendar events (freedesktop.org, 2026)', 'https://www.freedesktop.org/software/systemd/man/latest/systemd.time.html', False),
 ('P45', 'xdg-utils, xdg-open (freedesktop.org, 2026)', 'https://www.freedesktop.org/wiki/Software/xdg-utils/', False),
 ('P46', 'xdg-open(1) manual page (Ubuntu 24.04, 2026)', 'https://manpages.ubuntu.com/manpages/noble/man1/xdg-open.1.html', False),
 ('P47', 'pyperclip documentation (Al Sweigart, 2026)', 'https://pyperclip.readthedocs.io/en/latest/', False),
 ('P48', 'PyPI JSON metadata of pyperclip (Python Package Index, 2026)', 'https://pypi.org/pypi/pyperclip/json', False),
 ('P49', 'PyPI JSON metadata of playsound3 (Python Package Index, 2026)', 'https://pypi.org/pypi/playsound3/json', False),
 ('P50', 'PyPI JSON metadata of tzdata (Python Package Index, 2026)', 'https://pypi.org/pypi/tzdata/json', False),
 ('P51', 'PyPI JSON metadata of schedule (Python Package Index, 2026)', 'https://pypi.org/pypi/schedule/json', False),
 ('P52', 'Unix time (Wikipedia)', 'https://en.wikipedia.org/wiki/Unix_time', False),
 ('P53', 'Year 2038 problem (Wikipedia)', 'https://en.wikipedia.org/wiki/Year_2038_problem', False),
 ('P54', 'Cron (Wikipedia)', 'https://en.wikipedia.org/wiki/Cron', False),
 ('P55', 'Leap second (Wikipedia)', 'https://en.wikipedia.org/wiki/Leap_second', False),
 ('P56', 'Resolution 4 of the 27th CGPM (2022), On the use and future development of UTC (Bureau International des Poids et Mesures, 2022)', 'https://www.bipm.org/en/cgpm-2022/resolution-4', False),
 ('P57', 'tz database (Wikipedia)', 'https://en.wikipedia.org/wiki/Tz_database', False),
 ('P58', 'Gregorian calendar (Wikipedia)', 'https://en.wikipedia.org/wiki/Gregorian_calendar', False),
 ('P59', 'Launchd (Wikipedia)', 'https://en.wikipedia.org/wiki/Launchd', False),
 ('P60', 'Triskaidekaphobia (Wikipedia)', 'https://en.wikipedia.org/wiki/Triskaidekaphobia', False),
 ('P61', 'Coordinated Universal Time (Wikipedia)', 'https://en.wikipedia.org/wiki/Coordinated_Universal_Time', False),
 ('P62', 'ISO 8601 (Wikipedia)', 'https://en.wikipedia.org/wiki/ISO_8601', False),
 ('P63', 'uv - Python versions (Astral documentation)', 'https://docs.astral.sh/uv/concepts/python-versions/', False),
 ('P64', 'Download Python (python.org)', 'https://www.python.org/downloads/', False),
]
CONCEPTS = [
 ('Section', 'The time Module'),
 ('Section', 'Returning the Epoch Timestamp'),
 ('Section', 'Pausing Programs'),
 ('Section', 'Step 1: Set Up the Program to Track Times'),
 ('Section', 'Step 2: Track and Print Lap Times'),
 ('Section', 'Ideas for Similar Programs (stopwatch)'),
 ('Section', 'The datetime Module'),
 ('Section', 'Representing Duration'),
 ('Section', 'Pausing Until a Specific Date'),
 ('Section', 'Converting datetime Objects into Strings'),
 ('Section', 'Converting Strings into datetime Objects'),
 ('Section', 'Launching Other Programs from Python'),
 ('Section', 'Passing Command Line Arguments to Processes'),
 ('Section', 'Receiving Output Text from Launched Commands'),
 ('Section', 'Running Task Scheduler, launchd, and cron'),
 ('Section', 'Opening Files with Default Applications'),
 ('Section', 'Step 1: Count Down'),
 ('Section', 'Step 2: Play the Sound File'),
 ('Section', 'Ideas for Similar Programs (countdown)'),
 ('Section', 'Summary'),
 ('Section', 'Practice Questions'),
 ('Section', 'Practice Programs'),
 ('Section', 'Prettified Stopwatch'),
 ('Section', 'Friday the 13th Finder'),
 ('Figure', 'Figure 19-1: a screenshot of six overlapping calculator programs'),
 ('Table', 'Table 19-1: strftime() directives'),
 ('Program', 'calcProd.py'),
 ('Program', 'stopwatch.py'),
 ('Program', 'simplecountdown.py'),
 ('Module', 'time'),
 ('Module', 'datetime'),
 ('Module', 'subprocess'),
 ('Module', 'webbrowser'),
 ('Module', 'pyperclip'),
 ('Module', 'playsound3'),
 ('File', 'alarm.wav'),
 ('File', 'hello.txt'),
 ('File', 'calcProd.py (online materials)'),
 ('File', 'stopwatch.py (online materials)'),
 ('File', 'simplecountdown.py (online materials)'),
]
FINDINGS = [
 ('F1', 'Background',
  "Chapter 19 of the 3rd edition, Keeping Time, Scheduling Tasks, and Launching Programs, teaches how a program reads the clock and waits: the time module with time.time() and time.sleep() and Project 14, the Super Stopwatch; the datetime module with datetime and timedelta objects, strftime() with the directives of Table 19-1 and strptime(); and the launching of other programs with subprocess.run() and subprocess.Popen(), command line arguments, captured output and the start and open commands, ending with Project 15, the Simple Countdown, seven practice questions and two practice programs, the Prettified Stopwatch and the Friday the 13th finder [P01] [P03]. The chapter page of 2026-10-13 is 88,909 bytes with 29 listings (20 of them interactive sessions of 75 statements), 1 captioned figure (Figure 19-1, a screenshot of six calculators, with alt text) and 1 table (Table 19-1), and its sha256, 067b9119b1a4c68cf65acedab9e68df264d609e72345fdbb112bcfd6db475db7, equals the chapterDigest of the book's own chapter ontology [P01] [P03] [P04].",
  ['P01', 'P03', 'P04']),
 ('F2', 'The online materials',
  "The online materials of the 3rd edition (7,759,877 bytes, 91 files) hold three files for chapter 19, calcProd.py, stopwatch.py and simplecountdown.py, and none of alarm.wav, hello.txt, prettifiedStopwatch.py, fridayThirteenth.py or a crontab, a plist or a scheduler document [P01] [P02]. The Summary of the chapter says that the instructions for scheduling a program at a certain time are at the book's page at No Starch Press, but that page holds no such instructions (it names Scheduling Tasks only in the table of contents), and neither does the table of contents of the book online or the zip, so the one paragraph of the chapter on Task Scheduler, launchd and cron is all the book says about them [P01] [P02] [P03] [P04].",
  ['P01', 'P02', 'P03', 'P04']),
 ('F3', 'The chapter replayed',
  "The 75 statements of the chapter's 20 interactive sessions were replayed in order in a clean Python 3.14.6, with the zone of the process set to the author's America/Los_Angeles: 54 printed what the book prints and 21 did not, of which 7 depend on the clock (time.time(), time.ctime(), datetime.now(), fromtimestamp(time.time()) and the two values built from now), 1 is the en dash and 13 launch Windows or macOS programs or call a program that Linux lacks. With the dash repaired 55 match [P01]. The book's examples of the clock come from four different days (ctime at 11:05 on 17 March 2026, now() on 27 February 2026, fromtimestamp(time.time()) on 21 October 2026 and now on 2 December 2026), so no two of them can be compared; and in the zone of Istanbul one statement more differs, datetime.fromtimestamp(1000000), printed as 05:46:40 only in Los Angeles [P01].",
  ['P01']),
 ('F4', 'Four en dashes',
  "Four places in three listings of the chapter as served on its web page, listings 2, 6 (twice) and 12, write the en dash U+2013 instead of the minus sign (end_time – start_time, time.time() – last_time and oct_21st – about_thirty_years), and the interpreter refuses each with SyntaxError: invalid character '–' (U+2013); a reader who copies them gets a program that does not start [P01]. The shipped stopwatch.py has two of the dashes, uses CRLF line ends and has no f prefix on its print, so a reader who fixes the dashes still prints {lap_number}: {total_time}({lap_time}) literally, unlike the chapter, whose listing has the prefix; and the stopwatch of the chapter prints the total time and the lap time without a space between them while the practice program's output has one [P01] [P02].",
  ['P01', 'P02']),
 ('F5', 'The profiling listing',
  "The chapter times calcProd() with two time.time() readings, prints 2.844162940979004 seconds and refers to Chapter 13 of the author's other book for the method [P01] [P09]. The shipped calcProd.py is another program: it loops range(1, 100000), prints len(str(result)) and has an en dash, and its repaired form raises ValueError because Python refuses to convert an integer of more than 4300 digits to a string by default; with sys.set_int_max_str_digits(0) it prints 456569 digits, where the chapter's loop to 100001 gives 100000! of 456574 digits [P02] [P22]. On this machine the product took about 2.3 to 2.6 seconds and math.factorial(100000), which gives the same integer, took 0.136 seconds, and the chapter does not say that the digit limit stops printing the result [P24] [P10].",
  ['P01', 'P02', 'P09', 'P10', 'P22', 'P24']),
 ('F6', 'Time zone of the author',
  'The chapter says time.time() was called on March 17, 2026, at 11:04 PM Pacific Standard Time, but daylight saving time began in the United States on 8 March 2026, so the zone was Pacific Daylight Time at -07:00, and the printed ctime of 11:05:38 reads 23:05 on a 24-hour clock [P01] [P12] [P39]. The printed outputs of fromtimestamp(1000000), 05:46:40, are right only in Los Angeles, where the offset in January 1970 was -08:00: the same second is 13:46:40 in UTC and 15:46:40 in Istanbul, which was UTC+02:00 then; the chapter never says that the reading depends on the zone of the computer [P01] [P11].',
  ['P01', 'P11', 'P12', 'P39']),
 ('F7', 'The two-digit year',
  "Table 19-1 says %y is the year without century, 00 to 99, meaning 1970 to 2069, but Python and POSIX map 69 to 99 to 1969 to 1999 and 00 to 68 to 2000 to 2068, so '68' is 2068 and '69' is 1969; the book's examples, 63 as 2063 and 73 as 1973, are right either way [P01] [P10] [P34]. The chapter sends the reader to strftime.org for the directives, which now redirects (HTTP 301) to a cheatsheet of another company [P08].",
  ['P01', 'P08', 'P10', 'P34']),
 ('F8', 'Thirty years that are not',
  "The chapter's about_thirty_years is 365 * 30 days and it says it ignores leap years, but the example prints 28 October 1996 for 30 years before 21 October 2026, 7 days off because the span holds 7 leap days, and twice the span prints 5 November 1966, 15 days off the real 21 October 1966 [P01]. The text before the example calls the function datetime.delta(), which raises AttributeError; the function is datetime.timedelta() [P01] [P11].",
  ['P01', 'P11']),
 ('F9', 'Which clock',
  'The chapter measures elapsed time by subtracting two time.time() readings, which reads the system clock: that clock can be set by an administrator or a time service, so the difference can be negative, as a simulated clock set back by 10 seconds showed (-10.0 against +10.0 on a monotonic clock), while time.monotonic() and time.perf_counter() cannot go backwards and are what the documentation and PEP 418 name for intervals [P01] [P10] [P30]. The epoch timestamp counts seconds by a formula in which a day has 86400 seconds, so a leap second has no number: 23:59:59 on 31 December 2016 and the next midnight are one second apart in epoch time, and the type refuses 23:59:60 [P10] [P34].',
  ['P01', 'P10', 'P30', 'P34']),
 ('F10', 'Sleep and polling',
  "The chapter says time.sleep() blocks until the number of seconds has elapsed; since Python 3.5 a signal handler that returns does not shorten the sleep, which is retried for the time that remains, and only a handler that raises ends it, as PEP 475 says, and the sleep can be longer than asked [P01] [P10] [P31] [P17]. The chapter's loop until Halloween 2039 sleeps one second between checks and so uses almost no processor time, which was measured (under 0.05 s in 1.2 s against over 0.1 s in 0.3 s without the sleep), but a loop that sleeps a fixed second after its work drifts: with 0.02 s of work the 3600th round started 71.98 s late [P01] [P10].",
  ['P01', 'P10', 'P17', 'P31']),
 ('F11', 'What changed in Python',
  "Python 3.12 deprecated datetime.utcnow() and utcfromtimestamp(), which return naive values, in favour of now(datetime.UTC); parsing a day and a month without a year (strptime('02/29', '%m/%d') uses the year 1900) has drawn a DeprecationWarning since 3.13, and Python 3.15.0b4 raises ValueError for %d without a year; Python 3.14 added date.strptime() and time.strptime(); %:z does not exist in 3.11 [P11] [P26] [P27] [P29]. One program run under 11 interpreters (3.11, 3.12, 3.13, 3.14.0 to 3.14.6 and 3.15.0b4) compared 48 items and 11 of them differ between releases: the two strptime methods, the encoding default, the text of an error for sleep('1'), %:z, two year-less parses, the timeout message, the category and the message of the warning for a backslash followed by A, the text of the error for timedelta(months=1) and the deprecation of utcnow [P26] [P27] [P28] [P29].",
  ['P11', 'P26', 'P27', 'P28', 'P29']),
 ('F12', 'Zones and daylight saving',
  "The chapter has no time zone object: the zoneinfo module of Python 3.9 and later (PEP 615) attaches an IANA zone to a datetime and reads the data of the operating system or of the tzdata package, here tzdata 2026.5 (IANA release 2026e) beside the system's 2026c, and without either ZoneInfo raises ZoneInfoNotFoundError [P12] [P33] [P39]. A timedelta of one day added to an aware datetime moves the wall clock, so noon on 7 March 2026 in New York plus a day is noon on 8 March, a span of 23 hours; the hour from 02:00 to 03:00 that day does not exist and 01:30 on 1 November 2026 happens twice, told apart by fold (PEP 495) [P11] [P32].",
  ['P11', 'P12', 'P32', 'P33', 'P39']),
 ('F13', 'Launching programs on Linux',
  "The chapter's start and open commands are not portable: on this Ubuntu machine /usr/bin/open exists only because xdg-utils registers it as an alternative of xdg-open, start does not exist and subprocess.run(['start', 'hello.txt'], shell=True) exits 127, and with shell=True a list on POSIX runs only its first item, so ['echo', 'hi', 'there'] printed an empty line; ping -n 4 is the Windows flag and exits 2 on Linux [P01] [P13] [P45] [P46]. A command string built from a file name with shell=True ran a second command in the test ('x; echo INJECTED'), which shlex.quote prevented; webbrowser.open returned False and pyperclip raised PyperclipException with no browser and no clipboard program; playsound3 3.3.2, not the pinned 2.4.0, is the newest release [P13] [P18] [P20] [P47] [P48] [P49].",
  ['P01', 'P13', 'P18', 'P20', 'P45', 'P46', 'P47', 'P48', 'P49']),
 ('F14', 'Scheduling, run for real',
  "The chapter hands scheduling to Task Scheduler, launchd and cron in one paragraph and gives no syntax [P01]. Cron was run for real on this machine (cron 3.0pl1-184, Ubuntu 24.04): a Python job started by it two seconds after the turn of the minute saw PATH=/usr/bin:/bin, the working directory /root, 6 environment variables, no terminal, sh as its parent and a local clock of 22:36:01 UTC while the shell showed 01:36:01 +03; a TZ=Asia/Kolkata line in the crontab reached the job and set its clock to IST; a minute of 61 was refused by crontab with exit code 1 and 'bad minute' [P40] [P35]. When both day fields are restricted the command runs when either matches, so '0 0 13 * 5' fires on every 13th and on every Friday and cannot find Friday the 13th [P40]. The schedule follows the zone of the cron daemon: with the daemon started from a shell whose TZ was Europe/Istanbul an entry written on the Istanbul clock fired at the target moment and the entry for the same moment on the UTC clock did not, while the job itself saw UTC; a CRON_TZ=Asia/Kolkata line was passed to the job as a variable but did not move the schedule (the UTC entry fired and the Kolkata entry did not), and the Debian manual page does not mention CRON_TZ, which Wikipedia says an implementation may recognise [P40] [P54]. Not executed: Task Scheduler (schtasks) and launchd, whose property list was only written and read back with plistlib, and a systemd timer, whose OnCalendar expressions were only normalised by systemd-analyze because PID 1 here is not systemd [P41] [P42] [P43] [P44] [P23].",
  ['P01', 'P23', 'P35', 'P40', 'P41', 'P42', 'P43', 'P44', 'P54']),
 ('F15', 'Appendix B',
  "Appendix B answers Question 3 with time.asctime(), which prints the same text as ctime() for the current time, and Question 7 with weekday() equal to 0, Monday for 7 January 2019, and both are right [P06] [P10]. It answers Question 5 with 'the closest integer', which is incomplete: round(2.5) is 2 because ties go to the even number, round(x, 2) returns a float, and round(2.675, 2) is 2.67 [P06] [P25].",
  ['P06', 'P10', 'P25']),
 ('F16', 'The stopwatch and the countdown',
  'The Super Stopwatch needs a terminal: run without one it raises EOFError at the first input(), and in a pseudo-terminal with scripted key presses it printed the laps of the chapter once the dashes were repaired [P01] [P02]. The shipped simplecountdown.py matches the printed one apart from spacing, but the copy served at autbor.com differs (timeLeft set to 2, camel case and the Windows start line uncommented); autbor.com/alarm.wav redirects (HTTP 302) to a 582,952-byte file of 3.30 seconds that the online materials do not hold, and no sound could be played here [P01] [P02] [P07].',
  ['P01', 'P02', 'P07']),
 ('F17', 'Where the ideas come from',
  "The 1970 epoch was chosen arbitrarily: the first edition of the Unix Programmer's Manual (3 November 1971) counted sixtieths of a second from 1 January 1971 and the third edition (15 March 1972) from 1 January 1972 with a 32-bit count that 'guarantees a crisis every 2.26 years'; a signed 32-bit count of seconds ends at 03:14:07 UTC on 19 January 2038 [P52] [P53]. Leap seconds began in 1972, 27 have been added, the latest on 31 December 2016, and the General Conference on Weights and Measures decided in 2022 that the maximum UT1-UTC difference will be increased in or before 2035; a lawsuit filed on 30 September 2011 shut down the time zone database's mailing list on 6 October 2011 until ICANN took over on 14 October 2011; Thursday 4 October 1582 was followed by Friday 15 October 1582, a gap Python's date type does not have [P55] [P56] [P57] [P58].",
  ['P52', 'P53', 'P55', 'P56', 'P57', 'P58']),
 ('F18', 'Conclusion',
  "For an advanced course chapter 19 is best taught as the choice of a clock by the question asked, a monotonic clock for an interval and an aware datetime in a named zone for a moment on a calendar, and the choice of a launcher by the question asked, a list of arguments without a shell when the program is known and the operating system's scheduler when the program must run with no Python process alive [P01] [P10] [P11] [P12] [P13]. The chapter's listings need four repairs before they run, its outputs depend on the zone and the clock of the author, and its short account of scheduling needs the manual pages and the real behaviour of cron that this study recorded [P01] [P02] [P40].",
  ['P01', 'P02', 'P10', 'P11', 'P12', 'P13', 'P40']),
]


def X(code):
    """An executable example as one expression with no double quote and no line break: the code runs in a fresh
    namespace and the value of its variable out is the result."""
    lit = "'" + code.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace('"', "\\x22") + "'"
    return "(lambda g: (exec(%s, g), g['out'])[1])({})" % lit

# The helpers every example starts from: the modules, the short names for datetime, timedelta, date, UTC and ZoneInfo, err() returns what a call raised,
# warned() returns the value and the warnings a call drew, child() runs a child interpreter with environment variables set.
_PRE = r'''import io, os, re, sys, time, datetime, subprocess, warnings, signal, threading, math, calendar, shlex, sched, tempfile, struct, zoneinfo, shutil
from datetime import datetime as DT, timedelta as TD, date as D, timezone, UTC
from zoneinfo import ZoneInfo
def err(f):
    try: return ('ok', f())
    except Exception as e: return (type(e).__name__, str(e))
def warned(f):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always'); v = f()
    return v, [(x.category.__name__, str(x.message)) for x in w]
def child(code, **env):
    e = dict(os.environ); e.update(env)
    r = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, env=e); return r.stdout.strip() if r.returncode == 0 else r.stderr.strip().splitlines()[-1]
'''

# (top, mid, leaf, exemplar, definition, (the example as an expression, its result))
TAX = [
 ('EpochClock', 'EpochTimestamp', 'EpochZero', 'time.gmtime(0)',
  'The epoch of the time module is 00:00:00 UTC on 1 January 1970: time.gmtime(0) gives (1970, 1, 1, 0, 0, 0), calendar.timegm returns 0 for that moment, and time.time() returns the seconds since then as a float, not an int.',
  (X(_PRE + r'''out = (time.gmtime(0)[:6], time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(0)), calendar.timegm((1970,1,1,0,0,0)), DT(1970,1,1,tzinfo=UTC).timestamp(), type(time.time()).__name__)'''), "((1970, 1, 1, 0, 0, 0), '1970-01-01 00:00:00', 0, 0.0, 'float')")),
 ('EpochClock', 'EpochTimestamp', 'PosixFormula', 'tm_sec + tm_min*60 + tm_hour*3600 + tm_yday*86400 + ...',
  'POSIX defines the seconds since the epoch by a formula of the broken-down UTC fields in which every day has 86,400 seconds, so a leap second has no number: the formula gives 1773813875 for 06:04:35 UTC on 18 March 2026, the same as calendar.timegm, 23:59:59 on 31 December 2016 and the next midnight are 1 second apart, and datetime refuses a 60th second.',
  (X(_PRE + r'''def posix(y,mo,d,h,mi,s):
    tm_year=y-1900; tm_yday=(DT(y,mo,d)-DT(y,1,1)).days
    return s+mi*60+h*3600+tm_yday*86400+(tm_year-70)*31536000+((tm_year-69)//4)*86400-((tm_year-1)//100)*86400+((tm_year+299)//400)*86400
out = (posix(2026,3,18,6,4,35), calendar.timegm((2026,3,18,6,4,35)), posix(2000,2,29,12,0,0)==calendar.timegm((2000,2,29,12,0,0)), calendar.timegm((2017,1,1,0,0,0)) - calendar.timegm((2016,12,31,23,59,59)), err(lambda: DT(2016,12,31,23,59,60)), time.strptime('2016-12-31 23:59:60','%Y-%m-%d %H:%M:%S')[5])'''), "(1773813875, 1773813875, True, 1, ('ValueError', 'second must be in 0..59, not 60'), 60)")),
 ('EpochClock', 'EpochTimestamp', 'FloatPrecision', 'time.time() and time.time_ns()',
  'time.time() returns a float, a 64-bit double, which for a timestamp of 1773813875.35 has a spacing of 2.4e-07 seconds between neighbouring values, finer than a microsecond, while time.time_ns() returns an int of 19 digits that has no rounding at all.',
  (X(_PRE + r'''ts=1773813875.3518236
out = (type(ts).__name__, math.ulp(ts), math.ulp(ts)<1e-6, repr(ts), type(time.time_ns()).__name__, time.time_ns()>10**18, len(str(time.time_ns())))'''), "('float', 2.384185791015625e-07, True, '1773813875.3518236', 'int', True, 19)")),
 ('EpochClock', 'ClockKinds', 'ClockInfoTable', 'time.get_clock_info("monotonic")',
  'time.get_clock_info reports for each clock whether it is monotonic and whether it is adjustable: on Linux time.time reads CLOCK_REALTIME and is adjustable but not monotonic, while monotonic and perf_counter read CLOCK_MONOTONIC and are monotonic and not adjustable; a difference of two monotonic readings across time.sleep(0.05) is at least 0.05.',
  (X(_PRE + r'''a=time.monotonic(); b=time.perf_counter(); time.sleep(0.05); a2=time.monotonic(); b2=time.perf_counter()
out = ({n: (time.get_clock_info(n).monotonic, time.get_clock_info(n).adjustable, time.get_clock_info(n).implementation) for n in ('time','monotonic','perf_counter','process_time')}, a2-a >= 0.05, b2-b >= 0.05)'''), "({'time': (False, True, 'clock_gettime(CLOCK_REALTIME)'), 'monotonic': (True, False, 'clock_gettime(CLOCK_MONOTONIC)'), 'perf_counter': (True, False, 'clock_gettime(CLOCK_MONOTONIC)'), 'process_time': (True, False, 'clock_gettime(CLOCK_PROCESS_CPUTIME_ID)')}, True, True)")),
 ('EpochClock', 'ClockKinds', 'SteppedWallClock', 'end_time - start_time',
  'The difference of two readings of an adjustable clock is wrong when someone sets the clock between them: if the wall clock reads 1000.0 and then, set back, 990.0, the difference is -10.0 seconds, while the two readings of a monotonic clock 50.0 and 60.0 give the true +10.0.',
  (X(_PRE + r'''class Fake:
    def __init__(s, seq): s.seq=iter(seq)
    def __call__(s): return next(s.seq)
wall=Fake([1000.0, 990.0]); mono=Fake([50.0, 60.0])
w0=wall(); m0=mono(); w1=wall(); m1=mono()
out=(w1-w0, m1-m0, time.get_clock_info('time').adjustable, time.get_clock_info('monotonic').adjustable)'''), '(-10.0, 10.0, True, False)')),
 ('EpochClock', 'ClockKinds', 'RoundFunction', 'round(time.time() - last_time, 2)',
  'round(x) with no digits returns an int and rounds a tie to the even neighbour, so round(2.5) is 2 and round(3.5) is 4, while round(x, 2) returns a float and round(2.675, 2) is 2.67 because the float nearest 2.675 lies just below it.',
  (X(_PRE + r'''out = (round(2.4), round(2.5), round(3.5), type(round(2.5)).__name__, round(2.675,2), type(round(2.0,2)).__name__, round(3.14159,2), round(0.5), round(-0.5), round(1773813875.3518236,2))'''), "(2, 2, 4, 'int', 2.67, 'float', 3.14, 0, 0, 1773813875.35)")),
 ('EpochClock', 'ClockKinds', 'ProfilingByClock', 'calcProd()',
  'Profiling code by the time between two clock readings measures one run on one machine: the product of 1 to 100000 built by a loop equals math.factorial(100000), has 1,516,705 bits and 456,574 decimal digits, and converting it to a string raises ValueError under the default limit of 4300 digits.',
  (X(_PRE + r'''def calc():
    p=1
    for i in range(1,100001): p=p*i
    return p
r=calc()
out = (r==math.factorial(100000), r==math.prod(range(1,100001)), r.bit_length(), err(lambda: str(r))[0], sys.get_int_max_str_digits(), len(str(r)) if sys.set_int_max_str_digits(0) is None else 0)'''), "(True, True, 1516705, 'ValueError', 4300, 456574)")),
 ('EpochClock', 'PausingPrograms', 'SleepFunction', 'time.sleep(5)',
  'time.sleep(seconds) blocks the calling thread and returns None; a negative number raises ValueError and a string raises TypeError, and a monotonic clock shows that the pause lasted at least as long as asked.',
  (X(_PRE + r'''t=time.monotonic(); r=time.sleep(0.2); e=time.monotonic()-t
out = (r, e>=0.2, e<0.5, err(lambda: time.sleep(-1)), err(lambda: time.sleep('1')))'''), '(None, True, True, (\'ValueError\', \'sleep length must be non-negative\'), (\'TypeError\', "\'str\' object cannot be interpreted as an integer or float"))')),
 ('EpochClock', 'PausingPrograms', 'SleepAndSignals', 'signal.setitimer(signal.ITIMER_REAL, 0.05)',
  'Since Python 3.5 a signal handler that returns does not cut time.sleep short, because the call is retried for the time that remains, while a handler that raises an exception ends the sleep at once; KeyboardInterrupt, which Ctrl-C raises, derives from BaseException and not from Exception.',
  (X(_PRE + r'''hits=[]
signal.signal(signal.SIGALRM, lambda s,f: hits.append('handler ran'))
signal.setitimer(signal.ITIMER_REAL, 0.05)
t=time.monotonic(); time.sleep(0.3); e=time.monotonic()-t
def h(s,f): raise RuntimeError('from handler')
signal.signal(signal.SIGALRM, h); signal.setitimer(signal.ITIMER_REAL, 0.05)
t2=time.monotonic()
try: time.sleep(5)
except RuntimeError as ex: r=str(ex)
out = (hits, e>=0.3, r, time.monotonic()-t2<1, issubclass(KeyboardInterrupt, Exception), issubclass(KeyboardInterrupt, BaseException))'''), "(['handler ran'], True, 'from handler', True, False, True)")),
 ('EpochClock', 'PausingPrograms', 'PollingLoops', 'while datetime.datetime.now() < halloween_2039:',
  'A loop that sleeps one second between clock checks wakes about once a second and uses almost no processor time (under 0.05 s of CPU in 1.2 s), while the same loop without the sleep keeps a processor busy (over 0.1 s of CPU in 0.3 s).',
  (X(_PRE + r'''end=DT.now()+TD(seconds=1.2); c0=time.process_time(); t0=time.monotonic()
while DT.now()<end: time.sleep(1)
slept=time.process_time()-c0; w=time.monotonic()-t0
c0=time.process_time(); end=DT.now()+TD(seconds=0.3)
while DT.now()<end: pass
busy=time.process_time()-c0
out=(round(w)>=1, slept<0.05, busy>0.1)'''), '(True, True, True)')),
 ('EpochClock', 'PausingPrograms', 'SleepDrift', 'time.sleep(1) in a loop',
  'A loop that sleeps a fixed second after work that takes 0.02 s starts its 3600th round 3670.98 s after the first, 71.98 s late, while a loop that sleeps until the next tick of the clock starts it at 3599.0 s, exactly on schedule.',
  (X(_PRE + r'''class C:
    def __init__(s): s.t=0.0
    def now(s): return s.t
    def sleep(s,d): s.t+=d
def drifting(c, n, work):
    starts=[]
    for _ in range(n): starts.append(c.now()); c.sleep(work); c.sleep(1.0)
    return starts[-1]
def anchored(c, n, work):
    t0=c.now(); starts=[]
    for i in range(n): starts.append(c.now()); c.sleep(work); c.sleep(max(0.0, t0+(i+1)*1.0-c.now()))
    return starts[-1]
out=(round(drifting(C(),3600,0.02),2), round(anchored(C(),3600,0.02),2))'''), '(3670.98, 3599.0)')),
 ('DatetimeValues', 'MomentsAndFields', 'DatetimeObject', 'datetime.datetime(2026, 10, 21, 16, 29, 0)',
  'A datetime object holds a moment as year, month, day, hour, minute, second and microsecond; month, day and the fields are checked when it is made, so datetime(2026, 2, 30) raises ValueError and a call without the day raises TypeError.',
  (X(_PRE + r'''dt=DT(2026,10,21,16,29,0)
out = (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, dt, DT(2026,10,21), err(lambda: DT(2026,10)), err(lambda: DT(2026,13,1)), err(lambda: DT(2026,2,30)), dt.weekday(), dt.isoweekday())'''), '(2026, 10, 21, 16, 29, 0, 0, datetime.datetime(2026, 10, 21, 16, 29), datetime.datetime(2026, 10, 21, 0, 0), (\'TypeError\', "function missing required argument \'day\' (pos 3)"), (\'ValueError\', \'month must be in 1..12, not 13\'), (\'ValueError\', \'day 30 must be in range 1..28 for month 2 in year 2026\'), 2, 3)')),
 ('DatetimeValues', 'MomentsAndFields', 'CurrentMoment', 'datetime.datetime.now()',
  'datetime.now() returns the current moment as a naive datetime in the local zone, within a second of datetime.fromtimestamp(time.time()) and of datetime.today(), and datetime.now(datetime.UTC) returns the same instant as an aware value with the offset 0.',
  (X(_PRE + r'''a=DT.now(); b=DT.fromtimestamp(time.time()); c=DT.now(UTC)
out = (abs((a-b).total_seconds())<1, a.tzinfo, c.tzinfo, c.utcoffset(), type(a).__name__, DT.today().tzinfo, abs((DT.now()-DT.today()).total_seconds())<1)'''), "(True, None, datetime.timezone.utc, datetime.timedelta(0), 'datetime', None, True)")),
 ('DatetimeValues', 'MomentsAndFields', 'DatetimeComparison', 'new_years_2027 > halloween_2026',
  'Datetime values are compared with ==, <, > and sorted, the later moment is the greater, two separately made values of one moment are equal but not the same object, and subtracting gives a timedelta of 62 days between 31 October 2026 and 1 January 2027.',
  (X(_PRE + r'''h=DT(2026,10,31,0,0,0); n=DT(2027,1,1,0,0,0); o=DT(2026,10,31,0,0,0)
out = (h==o, h>n, n>h, n!=o, h is o, sorted([n,h]) == [h,n], max(n,h)==n, n-h)'''), '(True, False, True, True, False, True, True, datetime.timedelta(days=62))')),
 ('DatetimeValues', 'MomentsAndFields', 'WeekdayOfDate', 'datetime.date(2019, 1, 7).strftime("%A")',
  "The weekday of a date comes from strftime('%A') as a name, from weekday() as a number in which Monday is 0, from isoweekday() in which Monday is 1, and from calendar.day_name; 7 January 2019 is a Monday, in ISO week 2.",
  (X(_PRE + r'''d=DT(2019,1,7)
out=(d.weekday(), d.strftime('%A'), d.isoweekday(), calendar.day_name[d.weekday()], d.date().isocalendar(), D(2019,1,7).strftime('%w'))'''), "(0, 'Monday', 1, 'Monday', datetime.IsoCalendarDate(year=2019, week=2, weekday=1), '1')")),
 ('DatetimeValues', 'DurationsTimedelta', 'TimedeltaObject', 'datetime.timedelta(days=11, hours=10, minutes=9, seconds=8)',
  'A timedelta holds a duration and keeps only days, seconds and microseconds: 11 days, 10 hours, 9 minutes and 8 seconds is days 11, seconds 36548, microseconds 0, 986948.0 seconds in all, and a negative duration is normalised so that timedelta(seconds=-1) has days -1 and seconds 86399.',
  (X(_PRE + r'''d=TD(days=11, hours=10, minutes=9, seconds=8)
out=(d.days, d.seconds, d.microseconds, d.total_seconds(), str(d), repr(d), TD(weeks=1,hours=24).days, TD(milliseconds=1500), TD(seconds=-1), (TD(seconds=-1).days, TD(seconds=-1).seconds), str(TD(seconds=-1)), abs(TD(days=-2)), TD.resolution)'''), "(11, 36548, 0, 986948.0, '11 days, 10:09:08', 'datetime.timedelta(days=11, seconds=36548)', 8, datetime.timedelta(seconds=1, microseconds=500000), datetime.timedelta(days=-1, seconds=86399), (-1, 86399), '-1 day, 23:59:59', datetime.timedelta(days=2), datetime.timedelta(microseconds=1))")),
 ('DatetimeValues', 'DurationsTimedelta', 'NoMonthsOrYears', 'datetime.timedelta(months=1)',
  'timedelta takes weeks, days, hours, minutes, seconds, milliseconds and microseconds but no months or years, because a month has 28 to 31 days, so timedelta(months=1) raises TypeError and 31 January plus 30 days is 2 March 2026.',
  (X(_PRE + r'''out = (err(lambda: TD(months=1)), err(lambda: TD(years=1)), DT(2026,1,31)+TD(days=30), DT(2026,1,31)+TD(days=31), (DT(2026,3,1)-DT(2026,2,1)).days, (DT(2027,3,1)-DT(2027,2,1)).days, (DT(2024,3,1)-DT(2024,2,1)).days)'''), '((\'TypeError\', "__new__() got an unexpected keyword argument \'months\'"), (\'TypeError\', "__new__() got an unexpected keyword argument \'years\'"), datetime.datetime(2026, 3, 2, 0, 0), datetime.datetime(2026, 3, 3, 0, 0), 28, 28, 29)')),
 ('DatetimeValues', 'DurationsTimedelta', 'DurationArithmetic', 'now + thousand_days',
  'A timedelta is added to or subtracted from a datetime, multiplied or divided by a number, divided by another timedelta to give a number, and added to another timedelta, but two durations cannot be multiplied and a timedelta plus an int raises TypeError; 1000 days after 2 December 2026 is 28 August 2029, a Tuesday.',
  (X(_PRE + r'''d=TD(days=1, hours=12); now=DT(2026,12,2,18,38,50,636181); t=TD(days=1000)
out = (d*2, d/2, d*1.5, d//TD(hours=1), d/TD(hours=1), d%TD(hours=5), divmod(d, TD(hours=5)), err(lambda: d*d), err(lambda: d+1), now+t, (now+t).strftime('%B %d, %Y'), (now+t).weekday())'''), '(datetime.timedelta(days=3), datetime.timedelta(seconds=64800), datetime.timedelta(days=2, seconds=21600), 36, 36.0, datetime.timedelta(seconds=3600), (7, datetime.timedelta(seconds=3600)), (\'TypeError\', "unsupported operand type(s) for *: \'datetime.timedelta\' and \'datetime.timedelta\'"), (\'TypeError\', "unsupported operand type(s) for +: \'datetime.timedelta\' and \'int\'"), datetime.datetime(2029, 8, 28, 18, 38, 50, 636181), \'August 28, 2029\', 1)')),
 ('DatetimeValues', 'DurationsTimedelta', 'ThirtyYearsError', 'oct_21st - about_thirty_years',
  "The chapter's about_thirty_years is 365 * 30 days, but the 30 years from 21 October 1996 to 21 October 2026 hold 7 leap days (29 February of 2000, 2004, 2008, 2012, 2016, 2020 and 2024), so subtracting 10,950 days from 21 October 2026 gives 28 October 1996, 7 days off, and twice that gives 5 November 1966, 15 days off; datetime.delta() raises AttributeError.",
  (X(_PRE + r'''import datetime
o=DT(2026,10,21,16,29,0); t=TD(days=365*30)
out = (o-t, o-2*t, (o-DT(1996,10,21,16,29)).days - 365*30, o.replace(year=1996), (o-2*t).strftime('%B %d, %Y'), (o.replace(year=1966)-(o-2*t)).days, err(lambda: datetime.delta(days=1)), hasattr(datetime,'timedelta'))'''), '(datetime.datetime(1996, 10, 28, 16, 29), datetime.datetime(1966, 11, 5, 16, 29), 7, datetime.datetime(1996, 10, 21, 16, 29), \'November 05, 1966\', -15, (\'AttributeError\', "module \'datetime\' has no attribute \'delta\'"), True)')),
 ('DatetimeValues', 'FormatAndParse', 'DirectiveTable', 'Table 19-1',
  'Table 19-1 lists the strftime directives, and on 3 November 2026 at 16:29:07 they give %Y 2026, %y 26, %m 11, %B November, %b Nov, %d 03, %j 307, %w 2, %A Tuesday, %a Tue, %H 16, %I 04, %M 29, %S 07, %p PM and %% as one percent sign; %w counts Sunday as 0.',
  (X(_PRE + r'''dt=DT(2026,11,3,16,29,7)
dirs='%Y %y %m %B %b %d %j %w %A %a %H %I %M %S %p %%'.split()
out = ({d: dt.strftime(d) for d in dirs}, {d.strftime('%a'): d.strftime('%w') for d in (DT(2026,11,1)+TD(days=i) for i in range(7))})'''), "({'%Y': '2026', '%y': '26', '%m': '11', '%B': 'November', '%b': 'Nov', '%d': '03', '%j': '307', '%w': '2', '%A': 'Tuesday', '%a': 'Tue', '%H': '16', '%I': '04', '%M': '29', '%S': '07', '%p': 'PM', '%%': '%'}, {'Sun': '0', 'Mon': '1', 'Tue': '2', 'Wed': '3', 'Thu': '4', 'Fri': '5', 'Sat': '6'})")),
 ('DatetimeValues', 'FormatAndParse', 'StrftimeFormat', "oct_21st.strftime('%Y/%m/%d %H:%M:%S')",
  "strftime returns text from a format of directives and other characters: '%Y/%m/%d %H:%M:%S' gives '2026/10/21 16:29:00', '%I:%M %p' gives '04:29 PM', the directives %e, %k and %-d are platform extensions, and %z and %Z are empty for a naive value.",
  (X(_PRE + r'''o=DT(2026,10,21,16,29,0)
out=(o.strftime('%Y/%m/%d %H:%M:%S'), o.strftime('%I:%M %p'), o.strftime("%B of '%y"), o.strftime('%-d %-m'), o.strftime('%e|%k|%l'), o.strftime('%f'), DT(2026,10,21,16,29,0,123).strftime('%f'), o.strftime('%z|%Z|'), o.replace(tzinfo=UTC).strftime('%z|%Z|%:z'))'''), '(\'2026/10/21 16:29:00\', \'04:29 PM\', "October of \'26", \'21 10\', \'21|16| 4\', \'000000\', \'000123\', \'||\', \'+0000|UTC|+00:00\')')),
 ('DatetimeValues', 'FormatAndParse', 'StrptimeParse', "datetime.datetime.strptime('October 21, 2026', '%B %d, %Y')",
  "strptime reads a datetime from text by a format and raises ValueError when the text does not match, as '2026-10-21' does for '%Y/%m/%d'; it accepts '2026-1-5' for '%Y-%m-%d', refuses leading and trailing spaces, and since Python 3.14 date.strptime and time.strptime exist beside datetime.strptime.",
  (X(_PRE + r'''import datetime
p=DT.strptime
out=(p('October 21, 2026','%B %d, %Y'), p('2026/10/21 16:29:00','%Y/%m/%d %H:%M:%S'), p("November of '63","%B of '%y"), err(lambda: p('2026-10-21','%Y/%m/%d')), p('2026-1-5','%Y-%m-%d'), err(lambda: p('  2026','%Y')), err(lambda: p('2026 ','%Y')), err(lambda: p('2026-10-21T16:29:00Z','%Y-%m-%dT%H:%M:%S')), p('2026-10-21T16:29:00Z','%Y-%m-%dT%H:%M:%S%z'), hasattr(D,'strptime'), D.strptime('2026-10-21','%Y-%m-%d'), datetime.time.strptime('16:29','%H:%M'))'''), '(datetime.datetime(2026, 10, 21, 0, 0), datetime.datetime(2026, 10, 21, 16, 29), datetime.datetime(2063, 11, 1, 0, 0), (\'ValueError\', "time data \'2026-10-21\' does not match format \'%Y/%m/%d\'"), datetime.datetime(2026, 1, 5, 0, 0), (\'ValueError\', "time data \'  2026\' does not match format \'%Y\'"), (\'ValueError\', \'unconverted data remains:  \'), (\'ValueError\', \'unconverted data remains: Z\'), datetime.datetime(2026, 10, 21, 16, 29, tzinfo=datetime.timezone.utc), True, datetime.date(2026, 10, 21), datetime.time(16, 29))')),
 ('DatetimeValues', 'FormatAndParse', 'TwoDigitYear', '%y',
  "The %y directive follows POSIX: 69 to 99 mean 1969 to 1999 and 00 to 68 mean 2000 to 2068, so '68' is 2068 and '69' is 1969, which is not the 1970 to 2069 that Table 19-1 prints; the book's two examples, 63 as 2063 and 73 as 1973, are right either way.",
  (X(_PRE + r'''out=([(s, DT.strptime(s,'%y').year) for s in ('00','26','63','68','69','70','73','99')], [(s, time.strptime(s,'%y').tm_year) for s in ('68','69')], DT(2026,1,1).strftime('%y'), DT(1969,1,1).strftime('%y'), DT(2069,1,1).strftime('%y'))'''), "([('00', 2000), ('26', 2026), ('63', 2063), ('68', 2068), ('69', 1969), ('70', 1970), ('73', 1973), ('99', 1999)], [('68', 2068), ('69', 1969)], '26', '69', '69')")),
 ('DatetimeValues', 'FormatAndParse', 'YearlessParsing', "strptime('02/29', '%m/%d')",
  "A format with a month and a day but no year uses the year 1900, which is not a leap year, so '02/29' raises ValueError and draws a DeprecationWarning from Python 3.13 on, '02/29;1984' with a year parses, and 21 October without a year silently becomes 1900-10-21.",
  (X(_PRE + r'''out=(warned(lambda: err(lambda: DT.strptime('02/29','%m/%d'))), warned(lambda: DT.strptime('02/29;1984','%m/%d;%Y')), warned(lambda: DT.strptime('10/21','%m/%d')))'''), "((('ValueError', 'day 29 must be in range 1..28 for month 2 in year 1900'), [('DeprecationWarning', 'Parsing dates involving a day of month without a year specified is ambiguous\\nand fails to parse leap day. The default behavior will change in Python 3.15\\nto either always raise an exception or to use a different default year (TBD).\\nTo avoid trouble, add a specific year to the input & format.\\nSee https://github.com/python/cpython/issues/70647.')]), (datetime.datetime(1984, 2, 29, 0, 0), []), (datetime.datetime(1900, 10, 21, 0, 0), []))")),
 ('DatetimeValues', 'FormatAndParse', 'IsoFormats', 'datetime.isoformat()',
  'ISO 8601 and RFC 3339 write 2026-10-21T16:29:07+00:00 and with Z for zero offset; isoformat writes it and fromisoformat reads it, accepting Z since Python 3.11, the basic form 20261021T162907+0300 and the week date 2026-W43-3, and raising ValueError for 21/10/2026.',
  (X(_PRE + r'''dt=DT(2026,10,21,16,29,7,123456,tzinfo=UTC)
out=(dt.isoformat(), dt.isoformat(timespec='seconds'), DT.fromisoformat('2026-10-21T16:29:07Z'), DT.fromisoformat('20261021T162907+0300'), DT.fromisoformat('2026-10-21 16:29'), D.fromisoformat('2026-W43-3'), err(lambda: DT.fromisoformat('21/10/2026')), DT(2026,10,21,16,29).isoformat(), str(DT(2026,10,21,16,29)), DT(2026,10,21,16,29,7,tzinfo=UTC).isoformat().replace('+00:00','Z'))'''), '(\'2026-10-21T16:29:07.123456+00:00\', \'2026-10-21T16:29:07+00:00\', datetime.datetime(2026, 10, 21, 16, 29, 7, tzinfo=datetime.timezone.utc), datetime.datetime(2026, 10, 21, 16, 29, 7, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800))), datetime.datetime(2026, 10, 21, 16, 29), datetime.date(2026, 10, 21), (\'ValueError\', "Invalid isoformat string: \'21/10/2026\'"), \'2026-10-21T16:29:00\', \'2026-10-21 16:29:00\', \'2026-10-21T16:29:07Z\')')),
 ('TimeZonesAndPitfalls', 'ZoneAwareness', 'NaiveVersusAware', 'datetime.now(datetime.UTC)',
  'A datetime without a tzinfo is naive and one with a tzinfo is aware; a naive and an aware value are never equal, comparing them or subtracting one from the other raises TypeError, 16:29 UTC equals 19:29 in Istanbul because they are one instant, and replace(tzinfo=UTC) labels a naive value without moving it.',
  (X(_PRE + r'''n=DT(2026,10,21,16,29); a=DT(2026,10,21,16,29,tzinfo=UTC); a2=DT(2026,10,21,19,29,tzinfo=ZoneInfo('Europe/Istanbul'))
out = (n==a, err(lambda: n<a), err(lambda: n-a), a==a2, a2.utcoffset(), n.replace(tzinfo=UTC)==a, n.tzinfo, a.tzinfo)'''), '(False, (\'TypeError\', "can\'t compare offset-naive and offset-aware datetimes"), (\'TypeError\', "can\'t subtract offset-naive and offset-aware datetimes"), True, datetime.timedelta(seconds=10800), True, None, datetime.timezone.utc)')),
 ('TimeZonesAndPitfalls', 'ZoneAwareness', 'UtcnowDeprecated', 'datetime.utcnow()',
  'datetime.utcnow() and utcfromtimestamp() return naive values and have drawn a DeprecationWarning since Python 3.12; because the result is naive, treating it as local time shifts it by the offset of the zone, here -3.0 hours in Istanbul, and datetime.now(datetime.UTC) is the aware replacement.',
  (X(_PRE + r'''v=warned(lambda: (DT.utcnow().tzinfo, DT.utcfromtimestamp(0)))
b=child("import datetime,warnings; warnings.simplefilter('ignore'); u=datetime.datetime.utcnow(); print(u.timestamp()-datetime.datetime.now(datetime.UTC).timestamp())", TZ='Europe/Istanbul')
out=(v[0], v[1], warned(lambda: DT.now(UTC).tzinfo)[1], DT.fromtimestamp(0, UTC), UTC is timezone.utc, round(float(b)/3600,2))'''), "((None, datetime.datetime(1970, 1, 1, 0, 0)), [('DeprecationWarning', 'datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).'), ('DeprecationWarning', 'datetime.datetime.utcfromtimestamp() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.fromtimestamp(timestamp, datetime.UTC).')], [], datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), True, -3.0)")),
 ('TimeZonesAndPitfalls', 'ZoneAwareness', 'ZoneInfoZones', "ZoneInfo('America/Los_Angeles')",
  "The zoneinfo module attaches an IANA zone with its daylight saving rules to a datetime: Los Angeles is -07:00 PDT on 1 July 2026 and -08:00 PST on 1 January, Istanbul is +03:00 all year since 2016, and the data come from the system's zoneinfo directory or from the tzdata package, so without both ZoneInfo raises ZoneInfoNotFoundError.",
  (X(_PRE + r'''import importlib.metadata as md
la=ZoneInfo('America/Los_Angeles'); ist=ZoneInfo('Europe/Istanbul')
d=DT(2026,7,1,12,tzinfo=la)
r=subprocess.run([sys.executable,'-S','-c',"import zoneinfo; zoneinfo.ZoneInfo('Europe/Istanbul')"],env=dict(os.environ,PYTHONTZPATH='/nonexistent'),capture_output=True,text=True)
out=(d.utcoffset(), d.tzname(), DT(2026,1,1,12,tzinfo=la).utcoffset(), DT(2026,1,1,12,tzinfo=la).tzname(), ist.utcoffset(DT(2026,7,1)), ist.utcoffset(DT(2015,7,1)), ist.utcoffset(DT(2017,1,1)), la.key, md.version('tzdata'), zoneinfo.TZPATH[:2], len(zoneinfo.available_timezones())>400, r.stderr.strip().splitlines()[-1])'''), '(datetime.timedelta(days=-1, seconds=61200), \'PDT\', datetime.timedelta(days=-1, seconds=57600), \'PST\', datetime.timedelta(seconds=10800), datetime.timedelta(seconds=10800), datetime.timedelta(seconds=10800), \'America/Los_Angeles\', \'2026.5\', (\'/usr/share/zoneinfo\', \'/usr/lib/zoneinfo\'), True, "zoneinfo._common.ZoneInfoNotFoundError: \'No time zone found with key Europe/Istanbul\'")')),
 ('TimeZonesAndPitfalls', 'ZoneAwareness', 'FromTimestampZones', 'datetime.datetime.fromtimestamp(1000000)',
  'fromtimestamp(1000000) with no zone uses the local zone of the process, so it prints 05:46:40 in Los Angeles, 13:46:40 in UTC and 15:46:40 in Istanbul, which was UTC+02:00 in 1970; the local zone is read from TZ or the system, and time.tzset() changes it while the program runs.',
  (X(_PRE + r'''la=ZoneInfo('America/Los_Angeles'); ist=ZoneInfo('Europe/Istanbul')
c="import time, datetime; print(time.strftime('%Z %z', time.localtime(1791841200)), datetime.datetime.fromtimestamp(1791841200).isoformat())"
os.environ['TZ']='Asia/Kolkata'; time.tzset(); t1=time.strftime('%H:%M %Z', time.localtime(1791841200)); os.environ['TZ']='UTC'; time.tzset(); t2=time.strftime('%H:%M %Z', time.localtime(1791841200))
out=([DT.fromtimestamp(1000000, z).isoformat() for z in (UTC, la, ist)], [child("import datetime; print(repr(datetime.datetime.fromtimestamp(1000000)))", TZ=z) for z in ('America/Los_Angeles','UTC','Europe/Istanbul')], [child(c, TZ=z) for z in ('UTC','Europe/Istanbul','America/Los_Angeles','Asia/Kolkata')], t1, t2)'''), "(['1970-01-12T13:46:40+00:00', '1970-01-12T05:46:40-08:00', '1970-01-12T15:46:40+02:00'], ['datetime.datetime(1970, 1, 12, 5, 46, 40)', 'datetime.datetime(1970, 1, 12, 13, 46, 40)', 'datetime.datetime(1970, 1, 12, 15, 46, 40)'], ['UTC +0000 2026-10-12T21:40:00', '+03 +0300 2026-10-13T00:40:00', 'PDT -0700 2026-10-12T14:40:00', 'IST +0530 2026-10-13T03:10:00'], '03:10 IST', '21:40 UTC')")),
 ('TimeZonesAndPitfalls', 'ZoneAwareness', 'PstVersusPdt', 'time.ctime()',
  "On 17 March 2026 Los Angeles keeps daylight saving time (since 8 March), so 06:04:35 UTC is 23:04:35 PDT at -07:00, not Pacific Standard Time as the chapter says, and time.ctime prints the same instant as 'Tue Mar 17 23:04:35 2026' in Los Angeles, 'Wed Mar 18 06:04:35 2026' in UTC and 'Wed Mar 18 09:04:35 2026' in Istanbul.",
  (X(_PRE + r'''la=ZoneInfo('America/Los_Angeles'); d=DT.fromtimestamp(1773813875.3518236, la)
cc="import time; print(time.ctime(1773813875))"
out=(d.isoformat(timespec='seconds'), d.tzname(), d.utcoffset(), d.dst(), DT(2026,3,8,3,0,tzinfo=la).tzname(), DT(2026,3,8,1,59,tzinfo=la).tzname(), DT(2026,3,17).strftime('%A'), time.asctime(time.gmtime(1773813875)), child(cc, TZ='America/Los_Angeles'), child(cc, TZ='UTC'), child(cc, TZ='Europe/Istanbul'))'''), "('2026-03-17T23:04:35-07:00', 'PDT', datetime.timedelta(days=-1, seconds=61200), datetime.timedelta(seconds=3600), 'PDT', 'PST', 'Tuesday', 'Wed Mar 18 06:04:35 2026', 'Tue Mar 17 23:04:35 2026', 'Wed Mar 18 06:04:35 2026', 'Wed Mar 18 09:04:35 2026')")),
 ('TimeZonesAndPitfalls', 'DaylightSaving', 'WallClockArithmetic', 'aware_datetime + timedelta(days=1)',
  'Adding a timedelta to an aware datetime moves the wall-clock reading and keeps the zone: noon on 7 March 2026 in New York plus one day is noon on 8 March, but the two moments are 82800 seconds, 23 hours, apart in UTC, and the subtraction of two values in one zone ignores the change of offset.',
  (X(_PRE + r'''ny=ZoneInfo('America/New_York'); a=DT(2026,3,7,12,0,tzinfo=ny); b=a+TD(days=1)
out=(a.isoformat(), b.isoformat(), (b.astimezone(UTC)-a.astimezone(UTC)), (b-a), (a.astimezone(UTC)+TD(days=1)).astimezone(ny).isoformat(), (a+TD(hours=24)).isoformat())'''), "('2026-03-07T12:00:00-05:00', '2026-03-08T12:00:00-04:00', datetime.timedelta(seconds=82800), datetime.timedelta(days=1), '2026-03-08T13:00:00-04:00', '2026-03-08T12:00:00-04:00')")),
 ('TimeZonesAndPitfalls', 'DaylightSaving', 'GapAndFold', 'datetime(2026, 11, 1, 1, 30, fold=1)',
  'When clocks go forward, 02:30 on 8 March 2026 in New York does not exist and converts to 03:30 EDT; when they go back, 01:30 on 1 November 2026 happens twice, fold=0 meaning the first, 05:30 UTC, and fold=1 the second, 06:30 UTC, although the two values compare equal.',
  (X(_PRE + r'''ny=ZoneInfo('America/New_York')
g=DT(2026,3,8,2,30,tzinfo=ny); f0=DT(2026,11,1,1,30,tzinfo=ny); f1=f0.replace(fold=1)
out=(g.isoformat(), g.astimezone(UTC).isoformat(), g.astimezone(UTC).astimezone(ny).isoformat(), f0.isoformat(), f1.isoformat(), f0==f1, f0.astimezone(UTC).isoformat(), f1.astimezone(UTC).isoformat(), (f1.astimezone(UTC)-f0.astimezone(UTC)), (f1-f0))'''), "('2026-03-08T02:30:00-05:00', '2026-03-08T07:30:00+00:00', '2026-03-08T03:30:00-04:00', '2026-11-01T01:30:00-04:00', '2026-11-01T01:30:00-05:00', True, '2026-11-01T05:30:00+00:00', '2026-11-01T06:30:00+00:00', datetime.timedelta(seconds=3600), datetime.timedelta(0))")),
 ('TimeZonesAndPitfalls', 'LimitsOfTime', 'Year2038', '2**31',
  "A signed 32-bit time_t counts to 2147483647, 03:14:07 UTC on 19 January 2038, and 2**31 wraps to -2147483648, which is 20:45:52 UTC on 13 December 1901; a 64-bit value reaches datetime's year 9999 and negative timestamps are dates before 1970.",
  (X(_PRE + r'''t=2**31
packed=struct.pack('<I', t); wrapped=struct.unpack('<i', packed)[0]
out=(DT.fromtimestamp(t-1, UTC).isoformat(), DT.fromtimestamp(t, UTC).isoformat(), wrapped, DT.fromtimestamp(wrapped, UTC).isoformat(), time.gmtime(2**40)[0], DT.fromtimestamp(253402300799, UTC).isoformat(), err(lambda: DT.fromtimestamp(253402300800, UTC)), struct.calcsize('l'), struct.calcsize('q'), DT.fromtimestamp(-1, UTC).isoformat(), DT.fromtimestamp(-86400*365*100, UTC).isoformat(), err(lambda: DT.fromtimestamp(-62135596801, UTC)))'''), "('2038-01-19T03:14:07+00:00', '2038-01-19T03:14:08+00:00', -2147483648, '1901-12-13T20:45:52+00:00', 36812, '9999-12-31T23:59:59+00:00', ('ValueError', 'year must be in 1..9999, not 10000'), 8, 8, '1969-12-31T23:59:59+00:00', '1870-01-25T00:00:00+00:00', ('ValueError', 'year must be in 1..9999, not 0'))")),
 ('TimeZonesAndPitfalls', 'LimitsOfTime', 'DatetimeRange', 'datetime.date.max',
  "The datetime types run from 1 January of the year 1 to 31 December 9999, date.max is 9999-12-31, and arithmetic beyond either end raises OverflowError ('date value out of range') instead of wrapping.",
  (X(_PRE + r'''out=(D.min, D.max, DT.max, err(lambda: DT.max+TD(microseconds=1)), err(lambda: DT.min-TD(days=1)), err(lambda: D(1,1,1)-TD(days=1)), D(1,1,1).weekday(), D(1,1,1).toordinal(), D.fromordinal(1))'''), "(datetime.date(1, 1, 1), datetime.date(9999, 12, 31), datetime.datetime(9999, 12, 31, 23, 59, 59, 999999), ('OverflowError', 'date value out of range'), ('OverflowError', 'date value out of range'), ('OverflowError', 'date value out of range'), 0, 1, datetime.date(1, 1, 1))")),
 ('TimeZonesAndPitfalls', 'LimitsOfTime', 'GregorianCalendar', 'datetime.date(1582, 10, 5)',
  "Python's date uses the Gregorian rules for every year, so 5 October 1582, a day that did not exist in the countries that adopted the calendar then, is a Tuesday in Python, 1900 and 2100 are not leap years, 2000 is, the years 1 to 9999 hold 2424 leap years and 3,652,059 days.",
  (X(_PRE + r'''out=(D(1582,10,5).strftime('%A %d %B %Y'), D(1582,10,4).toordinal()+1==D(1582,10,5).toordinal(), calendar.isleap(1900), calendar.isleap(2000), calendar.isleap(2024), calendar.isleap(2100), calendar.monthrange(2026,2), sum(calendar.isleap(y) for y in range(1,10000)), 365*9999+sum(calendar.isleap(y) for y in range(1,10000)))'''), "('Tuesday 05 October 1582', True, False, True, True, False, (calendar.SUNDAY, 28), 2424, 3652059)")),
 ('LaunchingPrograms', 'RunAndPopen', 'RunWaits', "subprocess.run(['C:\\\\Windows\\\\System32\\\\calc.exe'])",
  "subprocess.run starts the program, waits until it ends and returns a CompletedProcess that records the arguments and the return code, which prints as CompletedProcess(args=['sleep', '0.3'], returncode=0); capture_output adds stdout and stderr to the repr.",
  (X(_PRE + r'''t=time.monotonic(); r=subprocess.run(['sleep','0.3']); e=time.monotonic()-t
r2=subprocess.run([sys.executable,'-c','print("hi")'], capture_output=True, text=True)
out=(r, r.returncode, r.args, e>=0.3, type(r).__name__, r.stdout, r.stderr, repr(r2).replace(sys.executable,'PY'), subprocess.run(['true']), subprocess.run(['false']))'''), '(CompletedProcess(args=[\'sleep\', \'0.3\'], returncode=0), 0, [\'sleep\', \'0.3\'], True, \'CompletedProcess\', None, None, \'CompletedProcess(args=[\\\'PY\\\', \\\'-c\\\', \\\'print("hi")\\\'], returncode=0, stdout=\\\'hi\\\\n\\\', stderr=\\\'\\\')\', CompletedProcess(args=[\'true\'], returncode=0), CompletedProcess(args=[\'false\'], returncode=1))')),
 ('LaunchingPrograms', 'RunAndPopen', 'PopenNoWait', 'calc_proc = subprocess.Popen([...])',
  'subprocess.Popen returns at once with a Popen object; poll() returns None while the process runs and its return code after, wait() blocks until it ends, and wait(timeout=0.1) on a process that runs longer raises TimeoutExpired.',
  (X(_PRE + r'''t=time.monotonic(); p=subprocess.Popen(['sleep','0.4']); back=time.monotonic()-t
polls=[p.poll()]; code=p.wait(); polls.append(p.poll())
q=subprocess.Popen(['sleep','0.3']); first=q.poll() is None; n=0
while q.poll() is None: n+=1; time.sleep(0.01)
out=(back<0.2, polls, code, type(p).__name__, p.returncode, p.pid>0, first, n>3, q.wait(), err(lambda: subprocess.Popen(['sleep','2']).wait(timeout=0.1)))'''), '(True, [None, 0], 0, \'Popen\', 0, True, True, True, 0, (\'TimeoutExpired\', "Command \'[\'sleep\', \'2\']\' timed out after 0.1 seconds"))')),
 ('LaunchingPrograms', 'RunAndPopen', 'CheckAndTimeout', 'subprocess.run(cmd, check=True, timeout=10)',
  'run() does not raise for a program that fails unless check=True, which raises CalledProcessError with the return code; timeout kills the child and raises TimeoutExpired; a missing program raises FileNotFoundError and a directory PermissionError.',
  (X(_PRE + r'''out=(err(lambda: subprocess.run(['false'],check=True)), err(lambda: subprocess.run(['sleep','5'],timeout=0.2)), err(lambda: subprocess.run(['no-such-program-xyz'])), err(lambda: subprocess.run(['/etc'])), err(lambda: subprocess.run(['sh','-c','exit 2'],check=True)), issubclass(subprocess.CalledProcessError, subprocess.SubprocessError), issubclass(FileNotFoundError, OSError))'''), '((\'CalledProcessError\', "Command \'[\'false\']\' returned non-zero exit status 1."), (\'TimeoutExpired\', "Command \'[\'sleep\', \'5\']\' timed out after 0.2 seconds"), (\'FileNotFoundError\', "[Errno 2] No such file or directory: \'no-such-program-xyz\'"), (\'PermissionError\', "[Errno 13] Permission denied: \'/etc\'"), (\'CalledProcessError\', "Command \'[\'sh\', \'-c\', \'exit 2\']\' returned non-zero exit status 2."), True, True)')),
 ('LaunchingPrograms', 'ArgumentsAndOutput', 'ArgumentList', "subprocess.Popen(['notepad.exe', 'hello.txt'])",
  "Each item of the list becomes one argument of the program with no shell in between, so 'my file.txt' with a space arrives as one argument and *.txt arrives as the text *.txt, unexpanded; shlex.split cuts a command line into such a list.",
  (X(_PRE + r'''import ast
c='import sys; print(sys.argv[1:])'
r=subprocess.run([sys.executable,'-c','import sys; print(sys.argv)','one','two words'],capture_output=True,text=True)
out=(subprocess.run([sys.executable,'-c',c,'my file.txt','a b','--x=1'],capture_output=True,text=True).stdout.strip(), shlex.split("notepad 'my file.txt' x"), subprocess.run([sys.executable,'-c',c,'*.txt'],capture_output=True,text=True).stdout.strip(), r.stdout.strip(), len(ast.literal_eval(r.stdout)), subprocess.run(['sh','-c','echo "$0|$1|$2"','zero','one'],capture_output=True,text=True).stdout.strip())'''), '("[\'my file.txt\', \'a b\', \'--x=1\']", [\'notepad\', \'my file.txt\', \'x\'], "[\'*.txt\']", "[\'-c\', \'one\', \'two words\']", 3, \'zero|one|\')')),
 ('LaunchingPrograms', 'ArgumentsAndOutput', 'CaptureOutput', "subprocess.run(['ping', '-n', '4', 'nostarch.com'], capture_output=True, text=True)",
  "capture_output=True collects stdout and stderr, as bytes unless text=True makes them str, and cannot be combined with stdout=; the book's ping -n 4 is the Windows flag and exits 2 on Linux, where -c 2 sends two packets, here to 127.0.0.1 with no loss.",
  (X(_PRE + r'''r=subprocess.run([sys.executable,'-c','import sys; print("out"); print("err", file=sys.stderr)'],capture_output=True)
t=subprocess.run([sys.executable,'-c','import sys; print("out"); print("err", file=sys.stderr)'],capture_output=True,text=True)
a=subprocess.run(['ping','-n','4','localhost'],capture_output=True,text=True); b=subprocess.run(['ping','-c','2','-W','2','127.0.0.1'],capture_output=True,text=True)
out=(r.stdout, r.stderr, t.stdout, t.stderr, type(r.stdout).__name__, type(t.stdout).__name__, err(lambda: subprocess.run(['echo'],capture_output=True,stdout=subprocess.PIPE)), a.returncode, b.returncode, '2 received' in b.stdout, b.stdout.splitlines()[0].split(' (')[0], '0% packet loss' in b.stdout)'''), "(b'out\\n', b'err\\n', 'out\\n', 'err\\n', 'bytes', 'str', ('ValueError', 'stdout and stderr arguments may not be used with capture_output.'), 2, 0, True, 'PING 127.0.0.1', True)")),
 ('LaunchingPrograms', 'ArgumentsAndOutput', 'ShellTrueList', "subprocess.run(['start', 'hello.txt'], shell=True)",
  "On Windows shell=True with a list hands the list to cmd.exe, whose start command opens the file; on POSIX the first item alone is the command string and the others become the shell's own arguments, so ['echo', 'hi', 'there'] prints an empty line and ['start', 'hello.txt'] exits 127 with 'start: not found'.",
  (X(_PRE + r'''out=(subprocess.run(['echo','hi','there'],shell=True,capture_output=True,text=True).stdout, subprocess.run('echo hi there',shell=True,capture_output=True,text=True).stdout, subprocess.run(['start','hello.txt'],shell=True,capture_output=True,text=True).returncode, subprocess.run(['start','hello.txt'],shell=True,capture_output=True,text=True).stderr.strip().split(': ',1)[1], shutil.which('start'))'''), "('\\n', 'hi there\\n', 127, '1: start: not found', None)")),
 ('LaunchingPrograms', 'ArgumentsAndOutput', 'ShellInjection', "f'echo opening {name}' with shell=True",
  "A command string built from a file name and run with shell=True lets the name carry shell syntax: a name of 'x; echo INJECTED' runs a second command, while shlex.quote makes it one word and a list with no shell never interprets it.",
  (X(_PRE + r'''name='x; echo INJECTED'
a=subprocess.run(f'echo opening {name}',shell=True,capture_output=True,text=True).stdout
b=subprocess.run(f'echo opening {shlex.quote(name)}',shell=True,capture_output=True,text=True).stdout
c=subprocess.run(['echo','opening',name],capture_output=True,text=True).stdout
out=(a,b,c,shlex.quote(name),shlex.quote('plain.txt'))'''), '(\'opening x\\nINJECTED\\n\', \'opening x; echo INJECTED\\n\', \'opening x; echo INJECTED\\n\', "\'x; echo INJECTED\'", \'plain.txt\')')),
 ('LaunchingPrograms', 'ExitAndStopping', 'ExitCodes', 'proc.returncode',
  "A program that ends normally returns 0, sys.exit(3) returns 3, an uncaught exception 1, sys.exit('msg') 1, os._exit(263) 7 because only the low 8 bits are kept, and a process killed by signal 9 or 15 shows as -9 or -15 in returncode.",
  (X(_PRE + r'''c=lambda code: subprocess.run([sys.executable,'-c',code]).returncode
out=(c('pass'), c('import sys; sys.exit(3)'), c('raise ValueError'), c('import sys; sys.exit("msg")'), c('import os; os._exit(256+7)'), c('import os,signal; os.kill(os.getpid(), signal.SIGKILL)'), c('import os,signal; os.kill(os.getpid(), signal.SIGTERM)'))'''), '(0, 3, 1, 1, 7, -9, -15)')),
 ('LaunchingPrograms', 'ExitAndStopping', 'TerminateVsKill', 'proc.terminate(), proc.kill()',
  'terminate() sends SIGTERM, which a program can handle to save its work and exit with 0, kill() sends SIGKILL, which cannot be handled and leaves return code -9, and signal.signal(SIGKILL, handler) raises OSError.',
  (X(_PRE + r'''code="import signal,time,sys\nsignal.signal(signal.SIGTERM, lambda s,f: (print('asked to stop, saving work', flush=True), sys.exit(0)))\nprint('ready', flush=True)\ntime.sleep(30)"
p=subprocess.Popen([sys.executable,'-c',code], stdout=subprocess.PIPE, text=True); p.stdout.readline(); p.terminate(); o=p.communicate()[0]; a=(o.strip(), p.returncode)
p=subprocess.Popen([sys.executable,'-c',code], stdout=subprocess.PIPE, text=True); p.stdout.readline(); p.kill(); o=p.communicate()[0]; b=(o.strip(), p.returncode)
out=(a,b, signal.SIGKILL.value, signal.SIGTERM.value, err(lambda: signal.signal(signal.SIGKILL, lambda *a: 0)))'''), "(('asked to stop, saving work', 0), ('', -9), 9, 15, ('OSError', '[Errno 22] Invalid argument'))")),
 ('LaunchingPrograms', 'OpeningFilesWithDefaultApps', 'OpenCommand', "subprocess.run(['open', 'hello.txt'])",
  'open is a macOS command; on this Ubuntu machine /usr/bin/open exists only because the xdg-utils package registers an alternative that points to xdg-open, and for a file that does not exist it exits 2 with a message from xdg-open; os.startfile is defined on Windows only.',
  (X(_PRE + r'''r=subprocess.run(['open','/nonexistent-file'],capture_output=True,text=True)
out=(shutil.which('open'), os.path.realpath(shutil.which('open')), shutil.which('xdg-open'), r.returncode, r.stderr.strip().splitlines()[-1], hasattr(os,'startfile'), sys.platform, os.name)'''), '(\'/usr/bin/open\', \'/usr/bin/xdg-open\', \'/usr/bin/xdg-open\', 2, "xdg-open: file \'/nonexistent-file\' does not exist", False, \'linux\', \'posix\')')),
 ('LaunchingPrograms', 'OpeningFilesWithDefaultApps', 'Webbrowser', 'webbrowser.open(url)',
  "webbrowser.open returns False and webbrowser.get() raises Error ('could not locate runnable browser') on a machine with no browser and no BROWSER variable, so the call must be checked on a server or in a container.",
  (X(_PRE + r'''import webbrowser
out=(webbrowser.open('file:///nonexistent'), err(lambda: webbrowser.get()), webbrowser.open_new_tab.__name__, os.environ.get('BROWSER'))'''), "(False, ('Error', 'could not locate runnable browser'), 'open_new_tab', None)")),
 ('LaunchingPrograms', 'OpeningFilesWithDefaultApps', 'ClipboardAndSound', 'pyperclip.copy(text)',
  "pyperclip 1.11.0 raises PyperclipException, a RuntimeError, when no copy and paste program such as xclip, xsel or wl-clipboard is installed, and playsound3 3.3.2, which replaces the book's pinned playsound3 2.4.0, exposes playsound(), backends and PlaysoundException.",
  (X(_PRE + r'''import pyperclip, playsound3, importlib.metadata as md
e=err(lambda: pyperclip.copy('x'))
out=(md.version('pyperclip'), e[0], e[1][:60], pyperclip.PyperclipException.__mro__[1].__name__, md.version('playsound3'), sorted(n for n in dir(playsound3) if not n.startswith('_'))[:8], hasattr(playsound3,'playsound'))'''), "('1.11.0', 'PyperclipException', 'Pyperclip could not find a copy/paste mechanism for your sys', 'RuntimeError', '3.3.2', ['AVAILABLE_BACKENDS', 'DEFAULT_BACKEND', 'PlaysoundException', 'backends', 'playsound', 'playsound3', 'prefer_backends'], True)")),
 ('SchedulingTasks', 'OsSchedulers', 'CronFields', '30 9 * * 1-5',
  "A crontab entry has five time fields, minute, hour, day of month, month and day of week, and the command; '30 9 * * 1-5' runs at 09:30 on weekdays, '*/15 * * * *' every quarter hour, and when both day fields are restricted a day matches if either does, so '0 0 13 * 5' fires on every 13th and every Friday, not on Friday the 13th.",
  (X(_PRE + r'''def parse(f, lo, hi):
    vals=set()
    for part in f.split(','):
        step=1
        if '/' in part: part, s = part.split('/'); step=int(s)
        if part=='*': a,b=lo,hi
        elif '-' in part: a,b=map(int,part.split('-'))
        else: a=b=int(part)
        if '/' in f and '-' not in part and part!='*' : b=hi
        vals.update(range(a,b+1,step))
    return vals
def nxt(expr, start):
    m,h,dom,mon,dow=expr.split()
    M,H,DOM,MON=parse(m,0,59),parse(h,0,23),parse(dom,1,31),parse(mon,1,12)
    DOW=parse(dow.replace('7','0'),0,6)
    t=start.replace(second=0,microsecond=0)+TD(minutes=1)
    while True:
        cd=(t.weekday()+1)%7
        ok=t.minute in M and t.hour in H and t.month in MON
        dm=dom=='*'; dwm=dow=='*'
        day=(t.day in DOM) if dwm else (cd in DOW) if dm else (t.day in DOM or cd in DOW)
        if ok and day: return t
        t+=TD(minutes=1)
s=DT(2026,10,13,9,30)
out=(nxt('30 9 * * 1-5', s), nxt('*/15 * * * *', s), nxt('0 0 13 * 5', s), nxt('0 4 * * *', s), nxt('0 0 29 2 *', s), sorted(parse('*/20',0,59)))'''), '(datetime.datetime(2026, 10, 14, 9, 30), datetime.datetime(2026, 10, 13, 9, 45), datetime.datetime(2026, 10, 16, 0, 0), datetime.datetime(2026, 10, 14, 4, 0), datetime.datetime(2028, 2, 29, 0, 0), [0, 20, 40])')),
 ('SchedulingTasks', 'OsSchedulers', 'CronEnvironment', 'crontab -e',
  "A job started by cron does not run in the shell that installed it: on this machine a Python job run by cron 3.0pl1 saw PATH=/usr/bin:/bin, the working directory /root, 6 environment variables, no terminal, sh as its parent and a clock in UTC while the shell's TZ was Europe/Istanbul; a TZ=Asia/Kolkata line reached the job and set its clock to IST, but the time an entry fires follows the zone of the cron daemon, not of the job, and a CRON_TZ line was passed to the job as a variable and did not move the schedule.",
  None),
 ('SchedulingTasks', 'OsSchedulers', 'LaunchdPlist', 'StartCalendarInterval',
  'launchd on macOS reads a property list in which StartCalendarInterval names the hour and minute of a daily job; plistlib writes and reads such a file as XML and the result reads back equal to the dictionary, but nothing here ran launchd.',
  (X(_PRE + r'''import plistlib
d={'Label':'org.example.backup','ProgramArguments':['/usr/bin/python3','/Users/al/backup.py'],'StartCalendarInterval':{'Hour':4,'Minute':0}}
b=plistlib.dumps(d); back=plistlib.loads(b)
out=(back==d, b.decode().splitlines()[:3], len(b), b.count(b'<key>'), plistlib.FMT_XML.name)'''), '(True, [\'<?xml version="1.0" encoding="UTF-8"?>\', \'<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\', \'<plist version="1.0">\'], 501, 5, \'FMT_XML\')')),
 ('SchedulingTasks', 'OsSchedulers', 'SystemdCalendar', 'OnCalendar=Mon..Fri 09:00',
  "A systemd timer takes an OnCalendar expression, and systemd-analyze calendar normalises it without running anything: 'Mon..Fri 09:00' becomes 'Mon..Fri *-*-* 09:00:00', 'daily' becomes '*-*-* 00:00:00' and 'weekly' becomes 'Mon *-*-* 00:00:00'; the container's PID 1 is not systemd, so no timer ran.",
  (X(_PRE + r'''def cal(expr, tz):
    r=subprocess.run(['systemd-analyze','calendar',expr],capture_output=True,text=True,env=dict(os.environ,TZ=tz)); return r.stdout.splitlines()[:2]
out=(cal('Mon..Fri 09:00','UTC'), cal('*-*-* 04:00','Europe/Istanbul'), cal('daily','UTC'), cal('weekly','UTC'))'''), "(['  Original form: Mon..Fri 09:00', 'Normalized form: Mon..Fri *-*-* 09:00:00'], ['  Original form: *-*-* 04:00', 'Normalized form: *-*-* 04:00:00'], ['  Original form: daily', 'Normalized form: *-*-* 00:00:00'], ['  Original form: weekly', 'Normalized form: Mon *-*-* 00:00:00'])")),
 ('SchedulingTasks', 'InProcessScheduling', 'SchedModule', 'sched.scheduler(time.monotonic, time.sleep)',
  'sched.scheduler keeps events in a queue ordered by time and then priority and run() calls them in that order: with a fake clock, events at 0 s, 2 s and two at 5 s with priorities 1 and 0 ran as now, two, five with priority 0, five, and cancel() on an event that has run raises ValueError.',
  (X(_PRE + r'''clock=[0.0]; log=[]
s=sched.scheduler(lambda: clock[0], lambda d: clock.__setitem__(0, clock[0]+d))
s.enter(5, 1, log.append, ('five',)); s.enter(2, 1, log.append, ('two',)); s.enter(5, 0, log.append, ('five, priority 0',)); s.enter(0, 9, log.append, ('now',))
n=len(s.queue); s.run()
clock2=[100.0]; log2=[]
s2=sched.scheduler(lambda: clock2[0], lambda d: clock2.__setitem__(0, clock2[0]+d))
e=s2.enterabs(130, 1, log2.append, ('thirty',)); s2.enterabs(110, 1, log2.append, ('ten',)); s2.cancel(e); s2.enterabs(90, 1, log2.append, ('past',))
s2.run()
out=(n, log, clock[0], s.empty(), log2, clock2[0], err(lambda: s2.cancel(e))[0])'''), "(4, ['now', 'two', 'five, priority 0', 'five'], 5.0, True, ['past', 'ten'], 110.0, 'ValueError')")),
 ('SchedulingTasks', 'InProcessScheduling', 'TimerThread', 'threading.Timer(0.1, func)',
  'threading.Timer is a Thread that calls a function once after a delay; nothing has run right after start(), the call has run after join(), and cancel() stops a timer that has not fired.',
  (X(_PRE + r'''hits=[]
t=threading.Timer(0.1, hits.append, args=('fired',)); t.start(); mid=list(hits); t.join()
t2=threading.Timer(5, hits.append, args=('never',)); t2.start(); t2.cancel(); t2.join(1)
out=(mid, hits, threading.Timer.__mro__[1].__name__, t.is_alive(), t2.is_alive(), t.daemon)'''), "([], ['fired'], 'Thread', False, False, False)")),
 ('SchedulingTasks', 'InProcessScheduling', 'AsyncioCallLater', 'loop.call_later(0.2, func)',
  'An asyncio event loop runs a callback after a delay with call_later or at a loop time with call_at: callbacks scheduled with call_soon, then call_later 0.1 and 0.2, ran in the order soon, later 0.1, later 0.2.',
  (X(_PRE + r'''import asyncio
log=[]
async def main():
    loop=asyncio.get_running_loop(); loop.call_later(0.2, log.append, 'later 0.2'); loop.call_later(0.1, log.append, 'later 0.1'); loop.call_soon(log.append, 'soon')
    await asyncio.sleep(0.3)
asyncio.run(main())
out=log'''), "['soon', 'later 0.1', 'later 0.2']")),
 ('SchedulingTasks', 'InProcessScheduling', 'ScheduleLibrary', "schedule.every().day.at('10:30').do(job)",
  "The third-party schedule 1.2.2 runs jobs written as every().day.at('10:30').do(job) inside a running Python process: the first run is set for 10:30:00 and an every(10).minutes job is more than 590 seconds away; the process must keep calling run_pending, so it is not an operating system scheduler.",
  (X(_PRE + r'''import schedule, importlib.metadata as md
s=schedule.Scheduler(); j=s.every().day.at('10:30').do(print, 'job'); k=s.every(10).minutes.do(print, 'tick')
out=(md.version('schedule'), j.next_run.strftime('%H:%M:%S'), (k.next_run-DT.now()).total_seconds()>590, str(j)[:30], s.idle_seconds is not None, len(s.jobs))'''), "('1.2.2', '10:30:00', True, 'Job(interval=1, unit=days, do=', True, 2)")),
 ('BookAndPractice', 'ListingsAsPrinted', 'EnDashListings', 'end_time – start_time',
  "Four places in three listings of the chapter, listings 2, 6 and 12 of the web page, write the en dash U+2013 where the minus sign belongs, and the compiler refuses the character with SyntaxError 'invalid character'; a minus sign compiles, and the en dash is not an identifier character either.",
  (X(_PRE + r'''out = (err(lambda: compile('x = 5 – 3', 'f', 'exec')), err(lambda: compile('x = 5 - 3', 'f', 'exec'))[0], err(lambda: compile("print(f'{5 – 3}')", 'f', 'exec')), ord('–'), '–'.isidentifier())'''), '((\'SyntaxError\', "invalid character \'–\' (U+2013) (f, line 1)"), \'ok\', (\'SyntaxError\', "invalid character \'–\' (U+2013) (f, line 1)"), 8211, False)')),
 ('BookAndPractice', 'ListingsAsPrinted', 'ShippedFiles', 'calcProd.py, stopwatch.py, simplecountdown.py',
  'The online materials ship three files for the chapter and none of them is the printed listing: stopwatch.py has two en dashes, CRLF line ends and a print without the f prefix, calcProd.py loops to 99999, prints a digit count and has an en dash, and simplecountdown.py differs from the chapter only in spacing; the study fetched them and compared their SHA-256 hashes.',
  None),
 ('BookAndPractice', 'ListingsAsPrinted', 'ReplayOfListings', '>>> statements of the interactive sessions',
  "The 75 statements of the 20 interactive sessions were replayed in a clean Python 3.14.6 in the author's zone, America/Los_Angeles: 54 printed what the book prints and 21 did not, of which 7 depend on the clock, 1 is the en dash and 13 need Windows or macOS or a program Linux lacks; with the dash repaired 55 match, and in the zone of Istanbul one more differs, fromtimestamp(1000000).",
  None),
 ('BookAndPractice', 'SuperStopwatch', 'LapArithmetic', 'lap_time = round(time.time() - last_time, 2)',
  'The stopwatch program rounds each difference to two digits, so for the readings 0, 3.56, 8.63, 17.68 and 19.11 it prints laps 3.56, 5.07, 9.05 and 1.43 with the totals 3.56, 8.63, 17.68 and 19.11, while the unrounded last lap is 1.4299999999999997.',
  (X(_PRE + r'''seq=[0.0, 3.56, 8.63, 17.68, 19.11]; start=seq[0]; last=start; rows=[]
for i, now in enumerate(seq[1:], 1):
    lap=round(now-last,2); total=round(now-start,2); rows.append((i,total,lap)); last=now
printed=[f'Lap #{n}: {tot}({lap})' for n,tot,lap in rows]
out=(printed, round(8.63-3.56,2), 8.63-3.56, round(19.11-17.68,2), 19.11-17.68)'''), "(['Lap #1: 3.56(3.56)', 'Lap #2: 8.63(5.07)', 'Lap #3: 17.68(9.05)', 'Lap #4: 19.11(1.43)'], 5.07, 5.07, 1.43, 1.4299999999999997)")),
 ('BookAndPractice', 'SuperStopwatch', 'ColumnFormatting', 'str(lap_time).rjust(6)',
  "The Prettified Stopwatch pads the lap number to 2 characters and the times to 6 with rjust, which produces the book's lines such as 'Lap # 1:   3.56 (  3.56)', and an f-string with >2 and >6 produces the same text; str(2.0).ljust(6) is '2.0   ' and a float is formatted without losing a trailing zero only by .2f.",
  (X(_PRE + r'''expected=['Lap # 1:   3.56 (  3.56)','Lap # 2:   8.63 (  5.07)','Lap # 3:  17.68 (  9.05)','Lap # 4:  19.11 (  1.43)']
rows=[(1,3.56,3.56),(2,8.63,5.07),(3,17.68,9.05),(4,19.11,1.43)]
got=['Lap #' + str(n).rjust(2) + ': ' + str(t).rjust(6) + ' (' + str(l).rjust(6) + ')' for n,t,l in rows]
got2=[f'Lap #{n:>2}: {t:>6} ({l:>6})' for n,t,l in rows]
out=(got==expected, got2==expected, [str(x).ljust(6) for x in (2.0,)], str(2.0), str(round(2.004,2)), f'{round(2.004,2):.2f}', len(max(expected,key=len)))'''), "(True, True, ['2.0   '], '2.0', '2.0', '2.00', 24)")),
 ('BookAndPractice', 'SimpleCountdown', 'CountdownLoop', 'while time_left > 0:',
  'The countdown loop prints the time left, sleeps one second and subtracts one; counted with a fake sleep, 3 seconds print 3, 2 and 1 and then Beep!, after 3.0 seconds of sleeping, and the real program takes slightly longer than the sum of its sleeps.',
  (X(_PRE + r'''lines=[]; left=3; t=[0.0]
def sleep(d): t[0]+=d
while left>0:
    lines.append(str(left)+' '); sleep(1); left-=1
lines.append('Beep!')
out=(lines, t[0])'''), "(['3 ', '2 ', '1 ', 'Beep!'], 3.0)")),
 ('BookAndPractice', 'SimpleCountdown', 'AlarmSound', 'autbor.com/alarm.wav',
  'autbor.com/alarm.wav answers 302 and redirects to automatetheboringstuff.com/src/alarm.wav, a 582,952-byte 16-bit stereo 44.1 kHz file of 3.30 seconds; the online materials do not hold it, and no sound could be played in the container, so the playing was not heard.',
  None),
 ('BookAndPractice', 'PracticePrograms', 'FridayForward', 'while len(found) < 10: if d.day == 13 and d.weekday() == 4',
  'Walking forward one day at a time from 13 October 2026 finds the next ten Friday the 13ths: 13 November 2026, 13 August 2027, 13 October 2028, 13 April 2029, 13 July 2029, 13 September 2030, 13 December 2030, 13 June 2031, 13 February 2032 and 13 August 2032.',
  (X(_PRE + r'''d=D(2026,10,13); one=TD(days=1); found=[]
while len(found)<10:
    if d.day==13 and d.weekday()==4: found.append(d)
    d+=one
out=([x.isoformat() for x in found], [x.strftime('%B %Y') for x in found][:3], all(x.strftime('%A')=='Friday' for x in found))'''), "(['2026-11-13', '2027-08-13', '2028-10-13', '2029-04-13', '2029-07-13', '2030-09-13', '2030-12-13', '2031-06-13', '2032-02-13', '2032-08-13'], ['November 2026', 'August 2027', 'October 2028'], True)")),
 ('BookAndPractice', 'PracticePrograms', 'FridayBackward', 'd -= datetime.timedelta(days=1)',
  "Walking backward from 13 October 2026 finds 3485 Friday the 13ths, the latest 13 March 2026 and the earliest 13 April of the year 1, then date arithmetic raises OverflowError at 1 January of the year 1, 739,901 days back; the 400-year Gregorian cycle of 146,097 days is a multiple of 7 and holds 688 Friday the 13ths, more than any other weekday's 13ths.",
  (X(_PRE + r'''from collections import Counter
d=D(2026,10,13); one=TD(days=1); n=0; first=None; last=None
try:
    while True:
        if d.day==13 and d.weekday()==4:
            n+=1; last=d
            if first is None: first=d
        d-=one
except OverflowError as e: stop=(str(e), d)
byday=Counter(D(y,m,13).weekday() for y in range(2000,2400) for m in range(1,13))
out=(first, last, n, stop, (D(2026,10,13)-D(1,1,1)).days, sorted(byday.items()), (400*365+97)%7, 400*365+97)'''), "(datetime.date(2026, 3, 13), datetime.date(1, 4, 13), 3485, ('date value out of range', datetime.date(1, 1, 1)), 739901, [(0, 685), (1, 685), (2, 687), (3, 684), (4, 688), (5, 684), (6, 687)], 0, 146097)")),
 ('BookAndPractice', 'PracticePrograms', 'AppendixBAnswers', 'round(2.5)',
  "Appendix B answers question 3 with time.asctime(), which prints what ctime() prints for the current time, question 5 with 'the closest integer', which is incomplete because round(2.5) is 2 and round(x, 2) returns a float, and question 7 with weekday() equal to 0 for Monday, which is right.",
  (X(_PRE + r'''out=(round(2.4), round(2.5), round(3.5), type(round(2.5)).__name__, type(round(2.5,2)).__name__, child("import time; print(time.asctime() == time.ctime())"), child("import time; print(time.asctime(time.localtime(5)) == time.ctime(5))"), time.asctime(time.gmtime(0)), DT(2019,1,7).weekday())'''), "(2, 2, 4, 'int', 'float', 'True', 'True', 'Thu Jan  1 00:00:00 1970', 0)")),
]

CLAIMS = [
 (X(_PRE + r'''import importlib.metadata as m
out = (m.version('pyperclip'), m.version('playsound3'), m.version('tzdata'), m.version('schedule'), sys.version_info[:2] >= (3, 14))'''), "('1.11.0', '3.3.2', '2026.5', '1.2.2', True)"),
 (X(_PRE + r'''out = (365 * 30, 365 * 60, 54 + 21, 6 + 1 + 13 + 1, 55 + 20, 75 - 54, 2026 - 1996, 2026 - 1966)'''), '(10950, 21900, 75, 21, 75, 21, 30, 60)'),
 (X(_PRE + r'''out = (sys.get_int_max_str_digits(), len(str(math.factorial(1000))), math.factorial(100000).bit_length(), 2**31 - 1, 2**32)'''), '(4300, 2568, 1516705, 2147483647, 4294967296)'),
 (X(_PRE + r'''out = (round(2**32 / 60 / (365.2425 * 86400), 3), round(2**31 / 86400 / 365.2425, 2), calendar.timegm((2038, 1, 19, 3, 14, 7)) == 2**31 - 1, 10 + 27)'''), '(2.268, 68.05, True, 37)'),
 (X(_PRE + r'''out = (D(1582, 10, 4) + TD(days=1), 15 - 5, D(1582, 10, 15).weekday(), D(1582, 10, 4).weekday())'''), '(datetime.date(1582, 10, 5), 10, 4, 0)'),
 (X(_PRE + r'''out = (TD.max.days, TD.min.days, TD(days=1).total_seconds(), TD(weeks=1) == TD(days=7), TD(hours=36) == TD(days=1, hours=12))'''), '(999999999, -999999999, 86400.0, True, True)'),
 (X(_PRE + r'''out = (time.gmtime(1000000)[:6], DT.fromtimestamp(1000000, UTC).isoformat(), calendar.timegm((1970, 1, 12, 13, 46, 40)))'''), "((1970, 1, 12, 13, 46, 40), '1970-01-12T13:46:40+00:00', 1000000)"),
 (X(_PRE + r'''out = (DT(2026, 3, 8).strftime('%A'), DT(2026, 11, 1).strftime('%A'), DT(2026, 3, 17).strftime('%A'), DT(2026, 10, 13).strftime('%A'), DT(2026, 10, 31).strftime('%A'))'''), "('Sunday', 'Sunday', 'Tuesday', 'Tuesday', 'Saturday')"),
 (X(_PRE + r'''out = (len(max(['Lap # 1:   3.56 (  3.56)', 'Lap # 4:  19.11 (  1.43)'], key=len)), 'Lap #'.ljust(7) + '|', '3.56'.rjust(6), '5.07'.ljust(6) + '|')'''), "(24, 'Lap #  |', '  3.56', '5.07  |')"),
 (X(_PRE + r'''out = (subprocess.run([sys.executable, '-c', 'pass']).returncode, subprocess.run(['sleep', '0']).returncode, subprocess.run(['sh', '-c', 'exit 5']).returncode)'''), '(0, 0, 5)'),
 (X(_PRE + r'''out = (shlex.split('a "b c" d'), shlex.quote('a b'), shlex.join(['a', 'b c']))'''), '([\'a\', \'b c\', \'d\'], "\'a b\'", "a \'b c\'")'),
 (X(_PRE + r'''out = (hasattr(time, 'tzset'), hasattr(os, 'startfile'), hasattr(time, 'clock'), hasattr(time, 'monotonic_ns'), hasattr(DT, 'utcnow'), hasattr(UTC, 'utcoffset'))'''), '(True, False, False, True, True, True)'),
 (X(_PRE + r'''out = (calendar.monthrange(2024, 2)[1], calendar.monthrange(2026, 2)[1], calendar.monthrange(2100, 2)[1], calendar.isleap(2000), len(calendar.month_name))'''), '(29, 28, 28, True, 13)'),
]
ERRORS = []

BEH = [
 ['an en dash in an expression is a SyntaxError and a minus sign is not',
  r'''for src in ('x = 5 \u2013 3', 'x = 5 - 3'):
    try:
        compile(src, 'f', 'exec'); print('compiles')
    except SyntaxError as e:
        print(type(e).__name__, e.msg)''',
  "SyntaxError invalid character '–' (U+2013)\ncompiles"],
 ['the stopwatch print without the f prefix prints the braces',
  r'''lap_number = 1
print('Lap #{lap_number}: ')
print(f'Lap #{lap_number}: ')''',
  'Lap #{lap_number}: \nLap #1:'],
 ['a backslash followed by U or A in a string draws a warning or an error',
  r'''import warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); compile("p = 'C:\\\\Users\\Al\\\\hello.txt'", 'f', 'exec')
print([x.category.__name__ for x in w])
try:
    compile("p = 'C:\\\\Users\\\\Al\\\\hello.txt'", 'f', 'exec'); print('doubled backslashes compile cleanly')
except SyntaxError as e:
    print(e.msg)''',
  "['SyntaxWarning']\ndoubled backslashes compile cleanly"],
 ['strptime with a month and a day and no year draws a DeprecationWarning for 29 February',
  r'''import warnings, datetime
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    try: datetime.datetime.strptime('02/29', '%m/%d')
    except ValueError as e: print(e)
print([x.category.__name__ for x in w])''',
  "day 29 must be in range 1..28 for month 2 in year 1900\n['DeprecationWarning']"],
 ['utcnow draws a DeprecationWarning',
  r'''import warnings, datetime
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); datetime.datetime.utcnow()
print([x.category.__name__ for x in w], datetime.datetime.now(datetime.UTC).tzinfo)''',
  "['DeprecationWarning'] UTC"],
 ['round goes to the even neighbour and returns an int without digits',
  r'''print(round(2.5), round(3.5), round(2.675, 2), type(round(2.5)).__name__, type(round(2.5, 1)).__name__)''',
  '2 4 2.67 int float'],
 ['the two-digit year 68 is 2068 and 69 is 1969',
  r'''import datetime
print(datetime.datetime.strptime('68', '%y').year, datetime.datetime.strptime('69', '%y').year)''',
  '2068 1969'],
 ['a day added across the change to daylight saving time is 23 hours long in UTC',
  r'''import datetime, zoneinfo
ny = zoneinfo.ZoneInfo('America/New_York'); a = datetime.datetime(2026, 3, 7, 12, tzinfo=ny); b = a + datetime.timedelta(days=1)
print(b - a, b.astimezone(datetime.UTC) - a.astimezone(datetime.UTC))''',
  '1 day, 0:00:00 23:00:00'],
 ['the same epoch second prints three different clocks in three zones',
  r'''import os, subprocess, sys
for z in ('America/Los_Angeles', 'UTC', 'Europe/Istanbul'):
    print(z, subprocess.run([sys.executable, '-c', 'import datetime; print(datetime.datetime.fromtimestamp(1000000))'], capture_output=True, text=True, env=dict(os.environ, TZ=z)).stdout.strip())''',
  'America/Los_Angeles 1970-01-12 05:46:40\nUTC 1970-01-12 13:46:40\nEurope/Istanbul 1970-01-12 15:46:40'],
 ['SIGKILL cannot be handled',
  r'''import signal
try: signal.signal(signal.SIGKILL, lambda *a: None)
except OSError as e: print(type(e).__name__, e.errno)''',
  'OSError 22'],
 ['a child that calls sys.exit(3) leaves return code 3',
  r'''import subprocess, sys
print(subprocess.run([sys.executable, '-c', 'import sys; sys.exit(3)']).returncode)''',
  '3'],
 ['a list with shell=True runs only its first item on POSIX',
  r'''import subprocess
r = subprocess.run(['echo', 'hi', 'there'], shell=True, capture_output=True, text=True)
print(repr(r.stdout))''',
  "'\\n'"],
 ['time.sleep returns None and lasts at least the time asked on the monotonic clock',
  r'''import time
t = time.monotonic(); r = time.sleep(0.1); print(r, time.monotonic() - t >= 0.1)''',
  'None True'],
 ['sched runs events in time and priority order with a fake clock',
  r'''import sched
c = [0]; log = []
s = sched.scheduler(lambda: c[0], lambda d: c.__setitem__(0, c[0] + d))
s.enter(2, 1, log.append, ('b',)); s.enter(1, 1, log.append, ('a',)); s.enter(2, 0, log.append, ('b0',))
s.run(); print(log, c[0])''',
  "['a', 'b0', 'b'] 2"],
 ['the Friday the 13th count in the 400 years from 2000 is 688',
  r'''import datetime
print(sum(1 for y in range(2000, 2400) for m in range(1, 13) if datetime.date(y, m, 13).weekday() == 4))''',
  '688'],
 ['the date of the Gregorian reform in Python has a Tuesday on the missing day',
  r'''import datetime
print(datetime.date(1582, 10, 5).strftime('%A'), datetime.date(1582, 10, 4).weekday(), (datetime.date(1582, 10, 15) - datetime.date(1582, 10, 4)).days)''',
  'Tuesday 0 11'],
 ['the POSIX epoch second of 2038-01-19 03:14:07 UTC is 2**31 - 1',
  r'''import calendar
print(calendar.timegm((2038, 1, 19, 3, 14, 7)), 2**31 - 1)''',
  '2147483647 2147483647'],
]

BODY = {}
def _b(key, p1, p2):
    BODY[key] = p1 + "\n\n" + p2

# ---- the six subjects ----
_b('EpochClock',
 'The chapter opens with the system clock: the time module reads it, time.time() returns the number of seconds since the Unix epoch, time.sleep() pauses a program, and Project 14, the Super Stopwatch, subtracts two readings to time laps [S]. The Python documentation defines the epoch as the point where the time begins, 1 January 1970 00:00:00 UTC on all platforms it describes, and lists clocks that differ in whether they can go backwards [PY][PEP418].',
 'Three ideas carry this subject. The epoch timestamp covers the zero point, the POSIX formula that ignores leap seconds and the precision of a float. The clock kinds cover the wall clock, the monotonic clock, the stepped clock, round() and profiling. Pausing programs covers sleep, signals, polling loops and drift. Each was executed under Python 3.14.6 (This study, 2026).')
_b('DatetimeValues',
 'The second half of the time material is the datetime module: datetime objects hold a moment, timedelta objects hold a duration, strftime() turns a moment into text with the directives of Table 19-1, and strptime() reads text back into a moment [S]. The Python documentation describes the types as naive or aware and lists the directives and the rules for two-digit years [PY].',
 "Three ideas carry this subject. Moments and fields cover making, reading, comparing and naming the weekday of a datetime. Durations cover timedelta, its missing months and the chapter's thirty-year example. Format and parse cover the directive table, strptime, the two-digit year rule, the yearless date and ISO 8601 (This study, 2026).")
_b('TimeZonesAndPitfalls',
 'The chapter never uses a time zone object, yet it prints times of day and says that its examples were run in Pacific Standard Time [S]. The Python documentation says that a naive datetime does not contain time zone information and that the zoneinfo module provides the IANA time zone database [PY][PEP615].',
 'Three ideas carry this subject. Zone awareness covers naive and aware values, the deprecation of utcnow, the zone database and the zone of the process. Daylight saving covers the day of 23 hours, the missing hour and the repeated hour. Limits of time cover the year 2038, the range of the date types and the Gregorian calendar (This study, 2026).')
_b('LaunchingPrograms',
 "The chapter's third part launches other programs from Python: subprocess.run() starts a program and waits, subprocess.Popen() starts it and returns at once, a list of strings carries the command line arguments, capture_output=True collects the text, and start or open opens a file with its default application [S]. The Python documentation says that the recommended approach for invoking subprocesses is the run() function for all use cases it can handle [PY].",
 'Four ideas carry this subject. Run and Popen cover waiting and not waiting. Arguments and output cover the argument list, capturing text, shell=True with a list and injection. Exit and stopping cover return codes, terminate and kill. Opening files covers the open command, the browser, the clipboard and sound. The Windows and macOS programs were not run (This study, 2026).')
_b('SchedulingTasks',
 "The chapter hands scheduling to the operating system in one paragraph: Task Scheduler on Windows, launchd on macOS and cron on Linux, with instructions it says are at the book's page at No Starch Press [S]. The Python standard library offers only schedulers that live inside a running process: the sched module, threading.Timer and the call_later method of an asyncio event loop [PY].",
 'Two ideas carry this subject. Operating system schedulers cover the cron fields and environment, a launchd property list and a systemd calendar expression. In-process scheduling covers sched, Timer, asyncio and the schedule package. Cron was run for real on this machine; Task Scheduler and launchd were not (This study, 2026).')
_b('BookAndPractice',
 'The chapter ends with Project 14, the Super Stopwatch, Project 15, the Simple Countdown, a summary, seven practice questions with their answers in Appendix B and two practice programs, the Prettified Stopwatch and the Friday the 13th finder [S][APPB]. The online materials ship three files for the chapter [S].',
 'Four ideas carry this subject. The listings as printed cover the en dashes, the shipped files and the replay of the sessions. The Super Stopwatch covers its arithmetic and its columns. The Simple Countdown covers its loop and its sound. The practice programs cover the Friday the 13th finder and the answers of Appendix B (This study, 2026).')
# ---- the mid concepts ----
_b('EpochTimestamp',
 'The chapter says time.time() returns a float of the seconds that have passed since the Unix epoch, which it calls the reference moment of 1 January 1970 UTC, and calls the value an epoch timestamp [S]. POSIX defines the seconds since the epoch by an expression of the year, day of the year, hour, minute and second in which a day has exactly 86400 seconds [POSIX].',
 'Three small programs tested the definition: the zero point, the POSIX expression against calendar.timegm, and the precision of a float timestamp against an integer count of nanoseconds (This study, 2026).')
_b('ClockKinds',
 'The chapter profiles a loop by subtracting one time.time() reading from another, and the Python documentation lists several clocks that differ in whether they are monotonic and whether they can be adjusted [S][PY]. PEP 418 added monotonic() and perf_counter() because the system clock can go backwards [PEP418].',
 'The clocks were queried with get_clock_info, a clock that is set back was simulated, round() was run on the values the stopwatch rounds, and the profiling listing was compared with math.factorial (This study, 2026).')
_b('PausingPrograms',
 'The chapter says time.sleep() blocks, that is it will not return, until the number of seconds passed has elapsed, and uses it to count seconds in the stopwatch and to wait in a loop until Halloween 2039 [S]. The Python documentation says the sleep is at least the time asked unless a signal handler raises an exception, a rule that PEP 475 introduced in Python 3.5 [PY][PEP475].',
 'Sleep was timed on a monotonic clock, a signal was delivered during a sleep, a polling loop was measured in processor time, and a loop that sleeps a fixed second was compared with one that sleeps until the next tick (This study, 2026).')
_b('MomentsAndFields',
 'The chapter makes a datetime with datetime.datetime(2026, 10, 21, 16, 29, 0), reads the year, month, day, hour, minute and second attributes, calls datetime.datetime.now(), and compares moments with the usual operators [S]. The Python documentation lists the same fields and adds microsecond, tzinfo and fold [PY].',
 'The fields, the checks on their values, now() against fromtimestamp(time.time()), the comparison operators and the weekday of 7 January 2019 were executed (This study, 2026).')
_b('DurationsTimedelta',
 'The chapter makes a timedelta with keyword arguments for weeks, days, hours, minutes, seconds and the smaller units, reads its days, seconds and microseconds attributes, uses total_seconds(), adds 1000 days to now and subtracts about thirty years from 21 October 2026 [S]. The Python documentation says all arguments are optional and default to 0 and that only days, seconds and microseconds are stored [PY].',
 'The attributes, a negative duration, the missing months, the arithmetic operators and the thirty-year example were executed and the leap days between 1996 and 2026 were counted (This study, 2026).')
_b('FormatAndParse',
 'Table 19-1 of the chapter lists strftime directives from %Y to %%, strftime() turns a datetime into text and strptime() reads text into a datetime with the same directives, and the chapter sends the reader to strftime.org for the full list [S]. The Python documentation has two tables of the directives, one for the C standard and one for Python, with notes on platform differences [PY].',
 'Every directive of the table was run on a fixed moment, the %y rule was run at its edges, strptime was run with inputs it accepts and refuses, and the year-less date was run under 3.14.6 and the other releases (This study, 2026).')
_b('ZoneAwareness',
 "The chapter's outputs depend on the zone of the author's computer, which it names once as Pacific Standard Time [S]. The Python documentation separates naive values from aware values and says that ZoneInfo gives an IANA time zone with the daylight saving time rules [PY][IANA].",
 "Naive and aware values were compared, utcnow() was run with warnings on, ZoneInfo was run with and without the tzdata package, fromtimestamp() was run in three zones, and the author's date was converted to Los Angeles time (This study, 2026).")
_b('DaylightSaving',
 'The chapter adds timedelta values to datetime values and does not say that a day is not always 24 hours [S]. PEP 495 added the fold attribute so that a time that happens twice on the day the clocks go back can be told apart [PEP495].',
 'A day was added to a New York datetime across the change of 8 March 2026, a time that does not exist and a time that happens twice were converted to UTC (This study, 2026).')
_b('LimitsOfTime',
 'The chapter counts time from 1970 and adds thousands of days, and it does not say where the counting ends [S]. The Python documentation says the year of a date is limited to 1 through 9999 and that the date type uses the Gregorian calendar in both directions [PY].',
 'A 32-bit counter was wrapped, the ends of the date range were passed, and the calendar was queried for the reform of 1582 (This study, 2026).')
_b('RunAndPopen',
 'The chapter says subprocess.run() launches a process, waits for it and returns a CompletedProcess, and that Popen returns a Popen object at once whose poll() returns None while the process runs and whose wait() blocks [S]. The Python documentation describes run() as the recommended approach and Popen as the underlying interface [PY].',
 'Both were run on Linux with sleep, true and false as the programs, with the waiting timed on a monotonic clock, and with check and timeout (This study, 2026).')
_b('ArgumentsAndOutput',
 'The chapter says to pass a list as the sole argument to run(), that the first string is the executable file name, that the other strings are the command line arguments and that the list is in effect the sys.argv of the launched program; it collects the output of ping with capture_output=True and text=True [S]. The Python documentation warns that shell=True can be a security hazard if the command includes unsanitized input and points to shlex.quote [PY][SHLEX].',
 "The arguments a child received were printed, output was captured as bytes and as text, the book's ping flags were run on Linux, and a list with shell=True was run on POSIX (This study, 2026).")
_b('ExitAndStopping',
 'The chapter says poll() returns None while a process runs and its exit code when it ends, and shows the code 0 [S]. The Python documentation says a negative returncode -N means the child was terminated by signal N on POSIX [PY][SIGNAL].',
 'Seven children were run to see the codes they return, and a child that handles SIGTERM was stopped with terminate() and with kill() (This study, 2026).')
_b('OpeningFilesWithDefaultApps',
 'The chapter opens a text file with start on Windows and open on macOS and Linux, through subprocess.run() with shell=True for start, and names pyperclip in its practice program and playsound3 for the sound [S]. The documentation of webbrowser adds the module for URLs and that of pyperclip lists the programs it needs on Linux [PY][PYPERCLIP].',
 'The open command was traced to its package on this Ubuntu machine, webbrowser was called without a browser, and pyperclip and playsound3 were imported in the newest version (This study, 2026).')
_b('OsSchedulers',
 "The Summary of the chapter says the operating system's scheduler saves writing clock-checking code, and the section Running Task Scheduler, launchd, and cron names the three programs [S]. A crontab line has five time fields and a command, and when both day fields are restricted the command runs when either matches [POSIX][CRON].",
 'A function that finds the next minute an entry matches was written and run, cron itself was run on this machine and recorded, a launchd property list was written with plistlib, and systemd-analyze normalised calendar expressions (This study, 2026).')
_b('InProcessScheduling',
 "The chapter's own way to wait for a date is a while loop that calls time.sleep(1) until datetime.now() reaches Halloween 2039 [S]. The standard library has the sched module with a priority queue of events, threading.Timer for one call after a delay and the asyncio loop methods call_later and call_at [PY][SCHED].",
 'Each was run with short delays or with a fake clock, and the third-party schedule 1.2.2 was installed and run (This study, 2026).')
_b('ListingsAsPrinted',
 "The chapter prints 29 listings, 20 of them interactive sessions, and the online materials ship three files for it [S]. The book's Windows listings, such as subprocess.run(['C:\\\\Windows\\\\notepad.exe', 'C:\\\\Users\\Al\\\\hello.txt']), are part of those listings [S].",
 "The listings were compiled, the 75 statements of the sessions were replayed in a pseudo-terminal in the author's zone, and the three shipped files were fetched and hashed (This study, 2026).")
_b('SuperStopwatch',
 'Project 14 asks for a stopwatch that prints the lap number, the total time and the lap time each time the user presses ENTER, with the instructions printed first and round(..., 2) on both times [S]. The practice program rewrites the output in columns with rjust and ljust and copies it to the clipboard with pyperclip [S].',
 'The stopwatch was assembled from its two steps and run in a pseudo-terminal, and the arithmetic and the columns were run on fixed readings (This study, 2026).')
_b('SimpleCountdown',
 'Project 15 counts down from 60, prints the time left, sleeps a second per number and then plays alarm.wav by opening it with start or open, with the Windows line commented out in the listing [S]. The sound file is at autbor.com [S].',
 'The program was assembled from its two steps and run for 60 seconds, the sound file was fetched, and the version served at autbor.com was compared with the printed one (This study, 2026).')
_b('PracticePrograms',
 'The chapter asks for a Friday the 13th finder in two forms: one that walks forward from the current date and one that works out when the next Friday the 13th falls, and answers seven questions in Appendix B [S][APPB]. The weekday() method returns 0 for Monday and the weekday for 13 is 4 for Friday [PY].',
 'The finders were run from a fixed date and the 400-year cycle was counted, and the three answers of Appendix B that involve code were executed (This study, 2026).')
# ---- the leaf concepts ----
_b('EpochZero',
 'The chapter defines the Unix epoch as January 1, 1970, at midnight, UTC, a standard reference time for many programming languages, and says time.time() returns the epoch timestamp as a float of the seconds since then [S]. The Python documentation says the epoch is the point where the time starts and that gmtime(0) shows it [PY].',
 'time.gmtime(0) gave 1970-01-01 00:00:00, calendar.timegm of that moment gave 0, datetime(1970, 1, 1, tzinfo=UTC).timestamp() gave 0.0, and type(time.time()) was float (This study, 2026).')
_b('PosixFormula',
 'The chapter does not say how a moment becomes a count of seconds, and POSIX gives the expression: tm_sec + tm_min*60 + tm_hour*3600 + tm_yday*86400 plus a term per year, with every day exactly 86400 seconds long [POSIX]. The Python documentation adds that leap seconds are not counted in the epoch timestamp [PY].',
 'The expression was written out and gave 1773813875 for 06:04:35 UTC on 18 March 2026, equal to calendar.timegm; it agreed for 29 February 2000; the second between 23:59:59 on 31 December 2016 and midnight was 1, and datetime(2016, 12, 31, 23, 59, 60) raised ValueError (This study, 2026).')
_b('FloatPrecision',
 'The chapter prints time.time() as 1773813875.3518236 and later calls round() on differences because the values have many digits after the decimal point [S]. The Python documentation says the return value is a float and that not all systems provide time with a better precision than 1 second [PY].',
 'math.ulp of that timestamp was 2.38e-07 seconds, below one microsecond, so a float holds a moment of 2026 to a fraction of a microsecond; time.time_ns() returned an int of 19 digits (This study, 2026).')
_b('ClockInfoTable',
 'The chapter uses only time.time() to measure time, and the Python documentation says time.monotonic() cannot go backwards and is not affected by system clock updates, while perf_counter() has the highest available resolution for short durations [S][PY][PEP418]. get_clock_info() reports the implementation and whether a clock is monotonic or adjustable [PY].',
 'On this Linux machine time was adjustable and not monotonic and read CLOCK_REALTIME, monotonic and perf_counter were monotonic, not adjustable and read CLOCK_MONOTONIC, and process_time read CLOCK_PROCESS_CPUTIME_ID; the difference of two monotonic readings across sleep(0.05) was at least 0.05 (This study, 2026).')
_b('SteppedWallClock',
 'The stopwatch subtracts one time.time() reading from another, which the chapter treats as elapsed time [S]. The documentation says time.time() may return a lower value than a previous call if the system clock has been set back between the two calls, which a monotonic clock cannot do [PY][PEP418].',
 'A fake wall clock reading 1000.0 and then 990.0 gave a difference of -10.0, a fake monotonic clock reading 50.0 and 60.0 gave 10.0, and get_clock_info reported time as adjustable and monotonic as not (This study, 2026).')
_b('RoundFunction',
 'The chapter uses round() on both times of the stopwatch and Practice Question 5 asks what it returns; Appendix B answers that it returns the closest integer to its argument [S][APPB]. The Python documentation says that with no digits round() returns an integer and that values are rounded to the closest multiple of 10 to the power minus ndigits, with ties going to the even choice [PY].',
 'round(2.5) was 2 and round(3.5) was 4, both ints, round(2.675, 2) was the float 2.67 because the stored value lies below 2.675, round(2.0, 2) was a float, and round(1773813875.3518236, 2) was 1773813875.35 (This study, 2026).')
_b('ProfilingByClock',
 "The chapter times calcProd() with time.time() and prints that it took 2.844162940979004 seconds, and the method follows Chapter 13 of the author's other book [S][BTBS]. The Python documentation of timeit says to use perf_counter for such timings and the int to string conversion limit of 4300 digits applies to the product [PY][STDTYPES].",
 'The loop gave the same integer as math.factorial(100000) and math.prod, with 1,516,705 bits and 456,574 digits, and str() of it raised ValueError under the limit of 4300; the run time on this machine was in the order of 2.3 to 2.6 s against 0.136 s for math.factorial (This study, 2026).')
_b('SleepFunction',
 'The chapter says time.sleep() will block until the number of seconds you passed has elapsed, and Practice Question 4 answers time.sleep(5) [S][APPB]. The Python documentation says the suspension time may be longer than requested by an arbitrary amount because of the scheduling of other activity [PY].',
 "sleep(0.2) returned None, took at least 0.2 s on a monotonic clock and under 0.5 s, sleep(-1) raised ValueError and sleep('1') raised TypeError (This study, 2026).")
_b('SleepAndSignals',
 'The chapter suggests that a program can print a message such as Press CTRL-C to cancel and handle KeyboardInterrupt around a sleep [S]. Since Python 3.5 a sleep is retried after a signal handler returns, and a handler that raises an exception ends it, a rule PEP 475 introduced [PY][PEP475].',
 'A handler for SIGALRM that returned left sleep(0.3) at least 0.3 s long, a handler that raised RuntimeError ended sleep(5) in under one second, and KeyboardInterrupt was a subclass of BaseException and not of Exception (This study, 2026).')
_b('PollingLoops',
 "The chapter's pause until Halloween 2039 is a while loop that calls time.sleep(1) between checks so that the computer does not waste CPU processing cycles by checking the time over and over as fast as possible [S]. The Python documentation of the time module counts CPU time with process_time [PY].",
 'A loop with sleep(1) used under 0.05 s of processor time in 1.2 s and a loop without it used more than 0.1 s in 0.3 s (This study, 2026).')
_b('SleepDrift',
 "The chapter's loop sleeps one second per round, and each round also takes the time of its own work [S]. A loop that sleeps a fixed interval after the work accumulates the work as drift, which a loop that sleeps until the next tick of a monotonic clock avoids [T].",
 'With a fake clock and 0.02 s of work, 3600 rounds of the fixed sleep reached the last start at 3670.98 s and the anchored loop at 3599.0 s (This study, 2026).')
_b('DatetimeObject',
 'The chapter makes a moment with datetime.datetime(2026, 10, 21, 16, 29, 0) and says the datetime function takes year, month, day, hour, minute and second, with hour, minute and second defaulting to 0 [S]. The Python documentation says the year, month and day arguments are required and that out-of-range values raise ValueError [PY].',
 'The fields read back as 2026, 10, 21, 16, 29, 0 and 0 microseconds, datetime(2026, 10) raised TypeError, month 13 and 30 February raised ValueError, and the moment was a Wednesday with weekday() equal to 2 (This study, 2026).')
_b('CurrentMoment',
 'The chapter calls datetime.datetime.now() for the current moment and datetime.datetime.fromtimestamp(time.time()) for the same moment from an epoch timestamp [S]. The documentation says now() returns the current local date and time and, with a tz argument, the time in that zone [PY].',
 'now() and fromtimestamp(time.time()) were within one second of each other, both were naive, and now(datetime.UTC) was aware with an offset of zero (This study, 2026).')
_b('DatetimeComparison',
 'The chapter compares halloween_2026 with oct_31_2026 and new_years_2027 with the operators ==, > and says a datetime later in time is greater [S]. The documentation says naive and aware values cannot be compared for order and that equality of naive and aware values is always false [PY].',
 'Two values of one moment were equal and not the same object, sorted() and max() used the order, and the difference between 31 October 2026 and 1 January 2027 was a timedelta of 62 days (This study, 2026).')
_b('WeekdayOfDate',
 'Practice Question 7 asks which day of the week 7 January 2019 was, and Appendix B answers with weekday() equal to 0, Monday [S][APPB]. The documentation says weekday() returns Monday as 0 and isoweekday() returns Monday as 1 [PY].',
 '7 January 2019 formatted as Monday, weekday() was 0, isoweekday() was 1, calendar.day_name agreed and isocalendar() gave week 2 (This study, 2026).')
_b('TimedeltaObject',
 'The chapter makes a timedelta of 11 days, 10 hours, 9 minutes and 8 seconds and shows its days, seconds and microseconds attributes as (11, 36548, 0), and says total_seconds() returns the duration in seconds [S]. The documentation says only days, seconds and microseconds are stored and are normalised, so the seconds are in the range 0 to 86399 [PY].',
 'The attributes were 11, 36548 and 0, total_seconds() was 986948.0, str() gave 11 days, 10:09:08, timedelta(seconds=-1) was days=-1, seconds=86399, and the resolution was 1 microsecond (This study, 2026).')
_b('NoMonthsOrYears',
 'The chapter says there is no month or year keyword argument because a month or year is a variable amount of time depending on the particular month or year [S]. The documentation lists the seven arguments and no larger unit [PY].',
 'timedelta(months=1) and timedelta(years=1) raised TypeError, 31 January plus 30 days was 2 March and plus 31 days 3 March, and February had 28 days in 2026 and 2027 and 29 in 2024 (This study, 2026).')
_b('DurationArithmetic',
 'The chapter adds thousand_days, a timedelta of 1000 days, to now and gets 28 August 2029, and says timedelta objects can be added to or subtracted from datetime objects [S]. The documentation lists the operations with another timedelta, an int or float, and a datetime [PY].',
 'A timedelta of 1 day and 12 hours doubled to 3 days, halved to 18 hours, divided by an hour to 36.0, divmod by 5 hours gave 7 and 1 hour, d * d and d + 1 raised TypeError, and 2 December 2026 plus 1000 days was a Tuesday (This study, 2026).')
_b('ThirtyYearsError',
 'The chapter subtracts about_thirty_years, timedelta(days=365 * 30), from 21 October 2026 and says it ignores leap years, and it prints 28 October 1996 [S]. The text before the example calls the module function datetime.delta(), which does not exist [S][PY].',
 'The 30 years before 21 October 2026 hold 7 leap days, so the real date is 21 October 1996 and the printed one is 7 days later; twice the span gave 5 November 1966, 15 days after the real 21 October 1966; datetime.delta raised AttributeError (This study, 2026).')
_b('DirectiveTable',
 'Table 19-1 lists the strftime directives %Y, %y, %m, %B, %b, %d, %j, %w, %A, %a, %H, %I, %M, %S, %p and %%, with a column for the meaning [S]. The documentation lists more directives and says some depend on the platform and the locale [PY].',
 'For 3 November 2026 at 16:29:07 every directive gave the text the table describes, %j was 307, %w was 2 for Tuesday, and over a week %w ran from 0 for Sunday to 6 for Saturday (This study, 2026).')
_b('StrftimeFormat',
 "The chapter calls oct_21st.strftime('%Y/%m/%d %H:%M:%S') and gets 2026/10/21 16:29:00, and also formats %I:%M %p and a custom text containing the directives [S]. The documentation says directives other than those of the C standard may differ between platforms [PY].",
 "The three formats gave 2026/10/21 16:29:00, 04:29 PM and October of '26; %-d, %e and %k worked on glibc; %f gave 000123 for 123 microseconds; %z and %Z were empty for a naive value and +0000 and UTC for an aware one, and %:z gave +00:00 on 3.14 (This study, 2026).")
_b('StrptimeParse',
 "The chapter calls datetime.datetime.strptime('October 21, 2026', '%B %d, %Y') and says the string must match the format exactly or it raises ValueError [S]. The documentation says strptime is a class method that parses a string by a format, and 3.14 added date.strptime and time.strptime [PY][WN314].",
 "The matching strings parsed, '2026-10-21' against '%Y/%m/%d' raised ValueError, '2026-1-5' parsed for %m and %d, leading and trailing spaces raised, a trailing Z needed %z, and both new strptime methods existed on 3.14.6 (This study, 2026).")
_b('TwoDigitYear',
 "Table 19-1 says %y is the year without century, '00' to '99' (1970 to 2069) [S]. The documentation says values 69 to 99 are mapped to 1969 to 1999 and values 0 to 68 to 2000 to 2068, following POSIX and ISO C [PY][POSIX].",
 "'68' parsed as 2068, '69' as 1969, '00' as 2000 and '99' as 1999; the book's examples '63' as 2063 and '73' as 1973 were right; formatting 1969 and 2069 both gave '69' (This study, 2026).")
_b('YearlessParsing',
 "The chapter's strptime examples all include a year [S]. The documentation says that parsing a day and a month without a year always uses 1900, which is not a leap year, so 29 February fails, and that the behaviour will change [PY][WN].",
 "strptime('02/29', '%m/%d') raised ValueError for day 29 in year 1900 and drew a DeprecationWarning under 3.14.6; '02/29;1984' with %Y parsed; '10/21' gave 1900-10-21 with no warning; Python 3.15.0b4 raised ValueError for %d without a year even for 10/21 (This study, 2026).")
_b('IsoFormats',
 'The chapter writes dates as 2026/10/21 and October 21, 2026 and does not mention the international standard [S]. ISO 8601 and RFC 3339 write 2026-10-21T16:29:07+00:00, and the documentation says fromisoformat accepts most ISO 8601 formats since 3.11 [PY][RFC3339][ISO].',
 'isoformat gave 2026-10-21T16:29:07.123456+00:00 and with timespec seconds dropped the fraction; fromisoformat read Z, the basic form 20261021T162907+0300 and 2026-W43-3; 21/10/2026 raised ValueError (This study, 2026).')
_b('NaiveVersusAware',
 "The chapter's datetime values carry no zone, and the book does not use the words naive or aware [S]. The documentation says an aware object can locate itself relative to other aware objects, a naive object cannot, and that comparing the two for order raises TypeError [PY].",
 'A naive and an aware value of 16:29 were not equal, comparing and subtracting them raised TypeError, 16:29 UTC and 19:29 in Istanbul compared equal with an offset of three hours, and replace(tzinfo=UTC) made the naive value equal to the aware one (This study, 2026).')
_b('UtcnowDeprecated',
 'The chapter uses datetime.datetime.now() and does not use utcnow(), which many older programs use for UTC [S]. Python 3.12 deprecated utcnow() and utcfromtimestamp() because they return naive values, and the documentation names now(UTC) and fromtimestamp(ts, UTC) as the replacements [PY][WN312].',
 'utcnow() returned a value with tzinfo None, both calls drew a DeprecationWarning that names the replacement, now(UTC) drew none, and in a process with TZ=Europe/Istanbul the timestamp of the naive utcnow() value was 3.0 hours less than the real one (This study, 2026).')
_b('ZoneInfoZones',
 "The chapter says nothing about zones beyond the author's own, and the zoneinfo module appeared in Python 3.9 with the data taken from the system or the tzdata package [S][PEP615]. The IANA database is the source of the zone rules and names [IANA].",
 'Los Angeles was -07:00 PDT on 1 July 2026 and -08:00 PST on 1 January; Istanbul was +03:00 in 2015, 2017 and 2026 on the data of tzdata 2026.5; with PYTHONTZPATH pointing nowhere and no site packages ZoneInfo raised ZoneInfoNotFoundError (This study, 2026).')
_b('FromTimestampZones',
 "The chapter calls datetime.datetime.fromtimestamp(1000000) and prints datetime.datetime(1970, 1, 12, 5, 46, 40), a reading that is the local clock of the author's zone [S]. The documentation says fromtimestamp without a tz gives the local date and time of the platform [PY].",
 'The same epoch second gave 13:46:40 in UTC, 05:46:40 in Los Angeles and 15:46:40 in Istanbul, which was UTC+02:00 in January 1970; an epoch second of 2026 printed as 21:40 UTC, 00:40 in Istanbul, 14:40 PDT and 03:10 IST; time.tzset() moved the clock of a running process (This study, 2026).')
_b('PstVersusPdt',
 'The chapter says it calls time.time() on March 17, 2026, at 11:04 PM Pacific Standard Time [S]. The United States was on daylight saving time from 8 March 2026, and the IANA data give the abbreviation PDT and the offset -07:00 for Los Angeles on that day [IANA].',
 '1773813875.35 seconds was 23:04:35 PDT on a Tuesday, the offset was -07:00 and dst() one hour; at 1:59 on 8 March the zone was PST and at 3:00 PDT; ctime of the same second gave 23:04:35 in Los Angeles, 06:04:35 in UTC and 09:04:35 in Istanbul (This study, 2026).')
_b('WallClockArithmetic',
 "The chapter's thousand-day and thirty-year examples use naive values, for which a day is 24 hours by definition [S]. For an aware value the documentation says arithmetic acts on the wall clock and ignores the change of offset, so it recommends converting to UTC to add real durations [PY].",
 'Noon on 7 March 2026 in New York plus one day was noon on 8 March at -04:00, the difference in UTC was 82800 seconds, and adding the day in UTC then converting gave 13:00 local; the subtraction in the zone said 1 day (This study, 2026).')
_b('GapAndFold',
 'The chapter does not meet local times that do not exist or exist twice, and PEP 495 added fold so that the second pass through an hour can be told from the first [S][PEP495]. The documentation says a time in the gap is invalid and that ambiguous times take fold=0 by default [PY].',
 '02:30 on 8 March 2026 in New York read back as 03:30 EDT after a trip through UTC; 01:30 on 1 November 2026 with fold=0 was 05:30 UTC and with fold=1 06:30 UTC, the two values compared equal and their difference in the zone was zero while in UTC it was one hour (This study, 2026).')
_b('Year2038',
 'The chapter counts seconds with a float and does not mention that C programs have counted them in 32 bits [S]. A signed 32-bit time_t overflows at 03:14:07 UTC on 19 January 2038, and Python on a 64-bit platform has no such limit [PY][UNIX2038].',
 '2**31 - 1 was 2038-01-19T03:14:07 UTC, 2**31 packed as unsigned and read as signed was -2147483648, which is 1901-12-13T20:45:52 UTC, the time_t of this machine had 8 bytes, and the last timestamp datetime accepts was 253402300799 (This study, 2026).')
_b('DatetimeRange',
 "The chapter's dates lie between 1970 and 2039, far from the limits of the type [S]. The documentation gives MINYEAR as 1 and MAXYEAR as 9999 and says date arithmetic past the ends raises OverflowError [PY].",
 "date.min was 0001-01-01 and date.max 9999-12-31, datetime.max plus one microsecond and date.min minus a day raised OverflowError ('date value out of range'), and the first of January of the year 1 is a Monday with ordinal 1 (This study, 2026).")
_b('GregorianCalendar',
 'The chapter uses dates from 1970 to 2039 and the Gregorian rules without naming them [S]. The documentation calls date an idealized naive date, assuming the current Gregorian calendar always was, and always will be, in effect [PY][GREG].',
 '5 October 1582 formatted as Tuesday, one day after 4 October by ordinal, though the countries that adopted the calendar went from 4 October to 15 October; 1900 and 2100 were not leap years, 2000 and 2024 were, and the years 1 to 9999 held 2424 leap years (This study, 2026).')
_b('RunWaits',
 "The chapter calls subprocess.run(['C:\\\\Windows\\\\System32\\\\calc.exe']) and shows CompletedProcess(args=['C:\\\\Windows\\\\System32\\\\calc.exe'], returncode=0), and says run() waits [S]. The documentation says run() waits for the command to complete and returns a CompletedProcess instance [PY].",
 "run(['sleep', '0.3']) took at least 0.3 s, printed as CompletedProcess(args=['sleep', '0.3'], returncode=0), and had stdout and stderr None; with capture_output=True and text=True the repr added stdout='hi\\n' and stderr='' (This study, 2026).")
_b('PopenNoWait',
 'The chapter says Popen returns a Popen object at once, that poll() returns None while the process runs and an exit code afterwards, and that wait() blocks until the process ends [S]. The documentation adds that wait(timeout) raises TimeoutExpired [PY].',
 "Popen(['sleep', '0.4']) came back in under 0.2 s, poll() gave None and then 0, a polling loop counted more than three rounds before the end, wait() returned 0, and wait(timeout=0.1) on a sleep of 2 s raised TimeoutExpired (This study, 2026).")
_b('CheckAndTimeout',
 "The chapter's runs all return 0 and it does not discuss failure of the launched program [S]. The documentation says check=True raises CalledProcessError for a non-zero code and that timeout kills the child and raises TimeoutExpired [PY].",
 'false with check=True raised CalledProcessError with status 1, sleep 5 with timeout 0.2 raised TimeoutExpired, a missing program raised FileNotFoundError, a directory raised PermissionError, and the exceptions derived from SubprocessError and OSError (This study, 2026).')
_b('ArgumentList',
 'The chapter says the first string of the list is the executable and the others are the arguments, and that the list is in effect the sys.argv of the launched program [S]. The documentation says that on POSIX with shell=False the list is the argument vector, so no splitting or expansion happens [PY][SHLEX].',
 "A child that printed sys.argv[1:] received 'my file.txt', 'a b' and '--x=1' as three items, a pattern *.txt arrived unexpanded, and shlex.split cut a command line with a quoted name into three words (This study, 2026).")
_b('CaptureOutput',
 "The chapter runs subprocess.run(['ping', '-n', '4', 'nostarch.com'], capture_output=True, text=True) and prints the Windows output of ping [S]. The documentation says capture_output is shorthand for stdout=PIPE and stderr=PIPE, that text=True gives str, and that it cannot be used with stdout [PY].",
 "Without text=True stdout was b'out\\n', with it 'out\\n', and capture_output with stdout= raised ValueError; ping -n 4 exited with 2 on Linux and ping -c 2 -W 2 127.0.0.1 exited with 0, 2 received and 0% packet loss (This study, 2026).")
_b('ShellTrueList',
 "The chapter runs subprocess.run(['start', 'hello.txt'], shell=True) and explains that the operating system knows the file associations [S]. The documentation says that on POSIX with shell=True and a sequence, the first item is the command string and any additional items are arguments to the shell itself [PY].",
 "On this machine ['echo', 'hi', 'there'] with shell=True printed an empty line, the string 'echo hi there' printed hi there, ['start', 'hello.txt'] exited with 127 and the message start: not found, and shutil.which('start') was None (This study, 2026).")
_b('ShellInjection',
 'The chapter builds no command from user input, and the documentation says shell=True can be a security hazard if the command includes unsanitized input from an untrusted source [S][PY]. shlex.quote returns a shell-escaped version of a string [SHLEX].',
 "A file name of 'x; echo INJECTED' made the shell print INJECTED on a second line, shlex.quote turned it into one word, and a list without a shell printed it as one argument (This study, 2026).")
_b('ExitCodes',
 'The chapter shows returncode=0 for each run and says poll() returns the exit code of a terminated process [S]. The documentation says a negative returncode -N means the child was terminated by signal N on POSIX [PY][SIGNAL].',
 "The codes were 0 for a normal end, 3 for sys.exit(3), 1 for an uncaught exception and for sys.exit('msg'), 7 for os._exit(263) because only eight bits are kept, -9 after SIGKILL and -15 after SIGTERM (This study, 2026).")
_b('TerminateVsKill',
 'The chapter does not stop a launched process, and the documentation says terminate() sends SIGTERM and kill() sends SIGKILL on POSIX [S][PY]. The signal documentation says SIGKILL cannot be caught or ignored [SIGNAL].',
 'A child with a SIGTERM handler printed that it was saving its work and exited with 0 after terminate(); the same child gave return code -9 and no output after kill(); signal.signal(SIGKILL, handler) raised OSError with errno 22 (This study, 2026).')
_b('OpenCommand',
 "The chapter says that on Windows the equivalent of double-clicking is the start command and that on macOS and Linux this is the open command, and its countdown comments pass 'open' for macOS and Linux [S]. The freedesktop project's tool for Linux is xdg-open, which opens a file in the user's preferred application [XDG].",
 "/usr/bin/open on this Ubuntu machine resolved to /usr/bin/xdg-open, put there by the postinst script of xdg-utils through update-alternatives; for a missing file it exited with 2; with no desktop session it could not open anything; hasattr(os, 'startfile') was False (This study, 2026).")
_b('Webbrowser',
 'The chapter suggests webbrowser.open() to open a website at the end of the countdown [S]. The documentation says open returns True if a browser was successfully launched and False otherwise [PY].',
 "On this machine webbrowser.open('file:///nonexistent') returned False, webbrowser.get() raised Error with the message could not locate runnable browser, and BROWSER was not set (This study, 2026).")
_b('ClipboardAndSound',
 'The Practice Program copies its output with pyperclip, which the chapter introduced in Chapter 8, and the chapter names playsound3 from Chapter 12 for sound files [S]. The Appendix A of the book pins playsound3==2.4.0, and PyPI shows 3.3.2 as the newest release [APPA][PYPI].',
 'With pyperclip 1.11.0 and no clipboard program copy() raised PyperclipException; playsound3 3.3.2 imported and exposed playsound, backends and PlaysoundException; the pinned 2.4.0 printed audio-system noise and returned None; nothing was heard (This study, 2026).')
_b('CronFields',
 'The chapter names cron as the Linux scheduler and gives no syntax [S]. A crontab line has the minute, hour, day of month, month and day of week fields and the command, and when both day fields are restricted the command runs when either matches the current time [POSIX][CRON].',
 "A matcher written to that rule found the next run of '30 9 * * 1-5' after 09:30 on Tuesday 13 October 2026 on Wednesday 14 October at 09:30, '*/15 * * * *' at 09:45, '0 0 13 * 5' on Friday 16 October and '0 0 29 2 *' on 29 February 2028; the function is the study's own and real cron was not asked about the day rule (This study, 2026).")
_b('CronEnvironment',
 'The chapter does not say what a job started by cron sees, and the Debian manual page says cron sets up some environment variables itself and runs commands with /bin/sh [S][CRON]. The manual page of the cron version Debian ships does not mention CRON_TZ [CRON].',
 "A Python job started by cron on this machine at the turn of a minute saw PATH=/usr/bin:/bin, the working directory /root, 6 environment variables, no terminal, sh as parent and a clock in UTC while the shell's TZ was Europe/Istanbul; a TZ=Asia/Kolkata line reached the job and set its clock to IST; the entries written under CRON_TZ lines fired by the clock of the cron daemon, not of the line (This study, 2026).")
_b('LaunchdPlist',
 'The chapter names launchd and no file format, and launchd reads jobs from property lists with a Label, ProgramArguments and StartCalendarInterval [S][APPLE]. The plistlib module reads and writes such files [PY].',
 'plistlib.dumps wrote a 501-byte XML plist with 5 keys for a job at 04:00 daily, loads read it back equal to the dictionary, and launchctl was not on this machine, so no job was loaded or run (This study, 2026).')
_b('SystemdCalendar',
 'The chapter does not mention systemd, which most Linux distributions use for timers; a timer unit has an OnCalendar expression such as Mon..Fri 09:00 [S][SYSTEMD]. systemd-analyze calendar normalises an expression and prints the next time it fires [SYSTEMD].',
 'Mon..Fri 09:00 became Mon..Fri *-*-* 09:00:00, daily became *-*-* 00:00:00 and weekly became Mon *-*-* 00:00:00; systemctl list-timers failed because PID 1 here is not systemd, so no timer was started (This study, 2026).')
_b('SchedModule',
 "The chapter's alternative to the operating system scheduler is its own loop with time.sleep(1) [S]. The sched module keeps events in a queue ordered by time then priority, and enter and enterabs add them, cancel removes one and run executes them [PY][SCHED].",
 'With a fake clock the events ran in the order now, two, five with priority 0, five and the clock ended at 5.0; an event cancelled before run() did not run, one in the past ran first, and cancelling an event that had run raised ValueError (This study, 2026).')
_b('TimerThread',
 'The chapter does not use threads, and threading.Timer is a Thread that calls a function once after an interval, with cancel() to stop it before it fires [S][PY]. A Timer is a subclass of Thread and is not a daemon unless set [PY].',
 'A Timer of 0.1 s had not fired right after start(), had after join(), a Timer of 5 s that was cancelled never fired, and the class derived from Thread with daemon False (This study, 2026).')
_b('AsyncioCallLater',
 'The chapter does not use asyncio, and the event loop methods call_later(delay, callback) and call_at(when, callback) schedule a callback [S][PY]. call_soon schedules it for the next iteration of the loop [PY].',
 'callbacks scheduled with call_later(0.2), call_later(0.1) and call_soon ran in the order soon, later 0.1, later 0.2 inside asyncio.run (This study, 2026).')
_b('ScheduleLibrary',
 "The chapter names no third-party scheduler, and the schedule package, version 1.2.2 on PyPI from 2024, runs jobs written as every().day.at('10:30').do(job) while a program keeps calling run_pending [S][PYPI]. It is not an operating system scheduler and stops with its process [PYPI].",
 'schedule 1.2.2 was installed, the first run of a daily job at 10:30 was set to 10:30:00, a job every 10 minutes was more than 590 seconds away, and the scheduler held 2 jobs (This study, 2026).')
_b('EnDashListings',
 "The chapter's listings write end_time – start_time and time.time() – last_time and oct_21st – about_thirty_years, and the text says to subtract [S]. The Python grammar has no use for the en dash U+2013, which the compiler reports as an invalid character [PY].",
 "The compiler refused the character in listings 2, 6 and 12 of the page, four dashes in all, with SyntaxError invalid character; the same expression with a minus sign compiled, an f-string with the dash raised too, and '–'.isidentifier() was False (This study, 2026).")
_b('ShippedFiles',
 'The online materials of the 3rd edition hold calcProd.py, stopwatch.py and simplecountdown.py for this chapter and no alarm.wav, hello.txt, prettifiedStopwatch.py or fridayThirteenth.py, and no document about the operating system schedulers [S][P02]. The download is a zip of 91 files [P02].',
 'stopwatch.py had two en dashes, CRLF line ends and a print without the f prefix, so it prints {lap_number} literally; calcProd.py looped to 99999, printed a digit count and had an en dash, and its repaired form raised ValueError at 4300 digits; simplecountdown.py matched the page apart from spacing, and the copy served at autbor.com differed (This study, 2026).')
_b('ReplayOfListings',
 "The chapter shows 20 interactive sessions, which a reader types into the shell and compares with the printed text [S]. A comparison of a book's outputs with a new run separates changes of Python from the clock and the platform of the author [T].",
 'Of 75 statements replayed as printed, 54 matched and 21 differed: 7 by the clock, 1 by the en dash and 13 because they launch Windows or macOS programs; with the dash repaired 55 matched, and in the zone of Istanbul 54 matched, the zone alone changing fromtimestamp(1000000) (This study, 2026).')
_b('LapArithmetic',
 'Project 14 computes lap_time as round(time.time() - last_time, 2) and total_time as round(time.time() - start_time, 2) and prints Lap #1: 3.56(3.56) [S]. The printed example in the Practice Program shows the same numbers in columns [S].',
 'Readings of 0, 3.56, 8.63, 17.68 and 19.11 gave laps 3.56, 5.07, 9.05 and 1.43; the print had no space before the bracket, 19.11 - 17.68 was 1.4299999999999997 before rounding, and round gave 1.43 (This study, 2026).')
_b('ColumnFormatting',
 'The Prettified Stopwatch asks for the lap number, total time and lap time lined up in columns with rjust() and ljust(), with the output Lap # 1:   3.56 (  3.56) [S]. The documentation of str says rjust pads on the left to a width and ljust on the right [PY].',
 "rjust(2) on the number and rjust(6) on the times gave the printed lines exactly, an f-string with :>2 and :>6 gave the same, str(2.0).ljust(6) was '2.0   ', and a float shows its trailing zero only through the format .2f (This study, 2026).")
_b('CountdownLoop',
 'Project 15 sets time_left = 60, prints it, sleeps one second and subtracts one in a while loop that runs while time_left is greater than 0 [S]. The loop sleeps a fixed second after the print and so ends a little later than 60 seconds [T].',
 'With a fake sleep, a countdown from 3 printed 3, 2 and 1, then Beep!, after 3.0 seconds of sleeping; the real program, run for 60 seconds, printed 60 to 1 (This study, 2026).')
_b('AlarmSound',
 'The chapter says to play the sound file by opening alarm.wav with the default application, and gives autbor.com/alarm.wav as the place of the file [S]. The short link redirects to the sound file at automatetheboringstuff.com [T].',
 'The link answered 302 with the address automatetheboringstuff.com/src/alarm.wav, the file had 582,952 bytes, 16 bits, two channels, 44.1 kHz and 3.30 seconds, and no sound could be played in the container (This study, 2026).')
_b('FridayForward',
 'The first practice program asks for a program that finds the next Friday the 13th, and the chapter hints at weekday() and a loop that adds a timedelta of one day [S]. weekday() returns 4 for Friday and the day of the month 13 is checked with .day [PY].',
 'From 13 October 2026 the next ten were 13 November 2026, 13 August 2027, 13 October 2028, 13 April 2029, 13 July 2029, 13 September 2030, 13 December 2030, 13 June 2031, 13 February 2032 and 13 August 2032, and every one formatted as Friday (This study, 2026).')
_b('FridayBackward',
 'The second practice program asks for the program run in the other direction, going back one day at a time [S]. The range of the date type ends at the year 1, where subtracting a day raises OverflowError [PY].',
 'Going back from 13 October 2026 found 3485 Friday the 13ths, the latest on 13 March 2026 and the earliest on 13 April of the year 1, then date arithmetic raised OverflowError at 1 January of the year 1, after 739901 days; 400 years hold 688 Friday the 13ths against 685 on a Monday (This study, 2026).')
_b('AppendixBAnswers',
 'Appendix B answers Question 3 with time.asctime(), Question 5 with the closest integer and Question 7 with weekday() equal to 0 [S][APPB]. The documentation says asctime() formats like ctime() but takes a time tuple, and with no argument uses localtime() [PY].',
 "asctime() equalled ctime() with no argument and for a given time, round(2.5) was 2 and round(2.5, 2) a float, so 'closest integer' is incomplete, and 7 January 2019 had weekday() 0 (This study, 2026).")

PUBS.sort(key=lambda p: p[0])
_CITE = {
 "S": "(Sweigart, 2025)", "APPA": "(Sweigart, 2025)", "APPB": "(Sweigart, 2025)", "BTBS": "(Sweigart, 2020)", "PYPERCLIP": "(Sweigart, 2026)",
 "PY": "(Python Software Foundation, 2026)", "WN": "(Python Software Foundation, 2026)", "WN312": "(Python Software Foundation, 2026)", "WN314": "(Python Software Foundation, 2026)",
 "STDTYPES": "(Python Software Foundation, 2026)", "SHLEX": "(Python Software Foundation, 2026)", "SIGNAL": "(Python Software Foundation, 2026)", "SCHED": "(Python Software Foundation, 2026)",
 "PEP418": "(Stinner, 2012)", "PEP475": "(Natali and Stinner, 2014)", "PEP495": "(Belopolsky and Peters, 2015)", "PEP615": "(Ganssle, 2020)",
 "POSIX": "(IEEE and The Open Group, 2024)", "RFC3339": "(Klyne and Newman, 2002)", "IANA": "(Internet Assigned Numbers Authority, 2026)",
 "CRON": "(Vixie and Debian, 2026)", "APPLE": "(Apple, 2026)", "SYSTEMD": "(Freedesktop.org, 2026)", "XDG": "(Freedesktop.org, 2026)",
 "PYPI": "(Python Package Index, 2026)", "UNIX2038": "(Wikipedia, 2026)", "GREG": "(Wikipedia, 2026)", "ISO": "(Wikipedia, 2026)",
 "P02": "(No Starch Press, 2025)", "T": "(This study, 2026)",
}
for _k in list(BODY):
    _t = BODY[_k]
    for _n, _v in _CITE.items():
        _t = _t.replace("[" + _n + "]", _v)
    BODY[_k] = _t.replace('"', "'")
