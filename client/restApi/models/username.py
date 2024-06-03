from mongoengine import Document, StringField, BooleanField

class Username(Document):
    username = StringField(required=True, unique=True)
    label = BooleanField(required=True)
