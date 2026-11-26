#!/bin/bash
# usage: deckchecks.sh NN DECK MANIFEST LOGDIR
cd /home/claude/advancedprogrammingwithpython/08-tooling; mkdir -p $4
python3 sen0414_deck_standard_check_v1_3_0.py $1 $2 $3 > $4/deck_standard_v1_3_0.log 2>&1; echo std=$?
for p in "deck_fit_check_v1_0_0:fit" "deck_layout_check_v1_0_0:layout" "deck_notes_check_v1_0_0:notes" "sen0414_deck_overlap_check_v1_0_0:overlap" "sen0414_reader_notes_check_v1_0_0:reader_notes" "sen0414_story_prose_check_v1_0_0:story_prose"; do python3 ${p%:*}.py $2 > $4/${p#*:}.log 2>&1; echo ${p#*:}=$?; done
