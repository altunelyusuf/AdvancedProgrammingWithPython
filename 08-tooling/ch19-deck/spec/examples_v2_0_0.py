"""Chapter 19 deck examples, version 2.0.0: the 18 code examples of the chapter 19 lecture deck (Keeping Time, Scheduling Tasks and Launching Programs).
One example per code slide, in slide order; the example order is the page-tab order of the chapter-code manifest. `groups` are the code boxes of a slide, each with the
explanation that stands beside it; the lines of all groups, in order, are the example's code. A code box holds at most 30 words (the '>>> ' prompt of each line counts one).
Nothing here depends on the clock or the zone of the machine: every moment is built from numbers, every zone is named, and a clock the program reads is either a
monotonic one compared with a bound or a stand-in the program moves itself (marked EMULATED on its slide). No example uses a lambda or a keyboard, none reads the network.
Nothing here carries a result; chapter_deck_build_v2_1_0.py runs the code and takes every printed result from the run."""
__version__ = "2.0.0"

EXAMPLES = [
    # ------------------------------------------------------------ part 1: time as a number
    dict(id="epoch", name="Epoch timestamp", title="Returning the epoch timestamp: the number behind a date", part=1, visual="epoch",
         concepts=["The time Module", "Returning the Epoch Timestamp", "time"],
         groups=[
             (["import calendar", "from datetime import datetime, UTC", "t = calendar.timegm((2026, 3, 18, 6, 4, 35))", "print('timestamp:', t)"],
              "timegm() turns a UTC date into the epoch count: seconds since 1 January 1970, 00:00 UTC."),
             (["print('zero:', datetime.fromtimestamp(0, UTC).isoformat())", "print('last:', datetime.fromtimestamp(2**31 - 1, UTC).isoformat())"],
              "Zero is the epoch. 2**31 - 1 is the last second a signed 32-bit counter can hold: the 2038 problem."),
             (["print('wrapped:', datetime.fromtimestamp(-2**31, UTC).isoformat())"],
              "One second later a 32-bit counter wraps to the most negative number: December 1901."),
         ]),
    dict(id="clocks", name="Which clock", title="Clocks and what each measures: time(), monotonic(), perf_counter()", part=1, visual="clocks",
         concepts=["The time Module", "time"],
         groups=[
             (["import time", "for name in ('time', 'monotonic', 'perf_counter'):", "    info = time.get_clock_info(name)", "    print(name, info.monotonic, info.adjustable)"],
              "get_clock_info() tells whether a clock only moves forward (monotonic) and whether the system can set it (adjustable)."),
             (["wall, mono = [1000.0, 990.0], [50.0, 60.0]", "print('wall clock set back 10 s:', wall[1] - wall[0])", "print('monotonic clock:', mono[1] - mono[0])"],
              "EMULATED: two lists stand in for clocks. When someone sets the wall clock back, the difference of two readings goes negative."),
             (["start = time.monotonic()", "time.sleep(0.2)", "print('lasted at least 0.2:', time.monotonic() - start >= 0.2)"],
              "To time a duration use a monotonic clock; the check compares with a bound, not with an exact number."),
         ]),
    dict(id="sleep", name="Pausing programs", title="Pausing programs: time.sleep() and what it does not promise", part=1, visual="sleep",
         concepts=["Pausing Programs", "time"],
         groups=[
             (["import time", "start = time.monotonic()", "result = time.sleep(0.2)", "print('returns', result, '| at least 0.2:', time.monotonic() - start >= 0.2)"],
              "sleep() pauses at least the time asked and returns None: it promises a minimum, not an exact time."),
             (["work, rounds = 0.02, 3600", "print('sleep after work:', round((rounds - 1) * (work + 1.0), 2))", "print('fixed tick:', round((rounds - 1) * 1.0, 2))"],
              "A loop that sleeps one second after its work adds the work to every round; a fixed tick does not."),
         ]),
    dict(id="stopwatch", name="Stopwatch laps", title="Project 14: a first stopwatch with laps", part=1, visual="stopwatch",
         concepts=["Step 1: Set Up the Program to Track Times", "Step 2: Track and Print Lap Times", "stopwatch.py", "Ideas for Similar Programs (stopwatch)"],
         groups=[
             (["now = [1000.0]", "def clock():", "    return now[0]", "start_time = last_time = clock()", "lap_number = 1"],
              "EMULATED: a list holds the time, so the user's key presses can be simulated. The real program calls time.time()."),
             (["for gap in (3.56, 5.07, 9.05, 1.43):", "    now[0] += gap", "    lap_time = round(clock() - last_time, 2)", "    total_time = round(clock() - start_time, 2)"],
              "Each press adds the gap to the clock. The lap time is the clock minus the last lap; the total is the clock minus the start."),
             (["    print(f'Lap #{lap_number}: {total_time} ({lap_time})')", "    lap_number += 1", "    last_time = clock()"],
              "Print the lap, count it, and remember when it ended."),
         ]),
    # ------------------------------------------------------------ part 2: dates and times of day
    dict(id="durations", name="Durations", title="datetime: dates, times and timedelta arithmetic", part=2, visual="durations",
         concepts=["The datetime Module", "Representing Duration", "Pausing Until a Specific Date", "datetime"],
         groups=[
             (["from datetime import datetime, timedelta", "d = timedelta(days=11, hours=10, minutes=9, seconds=8)", "print(d.days, d.seconds, d.total_seconds())"],
              "A timedelta stores days, seconds and microseconds, so 10 hours 9 minutes 8 seconds become 36548 seconds."),
             (["try:", "    timedelta(months=1)", "except TypeError:", "    print('TypeError: timedelta has no months')"],
              "There is no month or year: their lengths vary."),
             (["start = datetime(2026, 10, 21, 16, 29)", "back = start - timedelta(days=365 * 30)", "print(back.date(), start.replace(year=1996).date())"],
              "Thirty years of 365 days are 7 leap days short of thirty calendar years."),
         ]),
    dict(id="strftime", name="datetime to string", title="datetime to string: strftime() and its directives", part=2, visual="strftime",
         concepts=["Converting datetime Objects into Strings", "Table 19-1: strftime() directives"],
         groups=[
             (["from datetime import datetime", "dt = datetime(2026, 11, 3, 16, 29, 7)", "print(dt.strftime('%Y/%m/%d %H:%M:%S'))"],
              "strftime() writes a moment as text; each % directive stands for a part of it."),
             (["print(dt.strftime('%I:%M %p'))", "print(dt.strftime('%A, %B %d'))", "print(dt.strftime('%j %w'))"],
              "12-hour clock with AM or PM, the weekday and month names, and the day of the year with the weekday number."),
             (["print(dt.isoformat())", "print(datetime.fromisoformat('2026-11-03T16:29:07'))"],
              "isoformat() and fromisoformat() are the standard pair to store a moment as text and read it back."),
         ]),
    dict(id="strptime", name="String to datetime", title="String to datetime: strptime() and its errors", part=2, visual="strptime",
         concepts=["Converting Strings into datetime Objects"],
         groups=[
             (["from datetime import datetime", "print(datetime.strptime('October 21, 2026', '%B %d, %Y'))"],
              "strptime() reads text with a format; the format must match the text exactly."),
             (["for text in ('2026-10-21', 'Oct 21, 2026'):", "    try: datetime.strptime(text, '%B %d, %Y')", "    except ValueError as e: print('ValueError:', e)"],
              "A wrong separator, or Oct where %B wants October, gives a ValueError that quotes the text and the format."),
             (["for text in ('00', '26', '68', '69', '99'):", "    print(text, datetime.strptime(text, '%y').year)"],
              "A two-digit year reads 00 to 68 as 2000 to 2068 and 69 to 99 as 1969 to 1999."),
         ]),
    dict(id="zones", name="Time zones", title="Time zones with zoneinfo", part=2, visual="zones",
         concepts=["The datetime Module", "datetime"],
         groups=[
             (["from datetime import datetime, UTC", "from zoneinfo import ZoneInfo", "naive = datetime(2026, 10, 21, 16, 29)", "aware = naive.replace(tzinfo=UTC)", "print(naive == aware)"],
              "A naive moment has no zone and an aware one has. They are never equal."),
             (["try: naive - aware", "except TypeError as e: print('TypeError:', e)"],
              "Subtracting a naive from an aware moment is refused."),
             (["for zone in ('America/Los_Angeles', 'UTC', 'Europe/Istanbul'):", "    print(zone, datetime.fromtimestamp(1000000, ZoneInfo(zone)).isoformat())"],
              "One timestamp, three zones: the same instant is written with three local clocks."),
         ]),
    dict(id="dst", name="Daylight saving time", title="Daylight saving time: a day with 23 hours and an hour that happens twice", part=2, visual="dst",
         concepts=["The datetime Module", "datetime"],
         groups=[
             (["from datetime import datetime, timedelta, UTC", "from zoneinfo import ZoneInfo", "ny = ZoneInfo('America/New_York')", "x = datetime(2026, 3, 7, 12, tzinfo=ny)", "y = x + timedelta(days=1)"],
              "Adding one day to noon in New York on 7 March crosses the night the clocks go forward."),
             (["print('wall:', y - x)", "print('real:', y.astimezone(UTC) - x.astimezone(UTC))"],
              "On the wall clock one day passed; in real time only 23 hours did."),
             (["first = datetime(2026, 11, 1, 1, 30, tzinfo=ny)", "second = first.replace(fold=1)", "a, b = first.astimezone(UTC), second.astimezone(UTC)", "print(a.hour, b.hour, first == second)"],
              "On 1 November 01:30 happens twice; fold=1 picks the second. They print equal but are an hour apart."),
         ]),
    # ------------------------------------------------------------ part 3: launching programs
    dict(id="run", name="subprocess.run", title="subprocess.run(): launch a program and read its output", part=3, visual="run",
         concepts=["Launching Other Programs from Python", "Receiving Output Text from Launched Commands", "subprocess"],
         groups=[
             (["import subprocess, sys", "child = 'import sys; print(\"out\"); print(\"err\", file=sys.stderr)'", "command = [sys.executable, '-c', child]"],
              "The program to launch is a list: the program, then its arguments. Here the program is Python itself."),
             (["done = subprocess.run(command, capture_output=True)", "print(done.returncode, done.stdout, done.stderr)"],
              "run() waits for the program to end and returns a CompletedProcess. The output arrives as bytes."),
             (["done = subprocess.run(command, capture_output=True, text=True)", "print(type(done.stdout).__name__, repr(done.stdout))"],
              "text=True gives text instead of bytes."),
         ]),
    dict(id="popen", name="subprocess.Popen", title="subprocess.Popen(): start now, wait later", part=3, visual="popen",
         concepts=["Launching Other Programs from Python", "subprocess"],
         groups=[
             (["import subprocess", "p = subprocess.Popen(['sleep', '0.4'])", "print('poll():', p.poll())"],
              "Popen() returns at once. poll() answers None while the program is still running."),
             (["print('wait():', p.wait())", "print('poll():', p.poll())"],
              "wait() blocks until the program ends and returns its exit code; poll() then returns the same code."),
             (["for call in (['nosuch'], ['false']):", "    try:", "        subprocess.run(call, check=True)", "    except Exception as e:", "        print(type(e).__name__, e)"],
              "A missing program raises FileNotFoundError. With check=True a failing program raises CalledProcessError."),
         ]),
    dict(id="exits", name="Exit codes", title="Exit codes and signals", part=3, visual="exits",
         concepts=["Launching Other Programs from Python", "subprocess"],
         groups=[
             (["import subprocess, sys", "def code_of(source):", "    return subprocess.run([sys.executable, '-c', source], stderr=subprocess.DEVNULL).returncode"],
              "A small helper runs a Python program given as text and returns its exit code, hiding its error text."),
             (["kill = 'import os, signal; os.kill(os.getpid(), signal.SIG%s)'", "print(code_of('pass'), code_of('import sys; sys.exit(3)'), code_of('raise ValueError'))"],
              "0 means success; sys.exit(3) gives 3; an uncaught exception gives 1."),
             (["print(code_of(kill % 'KILL'), code_of(kill % 'TERM'))"],
              "A program ended by a signal returns the negative of the signal number: -9 for KILL and -15 for TERM."),
         ]),
    dict(id="shell", name="Shell safety", title="Shell safety: a list of arguments, not a string", part=3, visual="shell",
         concepts=["Passing Command Line Arguments to Processes", "Opening Files with Default Applications", "webbrowser", "hello.txt"],
         groups=[
             (["import subprocess, shlex", "def sh(args, **kw):", "    return subprocess.run(args, capture_output=True, text=True, **kw).stdout", "name = 'x; echo INJECTED'"],
              "A helper runs a command and returns its text. The file name contains a semicolon, as a hostile file name could."),
             (["print(repr(sh(f'echo opening {name}', shell=True)))", "print(repr(sh(f'echo opening {shlex.quote(name)}', shell=True)))"],
              "Built into a string for the shell, the name runs a second command. shlex.quote() makes it one harmless word."),
             (["print(repr(sh(['echo', 'opening', name])))"],
              "The safest way needs no quoting: pass a list, and the name stays one argument."),
         ]),
    # ------------------------------------------------------------ part 4: scheduling
    dict(id="sched", name="In-process scheduler", title="In-process scheduling: the sched module", part=4, visual="sched",
         concepts=["Running Task Scheduler, launchd, and cron"],
         groups=[
             (["import sched", "now, log = [0.0], []", "def clock(): return now[0]", "def advance(seconds): now[0] += seconds", "s = sched.scheduler(clock, advance)"],
              "EMULATED: a list holds the time, and advance() moves it instead of sleeping, so the run is instant."),
             (["jobs = ((5, 1, 'five'), (2, 1, 'two'), (5, 0, 'five-0'), (0, 9, 'now'))", "for delay, priority, name in jobs:", "    s.enter(delay, priority, log.append, (name,))"],
              "Each job has a delay, a priority and an action. enter() adds it to the list."),
             (["s.run()", "print(log, now[0])"],
              "run() takes the jobs soonest first; equal times go by priority, and the clock ends at 5."),
         ]),
    dict(id="cron", name="Cron fields", title="Cron fields: when does a job next run?", part=4, visual="cron",
         concepts=["Running Task Scheduler, launchd, and cron"],
         groups=[
             (["from datetime import datetime, timedelta", "def matches(text, value):", "    return text == '*' or str(value) in text.split(',')"],
              "A cron field is * (any) or a list of numbers. This small matcher knows only those two forms."),
             (["def next_run(fields, t):", "    while True:", "        t += timedelta(minutes=1)", "        now = (t.minute, t.hour, t.isoweekday() % 7)", "        if all(map(matches, fields, now)):", "            return t"],
              "Step forward a minute at a time until every field matches. Cron counts Sunday as 0."),
             (["start = datetime(2026, 10, 13, 9, 30)", "fmt = '%Y-%m-%d %H:%M %a'", "print(next_run(('30', '9', '1,2,3,4,5'), start).strftime(fmt))", "print(next_run(('0', '0', '5'), start).strftime(fmt))"],
              "'30 9 * * 1-5' is 09:30 on weekdays; '0 0 * * 5' is midnight on Fridays."),
         ]),
    # ------------------------------------------------------------ part 5: practice programs
    dict(id="countdown", name="Countdown timer", title="Project 15: a countdown timer", part=5, visual="countdown",
         concepts=["Step 1: Count Down", "Step 2: Play the Sound File", "Ideas for Similar Programs (countdown)", "simplecountdown.py", "playsound3", "alarm.wav"],
         groups=[
             (["now = [0.0]", "time_left = 5"],
              "EMULATED: a number stands in for the clock that time.sleep(1) would move; the real program sleeps one second per count."),
             (["while time_left > 0:", "    print(time_left, end=' ')", "    now[0] += 1", "    time_left = time_left - 1"],
              "Print the count, let one second pass, count down. The loop ends at 0."),
             (["print()", "print('counted', now[0], 'seconds; the alarm needs a sound card')"],
              "The real program then plays alarm.wav with playsound3; there is no sound card here."),
         ]),
    dict(id="pretty", name="Prettified stopwatch", title="Practice program: a prettified stopwatch", part=5, visual="pretty",
         concepts=["Prettified Stopwatch", "Practice Programs"],
         groups=[
             (["rows = [(1, 3.56, 3.56), (2, 8.63, 5.07), (3, 17.68, 9.05), (4, 19.11, 1.43)]"],
              "Four laps as (number, total time, lap time), the numbers of the first stopwatch."),
             (["for number, total, lap in rows:", "    print('Lap #' + str(number).rjust(2) + ': ' + str(total).rjust(6) + ' (' + str(lap).rjust(6) + ')')"],
              "rjust() pads on the left so the columns line up."),
         ]),
    dict(id="friday", name="Friday the 13th", title="Practice program: the Friday the 13th finder", part=5, visual="friday",
         concepts=["Friday the 13th Finder"],
         groups=[
             (["from datetime import date, timedelta", "day = date(2026, 10, 13)", "found = []"],
              "Start on a fixed day, so the result never changes."),
             (["while len(found) < 10:", "    if day.day == 13 and day.weekday() == 4:", "        found.append(day.isoformat())", "    day += timedelta(days=1)"],
              "Walk forward a day at a time; weekday() is 4 for Friday."),
             (["print(found[0], '...', found[-1])", "print(len(found), 'dates')"],
              "The first and the tenth Friday the 13th after that day."),
         ]),
]

BY_ID = {e["id"]: e for e in EXAMPLES}


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def code_text(ex):
    return "\n".join(code_lines(ex)) + "\n"
