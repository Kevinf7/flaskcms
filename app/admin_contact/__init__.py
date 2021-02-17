from flask import Blueprint

bp = Blueprint('admin_contact', __name__)

from app.admin_contact import routes
