from mongoengine import *

class Department(Document):
    """An organization within a college within a university that provides one or more
    degree programs to its students."""
    name = StringField(min_length=3, max_length=80, required=True, unique=True)
    abbreviation = StringField(min_length=1, max_length=16, required=True)
    courses = ListField(ReferenceField('Course'))
    degreeCatalogs = ListField(ReferenceField('DegreeCatalog'))
    def __init__ (self, name, abbreviation,  **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.abbreviation = abbreviation

    meta = {
            "collection": "departments",
            "indexes":[
                {"fields":["abbreviation"],
                "name":"departments_pk",
                "unique": True
                
                }
            ]
           }
    def __str__(self):
        return f"Department - abbreviation: {self.abbreviation} name: {self.name}"
    
    def add_course(self, course):
        self.courses.append(course)
    
    def remove_course(self, course):
        self.courses.remove(course)
    
    def add_degreeCatalog(self, degreeCatalog):
        self.degreeCatalogs.append(degreeCatalog)
    
    def remove_degreeCatalog(self, degreeCatalog):
        self.degreeCatalogs.remove(degreeCatalog)