from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db, csrf
from app.admin_page import bp
from app.admin_page.models import Page, PageHomeMain, PageContact, PageStatus
from app.admin_media.models import ImageType, Images
from app.admin_media.routes import process_image
from datetime import datetime
from app.breadcrumb import set_breadcrumb


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
    edit_ver = None
    if request.method == 'POST':
        page_id = request.form.get('id')
        page = PageHomeMain.query.filter_by(id=int(page_id)).first()
        if page:
            action = request.form.get('action')
            heading = request.form.get('heading')
            important = request.form.get('important')
            text = request.form.get('text')
            image_id = request.form.get('image_id')
            
            if action == 'Delete':
                if page.page_status.name == 'draft':
                    db.session.delete(page)
                    db.session.commit()
                    flash('Draft deleted', 'success')
                else:
                    flash('This page is not a draft', 'danger')
            elif action == 'Save':
                if page.page_status.name == 'draft':
                    new_image = request.files['new_image']
                    resp = {'status':'ok'}
                    if new_image:
                        upload_path = current_app.config['UPLOAD_PATH_PAGE']
                        upload_path_thumb = current_app.config['UPLOAD_PATH_THUMB_PAGE']
                        img_type_obj = ImageType.query.filter_by(name='page').first()
                        resp = process_image(new_image,upload_path,upload_path_thumb,img_type_obj)
                    if resp['status'] == 'error':
                        flash(resp['msg'])
                    else:
                        page.heading = heading
                        page.important = important
                        page.text = text
                        if new_image:
                            img = Images.query.filter_by(filename=resp['msg']).first()
                            page.image = img 
                        page.author = current_user
                        page.update_date = datetime.utcnow()
                        page.create_date = datetime.utcnow()
                        db.session.add(page)
                        db.session.commit()
                        flash('Draft saved', 'success')
                else:
                    flash('This page is not a draft', 'danger')
            elif action == 'Save as draft':
                draft = PageHomeMain.query.filter_by(page_status=PageStatus.getStatus('draft')).first()
                if not draft:
                    new_draft = PageHomeMain(heading=heading, important=important, text=text,\
                        image_id=image_id, page_id=Page.getPage('home_main').id, \
                        page_status=PageStatus.getStatus('draft'), author=current_user, \
                        update_date=datetime.utcnow(), create_date = datetime.utcnow())
                    db.session.add(new_draft)
                    db.session.commit()
                    flash('Saved as draft', 'success')
                else:
                    draft.heading = heading
                    draft.important = important
                    draft.text = text
                    draft.image_id = image_id
                    draft.author = current_user
                    draft.update_date = datetime.utcnow()
                    draft.create_date = datetime.utcnow()
                    db.session.add(draft)
                    db.session.commit()
                    flash('Saved as draft', 'success')
            elif action == 'Publish':
                if page.page_status == PageStatus.getStatus('published'):
                    flash('Page already published', 'danger')
                elif page.page_status == PageStatus.getStatus('draft'):
                    new_image = request.files['new_image']
                    resp = {'status':'ok'}
                    if new_image:
                        upload_path = current_app.config['UPLOAD_PATH_PAGE']
                        upload_path_thumb = current_app.config['UPLOAD_PATH_THUMB_PAGE']
                        img_type_obj = ImageType.query.filter_by(name='page').first()
                        resp = process_image(new_image,upload_path,upload_path_thumb,img_type_obj)
                    if resp['status'] == 'error':
                        flash(resp['msg'])
                    else:
                        # there should only be 1 published.. this is just to make 100% sure
                        page_pub = PageHomeMain.query.filter_by(page_status=PageStatus.getStatus('published')).all()
                        for p in page_pub:
                            db.session.delete(p)
                        page.heading = heading
                        page.important = important
                        page.text = text
                        if new_image:
                            img = Images.query.filter_by(filename=resp['msg']).first()
                            page.image = img 
                        page.page_status = PageStatus.getStatus('published')
                        page.author = current_user
                        page.update_date = datetime.utcnow()
                        page.page.last_publish_by = current_user
                        page.page.last_publish_date = datetime.utcnow()
                        db.session.add(page)
                        db.session.commit()
                        flash('Page published', 'success')
                else:
                    flash('Status error', 'danger')
            elif action == 'Edit this version':
                edit_ver = PageHomeMain.query.filter_by(id=page_id).first()
            else:
                flash('Submit button error', 'danger')
        else:
            flash('id error', 'danger')

    if not edit_ver:
        page_draft = PageHomeMain.query.filter_by(page_status=PageStatus.getStatus('draft')).first()
        if page_draft:
            edit_ver = page_draft
        else:
            edit_ver = PageHomeMain.query.filter_by(page_status=PageStatus.getStatus('published')).first()
    
    all_ver = PageHomeMain.query.order_by(PageHomeMain.update_date.desc()).all()
    return render_template('admin_page/page_home_main.html', all_ver=all_ver, edit_ver=edit_ver)


