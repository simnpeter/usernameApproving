from mongoengine import Document, StringField, BooleanField

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    approved = BooleanField(required=True)
    approved_human = BooleanField(default=False)
    is_admin = BooleanField(default=False)