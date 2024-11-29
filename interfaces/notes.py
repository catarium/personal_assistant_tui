from interfaces.base import interface
from models.note import Note, NoteDB
from interfaces.note import main as note_interface


def main(db: NoteDB):
    interface((show_list, (db,)), [
        ['Добавить заметку', add, [db], False], 
        ['Перейти к заметке', go_to_note, (db,), False], 
        ['Экспортировать в CSV', export_csv, (db,), False],
        ['Импортировать из CSV', import_csv, (db,), False]])


def show_list(db: NoteDB):
    data = db.get_all()
    return '\n'.join([f'{r.id}    {r.title}    {r.timestamp}' for r in data])


def go_to_note(db):
    note_id = int(input('Введите id заметки: '))
    note_interface(db, note_id)


def add(db: NoteDB):
    title = input('Введите название: ')
    if not title:
        print('Ошибка: обязательное поле')
    content = input('Введите текст: ')
    note = Note(title, content)
    db.add(note)

def export_csv(db: NoteDB):
    path = input('Введите путь до файла: ')
    db.export_csv(path)

def import_csv(db: NoteDB):
    path = input('Введите путь до файла: ')
    db.import_csv(path)

