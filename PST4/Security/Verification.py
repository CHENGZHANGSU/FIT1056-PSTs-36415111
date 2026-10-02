import bcrypt

class Verification:
    def __init__(self, account, entered_password) -> None:
        self._account = "admin"
        self._password = "admin123".encode('utf-8')
        self._entered_account = account
        self._entered_password = entered_password.encode('utf-8')

    def verify(self) -> bool:
        _hashed_password = bcrypt.hashpw(self._password, bcrypt.gensalt())
        if bcrypt.checkpw(self._entered_password, _hashed_password) and self._account == self._entered_account:
            return True
        else:
            return False
