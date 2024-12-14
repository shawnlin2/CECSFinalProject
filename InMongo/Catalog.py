from mongoengine import *

class Catalog(Document):
    title = StringField( min_length=0, max_length=30, required=True)
    catalog_type = StringField(required=True, max_length=80)
    # course_requirements = ListField(ReferenceField('CourseRequirement',reverse_delete_rule=CASCADE))
    # catalog_courses = ListField(ReferenceField('CatalogCourse',reverse_delete_rule=CASCADE))

    def __init__(self, title, catalog_type, *args, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.catalog_type = catalog_type
        # self.course_requirements = course_requirements if course_requirements else [] #just make sures the list is empty defaults to an empty list
        # self.catalog_courses = catalog_courses if catalog_courses else []
    def __str__(self):
        return f"Catalog Title - {self.title}, Catalog Type - {self.catalog_type}"