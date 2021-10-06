from db_manager import UserData, DB
from hashlib import sha256
from string import ascii_letters, digits
from exeptions import *


class AppAuth:
    _rus_alpha = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    _username_allowed_chars = _rus_alpha + _rus_alpha.upper() + ascii_letters + digits + "_"
    _password_allowed_chars = _rus_alpha
    _full_name_allowed_chars_rus = _rus_alpha + _rus_alpha.upper() + " " + "-"
    _full_name_allowed_chars_en = ascii_letters + " " + '-'
    __salt = "saltFSZB0hrZe6"

    def __init__(self):
        self.db = DB()

    def login(self, username: str, password: str) -> bool:
        if not self.db.is_user_exists(username):
            return False
        return self.db.get_user_data(username).password_hash == self._get_password_hash(password)

    def try_register(self, **kwargs):
        password = kwargs.get("password")
        if not self._is_valid_password(password):
            raise InvalidPassword()
        kwargs["password_hash"] = self._get_password_hash(password)
        print(kwargs)
        user_data = UserData(**kwargs)
        if not self._is_valid_username(user_data.username):
            raise InvalidUsername()
        if self.db.is_user_exists(user_data.username):
            raise UserAlreadyExists()
        if not self._is_valid_full_name(user_data.lastname, user_data.name, user_data.patronymic):
            raise InvalidFullName()
        if not self._is_valid_phone_number(user_data.phone_number):
            raise InvalidPhoneNumber()

        self.db.add_user(user_data)

    @staticmethod
    def _get_password_hash(password: str) -> str:
        return sha256(bytes(password + AppAuth.__salt, encoding="utf-8")).hexdigest()

    @staticmethod
    def _is_str_contains_only_allowed_chars(testing_str: str, allowed_chars: str) -> bool:
        return set(testing_str) <= set(allowed_chars)

    def _is_valid_username(self, username: str) -> bool:
        return not (username is None or len(username) < 3
                    or not self._is_str_contains_only_allowed_chars(username, self._username_allowed_chars))

    def _is_valid_password(self, password: str) -> bool:
        return not (password is None or len(password) < 9
                    or not self._is_str_contains_only_allowed_chars(password, self._password_allowed_chars))

    def _is_valid_phone_number(self, number: str) -> bool:
        if len(number) < 11:
            return False
        if number[:2] == '+7':
            if len(number) == 12 and self._is_str_contains_only_allowed_chars(number[1:], digits):
                return True
            return False
        if number[0] == '8':
            if len(number) == 11 and self._is_str_contains_only_allowed_chars(number, digits):
                return True
            return False
        return False

    def _is_valid_full_name(self, lastname: str, name: str, patronymic: str) -> bool:
        if len(lastname) < 2 or len(name) < 2:
            return False
        return (self._is_str_contains_only_allowed_chars(lastname + name + patronymic,
                                                         AppAuth._full_name_allowed_chars_en) or
                self._is_str_contains_only_allowed_chars(lastname + name + patronymic,
                                                         AppAuth._full_name_allowed_chars_rus))


