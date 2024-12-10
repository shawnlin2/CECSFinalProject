from sqlalchemy import *
from sqlalchemy.orm import *
from orm_base import Base
from DegreeCatalog import DegreeCatalog

class CourseRequirement(Base):
    totalPoints = mapped_column('totalPoints',Integer(), CheckConstraint('totalPoints > 0 and totalPoints < 100'), nullable= False)
    name = mapped_column('name', String(80), CheckConstraint('LENGTH(name) > 0', name = 'course_requirement_name'), nullable= False, primary_key=True)
    degreeType = mapped_column('degree_type', String(80), 
                         CheckConstraint('LENGTH(type) > 0', name = 'Degree_Catalog_type'), nullable=False, 
                         primary_key= True)
    degreeCatalog = relationship(back_populates= 'courseRequirement')
    catalog = relationship(back_populates= 'courseRequirement')

    __table_args__ = (ForeignKeyConstraint([degreeType], [DegreeCatalog.degreeType]))
    
    def __init__(self, totalPoints, name, degreeCatalog, degreeType, catalog, **kwargs):
        super().__init__(**kwargs)
        self.totalPoints = totalPoints
        self.name = name
        self.degreeCatalog = degreeCatalog
        self.degreeType = degreeType
        self.catalog = catalog
    
    def __str__(self):
        return f'Degree Type{self.degreeType}, Course Requirement {self.name}, Total Points: {self.totalPoints}'
    