from sqlalchemy import *
from sqlalchemy.orm import *

from orm_base import Base
from Catalog import Catalog
from Course import Course

class CatalogCourse(Base):
    catalog = relationship(back_populates= 'catalogCourse')
    course = relationship(back_populates='catalogCourse')
    title = mapped_column('title', String(30), CheckConstraint('LENGTH(title) > 0'), nullable= False, primary_key=True)
    name = mapped_column('name', String(80), CheckConstraint('LENGTH(name) > 0', name = 'Course_name'), nullable= False
                         , primary_key= True)
    __table_args__ = (ForeignKeyConstraint([title], [Catalog.title]), ForeignKeyConstraint([name], [Course.name]))

    def __init__(self, catalog, course, title, name, **kwargs):
        super().__init__(**kwargs)
        self.catalog = catalog
        self.course = course
        self.title = title
        self.name = name
    
    def __str__(self):
        return f'Catalog: {self.title}, Course: {self.name}'
    
    
    