from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from config import Config


db = SQLAlchemy()
# compare_type = true - this is so that flask migrate detect changes to columns like size
migrate = Migrate(compare_type=True)
moment = Moment()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        login_manager.init_app(app)
        migrate.init_app(app,db)
        moment.init_app(app)

        from app.admin_blog import bp as admin_blog_bp
        app.register_blueprint(admin_blog_bp, url_prefix='/admin')

        from app.admin_contact import bp as admin_contact_bp
        app.register_blueprint(admin_contact_bp, url_prefix='/admin')

        from app.admin_dashboard import bp as admin_dashboard_bp
        app.register_blueprint(admin_dashboard_bp, url_prefix='/admin')

        from app.email import bp as email_bp
        app.register_blueprint(email_bp)

        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)

        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

    return app
