from app import ma
from app.call.model import *

class CallSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Call
        exclude = ('is_deleted',)