
from mongoengine import *
from Department import Department
class DegreeCatalog(Document):
    """What is Required to take a course"""
    degree_type = StringField(min_length=10, max_length=80, required=True)

    total_units = IntField(required=True)

    abbreviation = StringField(min_length=1,max_length=16, required=True)
    department = ReferenceField(Department, reverse_delete_rule= 2)
    course_requirements = ListField(ReferenceField('CourseRequirement'))

    meta = {
            "collection": "degree_catalogs",
            "indexes":[
                {"fields":["degree_type"],
                "name":"degree_catalogs_pk",
                "unique": True
                
                }
            ]
           }

    def __init__ (self, degree_type, department,total_units, abbreviation, **kwargs):
        super().__init__(**kwargs)
        self.degree_type= degree_type
        self.department = department
        self.total_units = total_units
        self.abbreviation = abbreviation
        # self.catalog_requirements = catalog_requirements


    def __str__(self):
        return f'Degree Type {self.degree_type}, Abbreviation {self.department.abbreviation}, Department {self.department.name}'

    def add_course_requirement(self, courseRequirement):
        self.course_requirements.append(courseRequirement)
    
    def remove_course_requirement(self, courseRequirement):
        self.course_requirements.remove(courseRequirement)

