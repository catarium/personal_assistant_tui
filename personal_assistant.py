from interfaces.base import interface
from interfaces.notes import main as notes_interface
from interfaces.tasks import main as tasks_interface
from interfaces.contacts import main as contacts_interface
from interfaces.finances import main as finance_interface
from interfaces.calc import main as calc

from models.note import NoteDB
from models.task import TaskDB
from models.finance import FinanceDB
from models.contact import ContactDB


notes_db = NoteDB('notes.json')
tasks_db = TaskDB('tasks.json')
finance_db = FinanceDB('finance.json')
contacts_db = ContactDB('contacts.json')
interface((lambda: '1', ()), [['Управление заметками', notes_interface, [notes_db], False],
                              ['Управление задачами', tasks_interface, [tasks_db], False],
                              ['Управление контактами', contacts_interface, [contacts_db], False],
                              ['Управление финансами', finance_interface, [finance_db], False],
                              ['Калькулятор', calc, [], False],])

