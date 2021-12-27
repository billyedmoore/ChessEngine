from .Database import Database
from sqlite3 import IntegrityError
import os
import re
import hashlib


class User():
    """
    Server side user class
    """

    def __init__(self, user_id, username, email, password, elo=1500, db_name="user.db"):
        self.db_name = db_name
        self.db = Database(db_name=self.db_name)
        self.id = user_id
        self.username = username.lower()
        self.email = email
        self.password = password
        self._elo = elo

    @property
    def elo(self):
        # prevents the setting of elo without changing the db
        return self._elo

    @elo.setter
    def elo(self, elo):
        if not isinstance(elo, int) and not isinstance(elo, float):
            print("Cant set elo to :", elo)
            raise TypeError("ELO must be an integer")
        else:
            # update in db
            self.db.update_elo(self.id, elo)

            # if added succesfully change locally on the class
            self._elo = elo

    def is_auth(self):
        """
        Tests wether a user is authenticated (wether the self.password is the
        correct password).
        """
        correct_pass_hash, salt = self.db.get_pass_hash(self.username)
        if not correct_pass_hash:
            return False
        test_pass_hash, salt = User.hash_password(self.password, salt=salt)
        return(test_pass_hash == correct_pass_hash)

    @staticmethod
    def get_user(username: str, password: str, db_name=""):
        """
        Returns a user by username aslong as the password is correct.
        """
        db = Database()
        if db_name:
            db = Database(db_name=db_name)
        # TODO: hashing
        details = db.get_user_details(username)
        if details:
            print(details)
            user = User(details[0], details[1], details[2],
                        password, elo=details[5])
            return (user if user.is_auth() else None)
        else:
            return None

    @staticmethod
    def create_user(username: str, email: str, password: str, elo=1500, db_name=""):
        """
        Append a user to the database and return a boolean value.

        Parameters:
            string username - the users username
            string email - the users email
            string password - the users plain text password
            int elo - the users elo
            string db_name - the name of the db to add the user to or None for 
                             default db
        """
        pass_hash, salt = User.hash_password(password)
        db = Database()
        if db_name:
            db = Database(db_name=db_name)

        try:
            user_id = db.insert_user(
                username.lower(), email, pass_hash, salt, elo=elo)
            if user_id:
                return True
        except IntegrityError:
            return False

        # return User(user_id, username, email, password, db_name=db_name)

    @staticmethod
    def is_valid_user(username, email, password):
        """
        Checks that a user is valid accoring to the rules layed out in the
        design of the program

        Parameters:
            string email    - the email to test
            string username - the username to test
            string password - the password to test

        Return Values:
            bool is_valid - wether the email username and pasword provided are 
                            all in accordance with the rules
        """
        if not User.is_valid_password(password):
            return (False, "password")
        elif not User.is_valid_username(username):
            return (False, "username")
        elif not User.is_valid_email(email):
            return (False, "email")
        else:
            return (True, "")

    @staticmethod
    def is_valid_password(password):
        """
        Checks that the password is bettween 10 and 30 characters in length as
        specified in design

        Parameters:
            string password - the password to test

        Return Values:
            bool is_valid - wether or not the password is acceptable
        """
        return (isinstance(password, str) and len(password) >= 10 and len(password) <= 30)

    @staticmethod
    def is_valid_email(email):
        """
        Checks that an email is approximatly valid, this isn't ideal because
        it gives no guarentee that the user has the email.

        Parameters:
            string email - the email to test

        Return Values:
            bool is_valid - wether or not the email is valid
        """
        # heavily inpired by https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return bool(re.fullmatch(email_regex, email))

    @staticmethod
    def is_valid_username(username):
        """
        Checks that a username is less that 15 characters in length so that it
        can be used as specified in the design stage

        Parameters:
            string username

        Return Values:
            bool is_valid - wether or not the password is acceptable
        """
        return (isinstance(username, str) and len(username) <= 15)

    @staticmethod
    def hash_password(password: str, salt=b""):
        """
        Hash a password with sha256 so it can be stored in the database or
        compared to the password hash that is stored already.

        Parameters:
            string password - the password to hash as a string
            bytes salt - the salt to be used or None to generate a new salt

        Return Values:
           bytes pass_hash - the hashed password
           bytes salt - the salt used to hash the password
        """
        if not salt:
            salt = os.urandom(16)
        pass_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf_8"), salt, 1000000)
        return pass_hash, salt
