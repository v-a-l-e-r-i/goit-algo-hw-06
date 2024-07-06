from collections import UserDict
import re


class LengthPhoneNumberError(Exception):
    pass


class NotNumberError(Exception):
    pass


def get_phone(func):
    def inner(self, phone):
        if len(phone) != 10:
            raise LengthPhoneNumberError("Іncorrectly entered phone number")
        elif re.findall("\D", phone):
            raise NotNumberError("Need enter a phone number")

        return func(self, phone)

    return inner


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    @get_phone
    def __init__(self, value):
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        try:
            self.phones.append(Phone(phone_number))
        except Exception as e:
            print(e)

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone_number != phone.value]

    def check_phone_is_found(self, number):
        for phone in self.phones:
            if phone.value == number:
                return self.phones.index(phone)
        raise ValueError

    def edit_phone(self, old_phone, new_phone_number):
        try:
            self.phones[self.check_phone_is_found(old_phone)] = Phone(new_phone_number)
        except NotNumberError or LengthPhoneNumberError as e:
            print(e)
            
    def find_phone(self, phone):
        for item in self.phones:
            if item.value == phone:
                return item
        return None

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
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

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
john.edit_phone("1244567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("1112223333")
print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

# Видалення запису Jane
book.delete("Jane")

print(book)
