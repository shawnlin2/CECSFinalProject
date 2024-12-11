from mongoengine import*

from CourseRequirement import CourseRequirement

class Requirement(Document):
    name = StringField(min_length=10, max_length=80, unique=True)
    course_requirements = ListField(ReferenceField('CourseRequirement', reverse_delete_rule=CASCADE))

    def __init__(self, name, course_requirements = None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.course_requirements = course_requirements if course_requirements else []

    def __str__(self):
        return f'Requirement Type: {self.name}'