"""
exceptions.py
-------------
This module defines custom exception classes for the address book application.
Each exception is used to signal specific error conditions
in the application logic.
"""


class NoRecordError(Exception):
    """
    Raised when an action is attempted on a non-existent user record.
    """

    pass


class InvalidPhoneNumberFormatError(Exception):
    """
    Raised when a phone number is entered in an invalid format.
    """

    pass


class InvalidBirthdayFormatError(Exception):
    """
    Raised when a birthday is entered in an invalid format.
    """

    pass


class NoPhoneError(Exception):
    """
    Raised when an action is attempted on a non-existent phone number.
    """

    pass
