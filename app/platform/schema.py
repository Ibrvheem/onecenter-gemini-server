from app import ma
from app.platform.model import *

class PlatformSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Platform
        exclude = ('is_deleted',)