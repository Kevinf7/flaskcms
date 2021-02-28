from flask import render_template, redirect, url_for, flash, request, make_response, jsonify, current_app
from flask_login import login_required, current_user
from app import db, csrf
from app.admin_page import bp
from app.admin_page.models import Page, PageHome, PageContact, PageStatus
from app.admin_media.models import Images
import os
from PIL import Image
from datetime import datetime


# ADMIN PAGE routes 

@bp.route('/page',methods=['GET'])
@login_required
def page():
    page = request.args.get('page',1,type=int)
    pages = Page.query.order_by(Page.name.asc()) \
    .paginate(page,current_app.config['PAGES_PER_PAGE'],False)

    return render_template('admin_page/page.html',pages=pages)


# imageuploader for tinyMCE
@bp.route('/page/imageuploader', methods=['POST'])
@login_required
@csrf.exempt
def imageuploader():
    file = request.files.get('file')
    if file:
        filename = file.filename.lower()
        fn, ext = filename.split('.')
        # truncate filename (excluding extension) to 30 characters
        fn = fn[:30]
        filename = fn + '.' + ext
        if ext in ['jpg', 'gif', 'png', 'jpeg']:
            try:
                # everything looks good, save file
                img_fullpath = os.path.join(current_app.config['UPLOAD_PATH_PAGE'], filename)
                file.save(img_fullpath)
                # get the file size to save to db
                file_size = os.stat(img_fullpath).st_size
                size = 160, 160
                # read image into pillow
                im = Image.open(img_fullpath)
                # get image dimension to save to db
                file_width, file_height = im.size
                # convert to thumbnail
                im.thumbnail(size)
                thumbnail = fn + '-thumb.jpg'
                tmb_fullpath = os.path.join(current_app.config['UPLOAD_PATH_THUMB_PAGE'], thumbnail)
                # PNG is index while JPG needs RGB
                if not im.mode == 'RGB':
                    im = im.convert('RGB')
                # save thumbnail
                im.save(tmb_fullpath, "JPEG")

                # save to db
                img = Images(filename=filename, thumbnail=thumbnail, file_size=file_size, \
                            file_width=file_width, file_height=file_height)
                db.session.add(img)
                db.session.commit()
            except IOError:
                return make_response('Cannot create thumbnail for ' + filename, 500)

            return jsonify({'location' : filename})

    # fail, image did not upload
    return make_response('Filename needs to be JPG, JPEG, GIF or PNG', 400)


# Custom page routes

@bp.route('/page/page_home',methods=['GET'])
@login_required
def page_home():
    return redirect(url_for('admin_page.page'))


@bp.route('/page/page_contact', methods=['GET', 'POST'])
@login_required
def page_contact():
    edit_ver = None
    if request.method == 'POST':
        btn = request.form.get('submit_btn')
        page_id = request.form.get('id')
        page = PageContact.query.filter_by(id=int(page_id)).first()
        if page:
            if btn == 'Save':
                content = request.form.get('content')
                if page.page_status.name == 'draft':
                    page.content = content
                    page.update_by = current_user.email
                    page.update_date = datetime.utcnow()
                    page.create_date = datetime.utcnow()
                    db.session.add(page)
                    db.session.commit()
                    flash('Successfully updated draft', 'success')
                else:
                    flash('This page is not a draft, not saved', 'danger')
            elif btn == 'Save as draft':
                draft = PageContact.query.filter_by(page_status=PageStatus.getStatus('draft')).first()
                if not draft:
                    content = request.form.get('content')
                    new_draft = PageContact(content=content, page_id=Page.getPage('contact').id, \
                        page_status=PageStatus.getStatus('draft'), update_by=current_user.email, \
                        update_date=datetime.utcnow(), create_date = datetime.utcnow())
                    db.session.add(new_draft)
                    db.session.commit()
                    flash('Successfully saved new draft', 'success')
                else:
                    content = request.form.get('content')
                    draft.content = content
                    draft.update_by = current_user.email
                    draft.update_date = datetime.utcnow()
                    draft.create_date = datetime.utcnow()
                    db.session.add(draft)
                    db.session.commit()
                    flash('Successfully saved as draft', 'success')
            elif btn == 'Publish':
                if page.page_status == PageStatus.getStatus('published'):
                    flash('Page is already published', 'danger')
                elif page.page_status == PageStatus.getStatus('draft'):
                    # there should only be 1 published.. this is just to make 100% sure
                    page_pub = PageContact.query.filter_by(page_status=PageStatus.getStatus('published')).all()
                    for p in page_pub:
                        p.page_status = PageStatus.getStatus('archived')
                        db.session.add(p)
                    content = request.form.get('content')
                    page.content = content
                    page.page_status = PageStatus.getStatus('published')
                    page.update_by = current_user.email
                    page.update_date = datetime.utcnow()
                    page.page.last_publish_by = current_user.email
                    page.page.last_publish_date = datetime.utcnow()
                    db.session.add(page)
                    db.session.commit()
                    flash('Successfully published', 'success')
                else:
                    flash('Status error, not published', 'danger')
            elif btn == 'Edit this version':
                edit_ver = PageContact.query.filter_by(id=page_id).first()
            else:
                flash('Submit button error, not published', 'danger')
        else:
            flash('id error', 'danger')

    if not edit_ver:
        page_draft = PageContact.query.filter_by(page_status=PageStatus.getStatus('draft')).first()
        if page_draft:
            edit_ver = page_draft
        else:
            edit_ver = PageContact.query.filter_by(page_status=PageStatus.getStatus('published')).first()

    all_ver = PageContact.query.order_by(PageContact.update_date.desc()).limit(20).all()
    return render_template('admin_page/page_contact.html', all_ver=all_ver, edit_ver=edit_ver)
