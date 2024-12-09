from sqlalchemy import *
from sqlalchemy.orm import *
from orm_base import Base

class Catalog(Base):

    title = mapped_column('title', String(30), CheckConstraint('LENGTH(title) > 0'), nullable= False, primary_key=True)
    def __init__(self, title, **kwargs):
        super().__init__()
        self.title = title
