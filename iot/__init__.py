'''Flask creat_app()'''
from flask import Flask
from flask_mqtt import Mqtt

from iot.common.db import db, migrate

mqtt = Mqtt()

def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    mqtt.init_app(app)

    from iot.api.api import api_bp
    from iot.frontend.controllers import frontend_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(frontend_bp, url_prefix='')

    import iot.common.mqtt

    return app
