from mongoengine import *
from Catalog import Catalog

class Inclusive(Catalog):
    
    def __init__(self, title: str, **kwargs):
        super().__init__(title, **kwargs)
    
    def __str__(self):
        return f"{super(Inclusive, self).__str__()} Inclusive"