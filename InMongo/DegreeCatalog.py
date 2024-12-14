
from mongoengine import *

class DegreeCatalog(Document):
    """What is Required to take a course"""
    degree_type = StringField(min_length=10, max_length=80, required=True)

    total_units = IntField(required=True)

    # abbreviation = StringField(min_length=1,max_length=16, required=True)
    department = ReferenceField('Department')
    # catalog_requirements = ListField(ReferenceField('Requirements'))


    def __init__ (self, degree_type, department,total_units, **kwargs):
        super().__init__(**kwargs)
        self.degree_type= degree_type
        self.department = department
        self.total_units = total_units
        # self.catalog_requirements = catalog_requirements


    def __str__(self):
        return f'Degree Type {self.degree_type}, Abbreviation {self.department.abbreviation}, Department {self.department.name}'



