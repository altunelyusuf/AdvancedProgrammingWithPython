#!/usr/bin/env python3
"""Chapter 13: observes, once, what the public sites the chapter names answer today, with requests and Beautiful Soup, and
writes what it saw with the date. A web site changes; the record is an observation of the day, not something the build can
re-check, and no check reads it.
1.0.1 (over 1.0.0): run under Python 3.14.6 with requests 2.34.2, Beautiful Soup 4.15.0 and urllib.robotparser of that
interpreter; adds what the file of the Romeo and Juliet download weighs in bytes and in characters and the chunks that
iter_content(100000) gives for it, the exact bytes of example3.html, the robots.txt rules as 3.14.6 applies them to the search
page of PyPI, the forecast page of weather.gov that the chapter inspects (it still has the forecast-text class), the free
forecast API of weather.gov, the front page of the 2048 game and the error message of a failed download with and without the
.html that the chapter prints. Sites are asked once each, with the default user agent of requests unless a site's
documentation asks for a name (api.weather.gov), nothing is posted, and no key of anyone is sent.
Usage: sen0414_ch13_live_v1_0_1.py   (run with the interpreter that has requests and bs4)  -> ch13-page/live_observations_v1_0_1.json"""
__version__ = "1.0.1"
import datetime, hashlib, json, os, sys, urllib.parse, urllib.robotparser
import requests, bs4
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "08-tooling", "ch13-page", "live_observations_v1_0_1.json")
obs = []
def see(what, f):
    try: v = f()
    except Exception as e: v = "raised %s: %s" % (type(e).__name__, str(e)[:120])
    obs.append({"what": what, "saw": v})
def get(u, **k): return requests.get(u, timeout=30, **k)
r = get("https://automatetheboringstuff.com/files/rj.txt")
see("rj.txt of the chapter: status, content type, bytes, characters, first line", lambda: [r.status_code, r.headers.get("content-type"), len(r.content), len(r.text), r.text.split("\n")[0]])
see("rj.txt: the sizes iter_content(100000) gives, and the last-modified date of the file", lambda: [[len(c) for c in r.iter_content(100000)], r.headers.get("last-modified")])
CHAPTER_FIRST_210 = "The Project Gutenberg EBook of Romeo and Juliet, by William Shakespeare\n\nThis eBook is for the use of anyone anywhere at no cost and with\nalmost no restrictions whatsoever.  You may copy it, give it away or"
see("rj.txt: whether the text begins with the lines the chapter prints for text[:210] (the real 210 characters run on into a fifth line), and the real length against the printed 178978", lambda: [r.text.startswith(CHAPTER_FIRST_210), r.text[:210].splitlines()[-1], len(r.text), len(r.text) - 178978])
r = get("https://autbor.com/example3.html"); s = bs4.BeautifulSoup(r.text, "html.parser")
see("autbor.com/example3.html: status, bytes, sha256 of the bytes, CRLF line ends, p elements, text of the first", lambda: [r.status_code, len(r.content), hashlib.sha256(r.content).hexdigest(), r.content.count(b"\r\n"), len(s.select("p")), s.select("p")[0].get_text()])
see("autbor.com/example3.html: title, alt text of the picture, elements with the id author", lambda: [s.title.get_text(), s.select("img")[0].get("alt"), len(s.select("#author"))])
r = get("https://xkcd.com"); s = bs4.BeautifulSoup(r.text, "html.parser")
see("xkcd.com front page: status, '#comic img' src starts with, 'a[rel=prev]' count and its href form", lambda: [r.status_code, s.select("#comic img")[0].get("src").split("/comics/")[0], len(s.select('a[rel="prev"]')), s.select('a[rel="prev"]')[0].get("href").split("/")[-2].isdigit()])
r = get("https://xkcd.com/1/"); s = bs4.BeautifulSoup(r.text, "html.parser")
see("xkcd.com/1/: href of the first 'a[rel=prev]', and the comic image file", lambda: [r.status_code, s.select('a[rel="prev"]')[0].get("href"), os.path.basename(s.select("#comic img")[0].get("src"))])
r = get("https://xkcd.com/1358/"); s = bs4.BeautifulSoup(r.text, "html.parser")
see("xkcd.com/1358/ (printed in the chapter's output): status, comic image file name", lambda: [r.status_code, os.path.basename(s.select("#comic img")[0].get("src"))])
r = get("https://pypi.org/search/?q=boring+stuff"); s = bs4.BeautifulSoup(r.text, "html.parser")
see("pypi.org search page fetched by requests: status, title, '.package-snippet' count", lambda: [r.status_code, s.title.get_text(), len(s.select(".package-snippet"))])
r = get("https://pypi.org/robots.txt"); rp = urllib.robotparser.RobotFileParser(); rp.parse(r.text.splitlines())
see("pypi.org/robots.txt: Disallow lines", lambda: [ln for ln in r.text.splitlines() if ln.startswith("Disallow")])
see("pypi.org/robots.txt read by urllib.robotparser of %s: may '*' fetch the search page of searchpypi.py, a project page, /simple/" % sys.version.split()[0], lambda: [rp.can_fetch("*", "https://pypi.org/search/?q=boring+stuff"), rp.can_fetch("*", "https://pypi.org/project/pyautogui/"), rp.can_fetch("*", "https://pypi.org/simple/requests/")])
r = get("https://xkcd.com/robots.txt"); rx = urllib.robotparser.RobotFileParser(); rx.parse(r.text.splitlines())
see("xkcd.com/robots.txt, and what urllib.robotparser says of the front page and of the prev link", lambda: [r.text.splitlines(), rx.can_fetch("*", "https://xkcd.com/1358/"), rx.can_fetch("GPTBot", "https://xkcd.com/1358/")])
r = get("https://api.openweathermap.org/geo/1.0/direct?q=San Francisco,CA,US&appid=30ee784a80d81480dab1749d33980112")
see("OpenWeather geocoding call with the chapter's example key: status, content type, body", lambda: [r.status_code, r.headers.get("content-type"), r.text])
r = get("https://inventwithpython.com/page_that_does_not_exist")
def e404(r=r):
    try: r.raise_for_status()
    except Exception as e: return [r.status_code, str(e)]
