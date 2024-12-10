from sqlalchemy import *
from sqlalchemy.orm import *
from orm_base import Base

class Catalog(Base):

    title = mapped_column('title', String(30), CheckConstraint('LENGTH(title) > 0'), nullable= False, primary_key=True)
    catalogType = mapped_column('catalog_type', String(80), nullable = False)
    courseRequirement = relationship(back_populates= 'catalog', passive_deletes= 'all')
    catalogCourse = relationship(back_populates= 'catalog', passive_deletes= 'all')
    __mapper_args__ = {'polymorphic_on': catalogType}
    def __init__(self, title, **kwargs):
        super().__init__()
        self.title = title

    def __str__(self):
        return f'Catalog Title: {self.title}, Catalog Type: {self.catalogType}'
