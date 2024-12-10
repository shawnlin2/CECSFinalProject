from sqlalchemy import *
from sqlalchemy.orm import *

from orm_base import Base

class CatalogCourse(Base):
    catalog = relationship(back_populates= 'catalogCourse')
    course = relationship(back_populates='catalogCourse')
    title = mapped_column('title', String())