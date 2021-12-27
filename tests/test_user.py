import unittest
from server_side import User
import os


class TestUserMethods(unittest.TestCase):
    def test_hash_password(self):
        """
        Create a user and test weather they are authorised by checking their
        password vs the db hash
        """

        os.system("rm -rf test.db")
        os.system("del /f test.db")

        user = User.User.create_user(
            "billyedmoore", "billy@email.com", "password", db_name="test.db")
        self.assertTrue(bool(User.User.get_user(
            "billyedmoore", "password")))

        os.system("rm -rf test.db")
        os.system("del /f test.db")

    def test_is_valid_email(self):
        emails = ["billy@gmail.com", "a@a.com",
                  "president@whitehouse.gov", "adfjlksdf",
                  "#@%^%#$@#$@#.com", "adfjlksdf"]
        email_test = [User.User.is_valid_email(email) for email in emails]
        self.assertEqual(email_test, [True, True, True, False, False, False])
