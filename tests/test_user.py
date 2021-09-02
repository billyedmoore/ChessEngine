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
