class CustomException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg


class FileNotFoundInDb(CustomException):
    def __init__(self, msg):
        super().__init__(msg)


class FileNotFoundInFolder(CustomException):
    def __init__(self, msg):
        super().__init__(msg)


class LastModifyChanged(CustomException):
    def __init__(self, msg):
        super().__init__(msg)


class ChkChanged(CustomException):
    def __init__(self, msg):
        super().__init__(msg)
