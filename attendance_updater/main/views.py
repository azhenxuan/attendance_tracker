from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dateselection')
def dateselection():
	return render_template('dateselection.html')
	
@main.route('/markattendance')
def mark():
	return render_template('mark.html')
	
@main.route('/addnew')
def addnew():
	return render_template('addnew.html')