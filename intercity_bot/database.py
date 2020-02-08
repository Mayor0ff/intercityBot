import sqlite3
from intercity_bot.user import User

class Database:

    def __init__(self):
        self.connection = sqlite3.connect("database.db", check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                register_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                session TEXT NOT NULL DEFAULT "[]",
                cookie_session TEXT
            )
        """)
        self.connection.commit()
        
    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", [user_id])
        result = self.cursor.fetchone()

        if result:
            return User(self, result[0], result[1], result[3], result[4])
        else:
            return None

    def get_user_telegram(self, telegram_id):
        self.cursor.execute("SELECT * FROM users WHERE telegram_id = ?", [telegram_id])
        result = self.cursor.fetchone()
        self.connection.commit()

        if result:
            return User(self, result[0], result[1], result[3], result[4])
        else:
            return None

    def create_user(self, telegram_id: int):
        self.cursor.execute("INSERT INTO users (telegram_id) VALUES (?)", [telegram_id])
        self.connection.commit()
        return User(self, self.cursor.lastrowid, telegram_id, "[]", None)

    def update_user_session(self, user: User, session: str):
        self.cursor.execute("UPDATE users SET session = ? WHERE id = ?", [session, user.id])
        self.connection.commit()

    def update_user_cookie_session(self, user: User, cookie_session: str):
        self.cursor.execute("UPDATE users SET cookie_session = ? WHERE id = ?", [cookie_session, user.id])
        self.connection.commit()