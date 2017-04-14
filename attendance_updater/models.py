from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(40), unique=True, nullable = False)
    username = db.Column(db.String(20), nullable = False, index=True)
    password_hash = db.Column(db.String(100), nullable = False)

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
    id = db.Column(db.Integer, primary_key=True, )
    date = db.Column(db.Date)
    student_nric = db.Column(db.String(9), db.ForeignKey('students.nric'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    
class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(3), index=True)
    time = db.Column(db.Time)
    db.relationship('Attendance', backref = 'classes')
    db.relationship('Student', backref = 'classes')
    
class Student(db.Model):
    __tablename__ = 'students'
    nric = db.Column(db.String(10), primary_key = True, index = True)
    name = db.Column(db.String(30), index = True)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(1))
    date_join = db.Column(db.Date)
    last_payment = db.Column(db.Date)
    premium = db.Column(db.Boolean)
    extra_classes = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    highest_test = db.Column(db.String)
    date_intermediate = db.Column(db.Date)
    date_premium = db.Column(db.Date)
    referred_by = db.Column(db.String(50))
    remarks = db.Column(db.String(80))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    db.relationship('Attendance', backref = 'students')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
