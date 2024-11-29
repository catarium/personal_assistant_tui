import json
import datetime
import csv


class FinanceRecord:
    def __init__(self, amount: float, category: str, record_id=None, date=None, description: str = ''):
        self.id = record_id
        self.amount = amount
        self.category = category
        if not date:
            self.date = datetime.datetime.now().strftime('%d-%m-%Y')
        else:
            self.date = date
        self.description = description

    def get_data(self):
        return {
            'record_id': self.id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description
        }

    def set_id(self, record_id):
        self.id = record_id


class FinanceDB:
    def __init__(self, filename: str):
        self.filename = filename
        try:
            with open(filename) as f:
                json_data = json.load(f)
                self.data = [FinanceRecord(**el) for el in json_data]
        except FileNotFoundError:
            self.data = []

    def dump(self):
        with open(self.filename, 'w') as f:
            json_data = [record.get_data() for record in self.data]
            json.dump(json_data, f)

    def get(self, record_id):
        return next((record for record in self.data if record.id == record_id), None)

    def get_all(self):
        return self.data

    def add(self, record: FinanceRecord):
        try:
            record.set_id(self.data[-1].id + 1)
        except IndexError:
            record.set_id(1)
        self.data.append(record)
        self.dump()

    def edit(self, record_id, amount=None, category=None, date=None, description=None):
        record = self.get(record_id)
        if not record:
            return None
        
        if amount is not None:
            record.amount = amount
        if category is not None:
            record.category = category
        if date is not None:
            record.date = date
        if description is not None:
            record.description = description
        
        self.dump()

    def delete(self, record_id):
        record = self.get(record_id)
        if not record:
            return None
        self.data.remove(record)
        self.dump()

    def export_csv(self, path):
        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['record_id', 'amount', 'category', 'date', 'description'])
            writer.writeheader()
            writer.writerows([record.get_data() for record in self.data])

    def import_csv(self, path):
        with open(path) as f:
            reader = csv.DictReader(f)
            for el in reader:
                el['amount'] = float(el['amount'])
                note = FinanceRecord(**el)
                try:
                    note.set_id(self.data[-1].id + 1)
                except IndexError:
                    note.set_id(1)
                self.data.append(note)
        self.dump()

    def calculate_balance(self):
        return sum(record.amount for record in self.data)

    def filter_by_category(self, category):
        return [record for record in self.data if record.category == category]

    def filter_by_date(self, start_date=None, end_date=None):
        filtered_records = []
        
        for record in self.data:
            record_date = datetime.datetime.strptime(record.date, '%d-%m-%Y')
            
            if start_date and end_date:
                start_date_dt = datetime.datetime.strptime(start_date, '%d-%m-%Y')
                end_date_dt = datetime.datetime.strptime(end_date, '%d-%m-%Y')
                if start_date_dt <= record_date <= end_date_dt:
                    filtered_records.append(record)
            elif start_date and not end_date and start_date_dt <= record_date:
                filtered_records.append(record)
            elif end_date and not start_date and record_date <= end_date_dt:
                filtered_records.append(record)

        return filtered_records
