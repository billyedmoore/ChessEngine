import os
import sqlite3


class Database():
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
                print("db dont exist")
                self.create_tables()

    def _sql_query(self, sql, data=()):
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(sql, data)
            result = cur.fetchall()
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
        sql = "SELECT * FROM User WHERE Username=?"
        user = self._sql_query(sql, data=(username,))
        print(user)
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
            return None

    def insert_user(self, username, email, pass_hash, salt, elo=1500):
        """
        Insert user into database.
        """
        sql = "INSERT INTO User (Username,Email,Password,Salt,ELO) VALUES (?,?,?,?,?)"
        data = (username, email, pass_hash, salt, elo)
        self._sql_query(sql, data=data)
