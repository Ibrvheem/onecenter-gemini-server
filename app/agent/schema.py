from app import ma
from app.agent.model import *

class AgentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Agent
        include_fk = True
        exclude = ('is_deleted',)