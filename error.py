class Error(Exception):
    def __init__(self, msg=""):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__

class NoCommandError(Error):
    def __init__(self, command):
        Error.__init__(self, f"No such command to do: {command}")

class MissingRequiredKeyError(Error):
    def __init__(self, missing_key):
        Error.__init__(self, f"Missing requred keys: {missing_key}")