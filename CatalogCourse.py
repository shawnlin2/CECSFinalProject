
from mongoengine import *

from Catalog import Catalog
from Course import Course

class CatalogCourse(Document):
    catalog = ReferenceField(Catalog, reverse_delete_rule=2)
    course = ReferenceField(Course, reverse_delete_rule = 2)
    title = StringField(min_length=10, max_length=30, required=True)
    abbreviation = StringField(min_length=1, max_length=16, required=True)
    courseNum = IntField(min_value=10, max_value=999, primary_key=True)
    

    meta = {
            "collection": "course_requirements",
            "indexes":[
                {"fields":['title', 'abbreviation', 'courseNum' ],
                "name":"requirement_types_pk",
                "unique": True
                
                }
            ]
           }
    
    def clean(self):
        if len(self.title) == 0:
            raise ValidationError("Title must not be empty")
        if len(self.name):
            raise  ValidationError("Name must not be empty ")

    def __init__(self, catalog, course, title, abbreviation, courseNum, name, courseRequirementName, degreeType, requirementTypeName, **kwargs):
        super().__init__(**kwargs)
        self.catalog = catalog
        self.course = course
        self.title = title
        self.name = name
        self.abbreviation = abbreviation
        self.courseNum = courseNum
        self.course_requirementName = courseRequirementName
        self.degreeType = degreeType
        self.requirementTypeName = requirementTypeName
    def __str__(self):
        return f'Catalog {self.title}, Course {self.name}'