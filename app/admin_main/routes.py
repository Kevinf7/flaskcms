from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_user, logout_user, login_required
from app import db, login_manager
from app.admin_main import bp


# ADMIN MAIN routes

@bp.route('/about', methods=['GET'])
@login_required
def about():
    return render_template('admin_main/about.html')