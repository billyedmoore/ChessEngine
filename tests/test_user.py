import unittest
from server_side import User
import os


class TestUserMethods(unittest.TestCase):

    def test_hash_password(self):
        """
        Create a user and test wether they are authourised by checking their 
        password vs the db hash
        """
        try:
            os.system("rm -rf test.db")
        except:
            pass
        user = User.User.create_user(
            "billyedmoore", "billy@email.com", "password", db_name="test.db")
        self.assertTrue(user.is_auth())
        os.system("rm -rf test.db")

    def test_is_valid_email(self):
        emails = ["billy@gmail.com", "a@a.com",
                  "president@whitehouse.gov", "adfjlksdf",
                  "#@%^%#$@#$@#.com", "adfjlksdf"]
        email_test = [User.User.is_valid_email(email) for email in emails]
        self.assertEqual(email_test, [True, True, True, False, False, False])
