from app import celery, db

import os
from app.call.model import Call, Response
from app.partner.model import Partner
from app.resource.model import Resource

from app.review.model import Review
from helpers.gemini import pinecone_train_with_resource
from helpers.langchain import delete_resource, qa_chain, train_with_resource
from helpers.openai import transcribe, rewrite



@celery.task
def create_transcript(review_id, transient_audio_file=None):
    try:
        if transient_audio_file:
            print(transient_audio_file)
            review = Review.get_by_id(review_id)
            transcript = transcribe(transient_audio_file)
            review.content = rewrite(transcript).get('content')
            review.update()
            os.remove(transient_audio_file)
            return "Review Generated Successfully!"
    except Exception as e:
        print(e)
        if transient_audio_file:
            try:
                os.remove(transient_audio_file)
            except:
                pass
        db.session.rollback()
        return "Review Could Not Be Generated Successfully!"

@celery.task
def start_training(resource_id):
    try:
        
        resource = Resource.get_by_id(resource_id)
        partner = Partner.get_by_id(resource.partner_id)
        resource.update(training_status = 'pending')
        
        # train_with_resource(resource.url, partner.identity)
        pinecone_train_with_resource(resource.url, partner.identity)
        resource.update(training_status = 'complete')
        return "Resource Training Completed Successfully!"
    except Exception as e:
        print(e)
        resource.update(training_status = 'failed')
        return "Resource Training Could Not Be Intialized Successfully!"

@celery.task
def undo_training(resource_id):
    try:
        
        resource = Resource.get_by_id(resource_id)
        partner = Partner.get_by_id(resource.partner_id)
        resource.update(training_status = 'pending')
        
        delete_resource(resource.url, partner.identity)
        resource.delete()
        return "Resource Deleted Successfully!"
    except Exception as e:
        print(e)
        db.session.rollback()
        return "Resource could not be deleted!"

@celery.task
def do_long_call(user_id, session_id, question, partner_id):
    try:
        
        history = Call.get_by_user_id_and_session_id(user_id, session_id)
        partner = Partner.get_by_id(partner_id)
        answer = qa_chain(question, history, partner)
        Call.create(user_id, partner.id, session_id, question, answer)
        Response.create(user_id, partner_id, session_id, answer)
        return "Call Completed Successfully!"
    except Exception as e:
        print(e)
        db.session.rollback()
        return "Call failed!"