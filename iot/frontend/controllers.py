'''
Frontend
'''
import os
import re

from flask import (Blueprint, current_app, jsonify, make_response,
                   render_template, send_from_directory)

frontend_bp = Blueprint('frontend_bp', __name__)

@frontend_bp.route('/', defaults={'path': ''})
@frontend_bp.route('/<path:path>')
def catch_all(path):
    if not path:
        return angular_page()
    is_angular_page = re.match(r'^((?!api\/)\w\/?)+$', path)
    if is_angular_page:
        return angular_page()
    is_angular_src = re.match(r'.*\.(js|css|json|html)', path)
    if is_angular_src:
        return angular_src(is_angular_src[0])
    return make_response(jsonify({'message': 'Not found'}), 404)

def angular_page():
    '''index.html'''
    return send_from_directory('angular/dist', 'index.html')

def angular_src(path):
    '''angular static files'''
    print(path)
    if path.split('.')[-1] == 'js':
        return send_from_directory('angular/dist', path, mimetype='text/javascript')
    return send_from_directory('angular/dist', path)

@frontend_bp.route('/favicon.ico')
def favicon():
    '''route for favicon.ico'''
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
