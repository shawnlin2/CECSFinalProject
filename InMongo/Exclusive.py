from mongoengine import *
from Catalog import Catalog
class Exclusive(Catalog):
    meta = {'allow_inheritance': True, 'collection': 'exclusive_catalog'}


    def __init__(self, title: str, **kwargs):
        super().__init__(title, **kwargs)
    
    def __str__(self):
        return f"Exclusive Catalog {self.title}"