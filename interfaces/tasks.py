from interfaces.base import interface
from models.task import Task, TaskDB
from interfaces.task import main as task_interface 


def main(db: TaskDB):
    interface((show_list, (db,)), [
        ['Добавить задачу', add, [db], False], 
        ['Перейти к задаче', go_to_task, (db,), False], 
        ['Отметить задачу', remark, (db,), False], 
        ['Отфильтровать', filter_tasks, [], False], 
        ['Экспортировать в CSV', export_csv, (db,), False],
        ['Импортировать из CSV', import_csv, (db,), False]])


rule = {}


def show_list(db: TaskDB):
    data = db.get_all()
    for k, v in rule.items():
        data = list(filter(lambda x: getattr(x, k) == v, data))
    return '\n'.join([f'{r.id}    {r.title}    {r.priority}    {r.due_date}    {r.done}' for r in data])


def go_to_task(db):
    task_id = int(input('Введите id задачи: '))
    task_interface(db, task_id)


def add(db: TaskDB):
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
    done = False
    task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            done=done
            )
    db.add(task)


def remark(db: TaskDB):
    task_id = int(input('Введите id задачи: '))
    task = db.get(task_id)
    if not task_id:
        return
    db.edit(task_id=task.id, 
            title=task.title, 
            description=task.description, 
            priority=task.priority, 
            due_date=task.due_date, 
            done=not task.done)


def filter_tasks():
    global rule
    rule = {}
    done = input('Введите статус выполненный (1) не выполненный (0): ')
    if done != '':
        rule['done'] = bool(int(done))
    due_date = input('Введите срок выполнения: ')
    if due_date:
        rule['due_date'] = due_date
    priority = input('Задайте уровень приоритета от 1 до 3: ')
    match priority:
        case '1':
            priority = 'Низкий'
        case '2':
            priority = 'Средний'
        case '3':
            priority = 'Высокий'
        case '':
            priority = ''
        case _:
            print('Ошибка: неверный ввод')
            input()
            return
    if priority:
        rule['priority'] = priority
    print(rule)
    input()


def export_csv(db: TaskDB):
    path = input('Введите путь до файла: ')
    db.export_csv(path)


def import_csv(db: TaskDB):
    path = input('Введите путь до файла: ')
    db.import_csv(path)

