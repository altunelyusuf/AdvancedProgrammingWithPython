command = input('Command: ')
match command.split():
    case ['go', direction]:
        print(f'going {direction}')
    case ['quit']:
        print('bye')
    case _:
        print('unknown command')
