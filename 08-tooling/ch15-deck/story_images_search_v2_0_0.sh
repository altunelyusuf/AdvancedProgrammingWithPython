#!/usr/bin/env bash
# Searches Openverse (api.openverse.org) for pictures under Creative Commons licences; used to find the story pictures of the chapter 15 deck (Wikimedia answered HTTP 429).
# Usage: bash story_images_search_v2_0_0.sh "QUERY" [PAGE_SIZE]   prints id, source, licence, title, creator, url
q="$1"
curl -sS -m 60 -A "SEN0414-course/1.0 (altunel.yusuf@gmail.com)" "https://api.openverse.org/v1/images/?q=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")&page_size=${2:-8}" | python3 -c "
import json,sys
try:
  d=json.load(sys.stdin)
  for r in d['results']: print(r['id'][:8],r['source'],r['license'],r['license_version'],'|',r['title'][:60],'|',r['creator'],'|',r['url'][:100])
except Exception as e: print('ERR',e)
"
