from flask import Blueprint, request, make_response
from app.celery.tasks import create_transcript
from app.route_guard import auth_required

from app.review.model import *
from app.review.schema import *
from helpers.elevenlabs import vocalize
from helpers.ephemeral import Ephemeral

bp = Blueprint('review', __name__)

@bp.post('/review')
# @auth_required()
def create_review():
    name = request.json.get('name')
    email = request.json.get('email')
    company = request.json.get('company')
    if name and email and company:
        existing_review = Review.get_by_email(email.lower())
        if not existing_review:
            review = Review.create(name, email.lower(), company)
            text = f"Hello {name.split()[0]}, thank you for joining the wait list. In 30 seconds, tell us your experience with {company}."
            speech = vocalize(text)
            response = make_response(speech)
            response.headers['Content-Type'] = 'application/octet-stream'  # Set the content type to octet-stream
            response.headers['Review-Id'] = str(review.id)  # Add the integer as a custom header
            response.headers['Access-Control-Expose-Headers'] = 'Review-Id'
            return response, 201
        else:
            text = f"Sorry {name.split()[0]}, it seem like you've already reviewed {existing_review.company} with your email."
            speech = vocalize(text)
            response = make_response(speech)
            response.headers['Content-Type'] = 'application/octet-stream'  # Set the content type to octet-stream
            return response, 200
    return {'status':'error', 'message':'name, email & company required'}, 400

@bp.get('/review/<int:id>')
# @auth_required()
def get_review(id):
    review = Review.get_by_id(id)
    if review is None:
        return {'message': 'Review not found'}, 404
    return ReviewSchema().dump(review), 200

@bp.patch('/review/<int:id>')
# @auth_required()
def update_review(id):
    review = Review.get_by_id(id)
    if review is None:
        return {'message': 'Review not found'}, 404
    speech = request.files.get('speech')
    transient_audio_file = Ephemeral(speech)
    create_transcript.delay(review.id, transient_audio_file.save())
    text = f"Thank you for your review {review.name.split()[0]}, goodbye!"
    speech = vocalize(text)
    response = make_response(speech)
    response.headers['Content-Type'] = 'application/octet-stream'  # Set the content type to octet-stream
    return response, 200

@bp.delete('/review/<int:id>')
# @auth_required()
def delete_review(id):
    review = Review.get_by_id(id)
    if review is None:
        return {'message': 'Review not found'}, 404
    review.delete()
    return {'message': 'Review deleted successfully'}, 200

@bp.get('/reviews')
# @auth_required()
def get_reviews():
    reviews = Review.get_all()
    return ReviewSchema(many=True).dump(reviews), 200