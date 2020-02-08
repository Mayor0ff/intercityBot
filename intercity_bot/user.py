import json

class User:

    def __init__(self, database, id, telegram_id, session, cookie_session):
        self.database = database
        self.id = id
        self.telegram_id = telegram_id
        self.session = dict(json.loads(session))
        self.cookie_session = cookie_session

    def update_session(self, session):
        self.session = session
        self.database.update_user_session(self, json.dumps(session))

    def update_cookie_session(self, cookie_session):
        self.cookie_session = cookie_session
        self.database.update_user_cookie_session(self, cookie_session)
        