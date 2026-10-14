#!/usr/bin/env python3
"""sen0414_page_key_substitute v1_0_0 - makes a COPY of a chapter page whose embedded exam-release public key is replaced by the public half of a
freshly made TEST key, so that the page test can run its mock-exam release step on a machine that does not hold the instructor's private key.
The repository page is never changed. A pass obtained this way proves the page's logic (it verifies a release code signed by a key it trusts);
it does not prove anything about the real instructor key.

Usage: sen0414_page_key_substitute_v1_0_0.py NN PAGEVER OUTDIR     e.g. 07 9_28_0 /tmp/x   (writes OUTDIR/page.html and OUTDIR/test_key.json)
"""
__version__ = "1.0.0"
import base64, json, os, sys
from cryptography.hazmat.primitives.asymmetric import ec

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# the placeholder public key the repository pages carry (x, y of the P-256 key in course_page_config)
PLACEHOLDER = ("_zsDxa14DjwKPcKRIclVIdm2WzU5KQJ4mFfSc4K7Fwc", "C112ODgH30Twsw-Lrzvb4YQHF8wRpe8Iqo1KuiSIqvk")


def b64u(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def main():
    n, pv, out = sys.argv[1:4]
    os.makedirs(out, exist_ok=True)
    key = ec.generate_private_key(ec.SECP256R1())
    num = key.private_numbers(); pub = num.public_numbers
    jwk = {"kty": "EC", "crv": "P-256", "d": b64u(num.private_value.to_bytes(32, "big")), "x": b64u(pub.x.to_bytes(32, "big")), "y": b64u(pub.y.to_bytes(32, "big"))}
    json.dump({"private_jwk": jwk, "note": "TEST-ONLY key made by sen0414_page_key_substitute; not the instructor's"}, open(os.path.join(out, "test_key.json"), "w"))
    src = os.path.join(REPO, "03-materials", "ch%s" % n, "page", "sen0414_ch%s_page_v%s.html" % (n, pv))
    s = open(src, encoding="utf-8").read()
    a, b = PLACEHOLDER
    assert s.count(a) >= 1 and s.count(b) >= 1, "the page does not carry the placeholder public key"
    s = s.replace(a, jwk["x"]).replace(b, jwk["y"])
    open(os.path.join(out, "page.html"), "w", encoding="utf-8").write(s)
    print("placeholders replaced:", PLACEHOLDER[0][:8], PLACEHOLDER[1][:8])


if __name__ == "__main__":
    main()
