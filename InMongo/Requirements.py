
from mongoengine import *
from Catalog import Catalog

class Requirements(Catalog):
    """What is Required to take a course"""
    remaining_units = IntField(min_value=1, max_value=20, required=True)

    def __init__(self,title,remaining_units):
        super().__init__(title=title)
        self.remaining_units = remaining_units



    def __str__(self):
        return f'Requirements Catalog {self.title}, Remaining Units: {self.remaining_units}'
