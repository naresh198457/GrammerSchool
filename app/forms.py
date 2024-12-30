from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from app.models import User
import pandas as pd
from app.functions import same_letter_must_fit_into_both

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


class practiceform(FlaskForm):
    Desc1_text = StringField('Description of Common letter', render_kw={'readonly':True})
    submit_button_1 = SubmitField('Common Letter')
    Desc2_text = StringField('Description of Identify Next Number', render_kw={'readonly':True})
    submit_button_2 = SubmitField('Identify Next Number')
    Desc3_text = StringField('Description of Next Letter Pair', render_kw={'readonly':True})
    submit_button_3 = SubmitField('Next Letter Pair')


# # FlaskForm for Questions
# df = same_letter_must_fit_into_both(7)
# class commonletterform(FlaskForm):
    
#     questions = []
#     for index, row in df.iterrows():
#         field = RadioField(
#             #row["Question"],
#             'label',
#             choices=[
#                 ("option_a", row["option_a"]),
#                 ("option_b", row["option_b"]),
#                 ("option_c", row["option_c"]),
#                 ("option_d", row["option_d"]),
#                 ("option_e", row["option_e"]),
#             ],
#             default=None
#         )
#         questions.append(field)
#     submit = SubmitField('Submit')

class commonletterquestionform(FlaskForm):
    options = RadioField('Options', choices=[], validators=[DataRequired()])
    submit = SubmitField('Next')