"""
main.py
-------
This is the main entry point for the address book assistant bot
It provides a command-line interface for managing contacts,
phone numbers, and birthdays.
"""

import pickle
from entities import AddressBook, Record, \
    CONGRATULATION_DATE_KEY, USER_KEY
from helpers import input_error

# Description of what program can do
ASSISTANT_INFO = """
==================== ASSISTANT BOT COMMANDS ====================

Contacts Management:
  add <name> <phone>           Add new contact. Phone must be exactly 10 digits
  change <name> <old> <new>    Change a contact's phone number
  phone <name>                 Show all phone numbers for a contact
  clear                        Remove all contacts from the address book

Birthday Management:
  add-birthday <name> <date>   Add a birthday to a contact (format: DD.MM.YYYY)
  show-birthday <name>         Show the birthday for a contact
  birthdays                    List all upcoming birthdays in the next 7 days

General:
  all                          Show all saved contacts
  info                         Show this help message
  close                        Print 'Good bye!' and exit the assistant
  exit                         Exit the program immediately
  hello                        Just say 'Hi!'

Notes:
- Phone numbers must be 10 digits (no spaces, plus, or special characters)
- Birthday format must be DD.MM.YYYY (e.g., 28.09.2025)
- Arguments in <angle brackets> are required
===============================================================
"""
"""
str: Information about supported commands for the assistant bot.
"""

CACHE_FILE_NAME = "addressbook.dat"
"""
str: The filename where the address book is persisted.
"""


@input_error
def use_case():
    """
    Main use case for the assistant bot. Handles user interaction
    and command processing.
    """
    print("Welcome to the assistant bot!")
    print(format_info())
    address_book = load_address_book(CACHE_FILE_NAME)
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
       
        if command == "info":
            print(format_info())
        elif command == "hello":
            print("Hi!")
        elif command == "add":
            print(add_contact(args, address_book))
        elif command == "change":
            print(change_contact(args, address_book))
        elif command == "phone":
            print(find_numbers_by_name(args, address_book))
        elif command == "add-birthday":
            print(add_birthday(args, address_book))
        elif command == "show-birthday":
            print(show_birthday(args, address_book))
        elif command == "birthdays":
            print(birthdays(args, address_book))
        elif command == "all":
            print(output_all_contacts(address_book))
        elif command in "close":
            print("Good bye!")
            save_address_book(address_book, CACHE_FILE_NAME)
            break
        elif command == "exit":
            save_address_book(address_book, CACHE_FILE_NAME)
            break
        else:
            print("Invalid command.")


def parse_input(user_input):
    """
    Parse the user input into a command and arguments.
    Args:
        user_input (str): The raw input string from the user.
    Returns:
        tuple: (command, *args)
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, address_book: AddressBook):
    """
    Add a new contact or update an existing one with a phone number.
    Args:
        args (list): [name, phone]
        address_book (AddressBook): The address book instance.
    Returns:
        str: Result message.
    """
    name, phone, *_ = args
    contact = None
    result_message = None
    if name in address_book.data:
        contact = address_book.find(name)
        result_message = "Contact updated."
    else:
        contact = Record(name)
        address_book.add_record(contact)
        result_message = "Contact added."
    contact.add_phone(phone)
    return result_message


@input_error
def output_all_contacts(address_book: AddressBook):
    """
    Output all contacts in the address book.
    Args:
        address_book (AddressBook): The address book instance.
    Returns:
        str: All contacts or a message if none exist.
    """
    all_contacts = address_book.all_records()
    if len(all_contacts) > 0:
        return f"Here's all added contacts:\n{all_contacts}."
    else:
        return "No contacts added so far."


@input_error
def find_numbers_by_name(args, address_book: AddressBook):
    """
    Find all phone numbers for a given contact name.
    Args:
        args (list): [name]
        address_book (AddressBook): The address book instance.
    Returns:
        str: Phone numbers for the contact.
    """
    name = args[0]
    phones = address_book.find_phones(name)
    return f"Phone numbers of {name}:\n {phones}."


@input_error
def change_contact(args, address_book: AddressBook):
    """
    Change a contact's phone number.
    Args:
        args (list): [name, old_phone, new_phone]
        address_book (AddressBook): The address book instance.
    Returns:
        str: Result message.
    """
    name, old_phone, new_phone, *_ = args
    contact_record = address_book.find(name)
    contact_record.edit_phone(old_phone, new_phone)
    return "Contact changed."


@input_error
def add_birthday(args, address_book: AddressBook):
    """
    Add a birthday to a contact.
    Args:
        args (list): [name, birthday]
        address_book (AddressBook): The address book instance.
    Returns:
        str: Result message.
    """
    name, birthday, *_ = args
    record = address_book.find(name)
    record.add_birthday(birthday)
    return f"Birthday added for {name}"


@input_error
def show_birthday(args, address_book: AddressBook):
    """
    Show the birthday of a contact.
    Args:
        args (list): [name]
        address_book (AddressBook): The address book instance.
    Returns:
        str: Birthday or message if not set.
    """
    name = args[0]
    user = address_book.find(name)
    birthday = user.birthday
    if birthday is not None:
        return f"Birthday of {name}'s is {birthday}"
    else:
        return f"No birthday added for user {name}"


@input_error
def birthdays(args, address_book: AddressBook):
    """
    Show all upcoming birthdays.
    Args:
        args (list): Not used.
        address_book (AddressBook): The address book instance.
    Returns:
        str: List of upcoming birthdays or a message if none.
    """
    upcoming_birthdays = address_book.get_upcoming_birthdays()
    result = ""
    if upcoming_birthdays:
        result += "Upcoming birthdays:\n"
        for birthday_item in upcoming_birthdays:
            result += f"{birthday_item[USER_KEY].name}: \
            {birthday_item[CONGRATULATION_DATE_KEY]}\n"
    else:
        result += "No upcoming birthdays for now."
    return result


@input_error
def format_info():
    """
    Return information about supported commands.
    Returns:
        str: Supported commands info.
    """
    return ASSISTANT_INFO


def load_address_book(filename: str) -> AddressBook:
    """
    Load the AddressBook's state from a file, or create a new one if
    the file does not exist.
    Args:
        filename (str): The filename to load from.
    Returns:
        AddressBook: The loaded or new address book.
    """
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()


def save_address_book(address_book: AddressBook, filename: str):
    """
    Save the AddressBook to a file.
    Args:
        address_book (AddressBook): The address book instance.
        filename (str): The filename to save to.
    """
    with open(filename, "wb") as file:
        pickle.dump(address_book, file)


if __name__ == "__main__":
    use_case()
