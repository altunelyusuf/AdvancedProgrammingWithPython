#!/usr/bin/env python3
"""Chapter 13: observes, once, what the public sites the chapter names answer today, with requests and Beautiful Soup
(site directories on PYTHONPATH as for sen0414_ch13_thirdparty_v1_0_0.py), and writes what it saw with the date.
A web site changes; the record is an observation of the day, not something the build can re-check, and no check reads it.
Usage: sen0414_ch13_live_v1_0_0.py <python> <site-dir> [<site-dir> ...]  (run it with that interpreter)   -> ch13-page/live_observations_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, json, os, sys
import requests, bs4
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "08-tooling", "ch13-page", "live_observations_v1_0_0.json")
obs = []
def see(what, f):
    try: v = f()
    except Exception as e: v = "raised %s: %s" % (type(e).__name__, str(e)[:120])
    obs.append({"what": what, "saw": v})
def get(u): return requests.get(u, timeout=30)
r = get("https://automatetheboringstuff.com/files/rj.txt")
see("rj.txt of the chapter: status, number of characters, first line", lambda: [r.status_code, len(r.text), r.text.split("\n")[0]])
r = get("https://autbor.com/example3.html"); s = bs4.BeautifulSoup(r.text, "html.parser")
see("autbor.com/example3.html: status, p elements, text of the first", lambda: [r.status_code, len(s.select("p")), s.select("p")[0].get_text()])
r = get("https://xkcd.com"); s = bs4.BeautifulSoup(r.text, "html.parser")
see("xkcd.com front page: '#comic img' src starts with, 'a[rel=prev]' count", lambda: [r.status_code, s.select("#comic img")[0].get("src").split("/comics/")[0], len(s.select('a[rel="prev"]'))])
r = get("https://xkcd.com/1/"); s = bs4.BeautifulSoup(r.text, "html.parser")
see("xkcd.com/1/: href of the first 'a[rel=prev]'", lambda: [r.status_code, s.select('a[rel="prev"]')[0].get("href")])
r = get("https://pypi.org/search/?q=boring+stuff"); s = bs4.BeautifulSoup(r.text, "html.parser")
see("pypi.org search page fetched by requests: status, title, '.package-snippet' count", lambda: [r.status_code, s.title.get_text(), len(s.select(".package-snippet"))])
r = get("https://pypi.org/robots.txt")
see("pypi.org/robots.txt: Disallow lines", lambda: [ln for ln in r.text.splitlines() if ln.startswith("Disallow")])
r = get("https://xkcd.com/robots.txt")
see("xkcd.com/robots.txt", lambda: r.text.splitlines())
r = get("https://api.openweathermap.org/geo/1.0/direct?q=San Francisco,CA,US&appid=30ee784a80d81480dab1749d33980112")
see("OpenWeather geocoding call with the chapter's example key: status, content type, body", lambda: [r.status_code, r.headers.get("content-type"), r.text])
r = get("https://inventwithpython.com/page_that_does_not_exist")
def e404():
    try: r.raise_for_status()
    except Exception as e: return [r.status_code, str(e)]
see("inventwithpython.com/page_that_does_not_exist: status and the raise_for_status message", e404)
r = get("https://www.openstreetmap.org/search?query=777%20Valencia%20St%2C%20San%20Francisco%2C%20CA%2094110")
see("openstreetmap.org search URL of showmap.py: status", lambda: r.status_code)
json.dump({"_version": "1.0.0", "observed": datetime.date.today().isoformat(), "with": "requests %s, beautifulsoup4 %s, Python %s" % (requests.__version__, bs4.__version__, sys.version.split()[0]),
           "_note": "Single requests made on the day named, through the build machine's proxy, to the public pages the chapter names. A record of one observation; web sites change and nothing re-checks it.", "items": obs}, open(OUT, "w"), indent=1)
print("observed", len(obs), "things on", datetime.date.today())
