from mongoengine import *

class Student(Document):
    lastName = StringField(db_field='last_name', min_length=4, max_length=90, required=True)
    firstName = StringField(db_field='first_name', min_length=4, max_length=90, required=True)
    studentID = IntField(min_value=0, max_value=10, required=True, unique=True)


