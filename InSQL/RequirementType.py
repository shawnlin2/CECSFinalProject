from sqlalchemy import *
from sqlalchemy.orm import *
from orm_base import Base

class RequirementType(Base):
    name = mapped_column('name', String(80), CheckConstraint('LENGTH(name) > 0', name = 'RequirementType_name'), 
                         nullable= False, primary_key= True)
    
    courseRequirement = relationship(back_populates= 'requirementType', passive_deletes= True)

    def __init__(self, name, **kwargs):
        self.name = name
    
    def __str__(self):
        return f'Name: {self.name}'
    
        
        
