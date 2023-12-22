from flask import Blueprint, g, request
from app.agent.model import Agent
from app.celery.tasks import start_training, undo_training
from app.route_guard import auth_required

from app.resource.model import *
from app.resource.schema import *

bp = Blueprint('resource', __name__)

@bp.post('/resource')
@auth_required('agentadmin')
def create_resource():
    title = request.json.get('title')
    description = request.json.get('description')
    url = request.json.get('url')
    if not url:
        return {'message': 'Resource URL can not be empty'}, 400
    agent = Agent.get_by_user_id(g.user.id)
    resource = Resource.create(title, description, url, agent.partner_id)
    return ResourceSchema().dump(resource), 201

@bp.get('/resource/<int:id>')
@auth_required('agentadmin')
def get_resource(id):
    resource = Resource.get_by_id(id)
    if resource is None:
        return {'message': 'Resource not found'}, 404
    return ResourceSchema().dump(resource), 200

@bp.patch('/resource/<int:id>')
@auth_required('agentadmin')
def update_resource(id):
    resource = Resource.get_by_id(id)
    if resource is None:
        return {'message': 'Resource not found'}, 404
    title = request.json.get('title')
    description = request.json.get('description')
    url = request.json.get('url')
    resource.update(title, description, url)
    return ResourceSchema().dump(resource), 200

@bp.delete('/resource/<int:id>')
@auth_required('agentadmin')
def delete_resource(id):
    resource = Resource.get_by_id(id)
    if resource is None:
        return {'message': 'Resource not found'}, 404
    undo_training.delay(resource.id)
    return {'message': 'Resource Scheduled for Removal'}, 200

@bp.get('/resources')
@auth_required('agentadmin')
def get_resources():
    # resources = Resource.get_all()
    agent = Agent.get_by_user_id(g.user.id)
    resources = Resource.get_by_partner_id(agent.partner_id)
    return ResourceSchema(many=True).dump(resources), 200

@bp.post('/resource/<int:id>/train')
@auth_required('agentadmin')
def train_model_with_resource(id):
    resource = Resource.get_by_id(id)
    if resource is None:
        return {'message': 'Resource not found'}, 404
    elif resource.training_status == 'complete':
        return {'message': 'Resource already used for training'}, 404
    elif resource.training_status == 'processing':
        return {'message': 'Resource training in progress'}, 404
    # start resource training here
    start_training.delay(resource.id)
    resource.training_status == 'processing'
    return {'message': 'Resource training initialized successfully'}, 200