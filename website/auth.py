from ast import IsNot
from pickle import FALSE, TRUE
from flask import Blueprint, render_template, request, flash, redirect, url_for

from website.access_control import admin_access
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
import time
from . import db
from flask_login import login_user, login_required, logout_user, current_user


## UTWORZENIE BLUEPRINTA
auth = Blueprint('auth', __name__)

### URL ROUTING

## LOGIN PAGE
# input:
# - employee number
# - employee password
# Check if emp number and passwords requirements are fulfilled, if
# yes, login in user. When user provides false data that could not
# be found in database, error message flashes on login screen
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # DATA ACQUISITION
        empNumber = request.form.get('employee_nb')
        empPassword = request.form.get('password')

        # CHECKING INPUT REQUIREMENTS
        if len(empNumber) < 5:
            flash('Numer pracownika jest za krótki', category='error')
        elif len(empPassword) < 5:
            flash('Hasło jest za krótkie', category='error')
        else:
            # SEARCHING FOR AN USER WITH ROLE
            user = User.query.filter_by(empNb = empNumber).first()
            if user:
                if check_password_hash(user.password, empPassword):
                    # IF PASSWORD MATCHES, LOGIN IN USER
                    login_user(user, remember=True)
                    return redirect(url_for('views.success_login'))
                else:
                    # IF PASSWORD IS INVALID, FLASH ERROR MESSAGE
                    flash('Hasło jest niepoprawne!', category='error')
            else:
                # IF RECORD NOT FOUND IN DATABASE, FLASH ERROR MESSAGE
                flash('Nie ma takiego użytkownika!', category='error')

    # IF METHOD GET, RENDER TEMPLATE 'LOGIN'    
    return render_template('login.html', user = current_user)

## USER ADDING PAGE
# input:
# - emp number, name, password
# - admin checkbox
# To access this route, admin permission is needed. 
# Check if data requirements are fulfilled, if yes,
# add user to database
@auth.route('/signin', methods=['GET', 'POST'])
@login_required
@admin_access
def signin():
    if request.method == 'POST':
        # DATA ACQUISITION
        empNumber = request.form.get('employee_nb')
        empName = request.form.get('employee_name')
        empPassword1 = request.form.get('password')
        empPassword2 = request.form.get('password2')
        adminCheck = request.form.get('switch')

        # CHECKING INPUT REQUIREMENTS
        if len(empNumber) < 5:
            flash('Numer pracownika jest za krótki', category='error')
        elif len(empPassword1) < 5:
            flash('Hasło jest za krótkie', category='error')
        elif empPassword1 != empPassword2:
            flash('Hasła nie pokrywają się!', category='error')
        else:
            # CHECK IF USER IS ALREADY IN DATABASE
            users = User.query.filter_by(empNb = empNumber).first()
            
            # IF USER EXIST IN DATABASE, FLASH ERROR MESSAGE AND RENDER TEMPLATE AGAIN
            if users:
                flash('Użytkownik o takim numerze już istnieje!', category='error')
                return render_template('signin.html', user = current_user)

            # IF USER DO NOT EXIST IN DATABASE, CHECK ADMIN CHECKBOX STATUS, AND ADD USER WITH SELECTED ROLE
            if not users:
                if adminCheck == 'on':
                    new_user = User(empNb = empNumber, empName = empName, password = generate_password_hash(empPassword1, method='sha256'), role_id = 1)
                else :
                    new_user = User(empNb = empNumber, empName = empName, password = generate_password_hash(empPassword1, method='sha256'), role_id = 2)
                
                # COMMIT CHANGES TO DATABASE AND RENDER SUCCESS ROUTE
                db.session.add(new_user)
                db.session.commit()

                return redirect(url_for('views.success_create'))

    # IF METHOD GET, RENDER TEMPLATE 'SIGNIN' 
    return render_template('signin.html', user = current_user)

## USER LOGOUT PAGE
# To access this route, login permission is needed. 
# Logout current user
@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('success_logout.html')