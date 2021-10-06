import sqlite3


class UserData:
    def __init__(self, user_data_list=None, **kwargs):
        if user_data_list is not None:
            assert len(user_data_list) == 8, f"Неправильное количество аргументов ({len(user_data_list)})"
            self.user_data_dict = dict()
            self.user_data_dict["username"] = user_data_list[0]
            self.user_data_dict["password_hash"] = user_data_list[1]
            self.user_data_dict["lastname"] = user_data_list[2]
            self.user_data_dict["name"] = user_data_list[3]
            self.user_data_dict["patronymic"] = user_data_list[4]
            self.user_data_dict["birthday"] = user_data_list[5]
            self.user_data_dict["place_of_birth"] = user_data_list[6]
            self.user_data_dict["phone_number"] = user_data_list[7]
            kwargs = self.user_data_dict
        self.user_data_dict = kwargs
        self.username = kwargs.get("username")
        self.password_hash = kwargs.get("password_hash")
        self.lastname = kwargs.get("lastname")
        self.name = kwargs.get("name")
        self.patronymic = kwargs.get("patronymic")
        self.birthday = kwargs.get("birthday")
        self.place_of_birth = kwargs.get("place_of_birth")
        self.phone_number = kwargs.get("phone_number")

    def get_user_data_list(self):
        return [self.username, self.password_hash, self.lastname, self.name, self.patronymic,
                self.birthday, self.place_of_birth, self.phone_number]

    def get_user_data_dict(self):
        return self.user_data_dict


class DB:
    def __init__(self, filename="data.db"):
        self._cursor = sqlite3.connect(filename)
        self._create_users_table()

    def _create_users_table(self):
        self._cursor.execute("CREATE TABLE IF NOT EXISTS users ("
                             "username TEXT PRIMARY KEY NOT NULL,"
                             "password_hash TEXT NOT NULL,"
                             "lastname TEXT,"
                             "name TEXT,"
                             "patronymic TEXT,"
                             "birthday TEXT,"
                             "place_of_birth TEXT,"
                             "phone_number TEXT);")
        self._cursor.commit()

    def _delete_users_table(self):
        self._cursor.execute(r"DROP TABLE IF EXISTS users")
        self._cursor.commit()

    def close(self):
        self._cursor.close()

    def add_user(self, user_data: UserData):
        self._cursor.execute("INSERT INTO users(username, password_hash, lastname, name, patronymic, birthday,"
                             " place_of_birth, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                             user_data.get_user_data_list())
        self._cursor.commit()

    def get_user_data(self, username: str) -> UserData:
        result = self._cursor.execute("SELECT username, password_hash, lastname, name, patronymic, birthday,"
                                      " place_of_birth, phone_number"
                                      " FROM users"
                                      " WHERE username = ?;", (username,)).fetchall()[0]
        ud =UserData(user_data_list=list(result))
        print(ud.user_data_dict)
        return ud

    def update_user_data(self, user_data: UserData):
        self._cursor.execute("UPDATE users "
                             "SET"
                             " password_hash = ?,"
                             " lastname = ?,"
                             " name = ?,"
                             " patronymic = ?,"
                             " birthday = ?,"
                             " place_of_birth = ?,"
                             " phone_number = ?"
                             "WHERE username = ?;", user_data.get_user_data_list()[1:] + [user_data.username])
        self._cursor.commit()

    def is_user_exists(self, username: str) -> bool:
        return len(self._cursor.execute("SELECT 1"
                                        " FROM users"
                                        " WHERE username = ?;", (username,)).fetchall()) > 0
