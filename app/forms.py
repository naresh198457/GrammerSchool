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
    Desc4_text = StringField('Description of Arthematics', render_kw={'readonly':True})
    submit_button_4 = SubmitField('Arthematics')

class commonletterquestionform(FlaskForm):
    options = RadioField('Options', choices=[], validators=[DataRequired()])
    submit = SubmitField('Next')

class findnextletterpairform(FlaskForm):
    options = RadioField('Options', choices=[], validators=[DataRequired()])
    submit = SubmitField('Next')

class Arithmeticsform(FlaskForm):
    No_1_1s=StringField('Number 1 1 place',render_kw={'redaonly':True})
    No_1_10s=StringField('Number 1 10 place',render_kw={'redaonly':True})
    No_1_100s=StringField('Number 1 100 place',render_kw={'redaonly':True})
    No_2_1s=StringField('Number 2 1 place',render_kw={'redaonly':True})
    No_2_10s=StringField('Number 2 10 place',render_kw={'redaonly':True})
    No_2_100s=StringField('Number 2 100 place',render_kw={'redaonly':True})
    No_3_1s=StringField('Number 3 1 place',validators=[DataRequired()])
    No_3_10s=StringField('Number 3 10 place')
    No_3_100s=StringField('Number 3 100 place')
    Symbol=StringField('Number 1',render_kw={'readonly':True})
    Next_Button=SubmitField('Next')


class BTForm(FlaskForm):
    BT_Question=StringField('Question',render_kw={'readonly':True})
    BT_Answer=StringField('Answer',render_kw={'readonly':True})
    BT_Ans_Rev_Button=SubmitField('Answer')
    BT_Next=SubmitField('Next')