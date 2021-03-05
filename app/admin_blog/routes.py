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
    posts = Post.query.order_by(Post.create_date.asc()) \
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

'''
# add a new post
@bp.route('/add_post/',methods=['GET','POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        heading = form.heading.data
        slug = slugify(heading)
        if Post.getPostBySlug(slug) is None:
            # write post to db
            post = Post(heading=heading,slug=slug,post=form.post.data,author=current_user)
            db.session.add(post)
            db.session.commit()

            # tags should be separated by commas (,) and start with hash (#)
            tags = form.tags.data
            tag_list = [t.strip() for t in tags.split(',')]
            processTags(tag_list,post)

            flash('Your post has been published!','success')
            return redirect(url_for('main.index'))
        flash('Error post not created as title already exists in database.','danger')
        return redirect(url_for('main.index'))
    return render_template('post/add_post.html',form=form)

# edit an existing post which you posted
@bp.route('/edit_post/<slug>',methods=['GET','POST'])
@login_required
def edit_post(slug):
    old_slug = slug
    post = Post.getPostBySlug(slug)
    # slug is wrong
    if post is None:
        flash('No such post exists.','danger')
        return redirect(url_for('index'))
    # users's cannot edit other user's post, not needed in this blog but there anyways
    if post.author.id != current_user.id:
        flash("You are not authorised to edit someone else's post",'danger')
        return redirect(url_for('main.index'))

    form = PostForm()
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

# delete an existing post - only admin can perform
@bp.route('/del_post/<slug>',methods=['GET','POST'])
@login_required
def del_post(slug):
    post = Post.getPostBySlug(slug)
    # slug is wrong
    if post is None:
        flash('No such post exists.','danger')
        return redirect(url_for('index'))
    # only admin can delete post
    if not current_user.is_admin():
        flash('You do not have permission to perform this function','danger')
        return redirect(url_for('main.index'))

    # user confirms he wants to delete
    if request.method == 'POST':
        #we want to do a soft delete only
        post.current=False
        db.session.add(post)
        #also delete all the tag links associated to this post
        tagged = Tagged.query.filter_by(post_id=post.id).all()
        for t in tagged:
            db.session.delete(t)
        db.session.commit()
        flash('The post has been deleted','danger')
        return redirect(url_for('main.index'))
    tags = post.getTagNamesStr()
    return render_template('post/del_post.html',post=post,tags=tags)
'''