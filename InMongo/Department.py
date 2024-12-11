from mongoengine import *
from DegreeCatalog import DegreeCatalog
from Course import Course

class Department(Document):
    """An organization within a college within a university that provides one or more
    degree programs to its students."""
    name = StringField(min_length=3, max_length=80, required=True, unique=True)
    abbreviation = StringField(min_length=3, max_length=16, required=True)
    degree_catalogs = ListField(ReferenceField(DegreeCatalog, reverse_delete_rule=2))
    courses = ListField(ReferenceField(Course, reverse_delete_rule=2))

    def __init__ (self, name, abbreviation,degree_catalogs,courses,  **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.abbreviation = abbreviation
        self.degree_catalogs = degree_catalogs
        self.courses = courses if courses else []

    def __str__(self):
        return f"Department - abbreviation: {self.abbreviation} name: {self.name}"