from app import ma
from app.user.model import *

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        exclude = ('password', 'created_at', 'updated_at')
    agent = ma.Nested("AgentSchema")
