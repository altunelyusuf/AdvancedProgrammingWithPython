"""Writes limits_v1_0_0.json, the chapter 19 page's 'Provenance & known limits' entries, from the records Phase A made
(live_observations_v1_0_0.json, interpreter_record_v1_0_0.json, third_party_record_v1_0_0.json), pywheels_v1_0_0.json, standin_v1_0_0.json and the
'Not executed' sentence of sen0414_ch19_rdodi_data_v1_0_6.py. Numbers are read from those files. Usage: limits_make_v1_0_0.py"""
__version__ = "1.0.0"
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(H, n)))
lv, ir, pw, so, tp = J("live_observations_v1_0_0.json"), J("interpreter_record_v1_0_0.json"), J("pywheels_v1_0_0.json"), J("standin_v1_0_0.json"), J("third_party_record_v1_0_0.json")
src = open(os.path.join(H, "..", "sen0414_ch19_rdodi_data_v1_0_6.py"), encoding="utf-8").read()
live = {i["what"]: i["saw"] for i in lv["items"]}
find = lambda start: next(v for k, v in live.items() if k.startswith(start))
m = re.search(r"Not executed, and said so where it comes up: (.*?)\.\s+The chapter's 75 interactive statements", src, re.S)
notexec = re.sub(r"\s+", " ", m.group(1)).strip()
pg = find("chapter 19 page: status"); mat = find("online materials of the 3rd edition: status")
cron = find("cron, for real: a crontab with the entry '* * * * *'")
meas = {}
for i in tp["items"]:
    for l in i["output"].split("\n"):
        mm = re.search(r"MEASURED (loop [\d.]+ s, math\.prod [\d.]+ s, math\.factorial [\d.]+ s)", l)
        if mm: meas["fact"] = mm.group(1)
        if l.startswith("MEASURED wall time of the run: 60.037"): meas["sleep"] = l[len("MEASURED "):]
assert len(meas) == 2, meas
rec = so["recorded"]
out = []
out.append("Python and libraries on this page: the examples run in your browser, in Python 3.13.2 with schedule 1.2.2, pyperclip 1.11.0, playsound3 3.3.2 and the time zone database tzdata 2026.5 (the versions the research ran, embedded as wheels), while the research ran Python 3.14.6 on Linux. Each concept example and each chapter example was run in the browser and compared with its recorded result.")
out.append("Recorded, not run: %d examples need something a browser's Python cannot give (another program, a shell, a thread, a real timer, the signals of an operating system, the process time zone, a system zone, a web browser program or the C library of Linux) or word an error, a warning or a method as Python 3.14 does and Python 3.13 does not, and one that takes about six seconds in a browser; each is shown with its output recorded under Python 3.14.6, labelled 'Recorded, not run on this page', with its reason: %s." % (len(rec), ", ".join(sorted(rec))))
out.append("Clock-dependent results are never shown as live: the examples that run use a fixed moment, a fixed zone or a stand-in clock (called EMULATED where the book's loop is run against it), and print values that do not depend on the day they are run. What the book's own statements print when they read the real clock (time.time(), time.ctime(), datetime.now()) differs from the book on every run, by design; the research recorded where each block differs.")
out.append("The four libraries: %s are embedded as the PyPI wheels, unchanged, and unpacked in the browser; their licences are %s (recorded in 03-materials/ch19/assets/ASSETS_PROVENANCE_v1_0_0.md). No file of the book's online materials (a zip of %s bytes) is on this page." % (", ".join(w["file"] for w in pw["wheels"]), ", ".join(sorted({w["licence"] for w in pw["wheels"]})), "{:,}".format(mat[1])))
out.append("NOT EXECUTED: " + notexec + ".")
out.append("MEASURED, single runs on the machine of the day, not results of a program on this page: %s; %s." % (meas["fact"], meas["sleep"]))
out.append("What the public sites answered on 2026-10-13 is in live_observations_v1_0_0.json: the chapter's page (status %d, %s bytes, equal to the digest in the book's ontology), the newest PyPI releases (tzdata 2026.5, playsound3 3.3.2, pyperclip 1.11.0) and the pages of the stories; cron 3.0pl1 was installed and run for real on the machine of the study (%s)." % (pg[0], "{:,}".format(pg[1]), "first record %s seconds after the crontab was installed" % cron["seconds from install to first record"]))
out.append("One program was run under %d interpreters (%s) with the same package versions; the %d items that differ between them are listed in interpreter_record_v1_0_0.json (for example the wording of date and time errors, date.strptime, which Python 3.14 added, and the warning for a month and day without a year). The book's Appendix A pins playsound3 2.4.0, and the chapter's statements were also replayed with that version." % (len(ir["interpreters"]), ", ".join(ir["interpreters"]), len(ir["differ"])))
json.dump({"_version": __version__, "limits": out}, open(os.path.join(H, "limits_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
for x in out: print("-", x[:200])
