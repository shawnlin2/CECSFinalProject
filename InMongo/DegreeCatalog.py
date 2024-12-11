
from mongoengine import *

from Department import Department

from Requirements import Requirements

class DegreeCatalog(Document):
    """What is Required to take a course"""
    degree_type = StringField(min_length=10, max_length=80, required=True)

    abbreviation = StringField(min_length=6,max_length=16, required=True)
    department = ReferenceField(Department, reverse_delete_rule=2)
    catalog_requirements = ListField(ReferenceField(Requirements, reverse_delete_rule=2))



    def __init__ (self, degree_type, abbreviation,department,catalog_requirements, **kwargs):
        super().__init__(**kwargs)
        self.degree_type= degree_type
        self.abbreviation = abbreviation
        self.department = department
        self.catalog_requirements = catalog_requirements


    def __str__(self):
        return f'Degree Type {self.degree_type}, Abbreviation  {self.abbreviation}, Abbreviation {self.department.abbreviation}, Department {self.department.name}'



