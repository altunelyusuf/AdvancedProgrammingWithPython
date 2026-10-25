#!/usr/bin/env python3
"""sen0414_manifest_error_first_scan v1_0_0 - the first-line error scan of a chapter-code manifest (the lesson of the error-first finding, ex:CR2_ErrFirst, Iteration 19).
The page template draws a result as a chart or table, but an output whose FIRST line matches ^(\\w*Error|Traceback|Stopped after) is drawn as text, and the page test 9.37.0 (P2) then fails the example for want of a visual. An example whose result is an error must therefore be written so that its recorded result starts with an ordinary result line (the deck's example prints a line first, then the error text).
Usage: sen0414_manifest_error_first_scan_v1_0_0.py MANIFEST.json [MANIFEST.json ...]   (exit 0 only when no example of any manifest has a recorded result whose first line matches; prints each offending example by order, name and slide)"""
__version__ = "1.0.0"
import json, re, sys
ERR = re.compile(r"^(\w*Error|Traceback|Stopped after)")


def main():
    assert len(sys.argv) > 1, __doc__
    bad = 0
    for f in sys.argv[1:]:
        m = json.load(open(f, encoding="utf-8")); ex = m["examples"]; hit = []
        for e in ex:
            first = str(e.get("expected", "")).strip().splitlines()[:1]
            if first and ERR.match(first[0]):
                hit.append(e)
        print("%s: %d examples, %d with an error message as the first line of the recorded result" % (f, len(ex), len(hit)))
        for e in hit:
            print("  OFFENDS order %s name %s slide %s: %s" % (e.get("order"), e.get("name"), e.get("slide"), str(e["expected"]).strip().splitlines()[0][:80])); bad += 1
    print("RESULT: %s" % ("FAIL" if bad else "PASS")); sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
