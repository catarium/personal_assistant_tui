from interfaces.base import interface
from models.note import Note, NoteDB
from interfaces.note import main as note_interface
import re

res = None

def main():
    interface((lambda: res, []), [
        ['Ввести выражение', math, [], False],])

def math():
    global res
    inp = input('Введите ваше выражение: ')
    if re.search(r"(\d|\s|\*|/|\+|-)+", inp).group(0) != inp:
        print('Ошибка синтаксиса')
        input()
    res = eval(inp)

