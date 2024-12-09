from sqlalchemy import String, Integer,CheckConstraint, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped
from orm_base import Base
class Department(Base):
    abbreviation = mapped_column('abbreviation',String(16), CheckConstraint('LENGTH(name) > 3'),
                                 nullable= False, primary_key= True)
    name = mapped_column('name', String(80), CheckConstraint('LENGTH(name) > 3'), nullable= False)
    __table_args__ = (UniqueConstraint('name', name= 'department_uk_01'))
    
    def __init__ (self, name, abbreviation, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.abbreviation = abbreviation

    def __str__(self):
        return f"Department - abbreviation: {self.abbreviation} name: {self.name}"