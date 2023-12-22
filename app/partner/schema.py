from app import ma
from app.partner.model import *

class PartnerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Partner
        exclude = ('is_deleted',)