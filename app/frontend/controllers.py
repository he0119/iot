import os

from flask import (Blueprint, make_response, render_template,
                   send_from_directory, jsonify)
from flask_restful import Api

from app.api.resources.device import Status
from app.api.resources.token import Token

frontend_bp = Blueprint('frontend_bp', __name__)

@frontend_bp.route('/')
@frontend_bp.route('/index')
def index():
    return render_template("index.html")

@frontend_bp.route('/history')
def history():
    return render_template("history.html")
