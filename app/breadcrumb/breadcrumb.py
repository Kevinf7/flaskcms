
from flask import url_for, request, g
from functools import wraps


class Breadcrumb(object):
    map=[]
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        with app.app_context():
            Breadcrumb.map.append({'key': 'home', 'name': 'Home', 
                'url': url_for('admin_main.index'), 'icon': '<i class="fas fa-home"></i>'})
            Breadcrumb.map.append({'key': 'blog', 'name': 'Blog', 
                'url': url_for('admin_blog.blog'), 'icon': ''})
            Breadcrumb.map.append({'key': 'post', 'name': 'Create Post', 
                'url': url_for('admin_blog.post'), 'icon': ''})
            Breadcrumb.map.append({'key': 'edit-post', 'name': 'Edit Post', 
                'url': url_for('admin_blog.edit_post'), 'icon': '', 'has-arg': True})
            Breadcrumb.map.append({'key': 'tag', 'name': 'Tags', 
                'url': url_for('admin_blog.tag'), 'icon': ''})
            Breadcrumb.map.append({'key': 'media', 'name': 'Media', 
                'url': url_for('admin_media.media'), 'icon': '', 'has-arg': True})
            Breadcrumb.map.append({'key': 'message', 'name': 'Messages', 
                'url': url_for('admin_message.message'), 'icon': ''})
            Breadcrumb.map.append({'key': 'about', 'name': 'About Flask CMS', 
                'url': url_for('admin_main.about'), 'icon': ''})
            Breadcrumb.map.append({'key': 'comment', 'name': 'Comments', 
                'url': url_for('admin_blog.comment'), 'icon': ''})
            Breadcrumb.map.append({'key': 'page', 'name': 'Pages', 
                'url': url_for('admin_page.page'), 'icon': ''})
            Breadcrumb.map.append({'key': 'store', 'name': 'Store', 
                'url': url_for('admin_store.store'), 'icon': ''})
            Breadcrumb.map.append({'key': 'product', 'name': 'Product', 
                'url': url_for('admin_store.product'), 'icon': ''})
            Breadcrumb.map.append({'key': 'page-contact', 'name': 'Contact', 
                'url': url_for('admin_page.page_contact'), 'icon': ''})
            Breadcrumb.map.append({'key': 'page-home-main', 'name': 'Home-Main', 
                'url': url_for('admin_page.page_home_main'), 'icon': ''})
            Breadcrumb.map.append({'key': 'page-home-hero', 'name': 'Home-Hero', 
                'url': url_for('admin_page.page_home_hero'), 'icon': ''})
            Breadcrumb.map.append({'key': 'page-home-splash', 'name': 'Home-Splash', 
                'url': url_for('admin_page.page_home_splash'), 'icon': ''})
            Breadcrumb.map.append({'key': 'site-setting', 'name': 'Site Settings', 
                'url': url_for('admin_main.site_setting'), 'icon': ''})


def set_breadcrumb(path):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            breadcrumb = []
            key = path.split()
            for k in key:
                for b in Breadcrumb.map:
                    if k == b['key']:
                        new_b = b.copy()
                        if 'has-arg' in b:
                            if b['has-arg']:
                                r = request.query_string
                                if r:
                                    r = r.decode('utf-8')
                                    new_b['url'] = new_b['url'] + '?' + r
                        breadcrumb.append(new_b)
            setattr(g, 'breadcrumb', breadcrumb)
            return f(*args, **kwargs)
        return wrapper
    return decorator
