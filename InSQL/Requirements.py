from sqlalchemy import *
from sqlalchemy.orm import *
from Catalog import Catalog

class Requirements(Catalog):
    remainingUnits = mapped_collection('remaining_units', INTEGER, 
                                       CheckConstraint('remaining_units > 0 and remaining_units < 20'), nullable = False)
    
    def __init__(self, title, remainingUnits, **kwargs):
        super().__init__(title, **kwargs)
        self.remainingUnits = remainingUnits
