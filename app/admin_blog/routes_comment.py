from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from app import db
from app.admin_blog import bp
from app.admin_blog.models import Comment
from app.breadcrumb import set_breadcrumb


# ADMIN BLOG COMMENT routes

@bp.route('/comment',methods=['GET'])
@login_required
@set_breadcrumb('home blog comment')
def comment():
    page = request.args.get('page',1,type=int)
    comments = Comment.query.order_by(Comment.create_date.desc()) \
    .paginate(page,current_app.config['COMMENTS_PER_PAGE'],False)

    return render_template('admin_blog/comment.html',comments=comments)


@bp.route('/del_comment',methods=['POST'])
@login_required
def del_comment():
    comment_id = request.form.get('id')
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment is None:
        flash('No such comment','danger')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('The comment has been deleted','success')
    return redirect(url_for('admin_blog.comment'))


