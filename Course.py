from mongoengine import *
from Department import Department
class Course(Document):
    """Course Offered within a Department and in line with a Degree Catalog."""

    # The number of the Course
    courseNum = IntField(min_value=10, max_value=999)

    # The length of the Lecture
    lectureHour = IntField(required=True)

    # The name of the course
    courseName = StringField(min_length=3, max_length=60, required=True)

    # The units the course is worth
    unit = IntField(min_value=1, max_value=5, required=True)

    # Department that offers said course
    department = ReferenceField(Department, required=True, reverse_delete_rule=2)
    abbreviation = StringField(min_length=1, max_length=16, required=True)

    course_catologs = ListField(ReferenceField('CatalogCourse'))
    meta = {
            "collection": "courses",
            "indexes":[
                {"fields":["abbreviation", 'courseNum'],
                "name":"courses_pk",
                "unique": True
                
                }
            ]
           }

    @property
    def isUpperDivision(self):
        """Determine if the course is upper-division based on course number."""
        return self.courseNum >= 300

    def __init__(self, courseNum, lectureHour, courseName, unit, department, abbreviation, **kwargs):
        super().__init__(**kwargs)
        self.courseNum = courseNum
        self.lectureHour = lectureHour
        self.courseName = courseName
        self.unit = unit
        self.department = department
        self.abbreviation = abbreviation

    def __str__(self):
        return (
            f"Course: {self.courseName}, Course number: {self.courseNum}, "
            f"Lecture hours: {self.lectureHour}, Units: {self.unit}, "
            f"Department: {self.department.abbreviation}"
        )
    def add_course_catalog(self, course_catalog):
        self.course_catologs.append(course_catalog)
    
    def remove_course_catalog(self, course_catalog):
        self.course_catologs.remove(course_catalog)
    