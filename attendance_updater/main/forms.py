from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, DateField, BooleanField, SelectField, SelectMultipleField
from wtforms_components import TimeField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, Optional
from wtforms import ValidationError
from ..util.validators import Unique
from ..models import Student

class SubmitForm(FlaskForm):
    name = StringField("Student's name", validators=[Required()])
    nric = StringField(validators=[Required(),Length(min=9, max=9),
                       Unique(Student, Student.nric, message=
                              'user')])
    age = StringField(validators=[Required(), Length(min=1, max=2)])
    sex = RadioField(choices = [('M','Male'),('F','Female')])
    date_join = DateField('Start Date (DD/MM/YYYY)', format='%d/%m/%Y')
    status = BooleanField("Intermediate User?")
    high_test = StringField("Highest intermediate qualification")
    premium = BooleanField("Premium user?")
    referred_by = StringField("Referred by which other student?")
    remarks = StringField("Additional comments")
    day = StringField("Class on which day? (MON, THU, SUN, etc)" \
                      , validators=[Required(), Length(min=3,max=3)])
    time = TimeField("What time is his lesson? \
                     (e.g 08:00 ,17:00, 16:00)", format='%H:%M',
                      validators=[Required()])
    submit = SubmitField('Add student')

class ClassSelectForm(FlaskForm):
    classes = SelectField('Choose a class', coerce = int, choices = [])
    submit = SubmitField('Obtain class')

class AttendanceForm(FlaskForm):
    students = SelectMultipleField('Mark their attendance (unmark if not here)',
                                   choices = [])
    submit = SubmitField('Mark attendance!')
