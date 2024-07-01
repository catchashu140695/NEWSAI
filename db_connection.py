import sqlite3
from sqlite3 import Error

class DatabaseConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            print(f"Successfully Connected to SQLite Database '{self.db_file}'")
        except Error as e:
            print(f"Error connecting to database: {e}")
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            print("Connection closed")
