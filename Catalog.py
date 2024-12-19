from mongoengine import *
from CourseRequirement import CourseRequirement

class Catalog(Document):
    title = StringField(min_length=0, max_length=30, required=True)
    catalog_courses = ListField(ReferenceField('CatalogCourse'))
    course_requirement = ReferenceField(CourseRequirement, reverse_delete_rule = 2)
    course_requirementName = StringField(min_length = 1, max_length=80, required=True)
    degreeType = StringField(min_length=10, max_length=80, required=True)
    requirementTypeName = StringField(min_length=1, max_length=80)
    meta = {
            "collection": "catalogs",
            "indexes":[
                {"fields":['title'],
                "name":"catalogs_pk",
                "unique": True
                
                }
            ],
            "index_cls": False,
            'allow_inheritance': True
           }
    
    def __init__(self, title, courseRequirement,courseRequirementName, degreeType, requirementTypeName, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.course_requirement = courseRequirement
        self.course_requirementName = courseRequirementName
        self.degreeType = degreeType
        self.requirementTypeName = requirementTypeName
        #Removed the calls here as we can use an add function to put catalog_courses into the table

    def add_catalog_course(self, catalog_course):
        self.catalog_courses.append(catalog_course)
    def remove_catalog_course(self, catalog_course):
        self.catalog_courses.remove(catalog_course)
    
    def __str__(self):
        return f"Catalog Title - {self.title}"