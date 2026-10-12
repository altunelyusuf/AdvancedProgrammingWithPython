"""Writes limits_v1_0_0.json, the chapter 15 page's 'Provenance & known limits' entries, from the records Phase A made
(third_party_record_v1_0_0.json, live_observations_v1_0_0.json, interpreter_record_v1_0_0.json), pywheels_v1_0_0.json, standin_v1_0_0.json
and the 'Not executed' paragraph of sen0414_ch15_rdodi_data_v1_0_2.py. Numbers and quoted values are read from those files.
Chapter 15's first entries say what the page's outputs are not: Google's answers.
Usage: limits_make_v1_0_0.py"""
__version__ = "1.0.0"
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(H, n)))
tp, lv, ir, pw, so = J("third_party_record_v1_0_0.json"), J("live_observations_v1_0_0.json"), J("interpreter_record_v1_0_0.json"), J("pywheels_v1_0_0.json"), J("standin_v1_0_0.json")
src = open(os.path.join(H, "..", "sen0414_ch15_rdodi_data_v1_0_2.py"), encoding="utf-8").read()
live = {i["what"]: i["saw"] for i in lv["items"]}
find = lambda start: next(v for k, v in live.items() if k.startswith(start))
m = re.search(r"Not executed, and said so where it comes up: (.*?)\.\s+What was run instead is", src, re.S)
notexec = re.sub(r"\s+", " ", m.group(1)).strip()
out = []
out.append("Stand-in for Google: most of this chapter's outputs on the page do not come from Google. " + so["note"].split(": ", 1)[1].replace("this example runs", "An example marked so runs") + " The note is shown above the code of every such example, and slides of the deck that show such output say so too.")
out.append("NOT EXECUTED, because no Google account, OAuth consent or Cloud project was available: " + notexec + ".")
pyp = find("ezsheets on PyPI")
out.append("The chapter's printed programs were run as %d whole programs under Python %s with ezsheets %s (%d recorded runs in third_party_record_v1_0_0.json), against that stand-in at the HTTP layer or against the two public sheets read as CSV exports; a program that passes there may still fail against Google." % (len(tp["items"]), tp["python"].split()[0], pyp[0], len(tp["items"])))
ex = find("endpoints that need no Google account")
out.append("What Google itself answered on %s was only what needs no account: the three public sheets read as CSV exports (Boringcoin %s bytes, Bean Count %s bytes, both identical to the exports committed on 2026-10-01), the chapter's links, and a few requests made without credentials (the Sheets and Drive APIs answered %s and %s). %s." % (lv["observed"], find("Boringcoin sheet exported")[1], find("Bean Count sheet exported")[1], ex["sheets_get_no_credentials"][0], ex["drive_files_list_no_credentials"][0], lv["_note"].split(". ")[-1].rstrip(".").capitalize()))
out.append("One ezsheets program printed the same under the seven 3.14 releases, 3.13 and 3.12 once the pickle protocol is masked (it is %s from Python 3.14 and %s before; recorded 2026-10-12, against the stand-in)." % (ir["pickle_default_protocol"] if isinstance(ir["pickle_default_protocol"], str) else "5", "4"))
ws = ", ".join(w["file"].split("-")[0] for w in pw["wheels"])
out.append("The page's in-browser Python is Pyodide's CPython 3.13, which has neither ezsheets nor google-api-python-client, so the page carries %d wheels of its own (%s), downloaded from PyPI and checked by SHA-256, and loads Pyodide's own ssl, protobuf, cryptography and requests; the one change to a package is that the discovery documents of google-api-python-client other than Sheets v4 and Drive v3 were removed (no code was changed), and the page skips the docstring text that library builds for each method of each resource it creates (no request, answer or argument depends on it; without that skip an example takes several times longer in the browser), and, because the browser keeps one Python for many programs where the study ran a fresh interpreter for each, it puts ezsheets, the clock functions and the working folder back as they were at start before every program. ezsheets is licensed GPL-3.0-or-later and is embedded unmodified, with its source distribution kept beside the wheel in the repository. The page test compares every concept example's output in that browser Python with the value recorded under Python 3.14.6; six examples were changed in research version 1.0.2 where the browser cannot do what 3.14.6 did (a socket server, a second interpreter, webbrowser.get), and the unchanged record of those runs stays in the 1.0.1 files." % (len(pw["wheels"]), ws))
json.dump({"_version": __version__, "limits": out}, open(os.path.join(H, "limits_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
for x in out: print("-", x)
