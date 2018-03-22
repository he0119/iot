'''main entry for flask app'''
import os

from flask import jsonify, make_response, send_from_directory

from iot import app
from iot.api.api import api_bp
from iot.frontend.controllers import frontend_bp

app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(frontend_bp, url_prefix='')

@app.errorhandler(404)
def not_found(error):
    '''handle 404 error'''
    return make_response(jsonify({'message': 'Not found'}), 404)

@app.route('/favicon.ico')
def favicon():
    '''route for favicon.ico'''
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
