'''
Frontend
'''
import re

from flask import Blueprint, jsonify, make_response, send_from_directory

frontend_bp = Blueprint('frontend_bp', __name__)
angular_dir = 'angular'


@frontend_bp.route('/', defaults={'path': ''})
@frontend_bp.route('/<path:path>')
def catch_all(path):
    '''catch all path'''
    # except api/*
    is_angular_page = re.match(r'^((?!api\/)\w\/?)+$', path)
    if is_angular_page or not path:
        return angular_page()

    # files with certain suffix
    is_angular_src = re.match(
        r'^.*\.(html|ico|js|css|json|woff|woff2|ttf|eot|svg|txt)$', path)
    if is_angular_src:
        return angular_src(is_angular_src[0])

    return make_response(jsonify({'message': 'Not found'}), 404)


def angular_page():
    '''index.html'''
    return send_from_directory(angular_dir, 'index.html')


def angular_src(path):
    '''angular static files'''
    if path.split('.')[-1] == 'js':
        return send_from_directory(angular_dir, path, mimetype='text/javascript')
    return send_from_directory(angular_dir, path)
