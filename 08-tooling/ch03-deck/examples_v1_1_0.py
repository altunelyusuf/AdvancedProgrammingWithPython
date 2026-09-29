__version__ = "1.1.0"
# 1.1.0: everything of 1.0.0, plus the counting program the redesigned deck traces pass by pass (forsum). Outputs still come
# from executing them (examples_run_v1_1_0.py), never from typing.
from examples_v1_0_0 import EX, PROGRAMS as _P
PROGRAMS = dict(_P)
PROGRAMS["forsum_v1_0_0.py"] = ("total = 0\nfor n in range(1, 4):\n    total += n\nprint(total)\n", [[]])
PROGRAMS["chunks_old_v1_0_0.py"] = ("import io\nfile = io.StringIO('abcdefgh')\nwhile True:\n    chunk = file.read(3)\n    if not chunk:\n        break\n    print(chunk)\n", [[]])
