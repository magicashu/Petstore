from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField,RadioField, SubmitField,IntegerField, BooleanField,DecimalField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    sex = RadioField('Gender', choices = [('M','Male'),('F','Female')], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(),Length( max=2)])#no auto increment 
    whatsApp = IntegerField('WhatsApp', validators=[DataRequired(),Length(min=10, max=13)])#direct link to whatsapp
    breed = StringField('Breed Name',validators=[])
    price = DecimalField('Price', validators=[DataRequired ()])
    description =  TextAreaField('Description',validators=[DataRequired()])
    submit = SubmitField('Post')