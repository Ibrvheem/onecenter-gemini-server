from flask import Blueprint, request
from app.agent.model import Agent
from app.route_guard import auth_required

from app.partner.model import *
from app.partner.schema import *
from app.user.model import User

bp = Blueprint('partner', __name__)

@bp.post('/partner')
# @auth_required()
def create_partner():
    name = request.json.get('name')
    category = request.json.get('category')
    description = request.json.get('description')
    email = request.json.get('email')
    phone = request.json.get('phone')
    address = request.json.get('address')
    logo = request.json.get('logo')
    website = request.json.get('website')
    agent = request.json.get('agent')
    if not agent.get('email') or not agent.get('password'):
        return {'message': 'Account needs email and password'}, 400
    partner = Partner.create(name, category, description, email, phone, address, logo, website)
    if not partner:
        return {'message': 'Partner already exists or you have invalid parameters'}, 400
    user = User.create(agent.get('name'), agent.get('phone'), agent.get('email'), agent.get('password', 'password'), 'agentadmin')
    Agent.create(agent.get('name'), agent.get('email'), agent.get('phone'), partner.id, user.id)
    return PartnerSchema().dump(partner), 201

@bp.get('/partner/<int:id>')
@auth_required()
def get_partner(id):
    partner = Partner.get_by_id(id)
    if partner is None:
        return {'message': 'Partner not found'}, 404
    return PartnerSchema().dump(partner), 200

@bp.patch('/partner/<int:id>')
@auth_required()
def update_partner(id):
    partner = Partner.get_by_id(id)
    if partner is None:
        return {'message': 'Partner not found'}, 404
    name = request.json.get('name')
    category = request.json.get('category')
    description = request.json.get('description')
    email = request.json.get('email')
    phone = request.json.get('phone')
    address = request.json.get('address')
    logo = request.json.get('logo')
    website = request.json.get('website')
    partner.update(name, category, description, email, phone, address, logo, website)
    return PartnerSchema().dump(partner), 200

@bp.delete('/partner/<int:id>')
@auth_required()
def delete_partner(id):
    partner = Partner.get_by_id(id)
    if partner is None:
        return {'message': 'Partner not found'}, 404
    partner.delete()
    return {'message': 'Partner deleted successfully'}, 200

@bp.get('/partners')
# @auth_required()
def get_partners():
    partners = Partner.get_all()
    return PartnerSchema(many=True).dump(partners), 200