#!/usr/bin/env python3
"""SEN0414 chapter 1 corpus, version 1.1.0: the concepts of the chapter, each explained in paragraphs that answer
what it is, why it matters, where it is met and how it works (and what to watch for).

Used by sen0414_ch01_domain_build_v1_2_0.py (TBox/ABox: the leaf individuals) and
sen0414_ch01_document_build_v1_2_0.py (the document: one section per concept, paragraphs joined by a blank line,
each opening with its facet, e.g. "What it is: ...").
Every quoted claim was taken from text actually read (docs.python.org glossary, tutorial, language reference,
library reference, howto on free threading, What's New 3.13 and 3.14; peps.python.org PEPs 1, 8, 701, 703, 779; the
developer's guide; docs.astral.sh/uv) and every number or output was executed (CHECKS below, run by the builders).
"""
__version__ = "1.1.0"
W, Y, E, H, K, C = "What it is", "Why it matters", "Where you meet it", "How it works", "Watch out", "What changed"
SW, PSF, PEP8, PEP701, WARSAW, GROSS, WOUTERS, ASTRAL, SO = ("(Sweigart, 2025)", "(Python Software Foundation, 2026)", "(Van Rossum et al., 2001)",
    "(Galindo Salgado et al., 2022)", "(Warsaw et al., 2000)", "(Gross, 2023)", "(Wouters et al., 2025)", "(Astral, 2026)", "(Stack Overflow, 2025)")

