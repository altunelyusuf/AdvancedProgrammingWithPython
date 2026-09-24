"""Chapter 2 content for the RDODI build: sources, findings, taxonomy and section bodies.
Every claim was read from the source it cites on 2026-09-24; every behaviour was executed under Python 3.14.4."""
CH = 2
TITLE = "Flow control for an advanced course: chapter 2 of the 3rd edition and today's Python"
QUESTION = "What does chapter 2 of the 3rd edition teach about Boolean logic and flow control, and what must an advanced course add so that it matches current Python?"
PUBS = [
 ("P01","Automate the Boring Stuff with Python, 3rd edition - Chapter 2, if-else and Flow Control (Al Sweigart, No Starch Press, 2025)","https://automatetheboringstuff.com/3e/chapter2.html",True),
 ("P02","The Python Tutorial, 4. More Control Flow Tools (Python 3.14.7 documentation)","https://docs.python.org/3/tutorial/controlflow.html",False),
 ("P03","The Python Language Reference, 8. Compound statements (Python 3.14.7 documentation)","https://docs.python.org/3/reference/compound_stmts.html",False),
 ("P04","The Python Language Reference, 6. Expressions (Python 3.14.7 documentation)","https://docs.python.org/3/reference/expressions.html",False),
 ("P05","The Python Standard Library, Built-in Types - Truth Value Testing (Python 3.14.7 documentation)","https://docs.python.org/3/library/stdtypes.html",False),
 ("P06","PEP 634 - Structural Pattern Matching: Specification (Bucher and van Rossum, 2020; Python 3.10)","https://peps.python.org/pep-0634/",False),
 ("P07","PEP 636 - Structural Pattern Matching: Tutorial","https://peps.python.org/pep-0636/",False),
 ("P08","PEP 765 - Disallow return/break/continue that exit a finally block (Katriel and Coghlan, 2024; Python 3.14)","https://peps.python.org/pep-0765/",False),
 ("P09","What's new in Python 3.14 (Python documentation)","https://docs.python.org/3/whatsnew/3.14.html",False),
 ("P10","PEP 8 - Style Guide for Python Code","https://peps.python.org/pep-0008/",False),
]
CONCEPTS = [("Section",x) for x in ("Boolean Values","Comparison Operators","Boolean Operators","Mixing Boolean and Comparison Operators","Components of Flow Control","Flow Control Statements","A Short Program: Opposite Day","A Short Program: Dishonest Capacity Calculator")] + \
 [("Concept",x) for x in ("Boolean value","Comparison operator","Boolean operator","Block","Flow control statement")] + \
 [("Operator",x) for x in ("==","!=","<",">","<=",">=","and","or","not")] + [("Statement",x) for x in ("if","else","elif")]
