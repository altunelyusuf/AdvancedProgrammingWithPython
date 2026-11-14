"""Presenter notes of the chapter 19 deck, v2.1.0. Full sentences that carry the lecture; 60 to 140 words on a content slide, at least 30 on a title, part or resources slide.
A code slide's notes say what to point at and what the result shows; every note leads into the next slide."""

NOTES_NEW = {
    "title": "Welcome to chapter 19. Today we learn how a program keeps time, how it waits, and how it starts other programs and runs jobs later. "
             "Time looks simple, yet it hides traps: clocks that can be set back, days with twenty-three hours, and calendars that skipped ten days. "
             "Every example in this deck runs on the chapter page, in the same order as the slides, so you can change a line and watch the result change. "
             "Where waiting would be slow, a stand-in clock moves instead, and the slide says so.",
    "route": "This is the route for the session. There are five parts: time as a number, dates and times of day, launching other programs, scheduling, and three practice programs. "
             "The table shows which slides belong to each part, how many code examples each part holds, and what you will run in it. "
             "If you are short of time, the ranges let you jump to the part you need. "
             "Notice that the code examples are the same eighteen that sit in the Slide code tab of the page, in this order. "
             "Next we look at the two questions that tie the whole chapter together.",
    "questions": "Two questions guide the chapter. The first asks how a program can measure, store and print a moment without being wrong about clocks, zones or calendars. "
                 "The second asks how a program can start other programs and run its own jobs later without a shell surprise. "
                 "Keep both in mind while we go through the parts, because every example answers a piece of one of them. "
                 "The arrows point to where the answers come back: the summary for the first question and the practice questions for the second. "
                 "Now we begin with the first part, where a moment becomes a number.",
    "divider1": "Part one is about time as a number. A timestamp is a count of seconds from an agreed starting point called the epoch. "
                "We will see that time() follows the wall clock, which a person can set back, while monotonic() only moves forward. "
                "We will see that sleep() promises to wait at least as long as asked, never exactly, and that a stopwatch must read one clock for every lap. "
                "Each of the four concepts on this slide has a one-line meaning beside it, and the table on the right lists the slides of the part. "
                "Start with the everyday pictures on the next slide.",
    "divider2": "Part two is about dates and times of day with the datetime module. A datetime holds a date and a time, and a timedelta holds a length of time. "
                "strftime writes a moment as text, and strptime reads text back, refusing anything that does not match the format. "
                "A time zone turns one moment into a clock reading, and because of daylight saving time a day can have twenty-three hours. "
                "The four concepts on this slide carry those ideas, and the table lists the slides. "
                "First, a picture from everyday life for the datetime module.",
    "divider3": "Part three is about launching other programs with the subprocess module. run starts a program, waits and gives you a result. Popen starts a program and returns at once, so you can do other work meanwhile. "
                "The exit code tells how the program ended: zero is success and anything else is a failure. "
                "Finally, a list of arguments is safer than one string given to a shell, because a string can carry a second command. "
                "Each concept below has a meaning line, and the table lists the slides of this part. Next, an everyday picture for launching programs.",
    "divider4": "Part four is about scheduling, which means doing something later or again and again. The sched module keeps a list of jobs ordered by time and then priority. "
                "A cron entry has five fields that say when a job runs, and we will write a small matcher for them. "
                "The system schedulers, Task Scheduler on Windows, launchd on macOS and cron on Linux, start your program for you so it does not have to stay in memory. "
                "The four concepts here are sched, priority, cron and the native tools. The next slide gives the everyday picture.",
    "divider5": "Part five has three small programs that bring the chapter together. A countdown timer counts down and then rings. A prettified stopwatch prints laps in neat columns. "
                "A Friday the 13th finder walks the calendar one day at a time and collects the dates. "
                "Each program uses calls from the earlier parts, so this is a chance to see them work together. "
                "Try to predict what each program prints before you look at the result. "
                "Start with the everyday picture of a kitchen timer on the next slide.",
    "A1": "Think of a kilometre-zero stone in a city square. Every distance on the road is counted from that stone, and in the same way every timestamp is counted from the epoch. "
          "The timestamp is the distance, and a stopwatch such as perf_counter is a runner's watch that only measures how long a run took. "
          "Sleeping is like telling a friend you will wake them after at least an hour: it may be later, never sooner. "
          "A stopwatch must use one clock for every lap, otherwise the laps do not add up. "
          "The table maps each chapter concept to a picture like this. Next comes a true story about why the epoch is 1970.",
    "A2": "A boarding pass is a good picture for the datetime module. It shows a date, a time and the city whose clock the time belongs to. "
          "The flight's length is a duration, which is a timedelta, not a date. "
          "Printing the pass in the format the airport wants is strftime, and reading a handwritten date back is strptime, which refuses it when the format is wrong. "
          "Notice that a pass without a city would be ambiguous, which is exactly the problem of a naive datetime. "
          "The table lists the other concepts with their pictures. Next is the story of the ten days that did not happen.",
    "A3": "Imagine asking a colleague to do a job and bring back the result. That is run: you wait, and you get the answer. "
          "Popen is handing the job over and carrying on with your own work, then asking later whether it is finished. "
          "The exit code is the colleague's reply, zero for all went well and anything else for a problem. "
          "A list of items is safer than a spoken sentence, because a sentence can be misheard as an extra instruction, and that is the shell problem. "
          "The table lists the rest of the concepts. Now we look at the next part.",
    "A4": "A caretaker who checks a list every minute and starts whatever is due is cron. You tell the caretaker once, and the job comes back at the set times. "
          "A repeating alarm clock is a schedule, and an alarm with a priority is a job ordered in sched. "
          "The small program calcProd.py is a job the caretaker could run, and pyperclip is a shared clipboard that every program in the building can read and write. "
          "The table maps the remaining concepts. Next is the story of how cron once woke every minute at Purdue.",
    "A5": "A kitchen timer counts down and rings, which is the countdown project. A stopwatch counts up and notes laps, which is the prettified stopwatch. "
          "Turning the pages of a calendar one day at a time until you find a Friday the 13th is the third project. "
          "Each project is small, but each one depends on a call from an earlier part: sleep, monotonic or perf_counter, and timedelta. "
          "As you read the next slides, say aloud which earlier call each line uses. "
          "The first practice program is the countdown timer.",
    "epoch": "Point at the first line that builds a timestamp: calendar.timegm turns a date into the number of seconds since the first of January 1970 in UTC. "
             "The result table shows second zero is the epoch itself, printed as midnight on the first of January 1970. "
             "Then look at the number two to the power thirty-one minus one: it is the last second that a signed thirty-two-bit counter can hold, which prints as January 2038. "
             "One second later the counter wraps to the most negative value and reads as December 1901. "
             "Next we compare the clocks Python gives us.",
    "clocks": "Point at the loop that asks three clocks about themselves. get_clock_info tells whether a clock only moves forward, which is monotonic, and whether someone can set it, which is adjustable. "
              "The table shows time() can be set by hand and can go back, while monotonic() and perf_counter() never go back. "
              "The red and green boxes use stand-in numbers: setting the wall clock back ten seconds makes the difference negative, and the monotonic clock still shows ten. "
              "So use monotonic() to measure how long, and time() to learn what time it is. Next is the sleep function.",
    "sleep": "Point at the arithmetic version of the loop: sleeping one second after each piece of work lets the small delays add up. "
             "The chart compares the total after three thousand six hundred rounds, about 3671 seconds, against a plan of 3599 seconds that sleeps only until the next tick. "
             "The first drifts late by the time the work itself takes, while a fixed tick does not drift. "
             "Remember also that sleep returns None and promises at least the time asked, never less. "
             "The real program would wait; this one uses numbers so it runs at once. Next, the stopwatch.",
    "stopwatch": "Point at the line that subtracts the last lap from the clock now: that is a lap, and the clock now minus the start is the total. "
                 "A stand-in clock moves by given gaps, so the laps come out exact and the page can show them without waiting. "
                 "The table lists each lap and the total. The real program waits for the Enter key and reads perf_counter at each press. "
                 "Notice that every reading comes from one clock, which is what keeps the laps consistent. "
                 "This finishes part one. Next we move to dates and times of day.",
    "durations": "Point at the timedelta built from days, hours, minutes and seconds. It stores days, seconds and microseconds only, so there is no month or year, because their lengths vary. "
                 "The table shows that days and seconds are the parts and total_seconds is the whole. "
                 "The red row shows that asking for months raises a TypeError. "
                 "The last example subtracts thirty years counted as 365 days each and lands a week away from the same date in 1996, because leap days were missed. "
                 "So use calendar-aware tools when you mean years. Next, writing a datetime as text.",
    "strftime": "Point at the string of directives in the first call. Each percent code stands for a part of the moment: Y is the year, m the month, d the day, H the hour and M the minute. "
                "The second group shows the twelve-hour clock with AM and PM, the names of the weekday and the month, and the day of the year. "
                "The tables show what each call printed. isoformat is the standard text form, and fromisoformat reads it back unchanged. "
                "Keep a list of directives nearby, since nobody remembers them all. Next we do the opposite: reading text.",
    "strptime": "Point at the format given to strptime: it has to match the text exactly. The first table shows the good text becoming a datetime, "
                "while a date with the wrong separator and a date with Oct where B expects October both raise a ValueError. "
                "The second table is the two-digit year rule: sixty-nine to ninety-nine become 1969 to 1999, and zero to sixty-eight become 2000 to 2068. "
                "Catching ValueError lets a program report bad input instead of stopping. "
                "Next, a moment with a time zone.",
    "zones": "Point at the comparison of a naive and an aware moment: the equality is False, and subtracting them raises a TypeError, because one has no zone. "
             "The third example turns one timestamp, second one million of the epoch, into three local clock readings with ZoneInfo. "
             "The right table shows the same instant written in Los Angeles, UTC and Istanbul. "
             "The lesson is to name the zone whenever a moment leaves your program. "
             "Next, the day that has twenty-three hours.",
    "dst": "Point at the one-day addition: noon in New York on 7 March plus one day is noon the next day on the wall clock, yet the real difference is twenty-three hours. "
           "The left chart shows twenty-four wall hours against twenty-three real ones. "
           "The second part is the autumn change, when 01:30 happens twice. The fold value tells which one you mean, and the right chart shows the two readings are one hour apart in UTC. "
           "Yet the comparison of the two reads True. So compare moments in UTC. Part two ends here.",
    "run": "Point at the call to run: it starts the child program, waits and returns a result object. "
           "The table shows that capture_output collects what the child printed, text=True gives strings instead of bytes, and returncode zero means success. "
           "The child here is Python itself, so the example runs on any machine and in the browser page, where a stand-in plays the child. "
           "Notice that the parent only continues after the child ends. "
           "Next, the call that does not wait.",
    "popen": "Point at the Popen call, which starts the program and returns at once. poll gives None while the child is still running, and wait blocks until it ends and returns the exit code. "
             "The flow shows the child started at once, the wait that blocks, and the exit code at the end. "
             "Two errors are worth knowing: a missing program raises FileNotFoundError, and check equals True makes run raise CalledProcessError for a non-zero exit code. "
             "In the browser page the child is an honest stand-in. Next, what the exit codes mean.",
    "exits": "Point at the exit code of each child. Zero means success and any other number a failure. A child that ends with an uncaught exception exits with one. "
             "On Linux and macOS a negative return code means a signal ended the child: minus nine is KILL and minus fifteen is TERM. "
             "The table lists each case with its code, so read the code before you assume the job worked. "
             "A program that ignores the exit code of the program it launched can carry on with a broken result. "
             "Next, the shell and why it needs care.",
    "shell": "Point at the string with a semicolon: given to a shell, it runs a second command, which is how shell injection works. "
             "shlex.quote protects a single value by wrapping it safely, and the safest form is a list of arguments with no shell, where nothing is read as a command. "
             "The table compares three calls: the f-string runs two commands and prints the injected word, while the quoted version and the list of arguments run one harmless command. "
             "In the browser page the shell is a stand-in that understands echo only, and the slide says so. "
             "Next, opening a file in its default program.",
    "compare_open": "This table compares ways to open a file in its default program. webbrowser.open works on every system and is the one you can rely on. "
                    "os.startfile is only available on Windows. On macOS the program open does the job, and on Linux the program xdg-open does it, and you launch both with subprocess. "
                    "These are not run here, because a machine without a screen has no default application to open. "
                    "Remember that the right answer depends on the operating system, so a portable program checks first. "
                    "Part three ends here. Next we move to scheduling.",
    "compare_native": "This table compares the scheduler built into each operating system. Task Scheduler is on Windows, launchd on macOS and cron on Linux. "
                      "Each starts your program at set times, so the program does not have to wait in memory, and each has its own format for saying when. "
                      "Your Python script does not change; only the entry that starts it does. "
                      "Read the cron row closely, since the next slide shows how its five fields are read. "
                      "Part four closes with this slide, and then we move to the practice programs.",
    "sched": "Point at the jobs added with enter: each has a delay, a priority and an action. "
             "The sched module keeps them in order of time, and where times are equal, the lower priority number goes first. "
             "The stand-in clock is advanced instead of sleeping, so run finishes at once and the log shows the order. "
             "The diagram reads the log from left to right, and the clock ends at five seconds. "
             "The two jobs due at five seconds show priority at work. Next, the five cron fields.",
    "cron": "Point at the list of five fields: minute, hour, day of the month, month and day of the week. "
            "The small matcher here knows only a star and lists of numbers, and it counts Sunday as zero. "
            "It steps one minute at a time from a start until every field matches the clock, which gives the next run. "
            "The result shows the next run for two schedules, one on a Wednesday morning and one at midnight on a Friday. "
            "Real cron has more syntax, and the manual lists it. Next, how the native schedulers look.",
    "countdown": "Point at the loop that counts down from the start number: it prints each value and then waits one step. "
                 "In this run a number stands in for the clock, so the loop finishes at once. "
                 "The real program sleeps one second per count and then calls playsound3 for the alarm, which needs a sound file and a speaker. "
                 "Notice that the countdown is a loop plus a pause plus a final action, the same shape as many small tools. "
                 "Next, a stopwatch with neat columns.",
    "pretty": "Point at rjust, which pads each number on the left to a fixed width so the columns line up. "
              "The laps are the same as in the first stopwatch, only printed in neat columns. "
              "The table shows the printed lines, and the alignment is the whole point of this example. "
              "A small change in the print line, not in the logic, makes the output readable. "
              "Next, the last practice program.",
    "friday": "Point at the loop that steps one day at a time from a start date with a timedelta. "
              "A date is a Friday the 13th when its day is thirteen and its weekday is four, because Monday is zero. "
              "The program collects ten dates, from 13 November 2026 to 13 August 2032, and the table lists all ten in two rows. "
              "Stepping one day at a time is simple and fast enough for six years. "
              "Next, a short practice list.",
    "practice": "These are the practice questions. Predict the answer first, then run what you can on the chapter page and compare. "
                "Each question points back to the part where the idea was shown, so you can look up the slide if you are stuck. "
                "Pay special attention to the questions about zones, exit codes and the shell, since those are where real programs go wrong. "
                "Work in pairs if you can, and explain your answer in one sentence. "
                "Next comes the summary of the chapter.",
    "summary": "Five sentences to remember. A timestamp counts seconds from the epoch. The datetime module holds dates and durations. A moment needs a zone to be exact. "
               "subprocess works best with a list of arguments and an exit code you read. A scheduler starts your program for you. "
               "Look back at the two questions from the start: the first is answered by the first three sentences, the second by the last two. "
               "The last slide has the links to read next.",
    "resources": "These are the links to read next. The chapter is the first one, then the documentation of the time, datetime, zoneinfo and subprocess modules. "
                 "The POSIX definition of seconds since the epoch settles what counts as a second, and the crontab manual lists every cron field. "
                 "The two package pages show the schedule and tzdata projects, and the Wikipedia pages are the stories we told. "
                 "Choose one link that matches your weakest part and read it this week.",
}