# (id, label or None for the camel-case label, level, parent, leaf, paras)
# leaf = None for levels 1 and 2, else (example label, definition, io-example or None)
NODES = [
 ("Value", None, 1, None, None, [
  (W, "A value is a piece of data that a Python program can compute with, store and print. The whole number 42, the decimal 3.14 and the text 'Alice' are all values, and each has a data type that decides what can be done with it %s." % SW),
  (Y, "Everything a program does is the handling of values, so knowing which kinds exist and how they behave is the base on which operators, variables and functions are built. A learner who can say what kind of value an expression produces can usually predict whether the expression will run or fail."),
  (E, "Values appear wherever an expression is evaluated. In the interactive shell the result of each expression is printed as soon as it is computed, and every line of a program that adds, joins or prints something works on values %s." % SW),
  (H, "The chapter works with three kinds of value: integers, floating-point numbers and strings. The following sections take the numeric kinds first and then text, and afterwards explain what a data type is and how an expression combines values into a new one."),
  (K, "Two values that print almost identically can be of different kinds. The integer 7 and the string '7' look alike on the screen, yet 7 + 1 gives 8 while '7' + 1 raises a TypeError."),
 ], None),
 ("NumericValue", None, 2, "Value", None, [
  (W, "Numeric values are numbers that a program can do arithmetic with. The chapter meets two kinds of them: integers, which are whole numbers, and floating-point numbers, which have a fractional part %s." % SW),
  (Y, "The two kinds look alike on the page but are stored differently, and the difference decides whether a result is exact. Knowing it prevents the surprise of a calculation that is off by a tiny amount."),
  (H, "An integer is stored exactly, however large it grows, while a float is stored in binary with a fixed precision and can only approximate many decimal fractions %s. When an integer and a float meet in one expression, the integer operand is converted to floating point, so 4 * 3.75 - 1 evaluates to 14.0 %s." % (PSF, PSF)),
  (K, "Division with the / operator always returns a float, even when the division is exact: 6 / 3 evaluates to 2.0 and not to 2 %s." % PSF),
 ], None),
 ("Integer", None, 3, "NumericValue", ("the integer 2 ** 100", "A whole number. Python integers have unlimited precision, so 2 ** 100 is exact.", ("2 ** 100", "1267650600228229401496703205376")), [
  (W, "An integer is a whole number without a fractional part, such as 42, 0 or -7. In Python it belongs to the type int, the same name that the int function uses when it converts a value %s." % PSF),
  (Y, "Integers count things: the items of a list, the steps of a loop, the years of an age. Because an integer is stored exactly, it is the right choice whenever a result must not be approximate."),
  (E, "Integers come from whole-number literals, from the operators +, - and * applied to integers, from floor division and the modulus operator, and from len, which returns a count of characters."),
  (H, "Python integers have unlimited precision, so 2 ** 100 evaluates exactly to 1267650600228229401496703205376 and does not overflow as the fixed-size integers of many other languages do %s. The result is exact however many digits it needs." % PSF),
  (K, "An integer typed at the keyboard arrives as text. The call int('42') gives the integer 42, but the string '42' itself cannot be used in arithmetic until it has been converted."),
 ]),
 ("FloatingPoint", None, 3, "NumericValue", ("the float sum 0.1 + 0.2", "A number with a fractional part, stored in binary, so some decimal values cannot be represented exactly.", ("0.1 + 0.2", "0.30000000000000004")), [
  (W, "A floating-point number, or float, is a number with a fractional part, such as 3.14 or -0.5. In Python it belongs to the type float %s." % PSF),
  (Y, "Floats make it possible to work with measurements and fractions such as prices, averages and temperatures. They are the result whenever a calculation needs a fractional part, as the division operator / always does."),
  (E, "A float appears when a literal contains a decimal point, when the operator / is used, when the float function converts a value, and whenever an integer and a float are mixed in one expression."),
  (H, "Floats are stored in binary with a fixed precision, so some decimal fractions cannot be represented exactly. The sum 0.1 + 0.2 therefore evaluates to 0.30000000000000004, and round(0.1 + 0.2, 2) gives 0.3 %s." % PSF),
  (K, "Comparing two floats for exact equality after arithmetic is risky for the same reason. The binary storage is also why the closing section of the chapter, How Computers Store Data with Binary Numbers, matters even for everyday decimal calculations %s." % SW),
 ]),
 ("TextValue", None, 2, "Value", None, [
  (W, "Text values are sequences of characters that a program reads, stores and prints. Chapter 1 treats text as a value like any other, with the same expression rules it uses for numbers %s." % SW),
  (Y, "Most programs exist to read names, show messages and handle words, so text is as common as numbers. Treating text as an ordinary value lets the same operators and functions work on both, each with a meaning suited to its type."),
  (H, "In Python, text is represented by the string type, written between quotes. The operators + and * act on strings as joining and repeating, and functions such as len measure them."),
 ], None),
 ("String", None, 3, "TextValue", ("the string 'Alice'", "A sequence of characters written between quotes.", ("'Alice' * 3", "'AliceAliceAlice'")), [
  (W, "A string is a sequence of characters written between quotes, such as 'Alice' or 'Hello, world!'. Python names the type str, and either single or double quotes can enclose the text %s." % PSF),
  (Y, "Strings carry everything a person reads or types: names, messages, file contents and the answers given to input. A program that cannot handle strings cannot talk to its user."),
  (E, "Strings are written as literals in the source code, returned by the input function, produced by the str function and built by formatted string literals. They are what print finally shows."),
  (H, "The same operators that act on numbers act on strings with another meaning: + joins two strings and * repeats a string. Strings are immutable, so an operation never changes a string in place; it creates a new one %s." % PSF),
  (K, "A string that looks like a number is still text. The string '7' and the integer 7 are different values, and Python does not convert between them silently %s." % SW),
 ]),
 ("ValueModel", "Value model", 2, "Value", None, [
  (W, "The value model is the pair of ideas that explain what a value is: every value has a data type, and an expression is the piece of code that evaluates to a value. The two ideas depend on each other, because the type of an expression's result is decided by the types of the values it combines."),
  (Y, "Without the idea of a type, the error messages of Python are hard to read, since many of them say that a type did not fit an operation. Without the idea of an expression, the shell, the function call and the formatted string look like unrelated features."),
  (H, "A learner can test the model in the shell by typing an expression, reading its value and asking for its type with the type function. The next two sections define the two ideas and show how they are used."),
 ], None),
 ("DataType", None, 3, "ValueModel", ("type(3.5)", "The kind of a value, which decides which operations apply to it; the type function reports it.", ("type(3.5)", "<class 'float'>")), [
  (W, "A data type is the kind of a value, and it decides what the value can do and what can be done with it. Every Python object has a type, which can be read with the type function %s." % PSF),
  (Y, "The type decides which operations are meaningful. Numbers can be divided, strings can be joined, and asking Python to do something that a type does not support ends in a TypeError instead of a silent guess."),
  (E, "Types are visible in the shell: type(7) gives <class 'int'>, type(3.5) gives <class 'float'> and type('Alice') gives <class 'str'>. They are also named in error messages, which report both types involved in a failed operation."),
  (H, "A value gets its type when it is created: the literal 42 creates an int and 3.14 creates a float. Python checks types when an operation runs, not before the program starts, so a wrong combination is reported only when its line executes."),
  (K, "A variable does not have a type of its own; the value it refers to has one. Assigning a string to a name that held a number is allowed and simply changes what the name refers to."),
 ]),
 ("Expression", None, 3, "ValueModel", ("3 * (2 + 4)", "A piece of code that evaluates to a value, built from values, operators, names and function calls.", ("3 * (2 + 4)", "18")), [
  (W, "An expression is a piece of code that Python can evaluate to a value. It is built from literals, names, operators and function calls; 2 + 3 * 6 is an expression whose value is 20 %s." % PSF),
  (Y, "Expressions are the building blocks of programs. Almost everything a program computes is an expression, and larger expressions are made by putting smaller ones inside them. Reading an expression correctly means finding the order in which its parts are evaluated."),
  (E, "The interactive shell evaluates expressions the moment they are typed and prints their values. Inside programs, expressions appear on the right of an assignment, inside the parentheses of a function call and inside the braces of an f-string."),
  (H, "Python evaluates the smallest parts first and replaces each with its value until one value remains. In 3 * (2 + 4) the parentheses give 6 and the multiplication then gives 18, and an operator of higher precedence is evaluated before one of lower precedence."),
  (K, "An expression is not the same thing as a statement. An assignment such as spam = 42 is a statement: it stores a value but is not itself an expression, so it produces no value to print %s." % PSF),
 ]),
 ("Operation", None, 1, None, None, [
  (W, "An operation combines values into a new value, and in Python most operations are written with operators placed between their operands. The chapter covers arithmetic on numbers, joining and repeating of strings, and the assignment that gives a value a name."),
  (Y, "Operations are what make a program do work; without them values could only be stored and shown. Their rules are fixed by the language, so two readers who follow the rules reach the same answer whatever they expect %s." % PSF),
  (E, "Operations appear in every expression typed in the shell and on nearly every line of a program, from adding two quantities to storing the answer."),
  (H, "Each operation takes operands of particular types and produces a value whose type depends on them. When the types do not fit, Python stops with a TypeError instead of guessing."),
 ], None),
 ("ArithmeticOperation", None, 2, "Operation", None, [
  (W, "Arithmetic operations calculate with numbers. The chapter introduces seven operators for them: +, -, *, /, //, %% and ** %s." % SW),
  (Y, "These seven cover addition, subtraction, multiplication, true division, whole-number division, the remainder and exponentiation, which is enough to model most everyday calculations."),
  (H, "Each operator takes two numbers and returns a number, and the result is a float whenever either operand is a float or the operator is /. Several operators in one expression are applied in a documented order."),
 ], None),
 ("Operator", None, 3, "ArithmeticOperation", ("7 % 3", "A symbol such as +, * or % that performs an operation on its operands; the type of the operands decides its meaning.", ("7 % 3", "1")), [
  (W, "An operator is a symbol that tells Python to perform an operation on the values around it, which are called its operands. In 7 %% 3 the symbol %% is the operator and 7 and 3 are its operands %s." % PSF),
  (Y, "Operators let a program write a calculation in the notation of mathematics, so that a line such as price * count reads almost like the formula it implements."),
  (E, "The chapter uses the arithmetic operators on numbers, the operators + and * on strings, and the single equals sign for assignment, which is a statement and not an operator inside an expression."),
  (H, "Most operators in the chapter are binary: they take an operand on each side. The same symbol can mean different things for different types, so the type of the operands decides what the operator does: 2 + 3 adds, while 'a' + 'b' joins."),
  (K, "Treat / and // as different operators: 7 / 2 gives 3.5, while 7 // 2 gives 3."),
 ]),
 ("Precedence", None, 3, "ArithmeticOperation", ("2 + 3 * 6 evaluated", "The order in which operators apply: ** first, then *, /, //, %, then + and -; parentheses override it.", ("2 + 3 * 6", "20")), [
  (W, "Operator precedence is the rule that decides which operator is applied first when an expression contains several. It is fixed by the language: ** binds first, then *, /, // and %%, then + and - %s." % PSF),
  (Y, "Precedence makes an expression mean exactly one thing. Without it, 2 + 3 * 6 could be read as 30 or as 20, and two programmers could disagree about what a line computes."),
  (E, "Every expression that mixes operators depends on it, including long formulas and the expressions inside f-strings and function calls."),
  (H, "Python applies the operator of higher precedence first, so 2 + 3 * 6 evaluates to 20. Parentheses override the order: (2 + 3) * 6 evaluates to 30. Operators of equal precedence, such as * and /, are applied from left to right."),
  (K, "The power operator binds more tightly than a minus sign on its left, so -3 ** 2 evaluates to -9 while (-3) ** 2 evaluates to 9 %s." % PSF),
 ]),
 ("IntegerDivision", None, 3, "ArithmeticOperation", ("23 // 7 and 23 % 7", "Floor division gives the whole-number quotient; the modulus operator gives the remainder.", ("23 // 7", "3")), [
  (W, "Integer division splits a division into a whole-number quotient and a remainder. Floor division, written //, gives the quotient rounded down, and the modulus operator, written %%, gives the remainder %s." % SW),
  (Y, "Many problems ask how many whole groups fit and what is left over: packing items into boxes, converting seconds to minutes, splitting a total into equal parts. Floor division and the modulus operator answer exactly those two questions."),
  (E, "They appear in clock and calendar arithmetic and in any program that must divide a quantity into whole units."),
  (H, "For 23 and 7 the quotient 23 // 7 is 3 and the remainder 23 % 7 is 2, because 3 * 7 + 2 equals 23. True division gives 23 / 7 = 3.2857142857142856, which is a float."),
  (K, "Floor division rounds down, not toward zero: -7 // 2 evaluates to -4, because -3.5 rounded downward is -4 %s." % PSF),
 ]),
 ("TextOperation", None, 2, "Operation", None, [
  (W, "Text operations build new strings from existing ones. Two operators work on strings in the chapter: + joins them and * repeats them, which the chapter calls string concatenation and string replication %s." % SW),
  (Y, "Joining and repeating are enough to assemble a sentence from pieces or to draw a line of dashes, and they show that one operator symbol can mean different things for different types."),
  (H, "Both operations return a new string and leave the original strings unchanged. The operator + needs two strings, and the operator * needs a string and an integer."),
 ], None),
 ("Concatenation", None, 3, "TextOperation", ("'Alice' + 'Bob'", "Joining two strings with +. Joining a string to a number raises a TypeError.", ("'Alice' + 'Bob'", "'AliceBob'")), [
  (W, "String concatenation joins two strings into one with the + operator, so 'Alice' + 'Bob' gives 'AliceBob' %s." % SW),
  (Y, "Programs constantly assemble messages from pieces such as a greeting, a name and some punctuation, and concatenation is the plainest way to do it."),
  (E, "Concatenation appears in output messages, in prompts and file names, and in any line that mixes literal text with the contents of a variable."),
  (H, "Python creates a new string that holds the characters of the left string followed by those of the right one. No space is added, so 'Hello' + 'world' gives 'Helloworld' and a space has to be part of one of the strings."),
  (K, "Both operands must be strings. The expression 'Alice' + 42 raises a TypeError, because Python does not convert types silently; convert the number with str, or use an f-string %s." % SW),
 ]),
 ("Replication", None, 3, "TextOperation", ("'Alice' * 3", "Repeating a string an integer number of times with *.", ("'Alice' * 3", "'AliceAliceAlice'")), [
  (W, "String replication repeats a string a whole number of times with the * operator, so 'Alice' * 3 gives 'AliceAliceAlice' %s." % SW),
  (Y, "Replication builds repeated patterns without typing them out, for example a row of dashes under a title or a padding of spaces."),
  (E, "Replication appears in the layout of text output, in the separators of printed tables and in small demonstrations that one operator can mean something different for strings than for numbers."),
  (H, "The operands are a string and an integer, in either order, and the integer says how many copies to make. A count of zero or less gives the empty string, because values of n less than 0 are treated as 0 %s." % PSF),
  (K, "The count must be an integer. The expression 'Alice' * 2.5 raises a TypeError, and multiplying two strings is not allowed either."),
 ]),
 ("BindingOperation", None, 2, "Operation", None, [
  (W, "A binding operation gives a value a name, so that later lines can refer to it. In Python the main binding operation is the assignment statement %s." % SW),
  (Y, "Without names every value would have to be recomputed or retyped each time it was needed. Binding lets a program keep results, reuse them and give them meaning."),
  (H, "The language reference puts the idea briefly: names refer to objects, and names are introduced by name binding operations %s. The chapter's section Storing Values in Variables introduces the idea with the equals sign." % PSF),
 ], None),
 ("Variable", None, 3, "BindingOperation", ("spam = 42", "A name that refers to a value; assigning to the name again makes it refer to a new value.", None), [
  (W, "A variable is a name that refers to a value stored in the computer's memory. After spam = 42, the name spam refers to the integer 42 and can be used wherever that value is needed %s." % SW),
  (Y, "Variables let a program remember results, reuse them in later expressions and describe them with meaningful words, so that tax_rate is easier to understand than a bare 0.125."),
  (E, "Variables appear on nearly every line of a program: on the left of an assignment, inside expressions, as the arguments of function calls and inside f-strings."),
  (H, "Python's language reference says that names refer to objects %s. Assigning again with the same name makes it refer to a new value, and a name that was never assigned cannot be used: reading it raises a NameError." % PSF),
  (K, "Variable names are case-sensitive, cannot contain spaces and cannot start with a digit. PEP 8 recommends lowercase words separated by underscores, as in my_age %s." % PEP8),
 ]),
 ("Assignment", None, 3, "BindingOperation", ("spam = 42", "Storing a value in a variable with =; the variable names the value, and the name follows PEP 8's lower_case convention.", None), [
  (W, "An assignment statement stores a value in a variable with the equals sign. In spam = 42 the name on the left is bound to the value of the expression on the right %s." % SW),
  (Y, "Assignment is how a program keeps a result: the answer of one expression is stored so that later expressions can use it."),
  (E, "Assignment is the most common statement in the chapter's programs. The first program assigns the user's name and age, and every later chapter builds on the same form."),
  (H, "Python evaluates the right-hand side first and only then binds the name, so spam = spam + 1 reads the old value, adds one and stores the result under the same name. The assignment itself produces no value to print."),
  (K, "The equals sign is not mathematical equality. It means store, not compare, and a program that needs to compare two values uses a different operator that a later chapter introduces."),
 ]),
 ("BuiltInFunction", "Built-in function", 1, None, None, [
  (W, "A built-in function is a function that Python provides ready to use, without importing anything. The chapter's first program uses six of them: print, input, len, str, int and float %s." % PSF),
  (Y, "Built-in functions give a program its first abilities to communicate and convert: showing text, reading the user's answer, measuring a string and changing a value from one type to another."),
  (E, "They are available in every Python program and in the interactive shell, and the sections Your First Program and Dissecting the Program walk through them line by line."),
  (H, "A built-in function is used by calling it: its name is followed by parentheses that hold the arguments. The call is an expression, so its result can be stored, printed or used inside a larger expression."),
 ], None),
 ("CallMechanism", "Calling a function", 2, "BuiltInFunction", None, [
  (W, "Calling a function means asking Python to run it now, with given values. The call is written as the function's name followed by parentheses, and the values inside the parentheses are the arguments %s." % PSF),
  (Y, "Calling is how a program reuses work that has already been written, whether Python wrote it or the learner did, instead of repeating the steps each time."),
  (H, "The next section explains a function call in detail: what goes in, what comes out and how a call fits inside an expression."),
 ], None),
 ("FunctionCall", "Function call", 3, "CallMechanism", ("round(3.14159, 2)", "Running a function by writing its name followed by parentheses that hold its arguments; the call evaluates to the function's return value.", ("round(3.14159, 2)", "3.14")), [
  (W, "A function call runs a function with the values given inside parentheses, called its arguments, and the call evaluates to the function's return value. In round(3.14159, 2) the name round is the function, 3.14159 and 2 are the arguments, and the value is 3.14 %s." % PSF),
  (Y, "Function calls let a program use ready-made solutions: measuring a string, converting a type, rounding a number. A learner who can read a call can read most lines of a beginner's program."),
  (E, "A call can stand alone as a statement, as in print('Hello'), or sit inside an expression, as in len(name) + 1, and one call can contain another, as in int(input())."),
  (H, "Python evaluates the arguments first and then runs the function with them. A function returns a value to the place where it was called; if its code ends without a return statement the value is None %s. The print function returns None, so a call to print is used for what it does and not for what it returns." % PSF),
  (K, "The parentheses are required. Writing print without them does not call the function; it only names it, and a program that does this displays nothing."),
 ]),
 ("IOFunction", "Input-output function", 2, "BuiltInFunction", None, [
  (W, "Input-output functions connect a program to its user: print sends text out, and input reads text in %s." % SW),
  (Y, "A program that cannot show results or ask questions cannot be used by anyone. Input and output are the two directions of every conversation between a program and its user."),
  (H, "Both functions work with text. print turns its arguments into strings and writes them, and input returns whatever the user typed as a string, so numbers read from the keyboard must be converted before they are used in arithmetic."),
 ], None),
 ("Output", None, 3, "IOFunction", ("print('Hello, world!')", "print() writes its arguments as text to the screen.", None), [
  (W, "The print function writes its arguments to the screen as text. The call print('Hello, world!') displays Hello, world! and then moves to a new line %s." % PSF),
  (Y, "Output is how a program reports what it has done. Without print, a program run from a file would compute silently and its user would see nothing."),
  (E, "print appears in the chapter's first program, in nearly every example of the course, and as a simple way to look inside a program that misbehaves."),
  (H, "All arguments are converted to strings as str does and written one after another, separated by a space and followed by a new line, because the keyword arguments sep and end default to a space and a newline %s." % PSF),
  (K, "In the interactive shell a bare expression is displayed automatically, but in a saved program only print produces output: an expression on a line of its own is evaluated and its value is thrown away."),
 ]),
 ("Input", None, 3, "IOFunction", ("input() reading a name", "input() waits for the user to type and always returns a string - input as text.", None), [
  (W, "The input function waits for the user to type a line and returns it. If it is given a prompt, input writes that text first, without a trailing newline %s." % PSF),
  (Y, "Input is what lets one program serve many people: the same code can greet any name or calculate with any age that the user supplies."),
  (E, "The chapter's first program uses it twice, to read a name and an age, and the Playground and the Step through view of this page supply the typed lines for you."),
  (H, "input reads a line from the keyboard, strips the trailing newline and returns the rest as a string %s. Whatever the user types, even 20, arrives as text." % PSF),
  (K, "Because the result is always a string, adding 1 to it fails, and int(input()) is the usual way to read a whole number. Typing something that is not a whole number then raises a ValueError."),
 ]),
 ("ConversionFunction", None, 2, "BuiltInFunction", None, [
  (W, "Conversion functions change a value from one data type to another. The chapter uses three of them: str, int and float %s." % PSF),
  (Y, "Values arrive and leave as text, yet arithmetic needs numbers and messages need strings, so conversion is the bridge between the two."),
  (H, "Each function takes a value and returns a new one of its own type, leaving the original unchanged: int('42') returns the integer 42, float('3.5') returns the float 3.5 and str(29) returns the string '29'."),
 ], None),
 ("TypeConversion", None, 3, "ConversionFunction", ("int('42')", "str(), int() and float() convert a value between types; int() refuses a string that is not a whole number.", ("int('42')", "42")), [
  (W, "Type conversion produces a value of another type from an existing one. The call int('42') gives the integer 42, float('3.5') gives the float 3.5 and str(29) gives the string '29' %s." % PSF),
  (Y, "Without conversion, text from the keyboard could not be used in arithmetic and numbers could not be joined into a message."),
  (E, "Conversion appears wherever input is read as a number, as in int(input()), and wherever a number is placed into a message, as in str(age)."),
  (H, "The conversion function reads the value it is given and builds a new one; it does not change the original. The function int refuses text that is not a whole number: int('4.2') raises a ValueError, whereas int(4.7) is 4 because converting a float discards its fraction."),
  (K, "Converting the float 4.7 with int does not round it: round(4.7) is 5 while int(4.7) is 4. Use the function that matches the intention."),
 ]),
 ("MeasurementFunction", None, 2, "BuiltInFunction", None, [
  (W, "A measurement function reports a property of a value without changing it. The first one the chapter uses is len %s." % SW),
  (Y, "Knowing the size of a value is the starting point of many decisions, such as whether a password is long enough or whether a name fits a label."),
  (H, "The function len takes one argument and returns a whole number, the number of items in it; for a string the items are characters. Later chapters use the same function on lists and dictionaries."),
 ], None),
 ("Length", None, 3, "MeasurementFunction", ("len('hello')", "len() returns the number of characters in a string.", ("len('hello')", "5")), [
  (W, "The len function returns the number of items in an object; for a string it is the number of characters, so len('hello') is 5 %s." % PSF),
  (Y, "Counting characters answers practical questions, such as whether a name is empty or a text is too long for a field."),
  (E, "The function len is used on strings in this chapter and on lists, dictionaries and other collections in later ones."),
  (H, "The function counts every character, including spaces and punctuation, and returns an integer, so len('a b') is 3. The result can be used in arithmetic, or joined into a message after conversion with str."),
  (K, "The function len counts the characters of a string, not the digits of a number: len(12345) raises a TypeError, while len(str(12345)) is 5."),
 ]),
 ("ExecutionEnvironment", None, 1, None, None, [
  (W, "An execution environment is the software that reads a Python program and carries it out: the interpreter, the way it was built and the version in use. The same program can behave slightly differently in different environments."),
  (Y, "Where code runs matters as much as what it says. The Python that students run in 2026 is newer than the one the chapter describes, so what they see on the screen may differ from the book's pages: Python 3.14 is a current release and the first release of 3.15 is scheduled for 1 October 2026 %s." % PSF),
  (E, "The environment is met the first time Python is started, in the interactive shell, and again every time a script is run, a package is installed or a version is chosen."),
  (H, "The sections below explain the shell in which expressions are typed, the interpreter and its CPython implementation, the builds that decide how threads can run, and the version and proposal system that governs how Python changes."),
 ], None),
 ("InteractiveEnvironment", None, 2, "ExecutionEnvironment", None, [
  (W, "An interactive environment lets a learner type Python and see the result immediately. The chapter starts with Entering Expressions into the Interactive Shell, where each expression is evaluated as soon as it is entered %s." % SW),
  (Y, "Immediate feedback shortens the cycle of trying an idea and seeing whether it works, which is why interpreted languages typically have a shorter development and debugging cycle than compiled ones %s." % PSF),
  (H, "The environment reads a line, evaluates it, prints the result and waits for the next line. This is called the read-eval-print loop, or REPL %s." % PSF),
 ], None),
 ("InteractiveShell", None, 3, "InteractiveEnvironment", ("the Python 3.13+ interactive interpreter", "The shell that evaluates expressions as they are typed. Python 3.13 replaced it with a better interactive interpreter.", None), [
  (W, "The interactive shell is the program in which a learner types Python statements and expressions at a prompt and sees the results at once. It is also called the interactive interpreter or the REPL, an acronym for read-eval-print loop %s." % PSF),
  (Y, "The shell is the quickest place to test an idea, check what an expression does or explore a module, and it removes the need to save and run a file for a one-line experiment."),
  (E, "The shell starts when python is run with no arguments, which is how the Python tutorial begins, and the Playground of this page offers the same experience in the browser."),
  (H, "In interactive mode the interpreter prompts with three greater-than signs (>>>) for a new command and with three dots (...) for continuation lines. The value of the last expression printed is kept in the variable _, so the next line can continue the calculation %s." % PSF),
  (C, "Python 3.13 replaced the shell with a new interactive interpreter that supports multiline editing with history, colour in prompts and tracebacks by default, and the commands help, exit and quit without parentheses %s." % PSF),
  (K, "A learner who cannot leave the shell can type quit(); the end-of-file key, Control-D on Unix or Control-Z on Windows, also works at the primary prompt %s." % PSF),
 ]),
 ("PythonImplementation", "Python implementation", 2, "ExecutionEnvironment", None, [
  (W, "Python is a language, and a Python implementation is a program that reads code written in that language and carries it out. The language defines what a program means; the implementation decides how the computer does it."),
  (Y, "Separating the two explains why code written for the language can run on more than one program, and why features such as the global interpreter lock or the interactive shell belong to an implementation and not to the language itself."),
  (H, "The implementation that students use is CPython. The next sections define the interpreter, name CPython and its alternatives, and describe the bytecode that CPython produces on the way."),
 ], None),
 ("PythonInterpreter", "Python interpreter", 3, "PythonImplementation", ("python3.14 script.py", "The program that reads Python source code and runs it, either line by line in the shell or from a file.", None), [
  (W, "The Python interpreter is the program that reads Python code and runs it. Python is an interpreted language, as opposed to a compiled one, which means that source files can be run directly without explicitly creating an executable first %s." % PSF),
  (Y, "Running source files directly gives interpreted languages a shorter development and debugging cycle than compiled ones, although their programs generally run more slowly %s. For a learner the benefit is immediate: write a line, run it and see the result." % PSF),
  (E, "The interpreter is started by typing a command such as python3.14 in a terminal. With no arguments it opens the interactive shell, with a file name it runs the script in that file, and python -c runs the statements given on the command line %s." % PSF),
  (H, "Inside the interpreter the source code is first compiled to bytecode, which a virtual machine then executes. The word interpreted is therefore a simplification, and the Python glossary itself admits that the distinction can be blurry because of the presence of the bytecode compiler %s." % PSF),
  (K, "A computer can hold several interpreters. The commands python, python3 and versioned names such as python3.14 may point to different versions, so a learner should check which one is running with python --version."),
 ]),
 ("CPython", "CPython", 3, "PythonImplementation", ("sys.implementation.name", "The canonical implementation of Python as distributed on python.org; the name distinguishes it from others such as Jython or IronPython.", None), [
  (W, "CPython is the canonical implementation of the Python programming language, as distributed on python.org. The name CPython is used when it is necessary to distinguish this implementation from others such as Jython or IronPython %s." % PSF),
  (Y, "Unless it says otherwise, this course means CPython when it says Python: CPython is the reference interpreter for which the core developers write the language's design documents %s. Knowing the name explains why the global interpreter lock, bytecode and the free-threaded build are described as features of CPython." % WARSAW),
  (E, "A learner meets CPython by downloading Python from python.org or by installing it with a tool such as uv. The name appears in sys.implementation.name, which holds 'cpython', and in the release notes of every version."),
  (H, "CPython compiles Python source code to bytecode, the internal representation of a program in the CPython interpreter, and a virtual machine executes that bytecode %s. It can be built in more than one way: the default build has a global interpreter lock, and the free-threaded build, available from Python 3.13, does not." % PSF),
  (K, "Bytecode is specific to CPython and its version: bytecodes are not expected to work between different Python virtual machines, nor to be stable between Python releases %s." % PSF),
 ]),
 ("Bytecode", None, 3, "PythonImplementation", ("dis.dis('a + b * 2')", "The internal representation of a program inside CPython, produced by compiling source code and executed by a virtual machine.", None), [
  (W, "Bytecode is the internal representation of a Python program inside the CPython interpreter. Python source code is compiled into bytecode, which is said to run on a virtual machine that executes the machine code corresponding to each bytecode %s." % PSF),
  (Y, "Compiling once to a compact internal form lets CPython run the same program repeatedly without reading the source text again: the bytecode is cached in .pyc files, so executing the same file is faster the second time %s." % PSF),
  (E, "A learner rarely sees bytecode, but the dis module can display it. Under Python 3.14 the call dis.dis('a + b * 2') lists instructions that load the names a and b and the number 2, multiply, and only then add, which is the order that precedence demands."),
  (H, "The compiler turns each statement into a short list of such instructions, and the virtual machine, a computer defined entirely in software, executes them one by one %s." % PSF),
  (K, "Bytecode is an implementation detail. The instruction names change between Python releases, so programs should never depend on them %s." % PSF),
 ]),
 ("InterpreterBuild", None, 2, "ExecutionEnvironment", None, [
  (W, "An interpreter build is one particular way of compiling the CPython interpreter from its source code. The default build and the free-threaded build behave alike for most programs but differ in how threads can use the processor %s." % PSF),
  (Y, "The build decides how programs can use the machine, and it is the reason a course on advanced Python has to explain threads and the global interpreter lock before it can explain multithreading."),
  (H, "A build is chosen when CPython is compiled, with configuration options such as --disable-gil, and a user can tell which one is running from the output of python -VV or by calling sys._is_gil_enabled() %s." % PSF),
 ], None),
 ("Thread", None, 3, "InterpreterBuild", ("threading.Thread(target=f)", "A separate flow of execution inside one program; all threads of a program share the same memory.", None), [
  (W, "A thread is a separate flow of execution inside one program, so that several activities can be in progress at once. In the threading module the Thread class represents an activity that is run in a separate thread of control %s." % PSF),
  (Y, "Threads let a program keep working while one activity waits, for example while a file is read or an answer arrives over a network, and on a machine with several processor cores they can in principle run at the same moment."),
  (E, "Programs use threads for tasks that wait on input and output, such as downloading several pages, and the threading module is the standard way to start them. The course returns to multithreading later."),
  (H, "All threads of a program share the same memory space, because the threading module operates within a single process %s. A thread is started by calling its start method, and another thread can wait for it to finish with join." % PSF),
  (K, "Because threads share memory, two threads that change the same value can disturb each other. Built-in types in the free-threaded build use internal locks, yet the documentation recommends threading.Lock or other synchronization primitives instead of relying on them %s." % PSF),
 ]),
 ("GlobalInterpreterLock", "Global interpreter lock", 3, "InterpreterBuild", ("sys._is_gil_enabled()", "The lock that lets only one thread run Python bytecode at a time in the default CPython build.", None), [
  (W, "The global interpreter lock, or GIL, is the mechanism the CPython interpreter uses to ensure that only one thread executes Python bytecode at a time %s." % PSF),
  (Y, "The lock simplifies the CPython implementation by making the object model, including critical built-in types such as dict, implicitly safe against concurrent access. The price is that much of the parallelism offered by multi-processor machines is lost %s." % PSF),
  (E, "The GIL matters whenever a program uses several threads for computation: PEP 703 calls it an obstacle to using multi-core CPUs from Python efficiently %s. It matters much less for programs that wait on input and output, because the GIL is always released when doing I/O %s." % (GROSS, PSF)),
  (H, "A thread must hold the GIL to run Python bytecode, and the other threads wait for their turn. Some extension modules release the GIL during heavy work such as compression or hashing, and since Python 3.13 the GIL can be disabled in a free-threaded build %s." % PSF),
  (K, "The GIL is a mechanism of the CPython interpreter, not a rule of the language, and the default build of CPython still has it."),
 ]),
 ("FreeThreadedBuild", "Free-threaded build", 3, "InterpreterBuild", ("a CPython built with --disable-gil", "A build of CPython, configured with --disable-gil, in which several threads can run Python bytecode at the same time.", None), [
  (W, "A free-threaded build is a build of CPython that supports free threading, a threading model in which multiple threads can run Python bytecode simultaneously within the same interpreter. It is configured with the --disable-gil option before compilation %s." % PSF),
  (Y, "Free-threaded execution allows full use of the available processing power by running threads in parallel on the available CPU cores. Programs designed with threading in mind run faster on multi-core hardware, although not all software benefits automatically %s." % PSF),
  (E, "Since Python 3.13 the official macOS and Windows installers can optionally install free-threaded binaries, and the executable is usually named python3.13t. Python 3.14 made free-threaded Python officially supported %s." % PSF),
  (H, "PEP 703 proposed making the GIL optional, and PEP 779 set the criteria for supported status. The work has three phases: phase I made the free-threaded build available but explicitly experimental, phase II makes it officially supported but still optional, and phase III would make it the default %s." % WOUTERS),
  (K, "Some third-party packages with an extension module may not be ready for a free-threaded build, and importing such a module can switch the GIL back on with a warning %s." % PSF),
 ]),
 ("PythonRelease", "Python release", 2, "ExecutionEnvironment", None, [
  (W, "A Python release is a published version of the language and its interpreter, identified by a version number, together with the proposals and the schedule that lead up to it."),
  (Y, "Features, error messages and even the interactive shell change between releases, so a learner needs to know which release is in use and which releases are still supported."),
  (H, "Each release follows a documented schedule: a first release date, a period in which bugs are fixed, a period in which only security fixes are made, and an end-of-life date %s. Changes to the language are proposed in Python Enhancement Proposals." % PSF),
 ], None),
 ("PythonVersion", "Python version", 3, "PythonRelease", ("python --version", "The number that identifies a Python release, such as 3.14.4; sys.version_info reports its major, minor and micro parts.", None), [
  (W, "A Python version is the number that identifies a release, such as 3.14.4. Python reports it with python --version, and a program can read it from sys.version_info, whose fields include major, minor and micro."),
  (Y, "The version decides which features a program can use. Python 3.13 introduced the new interactive interpreter and Python 3.14 made free-threaded Python officially supported, so a program written for a newer version may fail on an older one %s." % PSF),
  (E, "The version is shown in the banner when the shell starts, in the output of python --version and in the title of the documentation, which names the release it describes, for example 3.14.8."),
  (H, "The developer's guide lists every branch with a status. A new version is first released each October, bugfix releases follow, and security fixes continue until the end-of-life date five years after the first release: for 3.14 that is October 2030 %s." % PSF),
  (K, "The course uses 3.14, but the chapter's examples were run under both Python 3.12.3 and Python 3.14.4 and printed identical output, so an older installed version does not change the results shown here."),
 ]),
 ("PEP", "Python Enhancement Proposal", 3, "PythonRelease", ("PEP 8", "A design document that proposes a new feature for Python or records a design decision, such as PEP 8 for style.", None), [
  (W, "A Python Enhancement Proposal, or PEP, is a design document that provides information to the Python community or describes a new feature for Python or its processes or environment %s." % WARSAW),
  (Y, "PEPs are the primary mechanism for proposing major new features, for collecting community input on an issue and for documenting the design decisions that have gone into Python %s. They explain not only what Python does but why." % WARSAW),
  (E, "A learner meets PEPs in release notes and documentation. PEP 8 is the style guide for Python code, PEP 701 gave f-strings a formal grammar, PEP 703 made the global interpreter lock optional and PEP 779 set the criteria for supporting the free-threaded build."),
  (H, "The author of a PEP is responsible for building consensus within the community and documenting dissenting opinions. PEPs are maintained as text files in a versioned repository, so their revision history is the historical record of the proposal %s." % WARSAW),
  (K, "A PEP records a proposal and its status, not a promise. When the reference implementation is complete and incorporated into the main source code repository, the status changes to Final, and the Steering Council has the final authority over approval %s." % WARSAW),
 ]),
 ("ModernPractice", "Modern practice", 1, None, None, [
  (W, "Modern practice is the way Python programmers work today: the idioms that experienced developers prefer and the tools they use to install, run and organise code. An advanced course teaches this practice alongside the basics of the textbook."),
  (Y, "A student who learns only the basics writes code that works but looks dated, and a student who has never installed a package cannot use the libraries that make Python useful. Pairing each basic with its current counterpart avoids unlearning later."),
  (E, "The chapter's string building meets the f-string, and its first program meets the tooling that installs Python and the packages it needs."),
  (H, "Two branches follow: string formatting, which replaces repeated concatenation with a clearer form, and tooling, which covers packages, virtual environments and the package manager uv."),
 ], None),
 ("StringFormatting", None, 2, "ModernPractice", None, [
  (W, "String formatting builds a string out of text and values in one step. Building strings by concatenation works, but a formatted string literal lets a program write an expression between braces inside the string, and the Python tutorial notes that the older str.format() method requires more manual effort %s." % PSF),
  (Y, "Concatenation requires converting every number with str and keeping track of spaces, which is easy to get wrong. A format places each value where it belongs in the sentence and does the conversion itself."),
  (H, "Python 3.12 gave f-strings a formal grammar %s. The next section explains how an f-string is written and evaluated." % PEP701),
 ], None),
 ("FString", "F-string", 3, "StringFormatting", ("f'{2 ** 8}'", "An f-string evaluates expressions inside braces as it builds the string; PEP 701 gave f-strings a formal grammar.", ("f'{2 ** 8}'", "'256'")), [
  (W, "An f-string, short for formatted string literal, is a string literal prefixed with f or F whose braces hold expressions %s. Python evaluates each expression and inserts its value into the text, so f'{2 ** 8}' gives '256'." % PSF),
  (Y, "An f-string states in one place both the sentence the user will read and the values that fill it. It is shorter than concatenation, needs no str calls and keeps spaces and punctuation visible."),
  (E, "f-strings are the idiomatic way to build messages for print, such as f'It is good to meet you, {my_name}.' in the first program, and they appear throughout the examples of this course."),
  (H, "Python evaluates the expression inside each pair of braces when the string is built, converts the result to text and puts it in place. Any expression is allowed, so the braces can hold arithmetic or a function call, as in f'{len(name)} letters'. After a colon the braces can hold a format specification: f'{1 / 3:.2f}' gives '0.33'. PEP 701 gave f-strings a formal grammar in Python 3.12 %s." % PEP701),
  (K, "The prefix f is required. Without it the braces are ordinary characters, and 'It is {my_age}' prints the braces literally."),
 ]),
 ("Tooling", None, 2, "ModernPractice", None, [
  (W, "Tooling is the set of programs a Python developer uses around the language itself: to install interpreters and packages, to keep projects apart and to run code. Working with these tools is part of programming as much as writing code is."),
  (Y, "Much of Python's usefulness comes from packages written by others, so a learner who cannot install and isolate them is limited to the standard library."),
  (H, "The next sections explain what a package is, how a virtual environment keeps projects separate, and how a package manager automates both."),
 ], None),
 ("Package", None, 3, "Tooling", ("import random", "A Python module that can contain submodules; packages are how code is shared and installed, from the standard library to third-party libraries.", None), [
  (W, "A package is a Python module that can contain submodules or, recursively, subpackages. A module is an object that serves as an organizational unit of Python code, and it is loaded into a program by importing it %s." % PSF),
  (Y, "Packages let code be shared. The standard library is the collection of packages and modules distributed with the interpreter, and third-party packages add everything else that a project may need %s." % PSF),
  (E, "A program uses a package by importing it with an import statement, and a project installs the packages it needs with a package manager such as uv."),
  (H, "Python applications often use packages that do not come as part of the standard library, and they sometimes need a specific version of a library, for example because a particular bug has been fixed in it %s." % PSF),
  (K, "One Python installation cannot satisfy every application. If application A needs version 1.0 of a module and application B needs version 2.0, installing either one leaves the other unable to run, which is the problem a virtual environment solves %s." % PSF),
 ]),
 ("VirtualEnvironment", "Virtual environment", 3, "Tooling", ("python -m venv .venv", "A self-contained directory with its own Python interpreter and packages, so that different projects can use different versions of the same library.", None), [
  (W, "A virtual environment is a self-contained directory tree that contains a Python installation for a particular version of Python, plus a number of additional packages %s." % PSF),
  (Y, "Different applications can use different virtual environments, so conflicting requirements stop mattering: application A can keep version 1.0 of a library while application B uses version 2.0, and upgrading one does not affect the other %s." % PSF),
  (E, "A common directory location for a virtual environment is .venv, inside the project folder. The uv tool creates one automatically: in its documentation the command uv add ruff reports Creating virtual environment at: .venv %s." % ASTRAL),
  (H, "The venv module creates and manages virtual environments. Running python -m venv tutorial-env makes the directory tutorial-env with a copy of the Python interpreter and supporting files inside it, for the Python version from which the command was run %s." % PSF),
  (K, "A virtual environment belongs to one project. The packages installed into it are not visible to other environments, and deleting its directory removes them."),
 ]),
 ("PackageManager", "Package manager", 3, "Tooling", ("uv", "A tool that installs Python packages and interpreters. uv, built in Rust, was the most admired technology in the 2025 Stack Overflow survey.", None), [
  (W, "A package manager is a tool that installs, upgrades and removes packages and keeps track of the versions a project needs. The tool uv is a package and project manager for Python, written in Rust, whose documentation promises a single tool to replace pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv and more %s." % ASTRAL),
  (Y, "Installing the right interpreter and the right package versions by hand is slow and easy to get wrong. The tool uv installs and manages Python versions, creates virtual environments, runs scripts and records a project's dependencies in a lockfile %s." % ASTRAL),
  (E, "The tool uv works on macOS, Linux and Windows. It was the most admired technology in the 2025 Stack Overflow Developer Survey at 74 per cent, and it installed the Python 3.14.4 that was used to check this chapter's examples %s." % SO),
  (H, "A project starts with uv init, packages are added with uv add and programs are run with uv run; each command works inside the project's virtual environment, which uv creates when it is needed %s." % ASTRAL),
  (K, "The tool uv presents itself as a replacement for tools such as pip and virtualenv, so a learner will meet those names in older documentation and should know that they do the same jobs separately."),
 ]),
]

