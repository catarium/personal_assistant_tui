import json
import datetime
import csv


class Note:
    def __init__(self, title: str, content: str, note_id=None, timestamp=None):
        self.id = note_id
        self.title = title
        self.content = content
        if not timestamp:
            self.timestamp = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
        else:
            self.timestamp = timestamp

    def get_data(self):
        return {
                'title': self.title,
                'content': self.content,
                'timestamp': self.content
                }

    def set_id(self, note_id):
        self.id = note_id


class NoteDB:
    def __init__(self, filename: str):
        self.filename = filename
        with open(filename) as f:
            json_data = json.load(f)
            self.data = [Note(**el) for el in json_data]

    def dump(self):
        with open(self.filename, 'w') as f:
            json_data = [{'note_id': el.id,
                          'title': el.title,
                          'content': el.content,
                          'timestamp': el.timestamp} 
                         for el in self.data]
            json.dump(json_data, f)

    def get(self, note_id):
        try:
            return list(filter(lambda x: x.id == note_id, self.data))[0]
        except IndexError:
            return None

    def get_all(self):
        return self.data

    def add(self, note: Note):
        try:
            note.set_id(self.data[-1].id + 1)
        except IndexError:
            note.set_id(1)
        self.data.append(note)
        self.dump()

    def edit(self, note_id, title, content):
        try:
            old_note =  next(filter(lambda x: x.id == note_id, self.data))
        except StopIteration:
            return None
        note = Note(title, content)
        note.set_id(note_id)
        self.data.insert(self.data.index(old_note), note)
        self.data.remove(old_note)
        self.dump()

    def delete(self, note_id):
        try:
            note =  next(filter(lambda x: x.id == note_id, self.data))
        except StopIteration:
            return None
        self.data.remove(note)
        self.dump()

    def export_csv(self, path):
        with open(self.filename) as f:
            json_data = json.load(f)
        with open(path, 'w') as f:
            writer = csv.DictWriter(f, ['note_id', 'title', 'content', 'timestamp'])
            writer.writerow({'note_id': 'note_id', 'title': 'title', 'content': 'content', 'timestamp': 'timestamp'})
            writer.writerows(json_data)

    def import_csv(self, path):
        with open(path) as f:
            reader = csv.DictReader(f)
            for el in reader:
                el.pop('note_id', None)
                print(el)
                note = Note(**el)
                try:
                    note.set_id(self.data[-1].id + 1)
                except IndexError:
                    note.set_id(1)
                self.data.append(note)
        self.dump()

