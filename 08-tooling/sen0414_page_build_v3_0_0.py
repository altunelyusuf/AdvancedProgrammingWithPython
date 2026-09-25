#!/usr/bin/env python3
"""Version 3 of a SEN0414 chapter page: the course-neutral template course_page_template_v3_0_0.html filled with
the chapter's page data and course_page_config.json. Version 3 applies the owner's rules of 2026-09-25: code the
student edits really runs (Brython, which also works when published on claude.ai); agents answer from their own
slice of the ontology and the page's research record; menu clicks change the main area and the detail card opens
only on request; the tab row is the sub-menu of the selected top-level item. Usage: sen0414_page_build_v3_0_0.py <NN>"""
import json, os, sys
N = sys.argv[1]; REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = open(os.path.join(REPO, "08-tooling", "course_page_template_v3_0_0.html")).read()
P = os.path.join(REPO, "08-tooling", "ch%s-page" % N)
d = json.load(open(os.path.join(P, "page_data_v2.json")))
safe = lambda o: json.dumps(o).replace("</", "<\\/")
h = (T.replace("__TITLE__", d["title"]).replace("__COURSE__", d["course"]["line"]).replace("__SUB__", d["course"]["chapter_sub"].replace("{n}", str(d["chapter"])))
      .replace("__PY__", d["python"]).replace("__DATA__", safe(d)).replace("__QUIZ__", safe(json.load(open(os.path.join(P, "quiz.json")))))
      .replace("__OBJ__", safe(json.load(open(os.path.join(P, "objectives.json"))))))
out = os.path.join(REPO, "03-materials", "ch%s" % N, "page", "sen0414_ch%s_page_v3_0_0.html" % N)
open(out, "w").write(h); print("written", out, len(h), "bytes")
