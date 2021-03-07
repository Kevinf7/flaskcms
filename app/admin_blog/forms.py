from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, Optional

# ADMIN BLOG forms

class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    post = TextAreaField('Write something')
    tags = StringField('Tags')
    submit = SubmitField('Submit')

# Two forms for commeting, one if user is not logged in
class CommentFormAnon(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email', validators=[Length(max=50), Email()])
    comment = TextAreaField('Comment', validators=[InputRequired(), Length(max=1000)])
    submit = SubmitField('Submit')
    recaptcha = RecaptchaField()




