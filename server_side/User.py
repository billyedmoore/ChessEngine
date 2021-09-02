from .Database import Database
import os
import hashlib


class User():

    def __init__(self, username, email, password, elo=1500, db_name="user.db"):
        self.db_name = db_name
        self.db = Database(db_name=self.db_name)
        self.username = username
        self.email = email
        self.password = password
        self.elo = elo

    @staticmethod
    def get_user(username: str, db_name=""):
        db = Database()
        if db_name:
            db = Database(db_name=db_name)
        # TODO: hashing
        details = db.get_user_details(username)
        print(details)
        if details:
            return User(details[0], details[1], details[2], elo=details[3])
        else:
            return None

    @staticmethod
    def create_user(username: str, email: str, password: str, elo=1500, db_name=""):
        pass_hash, salt = User.hash_password(password)
        db = Database()
        if db_name:
            db = Database(db_name=db_name)
        db.insert_user(username, email, pass_hash, salt, elo=elo)
        return User(username, email, password, db_name=db_name)

    @staticmethod
    def hash_password(password: str, salt=b""):

        if not salt:
            salt = os.urandom(16)
        pass_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf_8"), salt, 1000000)
        return pass_hash, salt

    def is_auth(self):
        correct_pass_hash, salt = self.db.get_pass_hash(self.username)
        if not correct_pass_hash:
            return False
        test_pass_hash, salt = User.hash_password(self.password, salt=salt)
        return(test_pass_hash == correct_pass_hash)
