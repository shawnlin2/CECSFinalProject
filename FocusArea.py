from mongoengine import*

class FocusArea(Document):
    """Class to define Focus area Selecting one of three Focus areas
        / with the other optional courses"""

    name = StringField(min_length=3, max_length= 100, required=True, unique=True)

    description = StringField(min_length=10, max_length=300, required=True)

    mandatory_course = ReferenceField('Course', required=True)

    optional_courses = ListField(ReferenceField('Course'))

    meta = {
        'indexes':[
            {'fields' : ['name'],'unique' : True}
        ]
    }

    def clean(self):
        if not self.mandatory_course.isUpperDivision:
            raise ValidationError(f"The Mandatory Course is f{self.mandatory_course} is not upper division")

        for course in self.optional_courses:
            if not course.isUpperDivision:
                raise ValidationError(f'The optional course {course.courseName} is not upper Division')


    def __init__ (self, name, description,mandatory_course,optional_course, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.mandatory_course = mandatory_course
        self.optional_courses = optional_course
    def __str__(self):
        return (f"Focuse area {self.name} : {self.description}, Mandatory Course: {self.mandatory_course}\n "
                 f"Optional courses {[course.courseName for course in self.optional_courses]}")