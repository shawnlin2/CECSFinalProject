from mongoengine import *
from CourseRequirement import CourseRequirement

class Catalog(Document):
    title = StringField('title', min_length=0, max_length=30, required=True)
    catalog_type = StringField('catalogType', required=True, max_length=80)
    catalog_courses = ListField(ReferenceField('CatalogCourse'))
    course_requirement = ReferenceField(CourseRequirement, reverse_delete_rule = 2)
    course_requirementName = StringField('courseRequirementName',min_length = 1, max_length=80, unique=True, required=True)
    degreeType = StringField('degreeType', min_length=10, max_length=80, required=True)
    requirementTypeName = StringField('requirementTypeName', min_length=10, max_length=80)
    meta = {
            "collection": "course_requirements",
            "indexes":[
                {"fields":["degreeType", 'requirementTypeName', 'course_requirementName', 'title'],
                "name":"requirement_types_pk",
                "unique": True
                
                }
            ]
           }
    def __init__(self, title, catalog_type, *args, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.catalog_type = catalog_type
        #Removed the calls here as we can use an add function to put catalog_courses into the table

    def add_catalog_course(self, catalog_course):
        self.catalog_courses.append(catalog_course)
    def remove_catalog_course(self, catalog_course):
        self.catalog_courses.remove(catalog_course)
    
    def __str__(self):
        return f"Catalog Title - {self.title}, Catalog Type - {self.catalog_type}"