FINDINGS = [
 ("F1","Background","Chapter 2 of the 3rd edition introduces the Boolean values True and False, the six comparison operators, the Boolean operators and, or and not, how comparison and Boolean operators mix, the components of flow control - conditions and blocks - and the if, else and elif statements, with two short programs.",["P01"]),
 ("F2","Contemporary developments","Python 3.10 added structural pattern matching: a match statement compares a value against successive case patterns, closer to pattern matching than to the switch statement of C or Java. Python 3.14 adopted PEP 765, which disallows return, break and continue that exit a finally block.",["P06","P02","P08"]),
 ("F3","Comparative analysis","The reference documentation makes precise what the chapter leaves informal: and and or return one of their operands rather than a Boolean - x and y returns x if x is false - and evaluate the second operand only when needed; comparisons chain, so x < y <= z means x < y and y <= z; many values besides False count as false, including None, zero of any numeric type and empty sequences; the conditional expression x if C else y chooses a value in one line; and PEP 8 advises against comparing Boolean values to True or False with ==.",["P04","P05","P10"]),
 ("F4","Conclusion","For an advanced course, chapter 2 is best taught as decision-making in real Python: truthiness and short-circuit evaluation as working tools, chained comparisons and conditional expressions as idioms, and the match statement as the modern alternative to long elif chains.",["P04","P05","P06"]),
]
# (top, mid, leaf, exemplar, definition, io-or-None)
TAX = [
 ("Value","TruthValue","BooleanValue","the values True and False","The two Boolean values, written with a capital letter; the result of every comparison.",("42 == 42","True")),
 ("Value","TruthValue","Truthiness","bool('') and bool('0')","Any value can be tested for truth: None, False, zero and empty sequences are false, so bool('') is False while bool('0') is True.",("bool('0')","True")),
 ("Comparison","EqualityComparison","Equality","42 == '42'","== and != compare values; an integer never equals a string, so 42 == '42' is False.",("42 == '42'","False")),
 ("Comparison","OrderingComparison","Ordering","2 != 3 and 4 < 5","<, >, <= and >= compare order and return a Boolean value.",("(4 < 5) and (5 < 6)","True")),
 ("Comparison","OrderingComparison","ChainedComparison","1 < 2 < 3","Comparisons chain: x < y <= z means x < y and y <= z, with y evaluated once.",("1 < 2 < 3","True")),
 ("BooleanOperation","LogicalOperator","AndOperator","True and False","and is true only when both operands are true.",("True and False","False")),
 ("BooleanOperation","LogicalOperator","OrOperator","True or False","or is true when either operand is true.",("True or False","True")),
 ("BooleanOperation","LogicalOperator","NotOperator","not True","not inverts a single Boolean value.",("not True","False")),
 ("BooleanOperation","Evaluation","ShortCircuit","'' or 'default'","and and or stop as soon as the answer is known and return an operand, so '' or 'default' returns 'default'.",("'' or 'default'","'default'")),
 ("FlowControl","ControlStructure","Condition","the expression after if","A condition is an expression evaluated for truth to decide which block runs.",None),
 ("FlowControl","ControlStructure","Block","an indented group of lines","A block is a group of lines at the same indentation; Python uses indentation, not braces, to mark it.",None),
 ("FlowControl","Branching","IfStatement","if name == 'Alice':","if runs its block only when its condition is true.",None),
 ("FlowControl","Branching","ElifClause","elif age < 12:","elif tests a further condition only when every earlier one was false; at most one branch runs.",None),
 ("FlowControl","Branching","ElseClause","else:","else runs its block when no earlier condition in the chain was true.",None),
 ("FlowControl","ExpressionForm","ConditionalExpression","'even' if 10 % 2 == 0 else 'odd'","x if C else y chooses between two values in a single expression.",("'even' if 10 % 2 == 0 else 'odd'","'even'")),
 ("ModernPractice","PatternMatching","MatchStatement","match command:","Since Python 3.10 a match statement compares a value against successive case patterns - the modern alternative to a long elif chain.",None),
 ("ModernPractice","Style","BooleanComparisonStyle","if greeting: rather than if greeting == True:","PEP 8 advises testing a Boolean directly instead of comparing it to True or False with ==.",None),
]
ERRORS = []
S = "Sweigart, 2025"; PSF = "Python Software Foundation, 2026"; B = "Bucher and Van Rossum, 2020"; K = "Katriel and Coghlan, 2024"; V = "Van Rossum et al., 2001"
BODY = {
 "Value": "Chapter 2 adds a new kind of value, the Boolean, and with it the idea that any value can be tested for truth (%s)." % S,
 "TruthValue": "Truth is the currency of flow control: every decision a program makes reduces to a true or false value (%s)." % S,
 "BooleanValue": "The Boolean values True and False are written with a capital letter, and every comparison produces one, so 42 == 42 evaluates to True (%s)." % S,
 "Truthiness": "Python tests any value for truth, not only Booleans: None, False, zero of any numeric type and empty sequences are false, so bool('') is False while bool('0') is True (%s)." % PSF,
 "Comparison": "Comparison operators ask a question about two values and answer with a Boolean value (%s)." % S,
 "EqualityComparison": "Equality comparisons ask whether two values are the same, a different question from assignment's single equals sign (%s)." % S,
 "Equality": "The == and != operators compare values, and an integer never equals a string, so 42 == '42' evaluates to False (%s)." % S,
 "OrderingComparison": "Ordering comparisons ask which of two values comes first, and they combine with Boolean operators into longer conditions (%s)." % S,
 "Ordering": "The operators <, >, <= and >= compare order, so (4 < 5) and (5 < 6) evaluates to True (%s)." % S,
 "ChainedComparison": "Comparisons chain, so x < y <= z means x < y and y <= z with y evaluated only once; 1 < 2 < 3 evaluates to True (%s)." % PSF,
 "BooleanOperation": "The Boolean operators and, or and not combine truth values, and the chapter shows them mixed with comparisons in one expression (%s)." % S,
 "LogicalOperator": "Each Boolean operator has a truth table the chapter sets out, and the three together can express any condition a program needs (%s)." % S,
 "AndOperator": "The and operator is true only when both operands are true, so True and False evaluates to False (%s)." % S,
 "OrOperator": "The or operator is true when either operand is true, so True or False evaluates to True (%s)." % S,
 "NotOperator": "The not operator inverts one Boolean value, so not True evaluates to False (%s)." % S,
 "Evaluation": "How Boolean operators evaluate matters as much as what they return, because the second operand is sometimes never evaluated at all (%s)." % PSF,
 "ShortCircuit": "The and and or operators stop as soon as the answer is known and return one of their operands rather than a Boolean, so '' or 'default' returns 'default' - a common idiom for fallback values (%s)." % PSF,
 "FlowControl": "Flow control decides which lines run and in what order, built from conditions and blocks (%s)." % S,
 "ControlStructure": "The chapter's Components of Flow Control section names the two parts every decision needs: a condition and a block (%s)." % S,
 "Condition": "A condition is an expression evaluated for its truth value, and it decides which block of code runs next (%s)." % S,
 "Block": "A block is a group of lines at the same indentation; Python marks blocks with indentation rather than braces, so indentation is part of the program's meaning (%s)." % S,
 "Branching": "The Flow Control Statements section builds branches with if, else and elif, as the Opposite Day and Dishonest Capacity Calculator programs show (%s)." % S,
 "IfStatement": "An if statement runs its block only when its condition is true, and skips it otherwise (%s)." % S,
 "ElifClause": "An elif clause tests a further condition only when every earlier condition was false, so at most one branch of the chain runs (%s)." % S,
 "ElseClause": "An else clause runs its block when no earlier condition in the chain was true (%s)." % S,
 "ExpressionForm": "Some decisions choose a value rather than run a block, and Python has an expression form for that case (%s)." % PSF,
 "ConditionalExpression": "The conditional expression x if C else y evaluates the condition first and returns one of two values, so 'even' if 10 %% 2 == 0 else 'odd' gives 'even' (%s)." % PSF,
 "ModernPractice": "An advanced course pairs the chapter's if-elif chains with the forms current Python offers for the same decisions (%s)." % B,
 "PatternMatching": "Pattern matching tests a value's shape as well as its value, which elif chains can only imitate (%s)." % B,
 "MatchStatement": "Since Python 3.10 a match statement compares a value against successive case patterns - closer to pattern matching than to the switch statement of C or Java - and replaces long elif chains (%s)." % B,
 "Style": "Style guidance keeps conditions readable, and the conventions for Boolean tests are among the most often broken (%s)." % V,
 "BooleanComparisonStyle": "PEP 8 advises testing a Boolean directly - if greeting: - instead of comparing it to True with == (%s); Python 3.14 also tightened flow control by adopting PEP 765, which disallows return, break and continue that exit a finally block (%s)." % (V, K),
}
