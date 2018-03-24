'''
All Flask extensions are created here
'''
from flask import Flask
from flask_mqtt import Mqtt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
mqtt = Mqtt()

def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    mqtt.init_app(app)

    import iot.common.mqtt

    from iot.api.api import api_bp
    from iot.frontend.controllers import frontend_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(frontend_bp, url_prefix='')

    return app
