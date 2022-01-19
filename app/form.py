from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class PhonebookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')
