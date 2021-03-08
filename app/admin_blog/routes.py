from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required
from app import db
from app.admin_blog import bp
from app.admin_blog.models import Post, Tag, Tagged
from app.admin_blog.forms import PostForm
from app.admin_media.models import Images
from datetime import datetime
from slugify import slugify
from app.breadcrumb import set_breadcrumb


# ADMIN BLOG routes

@bp.route('/blog',methods=['GET'])
@login_required
@set_breadcrumb('home blog')
def blog():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.active.desc(), Post.create_date.desc()) \
    .paginate(page,current_app.config['PAGES_PER_PAGE'],False)

    return render_template('admin_blog/blog.html',posts=posts)


def processTags(tags_new,post):
    changed=False
    # get all current tags for post
    tags_current = post.getTagNames()
    # check if any tags should be deleted
    for tag in tags_current:
        if tag not in tags_new:
            # tag has been deleted, delete from Tagged table
            id = Tag.getTagId(tag)
            Tagged.query.filter_by(post_id=post.id,tag_id=id).delete()
            changed=True

    # is there tags to add?
    if not(len(tags_new) == 1 and tags_new[0] == ''):
        # if tag doesn't exist create it in Tags table
        for tag in tags_new:
            if Tag.getTagId(tag) == -1:
                t = Tag(name=tag)
                db.session.add(t)
                changed=True

        #check if any tags should be added
        for tag in tags_new:
            if tag not in tags_current:
                # tag is new, add to Tagged table
                id = Tag.getTagId(tag)
                t = Tagged(post_id=post.id, tag_id=id)
                db.session.add(t)
                changed=True
    # maybe better, just call commit once
    if changed:
        db.session.commit()


@bp.route('/post',methods=['GET','POST'])
@login_required
@set_breadcrumb('home blog post')
def post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        slug = slugify(title)
        if Post.getPostBySlug(slug) is None:
            post = Post(title=title,slug=slug,post=form.post.data,author=current_user)
            db.session.add(post)
            db.session.commit()

            # tags should be separated by commas (,) and start with hash (#)
            tags = form.tags.data
            tag_list = [t.strip() for t in tags.split(',')]
            processTags(tag_list,post)

            flash('Your post has been published','success')
        else:
            flash('Error post not created as title already exists in database','danger')
    return render_template('admin_blog/post.html',form=form)


@bp.route('/edit_post',methods=['GET','POST'])
@login_required
@set_breadcrumb('home blog edit-post')
def edit_post():
    id = request.args.get('id')
    if id:
        post = Post.query.filter_by(id=id).first()
        if not post:
            flash('Post not found','danger')
            return redirect(url_for('admin_blog.blog'))
    else:
        flash('id is missing','danger')
        return redirect(url_for('admin_blog.blog'))
    form = PostForm()
    return render_template('admin_blog/post.html',form=form,post=post)
'''
    if form.validate_on_submit():
        heading = form.heading.data
        slug = slugify(heading)
        # check if heading already exists
        check_post = Post.getPostBySlug(slug)
        if (check_post is not None):
            if (check_post.id != post.id):
                flash('Error post not created as title already exists in database.','danger')
                return redirect('/post_detail/' + old_slug)

        post.heading = heading
        post.slug = slug
        post.post = form.post.data
        post.update_date = datetime.utcnow()
        db.session.add(post)
        db.session.commit()

        # tags should be separated by commas (,) and start with hash (#)
        tags = form.tags.data
        tag_list = [t.strip() for t in tags.split(',')]
        processTags(tag_list,post)

        flash('Your post has been updated!','success')
        return redirect('/post_detail/' + slug)

    tags = post.getTagNamesStr()
    return render_template('post/edit_post.html',form=form,post=post,tags=tags)
'''

@bp.route('/del_post',methods=['POST'])
@login_required
def del_post():
    post_id = request.form.get('id')
    del_type = request.form.get('delType')
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('No such post exist','danger')
    elif del_type != 'soft' and del_type != 'hard':
        flash('Select option error','danger')
    else:
        tagged = Tagged.query.filter_by(post_id=post.id).all()
        for t in tagged:
            db.session.delete(t)
        if del_type == 'soft':
            post.active=False
            db.session.add(post)
            flash('The post has been soft deleted','success')
        elif del_type == 'hard':
            db.session.delete(post)
            flash('The post has been hard (permanently) deleted','success')
        db.session.commit()
        
    return redirect(url_for('admin_blog.blog'))
