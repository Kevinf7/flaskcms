INSERT INTO role (name)
VALUES ('admin'),('user');

from app.admin_dashboard.models import User
from app import db
from datetime import datetime
now = datetime.now()
u = User(email="kevin_foong@yahoo.com", firstname="Kevin", lastname="Foong", password_hash="123", role_id=1, last_seen=now, create_date=now)
u.set_password('abc')
db.session.add(u)
db.session.commit()