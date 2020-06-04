from flask_login import UserMixin
import json
import uuid

PROFILE_FILE = "profiles.json"

class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.id = self.get_id()

    def get_id(self):
        if self.username is not None:
            try:
                with open(PROFILE_FILE) as f:
                    user_profiles = json.load(f)
                    if self.username in user_profiles:
                        return user_profiles[self.username][1]
            except IOError:
                pass
            except ValueError:
                pass
        return str(uuid.uuid4())

    @staticmethod
    def adduser(user):
        with open(PROFILE_FILE, 'r+') as f:
            try:
                profiles = json.load(f)
            except ValueError:
                profiles = {}
            profiles[user.get('username')] = [user.get('email'), user.get('name'), 
                                        user.get('title'), user.get('id')]
            f.seek(0, 0)
            f.write(json.dumps(profiles))

    @staticmethod
    def get(user_id):
        if not user_id:
            return None
        try:
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                for user_name, profile in user_profiles.items():
                    if profile[1] == user_id:
                        return User(user_name)
        except:
            return None
        return None
