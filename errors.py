# Ошибки при входе в аккаунт
class Incorrect_Password(Exception):
    pass


class Invalid_Login(Incorrect_Password):
    pass

# Ошибки при регистрации

class Length_Of_Password_Error(Exception):
    pass


class Name_Already_Taken_Error(Length_Of_Password_Error):
    pass

# Ошибки в настройках(Используется тот же Name_Already_Taken_Error)

# Ошибки при создании папки и цели

class Name_Is_Not_Written(Exception):
    pass