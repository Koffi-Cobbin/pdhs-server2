__author__ = 'Koffi Cobbin'

class DepartmentError(Exception):
    def __init__(self, message):
        self.message = message

class DepartmentDontExistError(DepartmentError):
    pass
