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

==

Contact

INSERT INTO contact(name,email,message,user_read,create_date)
VALUES("John Smith", "john.smith@abc.com", "Hello how are you?", false, now());

INSERT INTO contact(name,email,message,user_read,create_date)
VALUES("Amy Burr", "amy.burr@abc.com", "What a great website. Well done!", false, now());

INSERT INTO contact(name,email,message,user_read,create_date)
VALUES("Troy Trojan", "troy@aabb.com", "Please help", false, now());

==

Page

insert into page (name, update_by, update_date, create_date)
values ('Home', 'kevin_foong@yahoo.com', now(), now());

insert into page (name, update_by, update_date, create_date)
values ('Contact Us', 'kevin_foong@yahoo.com', now(), now());

INSERT into page_contact (content, page_id, update_by, update_date, create_date)
VALUES ("Drop me a line! Either fill in the form below or send me an email. I will get back to you shortly.", 2, "kevin_foong@yahoo.com", now(), now());

INSERT into page_contact (content, page_id, update_by, update_date, create_date)
VALUES ("Drop me a line! Either fill in the form below or send me an <a href='abc'>email</a>. I will get back to you shortly. Thanks!", 2, "kevin_foong@yahoo.com", now(), now());

INSERT into page_contact_curr (page_contact_id)
VALUES (1);