see("inventwithpython.com/page_that_does_not_exist: status and the raise_for_status message (the chapter prints a url ending .html)", e404)
r = get("https://inventwithpython.com/page_that_does_not_exist.html")
see("inventwithpython.com/page_that_does_not_exist.html: status", lambda: r.status_code)
r = get("https://www.openstreetmap.org/search?query=777%20Valencia%20St%2C%20San%20Francisco%2C%20CA%2094110")
see("openstreetmap.org search URL of showmap.py: status", lambda: r.status_code)
r = get("https://forecast.weather.gov/zipcity.php?inputstring=94105"); s = bs4.BeautifulSoup(r.text, "html.parser")
see("forecast.weather.gov for the ZIP code 94105 (the chapter's Developer Tools example): status, final path, 'div.col-sm-10.forecast-text' count, text of the first (it changes every day)", lambda: [r.status_code, urllib.parse.urlsplit(r.url).path, len(s.select("div.col-sm-10.forecast-text")), s.select("div.col-sm-10.forecast-text")[0].get_text()])
H = {"User-Agent": "SEN0414-teaching-example"}
def nws():
    p = get("https://api.weather.gov/points/37.7790,-122.4199", headers=H); j = p.json(); f = get(j["properties"]["forecast"], headers=H); pe = f.json()["properties"]["periods"]
    return [p.status_code, p.headers.get("content-type"), j["properties"]["forecast"], f.status_code, len(pe), sorted(pe[0])[:6], pe[0]["name"], pe[0]["temperature"], pe[0]["temperatureUnit"]]
see("api.weather.gov, a free forecast API the chapter names, no key: points then forecast for the chapter's San Francisco latitude and longitude (values change)", nws)
r = get("https://play2048.co")
see("play2048.co, the game of the chapter's practice program: status and final URL", lambda: [r.status_code, r.url])
json.dump({"_version": "1.0.1", "observed": datetime.date.today().isoformat(), "with": "requests %s, beautifulsoup4 %s, Python %s" % (requests.__version__, bs4.__version__, sys.version.split()[0]),
           "_note": "Single requests made on the day named, through the build machine's proxy, to the public pages the chapter names. A record of one observation; web sites change and nothing re-checks it.", "items": obs}, open(OUT, "w"), indent=1)
print("observed", len(obs), "things on", datetime.date.today())
