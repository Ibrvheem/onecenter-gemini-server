from app import ma
from app.resource.model import *

class ResourceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Resource
        exclude = ('is_deleted',)