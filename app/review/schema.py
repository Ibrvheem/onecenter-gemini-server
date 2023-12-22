from app import ma
from app.review.model import *

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        exclude = ('is_deleted',)