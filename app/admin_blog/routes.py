from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required
from app import db
from app.admin_blog import bp
from app.admin_blog.models import Post 


# ADMIN BLOG routes

@bp.route('/post')
def index():
    return render_template('admin_blog/index.html')
