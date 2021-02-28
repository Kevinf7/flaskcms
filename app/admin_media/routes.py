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
    msg = request.args.get('msg')
    style = request.args.get('style')
    if msg != '' and style != '':
        if style == 's' or style == 'd':
            if style == 's':
                s = 'success'
            else:
                s = 'danger'
            flash(msg, s)

    # get page number from url. If no page number use page 1
    page = request.args.get('page',1,type=int)
    # True means 404 error is returned if page is out of range. False means an empty list is returned
    images = Images.query.order_by(Images.create_date.desc()) \
                        .paginate(page,current_app.config['IMAGES_PER_PAGE'],False)
    return render_template('admin_media/media.html',images=images)


@bp.route('/media/del_image',methods=['POST'])
@login_required
def del_image():
    id = request.get_json()['id']
    image = Images.getImage(id)

    if image is None:
        response = jsonify({'code': 500, 'msg': 'internal server error'})
        response.status_code = 500
        return response

    img_fullpath = os.path.join(current_app.config['UPLOAD_PATH_PAGE'], image.filename)
    tmb_fullpath = os.path.join(current_app.config['UPLOAD_PATH_THUMB_PAGE'], image.thumbnail)
    try:
        # delete image and thumbnail from file system
        os.remove(img_fullpath)
        os.remove(tmb_fullpath)
        # delete from db
        db.session.delete(image)
        db.session.commit()
        response = jsonify({'code': 200, 'msg': 'The image has been successfully deleted'})
        response.status_code = 200
        return response
    except OSError:
        response = jsonify({'code': 400, 'msg': 'error deleting image'})
        response.status_code = 400
        return response

