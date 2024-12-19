from mongoengine import *
from Catalog import Catalog
class Exclusive(Catalog):


    def __init__(self, title, courseRequirement,courseRequirementName, degreeType, requirementTypeName, **kwargs):
        super().__init__(title, courseRequirement,courseRequirementName, degreeType, requirementTypeName, **kwargs)
    
    def __str__(self):
        return f"Exclusive Catalog {self.title}"