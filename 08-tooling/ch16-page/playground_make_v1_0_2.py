#!/usr/bin/env python3
"""Writes playground_v1_0_2.json (NEW file; refuses to overwrite) over playground_v1_0_1.json: the same program with the same behaviour and
output, no line longer than 100 characters (long SQL strings and calls broken over several lines). Prints the longest line. Usage: playground_make_v1_0_2.py"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(H, "playground_v1_0_2.json")
if os.path.exists(out): sys.exit("refusing to overwrite " + out)
d = json.load(open(os.path.join(H, "playground_v1_0_1.json"), encoding="utf-8"))
code = '''import sqlite3
conn = sqlite3.connect(':memory:', autocommit=True)
conn.execute('PRAGMA foreign_keys = ON')
conn.execute(
    'CREATE TABLE IF NOT EXISTS meals '
    '(id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE) STRICT'
)
conn.execute(
    'CREATE TABLE IF NOT EXISTS ingredients '
    '(name TEXT NOT NULL, meal_id INTEGER NOT NULL, '
    'FOREIGN KEY(meal_id) REFERENCES meals(id)) STRICT'
)
FIND = (
    'SELECT ingredients.name FROM ingredients '
    'JOIN meals ON meals.id = ingredients.meal_id '
    'WHERE meals.name = ? ORDER BY ingredients.rowid'
)
USED = (
    'SELECT meals.name FROM meals '
    'JOIN ingredients ON meals.id = ingredients.meal_id '
    'WHERE ingredients.name = ? ORDER BY meals.id'
)
while True:
    line = input('> ').strip()
    if line == 'quit':
        break
    if ':' in line:
        meal, _, rest = line.partition(':')
        meal = meal.strip()
        items = [item.strip() for item in rest.split(',') if item.strip()]
        conn.execute('BEGIN')
        try:
            meal_id = conn.execute(
                'INSERT INTO meals (name) VALUES (?)', [meal]
            ).lastrowid
            conn.executemany(
                'INSERT INTO ingredients (name, meal_id) VALUES (?, ?)',
                [(item, meal_id) for item in items]
            )
            conn.execute('COMMIT')
            print('Meal added:', meal)
        except sqlite3.IntegrityError as error:
            conn.execute('ROLLBACK')
            print('Not added:', error)
        continue
    found = conn.execute(FIND, [line]).fetchall()
    if found:
        print('Ingredients of ' + line + ':')
        for (item,) in found:
            print('  ' + item)
    used = conn.execute(USED, [line]).fetchall()
    if used:
        print('Meals that use ' + line + ':')
        for (name,) in used:
            print('  ' + name)
    if not found and not used:
        print('Nothing known about ' + line)
conn.close()'''
d["code"] = code
d["_version"] = "1.0.2"
d["_note"] += " Version 1.0.2 (over 1.0.1): the same program with no line longer than 100 characters (the highlighted overlay of the editor is as wide as the longest line); SQL strings and calls are broken over several lines, behaviour and output unchanged."
json.dump(d, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("longest line:", max(len(l) for l in code.split("\n")))
