#!/bin/bash
# usage: links_live_check_v1_0_0.sh  (reads the RESOURCES links of the chapter 25 content, asks each once with the generic user agent of the course, prints the status)
cd /home/claude/advancedprogrammingwithpython/08-tooling/ch25-deck/spec_v4_0_0
python3 -c "
import content_v4_0_0 as T
for t,u,h in T.RESOURCES: print(u)" | while read u; do
  c=$(curl -s -o /dev/null -m 30 -L -w '%{http_code}' -A 'SEN0414-course-materials/1.0 (course materials; contact via GitHub altunelyusuf)' "$u"); echo "$c $u"; sleep 2
done
