from collections import UserDict


class PhoneTooShortError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def get_phone(func):
        def inner(self, phone):
            if len(phone) < 10:
                raise PhoneTooShortError("Phone number is too short")
            return func(self, phone)

        return inner

    @get_phone
    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone_number != phone.value]

    def edit_phone(self, phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                phone.value = new_phone_number

    def find_phone(self, phone):
        for item in self.phones:
            if item.value == phone:
                return item.value
        return "Don`t has this number"

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, contact: Record):
        self.data[contact.name.value] = contact

    def delete(self, name):
        self.data.pop(name)

    def find(self, name: str):
        return self.data.get(name, None)

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
try:
    john_record.add_phone("1234567890")
    john_record.add_phone("555555555")
except PhoneTooShortError as e:
    print(e)

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі

print(book)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("1234567890")
print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

# Видалення запису Jane
book.delete("Jane")

print(book)
