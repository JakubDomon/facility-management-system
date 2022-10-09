from ast import IsNot
from pickle import FALSE, TRUE
from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy import null
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
import time
from . import db

## UTWORZENIE BLUEPRINTA
auth = Blueprint('auth', __name__)

## URL ROUTING
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        empNumber = request.form.get('employee_nb')
        empPassword = request.form.get('password')

        print('dupa')

        if len(empNumber) < 5:
            flash('Numer pracownika jest za krótki', category='error')
        elif len(empPassword) < 5:
            flash('Hasło jest za krótkie', category='error')
        else:
            # SEARCHING FOR AN USER WITH ROLE
            user = User.query.filter_by(empNb = empNumber).first()
            if user:
                if check_password_hash(user.password, empPassword):
                    print('Logged IN')
                    return redirect(url_for('views.manage'))
                else:
                    print('Niepoprawne hasło')
            else:
                print("Nie ma takiego użytkownika")
            
    return render_template('login.html')

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        empNumber = request.form.get('employee_nb')
        empPassword1 = request.form.get('password')
        empPassword2 = request.form.get('password2')
        adminCheck = request.form.get('switch')

        if len(empNumber) < 5:
            flash('Numer pracownika jest za krótki', category='error')
        elif len(empPassword1) < 5 or len(empPassword2) < 5:
            flash('Hasło jest za krótkie', category='error')
        elif empPassword1 != empPassword2:
            flash('Hasła nie pokrywają się!', category='error')
        else:
            # USER CREATION
            print(adminCheck)

            if adminCheck == 'on':
                new_user = User(empNb = empNumber, password = generate_password_hash(empPassword1, method='sha256'), isAdmin = 1)
            else :
                new_user = User(empNb = empNumber, password = generate_password_hash(empPassword1, method='sha256'), isAdmin = 0)
            
            db.session.add(new_user)
            db.session.commit()
            flash('Pomyślnie utworzono nowe konto pracownika', category='success')
            return redirect(url_for('views.home'))


    
    return render_template('signin.html')