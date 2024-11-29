from models.note import Note, NoteDB
from interfaces.base import interface


def main(db: NoteDB, note_id):
    interface((show_note, (db, note_id)), [['Изменить', edit_note, (db, note_id), False], ['Удалить', delete_note, (db, note_id), True]])


def show_note(db: NoteDB, note_id):
    note = db.get(note_id)
    res = (f"id: {note_id}\n"
           f"title: {note.title}\n"
           f"created/edited: {note.timestamp}\n"
           f"{note.content}")
    return res


def edit_note(db, note_id):
    title = input('Введите название: ')
    content = input('Введите текст: ')
    db.edit(note_id, title, content)


def delete_note(db, note_id):
    db.delete(note_id)

