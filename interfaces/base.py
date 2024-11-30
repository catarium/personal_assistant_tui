import os
import platform


def interface(text: list, actions: list[tuple]):
    actions.append(('Назад', lambda: None, [], True))
    if platform.system == 'Windows':
        command = 'cls'
    else:
        command = 'clear'
    while True:
        os.system(command)
        print(text[0](*text[1]))
        actions_out = '\n'.join([f'{i + 1}. {actions[i][0]}' for i in range(len(actions))])
        print(f'Выберите действие:')
        print(actions_out)
        try:
            inp = int(input())
            actions[inp - 1][1](*actions[inp - 1][2])
        except IndexError:
            print('invalid input')
            input()
            continue
        except ValueError:
            print('invalid input')
            input()
            continue
        if actions[inp - 1][3]:
            break


