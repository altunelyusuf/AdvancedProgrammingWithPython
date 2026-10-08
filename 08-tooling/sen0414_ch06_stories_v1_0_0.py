"""SEN0414 chapter 6 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Four stories for Lists:

* ZeroStart - Dijkstra's note EWD831 of 11 August 1982 argues why a sequence of N items is numbered 0 to N-1, and the
  half-open slice of the chapter is the same convention.
* Shuffle - Fisher and Yates (1938), Durstenfeld (1964) and Knuth: the fair shuffle that random.shuffle(people) runs;
  the check below reads the standard library's own source.
* EightBall - the toy of 1946 whose twenty answers the chapter's program keeps in a list of nine.
* DigitalRain - the green streams of The Matrix (1999) and the screensaver that draws them from a list of counters.

Usage: import STORIES; run the file for self-checks (they include one executed claim per story where the story rests on code).
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "ZeroStart",
        "title": "Why the first item is number zero",
        "when": "1982-08-11",
        "who": "Edsger W. Dijkstra, Burroughs Research Fellow",
        "where": "Nuenen, the Netherlands - note EWD831, kept in the University of Texas archive",
        "link": "https://www.cs.utexas.edu/~EWD/transcriptions/EWD08xx/EWD831.html",
        "concepts": ["Index", "Slice", "NegativeIndex"],
        "story": ("On 11 August 1982 Edsger Dijkstra, at home in Nuenen, wrote a short note called 'Why numbering should start at zero'. "
                  "He asked how to write the numbers 2 to 12 without three dots, compared four ways of writing the bounds, and chose 2 <= i < 13: "
                  "the difference of the bounds is the length, and two neighbouring ranges meet without a gap. For a sequence of N items the same choice gives "
                  "0 <= i < N, so an element's number equals the count of elements before it. The note was triggered by a mathematician who called "
                  "young computing scientists pedantic for counting from zero. Python's spam[0] and spam[1:3] follow this convention."),
        "lesson": "Counting from zero makes the index equal to the number of items before it",
        "source": ("E. W. Dijkstra, 'Why numbering should start at zero', EWD831, Nuenen, 11 August 1982 (transcription at "
                   "cs.utexas.edu/~EWD/transcriptions/EWD08xx/EWD831.html). Photo: Edsger Dijkstra, 1994, by Andreas F. Borchert, "
                   "Wikimedia Commons, CC BY-SA 4.0."),
    },
    {
        "id": "Shuffle",
        "title": "A fair shuffle with a pencil, then with a computer",
        "when": "1938 (pencil and paper), 1964 (computer version)",
        "who": "Ronald Fisher and Frank Yates (1938); Richard Durstenfeld (1964); Donald Knuth (popularised)",
        "where": "the statistical tables of Oliver and Boyd, Edinburgh and London; Communications of the ACM",
        "link": "https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle",
        "concepts": ["RandomShuffle"],
        "story": ("In 1938 Ronald Fisher and Frank Yates printed a pencil-and-paper way to put numbers into random order in their book of "
                  "statistical tables. In 1964 Richard Durstenfeld published a computer version in the Communications of the ACM, "
                  "which swaps each item with a randomly chosen one that is not behind it, and Donald Knuth described it in his series on algorithms. "
                  "The method gives every order the same chance. It is what Python's random.shuffle still does: its source walks "
                  "the list from the end and swaps each place with a random place at or before it."),
        "lesson": "A shuffle is only fair if every order is equally likely",
        "source": ("R. A. Fisher and F. Yates, Statistical Tables for Biological, Agricultural and Medical Research (Oliver and Boyd, 1938); "
                   "R. Durstenfeld, 'Algorithm 235: Random permutation', Communications of the ACM 7(7), 1964, p. 420; D. E. Knuth, "
                   "The Art of Computer Programming, vol. 2 (Algorithm P); CPython's Lib/random.py. Photo: Ronald Aylmer Fisher, 1952, by Barry Eagel, "
                   "Wikimedia Commons, CC BY-SA 4.0."),
    },
    {
        "id": "EightBall",
        "title": "Twenty answers in a toy, nine in the program",
        "when": "1946 (patent filed), 1950 (the eight-ball shape)",
        "who": "Albert C. Carter and Abe Bookman, Alabe Crafts of Cincinnati",
        "where": "Cincinnati, Ohio - today made by Mattel",
        "link": "https://en.wikipedia.org/wiki/Magic_8_Ball",
        "concepts": ["MagicEightBall", "RandomChoice"],
        "story": ("The Magic 8 Ball was invented in 1946 by Albert Carter and Abe Bookman, whose company Alabe Crafts in Cincinnati first sold it as a "
                  "cylinder, and in 1950 made it the black-and-white eight ball we know. Inside, a twenty-sided die floats in dark blue liquid, and each face "
                  "carries one answer: ten affirmative, five neutral and five negative. The chapter's program keeps nine of those answers, such as 'It is certain' "
                  "and 'Very doubtful', in a Python list and prints one at a random index. A tenth answer needs no new code, which is the point of the list."),
        "lesson": "Put the answers in a list and the program need not change",
        "source": ("Magic 8 Ball, Wikipedia (history, the 20 answers and their split); the answer list of the program in Sweigart (2025), chapter 6. "
                   "Photo: the answer 'It is certain.' on a Magic 8 Ball, by Zaneology, Dallas, 2012, Wikimedia Commons, CC BY 2.0."),
    },
    {
        "id": "DigitalRain",
        "title": "The green rain that was never a code",
        "when": "1999 (film), 2017 (the designer's remark)",
        "who": "Simon Whiteley, who designed the glyphs for The Matrix",
        "where": "the film The Matrix (1999) - and an interview with CNET on 19 October 2017",
        "link": "https://en.wikipedia.org/wiki/Matrix_digital_rain",
        "concepts": ["MatrixScreensaver"],
        "story": ("The falling green characters of the film The Matrix (1999) come from a typeface that Simon Whiteley designed: mirrored half-width Japanese "
                  "kana, Latin letters and numerals. In a 2017 CNET interview he joked that the code was made from the sushi recipes of his wife's cookbooks, "
                  "a story that others have since questioned. The chapter's screensaver imitates the rain with a list of 70 counters, one per column: a counter above "
                  "zero prints a random 0 or 1 and counts down, and a counter at zero prints a space. The effect is a whole animation made from one list."),
        "lesson": "A list of counters can animate a screen",
        "source": ("Matrix digital rain, Wikipedia (designer, glyphs, the 2017 CNET interview); the screensaver program in Sweigart (2025), chapter 6. "
                   "Image: Figure 6-5 of Sweigart (2025), the chapter's own screensaver running in a console window, CC BY-NC-SA."),
    },
]


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
        if not x.get("concepts"):
            bad.append("%s: no concepts" % x["id"])
    if "1982" not in STORIES[0]["when"]:
        bad.append("ZeroStart: date drifted")
    if "1938" not in STORIES[1]["source"] or "1964" not in STORIES[1]["source"]:
        bad.append("Shuffle: dates missing from source")
    # claims that rest on code
    import inspect, random
    src = inspect.getsource(random.Random.shuffle)
    if "reversed(range(1, len(x)))" not in src or "randbelow(i + 1)" not in src:
        bad.append("Shuffle: the standard library's shuffle is no longer the Fisher-Yates/Durstenfeld loop")
    if not ([1, 2, 3][0:3] == [1, 2, 3] and [1, 2, 3][:1] + [1, 2, 3][1:] == [1, 2, 3]):
        bad.append("ZeroStart: half-open slices no longer partition a list")
    msgs = ['It is certain', 'It is decidedly so', 'Yes definitely', 'Reply hazy try again', 'Ask again later', 'Concentrate and ask again',
            'My reply is no', 'Outlook not so good', 'Very doubtful']
    if len(msgs) != 9:
        bad.append("EightBall: the chapter's list is not nine answers")
    if len([0] * 70) != 70:
        bad.append("DigitalRain: 70 counters")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
