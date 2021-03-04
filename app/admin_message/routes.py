from flask import render_template, redirect, request, current_app, url_for, flash
from flask_login import login_required
from app import db
from app.admin_message import bp
from app.admin_message.models import Message


# ADMIN MESSAGE routes 

@bp.route('/message',methods=['GET'])
@login_required
def message():
    page = request.args.get('page',1,type=int)
    messages = Message.query.order_by(Message.user_read.asc(), Message.create_date.desc()) \
    .paginate(page,current_app.config['MESSAGES_PER_PAGE'],False)

    return render_template('admin_message/message.html',messages=messages)


@bp.route('/message/mark_read',methods=['POST'])
@login_required
def mark_read():
    if request.method == 'POST':
        id = request.form.getlist('chk')
        if not id:
            flash('Nothing to update','danger')
            return redirect(url_for('admin_message.message'))
        for i in id:
            c = Message.query.filter_by(id=i).first()
            c.user_read = 1-c.user_read
            db.session.add(c)
        db.session.commit()
        flash('Update successful','success')
    return redirect(url_for('admin_message.message'))
