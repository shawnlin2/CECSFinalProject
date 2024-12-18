from mongoengine import *
from Catalog import Catalog

class Inclusive(Catalog):

    meta = {'allow_inheritance': True, 'collection': 'inclusive_catalog'}
    
    def __init__(self, title: str, **kwargs):
        super().__init__(title, **kwargs)
    
    def __str__(self):
        return f"Inclusive Catalog: {self.title}"