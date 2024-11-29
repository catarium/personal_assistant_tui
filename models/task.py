import json
import datetime
import csv


class Task:
    def __init__(self, title: str, 
                 priority: str, 
                 due_date: str, 
                 description: str|None = None, 
                 done: bool = False, 
                 task_id=None):
        self.id = task_id
        self.title = title
        self.description = description 
        self.priority = priority
        self.done = done
        self.due_date = due_date

    def get_data(self):
        return {
                'title': self.title,
                'content': self.content,
                'timestamp': self.content
                }

    def set_id(self, note_id):
        self.id = note_id


class TaskDB:
    def __init__(self, filename: str):
        self.filename = filename
        with open(filename) as f:
            json_data = json.load(f)
            self.data = [Task(**el) for el in json_data]

    def dump(self):
        with open(self.filename, 'w') as f:
            json_data = [{'task_id': el.id,
                          'title': el.title,
                          'description': el.description,
                          'priority': el.priority,
                          'due_date': el.due_date,
                          'done': el.done} 
                         for el in self.data]
            json.dump(json_data, f)

    def get(self, task_id):
        try:
            return list(filter(lambda x: x.id == task_id, self.data))[0]
        except IndexError:
            return None

    def get_all(self):
        return self.data

    def add(self, task: Task):
        try:
            task.set_id(self.data[-1].id + 1)
        except IndexError:
            task.set_id(1)
        self.data.append(task)
        self.dump()

    def edit(self, task_id, title, description, due_date, done, priority):
        try:
            old_note =  next(filter(lambda x: x.id == task_id, self.data))
        except StopIteration:
            return None
        note = Task(task_id=task_id,
                    title=title, 
                    description=description,
                    due_date=due_date,
                    done=done,
                    priority=priority)
        self.data.insert(self.data.index(old_note), note)
        self.data.remove(old_note)
        self.dump()

    def delete(self, task_id):
        try:
            task =  next(filter(lambda x: x.id == task_id, self.data))
        except StopIteration:
            return None
        self.data.remove(task)
        self.dump()

    def export_csv(self, path):
        with open(self.filename) as f:
            json_data = json.load(f)
        with open(path, 'w') as f:
            writer = csv.DictWriter(f, ['task_id', 'title', 'description', 'priority', 'due_date', 'done'])
            writer.writerow({'task_id': 'task_id', 
                             'title': 'title', 
                             'description': 'description', 
                             'priority': 'priority', 
                             'due_date': 'due_date', 
                             'done': 'done'})
            writer.writerows(json_data)

    def import_csv(self, path):
        with open(path) as f:
            reader = csv.DictReader(f)
            for el in reader:
                el.pop('note_id', None)
                print(el)
                task = Task(**el)
                try:
                    task.set_id(self.data[-1].id + 1)
                except IndexError:
                    task.set_id(1)
                self.data.append(task)
        self.dump()

