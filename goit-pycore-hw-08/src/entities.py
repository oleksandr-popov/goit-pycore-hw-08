"""
entities.py
-------------
This module defines the core data structures for the address book application,
including fields, records, and the address book itself.

Classes:
    Field: Base class for fields in records.
    Name: Represents a user's name.
    Phone: Represents a user's phone number.
    Birthday: Represents a user's birthday.
    Record: Represents a contact record.
    AddressBook: Stores and manages multiple records.
"""

from collections import UserDict
from datetime import datetime, date, timedelta
from helpers import (
    NoRecordError,
    InvalidPhoneNumberFormatError,
    InvalidBirthdayFormatError,
    NoPhoneError,
)

PHONE_LENGTH = 10
USER_KEY = "user"
BIRTHDAY_KEY = "birthday"
CONGRATULATION_DATE_KEY = "congratulation_date"
DATE_PATTERN = "%Y.%m.%d"
DAYS_OF_UPCOMING_RANGE = 7
ISO_SATURDAY = 6
ISO_SUNDAY = 7


class Field:
    """
    Base class for fields in Records
    Implements holding of some data as string,
    and rendering of this data via __str__ method.
    """

    def __init__(self, value):
        """
        Initialize a Field with a value.
        Args:
            value: The value to store in the field.
        """
        self.value = value

    def __str__(self):
        """Return string representation of the field value."""
        return str(self.value)

    def __repr__(self):
        """Return string representation for debugging."""
        return self.__str__()


class Name(Field):
    """
    Name of user.
    Note that name cannot be empty, exception will be raised otherwise.
    """

    def __init__(self, value: str):
        """
        Initialize a Name field.
        Args:
            value (str): The name value. Must not be empty.
        Raises:
            ValueError: If the name is empty.
        """
        if len(value) == 0:
            raise ValueError("Empty name is not supported")
        super().__init__(value)


class Phone(Field):
    """
    Phone of user.
    Note that it's strongly required that phone contains only numbers,
    and exactly 10 numbers.
    Exception will be thrown if this condition is not fulfilled.
    """

    def __init__(self, value: str):
        """
        Initialize a Phone field.
        Args:
            value (str): The phone number as a string of digits.
        Raises:
            InvalidPhoneNumberFormatError: If the phone number
            is not 10 digits or contains non-digits.
        """
        if len(value) != PHONE_LENGTH:
            raise InvalidPhoneNumberFormatError(
                f"Phone length is not correct, \
                    it supposed to have {PHONE_LENGTH} symbols"
            )
        if not value.isdigit():
            raise InvalidPhoneNumberFormatError(
                "Phone number is supposed to contain only digits"
            )
        super().__init__(value)

    def __eq__(self, other):
        """Check equality based on phone value."""
        return self.value == other.value


