
from mongoengine import *

class Requirements(Document):
    """What is Required to take a course"""
    units = IntField(required=True)


