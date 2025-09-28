"""
helpers.py
----------
This module provides helper functions and decorators for error
handling in the address book application.
"""

from functools import wraps
from exceptions import (
    NoRecordError,
    InvalidBirthdayFormatError,
    InvalidPhoneNumberFormatError,
    NoPhoneError,
)

DEFAULT_ERROR_MESSAGE = "Make sure you enter correct command and arguments" \
                        "(run 'info' command if you have any doubts)."
"""
str: Default error message for general errors.
"""


def input_error(func):
    """
    Decorator for handling input errors in command functions.
    Catches custom exceptions and common errors, returning
    user-friendly messages.

    Args:
        func (callable): The function to wrap.
    Returns:
        callable: The wrapped function with error handling.
    """

    @wraps(func)
    def inner(*args, **kwargs):
        # we do main error handling via custom exceptions,
        # and leave general errors handling just for case.
        try:
            return func(*args, **kwargs)
        except NoRecordError:
            return "No such user found. Make sure you enter name of " \
                    "existing contact. Run 'all' " \
                    "command to see all contacts you have."
        except InvalidPhoneNumberFormatError:
            return "Invalid format of phone number. Make sure you " \
                    "enter number with exactly 10 symbols, and " \
                    "it contains only digits."
        except InvalidBirthdayFormatError:
            return "Invalid format of birtday. " \
                    "Make sure you use DD.MM.YYYY format."
        except NoPhoneError:
            return "No such phone number found. Make sure you " \
                    "enter existing phone number, which " \
                    "was added to contact before."
        except ValueError:
            return f"ValueError. {DEFAULT_ERROR_MESSAGE}"
        except KeyError:
            return f"KeyError. {DEFAULT_ERROR_MESSAGE}"
        except IndexError:
            return f"Index error. {DEFAULT_ERROR_MESSAGE}"
        except Exception:
            return f"Unexpected error. {DEFAULT_ERROR_MESSAGE}"

    return inner
