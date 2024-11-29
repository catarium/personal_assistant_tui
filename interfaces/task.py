from models.task import Task, TaskDB
from interfaces.base import interface


def main(db: TaskDB, task_id):
    interface((show_note, (db, task_id)), [['Изменить', edit_note, (db, task_id), False],
                                           ['Отметить', remark, (db, task_id), False], 
                                           ['Удалить', delete_note, (db, task_id), True]])


def show_note(db: TaskDB, task_id):
    task = db.get(task_id)
    res = (f"id: {task_id}\n"
           f"title: {task.title}\n"
           f"due_date: {task.due_date}\n"
           f"priority: {task.priority}\n"
           f"done: {task.done}\n"
           f"description: {task.description}\n")
    return res


def edit_note(db, task_id):
    title = input('Введите название: ')
    if not title:
        print('Ошибка: обязательное поле')
        input()
        return
    description = input('Введите описание: ')
    priority = input('Задайте уровень приоритета от 1 до 3: ')
    match priority:
        case '1':
            priority = 'Низкий'
        case '2':
            priority = 'Средний'
        case '3':
            priority = 'Высокий'
        case _:
            print('Ошибка: неверный ввод')
            input()
            return
    due_date = input('Введите срок выполнения: ')
    done = bool(int(input('Введите статус выполнения выполнено (1) не выполнено (0): ')))
    db.edit(task_id=task_id, title=title, description=description, priority=priority, due_date=due_date, done=done)


def remark(db: TaskDB, task_id):
    task = db.get(task_id)
    if not task_id:
        return
    db.edit(task_id=task.id, 
            title=task.title, 
            description=task.description, 
            priority=task.priority, 
            due_date=task.due_date, 
            done=not task.done)


def delete_note(db, note_id):
    db.delete(note_id)

