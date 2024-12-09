from sqlalchemy import *
from sqlalchemy.orm import *
from Catalog import Catalog

class Exclusive(Catalog):
    def __init__(self, title, **kwargs):
        super().__init__(title, **kwargs)

    def __str__(self):
        return super().__str__() + "Exclusive"