from sqlalchemy import *
from sqlalchemy.orm import *
from orm_base import Base
from Department import Department
class Course(Base):
    num = mapped_column('num',Integer(), CheckConstraint('num > 0', name = 'Course_num'), nullable= False, primary_key=True)
    lectureHour = mapped_column('lecture_hour', Time(), nullable = False)
    name = mapped_column('name', String(80), CheckConstraint('LENGTH(name) > 0', name = 'Course_name'), nullable= False)
    unit = mapped_column('unit', Integer(), CheckConstraint('unit > 0 and unit < 5', name = 'Course_unit'), nullable=False)
    isUpper = mapped_column('is_upper', Boolean(), nullable= False)

    courseCatolog = relationship(back_populates='course', passive_deletes= 'all')
    department = relationship(back_populates= 'course')
    abbreviation = mapped_column('abbreviation',String(16), CheckConstraint('LENGTH(name) > 3'),
                                 nullable= False, primary_key= True)
    __table_args__ = (ForeignKeyConstraint([abbreviation], [Department.abbreviation]),)
    
    def __init__(self, num, lectureHour, name, unit, isUpper, courseCatolog, abbreviation, **kwargs):
        super().__init__(**kwargs)
        self.num = num
        self.lectureHour = lectureHour
        self.name = name
        self.unit = unit
        self.isUpper = isUpper
        self.courseCatolog = courseCatolog
        self.abbreviation = abbreviation
    
    def __str__(self):
        return f''