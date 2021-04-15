from flask import render_template, request, current_app, flash, session
from app import db
from app.admin_store import bp
from flask_login import login_required
from app.breadcrumb import set_breadcrumb
from app.admin_store.models import Category, CategoryGeneral, Size, Color
from sqlalchemy import asc


# ADMIN STORE routes

@bp.route('/store',methods=['GET','POST'])
@login_required
@set_breadcrumb('home store')
def store():
    if 'store_show_type' in session:
        show_type = session['store_show_type']
    else:
        show_type = 'all'
    if request.method == 'POST':
        s = request.form.get('show_type')
        if s=='all':
            show_type='all'
        else:
            if s:
                cat = Category.query.filter_by(id=int(s)).first()
                if not cat:
                    flash('Show type error', 'danger')
                else:
                    show_type = s
    page = request.args.get('page',1,type=int)
    category = Category.query.order_by(asc(Category.display)).all()
    if show_type == 'all':
        session['store_show_type']='all'
        catgen = CategoryGeneral.query.order_by(asc(CategoryGeneral.title)) \
            .paginate(page,current_app.config['STORE_PER_PAGE'],False)
    else:
        session['store_show_type'] = show_type
        catgen = CategoryGeneral.query.join(Category) \
            .filter(Category.id==int(show_type)) \
            .order_by(asc(CategoryGeneral.title)) \
            .paginate(page,current_app.config['STORE_PER_PAGE'],False)
    return render_template('admin_store/store.html',catgen=catgen
        ,category=category,show_type=show_type)


@bp.route('/product',methods=['GET','POST'])
@login_required
@set_breadcrumb('home store product')
def product():
    if request.method == 'POST':
        category = request.form.get('category')
        title = request.form.get('title')
        description = request.form.get('description')
        size = request.form.get('size')
        color = request.form.get('color')
        quantity = request.form.get('quantity')
    category = Category.query.order_by(asc(Category.display)).all()
    size = Size.query.order_by(asc(Size.name)).all()
    color = Color.query.order_by(asc(Color.name)).all()
    return render_template('admin_store/product.html',category=category
        ,size=size,color=color)