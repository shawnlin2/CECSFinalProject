from sqlalchemy import *
from sqlalchemy.orm import *
from orm_base import Base
from Department import Department
class DegreeCatalog(Base):
    type = mapped_column('type', String(80), 
                         CheckConstraint('LENGTH(type) > 0', name = 'Degree_Catalog_type'), nullable=False, 
                         primary_key= True)
    abbreviation = mapped_column('abbreviation', String(16), CheckConstraint('LENGTH(abbreviation) > 2', name = 'Degree_Catalog_abbreviation'), nullable= False)
    department = relationship(back_populates= 'degreeCatalog')
    catalog = relationship(back_populates= 'degreeCatalog', passive_deletes= 'all')
    

    __table_args__ = (ForeignKeyConstraint([department], [Department.abbreviation]),)

