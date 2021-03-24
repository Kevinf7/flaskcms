from flask import render_template, redirect, url_for, flash, g
from sqlalchemy import desc
from flask_login import current_user, login_required
from app import db
from app.admin_main import bp
from app.admin_blog.models import Post, Tag, Tagged, Comment
from app.admin_page.models import Page
from app.admin_media.models import Images, ImageType
from app.admin_message.models import Message
from app.breadcrumb import set_breadcrumb


# ADMIN MAIN routes

@bp.route('/')
@bp.route('/index')
@login_required
@set_breadcrumb('home')
def index():
    total_post = Post.query.filter_by(active=True).count()
    post_latest = Post.query.order_by(desc(Post.update_date)).limit(3).all()
    total_tags = db.session.query(Tag).count()
    top_tags = db.session.query(Tag, db.func.count(Tagged.tag_id)) \
        .join(Tagged).group_by(Tagged.tag_id).limit(3).all()
    total_comment = Comment.query.count()
    last_login = current_user.last_seen
    new_comment = Comment.query.filter(Comment.create_date>=last_login).count()
    total_pages = Page.query.count()
    page_latest = Page.query.order_by(desc(Page.last_publish_date)).first()
    total_media_blog = db.session.query(Images).join(ImageType).filter(ImageType.name=='blog').count()
    total_media_page = db.session.query(Images).join(ImageType).filter(ImageType.name=='page').count()
    total_message = Message.query.count()
    new_message = Message.query.filter(Message.create_date>=last_login).count()
    image_latest = Images.query.order_by(desc(Images.create_date)).limit(3).all()
    comment_latest = Comment.query.order_by(desc(Comment.create_date)).first()

    return render_template('admin_main/index.html', total_post=total_post, \
        total_tags=total_tags, total_comment=total_comment, \
        new_comment=new_comment, total_pages=total_pages, \
        total_media_blog=total_media_blog, total_media_page=total_media_page, \
        total_message=total_message, new_message=new_message, post_latest=post_latest, \
        page_latest=page_latest, top_tags=top_tags, image_latest=image_latest, \
        comment_latest=comment_latest)
    

@bp.route('/about', methods=['GET'])
@login_required
@set_breadcrumb('home about')
def about():
    return render_template('admin_main/about.html')


# Used by breadcrumbs
@bp.app_context_processor 
def inject_breadcrumb():
    breadcrumb = getattr(g, 'breadcrumb', '')
    return dict(breadcrumb=breadcrumb)


