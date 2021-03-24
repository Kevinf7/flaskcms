from flask import flash, request, current_app
from flask_login import current_user
from app.admin_page.models import Page, PageStatus
from app.admin_media.models import ImageType, Images
from app.admin_media.routes import process_image
from app import db
from datetime import datetime


def getUploadedImage(img_num):
    r = request.files
    img_key = 'new_image'+str(img_num)
    if img_key in r:
        new_image = request.files[img_key]
        if new_image:
            upload_path = current_app.config['UPLOAD_PATH_PAGE']
            upload_path_thumb = current_app.config['UPLOAD_PATH_THUMB_PAGE']
            img_type_obj = ImageType.query.filter_by(name='page').first()
            resp = process_image(new_image,upload_path,upload_path_thumb,img_type_obj)
            if resp['status'] == 'error':
                flash(resp['msg'])
                return False
            else:
                return Images.query.filter_by(filename=resp['msg']).first()
    return False


def page_post(page_model, page_name, fields, num_images):
    edit_ver = None
    if request.method == 'POST':
        page_id = request.form.get('id')
        page = page_model.query.filter_by(id=int(page_id)).first()
        if page:
            data = {}
            for f in fields:
                if f['type'] == 'int':
                    data[f['name']] = request.form.get(f['name'], type=int)
                else:
                    data[f['name']] = request.form.get(f['name'])
            image_id = []
            for r in range(1,num_images+1):
                image_id.append(request.form.get('image_id'+str(r), type=int))       
            action = request.form.get('action')
            if action == 'Delete':
                if page.page_status.name == 'draft':
                    db.session.delete(page)
                    db.session.commit()
                    flash('Draft deleted', 'success')
                else:
                    flash('This page is not a draft', 'danger')
            elif action == 'Save':
                if page.page_status.name == 'draft':
                    for r in range(1,num_images+1):
                        excludeimg = request.form.get('excludeimg'+str(r))
                        if excludeimg=='true':
                            setattr(page,'image'+str(r),None)
                        else:
                            new_path = request.form.get('new_path'+str(r))
                            if new_path:
                                i = new_path.rsplit('/',1)
                                img = Images.query.filter_by(filename=i[1]).first()
                                setattr(page,'image'+str(r),img)
                            else:
                                img = getUploadedImage(r)
                                if img:
                                    setattr(page,'image'+str(r),img)
                    for f in fields:
                        setattr(page,f['name'],data[f['name']])
                    page.author = current_user
                    page.update_date = datetime.utcnow()
                    page.create_date = datetime.utcnow()
                    db.session.add(page)
                    db.session.commit()
                    flash('Draft saved', 'success')
                else:
                    flash('This page is not a draft', 'danger')
            elif action == 'Save as draft':
                draft = page_model.query.filter_by(page_status=PageStatus.getStatus('draft')).first()
                if not draft:
                    new_draft = page_model(page_id=Page.getPage(page_name).id, \
                        page_status=PageStatus.getStatus('draft'), author=current_user, \
                        update_date=datetime.utcnow(), create_date = datetime.utcnow())
                    for r in range(1,num_images+1):
                        setattr(new_draft,'image_id'+str(r),image_id[r-1])
                    for f in fields:
                        setattr(new_draft,f['name'],data[f['name']])
                    db.session.add(new_draft)
                    db.session.commit()
                    flash('Saved as draft', 'success')
                else:
                    for r in range(1,num_images+1):
                        setattr(draft,'image_id'+str(r),image_id[r-1])
                    for f in fields:
                        setattr(draft,f['name'],data[f['name']])
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
                    page_pub = page_model.query.filter_by(page_status=PageStatus.getStatus('published')).all()
                    for p in page_pub:
                        db.session.delete(p)

                    for r in range(1,num_images+1):
                        excludeimg = request.form.get('excludeimg'+str(r))
                        if excludeimg=='true':
                            setattr(page,'image'+str(r),None)
                        else:
                            new_path = request.form.get('new_path'+str(r))
                            if new_path:
                                i = new_path.rsplit('/',1)
                                img = Images.query.filter_by(filename=i[1]).first()
                                setattr(page,'image'+str(r),img)
                            else:
                                img = getUploadedImage(r)
                                if img:
                                    setattr(page,'image'+str(r),img)
                    for f in fields:
                        setattr(page,f['name'],data[f['name']])
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
                edit_ver = page_model.query.filter_by(id=page_id).first()
            else:
                flash('Submit button error', 'danger')
        else:
            flash('id error', 'danger')

    if not edit_ver:
        page_draft = page_model.query.filter_by(page_status=PageStatus.getStatus('draft')).first()
        if page_draft:
            edit_ver = page_draft
        else:
            edit_ver = page_model.query.filter_by(page_status=PageStatus.getStatus('published')).first()
    
    all_ver = page_model.query.order_by(page_model.update_date.desc()).all()
    return([edit_ver, all_ver])