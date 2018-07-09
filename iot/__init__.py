'''
All Flask extensions are created here
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from flask_socketio import SocketIO

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()

def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    swaggerui_blueprint = get_swaggerui_blueprint(
        app.config.get('SWAGGER_URL'),
        app.config.get('SWAGGER_API_URL'))
    from iot.api.api import api_bp
    from iot.frontend.controllers import frontend_bp

    app.register_blueprint(frontend_bp, url_prefix='')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(swaggerui_blueprint,
                           url_prefix=app.config.get('SWAGGER_URL'))

    return app
