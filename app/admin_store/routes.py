from flask import render_template, request, current_app
from app import db
from app.admin_store import bp
from flask_login import login_required
from app.breadcrumb import set_breadcrumb
from app.admin_store.models import Category, CategoryGeneral
from sqlalchemy import asc


# ADMIN STORE routes

@bp.route('/store',methods=['GET','POST'])
@login_required
@set_breadcrumb('home store')
def store():
    page = request.args.get('page',1,type=int)
    category = Category.query.order_by(asc(Category.display)).all()
    catgen = CategoryGeneral.query.order_by(asc(CategoryGeneral.title)) \
        .paginate(page,current_app.config['STORE_PER_PAGE'],False)
    return render_template('admin_store/store.html',catgen=catgen,category=category)


@bp.route('/product',methods=['GET','POST'])
@login_required
@set_breadcrumb('home store product')
def product():
    return render_template('admin_store/product.html')