

class User():
    """
    A user class for use on the client side
    """

    def __init__(self, user_id, username, email, elo, session_auth):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.elo = elo
        self.session_auth = session_auth

    @staticmethod
    def login(client, username, password):
        """
        Returns None or a User Object, None should be handled as a failed login
        """
        user_dict = client.login(username, password)
        print(user_dict)
        if not user_dict:
            # incorrect username or password
            return None
        else:
            return User(user_dict["user_id"], user_dict["username"],
                        user_dict["email"], user_dict["elo"],
                        user_dict["session_auth"])
