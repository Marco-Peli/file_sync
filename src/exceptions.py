class CustomException(Exception):
    def __init__(self, msg, code):
        super().__init__(msg)
        self.msg = msg
        self.code = code

    def __str__(self):
        return self.msg


class FileNotFoundInDb(CustomException):
    def __init__(self, msg):
        super().__init__(msg)


class LastModifyChanged(CustomException):
    def __init__(self, msg):
        super().__init__(msg)


class ChkChanged(CustomException):
    def __init__(self, msg):
        super().__init__(msg)
