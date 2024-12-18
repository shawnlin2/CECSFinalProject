from mongoengine import*

from CourseRequirement import CourseRequirement

class RequirementType(Document):
    name = StringField(min_length=10, max_length=80, unique=True)
    course_requirements = ListField(ReferenceField('CourseRequirement'))

    meta = {
            "collection": "requirements",
            "indexes":[
                {"fields":["name"],
                "name":"requirement_types_pk",
                "unique": True
                
                }
            ]
           }
    def __init__(self, name, course_requirements = None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        #We should make an add function to put stuff into course_requirements

    def __str__(self):
        return f'Requirement Type: {self.name}'
    
    def add_course_requirement(self, course_requirement):
        self.course_requirements.append(course_requirement)
    
    def remove_course_requirement(self, course_requirement):
        self.course_requirements.remove(course_requirement)