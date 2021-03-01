import os
from flask import current_app, flash, redirect, render_template, request, url_for, jsonify
from flask_login import login_required
from app import db, csrf
from app.admin_media import bp
from app.admin_media.models import Images


# ADMIN_MEDIA routes

@bp.route('/media',methods=['GET'])
@login_required
def media():
    # get page number from url. If no page number use page 1
    page = request.args.get('page',1,type=int)
    # True means 404 error is returned if page is out of range. False means an empty list is returned
    images = Images.query.order_by(Images.create_date.desc()) \
                        .paginate(page,current_app.config['IMAGES_PER_PAGE'],False)
    return render_template('admin_media/media.html',images=images)


@bp.route('/media/del_image',methods=['POST'])
@login_required
def del_image():
    id = request.form.get('id')
    image = Images.getImage(id)

    if image is None:
        flash('No such image.','danger')
    else:
        img_fullpath = os.path.join(current_app.config['UPLOAD_PATH_PAGE'], image.filename)
        tmb_fullpath = os.path.join(current_app.config['UPLOAD_PATH_THUMB_PAGE'], image.thumbnail)
        try:
            os.remove(img_fullpath)
            os.remove(tmb_fullpath)
            db.session.delete(image)
            db.session.commit()
            flash('The image has been successfully deleted','success')
        except OSError:
            flash('System error, image not deleted','danger')
    
    return redirect(url_for('admin_media.media'))

