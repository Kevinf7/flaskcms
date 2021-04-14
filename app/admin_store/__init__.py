from flask import Blueprint

bp = Blueprint('admin_store', __name__)

from app.admin_store import routes
