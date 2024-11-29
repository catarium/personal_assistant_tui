from interfaces.base import interface
from models.finance import FinanceRecord, FinanceDB
from interfaces.finance import main as finance_interface
import datetime


rule = []

def main(db: FinanceDB):
    interface((show_list, (db,)), [
        ['Добавить запись', add_record, [db], False], 
        ['Просмотреть запись', view_record, (db,), False], 
        ['Фильтровать записи', filter_records, (db,), False],
        ['Фин отчетность', fin_stats, (db,), False], 
        ['Экспортировать в CSV', export_csv, (db,), False],
        ['Импортировать из CSV', import_csv, (db,), False]
    ])

def show_list(db: FinanceDB):
    data = db.get_all()
    for f in rule:
        data = list(filter(f, data))
    return '\n'.join([f'{r.id}    {r.amount}    {r.category}    {r.date}    {r.description}' for r in data])

def fin_stats(db: FinanceDB):
    data = db.get_all()
    for f in rule:
        data = list(filter(f, data))
    print((f"Расходы: {sum(filter(lambda x: x < 0, map(lambda x: x.amount, data)))}"))
    print((f"Доходы: {sum(filter(lambda x: x > 0, map(lambda x: x.amount, data)))}"))
    print((f"Итого: {sum(map(lambda x: x.amount, data))}"))
    input()

def view_record(db: FinanceDB):
    record_id = int(input('Введите id записи: '))
    finance_interface(db, record_id)

def add_record(db: FinanceDB):
    amount = float(input('Введите сумму (положительное число для доходов, отрицательное для расходов): '))
    category = input('Введите категорию операции: ')
    date = input('Введите дату операции (ДД-ММ-ГГГГ): ')
    description = input('Введите описание операции: ')
    
    record = FinanceRecord(amount=amount, category=category, date=date, description=description)
    db.add(record)




def filter_records(db):
    global rule
    rule.clear()
    
    category_input = input('Введите категорию для фильтрации (оставьте пустым для пропуска): ')
    if category_input:
        filt = input('Введите значение категории: ')
        rule.append(lambda x: getattr(x, category_input) == filt)

    start_date = input('Введите начальную дату для фильтрации (ДД-ММ-ГГГГ): ')
    end_date = input('Введите конечную дату для фильтрации (ДД-ММ-ГГГГ): ')


    def date_filter(record):
        record_date = datetime.datetime.strptime(record.date, '%d-%m-%Y')
        
        if start_date and end_date:
            start_date_dt = datetime.datetime.strptime(start_date, '%d-%m-%Y')
            end_date_dt = datetime.datetime.strptime(end_date, '%d-%m-%Y')
            print(start_date_dt <= record_date <= end_date_dt)
            if start_date_dt <= record_date <= end_date_dt:
                return True
        elif start_date and not end_date and datetime.datetime.strptime(start_date, '%d-%m-%Y') <= record_date:
            return True
        elif end_date and not start_date and record_date <= datetime.datetime.strptime(end_date, '%d-%m-%Y'):
            return True
        return False

    rule.append(date_filter)


def export_csv(db: FinanceDB):
    path = input('Введите путь до файла для экспорта: ')
    db.export_csv(path)

def import_csv(db: FinanceDB):
    path = input('Введите путь до файла для импорта: ')
    db.import_csv(path)