# claims whose output is quoted in the texts above: (expression, expected repr). Run by the builders under Python 3.14.
CHECKS = [("7 + 1", "8"), ("6 / 3", "2.0"), ("4 * 3.75 - 1", "14.0"), ("2 ** 100", "1267650600228229401496703205376"),
 ("0.1 + 0.2", "0.30000000000000004"), ("round(0.1 + 0.2, 2)", "0.3"), ("2 + 3 * 6", "20"), ("(2 + 3) * 6", "30"), ("-3 ** 2", "-9"), ("(-3) ** 2", "9"),
 ("23 // 7", "3"), ("23 % 7", "2"), ("23 / 7", "3.2857142857142856"), ("-7 // 2", "-4"), ("7 // 2", "3"), ("7 / 2", "3.5"), ("7 % 3", "1"),
 ("3 * (2 + 4)", "18"), ("'Alice' + 'Bob'", "'AliceBob'"), ("'Hello' + 'world'", "'Helloworld'"), ("'Alice' * 3", "'AliceAliceAlice'"),
 ("'ab' * 0", "''"), ("'ab' * -1", "''"), ("3 * 'ab'", "'ababab'"), ("len('hello')", "5"), ("len('a b')", "3"), ("len(str(12345))", "5"),
 ("int('42')", "42"), ("float('3.5')", "3.5"), ("str(29)", "'29'"), ("int(4.7)", "4"), ("round(4.7)", "5"), ("round(3.14159, 2)", "3.14"),
 ("f'{2 ** 8}'", "'256'"), ("f'{1 / 3:.2f}'", "'0.33'"), ("type(7)", "<class 'int'>"), ("type(3.5)", "<class 'float'>"), ("type('Alice')", "<class 'str'>"),
 ("__import__('sys').implementation.name", "'cpython'"), ("print() is None", "True"), ("8 / 2 * 3", "12.0")]