@bp.route('/page/page_contact', methods=['GET', 'POST'])
@login_required
@set_breadcrumb('home page page-contact')
def page_contact():
    edit_ver = None
    if request.method == 'POST':
        action = request.form.get('action')
        page_id = request.form.get('id')
        page = PageContact.query.filter_by(id=int(page_id)).first()
        if page:
            if action == 'Delete':
                if page.page_status.name == 'draft':
                    db.session.delete(page)
                    db.session.commit()
                    flash('Draft deleted', 'success')
                else:
                    flash('This page is not a draft', 'danger')
            elif action == 'Save':
                content = request.form.get('content')
                if page.page_status.name == 'draft':
                    page.content = content
                    page.author = current_user
                    page.update_date = datetime.utcnow()
                    page.create_date = datetime.utcnow()
                    db.session.add(page)
                    db.session.commit()
                    flash('Draft saved', 'success')
                else:
                    flash('This page is not a draft', 'danger')
            elif action == 'Save as draft':
                draft = PageContact.query.filter_by(page_status=PageStatus.getStatus('draft')).first()
                if not draft:
                    content = request.form.get('content')
                    new_draft = PageContact(content=content, page_id=Page.getPage('contact').id, \
                        page_status=PageStatus.getStatus('draft'), author=current_user, \
                        update_date=datetime.utcnow(), create_date = datetime.utcnow())
                    db.session.add(new_draft)
                    db.session.commit()
                    flash('Saved as draft', 'success')
                else:
                    content = request.form.get('content')
                    draft.content = content
                    draft.author = current_user
                    draft.update_date = datetime.utcnow()
                    draft.create_date = datetime.utcnow()
                    db.session.add(draft)
                    db.session.commit()
                    flash('Saved as draft', 'success')
            elif action == 'Publish':
                if page.page_status == PageStatus.getStatus('published'):
                    flash('Page already published', 'danger')
                elif page.page_status == PageStatus.getStatus('draft'):
                    # there should only be 1 published.. this is just to make 100% sure
                    page_pub = PageContact.query.filter_by(page_status=PageStatus.getStatus('published')).all()
                    for p in page_pub:
                        db.session.delete(p)
                    content = request.form.get('content')
                    page.content = content
                    page.page_status = PageStatus.getStatus('published')
                    page.author = current_user
                    page.update_date = datetime.utcnow()
                    page.page.last_publish_by = current_user
                    page.page.last_publish_date = datetime.utcnow()
                    db.session.add(page)
                    db.session.commit()
                    flash('Page published', 'success')
                else:
                    flash('Status error', 'danger')
            elif action == 'Edit this version':
                edit_ver = PageContact.query.filter_by(id=page_id).first()
            else:
                flash('Submit button error', 'danger')
        else:
            flash('id error', 'danger')

    if not edit_ver:
        page_draft = PageContact.query.filter_by(page_status=PageStatus.getStatus('draft')).first()
        if page_draft:
            edit_ver = page_draft
        else:
            edit_ver = PageContact.query.filter_by(page_status=PageStatus.getStatus('published')).first()


    all_ver = PageContact.query.order_by(PageContact.update_date.desc()).all()
    return render_template('admin_page/page_contact.html', all_ver=all_ver, edit_ver=edit_ver)
