"""Mission stage of the SEN0414 slide-renewal lineage. Composed as a module and appended."""

MISSION = """
ex:Mission a backlog:Mission ;
    rdfs:label "Teach SEN0414 from the edition students now read"@en ;
    backlog:missionFor ex:Backlog ;
    backlog:hasMissionStatement "Every SEN0414 lecture deck teaches what the third edition of the course textbook teaches, in its order, with its tools - renewed from the book's content and from researched evidence on each subject, not renumbered from the first edition's." ;
    backlog:hasMissionOrigin "Ruled by the owner on 2026-09-24: the slides are to be updated not only to match chapter numbers but to the updated book content, with RDODI research on the subject. Measured before this mission was written: the course repository holds seventeen decks - fourteen following the first edition's chapters, one raw draft of chapter 15, and two on GUI programming (tkinter, PySimpleGUI) that correspond to no chapter of either edition. The owner then fixed what is taught: an advanced course, Python chosen for its libraries and reach; the language chapters, regular expressions, files, spreadsheets, the web, time and scheduling, and speech engines; multithreading, which the third edition dropped, taught from the second edition's chapter 17; and no command-line programs, or chapters equally outdated. Against the third edition, six chapters are entirely new with no deck at all, and the chapters whose decks exist teach different tools in several places: file paths as objects rather than strings, debugging through logging rather than assertions, browser automation with a different library, PDF reading with a library whose earlier function no longer exists, and mail through a service interface rather than the protocols." ;
    backlog:hasMissionOutcome "A student opening any SEN0414 deck finds the chapter, the terms and the code of the book in their hands, and an instructor can trace every slide's claim to the book or to a researched source." ;
    backlog:outcomeRationale "Renumbering would have been cheaper and wrong. The course-content comparison already measured that the book keeps its calls and changes its lessons: 78 per cent of the first edition's constructs survive into the third, but only 45 of 96 concepts do. A deck renumbered to the new chapter would teach the old lesson under the new title." ;
    backlog:decidedBy backlog:Owner ;
    backlog:producedByStage ex:Out_Mission ;
    backlog:missionSource "The third edition of Automate the Boring Stuff with Python, read at https://automatetheboringstuff.com/3e/ and modelled chapter by chapter in the automate-python-book-3e ontology. Research by RDODI's four-stage procedure (v1.6.0), with its Pedagogy and Professional Standards stage and the Courseware profile for the teaching output - learning-design terms such as worked examples, assessment items and Bloom levels are taken from that vocabulary, not re-minted. Structured by CME's standards adoption: each deck is a teaching material described by IEEE Learning Object Metadata and aligned to the course's learning outcomes." .
"""


def mission_block():
    return MISSION
