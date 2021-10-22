class LabException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class RegistrationException(LabException):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidUsername(RegistrationException):
    _message = 'Имя пользователя должно быть не короче трех символов и содержать только латиницу, кириллицу и "_"'

    def __init__(self):
        super().__init__(self._message)


class InvalidPassword(RegistrationException):
    _message = 'Пароль должн быть не короче девяти символов и содержать только кириллицу (прописные буквы)'

    def __init__(self):
        super().__init__(self._message)


class UserAlreadyExists(RegistrationException):
    _message = 'Пользователь с таким логином уже существует'

    def __init__(self):
        super().__init__(self._message)


class InvalidPhoneNumber(RegistrationException):
    _message = 'Номер телефона должен состоять из 11 цифр и начинаться с "+7" или "8"'

    def __init__(self):
        super().__init__(self._message)


class InvalidFullName(RegistrationException):
    _message = 'Фамилия и имя должны быть не короче двух символов и должны содержать только кириллицу или ' \
               'только латиницу'

    def __init__(self):
        super().__init__(self._message)


class InvalidPasswordChange(RegistrationException):
    _message = "Пароль не может совпадать с отчеством"

    def __init__(self):
        super().__init__(self._message)


class NotLoggedInException(RegistrationException):
    _message = "Вы не можете поменять данные, так как не вошли"

    def __init__(self):
        super().__init__(self._message)


class PassGeneratorException(LabException):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidAlphasSetException(PassGeneratorException):
    _message = "Неправильный набор алфавитов для генерации пароля (должен быть минимум один алфавит)"

    def __init__(self):
        super().__init__(self._message)
