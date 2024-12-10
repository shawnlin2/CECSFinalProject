from mongoengine import *

class DegreeCatalog(Document):
    """What Degrees are available within what department ensuring Data Integrity"""
    degree_choices = (
        (1,'Bachelor'),
        (2,'Master'),
    )

    degree_type = IntField(required= True, choices=degree_choices)
    department = ReferenceField('Department', required=True, reverse_delete_rule=CASCADE)
    degreeProgramName = StringField(required=True, unique=True, max_length=100)

    meta = {
        'collection': 'degree_program',
        'indexes': [
            'degree_type', 
            'department',
        ]
    }

    def __str__(self):
        return f'{self.degree_type}, Department {self.department}, Degree Program Name {self.degreeProgramName} '
