import json
import csv


class Contact:
    def __init__(self, name: str, phone: str = '', email: str = '', contact_id=None):
        self.id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

    def get_data(self):
        return {
            'contact_id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }

    def set_id(self, contact_id):
        self.id = contact_id


class ContactDB:
    def __init__(self, filename: str):
        self.filename = filename
        try:
            with open(filename) as f:
                json_data = json.load(f)
                self.data = [Contact(**el) for el in json_data]
        except FileNotFoundError:
            self.data = []

    def dump(self):
        with open(self.filename, 'w') as f:
            json_data = [contact.get_data() for contact in self.data]
            json.dump(json_data, f)

    def get(self, contact_id):
        return next((contact for contact in self.data if contact.id == contact_id), None)

    def get_all(self):
        return self.data

    def add(self, contact: Contact):
        try:
            contact.set_id(self.data[-1].id + 1)
        except IndexError:
            contact.set_id(1)
        self.data.append(contact)
        self.dump()

    def edit(self, contact_id, name=None, phone=None, email=None):
        contact = self.get(contact_id)
        if not contact:
            return None
        
        if name is not None:
            contact.name = name
        if phone is not None:
            contact.phone = phone
        if email is not None:
            contact.email = email
        
        self.dump()

    def delete(self, contact_id):
        contact = self.get(contact_id)
        if not contact:
            return None
        self.data.remove(contact)
        self.dump()

    def export_csv(self, path):
        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['contact_id', 'name', 'phone', 'email'])
            writer.writeheader()
            writer.writerows([contact.get_data() for contact in self.data])

    def import_csv(self, path):
        with open(path) as f:
            reader = csv.DictReader(f)
            for el in reader:
                el['contact_id'] = None  # ID будет установлен автоматически при добавлении
                contact = Contact(**el)
                try:
                    contact.set_id(self.data[-1].id + 1)
                except IndexError:
                    contact.set_id(1)
                self.data.append(contact)
        self.dump()
