from flask import render_template, redirect, request, current_app, url_for, flash
from flask_login import login_required
from app import db
from app.admin_contact import bp
from app.admin_contact.models import Contact


# ADMIN CONTACT routes 

@bp.route('/contact',methods=['GET','POST'])
@login_required
def contact():
    page = request.args.get('page',1,type=int)
    contacts = Contact.query.order_by(Contact.user_read.asc(), Contact.create_date.desc()) \
    .paginate(page,current_app.config['MESSAGES_PER_PAGE'],False)

    return render_template('admin_contact/contact.html',contacts=contacts)


@bp.route('/contact/mark_read',methods=['POST'])
@login_required
def mark_read():
    if request.method == 'POST':
        id = request.form.getlist('chk')
        for i in id:
            c = Contact.query.filter_by(id=i).first()
            c.user_read = 1-c.user_read
            db.session.add(c)
        db.session.commit()
        flash('Update successful','success')
    return redirect(url_for('admin_contact.contact'))
