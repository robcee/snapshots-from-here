import base64
import random
import time

import settings


class Snappy(object):
    """All the snapshot functionality"""
    def __init__(self):
        self.token = ''
        self.env = 'dev'
        self.db = settings.DATABASE

    def set_environment(self, env='dev'):
        if env == 'test':
            self.env = env
            self.db = settings.TEST_DATABASE
    
    def get_or_create_email(self, email):
        """Find the email address in the system
        or create it if it doesn't exist.
        """
        email = email.lower().strip()
        if not self.db.users.find_one({"email":email}):
            self.db.users.update({"email":email},
                                 {"$set":{"token":self._generate_token(email)}},
                                   upsert=True)
        emailer = self.db.users.find_one({"email":email})
        self.token = emailer['token']
        return emailer

    def _generate_token(self, email):
        """Generate a token based on the timestamp and the user's
        email address.
        """
        random_int = str(random.randrange(100, 10000))
        token_string = '%s%s%s' % (random_int,
                                   email,
                                   str(int(time.time())))
        return base64.b64encode(token_string)
