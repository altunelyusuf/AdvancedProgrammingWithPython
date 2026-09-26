__version__ = "1.0.1"
# A first program, in the chapter's spirit: say hello, ask for a name, and use it.
print('Hello, world!')
print('What is your name?')
my_name = input()
print(f'It is good to meet you, {my_name}.')
print(f'The length of your name is {len(my_name)}.')
my_age = int(input('What is your age? '))
print(f'You will be {my_age + 1} in a year.')
