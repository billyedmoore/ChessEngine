import os
import sqlite3


class Database():
    """
    Interface with the database directly.
    Shouldn't perform validation at this level as these methods should only
    be called with valid values for example these methods woudldn't prevent
    you having a character below 10 characters in length.
    """

    def __init__(self, reset=False, db_name="user.db"):
        self.db_name = db_name
        if reset:
            try:
                os.system(f"rm -r {self.db_name}")
            except:
                pass
            self.create_tables()
        else:
            if not os.path.isfile(f"{self.db_name}"):
                # print("creating database")
                self.create_tables()

    def _sql_query(self, sql, data=(), get_last_row_id=False):
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(sql, data)
            result = cur.fetchall()
            if get_last_row_id:
                result = cur.lastrowid
            db.commit()
        return result

    def create_tables(self):
        self._create_users_table()

    def _create_users_table(self):
        sql = """
            CREATE TABLE User(
                UserId INTEGER NOT NULL UNIQUE,
                Email TEXT NOT NULL UNIQUE,
                Username TEXT NOT NULL UNIQUE,
                Password BLOB NOT NULL,
                Salt BLOB NOT NULL,
                ELO INTEGER NOT NULL,
                PRIMARY KEY("UserId")
            );
            """
        self._sql_query(sql)

    def get_user_details(self, username):
        """
        Get user details, only allows you to get details with the corrected 
        hashed_password
        """
        sql = "SELECT UserId,Username,Email,Password,Salt,ELO FROM User WHERE Username=?"
        user = self._sql_query(sql, data=(username,))
        if user:
            return user[0]
        else:
            return None

    def get_pass_hash(self, username):
        """
        Get the password hash for a user by username. Not sure if this is
        very insecure or not.
        """
        sql = "SELECT Password,Salt FROM User WHERE Username=?"
        pass_hash = self._sql_query(sql, data=(username,))
        if pass_hash:
            return pass_hash[0][0], pass_hash[0][1]
        else:
            print(f"No hash with the username {username}")
            return None, None

    def update_elo(self, user_id, new_elo):
        sql = "UPDATE User SET ELO=? WHERE UserId=?"
        self._sql_query(sql, data=(new_elo, user_id))

    def insert_user(self, username, email, pass_hash, salt, elo=1500):
        """
        Insert user into database.
        """
        sql = "INSERT INTO User (Username,Email,Password,Salt,ELO) VALUES (?,?,?,?,?)"
        data = (username, email, pass_hash, salt, elo)
        user_id = self._sql_query(sql, data=data, get_last_row_id=True)
        return user_id
