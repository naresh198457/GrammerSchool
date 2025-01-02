from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired

import pandas as pd
from app.functions import same_letter_must_fit_into_both

class practiceform(FlaskForm):
    Desc1_text = StringField('Description of Common letter', render_kw={'readonly':True})
    submit_button_1 = SubmitField('Common Letter')
    Desc2_text = StringField('Description of Identify Next Number', render_kw={'readonly':True})
    submit_button_2 = SubmitField('Identify Next Number')
    Desc3_text = StringField('Description of Next Letter Pair', render_kw={'readonly':True})
    submit_button_3 = SubmitField('Next Letter Pair')

class commonletterquestionform(FlaskForm):
    options = RadioField('Options', choices=[], validators=[DataRequired()])
    submit = SubmitField('Next')

class findnextletterpairform(FlaskForm):
    options = RadioField('Options', choices=[], validators=[DataRequired()])
    submit = SubmitField('Next')