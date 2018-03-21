'''main entry for flask app'''
from app import app
from app.api.api import api_bp
from app.frontend.controllers import frontend_bp

app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(frontend_bp, url_prefix='')
