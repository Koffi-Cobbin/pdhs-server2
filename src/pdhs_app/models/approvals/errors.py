class ApprovalError(Exception):
    def __init__(self, message):
        self.message = message


class ApprovalDontExistError(ApprovalError):
    pass
