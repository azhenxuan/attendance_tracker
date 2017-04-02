from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from . import main
from .. import db
from .forms import SubmitForm, ClassSelectForm, AttendanceForm
from ..models import Student, Class, Attendance
import datetime, calendar

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/classselection', methods=['GET', 'POST'])
@login_required
def classselection():
    if current_user.is_authenticated:
        classes = [(c.id ,toString(c.day, c.time)) for c in Class.query.order_by(Class.time)]
        form = ClassSelectForm()
        form.classes.choices = classes
        if form.validate_on_submit():
            today_date = datetime.date.today()
            which_day = calendar.day_name[today_date.weekday()][:3].upper()
            if which_day == Class.query.filter(Class.id == form.classes.data).first().day:
                return redirect(url_for('.mark', classID = form.classes.data))
            else:
                flash("This class' not today!")
        return render_template('classselection.html', form = form)
    return redirect(url_for('auth.login'))

def toString(day, time):
    if day == "MON":
        day = "Monday"
    elif day == "TUE":
        day = "Tuesday"
    elif day == "WED":
        day = "Wednesday"
    elif day == "THU":
        day = "Thursday"
    elif day == "FRI":
        day = "Friday"
    elif day == "SAT":
        day = "Saturday"
    elif day == "SUN":
        day = "Sunday"
    else:
        print("error with day, raise it up to zx")
    
    if int(str(time)[:2]) > 12:
        time = str(int(str(time)[:2]) - 12) + "PM"
    else:
        time = str(int(str(time)[:2])) + "AM"
    return day + ", " + time
	
@main.route('/mark/<int:classID>', methods=['GET', 'POST'])
@login_required
def mark(classID):
    if current_user.is_authenticated:
        students = Student.query.filter(Student.class_id == classID).all()
        form = AttendanceForm()
        form.students.choices = [(student.nric, student.name) for student in students]
        week_class = retrieveAttendanceCurrentWeek(classID)
        form.students.data = [attendance.student_nric for attendance in week_class]
        if form.validate_on_submit():
            today_date = datetime.date.today()
            for student_nric in form.students.data:
                attendance = Attendance(date = today_date,
                                        class_id = classID,
                                        student_nric = student_nric)
                db.session.add(attendance)
            flash("The students' attendance has been taken")
        return render_template('mark.html', form = form)
    return redirect(url_for('auth.login'))

def retrieveAttendanceCurrentWeek(classID):
    today_date = datetime.date.today()
    week_ago = [(today_date - datetime.timedelta(days = i)) for i in range(7)]
    week_class = Attendance.query.filter(Attendance.class_id == classID).filter(Attendance.date.in_(week_ago)).all()
    return week_class

	
@main.route('/addnew', methods=['GET', 'POST'])
@login_required
def addnew():
    if current_user.is_authenticated:
        form = SubmitForm()
        if form.validate_on_submit():
            if Class.query.filter((Class.time == form.time.data)
                                & (Class.day == form.day.data)).first() == None:
                newclass = Class(day = form.day.data,
                                 time = form.time.data)
                db.session.add(newclass)
            class_id = Class.query.filter((Class.time == form.time.data)
                                    & (Class.day == form.day.data)).first().id
            student = Student(nric=form.nric.data,
                            name = form.name.data,
                            age = form.age.data,
                            sex = form.sex.data,
                            date_join = form.date_join.data,
                            status = form.status.data,
                            highest_test = form.high_test.data,
                            premium = form.premium.data,
                            referred_by = form.referred_by.data,
                            remarks = form.remarks.data,
                            class_id = class_id)
            db.session.add(student)
            flash('The student has been registered')
        return render_template('addnew.html', form=form)
    return redirect(url_for('auth.login'))
