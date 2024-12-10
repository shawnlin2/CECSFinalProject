
from mongoengine import *

class Requirements(Document):
    """What is Required to take a course"""
    degree_type = ReferenceField('DegreeCatalog', required=True)
    name = StringField(min_length=10, max_length=30, required=True) 
    total_point = IntField(required=True)

    meta = {
        'collection': 'requirements',
        'indexes': [
            {'fields': ['degree_type', 'name'], 'unique': True}
        ]
    }#This pretty much creates the unique composite with the degree type FK and the name as a Pk think composite key

    def __init__ (self, degree_type, name,total_point, **kwargs):
        super().__init__(**kwargs)
        self.degree_type= degree_type
        self.name = name
        self.total_point = total_point


    def __str__(self):
        return f'Degree Type {self.degree_type}, Name  {self.name}, Total Points {self.total_point}'



