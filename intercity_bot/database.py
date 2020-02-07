import sqlite3
from intercity_bot import user

class Database:

    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                register_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                cookie_session TEXT
            )
        """)
        self.connection.commit()
        
    def get_user(self, user_id):
        pass

    def get_user_telegram(self, telegram_id):
        pass

    def create_user(self, telegram_id):
        self.cursor.execute("INSERT INTO users (telegram_id) VALUES (?)", telegram_id)
        self.connection.commit()