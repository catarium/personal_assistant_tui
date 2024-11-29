from models.finance import FinanceRecord, FinanceDB
from interfaces.base import interface


def main(db: FinanceDB, record_id):
    interface((show_record, (db, record_id)), [
        ['Изменить запись', edit_record, (db, record_id), False],
        ['Удалить запись', delete_record, (db, record_id), True]
    ])


def show_record(db: FinanceDB, record_id):
    record = db.get(record_id)
    if record:
        res = (f"id: {record.id}\n"
               f"amount: {record.amount}\n"
               f"category: {record.category}\n"
               f"date: {record.date}\n"
               f"description: {record.description}\n")
        return res
    else:
        return "Запись не найдена."


def edit_record(db: FinanceDB, record_id):
    record = db.get(record_id)
    
    if not record:
        print('Запись не найдена.')
        return
    
    amount_input = input(f'Введите новую сумму (текущая: {record.amount}): ')
    category_input = input(f'Введите новую категорию (текущая: {record.category}): ')
    date_input = input(f'Введите новую дату (текущая: {record.date}): ')
    description_input = input(f'Введите новое описание (текущее: {record.description}): ')
    
    db.edit(
        record_id,
        amount=float(amount_input) if amount_input else None,
        category=category_input if category_input else None,
        date=date_input if date_input else None,
        description=description_input if description_input else None
    )


def delete_record(db: FinanceDB, record_id):
    if db.delete(record_id):
        print('Запись удалена.')
    else:
        print('Запись не найдена.')
