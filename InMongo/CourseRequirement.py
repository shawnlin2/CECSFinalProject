from mongoengine import*

from DegreeCatalog import DegreeCatalog

class CourseRequirement(Document):
    total_points = IntField(min_value=1, max_value=100, required=True)
    name = StringField(max_length=80, unique=True, required=True)
    degree_type = StringField(max_length=80, required=True)
    degree_catalog = ReferenceField(DegreeCatalog, reverse_delete_rule=2)
    catalog = ListField(ReferenceField('Catalog'))

    def __init__(self, total_points, name, degree_type, degree_catalog, **kwargs):
        super().__init__(**kwargs)
        self.total_points = total_points
        self.name = name
        self.degree_type = degree_type
        self.degree_catalog = degree_catalog

    def clean(self):
        if len(self.name) == 0:
            raise ValidationError("Course requirement name must not be empty")

    def __str__(self):
        return f'Course Requirement: {self.name}, Degree Type: {self.degree_type}, Total Points:  {self.total_points}'
