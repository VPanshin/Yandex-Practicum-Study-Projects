"""Module with custom exceptions."""


class APIDoNotResponde(Exception):
    pass


class APIResponseException(Exception):
    pass


class JSONFormatException(Exception):
    pass
