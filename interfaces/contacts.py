from interfaces.base import interface
from models.contact import ContactDB, Contact

def main(db: ContactDB):
    interface((show_contacts, (db,)), [
        ['Добавить контакт', add_contact, [db], False],
        ['Поиск контакта', search_contact, [db], False],
        ['Перейти к контакту', go_to_contact, (db,), False],
        ['Экспортировать в CSV', export_contacts_csv, [db], False],
        ['Импортировать из CSV', import_contacts_csv, [db], False]
    ])


def show_contacts(db: ContactDB):
    contacts = db.get_all()
    return '\n'.join([f'ID: {c.id}, Name: {c.name}, Phone: {c.phone}, Email: {c.email}' for c in contacts])


def go_to_contact(db: ContactDB):
    contact_id = int(input('Введите ID контакта: '))
    if db.get(contact_id):
        interface((show_contact_details, (db, contact_id)), [
            ['Редактировать контакт', edit_contact, (db, contact_id), False],
            ['Удалить контакт', delete_contact, (db, contact_id), True]
        ])
    else:
        print('Контакт не найден.')
        input()

def add_contact(db: ContactDB):
    name = input('Введите имя контакта: ')
    if not name:
        print('Ошибка: имя контакта обязательно.')
        input()
        return
    
    phone = input('Введите номер телефона (оставьте пустым если нет): ')
    email = input('Введите адрес электронной почты (оставьте пустым если нет): ')
    
    contact = Contact(name=name, phone=phone, email=email)
    db.add(contact)
    print('Контакт добавлен.')

def search_contact(db: ContactDB):
    query = input('Введите имя или номер телефона для поиска: ')
    results = [contact for contact in db.get_all() if query in (contact.name, contact.phone)]
    
    if results:
        print('Найденные контакты:')
        for c in results:
            print(f'ID: {c.id}, Name: {c.name}, Phone: {c.phone}, Email: {c.email}')
        input()
    else:
        print('Контакты не найдены.')
        input()

def show_contact_details(db: ContactDB, contact_id):
    contact = db.get(contact_id)
    if contact:
        res = (f"ID: {contact.id}\n"
               f"Name: {contact.name}\n"
               f"Phone: {contact.phone}\n"
               f"Email: {contact.email}\n")
        return res
    else:
        return "Контакт не найден."

def edit_contact(db: ContactDB, contact_id):
    contact = db.get(contact_id)
    
    if not contact:
        print('Контакт не найден.')
        return
    
    name_input = input(f'Введите новое имя (текущее: {contact.name}): ')
    phone_input = input(f'Введите новый номер телефона (текущий: {contact.phone}): ')
    email_input = input(f'Введите новый адрес электронной почты (текущий: {contact.email}): ')
    
    db.edit(
         contact_id,
         name=name_input if name_input else None,
         phone=phone_input if phone_input else None,
         email=email_input if email_input else None
     )
    
    print('Контакт обновлен.')

def delete_contact(db: ContactDB, contact_id):
    if db.delete(contact_id):
        print('Контакт удален.')
    else:
        print('Контакт не найден.')

def export_contacts_csv(db: ContactDB):
    path = input('Введите путь до файла для экспорта контактов в CSV: ')
    db.export_csv(path)
    print('Контакты экспортированы.')

def import_contacts_csv(db: ContactDB):
    path = input('Введите путь до файла для импорта контактов из CSV: ')
    db.import_csv(path)
    print('Контакты импортированы.')