RAISES = [("'7' + 1", "TypeError"), ("'Alice' + 42", "TypeError"), ("'Alice' * 2.5", "TypeError"), ("'a' * 'b'", "TypeError"), ("int('4.2')", "ValueError"),
 ("len(12345)", "TypeError"), ("spam = 1; Spam", "NameError"), ("never_assigned_name", "NameError"), ("1abc = 3", "SyntaxError"), ("my age = 3", "SyntaxError")]

def facet_text(paras):
    return "\n\n".join("%s: %s" % (f, t) for f, t in paras)

if __name__ == "__main__":
    import subprocess, sys
    py = sys.argv[1] if len(sys.argv) > 1 else "python3.14"
    code = "import json\nout=[]\nfor e,x in %r:\n    out.append((e,repr(eval(e))==x or repr(eval(e))))\nfor e,x in %r:\n    try:\n        exec(e) if '=' in e and '==' not in e else eval(e)\n        out.append((e,'no error'))\n    except BaseException as ex:\n        out.append((e,type(ex).__name__==x or type(ex).__name__))\nprint(json.dumps(out))" % (CHECKS, RAISES)
    res = __import__("json").loads(subprocess.run([py, "-c", code], capture_output=True, text=True).stdout)
    bad = [r for r in res if r[1] is not True]
    print(len(res), "claims executed under", subprocess.run([py, "--version"], capture_output=True, text=True).stdout.strip(), "- failures:", bad)
    ids = [n[0] for n in NODES]; assert len(ids) == len(set(ids))
    print(len(NODES), "concepts;", sum(len(n[5]) for n in NODES), "paragraphs;", sum(len(t.split()) for n in NODES for f, t in n[5]), "words")
