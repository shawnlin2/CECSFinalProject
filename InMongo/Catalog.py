from mongoengine import *
from CourseRequirement import CourseRequirement

class Catalog(Document):
    title = StringField( min_length=0, max_length=30, required=True)
    catalog_type = StringField(required=True, max_length=80)
    catalog_courses = ListField(ReferenceField('CatalogCourse'))
    course_requirement = ReferenceField(CourseRequirement, reverse_delete_rule = 2)
    def __init__(self, title, catalog_type, *args, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.catalog_type = catalog_type
        #Removed instances of ListField since when you create a catalogCourse object it will automatically fill the space
        #If not you would just make an add function like in his sample for Advance HW
    def __str__(self):
        return f"Catalog Title - {self.title}, Catalog Type - {self.catalog_type}"