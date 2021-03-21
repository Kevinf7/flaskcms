from flask import render_template
from app.main import bp
from app.admin_page.models import PageHomeMain, PageStatus


@bp.route('/')
@bp.route('/index')
def index():
    main = PageHomeMain.query.filter_by(page_status=PageStatus.getStatus('published')).first()
    return render_template('main/index.html', main=main)


@bp.route('/blog')
def blog():
    return render_template('main/blog.html')


@bp.route('/contact')
def contact():
    return render_template('main/contact.html')