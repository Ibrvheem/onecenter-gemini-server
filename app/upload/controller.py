from flask import Blueprint, request

from app.route_guard import auth_required

from app.upload.model import *
from app.upload.schema import *
from helpers.upload import do_upload, remove_upload
bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.post('/add')
@auth_required()
def add():
    file = request.files.get('file')
    if file:
        url = do_upload(file)
        if url:
            return {'url': url, 'message': 'File uploaded successfully'}
        return {'error': 'Error uploading file'}
    return {'error': 'No file to upload'}

@bp.delete('/remove/<file_to_remove>')
@auth_required()
def remove(file_to_remove):
    if remove_upload(file_to_remove):
        return {'success': 'File removed'}
    return {'error': 'Error removing file'}

@bp.put('/update/<file_to_update>')
@auth_required()
def update(file_to_update):
    file = request.files.get('file')
    if file:
        url = do_upload(file, file_to_update)
        if url:
            return {'url': url, 'message': 'File updated successfully'}
        return {'error': 'Error uploading file'}
    return {'error': 'No file to update'}

@bp.patch('/update/<file_to_update>')
@auth_required()
def update_file_content(file_to_update):
    content = request.form.get('content')
    if content:
        url = do_upload(content, file_to_update)
        if url:
            return {'url': url, 'message': 'File content updated successfully'}
        return {'error': 'Error updating file content'}
    return {'error': 'No file content to update'}
