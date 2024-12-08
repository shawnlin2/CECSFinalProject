from mongoengine import *

class Course(Document):
    """Course Offered within a Department and in line with a Degree Catalog
     Ensures that a student takes classes that they need to take an avoid taking
     classes that they do not need"""

    #The number of the Course
    courseNum = IntField(required= True)


    #The length of the Lecture
    lectureHour = IntField(required= True)

    #The name of the course
    courseName = StringField(min_length=3, max_length=60, required=True, unique=True)

    #The units the course is worth
    unit = IntField(required=True)

    #Department that offers said course
    department = ReferenceField('Department', required=True)

    isUpperDivision = BooleanField()





    def clean(self):
        """This is just ensuring the course number is between a required amount, this is called & Units are the correct amount
        when you call a .save( ) mongo engine will automatically run this clean method, this is to check the numbies
        for the course number are valid."""

        if( 10 < self.courseNum > 9999):
            raise ValidationError(f"Error the course number must be between 10 and 9999, the number entered was {self.courseNum}")

        if(0 <= self.unit >5):
            raise ValidationError(f"Error the number of units must be between 1 - 5 units, the units you entered were {self.unit}")


        #If the courseNum is greater than 300 returns True, else returns False, and we don't have to promprt
        #User for any info since its solely based off of the courseNumber
        self.isUpperDivision = self.courseNum >= 300


    def __init__ (self, courseNum, lectureHour,courseName,unit, department, **kwargs):
        super().__init__(**kwargs)
        self.courseNum = courseNum
        self.lectureHour = lectureHour
        self.courseName = courseName
        self.unit = unit
        self.department = department


    def __str__(self):
        return f'Course {self.courseName}, Course number {self.courseNum}, Hours of lecture {self.lectureHour}, Number of units {self.unit}, Department of {self.course.department.name} '

