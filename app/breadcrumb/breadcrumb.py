
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
            Breadcrumb.map.append({'key': 'page', 'name': 'Pages', 
                'url': url_for('admin_page.page'), 'icon': ''})
            Breadcrumb.map.append({'key': 'page-contact', 'name': 'Contact Us', 
                'url': url_for('admin_page.page_contact'), 'icon': ''})
            Breadcrumb.map.append({'key': 'media-page', 'name': 'Media', 
                'url': url_for('admin_media.media'), 'icon': ''})
            Breadcrumb.map.append({'key': 'media-blog', 'name': 'Media', 
                'url': url_for('admin_media.media'), 'icon': ''})
            Breadcrumb.map.append({'key': 'message', 'name': 'Messages', 
                'url': url_for('admin_message.message'), 'icon': ''})    


def set_breadcrumb(path):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            breadcrumb = []
            key = path.split()
            for k in key:
                for b in Breadcrumb.map:
                    if k == b['key']:
                        breadcrumb.append(b)
            setattr(g, 'breadcrumb', breadcrumb)
            return f(*args, **kwargs)
        return wrapper
    return decorator
