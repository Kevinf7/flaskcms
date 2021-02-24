from flask import render_template, redirect, url_for, flash, request, make_response, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.admin_page import bp
from app.admin_page.models import Page, PageHome, PageHomeCurr, PageContact, PageContactCurr
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



# Handles javascript image uploads from tinyMCE
@bp.route('/imageuploader', methods=['POST'])
@login_required
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
                img_fullpath = os.path.join(current_app.config['UPLOADED_PATH'], filename)
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
                tmb_fullpath = os.path.join(current_app.config['UPLOADED_PATH_THUMB'], thumbnail)
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
                output = make_response(404)
                output.headers['Error'] = 'Cannot create thumbnail for ' + filename
                return output
            return jsonify({'location' : filename})

    # fail, image did not upload
    output = make_response(404)
    output.headers['Error'] = 'Filename needs to be JPG, JPEG, GIF or PNG'
    return output


# Custom page routes

@bp.route('/page/page_home',methods=['GET'])
@login_required
def page_home():
    return redirect(url_for('admin_page.page'))


@bp.route('/page/page_contact', methods=['GET', 'POST'])
@login_required
def page_contact():
    if request.method == 'POST':
        content = request.form.get('content')
        page_contact_id = request.form.get('id')
        pc = PageContact.query.filter_by(id=page_contact_id).first()
        if pc:
            pc.content = content
            pc.update_date = datetime.now()
            pc.update_by = current_user.email
            db.session.add(pc)
            db.session.commit()
            flash('Successfully updated', 'success')
        else:
            flash('id error, not updated', 'danger')
    this_ver = db.session.query(PageContact) \
        .join(PageContactCurr).first()
    all_ver = PageContact.query.order_by(PageContact.update_date.desc()).limit(5).all()
    return render_template('admin_page/page_contact.html', this_ver=this_ver, all_ver=all_ver)


@bp.route('/page/page_contact_curr', methods=['POST'])
@login_required
def page_contact_curr():
    if request.method == 'POST':
        page_contact_id = request.form.get('id')
        pc = PageContact.query.filter_by(id=page_contact_id).first()
        if pc:
            pcc = PageContactCurr.query.first()
            if pcc.page_contact_id == page_contact_id:
                flash('page is already current, not updated', 'danger')
            else:
                pcc.page_contact_id = page_contact_id
                db.session.add(pcc)
                db.session.commit()
                flash('Successfully updated', 'success')
        else:
            flash('id error, not updated', 'danger')

    return redirect(url_for('admin_page.page_contact'))
