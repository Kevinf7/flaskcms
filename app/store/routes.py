from flask import render_template
from app import db
from app.store import bp


# STORE routes

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('store/index.html')