STORY_NOTES_NEW = {
    "epoch": "The Unix engineers at Bell Labs first counted time in sixtieths of a second from 1971, then from 1972, and only later settled on seconds from 1970. "
             "The reason is simple: sixtieths of a second in a thirty-two-bit counter last about two and a third years, so the unit had to become seconds. "
             "The picture is a DEC PDP-11 in the Computer History Museum, the family of machines Unix ran on, not a page of the manual. "
             "The lesson is that an epoch is a convention engineers chose, not a law of nature. "
             "Open the link to read the full history. Next, what happens when that counter runs out.",
    "y2038": "A signed thirty-two-bit counter of seconds runs out at 03:14:07 UTC on 19 January 2038, and the next second wraps to December 1901. "
             "The picture is a drawing of that wrap, since no free photograph of the event exists. "
             "Systems that store a timestamp in thirty-two bits, such as old file formats and embedded devices, are the ones at risk, while modern systems use sixty-four bits. "
             "The lesson is to know how many bits your timestamp has. "
             "Open the link for the full story. Next, ten days that did not happen.",
    "gregorian": "In October 1582, after Thursday 4 October came Friday 15 October, because Pope Gregory XIII's reform removed ten days to bring Easter back to its season. "
                 "The picture is a calendar page of October 1582 with those days missing. "
                 "Python's date type is proleptic, meaning it applies today's calendar backwards, so it does have a 10 October 1582 and calls it a Tuesday. "
                 "The lesson is that before 1582 Python dates are not the dates people used at the time. "
                 "Follow the link to read more. Next, the strptime and strftime pair.",
    "leap": "Twenty-seven leap seconds were added between 1972 and 2016 to keep civil time near the Earth's rotation, which is not steady. "
            "POSIX time skips them, as every day has exactly 86400 seconds, so the last second of a leap day has no timestamp of its own. "
            "The picture shows the cesium of an atomic clock, the part that keeps the second, not a leap second itself, and the slide says so. "
            "The lesson is that epoch seconds are not the same as the SI seconds counted by atomic clocks. "
            "Open the link for the list. Next, why zones are a data problem.",
    "tzdb": "The rules for time zones and daylight saving are data that volunteers maintain, and in 2011 a lawsuit led to the shutdown of the database for a time. "
            "The picture is a world map of the standard time zones, which the database describes the rules of, not the database itself. "
            "Because governments change the rules, often at short notice, the data needs updating, and Python reads it from the system or from the tzdata package. "
            "The lesson is to keep tzdata up to date. "
            "Open the link to read the story. Next, how cron started jobs.",
    "cron": "Version 7 cron woke every minute and read its table of jobs. At Purdue a graduate student, Robert Brown, read the paper of Franta and Maly and wrote a version with an event list that sleeps until the next job. "
            "The reason was that waking every minute used resources and overloaded a time-shared VAX with a hundred users. "
            "The picture is a VAX 11/780 in a museum, the kind of machine of the story, not the Purdue one. "
            "The lesson is that a scheduler is a daemon, and the job it starts does not inherit your shell. "
            "Open the link to read more. Next, the sched module.",
}
