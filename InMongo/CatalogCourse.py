
from mongoengine import *

from Catalog import Catalog
from Course import Course

class CatalogCourse(Document):
    catalog = ReferenceField(Catalog, reverse_delete_rule=2)
    course = ReferenceField(Course, reverse_delete_rule=2)
    title = StringField(min_length=10, max_length=30, required=True, unique=True)
    name = StringField(min_length=8 ,max_length=80, required= True, unique=True)

    def clean(self):
        if len(self.title) == 0:
            raise ValidationError("Title must not be empty")
        if len(self.name):
            raise  ValidationError("Name must not be empty ")

    def __init__(self, catalog, course, title, name, **kwargs):
        super().__init__(**kwargs)
        self.catalog = catalog
        self.course = course
        self.title = title
        self.name = name

    def __str__(self):
        return f'Catalog {self.title}, Course {self.name}'