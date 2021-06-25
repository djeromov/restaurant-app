#models for google firestore NoSQL database

from datetime import datetime
import pytz
import locale

from flask_login import UserMixin

#for encrypting passwords
from flask_bcrypt import Bcrypt

from gfs_connection import db


bcrypt = Bcrypt()

class User(UserMixin):
    """User."""

    def __init__(self, username, password, is_admin=False, isDeletable=True):
        self.username = username
        self.id = username #for flask-login to work
        self.password = password
        self.is_admin = is_admin 
        self.isDeletable = isDeletable

    @staticmethod
    def from_dict(source):
        return User(source['username'], source['password'], source['is_admin'], source['isDeletable'])

    def to_dict(self):
        return {
            'username' : self.username,
            'password' : self.password,
            'is_admin' : self.is_admin,
            'isDeletable' : self.isDeletable
        }


    @classmethod
    def register(cls, username, password, is_admin):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        #coerce form input
        if type(is_admin) != bool:
            is_admin_bool = True if is_admin == "True" else False
        else:
            is_admin_bool = is_admin

        new_user = cls(username=username, password=hashed_utf8, is_admin=is_admin_bool)

        db.collection('users').document(username).set(new_user.to_dict())

        # return instance of user w/username and hashed pwd
        return new_user

    @classmethod
    def delete(cls, username):
        user = cls.get(username)
        if user.isDeletable:
            db.collection('users').document(username).delete()
            return True
        else:
            return False


    @staticmethod
    def get(username):
        doc = db.collection('users').document(username).get()
        if doc.exists:
            return User.from_dict(doc.to_dict())
        else:
            return None

    @staticmethod
    def get_all():
        docs = db.collection('users').stream()
        return [doc.to_dict() for doc in docs]


    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """
        user = User.get(username)

        if user and bcrypt.check_password_hash(user.password, password):
            # return user instance
            return user
        else:
            return False


class Restaurant():
    """Restaurant."""

    @staticmethod
    def get_menu():
        doc = db.collection('restaurant').document('menu').get()

        if doc.exists:
            menu = doc.to_dict()['text']
        else:
            menu = ''

        return menu


    @staticmethod
    def set_menu(user_input):

        updated_menu = {
            'text' : user_input
        }
        db.collection('restaurant').document('menu').set(updated_menu)


    @staticmethod
    def get_whatsapp_phone():
        doc = db.collection('restaurant').document('settings').get()


        if doc.exists:
            whatsapp_phone = doc.to_dict()['whatsapp_phone']
        else:
            whatsapp_phone = ''

        return whatsapp_phone

    @staticmethod
    def set_whatsapp_phone(whatsapp_phone):

        settings_ref = db.collection('restaurant').document('settings')
        settings_ref.update({'whatsapp_phone': whatsapp_phone})

    @property
    def whatsapp_phone(cls):
        return cls.get_whatsapp_phone()

    @property
    def menu(cls):
        return cls.get_menu()

    @property
    def today(cls):
        locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')
        time_zone = pytz.timezone('America/Bogota')
        current_time = datetime.now(tz=time_zone)
        return f"{current_time.strftime('%A %-d %B %Y').title()}"

