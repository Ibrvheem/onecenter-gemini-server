from flask import Blueprint, request
from app.route_guard import auth_required

from app.platform.model import *
from app.platform.schema import *

bp = Blueprint('platform', __name__)

@bp.post('/platform')
@auth_required('admin')
def create_platform():
    name = request.json.get('name')
    username = request.json.get('username')
    password = request.json.get('password')
    platform = Platform.create(name, username, password)
    return PlatformSchema().dump(platform), 201

@bp.get('/platform/<int:id>')
@auth_required('admin')
def get_platform(id):
    platform = Platform.get_by_id(id)
    if platform is None:
        return {'message': 'Platform not found'}, 404
    return PlatformSchema().dump(platform), 200

@bp.patch('/platform/<int:id>')
@auth_required('admin')
def update_platform(id):
    platform = Platform.get_by_id(id)
    if platform is None:
        return {'message': 'Platform not found'}, 404
    platform.update()
    return PlatformSchema().dump(platform), 200

@bp.delete('/platform/<int:id>')
@auth_required('admin')
def delete_platform(id):
    platform = Platform.get_by_id(id)
    if platform is None:
        return {'message': 'Platform not found'}, 404
    platform.delete()
    return {'message': 'Platform deleted successfully'}, 200

@bp.get('/platforms')
@auth_required('admin')
def get_platforms():
    platforms = Platform.get_all()
    return PlatformSchema(many=True).dump(platforms), 200