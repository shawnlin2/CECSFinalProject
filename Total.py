from mongoengine import *
from Catalog import Catalog

class Total(Catalog):
    remainingUnits = IntField(db_field='remaining_units', min_value=1, max_value=50, required=True)

    def __init__(self, title: str, remainingUnits: int, **kwargs):
        super().__init__(title, **kwargs)
        self.remainingUnits = remainingUnits
    
    def __str__(self):
        return f"{super(Total, self).__str__()} Remaining Units: {self.remainingUnits}"