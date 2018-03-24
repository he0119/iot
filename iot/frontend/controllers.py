import os

from flask import (Blueprint, render_template, jsonify,
                   make_response, send_from_directory, current_app)

frontend_bp = Blueprint('frontend_bp', __name__)

@frontend_bp.route('/')
@frontend_bp.route('/index')
def index():
    '''index.html'''
    return render_template('index.html')

@frontend_bp.route('/history')
def history():
    '''history.html'''
    return render_template('history.html')

@frontend_bp.app_errorhandler(404)
def not_found(error):
    '''handle 404 error'''
    return make_response(jsonify({'message': 'Not found'}), 404)

@frontend_bp.route('/favicon.ico')
def favicon():
    '''route for favicon.ico'''
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')
