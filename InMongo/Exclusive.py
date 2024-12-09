from mongoengine import *
from InMongo.Catalog import Catalog

class Exclusive(Catalog):
    
    def __init__(self, title: str, **kwargs):
        super().__init__(title, **kwargs)
    
    def __str__(self):
        return f"{super(Exclusive, self).__str__()} Exclusive"