class Birthday(Field):
    """
    Birthday of user.
    Stores the date as a datetime.date object.
    """

    RAW_DATE_PATTERN = "%d.%m.%Y"

    def __init__(self, value: str):
        """
        Initialize a Birthday field.
        Args:
            value (str): The birthday in DD.MM.YYYY format.
        Raises:
            InvalidBirthdayFormatError: If the date format is invalid.
        """
        try:
            super().__init__(
                datetime.strptime(value,
                                  Birthday.RAW_DATE_PATTERN).date())
        except ValueError:
            raise InvalidBirthdayFormatError(
                "Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        """Return the birthday as a string in DD.MM.YYYY format."""
        return date.strftime(self.value, Birthday.RAW_DATE_PATTERN)


class Record:
    """
    One Record corresponds to a single user, contains name and can
    contain some phone numbers and birthday.
    Attributes:
        name (Name): The name of the contact.
        phones (list[Phone]): List of phone numbers.
        birthday (Birthday|None): The birthday of the contact.
    """

    def __init__(self, name):
        """
        Initialize a Record.
        Args:
            name (str): The name of the contact.
        """
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        """Return string representation of the record."""
        return f"Contact name: {self.name.value}, birthday: {self.birthday}, \
            phones: {'; '.join(p.value for p in self.phones)}"

    def __repr__(self):
        """Return string representation for debugging."""
        return self.__str__()

    def add_phone(self, phone: str):
        """
        Add a phone number to the record.
        Args:
            phone (str): The phone number to add.
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        """
        Remove a phone number from the record.
        Args:
            phone (str): The phone number to remove.
        """
        self.phones.remove(Phone(phone))

    def edit_phone(self, phone: str, new_phone: str):
        """
        Edit an existing phone number.
        Args:
            phone (str): The phone number to replace.
            new_phone (str): The new phone number.
        Raises:
            NoPhoneError: If the phone number is not found.
        """
        phone_object = Phone(phone)
        existing_phone_index = self.phones.index(phone_object)
        if existing_phone_index < 0:
            raise NoPhoneError
        self.phones[existing_phone_index] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone:
        """
        Find a phone number in the record.
        Args:
            phone (str): The phone number to find.
        Returns:
            Phone: The Phone object if found, else None.
        """
        for maybe_phone in self.phones:
            if maybe_phone.value == phone:
                return maybe_phone

    def add_birthday(self, birthday: str):
        """
        Add a birthday to the record.
        Args:
            birthday (str): The birthday in DD.MM.YYYY format.
        """
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):
    """
    Contains all info about users and their phone numbers.
    Raw user's name is a key for each record.
    Inherits from UserDict.
    """

    def add_record(self, record: Record):
        """
        Add a record to the address book.
        Args:
            record (Record): The record to add.
        """
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """
        Find a record by name.
        Args:
            name (str): The name to search for.
        Returns:
            Record: The found record.
        Raises:
            NoRecordError: If the record is not found.
        """
        if name not in self.data:
            raise NoRecordError()
        return self.data.get(name)

    def delete(self, name: str):
        """
        Delete a record by name.
        Args:
            name (str): The name of the record to delete.
        Raises:
            NoRecordError: If the record is not found.
        """
        if name not in self.data:
            raise NoRecordError()
        self.data.pop(name)

    def all_records(self) -> list[Record]:
        """Return a list of all records in the address book."""
        return list(self.data.values())

    def find_phones(self, name: str) -> list[Record]:
        """
        Find all phone numbers for a given contact name.
        Args:
            name (str): The name of the contact.
        Returns:
            list[Phone]: List of phone numbers.
        """
        return self.find(name).phones

    def get_upcoming_birthdays(self) -> list:
        """
        Returns list of user's records, which has upcoming birthday within
        the next DAYS_OF_UPCOMING_RANGE days.
        Returns:
            list[dict]: List of dicts with user and congratulation date.
        """
        current_date = datetime.today().date()
        current_year = current_date.year
        upcoming_birthdays_result = []
        for record in self.all_records():
            birthday = record.birthday
            if birthday is None:
                continue
            birthday_date = birthday.value
            birthday_month = birthday_date.month
            birthday_day = birthday_date.day
            this_year_birthday_date = date(current_year,
                                           birthday_month, birthday_day)
            is_birthday_passed = this_year_birthday_date < current_date
            congrats_date: date
            if is_birthday_passed:
                congrats_date = date(current_year + 1,
                                     birthday_month, birthday_day)
            else:
                congrats_date = this_year_birthday_date
            congrats_day_of_week = congrats_date.isoweekday()
            is_congrats_date_in_weekend = congrats_day_of_week >= ISO_SATURDAY
            if is_congrats_date_in_weekend:
                days_factor = 1 if congrats_day_of_week == ISO_SUNDAY else 2
                congrats_date = congrats_date + timedelta(days=days_factor)
            if (
                congrats_date.toordinal() - current_date.toordinal()
            ) <= DAYS_OF_UPCOMING_RANGE:
                upcoming_birthdays_result.append(
                    {
                        USER_KEY: record,
                        CONGRATULATION_DATE_KEY: datetime.strftime(
                            congrats_date, DATE_PATTERN
                        ),
                    }
                )
        return upcoming_birthdays_result
