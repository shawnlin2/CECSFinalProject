from mongoengine import *

from Course import Course


class Student(Document):
    lastName = StringField(db_field='last_name', min_length=4, max_length=90, required=True)
    firstName = StringField(db_field='first_name', min_length=4, max_length=90, required=True)
    studentID = IntField(min_value=0, max_value=10, required=True, unique=True)

    courses = ListField(ReferenceField('Course'), db_field='courses_taken')


    def clean(self):
        """
        Making sure students don't exceed the 18 unit Max, probably need to keep track of prior takin courses
        """

        total_units = sum(course.unit for course in self.courses)
        if total_units > 18:
            raise ValidationError(f"Total units {total_units} exceeds the max amount of 18 units")

    def __init__ (self, lastName, firstName,studentID,courses= None,**kwargs):
        super().__init__(**kwargs)
        self.firstName = firstName
        self.lastName = lastName
        self.studentID = studentID
        self.courses = courses or []



    def __str__(self):
        course_names = [course.courseName for course in self.courses] if self.courses else "None"
        return f"Student - name: {self.firstName}  {self.lastName}, ID#: {self.studentID}, Courses: {course_names}"
