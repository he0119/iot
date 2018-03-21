'''main entry for flask app'''
import os

from flask import jsonify, make_response, send_from_directory

from app import app
from app.api.api import api_bp
from app.frontend.controllers import frontend_bp

app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(frontend_bp, url_prefix='')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'message': 'Not found'}), 404)

@app.route('/favicon.ico')
def favicon():
    print(frontend_bp.root_path)
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
