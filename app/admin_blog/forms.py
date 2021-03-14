from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import InputRequired, Email, Length


# ADMIN BLOG forms

class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    post = TextAreaField('Write something')
    tags = HiddenField('Tags')
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email', validators=[Length(max=50), Email()])
    comment = TextAreaField('Comment', validators=[InputRequired(), Length(max=1000)])
    submit = SubmitField('Submit')
    recaptcha = RecaptchaField()




