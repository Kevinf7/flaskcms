from flask import render_template
from app import db
from app.admin_store import bp
from flask_login import login_required
from app.breadcrumb import set_breadcrumb


# ADMIN STORE routes

@bp.route('/store',methods=['GET'])
@login_required
@set_breadcrumb('home store')
def store():
    return render_template('admin_store/store.html')