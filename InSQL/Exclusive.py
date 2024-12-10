from sqlalchemy import *
from sqlalchemy.orm import *
from Catalog import Catalog

class Exclusive(Catalog):
    __mapper_args__ = {'polymorphic_identity': 'exclusive'}
    def __init__(self, title, **kwargs):
        super().__init__(title, **kwargs)

    def __str__(self):
        return super().__str__() + "Exclusive"