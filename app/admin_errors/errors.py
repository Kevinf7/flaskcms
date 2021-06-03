from flask import render_template
from . import bp
from flask_wtf.csrf import CSRFError


@bp.app_errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('admin_errors/csrf_error.html', reason=e.description), 400

@bp.app_errorhandler(400)
def bad_request(e):
    return render_template('admin_errors/400.html'), 400

@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('admin_errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('admin_errors/500.html'), 500
