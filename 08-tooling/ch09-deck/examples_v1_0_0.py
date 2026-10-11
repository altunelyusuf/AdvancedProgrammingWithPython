"""Chapter 9 deck examples: every console session and whole program the lecture deck shows and the page's Lab tab
offers. Nothing here carries a result; examples_run_v1_0_0.py runs it all under the interpreter given and records
the results. A console group is one session: its rows run in order in one namespace (as the deck check re-runs
them per slide)."""
__version__ = "1.0.0"
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("base9", os.path.join(HERE, "..", "sen0414_ch09_corpus_base_v1_0_0.py"))
B = importlib.util.module_from_spec(_s)
_s.loader.exec_module(B)

CONSOLES = {
    "title": ["import re", "re.findall(r'\\d', 'R2D2')"],
    "manual": ["message = 'Call me at 415-555-1011 tomorrow. 415-555-9999 is my office.'",
               "is_phone_number = lambda t: len(t)==12 and t[:3].isdecimal() and t[3]=='-' and t[4:7].isdecimal() and t[7]=='-' and t[8:].isdecimal()",
               "[message[i:i+12] for i in range(len(message)) if is_phone_number(message[i:i+12])]",
               "is_phone_number('Moshi moshi')"],
    "objects": ["import re",
                "phoneNumRegex = re.compile(r'\\d{3}-\\d{3}-\\d{4}')",
                "mo = phoneNumRegex.search('My number is 415-555-4242.')",
                "mo.group()",
                "mo.span()",
                "phoneNumRegex.search('no digits here')",
                "re.match('c', 'abcdef')",
                "re.search('c', 'abcdef').span()",
                "re.fullmatch('p.*n', 'python').span()"],
    "grouping": ["import re",
                 "groupRegex = re.compile(r'(\\d\\d\\d)-(\\d\\d\\d-\\d\\d\\d\\d)')",
                 "mo = groupRegex.search('My number is 415-555-4242.')",
                 "mo.group(1)",
                 "mo.group(2)",
                 "mo.groups()",
                 "re.search(r'Cat(erpillar|astrophe|ch|egory)', 'Catch me if you can.').group(1)",
                 "re.match(r'(?P<first_name>\\w+) (?P<last_name>\\w+)', 'Malcolm Reynolds').groupdict()",
                 "re.search(r'\\b(\\w+) \\1\\b', 'this is is a typo').group()"],
    "charsets": ["import re",
                 "re.findall(r'[aeiouAEIOU]', 'RoboCop eats BABY FOOD.')",
                 "''.join(re.findall(r'[^aeiouAEIOU]', 'RoboCop eats BABY FOOD.'))",
                 "re.findall(r'\\d+\\s\\w+', '12 drummers, 11 pipers, 10 lords')",
                 "re.findall(r'.at', 'The cat in the hat sat on the flat mat.')"],
    "repetition": ["import re",
                   "re.search(r'42!?', '42').group()",
                   "re.search(r'Eggs( and spam)*', 'Eggs and spam and spam').span()",
                   "re.search(r'Eggs( and spam)+', 'Eggs') is None",
                   "re.fullmatch(r'(Ha){3,5}', 'HaHaHaHa') is not None",
                   "re.search(r'(Ha){3,5}', 'HaHaHaHaHa').group()",
                   "re.search(r'(Ha){3,5}?', 'HaHaHaHaHa').group()",
                   "re.search(r'<.*?>', '<To serve man> for dinner.>').group()",
                   "re.search(r'<.*>', '<To serve man> for dinner.>').group()"],
    "anchors": ["import re",
                "re.search(r'^\\d+$', '1234567890').span()",
                "re.search(r'^\\d+$', '12345xyz67890') is None",
                "re.findall(r'\\bcat.*?\\b', 'The cat found a catapult catalog in the catacombs.')",
                "re.findall(r'\\Bcat\\B', 'certificate')",
                "re.findall(r'\\d+(?= dollars)', '5 dollars and 7 euros')",
                "re.findall(r'(?<=\\$)\\d+', 'cost $30 or 40')"],
    "finding": ["import re",
                "re.findall(r'\\d{3}-\\d{3}-\\d{4}', 'Cell: 415-555-9999 Work: 212-555-0000')",
                "re.findall(r'(\\w+)=(\\d+)', 'set width=20 and height=10')",
                "re.compile(r'\\d{3}').findall('123456')",
                "[(m.start(), m.end(), m.group()) for m in re.finditer(r'\\w+ly\\b', 'He was carefully disguised but captured quickly by police.')]"],
    "replacing": ["import re",
                  "re.compile(r'Agent \\w+').sub('CENSORED', 'Agent Alice contacted Agent Bob.')",
                  "re.compile(r'Agent (\\w)\\w*').sub(r'\\1****', 'Agent Alice contacted Agent Bob.')",
                  "re.sub(r'\\d+', lambda m: str(int(m.group()) * 2), '3 cats 12 dogs')",
                  "re.escape('a.b*c')"],
    "flags": ["import re",
              "re.search('robocop', 'ROBOCOP protects', re.I).group()",
              "re.search('.*', 'Serve the public trust.\\nProtect the innocent.', re.DOTALL).group()",
              "re.search(r'\\d{3}  # area code\\n-\\d{4}  # number', '415-5551', re.VERBOSE).group()",
              "int(re.I | re.S | re.X)"],
}

# name -> (code, stdin text or None)
PROGRAMS = {
    "contactExtractor_v1_0_0.py": (B.CONTACT_EXTRACTOR, None),
    "strongPasswordDetector_v1_0_0.py": (B.STRONG_PASSWORD, B.STRONG_PASSWORD_INPUT),
    "regexStrip_v1_0_0.py": (B.REGEX_STRIP, None),
}
