from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from app.models import User
from pandas import read_csv

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    firstname=StringField('First Name',
                          validators=[DataRequired()])
    lastname=StringField('Last Name',
                          validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # validation 
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different username. ')


class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class contactForm(FlaskForm):
    Name=StringField('Name',validators=[DataRequired(message ="Please enter your name.")])
    Email=StringField('Email',validators=[DataRequired(message = "Please enter your email address"),Email()])
    Subject=StringField('Subject',validators = [DataRequired(message = "Please enter a subject.")])
    Message=TextAreaField('Message',validators=[DataRequired(message = "Please enter a message.")])
    CF_Submit_Button=SubmitField('Send')