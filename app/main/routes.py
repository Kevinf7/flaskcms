from flask import render_template, current_app, request, flash, redirect, url_for
from flask_login import current_user
from app import db
from app.main import bp
from app.email import email
from app.admin_page.models import PageHomeMain, PageHomeHero, PageStatus, PageContact, PageHomeSplash
from app.admin_blog.models import Post, Tag, Tagged, Comment
from app.admin_message.models import Message
from sqlalchemy import desc
from datetime import datetime



def get_summary_posts(posts):
    for index, post in enumerate(posts.items):
        # split first occcurence of below string and keep everything on the left
        p = post.post.split('<!-- pagebreak -->',1)[0]
        posts.items[index].summary = p
    return posts


def get_num_comments(posts):
    for index, post in enumerate(posts.items):
        n = post.query.join(Comment).filter(post.id==Comment.post_id).count()
        posts.items[index].num_comments = n
    return posts


@bp.route('/')
@bp.route('/index')
def index():
    main = PageHomeMain.query.filter_by(page_status=PageStatus.getStatus('published')).first()
    hero = PageHomeHero.query.filter_by(page_status=PageStatus.getStatus('published')).first()
    top_post = Post.query.order_by(desc(Post.create_date)).limit(3).all()
    contact = PageContact.query.filter_by(page_status=PageStatus.getStatus('published')).first()
    splash = PageHomeSplash.query.filter_by(page_status=PageStatus.getStatus('published')).first()
    return render_template('main/index.html', 
        main=main, hero=hero, top_post=top_post, contact=contact, splash=splash)


@bp.route('/blog', methods=['GET'])
def blog():
    top_post = Post.query.order_by(desc(Post.create_date)).limit(3).all()
    tags = db.session.query(Tag, db.func.count(Tagged.tag_id)) \
        .join(Tagged).group_by(Tagged.tag_id) \
        .order_by(desc(db.func.count(Tagged.tag_id))).all()
    page = request.args.get('page',1,type=int)
    tag_name = request.args.get('tag')
    tag_id = Tag.getTagId(tag_name)
    if tag_id == -1:
        posts = Post.query.filter_by(active=True) \
            .order_by(Post.active.desc(),Post.create_date.desc()) \
            .paginate(page,current_app.config['USER_POSTS_PER_PAGE'],False)
    else:
        posts = Post.query.filter(Post.active==True,Post.tags.any(tag_id=tag_id)) \
            .order_by(Post.active.desc(),Post.create_date.desc()) \
            .paginate(page,current_app.config['USER_POSTS_PER_PAGE'],False)
            
    posts = get_summary_posts(posts)
    posts = get_num_comments(posts)
    contact = PageContact.query.filter_by(page_status=PageStatus.getStatus('published')).first()
    return render_template('main/blog.html', posts=posts, tags=tags, top_post=top_post, tag_name=tag_name, contact=contact)


@bp.route('/blog_single/<slug>')
def blog_single(slug):
    post = Post.getPostBySlug(slug)
    if post is None:
        flash('No such post exists.','danger')
        return redirect(url_for('main.blog'))
    top_post = Post.query.order_by(desc(Post.create_date)).limit(3).all()
    tags = db.session.query(Tag, db.func.count(Tagged.tag_id)) \
        .join(Tagged).group_by(Tagged.tag_id) \
        .order_by(desc(db.func.count(Tagged.tag_id))).all()
    n = Post.query.join(Comment).filter(post.id==Comment.post_id).count()
    post.num_comments = n
    contact = PageContact.query.filter_by(page_status=PageStatus.getStatus('published')).first()
    return render_template('main/blog-single.html', post=post, tags=tags, top_post=top_post, contact=contact)


@bp.route('/add_comment',methods=['POST'])
def add_comment():
    anchor=''
    slug = request.form.get('slug')
    post = Post.getPostBySlug(slug)
    if post is None:
        flash('No such post exists.','danger')
        return redirect(url_for('main.blog'))
    comment = request.form.get('comment')
    admin = request.form.get('admin')
    if admin == 'yes':
        if current_user:
            cmt = Comment(comment=comment,post=post,user=current_user, \
                create_date=datetime.utcnow())
            db.session.add(cmt)
            db.session.commit()
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        if not name or name=='' or not email or email=='':
            flash('Name and Email are mandatory fields','danger')
            anchor='comment_form'
        else:
            cmt = Comment(comment=comment,post=post,name=name, \
                email=email,create_date=datetime.utcnow())
            db.session.add(cmt)
            db.session.commit()
            anchor='comment_top'
    return redirect(url_for('main.blog_single',slug=slug,_anchor=anchor))


@bp.route('/contact', methods=['GET'])
def contact():
    contact = PageContact.query.filter_by(page_status=PageStatus.getStatus('published')).first()
    return render_template('main/contact.html',contact=contact)


@bp.route('/new_message', methods=['POST'])
def new_message():
    recaptcha = request.form.get('g-recaptcha-response')
    if recaptcha:
        msg = Message(name=request.form.get('name'), \
            email=request.form.get('email'), message=request.form.get('message'))
        db.session.add(msg)
        db.session.commit()

        create_date = msg.create_date.strftime('%d/%m/%y %H:%M')
        result = email.send_email('Someone has commented on flaskcms',
            sender=current_app.config['MAIL_FROM'],
            recipients=current_app.config['MAIL_ADMINS'],
            text_body=render_template('main/email_contact.txt',
                                        msg=msg, create_date=create_date),
            html_body=render_template('main/email_contact.html',
                                        msg=msg, create_date=create_date))
        if result:
            flash('Message has been sent', 'success')
        else:
            flash('System error', 'danger')
    else:
        flash('You need to check Recaptcha', 'danger')
    return redirect(url_for('main.contact',_anchor='contact_form'))


