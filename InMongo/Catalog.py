from mongoengine import *

class Catalog(Document):
    title = StringField(db_field='title', min_length=0, max_length=30, required=True)

    meta = {'allow_inheritance': True, 'collection': 'catalogs'}

    def __init__(self, title: str, *args, **kwargs):
        super(Catalog, self).__init__(**kwargs)
        self.title = title
    
    def __str__(self):
        return f"Catalog - {self.title}"