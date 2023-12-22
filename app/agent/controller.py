from flask import Blueprint, g, request
from app.route_guard import auth_required

from app.agent.model import *
from app.agent.schema import *
from app.user.model import User

bp = Blueprint('agent', __name__)

@bp.post('/agent')
@auth_required('agentadmin')
def create_agent():
    name = request.json.get('name')
    email = request.json.get('email')
    phone = request.json.get('phone')
    password = request.json.get('password')
    role = request.json.get('role')
    user = User.create(name, phone, email, password, role)

    loggedin_agent = Agent.get_by_user_id(g.user.id)
    agent = Agent.create(name, email, phone, loggedin_agent.partner_id, user.id)
    return AgentSchema().dump(agent), 201

@bp.get('/agent/<int:id>')
@auth_required('agentadmin')
def get_agent(id):
    agent = Agent.get_by_id(id)
    if agent is None:
        return {'message': 'Agent not found'}, 404
    return AgentSchema().dump(agent), 200

@bp.patch('/agent/<int:id>')
@auth_required()
def update_agent(id):
    agent = Agent.get_by_id(id)
    if agent is None:
        return {'message': 'Agent not found'}, 404
    name = request.json.get('name')
    phone = request.json.get('phone')
    role = request.json.get('role')
    user = User.get_by_id(agent.user_id)
    user.role = role or user.role
    agent.update(name, phone)
    return AgentSchema().dump(agent), 200

@bp.delete('/agent/<int:id>')
@auth_required('agentadmin')
def delete_agent(id):
    agent = Agent.get_by_id(id)
    if agent is None:
        return {'message': 'Agent not found'}, 404
    user = User.get_by_id(agent.user_id)
    agent.delete()
    user.delete()
    return {'message': 'Agent deleted successfully'}, 200

@bp.get('/agents')
@auth_required('agentadmin')
def get_agents():
    agent = Agent.get_by_user_id(g.user.id)
    agents = Agent.get_all_by_partner_id(agent.partner_id)
    return AgentSchema(many=True).dump(agents), 200