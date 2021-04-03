from flask import render_template, request, current_app
from flask_login import login_required
from app.admin_page import bp
from app.admin_page.models import Page, PageHomeMain, PageHomeHero, PageContact
from app.breadcrumb import set_breadcrumb
from .common import page_post


# ADMIN PAGE routes 

@bp.route('/page',methods=['GET'])
@login_required
@set_breadcrumb('home page')
def page():
    page = request.args.get('page',1,type=int)
    pages = Page.query.order_by(Page.name.asc()) \
    .paginate(page,current_app.config['PAGES_PER_PAGE'],False)

    return render_template('admin_page/page.html',pages=pages)


@bp.route('/page/page_home_main',methods=['GET', 'POST'])
@login_required
@set_breadcrumb('home page page-home-main')
def page_home_main():
    fields = [
        {'name': 'heading', 'type': 'str'},
        {'name': 'important', 'type': 'str'},
        {'name': 'text', 'type': 'str'},
    ]
    edit_ver, all_ver = page_post(PageHomeMain,'home_main',fields,1)
    return render_template('admin_page/page_home_main.html', edit_ver=edit_ver, all_ver=all_ver, num_images=1)


@bp.route('/page/page_home_hero',methods=['GET', 'POST'])
@login_required
@set_breadcrumb('home page page-home-hero')
def page_home_hero():
    fields = [
        {'name': 'heading', 'type': 'str'},
        {'name': 'text', 'type': 'str'},
        {'name': 'heading2', 'type': 'str'},
        {'name': 'text2', 'type': 'str'}
    ]
    edit_ver, all_ver = page_post(PageHomeHero,'home_hero',fields,2)
    return render_template('admin_page/page_home_hero.html', edit_ver=edit_ver, all_ver=all_ver, num_images=2)


@bp.route('/page/page_contact', methods=['GET', 'POST'])
@login_required
@set_breadcrumb('home page page-contact')
def page_contact():
    fields = [
        {'name': 'title', 'type': 'str'},
        {'name': 'main_content', 'type': 'str'},
        {'name': 'contact_content', 'type': 'str'},
        {'name': 'phone', 'type': 'str'},
        {'name': 'email', 'type': 'str'},
        {'name': 'address', 'type': 'str'}
    ]
    edit_ver, all_ver = page_post(PageContact,'contact',fields,1)
    return render_template('admin_page/page_contact.html', edit_ver=edit_ver, all_ver=all_ver, num_images=1)
