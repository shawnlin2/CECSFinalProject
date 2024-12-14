from sqlalchemy import *
from sqlalchemy.orm import *
from orm_base import Base
from Department import Department
class DegreeCatalog(Base):
    degreeType = mapped_column('degree_type', String(80), 
                         CheckConstraint('LENGTH(type) > 0', name = 'Degree_Catalog_type'), nullable=False, 
                         primary_key= True)
    abbreviation = mapped_column('abbreviation', String(16), CheckConstraint('LENGTH(abbreviation) > 2', name = 'Degree_Catalog_abbreviation'), nullable= False)
    department = relationship(back_populates= 'degreeCatalog')
    catalogRequirement = relationship(back_populates='degreeCatalog')

    __table_args__ = (ForeignKeyConstraint([department], [Department.abbreviation]),)

    def __init__(self, degreeType, abbreviation, department, **kwargs):
        super().__init__(**kwargs)
        self.degreeType = degreeType
        self.abbreviation = abbreviation
        self.department = department
    
    def __str__(self):
        return f'Degree Type {self.degreeType}, Abbreviation: {self.abbreviation}'


