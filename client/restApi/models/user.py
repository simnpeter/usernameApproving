from mongoengine import Document, StringField, BooleanField, DateTimeField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    approved_ai = BooleanField(required=True)
    approved_human = BooleanField(default=None, null=True)
    is_admin = BooleanField(default=False)
    modified = DateTimeField(default=datetime.now)

    meta = {
        'collection': 'users'
    }