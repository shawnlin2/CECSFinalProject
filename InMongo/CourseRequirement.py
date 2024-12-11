from mongoengine import*

class CourseRequirement(Document):
    total_points = IntField(min_value=1, max_value=100, required=True)
    name = StringField(max_length=80, unique=True, required=True)
    '''The thing I think we need to fix here is that if we're already referencing the degree catalog thus I dont think we need
    the degree type in here since can pull it from degree catalog thus I dont think it should be in the init either lmk
    what yall think ?'''
    # degree_type = ReferenceField('DegreeCatalog') # I think this should be a refernce field passed in from degree catalog and maybe not an object
    degree_catalog = ReferenceField('DegreeCatalog')

    def __init__(self, total_points, name, degree_catalog, **kwargs):
        super().__init__(**kwargs)
        self.total_points = total_points
        self.name = name
        self.degree_catalog = degree_catalog

    def clean(self):
        if len(self.name) == 0:
            raise ValidationError("Course requirement name must not be empty")

    def __str__(self):
        return f'Course Requirement: {self.name}, Degree Type: {self.degree_catalog.degree_type}, Total Points:  {self.total_points}'
