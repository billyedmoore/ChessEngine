from .Database import Database
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
        self.username = username
        self.email = email
        self.password = password
        self.elo = elo

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
        Append a user to the database and return their user object.

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
        user_id = db.insert_user(username, email, pass_hash, salt, elo=elo)
        return User(user_id, username, email, password, db_name=db_name)

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
