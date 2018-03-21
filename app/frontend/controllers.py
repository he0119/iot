from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend_bp', __name__)

@frontend_bp.route('/')
@frontend_bp.route('/index')
def index():
    return render_template("index.html")

@frontend_bp.route('/history')
def history():
    return render_template("history.html")
