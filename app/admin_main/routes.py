from flask import render_template, redirect, url_for, flash, g
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.admin_main import bp
from app.breadcrumb import set_breadcrumb


# ADMIN MAIN routes

@bp.route('/')
@bp.route('/index')
@login_required
@set_breadcrumb('home')
def index():
    return render_template('admin_main/index.html')
    

@bp.route('/about', methods=['GET'])
@login_required
def about():
    return render_template('admin_main/about.html')


# Used by breadcrumbs
@bp.app_context_processor 
def inject_breadcrumb():
    breadcrumb = getattr(g, 'breadcrumb', '')
    return dict(breadcrumb=breadcrumb)


