from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(40), primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(50))
    admin = db.Column(db.Boolean)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    db.relationship('Class', backref = 'attendance')
    db.relationship('Student', backref = 'students')
    
class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key = True)
    day = db.Column(db.String(3), index=True)
    time = db.Column(db.Time)
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendance.id'))
    

class Student(db.Model):
    __tablename__ = 'students'
    nric = db.Column(db.String(10), primary_key = True)
    name = db.Column(db.String(30), index = True)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(1))
    date_join = db.Column(db.Date)
    last_payment = db.Column(db.Date)
    premium = db.Column(db.Boolean)
    extra_classes = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    highest_test = db.Column(db.Date)
    date_intermediate = db.Column(db.Date)
    date_premium = db.Column(db.Date)
    referred_by = db.Column(db.String(50))
    remarks = db.Column(db.String(80))
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendance.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
