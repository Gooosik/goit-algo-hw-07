from collections import UserDict
import datetime

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid input."
    return inner

class Field:
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, phone):
        if not phone.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(phone) != 10:
            raise ValueError("Invalid phone number length")
        super().__init__(phone)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]
    
    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Old phone number {old_phone} not found")
    
    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def __str__(self):
        phones_str = "; ".join(str(p) for p in self.phones)
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name}, phones: {phones_str}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def get_upcoming_birthdays(self):
        today = datetime.date.today()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value.replace(year=today.year)
                if bday < today:
                    bday = bday.replace(year=today.year + 1)
                delta = (bday - today).days
                if 0 <= delta <= 7:
                    if bday.weekday() >= 5:
                        bday += datetime.timedelta(days=(7 - bday.weekday()))
                    upcoming.append({"name": record.name.value, "birthday": bday.strftime("%d.%m.%Y")})
        return upcoming

    def __str__(self):
        if not self.data:
            return "No contacts found."
        return "\n".join(str(record) for record in self.data.values())

@input_error    
def parse_input(user_input):
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    return cmd.strip().lower(), args

@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return "Contact added."

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    return "Contact not found."

@input_error
def get_phone(args, book):
    name = args[0]
    record = book.find(name)
    return str(record) if record else "Contact not found."

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    return str(record.birthday) if record and record.birthday else "Birthday not found."

@input_error
def birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    return "\n".join([f"{b['name']}: {b['birthday']}" for b in upcoming]) if upcoming else "No upcoming birthdays."

def __str__(self):
    return "str"

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(get_phone(args, book))
        elif command == "all":
            print(book if book.data else "No contacts found.")
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
