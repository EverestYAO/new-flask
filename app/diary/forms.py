from flask_wtf import Form
from wtforms import StringField, SubmitField,TextAreaField
from wtforms import ValidationError
from wtforms.validators import Required

class DiaryForm(Form):
    title = StringField('title')
    body = TextAreaField("What's on your mind?", validators=[Required()])
    src = StringField("pics link?", validators=[Required()])
    submit = SubmitField('Submit')
